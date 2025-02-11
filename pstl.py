import functools
import random
import sys

def fact(i):
    if i == 00 or i == 1:
        return 1
    else:
        return i * fact(i-1)

@functools.lru_cache(maxsize=None)
def RecPart(n,k):
    if n == 0 or k == 0 : return 0
    if n == k:
        return 1

    return k*RecPart(n-1, k) + RecPart(n-1, k-1)

def generatorPartition(n,k):
    if k > n :
        raise TypeError("k > n")
    r = random.randint(1, RecPart(n, k))
    return auxPartition(n,k,r)

def auxPartition(n,k,r):
    if n == k:
        return [[i] for i in range(1, n + 1)]

    if r <= RecPart(n-1, k-1):
        partition = auxPartition(n - 1, k - 1, r)
        partition.append([n])
        return partition
    else:
        partition = auxPartition(n - 1, k, r - RecPart(n-1, k-1))
        rand_spot = random.randint(0, k-1)
        partition[rand_spot].append(n)
        return partition

print(generatorPartition(8,4))


"""
Ordered Partitions
Called Fubini numbers / Ordered Bell Numbers
P(n,k) = k! * S(n,k)

Recurrence call = 
P(n,k) = k* P(n-1,k) + P(n-1,k-1)
"""

def recOrdPart(n,k):
    return fact(k)*RecPart(n,k)

def generatorOrderedPartition(n,k):
    return fisherYates(generatorPartition(n,k))

def fisherYates(l):
    for i in range (len(l)-1):
        r = random.randint(i,len(l)-1)
        tmp = l[i]
        l[i] = l[r]
        l[r] = tmp
    return l

def uniformite(n,k):
    l = []
    for i in range (1,1000000) :
        sl = generatorPartition(n,k)
        inn = False
        for j in l:
            if j[0] == sl :
                j[1] += 1
                inn = True
                break
        if not inn :
            l.append([sl, 0])
    for j in l:
        print("p( ", j[0], " ) = ", j[1]/10000)



if (len(sys.argv) != 3) :
    raise TypeError("Il faut 2 arguments : n suivi de k")
n = int(sys.argv[1])
k = int(sys.argv[2])
print("Nb de combinaisons : ", RecPart(n,k))
uniformite(n,k)
