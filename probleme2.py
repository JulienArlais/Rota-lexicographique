import functools
import random
import sys

def fact(i):
    if i == 00 or i == 1:
        return 1
    else:
        return i * fact(i-1)

@functools.lru_cache(maxsize=None)
def nb_possibilites_2(k,n):
    return fact(k)/fact(n)

def n_permutation(k,n):
    if k < n :
        raise ValueError("k doit être >= n")
    l = [i for i in range(1,k+1)]
    return n_permutation_aux(k,n,l)
    
def n_permutation_aux(k,n,l):
    if n == 0 :
        return []
    i = l[random.randint(0, len(l)-1)]
    l.remove(i)
    res = n_permutation_aux(k, n-1,l)
    res.append(i)
    return res

def uniformite(k,n):
    l = []
    for i in range (1,1000000) :
        sl = n_permutation(k,n)
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

if (len(sys.argv) != 3) :
    raise TypeError("Il faut 2 arguments : k suivi de n")
k = int(sys.argv[1])
n = int(sys.argv[2])
print("Nb de combinaisons : ", int(nb_possibilites_2(k,n)))
uniformite(k,n)
