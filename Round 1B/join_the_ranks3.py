# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1B - Problem C. Join the Ranks
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b64
#
# Time:  O(R * S), optimized from join_the_ranks2.py
# Space: O(1)
#

from collections import deque

def group_gen(R, S):
    for i in xrange(1, S):
        for _ in xrange(R):
            yield i

def join_the_ranks():
    R, S = map(int, raw_input().strip().split())
    result, it = [], group_gen(R, S)
    for l in xrange(R+1, R*S, 2):
        # each step, merge 2 groups with the same rank, and keep the invariant:
        # 1. each group with rank X is followed by the group with rank (X+1) mod R
        # 2. the last group is not merged until it is the last step
        # each 2 groups (a, b) results in a pattern of sequence: 1*R, 2*R, ..., (S-1)*R
        a, b = next(it), next(it)
        result.append((a+b, l-(a+b)))
    a = next(it, None)
    if a:  # case: R*(S-1), 1*S, 2*S, ..., (R-1)*S, R*1
        assert(a == S-1)
        result.append((a , R*S-a))
    return "{}\n{}".format(len(result), "\n".join(map(lambda x: "{} {}".format(*x), result)))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, join_the_ranks())
