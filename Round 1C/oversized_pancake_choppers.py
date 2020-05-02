# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1C - Problem C. Oversized Pancake Choppers
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef4/00000000003179a1
#
# Time:  O(NlogN + log(D * N) * N + D * N * log(max(A)) + D * N)
#        = O(NlogN + D * N * log(max(A)))
# Space: O(D * N)
#

from collections import defaultdict
from bisect import bisect_left

def gcd(a, b):  # Time: O(log(a + b))
    while b:
        a, b = b, a % b
    return a

def binary_search_right(A, check):  # Time: O(log(D * N) * N)
    left, right = 0, len(A)-1
    while left <= right:
        mid = left + (right-left)//2
        if not check(A[mid]):
            right = mid-1
        else:
            left = mid+1
    return right

def oversized_pancake_choppers():
    N, D = map(int, raw_input().strip().split())
    A = sorted(map(int, raw_input().strip().split()))  # Time: O(NlogN)
    lookup = defaultdict(lambda: [0])
    for y in xrange(1, D+1):  # Time: O(D * N * log(max(A)))
        for x in A:
            common = gcd(x, y)
            lookup[x//common, y//common].append(lookup[x//common, y//common][-1]+y)
    targets = sorted(lookup.iterkeys(), cmp=lambda x, y: cmp(x[0]*y[1], x[1]*y[0]))
    M = 1
    for i in xrange(binary_search_right(targets, lambda a: sum(x*a[1]//a[0] for x in A) >= D)+1):  # Time: O(D * N)
        c = bisect_left(lookup[targets[i]], D)  # sum(len(lookup[targets[i]])) = O(D * N)
        M = max(M, (c-int(lookup[targets[i]][c] != D)) if c != len(lookup[targets[i]]) else c-1)
    return D-M

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, oversized_pancake_choppers())
