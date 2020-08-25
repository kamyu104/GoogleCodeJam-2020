# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Virtual World Finals - Problem B. Adjacent and Consecutive
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff31/00000000003b53ce
#
# Time:  O(N^2)
# Space: O(N)
#

from collections import defaultdict, Counter

def update_immediately_win(tiles, cells, M, C, active_tiles, active_cells):
    if M in active_tiles:
        for c in active_tiles[M]:
            active_cells[c].remove(M)
            if not active_cells[c]:
                del active_cells[c]
        del active_tiles[M]
    if C in active_cells:
        for m in active_cells[C]:
            active_tiles[m].remove(C)
            if not active_tiles[m]:
                del active_tiles[m]
        del active_cells[C]
    for c in xrange(max(C-1, 0), min(C+1, len(cells)-1)+1):
        if cells[c] != -2:
            continue
        if M-1 >= 0 and tiles[M-1] == -2:
            active_tiles[M-1].add(c)
            active_cells[c].add(M-1)
        if M+1 < len(tiles) and tiles[M+1] == -2:
            active_tiles[M+1].add(c)
            active_cells[c].add(M+1)

def compress_state(arr):  # Time: O(N)
    c, counter, counts, rank = 0, Counter(), [], {}
    for i, x in enumerate(arr):
        if x != -2:
            if c:
                counter[c] += 1
                counts.append(c)
            c = 0
            continue
        c += 1
        rank[i] = c
    if c:
        counter[c] += 1
        counts.append(c)
    curr, switch = -1, True
    lookup = {}
    for i, x in enumerate(arr):
        if x != -2:
            if not switch:
                switch = True
            continue
        if switch:
            switch = False
            curr += 1
        lookup[i] = (rank[i], counts[curr])
    return counter, lookup

def count_of_3_or_up(counter):  # Time: O(1)
    return len(counter)-int(1 in counter)-int(2 in counter)

def is_A_winning_state(Lt_Z, Lc_Z, K):  # Time: O(1)
    if K == 2:
        return Lt_Z == Lc_Z == 1
    return K%2 and 2*(Lt_Z+Lc_Z) > K

def is_A_winning(tiles, cells, active_tiles, active_cells, Lt, Lt_Z, Lc, Lc_Z, K):  # Time: O(1)
    if active_tiles:  # can win in 1 moves
        return True
    if count_of_3_or_up(Lt) and count_of_3_or_up(Lc):  # can win in 2 moves
        return True
    return is_A_winning_state(Lt_Z, Lc_Z, K)

def find_cell_to_fill(active_cells):  # Time: O(1)
    max_l, ts, cs = 0, frozenset(), set()
    lookup = defaultdict(set)
    stats = defaultdict(lambda:defaultdict(list))
    count = 8  # at most 8 if possible, ex. tile [9] with cells [3,5,6,8], tiles [2,4,5,7] with cell [2]
    for c, ms in active_cells.iteritems():
        for m in ms:
            lookup[c].add(m)
            count -= 1
            if not count:
                return stats, ts, cs
    for c, s in lookup.iteritems():
        stats[len(s)][frozenset(s)].append(c)
    for l, stat in stats.iteritems():
        for k, v in stat.iteritems():
            if len(v) == 1:
                if l > max_l:
                    max_l, ts = l, k
    if max_l:
        cs = stats[max_l][ts]
        del stats[max_l][ts]
        if not stats[max_l]:
            del stats[max_l]
    return stats, ts, cs

def B_try_to_avoid_2_moves_win(Lt, Lt_Z, Lc, Lc_Z, K):  # Time: O(1)
    if count_of_3_or_up(Lt) < count_of_3_or_up(Lc):
        Lt, Lc = Lc, Lt
        Lt_Z, Lc_Z = Lc_Z, Lt_Z
    if K == 0:
        return True
    if count_of_3_or_up(Lc) > 1:
        return False
    if count_of_3_or_up(Lc) == 1:
        max_key = max(k for k, v in Lc.iteritems() if v != 0)
        if Lc[max_key] > 1 or 1 not in Lt:
            return False
        if max_key == 3:  # split 3 into (0, 2) or (1, 1), and put the pivot i into one of Lt_1, using (1, 1) is enough
            return not is_A_winning_state(Lt_Z, Lc_Z-max_key//2+0, K-1)
        if max_key == 4:  # split 4 into (1, 2), and put the pivot i into one of Lt_1
            return not is_A_winning_state(Lt_Z, Lc_Z-max_key//2+1, K-1)
        if max_key == 5:  # split 5 into (2, 2), and put the pivot i into one of Lt_1
            return not is_A_winning_state(Lt_Z, Lc_Z-max_key//2+2, K-1)
        return False
    if 1 in Lc:
        Lt_Z = max(Lt_Z-1, 0)  # reduce the number of 2 in Lt_prime as possible
        return not is_A_winning_state(Lt_Z, Lc_Z, K-1)
    if K == 2*Lt_Z:  # Lc and Lt_prime are all 2s
        return False
    return not is_A_winning_state(Lt_Z, Lc_Z-1, K-1)

def update_L(L, count, v):  # Time: O(1)
    L[count[1]] -= v
    if not L[count[1]]:
        del L[count[1]]
    if count[0]-1:
        L[count[0]-1] += v
        if not L[count[0]-1]:
            del L[count[0]-1]
    if count[1]-count[0]:
        L[count[1]-count[0]] += v
        if not L[count[1]-count[0]]:
            del L[count[1]-count[0]]
    return (1 if v > 0 else -1) * (-(count[1]//2)+(count[0]-1)//2+(count[1]-count[0])//2)

def is_B_winning_state(tiles, cells, Lt, Lt_lookup, Lt_Z, Lc, Lc_lookup, Lc_Z, K, i, j):  # Time: O(1)
    if (((j-1 >= 0 and cells[j-1] == -2) or (j+1 < len(cells) and cells[j+1] == -2)) and
        ((i-1 >= 0 and tiles[i-1] == -2) or (i+1 < len(tiles) and tiles[i+1] == -2))):
        return False  # A would win immediately
    tiles[i], cells[j] = j, i
    Lt_Z_delta = update_L(Lt, Lt_lookup[i], 1)
    Lc_Z_delta = update_L(Lc, Lc_lookup[j], 1)
    can_B_win = not ((count_of_3_or_up(Lt) and count_of_3_or_up(Lc)) or
                     (K == 2 and (Lt_Z+Lt_Z_delta) == (Lc_Z+Lc_Z_delta) == 1) or
                     (K%2 and 2*((Lt_Z+Lt_Z_delta) + (Lc_Z+Lc_Z_delta)) > K))
    update_L(Lc, Lc_lookup[j], -1)
    update_L(Lt, Lt_lookup[i], -1)
    tiles[i], cells[j] = -2, -2
    return can_B_win

def is_B_winning(tiles, cells, active_tiles, active_cells, Lt, Lt_lookup, Lt_Z, Lc, Lc_lookup, Lc_Z, K):  # Time: O(N)
    if active_tiles:  # try to avoid A win immediately
        if len(active_tiles) == 1:  # one active tile to one or up active cells
            i, cs = next(active_tiles.iteritems())
            candidates = [c for c, x in enumerate(cells) if x == -2 and c not in cs]
            for j in candidates:  # try to put i to the places other than s
                can_B_win = is_B_winning_state(tiles, cells, Lt, Lt_lookup, Lt_Z, Lc, Lc_lookup, Lc_Z, K-1, i, j)
                if can_B_win:
                    return can_B_win
            if len(cs) == 1:
                candidates = [t for t, x in enumerate(tiles) if x == -2 and t != i]
                j = next(iter(cs))
                for i in candidates:  # try to put any other than i to the places s (only j)
                    can_B_win = is_B_winning_state(tiles, cells, Lt, Lt_lookup, Lt_Z, Lc, Lc_lookup, Lc_Z, K-1, i, j)
                    if can_B_win:
                        return can_B_win
            return False
        if len(active_cells) == 1:  # two or up active tiles to one active cells
            j, ts = next(active_cells.iteritems())
            assert(len(ts) != 1)  # len(ts) == 1 is covered by the previous checks
            candidates = [t for t, x in enumerate(tiles) if x == -2 and t not in ts]
            for i in candidates:  # try to put any other than i to the places s (only j)
                can_B_win = is_B_winning_state(tiles, cells, Lt, Lt_lookup, Lt_Z, Lc, Lc_lookup, Lc_Z, K-1, i, j)
                if can_B_win:
                    return can_B_win
            return False
        stats, ts, cs = find_cell_to_fill(active_cells)
        if cs and len(stats) == 1 and 1 in stats and len(stats[1]) == 1:  # one tile with one or up cells, the other is one or up tiles with one cell
            new_ts, new_cs = next(stats[1].iteritems())
            i, j = next(iter(new_ts)), next(iter(cs))
            can_B_win = (i not in ts) and is_B_winning_state(tiles, cells, Lt, Lt_lookup, Lt_Z, Lc, Lc_lookup, Lc_Z, K-1, i, j)
            if can_B_win:
                return can_B_win
            if len(ts) == 1 and len(new_cs) == 1:
                i, j = next(iter(ts)), next(iter(new_cs))
                can_B_win = is_B_winning_state(tiles, cells, Lt, Lt_lookup, Lt_Z, Lc, Lc_lookup, Lc_Z, K-1, i, j)
                if can_B_win:
                    return can_B_win
            return False
        return False
    return B_try_to_avoid_2_moves_win(Lt, Lt_Z, Lc, Lc_Z, K)

def adjacent_and_consecutive():
    N = input()
    result, tiles, cells, prev = [0, 0], [-2]*N, [-2]*N, True
    active_tiles, active_cells = defaultdict(set), defaultdict(set)
    A_already_won = False  # A can win in 0 moves
    Lt, Lt_lookup = compress_state(tiles)
    Lc, Lc_lookup = compress_state(cells)
    K = N
    Lt_Z = sum((k//2)*v for k, v in Lt.iteritems())
    Lc_Z = sum((k//2)*v for k, v in Lc.iteritems())
    for i in xrange(N):
        M, C = map(int, raw_input().strip().split())
        M, C = M-1, C-1
        Lt_Z += update_L(Lt, Lt_lookup[M], 1)
        Lc_Z += update_L(Lc, Lc_lookup[C], 1)
        tiles[M], cells[C] = C, M
        update_immediately_win(tiles, cells, M, C, active_tiles, active_cells)
        _, Lt_lookup = compress_state(tiles)
        _, Lc_lookup = compress_state(cells)
        K -= 1
        if not A_already_won:
            A_already_won = (C-1 >= 0 and abs(M-cells[C-1]) == 1) or (C+1 < len(cells) and abs(M-cells[C+1]) == 1)
        if i%2 == 0:
            curr = is_B_winning(tiles, cells, active_tiles, active_cells, Lt, Lt_lookup, Lt_Z, Lc, Lc_lookup, Lc_Z, K) if not A_already_won else False
            if prev and curr:
                result[i%2] += 1
        else:
            curr = A_already_won or is_A_winning(tiles, cells, active_tiles, active_cells, Lt, Lt_Z, Lc, Lc_Z, K)
            if prev and curr:
                result[i%2] += 1
        prev = curr
    return "%s %s" % tuple(result)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, adjacent_and_consecutive())
