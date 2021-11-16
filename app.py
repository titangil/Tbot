#!/usr/bin/python
#-*-coding: utf-8 -*-
##from __future__ import absolute_import
###
from csv import DictWriter
from flask import Flask, jsonify, render_template, request
import json
import numpy as np
import pandas as pd
from googletrans import Translator
import webbrowser
import dropbox
import nagisa
import cutlet
from janome.tokenizer import Tokenizer
t = Tokenizer()

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


katsu = cutlet.Cutlet()
################### Dropbox ##################
dropbox_access_token = "acFejDGvB7oAAAAAAAAAAeU29LoxJ8MEQg6bGRWWBR3cHo7vMBazvFdUVgK4f-XV"
dropbox_path = "/Tbot/talk.csv"
computer_path = r"talk.csv"
client = dropbox.Dropbox (dropbox_access_token)

################### CSV ######################

headersCSV = ['Japanese','English translated']      
#dict={'Japanese':'こんにちは','English translated':'Hello.'}


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
        #userId = 
        #userId = 
        profile = line_bot_api.get_profile(event['joined']['members'][0]['userId'])
        print(profile.display_name)
        #line_bot_api.push_message(event['source']['groupId'], TextSendMessage(text='Welcome'+profile.display_name))
        #print(type(userId))
        Welcomemsg = "Welcome "+profile.display_name+" to our group!😆🥳\nPlease add me as friend so I can start translate text for you!🤓\nType '/Help' for more information\n\nこんにちは "+profile.display_name+"さん!😆🥳\n友達になってください、そうすれば私はあなたのためにテキストを翻訳することができます。🤓\n詳細は「/Help」と入力してください。"
        line_bot_api.push_message(event['source']['groupId'], TextSendMessage(text= Welcomemsg))
        print('Someone Joined')
    if event['type'] == "memberLeft":
        profile = line_bot_api.get_profile(event['left']['members'][0]['userId'])
        #line_bot_api.push_message(event['source']['groupId'], TextSendMessage(text='Bye'+profile.display_name))
        byemsg = "So long "+profile.display_name+"\nHope we can meet again😢\n\nバイバイ"+profile.display_name+"さん\nまたお会いできることを願っています。😢"
        line_bot_api.push_message(event['source']['groupId'], TextSendMessage(text=byemsg))
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
        
        if msg == '/Download':
            client.files_delete(dropbox_path)
            client.files_upload (open (computer_path, "rb"). read (), dropbox_path)
            print ("upload: {}" .format (computer_path))
            link_to_download= client.sharing_create_shared_link(dropbox_path)
            replyObj = TextSendMessage(text="Dropbox Link:  "+ link_to_download.url)

        elif msg == '/Help':
            helpmsg = "- Text in Japanese will be translated to English\n- Text in English will be translated to Japanese\n- Type '/Download' to download the conversation\n- Type '/Clear' to delete all conversation"
            replyObj = TextSendMessage(text=helpmsg)
            
        elif msg == '/Clear':
            talk = open("talk.csv", "w")
            talk.truncate()
            talk.close()
            with open('talk.csv', 'w') as open_file:
                dw = DictWriter(open_file, delimiter=',', fieldnames=headersCSV)
                dw.writeheader()
           
            replyObj = TextSendMessage(text='Cleared all conversation successfully!')

        elif translation.src == 'en':
            
            translation = translator.translate(msg, dest='ja')
            replyObj = TextSendMessage(text="翻訳  🇺🇸 => 🇯🇵 　\n\n"+profile.display_name+"さんは\n　　「"+translation.text+"」   \nと言った\n\n"+ wordx)

            df = pd.read_csv('talk.csv')
            print(df.to_string()) 
           
        elif translation.src == 'ja':
            translation = translator.translate(msg, dest='en')
            replyObj = TextSendMessage(text="Translation  🇯🇵 => 🇺🇸  \n\n"+profile.display_name+" said\n        '"+translation.text+"\nRomanji\n        "+katsu.romaji(msg)+"'\n\n"+wordx)
            #print(katsu.romaji(msg))
         
            dict={'Japanese':msg,'English translated':translation.text}
            with open('talk.csv', 'a', newline='') as talk:

                dictwriter_object = DictWriter(talk, fieldnames=headersCSV)
                dictwriter_object.writerow(dict)
                talk.close()

                #f.write(dict)

            df = pd.read_csv('talk.csv')
            print(df.to_string()) 
            
            
         

        try:
            line_bot_api.reply_message(rtoken, replyObj)
            print("Translate and Reply Successfuly")
        except :
            confused = ['I have no idea what you are saying','Please Check your spelling','😵😵😵']
            rand = np.random.randint(0,2)
            replyObj = TextSendMessage(text=confused[rand])
            line_bot_api.reply_message(rtoken, replyObj)
            print("Translate and Reply Failed")

        


    else:
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
    return ''

if __name__ == '__main__':
    app.run(debug=True)

    
