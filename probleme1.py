import random
import sys


"""
 k = range
 n = sequence size
"""
def n_sequence(k,n):
    if k < n :
        raise ValueError("k doit être >= n")
    if n == 0 :
        return []

    val = random.randint(1, k)
    l = n_sequence(k, n-1)
    l.append(val)
    return l


def n_sequence_unranking(k, n, r):
    if k < n:
        raise ValueError("k doit être >= n")
    if n == 0:
        return []
    val = (r % k) + 1  # value between 1 and k
    r //=k
    return [val] + n_sequence_unranking(k,n-1,r)


def gen_sequence(n,k):
    r = random.randint(1, k**n - 1 )
    return n_sequence_unranking(k,n,r)
"""
 val can be [1,2,3,4,5,6,7,8,...k-1]
 
 so we can get like 9 , then remove 1/k
 
 generating enough of a big number to be able to remove a digit at a time nad have each one of it work as a random placement
"""
def uniformite(k,n):
    l = []
    for i in range (1,1000000) :
        sl = gen_sequence(n,k)
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


# Lexicographique

def n_sequence_lexico(k, n, r):
    if k < n:
        raise ValueError("k doit être >= n")
    if n == 0:
        return []
    val = (r % k) + 1 
    r //=k
    return n_sequence_lexico(k,n-1,r) + [val]

# Invariants

def dans_ordre_lexico(e1, e2) : 
    for i in range(len(e1)) :
        if ( e1[i] < e2[i] ) :
            return True
        elif ( e1[i] > e2[i] ) :
            return False
    return False

def invariant_ordre(k, n, r=0):
    if (r >= k**n - 1) :
        return True
    return dans_ordre_lexico(n_sequence_lexico(k,n,r), n_sequence_lexico(k,n,r+1)) and invariant_ordre(k, n, r+1)

def valeurs_correctes(k, e):
    for i in e :
        if i < 1 or i > k :
            return False
    return True

def invariant_resultat_valide(k, n, r=0):
    if (r >= k**n - 1) :
        return True
    res = n_sequence_lexico(k, n, r)
    return len(res) == n and valeurs_correctes(k, res) and invariant_resultat_valide(k, n, r + 1)

# Test lexicographique
k = 4
n = 3
print("Nb : ", k**n)
for i in range (0,k**n):
    print(n_sequence_lexico(k,n,i))
print("Invariant: ordre ?", invariant_ordre(k,n))
print("Invariant: resultat valide ?", invariant_resultat_valide(k,n))