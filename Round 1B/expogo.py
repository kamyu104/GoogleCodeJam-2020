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
    result = []
    while (x, y) not in TARGET:
        if x%2:
            if ((x-1)//2+y//2)%2:
                x, y = (x-1)//2, y//2
                result.append('E' if X > 0 else 'W')
            else:
                x, y = (x+1)//2, y//2
                result.append('W' if X > 0 else 'E')
        else:
            if (x//2+(y-1)//2)%2:
                x, y = x//2, (y-1)//2
                result.append('N' if Y > 0 else 'S')
            else:
                x, y = x//2, (y+1)//2
                result.append('S' if Y > 0 else 'N')
    if x:
        result.append('E' if X > 0 else 'W')
    else:
        result.append('N' if Y > 0 else 'S')
    return "".join(result)

TARGET = set([(1, 0), (0, 1)])
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, expogo())
