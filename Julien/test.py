import random


def P_generator(n, k):
    # Base case: if we need to partition 0 into 0 parts, return an empty partition
    if n == 0 and k == 0:
        return []
    # If we have to partition n into 0 parts, it's impossible unless n is 0
    if k == 0:
        return []
    # If we need to partition n into k parts and n < k, it's impossible
    if n < k:
        return []

    # Decide randomly whether to take a part of size k or to take 1 as part
    # Case 1: Take 1 as one part and partition (n-1) into (k-1) parts
    if random.random() < 0.5 and n > 0:
        rest = P_generator(n - 1, k - 1)
        if rest is not None:
            return [1] + rest

    # Case 2: Take a part of size >= k, reduce n by k, partition the rest into k parts
    if n >= k:
        rest = P_generator(n - k, k)
        if rest is not None:
            return [k] + rest

    # Return None if no valid partition is found in both cases
    return None


# Example usage
print(P_generator(10, 5))  # Example of partitioning 10 into 5 parts
