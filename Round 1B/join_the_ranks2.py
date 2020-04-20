# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1B - Problem C. Join the Ranks
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b64
#
# Time:  O(R^2 * S)
# Space: O(R * S)
#

def join_the_ranks():
    R, S = map(int, raw_input().strip().split())
    result, groups = [], [1]*(R*S)
    groups.reverse()  # treat groups as stack
    for l in xrange(R+1, R*S, 2):  # each step, decrease the number of adjacent cards of different ranks from (R*S-1) to (R-1) by 2, and sort extra 2 cards without the last one
        new_groups = []
        while len(new_groups) < R+2:  # Time: O(R)
            new_groups.append(groups.pop())
        result.append((new_groups[0]+new_groups[1], l-(new_groups[0]+new_groups[1])))
        new_groups[:] = new_groups[2:R] + [new_groups[R]+new_groups[0]] + [new_groups[1]+new_groups[R+1]]
        while new_groups:
            groups.append(new_groups.pop())
    groups.reverse()  # restore groups
    if (R*S-R)%2:  # if odd, decrease the number of adjacent cards of different ranks from R to (R-1) by 1
        assert(groups[0] == S-1 and groups[-1] == 1)
        result.append((groups[0], R*S-groups[0]))  # in the last step, the ranks of the top S-1 cards and the last one must be all R, and the others are sorted
        groups[:] = groups[1:-1] + [groups[-1]+groups[0]]
    assert(len(groups) == R and all(x == groups[0] for x in groups))
    return "{}\n{}".format(len(result), "\n".join(map(lambda x: "{} {}".format(*x), result)))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, join_the_ranks())
