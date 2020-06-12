from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, PostbackAction, AudioSendMessage

import variable_settings as varset
from translate import Translator
from urllib.parse import quote

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def showUse(event):
    try:
        text1 = '''
1.字太多不想打
    '''
        message = TextSendMessage(
            text=text1
        )
        line_bot_api.reply_message(event.reply_token,message)

    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def setLang(event, lang, sound, userid):
    try:
        varset.set(userid, lang + '/' +sound)
        message = TextSendMessage(
            text = '語言設定為：' + langtoword(lang)
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def setElselang(event):
    try:
        message = TextSendMessage(
            text = '請選擇語言：',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=PostbackAction(label='韓文', data='item=ko')
                    ),
                    QuickReplyButton(
                        action=PostbackAction(label='泰文', data='item=th')
                    ),
                    QuickReplyButton(
                        action=PostbackAction(label='越南文', data='item=vi')
                    ),
                    QuickReplyButton(
                        action=PostbackAction(label='法文', data='item=fr')
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendData(event, backdata, sound, userid):
    lang = backdata.get('item')
    setLang(event, lang, sound, userid)

def langtoword(lang):
    if lang == 'en': word = '英文'
    if lang == 'ja': word = '日文'
    if lang == 'ko': word = '韓文'
    if lang == 'th': word = '泰文'
    if lang == 'vi': word = '越南文'
    if lang == 'fr': word = '法文'
    return word

def showConfig(event, lang, sound):
    try:
        if sound == 'yes': sound1 = '發音'
        else: sound1 = '不發音'
        text1 = '語音設定為：' + langtoword(lang)
        text1 += '\n發音設定為：' + sound1
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def toggleSound(event, lang, sound, userid):
    try:
        if sound == 'yes':
            sound='no'
            sound1='不發音'
        else:
            sound='yes'
            sound1 = '發音'
        varset.set(userid, lang + '/' +sound)
        message = TextSendMessage(
            text = '語言設定為：' + sound1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendTranslate(event, lang, sound, mtext):
    try:
        translator = Translator(from_lang="zh-Hant", to_lang=lang)
        translation = translator.translate(mtext)
        if sound =='yes':
            text = quote(translation)
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='+text+'&language='+lang
            message = [
                TextSendMessage(
                    text = translation
                ),
                AudioSendMessage(
                    original_content_url= stream_url,
                    duration=20000
                ),
            ]
            else:
                message = TextSendMessage(
                    text = translation
                )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))