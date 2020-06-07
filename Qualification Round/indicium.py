# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Qualification Round - Problem E. Indicium
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd27/0000000000209aa0
#
# Time:  O(N^3 * sqrt(N))
# Space: O(N)
#

from collections import Counter, defaultdict
from functools import partial

# Time:  O(E * sqrt(V))
# Space: O(V)
# Source code from http://code.activestate.com/recipes/123641-hopcroft-karp-bipartite-matching/
# Hopcroft-Karp bipartite max-cardinality matching and max independent set
# David Eppstein, UC Irvine, 27 Apr 2002
def bipartiteMatch(graph):
    '''Find maximum cardinality matching of a bipartite graph (U,V,E).
    The input format is a dictionary mapping members of U to a list
    of their neighbors in V.  The output is a triple (M,A,B) where M is a
    dictionary mapping members of V to their matches in U, A is the part
    of the maximum independent set in U, and B is the part of the MIS in V.
    The same object may occur in both U and V, and is treated as two
    distinct vertices if this happens.'''
    
    # initialize greedy matching (redundant, but faster than full search)
    matching = {}
    for u in graph:
        for v in graph[u]:
            if v not in matching:
                matching[v] = u
                break
    
    while 1:
        # structure residual graph into layers
        # pred[u] gives the neighbor in the previous layer for u in U
        # preds[v] gives a list of neighbors in the previous layer for v in V
        # unmatched gives a list of unmatched vertices in final layer of V,
        # and is also used as a flag value for pred[u] when u is in the first layer
        preds = {}
        unmatched = []
        pred = dict([(u,unmatched) for u in graph])
        for v in matching:
            del pred[matching[v]]
        layer = list(pred)
        
        # repeatedly extend layering structure by another pair of layers
        while layer and not unmatched:
            newLayer = {}
            for u in layer:
                for v in graph[u]:
                    if v not in preds:
                        newLayer.setdefault(v,[]).append(u)
            layer = []
            for v in newLayer:
                preds[v] = newLayer[v]
                if v in matching:
                    layer.append(matching[v])
                    pred[matching[v]] = v
                else:
                    unmatched.append(v)
        
        # did we finish layering without finding any alternating paths?
        if not unmatched:
            unlayered = {}
            for u in graph:
                for v in graph[u]:
                    if v not in preds:
                        unlayered[v] = None
            return (matching,list(pred),list(unlayered))

        # recursively search backward through layers to find alternating paths
        # recursion returns true if found path, false otherwise
        def recurse(v):
            if v in preds:
                L = preds[v]
                del preds[v]
                for u in L:
                    if u in pred:
                        pu = pred[u]
                        del pred[u]
                        if pu is unmatched or recurse(pu):
                            matching[v] = u
                            return 1
            return 0
        
        def recurse_iter(v):
            def divide(v):
                if v not in preds:
                    return
                L = preds[v]
                del preds[v]
                for u in L :
                    if u in pred and pred[u] is unmatched:  # early return
                        del pred[u]
                        matching[v] = u
                        ret[0] = True
                        return
                stk.append(partial(conquer, v, iter(L)))

            def conquer(v, it):
                for u in it:
                    if u not in pred:
                        continue
                    pu = pred[u]
                    del pred[u]
                    stk.append(partial(postprocess, v, u, it))
                    stk.append(partial(divide, pu))
                    return

            def postprocess(v, u, it):
                if not ret[0]:
                    stk.append(partial(conquer, v, it))
                    return
                matching[v] = u

            ret, stk = [False], []
            stk.append(partial(divide, v))
            while stk:
                stk.pop()()
            return ret[0]

        for v in unmatched: recurse_iter(v)

def indicium():
    N, K = map(int, raw_input().strip().split())
    if K == N+1 or K == N**2-1 or (N == 3 and K in (5, 7)):
        return "IMPOSSIBLE"
    result, remain = [[int(i == j) for j in xrange(N)] for i in xrange(N)], K-N
    for i in reversed(xrange(N)):
        d = min(remain, N-1)
        result[i][i] += d
        remain -= d
    if 1 == result[-2][-2] < result[-1][-1]:  # 1, ..., 1, 2+ is invalid, make it a, b, c form
        result[-2][-2] += 1
        result[-1][-1] -= 1
    elif result[0][0] < result[1][1] == N:  # (N-1)-, N, ..., N is invalid, make it a, b, c form
        result[0][0] += 1
        result[1][1] -= 1
    count, numbers = Counter(result[i][i] for i in xrange(N)), range(1, N+1)
    numbers.sort(key=lambda x: N-count[x]) 
    for d in numbers:  # fill numbers greedily
        E = defaultdict(list)
        for i in xrange(N):
            for j in xrange(N):
                 if not result[i][j] and result[i][i] != d and result[j][j] != d:
                       E[j].append(i)
        M, _, _ = bipartiteMatch(E)  # make sure Latin square properties, Time: O(N^2 * sqrt(N))
        for i in xrange(N):
            if i in M:
                result[i][M[i]] = d
    return "POSSIBLE\n{}".format("\n".join(map(lambda x: " ".join(map(str, x)), result)))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, indicium())
