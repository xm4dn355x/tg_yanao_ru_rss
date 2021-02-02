# -*- coding: utf-8 -*-
########################################################################
#                                                                      #
# Модуль для работы с БД                                               #
#                                                                      #
# MIT License                                                          #
# Copyright (c) 2021 Michael Nikitenko                                 #
#                                                                      #
########################################################################


from time import sleep

import psycopg2
from psycopg2.extras import DictCursor

from bot_config import DB_NAME, DB_USER, DB_PASS, DB_HOST

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cursor = conn.cursor(cursor_factory=DictCursor)


def get_all_rows() -> psycopg2:
    """Возвращает все строки из БД"""
    cursor.execute('SELECT url FROM news')
    res = cursor.fetchall()
    return res


def insert_data_in_db(data: dict) -> bool:
    """Вставляет строку в базу и возвращает bool с результатом выполнения"""
    query = f"INSERT INTO news (title, url, img) VALUES ('{data['title']}', '{data['url']}', '{data['img']}')"
    cursor.execute(query)
    conn.commit()
    return True


if __name__ == '__main__':
    print('DB Engine')
    rows = get_all_rows()
    for row in rows:
        print(row)
    status = insert_data_in_db({
        'title': 'some title',
        'url': 'some url',
        'img': 'some img'
    })
    print(status)
    conn.close()
    sleep(30)
