# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Qualification Round - Problem C. Parenting Partnering Returns
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd27/000000000020bdf9
#
# Time:  O(NlogN)
# Space: O(1)
#

def parenting_partnering_returns():
    N = input()
    intervals = sorted(map(int, raw_input().strip().split()) + [i] for i in xrange(N))
    result, c_e, j_e = [None]*N, 0, 0
    for s, e, i in intervals:
        if c_e <= s:
            c_e = e
            result[i] = 'C'
        elif j_e <= s:
            j_e = e
            result[i] = 'J'
        else:
            return "IMPOSSIBLE"
    return "".join(result)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, parenting_partnering_returns())
