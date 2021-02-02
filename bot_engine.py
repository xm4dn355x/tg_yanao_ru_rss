# -*- coding: utf-8 -*-
########################################################################
#                                                                      #
#                                                                      #
#                                                                      #
# MIT License                                                          #
# Copyright (c) 2021 Michael Nikitenko                                 #
#                                                                      #
########################################################################

from telegram import Bot
from telegram.ext import Updater
from telegram.utils.request import Request

from bot_config import ADMIN_ID, CHAT_ID, TOKEN
req = Request(connect_timeout=3)
bot = Bot(request=req, token=TOKEN)
updater = Updater(bot=bot, use_context=True)
dispatcher = updater.dispatcher


def log_error(f):
    """Отлавливание ошибок"""
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error = f'ERROR {e} in '
            print(error)
            update = args[0]
            if update and hasattr(update, 'message'):
                update.message.bot.send_message(chat_id=ADMIN_ID, text=error)
            raise e
    return inner


@log_error
def post_in_channel(data: dict) -> None:
    """Постит пост в канал"""
    msg_text = f"""<a href="{data['url']}"><b>{data['title']}</b></a>"""
    bot.send_photo(chat_id=CHAT_ID, photo=data['img'], caption=msg_text, parse_mode='html')


if __name__ == '__main__':
    print('Telegram Bot Engine')
