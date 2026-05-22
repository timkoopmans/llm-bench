# Implementation Guide: find-the-largest-almost-missing-integer

## 1. Required Function Signatures

```python
class Solution:
    def largestInteger(self, nums: List[int], k: int) -> int:
```

## 2. Algorithm Steps

```
1. Compute n = len(nums). There are (n - k + 1) subarrays of size k.
2. For each unique value x in nums:
   a. Count how many subarrays of size k contain x.
   b. A subarray starting at index i (0-indexed, i in 0..n-k) contains x
      if x appears in nums[i : i+k].
   c. Count = number of starting indices i where x in nums[i:i+k].
3. Collect all x where count == 1.
4. Return max of that collection, or -1 if empty.
```

**Counting subarrays containing x:**
- Iterate i from 0 to n-k (inclusive).
- For each i, check if x appears in the slice nums[i:i+k].
- Increment counter if yes.

## 3. Required Imports

```python
from typing import List
```
(Only stdlib needed; no numpy/scipy required.)

## 4. Key Edge Cases

| Test | Situation | Strategy |
|---|---|---|
| `[0,0], k=1` | Duplicate values, each subarray has size 1 | Value 0 appears in 2 subarrays → count=2, not 1 → return -1 |
| `[3,9,2,1,7], k=3` | Multiple candidates; return **largest** | Track max over all qualifying x |
| `[3,9,7,2,1,7], k=4` | Duplicate 7 inflates its count | Only x=3 qualifies; return 3 |

## 5. Common Pitfalls

- **Off-by-one on subarray count:** There are `n - k + 1` subarrays (indices `0` to `n-k` inclusive). Using `range(n-k)` misses the last subarray. Use `range(n - k + 1)`.
- **Checking membership vs. counting occurrences:** The problem asks how many *subarrays* contain x, not how many times x appears total. Use `x in nums[i:i+k]` (boolean), not `nums[i:i+k].count(x)`.
- **Iterating over nums vs. unique values:** Iterating over `nums` directly instead of `set(nums)` double-counts when a value appears multiple times, which is harmless for correctness but wasteful. More importantly, it doesn't change the subarray count for x — just iterate over `set(nums)` to be clean.
- **k == n edge case:** Only one subarray exists (the whole array). Every element in nums appears in exactly 1 subarray — unless duplicates exist (duplicate x still appears in 1 subarray since there's only 1). This is handled correctly by the general algorithm.
- **k == 1 edge case:** Each element is its own subarray of size 1. A value x qualifies only if it appears exactly once in nums. This falls out naturally from the algorithm.
- **Return type:** Must return `-1` (integer), not `None` or `False`.

## 6. Suggested Private Helper Functions

- `_count_subarrays(nums, x, k) -> int`: Given the array, a target value x, and window size k, returns the number of size-k subarrays containing x. Encapsulates the inner loop cleanly and makes the main method readable.