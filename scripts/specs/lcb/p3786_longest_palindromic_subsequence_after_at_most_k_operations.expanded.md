# Implementation Guide: Longest Palindromic Subsequence After At Most K Operations

## 1. Required Function Signatures

```python
class Solution:
    def longestPalindromicSubsequence(self, s: str, k: int) -> int:
```

## 2. Algorithm Steps

**Core insight:** This is a DP on intervals. For each pair of characters `s[i]` and `s[j]`, the "cost" to make them equal is the minimum circular alphabet distance: `min(|ord(s[i]) - ord(s[j])|, 26 - |ord(s[i]) - ord(s[j])|)`.

**DP definition:** `dp[i][j][b]` = longest palindromic subsequence using substring `s[i..j]` with exactly `b` operations budget remaining (or at most `b`).

**Simpler equivalent formulation:** `dp[i][j]` = minimum operations needed to make the longest palindrome of length `L` from `s[i..j]`. But tracking length and cost together is cleaner as:

`dp[i][j][b]` = LPS length for `s[i..j]` using at most `b` ops.

**Recommended approach — 3D DP:**
1. Precompute `cost[i][j] = min(|ord(s[i])-ord(s[j])|, 26 - |ord(s[i])-ord(s[j])|)`.
2. Initialize `dp[i][i][b] = 1` for all `i`, `b` (single char is palindrome of length 1).
3. Fill by increasing substring length `length = 2..n`:
   - For each `(i, j)` with `j = i + length - 1`, for each budget `b = 0..k`:
     - Option A (skip one end): `max(dp[i+1][j][b], dp[i][j-1][b])`
     - Option B (use both ends): if `cost[i][j] <= b`, then `dp[i+1][j-1][b - cost[i][j]] + 2`
     - Take max of all options.
4. Return `dp[0][n-1][k]`.

**Base cases:** `dp[i][i][b] = 1`; for `i > j`, value is `0`.

## 3. Required Imports

```python
# No imports needed beyond Python builtins
```

## 4. Key Edge Cases

| Case | Strategy |
|------|----------|
| `k` large enough to match all pairs | Budget never runs out; answer equals full string length if even/+1 if odd |
| `k = 0` | Falls back to classic LPS (no operations allowed) |
| Single character | Return 1 immediately |
| All same characters | Cost always 0; answer = len(s) |
| `"aaazzz", k=4` | Cross-alphabet wrapping: `|a-z|=25`, `26-25=1`; cost is 1 per pair |

## 5. Common Pitfalls

- **Circular distance formula:** Must be `min(diff, 26 - diff)` where `diff = abs(ord(a) - ord(b))`. Forgetting the wrap gives wrong cost for `a`/`z` pairs.
- **Budget indexing:** `dp[i+1][j-1][b - cost[i][j]]` — when `i+1 > j-1` (length-2 substring), the inner range is empty; treat `dp[i+1][j-1][*] = 0` correctly (i.e., adding 2 to 0 gives 2).
- **Budget as exact vs. at-most:** DP with "at most b" means you can propagate: `dp[i][j][b] = max(dp[i][j][b], dp[i][j][b-1])` after filling, OR just take max across options naturally. Ensure budget isn't over-consumed.
- **Array size:** `dp` is `n × n × (k+1)`; with `n=200, k=200` this is 8M entries — fine for Python/list.
- **Loop order:** Outer loop must be substring **length** (shortest first), not `i` or `j` independently.

## 6. Suggested Private Helper Functions

- `_cost(a, b) -> int`: Returns circular alphabet distance between characters `a` and `b`. Encapsulates the `min(diff, 26-diff)` logic cleanly.
- `_build_dp(s, k) -> list`: Allocates and fills the 3D DP table; returns it so `longestPalindromicSubsequence` just reads `dp[0][n-1][k]`.