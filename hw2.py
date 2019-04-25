#!/usr/bin/env python
# coding: utf-8

# In[1]:


# code for single item

import sys
inputfile = []
for line in sys.stdin:
    if '\n' in line:
        inputfile.append(line[:-1])
    else:
        inputfile.append(line)
## input file as a string list

dic = {}
for sid in range(len(inputfile)):
    trans = inputfile[sid].split(' ')
    inputfile[sid] = transt
    for eid in range(len(trans)):
        if trans[eid] not in dic:
             dic[trans[eid]] = []
        dic[trans[eid]].append((sid + 1, eid + 1))
## use SPADE to get frequent pattern, first create SPADE dic by sid,eid
## item : [(sid1, eid1),(sid2, eid2)] both 1 based
sup = {}  ## 1-itemset frequency (item: frequency)
for x in dic:
    sup[x] = len(dic[x])
sup1 = {}  ## frequent 1-itemset (frequent item : frequency)
for x in sup:
    if sup[x] >= 2:
        sup1[x] = sup[x]

## get the frequent 1-itemset for case, 
##the i-itemset could calculated based on it 

def getNextItemset (dic, itemset1, itemset2):
    nextitemset = {}
    tmp = {}
    if len(itemset1) == 0 or len(itemset2) == 0:
        return nextitemset
    for x in itemset1:
        xloc = dic[x]
        for loc in xloc:
            sid = loc[0]
            eid = loc[-1]
            tran = inputfile[sid - 1]
            if eid < len(tran):
                y = tran[eid]
                if y in itemset2:
                    pattern = x + ' ' + y
                    if pattern not in dic:
                        dic[pattern] = []
                    dic[pattern].append((sid,eid + 1))
                    nextitemset[pattern] = len(dic[pattern])
    for x in nextitemset:
        if nextitemset[x] >=2:
            tmp[x] = nextitemset[x]
    return(tmp)

n = 2
sups = []
former = sup1
while n <= 5:
    latter = getNextItemset(dic, former, sup1)
    if(len(latter) == 0):
        break
    sups.append(latter)
    former = latter
    n += 1

def combineDic (sups):
    final = []
    for sup in sups:
        for x in sup:
            l = []
            l.append(sup[x])
            l.append(x)
            final.append(l)
    final.sort(key = lambda x: (-x[0],x[1]))
    return (final)

finals = combineDic(sups)
for x in range(20):
    if x >= len(finals):
        break
    print(finals[x])

