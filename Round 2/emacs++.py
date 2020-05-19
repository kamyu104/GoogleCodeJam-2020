# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 2 - Problem D. Emacs++
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ffb9/000000000033893b
#
# Time:  O(K * (logK)^2 + QlogK)
# Space: O(KlogK), fully correct by testing, optimized without MLE, but TLE in pypy2
#

from itertools import izip
from heapq import heappop, heappush

def dijkstra(adj, t):  # Time: O(KlogK)
    result, visited = {}, set()
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

def find_shortest_path(PRG, L, R, P, pair, lookup, brackets, t):  # Time: O(KlogK)
    result = []
    for is_reversed in xrange(2):
        adj = {}
        for src in brackets:
            dst = pair[src]
            w = P[src] if not is_reversed else P[dst]
            if src not in adj:
                adj[src] = {}
            adj[src][dst] = w if dst not in adj[src] else min(adj[src][dst], w)
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

def find_outer_brackets(pair, brackets, partition_idxs, i, l, r):
    if i == 0:
         return l, r
    if i == 1:
        if partition_idxs[i-1] == -1:  # virtual brackets we added
            return l, r
        return brackets[partition_idxs[i-1]], pair[brackets[partition_idxs[i-1]]]
    elif i == 2:
        return brackets[partition_idxs[i-1]], pair[brackets[partition_idxs[i-1]]]
    elif i == 3:
        if partition_idxs[i] == len(brackets):  # virtual brackets we added
            return l, r
        return pair[brackets[partition_idxs[i]]], brackets[partition_idxs[i]]

def which_subregion(partitions, t):  # Time: O(1)
    for i, p in enumerate(partitions):
        if p > t:
            return i
    return 0

def query(PRG, L, R, P, pair, lookup, tree, node, s, e):  # Time: O(K * (logK)^2) for lazy ctor, O(QlogK) for query, run at most O(KlogK) in each depth, at most O(logK) depth
    # depth, ceil_logK = 0, (len(PRG)-1).bit_length()
    while True:
        # depth += 1
        # assert(depth <= ceil_logK)
        if len(tree[node]) == 3:  # unvisited
            brackets, l, r = tree[node]
            partition_idxs = find_partitions(PRG, brackets)  # Time: O(K)
            partitions = map(lambda x: l if x == -1 else (r if x == len(brackets) else brackets[x]), partition_idxs)  # replace virtual brackets with outer brackets
            children = [0]*4
            tree[node] = [partitions, children, l, r]  # visited
            for i in partition_idxs:
                if i in (-1, len(brackets)):  # virtual brackets we added
                    continue
                lookup[brackets[i]] = find_shortest_path(PRG, L, R, P, pair, lookup, brackets, brackets[i])  # Time: O(KlogK)
            for i in xrange(len(partition_idxs)):
                new_brackets = find_subregions(brackets, partition_idxs, i)
                if not new_brackets:
                    continue
                new_l, new_r = find_outer_brackets(pair, brackets, partition_idxs, i, l, r)
                children[i] = len(tree)
                tree.append([new_brackets, new_l, new_r])
        partitions, children, l, r = tree[node]
        a, b = which_subregion(partitions, s), which_subregion(partitions, e)
        if a != b or s in partitions or e in partitions:
            break
        node = children[a]  # same subregion without covering partition nodes, visit subregion
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
    pair, lookup, tree = find_pair(PRG), {}, [[range(len(PRG)), -1, len(PRG)]]
    return sum(query(PRG, L, R, P, pair, lookup, tree, 0, s-1, e-1) for s, e in izip(S, E))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, emacs())
