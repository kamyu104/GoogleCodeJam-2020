# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 3 - Problem C. Pen Testing
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff7e/0000000000377630
#
# Time:  O(T * N^2 + N * S), S is the number of dead and used states
# Space: O(N * (T + S))
#

from sys import stdout
from collections import defaultdict
from operator import or_
from fractions import Fraction

def prob(dead_mask, alive_used_count):  # Time: O(N)
    arr = tuple(i for i in xrange(N) if not (dead_mask & POW[i]))
    good, bad = 0, 0
    left, right = 0, len(arr)-1
    while left < right:
        if arr[left]+arr[right]-alive_used_count[-1]-alive_used_count[-2] >= N:
            good += right-left
            right -= 1
        else:
            bad += right-left
            left += 1
    return Fraction(good, (good+bad))

def leftmost_used_up_prob(dead_mask, alive_used_count, lookup):  # Time: O(N)
    return (sum(memoization(dead_mask | POW[i], alive_used_count[1:], lookup)[1] for i in xrange(N) if not (dead_mask & POW[i])) / len(alive_used_count),
            sum(prob(dead_mask | POW[i], alive_used_count[1:]) for i in xrange(N) if not (dead_mask & POW[i])) / len(alive_used_count))

def careful_writing_prob(dead_mask, alive_used_count, lookup):  # Time: O(N)
    x = next(i for i in xrange(N) if not (dead_mask & POW[i]))
    return (sum(memoization(dead_mask | POW[x], (x+1,)*i + alive_used_count[i+1:], lookup)[1] for i in xrange(len(alive_used_count))) / len(alive_used_count),
            sum(prob(dead_mask | POW[x], (x+1,)*i + alive_used_count[i+1:]) for i in xrange(len(alive_used_count))) / len(alive_used_count))

def memoization(dead_mask, alive_used_count, lookup):  # Time: O(N * states)
    if alive_used_count not in lookup[dead_mask]:
        if USE_LEFTMOST:  # there is no effect of normalization for careful only, so just skip if careful only
            min_count = min(next(i for i in xrange(N) if not (dead_mask & POW[i])), min(alive_used_count))
            if min_count:  # normalized to reduce the number of duplicated states from 1346148 to 832025
                return memoization(reduce(or_, (POW[i-min_count] for i in xrange(N) if (dead_mask & POW[i]) or i-min_count < 0)), tuple(c-min_count for c in alive_used_count), lookup)
        ev = prob(dead_mask, alive_used_count)
        option_p = (RETURN, ev, ev)
        if len(alive_used_count) > 2:
            if USE_LEFTMOST:
                leftmost_used_up_p = leftmost_used_up_prob(dead_mask, alive_used_count, lookup)
                if leftmost_used_up_p[STRATEGY] > option_p[STRATEGY+1]:
                    option_p = (LEFTMOST, leftmost_used_up_p[0], leftmost_used_up_p[1])
            careful_writing_p = careful_writing_prob(dead_mask, alive_used_count, lookup)
            if careful_writing_p[STRATEGY] > option_p[STRATEGY+1]:
                option_p = (CAREFUL, careful_writing_p[0], careful_writing_p[1])
        lookup[dead_mask][alive_used_count] = option_p
    return lookup[dead_mask][alive_used_count]

def demask(mask):
    result = []
    for i in xrange(N):
        if not (mask & POW[i]):
            result.append(i)
    return result

USE_LEFTMOST = True
MEMOIZATION, HEURISTIC = range(2)
STRATEGY = MEMOIZATION
N = 15
POW = [1]
RETURN, LEFTMOST, CAREFUL = range(3)
for i in xrange(N-1):
    POW.append(POW[-1]*2)

lookup = defaultdict(dict)

# find specific state success rate
alive = (7, 8, 9)
alive_used_count = (1, 0, 0)
print "alive:", alive, "alive_used_count:", alive_used_count
print "return   - ev: %10s, prob: %10s" % ((prob(reduce(or_, (POW[i] for i in xrange(N) if i not in alive)), alive_used_count),)*2)
if USE_LEFTMOST: print "leftmost - ev: %10s, prob: %10s" % leftmost_used_up_prob(reduce(or_, (POW[i] for i in xrange(N) if i not in alive)), alive_used_count, lookup)
print "careful  - ev: %10s, prob: %10s" % careful_writing_prob(reduce(or_, (POW[i] for i in xrange(N) if i not in alive)), alive_used_count, lookup)

# find expected success rate
print "option: %s,: ev: %s, prob: %s" % memoization(0, (0,)*N, lookup)
print "key_count: %s, state_count: %s" % (len(lookup.keys()), sum(len(v) for v in lookup.itervalues()))

# list each number of states
# for k, v in lookup.iteritems():
#     print demask(k), len(v)
