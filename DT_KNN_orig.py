import sys
import math

# initialization
input_data = []
training = []
testing = []
ginis = []
attrs = []
list_attrs = []
SplitPoints = []
len_sps = []

# read input data
for row in sys.stdin:
    if "\n" in row:
        input_data.append(row[:-1])
    else:
        input_data.append(row)

# get training samples and testing samples
for x in input_data:
    temp = x.split(" ")
    if (temp[0] != '0'):
        training.append(temp)
    else:
        testing.append(temp)

# get attributes
nattr = len(training[0]) - 1
for i in range(1, nattr + 1):
    attr = training[0][i].split(":")
    attrs.append(attr[0])

# get attribute values
for i in range(1, nattr + 1):
    set_temp = set()
    for x in training:
        temp = x[i].split(":")
        set_temp.add(float(temp[1]))
    list_temp = list(set_temp)
    sorted(list_temp)
    list_temp.append(training[0][i].split(":")[0])
    list_attrs.append(list_temp)


# get labels
def get_lables(sample):
    set_label = set()
    for x in sample:
        set_label.add(x[0])
    labels = list(set_label)
    return (labels)


Labels = get_lables(training)
nlabel = len(Labels)


### Decision Tree ################################################
# get splitpoints
def GetSplitPoint(List):
    splitpoints = []
    for i in range(len(List) - 2):
        splitpoint = [(List[i] + List[i + 1]) / 2, List[-1]]
        splitpoints.append(splitpoint)
    return (splitpoints)


for x in list_attrs:
    splitpoint = GetSplitPoint(x)
    len_sps.append(len(splitpoint))
    SplitPoints = SplitPoints + splitpoint


# get gini index
def GetGinis(SPs, samples):
    ginis = []
    for x in SPs:
        nl, nr = 0, 0
        L = {}
        R = {}
        for k in Labels:
            L[k] = 0
        for k in Labels:
            R[k] = 0
        for y in samples:
            for i in range(1, nattr + 1):
                temp = y[i].split(":")
                if (temp[0] == x[1]):
                    if (float(temp[1]) < x[0]):
                        nl += 1
                        for k in Labels:
                            if (y[0] == k):
                                if k in L:
                                    L[k] += 1
                                else:
                                    L[k] = 1
                    elif (float(temp[1]) > x[0]):
                        nr += 1
                        for k in Labels:
                            if (y[0] == k):
                                if k in R:
                                    R[k] += 1
                                else:
                                    R[k] = 1
        left = 1
        right = 1
        n = nl + nr
        for k in Labels:
            left = left - (L[k] / nl) ** 2
            right = right - (R[k] / nr) ** 2
        gini = (nl / n) * left + (nr / n) * right
        ginis.append(gini)
    return ginis


Ginis = GetGinis(SplitPoints, training)


def Get_Min(ginis, SPs):
    min_index = 0
    for i in range(len(ginis)):
        if ginis[i] < ginis[min_index]:
            min_index = i
    gini_min_sp = SPs[min_index]
    return (gini_min_sp)


root = Get_Min(Ginis, SplitPoints)


# get leaf nodes
def get_leafnodes(sample, sp):
    lsample = []
    rsample = []
    for x in sample:
        for i in range(1, nattr + 1):
            temp = x[i].split(":")
            if (temp[0] == sp[1]):
                if (float(temp[1]) < sp[0]):
                    lsample.append(x)
                elif (float(temp[1]) > sp[0]):
                    rsample.append(x)
    return (lsample, rsample)


def DecisionTree(SPs, train):
    rootGinis = GetGinis(SPs, train)
    root = Get_Min(rootGinis, SPs)
    for i in range(len(SPs)):
        if SPs[i] == root:
            del SPs[i]
            break
    Lsample, Rsample = get_leafnodes(train, root)
    Llabels = get_lables(Lsample)
    Rlabels = get_lables(Rsample)
    if (len(Llabels) > 1):
        Llabel = None
        LnodeGinis = GetGinis(SPs, Lsample)
        Lnode = Get_Min(LnodeGinis, SPs)
        LLsample, LRsample = get_leafnodes(Lsample, Lnode)
        LLlabels = get_lables(LLsample)
        if (len(LLlabels) > 1):
            temp = {}
            for x in LLlabels:
                if x in temp:
                    temp[x] += 1
                else:
                    temp[x] = 1
            LLlabel = LLlabels[0]
            for y in temp:
                if temp[y] > temp[LLlabel]:
                    LLlabel = y
        elif (len(LLlabels) == 1):
            LLlabel = LLlabels[0]
        LRlabels = get_lables(LRsample)
        if (len(LRlabels) > 1):
            temp = {}
            for x in LRlabels:
                if x in temp:
                    temp[x] += 1
                else:
                    temp[x] = 1
            LRlabel = LRlabels[0]
            for y in temp:
                if temp[y] > temp[LRlabel]:
                    LRlabel = y
        elif (len(LRlabels) == 1):
            LRlabel = LRlabels[0]
    elif (len(Llabels) == 1):
        Llabel = Llabels[0]
        Lnode = None
        LLlabel = None
        LRlabel = None
    if (len(Rlabels) > 1):
        Rlabel = None
        RnodeGinis = GetGinis(SPs, Rsample)
        Rnode = Get_Min(RnodeGinis, SPs)
        RLsample, RRsample = get_leafnodes(Rsample, Rnode)
        RLlabels = get_lables(RLsample)
        if (len(RLlabels) > 1):
            temp = {}
            for x in RLlabels:
                if x in temp:
                    temp[x] += 1
                else:
                    temp[x] = 1
            RLlabel = RLlabels[0]
            for y in temp:
                if temp[y] > temp[RLlabel]:
                    RLlabel = y
        elif (len(RLlabels) == 1):
            RLlabel = RLlabels[0]
        RRlabels = get_lables(RRsample)
        if (len(RRlabels) > 1):
            temp = {}
            for x in RRlabels:
                if x in temp:
                    temp[x] += 1
                else:
                    temp[x] = 1
            RRlabel = RRlabels[0]
            for y in temp:
                if temp[y] > temp[RRlabel]:
                    RRlabel = y
        elif (len(RRlabels) == 1):
            RRlabel = RRlabels[0]
    elif (len(Rlabels) == 1):
        Rlabel = Rlabels[0]
        Rnode = None
        RLlabel = None
        RRlabel = None
    DT_list = [root, Lnode, Rnode, Llabel, Rlabel, LLlabel, LRlabel, RLlabel, RRlabel]
    return (DT_list)

DT = DecisionTree(SplitPoints, training)

def prediction(point, DT):
    for i in range(1, nattr + 1):
        feat = point[i].split(":")
        if (feat[0] == DT[0][1]):
            if (float(feat[1]) < DT[0][0]):
                if (DT[1] == None):
                    pl = DT[3]
                else:
                    for j in range(1, nattr + 1):
                        temp = point[j].split(":")
                        if (temp[0] == DT[1][1]):
                            if (float(temp[1]) < DT[1][0]):
                                pl = DT[5]
                            elif (float(temp[1]) > DT[1][0]):
                                pl = DT[6]
            elif (float(feat[1]) > DT[0][0]):
                if (DT[2] == None):
                    pl = DT[4]
                else:
                    for j in range(1, nattr + 1):
                        temp = point[j].split(":")
                        if (temp[0] == DT[2][1]):
                            if (float(temp[1]) < DT[2][0]):
                                pl = DT[7]
                            elif (float(temp[1]) > DT[2][0]):
                                pl = DT[8]
    return (pl)


for test in testing:
    pred_label = prediction(test, DT)
    print(pred_label)

### KNN ##########################################
print('')

# get distances between testing point and training points
def get_distance(point):
    dists = []
    for x in training:
        dist_sq = 0
        for i in range(1, nattr + 1):
            temp_train = float(x[i].split(":")[1])
            temp_test = float(point[i].split(":")[1])
            diff = (temp_test - temp_train) ** 2
            dist_sq = dist_sq + diff
        dist = [math.sqrt(dist_sq), x[0]]
        dists.append(dist)
    return (dists)


# predict label for each testing point
for test in testing:
    Ys = {}
    distances = get_distance(test)
    # sort distances by ascending order
    nrow = len(distances)
    for i in range(nrow - 1):
        for j in range(nrow - i - 1):
            if (distances[j][0] > distances[j + 1][0]):
                temp = distances[j + 1]
                distances[j + 1] = distances[j]
                distances[j] = temp
    # sort equal distances
    for i in range(nrow - 1):
        if (distances[i][0] == distances[i + 1][0]):
            l_1 = distances[i][1]
            l_2 = distances[i + 1][1]
            if (float(l_1) > float(l_2)):
                temp = distances[i + 1]
                distances[i + 1] = distances[i]
                distances[i] = temp
    distances = distances[0:3]
    for dist in distances:
        if dist[1] in Ys:
            Ys[dist[1]] += 1
        else:
            Ys[dist[1]] = 1
    Ys_list = list(Ys.keys())
    Ys_list.sort()
    Max = Ys_list[0]
    for y in Ys_list:
        if Ys[y] > Ys[Max]:
            Max = y
    print(Max)