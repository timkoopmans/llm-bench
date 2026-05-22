# Implementation Guide: Maximum Amount of Money Robot Can Earn

## 1. Required Function Signatures

```python
class Solution:
    def maximumAmount(self, coins: List[List[int]]) -> int:
```

## 2. Algorithm Steps

Use 3D dynamic programming where the third dimension tracks **neutralizations remaining** (0, 1, or 2).

**State:** `dp[i][j][k]` = maximum coins reachable at cell `(i, j)` with `k` neutralizations still available.

**Transition:**
```
For each cell (i, j), for each k in {0, 1, 2}:
  best_prev = max(dp[i-1][j][k], dp[i][j-1][k])   # came from top or left
  
  # Option A: Don't neutralize this cell
  dp[i][j][k] = best_prev + coins[i][j]
  
  # Option B: Neutralize this cell (only if coins[i][j] < 0 and k >= 1)
  if k >= 1:
    best_prev_with_skip = max(dp[i-1][j][k-1], dp[i][j-1][k-1])
    dp[i][j][k] = max(dp[i][j][k], best_prev_with_skip + 0)
```

**Base case:** `dp[0][0][k] = coins[0][0]` for k=0; `dp[0][0][k] = max(coins[0][0], 0)` for k>=1 (can neutralize start).

**Fill order:** row by row, left to right.

**Answer:** `dp[m-1][n-1][2]`

## 3. Required Imports

```python
from typing import List
```
(Only stdlib typing needed; no numpy/scipy.)

## 4. Key Edge Cases

| Case | Strategy |
|------|----------|
| All positive values (Example 2) | Neutralizations unused; dp still picks up all coins correctly |
| Single cell grid `[[v]]` | Base case handles it; answer is `max(v, 0)` effectively via k=2 |
| All negative grid | Robot must traverse; use neutralizations on worst two cells |
| First row/column only | Only one predecessor direction available; guard index bounds |

## 5. Common Pitfalls

- **Out-of-bounds predecessor:** When `i==0`, there's no `dp[i-1][j]`; when `j==0`, there's no `dp[i][j-1]`. Use `-inf` as sentinel for missing predecessors (not 0), so `max` naturally ignores them.
- **Neutralizing positive cells:** Only neutralizing negative cells makes sense, but the DP naturally handles this — neutralizing a positive cell gives `prev + 0` which is worse than `prev + coins[i][j]`, so it won't be chosen. No explicit guard needed.
- **Base case for k>0 at (0,0):** With 1 or 2 neutralizations, the robot *can* skip the start cell's negative value. Set `dp[0][0][k] = max(coins[0][0], 0)` for `k >= 1`.
- **Using `-inf` not `0` as init:** Initializing unreachable states to `0` causes incorrect results when all paths yield negative totals.
- **List import:** `List` must be imported from `typing` since the signature uses it.

## 6. Suggested Private Helper Functions

- **`_init_dp(m, n)`**: Creates a 3D list of shape `(m, n, 3)` filled with `-inf`. Keeps `maximumAmount` clean.
- **`_prev_best(dp, i, j, k)`**: Returns `max` of `dp[i-1][j][k]` and `dp[i][j-1][k]`, treating out-of-bounds as `-inf`. Centralizes the boundary guard logic used in every cell transition.