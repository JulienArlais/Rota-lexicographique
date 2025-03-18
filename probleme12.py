import random
import functools

"""
Integer Partition
P(n) = p(n-1) +  ..... + p(0)

And Pk(n) = Pk-1(n-1) + Pk(n-k)
Pk(n-k) means n-k elems onto k parts   
P(n-1) =  Partitions of n-1 into k-1 parts

"""

"""
the way i understood it is : 
P(n-1) =  Partitions of n-1 into k-1 parts
we place one ball into the box and we search in n-1 for k-1 boxes

And the other means we take k elems from n and we palce them into k boxs
"""

@functools.lru_cache(maxsize=None)
def P(n, k):
    """ Computes the number of ways to partition n into k positive parts. """
    if k > n:
        return 0  # Cannot partition if more parts than elements
    if k == n or k == 1:
        return 1  # Only one way to split n into n parts (1+1+...+1) or one part (n)
    return P(n-1, k-1) + P(n-k, k)

def gen_P(n, k):
    """ Generates a partition of n into k parts. """
    if k > n :
        return []
    if k <= 0 :
        return []
    if k == 1:
        return [n]
    if k == n:
        return [1] * n
    r = random.randint(1, P(n,k))
    if r <= P(n - 1, k - 1):
        return [1] + gen_P(n - 1, k - 1)
    else:
        r = r - P(n - 1, k - 1)
        partition = gen_P(n - k, k)
        return [x + 1 for x in partition]

def gen_P_unranking(n,k):
    r = random.randint(1, P(n,k))
    return P_generator_unranking(n,k,r)

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
    if r <= P(n - 1, k - 1):
        return [1] + P_generator_unranking(n - 1, k - 1, r)
    else:
        r = r - P(n - 1, k - 1)
        partition = P_generator_unranking(n - k, k, r)
        return [x + 1 for x in partition]  # Shift partition to ensure positivity

def uniformite12(n,k):
    l = []
    for i in range (1000000) :
        sl = gen_P(n, k)
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
k = 2
print("Nb : ", P(n, k))  # Nb partitions possible

# Test de la fonction naive
uniformite12(n,k)

# Test de l'unranking
for i in range(1, P(n,k)+1):
    print(P_generator_unranking(n,k,i))