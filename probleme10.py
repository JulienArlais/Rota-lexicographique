import random
import functools
import sys

@functools.lru_cache(maxsize=None)
def RecPart10(k, n):
    return 0

def partGen10(k,n):
    if k < n :
        raise ValueError("k doit être >= à n")
    l = [ [] for i in range (n)]
    return auxPartGen10(k,n,l)

def auxPartGen10(k,n,l):
    if k == 0:
        return l
    r = random.randint(0, n-1)
    l[r].append(k)
    return auxPartGen10(k-1,n,l)

def uniformite10(k,n):
    l = []
    for i in range (1000000) :
        sl = partGen10(k, n)
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
print("Nb : ", RecPart10(k,n))
print(uniformite10(k,n))