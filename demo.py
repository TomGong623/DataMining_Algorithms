import sys
import math

input_data = []

for row in sys.stdin:
    if "\n" in row:
        input_data.append(row[:-1])
    else:
        input_data.append(row)

N = int(input_data[0].split(" ")[0])
k = int(input_data[0].split(" ")[1])
Inputs = [[]] * N
centroids = [[]] * k

# get points
for i in range(1, N+1):
    x = float(input_data[i].split(" ")[0])
    y = float(input_data[i].split(" ")[1])
    Inputs[i-1] = [x, y]
# get centroids
for i in range(N+1, N+1+k):
    x = float(input_data[i].split(" ")[0])
    y = float(input_data[i].split(" ")[1])
    centroids[i-N-1] = [x, y]
