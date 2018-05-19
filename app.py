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
    value = [33, 67]
    value2 = [40, 60]
    labels = '教師比例', '學生比例'
    colors = ['lightcoral', 'lightskyblue']

    thegrid = GridSpec(1, 2)
    pl.subplot(thegrid[0, 0], aspect=1)
    pl.pie(value, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
    pl.title('中葉大學')

    pl.subplot(thegrid[0, 1], aspect=1)
    pl.pie(value2, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
    pl.title('小葉大學')

    pl.savefig('01.jpg')
    #Image.open('01.jpg').show()
    pl.gcf().clear()

    labels = '中葉大學', '小葉大學'

    thegrid = GridSpec(5, 5, width_ratios=[1, 0.1, 1, 0.1, 1], height_ratios=[1, 0.22, 1, 0.22, 1])
    pl.subplot(thegrid[0, 0])
    value3 = [77, 83]
    pa, pb = pl.bar(labels, value3)
    pa.set_facecolor('lightcoral')
    pb.set_facecolor('lightskyblue')
    pl.title('註冊率(%)')

    pl.subplot(thegrid[0, 2])
    value4 = [767, 483]
    pa, pb = pl.bar(labels, value4)
    pa.set_facecolor('lightcoral')
    pb.set_facecolor('lightskyblue')
    pl.title('學生數')

    pl.subplot(thegrid[0, 4])
    value5 = [55, 63]
    pa, pb = pl.bar(labels, value5)
    pa.set_facecolor('lightcoral')
    pb.set_facecolor('lightskyblue')
    pl.title('最低錄取分數')

    pl.subplot(thegrid[2, 0])
    value6 = [234, 189]
    pa, pb = pl.bar(labels, value6)
    pa.set_facecolor('lightcoral')
    pb.set_facecolor('lightskyblue')
    pl.title('科系經費(萬)')

    pl.subplot(thegrid[2, 2])
    value7 = [13, 16]
    pa, pb = pl.bar(labels, value7)
    pa.set_facecolor('lightcoral')
    pb.set_facecolor('lightskyblue')
    pl.title('就業比率(%)')

    pl.subplot(thegrid[2, 4])
    value8 = [20, 22]
    pa, pb = pl.bar(labels, value8)
    pa.set_facecolor('lightcoral')
    pb.set_facecolor('lightskyblue')
    pl.title('就業平均薪資(千)')

    pl.subplot(thegrid[4, 0])
    value9 = [10, 12]
    pa, pb = pl.bar(labels, value9)
    pa.set_facecolor('lightcoral')
    pb.set_facecolor('lightskyblue')
    pl.title('科系相關大公司就業比率(%)')

    pl.subplot(thegrid[4, 2])
    value10 = [77, 63]
    pa, pb = pl.bar(labels, value10)
    pa.set_facecolor('lightcoral')
    pb.set_facecolor('lightskyblue')
    pl.title('考碩班比率(%)')

    pl.savefig('02.jpg')
    #Image.open('02.jpg').show()
    pl.gcf().clear()

    message = ImageSendMessage(
        original_content_url='https://pbs.twimg.com/media/Db7U0hGUQAE1VEw.jpg:large',
        preview_image_url='https://pbs.twimg.com/media/Db7U0hGUQAE1VEw.jpg:large'
    )

    line_bot_api.reply_message(event.reply_token, message)
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)