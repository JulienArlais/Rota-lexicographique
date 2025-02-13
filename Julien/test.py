import functools
import random
from collections import Counter

from scipy.stats import chi2_contingency
def fact(i):
    if i == 00 or i == 1:
        return 1
    else:
        return i * fact(i-1)


def fisherYates(l):
    for i in range (len(l)-2):
        j = 0
        while i <= j < (len(l) - 1):
            j = random.randint(i,len(l)-1)
        l[i], l[j] = l[j], l[i]
    return l


@functools.lru_cache(maxsize=None)
def RecPart(n,k):
    if n == k:
        return 1
    if n == 0 or k == 0 : return 0

    return k*RecPart(n-1, k) + RecPart(n-1, k-1)

def generatorPartition(n,k):
    if n == k:
        return [[i] for i in range(1, n + 1)]
    if k > n or n == k:
        return []
    if n == 0 and k == 0:
        return []
    val = random.randint(1, RecPart(n, k))
    if val <= RecPart(n-1, k-1):
        partition = generatorPartition(n - 1, k - 1)
        partition.append([n])  # Add n as a new subset
        partition = fisherYates(partition)
        return partition
    else:
        partition = generatorPartition(n - 1, k)

        rand_spot = random.randint(0, k-1)
        partition[rand_spot].append(n)
        partition = fisherYates(partition)
        return partition


def aux_generator(n,k):

    return generatorPartition_unrank(n,k, random.randint(0,RecPart(n,k) - 1))
def generatorPartition_unrank(n,k,r):
    if n == k:
        return [[i] for i in range(1, n + 1)]

    threshold = RecPart(n-1,k-1)
    if r < threshold:
        partition = generatorPartition_unrank(n - 1, k - 1,r)
        partition.append([n])  # Add n as a new subset
        return fisherYates(partition)
    else:
        partition = generatorPartition_unrank(n - 1, k, r - threshold)
        rand_spot = random.randint(0, k-1)
        partition[rand_spot].append(n)
        return fisherYates(partition)
print(generatorPartition(8,4))


"""
Ordered Partitions
Called Fubini numbers / Ordered Bell Numbers
P(n,k) = k! * S(n,k)

Recurrence call = 
P(n,k) = k* P(n-1,k) + P(n-1,k-1)
"""

def uniformite(n,k):
    l = []
    for i in range (1000000) :
        sl = generatorPartition_unrank(n,k, random.randint(0, RecPart(n,k) - 1))
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


#print(generatorPartition(10,4))

n = 5
k = 2

print(uniformite(n,k))

