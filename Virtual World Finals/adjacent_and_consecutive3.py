# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Virtual World Finals - Problem B. Adjacent and Consecutive
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff31/00000000003b53ce
#
# Time:  O(NlogN)
# Space: O(N)
#

from collections import defaultdict, Counter
from random import randint, seed

# Template:
# https://github.com/kamyu104/LeetCode-Solutions/blob/master/Python/design-skiplist.py
class SkipNode(object):
    def __init__(self, level=0, val=None):
        self.val = val
        self.nexts = [None]*level
        self.prevs = [None]*level

class SkipList(object):
    P_NUMERATOR, P_DENOMINATOR = 1, 2  # P = 1/4 in redis implementation
    MAX_LEVEL = 32  # enough for 2^32 elements

    def __init__(self, end=float("inf"), can_duplicated=False):
        seed(0)
        self.__head = SkipNode()
        self.__len = 0
        self.__can_duplicated = can_duplicated
        self.add(end)
    
    def lower_bound(self, target):
        return self.__lower_bound(target, self.__find_prev_nodes(target))

    def find(self, target):
        return self.__find(target, self.__find_prev_nodes(target))
        
    def add(self, val):
        if not self.__can_duplicated and self.find(val):
            return False
        node = SkipNode(self.__random_level(), val)
        if len(self.__head.nexts) < len(node.nexts): 
            self.__head.nexts.extend([None]*(len(node.nexts)-len(self.__head.nexts)))
        prevs = self.__find_prev_nodes(val)
        for i in xrange(len(node.nexts)):
            node.nexts[i] = prevs[i].nexts[i]
            if prevs[i].nexts[i]:
                prevs[i].nexts[i].prevs[i] = node
            prevs[i].nexts[i] = node
            node.prevs[i] = prevs[i]
        self.__len += 1
        return True

    def remove(self, val):
        prevs = self.__find_prev_nodes(val)
        curr = self.__find(val, prevs)
        if not curr:
            return False
        self.__len -= 1   
        for i in reversed(xrange(len(curr.nexts))):
            prevs[i].nexts[i] = curr.nexts[i]
            if curr.nexts[i]:
                curr.nexts[i].prevs[i] = prevs[i]
            if not self.__head.nexts[i]:
                self.__head.nexts.pop()
        return True
    
    def __lower_bound(self, val, prevs):
        if prevs:
            candidate = prevs[0].nexts[0]
            if candidate:
                return candidate
        return None

    def __find(self, val, prevs):
        candidate = self.__lower_bound(val, prevs)
        if candidate and candidate.val == val:
            return candidate
        return None

    def __find_prev_nodes(self, val):
        prevs = [None]*len(self.__head.nexts)
        curr = self.__head
        for i in reversed(xrange(len(self.__head.nexts))):
            while curr.nexts[i] and curr.nexts[i].val < val:
                curr = curr.nexts[i]
            prevs[i] = curr
        return prevs

    def __random_level(self):
        level = 1
        while randint(1, SkipList.P_DENOMINATOR) <= SkipList.P_NUMERATOR and \
              level < SkipList.MAX_LEVEL:
            level += 1
        return level

    def __len__(self):
        return self.__len-1  # excluding end node
    
    def __str__(self):
        result = []
        for i in reversed(xrange(len(self.__head.nexts))):
            result.append([])
            curr = self.__head.nexts[i]
            while curr:
                result[-1].append(str(curr.val))
                curr = curr.nexts[i]
        return "\n".join(map(lambda x: "->".join(x), result))

def query_interval(intervals, x):  # Time: O(logN)
    it = intervals.lower_bound(x)
    return (x-it.prevs[0].val, (it.val-1)-it.prevs[0].val, it.val)

def update_immediately_win(tiles, cells, M, C, active_tiles, active_cells):  # Time: O(1)
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
    c, counter = 0, Counter()
    for i, x in enumerate(arr):
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
            if count < 0:
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

def B_try_to_avoid_1_or_2_moves_win(Lt, Lt_intervals, Lt_Z, Lc, Lc_intervals, Lc_Z, K, i, cs):  # Time: O(logN)
    assert(len(cs) <= 4)
    interval_i = query_interval(Lt_intervals, i)
    interval_js = {j:query_interval(Lc_intervals, j) for j in cs}
    if count_of_3_or_up(Lt) and count_of_3_or_up(Lc):
        # split the only 3 or up of Lt by i and put i into one of valid Lc[1]
        max_key = max(k for k, v in Lt.iteritems() if v != 0)
        if Lt[max_key] == 1 and interval_i[1] == max_key and 1 in Lc and Lc[1]-sum(interval_js[j][1] == 1 for j in cs) > 0:
            if max_key == 3:
                if interval_i[0] in (1, 3):
                    return not is_A_winning_state(Lt_Z, Lc_Z, K-1)
            if max_key == 4:
                if interval_i[0] in (2, 3):
                    return not is_A_winning_state(Lt_Z-1, Lc_Z, K-1)
            if max_key == 5:
                if interval_i[0] == 3:
                    return not is_A_winning_state(Lt_Z, Lc_Z, K-1)
            return False
        # put i of which Lt length is 1 and put it into the valid cells of the only Lc with length 3 or up
        if interval_i[1] > 1 or count_of_3_or_up(Lc) > 1:
            return False
        max_key = max(k for k, v in Lc.iteritems() if v != 0)
        if Lc[max_key] > 1:
            return False
        group = defaultdict(set)
        for j in cs:
            if interval_js[j][1] == max_key:
                group[interval_js[j][1]].add(interval_js[j][0])
        if max_key == 3:  # split 3 into (0, 2) or (1, 1), and put the pivot i into one of Lt_1
            if max_key not in group or 2 not in group[max_key]:
                return not is_A_winning_state(Lt_Z, Lc_Z-1, K-1)
            elif max_key not in group or 1 not in group[max_key] or 3 not in group[max_key]:
                return not is_A_winning_state(Lt_Z, Lc_Z, K-1)
            return False
        if max_key == 4:  # split 4 into (1, 2), and put the pivot i into one of Lt_1
            if max_key not in group or 2 not in group[max_key] or 3 not in group[max_key]:
                return not is_A_winning_state(Lt_Z, Lc_Z-1, K-1)
            return False
        if max_key == 5:  # split 5 into (2, 2), and put the pivot i into one of Lt_1
            if max_key not in group or 3 not in group[max_key]:
                return not is_A_winning_state(Lt_Z, Lc_Z, K-1)
            return False
        return False
    if 2*Lt_Z == 2*Lc_Z == K:  # both Lt and Lc prime are all 2s
        return False
    if interval_i[1] > 1:
        if 1 not in Lc or (Lc[1]-sum(interval_js[j][1] == 1 for j in cs) == 0):
            return False
        delta = int(interval_i[1]%2 == 0 or interval_i[0]%2 == 0)  # any pos of even length or even pos of odd length
        return not is_A_winning_state(Lt_Z-delta, Lc_Z, K-1)  # reduce the number of 2 in Lt_prime as possible
    if K-len(cs) == 0:
        return False
    group = defaultdict(set)
    for j in cs:
        group[interval_js[j][2], interval_js[j][1]].add(interval_js[j][0])
    reserved_Lc_Z, delta = 0, 0
    for (_, l), ps in group.iteritems():
        count = l//2
        reserved_Lc_Z += count
        if l%2 == 0:
            if len(ps) == l:
                count = 0
        else:
            for p in ps:
                if p%2 == 0:
                    count -= 1
        if count:
            delta = 1
            break
    else:
        delta = min(1, Lc_Z-reserved_Lc_Z)
    return not is_A_winning_state(Lt_Z, Lc_Z-delta, K-1)  # reduce the number of 2 in Lt_prime as possible

def B_try_to_avoid_2_moves_win(Lt, Lt_Z, Lc, Lc_Z, K):  # Time: O(1)
    if count_of_3_or_up(Lt) and count_of_3_or_up(Lc):
        # split the only 3 or up and put the pivot i into one of valid Lc[1]
        max_key = max(k for k, v in Lt.iteritems() if v != 0)
        if Lt[max_key] == 1 and 1 in Lc:
            if max_key == 3:
                return not is_A_winning_state(Lt_Z-1, Lc_Z, K-1)
            if max_key == 4:
                return not is_A_winning_state(Lt_Z-1, Lc_Z, K-1)
            if max_key == 5:
                return not is_A_winning_state(Lt_Z, Lc_Z, K-1)
            return False
        # put the pivot i of which Lt length is 1 and put it into the valid cells of the only Lc with length 3 or up
        if 1 not in Lt or count_of_3_or_up(Lc) > 1:
            return False
        max_key = max(k for k, v in Lc.iteritems() if v != 0)
        if Lc[max_key] > 1:
            return False
        if max_key == 3:  # split 3 into (0, 2) or (1, 1), and put the pivot i into one of Lt_1, using (1, 1) is enough
            return not is_A_winning_state(Lt_Z, Lc_Z-1, K-1)
        if max_key == 4:  # split 4 into (1, 2), and put the pivot i into one of Lt_1
            return not is_A_winning_state(Lt_Z, Lc_Z-1, K-1)
        if max_key == 5:  # split 5 into (2, 2), and put the pivot i into one of Lt_1
            return not is_A_winning_state(Lt_Z, Lc_Z, K-1)
        return False
    if 2*Lt_Z == 2*Lc_Z == K:  # both Lt and Lc prime are all 2s
        return False
    if 1 in Lt:  # exists 1
        assert(Lt[1] != 0)
        can_B_win = not is_A_winning_state(Lt_Z, max(Lc_Z-1, 0), K-1)  # reduce the number of 2 in Lc_prime as possible
        if can_B_win:
            return True
    if 1 in Lc:  # exists 1
        assert(Lc[1] != 0)
        can_B_win = not is_A_winning_state(max(Lt_Z-1, 0), Lc_Z, K-1)  # reduce the number of 2 in Lt_prime as possible
        if can_B_win:
            return True
    return False

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

def is_B_winning_state(tiles, cells, Lt, Lt_intervals, Lt_Z, Lc, Lc_intervals, Lc_Z, K, i, j):  # Time: O(logN)
    if (((j-1 >= 0 and cells[j-1] == -2) or (j+1 < len(cells) and cells[j+1] == -2)) and
        ((i-1 >= 0 and tiles[i-1] == -2) or (i+1 < len(tiles) and tiles[i+1] == -2))):
        return False  # A would win immediately
    interval_i = query_interval(Lt_intervals, i)
    interval_j = query_interval(Lc_intervals, j)
    Lt_Z_delta = update_L(Lt, interval_i, 1)
    Lc_Z_delta = update_L(Lc, interval_j, 1)
    can_B_win = not ((count_of_3_or_up(Lt) and count_of_3_or_up(Lc)) or
                     (K == 2 and (Lt_Z+Lt_Z_delta) == (Lc_Z+Lc_Z_delta) == 1) or
                     (K%2 and 2*((Lt_Z+Lt_Z_delta) + (Lc_Z+Lc_Z_delta)) > K))
    update_L(Lc, interval_j, -1)
    update_L(Lt, interval_i, -1)
    return can_B_win

def is_B_winning(tiles, cells, active_tiles, active_cells, Lt, Lt_intervals, Lt_Z, Lc, Lc_intervals, Lc_Z, K):  # Time: O(logN)
    if K == 0:
        return True
    if active_tiles:  # try to avoid A win immediately
        if len(active_tiles) == 1:  # one active tile to one or up active cells
            i, cs = next(active_tiles.iteritems())
            can_B_win = B_try_to_avoid_1_or_2_moves_win(Lt, Lt_intervals, Lt_Z, Lc, Lc_intervals, Lc_Z, K, i, cs)  # Time: O(logN)
            if can_B_win:
                return True
            if len(cs) == 1:
                j = next(iter(cs))
                ts = active_cells[j]
                return B_try_to_avoid_1_or_2_moves_win(Lc, Lc_intervals, Lc_Z, Lt, Lt_intervals, Lt_Z, K, j, ts)  # Time: O(logN)
            return False
        if len(active_cells) == 1:  # two or up active tiles to one active cells
            j, ts = next(active_cells.iteritems())
            assert(len(ts) != 1)  # len(ts) == 1 is covered by the previous checks
            return B_try_to_avoid_1_or_2_moves_win(Lc, Lc_intervals, Lc_Z, Lt, Lt_intervals, Lt_Z, K, j, ts)  # Time: O(logN)
        stats, ts, cs = find_cell_to_fill(active_cells)
        if cs and len(stats) == 1 and 1 in stats and len(stats[1]) == 1:  # one tile with one or up cells, the other is one or up tiles with one cell
            new_ts, new_cs = next(stats[1].iteritems())
            i, j = next(iter(new_ts)), next(iter(cs))
            can_B_win = (i not in ts) and is_B_winning_state(tiles, cells, Lt, Lt_intervals, Lt_Z, Lc, Lc_intervals, Lc_Z, K-1, i, j)
            if can_B_win:
                return True
            if len(ts) == 1 and len(new_cs) == 1:
                i, j = next(iter(ts)), next(iter(new_cs))
                return is_B_winning_state(tiles, cells, Lt, Lt_intervals, Lt_Z, Lc, Lc_intervals, Lc_Z, K-1, i, j)
            return False
        return False
    return B_try_to_avoid_2_moves_win(Lt, Lt_Z, Lc, Lc_Z, K)

def adjacent_and_consecutive():
    N = input()
    result, tiles, cells, prev = [0, 0], [-2]*N, [-2]*N, True
    active_tiles, active_cells = defaultdict(set), defaultdict(set)
    Lt_intervals = SkipList(end=N)
    Lt_intervals.add(-1)
    Lc_intervals = SkipList(end=N)
    Lc_intervals.add(-1)
    A_already_won = False  # A can win in 0 moves
    Lt = compress_state(tiles)
    Lc = compress_state(cells)
    K = N
    Lt_Z = sum((k//2)*v for k, v in Lt.iteritems())
    Lc_Z = sum((k//2)*v for k, v in Lc.iteritems())
    for i in xrange(N):
        M, C = map(int, raw_input().strip().split())
        M, C = M-1, C-1
        Lt_Z += update_L(Lt, query_interval(Lt_intervals, M), 1)  # Time: O(logN)
        Lc_Z += update_L(Lc, query_interval(Lc_intervals, C), 1)  # Time: O(logN)
        tiles[M], cells[C] = C, M
        Lt_intervals.add(M)  # Time: O(logN)
        Lc_intervals.add(C)  # Time: O(logN)
        update_immediately_win(tiles, cells, M, C, active_tiles, active_cells)  # Time: O(1)
        K -= 1
        if not A_already_won:
            A_already_won = (C-1 >= 0 and abs(M-cells[C-1]) == 1) or (C+1 < len(cells) and abs(M-cells[C+1]) == 1)
        if i%2 == 0:
            curr = is_B_winning(tiles, cells, active_tiles, active_cells, Lt, Lt_intervals, Lt_Z, Lc, Lc_intervals, Lc_Z, K) if not A_already_won else False
            if prev and curr:
                result[i%2] += 1
        else:
            curr = A_already_won or is_A_winning(tiles, cells, active_tiles, active_cells, Lt, Lt_Z, Lc, Lc_Z, K)
            if prev and curr:
                result[i%2] += 1
        prev = curr
    assert(result[0] >= result[1])
    return "%s %s" % tuple(result)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, adjacent_and_consecutive())
