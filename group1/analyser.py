import json
import jieba

def ListCheck(arg0, arg1):
    WordList =[]
    ContextList = arg0
    CheckList = arg1 
    for Context in ContextList:
        for Check in CheckList:
            if Check[0] == Context:
                WordList.append(Check)

    return WordList


schools=[] 
keyword =[]   

for f in open("schools.txt", "r",encoding ='UTF-8'):
    schools.append(f.strip('\ufeff').strip('\n').split(' '))

for f in open("keyword.txt", "r",encoding ='UTF-8'):
    keyword.append(f.strip('\ufeff').strip('\n').split(' '))

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

#Demo arranged database
for Com in CommentContent:
    print(CommentLevel[Com],":",CommentContent[Com])

seg_list = jieba.cut(title+content)


tag_dict = {}
compare_list = []
schooldict ={}

schoolcount = 0

for seg in seg_list:
    schnum = 0
    for sch in schools:
       schnum+=1
       for name in sch:
           if seg == name:
               if schooldict.get(sch[1],0) == 0:
                   schoolcount +=1
                   schooldict[sch[1]] = schnum

print(schooldict)
cnt = 0
for Com in CommentContent:
    seg_list = jieba.cut(CommentContent[Com])
    for seg in seg_list:
        for keyline in keyword:
            for key in keyline:
                if seg == key:
                    if tag_dict.get(str(Com), 0) == 0:
                        tag_dict[str(Com)] = [keyline[0]]
                    else:
                        tag_dict[str(Com)] = [tag_dict[str(Com)] ,keyline[0]]
        for sch in schools:
            for name in sch:
                if seg == name:
                    if tag_dict.get(str(Com), 0) == 0:
                        tag_dict[str(Com)] = sch[1]
                    else:
                        tag_dict[str(Com)] = [tag_dict[str(Com)] , sch[1]]
                
for tag in tag_dict:
    print(tag,":",CommentContent[int(tag)],":",tag_dict[tag])

print("共",len(CommentContent),"回覆")
print("共抽取",len(tag_dict),"份回復")
print("抽取率",str(len(tag_dict)/len(CommentContent)*100),"%")