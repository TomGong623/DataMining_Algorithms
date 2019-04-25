import sys

def GetFPCandidates(set_low):
    cands = set()
    for x in set_low:
        for y in set_low:
            templist = []
            List_x = x.split(" ")
            List_x.sort()
            List_y = y.split(" ")
            List_y.sort()
            l = len(List_x)
            if (List_x[l - 1] == List_y[l - 1]):
                pass
            else:
                for i in range(l - 1):
                    if (List_x[i] != List_y[i]):
                        break
                    else:
                        templist.append(List_x[i])
                templist.append(List_x[l - 1])
                templist.append(List_y[l - 1])
            templist.sort()
            if (len(templist) == l + 1):
                cands.add(" ".join(templist))
    return cands

def GetFP(transac, adds, min_sup, FP):
    P1 = set()
    while True:
        for x in adds:
            P1.add(x)
        cands = GetFPCandidates(P1)
        P1.clear()
        adds.clear()
        if len(cands) == 0:
            break
        for cand in cands:
            l = cand.split(" ")
            s = set(l)
            for x in transac:
                elems = set(x)
                if s <= elems:
                    if cand in adds:
                        adds[cand] = adds[cand] + 1
                    else:
                        adds[cand] = 1
        if (len(adds) == 0):
            break
        adds = min_sup_filter(adds, min_sup)
        if (len(adds) == 0):
            break
        for x in adds:
            FP[x] = adds[x]
    return FP

def GetCP(FP, CP):
    c_cands = {}
    for x in FP:
        sup = FP[x]
        elem = set(x.split(' '))
        if sup not in c_cands:
            c_cands[sup] = [elem]
        else:
            cnt = 0
            rm = []
            cands = c_cands[sup]
            for cand in cands:
                if (cand >= elem):
                    cnt += 1
                    break
                elif (cand < elem):
                    rm.append(cand)
            if len(rm) > 0:
                for x in rm:
                    cands.remove(x)
            if cnt == 0:
                cands.append(elem)
    for x in c_cands:
        for y in c_cands[x]:
            list_cpt = list(y)
            list_cpt.sort()
            cpt = ' '.join(list_cpt)
            CP[cpt] = x
    return CP

def GetMP(CP, MP):
    for x in CP:
        MP[x] = CP[x]
    tmp = set()
    for x in MP:
        for y in MP:
            if set(x.split(' ')) > set(y.split(' ')):
                tmp.add(y)
    for x in tmp:
        MP.pop(x)
    return MP

def SortPrint(PTs):
    l = []
    for PT in PTs:
        s = str(PTs[PT]) + ' [' + PT + ']'
        l.append(s)
    l.sort(key=lambda x: (-int(x[0]), x[3:-1]))
    for x in l:
        print(x)

def min_sup_filter(FP, min_sup):
    for key, value in dict(FP).items():
        if value < min_sup:
            del FP[key]
    return FP

def main():
    # Initialization
    input_data = []
    transac = []
    FP = {}
    CP = {}
    MP = {}
    for row in sys.stdin:
        if "\n" in row:
            input_data.append(row[:-1])
        else:
            input_data.append(row)
    min_sup = int(input_data[0])
    input_data.remove(input_data[0])
    for i in input_data:
        temp = i.split(" ")
        transac.append(temp)
    for x in transac:
        for elem in x:
            if elem in FP:
                FP[elem] += 1
            else:
                FP[elem] = 1
    FP = min_sup_filter(FP, min_sup)
    # Get Frequent Patterns
    add = FP.copy()
    FP = GetFP(transac, add, min_sup, FP)
    SortPrint(FP)
    print('')
    # Get Closed Frequent Patterns
    CP = GetCP(FP, CP)
    SortPrint(CP)
    print('')
    # Get Maximal Frequent Patterns
    MP = GetMP(CP, MP)
    SortPrint(MP)

if __name__ == "__main__":
    main()