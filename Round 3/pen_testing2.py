# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 3 - Problem C. Pen Testing
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff7e/0000000000377630
#
# Time:  O(T * N^2 + N * S), S is the number of dead and used states, pass in Python2 but sometimes TLE
# Space: O(N * S)
#
# Usage: python interactive_runner.py python local_testing_tool.py 0 -- pypy pen_testing.py
#
# Ultimate Solution - Success Rate: ~64.4%
#

from sys import stdout
from collections import defaultdict
from operator import or_

def prob(dead_mask, used_count):  # Time: O(N)
    arr = [i for i in xrange(N) if not (dead_mask & POW[i])]
    good, bad = 0, 0
    left, right = 0, len(arr)-1
    while left < right:
        if arr[left]+arr[right]-used_count[-1]-used_count[-2] >= N:
            good += right-left
            right -= 1
        else:
            bad += right-left
            left += 1
    return 1.0*good/(good+bad)

def leftmost_used_up_prob(dead_mask, used_count):  # Time: O(N)
    p = 0.0
    for i in xrange(N):
        if dead_mask & POW[i]:
            continue
        p += prob(dead_mask | POW[i], used_count[1:])
    return p / len(used_count)

def careful_writing_prob(dead_mask, used_count):  # Time: O(N)
    p = 0.0
    for x in xrange(N):
        if not (dead_mask & POW[x]):
            break
    for i in xrange(len(used_count)):
        p += prob(dead_mask | POW[x], (x+1,)*i + used_count[i+1:])
    return p / len(used_count)

def memoization(dead_mask, used_count, lookup):  # Time: O(N * states)
    if used_count not in lookup[dead_mask]:
        curr_p = (0, prob(dead_mask, used_count))
        if len(used_count) > 2:
            leftmost_used_up_p = leftmost_used_up_prob(dead_mask, used_count)
            if leftmost_used_up_p > curr_p[1]:
                curr_p = (1, leftmost_used_up_p)
            careful_writing_p = careful_writing_prob(dead_mask, used_count)
            if careful_writing_p > curr_p[1]:
                curr_p = (2, careful_writing_p)
        lookup[dead_mask][used_count] = curr_p
    return lookup[dead_mask][used_count]

def gen(used_count, option):
    if option == 1:
        i = next(i for i in xrange(N) if used_count[i] >= 0)
        while 0 <= used_count[i]:
            yield i
    elif option == 2:
        x = -min(used_count)+1
        for i in xrange(N):
            if used_count[i] < 0:
                continue
            while 0 <= used_count[i] < x:
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

def pen_testing(lookup, options, used_counts, questions):
    for t in xrange(T):
        if options[t] is not None:
            questions[t] = next(options[t], None)
            if questions[t] is not None:
                continue
        option = memoization(reduce(or_, (POW[-i-1] for i in used_counts[t] if i < 0), 0), tuple(i for i in used_counts[t] if i >= 0), lookup)[0]
        if not option:
            questions[t] = -1
            continue
        options[t] = gen(used_counts[t], option)
        questions[t] = next(options[t])

T, N, C = map(int, raw_input().strip().split())
POW = [1]
for i in xrange(N-1):
    POW.append(POW[-1]*2)
lookup = defaultdict(dict)
options, used_counts, questions = [None for _ in xrange(T)], [[0]*N for _ in xrange(T)], [None for _ in xrange(T)]
while True:
    pen_testing(lookup, options, used_counts, questions)
    if answer(questions, used_counts):
        break
    query(questions, used_counts)
