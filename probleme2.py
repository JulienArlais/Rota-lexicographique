import functools
import random
import sys


"""
read more bout the way its selecting , both it & the first one

"""
def fact(i):
    if i == 00 or i == 1:
        return 1
    else:
        return i * fact(i-1)

@functools.lru_cache(maxsize=None)
def nb_possibilites(k,n):
    return fact(k)//fact(k-n)


def n_permutation(k, n):
    if k < n:
        raise ValueError("k doit être >= n")
    l = [i for i in range(1, k + 1)]
    return n_permutation_aux(k, n, l)


def n_permutation_aux(k, n, l):
    if n == 0:
        return []
    i = l[random.randint(0, len(l) - 1)]
    l.remove(i)
    res = n_permutation_aux(k, n - 1, l)
    res.append(i)
    return res


def n_permutation_unranking(k,n):
    if k < n :
        raise ValueError("k doit être >= n")
    l = [i for i in range(1,k+1)]
    return n_permutation_aux_unranking(k,n,l, int(random.randint(1, nb_possibilites(k,n) - 1 )))


"""
    we're getting  f as factorial from len and everytime its getting smaller by 1 so its like doing
    6! then 5! then 4! , so no repetition
    and we use r as like a random picker
"""
def n_permutation_aux_unranking(k,n,l,r):
    if n == 0 :
        return []
    f = fact(len(l) - 1 )
    index = r // f  # Determine which element to pick
    r %= f  # Update rank for the next recursive call
    val = l.pop(index)

    return [val] + n_permutation_aux_unranking(k,n-1,l,r)

def uniformite(k,n):
    l = []
    for i in range (1,1000000) :
        sl = n_permutation_unranking(k,n)
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


"""

if (len(sys.argv) != 3) :
    raise TypeError("Il faut 2 arguments : k suivi de n")
k = int(sys.argv[1])
n = int(sys.argv[2])
print("Nb de combinaisons : ", int(nb_possibilites_2(k,n)))
"""
k = 5
n = 3
print("Nb : ", nb_possibilites(k,n))
for i in range (0, nb_possibilites(k,n) ) :
    print(n_permutation_aux_unranking(k,n,[i for i in range(1,k+1)],i))
#uniformite(k,n)
