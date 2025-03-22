import random
import functools
import sys


@functools.lru_cache(maxsize=None)
def coeff_bin(k, n):
    if n == 0:
        return 1
    elif k == n:
        return 1
    elif k <= 0 or n > k:
        return 0
    else:
        return coeff_bin(k - 1, n) + coeff_bin(k - 1, n - 1)


def CompNKGen(k, n):
    if k > n:
        raise ValueError("k doit être <= n")
    return auxCompNKGen(k, n, 0)


def auxCompNKGen(k, n, i):
    if k == n:
        l = []
        for i in range(k):
            l.append(i)
        return l
    if n == 0:
        return []
    r = random.randint(1, coeff_bin(n - 1 - i, n - k))
    val = coeff_bin(n - 2 - i, n - k - 1)
    if r <= val:
        return auxCompNKGen(k, n - 1, i) + [i]
    else:
        return auxCompNKGen(k, n, i + 1)


"""
(n-1, ,n-k ) is what we're doing
so when applying combinatrics logic where
(n,k) = (n-1,k) + (n-1,k-1)
we would get
(n-1, n-k) = (n-2, n-k) + (n-2, n-k-1)

in combinatorics
(n-1,k) meaning we are looking at k elems from the remaining n-1 elems

(n-1,k-1) meaning we took one elem and put it in k 
"""


def CompNKGen_unranking(k, n):
    if n == 0:
        return []
    if k > n:
        raise ValueError("k doit être <= n")
    r = random.randint(1, coeff_bin(n - 1, n - k))
    return auxCompNKGen_unranking(k, n, r, 0)


def auxCompNKGen_unranking(k, n, r, i):
    if k == n:
        l = []
        for i in range(1, k+1):
            l.append(i)
        return l
    if n == 0:
        return []
    val = coeff_bin(n - 1 - i, n - k - 1)
    if r <= val:
        return sorted(auxCompNKGen_unranking(k, n - 1, r, i) + [i])
    else:
        r = r - val
        return auxCompNKGen_unranking(k, n, r, i + 1)


def uniformite6(k, n):
    l = []
    for i in range(1000000):
        sl = CompNKGen(k, n)
        inn = False
        for j in l:
            if j[0] == sl:
                j[1] += 1
                inn = True
                break
        if not inn:
            l.append([sl, 1])
    for j in l:
        print("p( ", j[0], " ) = ", j[1] / 10000)
    return l

# Lexicographique

def auxCompNKGen_lexico(n, k, r, i):
    if k > n or k <= 0 :
        return []
    if k == 1:
        return [n]

    val = coeff_bin(n - 1 - i, k - 2)
    if r < val:
        return [i] + auxCompNKGen_lexico(n - i, k - 1, r, 1)
    else:
        return auxCompNKGen_lexico(n, k, r - val, i + 1)


n = 10
k = 4
# Test de la fonction naive
#res = uniformite6(k, n)

# Test de l'unranking
print("Nb :", coeff_bin(n-1, n-k))
for i in range(coeff_bin(n - 1, n - k)):
    print(auxCompNKGen_lexico(n, k, i, 1))