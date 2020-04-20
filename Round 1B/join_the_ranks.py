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

def find_len_B(deck, start):
    for i in xrange(start, len(deck)):
        if deck[i] == deck[0]:
            break
    for j in xrange(i+1, len(deck)):
        if deck[j] != deck[i]:
            break
    return j-start

def join_the_ranks():
    R, S = map(int, raw_input().strip().split())
    result, deck = [], range(1, R+1)*S
    for _ in xrange((R*S-R)//2):
        len_A = find_len_A(deck)
        len_B = find_len_B(deck, len_A)
        assert(len_A+len_B < len(deck))
        result.append((len_A, len_B))
        deck[:] = deck[len_A:len_A+len_B] + deck[:len_A] + deck[len_A+len_B:]
    if (R*S-R)%2:
        result.append((S-1, len(deck)-(S-1)))
        deck[:] = deck[S-1:] + deck[:S-1]
    return "{}\n{}".format(len(result), "\n".join(map(lambda x: "{} {}".format(*x), result)))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, join_the_ranks())
