# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1C - Problem B. Overexcited Fan
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef4/00000000003179a1
#
# Time:  O(L * U)
# Space: O(1)
#

from collections import defaultdict

def overrandomized():
    U = input()
    result, count = set(), defaultdict(int)
    for _ in xrange(L):
        _, R = raw_input().strip().split()
        result.add(R[-1])
        if len(R) == U:
            count[R[0]] += 1
    return "".join(list(result-set(count.keys())) +
                   sorted(count.keys(), key=lambda x:count[x], reverse=True))

L = 10**4
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, overrandomized())
