# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Virtual World Finals - Problem C. Hexacoin
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff31/00000000003b4bc5
#
# Time:  O(B^(D + 1) * D + N^2 * D), PyPy2 TLE in test set 3
# Space: O(B^(D + 1))
#

from fractions import gcd
from collections import defaultdict

def to_hex(x, D):  # Time: O(D)
    return ("{:0" + str(D) +  "X}").format(x)

def find_structures(D, U):  # Time: O(B^(D + 1) * D)
    lookup = defaultdict(int)
    B_POW_D = B**D
    for x in xrange(min(U, B_POW_D)):  # O(B^D) times
        y = U-x
        x_hex, y_hex = to_hex(x, D), to_hex(y, D)[:D]
        norm, hash_value = {'*':0}, 0
        for d, h in enumerate(x_hex+y_hex):  # O(B * D) times
            h = int(h, B)
            if d >= D:
                if y >= B_POW_D:  # D "*" in the suffix
                    lookup[hash_value] += 1
                    break
                for smaller_h in xrange(h):  # at most D-1 "*" in the suffix
                    delta = norm[smaller_h] if smaller_h in norm else len(norm)
                    lookup[hash_value*(B+1) + delta] += 1
            if h not in norm:
                norm[h] = len(norm)
            hash_value = hash_value*(B+1) + norm[h]
    return lookup

def match_structures_and_count(N, L, lookup):  # Time: O(N^2 * D)
    count = 0
    for i in xrange(N):  # O(N) times
        for j in xrange(i+1, N):  # O(N) times
            norm, hash_value = {'*':0}, 0
            for d, h in enumerate(L[i]+L[j]):  # O(D) times
                h = int(h, B)
                if h not in norm:
                    norm[h] = len(norm)
                hash_value = hash_value*(B+1) + norm[h]
                if d >= len(L[i])-1 and hash_value in lookup:
                    count += lookup[hash_value] * FACTORIAL[(B+1)-len(norm)]
    return count

def f(N, D, L, U):
    lookup = find_structures(D, U)
    return match_structures_and_count(N, L, lookup)

def hexacoin():
    N, D = map(int, raw_input().strip().split())
    S, E = map(lambda x: int(x, B), raw_input().strip().split())
    L = raw_input().strip().split()
    count = (f(N, D, L, E+1)-f(N, D, L, S)) + (f(N, D, L, B**D+E+1)-f(N, D, L, B**D+S))
    total = FACTORIAL[16]*N*(N-1)//2
    g = gcd(count, total)
    return "{} {}".format(count//g, total//g)

B = 16
FACTORIAL = [1]*(B+1)
for i in xrange(1, len(FACTORIAL)):
    FACTORIAL[i] = i*FACTORIAL[i-1]
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, hexacoin())
