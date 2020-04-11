# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1A - Problem B. Pascal Walk
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd74/00000000002b1353
#
# Time:  O(logN^2)
# Space: O(1)
#

def pattern_matching():
    N = input()
    rows = min(N, MIN_R)
    N -= rows
    lookup = set()
    row_sum = 2**(rows-1)
    for r in reversed(xrange(1, rows+1)):
        if N >= row_sum-1:
            N -= row_sum-1
            lookup.add(r)
        row_sum //= 2
    rows += N
    result, side = [], 1
    for r in xrange(1, rows+1):
        if r not in lookup:
            if side:
                result.append((r, 1))
            else:
                result.append((r, r))
            continue
        if side:
            result.extend((r, c) for c in xrange(1, r+1))
        else:
            result.extend((r, c) for c in reversed(xrange(1, r+1)))
        side ^= 1        
    return "\n".join( map(lambda x: "{} {}".format(x[0], x[1]), result))

MAX_N = 10**9
MIN_R = ((MAX_N+1)-1).bit_length()  # 2^R-1 >= MAX_N, R >= log2(MAX_N+1)
for case in xrange(input()):
    print 'Case #%d: \n%s' % (case+1, pattern_matching())
