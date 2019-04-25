import math

def entropy(a, b):
    info = -(a/(a+b))*math.log2(a/(a+b)) - (b/(a+b))*math.log2(b/(a+b))
    return info

def Gini(a, b):
    gini = 1 - (a/(a+b))**2 - (b/(a+b))**2
    return gini





