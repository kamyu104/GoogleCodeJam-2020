# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1B - Problem C. Join the Ranks
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b64
#
# Time:  O(R * S), optimized from join_the_ranks4.py
# Space: O(1)
#

def join_the_ranks():
    R, S = map(int, raw_input().strip().split())
    result = [((i//R+1)+((i+1)//R+1 if i+1 != (S-1)*R else 0), (R+1+i)-((i//R+1)+((i+1)//R+1 if i+1 != (S-1)*R else 0))) for i in xrange(0, (S-1)*R, 2)]
    return "{}\n{}".format(len(result), "\n".join(map(lambda x: "{} {}".format(*x), result)))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, join_the_ranks())
