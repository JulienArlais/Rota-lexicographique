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
def BellNumber(n):
    if n == 0:
        return 1
    else:
        sum = 0
        for k in range(0,n):
            sum += RecComb(n-1,k) * BellNumber(k)
        return sum


print(BellNumber(4))