# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Virtual World Finals - Problem A. Replace All
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff31/00000000003b532b
#
# Time:  O(N * (logN)^2), pass in PyPy2 but Python2
# Space: O(N)
#

from functools import partial

# Template: https://github.com/kamyu104/FacebookHackerCup-2020/blob/master/Qualification%20Round/running_on_fumes_chapter_2.py
# Range Minimum Query
class SegmentTree(object):  # 0-based index
    def __init__(self, N,
                 build_fn=lambda x, y: [y]*(2*x),
                 query_fn=lambda x, y: y if x is None else min(x, y),
                 update_fn=lambda x, y: y if x is None else x+y,
                 default_val=float("inf")):
        self.N = N
        self.H = (N-1).bit_length()
        self.query_fn = query_fn
        self.update_fn = update_fn
        self.default_val = default_val
        self.tree = build_fn(N, default_val)
        self.lazy = [None]*N
        for i in reversed(xrange(1, N)):
            self.tree[i] = query_fn(self.tree[2*i], self.tree[2*i+1])

    def __apply(self, x, val):
        self.tree[x] = self.update_fn(self.tree[x], val)
        if x < self.N:
            self.lazy[x] = self.update_fn(self.lazy[x], val)

    def update(self, L, R, h):  # Time: O(logN), Space: O(N)
        def pull(x):
            while x > 1:
                x //= 2
                self.tree[x] = self.query_fn(self.tree[x*2], self.tree[x*2+1])
                if self.lazy[x] is not None:
                    self.tree[x] = self.update_fn(self.tree[x], self.lazy[x])

        L += self.N
        R += self.N
        L0, R0 = L, R
        while L <= R:
            if L & 1:  # is right child
                self.__apply(L, h)
                L += 1
            if R & 1 == 0:  # is left child
                self.__apply(R, h)
                R -= 1
            L //= 2
            R //= 2
        pull(L0)
        pull(R0)

    def query(self, L, R):  # Time: O(logN), Space: O(N)
        def push(x):
            n = 2**self.H
            while n != 1:
                y = x // n
                if self.lazy[y] is not None:
                    self.__apply(y*2, self.lazy[y])
                    self.__apply(y*2 + 1, self.lazy[y])
                    self.lazy[y] = None
                n //= 2

        result = None
        if L > R:
            return result

        L += self.N
        R += self.N
        push(L)
        push(R)
        while L <= R:
            if L & 1:  # is right child
                result = self.query_fn(result, self.tree[L])
                L += 1
            if R & 1 == 0:  # is left child
                result = self.query_fn(result, self.tree[R])
                R -= 1
            L //= 2
            R //= 2
        return result

# Template: https://github.com/kamyu104/FacebookHackerCup-2019/blob/master/Round%203/chain_of_command.py
class HLD(object):  # Heavy-Light Decomposition
    def __init__(self, root, adj):
        self.__idx = [0]
        self.__children = adj
        self.__parent = [-1]*len(adj)  # Space: O(N)
        self.__size = [-1]*len(adj)
        self.__left = [-1]*len(adj)
        self.__right = [-1]*len(adj)
        self.__chain = [-1]*len(adj)

        for parent, children in enumerate(adj):
            for c in children:
                self.__parent[c] = parent
        self.__chain[root] = root
        self.__find_heavy_light(root)
        self.__decompose(root)

    def __find_heavy_light(self, i):  # Time: O(N)
        def divide(i):
            for j in reversed(xrange(len(children[i]))):
                c = children[i][j]
                stk.append(partial(postprocess, i, j, c))
                stk.append(partial(divide, c))
            stk.append(partial(init, i))

        def init(i):
            size[i] = 1

        def postprocess(i, j, c):
            size[i] += size[c]
            if size[c] > size[children[i][0]]:
                children[i][0], children[i][j] = children[i][j], children[i][0]  # put heavy idx in children[i][0]

        stk, children, size = [], self.__children, self.__size
        stk.append(partial(divide, i))
        while stk:
            stk.pop()()

    def __decompose(self, i):  # Time: O(N)
        def divide(i):
            stk.append(partial(conquer, i))
            for j in reversed(xrange(len(children[i]))):
                c = children[i][j]
                stk.append(partial(divide, c))
                stk.append(partial(preprocess, i, j, c))
            stk.append(partial(init, i))

        def init(i):
            left[i] = idx[0]
            idx[0] += 1

        def preprocess(i, j, c):
            chain[c] = c if j > 0 else chain[i]  # create a new chain if not heavy

        def conquer(i):
            right[i] = idx[0]

        stk, children, idx, chain, left, right = [], self.__children, self.__idx, self.__chain, self.__left, self.__right
        stk.append(partial(divide, i))
        while stk:
            stk.pop()()

    def children(self, i):
        return self.__children[i]

    def parent(self, i):
        return self.__parent[i]

    def left(self, i):
        return self.__left[i]

    def right(self, i):
        return self.__right[i]

    def chain(self, i):
        return self.__chain[i]

def query_min_result_from_i_to_root(hld, segment_tree, i):
    min_v = INF
    while i >= 0:  # Time: O((logN)^2), O(logN) queries with O(logN) costs
        j = hld.chain(i)  # find head of chain
        min_v = min(min_v, segment_tree.query(hld.left(j), hld.left(i)))
        i = hld.parent(j)  # move to parent chain
    return min_v

def add_value_from_i_to_root(hld, segment_tree, i, v):
    while i >= 0:  # Time: O((logN)^2), O(logN) queries with O(logN) costs
        j = hld.chain(i)  # find head of chain
        segment_tree.update(hld.left(j), hld.left(i), v)
        i = hld.parent(j)  # move to parent chain

def dfs(adj, root, C):
    stk = [root]
    while stk:
        node = stk.pop()
        for child in reversed(adj[node]):
            C[child] += C[node]
            stk.append(child)

def pack_the_slopes():
    N = input()
    adj = [[] for _ in xrange(N)]
    S, C = [INF]*N, [0]*N
    for _ in xrange(N-1):
       U, V, S_V, C_V = map(int, raw_input().strip().split())
       U -= 1
       V -= 1
       adj[U].append(V)
       S[V] = S_V
       C[V] = C_V

    dfs(adj, 0, C)  # Time: O(N)
    hld = HLD(0, adj)  # Time: O(N)
    lookup = {hld.left(i):S[i] for i in xrange(N)}
    segment_tree = SegmentTree(N, build_fn=lambda x, y: [lookup[i-x] if i >= x else y for i in xrange(2*x)], default_val=INF)
    count, cost = 0, 0
    for i in sorted(range(1, N), key=lambda x: C[x]):  # greedily send to target i
        v = query_min_result_from_i_to_root(hld, segment_tree, i)  # Time: O(N * (logN)^2)
        count += v
        cost += v * C[i]
        add_value_from_i_to_root(hld, segment_tree, i, -v)  # Time: O(N * (logN)^2)
    return "%s %s" % (count, cost)

MAX_S = 10**5
MAX_N = 10**5
INF = MAX_S*(MAX_N-1)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, pack_the_slopes())
