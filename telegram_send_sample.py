import subprocess
import configparser
import socket
from telegram_send import send2

config = configparser.ConfigParser()
config.read('config.ini')
config_name = 't'
bot_config = {'token': config.get(config_name, 'telegram_bot_token'), 'chat_id': config.get(config_name, 'service_account_teletgram_id')}
detail_bot_config = {'token': config.get(config_name, 'ptt_detail_bot_token'), 'chat_id': config.get(config_name, 'service_account_teletgram_id')}
msg = '[xxx]'
send2(messages=[msg], conf=bot_config, captions='ptt update1')
send2(messages=[msg], conf=detail_bot_config, captions='ptt update2')
