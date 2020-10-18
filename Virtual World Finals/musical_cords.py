# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Virtual World Finals - Problem D. Musical Cords
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff31/00000000003b532b
#
# Time:  O(NlogN + N * K) on average, pass in PyPy2 but Python2
# Space: O(N * K)
#

from math import sin, pi
from functools import partial
from random import randint

def nth_element(nums, n, compare=lambda a, b: a < b):
    def tri_partition(nums, left, right, target, compare):
        mid = left
        while mid <= right:
            if nums[mid] == target:
                mid += 1
            elif compare(nums[mid], target):
                nums[left], nums[mid] = nums[mid], nums[left]
                left += 1
                mid += 1
            else:
                nums[mid], nums[right] = nums[right], nums[mid]
                right -= 1
        return left, right

    left, right = 0, len(nums)-1
    while left <= right:
        pivot_idx = randint(left, right)
        pivot_left, pivot_right = tri_partition(nums, left, right, nums[pivot_idx], compare)
        if pivot_left <= n <= pivot_right:
            return
        elif pivot_left > n:
            right = pivot_left-1
        else:  # pivot_right < n.
            left = pivot_right+1

def binary_search(left, right, check_fn):
    while left <= right:
        mid = left + (right-left)//2
        if check_fn(mid):
            right = mid-1
        else:
            left = mid+1
    return left

def unordered_pair(i, j):
    return (i, j) if i < j else (j, i)

def f(R, D, L, i, j):
    return 2*R*sin(((D[j]-D[i])%NANODEGREE_360)*pi/NANODEGREE_360)+L[j]

def is_overllaped(N, D, i, x):
    return 0 < (D[i%N]-D[x%N])%NANODEGREE_360 <= NANODEGREE_180

def is_above(N, R, D, L, curr, prev, x):
    return f(R, D, L, x%N, curr%N) >= f(R, D, L, x%N, prev%N)

def check(N, R, D, L, curr, prev, x):
    return is_overllaped(N, D, curr, x) and is_above(N, R, D, L, curr, prev, x)

def musical_cords():
    N, R, K = map(int, raw_input().strip().split())
    D, L = [0]*N, [0]*N
    for i in xrange(N):
        D[i], L[i] = map(int, raw_input().strip().split())

    intervals = []
    for i in xrange(2*N-1):  # Total Time: O(NlogN)
        left = i
        while intervals and is_overllaped(N, D, i, intervals[-1][0]) and \
              is_above(N, R, D, L, i, intervals[-1][2], intervals[-1][0]):
            left = intervals.pop()[0]  # remove fully covered and smaller intervals, and expand the left point of the current one
        if intervals and is_overllaped(N, D, i, intervals[-1][1]):  # overlapped
            intersect = binary_search(intervals[-1][0], intervals[-1][1], partial(check, N, R, D, L, i, intervals[-1][2]))  # Time: O(logN)
            if intersect <= intervals[-1][1]:  # adjust both intervals
                intervals[-1][1] = left = intersect
            else:  # adjust the current interval by including the right point of the previous one
                left = intervals[-1][1]
        intervals.append([left, i, i])

    max_pair = [-1]*N
    for left, right, j in intervals:  # Time: O(N)
        for i in xrange(left, right):
            if max_pair[i%N] == -1 or f(R, D, L, i%N, j%N) > f(R, D, L, i%N, max_pair[i%N]):
                max_pair[i%N] = j%N
    pairs = {unordered_pair(i, j):f(R, D, L, i, j)+L[i] for i, j in enumerate(max_pair) if j != -1}  # Time: O(N)
    value_pairs = [(v, pair) for pair, v in pairs.iteritems()]
    nth_element(value_pairs, K-1, compare=lambda a, b: a > b)  # Time: O(N) on average
    possible_pairs = {unordered_pair(i, j):f(R, D, L, i, j)+L[i] for _, pair in value_pairs[:K] for i in pair for j in xrange(N) if j != i}  # Time: O(N * K)
    result = possible_pairs.values()
    nth_element(result, K-1, compare=lambda a, b: a > b)  # Time: O(N * K) on average
    return " ".join(map(lambda x: "%.10f"%x, sorted(result[:K], reverse=True)))  # Time: O(KlogK)

NANODEGREE_180 = 180*10**9
NANODEGREE_360 = 360*10**9
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, musical_cords())
