# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 2 - Problem D. Emacs++
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ffb9/000000000033893b
#
# Time:  O(KlogK + QlogK)
# Space: O(KlogK)
#

from itertools import izip
from functools import partial

# Template:
# https://github.com/kamyu104/FacebookHackerCup-2019/blob/master/Final%20Round/temporal_revision.py
class TreeInfos(object):
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
        if self.is_ancestor(a, b):
            return a
        if self.is_ancestor(b, a):
            return b
        for i in reversed(xrange(len(self.P[a]))):  # O(logN)
            if i < len(self.P[a]) and self.P[a][i] != -1 and \
              not self.is_ancestor(self.P[a][i], b):
                a = self.P[a][i]
        return self.P[a][0]

def add_dist_array(a, b):
    return [min(a[j]+b[j][i] for j in xrange(2)) for i in xrange(2)]

def add_dist_matrix(a, b):
    return [add_dist_array(a[i], b) for i in xrange(2)]

def accu_dist(up_dist_matrix, down_dist_matrix, P, curr, i):
    if i < len(up_dist_matrix[P[curr][i]]):
        up_dist_matrix[curr].append(add_dist_matrix(up_dist_matrix[curr][i],
                                                    up_dist_matrix[P[curr][i]][i]))
    if i < len(down_dist_matrix[P[curr][i]]):
        down_dist_matrix[curr].append(add_dist_matrix(down_dist_matrix[curr][i],
                                                      down_dist_matrix[P[curr][i]][i]))

def find_pairid_and_side(nodes):
    pairid_and_side = [None]*(len(nodes)*2)
    for i, (l, r) in enumerate(nodes):
        pairid_and_side[l], pairid_and_side[r] = (i, 0), (i, 1)
    return pairid_and_side

def build_tree(s):  # Time: O(K)
    nodes, children, stk = [], [[] for _ in xrange(len(s)//2)], []
    parent = -1
    for i, p in enumerate(s):
        if p == '(':
            if i:
                children[stk[-1]].append(len(nodes))
            stk.append(len(nodes))
            nodes.append([i, -1])
        else:
            nodes[stk.pop()][1] = i
    return nodes, children

def init_dist(L, R, P, nodes, children):
    def divide(curr):
        stk.append(partial(postprocess, curr))
        for child in reversed(children[curr]):
            stk.append(partial(divide, child))

    def postprocess(curr):
        l, r = nodes[curr]
        left_outer_to_right_outer[curr], right_outer_to_left_outer[curr] = R[l], L[r]
        child_idx = 0
        for child in children[curr]:
            child_idx_of_parent[child] = child_idx
            child_idx += 1
            child_l, child_r = nodes[child]
            left_outer_to_right_outer[curr] += left_outer_to_right_outer[child]+R[child_r]
            right_outer_to_left_outer[curr] += right_outer_to_left_outer[child]+L[child_l]
        left_outer_to_right_outer[curr] = min(left_outer_to_right_outer[curr], P[l])
        right_outer_to_left_outer[curr] = min(right_outer_to_left_outer[curr], P[r])

    left_outer_to_right_outer, right_outer_to_left_outer, child_idx_of_parent = [0]*len(nodes), [0]*len(nodes), [0]*len(nodes)
    stk = []
    stk.append(partial(divide, 0))
    while stk:
        stk.pop()()
    return left_outer_to_right_outer, right_outer_to_left_outer, child_idx_of_parent

def find_dist_and_prefix_sum(L, R, nodes, children, left_outer_to_right_outer, right_outer_to_left_outer):
    def divide(curr):
        for child in reversed(children[curr]):
            stk.append(partial(divide, child))
        stk.append(partial(preprocess, curr))

    def preprocess(curr):
        l, r = nodes[curr]
        prefix_sum_from_left_inner_to_left_outer, accu = [0]*len(children[curr]), 0
        for i, child in enumerate(children[curr]):
            child_l, _ = nodes[child]
            accu += L[child_l]
            prefix_sum_from_left_inner_to_left_outer[i] = accu
            accu += right_outer_to_left_outer[child]
        prefix_sum_from_left_outer_to_left_inner, accu = [0]*len(children[curr]), R[l]
        for i, child in enumerate(children[curr]):
            _, child_r = nodes[child]
            prefix_sum_from_left_outer_to_left_inner[i] = accu
            accu += left_outer_to_right_outer[child]+R[child_r]
        prefix_sum_from_right_inner_to_right_outer, accu =  [0]*len(children[curr]), 0
        for i, child in enumerate(reversed(children[curr])):
            _, child_r = nodes[child]
            accu += R[child_r]
            prefix_sum_from_right_inner_to_right_outer[~i] = accu
            accu += left_outer_to_right_outer[child]
        prefix_sum_from_right_outer_to_right_inner, accu =  [0]*len(children[curr]), L[r]
        for i, child in enumerate(reversed(children[curr])):
            child_l, _ = nodes[child]
            prefix_sum_from_right_outer_to_right_inner[~i] = accu
            accu += right_outer_to_left_outer[child]+L[child_l]
        for i, child in enumerate(children[curr]):
            left_outer_to_right_outer[child] = min(left_outer_to_right_outer[child],
                                                   prefix_sum_from_left_inner_to_left_outer[i]+
                                                   left_outer_to_right_outer[curr]+
                                                   prefix_sum_from_right_outer_to_right_inner[i])
            right_outer_to_left_outer[child] = min(right_outer_to_left_outer[child],
                                                   prefix_sum_from_right_inner_to_right_outer[i]+
                                                   right_outer_to_left_outer[curr]+
                                                   prefix_sum_from_left_outer_to_left_inner[i])
        prefix_sum_from_first_to_curr_child[curr].append(0)
        for child in children[curr]:
            _, child_r = nodes[child]
            prefix_sum_from_first_to_curr_child[curr].append(prefix_sum_from_first_to_curr_child[curr][-1]+
                                                             left_outer_to_right_outer[child]+R[child_r])
        prefix_sum_from_curr_to_first_child[curr].append(0)
        for child in children[curr]:
            child_l, _ = nodes[child]
            prefix_sum_from_curr_to_first_child[curr].append(prefix_sum_from_curr_to_first_child[curr][-1]+
                                                             right_outer_to_left_outer[child]+L[child_l])
        for i, child in enumerate(children[curr]):
            up = [[prefix_sum_from_left_inner_to_left_outer[i],
                   prefix_sum_from_left_inner_to_left_outer[i]+left_outer_to_right_outer[curr]],
                  [prefix_sum_from_right_inner_to_right_outer[i]+right_outer_to_left_outer[curr],
                   prefix_sum_from_right_inner_to_right_outer[i]]]
            for j in xrange(2):
                up[0][j] = min(up[0][j], left_outer_to_right_outer[child]+up[1][j])
            for j in xrange(2):
                up[1][j] = min(up[1][j], right_outer_to_left_outer[child]+up[0][j])
            up_dist_matrix[child] = [up]
        for i, child in enumerate(children[curr]):
            down = [[prefix_sum_from_left_outer_to_left_inner[i],
                     prefix_sum_from_right_outer_to_right_inner[i]+right_outer_to_left_outer[child]],
                    [prefix_sum_from_left_outer_to_left_inner[i]+left_outer_to_right_outer[child],
                     prefix_sum_from_right_outer_to_right_inner[i]]]
            for j in xrange(2):
                down[j][0] = min(down[j][0], left_outer_to_right_outer[curr]+down[j][1])
            for j in xrange(2):
                down[j][1] = min(down[j][1], right_outer_to_left_outer[curr]+down[j][0])
            down_dist_matrix[child] = [down]

    up_dist_matrix, down_dist_matrix = [[[] for _ in xrange(len(nodes))] for _ in xrange(2)]
    prefix_sum_from_first_to_curr_child, prefix_sum_from_curr_to_first_child = [[[] for _ in xrange(len(nodes))] for _ in xrange(2)]
    stk = []
    stk.append(partial(divide, 0))
    while stk:
        stk.pop()()
    return up_dist_matrix, down_dist_matrix, prefix_sum_from_first_to_curr_child, prefix_sum_from_curr_to_first_child

def init_up_dist_array(left_outer_to_right_outer, right_outer_to_left_outer, curr, side):
    if side == 0:
        return [0, left_outer_to_right_outer[curr]]
    return [right_outer_to_left_outer[curr], 0]

def init_down_dist_array(left_outer_to_right_outer, right_outer_to_left_outer, curr, side):
    if side == 0:
        return [0, right_outer_to_left_outer[curr]]
    return [left_outer_to_right_outer[curr], 0]

def go_up(left_outer_to_right_outer, right_outer_to_left_outer, tree_infos, up_dist_matrix, curr, side, lca):
    up_dist_array = init_up_dist_array(left_outer_to_right_outer, right_outer_to_left_outer, curr, side)
    for i in reversed(xrange(len(tree_infos.P[curr]))):  # O(logN)
        if i < len(tree_infos.P[curr]) and tree_infos.P[curr][i] != -1 and \
           tree_infos.D[tree_infos.P[curr][i]] > tree_infos.D[lca]:
            up_dist_array = add_dist_array(up_dist_array, up_dist_matrix[curr][i])
            curr = tree_infos.P[curr][i]
    assert(curr != lca and tree_infos.P[curr][0] == lca)
    return [curr, up_dist_array]

def go_down(left_outer_to_right_outer, right_outer_to_left_outer, tree_infos, down_dist_matrix, curr, side, lca):
    down_dist_array = init_down_dist_array(left_outer_to_right_outer, right_outer_to_left_outer, curr, side)
    for i in reversed(xrange(len(tree_infos.P[curr]))):  # O(logN)
        if i < len(tree_infos.P[curr]) and tree_infos.P[curr][i] != -1 and \
           tree_infos.D[tree_infos.P[curr][i]] > tree_infos.D[lca]:
            down_dist_array = add_dist_array(down_dist_array, down_dist_matrix[curr][i])
            curr = tree_infos.P[curr][i]
    assert(curr != lca and tree_infos.P[curr][0] == lca)
    return [curr, down_dist_array]

def prefix_sum(a, l, r):
    if l > r:
        return 0
    return a[r+1]-a[l]

def prefix_sum_of_child_node_from_left(R, nodes, children, prefix_sum_from_first_to_curr_child, curr, l, r):
    assert(l < r)
    return R[nodes[children[curr][l]][1]]+prefix_sum(prefix_sum_from_first_to_curr_child[curr], l+1, r-1)

def prefix_sum_of_child_node_from_right(L, nodes, children, prefix_sum_from_curr_to_first_child, curr, l, r):
    assert(l < r)
    return L[nodes[children[curr][r]][0]]+prefix_sum(prefix_sum_from_curr_to_first_child[curr], l+1, r-1)

def query(L, R, nodes, children, pairid_and_side,
          left_outer_to_right_outer, right_outer_to_left_outer, child_idx_of_parent,
          up_dist_matrix, down_dist_matrix,
          prefix_sum_from_first_to_curr_child, prefix_sum_from_curr_to_first_child,
          tree_infos,
          s, e):
    pairid_a, side_a = pairid_and_side[s]
    pairid_b, side_b = pairid_and_side[e]
    if pairid_a == pairid_b:
        return init_up_dist_array(left_outer_to_right_outer, right_outer_to_left_outer, pairid_a, side_a)[side_b]
    lca = tree_infos.lca(pairid_a, pairid_b)
    if lca == pairid_b:
        child_a, child_up_dist_array = go_up(left_outer_to_right_outer, right_outer_to_left_outer,
                                             tree_infos, up_dist_matrix, pairid_a, side_a, lca)
        return min(child_up_dist_array[i]+up_dist_matrix[child_a][0][i][side_b] for i in xrange(2))
    if lca == pairid_a:
        child_b, child_down_dist_array = go_down(left_outer_to_right_outer, right_outer_to_left_outer,
                                                 tree_infos, down_dist_matrix, pairid_b, side_b, lca)
        return min(child_down_dist_array[j]+down_dist_matrix[child_b][0][j][side_a] for j in xrange(2))
    child_a, child_up_dist_array = go_up(left_outer_to_right_outer, right_outer_to_left_outer,
                                         tree_infos, up_dist_matrix, pairid_a, side_a, lca)
    child_b, child_down_dist_array = go_down(left_outer_to_right_outer, right_outer_to_left_outer,
                                             tree_infos, down_dist_matrix, pairid_b, side_b, lca)
    result = min(child_up_dist_array[i]+up_dist_matrix[child_a][0][i][0]+
                 child_down_dist_array[j]+down_dist_matrix[child_b][0][j][0]
                 for i in xrange(2) for j in xrange(2))
    if child_idx_of_parent[child_a] < child_idx_of_parent[child_b]:
        result = min(result,
                     child_up_dist_array[1]+
                     prefix_sum_of_child_node_from_left(
                         R, nodes, children, prefix_sum_from_first_to_curr_child,
                         lca, child_idx_of_parent[child_a], child_idx_of_parent[child_b])+
                     child_down_dist_array[0])
    else:
        result = min(result,
                     child_up_dist_array[0]+
                     prefix_sum_of_child_node_from_right(
                         L, nodes, children, prefix_sum_from_curr_to_first_child,
                         lca, child_idx_of_parent[child_b], child_idx_of_parent[child_a])+
                     child_down_dist_array[1])
    return result

def emacspp():
    K, Q = map(int, raw_input().strip().split())
    PRG = raw_input().strip()
    L, R, P, S, E = [map(int, raw_input().strip().split()) for _ in xrange(5)]
    K += 2
    PRG = '('+PRG+')'
    L, R, P = [INF]+L+[INF], [INF]+R+[INF], [INF]+P+[INF]
    nodes, children = build_tree(PRG)
    pairid_and_side = find_pairid_and_side(nodes)
    left_outer_to_right_outer, right_outer_to_left_outer, child_idx_of_parent = init_dist(L, R, P, nodes, children)
    ret = find_dist_and_prefix_sum(L, R, nodes, children, left_outer_to_right_outer, right_outer_to_left_outer)
    up_dist_matrix, down_dist_matrix, prefix_sum_from_first_to_curr_child, prefix_sum_from_curr_to_first_child = ret
    tree_infos = TreeInfos(children, partial(accu_dist, up_dist_matrix, down_dist_matrix))
    return sum(query(L, R, nodes, children, pairid_and_side,
                     left_outer_to_right_outer, right_outer_to_left_outer, child_idx_of_parent,
                     up_dist_matrix, down_dist_matrix,
                     prefix_sum_from_first_to_curr_child, prefix_sum_from_curr_to_first_child,
                     tree_infos,
                     s, e)
               for s, e in izip(S, E))

INF = float("inf")
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, emacspp())
