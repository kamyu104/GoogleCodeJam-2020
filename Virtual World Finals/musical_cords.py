# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Virtual World Finals - Problem D. Musical Cords
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff31/00000000003b532b
#
# Time:  O(NlogN + N * K) on average, pass in PyPy2 but Python2
# Space: O(N)
#

from math import sin, pi
from functools import partial
from collections import defaultdict
from random import randint

def nth_element(nums, n, compare=lambda a, b: a < b):
    def partition_around_pivot(left, right, pivot_idx, nums, compare):
        new_pivot_idx = left
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
        for i in xrange(left, right):
            if compare(nums[i], nums[right]):
                nums[i], nums[new_pivot_idx] = nums[new_pivot_idx], nums[i]
                new_pivot_idx += 1
        nums[right], nums[new_pivot_idx] = nums[new_pivot_idx], nums[right]
        return new_pivot_idx

    left, right = 0, len(nums) - 1
    while left <= right:
        pivot_idx = randint(left, right)
        new_pivot_idx = partition_around_pivot(left, right, pivot_idx, nums, compare)
        if new_pivot_idx == n:
            return
        elif new_pivot_idx > n:
            right = new_pivot_idx - 1
        else:  # new_pivot_idx < n
            left = new_pivot_idx + 1

def binary_search(left, right, check_fn): 
    while left <= right:
        mid = left + (right-left)//2
        if check_fn(mid):
            right = mid-1
        else:
            left = mid+1
    return left

def hash(i, j):
    return (i, j) if i < j else (j, i)

def f(R, D, L, i, j):
    return 2*R*sin(((D[j]-D[i])%NANODEGREE_360)*pi/NANODEGREE_360)+L[j]

def musical_cords():
    def is_overllaped(N, D, i, x):
        return 0 < (D[i%N]-D[x%N])%NANODEGREE_360 <= NANODEGREE_180

    def is_intersected(N, R, D, L, prev, curr, x):
        return f(R, D, L, x%N, curr%N) >= f(R, D, L, x%N, prev%N)

    N, R, K = map(int, raw_input().strip().split())
    D, L = [0]*N, [0]*N
    for i in xrange(N):
        D[i], L[i] = map(int, raw_input().strip().split())
    
    intervals = [[0, 0, 0]]
    for i in xrange(1, 2*N):  # Total Time: O(NlogN)
        left = i
        while intervals and i-intervals[-1][0] < N and 0 < (D[i%N]-D[intervals[-1][0]%N])%NANODEGREE_360 <= NANODEGREE_180 and \
              f(R, D, L, intervals[-1][0]%N, i%N) >= f(R, D, L, intervals[-1][0]%N, intervals[-1][2]%N) and \
              f(R, D, L, intervals[-1][1]%N, i%N) >= f(R, D, L, intervals[-1][1]%N, intervals[-1][2]%N):
            left = intervals[-1][0]  # expand left of the current interval
            intervals.pop()  # remove fully covered and smaller
        if intervals and 0 < (D[i%N]-D[intervals[-1][1]%N])%NANODEGREE_360 <= NANODEGREE_180:  # overlapped
            left = binary_search(intervals[-1][0], intervals[-1][1], partial(is_overllaped, N, D, i))  # Time: O(logN)
            intersect = binary_search(left, intervals[-1][1], partial(is_intersected, N, R, D, L, intervals[-1][2], i))  # Time: O(logN)
            if left <= intersect <= intervals[-1][1]:  # shorten the previous interval
                intervals[-1][1] = left = intersect
            else:  # shorten the current interval
                left = intervals[-1][1]
        intervals.append([left, i, i])
    max_pair = [-1]*N
    for left, right, j in intervals:  # Time: O(N)
        for i in xrange(left, right):
            if max_pair[i%N] == -1 or f(R, D, L, i%N, j%N) > f(R, D, L, i%N, max_pair[i%N]):
                max_pair[i%N] = j%N
    pairs = defaultdict(int)
    for i, j in enumerate(max_pair):  # Time: O(N)
        if j != -1:
            pairs[hash(i, j)] = max(pairs[hash(i, j)], f(R, D, L, i, j)+L[i])
    value_pairs = [(v, k) for k, v in pairs.iteritems()]
    nth_element(value_pairs, K, compare=lambda a, b: a > b)  # Time: O(N) on average
    possible_pairs = defaultdict(int)
    for _, pairs in value_pairs[:K]:  # Time: O(N * K)
        for i in pairs:
            for j in xrange(N):
                if j != i:
                    possible_pairs[hash(i, j)] = max(possible_pairs[hash(i, j)], f(R, D, L, i, j)+L[i])
    result = possible_pairs.values()
    nth_element(result, K, compare=lambda a, b: a > b)  # Time: O(N * K) on average
    return " ".join(map(lambda x: "%.10f"%x, sorted(result[:K], reverse=True)))

NANODEGREE_180 = 180*10**9
NANODEGREE_360 = 360*10**9
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, musical_cords())
