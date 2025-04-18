import functools

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

def R_prefix(n,k,l,d0,d1):
    left_sum = S_func(n-l, k-1, d0 -l)
    right_sum = S_func(n-l, k-1, (d1 +1)-l)
    return left_sum - right_sum

def S_func(n,k,d):
    upper_bound_1 = n-k
    upper_bound_2 = n-d
    sum = 0
    for u in range(0, min(upper_bound_1, upper_bound_2) + 1):
        sum += stirling(n-u,k) * RecComb(n-d,u)
    return sum

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
            # print(f"mid = {mid} , inf = {inf}, sup = {sup}, index = {index}, d0 = {d0} , block of size {index}  with smallest elem between {d0} {mid-1}= {R_prefix(n, k, index, d0, mid)}")
            if r >= acc + R_prefix(n, k, index - 1, d0, mid - 1):
                # print("in first")
                inf = mid + 1
            else:
                # print("in second")
                sup = mid

        mid = inf
        threshold = stirling(n - index, k - 1)
        # print(f"threshold: {threshold}")
        acc = acc + R_prefix(n, k, index - 1, d0, mid - 2)
        # print(f"R_prefix = {R_prefix(n, k, index - 1, d0, mid-2)}")
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


n = 5
k = 3
print(stirling(n,k))
for i in range(0, stirling(n,k)):
    print("rank = " , i ,"partition = ",unranking_lexico(n,k,i))
print("Invariant: ordre ?", invariant_ordre(n,k))
print("Invariant: resultat valide ?", invariant_resultat_valide(n,k))