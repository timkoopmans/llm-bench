# Implementation Guide: Maximum Frequency After Subarray Operation

## 1. Required Function Signatures

```python
class Solution:
    def maxFrequency(self, nums: List[int], k: int) -> int:
```

## 2. Algorithm Steps

**Core insight:** You pick one contiguous subarray and add a constant `x` to every element in it. To maximize frequency of `k`, choose some source value `v ≠ k` (elements equal to `v` inside the subarray become `k` after adding `x = k - v`). Elements already equal to `k` outside the subarray stay `k`; elements equal to `k` inside the subarray become `k + x ≠ k` (unless `v == k`, skip that).

**Base count:** `base = count(k)` in the entire array (do nothing, subarray can be empty).

**For each candidate source value `v` (1..50, v ≠ k):**
Use a maximum-subarray (Kadane's) scan to find the contiguous subarray that maximizes:
- `+1` for each position where `nums[i] == v` (gains a `k`)
- `-1` for each position where `nums[i] == k` (loses a `k`)
- `0` otherwise

Let `best_gain` = result of Kadane's on this score array (minimum value is 0, not negative).

`answer = max(answer, base + best_gain)`

**Pseudocode:**
```
base = nums.count(k)
answer = base
for v in 1..50:
    if v == k: continue
    current = 0
    best = 0
    for num in nums:
        if num == v:   current += 1
        elif num == k: current -= 1
        if current < 0: current = 0   # reset (Kadane's)
        best = max(best, current)
    answer = max(answer, base + best)
return answer
```

## 3. Required Imports

```python
from typing import List
```
(No numpy/scipy needed; pure Python suffices.)

## 4. Key Edge Cases

| Case | Strategy |
|------|----------|
| All elements already equal `k` | `base` equals `n`; Kadane gains nothing; return `n` |
| No element equals `v` for any `v` | All gains are 0; return `base` |
| `k` appears nowhere initially | `base = 0`; best gain drives the answer |
| Single element array | Kadane handles length-1 correctly |
| `v == k` | **Skip** — adding `x = 0` changes nothing meaningful and corrupts the `-1` logic |

## 5. Common Pitfalls

- **Never let `current` go negative in Kadane's** — reset to 0, not to the negative value. Failing to reset means you drag losses across subarray boundaries.
- **Skipping `v == k` is critical** — if `v == k`, the score array has `+1` where you want `-1` and vice versa, producing wrong counts.
- **`base` counts all `k`s in the full array**, not just outside the subarray. Elements equal to `k` inside the subarray are correctly penalized by `-1` in the score, netting out to zero contribution from them.
- **Don't add `base` inside the loop per element** — add it once at the end: `base + best`.
- **Constraints are small (values 1–50)** — iterating over all 49 candidate values is O(49·n), perfectly fine for n=10^5.

## 6. Suggested Private Helper Functions

- `_kadane_gain(nums, v, k) -> int`: Takes the array and a target source value `v`; returns the best non-negative gain from Kadane's scan using the +1/-1/0 scoring described above. Keeps `maxFrequency` clean by isolating the inner loop logic.