import random
import functools

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


# Lexicographique

def MultiCombGen_lexico(k, n):
    if k < n :
        raise ValueError("k doit être >= n")
    if n == 0:
        return []
    r = random.randint(0, coeff_bin(k + n - 1, n))
    return auxMultiCombGen_lexico(k, n, r, 0)

def auxMultiCombGen_lexico(k, n, r, i=1):
    if n == 0:
        return []
    if r < coeff_bin(k - i + n - 1, n - 1):
        return [i] + auxMultiCombGen_lexico(k, n - 1, r, i)
    else:
        r = r - coeff_bin(k - i + n - 1, n - 1)
        return auxMultiCombGen_lexico(k, n, r, i + 1)


# Invariants

def dans_ordre_lexico(e1, e2) : 
    for i in range(len(e1)) :
        if ( e1[i] < e2[i] ) :
            return True
        elif ( e1[i] > e2[i] ) :
            return False
    return False

def invariant_ordre(k, n, r=0):
    if (r >= coeff_bin(k+n-1,n) - 1) :
        return True
    return dans_ordre_lexico(auxMultiCombGen_lexico(k,n,r), auxMultiCombGen_lexico(k,n,r+1)) and invariant_ordre(k, n, r+1)

def valeurs_correctes(k, e):
    for i in range (0,len(e)) :
        if e[i] < 1 or e[i] > k or (i < len(e)-1 and e[i] > e[i+1]):
            return False
    return True

def invariant_resultat_valide(k, n, r=0):
    if (r >= coeff_bin(k+n-1,n) - 1) :
        return True
    res = auxMultiCombGen_lexico(k, n, r)
    return len(res) == n and valeurs_correctes(k, res) and invariant_resultat_valide(k, n, r + 1)

k = 5
n = 3
print("Nb : ", coeff_bin(k+n-1,n))

for i in range(0,coeff_bin(k+n-1,n)):
    print(auxMultiCombGen_lexico(k,n,i))
print("Invariant: ordre ?", invariant_ordre(k,n))
print("Invariant: resultat valide ?", invariant_resultat_valide(k,n))
