import Get_data
from flask import Flask, abort, request
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

###above for import package

app = Flask(__name__)

line_bot_api = LineBotApi(line_channel_access_token)
handler = WebhookHandler(line_channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')



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
'''
def PrintImage(img, event):
    ext = 'png'
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        img.save(tf, "PNG")
        img.close()
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
        image = client.upload_from_path(path, config=config, anon=False)
        os.remove(path)
        print(path)
        image_message = ImageSendMessage(
            original_content_url=image['link'],
            preview_image_url=image['link']
        )
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='以下是您所查詢的資料'),
                image_message])
    except:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='操作失敗，請重新輸入'))
    return 0
'''

@handler.add(MessageEvent, message=(ImageMessage, TextMessage))
def handle_message(event):
    if isinstance(event.message, TextMessage):  #get input
        line_bot_api.reply_message(
            event.reply_token, event.message.text)




if __name__ == '__main__':
    app.run()
