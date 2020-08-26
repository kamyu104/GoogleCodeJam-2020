from random import shuffle, randint

T = 10000
print T
for _ in xrange(T):
    N = randint(4, 50)
    # N = 10**5
    print N
    tiles = range(1, N+1)
    shuffle(tiles)
    cells = range(1, N+1)
    shuffle(cells)
    for i in xrange(N):
        print tiles[i], cells[i]
