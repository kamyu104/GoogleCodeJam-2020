# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 3 - Problem D. Recalculating
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff7e/00000000003775e9
#
# Time:  O(N^2 * logN), even without MLE, it still faces TLE if N = 1687 in both Python2 / PyPy2
# Space: O(N^2), it gets MLE if N = 1687, since memory usage of "(x0, y0, x1, y1) * (4*N^2)" is much greater than 1GB in both Python2 / PyPy2
#

from collections import defaultdict, deque
from functools import partial
from fractions import gcd

class SegmentTree(object):
    def __init__(self, N, build_fn, update_fn, query_fn):
        self.N = N
        self.tree = build_fn(N)
        self.update_fn = update_fn
        self.query_fn = query_fn

    def __apply(self, x, val):
        self.update_fn(self.tree[x], val)

    def update(self, L, R, h):  # Time: O(logN), Space: O(N) 
        def pull(x):
            while x > 1:
                x //= 2
                self.query_fn(self.tree, x)

        L += self.N
        R += self.N
        L0, R0 = L, R
        while L <= R:
            if L & 1:  # is right child
                self.__apply(L, h)
                self.query_fn(self.tree, L)
                L += 1
            if R & 1 == 0:  # is left child
                self.__apply(R, h)
                self.query_fn(self.tree, R)
                R -= 1
            L //= 2
            R //= 2
        pull(L0)
        pull(R0)
    
    def query(self):
        return self.tree[1]

def group_rects(points, D):
    x_set, y_set = set(), set()
    for x, y in points:
        x_set.add(x-D)
        x_set.add(x+D)
        y_set.add(y-D)
        y_set.add(y+D)
    xs, ys = sorted(x_set), sorted(y_set)
    total = 0
    groups = defaultdict(list)
    debug = 0
    for j in xrange(len(ys)-1):
        rolling_hash, left, right = 0, 0, 0
        dq = deque()
        for i in xrange(len(xs)-1):
            while right < len(points) and points[right][0] <= xs[i]+D:
                if ys[j+1]-D <= points[right][1] <= ys[j]+D:
                    if dq:
                        a = dq[-1]
                        rolling_hash = (rolling_hash*P*P +
                                        (points[right][0]-points[a][0])*P+
                                        (points[right][1]-points[a][1]))%MOD
                    dq.append(right)
                right += 1
            while left < len(points) and points[left][0] < xs[i+1]-D:
                if ys[j+1]-D <= points[left][1] <= ys[j]+D:
                    a = dq.popleft()
                    if len(dq) >= 1:
                        b = dq[0]
                        rolling_hash = (rolling_hash -
                                        ((points[b][0]-points[a][0])*P+
                                         (points[b][1]-points[a][1]))*exp(2*(len(dq)-1)))%MOD
                left += 1
            if not dq:
                continue
            # the rectangle is fully covered by ordered repairs centers in dq,
            # normalized by shift to the first repair center
            x0, y0 = points[dq[0]][0]-(xs[i+1]-D), points[dq[0]][1]-(ys[j+1]-D)
            x1, y1 = points[dq[0]][0]-(xs[i]-D), points[dq[0]][1]-(ys[j]-D)
            total += (x1-x0)*(y1-y0)
            groups[rolling_hash].append((x0, y0, x1, y1))
            debug += 1
            assert(len(dq) <= len(points))
            assert(debug <= (2*len(points)-1)**2)
            assert(len(groups) <= len(points)**2)
    return total, groups

def calc_unique_area(groups):
    def build(N):
        tree = [[0, 0, 0] for _ in xrange(2*N)]
        for x in reversed(xrange(1, len(tree))):
            query(ys, tree, x)
        return tree

    def update(x, v):
        x[2] += v

    def query(ys, tree, x):
        N = len(tree)//2
        if x >= N:  # leaf node
            for i in xrange(2):
                tree[x][i] = ys[(x-N)+1]-ys[(x-N)] if i-tree[x][2] == 0 else 0
        else:
            for i in xrange(2):
                tree[x][i] = tree[2*x][i-tree[x][2]] + tree[2*x+1][i-tree[x][2]] if i-tree[x][2] >= 0 else 0

    unique = 0
    for rects in groups.itervalues():
        intervals, y_set = [], set()
        for x0, y0, x1, y1 in rects:
            intervals.append((x0, (y0, y1), +1))
            intervals.append((x1, (y0, y1), -1))
            y_set.add(y0)
            y_set.add(y1)
        intervals.sort(key=lambda x: x[0]) # at most O(N^2) intervals, total time: O(N^2 * logN)
        ys = sorted(y_set)  # at most O(N^2) intervals, total time: O(N^2 * logN)
        y_to_idx = {y:i for i, y in enumerate(ys)}
        segment_tree = SegmentTree(len(ys)-1, build_fn=build,  update_fn=update, query_fn=partial(query, ys))
        for i in xrange(len(intervals)-1):
            x0, (y0, y1), v = intervals[i]
            segment_tree.update(y_to_idx[y0], y_to_idx[y1]-1, v)  # at most O(N^2) intervals, total time: O(N^2 * logN)
            unique += (intervals[i+1][0]-x0)*segment_tree.query()[1]
    return unique

def recalculating():
    N, D = map(int, raw_input().strip().split())
    points = []
    for _ in xrange(N):
        x, y = map(int, raw_input().strip().split())
        points.append((x+y, x-y))
    points.sort()
    total, groups = group_rects(points, D)
    unique = calc_unique_area(groups)
    g = gcd(unique, total)
    return "{} {}".format(unique//g, total//g)

def exp(x):
    if x not in LOOKUP:
        LOOKUP[x] = pow(P, x, MOD)
    return LOOKUP[x]

LOOKUP = {}
MOD = 10**9+7
P = 113
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, recalculating())
