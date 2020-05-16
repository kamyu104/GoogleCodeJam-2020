# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 2 - Problem A. Incremental House of Pancakes
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ffb9/00000000003384ea
#
# Time:  O(log(L + R))
# Space: O(1)
#

from math import sqrt

def s(a, d, n):
    return (2*a + (n-1)*d)*n//2

def f(a, d, x):
    r = int((-(2*a-d)+sqrt((2*a-d)**2+8*d*x))/(2*d))
    if s(a, d, r) > x:  # adjust float accuracy
        r -= 1
    return r

def incremental_house_of_pancakes():
    L, R = map(int, raw_input().strip().split())
    is_swapped = False
    if L < R:
        L, R = R, L
        is_swapped = True
    n = f(1, 1, L-R)
    L -= s(1, 1, n)
    if L == R:
        is_swapped = False
    l = f(n+1, 2, L)
    r = f(n+2, 2, R)
    L -= s(n+1, 2, l)
    R -= s(n+2, 2, r)
    if is_swapped:
        L, R = R, L
    return "{} {} {}".format(n+l+r, L, R)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, incremental_house_of_pancakes())
