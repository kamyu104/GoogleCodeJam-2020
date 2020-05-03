# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1C - Problem C. Oversized Pancake Choppers
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef4/00000000003172d1
#
# Time:  O(NlogN + log(max(A) * D^2) * N + D * N * log(max(A)) + D * N)
#        = O(D * N * log(max(A))), dealing fraction with bucket
# Space: O(D * N)
#

from collections import defaultdict
from bisect import bisect_left

def gcd(a, b):  # Time: O(log(a + b))
    while b:
        a, b = b, a % b
    return a

def binary_search_right(left, right, check):  # Time: O(log(max(A) * D^2) * N)
    while left <= right:
        mid = left + (right-left)//2
        if not check(mid):
            right = mid-1
        else:
            left = mid+1
    return right

def oversized_pancake_choppers():
    N, D = map(int, raw_input().strip().split())
    bucket_size = D*(D-1)  # 1/bucket_size <= 1/(D-1)-1/D, => bucket_size >= D*(D-1)
    A = sorted(map(int, raw_input().strip().split()))  # Time: O(NlogN)
    limit = binary_search_right(1, max(A)*bucket_size, lambda a: sum(x*bucket_size//a for x in A) >= D)
    lookup = defaultdict(lambda: [0])
    for y in xrange(1, D+1):  # Time: O(D * N * log(max(A)))
        prev = None
        for x in A:
            if x*bucket_size >= (limit+1)*y:
                break
            if x != prev and x*bucket_size > limit*y and not (sum(a*y//x for a in A) >= D):
                break  # unknown range of the buckets, check again (at most once due to at most one fraction in a bucket)
            prev = x
            common = gcd(x, y)
            lookup[x//common, y//common].append(lookup[x//common, y//common][-1]+y)
    result = 0
    for count in lookup.itervalues():  # Time: O(D * N)
        c = bisect_left(count, D)  # sum(len(count)) = O(D * N)
        result = max(result, (c-int(count[c] != D)) if c != len(count) else c-1)
    return D-result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, oversized_pancake_choppers())
