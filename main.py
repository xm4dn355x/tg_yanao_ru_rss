# -*- coding: utf-8 -*-
########################################################################
#                                                                      #
# Телеграм бот для сбора RSS-ленты сайта yanao.ru, который репостит    #
# новости в телеграм канал.                                            #
#                                                                      #
# MIT License                                                          #
# Copyright (c) 2021 Michael Nikitenko                                 #
#                                                                      #
########################################################################

from time import sleep
from datetime import datetime

from requests.exceptions import ConnectionError
from urllib.error import URLError

from bot_engine import post_in_channel
from db_engine import insert_data_in_db
from rss_parser import find_new_posts, ParsingTimeoutError


def update_tg_channel():
    """Парсит RSS ленту, сверяет данные с базой и обновляет телеграм канал"""
    print(f'{datetime.now()} updating telegram channel')
    try:
        new_posts = find_new_posts()
        for post in new_posts:
            print(post)
            post_in_channel(post)
            insert_data_in_db(post)
            sleep(2)
    except ConnectionError:
        print(f'{datetime.now()} News Connection error')
    except URLError:
        print(f'{datetime.now()} RSS connection error')
    except AttributeError:
        print(f'{datetime.now()} IMG not loaded')
        raise AttributeError
    except TimeoutError:
        print(f'{datetime.now()} Parsing timeout')
    except ParsingTimeoutError:
        print(f'{datetime.now()} Custom Parsing Timeout Error')


def update_channel_loop():
    """Бесконечный цикл обновляющий канал раз в 5 минут"""
    while True:
        update_tg_channel()
        sleep(300)


if __name__ == '__main__':
    print('TG Bot yanao.ru RSS feed parser ')
    update_channel_loop()
