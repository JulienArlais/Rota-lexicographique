import functools

@functools.lru_cache(maxsize=None)
def P(n, k):
    """ Computes the number of ways to partition n into k positive parts. """
    if k == 0 or k > n:
        return 0
    if k == n or k == 1:
        return 1
    return P(n - 1, k - 1) + P(n - k, k)

def Un_P(n, k):
    return P(n+k, k)
@functools.lru_cache(None)
def P(n, max_part):
    """Counts partitions of n with largest part ≤ max_part."""
    if n == 0:
        return 1
    if n < 0 or max_part == 0:
        return 0
    return P(n - max_part, max_part) + P(n, max_part - 1)

def Generator(n, r):
    """Unranks the r-th partition of n in lexicographic order."""
    partition = []
    while n > 0:
        count = 0
        for i in range(1,n+ 1):  # Iterate in increasing order for lexicographic sorting
            count_next = P(n - i, i)
            if r < count_next:
                partition.append(i)
                n -= i
                break
            r -= count_next
    return partition


# Example usage
for i in range(15):  # Generate the first 15 lexicographic partitions of 8
    print(Generator(8, i))
