import random
import functools

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


# Lexicographique

def ncounting(n,k,j):
    if n == 0 and k >=0: 
        return 1
    acc = 0
    for i in range(j,n+1):
        acc += ncounting(n-i,k-1, i)
    return acc

def P_generator_unranking(n, k, r, j = 1):
    if n == 0:
        return []
    val = ncounting(n - j, k - 1, j)
    if r < val:
        return [j] + P_generator_unranking(n - j, k - 1, r, j)
    else :
        r -= val
        return P_generator_unranking(n, k, r, j + 1)

n = 8
k = 4
print("Nb : ", Un_P(n, k))

# Test de la fonction naive
#uniformite10(n,k)

# Test de l'unranking lexicographique
for j in range(0, Un_P(n, k)):
    print(P_generator_unranking(n,k,j))
