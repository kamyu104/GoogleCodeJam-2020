# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1B - Problem A. Expogo
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b62
#
# Time:  O(log|X| + log|Y|)
# Space: O(1)
#

def expogo():
    X, Y = map(int, raw_input().strip().split())
    if (abs(X)+abs(Y))%2 == 0:
        return "IMPOSSIBLE"
    N, total = 0, 0
    while not (total >= abs(X)+abs(Y)):
        N = 1 if not N else N*2
        total += N
    result = []
    while N:
        if abs(X) > abs(Y):
            if X > 0: 
                result.append('E')
                X -= N
            else:
                result.append('W')
                X += N
        else:
            if Y > 0:
                result.append('N')
                Y -= N
            else:
                result.append('S')
                Y += N
        N //= 2
    return "".join(reversed(result))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, expogo())
