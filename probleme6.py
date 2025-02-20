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
    if n == 0:
        return []
    if k > n :
        raise ValueError("k doit être <= n")
    r = random.randint(1, coeff_bin(n-1, n-k))
    return auxCompNKGen(k, n, r, 0)

def auxCompNKGen(k, n, r, i):
    if n == 0:
        return []
    if r <= coeff_bin(n - 2 - i, n - k - 1):
        return auxCompNKGen(k, n - 1, r, i) + [i]
    else:
        r = r - coeff_bin(n - 2 - i, n - k - 1)
        return auxCompNKGen(k, n, r, i + 1)

def uniformite6(k,n):
    l = []
    for i in range (1000000) :
        sl = CompNKGen(k, n)
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

if (len(sys.argv) != 3) :
    raise TypeError("Il faut 2 arguments : k suivi de n (k<n)")
k = int(sys.argv[1])
n = int(sys.argv[2])
print("Nb : ", coeff_bin(n-1,n-k))
print(uniformite6(k,n))