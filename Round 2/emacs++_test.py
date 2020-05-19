from random import randint

T = 200
print T
for i in xrange(T):
    if i == 0:
        K, Q, MAX_L, MAX_R, MAX_P = 100000, 100000, 1, 1, 1
    elif i == 100:
        K, Q, MAX_L, MAX_R, MAX_P = 100000, 100000, 10**6, 10**6, 10**6
    elif i%100 == 9:
        K, Q = 1000, 1000
    PRG, l, r = [], K//2, K//2
    if i%100 == 0:
        PRG.append('('*l + ')'*r)
    elif i%100 == 1:
        PRG.append('()'*l)
    else:
        while l or r:
            if l == 0 or (l < r and randint(0, 1)):
                PRG.append(')')
                r -= 1
            else:
                PRG.append('(')
                l -= 1
    L, R, P, S, E, lookup  = [], [], [], [], [], set()
    for _ in xrange(K):
        L.append(randint(1, MAX_L))
        R.append(randint(1, MAX_R))
        P.append(randint(1, MAX_P))
    for _ in xrange(min(K*(K-1), Q)):
        while True:
            a, b = randint(1, K), randint(1, K)
            if a != b and (a, b) not in lookup:
                lookup.add((a, b))
                break
        S.append(a)
        E.append(b)
    print K, len(S)
    print "".join(PRG)
    print " ".join(map(str, L))
    print " ".join(map(str, R))
    print " ".join(map(str, P))
    print " ".join(map(str, S))
    print " ".join(map(str, E))
