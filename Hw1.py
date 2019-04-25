#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys

inputfile = []
trans = {}
sup = {}
for line in sys.stdin:
    if '\n' in line:
        tmp = line[:-1]
        inputfile.append(tmp)
    else:
        inputfile.append(line)
# read file

min_sup = int(inputfile[0])
inputfile.remove(inputfile[0])
for x in range(len(inputfile)):
    l = inputfile[x].split(" ")
    trans[x] = l

# initialize min_sup and transaction dic
for x in trans:
    for ele in trans[x]:
        if ele in sup:
            sup[ele]  = sup[ele] + 1
        else:
            sup[ele] = 1
rm = []
for x in sup:
    if sup[x] < min_sup:
        rm.append(x)

for x in rm:
    sup.pop(x)

add = sup.copy()
basic = sup.copy()
# get basic sup

def getcandidate(set1):
    set2 = set()
    for x in set1:
        for y in set1:
            listx = x.split(' ')
            listx.sort()
            listy = y.split(' ')
            listy.sort()
            length = len(listx)
            newlist = []
            if(listx[length - 1] == listy[length - 1]):
                continue
            for n in range(len(listx) - 1):
                if(listx[n] != listy[n]):
                    break
                newlist.append(listx[n])
            newlist.append(listx[length - 1])
            newlist.append(listy[length - 1])
            newlist.sort()
            if (len(newlist) == length + 1):
                set2.add(' '.join(newlist))
    return set2
set1 = set()
while True:
    for x in add:
        set1.add(x)
    cand = getcandidate(set1)  ##get candidate for the next round
    set1.clear()
    add.clear()        ## empty the add dict for the next round
    if len(cand) == 0:
        break
    for x in cand:
        l = x.split(" ")
        s = set(l)
        for ele in trans.values():
            eles = set(ele)
            if s <= eles:
                if x in add:
                    add[x] = add[x] + 1
                else:
                    add[x] = 1
    if (len(add) < 1):
        break
    rm1 = []
    for x in add:
        if add[x] < min_sup:
            rm1.append(x)
    for x in rm1:
        add.pop(x)
    if (len(add) < 1):
        break
    for x in add:
        sup[x] = add[x]  ##update the values in add to sup
# get final sup
def sortPrint(st):
    l = []
    for x in st:
        s =str(sup[x]) + ' [' + x + ']'
        l.append(s)
    l.sort(key = lambda x: (-int(x[0]),x[3:-1]))
    
    for x in l:
        print(x)
sortPrint(sup)
print('')
# print for question 1, but need update     


closed = {}
for x in sup:
    support = sup[x]
    ele = set(x.split(' '))
    if support not in closed:
        closed[support] = [ele]
    else:
        cnt = 0
        minus = []
        l = closed[support]
        for s in l:
            if s >= ele:
                cnt += 1
                break
            if s < ele:
                minus.append(s)
        if len(minus) > 0:
            for x in minus:
                l.remove(x)
        if cnt == 0:
            l.append(ele)
closed2 = {}
for x in closed:
    for y in closed[x]:
        l = list(y)
        l.sort()
        stt = ' '.join(l)
        closed2[stt] = x
sortPrint(closed2)
print('')
#get the closed frequent itemset
max = []
for x in closed2:
    max.append(x)
tmpl = set()
for x in max:
    for y in max:
        if set(x.split(' ')) > set(y.split(' ')):
            tmpl.add(y)

for x in tmpl:
    max.remove(x)
sortPrint(max)    
# get the maximal frequent itemset

