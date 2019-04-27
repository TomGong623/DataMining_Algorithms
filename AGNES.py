import sys

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

# get points
for i in range(1, N + 1):
    temp = []
    sample = input_data[i].split(" ")
    for j in range(D):
        temp.append(float(sample[j]))
    temp.append(i - 1)
    samples[i - 1] = temp

for x in samples:
    print(x)

for i in range(N):
    for j in range(i, N):