// Copyright (c) 2020 kamyu. All rights reserved.

/*
 * Google Code Jam 2020 Round 3 - Problem D. Recalculating
 * https://codingcompetitions.withgoogle.com/codejam/round/000000000019ff7e/00000000003775e9
 *
 * Time:  O(N^2 * logN)
 * Space: O(N^2)
 *
 */

#include <iostream>
#include <functional>
#include <array>
#include <string>
#include <vector>
#include <deque>
#include <utility>
#include <tuple>
#include <unordered_set>
#include <unordered_map>
#include <algorithm>

using std::ios_base;
using std::cin;
using std::cout;
using std::endl;
using std::function;
using std::array;
using std::string;
using std::to_string;
using std::vector;
using std::deque;
using std::pair;
using std::tuple;
using std::tie;
using std::get;
using std::unordered_set;
using std::unordered_map;
using std::sort;

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
        int N,
        const function<void(vector<T> *, int)>& query_fn,
        const function<void(T *, int64_t)>& update_fn)
      : N_(N),
        tree_(2 * N),
        query_fn_(query_fn),
        update_fn_(update_fn) {
        for (int i = tree_.size() - 1; i >= 1; --i) {
            query_fn_(&tree_, i);
        }
    }

    void update(int L, int R, int val) {
        L += N_; R += N_;
        int L0 = L, R0 = R;
        for (; L <= R; L >>= 1, R >>= 1) {
            if ((L & 1) == 1) {
                apply(L++, val);
            }
            if ((R & 1) == 0) {
                apply(R--, val);
            }
        }
        pull(L0); pull(R0);
    }

    T query() {
        return tree_[1];
    }

 private:
    void apply(int x, int val) {
        update_fn_(&tree_[x], val);
        query_fn_(&tree_, x);
    }

    void pull(int x) {
        while (x > 1) {
            x >>= 1;
            query_fn_(&tree_, x);
        }
    }

    int N_;
    vector<T> tree_;
    const function<void(vector<T> *, int)> query_fn_;
    const function<void(T *, int64_t)> update_fn_;
};

Groups group_rects(const Points& points, int64_t D) {
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
            groups[rolling_hash].emplace_back(x0, y0, x1, y1);
        }
    }
    return groups;
}

pair<uint64_t, uint64_t> calc_unique_area(const Groups& groups) {
    using Event = tuple<int64_t, int64_t, int64_t, int64_t>;
    int64_t unique = 0, total = 0;
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
        // Node: [sum_len_of_covered, len_of_1_or_up_covered, len_of_2_or_up_covered, len_of_0_or_up_covered, count_of_covered]
        using Node = array<int64_t, 5>;  // define customized operations of segment tree
        const auto& query = [&ys](vector<Node> *tree, int x) {
            int N = tree->size() / 2;
            if (x >= N) {  // leaf node
                (*tree)[x][3] = ys[(x - N) + 1] - ys[(x - N)];
                (*tree)[x][0] = (*tree)[x][3] * (*tree)[x][4];
                for (int i = 1; i <= 2; ++i) {
                    (*tree)[x][i] = (i - (*tree)[x][4] > 0) ? 0 : (*tree)[x][3];
                }
            } else {
                (*tree)[x][3] = (*tree)[2 * x][3] + (*tree)[2 * x + 1][3];
                (*tree)[x][0] = (*tree)[x][3] * (*tree)[x][4] + (*tree)[2 * x][0] + (*tree)[2 * x + 1][0];
                for (int i = 1; i <= 2; ++i) {
                    (*tree)[x][i] = (i - (*tree)[x][4] > 0) ? (*tree)[2 * x][i - (*tree)[x][4]] + (*tree)[2 * x + 1][i - (*tree)[x][4]] : (*tree)[x][3];
                }
            }
        };
        const auto& update = [](Node *x, int64_t val) {
            (*x)[4] += val;
        };
        SegmentTree<Node> segment_tree(ys.size() - 1, query, update);  // init segment tree with customized operations
        for (int i = 0; i < intervals.size() - 1; ++i) {
            int64_t x, y0, y1, v;
            tie(x, y0, y1, v) = intervals[i];
            segment_tree.update(height_to_idx[y0], height_to_idx[y1] - 1, v);  // at most O(N^2) intervals, total time: O(N^2 * logN)
            unique += (get<0>(intervals[i + 1]) - x) * (segment_tree.query()[1] - segment_tree.query()[2]);
            total += (get<0>(intervals[i + 1]) - x) * segment_tree.query()[0];
        }
    }
    return {unique, total};
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
    const auto& groups = group_rects(points, D);
    uint64_t unique, total;
    tie(unique, total) = calc_unique_area(groups);
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
