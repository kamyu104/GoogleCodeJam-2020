# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 2 - Problem A. Incremental House of Pancakes
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ffb9/00000000003384ea
#
# Time:  O(log(L + R))
# Space: O(1)
#

def f(a, d, n):
    return (2*a + (n-1)*d)*n//2

def binary_search_right(left, right, check):
    while left <= right:
        mid = left + (right-left)//2
        if not check(mid):
            right = mid-1
        else:
            left = mid+1
    return right

def incremental_house_of_pancakes():
    L, R = map(int, raw_input().strip().split())
    is_swapped = False
    if L < R:
        L, R = R, L
        is_swapped = True
    n = binary_search_right(1, L-R, lambda x: f(1, 1, x) <= L-R)
    L -= f(1, 1, n)
    if L == R:
        is_swapped = False
    l = binary_search_right(1, L, lambda x: f(n+1, 2, x) <= L)
    r = binary_search_right(1, R, lambda x: f(n+2, 2, x) <= R)
    L -= f(n+1, 2, l)
    R -= f(n+2, 2, r)
    n = max(n+1 + (l-1)*2, n+2 + (r-1)*2)
    if is_swapped:
        L, R = R, L
    return "{} {} {}".format(n, L, R)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, incremental_house_of_pancakes())
