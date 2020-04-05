N = 50
cases = []
for i in xrange(2, N+1):
    for j in xrange(i, i*i+1):
        cases.append((i, j))
print len(cases)
for i, j  in cases:
    print i, j
