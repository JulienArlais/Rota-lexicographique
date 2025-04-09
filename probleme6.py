import random
import functools
import sys
import time
import matplotlib.pyplot as plt
import csv

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

def auxCompNKGen_lexico(n, k, r, i=1):
    if k > n or k <= 0 :
        return []
    if k == 1:
        return [n]

    val = coeff_bin(n - 1 - i, k - 2)
    if r < val:
        return [i] + auxCompNKGen_lexico(n - i, k - 1, r, 1)
    else:
        return auxCompNKGen_lexico(n, k, r - val, i + 1)

# Invariants

def dans_ordre_lexico(e1, e2) : 
    for i in range(len(e1)) :
        if ( e1[i] < e2[i] ) :
            return True
        elif ( e1[i] > e2[i] ) :
            return False
    return False

def invariant_ordre(n, k, r=0):
    if (r >= coeff_bin(n - 1, n - k) - 1) :
        return True
    return dans_ordre_lexico(auxCompNKGen_lexico(n,k,r), auxCompNKGen_lexico(n,k,r+1)) and invariant_ordre(n, k, r+1)

def valeurs_correctes(n, k, e):
    s = 0
    for i in e :
        if i < 0 or i > n-k+1 :
            return False
        s += i
    return s == n

def invariant_resultat_valide(n, k, r=0):
    if (r >= coeff_bin(n - 1, n - k) - 1) :
        return True
    res = auxCompNKGen_lexico(n, k, r)
    return len(res) == k and valeurs_correctes(n, k, res) and invariant_resultat_valide(n, k, r + 1)

n = 10
k = 4

print("Nb :", coeff_bin(n-1, n-k))
for i in range(coeff_bin(n - 1, n - k)):
    print(auxCompNKGen_lexico(n, k, i))
print("Invariant: ordre ?", invariant_ordre(n,k))
print("Invariant: resultat valide ?", invariant_resultat_valide(n,k))

def performance (n,k,r):
    with open('Performances/prob6.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(['n', 'Temps d\'exécution (secondes)'])
        for i in range (1, n):
            start_time = time.time()
            x = auxCompNKGen_lexico(n,i,r)
            elapsed_time = time.time() - start_time
            writer.writerow([i, elapsed_time])
    k_values = []
    execution_times = []
    with open('Performances/prob6.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            k_values.append(int(row[0]))
            execution_times.append(float(row[1]))
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, execution_times, color='r', linestyle='-', markersize=4)
    plt.title('Temps d\'exécution de n_sequence_lexico en fonction de k')
    plt.xlabel('k')
    plt.ylabel('Temps d\'exécution (secondes)')
    plt.grid(True)
    plt.savefig('Performances/graphe6.png')
    plt.show()

performance(495, 495, 0)