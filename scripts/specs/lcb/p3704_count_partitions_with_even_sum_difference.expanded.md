# Implementation Guide: count-partitions-with-even-sum-difference

## 1. Required Function Signatures

```python
class Solution:
    def countPartitions(self, nums: List[int]) -> int:
```

## 2. Algorithm Steps

**Key mathematical insight:** `left_sum - right_sum` is even if and only if `left_sum + right_sum` (i.e., `total_sum`) is even — because `(L - R)` is even ↔ `L` and `R` have the same parity ↔ `L + R` is even. So the difference is even for **every** valid partition if and only if `total_sum` is even.

**Approach A (direct simulation):**
1. Compute `total = sum(nums)`.
2. Initialize `left_sum = 0`, `count = 0`.
3. For `i` from `0` to `n-2` (inclusive):
   - Add `nums[i]` to `left_sum`.
   - Compute `right_sum = total - left_sum`.
   - If `(left_sum - right_sum) % 2 == 0`, increment `count`.
4. Return `count`.

**Approach B (parity shortcut):**
1. If `total_sum` is odd → return `0`.
2. If `total_sum` is even → return `n - 1` (all partitions qualify).

Both approaches are correct; Approach A is safer against edge-case misunderstanding.

## 3. Required Imports

```python
from typing import List
```
(No numpy/scipy/other stdlib needed.)

## 4. Key Edge Cases

| Test case | Strategy |
|---|---|
| `[10,10,3,7,6]` → 4 | All 4 of 4 partitions are even; total=36 (even) |
| `[1,2,2]` → 0 | total=5 (odd), zero valid partitions |
| `[2,4,6,8]` → 3 | total=20 (even), all 3 partitions valid |
| Minimum length `n=2` | Only one partition index (`i=0`); loop runs exactly once |

## 5. Common Pitfalls

- **Off-by-one on loop range:** Partitions exist for indices `i` in `[0, n-2]`. Use `range(n-1)` or `range(len(nums)-1)`. Using `range(n)` would attempt a partition leaving an empty right subarray — invalid per the problem statement.
- **Parity check with negative numbers:** `(-16) % 2 == 0` is `True` in Python (Python modulo always non-negative), so `% 2 == 0` works correctly for negative differences. Do **not** use `abs()` before checking — it's unnecessary but harmless.
- **Integer division trap:** Do not use `//` or floor division when computing difference; stick to plain subtraction and `% 2`.
- **`List` import:** The starter code uses `List[int]`. Without `from typing import List`, the class definition will raise a `NameError` at parse time. Don't forget this import.

## 6. Suggested Private Helper Functions

- **`_is_even_diff(left: int, right: int) -> bool`** — returns `(left - right) % 2 == 0`; isolates the parity check, making the main loop readable and easy to unit-test independently.
- **`_prefix_sums(nums: List[int]) -> List[int]`** — returns cumulative sums of length `n`; optional, but useful if you want to avoid a running-sum variable and instead look up `left_sum = prefix[i+1]` directly.