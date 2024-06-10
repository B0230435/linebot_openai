from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import time
import traceback
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

def QA_response(text):
    client = QuestionAnsweringClient(endpoint, credential)
    with client:
        question=text
        output = client.get_answers(
            question = question,
            project_name=knowledge_base_project,
            deployment_name=deployment
        )
    return output.answers[0].answer

# 定義你要回覆的訊息內容
reply_message = TextSendMessage(text='Hello, world!')

# 發送回覆訊息
line_bot_api.reply_message('REPLY_TOKEN', reply_message)

# 監聽用戶發送的訊息事件
def handle_message(event):
    user_message = event.message.text
    
    # 如果用戶發送的訊息是 "1"，則回覆 "2"
    if user_message == '1':
        reply_message = TextSendMessage(text='2')
        line_bot_api.reply_message(event.reply_token, reply_message)


def words_English_to_Chinese(word):
    # 字母與數字的映射字典
    words_dict = {
        "apple": "蘋果",
        "banana": "香蕉",
        "cat": "貓",
        "dog": "狗",
        "elephant": "大象",
        "flower": "花",
        "guitar": "吉他",
        "house": "房子",
        "ice": "冰",
        "jacket": "夾克"
    }
    if word in words_dict:
        word=words_dict[word]
    else:
        word="該單字不在字典中。"
    return words_English_to_Chinese(word)



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
    msg = event.message.text
    word=words_English_to_Chinese(msg)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(word))
         

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
