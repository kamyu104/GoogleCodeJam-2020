# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1B - Problem C. Join the Ranks
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b64
#
# Time:  O(R * S)
# Space: O(R)
#

from collections import deque

def join_the_ranks():
    R, S = map(int, raw_input().strip().split())
    result, groups = [], deque([1]*(R+2))
    for l in xrange(R+1, R*S, 2):
        # each step, merge 2 groups with the same rank, and keep the invariant:
        # 1. each group with rank X is followed by the group with rank (X+1) mod R
        # 2. the last group is not merged until it is the last step
        result.append((groups[0]+groups[1], l-(groups[0]+groups[1])))
        groups[R], groups[R+1] = groups[R]+groups[0], groups[1]+groups[R+1]
        groups.popleft(), groups.popleft()
        groups.extend([1]*(min(R*S-(l+1), 2)))
    if len(groups) == R+1:  # case: R*(S-1), 1*S, 2*S, ..., (R-1)*S, R*1
        assert(groups[0] == S-1 and groups[-1] == 1)
        result.append((groups[0], R*S-groups[0]))
        groups[-1] = groups[-1]+groups[0]  # merge the last group with the first one
        groups.popleft()
    assert(len(groups) == R and all(x == S for x in groups))
    return "{}\n{}".format(len(result), "\n".join(map(lambda x: "{} {}".format(*x), result)))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, join_the_ranks())
