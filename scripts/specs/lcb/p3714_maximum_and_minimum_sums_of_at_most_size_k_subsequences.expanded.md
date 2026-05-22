# Implementation Guide: minMaxSums

## 1. Required Function Signatures

```python
class Solution:
    def minMaxSums(self, nums: List[int], k: int) -> int:
```

## 2. Algorithm Steps

**Core insight:** Sort `nums`. For each element, count how many subsequences have it as the **minimum** or **maximum**, then multiply by its value.

**Sort** `nums` ascending. Let `n = len(nums)`.

**For element at index `i` as the MINIMUM:**
- It is the minimum of a subsequence of size `s` (1 ≤ s ≤ k) if the other `s-1` elements are all chosen from indices `> i` (i.e., ≥ nums[i] since sorted).
- Number of elements to the right: `right = n - 1 - i`
- Contribution: `nums[i] * sum(C(right, j) for j in 0..min(k-1, right))`

**For element at index `i` as the MAXIMUM:**
- It is the maximum when other elements are chosen from indices `< i`.
- Number of elements to the left: `left = i`
- Contribution: `nums[i] * sum(C(left, j) for j in 0..min(k-1, left))`

**Total answer** = sum of all min-contributions + all max-contributions, modulo 10^9+7.

**Precompute** Pascal's triangle (or factorials + modular inverses) up to `n` for fast binomial coefficients mod `MOD`.

**Pseudocode:**
```
sort nums
precompute C[n][r] mod MOD for 0 <= n <= N, 0 <= r <= k
ans = 0
for i in 0..n-1:
    left = i
    right = n - 1 - i
    coeff_min = sum(C(right, j) for j in 0..min(k-1, right))
    coeff_max = sum(C(left,  j) for j in 0..min(k-1, left))
    ans += nums[i] * (coeff_min + coeff_max)
return ans % MOD
```

## 3. Required Imports

```python
from typing import List
```
Only stdlib needed (no numpy/scipy).

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| `k=1`: only size-1 subsequences | Each element contributes as both min and max; `C(x,0)=1` handles it naturally |
| All equal elements `[1,1,1]` | Sorting + combinatorics still correct; no deduplication needed |
| `k >= n`: can take all elements | Cap loop at `min(k-1, left/right)` automatically |
| Large `n` (10^5), large `k` (70) | Precompute Pascal rows only up to depth `k`; O(n·k) total |

## 5. Common Pitfalls

- **Modular arithmetic**: Apply `% MOD` during precomputation of binomial coefficients, not just at the end — intermediate values explode otherwise.
- **Pascal's triangle size**: You need `C(n-1, j)` for `j` up to `k-1`. Build a 2D table of size `(n+1) x (k+1)` or use a 1D rolling array.
- **Off-by-one in left/right counts**: `left = i` (number of strictly smaller-indexed elements), `right = n-1-i`. A common mistake is using `n-i` for right.
- **Double-counting size-1 subsequences**: Each singleton has the same element as both min AND max — the formula naturally counts it twice (once in min-contribution, once in max-contribution), which is correct per the problem definition.
- **Missing `from typing import List`**: The starter code uses `List`; omitting this import causes a `NameError`.
- **Summing partial binomial prefix**: The inner sum goes from `j=0` to `min(k-1, left_or_right)`, NOT `k`. Forgetting the upper cap gives wrong results when `left < k-1`.

## 6. Suggested Private Helper Functions

- `_build_pascal(max_n, max_r, MOD)`: Returns 2D list `C` where `C[n][r] = nCr % MOD` for `0 ≤ n ≤ max_n`, `0 ≤ r ≤ max_r`. Uses standard Pascal recurrence.
- `_prefix_binom(C, n, max_j)`: Returns `sum(C[n][j] for j in 0..min(max_j, n)) % MOD` — the weighted count of valid subsequence sizes for one side.