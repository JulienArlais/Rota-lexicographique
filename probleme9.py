import random
import functools

@functools.lru_cache(maxsize=None)
def RecComb(n, k):
    if n == k :
        return 1
    elif k == 0:
        return 1
    elif(n <= 0 or k > n):
        return 0
    else:
        return RecComb(n-1,k-1) + RecComb(n-1, k)


"""
 recursive call is 
 B(n,k) = Sum (n,k) Bk , where k goes from 0 to n-1
 partition 
"""


def fact(i):
    if i == 00 or i == 1:
        return 1
    else:
        return i * fact(i-1)


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
        return partition
    else:
        partition = generatorPartition(n - 1, k)

        rand_spot = random.randint(0, k-1)
        partition[rand_spot].append(n)
        return partition


def partitions_gen(n,k):
    r = random.randint(1, RecPart(n, k) - 1)
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
        partition.append([n])
        return partition
    else:
        r = r - RecPart(n-1,k-1)
        bloc, r = (r//RecPart(n-1,k), r%RecPart(n-1,k))

        partition = generatorPartition_unranking(n - 1, k, r)

        partition[bloc].append(n)
        return partition


def uniformite9(n,k):
    l = []
    for i in range (1000000) :
        sl = generatorPartition(n, k)
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

n = 5
k = 3
print("Nb : ", RecPart(n,k))

# Test de la fonction naive
uniformite9(n,k)

# Test de l'unranking
for i in range(0,RecPart(n,k)):
    print(generatorPartition_unranking(n,k,i))