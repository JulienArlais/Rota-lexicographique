import random
import functools
import sys

@functools.lru_cache(maxsize=None)
def RecPart11(k, n):
    if k < n: 
        return 0
    if k == n or n == 1:
        return 1
    return RecPart11(k - 1, n - 1) + RecPart11(k - 1, n)

def partGen11(k, n):
    if k < n:
        raise ValueError("k doit être >= à n")
    l = [[i+1] for i in range(n)]
    return auxPartGen11(k - n, n, l)

def auxPartGen11(k, n, l):
    if k == 0:
        return l
    r = random.randint(0, n - 1)
    l[r].append(k + n)
    return auxPartGen11(k - 1, n, l)

def uniformite11(k,n):
    l = []
    for i in range (1000000) :
        sl = partGen11(k, n)
        sl2 = [len(i) for i in sl]
        inn = False
        for j in l:
            if j[0] == sl2 :
                j[1] += 1   
                inn = True
                break
        if not inn :
            l.append([sl2, 1])
    for j in l:
        print("p( ", j[0], " ) = ", j[1]/10000)

if (len(sys.argv) != 3) :
    raise TypeError("Il faut 2 arguments : k suivi de n (k>=n)")
k = int(sys.argv[1])
n = int(sys.argv[2])
print("Nb : ", RecPart11(k,n))
print(uniformite11(k,n))