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
    for l in xrange(R+1, R*S, 2):  # each step, decrease the number of adjacent cards of different ranks from (R*S-1) to (R-1) by 2, and sort extra 2 cards without the last one
        result.append((groups[0]+groups[1], l-(groups[0]+groups[1])))
        groups[R], groups[R+1] = groups[R]+groups[0], groups[1]+groups[R+1]
        groups.popleft(), groups.popleft()
        groups.extend([1]*(min(R*S-(l+1), 2)))
    if R*S-(l+1) == 1:  # if odd, decrease the number of adjacent cards of different ranks from R to (R-1) by 1
        assert(groups[0] == S-1 and groups[-1] == 1)
        result.append((groups[0], R*S-groups[0]))  # in the last step, the ranks of the top S-1 cards and the last one must be all R, and the others are sorted
        groups[-1] = groups[-1]+groups[0]
        groups.popleft()
    assert(len(groups) == R and all(x == groups[0] for x in groups))
    return "{}\n{}".format(len(result), "\n".join(map(lambda x: "{} {}".format(*x), result)))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, join_the_ranks())
