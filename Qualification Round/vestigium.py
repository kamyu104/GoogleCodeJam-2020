# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Qualification Round - Problem A. Vestigium
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd27/000000000020993c
#
# Time:  O(N^2)
# Space: O(N)
#

from itertools import imap, izip

def vestigium():
    N = input()
    M = [map(int, raw_input().strip().split()) for _ in xrange(N)]
    return "{} {} {}".format(
            sum(M[i][i] for i in xrange(N)),
            sum(imap(lambda x: len(set(x)) != N, M)),
            sum(imap(lambda x: len(set(x)) != N, izip(*M)))
        )

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, vestigium())
