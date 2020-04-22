# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1B - Problem C. Join the Ranks
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b64
#
# Time:  O(R * S), one-liner, optimized from join_the_ranks4.py
# Space: O(1)
#

def join_the_ranks():
    R, S = map(int, raw_input().strip().split())
    # each step, merge 2 groups with the same rank, and keep the invariant:
    # 1. each group with rank X is followed by the group with rank (X+1) mod R
    # 2. the last group is not merged until it is the last step
    # => each 2 groups (a, b) or odd group (a,) in the last step sequences in a pattern: 1*R, 2*R, ..., (S-1)*R
    return "{}\n{}".format(((S-1)*R+1)//2, "\n".join(map(lambda x: "{} {}".format(x[0]+x[1], x[2]-(x[0]+x[1])), ((i//R+1, (i+1)//R+1 if i+1 != (S-1)*R else 0, R+1+i) for i in xrange(0, (S-1)*R, 2)))))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, join_the_ranks())
