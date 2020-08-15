# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Virtual World Finals - Problem E. Replace All
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff31/00000000003b532b
#
# Time:  O(A^3)
# Space: O(A^2)
#

from collections import defaultdict
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

    
def floydWarshall(adj):  # Time:  O(N^3)
    for k in xrange(len(adj[0])): 
        for i in xrange(len(adj)): 
            for j in xrange((len(adj[i]))): 
                if adj[i][k] and adj[k][j]:
                    adj[i][j] = 1

def char_to_num(c):
    if c.isdigit():
        return int(c)
    if c.islower():
        return (ord(c)-ord('a')) + 10
    if c.isupper():
        return (ord(c)-ord('A')) + 36

def replace_all():
    S, N = raw_input().strip().split()
    has_alpha = [0]*ALPHABET_SIZE
    for c in S:
        has_alpha[char_to_num(c)] = 1
    adj = [[int(i == j) for j in xrange(ALPHABET_SIZE)] for i in xrange(ALPHABET_SIZE)]
    for A, B in raw_input().strip().split():
        adj[char_to_num(A)][char_to_num(B)] = 1
    floydWarshall(adj)  # Time: O(A^3)

    sources, sinks = [], [i for i in xrange(ALPHABET_SIZE) if not has_alpha[i]]
    for i in xrange(ALPHABET_SIZE):
        if any(adj[i][j] and adj[j][i] for j in xrange(i)):
            continue  # not a root
        if any(not has_alpha[j] for j in xrange(i, ALPHABET_SIZE) if adj[i][j] and adj[j][i]):
            continue  # not filled
        if not any(adj[i][j] for j in xrange(ALPHABET_SIZE) if i != j):
            continue  # no edge
        sources.append(i)
        sinks.append(i)
    E = defaultdict(list)
    for i in xrange(len(sources)):
        for j in xrange(len(sinks)):
            if sources[i] != sinks[j] and adj[sources[i]][sinks[j]]:
                E[j].append(i)
    return sum(has_alpha)-(len(sources)-len(bipartiteMatch(E)[0]))  # Time: O(A^2 * sqrt(A))

ALPHABET_SIZE = 62
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, replace_all())
