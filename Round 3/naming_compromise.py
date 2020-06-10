# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Round 3-Problem A. Naming Compromise
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff7e/00000000003774db
#
# Time:  O(C * J)
# Space: O(C * J)
#

def naming_compromise():
    S1, S2 = raw_input().strip().split()
    dp = [[float("inf") for _ in xrange(len(S2)+1)] for _ in xrange(len(S1)+1)]
    dp[0][0] = 0
    for i in xrange(len(S1)+1):
        for j in xrange(len(S2)+1):
            if i:
                dp[i][j] = min(dp[i][j], dp[i-1][j]+1)
            if j:
                dp[i][j] = min(dp[i][j], dp[i][j-1]+1)
            if i and j:
                dp[i][j] = min(dp[i][j], dp[i-1][j-1]+(S1[i-1] != S2[j-1]))
    mid = dp[-1][-1]//2
    result, i, j = [], len(S1), len(S2)
    while (i or j) and mid:
        if i and dp[i][j] == dp[i-1][j]+1:  # delete
            mid -= 1
            i -= 1
        elif j and dp[i][j] == dp[i][j-1]+1:  # insert
            mid -= 1
            result.append(S2[j-1])
            j -= 1
        elif i and j and dp[i][j] == dp[i-1][j-1]+(S1[i-1] != S2[j-1]):
            mid -= (S1[i-1] != S2[j-1])
            if S1[i-1] == S2[j-1]:  # same
                result.append(S2[i-1])
            else:  # replace
                result.append(S2[j-1])
            i -= 1
            j -= 1
        else:
            assert(False)
    return S1[:i] + "".join(reversed(result))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, naming_compromise())
