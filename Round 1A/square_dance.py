# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 1A - Problem C. Square Dance
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd74/00000000002b1355
#
# Time:  O(R * C)
# Space: O(R * C)
#

def neighbors(up, down, left, right, r, c):
    yield up[r][c], c
    yield down[r][c], c
    yield r, left[r][c]
    yield r, right[r][c]

def square_dance():
    R, C = map(int, raw_input().strip().split())
    S = [map(int, raw_input().strip().split()) for _ in xrange(R)]
    up = [[None]*C for _ in xrange(R)]
    down = [[None]*C for _ in xrange(R)]
    left = [[None]*C for _ in xrange(R)]
    right = [[None]*C for _ in xrange(R)]
    q, total = [], 0
    for r in xrange(R):
        for c in xrange(C):
            up[r][c] = r-1
            down[r][c] = r+1
            left[r][c] = c-1
            right[r][c] = c+1
            q.append((r, c))
            total += S[r][c]
    result = total
    while q:
        to_remove, new_q = [], []
        for r, c in q:
            neightbor_total, count = 0, 0
            for nr, nc in neighbors(up, down, left, right, r, c):
                if not (0 <= nr < R and 0 <= nc < C):
                    continue
                neightbor_total += S[nr][nc]
                count += 1
            if neightbor_total > S[r][c]*count:
                to_remove.append((r, c))
        if not to_remove:
            break
        lookup = set()
        for r, c in to_remove:
            lookup.add((r, c))
            total -= S[r][c]
        result += total
        for r, c in to_remove:
            for nr, nc in neighbors(up, down, left, right, r, c):
                if not (0 <= nr < R and 0 <= nc < C and (nr, nc) not in lookup):
                    continue
                lookup.add((nr, nc))
                new_q.append((nr, nc))
        for r, c in to_remove:
            if up[r][c] != -1:
                down[up[r][c]][c] = down[r][c]
            if down[r][c] != R:
                up[down[r][c]][c] = up[r][c]
            if left[r][c] != -1:
                right[r][left[r][c]] = right[r][c]
            if right[r][c] != C:
                left[r][right[r][c]] = left[r][c]
        q = new_q
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, square_dance())
