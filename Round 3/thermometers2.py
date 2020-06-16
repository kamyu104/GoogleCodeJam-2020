# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 3 - Problem B. Thermometers
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff7e/000000000037776b
#
# Time:  O(N^2)
# Space: O(1)
#

def check(D, z):
    for j in xrange(len(D)):  # check if z/2 could be mirrored through all segments
        if 2*D[j] <= z:  # multiply D[j] by 2 to avoid float operation of z
            return False
        z = 2*D[j]-z
    return True

def greedy(K, N, D, i):
    result, left, right = 0, 0, D[i%len(D)]
    for j in xrange(i+1, i+1+N):
        left, right = min(D[(j-1)%len(D)]-right, D[j%len(D)]), min(D[(j-1)%len(D)]-left, D[j%len(D)])
        if left >= right:  # empty interval
            break
        result += 1
    return result

def thermometers():
    K, N = map(int, raw_input().strip().split())
    X, T = [map(int, raw_input().strip().split()) for _ in xrange(2)]
    D = [(X[(i+1)]-X[i])%K for i in xrange(len(X)-1)]
    D.append(K-sum(D))  # handle case N = 0, 1 (although there is no such test case as official said)
    z = reduce(lambda x, y: y-x, D)
    if not (N-1)%2:
        if check(D, z):
            return N  # a ring
    else:
        if not z and greedy(K, N, D, 0) == N:
            return N  # a ring
    result = N+(N//2)  # no adjacent segments with 2 thermometers
    for i in xrange(N):
        chain, j = 0, i
        while j < i+N:
            j += greedy(K, N, D, j%N)
            chain += 1
        result = min(result, N+chain)
    return result  # chains

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, thermometers())
