import functools
import random
import time
import matplotlib
matplotlib.use('TkAgg')  # or 'QtAgg' if you have Qt
import matplotlib.pyplot as plt
import csv

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


# Unranking lexicographique

def n_permutation_unranking(k,n):
    if k < n :
        raise ValueError("k doit être >= n")
    l = [i for i in range(1,k+1)]
    return n_permutation_aux_unranking(k,n,l, int(random.randint(1, nb_possibilites(k,n) - 1 )))

"""
    we're getting f as falling factorial from len and everytime it's getting smaller by 1 so it's like doing
    6! then 5! then 4!, so no repetition
    and we use r as like a random picker
"""

def n_permutation_aux_unranking(k,n,l,r):
    if n == 0 :
        return []

    f = nb_possibilites(k-1, n-1)
    index = r // f   # Determine which element to pick
    r %= f           # Update rank for the next recursive call
    val = l.pop(index)

    return [val] + n_permutation_aux_unranking(k-1,n-1,l,r)

# Invariants

def dans_ordre_lexico(e1, e2) : 
    for i in range(len(e1)) :
        if ( e1[i] < e2[i] ) :
            return True
        elif ( e1[i] > e2[i] ) :
            return False
    return False

def invariant_ordre(k, n, r=0):
    if (r >= nb_possibilites(k,n) - 1) :
        return True
    return dans_ordre_lexico(n_permutation_aux_unranking(k,n,[i for i in range(1,k+1)],r), n_permutation_aux_unranking(k,n,[i for i in range(1,k+1)],r+1)) and invariant_ordre(k, n, r+1)

def valeurs_correctes(k, e):
    l = []
    for i in e :
        if i in l or i < 0 or i > k:
            return False
        l.append(i)
    return True

def invariant_resultat_valide(k, n, r=0):
    if (r >= nb_possibilites(k,n) - 1) :
        return True
    res = n_permutation_aux_unranking(k, n, [i for i in range(1,k+1)], r)
    return len(res) == n and valeurs_correctes(k, res) and invariant_resultat_valide(k, n, r + 1)

k = 4
n = 2

# Test de l'unranking lexicographique
print("Nb : ", nb_possibilites(k,n))
for i in range (0, nb_possibilites(k,n)) :
    print(n_permutation_aux_unranking(k,n,[i for i in range(1,k+1)],i))
print("Invariant: ordre ?", invariant_ordre(k,n))
print("Invariant: resultat valide ?", invariant_resultat_valide(k,n))

def performance (k,n,r):
    with open('Performances/prob2.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(['n', 'Temps d\'exécution (secondes)'])
        for i in range (1, n):
            start_time = time.time()
            x = n_permutation_aux_unranking(k,i,[j for j in range(1,k+1)],r)
            elapsed_time = time.time() - start_time
            writer.writerow([i, elapsed_time])
    n_values = []
    execution_times = []
    with open('Performances/prob2.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            n_values.append(int(row[0]))
            execution_times.append(float(row[1]))
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, execution_times, color='r', linestyle='-', markersize=4)
    plt.title('Temps d\'exécution de n_sequence_lexico en fonction de n')
    plt.xlabel('n')
    plt.ylabel('Temps d\'exécution (secondes)')
    plt.grid(True)
    plt.savefig('Performances/graphe2.png')
    plt.show()

performance(990, 990, 0)