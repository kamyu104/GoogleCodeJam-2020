# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 3 - Problem B. Thermometers
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff7e/000000000037776b
#
# Time:  O(N^2)
# Space: O(1)
#

def greedy(K, N, D, i):
    result, left, right = 0, 0, D[i%len(D)]
    for j in xrange(i+1, i+1+N):
        left, right = min(D[(j-1)%len(D)]-right, D[j%len(D)]), min(D[(j-1)%len(D)]-left, D[j%len(D)])
        if left >= right:  # empty interval
            break
        result += 1
    else:
        for j in reversed(xrange(i+1, i+1+N)):  # trace back to get the first interval
            left, right = D[(j-1)%len(D)]-right, D[(j-1)%len(D)]-left
    return result, left, right

def thermometers():
    K, N = map(int, raw_input().strip().split())
    X, T = [map(int, raw_input().strip().split()) for _ in xrange(2)]
    D = [(X[(i+1)]-X[i])%K for i in xrange(len(X)-1)]
    D.append(K-sum(D))
    result, left, right = greedy(K, N, D, 0)
    if result == N:
        assert(left < right)
        z = reduce(lambda x, y: y-x, D)
        if not (N-1)%2:
            if 2*left < z < 2*right:
                return N  # a ring
        else:
            if not z:
                return N  # a ring
    result = N+(N//2)  # no adjacent segments with 2 thermometers
    for i in xrange(N):
        chain, j = 0, i
        while j < i+N:
            j += greedy(K, N, D, j%N)[0]
            chain += 1
        result = min(result, N+chain)
    return result  # chains

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, thermometers())
