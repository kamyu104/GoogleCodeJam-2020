# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1C - Problem A. Overexcited Fan
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef4/0000000000317409
#
# Time:  O(M)
# Space: O(1)
#

def overexcited_fan():
    X, Y, M = raw_input().strip().split()
    X, Y = int(X), int(Y)
    for t, d in enumerate(M, 1):
        X, Y = X+LOOKUP[d][0], Y+LOOKUP[d][1]
        if t >= abs(X)+abs(Y):
            return t
    return "IMPOSSIBLE"

LOOKUP = {'E':(1, 0), 'S':(0, -1), 'W':(-1, 0), 'N': (0, 1)}
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, overexcited_fan())
