# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1B - Problem C. Join the Ranks
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b64
#
# Time:  O(R^2 * S^2)
# Space: O(R * S)
#

def find_len_A(deck):
    for i in xrange(1, len(deck)):
        if deck[i] != deck[0]:
            break
    for j in xrange(i+1, len(deck)):
        if deck[j] != deck[i]:
            break
    return j

def join_the_ranks():
    R, S = map(int, raw_input().strip().split())
    result, deck = [], range(1, R+1)*S
    for l in xrange(R+1, R*S, 2):  # each step, decrease the number of adjacent cards of different ranks from (R*S-1) to (R-1) by 2
        len_A = find_len_A(deck)
        result.append((len_A, l-len_A))
        deck[:] = deck[len_A:l] + deck[:len_A] + deck[l:]
    if (R*S-R)%2:  # if odd, decrease the number of adjacent cards of different ranks from R to (R-1) by 1
        result.append((S-1, len(deck)-(S-1)))  # in the last step, the ranks of the top S-1 cards and the last one must be all R, and the others are sorted
        deck[:] = deck[S-1:] + deck[:S-1]
    return "{}\n{}".format(len(result), "\n".join(map(lambda x: "{} {}".format(*x), result)))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, join_the_ranks())
