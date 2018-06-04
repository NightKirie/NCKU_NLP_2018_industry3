import json
import jieba

with open('test1.json') as inputdata:
        data = json.load(inputdata)


print(data)
for rawdata in data:
    print(rawdata)