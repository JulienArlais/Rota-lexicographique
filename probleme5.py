import functools
import random
import time
import matplotlib.pyplot as plt
import csv

def fact(i):
    if i == 00 or i == 1:
        return 1
    else:
        return i * fact(i-1)

def combination(n,k):
    return fact(n) / (fact(k) * fact(n-k))


@functools.lru_cache(maxsize=None)
def binomial_coef(n, k):
    if n == k :
        return 1
    elif k == 0:
        return 1
    elif(n <= 0 or k > n):
        return 0
    else:
        return binomial_coef(n - 1, k) + binomial_coef(n - 1, k - 1)


def combinationGenerator(n, k):
    if k > n:
        return []
    if n == 0 and k == 0:
        return []
    if k == 0:
        return []
    val = random.randint(1, binomial_coef(n, k))
    if val <= binomial_coef(n - 1, k):
        return combinationGenerator(n - 1, k)
    else:
        return combinationGenerator(n - 1, k - 1) + [n]

"""
Without Unranking
"""

print("--------GENERATING WITHOUT UNRANKING--------")
n = 5
k = 3
print("Nb :", binomial_coef(n, k))
for i in range(binomial_coef(n, k)):
    print(combinationGenerator(n, k))

def combinationGeneratorUnranking(n, k, r):
    if k == 0:
        return []
    if k > n:
        return []
    if r < binomial_coef(n - 1, k - 1):
        return combinationGeneratorUnranking(n - 1, k - 1, r) + [n]
    else:
        r = r - binomial_coef(n - 1, k - 1)
        return combinationGeneratorUnranking(n - 1, k, r)


def Comb(n,k):
    r = random.randint(1, binomial_coef(n, k) - 1)
    return combinationGeneratorUnranking(n, k, r)

"""
Without Unranking   
"""

print("--------GENERATING WITH UNRANKING--------")
n = 5
k = 3
print("Nb :", binomial_coef(n, k))
for i in range(binomial_coef(n, k)):
    print(combinationGeneratorUnranking(n, k, i))


def uniformComb(n,k):
    l = []
    for i in range (1000000) :
        sl = Comb(n,k)
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
    return l

# Lexicographique

def recGeneration(n, k, r) :
    if k == 0 :
        return []
    if n == k :
        return [i for i in range(k)]
    b = binomial_coef(n - 1, k - 1)
    if r < b :
        l = recGeneration(n-1, k-1, r)
        l.append(n-1)
        return l
    else :
        return recGeneration(n-1, k, r-b)
    
def unrankingRecursive(n, k, r) :
    l = recGeneration(n,k,r)
    l2 = [0 for i in range (k)]
    for i in range (k) :
        l2[i] = n - l[k - 1 - i]
    return l2

# Invariants

def dans_ordre_lexico(e1, e2) : 
    for i in range(len(e1)) :
        if ( e1[i] < e2[i] ) :
            return True
        elif ( e1[i] > e2[i] ) :
            return False
    return False

def invariant_ordre(n, k, r=0):
    if (r >= binomial_coef(n, k)-1) :
        return True
    return dans_ordre_lexico(unrankingRecursive(n,k,r), unrankingRecursive(n,k,r+1)) and invariant_ordre(n, k, r+1)

def valeurs_correctes(n, e):
    for i in range (0,len(e)) :
        if e[i] < 1 or e[i] > n or (i < len(e)-1 and e[i] >= e[i+1]):
            return False
    return True

def invariant_resultat_valide(n, k, r=0):
    if (r >= binomial_coef(n, k)-1) :
        return True
    res = unrankingRecursive(n, k, r)
    return len(res) == k and valeurs_correctes(n, res) and invariant_resultat_valide(n, k, r + 1)

n = 5
k = 3
print("Nb :", binomial_coef(n, k))
for i in range(binomial_coef(n, k)):
    print(unrankingRecursive(n,k,i))
print("Invariant: ordre ?", invariant_ordre(n,k))
print("Invariant: resultat valide ?", invariant_resultat_valide(n,k))

def performance (n,k,r):
    with open('Performances/prob5.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(['n', 'Temps d\'exécution (secondes)'])
        for i in range (1, n):
            start_time = time.time()
            x = unrankingRecursive(n,i,r)
            elapsed_time = time.time() - start_time
            writer.writerow([i, elapsed_time])
    k_values = []
    execution_times = []
    with open('Performances/prob5.csv', mode='r') as file:
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
    plt.savefig('Performances/graphe5.png')
    plt.show()

performance(495, 495, 3000)