#coding=utf-8
import json
import jieba
import sys
import os
RES_PATH = os.path.dirname(__file__) + '/rsc/'

def reqsyn(req, keydict, sc_board, score):
    for i in range(0,len(req)):
        for keyline in keydict:
            for key in keyline:
                if key == req[i]:
                    req[i] = keyline[0]
                    sc_board[keyline[0]] = score
    return req, sc_board

def reqspan(req, keydict, sc_board, score):
    newreq = req
    for _c in keydict:
        for dline in keydict[_c]:
            for _d in dline:
                for _r in req:
                    if _r == _d:
                        newreq.append(_c)
                        sc_board[_c]= 4
    return newreq, sc_board

def CommentGrading(article, req ,score,ComList,ComScore):
    for mes in article["messages"]:
        seg_m = jieba.cut(mes["push_content"])
        for seg in seg_m:
            for i in range(0,len(req)):
                if req[i] == seg:
                    if mes["push_content"] in ComList:
                        ComScore[mes["push_content"]]+=score[req[i]]
                    else:
                        ComList.append(mes["push_content"])
                        ComScore[mes["push_content"]] = score[req[i]]
    return ComList,ComScore
def search(tags):
    taglist = []
    tagscore = []
    outnumber = []
    request = []
    schools = []
    keyword = []
    department = []
    reqscore = {}
    dict_department = {}
    for tag in tags:
        request.append(tag)

    for f in open(RES_PATH+"schools.txt", "r",encoding ='utf-8'):
        schools.append(f.strip('\ufeff').strip('\n').strip('\t').split(' '))

    for f in open(RES_PATH+"keyword.txt", "r",encoding ='utf-8'):
        keyword.append(f.strip('\ufeff').strip('\n').strip('\t').split(' '))

    tmp = []
    collegue = "n"
    last =" "
    for f in open(RES_PATH+"department.txt", "r",encoding ='utf-8'):
        department.append(f.strip('\ufeff').strip('\n').strip('\t').split(' '))
        if f == "\n":
            if last == "\n":
                collegue = "n"
            else:
                last = "\n"
        else:   
            if collegue == "n":
                tmp = f.strip('\ufeff').strip('\n').strip('\t').split(' ')
                collegue = tmp[0]
                dict_department[collegue] = []
            else:
                dict_department[collegue].append(f.strip('\ufeff').strip('\n').strip('\t').split(' '))
    with open(RES_PATH+'filted.json',encoding = 'utf-8') as indata:
        content = json.load(indata)
    for f in open(RES_PATH+"tag.txt","r",encoding = 'utf-8'):
        taglist.append(f.strip('\ufeff').strip('\n').strip('\t').split(' '))
        tagscore.append(0)

    request, reqscore = reqsyn(request,schools, reqscore, 10)
    request, reqscore = reqsyn(request,department, reqscore,8)
    request, reqscore = reqsyn(request,keyword, reqscore, 6)
    request, reqscore = reqspan(request, dict_department, reqscore, 4)

    for j in range(0,len(request)):
        for i in range(0,len(taglist)):
            for tag in taglist[i]:
                if tag == request[j]:
                    tagscore[i]+=reqscore[request[j]]
            tagscore[i]-=2*(len(tag)-len(request))
    for i in range(0,len(taglist)):
        if tagscore[i]>0:
            if len(outnumber)<100:
                outnumber.append(i)
            else:
                minimun = 100
                minitag = -1
                for j in range(0,len(outnumber)):
                    if minimun > tagscore[outnumber[j]]:
                        minimun = tagscore[outnumber[j]]
                        minitag = j
                if minimun < tagscore[i]:
                    outnumber[minitag] = i

    #scan article comment
    OutCommentList = []
    OutCommentScore = {}
    for i in outnumber:
        article = content["articles"][i]
        OutCommentList, OutCommentScore= CommentGrading(article, request ,reqscore,OutCommentList,OutCommentScore)
    tmp = " "
    for j in range(0,len(OutCommentList)):
        MaxValueComIndex = j
        for i in range(j,len(OutCommentList)):
            if OutCommentScore[OutCommentList[MaxValueComIndex]] < OutCommentScore[OutCommentList[i]]:
                MaxValueComIndex = i
        tmp  = OutCommentList[MaxValueComIndex]
        OutCommentList[MaxValueComIndex] = OutCommentList[j]
        OutCommentList[j] = tmp
    return OutCommentList[0:10]