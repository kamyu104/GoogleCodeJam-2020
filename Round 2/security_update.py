# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 2 - Problem B. Security Update
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ffb9/000000000033871f
#
# Time:  O(ClogC + D)
# Space: O(C)
#

def security_update():
    C, D = map(int, raw_input().strip().split())
    T_R = map(int, raw_input().strip().split())
    T, R = [], []
    for i, x in enumerate(T_R, 1):
        if x > 0:
            T.append((x, i))
        elif x < 0:
            R.append((-x, i)) 
    resolved_T, last_merged = {0:0}, (0, 0, 0)
    R.sort(), T.sort()
    i, j = 0, 0
    while i != len(R) or j != len(T):
        if j == len(T) or (i != len(R) and R[i][0] <= len(resolved_T)):
            last_merged = (last_merged[0] if R[i][0] == last_merged[1] else last_merged[0]+1, R[i][0], R[i][1])
            resolved_T[R[i][1]] = last_merged[0]
            i += 1
        else:
            last_merged = (T[j][0], last_merged[1] if T[j][0] == last_merged[0] else len(resolved_T), T[j][1])
            resolved_T[T[j][1]] = last_merged[0]
            j += 1
    result = []
    for _ in xrange(D):
        U, V = map(int, raw_input().strip().split())
        result.append(max(abs(resolved_T[U-1]-resolved_T[V-1]), 1))
    return " ".join(map(str, result))
    
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, security_update())
