# [GoogleCodeJam 2020](https://codingcompetitions.withgoogle.com/codejam/archive/2020) ![Language](https://img.shields.io/badge/language-Python-orange.svg) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE) ![Progress](https://img.shields.io/badge/progress-11%20%2F%2011-ff69b4.svg)

Python solutions of Google Code Jam 2020. Solution begins with `*` means it will get TLE in the largest data set (total computation amount > `10^8`, which is not friendly for Python to solve in 5 ~ 15 seconds).

* [Code Jam 2019](https://github.com/kamyu104/GoogleCodeJam-2019)
* [Qualification Round](https://github.com/kamyu104/GoogleCodeJam-2020#qualification-round)
* [Round 1A](https://github.com/kamyu104/GoogleCodeJam-2020#round-1a)
* [Round 1B](https://github.com/kamyu104/GoogleCodeJam-2020#round-1b)

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
|A| [Expogo](https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b62)| [Python](./Round%201B/expogo.py) [Python](./Round%201B/expogo2.py) | _O(log(\|X\| + \|Y\|))_ | _O(1)_ | Medium | variant of [Pogo](https://code.google.com/codejam/contest/2437488/dashboard#s=p1) | Invariant, Greedy
|B| [Blindfolded Bullseye](https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b63)| [Python](./Round%201B/blindfolded_bullseye.py) | _O(156)_ | _O(1)_ | Medium || Probability, Binary Search, Geometry
|C| [Join the Ranks](https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b64)| [Python](./Round%201B/join_the_ranks.py) [Python](./Round%201B/join_the_ranks2.py)] | _O(R^2 * S^2)_ | _O(R * S)_ | Hard || Invariant, Sort
