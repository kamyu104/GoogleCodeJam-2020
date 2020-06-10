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
    i, j = len(S1), len(S2)
    result = []
    while i or j:
        if i and dp[i][j] == dp[i-1][j]+1:  # delete
            if mid:
                mid -= 1
            else:
                result.append(S1[i-1])
            i -= 1
        elif j and dp[i][j] == dp[i][j-1]+1:  # insert
            if mid:
                mid -= 1
                result.append(S2[j-1])
            j -= 1
        elif i and j and dp[i][j] == dp[i-1][j-1]+(S1[i-1] != S2[j-1]):
            if S1[i-1] == S2[j-1]:  # same
                result.append(S1[i-1])
            else:  # replace
                if mid:
                    mid -= 1
                    result.append(S2[j-1])
                else:
                    result.append(S1[i-1])
            i -= 1
            j -= 1
        else:
            assert(False)
    return "".join(reversed(result))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, naming_compromise())
