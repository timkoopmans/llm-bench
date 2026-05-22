# Implementation Guide: paint-house-iv

## 1. Required Function Signatures

```python
class Solution:
    def minCost(self, n: int, cost: List[List[int]]) -> int:
```

## 2. Algorithm Steps

The key insight: process pairs of houses simultaneously — house `i` (from left) and house `n-1-i` (from right, its equidistant partner).

**DP State:** `dp[c1][c2]` = minimum cost to paint all processed pairs so far, where the left house of the current pair has color `c1` and the right house has color `c2`.

**Initialization:** Before any pair is processed, `dp` is a 3×3 matrix of `+infinity`.

**For each pair index `i` in range `n//2`:**
1. Left house index = `i`, right house index = `n-1-i`
2. Create new `next_dp[3][3]` initialized to `+infinity`
3. For each new left color `c1` in {0,1,2}:
   - For each new right color `c2` in {0,1,2}:
     - Skip if `c1 == c2` (equidistant constraint)
     - Compute `pair_cost = cost[i][c1] + cost[n-1-i][c2]`
     - For each previous left color `p1` in {0,1,2}:
       - For each previous right color `p2` in {0,1,2}:
         - Skip if `dp[p1][p2]` is infinity
         - Skip if `p1 == c1` (left adjacency: house i-1 and house i same color)
         - Skip if `p2 == c2` (right adjacency: house n-i and house n-1-i same color)
         - Update: `next_dp[c1][c2] = min(next_dp[c1][c2], dp[p1][p2] + pair_cost)`
4. Set `dp = next_dp`

**Base case for i=0:** There is no previous pair, so `dp` starts as all-infinity. Handle by seeding: before the loop, for pair 0, just fill valid `(c1 != c2)` entries directly with `cost[0][c1] + cost[n-1][c2]`.

**Answer:** `min` over all `dp[c1][c2]`.

**Simplified approach:** Initialize `dp` as all-infinity, then treat "no previous pair" as the base: when `i==0`, the transition has no predecessor constraint, so seed `dp[c1][c2] = cost[0][c1] + cost[n-1][c2]` for all `c1 != c2`, then loop from `i=1`.

## 3. Required Imports

```python
from typing import List
```
No numpy/scipy needed. Use `float('inf')` for infinity.

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| `n=2` | Only one pair; answer is min over `c1 != c2` of `cost[0][c1] + cost[1][c2]` |
| All costs equal | Any valid coloring works; ensure all constraint combos checked |
| `n=4` (example 1) | Two pairs; verify adjacency between pairs is enforced |

## 5. Common Pitfalls

- **Adjacency direction for right side:** Right houses are processed right-to-left (`n-1-i` decreases as `i` increases). The adjacency constraint is between house `n-1-i` (current right) and house `n-i` (previous right). In DP terms: new `c2` must differ from previous `p2`. Don't accidentally check the wrong side.
- **Equidistant ≠ adjacent:** `c1 != c2` is the equidistant constraint (not adjacency). Don't confuse the two; both must be enforced independently.
- **Off-by-one in right index:** Right house for pair `i` is `n-1-i`, not `n-i`. Double-check indexing.
- **Base case seeding:** Don't apply predecessor constraints when `i==0` — there is no previous pair. Seed separately before the transition loop.
- **Integer overflow:** Not a Python concern, but don't use `sys.maxsize` arithmetic carelessly; `float('inf')` is safer.

## 6. Suggested Private Helper Functions

- `_init_dp(cost, n)`: Seeds the 3×3 dp table for pair index 0, enforcing only `c1 != c2`.
- `_transition(dp, cost, i, n)`: Given current `dp`, returns `next_dp` for pair `i` enforcing all three constraints (equidistant + both adjacencies).