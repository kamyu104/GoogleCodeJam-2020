# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1C - Problem C. Oversized Pancake Choppers
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef4/00000000003172d1
#
# Time:  O(D * log(D!) + NlogN + log(max(A) * D!) * N + D * N)
#        = O(D^2 * logD + NlogN + log(max(A)) * N + DlogD * N + D * N)
#        = O(N * DlogD)
# Space: O(D * N)
#

from collections import defaultdict
from bisect import bisect_left

def gcd(a, b):  # Time: O(log(a + b))
    while b:
        a, b = b, a % b
    return a

def binary_search_right(left, right, check):  # Time: O(log(max(A) * D!) * N)
    while left <= right:
        mid = left + (right-left)//2
        if not check(mid):
            right = mid-1
        else:
            left = mid+1
    return right

def oversized_pancake_choppers():
    N, D = map(int, raw_input().strip().split())
    lcm = 1
    for i in xrange(2, D+1):  # Time: O(D^2 * logD)
        lcm = lcm * i // gcd(lcm, i)
    A = sorted(map(int, raw_input().strip().split()))  # Time: O(NlogN)
    limit = binary_search_right(1, max(A)*lcm, lambda a: sum(x*lcm//a for x in A) >= D)
    lookup = defaultdict(lambda: [0])
    for y in xrange(1, D+1):  # Time: O(D * N)
        for x in A:
            key = x*(lcm//y)
            if key > limit:
                break
            lookup[key].append(lookup[key][-1]+y)
    result = 0
    for count in lookup.itervalues():  # Time: O(D * N)
        c = bisect_left(count, D)  # sum(len(count)) = O(D * N)
        result = max(result, (c-int(count[c] != D)) if c != len(count) else c-1)
    return D-result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, oversized_pancake_choppers())
