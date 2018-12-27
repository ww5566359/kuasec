from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('U2ft7oOQobM1CVXQL17cuoxb35w+XfAYJY89EP/TRUV89Y/GIXf0yJjlybUUJuJoBnyRji5HhpG2aDTQJQKZUZursXUca3KXjFV7ESoho+6WHv2dSQFdxyB/jpzaZkuF/8XVkUtS4Ha4ojG8tQ2hfQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('35b79be8e1a7e1c699feab3eabecbf05')
counter=0

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://pic.pimg.tw/bestcool2/4ae7bdc0eee2f.jpg',
            title='菜單',
            text='因為試營運的關係我們手臂只接受一位客人一份薯條',
            actions=[
                PostbackTemplateAction(label='原味薯條50元',text='原味薯條',data='1'),
                URITemplateAction(label='官方網站',uri='https://www.mcdelivery.com.tw/tw/browse/menu.html?daypartId=45&catId=97&gclid=EAIaIQobChMI4fOAu6-A3gIViLrACh03OAqzEAAYASAAEgI6MfD_BwE'),
                MessageTemplateAction(label='結帳',text='結帳'),
                ]
                               )
                                )

    if event.message.text == "原味薯條":
        Confirm_template = TemplateSendMessage(
            alt_text='目錄 template',
            template=ConfirmTemplate(
            title='這是ConfirmTemplate',
            text='好的一份原味薯條?',
            actions=[MessageTemplateAction(label='確定',text='確定'),
                MessageTemplateAction(label='取消',text='取消')
                    ]
                                   )
                                            )
        line_bot_api.reply_message(event.reply_token,Confirm_template)
    if event.message.text == "確定":       
        message = TextSendMessage(text='好的~餐點以送出')
        line_bot_api.reply_message(event.reply_token, message)
        line_bot_api.reply_message(event.reply_token,Confirm_template)
    line_bot_api.reply_message(event.reply_token, message)
    if event.message.text == "結帳":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="總共"+counter+"元"))
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port)
