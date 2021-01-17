# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 2 - Problem D. Emacs++
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ffb9/000000000033893b
#
# Time:  O(KlogK + QlogK), pass in PyPy2 but Python2
# Space: O(KlogK)
#
# concise but slower solution of emacs++2.py
#

from itertools import izip
from functools import partial

# Template:
# https://github.com/kamyu104/FacebookHackerCup-2019/blob/master/Final%20Round/temporal_revision.py
class TreeInfos(object):  # Time: O(NlogN), Space: O(NlogN), N is the number of nodes
    def __init__(self, children, cb=lambda *x:None):
        def preprocess(curr, parent):
            # depth of the node i
            D[curr] = 1 if parent == -1 else D[parent]+1
            # ancestors of the node i
            P[curr].append(parent)
            i = 0
            while P[curr][i] != -1:
                cb(P, curr, i)
                P[curr].append(P[P[curr][i]][i] if i < len(P[P[curr][i]]) else -1)
                i += 1
            # the subtree of the node i is represented by traversal index L[i]..R[i]
            C[0] += 1
            L[curr] = C[0]

        def divide(curr, parent):
            stk.append(partial(postprocess, curr))
            for i in reversed(xrange(len(children[curr]))):
                child = children[curr][i]
                if child == parent:
                    continue
                stk.append(partial(divide, child, curr))
            stk.append(partial(preprocess, curr, parent))

        def postprocess(curr):
            R[curr] = C[0]

        N = len(children)
        L, R, D, P, C = [0]*N, [0]*N, [0]*N, [[] for _ in xrange(N)], [-1]
        stk = []
        stk.append(partial(divide, 0, -1))
        while stk:
            stk.pop()()
        assert(C[0] == N-1)
        self.L, self.R, self.D, self.P = L, R, D, P

    # Template:
    # https://github.com/kamyu104/FacebookHackerCup-2019/blob/master/Final%20Round/little_boat_on_the_sea.py
    def is_ancestor(self, a, b):  # includes itself
        return self.L[a] <= self.L[b] <= self.R[b] <= self.R[a]

    def lca(self, a, b):
        if self.D[a] > self.D[b]:
            a, b = b, a
        if self.is_ancestor(a, b):
            return a
        for i in reversed(xrange(len(self.P[a]))):  # O(logN)
            if i < len(self.P[a]) and self.P[a][i] != -1 and \
              not self.is_ancestor(self.P[a][i], b):
                a = self.P[a][i]
        return self.P[a][0]

def add_dist_array(a, b):
    return [min(a[j]+b[j][i] for j in xrange(2)) for i in xrange(2)]

def add_dist_matrix(a, b):
    return [add_dist_array(a[i], b) for i in xrange(2)]

def accu_dist_matrix(dist_matrix, P, curr, i):
    for j in xrange(2):
        if i < len(dist_matrix[j][P[curr][i]]):
            dist_matrix[j][curr].append(add_dist_matrix(dist_matrix[j][curr][i], dist_matrix[j][P[curr][i]][i]))

def build_tree(s):  # Time: O(K)
    nodes, children, stk = [], [[] for _ in xrange(len(s)//2)], []
    for i, p in enumerate(s):
        if p == '(':
            if i:
                children[stk[-1]].append(len(nodes))
            stk.append(len(nodes))
            nodes.append([i, -1])
        else:
            nodes[stk.pop()][1] = i
    return nodes, children

def find_pairid_and_side(nodes):  # Time: O(K)
    pairid_and_side = [None]*(len(nodes)*2)
    for i, (l, r) in enumerate(nodes):
        pairid_and_side[l], pairid_and_side[r] = (i, 0), (i, 1)
    return pairid_and_side

def init_dist(L, R, P, nodes, children):  # Time: O(K)
    def divide(curr):
        stk.append(partial(postprocess, curr))
        for child in reversed(children[curr]):
            stk.append(partial(divide, child))

    def postprocess(curr):
        for d in xrange(2):
            dist[d][curr] = costs[d^1][nodes[curr][d]]
        child_idx = 0
        for child in children[curr]:
            child_idx_of_parent[child] = child_idx
            child_idx += 1
            for d in xrange(2):
                dist[d][curr] += dist[d][child]+costs[d^1][nodes[child][d^1]]
        for d in xrange(2):
            dist[d][curr] = min(dist[d][curr], P[nodes[curr][d]])

    dist, child_idx_of_parent = [[0]*len(nodes) for _ in xrange(2)], [0]*len(nodes)
    costs = [L, R]
    stk = []
    stk.append(partial(divide, 0))
    while stk:
        stk.pop()()
    return dist, child_idx_of_parent

def find_dist_matrix_and_prefix_sum(L, R, nodes, children, dist):  # Time: O(K)
    def divide(curr):
        for child in reversed(children[curr]):
            stk.append(partial(divide, child))
        stk.append(partial(preprocess, curr))

    def preprocess(curr):
        prefix_sum_from = [[[0]*len(children[curr]) for _ in xrange(2)] for _ in xrange(2)]
        for d, direction in enumerate([lambda x:x, lambda x:reversed(x)]):
            delta = -2*d+1
            for j in xrange(2):
                accu = 0
                for i in direction(xrange(len(children[curr]))):
                    child = children[curr][i]
                    accu += costs[d^j][nodes[child][d]-j*delta]
                    prefix_sum_from[j][d][i] = accu
                    accu += dist[d^j^1][child]
        for d in xrange(2):
            for i, child in enumerate(children[curr]):
                dist[d][child] = min(dist[d][child], prefix_sum_from[0][d][i]+dist[d][curr]+prefix_sum_from[1][d^1][i])
        for d in xrange(2):
            for i, child in enumerate(children[curr]):
                src, dst = child, curr
                if d:
                    src, dst = dst, src
                matrix = [[prefix_sum_from[d][0][i], prefix_sum_from[d][0][i]+dist[0][dst]],
                          [prefix_sum_from[d][1][i]+dist[1][dst], prefix_sum_from[d][1][i]]]
                for j in xrange(2):
                    for k in xrange(2):
                        matrix[j][k] = min(matrix[j][k], dist[j][src]+matrix[j^1][k])
                if d:
                    matrix = zip(*matrix)
                dist_matrix[d][child] = [matrix]
        for d in xrange(2):
            prefix_sum[d][curr].append(0)
            for child in children[curr]:
                prefix_sum[d][curr].append(prefix_sum[d][curr][-1]+dist[d][child]+costs[d^1][nodes[child][d^1]])

    dist_matrix, prefix_sum = [[[[] for _ in xrange(len(nodes))] for _ in xrange(2)] for _ in xrange(2)]
    costs = [L, R]
    stk = []
    stk.append(partial(divide, 0))
    while stk:
        stk.pop()()
    return dist_matrix, prefix_sum

def init_dist_array(dist, d, curr, side):
    return [0, dist[d][curr]] if not side else [dist[d^1][curr], 0]

def accu_dist(dist, tree_infos, dist_matrix, d, curr, side, lca):  # Time: O(logK)
    dist_array = init_dist_array(dist, d, curr, side)
    for i in reversed(xrange(len(tree_infos.P[curr]))):  # O(logN)
        if i < len(tree_infos.P[curr]) and tree_infos.P[curr][i] != -1 and \
           tree_infos.D[tree_infos.P[curr][i]] > tree_infos.D[lca]:
            dist_array = add_dist_array(dist_array, dist_matrix[d][curr][i])
            curr = tree_infos.P[curr][i]
    assert(curr != lca and tree_infos.P[curr][0] == lca)
    return [curr, dist_array]

def prefix_sum_in_range(a, l, r):
    if l > r:
        return 0
    return a[r+1]-a[l]

def sum_in_range(L, R, nodes, children, prefix_sum, d, curr, l, r):
    if d:
        l, r = r, l
    costs, rng = [L, R], [l, r]
    return costs[d^1][nodes[children[curr][rng[d]]][d^1]]+prefix_sum_in_range(prefix_sum[d][curr], l+1, r-1)

def query(L, R, nodes, children, pairid_and_side, dist, child_idx_of_parent, dist_matrix, prefix_sum, tree_infos, s, e):  # Time: O(logK) per query
    (pairid_a, side_a), (pairid_b, side_b) = pairid_and_side[s], pairid_and_side[e]
    if pairid_a == pairid_b:
        return init_dist_array(dist, 0, pairid_a, side_a)[side_b]
    lca = tree_infos.lca(pairid_a, pairid_b)
    if lca == pairid_b:
        child_a, child_up_dist_array = accu_dist(dist, tree_infos, dist_matrix, 0, pairid_a, side_a, lca)
        return min(child_up_dist_array[i]+dist_matrix[0][child_a][0][i][side_b] for i in xrange(2))
    if lca == pairid_a:
        child_b, child_down_dist_array = accu_dist(dist, tree_infos, dist_matrix, 1, pairid_b, side_b, lca)
        return min(child_down_dist_array[j]+dist_matrix[1][child_b][0][j][side_a] for j in xrange(2))
    child_a, child_up_dist_array = accu_dist(dist, tree_infos, dist_matrix, 0, pairid_a, side_a, lca)
    child_b, child_down_dist_array = accu_dist(dist, tree_infos, dist_matrix, 1, pairid_b, side_b, lca)
    result = min(child_up_dist_array[i]+dist_matrix[0][child_a][0][i][0]+child_down_dist_array[j]+dist_matrix[1][child_b][0][j][0]
                 for i in xrange(2) for j in xrange(2))
    desc = child_idx_of_parent[child_a] > child_idx_of_parent[child_b]
    return min(result,
               child_up_dist_array[desc^1]+
               sum_in_range(L, R, nodes, children, prefix_sum, desc, lca, child_idx_of_parent[child_a], child_idx_of_parent[child_b])+
               child_down_dist_array[desc])

def emacspp():
    K, Q = map(int, raw_input().strip().split())
    PRG = raw_input().strip()
    L, R, P, S, E = [map(int, raw_input().strip().split()) for _ in xrange(5)]
    K += 2
    PRG = '('+PRG+')'
    L, R, P = [INF]+L+[INF], [INF]+R+[INF], [INF]+P+[INF]
    nodes, children = build_tree(PRG)
    pairid_and_side = find_pairid_and_side(nodes)
    dist, child_idx_of_parent = init_dist(L, R, P, nodes, children)
    dist_matrix, prefix_sum = find_dist_matrix_and_prefix_sum(L, R, nodes, children, dist)
    tree_infos = TreeInfos(children, partial(accu_dist_matrix, dist_matrix))
    return sum(query(L, R, nodes, children, pairid_and_side, dist, child_idx_of_parent, dist_matrix, prefix_sum, tree_infos, s, e)
               for s, e in izip(S, E))

INF = float("inf")
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, emacspp())
