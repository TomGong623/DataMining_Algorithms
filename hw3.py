import sys
import math
L = []
Test = []
length = 0
label = []
#all dataset
for line in sys.stdin:
    length += 1
    if '\n' in line:
        subline = line[:-1]
        a = subline.split(' ')
        L.append(a)
    else:
        b = line.split(' ')
        L.append(b)
#test case
for i in range(length):
    if L[length - i - 1][0] =='0':
        c = L.pop()
        Test.insert(0, c)

#training dataset
for i in range(1, len(L[0])):
    for line in L:
        line[i] = line[i].split(':')
        line[i][1] = float(line[i][1])
    
#build tree
class Tree:
    def __init__(self, value=None, leftBranch=None, rightBranch=None, results=None, col=0, data=None):
        self.value = value
        self.leftBranch = leftBranch
        self.rightBranch = rightBranch
        self.results = results
        self.col = col
        self.data = data

#decision tree functions
def calculateDiffCount(datas):
        results = {}
        for data in datas:
            if data[0] not in results:
                results[data[0]] = 1
            else:
                results[data[0]] += 1
        return results

def gini(rows):
        length = len(rows)
        results = calculateDiffCount(rows)
        imp = 0.0
        for i in results:
            imp += results[i] / length * results[i] / length
        return 1 - imp
    
def splitDatas(rows, value, col):
        list1 = []
        list2 = []
        for row in rows:
            if (row[col][1] >= value):
                list1.append(row)
            else:
                list2.append(row)
        return (list1, list2)
    
def buildDecisionTree(rows, level, evaluationFunction=gini):
        currentGain = evaluationFunction(rows)
        column_length = len(rows[0])
        rows_length = len(rows)
        best_gain = 0.0
        best_value = None
        best_set = None

        
        for col in range(1, column_length):
            col_value_set = set([x[col][1] for x in rows])
            col_value_list = []
            for value in col_value_set:
                col_value_list.append(value)
            col_value_list.sort()
            split_list = []
            for i in range(len(col_value_list) - 1):
                mid = (col_value_list[i] + col_value_list[i + 1]) / 2
                split_list.append(mid)
            for value in split_list:
                list1, list2 = splitDatas(rows, value, col)
                p = len(list1) / rows_length
                gain = currentGain-p*evaluationFunction(list1)-(1-p)*(evaluationFunction(list2))
                if gain > best_gain:
                    best_gain = gain
                    best_value = (col, value)
                    best_set = (list1, list2)
                    
        if  level < 2 and best_gain > 0:
            leftBranch = buildDecisionTree(best_set[0], level + 1, evaluationFunction)
            rightBranch = buildDecisionTree(best_set[1], level + 1, evaluationFunction)
            return Tree(col=best_value[0], value=best_value[1], leftBranch=leftBranch, rightBranch=rightBranch)
        else:
            return Tree(results=calculateDiffCount(rows), data=rows)

def classify(data, tree):
    if tree.results != None:
        return tree.results
    else:
        branch = None
        v = data[tree.col][1]
        if v >= tree.value:
            branch = tree.leftBranch
        else:
            branch = tree.rightBranch
        return classify(data, branch)

level = 0
decisionTree = buildDecisionTree(L, level, evaluationFunction=gini)

#classify test case
for i in range(1, len(Test[0])):
    for line in Test:
        line[i] = line[i].split(':')
        line[i][1] = float(line[i][1])
for item in Test:
    a = classify(item, decisionTree)
    value_1 = max(a, key=a.get)
    print(value_1)

print()

#K-NN functions
def get_distance(point):
    dists = []
    for x in L:
        dist_sq = 0
        for i in range(1, len(L[0])):
            temp_train = float(x[i][1])
            temp_test = float(point[i][1])
            diff = (temp_test - temp_train)**2
            dist_sq = dist_sq + diff
        dist = [math.sqrt(dist_sq), x[0]]
        dists.append(dist)
    return(dists)

# predict label for each testing point 
for test in Test:
    Ys = {}
    distances = get_distance(test)
    # sort distances by ascending order
    nrow = len(distances)
    for i in range(nrow - 1):
        for j in range(nrow - i - 1):
            if (distances[j][0] > distances[j+1][0]):
                temp = distances[j+1]
                distances[j+1] = distances[j]
                distances[j] = temp
    # sort equal distances
    for i in range(nrow - 1):
        if (distances[i][0] == distances[i+1][0]):
            l_1 = distances[i][1]
            l_2 = distances[i+1][1]
            if (float(l_1) > float(l_2)):
                temp = distances[i+1]
                distances[i+1] = distances[i]
                distances[i] = temp
    distances = distances[0:3]
    for dist in distances:
        if dist[1] in Ys:
            Ys[dist[1]] += 1
        else:
            Ys[dist[1]] = 1
    t = True
    l = []
    for value in Ys.values():
        if value != 1:
            t = False
    if t == True:
        for key in Ys.keys():
            l.append(key)
        l.sort()
        print(l[0])
    else:
        Max = list(Ys)[0]
        for y in Ys:
            if Ys[y] > Ys[Max]:
                Max = y
        print(Max)
