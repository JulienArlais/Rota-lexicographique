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


def BellNumber(n,k):
    if n == 0:
        return 1
    else:
        sum = 0
        for i in range(0,k+1):
            sum += RecPart(n,i)
        return sum

print(BellNumber(4,4))
#print(generatorPartition_unranking(5,3,0))

def Bellnumber_partition_unranking(n,k,r):
    index = 0
    for i in range(1,k+1):
        r = r - RecPart(n,i)
        if r < 0 :
            index = i
            r = r + RecPart(n , i)
            break

    return generatorPartition_unranking(n,index,r)

for j in range(15):
    print(Bellnumber_partition_unranking(4,4,j))