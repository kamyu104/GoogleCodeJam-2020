# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1B - Problem C. Join the Ranks
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b64
#
# Time:  O(R^2 * S^2)
# Space: O(R * S)
#

def find_len_of_target(deck, start, check):
    for i in xrange(start, len(deck)):
        if check(deck[i]):
            break
    for j in xrange(i, len(deck)):
        if deck[j] != deck[i]:
            break
    return j-start

def join_the_ranks():
    R, S = map(int, raw_input().strip().split())
    result, deck = [], range(1, R+1)*S
    for _ in xrange((R*S-R)//2):  # each step, decrease the number of adjacent cards of different ranks from (R*S-1) to (R-1) by 2
        len_A = find_len_of_target(deck, 0, lambda x: x != deck[0])
        len_B = find_len_of_target(deck, len_A, lambda x: x == deck[0])
        assert(len_A+len_B < len(deck))  # the rank of the last card is always R and won't be exchanged in these steps
        result.append((len_A, len_B))
        deck[:] = deck[len_A:len_A+len_B] + deck[:len_A] + deck[len_A+len_B:]
    if (R*S-R)%2:  # if odd, decrease the number of adjacent cards of different ranks from R to (R-1) by 1
        result.append((S-1, len(deck)-(S-1)))  # in the last step, the ranks of the top S-1 cards and the last one must be all R, and the others are sorted
        deck[:] = deck[S-1:] + deck[:S-1]
    assert(all(deck[i] <= deck[i+1] for i in xrange(len(deck)-1)) and
           sum(deck[i] != deck[i+1] for i in xrange(len(deck)-1)) == R-1)
    return "{}\n{}".format(len(result), "\n".join(map(lambda x: "{} {}".format(*x), result)))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, join_the_ranks())
