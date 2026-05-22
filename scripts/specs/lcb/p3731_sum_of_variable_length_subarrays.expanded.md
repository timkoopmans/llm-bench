# Implementation Guide: sum-of-variable-length-subarrays

## 1. Required Function Signatures

```python
class Solution:
    def subarraySum(self, nums: List[int]) -> int:
```

## 2. Algorithm Steps

1. Initialize `total = 0`.
2. For each index `i` from `0` to `n-1`:
   - Compute `start = max(0, i - nums[i])`
   - Compute the sum of `nums[start : i+1]` (inclusive slice, so Python slice is `[start : i+1]`)
   - Add that sum to `total`
3. Return `total`.

**Pseudocode:**
```
total = 0
for i in range(len(nums)):
    start = max(0, i - nums[i])
    total += sum(nums[start : i+1])
return total
```

## 3. Required Imports

```python
from typing import List
```
No numpy/scipy/pandas needed.

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| `i=0`, `nums[0]` is large (start < 0) | `max(0, i - nums[i])` clamps start to 0 |
| `i - nums[i]` exactly equals 0 | start=0, include entire prefix up to i — handled naturally |
| Single-element array `n=1` | Loop runs once; `start = max(0, 0 - nums[0]) = 0`; sum is `nums[0]` |
| `nums[i]` larger than `i` | `max(0, ...)` prevents negative indexing — do NOT skip the max |

## 5. Common Pitfalls

- **Off-by-one on slice end:** Python slices are exclusive on the right. The subarray `nums[start ... i]` is inclusive of `i`, so the slice must be `nums[start : i+1]`, not `nums[start : i]`.
- **Negative index trap:** Without `max(0, ...)`, a negative `start` would silently produce a valid (but wrong) Python slice from the end of the list. The `max` is mandatory.
- **`i - nums[i]` type:** Both are `int`, so no float/rounding issue, but confirm `nums[i]` is treated as an integer offset, not a value to sum.
- **`List` import:** The starter code uses `List[int]` from `typing`. If you omit `from typing import List`, the class definition will raise a `NameError` at parse time. In Python 3.9+ you could use `list[int]`, but use `typing.List` for compatibility.
- **Do not mutate `nums`:** The loop reads `nums[i]` for the start calculation and then slices `nums`; mutating in-place would corrupt later iterations.

## 6. Suggested Private Helper Functions

- **`_subarray_sum(nums, i) -> int`:** Given the full list and index `i`, returns `sum(nums[max(0, i - nums[i]) : i + 1])`. Encapsulates the per-index logic; makes the main loop a one-liner accumulation and isolates the slicing/clamping logic for easy debugging.