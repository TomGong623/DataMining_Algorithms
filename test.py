import sys
import math

# initialization
input_data = []
training = []
testing = []
SplitPoints = []

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


### Decision Tree ####################
class DTree:
    def __init__(self, sp=None, Lbranch=None, Rbranch=None, labels=None, feat=0, Input=None):
        self.sp = sp
        self.Lbranch = Lbranch
        self.Rbranch = Rbranch
        self.labels = labels
        self.feat = feat
        self.Input = Input


def get_labelcounts(sample):
    labels = {}
    for x in sample:
        if x[0] in labels:
            labels[x[0]] += 1
        else:
            labels[x[0]] = 1
    return (labels)


def get_gini(sample):
    nrow = len(sample)
    labels = get_labelcounts(sample)
    gini = 1
    for x in labels:
        gini = gini - (labels[x] / nrow) ** 2
    return (gini)


def GetSplitPoint(List):
    splitpoints = []
    for i in range(len(List) - 1):
        splitpoint = (List[i] + List[i + 1]) / 2
        splitpoints.append(splitpoint)
    return (splitpoints)


def Split(sample, value, feat):
    list_L = []
    list_R = []
    for x in sample:
        temp = x[feat].split(":")
        if (float(temp[1]) < value):
            list_L.append(x)
        else:
            list_R.append(x)
    return (list_L, list_R)


def BuildDT(sample, depth):
    gini_D = get_gini(sample)
    col_length = len(sample[0])
    nrows = len(sample)
    max_gain = 0
    best_sp = None
    best_set = None
    for feat in range(1, col_length):
        set_feats = set()
        for x in sample:
            temp = x[feat].split(":")
            set_feats.add(float(temp[1]))
        list_feats = list(set_feats)
        list_feats.sort()
        SplitPoints = GetSplitPoint(list_feats)
        for sp in SplitPoints:
            listL, listR = Split(sample, sp, feat)
            p = len(listL) / nrows
            InfoGain = gini_D - p * get_gini(listL) - (1 - p) * get_gini(listR)
            if InfoGain > max_gain:
                max_gain = InfoGain
                best_sp = [feat, sp]
                best_set = [listL, listR]
    if (depth < 2 and max_gain > 0):
        LBranch = BuildDT(best_set[0], depth + 1)
        RBranch = BuildDT(best_set[1], depth + 1)
        return (DTree(feat=best_sp[0], sp=best_sp[1], Lbranch=LBranch, Rbranch=RBranch))
    else:
        return (DTree(labels=get_labelcounts(sample), Input=sample))


def Classifier(test, DT):
    if DT.labels == None:
        branch = None
        value = float(test[DT.feat].split(":")[1])
        if value >= DT.sp:
            branch = DT.Rbranch
        else:
            branch = DT.Lbranch
        return (Classifier(test, branch))
    else:
        return (DT.labels)


DecisionTree = BuildDT(training, depth=0)

for x in testing:
    Labels = Classifier(x, DecisionTree)
    Class = max(Labels, key=Labels.get)
    print(Class)

print("")


### KNN ####################
# get distances between testing point and training points
def get_distance(point):
    dists = []
    for x in training:
        dist_sq = 0
        for i in range(1, len(x)):
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
