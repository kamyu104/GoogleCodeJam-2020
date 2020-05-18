from random import randint

T = 100
print T
K, Q, MAX_L, MAX_R, MAX_P = 10, 10, 10**6, 10**6, 10**6
for _ in xrange(T):
    PRG, l, r = [], K//2, K//2
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
    for _ in xrange(Q):
        while True:
            a, b = randint(1, K), randint(1, K)
            if (a, b) not in lookup:
                lookup.add((a, b))
                break
        S.append(a)
        E.append(b)
    print K, Q
    print "".join(PRG)
    print " ".join(map(str, L))
    print " ".join(map(str, R))
    print " ".join(map(str, P))
    print " ".join(map(str, S))
    print " ".join(map(str, E))