import random
import functools

def fact(i):
    if i == 00 or i == 1:
        return 1
    else:
        return i * fact(i-1)


def permutation_Formula(n,k):
    return fact(n)/fact(n-k)


def fisherYates(l):
    for i in range (len(l)-1):
        r = random.randint(i,len(l)-1)
        tmp = l[i]
        l[i] = l[r]
        l[r] = tmp
    return l

def generator(n,k):
    if n == 0:
        []
    if n != k:
        return []
    partition = []
    for i in range(n):
        partition.append(i)

    return fisherYates(partition)


def uniformite8(n,k):
    l = []
    for i in range (1000000):
        sl = generator(n,k)
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

print(permutation_Formula(3,3))
print(uniformite8(3,3))
