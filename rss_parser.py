# -*- coding: utf-8 -*-
########################################################################
#                                                                      #
# Парсер ленты RSS                                                     #
#                                                                      #
# MIT License                                                          #
# Copyright (c) 2021 Michael Nikitenko                                 #
#                                                                      #
########################################################################


import functools
from datetime import datetime
from time import sleep
from threading import Thread

import feedparser
import requests
from bs4 import BeautifulSoup

from db_engine import get_all_rows


RSS_URL = 'https://www.yanao.ru/presscenter/news/rss/'


class ParsingTimeoutError(Exception):
    """Класс для Exception который вылетает при таймауте"""
    pass


def timeout(seconds: int):
    """Декоратор для обработки таймаутов. Принимает количество секунд для таймаута"""
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [ParsingTimeoutError('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, seconds))]

            def new_func():
                try:
                    res[0] = func(*args, **kwargs)
                except ParsingTimeoutError as e:
                    res[0] = e
            t = Thread(target=new_func)
            t.daemon = True
            try:
                t.start()
                t.join(seconds)
            except Exception as je:
                print('error starting thread')
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return deco


def get_rss_feed_data(rss_url: str) -> list:
    """Получает RSS ленту, парсит её и возвращает данные постов"""
    print(f'{datetime.now()} get RSS feed data')
    start = datetime.now()
    rss_feed = feedparser.parse(rss_url)
    entries = reversed(rss_feed.entries)
    res = []
    for entry in entries:
        title = entry.title
        url = entry.link
        try:
            img = 'https://yanao.ru' + entry.turbo_content.split('img src="')[1].split('"')[0]
        except IndexError:
            html = requests.get(url=url).text
            soup = BeautifulSoup(html, 'lxml')
            img = 'https://yanao.ru' + soup.find('div', class_='region__centered-block m-b-32').find('img').get('src')
            sleep(1)
        res.append({'title': title, 'url': url, 'img': img})
    print(f'RSS feed parsed in {(datetime.now() - start).seconds} seconds')
    return res


@timeout(seconds=120)
def find_new_posts() -> list:
    """Парсит RSS, сравнивает данные с базой и возвращает список неопубликованных постов"""
    rss_data = get_rss_feed_data(RSS_URL)
    db_data = get_all_rows()
    res = []
    for rss in rss_data:
        need_to_post = True
        for db in db_data:
            if rss['url'] == db['url']:
                need_to_post = False
        if need_to_post:
            res.append(rss)
    return res


if __name__ == '__main__':
    print('RSS parser')
    new_posts = find_new_posts()
    for data in new_posts:
        print(data)
