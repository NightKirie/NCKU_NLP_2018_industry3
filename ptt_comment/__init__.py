# coding: utf-8
import json
import sys
import re
import itertools
import random
import jieba

jieba.set_dictionary('res/dict.txt.big')
jieba.initialize()

with open('res/all.txt') as f:
    key_map = {}
    for line in f.readlines():
        words = sorted([x for x in re.split(r'[ \n]', line) if x is not ''], key=len)
        for word in words:
            key_map[word] = words[0]
            jieba.add_word(word)

with open('res/tagged.json') as f:
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
    index_sets = [word_index[x] for x in mapped]
    if len(index_sets) == 0:
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
                base = len(mapped.difference(a['tags']))
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
                    candidates.append((base+missed, -len(tagset), -hit/len(segged), s))
        
        if len(candidates) > 0:
            ret = [x[3] for x in sorted(candidates)][:10]
            random.shuffle(ret)
            return ret
    
    return []


# In[14]:
