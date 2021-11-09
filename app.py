#!/usr/bin/python
#-*-coding: utf-8 -*-
##from __future__ import absolute_import
###
from google.cloud import translate
from flask import Flask, jsonify, render_template, request
import json
import numpy as np
import requests
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ImageSendMessage, StickerSendMessage, AudioSendMessage
)
from linebot.models.template import *
from linebot import (
    LineBotApi, WebhookHandler
)


def translate_text(text="Hello, world!", project_id="gleaming-design-331610"):

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "en-US",
            "target_language_code": "ja",
        }
    )

    '''for translation in response.translations:
        print("Translated text: {}".format(translation.translated_text))'''
    return response.translation.translated_text



app = Flask(__name__)

lineaccesstoken = '/+mz28LZ+4TcWao8D1SiEkEJfSatxM8rLwa7MqMl6yMyffOdaJtnqHqzemci3Ogip6tk8Ye6U7HXK01qCGgYBkzqWAsCzRoGbnSIy7ySiatAQfkrO39tELLdO+ixRiC9cLXMvOTftT1w3hPgDcoWOQdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(lineaccesstoken)

####################### new ########################
@app.route('/')
def index():
    return "Hello World!"


@app.route('/webhook', methods=['POST'])
def callback():
    json_line = request.get_json(force=False,cache=False)
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    no_event = len(decoded['events'])
    for i in range(no_event):
        event = decoded['events'][i]
        event_handle(event)
    return '',200








def event_handle(event):
    print(event)
    try:
        userId = event['source']['userId']
    except:
        print('error cannot get userId')
        return ''

    try:
        rtoken = event['replyToken']
    except:
        print('error cannot get rtoken')
        return ''
    try:
        msgId = event["message"]["id"]
        msgType = event["message"]["type"]
    except:
        print('error cannot get msgID, and msgType')
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
        return ''

    if msgType == "text":

        msg = str(event["message"]["text"])

        '''data = {
          'auth_key': 'dasdsadasfasdsafdsgfvrscdadcas',
          'text': 'Hello',
          'target_lang': 'DE'
        }   '''
        
        #response = requests.post('https://api-free.deepl.com/v2/translate', data=data)
        replyObj = TextSendMessage(text=translate_text())
        line_bot_api.reply_message(rtoken, replyObj)
        print(msg)

    else:
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
    return ''

if __name__ == '__main__':
    app.run(debug=True)
