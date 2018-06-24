import json
import jieba
schools=[] 
keyword =[]   
department =[]
database = {}
for f in open("schools.txt", "r",encoding ='UTF-8'):
    schools.append(f.strip('\ufeff').strip('\n').split(' '))

for f in open("keyword.txt", "r",encoding ='UTF-8'):
    keyword.append(f.strip('\ufeff').strip('\n').split(' '))

for f in open("department.txt", "r",encoding ='UTF-8'):
        department.append(f.strip('\ufeff').strip('\n').split(' '))

with open('test0.json') as inputdata:
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
                   database[sch[1]] = {}

#print(database)
print(schooldict)
cnt = 0



for Com in CommentContent:
    seg_list = jieba.cut(CommentContent[Com])
    tag = []
    for seg in seg_list:
        for keyline in keyword:
            for key in keyline:
                if seg == key:
                    tag.append(str(keyline[0]))
        for sch in schools:
            for name in sch:
                if seg == name:
                    tag.append(str(sch[1]))
        for dep in department:
            for name in dep:
                if seg == name:
                    tag.append(str(dep[0])+"系")
    if tag != []:
        tag_dict[str(Com)] = tag


for tag in tag_dict:              
   print(tag_dict[tag])
print("_________________")

for tags in tag_dict:
    sortedtag = []
    for tag in tag_dict[tags]:
        for sch in schools:
            if tag == sch[1]:
                sortedtag.append(str(tag))
    for tag in tag_dict[tags]:
        for dep in department:
            if tag == (dep[0]+"系"):
                sortedtag.append(str(tag))
    for tag in tag_dict[tags]:
        for key in keyword:
            if tag == key[0]:
                sortedtag.append(str(tag))
    tag_dict[tags] = sortedtag

for tag in tag_dict:              
   print(tag_dict[tag])

#for tag in tag_dict:
#    print(tag,":",CommentContent[int(tag)],":",tag_dict[tag])

#print("共",len(CommentContent),"回覆")
#print("共抽取",len(tag_dict),"份回復")
#print("抽取率",str(len(tag_dict)/len(CommentContent)*100),"%")

#print(department)