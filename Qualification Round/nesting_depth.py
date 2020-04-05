# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2020 Qualification Round - Problem B. Nesting Depth
# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd27/0000000000209a9f
#
# Time:  O(N)
# Space: O(1)
#

def nesting_depth():
    S = map(int, list(raw_input().strip()))
    result = []
    for i in xrange(len(S)):
        count = S[i]-(S[i-1] if i-1 >= 0 else 0)
        if count > 0:
            result.append("("*count)
        elif count < 0:
            result.append(")"*-count)
        result.append(str(S[i]))
    if S[-1]:
        result.append(")"*S[-1])
    return "".join(result)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, nesting_depth())
