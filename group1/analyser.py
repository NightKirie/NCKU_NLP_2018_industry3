import json
import jieba

with open('test1.json') as inputdata:
        data = json.load(inputdata)

title = data['article_title'] 
content = data['content']
date = data['date']

cnt = -1
push_userid = " "

CommentContent = {}
CommentLevel = {}


#Arrange comments + connect broken messages
for mes in data['messages']:
    if push_userid != mes['push_userid']:
        cnt += 1
        CommentContent[cnt] = mes['push_content']
        CommentLevel[cnt] = mes['push_tag']
        push_userid = mes['push_userid']
    else:
        CommentContent[cnt] = CommentContent[cnt]+mes['push_content']
        CommentLevel[cnt] = mes['push_tag']

for Com in CommentContent:
    print(CommentContent[Com])
    print(" ")
