# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Virtual World Finals - Problem B. Adjacent and Consecutive
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff31/00000000003b53ce
#
# Time:  O(N^2)
# Space: O(N)
#

from collections import defaultdict, Counter

def stats_of_win_immediately(tiles, cells):  # Time: O(N)
    lookup = defaultdict(set)
    stats = defaultdict(lambda:defaultdict(list))
    for c in xrange(len(cells)):
        if cells[c] != -2:
            continue
        for nc in ((c-1), (c+1)):
            if not (0 <= nc < len(cells) and cells[nc] != -2):
                continue
            m = cells[nc]
            for nm in ((m-1), (m+1)):
                if 0 <= nm < len(tiles) and tiles[nm] == -2:
                    lookup[c].add(nm)
    for c, s in lookup.iteritems():
        stats[len(s)][frozenset(s)].append(c)
    return stats

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

def is_A_winning(tiles, cells, stats, Lt, Lt_Z, Lc, Lc_Z, K):  # Time: O(1)
    if stats:  # can win in 1 moves
        return True
    if count_of_3_or_up(Lt) and count_of_3_or_up(Lc):  # can win in 2 moves
        return True
    return is_A_winning_state(Lt_Z, Lc_Z, K)

def find_cell_to_fill(stats):  # Time: O(N)
    max_l, ts, cs = 0, frozenset(), set()
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
    return ts, cs

def B_try_to_avoid_and_win(tiles, cells, Lt, Lt_Z, Lc, Lc_Z, K):  # Time: O(1)
    if count_of_3_or_up(Lt) < count_of_3_or_up(Lc):
        Lt, Lc = Lc, Lt
        Lt_Z, Lc_Z = Lc_Z, Lt_Z
    if K == 0:
        return True
    K -= 1
    if count_of_3_or_up(Lc) > 1:
        return False
    if count_of_3_or_up(Lc) == 1:
        max_key = max(k for k, v in Lc.iteritems() if v != 0)
        if Lc[max_key] > 1 or 1 not in Lt:
            return False
        if max_key == 3:  # split 3 into (0, 2) or (1, 1), and put the pivot i into one of Lt_1, using (1, 1) is enough
            return not is_A_winning_state(Lt_Z, Lc_Z-max_key//2+0, K)
        if max_key == 4:  # split 4 into (1, 2), and put the pivot i into one of Lt_1
            return not is_A_winning_state(Lt_Z, Lc_Z-max_key//2+1, K)
        if max_key == 5:  # split 5 into (2, 2), and put the pivot i into one of Lt_1
            return not is_A_winning_state(Lt_Z, Lc_Z-max_key//2+2, K)
        return False
    if 1 in Lc:
        Lt_Z = max(Lt_Z-1, 0)  # reduce the number of 2 in Lt_prime as possible
        return not is_A_winning_state(Lt_Z, Lc_Z, K)
    if sum((k%2)*v for k, v in Lt.iteritems()) == 0:  # Lc and Lt_prime are all 2s
        return False
    return not is_A_winning_state(Lt_Z, Lc_Z-1, K)

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

def is_B_winning(tiles, cells, stats, Lt, Lt_lookup, Lt_Z, Lc, Lc_lookup, Lc_Z, K):  # Time: O(N)
    if stats:  # try to avoid A win immediately
        if len(stats) == 1 and 1 in stats and len(stats[1]) == 1:
            ts, cs = next(stats[1].iteritems())
            i = next(iter(ts))
            candidates = [c for c, x in enumerate(cells) if x == -2 and c not in cs]
            for j in candidates:  # try to put i to the places other than s
                can_B_win = is_B_winning_state(tiles, cells, Lt, Lt_lookup, Lt_Z, Lc, Lc_lookup, Lc_Z, K-1, i, j)
                if can_B_win:
                    return can_B_win
            if len(cs) == 1:
                candidates = [t for t, x in enumerate(tiles) if x == -2 and t not in ts]
                j = next(iter(cs))
                for i in candidates:  # try to put any other than i to the places s (only j)
                    can_B_win = is_B_winning_state(tiles, cells, Lt, Lt_lookup, Lt_Z, Lc, Lc_lookup, Lc_Z, K-1, i, j)
                    if can_B_win:
                        return can_B_win
            return False
        ts, cs = find_cell_to_fill(stats)
        if not cs:
            return False
        assert(len(cs) == 1)
        if not stats:
            candidates = [t for t, x in enumerate(tiles) if x == -2 and t not in ts]
            j = next(iter(cs))
            for i in candidates:  # try to put any other than i to the places s (only j)
                can_B_win = is_B_winning_state(tiles, cells, Lt, Lt_lookup, Lt_Z, Lc, Lc_lookup, Lc_Z, K-1, i, j)
                if can_B_win:
                    return can_B_win
            assert(len(ts) != 1)  # this case is excluded by the previous checks
            return False
        if len(stats) == 1 and 1 in stats and len(stats[1]) == 1:
            new_ts, new_cs = next(stats[1].iteritems())
            i, j = next(iter(new_ts)), next(iter(cs))
            can_B_win = (i not in ts) and is_B_winning_state(tiles, cells, Lt, Lt_lookup, Lt_Z, Lc, Lc_lookup, Lc_Z, K-1, i, j)
            if can_B_win:
                return can_B_win
            if len(ts) == 1:
                i, j = next(iter(ts)), next(iter(new_cs))
                can_B_win = (len(new_cs) == 1) and is_B_winning_state(tiles, cells, Lt, Lt_lookup, Lt_Z, Lc, Lc_lookup, Lc_Z, K-1, i, j)
                if can_B_win:
                    return can_B_win
            return False
        return False
    return B_try_to_avoid_and_win(tiles, cells, Lt, Lt_Z, Lc, Lc_Z, K)

def adjacent_and_consecutive():
    N = input()
    result, tiles, cells, prev = [0, 0], [-2]*N, [-2]*N, True
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
        stats = stats_of_win_immediately(tiles, cells)
        _, Lt_lookup = compress_state(tiles)
        _, Lc_lookup = compress_state(cells)
        K -= 1
        if not A_already_won:
            A_already_won = (C-1 >= 0 and abs(M-cells[C-1]) == 1) or (C+1 < len(cells) and abs(M-cells[C+1]) == 1)
        if i%2 == 0:
            curr = is_B_winning(tiles, cells, stats, Lt, Lt_lookup, Lt_Z, Lc, Lc_lookup, Lc_Z, K) if not A_already_won else False
            if prev and curr:
                result[i%2] += 1
        else:
            curr = A_already_won or is_A_winning(tiles, cells, stats, Lt, Lt_Z, Lc, Lc_Z, K)
            if prev and curr:
                result[i%2] += 1
        prev = curr
    return "%s %s" % tuple(result)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, adjacent_and_consecutive())
