# -*- coding: utf-8 -*-
########################################################################
#                                                                      #
# Парсер ленты RSS                                                     #
#                                                                      #
# MIT License                                                          #
# Copyright (c) 2021 Michael Nikitenko                                 #
#                                                                      #
########################################################################


from datetime import datetime

import feedparser
import requests
from bs4 import BeautifulSoup

from db_engine import get_all_rows


RSS_URL = 'https://www.yanao.ru/presscenter/news/rss/'


def get_rss_feed_data(rss_url: str) -> list:
    """Получает RSS ленту, парсит её и возвращает данные постов"""
    print('get RSS feed data')
    start = datetime.now()
    rss_feed = feedparser.parse(rss_url)
    entries = reversed(rss_feed.entries)
    res = []
    for entrie in entries:
        title = entrie.title
        url = entrie.link
        try:
            img = 'https://yanao.ru' + entrie.turbo_content.split('img src="')[1].split('"')[0]
        except IndexError:
            html = requests.get(url=url).text
            soup = BeautifulSoup(html, 'lxml')
            img = 'https://yanao.ru' + soup.find('div', class_='region__centered-block m-b-32').find('img').get('src')
        data = {
            'title': title,
            'url': url,
            'img': img
        }
        res.append(data)
    print(f'RSS feed parsed in {(datetime.now() - start).seconds} seconds')
    return res


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
