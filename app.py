from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

import matplotlib.pyplot as pl
pl.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
pl.rcParams['font.serif'] = ['Microsoft JhengHei']
from matplotlib.gridspec import GridSpec
import numpy
from PIL import Image

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
    figure = pl.figure()
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
    im = fig2img(figure)

    line_bot_api.reply_message(event.reply_token, ImageSendMessage(
        im
    ))
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


def fig2img(fig):
    """
    @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
    @param fig a matplotlib figure
    @return a Python Imaging Library ( PIL ) image
    """
    # put the figure pixmap into a numpy array
    buf = fig2data(fig)
    w, h, d = buf.shape
    return Image.frombytes("RGBA", (w, h), buf.tostring())


def fig2data(fig):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw()

    # Get the RGBA buffer from the figure
    w, h = fig.canvas.get_width_height()
    buf = numpy.fromstring(fig.canvas.tostring_argb(), dtype=numpy.uint8)
    buf.shape = (w, h, 4)

    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = numpy.roll(buf, 3, axis=2)
    return buf