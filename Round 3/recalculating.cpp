// Copyright (c) 2020 kamyu. All rights reserved.

/*
 * Google Code Jam 2020 Round 3 - Problem D. Recalculating
 * https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff7e/00000000003775e9
 *
 * Time:  O(N^2 * logN)
 * Space: O(N^2)
 *
 */

#include<bits/stdc++.h>

using namespace std;

using Groups = unordered_map<int64_t, vector<tuple<int64_t, int64_t, int64_t, int64_t>>>;
using Points = vector<array<int64_t, 2>>;

static const int64_t MOD = 1e9 + 7;
static const int64_t P = 113;

uint64_t pow(uint64_t a, uint64_t b, uint64_t m) {
    a %= m;
    uint64_t result = 1;
    while (b) {
        if (b & 1) {
            result = (result * a) % m;
        }
        a = (a * a) % m;
        b >>= 1;
    }
    return result;
}

static unordered_map<uint64_t, uint64_t> lookup;
int64_t exp_(uint64_t x) {
    if (!lookup.count(x)) {
        lookup[x] = pow(P, x, MOD);
    }
    return lookup[x];
}

uint64_t gcd(uint64_t a, uint64_t b) {
    while (b != 0) {
        const auto tmp = b;
        b = a % b;
        a = tmp;
    }
    return a;
}

pair<uint64_t, Groups> group_rects(const Points& points, int64_t D) {
    unordered_set<int64_t> x_set, y_set;
    for (auto& p : points) {
        x_set.emplace(p[0] - D);
        x_set.emplace(p[0] + D);
        y_set.emplace(p[1] - D);
        y_set.emplace(p[1] + D);
    }
    vector<int64_t> xs(cbegin(x_set), cend(x_set)), ys(cbegin(y_set), cend(y_set));
    sort(begin(xs), end(xs)), sort(begin(ys), end(ys));
    Groups groups;
    uint64_t total = 0;
    for (int j = 0; j < ys.size() - 1; ++j) {
        int64_t rolling_hash = 0;
        deque<int> dq;
        int left = 0, right = 0;
        for (int i = 0; i < xs.size() - 1; ++i) {
            for (; right < points.size() && points[right][0] <= xs[i] + D; ++right) {
                if (ys[j + 1] - D <= points[right][1] &&  points[right][1] <= ys[j] + D) {
                    if (!dq.empty()) {
                        auto a = dq.back();
                        auto x = ((points[right][0] - points[a][0]) % MOD + MOD) % MOD;
                        auto y = ((points[right][1] - points[a][1]) % MOD + MOD) % MOD;
                        rolling_hash = (rolling_hash * P * P + (x * P + y)) % MOD;
                    }
                    dq.emplace_back(right);
                }
            }
            for (; left < points.size() && points[left][0] < xs[i + 1] - D; ++left) {
                if (ys[j + 1] - D <= points[left][1] && points[left][1] <= ys[j] + D) {
                    auto a = dq.front(); dq.pop_front();
                    if (dq.size() >= 1) {
                        auto b = dq.front();
                        auto x = ((points[b][0] - points[a][0]) % MOD + MOD) % MOD;
                        auto y = ((points[b][1] - points[a][1]) % MOD + MOD) % MOD;
                        auto delta = ((x * P + y) * exp_(2 * (dq.size() - 1))) % MOD;
                        rolling_hash = ((rolling_hash - delta) % MOD + MOD) % MOD;
                    }
                }
            }
            if (dq.empty()) {
                continue;
            }
            // the rectangle is fully covered by ordered repair centers in dq,
            // normalized by shift to the first repair center
            int64_t x0 = points[dq.front()][0] - (xs[i + 1] - D), y0 = points[dq.front()][1] - (ys[j + 1] - D);
            int64_t x1 = points[dq.front()][0] - (xs[i] - D), y1 = points[dq.front()][1] - (ys[j] - D);
            total += (x1 - x0) * (y1 - y0);
            groups[rolling_hash].emplace_back(x0, y0, x1, y1);
        }
    }
    return {total, groups};
}

uint64_t calc_unique_area(const Groups& groups) {
    using Event = tuple<int64_t, int64_t, int64_t, int64_t>;
    int64_t unique = 0;
    for (const auto& kvp : groups) {
        vector<Event> intervals;
        for (const auto& rect : kvp.second) {
            int64_t x0, y0, x1, y1;
            tie(x0, y0, x1, y1) = rect;
            intervals.emplace_back(x0, y0, y1, +1);
            intervals.emplace_back(x1, y0, y1, -1);
        }
        sort(begin(intervals), end(intervals));
        unordered_set<int64_t> y_set;
        for (const auto& interval : intervals) {
            int64_t x, y0, y1, v;
            tie(x, y0, y1, v) = interval;
            y_set.emplace(y0);
            y_set.emplace(y1);
        }
        vector<int64_t> ys(cbegin(y_set), cend(y_set));
        sort(begin(ys), end(ys));
        unordered_map<int, int> height_to_idx;
        for (int i = 0; i < ys.size(); ++i) {
            height_to_idx[ys[i]] = i;
        }
        using Node = array<int64_t, 3>;
        vector<Node> tree(2 * (ys.size() - 1));
        auto query = [&](int x) {
            int N = tree.size() / 2;
            if (x >= N) {  // leaf node
                for (int i = 0; i < 2; ++i) {
                    tree[x][i] = (i - tree[x][2] == 0) ? ys[(x - N) + 1] - ys[(x - N)] : 0;
                }
            } else {
                for (int i = 0; i < 2; ++i) {
                    tree[x][i] = (i - tree[x][2] >= 0) ? tree[2 * x][i - tree[x][2]] + tree[2 * x + 1][i - tree[x][2]] : 0;
                }
            }
        };
        auto pull = [&](int x) {
            for (; x; x /= 2) {
                query(x);
            }
        };
        auto update = [&](int l, int r, int v) {
            int N = tree.size() / 2;
            l += N;
            r += N;
            int l0 = l, r0 = r;
            for (; l <= r; l /= 2, r /= 2) {
                if (l & 1) {
                    tree[l][2] += v;
                    query(l);
                    ++l;
                }
                if ((r & 1) == 0) {
                    tree[r][2] += v;
                    query(r);
                    --r;
                }
            }
            pull(l0), pull(r0);
        };
        for (int i = tree.size() - 1; i; --i) {
            query(i);
        }
        for (int i = 0; i < intervals.size() - 1; ++i) {
            int64_t x, y0, y1, v;
            tie(x, y0, y1, v) = intervals[i];
            update(height_to_idx[y0], height_to_idx[y1] - 1, v);
            unique += (get<0>(intervals[i + 1]) - x) * tree[1][1];
        }
    }
    return unique;
}

string recalculating() {
    int N; int64_t D;
    cin >> N >> D;
    Points points;
    for (int i = 0; i < N; ++i) {
        int64_t x, y;
        cin >> x >> y;
        points.push_back({x + y, x - y});
    }
    sort(begin(points), end(points));
    uint64_t total;
    Groups groups;
    tie(total, groups) = group_rects(points, D);
    const auto& unique = calc_unique_area(groups);
    const auto& g = gcd(unique, total);
    return to_string(unique / g) + " " + to_string(total / g);
}

int main() {
    ios_base::sync_with_stdio(false), cin.tie(nullptr);
    int T;
    cin >> T;
    for (int test = 1; test <= T; ++test) {
        cout << "Case #" << test << ": " << recalculating() << '\n';
    }
    return 0;
}