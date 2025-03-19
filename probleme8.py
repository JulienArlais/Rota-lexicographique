import random
import functools
"""
n marked balls into x plain boxes
meaning that we do put importance into n but because the order that we put them in in the end doesnt matter,
it ovverrides the order effect so in the end the order doesnt matter
"""
def fact(i):
    if i == 00 or i == 1:
        return 1
    else:
        return i * fact(i-1)


def permutation_Formula(n,k):
    return fact(n)/fact(n-k)


def generator(n,k):
    if k < n :
        return ValueError("K has to be superior or equal to n")
    partition = [0] * k
    for i in range(1,n+1):
        partition[i-1] = i
    return partition


print(generator(3,5))
