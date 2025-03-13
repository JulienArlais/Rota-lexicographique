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
        return coeff_bin(k - 1, n) + coeff_bin(k-1, n - 1)
    
def MultiCombGen(k, n):
    if k < n :
        raise ValueError("k doit être >= n")
    return auxMultiCombGen(k, n, 0)

def auxMultiCombGen(k, n, i):
    if n == 0:
        return []
    r = random.randint(1, coeff_bin(k + n -i - 1, n))
    if r <= coeff_bin(k - i + n - 2, n - 1):
        return auxMultiCombGen(k, n - 1, i) + [i]
    else:
        return auxMultiCombGen(k, n, i + 1)

def MultiCombGen_unranking(k, n):
    if k < n :
        raise ValueError("k doit être >= n")
    if n == 0:
        return []
    r = random.randint(1, coeff_bin(k + n - 1, n))
    return auxMultiCombGen_unranking(k, n, r, 0)

def auxMultiCombGen_unranking(k, n, r, i):
    if n == 0:
        return []
    if r <= coeff_bin(k - i + n - 2, n - 1):
        return auxMultiCombGen_unranking(k, n - 1, r, i) + [i]
    else:
        r = r - coeff_bin(k - i + n - 2, n - 1)
        return auxMultiCombGen_unranking(k, n, r, i + 1)

def uniformite4(k,n):
    l = []
    for i in range (1000000) :
        sl = MultiCombGen(k, n)
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
    raise TypeError("Il faut 2 arguments : k suivi de n (k>n)")
k = int(sys.argv[1])
n = int(sys.argv[2])
print("Nb : ", coeff_bin(k+n-1,n))

# Test de la fonction naive
print(uniformite4(k,n))

# Test de l'unranking
for i in range(1,coeff_bin(k+n-1,n)+1):
    print(auxMultiCombGen_unranking(k,n,i,0))