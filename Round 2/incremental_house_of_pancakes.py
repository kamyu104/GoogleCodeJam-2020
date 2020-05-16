# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 2 - Problem A. Incremental House of Pancakes
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ffb9/00000000003384ea
#
# Time:  O(log(L + R))
# Space: O(1)
#

def s(a, d, n):
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
    n = binary_search_right(1, L-R, lambda x: s(1, 1, x) <= L-R)
    L -= s(1, 1, n)
    if L == R:
        is_swapped = False
    l = binary_search_right(1, L, lambda x: s(n+1, 2, x) <= L)
    r = binary_search_right(1, R, lambda x: s(n+2, 2, x) <= R)
    L -= s(n+1, 2, l)
    R -= s(n+2, 2, r)
    if is_swapped:
        L, R = R, L
    return "{} {} {}".format(n+l+r, L, R)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, incremental_house_of_pancakes())
