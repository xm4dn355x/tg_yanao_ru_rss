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

from bot_engine import post_in_channel
from db_engine import insert_data_in_db
from rss_parser import find_new_posts


def update_tg_channel():
    """Парсит RSS ленту, сверяет данные с базой и обновляет телеграм канал"""
    print('updating telegram channel')
    new_posts = find_new_posts()
    for post in new_posts:
        print(post)
        post_in_channel(post)
        insert_data_in_db(post)
        sleep(2)


def update_channel_loop():
    """Бесконечный цикл обновляющий канал раз в 5 минут"""
    while True:
        update_tg_channel()
        sleep(300)


if __name__ == '__main__':
    print('TG Bot yanao.ru RSS feed parser ')
    update_channel_loop()
