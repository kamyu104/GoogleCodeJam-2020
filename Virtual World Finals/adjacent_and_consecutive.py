# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Virtual World Finals - Problem B. Adjacent and Consecutive
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff31/00000000003b53ce#problem
#
# Time:  O(N^4)
# Space: O(N)
#

from collections import defaultdict, Counter

def compress(arr):  # O(N)
    c, counter = 0, Counter()
    for x in arr:
        if x != -2:
            if c:
                counter[c] += 1
            c = 0
            continue
        c += 1
    if c:
        counter[c] += 1
    return counter

def count_3_or_up(counter):
    return len(counter)-int(1 in counter)-int(2 in counter)

def is_A_winning_state(Lt, Lc, Z_delta=0):
    K = sum(k*v for k, v in Lc.iteritems())  # k is either 1 or 2
    if K == 2:
        return Lc[2] == Lt[2] == 1
    Z = sum((k//2)*v for k, v in Lt.iteritems())
    Z = max(Z+Z_delta, 0)
    return K%2 == 1 and 2*(Lc[2]+Z) > K

def is_A_winning(tiles, cells):
    for i in xrange(len(tiles)):
        if tiles[i] != -2:
            continue
        for j in xrange(len(cells)):
            if cells[j] != -2:
                continue
            if j-1 >= 0 and abs(i-cells[j-1]) == 1:
                return True
            if j+1 < len(cells) and abs(i-cells[j+1]) == 1:
                return True
    Lt, Lc = compress(cells), compress(tiles)
    if count_3_or_up(Lt) < count_3_or_up(Lc):
        Lt, Lc = Lc, Lt
    if count_3_or_up(Lc):
        return True
    return is_A_winning_state(Lt, Lc)

def is_B_winning(tiles, cells):
    result = True
    for i in xrange(len(tiles)):
        if tiles[i] != -2:
            continue
        for j in xrange(len(cells)):
            if cells[j] != -2:
                continue
            tiles[i], cells[j] = j, i
            is_A_won = (j-1 >= 0 and abs(i-cells[j-1]) == 1) or (j+1 < len(cells) and abs(i-cells[j+1]) == 1)
            result = not is_A_won and not is_A_winning(tiles, cells)
            tiles[i], cells[j] = -2, -2
            if result:
                return True
    return result

def adjacent_and_consecutive():
    N = input()
    result, tiles, cells, prev = [0, 0], [-2]*N, [-2]*N, True
    needs, needed_count = defaultdict(set), defaultdict(int)
    is_A_won = False
    for i in xrange(N):
        M, C = map(int, raw_input().strip().split())
        M, C = M-1, C-1
        tiles[M], cells[C] = C, M
        if not is_A_won:
            is_A_won = (C-1 >= 0 and abs(M-cells[C-1]) == 1) or (C+1 < len(cells) and abs(M-cells[C+1]) == 1)
        if i%2 == 0:
            curr = is_B_winning(tiles, cells) if not is_A_won else False
            if prev and curr:
                result[i%2] += 1
        else:
            curr = is_A_won or is_A_winning(tiles, cells)
            if prev and curr:
                result[i%2] += 1
        prev = curr
    return "%s %s" % tuple(result)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, adjacent_and_consecutive())
