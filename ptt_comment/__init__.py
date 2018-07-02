# coding: utf-8
import json
import sys
import os
import re
import itertools
import random
import jieba

RES_PATH = os.path.dirname(__file__) + '/res/'

jieba.set_dictionary(RES_PATH + 'dict.txt.big')
jieba.initialize()

with open(RES_PATH + 'all.txt') as f:
    key_map = {}
    for line in f.readlines():
        words = sorted([x for x in re.split(r'[ \n]', line) if x is not ''], key=len)
        for word in words:
            key_map[word] = words[0]
            jieba.add_word(word)

with open(RES_PATH + 'tagged.json') as f:
    articles = json.load(f)['articles']

word_index = {}
for i, article in enumerate(articles):
    for word in article['tags']:
        if word not in word_index:
            word_index[word] = {i}
        else:
            word_index[word].add(i)


# In[10]:


def search(tags):
    
    if len(tags) == 0:
        return []
    
    mapped = set(key_map[x] for x in tags if x in key_map)

    if len(mapped) == 0:
        return []
    
    candidates = []
    added = set()
    tagset = set()
    
    for L in range(len(mapped),0,-1):
        candidates.clear()
        added.clear()
        for subset in itertools.combinations(mapped, L):
            for i in set.intersection(*[word_index[x] for x in subset]):
                if i in added:
                    continue
                else:
                    added.add(i)
                    
                a = articles[i]
                base_dif = len(mapped.difference(a['tags']))
                for s in a['messages']:
                    hit = 0
                    missed = 0
                    tagset.clear()
                    segged = jieba.lcut(s)
                    for word in segged:
                        if word in key_map:
                            if key_map[word] in mapped:
                                tagset.add(key_map[word])
                                hit += 1
                            else:
                                missed += 1
                    candidates.append((base_dif, missed, -len(tagset), -hit/len(segged), s))
        
        if len(candidates) > 0:
            return [x[4] for x in sorted(candidates)][:10]
    
    return []


# In[14]:
