"""
for sequences :
after the rules of exponentations :
x^n = x^(n-1) * x
so S(x, n) = S(x,n-1) * x

"""
import random
import functools

def RecSequence(x, n):
    if n == 0:
        return 1
    return x * RecSequence(x, n - 1)


def genSequences(sequence, n):
    seq = []
    while n > 0:
        r = random.randint(0, len(sequence) - 1)
        seq.append(sequence[r])
        n = n - 1
    return seq

def uniformiteSeq(X,n):
    l = []
    for i in range (1000000) :
        sl = genSequences(X,n)
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

print(RecSequence(3, 2))

sequence = ['a', 'b', 'c']
n = 2
print(genSequences(sequence, n))

#print(uniformiteSeq(sequence, n))
def fact (n) :
    if n == 0 :
        return 1
    return n * fact(n-1)


def genPermu(X, n):
    sequence = X[:]  # Copy the list to avoid modifying the original
    seq = []
    while n > 0 and X:
        r = random.randint(0, len(sequence) - 1)
        seq.append(sequence.pop(r))  # Pop removes and returns the element
        n -= 1
    return seq


def uniformitePerm(X,n):
    l = []
    for i in range (1000000) :
        sl = genPermu(X,n)
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

#print(uniformitePerm(sequence,n))

"""
k-multi combinations

( (x+ n-1) , n) 

formula is the same as combinations , we jsut change the variables
Multicomb(n,k ) = ( (n + k-1) , k ) = (n+k-1)! / k!(n-1)!

So since (n k ) = (n-1, k-1) + (n-1, k)
((n+k-1) , k ) = (n+k-1, k-1) +  (n+k-1, k)

 
"""

@functools.lru_cache(maxsize=None)
def MultiCombRec(n, k):
    if k == 0:
        return 1
    elif n == k:
        return 1
    elif n <= 0 or k > n:
        return 0
    else:
        return MultiCombRec(n - 1, k) + MultiCombRec(n, k - 1)


def AuxMultiCombGen(n, k, r):
    if k > n :
        return []
    if k == 0:
        return []
    if n == 0:
        return []
    if r <= MultiCombRec(n - 1, k):
        return AuxMultiCombGen(n - 1, k, r)
    else:
        return AuxMultiCombGen(n, k - 1, r-MultiCombRec(n,k-1)) + [n]

n = 5
k = 3

def MultiCombGen(n,k):
    r = random.randint(0,MultiCombRec(n,k))
    return AuxMultiCombGen(n,k,r)

def uniformiteMultiComb(n,k):
    l = []
    for i in range (1000000) :
        sl = MultiCombGen(n, k)
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

e