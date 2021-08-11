from django.conf import settings
from random import randint
from django.http import HttpResponse
from django.views import View
from telebot import TeleBot, types, logger
from .models import *
from threading import Timer
import logging
from .keys import telegramp_token

logger.setLevel(logging.DEBUG)
bot = TeleBot(telegramp_token)
update_id = None

class Check(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Бот запущен и работает.")


class UpdateBot(View):
    def post(self, request, *args, **kwargs):
        global update_id
        json_str = request.body.decode('UTF-8')
        update = types.Update.de_json(json_str)
        if update_id != update.update_id:
            bot.process_new_updates([update])
            update_id = update.update_id

        return HttpResponse(b'{"ok":true,"result":[]}')


@bot.message_handler(commands=['start'])
def start_message(message):
    text = '/////////////////////////'
    keyboard = types.InlineKeyboardMarkup()
    key_begin = types.InlineKeyboardButton(text='Начать')
    keyboard.add(key_begin)
    bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

    s = 'https://api.telegram.org/bot1859116308:AAEEntE7Cyn7eLNq8FO38_HJEZ6RW98LvGc/setWebhook?url=https://fcfc9b390e4c.ngrok.io/telegrm_check'