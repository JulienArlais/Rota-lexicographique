import random
import functools
@functools.lru_cache(maxsize=None)
def MultiCombRec(n, k):
    if k == 0:
        return 1
    elif n == k:
        return 1
    elif n <= 0 or k > n:
        return 0
    else:
        return MultiCombRec(n - 1, k) + MultiCombRec(n, k - 1)


def AuxMultiCombGen(n, k, r):
    if k > n :
        return []
    if k == 0:
        return []
    if n == 0:
        return []
    if r <= MultiCombRec(n - 1, k):
        return AuxMultiCombGen(n - 1, k, r)
    else:
        return AuxMultiCombGen(n, k - 1, r-MultiCombRec(n,k-1)) + [n]

n = 5
k = 3

def MultiCombGen(n,k):
    r = random.randint(0,MultiCombRec(n,k))
    return AuxMultiCombGen(n,k,r)

def uniformiteMultiComb(n,k):
    l = []
    for i in range (1000000) :
        sl = MultiCombGen(n, k)
        inn = False
        for j in l:
            if j[0] == sl :
                j[1] += 1
                inn = True
                break
        if not inn :
            l.append([sl, 1])
    for j in l:
        print("p( ", j[0], " ) = ", j[1]/10000)

print(uniformiteMultiComb(n,k))