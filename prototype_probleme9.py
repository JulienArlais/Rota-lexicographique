import functools

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
def RecPart(n,k):
    if n == k:
        return 1
    if n == 0 or k == 0 : return 0

    return k*RecPart(n-1, k) + RecPart(n-1, k-1)
def S(n,k,prefix, exactly = False):
    l = len(prefix)
    d = prefix[-1]
    if exactly:
        "  u = 0 "
        return RecPart(n-l,k-1) * RecComb(n-d, 0)
    else:
        nb_Part = 0
        end_val = n-k-l+1
        for u in range(0, end_val+1):
            nb_Part += RecPart(n-(l+u),k-1) * RecComb(n-d, u)
        return nb_Part

print(S(5,3,[1]))


def gen_helper(n, k, rank, startPoint):
    block = []
    nb_Part = 0
    test_number = startPoint
    exactly = False

    while rank != nb_Part:
        if not exactly:
            prefix = block + [test_number]
        else:
            prefix = block  # Maintain block when exactly is True

        nb_Part = S(n, k, prefix, exactly)

        print("-------------------------")
        print(f"Nb_part = {nb_Part}")
        print(f"rank = {rank}")
        print(f"block = {block}")
        print(f"prefix = {prefix}")
        print(f"exactly? = {exactly}")
        print("----------------------------")

        if exactly and rank <= nb_Part:
            return block, nb_Part
        if rank < nb_Part:
            block.append(test_number)
            exactly = True
        elif rank > nb_Part:
            rank -= nb_Part
            if not exactly:
                test_number += 1  # Ensure we move to the next test_number
            else:
                exactly = False
                test_number +=1  # Set test_number correctly

    return block, nb_Part

block , part = gen_helper(5,3,20,1)

print("block : ", block , " part = ", part)