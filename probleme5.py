
import functools
import random

def fact(i):
    if i == 00 or i == 1:
        return 1
    else:
        return i * fact(i-1)



def combination(n,k):
    return fact(n) / (fact(k) * fact(n-k))


@functools.lru_cache(maxsize=None)
def RecComb(n, k):
    if n == k :
        return 1
    elif k == 0:
        return 1
    elif(n <= 0 or k > n):
        return 0
    else:
        return RecComb(n-1,k) + RecComb(n-1, k-1)


def generator(n,k):
    if k > n:
        return []
    if n == 0 and k == 0:
        return []
    if k == 0:
        return []
    val = random.randint(1, RecComb(n,k))
    if val <= RecComb(n-1, k):
        return  generator(n-1, k)
    else:
        return generator(n-1, k-1) + [n]



def unrank_generator(n,k,r):
    if k == 0:
        return []
    if k > n:
        return []
    if r < RecComb(n-1,k-1):
        return unrank_generator(n-1,k-1,r) + [n]
    else:
        r = r - RecComb(n-1,k-1)
        return unrank_generator(n-1,k, r)


def Comb(n,k):
    r = random.randint(1,RecComb(n,k)-1)
    return unrank_generator(n,k,r)

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

# def unrank_generator_lexico(n,k,r):
#     l = []
#     x = 1
#     for i in range (1, k+1):
#         while RecComb(n-x, k-i) <= r :
#             r = r - RecComb(n-x, k-i)
#             x = x + 1
#         l.append(x) # found the number
#         x = x + 1
#     return l


def recGeneration(n, k, r) :
    if k == 0 :
        return []
    if n == k :
        return [i for i in range(k)]
    b = RecComb(n-1, k-1)
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

n = 5
k = 3
print("Nb :", RecComb(n,k))
for i in range(RecComb(n,k)):
    print(unrankingRecursive(n,k,i))