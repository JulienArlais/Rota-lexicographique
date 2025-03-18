import random
import functools

# Petit souci dans la version sans unranking mais la version avec marche

@functools.lru_cache(maxsize=None)
def P(n, k):
    """ Computes the number of ways to partition n into k positive parts. """
    if k == 0 or k > n:
        return 0
    if k == n or k == 1:
        return 1
    return P(n - 1, k - 1) + P(n - k, k)

def Un_P(n, k):
    return P(n+k, k)
    # sum = 0
    # for i in range(1,k+1):
    #     sum += P(n,i)
    # return sum

def gen_partition(n, k):
    index = 0
    r = random.randint(0, Un_P(n, k) - 1)
    for i in range(1, k + 1):
        cpt = P(n, i)
        if r < cpt:
            index = i
            break
        r -= cpt
    return P_generator_part(n, index)

def P_generator_part(n, k):
    if k > n:
        return []
    if k == 1:
        return [n]
    if k == n:
        return [1] * n
    val = P(n - 1, k - 1)
    r = random.randint(0, P(n, k) - 1)
    if r < val:
        return [1] + P_generator_part(n - 1, k - 1)
    else:
        partition = P_generator_part(n - 1, k)
        partition[0] += 1
        return sorted(partition)


# Avec unranking

def gen_partition_unranking(n,k):
    r = random.randint(0, Un_P(n,k)-1)
    return Generator(n,k,r)

"""
 changed it to match the logic in the bell number so that we wont have 
 different algorithms for each one
"""
def Generator(n, k, r):
    index = 0
    for i in range(1, k+1):
        r = r - P(n, i)
        if r < 0:
            index = i
            r = r + P(n, i)
            break
    return P_generator_unranking(n, index, r)

def P_generator_unranking(n, k, r):
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
    if r < P(n - 1, k - 1):
        return [1] + P_generator_unranking(n - 1, k - 1, r)
    else:
        r = r - P(n - 1, k - 1)
        partition = P_generator_unranking(n - k, k, r)
        return [x + 1 for x in partition]  # Shift partition to ensure positivity

n = 8
k = 4
print("Nb : ", Un_P(n, k))

# Test de la fonction naive
#uniformite10(n,k)

# Test de l'unranking
for j in range(0, Un_P(n, k)):
    print(Generator(n,k,j))
