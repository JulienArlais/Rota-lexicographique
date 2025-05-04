import csv
import functools
import random
import time
import math
import cProfile
import matplotlib
matplotlib.use('TkAgg')  # or 'QtAgg' if you have Qt
import matplotlib.pyplot as plt

# these will be used throughout the calls
n = 5
k = 3

r_prefix_call_count = 0
s_func_call_count = 0
@functools.lru_cache(maxsize=None)
def RecComb(n, k):
    if n == k :
        return 1
    elif k == 0:
        return 1
    elif(n <= 0 or k > n):
        return 0
    else:
        return RecComb(n-1,k-1) + RecComb(n-1, k)


@functools.lru_cache(maxsize=None)
def stirling(n,k):
    if n == k:
        return 1
    if n == 0 or k == 0 : return 0

    return k*stirling(n-1, k) + stirling(n-1, k-1)

"""
Partition generation non unranked
"""

def generatorPartition(n,k):
    if n == k:
        return [[i] for i in range(1, n + 1)]
    if k > n or n == k:
        return []
    if n == 0 and k == 0:
        return []
    val = random.randint(1, stirling(n, k))
    if val <= stirling(n-1, k-1):
        partition = generatorPartition(n - 1, k - 1)
        partition.append([n])  # Add n as a new subset
        return partition
    else:
        partition = generatorPartition(n - 1, k)

        rand_spot = random.randint(0, k-1)
        partition[rand_spot].append(n)
        return partition


def partitions_gen(n,k):
    return generatorPartition(n,k)

# Printing Partitions
print(partitions_gen(5,3))


"""
Partition gen using unranking
"""

def generatorPartition_unranking(n,k,r):
    if n == k:
        return [[i] for i in range(1, n + 1)]
    if k > n or n == k:
        return []
    if n == 0 and k == 0:
        return []
    if r < stirling(n-1, k-1):
        partition = generatorPartition_unranking(n - 1, k - 1, r)
        partition.append([n])
        return partition
    else:
        r = r - stirling(n-1,k-1)
        bloc, r = (r//stirling(n-1,k), r%stirling(n-1,k))

        partition = generatorPartition_unranking(n - 1, k, r)

        partition[bloc].append(n)
        return partition


print("---------Generating Partitions with Unranking ---------")
# Unranking
for i in range(0,stirling(n,k)):
    print(generatorPartition_unranking(n,k,i))

print("test with n = k ")
print(generatorPartition(8,8))

"""
Lexicoraphiccaly  generated partition with unranking
"""

@functools.lru_cache(maxsize=1000000)
def R_prefix(n,k,l,d0,d1):
    global r_prefix_call_count
    r_prefix_call_count += 1
    left_sum = S_func(n-l, k-1, d0 -l)
    right_sum = S_func(n-l, k-1, (d1 +1)-l)
    return left_sum - right_sum


@functools.lru_cache(maxsize=None)
def S_func(n,k,d):
    global s_func_call_count
    s_func_call_count += 1
    upper_bound_1 = n-k
    upper_bound_2 = n-d
    sum = 0
    for u in range(0, min(upper_bound_1, upper_bound_2) + 1):
        sum += stirling(n-u,k) * RecComb(n-d,u)
    return sum

def extract(n, res) :
    l = [i for i in range(1,n+1)]
    p = []
    for r in res:
        q = []
        for i in r:
            q.append(l.pop(i))
            #
        p.append(q)
    return p

def next_block(n, k, r):
    block = [0]
    acc = stirling(n - 1, k - 1)
    if r < acc:
        return (block, 0)
    d0 = 1
    index = 2
    inf = 2
    sup = n
    complete = False
    while not complete:
        while inf < sup:
            mid = (inf + sup) // 2
            if r >= acc + R_prefix(n, k, index - 1, d0, mid - 1):
                inf = mid + 1
            else:
                sup = mid

        mid = inf
        threshold = stirling(n - index, k - 1)
        acc = acc + R_prefix(n, k, index - 1, d0, mid - 2)
        block.append(mid - index)
        if r < threshold + acc:
            complete = True
        else:
            index += 1
            d0 = mid
            inf = d0 + 1
            sup = n
            acc = acc + threshold

    return (block, acc)

def unranking_lexico(n,k,r):
    n2 = n
    res = []
    while k > 1 :
        (b,acc) = next_block(n,k,r)
        res.append(b)
        r -= acc
        n -= len(b)
        k -= 1

    res.append([0 for i in range(n)])
    res = extract(n2,res)
    return res

# Invariants

def dans_ordre_lexico(e1, e2) :
    for i in range(min(len(e1), len(e2))) :
        if (dans_ordre_lexico_aux(e1[i], e2[i])) :
            return True
        elif (dans_ordre_lexico_aux(e1[i], e2[i])) :
            return False
    return False

def dans_ordre_lexico_aux(e1, e2) : 
    for i in range(min(len(e1), len(e2))) :
        if ( e1[i] < e2[i] ) :
            return True
        elif ( e1[i] > e2[i] ) :
            return False
    return len(e1) < len(e2)

def invariant_ordre(n, k, r=0):
    if (r == stirling(n, k) - 1) :
        return True
    return dans_ordre_lexico(unranking_lexico(n,k,r), unranking_lexico(n,k,r+1)) and invariant_ordre(n, k, r+1)

def valeurs_correctes(n, e):
    l = []
    for i in e :
        if i == [] :
            return False
        for j in i :
            if j in l or j < 0 or j > n:
                return False
            l.append(i)
    return True

def invariant_resultat_valide(n, k, r=0):
    if (r >= stirling(n, k) - 1) :
        return True
    res = unranking_lexico(n, k, r)
    for i in range(0, k-1):
        if not dans_ordre_lexico_aux(res[i], res[i+1]):
            return False
    return len(res) == k and valeurs_correctes(n, res) and invariant_resultat_valide(n, k, r + 1)


print("--------- Lexicographically Generated Partitions---------")
n = 5
k = 5
print(stirling(n,k))
for i in range(0, stirling(n,k)):
    print("rank = " , i ,"partition = ",unranking_lexico(n,k,i))
print("Invariant: ordre ?", invariant_ordre(n,k))
print("Invariant: resultat valide ?", invariant_resultat_valide(n,k))

def performance(n, sample_size=100, cluster_size=15,  name = "probleme9"):
    rows = [['n', 'Temps d\'exécution (secondes)']]  # header row
    n_values = []
    execution_times = []
    clear_interval = int(n / 2)
    counter = 0
    for n_ in range(2, n + 1):
        k = int(n_ / math.log(n_))
        val = stirling(n_, k)
        if val == 0:
            continue
        samples = [random.randint(0, val - 1) for _ in range(sample_size)]

        total_time = 0
        for r in samples:
            start_call = time.perf_counter()
            x = unranking_lexico(n_, k, r)
            total_time += time.perf_counter() - start_call

        counter += 1
        if counter >= clear_interval:
            stirling.cache_clear()
            RecComb.cache_clear()
            S_func.cache_clear()
            R_prefix.cache_clear()
            print(f"Caches cleared after {n_} (approx. {clear_interval} iterations).")

            # Warm-up after clearing cache
            for _ in range((n_ - int(sample_size/5)), n_):
                samples = [random.randint(0, val - 1) for _ in range(10)]
                for r in samples:
                    unranking_lexico(n_, k, r)

            counter = 0

        # Compute average time for the current sample
        average_time = total_time / sample_size
        print(f"n_use = {n_}, k = {k}, time: {average_time}")
        n_values.append(n_)
        execution_times.append(average_time)

        # Once we accumulate `cluster_size` points, we average and reset
        if len(n_values) == cluster_size:
            avg_n = int(sum(n_values) / len(n_values))
            avg_time = sum(execution_times) / len(execution_times)  # Average time over cluster
            rows.append([avg_n, avg_time])  # Store the cluster average
            n_values.clear()  # Reset n_values
            execution_times.clear()  # Reset execution_times

    # Write all rows once at the end
    with open('Performances/' + name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    # Now load and plot the data
    n_values = []
    execution_times = []
    with open('Performances/'+name, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
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

def performance_test(n,sample_size=100):
    rows = [['n', 'Temps d\'exécution (secondes)']]  # header row

    clear_interval = int(n / 2)
    counter = 0
    for n_ in range(2, n):
        k = int(n_ / math.log(n_))
        val = stirling(n_, k)
        if val == 0:
            continue
        samples = [random.randint(0, val - 1) for _ in range(sample_size)]

        total_time = 0
        for r in samples:
            start_call = time.perf_counter()
            x = unranking_lexico(n_, k, r)
            total_time += time.perf_counter() - start_call

        counter += 1
        if counter >= clear_interval:
            stirling.cache_clear()
            RecComb.cache_clear()
            S_func.cache_clear()
            R_prefix.cache_clear()
            print(f"Caches cleared after {n_} (approx. {clear_interval} iterations).")

            # Warm-up after clearing cache
            for _ in range((n_ - int(sample_size/3)) , n_):
                samples = [random.randint(0, val - 1) for _ in range(10)]
                for r in samples:
                    unranking_lexico(n_, k, r)

            counter = 0

        average_time = total_time / sample_size
        print(f"n_use = {n_}, k = {k}, time: {total_time}")


def test(n,k,sample_size=100):
    val = stirling(n, k)

    samples = [random.randint(0, val - 1) for _ in range(sample_size)]

    total_time = 0
    for r in samples:
        start_call = time.perf_counter()
        x = unranking_lexico(n, k, r)
        total_time += time.perf_counter() - start_call

    print(f"n_use = {n}, k = {k}, time: {total_time}")

performance(600,350)
