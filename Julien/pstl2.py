# https://en.wikipedia.org/wiki/Stirling_numbers_of_the_second_kind#Recurrence_relation
# { n k } = k*{ n-1 k } + { n-1 k-1 }
#         = (14 2 3, 1 24 3, 1 2 34)  +  (12 3 4, 1 23 4, 13 2 4)
# Répartir n boules dans k sacs, min.1 par sac

import random

def fact (n) :
    if n == 0 :
        return 1
    return n * fact(n-1)

# L'ordre des sacs n'est pas pris en compte

def stirling(n,k):
    if (k == n):
        return 1
    if (k == 0 or n == 0):
        return 0
    return k*stirling(n-1,k)+stirling(n-1,k-1)

# def partition(n,k):
#     if (n <= 0):
#         return []
#     if (k == 0):
#         return partition(n-1,k) + [n]
#     if (k == n):
#         return partition(n-1,k-1) + [n]
#     x = random.random()
#     if (x <= stirling(n-1,k-1)/stirling(n,k)):
#         return partition(n-1,k-1) + [n]
#     else :
#         return [partition(n-1,k) + [n]]

def partition(n,k):
    part = []
    tmp = []
    for i in range (0,k):
        part.append([])
    part = partition_aux(n,k,part,tmp)
    for t in tmp :
        x = random.randint(0,k-1)
        part[x].append(t)
    return part

def partition_aux(n,k,l,tmp):
    if (n <= 0):
        return l
    if (k == 0):
        tmp.append(n)
        return partition_aux(n-1,k,l,tmp)
    if (k == n):
        for i in l:
            if i == []:
                i.append(n)
                break
        return partition_aux(n-1,k-1,l,tmp)
    x = random.random()
    # print(stirling(n-1,k-1)/stirling(n,k))
    if (x <= stirling(n-1,k-1)/stirling(n,k)):
        for i in l:
            if i == []:
                i.append(n)
                break
        return partition_aux(n-1,k-1,l,tmp)
    else :
        tmp.append(n)
        return partition_aux(n-1,k,l,tmp) 

# L'ordre des sacs est pris en compte

def stirling2(n,k):
    return fact(k)*stirling(n,k)

def partition2(n,k):
    return

n = 3
k = 2

print(stirling(n,k))
print(partition(n,k))
# print(stirling2(n,k))
# print(partition2(n,k))

# Verification de l'uniformite pour le cas { 3 2 }

p12 = 0
p13 = 0
p23 = 0
for i in range (1,10000) :
    l = partition(n,k)
    if (l[0] == [3] or l[1] == [3]):
        p12 += 1
    elif (l[0] == [2] or l[1] == [2]):
        p13 += 1
    elif (l[0] == [1] or l[1] == [1]):
        p23 += 1

print("p12 = ", p12/100, "\np13 = ", p13/100, "\np23 = ",p23/100)
