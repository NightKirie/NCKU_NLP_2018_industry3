import jieba
from flask import Flask, abort, request
from linebot import (
        LineBotApi, WebhookHandler
        )
from linebot.exceptions import (
        InvalidSignatureError
        )
from linebot.models import *

import ckip
from config import line_channel_access_token, line_channel_secret
from forExcel import team3_excel_API as api3
from output import output_api as api5

# currently not used module
# import tempfile, os
# from imgurpython import ImgurClient
# import Get_data
# from config import client_id, client_secret, album_id, access_token, 
#     refresh_token, line_channel_access_token, line_channel_secret



# module level variable
app = Flask(__name__)

line_bot_api = LineBotApi(line_channel_access_token)
handler = WebhookHandler(line_channel_secret)

syno_depr = {}
syno_school = {}

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
        
        # tokenlize by jieba
        toks = [tok for tok in jieba.cut(event.message.text)]

        # fetch school and department list
        school = []
        depr = []

        for tok in toks:
            if tok in syno_school:
                school.append(syno_school[tok])
            elif tok in syno_depr:
                depr.append(syno_depr[tok])


        # tokenlize by ckip
        ctoks = ckip.seg(event.message.text)

        # fetch preference by 'Na' tag
        pref = [tok[0] for tok in ctoks if tok[1] == 'Na' and tok[0] not in syno_depr and tok[0] not in syno_school]

        # set action
        score_key = ['能不能上', '落點', '分析']
        if any(k in event.message.text for k in score_key):
            action = 'score'
        elif len(school) == 1:
            action = 'question'
        else:
            action = 'compare'

        # error handling
        if len(school) == 0:
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='sorry，沒偵測到要查詢的學校，請再試一次')])
            return
        elif len(depr) == 0:
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='sorry，沒偵測到要查詢的學系，請再試一次')])
            return
        elif len(school) != len(depr):
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='sorry，偵測到的學校與系所對不上，請再試一次')])
            return



        # DEBUG: add test data
        pref = ['教師數']

        # intent object:
        #   action (str): Action type. 
        #   school (list): List of school to be compared. Might be empty list.
        #   depr (list): List of department to be compared. Might be empty list.
        #   score (dict): Dict of scored, indexed by subject (cn, en, ma, sc, so). Might be empty dict.
        #   pref (list): The preference user interested. Might be empty list.
        intent = {
            'action': action, 
            'school':school,
            'depr':depr,
            'score': {},
            'pref': pref
        }

        # deubg message
        print('[app.py] intent:', repr(intent))

        # connect team3 API
        comp = api3(intent)
        print('comp:', str(comp))

        # connect team5 API
        api5(comp, line_bot_api, event)



def init():
    """
    initialize settings
    """
    # load zh-TW extension dictionary
    jieba.set_dictionary('./dictdata/dict.txt.big')

    # load user defined dictionary
    jieba.load_userdict('./dictdata/userdict.txt')

    # load school name synonym
    with open('./dictdata/syno_school.txt', encoding='utf8') as fin:
        for line in fin:
            toks = line.strip().split()
            for tok in toks:
                syno_school[tok] = toks[0]
                
    # load department name synonym
    with open('./dictdata/syno_depr.txt', encoding='utf8') as fin:
        for line in fin:
            toks = line.strip().split()
            for tok in toks:
                syno_depr[tok] = toks[0]

    jieba.initialize()

    print('[app.py] initialize complete')




# do initalization
init()

if __name__ == '__main__':
    app.run()
