# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 3 - Problem C. Pen Testing
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff7e/0000000000377630
#
# Time:  O(T * N^2), S is the number of dead and used states, pass in PyPy2 but Python2 due to no memoization
# Space: O(N * T), use heuristic without memoization
#
# Usage: python interactive_runner.py python local_testing_tool.py 2 -- python pen_testing_heuristic.py
#
# Expected Success Rate: ~64.1% (8736823189/13621608000 = 0.6413944072535342)
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

def careful_writing_prob(dead_mask, alive_used_count):  # Time: O(N)
    x = next(i for i in xrange(N) if not (dead_mask & POW[i]))
    return sum(prob(dead_mask | POW[x], (x+1,)*i + alive_used_count[i+1:])
               for i in xrange(len(alive_used_count))) / len(alive_used_count)

def heuristic(dead_mask, alive_used_count):  # Time: O(N * states)
    option_p = (RETURN, prob(dead_mask, alive_used_count))
    if len(alive_used_count) > 2:
        careful_writing_p = careful_writing_prob(dead_mask, alive_used_count)
        if careful_writing_p > option_p[1]:
            option_p = (CAREFUL, careful_writing_p)
    return option_p

def gen(used_count=None, option=None):
    if option == RETURN:
        while True:
            yield -1
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

def decide(gens, used_counts, questions):
    for t in xrange(T):
        questions[t] = next(gens[t], None)
        if questions[t] is not None:
            continue
        gens[t] = gen(used_counts[t], heuristic(reduce(or_, (POW[-i-1] for i in used_counts[t] if i < 0), 0), tuple(i for i in used_counts[t] if i >= 0))[0])
        questions[t] = next(gens[t])

def pen_testing():
    gens, used_counts, questions = [gen() for _ in xrange(T)], [[0]*N for _ in xrange(T)], [None for _ in xrange(T)]
    while True:
        decide(gens, used_counts, questions)
        if answer(questions, used_counts):
            break
        query(questions, used_counts)

RETURN, CAREFUL = range(2)
T, N, C = map(int, raw_input().strip().split())
POW = [1]
for i in xrange(N-1):
    POW.append(POW[-1]*2)
pen_testing()
