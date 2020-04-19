# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1B - Problem A. Expogo
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b62
#
# Time:  O(logX + logY)
# Space: O(1)
#

def expogo():
    X, Y = map(int, raw_input().strip().split())
    x, y = abs(X), abs(Y)
    if (x+y)%2 == 0:
        return "IMPOSSIBLE"
    lookup = ['E', 'W', 'N', 'S']
    if X < 0:
        lookup[E], lookup[W] = lookup[W], lookup[E]
    if Y < 0:
        lookup[N], lookup[S] = lookup[S], lookup[N]
    result = []
    while (x, y) not in TARGET:
        if x%2:
            if ((x-1)//2+y//2)%2:
                x, y = (x-1)//2, y//2
                result.append(E)
            else:
                x, y = (x+1)//2, y//2
                result.append(W)
        else:
            if (x//2+(y-1)//2)%2:
                x, y = x//2, (y-1)//2
                result.append(N)
            else:
                x, y = x//2, (y+1)//2
                result.append(S)
    result.append(E if x else N)
    return "".join(lookup[d] for d in result)

E, W, N, S = range(4)
TARGET = set([(1, 0), (0, 1)])
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, expogo())
