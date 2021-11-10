#!/usr/bin/python
#-*-coding: utf-8 -*-
##from __future__ import absolute_import
###
from flask import Flask, jsonify, render_template, request
import json
import numpy as np
from googletrans import Translator
import webbrowser

import nagisa

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ImageSendMessage, StickerSendMessage, AudioSendMessage
)
from linebot.models.template import *
from linebot import (
    LineBotApi, WebhookHandler
)
translator = Translator()
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
    
    print(event['type'])
    if event['type'] == "memberJoined":
        userId = event['joined']['members']
        userId = userId[0]['userId']
        print(userId.display_name)
        print(type(userId))
        #line_bot_api.push_message(event['source']['groupId'], TextSendMessage(text='Hello '))
        print('Someone Joined')
    if event['type'] == "memberLeft":
        line_bot_api.push_message(event['source']['groupId'], TextSendMessage(text='Hello World!'))
        print('Someone Left')
    
    
    try:
        userId = event['source']['userId']
    except:
        print('error cannot get userId')
        return ''


 
        return ''
    try:
        groupId = event['source']['groupId']
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

    
  
    '''group_count = str(line_bot_api.get_group_members_count(groupId))
    group_count_det = group_count
    group_count = str(line_bot_api.get_group_members_count(groupId))

    if group_count == group_count_det:
            replyObj = TextSendMessage(text='Welcome!')
            line_bot_api.reply_message(rtoken, replyObj)
            group_count_det= group_count'''

    

            
    if msgType == "text":
        profile = line_bot_api.get_profile(userId)
        group = line_bot_api.get_group_summary(groupId)
        group_count = str(line_bot_api.get_group_members_count(groupId))
        profile.display_name
        msg = str(event["message"]["text"])
        translation = translator.translate(msg)
        words = nagisa.tagging(msg)
        wordx = ""
        wordslength = len(words.words)
        for x in range(wordslength):
            if len(words.words[x]) == 1:
                wordx = wordx + words.words[x] + "\t\t   "+ words.postags[x]+"\n"
            elif len(words.words[x]) == 2:
                wordx = wordx + words.words[x] + "\t  "+ words.postags[x]+"\n"
            elif len(words.words[x]) == 3:
                wordx = wordx + words.words[x] + "\t"+ words.postags[x]+"\n"
        if translation.src == 'en':
            
            translation = translator.translate(msg, dest='ja')
            replyObj = TextSendMessage(text="翻訳  🇺🇸 => 🇯🇵 　\n\n"+profile.display_name+"さんは\n　　「"+translation.text+"」   \nと言った\n\n"+ wordx)
      
            #webbrowser.open("http://www.example.com")
        elif translation.src == 'ja':
            translation = translator.translate(msg, dest='en')
            replyObj = TextSendMessage(text="Translation  🇯🇵 => 🇺🇸  \n\n"+profile.display_name+" said\n        '"+translation.text+"'\n\n"+wordx)
          
            #webbrowser.open("http://www.example.com")
        
        try:
            line_bot_api.reply_message(rtoken, replyObj)
            print("Translate and Reply Successfuly")
        except :
            confused = ['Say that again bitch','I have no idea what you are saying','Check your spelling please']
            rand = np.random.randint(0,2)
            replyObj = TextSendMessage(text='<a href="where/you/want/the/link/to/go">text of the link</a>')
            line_bot_api.reply_message(rtoken, replyObj)
            print("Translate and Reply Failed")
    else:
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
    return ''

if __name__ == '__main__':
    app.run(debug=True)

    
