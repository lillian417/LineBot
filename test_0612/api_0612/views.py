from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, PostbackEvent
from urllib.parse import parse_qsl
from module import func
import variable_settings as varset

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

# Create your views here.
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                userid, lang, sound = readData(event)
                mtext = event.message.text 
                if mtext == '@使用說明':
                    func.showUse(event)
                    
                elif mtext == '@英文':
                    func.setLang(event, 'en', sound, userid)

                elif mtext == '@日文':
                    func.setLang(event, 'ja', sound, userid)

                elif mtext == '@其他語文':
                    func.setElselang(event)  

                elif mtext == '@顯示設定':
                    func.showConfig(event, lang, sound)

                elif mtext == '@切換發音':
                    func.toggleSound(event, lang, sound, userid)

                else:
                    func.sendTranslate(event, lang, sound, mtext)

            if isinstance(event, PostbackEvent):  #PostbackTemplateAction觸發此事件
                userid, lang, sound = readData(event)
                backdata = dict(parse_qsl(event.postback.data))  #取得Postback資料
                func.sendData(event, backdata, sound, userid)
                        
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def readData(event):
    userid = event.source.user_id
    try:
        data = varset.get(userid)
        datalist = data.split('/')
        lang = datalist[0]
        sound = datalist[1]
    except:
        varset.set(userid, 'en/no')
        lang = 'en'
        sound = 'no'
    return userid, lang, sound