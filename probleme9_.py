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
def RecPart(n,k):
    if n == k:
        return 1
    if n == 0 or k == 0 : return 0

    return k*RecPart(n-1, k) + RecPart(n-1, k-1)
def S(n,k,prefix, exactly = False):
    l = len(prefix)
    d = prefix[-1]
    if exactly:
        "  u = 0 "
        return RecPart(n-l,k-1) * RecComb(n-d, 0)
    else:
        nb_Part = 0
        end_val = n-k-l+1
        for u in range(0, end_val+1):
            nb_Part += RecPart(n-(l+u),k-1) * RecComb(n-d, u)
        return nb_Part

print(S(5,3,[1]))


def gen_helper(n, k, rank, startPoint):
    block = []
    nb_Part = 0
    test_number = startPoint
    exactly = False

    while rank != nb_Part:
        if not exactly:
            prefix = block + [test_number]
        else:
            prefix = block  # Maintain block when exactly is True

        nb_Part = S(n, k, prefix, exactly)

        print("-------------------------")
        print(f"Nb_part = {nb_Part}")
        print(f"rank = {rank}")
        print(f"block = {block}")
        print(f"prefix = {prefix}")
        print(f"exactly? = {exactly}")
        print("----------------------------")

        if exactly and rank <= nb_Part:
            return block, nb_Part
        if rank < nb_Part:
            block.append(test_number)
            exactly = True
        elif rank > nb_Part:
            rank -= nb_Part
            if not exactly:
                test_number += 1  # Ensure we move to the next test_number
            else:
                exactly = False
                test_number +=1  # Set test_number correctly

    return block, nb_Part

block , part = gen_helper(5,3,20,1)

#print("block : ", block , " part = ", part)


@functools.lru_cache(maxsize=None)
def stirling(n,k):
    if n == k:
        return 1
    if n == 0 or k == 0 : return 0

    return k*RecPart(n-1, k) + RecPart(n-1, k-1)

def R_prefix(n,k,l,d0,d1):

    left_sum = S_func((n-l),(k-1),l,d0 -l)
    right_sum = S_func((n-l),(k-1),l,(d1 +1)-l)
    return left_sum - right_sum

def S_func(n,k,l,d):
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

def next_block(n,k,r):
    block = [0]
    acc = stirling(n-1,k-1)
    if r < acc:
        return (block,0)
    d0 = 1
    index = 2
    inf = 2
    sup = n
    complete = False
    while not complete:
        while inf < sup:
            mid = (inf+sup)//2
            if r >= acc + R_prefix(n,k,index-1,d0,mid):
                inf = mid+1
            else:
                sup = mid
        mid = inf
        threshold = stirling(n-index, k -1)
        acc = acc + R_prefix(n,k,index-1,d0,mid-1)
        block.append(mid-index+1)
        if r < threshold + acc:
            complete = True
        else:
            index += 1
            d0 = mid
            inf = d0+1
            sup = n
            acc = acc + threshold
    return block,acc

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

n = 5
k = 3
print(stirling(n,k))
for i in range(0, stirling(n,k)):
    print("rank = " , i ,"partition = ",unranking_lexico(n,k,i))