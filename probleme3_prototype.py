import functools

def fact(i):
    if i == 00 or i == 1:
        return 1
    else:
        return i * fact(i-1)

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
def stirling(n, k):
    if n == k:
        return 1
    if n <= 0 or k <= 0 or k > n:
        return 0
    return k * stirling(n-1, k) + stirling(n-1, k-1)


@functools.lru_cache(maxsize=None)
def Ordered_Stirling(n, k):
    return fact(k) * stirling(n, k)



def R_prefix(n,k,l,d0,d1):
    left_sum = T_func(n-l, k-1, d0 -l)
    right_sum = T_func(n-l, k-1, (d1 +1)-l)
    return left_sum - right_sum

def T_func(n,k,d):
    upper_bound_1 = n-k
    upper_bound_2 = n-d
    sum = 0
    for u in range(0, min(upper_bound_1, upper_bound_2) + 1):
        sum += fact(k+1)* stirling(n-u,k) * stirling(n-d,u)
    return sum


def extract(n, res):
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
    acc = Ordered_Stirling(n-1,k-1)
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
            if r >= acc + R_prefix(n, k, index-1, d0, mid):
                inf = mid+1
            else:
                sup = mid
        mid = inf
        threshold = Ordered_Stirling(n-index, k -1)
        acc += R_prefix(n,k,index-1,d0,mid-1)
        block.append(mid-index+1)
        if r < threshold + acc:
            complete = True
        else:
            index +=1
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
print(Ordered_Stirling(n,k))
for i in range(0, Ordered_Stirling(n,k)):
    print("rank = " , i ,"partition = ",unranking_lexico(n,k,i))