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
def stirling(n, k):
    if n == k:
        return 1
    if n == 0 or k == 0 : return 0

    return k*stirling(n - 1, k) + stirling(n - 1, k - 1)


def generatorPartition(n,k):
    if n == k:
        return [[i] for i in range(1, n + 1)]
    if k > n or n == k:
        return []
    if n == 0 and k == 0:
        return []
    val = random.randint(1, stirling(n, k))
    if val <= stirling(n - 1, k - 1):
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
    if r < stirling(n - 1, k - 1):
        partition = generatorPartition_unranking(n - 1, k - 1, r)
        partition.append([n])
        return partition
    else:
        r = r - stirling(n - 1, k - 1)
        bloc, r = (r // stirling(n - 1, k), r % stirling(n - 1, k))

        partition = generatorPartition_unranking(n - 1, k, r)

        partition[bloc].append(n)
        return partition


def BellNumber(n,k):
    if n == 0:
        return 1
    else:
        sum = 0
        for i in range(0,k+1):
            sum += stirling(n, i)
        return sum

def Bellnumber_partition_unranking(n,k,r):
    index = 0
    for i in range(1,k+1):
        r = r - stirling(n, i)
        if r < 0 :
            index = i
            r = r + stirling(n, i)
            break
    return generatorPartition_unranking(n,index,r)

"""
    LEXICAL GENERATION
"""

def R_prefix(n,k,l,d0,d1):
    left_sum = U_func(n-l, k-1, d0 -l)
    right_sum = U_func(n-l, k-1, (d1+1)-l)
    return left_sum - right_sum

def U_func(n,k,d):
    upper_bound_1 = n
    total = 0
    for u in range(0, upper_bound_1 + 1):
        for i in range(1, (k+1) + 1): # plus one in the end to count that variable
            total += stirling(n - u, i - 1) * RecComb(n - d, u)
    return total

def extract(n, res ) :
    l = [i for i in range(1,n+1)]
    p = []
    for r in res:
        q = []
        for i in r:
            q.append(l.pop(i))
            #
        p.append(q)
    return p


def next_block(n, k, r):
    if k <= 1:
        block = []
        block.extend([0] * n)
        return block, 0

    block = [0]
    acc = BellNumber(n-1, k-1)
    if r < acc:
        return block,0

    d0 = 1
    index = 2
    inf = 2
    sup = n
    complete = False

    while not complete:
        while inf < sup:
            mid = (inf + sup) // 2
            if r >= acc + R_prefix(n, k, index-1, d0, mid-1):
                inf = mid + 1
            else:
                sup = mid

        mid = inf
        threshold = BellNumber(n - index, k - 1)
        acc += R_prefix(n, k, index-1, d0, mid - 2)

        block.append(mid - index)
        if r < threshold + acc:
            complete = True
        else:
            index += 1
            d0 = mid
            inf = d0 + 1
            sup = n
            acc += threshold

    return (block, acc)


def unranking_lexico(n, k, r):
    n2 = n
    res = []
    while n > 0 and k > 0:
        b, new_r = next_block(n, k, r)
        res.append(b)
        r -= new_r
        n -= len(b)
        k -= 1

    res = extract(n2, res)
    return res

n = 4
k = 3


print("Number of partitions : " ,BellNumber(n,k))
print("-----GENERATED WITH UNRANKING ------")
for j in range(BellNumber(n,k)):
    print(j,"",Bellnumber_partition_unranking(n,k,j))

print("-------LEXICALLY ORDERED-------")
for i in range(0, BellNumber(n,k)):
    print(i,"",unranking_lexico(n, k, i))

