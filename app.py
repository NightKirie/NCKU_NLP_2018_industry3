import random
from flask import Flask, request, abort
from imgurpython import ImgurClient
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import tempfile, os
from config import client_id, client_secret, album_id, access_token, refresh_token, line_channel_access_token, line_channel_secret
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl
pl.rcParams['font.sans-serif']=['Microsoft JhengHei']
pl.rcParams['font.serif']=['Microsoft JhengHei']
from matplotlib.gridspec import GridSpec
import numpy
from PIL import Image

###above for import package



app = Flask(__name__)

line_bot_api = LineBotApi(line_channel_access_token)
handler = WebhookHandler(line_channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')


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
pl.gcf().clear()



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'


@handler.add(MessageEvent, message=(ImageMessage, TextMessage))
def handle_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
        message_content = line_bot_api.get_message_content(event.message.id)
        with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name

        dist_path = tempfile_path + '.' + ext
        dist_name = os.path.basename(dist_path)
        os.rename(tempfile_path, dist_path)
        try:
            client = ImgurClient(client_id, client_secret, access_token, refresh_token)
            config = {
                'album': album_id,
                'name': 'Catastrophe!',
                'title': 'Catastrophe!',
                'description': 'Cute kitten being cute on '
            }
            path = os.path.join('static', 'tmp', dist_name)
            client.upload_from_path(path, config=config, anon=False)
            #os.remove(path)
            print(path)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=tempfile_path + "\n" + dist_path + "\n" + dist_name + "\n" + path ))
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='我的天啊'))
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='上傳失敗'))
        return 0

    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    elif isinstance(event.message, TextMessage):
        if event.message.text == "看看大家都傳了什麼圖片":
            client = ImgurClient(client_id, client_secret)
            images = client.get_album_images(album_id)
            index = random.randint(0, len(images) - 1)
            url = images[index].link
            image_message = ImageSendMessage(
                original_content_url=url,
                preview_image_url=url
            )
            line_bot_api.reply_message(
                event.reply_token, image_message)
            return 0
        else:
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=' yoyo'),
                    TextSendMessage(text='請傳一張圖片給我')
                ])
            return 0


if __name__ == '__main__':
    app.run()



