#-*-coding:utf-8-*-
import graphing
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *


outputText = []
outputImageUrl = ''
outputGraphing = []
outputReply = [TextSendMessage(text="您好，\n")]


def output(inputlist):
    global outputText
    global outputGraphing
    global outputImageUrl

    outputText = []                 #輸出文字部分
    outputGraphing = inputlist      #輸出圖形的content，會拿去graphing繪圖
    outputImageUrl = ''             #存圖片的url
    i = 1                           #迴圈用

    comp_content = inputlist[0]


    if '該搜尋條件不存在' in comp_content:
        outputText += comp_content + '，不好意思。\n\n'
        return
    else:
        outputText += comp_content + ':\n'

    while i < len(inputlist):
        comp = inputlist[i][0]
        comp_department = inputlist[i][1]
        comp_ans = inputlist[i][2]
        ##學年度_x(B)、學校名稱_x(G)、系所名稱_x(I)、學年度_y(O)、學期(P)、學年度(V)沒有輸出

        ##單純輸出文字
        if '設立別' in comp_content:
            if comp_ans == '':
                replyText = comp + comp_department + '，找不到為哪種設立別的大學系所(´;ω;`)'
            else:
                replyText = comp + comp_department + '為' + comp_ans + '的大學系所'
            del outputGraphing[i]    #只會輸出文字，所以全部清掉
            i -= 1
            outputText += replyText + '\n'

        ##單純輸出文字
        elif '縣市名稱' in comp_content:
            if comp_ans == '':
                replyText = comp + comp_department + '，找不到位在何處，不好意思(´Ａ｀。)'
            else:
                replyText = comp + comp_department + '位於' + comp_ans[-3:]
            del outputGraphing[i]  #只會輸出文字，所以全部清掉
            i -= 1
            outputText += replyText + '\n'

        ##單純輸出文字
        elif '體系別' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '是何種體系別，抱歉(☍﹏⁰)'
            else:
                replyText = comp + comp_department + '為' + comp_ans[-1:] + '體系別'
            del outputGraphing[i]  # 只會輸出文字，所以全部清掉
            i -= 1
            outputText += replyText + '\n'

        ##單純輸出文字
        elif '學校類別' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '是何種學校類別(╥﹏╥)'
            else:
                replyText = comp + comp_department + '的學校類別為' + comp_ans
            del outputGraphing[i]  # 只會輸出文字，所以全部清掉
            i -= 1
            outputText += replyText + '\n'

        ##單純輸出文字
        elif '系所代碼' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '對應的系所代碼_(┐「ε:)_'
            else:
                replyText = comp + comp_department + '，的系所代碼為' + comp_ans
            del outputGraphing[i]  # 只會輸出文字，所以全部清掉
            i -= 1
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '畢業專業學分數' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '的畢業專業學分數(›´ω`‹ )'
                del outputGraphing[i]    #移除找不到資料的，不要繪圖
            else:
                replyText = comp + comp_department + '畢業專業學分數為' + comp_ans
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '畢業通識/共同學分數' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '的畢業通識/共同學分數_(┐「﹃ﾟ｡)_'
                del outputGraphing[i]    #移除找不到資料的，不要繪圖
                i -= 1
            else:
                replyText = comp + comp_department + '畢業通識/共同學分數為' + comp_ans
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '畢業實習學分數' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的畢業實習學分數(っ´ω`c)'
                del outputGraphing[i]    #移除找不到資料的，不要繪圖
                i -= 1
            else:
                replyText = comp + comp_department + '畢業實習學分數為' + comp_ans
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '畢業其他畢業學分數' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的畢業其他畢業學分數數(›´ω`‹ )'
                del outputGraphing[i]    #移除找不到資料的，不要繪圖
                i -= 1
            else:
                replyText = comp + comp_department + '畢業其他畢業學分數為' + comp_ans
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '畢業總學分數' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的畢業總學分數(´ﾟдﾟ`)'
                del outputGraphing[i]    #移除找不到資料的，不要繪圖
                i -= 1
            else:
                replyText = comp + comp_department + '畢業總學分數為' + comp_ans
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '專業必修實際開設學分數' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的專業必修實際開設學分數( ×ω× )'
                del outputGraphing[i]    #移除找不到資料的，不要繪圖
            else:
                replyText = comp + comp_department + '專業必修實際開設學分數為' + comp_ans
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '專業選修實際開設學分數' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的專業選修實際開設學分數(´・ω・`)'
                del outputGraphing[i]    #移除找不到資料的，不要繪圖
                i -= 1
            else:
                replyText = comp + comp_department + '專業選修實際開設學分數為' + comp_ans
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '學生數' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的學生數(´_ゝ`)'
                del outputGraphing[i]    #移除找不到資料的，不要繪圖
                i -= 1
            else:
                replyText = comp + comp_department + '學生數為' + comp_ans
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '教師數' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的教師數(´･_･`)'
                del outputGraphing[i]
                #outputGraphing.remove([comp, comp_department, comp_ans])    #移除找不到資料的，不要繪圖
                i -= 1
            else:
                replyText = comp + comp_department + '教師數為' + comp_ans
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '上學年度畢業生數' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的上學年度畢業生數(ㆆᴗㆆ)'
                del outputGraphing[i]    #移除找不到資料的，不要繪圖
                i -= 1
            else:
                replyText = comp + comp_department + '上學年度畢業生數為' + comp_ans
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '當學年度新生註冊率' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的當學年度新生註冊率_(:3 」∠ )_'
                del outputGraphing[i]   #移除找不到資料的，不要繪圖
                i -= 1
            else:
                replyText = comp + comp_department + '當學年度新生註冊率為' + comp_ans
            outputText += replyText + '\n'

        ##單純輸出文字
        elif '採計及加權' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的採計及加權( º﹃º )'
            else:
                replyText = comp + comp_department + '採計及加權為' + comp_ans
            del outputGraphing[i]  # 只會輸出文字，所以全部清掉
            i -= 1
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '錄取人數' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的錄取人數╰(〒皿〒)╯'
                del outputGraphing[i]    #移除找不到資料的，不要繪圖
                i -= 1
            else:
                replyText = comp + comp_department + '錄取人數為' + comp_ans
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '普通生錄取分數' in comp_content:
            if comp_a_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的普通生錄取分數╮(╯_╰)╭'
                del outputGraphing[i]    #移除找不到資料的，不要繪圖
                i -= 1
            else:
                replyText = comp + comp_department + '普通生錄取分數為' + comp_ans
            outputText += replyText + '\n'

        ##單純輸出文字
        elif '普通生同分參酌' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的普通生同分參酌(｡ŏ_ŏ)'
            else:
                replyText = comp + comp_department + '普通生同分參酌為' + comp_ans
            del outputGraphing[i]  # 只會輸出文字，所以全部清掉
            i -= 1
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '原住民錄取分數' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的原住民錄取分數(›´ω`‹ )'
                del outputGraphing[i]    #移除找不到資料的，不要繪圖
                i -= 1
            else:
                replyText = comp + comp_department + '原住民錄取分數為' + comp_ans
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '退伍軍人錄取分數' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的退伍軍人錄取分數( ˘•ω•˘ )'
                del outputGraphing[i]    #移除找不到資料的，不要繪圖
                i -= 1
            else:
                replyText = comp + comp_department + '退伍軍人錄取分數為' + comp_ans
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '僑生錄取分數' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的僑生錄取分數(⁰⊖⁰)'
                del outputGraphing[i]    #移除找不到資料的，不要繪圖
                i -= 1
            else:
                replyText = comp + comp_department + '僑生錄取分數為' + comp_ans
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '蒙藏生錄取分數' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的蒙藏生錄取分數(〒︿〒)'
                del outputGraphing[i]    #移除找不到資料的，不要繪圖
                i -= 1
            else:
                replyText = comp + comp_department + '蒙藏生錄取分數為' + comp_ans
            outputText += replyText + '\n'

        ##輸出文字及長條圖
        elif '派外子女錄取分數' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的派外子女錄取分數இдஇ'
                del outputGraphing[i]    #移除找不到資料的，不要繪圖
                i -= 1
            else:
                replyText = comp + comp_department + '派外子女錄取分數為' + comp_ans
            outputText += replyText + '\n'

        ##直接輸出文字
        elif '學測分數' in comp_content:
            if comp_ans == '':
                replyText = '找不到' + comp + comp_department + '，這個系所的派外子女錄取分數இдஇ'
            else:
                replyText = comp + comp_department + '派外子女錄取分數為' + comp_ans
            del outputGraphing[i]  # 只會輸出圖片連結，所以全部清掉
            i -= 1
            outputText += replyText + '\n'

        ##沒有相關的分類
        else:
            outputGraphing = []
            outputText += "該搜尋條件不存在，不好意思。\n"
        i += 1

    #不用繪圖，或者只有一個資料要繪圖
    if len(outputGraphing) <= 2:
        outputGraphing = []
    #如果outputGraphing有東西才繪圖
    if outputGraphing:
        outputImageUrl = graphing.drawing([outputGraphing])
    outputText += '\n'




def output_api(list, line_bot_api, event):
    for listElement in list:
        output(listElement)
        print(outputText)
        print(outputGraphing)
        print(outputImageUrl)
        outputReply.append(TextSendMessage(text=outputText))
        if outputImageUrl:
            outputReply.append(ImageSendMessage(original_content_url=outputImageUrl, preview_image_url=outputImageUrl))
    line_bot_api.reply_message(
        event.reply_token, outputReply)


