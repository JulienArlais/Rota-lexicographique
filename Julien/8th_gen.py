import random
import functools

"""
Integer Partition
P(n) = p(n-1) +  ..... + p(0)

And Pk(n) = Pk-1(n-1) + Pk(n-k)
Pk(n-k) means n-k elems onto k parts   
P(n-1) =  Partitions of n-1 into k-1 parts

"""

"""
the way i understood it is : 
P(n-1) =  Partitions of n-1 into k-1 parts
we place one ball into the box and we search in n-1 for k-1 boxes

And the other means we take k elems from n and we palce them into k boxs
"""

def P(n):
    if n == 0:
        return 1
    sum = 0
    for i in range(1,n+1):
        sum += P(n-i)
    return sum


def P_generator(n,k):
    if n == 0:
        return []

    if n < k :
        return []
    if n == k :
        
    r = random.randint(1, P(n))
    if r < P(n-1):
        return P_generator(n-1,k-1)
    else:
        return P_generator(n-k,k)

    # Helper function to generate a partition of n into exactly k parts

# Example usage
print(P(10))
print(P_generator(10, 3))  # Generate a random partition of 10 into 3 parts
print(P(10))