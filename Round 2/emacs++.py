# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 2 - Problem D. Emacs++
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ffb9/000000000033893b
#
# Time:  O(K * (logK)^2 + QlogK), correct and fully tested by lots of edge cases,
#                                 optimized without MLE by lazy build,
#                                 pass in test case 1 for PyPy2 but TLE in test case 2 (time is very tight for Python/PyPy2)
# Space: O(KlogK)
#

from itertools import izip
from heapq import heappop, heappush
from bisect import bisect_left

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

def update_adj(lookup, brackets, adj, is_reversed, front, back, direction, dummy, d, l, r):  # Time: O(K)
    prev = back if front-d != dummy else dummy
    for src in direction(brackets):
        if prev == dummy:
            prev = src
            continue
        dst, via = prev, src-d
        if via == dst:
            w = l[src] if not is_reversed else r[dst]
        else:
            w = lookup[via][not is_reversed][src] + lookup[via][is_reversed][dst]
        adj[src][dst] = w if dst not in adj[src] else min(adj[src][dst], w)
        prev = src

def find_shortest_path(L, R, P, is_undir, pairs, lookup, brackets, t):  # Time: O(KlogK)
    result = []
    for is_reversed in xrange(1 if is_undir else 2):
        adj = {}
        for src in brackets:
            dst = pairs[src]
            w = P[src] if not is_reversed else P[dst]
            if src not in adj:
                adj[src] = {}
            adj[src][dst] = w if dst not in adj[src] else min(adj[src][dst], w)
        update_adj(lookup, brackets, adj, is_reversed,
                   brackets[0], brackets[-1], lambda x:x,
                   -1, 1, L, R)
        update_adj(lookup, brackets, adj, is_reversed,
                   brackets[-1], brackets[0], lambda x:reversed(x),
                   len(pairs), -1, R, L)
        result.append(dijkstra(adj, t))
    if is_undir:
        result.append(result[-1])
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

def find_partitions(PRG, pairs, parents, brackets):  # Time: O(K)
    result, mid = [-1]*4, (len(brackets)-1)//2
    if PRG[brackets[mid]] == '(':
        left, right = mid, find_next_bracket(PRG, brackets, mid, 1)
    else:
        left, right = find_next_bracket(PRG, brackets, mid, -1), mid
    while 2*(right-left+1) <= len(brackets)+2:  # including virtual brackets we added
        result[1], result[2] = brackets[left], brackets[right]
        left, right = find_next_bracket(PRG, brackets, left, -1), find_next_bracket(PRG, brackets, right, 1)
    result[0] = brackets[left] if left != -1 else parents[brackets[0]]
    result[-1] = brackets[right] if right != len(brackets) else parents[brackets[-1]]
    return result

def find_subregions(brackets, partitions):
    i, new_brackets = 0, [[] for _ in xrange(4)]
    for b in brackets:
        if i < 4 and b > partitions[i]:
            i += 1
        if i < 4 and b == partitions[i]:
            continue
        new_brackets[i%4].append(b)
    return new_brackets

def build(PRG, L, R, P, is_undir, pairs, parents, lookup, tree, node):  # Time: O(KlogK)
    brackets = tree[node][0]
    partitions = find_partitions(PRG, pairs, parents, brackets)  # Time: O(K)
    children = [0]*4
    tree[node] = [partitions, children, brackets[0], brackets[-1]]
    for p in partitions:
        if not (brackets[0] <= p <= brackets[-1]):  # virtual brackets we added
            continue
        lookup[p] = find_shortest_path(L, R, P, is_undir, pairs, lookup, brackets, p)  # Time: O(KlogK)
    for i, new_brackets in enumerate(find_subregions(brackets, partitions)):
        if not new_brackets:
            continue
        children[i] = len(tree)
        tree.append([new_brackets])

def query(PRG, L, R, P, is_undir, pairs, parents, lookup, tree, node, s, e):  # Time: O(K * (logK)^2) for lazy build, O(QlogK) for query, run at most O(KlogK) in each depth, at most O(logK) depth
    depth, ceil_log2_Kp1 = 0, ((len(PRG)+1)-1).bit_length()  # 2^d-1 >= k, d >= ceil(log(k+1))
    while True:
        depth += 1
        assert(depth <= ceil_log2_Kp1)
        if len(tree[node]) == 1:  # unvisited
            build(PRG, L, R, P, is_undir, pairs, parents, lookup, tree, node)
        partitions, children, front, back = tree[node]
        a, b = map(lambda x: bisect_left(partitions, x)%4, (s, e))
        if s == partitions[a] or e == partitions[b] or a != b:
            break
        node = children[a]  # same subregion without covering partition nodes, visit subregion
    return min(lookup[p][1][s] + lookup[p][0][e] for p in partitions if 0 <= p < len(PRG))  # find min LCA dist

def find_pairs_and_parents(s):  # Time: O(K)
    pairs, parents, stk = [0]*len(s), [None]*len(s), []
    parent = -1
    for right, p in enumerate(s):
        if p == '(':
            parents[right] = parent
            parent = right
            stk.append(right)
        else:
            left = stk.pop()
            parent = parents[left]
            pairs[left], pairs[right] = right, left
    for i in xrange(len(s)):
        if parents[i] is None:
            parents[i] = pairs[parents[pairs[i]]] if parents[pairs[i]] != -1 else len(s)
    return pairs, parents

def is_undirected(L, R, P, pairs):
    for i in xrange(len(pairs)):
        if P[i] != P[pairs[i]]:
            break
        if i-1 >= 0 and L[i] != R[i-1]:
            break
        if i+1 < len(pairs) and R[i] != L[i+1]:
            break
    else:
        return True
    return False

def emacspp():
    K, Q = map(int, raw_input().strip().split())
    PRG = raw_input().strip()
    L, R, P, S, E = [map(int, raw_input().strip().split()) for _ in xrange(5)]
    pairs, parents = find_pairs_and_parents(PRG)
    lookup, tree = [0]*K, [[range(len(PRG))]]
    is_undir = is_undirected(L, R, P, pairs)
    return sum(query(PRG, L, R, P, is_undir, pairs, parents, lookup, tree, 0, s-1, e-1) for s, e in izip(S, E))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, emacspp())
