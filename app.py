import jieba
from flask import Flask, abort, request
from linebot import (
        LineBotApi, WebhookHandler
        )
from linebot.exceptions import (
        InvalidSignatureError
        )
from linebot.models import *

import CKIP_Socket_Client
from config import client_id, client_secret, album_id, access_token, refresh_token, line_channel_access_token, line_channel_secret
from forExcel import team3_excel_API as api3
from output import output_api as api5

# currently not used module
# import tempfile, os
# from imgurpython import ImgurClient
# import Get_data


# module level variable
app = Flask(__name__)

line_bot_api = LineBotApi(line_channel_access_token)
handler = WebhookHandler(line_channel_secret)

synonym = {}

# static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    print("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'



@handler.add(MessageEvent, message=(ImageMessage, TextMessage))
def handle_message(event):
    if isinstance(event.message, TextMessage):  #get input
        print('received text message')
        
        # tokenlize
        ptoks = []
        toks = [tok for tok in jieba.cut(event.message.text)]

        for tok in toks:
            if tok in synonym:
                ptoks.append((tok, 'sch'))
            elif tok.strip() != '':
                ptoks.append(CKIP_Socket_Client.seg(tok)[0])

        print('message tokenlized with length: %d' % len(ptoks))
        print(ptoks)

        schools = []

        for tok in ptoks:
            if tok[1] == 'sch':
                schools.append(synonym[tok[0]])

        depr = ['資訊工程學系'] * len(schools)

        # intent object:
        #   action (str): Action type. 
        #   school (list): List of school to be compared. Might be empty list.
        #   depr (list): List of department to be compared. Might be empty list.
        #   score (dict): Dict of scored, indexed by subject (cn, en, ma, sc, so). Might be empty dict.
        #   pref (str): The preference user interested. Might be empty str.
        intent = {
            'action': 'compare', 
            'school':schools,
            'depr':depr,
            'score': {},
            'pref': '教師數'
        }

        print('intent:', str(intent))

        # connect team3 API
        comp = api3(intent)
        print('comp:', str(comp))

        # connect team5 API
        api5(comp, line_bot_api, event)



def init():
    """
    initialize global variable and settings
    """
    # load zh-TW extension dictionary
    jieba.set_dictionary('./dictdata/dict.txt.big')

    # load user defined dictionary
    jieba.load_userdict('./dictdata/userdict.txt')

    # load school name synonym
    with open('./dictdata/synonym.txt', encoding='utf8') as fin:
        for line in fin:
            toks = line.strip().split()
            for tok in toks:
                synonym[tok] = toks[0]

    print('initialize complete')



if __name__ == '__main__':
    app.run()
    init()



# unused function
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
