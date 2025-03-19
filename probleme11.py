import random
import functools
import sys
"""
It'll give the same result as problem 8

The order here doesnt matter  for both N and X 
so no matter way we put it it wot matter plus
because we have injective where it means no two elements can point into the same elem , so order matters
and because the maximum we can have per urn is 1 then we'll only have one result

"""


def generator(n,k):
    if k < n :
        return ValueError("k has to be superior or equal to n")
    partition = [0] * k
    for i in range(1,n+1):
        partition[i-1] = 1
    return partition


print(generator(3,5))


