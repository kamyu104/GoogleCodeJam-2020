# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1C - Problem C. Oversized Pancake Choppers
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef4/00000000003179a1
#
# Time:  O(D^2 * logD + NlogN + log(max(A) * D * N) * N + D * N * log(max(A)) + D * N)
#        = O(D * N * log(max(A)))
# Space: O(D * N)
#

from collections import defaultdict
from bisect import bisect_left

def gcd(a, b):  # Time: O(log(a + b))
    while b:
        a, b = b, a % b
    return a

def binary_search_right(left, right, check):  # Time: O(log(max(A) * D * N) * N)
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
    for y in xrange(1, D+1):  # Time: O(D * N * log(max(A)))
        for x in A:
            if x*(lcm//y) > limit:
                break
            common = gcd(x, y)
            lookup[x//common, y//common].append(lookup[x//common, y//common][-1]+y)
    result = 0
    for k, count in lookup.iteritems():  # Time: O(D * N)
        c = bisect_left(count, D)  # sum(len(count)) = O(D * N)
        result = max(result, (c-int(count[c] != D)) if c != len(count) else c-1)
    return D-result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, oversized_pancake_choppers())
