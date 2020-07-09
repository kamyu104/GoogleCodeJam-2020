// Copyright (c) 2020 kamyu. All rights reserved.

/*
 * Google Code Jam 2020 Round 3 - Problem D. Recalculating
 * https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff7e/00000000003775e9
 *
 * Time:  O(N^2 * logN)
 * Space: O(N^2)
 *
 * concise solution of recalculating.cpp
 *
 */

#include<bits/stdc++.h>

using namespace std;

using Groups = unordered_map<int64_t, vector<tuple<int64_t, int64_t, int64_t, int64_t>>>;
using Points = vector<array<int64_t, 2>>;

static const int64_t MOD = 1e9 + 7;
static const int64_t P = 113;

uint64_t gcd(uint64_t a, uint64_t b) {
    while (b != 0) {
        const auto tmp = b;
        b = a % b;
        a = tmp;
    }
    return a;
}

template <typename T>
class SegmentTree {
public:
    explicit SegmentTree(
        const vector<int64_t>& ys,
        const function<void(const vector<int64_t>&, vector<T> *, int)>& query_fn,
        const function<void(T *, int64_t)>& apply_fn)
      : tree_(2 * (ys.size() - 1)),
        ys_(ys),
        query_fn_(query_fn),
        apply_fn_(apply_fn)
    {
        for (int i = tree_.size() - 1; i >= 1; --i) {
            query_fn_(ys_, &tree_, i);
        }
    }

    void update(int L, int R, int h) {
        L += tree_.size() / 2; R += tree_.size() / 2;
        int L0 = L, R0 = R;
        for (; L <= R; L >>= 1, R >>= 1) {
            if ((L & 1) == 1) {
                apply_fn_(&tree_[L], h);
                query_fn_(ys_, &tree_, L++);
            }
            if ((R & 1) == 0) {
                apply_fn_(&tree_[R], h);
                query_fn_(ys_, &tree_, R--);
            }
        }
        pull(L0); pull(R0);
    }

    const T& query() {
        return tree_[1];
    }

private:
    void pull(int x) {
        while (x > 1) {
            x >>= 1;
            query_fn_(ys_, &tree_, x);
        }
    }

    vector<T> tree_;
    const vector<int64_t>& ys_;
    const function<void(const vector<int64_t>&, vector<T> *, int)>& query_fn_;
    const function<void(T *, int64_t)>& apply_fn_;
};

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
    vector<int64_t> exp(1, 1);
    while (exp.size() < points.size()) {
        exp.emplace_back(exp.back() * P * P % MOD);
    }
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
                        auto a = dq.back(), b = right;
                        auto x = ((points[b][0] - points[a][0]) % MOD + MOD) % MOD;
                        auto y = ((points[b][1] - points[a][1]) % MOD + MOD) % MOD;
                        auto delta = (x * P + y) % MOD;
                        rolling_hash = (rolling_hash * P * P + delta) % MOD;
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
                        auto delta = ((x * P + y) * exp[dq.size() - 1]) % MOD;
                        rolling_hash = ((rolling_hash - delta) % MOD + MOD) % MOD;
                    }
                }
            }
            if (dq.empty()) {
                continue;
            }
            // the rectangle is fully covered by ordered repair centers in dq,
            // normalized by being relative to the first repair center
            int64_t x0 = xs[i] - points[dq.front()][0], y0 = ys[j] - points[dq.front()][1];
            int64_t x1 = xs[i + 1] - points[dq.front()][0], y1 = ys[j + 1] - points[dq.front()][1];
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
        sort(begin(intervals), end(intervals));  // at most O(N^2) intervals, total time: O(N^2 * logN)
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

        using Node = array<int64_t, 3>;  // define customized operations of segment tree
        const auto& update = [](Node *x, int64_t val) {
            (*x)[2] += val;
        };
        const auto& query = [](const vector<int64_t>& ys, vector<Node> *tree, int x) {
            int N = tree->size() / 2;
            if (x >= N) {  // leaf node
                for (int i = 0; i < 2; ++i) {
                    (*tree)[x][i] = (i - (*tree)[x][2] == 0) ? ys[(x - N) + 1] - ys[(x - N)] : 0;
                }
            } else {
                for (int i = 0; i < 2; ++i) {
                    (*tree)[x][i] = (i - (*tree)[x][2] >= 0) ? (*tree)[2 * x][i - (*tree)[x][2]] + (*tree)[2 * x + 1][i - (*tree)[x][2]] : 0;
                }
            }
        };
        SegmentTree<Node> segment_tree(ys, query, update);  // init segment tree with customized operations
        for (int i = 0; i < intervals.size() - 1; ++i) {
            int64_t x, y0, y1, v;
            tie(x, y0, y1, v) = intervals[i];
            segment_tree.update(height_to_idx[y0], height_to_idx[y1] - 1, v);  // at most O(N^2) intervals, total time: O(N^2 * logN)
            unique += (get<0>(intervals[i + 1]) - x) * segment_tree.query()[1];
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
