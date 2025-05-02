import random
import functools

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


"""
 recursive call is 
 B(n,k) = Sum (n,k) Bk , where k goes from 0 to n-1
 partition 
"""

def fact(i):
    if i == 00 or i == 1:
        return 1
    else:
        return i * fact(i-1)


@functools.lru_cache(maxsize=None)
def stirling(n, k):
    if n == k:
        return 1
    if n == 0 or k == 0 : return 0

    return k*stirling(n - 1, k) + stirling(n - 1, k - 1)


def generatorPartition(n,k):
    if n == k:
        return [[i] for i in range(1, n + 1)]
    if k > n or n == k:
        return []
    if n == 0 and k == 0:
        return []
    val = random.randint(1, stirling(n, k))
    if val <= stirling(n - 1, k - 1):
        partition = generatorPartition(n - 1, k - 1)
        partition.append([n])  # Add n as a new subset
        return partition
    else:
        partition = generatorPartition(n - 1, k)

        rand_spot = random.randint(0, k-1)
        partition[rand_spot].append(n)
        return partition




def generatorPartition_unranking(n,k,r):
    if n == k:
        return [[i] for i in range(1, n + 1)]
    if k > n or n == k:
        return []
    if n == 0 and k == 0:
        return []
    if r < stirling(n - 1, k - 1):
        partition = generatorPartition_unranking(n - 1, k - 1, r)
        partition.append([n])
        return partition
    else:
        r = r - stirling(n - 1, k - 1)
        bloc, r = (r // stirling(n - 1, k), r % stirling(n - 1, k))

        partition = generatorPartition_unranking(n - 1, k, r)

        partition[bloc].append(n)
        return partition


def BellNumber(n,k):
    if n == 0:
        return 1
    else:
        sum = 0
        for i in range(0,k+1):
            sum += stirling(n, i)
        return sum

def Bellnumber_partition_unranking(n,k,r):
    index = 0
    for i in range(1,k+1):
        r = r - stirling(n, i)
        if r < 0 :
            index = i
            r = r + stirling(n, i)
            break
    return generatorPartition_unranking(n,index,r)

"""
    LEXICAL GENERATION
"""

def R_prefix(n,k,l,d0,d1):
    left_sum = U_func(n-l, k-1, d0 -l)
    right_sum = U_func(n-l, k-1, (d1+1)-l)
    return left_sum - right_sum

def U_func(n,k,d):
    upper_bound_1 = n
    total = 0
    for u in range(0, upper_bound_1 + 1):
        for i in range(1, (k+1) + 1): # plus one in the end to count that variable
            total += stirling(n - u, i - 1) * RecComb(n - d, u)
    return total

def extract(n, res ) :
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
    # print("---------------------------------")
    # print(" New Block Iteration ")
    # print(f" block n = {n}, k ={k}, r ={r}")
    if k <= 1:
        block = []
        block.extend([0] * n)
        return block, 0

    block = [0]
    acc = BellNumber(n-1, k-1)
    if r < acc:
        return block,0

    d0 = 1
    index = 2
    inf = 2
    sup = n
    complete = False

    while not complete:
        while inf < sup:
            mid = (inf + sup) // 2
            # print(f" d0 = {d0}, index = {index}, inf = {inf}, sup = {sup}, mid = {mid}, acc = {acc} , R_pref = {R_prefix(n, k, index, d0, mid)}")
            if r >= acc + R_prefix(n, k, index-1, d0, mid-1):
                # print("in first")
                inf = mid + 1
            else:
                # print("in second")
                sup = mid

        mid = inf
        threshold = BellNumber(n - index, k - 1)
        acc += R_prefix(n, k, index-1, d0, mid - 2)

        block.append(mid - index)
        if index > n:
            raise ValueError(f"index {index} is greater than allowed maximum {n}")
        if r < threshold + acc:
            # print(f"Done with block = {block}")
            complete = True
        else:
            # print("not done")
            # print(f" current block = {block}")
            index += 1
            d0 = mid
            inf = d0 + 1
            sup = n
            acc += threshold
            # print("------------------------------------")

    return (block, acc)


def unranking_lexico(n, k, r):
    n2 = n
    res = []
    while n > 0 and k > 0:
        b, new_r = next_block(n, k, r)
        res.append(b)
        r -= new_r
        n -= len(b)
        k -= 1

    res = extract(n2, res)
    return res

def unranking_lexico_main(n, k, r):
    if r >= BellNumber(n,k) :
        raise ValueError("r doit être inférieur au nombre de possibilités :", BellNumber(n,k))
    return unranking_lexico(n, k, r)

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
    if (r == BellNumber(n, k) - 1) :
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
    if (r >= BellNumber(n,k)) :
        return True
    res = unranking_lexico(n, k, r)
    return len(res) <= k and valeurs_correctes(n, res) and invariant_resultat_valide(n, k, r + 1)

n = 6
k = 4

print("Number of partitions : " ,BellNumber(n,k))
print("-----GENERATED WITH UNRANKING ------")
for j in range(BellNumber(n,k)):
    print(j,"",Bellnumber_partition_unranking(n,k,j))

print("-------LEXICALLY ORDERED-------")
for i in range(0, BellNumber(n,k)):
    print(i,"",unranking_lexico_main(n, k, i))

print("Invariant: ordre ?", invariant_ordre(n,k))
print("Invariant: resultat valide ?", invariant_resultat_valide(n,k))

