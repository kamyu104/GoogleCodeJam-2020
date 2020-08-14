# [GoogleCodeJam 2020](https://codingcompetitions.withgoogle.com/codejam/archive/2020) ![Language](https://img.shields.io/badge/language-Python-orange.svg) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE) ![Progress](https://img.shields.io/badge/progress-23%20%2F%2027-ff69b4.svg)

Python solutions of Google Code Jam 2020. Solution begins with `*` means it will get TLE in the largest data set (total computation amount > `10^8`, which is not friendly for Python to solve in 5 ~ 15 seconds). A problem was marked as `Very Hard` means that it was an unsolved problem during the contest and may not be that difficult.

* [Code Jam 2019](https://github.com/kamyu104/GoogleCodeJam-2019)
* [Qualification Round](https://github.com/kamyu104/GoogleCodeJam-2020#qualification-round)
* [Round 1A](https://github.com/kamyu104/GoogleCodeJam-2020#round-1a)
* [Round 1B](https://github.com/kamyu104/GoogleCodeJam-2020#round-1b)
* [Round 1C](https://github.com/kamyu104/GoogleCodeJam-2020#round-1c)
* [Round 2](https://github.com/kamyu104/GoogleCodeJam-2020#round-2)
* [Round 3](https://github.com/kamyu104/GoogleCodeJam-2020#round-3)
* [Virtual World Finals](https://github.com/kamyu104/GoogleCodeJam-2020#virtual-world-finals)
   
## Qualification Round
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|A| [Vestigium](https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd27/000000000020993c)| [Python](./Qualification%20Round/vestigium.py)| _O(N^2)_ | _O(N)_ | Easy | | Math |
|B| [Nesting Depth](https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd27/0000000000209a9f)| [Python](./Qualification%20Round/nesting_depth.py)| _O(N)_ | _O(1)_ | Easy | | String |
|C| [Parenting Partnering Returns](https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd27/000000000020bdf9)| [Python](./Qualification%20Round/parenting_partnering_returns.py)| _O(NlogN)_ | _O(1)_ | Easy | | Greedy |
|D| [ESAb ATAd](https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd27/0000000000209a9e)| [Python](./Qualification%20Round/esab_atad.py) |  _O(B^2/4)_ | _O(B)_ | Medium | | Bit Manipulation |
|E| [Indicium](https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd27/0000000000209aa0)| [Python](./Qualification%20Round/indicium.py) |  _O(N^3 * sqrt(N))_ | _O(N)_ | Hard | | Bipartite Matching, Greedy |

## Round 1A
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|A| [Pattern Matching](https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd74/00000000002b3034)| [Python](./Round%201A/pattern_matching.py)| _O(N * P)_ | _O(P)_ | Easy | | String |
|B| [Pascal Walk](https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd74/00000000002b1353)| [Python](./Round%201A/pascal_walk.py) | _O(logN^2)_ | _O(logN)_ | Medium | | Math, Greedy, Bit Manipulation |
|C| [Square Dance](https://codingcompetitions.withgoogle.com/codejam/round/000000000019fd74/00000000002b1355)| [Python](./Round%201A/square_dance.py)| _O(R * C)_ | _O(R * C)_ | Hard | | Simulation, BFS, Linked List |

## Round 1B
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|A| [Expogo](https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b62)| [Python](./Round%201B/expogo.py) [Python](./Round%201B/expogo2.py) | _O(log(\|X\| + \|Y\|))_ | _O(1)_ | Medium | Variant of [Pogo](https://code.google.com/codejam/contest/2437488/dashboard#s=p1) | Invariant, Greedy
|B| [Blindfolded Bullseye](https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b63)| [Python](./Round%201B/blindfolded_bullseye2.py) | _O(128)_ | _O(1)_ | Medium || Probability, Binary Search, Geometry
|C| [Join the Ranks](https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b64)| [Python](./Round%201B/join_the_ranks5.py) | _O(R * S)_ | _O(1)_ | Hard | One-Liner | Invariant, Sort

## Round 1C
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|A| [Overexcited Fan](https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef4/0000000000317409)| [Python](./Round%201C/overexcited_fan.py) | _O(M)_ | _O(1)_ | Easy || Simulation, Math
|B| [Overrandomized](https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef4/00000000003179a1)| [Python](./Round%201C/overrandomized.py) | _O(L * U)_ | _O(1)_ | Easy || Probability
|C| [Oversized Pancake Choppers](https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef4/00000000003172d1)| [PyPy](./Round%201C/oversized_pancake_choppers.py) [Python](./Round%201C/oversized_pancake_choppers2.py) [Python](./Round%201C/oversized_pancake_choppers3.py) | _O(N * DlogD)_ | _O(D * N)_ | Hard || Sort, Hash Table, Euclidean Algorithm, Binary Search, Greedy, Bucket, LCM

## Round 2
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|A| [Incremental House of Pancakes](https://codingcompetitions.withgoogle.com/codejam/round/000000000019ffb9/00000000003384ea)| [Python](./Round%202/incremental_house_of_pancakes.py) [Python](./Round%202/incremental_house_of_pancakes2.py)| _O(log(L + R))_ | _O(1)_ | Easy || Binary Search, Math
|B| [Security Update](https://codingcompetitions.withgoogle.com/codejam/round/000000000019ffb9/000000000033871f)| [Python](./Round%202/security_update.py) | _O(ClogC + D)_ | _O(C)_ | Medium || Sort
|C| [Wormhoe in One](https://codingcompetitions.withgoogle.com/codejam/round/000000000019ffb9/00000000003386d0)| [Python](./Round%202/wormhole_in_one.py) | _O(N^2)_ | _O(N^2)_ | Medium || Math
|D| [Emacs++](https://codingcompetitions.withgoogle.com/codejam/round/000000000019ffb9/000000000033893b)| [PyPy*](./Round%202/emacs++.py) [PyPy](./Round%202/emacs++2_concise.py) | _O(KlogK + QlogK)_ | _O(KlogK)_ | Hard || Tree, Lazy Construction, Middle Line, Dijkstra's Algorithm, Iterative Recursion, LCA, Prefix Sum, Tree Ancestors (Binary Jump)

## Round 3
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|A| [Naming Compromise](https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff7e/00000000003774db)| [Python](./Round%203/naming_compromise.py) | _O(C * J)_ | _O(C * J)_ | Easy | | DP, Edit Distance
|B| [Thermometers](https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff7e/000000000037776b)| [Python](./Round%203/thermometers.py) [Python](./Round%203/thermometers2.py) |  _O(N^2)_ | _O(1)_ | Hard || Greedy, Mirror
|C| [Pen Testing](https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff7e/0000000000377630)| [PyPy](./Round%203/pen_testing_heuristic.py)<br>[Python](./Round%203/pen_testing.py)<br>[PyPy](./Round%203/pen_testing2_heuristic.py)<br>[Python](./Round%203/pen_testing2.py) | _O(T * N^2 + N * S)_ | _O(N * (T + S))_ | Hard || Heuristic, Memoization, Probability
|D| [Recalculating](https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff7e/00000000003775e9)| [*PyPy](./Round%203/recalculating.py)<br>[C++](./Round%203/recalculating.cpp)<br>[*PyPy](./Round%203/recalculating2.py)<br>[C++](./Round%203/recalculating2.cpp) | _O(N^2 * logN)_ | _O(N^2)_ | Hard || Coordinate Rotation, Sliding Window, Rolling Hash, Rabin-Karp Algorithm, Line Sweep, Coordinate Compression, Segment Tree

## Virtual World Finals
You can relive the magic of the 2020 Code Jam Virtual World Finals by watching the [Live Stream Recording](https://codingcompetitionsonair.withgoogle.com/events/code-jam-2020-world-finals?fbclid=IwAR2eaJii-Qe-tLyG170fCN715qXhtWYdgmqOALF6Z4WqQw48oMtZ305zvfA) of the competition, problem explanations, interviews with Google and Code Jam engineers, and announcement of winners.

| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|A| [Pack the Slopes](https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff31/00000000003b4f31)||||||
|B| [Adjacent and Consecutive](https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff31/00000000003b53ce)||||||
|C| [Hexacoin Jam](https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff31/00000000003b4bc5)||||||
|D| [Musical Cords](https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff31/00000000003b532b)| [PyPy](./Virtual%20World%20Finals/musical_cords.py) | _O(NlogN + N * K)_ | _O(N)_ | Very Hard || Geometry, Trigonometric Functions, Two Pointers, Binary Search, Quick Select, Sort
|E| [Replace All](https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff31/00000000003b4bc4)||||||
