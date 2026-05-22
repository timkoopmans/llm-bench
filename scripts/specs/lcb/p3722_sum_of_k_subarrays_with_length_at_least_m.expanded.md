# Implementation Guide: `maxSum` — Sum of K Subarrays with Length ≥ M

---

## 1. Required Function Signature

```python
class Solution:
    def maxSum(self, nums: List[int], k: int, m: int) -> int:
```

---

## 2. Algorithm Steps

**Approach: DP with prefix sums**

**Prefix sum setup:**
- Build `prefix[i]` = sum of `nums[0..i-1]` (length n+1). Subarray sum `nums[i..j]` = `prefix[j+1] - prefix[i]`.

**DP definition:**
- `dp[i][j]` = maximum sum using exactly `i` subarrays from the first `j` elements of `nums` (i.e., `nums[0..j-1]`).
- Base: `dp[0][j] = 0` for all j; everything else = `-infinity`.

**Transition:** For each count `i` from 1 to k, for each ending position `j` from `i*m` to `n`:
- Either skip `nums[j-1]`: `dp[i][j] = dp[i][j-1]`
- Or end a subarray at position `j` with length `L >= m`: pick best starting point. The subarray ends at index `j-1`, starts at some index `s` where `s <= j-m`, giving sum `prefix[j] - prefix[s]`. We want max over valid `s` of `dp[i-1][s] + prefix[j] - prefix[s]` = `prefix[j] + max_over_s(dp[i-1][s] - prefix[s])`.

**Optimization (avoid O(n²) inner loop):**
- Maintain a running maximum `best = max(dp[i-1][s] - prefix[s])` for `s` from 0 up to `j - m`. As `j` increases, extend `best` by one new valid `s` each step.

**Full pseudocode:**
```
prefix[0..n] built once
dp[0..k][0..n] = -inf; dp[0][0..n] = 0
for i in 1..k:
    best = -inf
    for j in i*m .. n:
        # new valid start s = j - m becomes available
        s = j - m
        best = max(best, dp[i-1][s] - prefix[s])
        dp[i][j] = max(dp[i][j-1], best + prefix[j])
return dp[k][n]
```

---

## 3. Required Imports

```python
from typing import List
```
No numpy/scipy needed.

---

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| All negatives, forced to pick all elements (Example 2) | `-inf` init ensures only valid selections are considered; forced picks accumulate negative sums correctly |
| k=1, m=full array | Only one valid subarray; DP handles naturally |
| Subarray must be exactly minimum length m | The `s = j - m` indexing enforces minimum length |

---

## 5. Common Pitfalls

- **Off-by-one in prefix indexing:** `prefix[j] - prefix[s]` covers `nums[s..j-1]`. Ensure `prefix` has length `n+1`.
- **`-inf` initialization:** Use `float('-inf')`, not `0`. Using `0` causes wrong answers when all sums are negative.
- **Loop start for j:** Must start at `j = i*m` (need at least `i` subarrays of length `m` each), not at `j = m`. Starting too early leaves `dp[i-1][s]` as `-inf`, silently corrupting `best`.
- **`best` reset per row:** Reset `best = float('-inf')` at the start of each `i` iteration, not once globally.
- **Skip option propagation:** `dp[i][j] = max(dp[i][j-1], ...)` — forgetting the skip option causes answers to be too small.
- **`dp[i][j-1]` access when j=i\*m:** `j-1 = i*m - 1` which is within bounds (initialized to `-inf`), so the max correctly ignores it.

---

## 6. Suggested Private Helper Functions

- `_build_prefix(nums)` — returns prefix sum array of length `n+1`; keeps main logic clean and testable.
- `_init_dp(k, n)` — returns 2D list `(k+1) x (n+1)` filled with `-inf`, then sets row 0 to 0; isolates initialization logic.