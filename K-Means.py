import sys
import copy
# initialization
input_data = []
for row in sys.stdin:
    if "\n" in row:
        input_data.append(row[:-1])
    else:
        input_data.append(row)

N = int(input_data[0].split(" ")[0])
k = int(input_data[0].split(" ")[1])
tail = input_data[-1].split(" ")[-1]
if (tail == ""):
    D = len(input_data[-1].split(" ")) - 1
else:
    D = len(input_data[-1].split(" "))
samples = [[]] * N
centroids = {}

# get points
for i in range(1, N + 1):
    temp = []
    sample = input_data[i].split(" ")
    for j in range(D):
        temp.append(float(sample[j]))
    temp.append(0)
    samples[i - 1] = temp
# get centroids
for i in range(N + 1, N + 1 + k):
    temp = []
    centroid = input_data[i].split(" ")
    for j in range(D):
        temp.append(float(centroid[j]))
    centroids[i - N - 1] = temp

# cluster sample points
def Clustering(samps, cents):
    for x in samps:
        dists = {}
        for y in cents:
            dist = 0
            for i in range(D):
                diff = (x[i] - cents[y][i]) ** 2
                dist += diff
            dists[y] = dist
        Min = 0
        for c in dists:
            if (dists[c] < dists[Min]):
                Min = c
        for c in dists:
            if (dists[c] == dists[Min]):
                if (c < Min):
                    Min = c
        x[-1] = Min
    return samps

# re-assign centroids
def AssignCents(samps, cents):
    Cents = cents
    for x in cents:
        for i in range(D):
            cor = 0
            n = 0
            for y in samps:
                if (y[-1] == x):
                    n += 1
                    cor += y[i]
            if (n == 0):
                Cents[x][i] = 0
            else:
                Cents[x][i] = cor / n
    return Cents


if __name__ == "__main__":
    cond = True
    while (cond == True):
        temp = copy.deepcopy(centroids)
        samples = Clustering(samples, centroids)
        centroids = AssignCents(samples, centroids)
        if (temp != centroids):
            cond = True
        else:
            cond = False
    for x in samples:
        print(x[-1])