# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 3 - Problem B. Thermometers
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff7e/000000000037776b
#
# Time:  O(N^2)
# Space: O(1)
#

def getX(X, K, N, i):
    assert(-1 <= i <= 2*N)
    return X[i%N]+(i//N)*K

def greedy(K, N, X, i):
    # init curr with 0, and assumed that it starts at curr+v with v in range of (X[i], X[i+1])
    result, curr, left, right = 0, 0, getX(X, K, N, i), getX(X, K, N, i+1)
    for j in xrange(i+1, i+1+N):
        curr = 2*getX(X, K, N, j)-curr
        if not (j-(i+1))%2:  # X[j] < curr-v < X[j+1]
            left = max(left, curr-getX(X, K, N, j+1))
        else:  # X[j] < curr+v < X[j+1]
            right = min(right, getX(X, K, N, j+1)-curr)
        if left >= right:
            break
        result += 1
    return result, curr, left, right

def thermometers():
    K, N = map(int, raw_input().strip().split())
    X, T = [map(int, raw_input().strip().split()) for _ in xrange(2)]
    result, curr, left, right = greedy(K, N, X, -1)
    if result == N:
        assert(left < right)
        if not (N-1)%2:  # the last step is curr-v
            if 2*left < (curr-K) and (curr-K) < 2*right:  # curr-v == v+K, => v = (curr-K)/2 and left < v < right
                return N
        else:  # the last step is curr+v
            if not (curr-K):  # curr+v == v+K, => curr-K == 0 and left < right
                return N
    result = N+(N//2)
    for i in xrange(N):
        extra, j = 0, i
        while j < i+N:
            extra += 1
            j += greedy(K, N, X, j%N)[0]
        result = min(result, N+extra)
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, thermometers())
