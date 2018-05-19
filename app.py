from flask import Flask, request, abort
import matplotlib.pyplot as pl
from matplotlib.gridspec import GridSpec
pl.rcParams['font.sans-serif']=['Microsoft JhengHei']
pl.rcParams['font.serif']=['Microsoft JhengHei']
from PIL import Image
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Ie/Zd3EYV5q9mwQjAuEGe2xkjuBH25g0hlzzOu2B+WOFRrluCuvowKaZqmlAN+KMzQkYWA8yiFFjSPN+uuiTYMhU0HNioAv7PqNqTQk14oBZRD/aYQ46faf16HziOZghcxWuYjOXZIZM1jnBMMYdewdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('2851d4db0aa44fce3cdfd5e471cf2f98')

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = ImageSendMessage(
        original_content_url='https://truth.bahamut.com.tw/s01/201805/5147c83d710be51e32b29c9b0fc83656.JPG',
        preview_image_url='https://truth.bahamut.com.tw/s01/201805/5147c83d710be51e32b29c9b0fc83656.JPG'
    )

    line_bot_api.reply_message(event.reply_token, message)
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)