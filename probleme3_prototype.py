import functools


def fact(i):
    if i == 0 or i == 1:
        return 1
    else:
        return i * fact(i - 1)


@functools.lru_cache(maxsize=None)
def RecComb(n, k):
    if n == k:
        return 1
    elif k == 0:
        return 1
    elif (n <= 0 or k > n):
        return 0
    else:
        return RecComb(n - 1, k - 1) + RecComb(n - 1, k)


@functools.lru_cache(maxsize=None)
def stirling(n, k):
    if n == k:
        return 1
    if n <= 0 or k <= 0 or k > n:
        return 0
    return k * stirling(n - 1, k) + stirling(n - 1, k - 1)


@functools.lru_cache(maxsize=None)
def Ordered_Stirling(n, k):
    return fact(k) * stirling(n, k)


def R_prefix(n,k,l,d0,d1):
    left_sum = T_func(n-l, k-1, d0-l)
    right_sum = T_func(n-l, k-1, d1-l)
    return left_sum - right_sum
def T_func(n,k,d):
    upper_bound_1 = n-k
    upper_bound_2 = n-d
    sum = 0
    for u in range(0, min(upper_bound_1, upper_bound_2) + 1):
        sum += fact(k)*stirling(n-u,k) * RecComb(n-d,u)
    return sum
def extract(n, res):
    l = [i for i in range(1, n + 1)]
    p = []
    for r in res:
        q = []
        for i in r:
            q.append(l.pop(i))
        p.append(q)
    return p


def next_block(n, k, r):
    block = []
    acc = 0

    d0 = 0
    index = 1
    inf = 1
    sup = n
    complete = False

    while not complete:
        while inf < sup:
            mid = (inf + sup) // 2
            if r >= acc + R_prefix(n, k, index-1, d0, mid):
                inf = mid + 1
            else:
                sup = mid
        mid = inf
        threshold = Ordered_Stirling(n-index , k-1)

        acc = acc + R_prefix(n,k,index-1,d0, mid-1)

        block.append(mid - index)

        # Ensuring cete condition can be met
        if r < threshold + acc:
            complete = True
        else:
            index += 1
            d0 = mid
            inf = d0 + 1
            sup = n
            acc += threshold

    return (block, acc)

def unranking_lexico(n, k, r):
    n2 = n
    res = []
    while k > 1:
        (b, acc) = next_block(n, k, r)
        res.append(b)
        r -= acc
        n -= len(b)
        k -= 1

    res.append([0 for i in range(n)])
    res = extract(n2, res)
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
    if (r >= Ordered_Stirling(n,k) - 1) :
        return True
    res = unranking_lexico(n, k, r)
    return len(res) == k and valeurs_correctes(n, res) and invariant_resultat_valide(n, k, r + 1)


n = 5
k = 3
print(Ordered_Stirling(n,k))
# print(unranking_lexico(n, k,7))
for i in range(0, Ordered_Stirling(n,k)):    # print("----------------------------------")
    print("rank = ", i, "partition = ", unranking_lexico(n, k, i))
    # print("----------------------------------")
print("Invariant: ordre ?", invariant_ordre(n,k))
print("Invariant: resultat valide ?", invariant_resultat_valide(n,k))

n = 5
k = 3
l = 2
d0 = 3
# def nrml_T_func(n,k,d,l):
#     upper_bound1 = n-k-l+1
#     upper_bound2 = n-d
#     total = 0
#     for u in range(0, min(upper_bound1, upper_bound2)+1):
#         total += fact(k-1)*stirling(n-l-u, k-1)*RecComb(n-d,u)
#     return total


# print(nrml_T_func(n,k,d0,l))
# print(T_func(n-l,k-1,d0-l))
