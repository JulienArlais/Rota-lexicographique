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
    return generatorPartition_unranking(n,k,r)

def generatorPartition_unranking(n,k,r):
    if n == k:
        return [[i] for i in range(1, n + 1)]
    if k > n or n == k:
        return []
    if n == 0 and k == 0:
        return []
    if r < RecPart(n-1, k-1):
        partition = generatorPartition_unranking(n - 1, k - 1, r)
        partition.append([n])  # Add n as a new subset
        return partition
    else:
        r = r - RecPart(n-1,k-1)
        bloc, r = (r//RecPart(n-1,k), r%RecPart(n-1,k))

        partition = generatorPartition_unranking(n - 1, k, r)

        partition[bloc].append(n)
        return partition


def fisherYates(l):
    for i in range (len(l)-1):
        r = random.randint(i,len(l)-1)
        tmp = l[i]
        l[i] = l[r]
        l[r] = tmp
    return l


def Ordered_Partition(n,k):
    return fact(k) * RecPart(n,k)

def Aux_Ordered_Partition_gen(n,k,r):
    return fisherYates(generatorPartition_unranking(n,k,r))
def Ordered_Partition_gen(n,k):
    r = Ordered_Partition(n,k)
    return Aux_Ordered_Partition_gen(n,k,r)


def uniformOrderedPart(n,k):
    l = []
    for i in range (1000000) :
        sl = Ordered_Partition_gen(n,k)
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
    return l
print(Ordered_Partition(4,2))

uniformOrderedPart(4,2)