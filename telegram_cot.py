#!/bin/bash
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Job
import uuid
import configparser
import time
import random


config = configparser.ConfigParser()
config.read('config.ini')

config_name = config.get('HOSTNAMES', 'IP_ADDRESS')

token = config.get(config_name, 'telegram_bot_token')
print('token type = {}, {}'.format(type(token).__name__, token))
updater = Updater(token=config.get(config_name, 'telegram_bot_token'))
j = updater.job_queue
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def generate_keys(bot, update):
    user_id = update.message.from_user.id
    bot.send_message(chat_id=update.message.chat_id, text="user_id: {0}.".format(user_id))


def registry(bot, update):
    registry_process(bot, update)


def registry_process(bot, update):
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    bot.send_message(chat_id=update.message.chat_id, text="Hi {0}, your id is {1}.".format(first_name, user_id))


def echo_random_key(bot, update):
    print('update={0}'.format(update))
    user_id = update.message.from_user.id
    input_msg = update.message.text.strip()
    first_name = update.message.from_user.first_name
    bot.send_message(chat_id=update.message.chat_id, text='Hi {0}, your id is {1}. msg is {2}'.format(first_name, user_id, input_msg))


def make_new_pin(bot, update):
    print('update={0}'.format(update))
    user_id = update.message.from_user.id
    bot.send_message(chat_id=update.message.chat_id, text='made new pin, from {0}'.format(user_id))


def callback_minute(bot, job):
    some_chat_id = 12345
    bot.send_message(chat_id=some_chat_id, text='Please input pin for reason')
    print('callback done')


start_handler = CommandHandler('registry', registry)
dispatcher.add_handler(start_handler)

start_handler = CommandHandler('key', registry)
dispatcher.add_handler(start_handler)

start_handler = CommandHandler('asyouwere', generate_keys)
dispatcher.add_handler(start_handler)

start_handler = CommandHandler('raining', make_new_pin)
dispatcher.add_handler(start_handler)


start_handler = CommandHandler('', registry)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo_random_key)
dispatcher.add_handler(echo_handler)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="OOOOOOO")


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

job_minute = j.run_repeating(callback_minute, interval=60, first=0)

updater.start_polling()
updater.idle()
