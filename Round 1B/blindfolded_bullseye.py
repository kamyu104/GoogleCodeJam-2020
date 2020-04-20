# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1B - Problem B. Blindfolded Bullseye
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b63
#
# Time:  O(N + 4 * ceil(log(2*10^9 + 1)/log2)), 1-(1-pi/16)^N >= 99.9%, N >= 32
#        = O(32 + 4 * 31) = O(156) for 99.9% cases of test set 3
# Space: O(1)
#
# Usage: python interactive_runner.py python local_testing_tool.py 2 -- python blindfolded_bullseye.py
#

from sys import stdout
from random import randint

def binary_search(left, right, check, is_left):
    while left <= right:
        mid = left + (right-left)//2
        if check(mid) == is_left:
            right = mid-1
        else:
            left = mid+1
    return left if is_left else right

def query(x, y):
    print x, y
    stdout.flush()
    r = raw_input().strip()
    if r == "WRONG":  # error
        exit()
    if r == "CENTER":
        raise
    return r == "HIT"

def blindfolded_bullseye():
    while True:
        x0, y0 = randint(-M, M), randint(-M, M)
        if query(x0, y0):  # hit rate = pi*(M/2)^2 / (2*M)^2 = pi/16 for test set 3
            break
    left_x = binary_search(-M, x0, lambda x: query(x, y0), True)
    right_x = binary_search(x0, M, lambda x: query(x, y0), False)
    left_y = binary_search(-M, y0, lambda y: query(x0, y), True)
    right_y = binary_search(y0, M, lambda y: query(x0, y), False)
    query((left_x+right_x)//2, (left_y+right_y)//2)
    exit()  # should not reach here

M = 10**9
T, A, B = map(int, raw_input().strip().split())
for case in xrange(T):
    try:
        blindfolded_bullseye()
    except:
        pass
