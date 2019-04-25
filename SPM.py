import sys

def SortSFP(PTs):
    opts = []
    for PT in PTs:
        temp = []
        temp.append(PTs[PT])
        temp.append(PT)
        opts.append(temp)
    opts.sort(key=lambda x: (-x[0], x[1]))
    return (opts)

def main():
    min_sup = 2
    input_data = []
    seqs = []
    subseqs = []
    SFP = {}

    for row in sys.stdin:
        if "\n" in row:
            input_data.append(row[:-1])
        else:
            input_data.append(row)

    for x in input_data:
        temp = x.split(" ")
        seqs.append(temp)

    nrow = len(seqs)
    for i in range(nrow):
        nelem = len(seqs[i])
        for j in range(nelem):
            temp = seqs[i][j]
            l = nelem - j
            if (l > 5):
                k = 1
                while (k < 5):
                    temp = temp + " " + seqs[i][j+k]
                    subseqs.append(temp)
                    k = k + 1
            else:
                k = 1
                while (k < l):
                    temp = temp + " " + seqs[i][j+k]
                    subseqs.append(temp)
                    k = k + 1

    for x in subseqs:
        temp = x.split(" ")
        if (len(temp) > 5):
            subseqs.remove(x)

    for x in subseqs:
        if x in SFP:
            SFP[x] += 1
        else:
            SFP[x] = 1

    for key, value in dict(SFP).items():
        if value < min_sup:
            del SFP[key]

    res = SortSFP(SFP)
    for x in range(20):
        if x >= len(res):
            break
        print(res[x])

if __name__ == "__main__":
    main()