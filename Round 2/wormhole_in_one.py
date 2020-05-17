# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 2 - Problem C. Wormhoe in One
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ffb9/00000000003386d0
#
# Time:  O(N^2)
# Space: O(N^2)
#

from collections import defaultdict

def gcd(a, b):  # Time: O(log(a + b))
    while b:
        a, b = b, a % b
    return a

def wormhole_in_one():
    N = input()
    H = []
    for _ in xrange(N):
        H.append(map(int, raw_input().strip().split()))
    directions = defaultdict(set)
    for i in xrange(len(H)):
        x1, y1 = H[i]
        for j in xrange(len(H)):
            if i == j:
                continue
            x2, y2 = H[j]
            a, b = y2-y1, x2-x1
            if b == 0:
                a = 1
            else:
                if b < 0:
                    a, b = -a, -b
                common = gcd(abs(a), b)
                a, b = a//common, b//common
            directions[a, b].add(j)
    result = 1
    for points in directions.itervalues():
        result = max(result, len(points)+min(1 if len(points)%2 else 2, N-len(points)))
    return result
    
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, wormhole_in_one())
