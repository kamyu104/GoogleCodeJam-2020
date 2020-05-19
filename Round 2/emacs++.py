# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 2 - Problem D. Emacs++
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ffb9/000000000033893b
#
# Time:  O(K * (logK)^2 + QlogK)
# Space: O(KlogK), optimized without MLE, but TLE in pypy2
#

from collections import defaultdict
from itertools import izip
from heapq import heappop, heappush

def dijkstra(adj, result, t, is_reversed):
    visited = set()
    min_heap = [(0, t)]
    while min_heap and len(visited) != len(adj):
        curr, u = heappop(min_heap)
        if u in visited:
            continue
        visited.add(u)
        for v, w in adj[u].iteritems():
            if v in visited:
                continue
            if v in result[is_reversed] and result[is_reversed][v] <= curr+w:
                continue
            result[is_reversed][v] = curr+w
            heappush(min_heap, (curr+w, v))

def find_shortest_path(PRG, L, R, P, pair, lookup, brackets, t):  # Time: O(KlogK)
    result = [{}, {}]
    for is_reversed in xrange(2):
        adj = defaultdict(dict)
        prev = brackets[-1] if brackets[0]-1 != -1 else -1
        for src in brackets:
            if prev == -1:
                prev = src
                continue
            dst, via = prev, src-1
            if via == dst:
                w = L[src] if not is_reversed else R[dst]
            else:
                w = lookup[via][not is_reversed][src] + lookup[via][is_reversed][dst]
            adj[src][dst] = w if dst not in adj[src] else min(adj[src][dst], w)
            prev = src
        prev = brackets[0] if brackets[-1]+1 != len(PRG) else len(PRG)
        for src in reversed(brackets):
            if prev == len(PRG):
                prev = src
                continue
            dst, via = prev, src+1
            if via == dst:
                w = R[src] if not is_reversed else L[dst]
            else:
                w = lookup[via][not is_reversed][src] + lookup[via][is_reversed][dst]
            adj[src][dst] = w if dst not in adj[src] else min(adj[src][dst], w)
            prev = src
        for src in brackets:
            dst = pair[src]
            w = P[src] if not is_reversed else P[dst]
            adj[src][dst] = w if dst not in adj[src] else min(adj[src][dst], w)
        dijkstra(adj, result, t, is_reversed)
    return result

def find_next(PRG, brackets, curr, d):
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
        left, right = mid, find_next(PRG, brackets, mid, 1)
    else:
        left, right = find_next(PRG, brackets, mid, -1), mid
    while 2*(right-left+1) <= len(brackets)+2:  # including virtual brackets we added
        result[1], result[2] = left, right
        left, right = find_next(PRG, brackets, left, -1), find_next(PRG, brackets, right, 1)
    result[0], result[-1] = left, right
    return result

def region(partitions, t):  # Time: O(1)
    for i, p in enumerate(partitions):
        if p > t:
            return i
    return 0

def query(PRG, L, R, P, pair, lookup, tree, node, s, e):  # Time: O(K * (logK)^2), run at most O(KlogK) in each depth, at most O(logK) depth
    if len(tree[node]) == 3:
        brackets, l, r = tree[node]
        partition_idxs = find_partitions(PRG, brackets)  # Time: O(K)
        partitions = map(lambda x: l if x == -1 else (r if x == len(brackets) else brackets[x]), partition_idxs)  # replace virtual brackets with outer brackets
        children = [0]*4
        tree[node] = [partitions, children, l, r]
        for i in partition_idxs:
            if i in (-1, len(brackets)):  # virtual brackets we added
                continue
            lookup[brackets[i]] = find_shortest_path(PRG, L, R, P, pair, lookup, brackets, brackets[i])  # Time: O(KlogK)
        for i in xrange(len(partition_idxs)):
            new_l, new_r = l, r
            if i == 0:
                if partition_idxs[0] == -1:  # virtual brackets we added
                    continue
                new_brackets = brackets[:partition_idxs[0]] + brackets[partition_idxs[-1]+1:]
            else:
                new_brackets = brackets[partition_idxs[i-1]+1:partition_idxs[i]]
                if brackets[partition_idxs[i-1]] == '(':
                    new_l, new_r = partition_idxs[i-1], pair[brackets[partition_idxs[i-1]]]                    
            if not new_brackets:
                continue
            children[i] = len(tree)
            tree.append([new_brackets, new_l, new_r])
    partitions, children, l, r = tree[node]
    a, b = region(partitions, s), region(partitions, e)
    if not (a != b or s in partitions or e in partitions):  # same region without covering partition nodes
        return query(PRG, L, R, P, pair, lookup, tree, children[a], s, e)
    return min((lookup[p][1][s] if s != p else 0) + (lookup[p][0][e] if p != e else 0) for p in partitions if 0 <= p < len(PRG)) 

def find_pair(s):  # Time: O(K)
    result, stk = [0]*len(s), []
    for right, p in enumerate(s):
        if p == '(':
            stk.append(right)
        else:
            left = stk.pop()
            result[left], result[right] = right, left
    return result

def emacs():
    K, Q = map(int, raw_input().strip().split())
    PRG = raw_input().strip()
    L, R, P, S, E = [map(int, raw_input().strip().split()) for _ in xrange(5)]
    result, pair, lookup, tree = 0, find_pair(PRG), {}, [[range(len(PRG)), -1, len(PRG)]]
    return sum(query(PRG, L, R, P, pair, lookup, tree, 0, s-1, e-1) for s, e in izip(S, E))  # Time: O(QlogK)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, emacs())
