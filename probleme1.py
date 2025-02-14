import random
import sys

def n_sequence(k,n):
    if k < n :
        raise ValueError("k doit être >= n")
    if n == 0 :
        return []
    
    val = random.randint(1, k)
    l = n_sequence(k, n-1)
    l.append(val)
    return l

def uniformite(k,n):
    l = []
    for i in range (1,1000000) :
        sl = n_sequence(k,n)
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
print("Nb de combinaisons : ", k**n)
uniformite(k,n)
