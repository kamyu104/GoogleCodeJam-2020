# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 2 - Problem D. Emacs++
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ffb9/000000000033893b
#
# Time:  O(K * (logK)^2 + QlogK), correct and fully tested by lots of edge cases, optimized without MLE by lazy build,
#                                 but still TLE in PyPy2 (time is very tight for Python/PyPy2)
# Space: O(KlogK)
#

from itertools import izip
from heapq import heappop, heappush
from bisect import bisect_right

def dijkstra(adj, t):  # Time: O(KlogK)
    result, visited = {t:0}, set()
    min_heap = [(0, t)]
    while min_heap and len(visited) != len(adj):
        curr, u = heappop(min_heap)
        if u in visited:
            continue
        visited.add(u)
        for v, w in adj[u].iteritems():
            if v in visited:
                continue
            if v in result and result[v] <= curr+w:
                continue
            result[v] = curr+w
            heappush(min_heap, (curr+w, v))
    return result

def update_adj(lookup, brackets, adj, is_reversed, front, back, direction, end, d, l, r):  # Time: O(K)
    prev = back if front-d != end else end
    for src in direction(brackets):
        if prev == end:
            prev = src
            continue
        dst, via = prev, src-d
        if via == dst:
            w = l[src] if not is_reversed else r[dst]
        else:
            w = lookup[via][not is_reversed][src] + lookup[via][is_reversed][dst]
        adj[src][dst] = w if dst not in adj[src] else min(adj[src][dst], w)
        prev = src

def find_shortest_path(L, R, P, pair, lookup, brackets, t):  # Time: O(KlogK)
    result = []
    for is_reversed in xrange(2):
        adj = {}
        for src in brackets:
            dst = pair[src]
            w = P[src] if not is_reversed else P[dst]
            if src not in adj:
                adj[src] = {}
            adj[src][dst] = w if dst not in adj[src] else min(adj[src][dst], w)
        update_adj(lookup, brackets, adj, is_reversed,
                   brackets[0], brackets[-1], lambda x:x,
                   -1, 1, L, R)
        update_adj(lookup, brackets, adj, is_reversed,
                   brackets[-1], brackets[0], lambda x:reversed(x),
                   len(pair), -1, R, L)
        result.append(dijkstra(adj, t))
    return result

def find_next_bracket(PRG, brackets, curr, d):  # Time: O(K)
    count = 0
    while True:
        curr += d
        if not (0 <= curr < len(brackets)):
            break
        if PRG[brackets[curr]] == '(':
            count += 1
        else:
            count -= 1
        if count == -d:
            break
    return curr

def find_partitions(PRG, brackets):  # Time: O(K)
    result, mid = [-1]*4, (len(brackets)-1)//2
    if PRG[brackets[mid]] == '(':
        left, right = mid, find_next_bracket(PRG, brackets, mid, 1)
    else:
        left, right = find_next_bracket(PRG, brackets, mid, -1), mid
    while 2*(right-left+1) <= len(brackets)+2:  # including virtual brackets we added
        result[1], result[2] = left, right
        left, right = find_next_bracket(PRG, brackets, left, -1), find_next_bracket(PRG, brackets, right, 1)
    result[0], result[-1] = left, right
    return result

def find_subregions(brackets, partition_idxs, i):
    if i == 0:
        if partition_idxs[0] == -1:  # virtual brackets we added
            return []
        return brackets[:partition_idxs[0]] + brackets[partition_idxs[-1]+1:]
    return brackets[partition_idxs[i-1]+1:partition_idxs[i]]

def find_outer_brackets(pair, brackets, partition_idxs, i, outer_l, outer_r):
    if i == 0:
         return outer_l, outer_r
    elif i == 1:
        if partition_idxs[i-1] == -1:  # virtual brackets we added
            return outer_l, outer_r
        return brackets[partition_idxs[i-1]], pair[brackets[partition_idxs[i-1]]]
    elif i == 2:
        return brackets[partition_idxs[i-1]], pair[brackets[partition_idxs[i-1]]]
    elif i == 3:
        if partition_idxs[i] == len(brackets):  # virtual brackets we added
            return outer_l, outer_r
        return pair[brackets[partition_idxs[i]]], brackets[partition_idxs[i]]

def build(PRG, L, R, P, pair, lookup, tree, node):  # Time: O(KlogK)
    brackets, outer_l, outer_r = tree[node]
    partition_idxs = find_partitions(PRG, brackets)  # Time: O(K)
    partitions = map(lambda x: outer_l if x == -1 else (outer_r if x == len(brackets) else brackets[x]), partition_idxs)  # replace virtual brackets with outer brackets
    children = [0]*4
    tree[node] = [partitions, children, outer_l, outer_r]  # visited
    for i in partition_idxs:
        if i in (-1, len(brackets)):  # virtual brackets we added
            continue
        lookup[brackets[i]] = find_shortest_path(L, R, P, pair, lookup, brackets, brackets[i])  # Time: O(KlogK)
    for i in xrange(len(partition_idxs)):
        new_brackets = find_subregions(brackets, partition_idxs, i)
        if not new_brackets:
            continue
        new_outer_l, new_outer_r = find_outer_brackets(pair, brackets, partition_idxs, i, outer_l, outer_r)
        children[i] = len(tree)
        tree.append([new_brackets, new_outer_l, new_outer_r])

def query(PRG, L, R, P, pair, lookup, tree, node, s, e):  # Time: O(K * (logK)^2) for lazy build, O(QlogK) for query, run at most O(KlogK) in each depth, at most O(logK) depth
    depth, ceil_log2_Kp1 = 0, ((len(PRG)+1)-1).bit_length()  # 2^d-1 >= k, d >= ceil(log(k+1))
    while True:
        depth += 1
        assert(depth <= ceil_log2_Kp1)
        if len(tree[node]) == 3:  # unvisited
            build(PRG, L, R, P, pair, lookup, tree, node)
        partitions, children, l, r = tree[node]
        if s in partitions or e in partitions:
            break
        a, b = map(lambda x: bisect_right(partitions, x)%len(partitions), (s, e))
        if a != b:
            break
        node = children[a]  # same subregion without covering partition nodes, visit subregion
    return min(lookup[p][1][s] + lookup[p][0][e] for p in partitions if 0 <= p < len(PRG))

def find_pair(s):  # Time: O(K)
    result, stk = [0]*len(s), []
    for right, p in enumerate(s):
        if p == '(':
            stk.append(right)
        else:
            left = stk.pop()
            result[left], result[right] = right, left
    return result

def emacspp():
    K, Q = map(int, raw_input().strip().split())
    PRG = raw_input().strip()
    L, R, P, S, E = [map(int, raw_input().strip().split()) for _ in xrange(5)]
    pair, lookup, tree = find_pair(PRG), [0]*K, [[range(len(PRG)), -1, len(PRG)]]
    return sum(query(PRG, L, R, P, pair, lookup, tree, 0, s-1, e-1) for s, e in izip(S, E))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, emacspp())
