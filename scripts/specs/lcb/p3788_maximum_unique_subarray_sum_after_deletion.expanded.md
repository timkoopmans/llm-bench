# Implementation Guide: Maximum Unique Subarray Sum After Deletion

## 1. Required Function Signatures

```python
class Solution:
    def maxSum(self, nums: List[int]) -> int:
```

## 2. Algorithm Steps

The key insight: you can delete any elements, so you can always construct the ideal multiset. Order doesn't matter for the final subarray — you just need to pick the best unique subset.

**Plain English:**
1. Since deletions are free and you can remove duplicates, what remains is: for each distinct value, you may include it **at most once**.
2. Negative numbers never help the sum (including a negative number reduces the total), so exclude all negatives.
3. Among the remaining positive unique values, include all of them.
4. **Special case:** If all numbers are negative (or zero), the best you can do is return the single largest (least negative) element — you cannot make the array empty.

**Pseudocode:**
```
unique_vals = set of distinct values in nums
positives = [v for v in unique_vals if v > 0]
if positives is non-empty:
    return sum(positives)
else:
    return max(nums)   # all values <= 0; pick the largest single element
```

## 3. Required Imports

```python
from typing import List
```
No numpy/scipy/pandas needed.

## 4. Key Edge Cases

| Case | Example | Strategy |
|---|---|---|
| All positive, all unique | `[1,2,3,4,5]` | Sum everything |
| Duplicates present | `[1,1,0,1,1]` | Deduplicate; 0 is not positive, so return 1 |
| Mix of pos/neg with duplicates | `[1,2,-1,-2,1,0,-1]` | Keep unique positives: {1,2} → 3 |
| All negative | `[-3,-1,-2]` | Return max = -1 |
| Single element | `[5]` or `[-5]` | Works naturally with both branches |
| Zero only | `[0,0]` | No positives → return max(nums) = 0 |

## 5. Common Pitfalls

- **Including zero:** Zero contributes nothing to the sum. The algorithm naturally excludes it from `positives` (`v > 0`), which is correct.
- **"Subarray" wording confusion:** The problem says "subarray" but deletions reorder nothing — after deletions you pick a contiguous subarray. However, since you can delete freely, you can always isolate any subset of unique positive values as a contiguous block. Don't over-engineer a sliding-window solution.
- **All-non-positive fallback:** Forgetting this branch causes a return of 0 (empty sum) when the answer should be negative. Always guard with `if positives else max(nums)`.
- **Using `set(nums)` directly for dedup:** Fine here — `set` gives distinct values, which is exactly what you need.
- **`List` import:** Must import `from typing import List`; omitting it causes a `NameError` at class definition time in Python < 3.9.

## 6. Suggested Private Helper Functions

- **`_unique_positives(nums)`** — Returns a list of values from `nums` that are both distinct and strictly greater than zero. Keeps `maxSum` readable.
- **`_all_nonpositive(nums)`** — Returns `True` if every element ≤ 0; used to gate the fallback branch cleanly.