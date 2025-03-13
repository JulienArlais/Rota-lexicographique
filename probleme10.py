import random
import functools
import sys

"""
 idk if my uniformity is correct
 
"""
@functools.lru_cache(maxsize=None)
def P(n, k):
    """ Computes the number of ways to partition n into k positive parts. """
    if k == 0:
        return 0
    if k > n:
        return 0  # Cannot partition if more parts than elements
    if k == n or k == 1:
        return 1  # Only one way to split n into n parts (1+1+...+1) or one part (n)
    return P(n-1, k-1) + P(n-k, k)

def P_generator(n, k, r):
    """ Generates a partition of n into k parts. """
    if k > n :
        return []
    if k <= 0 :
        return []
    if k == 1:
        return [n]
    if k == n:
        return [1] * n
    # Randomly pick between the two cases, weighted by number of partitions
    if r <= P(n - 1, k - 1):
        return [1] + P_generator(n - 1, k - 1, r)
    else:
        r = r - P(n - 1, k - 1)
        partition = P_generator(n - k, k, r)
        return [x + 1 for x in partition]  # Shift partition to ensure positivity

def Generator(n,k,r):
    index = 0
    for i in range(1,k+1):
        r = r - P(n,i)
        if r < 0:
            index = i
            r = r + P(n , i)
            break

    return P_generator(n,index,r)

def Un_P(n,k):
    return P(n+k,k)
    # sum = 0
    # for i in range(1,k+1):
    #     sum += P(n,i)
    # return sum

n = 8
k = 3
print("Nb : ", Un_P(n,k))

# Test de l'unranking
for j in range(0, Un_P(n,k)):
    print(Generator(n,k,j))


def gen_unranking(n,k):
    r = random.randint(0, Un_P(n,k))
    return Generator(n,k,r)

def uniformite10(n,k):
    l = []
    for i in range (1000000) :
        sl = gen_unranking(n, k)
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

uniformite10(5,3)

