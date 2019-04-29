import sys

input_data = []
dists = {}
clusters = {}
results = {}

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

# get points
for i in range(1, N + 1):
    temp = []
    sample = input_data[i].split(" ")
    for j in range(D):
        temp.append(float(sample[j]))
    temp.append(i - 1)
    samples[i - 1] = temp
    clusters[i - 1] = [i - 1]

for i in range(N):
    for j in range(i + 1, N):
        dist = 0
        for z in range(D):
            diff = (samples[i][z] - samples[j][z]) ** 2
            dist += diff
        dists[dist] = [i, j]

while (len(clusters) > k):
    rm = None
    Min = list(dists.keys())[0]
    for dist in dists:
        if (dist < Min):
            Min = dist
    head = dists[Min][0]
    link = dists[Min][1]
    for c in clusters:
        if (head in clusters[c] and link not in clusters[c]):
            for d in clusters:
                if (link in clusters[d]):
                    clusters[c] = clusters[c] + clusters[d]
                    rm = d
    if (rm != None):
        clusters.pop(rm)
    dists.pop(Min)

for x in clusters:
    Min = clusters[x][0]
    for y in clusters[x]:
        if (y < Min):
            Min = y
    results[Min] = clusters[x]

for x in samples:
    for c in results:
        if (x[-1] in results[c]):
            print(c)
