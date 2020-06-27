# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 3 - Problem C. Pen Testing
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff7e/0000000000377630
#
# Time:  O(T * N^2 + N * S), S is the number of dead and used states, pass in Python2 but sometimes TLE
# Space: O(N * (T + S))
#
# Usage: python interactive_runner.py python local_testing_tool.py 0 -- python pen_testing.py
#
# Ultimate Solution - Expected Success Rate: ~64.4% (84215420099/130767436800 = 0.6440091062410425)
#

from sys import stdout
from collections import defaultdict
from operator import or_

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
    return 1.0*good/(good+bad)

def leftmost_used_up_prob(dead_mask, alive_used_count):  # Time: O(N)
    return sum(memoization(dead_mask | POW[i], alive_used_count[1:], lookup)[1]
               for i in xrange(N) if not (dead_mask & POW[i])) / len(alive_used_count)

def careful_writing_prob(dead_mask, alive_used_count):  # Time: O(N)
    x = next(i for i in xrange(N) if not (dead_mask & POW[i]))
    return sum(memoization(dead_mask | POW[x], (x+1,)*i + alive_used_count[i+1:], lookup)[1]
               for i in xrange(len(alive_used_count))) / len(alive_used_count)

def memoization(dead_mask, alive_used_count, lookup):  # Time: O(N * states)
    if alive_used_count not in lookup[dead_mask]:
        min_count = min(next(i for i in xrange(N) if not (dead_mask & POW[i])), min(alive_used_count))
        if min_count:  # normalized to reduce the number of duplicated states from 1346148 to 832025
            return memoization(reduce(or_, (POW[i-min_count] for i in xrange(N) if (dead_mask & POW[i]) or i-min_count < 0)), tuple(c-min_count for c in alive_used_count), lookup)
        option_p = (RETURN, prob(dead_mask, alive_used_count))
        if len(alive_used_count) > 2:
            leftmost_used_up_p = leftmost_used_up_prob(dead_mask, alive_used_count)
            if leftmost_used_up_p > option_p[1]:
                option_p = (LEFTMOST, leftmost_used_up_p)
            careful_writing_p = careful_writing_prob(dead_mask, alive_used_count)
            if careful_writing_p > option_p[1]:
                option_p = (CAREFUL, careful_writing_p)
        lookup[dead_mask][alive_used_count] = option_p
    return lookup[dead_mask][alive_used_count]

def gen(used_count=None, option=None):
    if option == RETURN:
        while True:
            yield -1
    elif option == LEFTMOST:
        i = next(i for i in xrange(N) if used_count[i] >= 0)
        while 0 <= used_count[i]:
            yield i
    elif option == CAREFUL:
        dead_mask = reduce(or_, (POW[-i-1] for i in used_count if i < 0), 0)
        x = next(i for i in xrange(N) if not (dead_mask & POW[i]))
        for i in xrange(N):
            if used_count[i] < 0:
                continue
            while 0 <= used_count[i] < x+1:
                yield i
            if used_count[i] < 0:
                break

def query(questions, used_counts):
    print " ".join(map(lambda x: str(x+1), questions))
    stdout.flush()
    for t, r in enumerate(map(int, (raw_input().strip().split()))):
        if questions[t] == -1:
            continue
        used_counts[t][questions[t]] += 1
        if not r:
            used_counts[t][questions[t]] *= -1

def answer(questions, used_counts):
    if any(i != -1 for i in questions):
        return False
    print " ".join(map(lambda x: str(x+1), questions))
    stdout.flush()
    alives = [[] for _ in xrange(T)]
    for t in xrange(T):
        for i in reversed(xrange(N)):
            if used_counts[t][i] < 0:
                continue
            alives[t].append(i)
            if len(alives[t]) == 2:
                break
    print " ".join(map(lambda x: "{} {}".format(x[0]+1, x[1]+1), alives))
    stdout.flush()
    return True

def pen_testing(lookup, gens, used_counts, questions):
    for t in xrange(T):
        questions[t] = next(gens[t], None)
        if questions[t] is not None:
            continue
        gens[t] = gen(used_counts[t], memoization(reduce(or_, (POW[-i-1] for i in used_counts[t] if i < 0), 0), tuple(i for i in used_counts[t] if i >= 0), lookup)[0])
        questions[t] = next(gens[t])

RETURN, LEFTMOST, CAREFUL = range(3)
T, N, C = map(int, raw_input().strip().split())
POW = [1]
for i in xrange(N-1):
    POW.append(POW[-1]*2)
lookup = defaultdict(dict)
gens, used_counts, questions = [gen() for _ in xrange(T)], [[0]*N for _ in xrange(T)], [None for _ in xrange(T)]
while True:
    pen_testing(lookup, gens, used_counts, questions)
    if answer(questions, used_counts):
        break
    query(questions, used_counts)
