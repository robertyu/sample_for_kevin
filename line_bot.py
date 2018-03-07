from flask import Flask, request, abort, send_file, Response
from telegram_send_isolate import send_message
import configparser
import traceback
import os
import io
from random import randint
from PIL import Image

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, JoinEvent
)

app = Flask(__name__)

line_bot_api = LineBotApi('LINE_KEY')
handler = WebhookHandler('WEB_HOOK_KEY')

config = configparser.ConfigParser()
config.read('config.ini')
config_name = 'LINEBOT'
bot_config = {'token': config.get(config_name, 'ptt_detail_bot_token'), 'chat_id': config.get(config_name, 'service_account_teletgram_id')}
_keywords = []


def send_info(head, description, content):
    send_message(messages=['[{0}] {1}, {2}'.format(head, description, content)], conf=bot_config, captions='line_bot update')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    print('callback-signature:{}'.format(signature))

    # get request body as text
    body = request.get_data(as_text=True)
    print('callback-body:{}'.format(body))
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except Exception:
        send_info('error', 'exception', traceback.format_exc())
        abort(400)

    print('callback-OK')
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global _images
    print('event:{0}'.format(event))
    print('event reply_token:{0}'.format(event.reply_token))
    print('event message:{0}'.format(event.message.text))
    msg = ['r']
    if event.message.text in msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))


@handler.add(JoinEvent)
def handle_join(event):
    print('event:{0}'.format(event))
    print('event reply_token:{0}'.format(event.reply_token))
    print('event source:{0}'.format(event.source))
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Joined this ' + event.source.type))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555)
