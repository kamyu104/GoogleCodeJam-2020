# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1B - Problem B. Blindfolded Bullseye
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b63
#
# Time:  O(N + 4 * ceil(log(2*10^9 + 1)/log2)), 1-(1-pi/16)^N >= 99.9%, N >= 32
#        = O(32 + 4 * 31) = O(156) for 99.9% cases
# Space: O(1)
#
# Usage: python interactive_runner.py python local_testing_tool.py 2 -- python blindfolded_bullseye.py
#

from sys import stdout
from random import randint

def binary_search(left, right, check):
    while left <= right:
        mid = left + (right-left)//2
        if check(mid):
            right = mid-1
        else:
            left = mid+1
    return left, right

def query(x, y):
    print x, y
    stdout.flush()
    r = raw_input().strip()
    if r == "WRONG":  # error
        exit()
    if r == "CENTER":
        raise "CENTER"
    return r == "HIT"

def blindfolded_bullseye():
    while True:
        x0 = randint(-B, B)
        y0 = randint(-B, B)
        if query(x0, y0):
            break

    left_x, _ = binary_search(-B, x0, lambda x: query(x, y0))
    _, right_x = binary_search(x0, B, lambda x: not query(x, y0))
    left_y, _ = binary_search(-B, y0, lambda y: query(x0, y))
    _, right_y = binary_search(y0, B, lambda y: not query(x0, y))
    query((left_x+right_x)//2, (left_y+right_y)//2)
    exit()

B = 10**9
T, A, B = map(int, raw_input().strip().split())
for case in xrange(T):
    try:
        blindfolded_bullseye()
    except:
        pass
