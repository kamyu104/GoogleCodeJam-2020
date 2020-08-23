# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Virtual World Finals - Problem B. Adjacent and Consecutive
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff31/00000000003b53ce
#
# Time:  O(N^3)
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

def count_of_3_or_up(counter):  # Time: O(1)
    return len(counter)-int(1 in counter)-int(2 in counter)

def is_A_winning_state(Lt, Lc, Z_delta=0):  # Time: O(N)
    K = sum(k*v for k, v in Lc.iteritems())  # k is either 1 or 2
    Z = sum((k//2)*v for k, v in Lt.iteritems())
    Z = max(Z+Z_delta, 0)
    if K == 2:
        return Lc[2] == Z == 1
    return K%2 and 2*(Lc[2]+Z) > K

def is_A_winning(tiles, cells):  # Time: O(N)
    if stats_of_win_immediately(tiles, cells):  # can win in 1 moves
        return True
    Lt, Lc = compress_state(cells), compress_state(tiles)
    if count_of_3_or_up(Lt) < count_of_3_or_up(Lc):
        Lt, Lc = Lc, Lt
    if count_of_3_or_up(Lc):  # can win in 2 moves
        return True
    return is_A_winning_state(Lt, Lc)

def B_try_to_avoid_and_win(tiles, cells):  # Time: O(N)
    Lt, Lc = compress_state(tiles), compress_state(cells)
    if count_of_3_or_up(Lt) < count_of_3_or_up(Lc):
        Lc, Lt = Lt, Lc
    K = sum(k*v for k, v in Lc.iteritems())
    if K == 0:
        return True
    if count_of_3_or_up(Lc) > 1 or (count_of_3_or_up(Lc) == count_of_3_or_up(Lt) == 1):
        return False
    if count_of_3_or_up(Lc) == 1:
        max_key = max(Lc.iterkeys())
        if Lc[max_key] > 1 or Lt[1] == 0:
            return False
        del Lc[max_key]
        if max_key == 3:  # split 3 into (0, 2) or (1, 1), and put the pivot i into one of Lt_1, using (1, 1) is enough
            Lc[1] += 2
            return not is_A_winning_state(Lt, Lc)
        if max_key == 4:  # split 4 into (1, 2), and put the pivot i into one of Lt_1
            Lc[1] += 1
            Lc[2] += 1
            return not is_A_winning_state(Lt, Lc)
        if max_key == 5:  # split 5 into (2, 2), and put the pivot i into one of Lt_1
            Lc[2] += 2
            return not is_A_winning_state(Lt, Lc)
        return False
    if Lc[1]:
        Lc[1] -= 1
        return not is_A_winning_state(Lt, Lc, -1)  # reduce the number of 2 in Lt_prime as possible
    if sum((k%2)*v for k, v in Lt.iteritems()) == 0:  # Lc and Lt_prime are all 2s
        return False
    Lc[2] -= 1
    Lc[1] += 1
    return not is_A_winning_state(Lt, Lc)

def find_break_cell(stats):  # Time: O(N)
    max_l, to_del = 0, None
    for l, stat in stats.iteritems():
        for k, v in stat.iteritems():
            if len(v) == 1:
                if l > max_l:
                    max_l, to_del = l, k
    if max_l:
        j = stats[max_l][to_del][0]
        del stats[max_l][to_del]
        if not stats[max_l]:
            del stats[max_l]
        return to_del, j
    return to_del, -2

def is_B_winning(tiles, cells):  # Time: O(N^2)
    stats = stats_of_win_immediately(tiles, cells)
    if stats:  # try to avoid A win immediately
        if len(stats) == 1 and 1 in stats and len(stats[1]) == 1:
            i, s = next(stats[1].iteritems())
            i = next(iter(i))
            candidates = [c for c, x in enumerate(cells) if x == -2 and c not in s]
            for j in candidates:  # try to put i to the places other than s
                tiles[i], cells[j] = j, i
                can_B_win = not is_A_winning(tiles, cells)
                tiles[i], cells[j] = -2, -2
                if can_B_win:
                    return can_B_win
            if len(s) == 1:
                candidates = [j for j, x in enumerate(tiles) if x == -2 and j != i]
                j = next(iter(s))
                for i in candidates:  # try to put any other than i to the places s (only j)
                    tiles[i], cells[j] = j, i
                    can_B_win = not is_A_winning(tiles, cells)
                    tiles[i], cells[j] = -2, -2
                    if can_B_win:
                        return can_B_win
            return False
        candidates, j = find_break_cell(stats)
        if j == -2:
            return False
        if not stats:
            candidates = [t for t, x in enumerate(tiles) if x == -2 and t not in candidates]
            for i in candidates:  # try to put any other than i to the places s (only j)
                tiles[i], cells[j] = j, i
                can_B_win = not is_A_winning(tiles, cells)
                tiles[i], cells[j] = -2, -2
                if can_B_win:
                    return can_B_win
            return False
        if len(stats) == 1 and 1 in stats and len(stats[1]) == 1:
            i, s = next(stats[1].iteritems())
            i = next(iter(i))
            tiles[i], cells[j] = j, i
            A_already_won = (j-1 >= 0 and abs(i-cells[j-1]) == 1) or (j+1 < len(cells) and abs(i-cells[j+1]) == 1)
            can_B_win = not A_already_won and not is_A_winning(tiles, cells)
            tiles[i], cells[j] = -2, -2
            return can_B_win
        return False
    return B_try_to_avoid_and_win(tiles, cells)

def adjacent_and_consecutive():
    N = input()
    result, tiles, cells, prev = [0, 0], [-2]*N, [-2]*N, True
    A_already_won = False  # A can win in 0 moves
    for i in xrange(N):
        M, C = map(int, raw_input().strip().split())
        M, C = M-1, C-1
        tiles[M], cells[C] = C, M
        if not A_already_won:
            A_already_won = (C-1 >= 0 and abs(M-cells[C-1]) == 1) or (C+1 < len(cells) and abs(M-cells[C+1]) == 1)
        if i%2 == 0:
            curr = is_B_winning(tiles, cells) if not A_already_won else False
            if prev and curr:
                result[i%2] += 1
        else:
            curr = A_already_won or is_A_winning(tiles, cells)
            if prev and curr:
                result[i%2] += 1
        prev = curr
    return "%s %s" % tuple(result)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, adjacent_and_consecutive())
