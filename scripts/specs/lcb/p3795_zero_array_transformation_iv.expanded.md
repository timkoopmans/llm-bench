# Implementation Guide: `minZeroArray`

---

## 1. Required Function Signatures

```python
class Solution:
    def minZeroArray(self, nums: List[int], queries: List[List[int]]) -> int:
```

---

## 2. Algorithm Steps

**Core idea:** Binary search on `k` (number of queries used). For a given `k`, check if the first `k` queries can zero out `nums`.

**Feasibility check for a given `k`:**
- For each index `i` in `nums`, determine the maximum total decrement achievable using the first `k` queries.
- A query `[l, r, val]` can contribute `val` to index `i` if `l <= i <= r` (we can always choose to include index `i` in the subset).
- Index `i` is satisfiable if `sum of val_j for all queries j <= k where l_j <= i <= r_j >= nums[i]`.
- All indices must be satisfiable.

**Binary search:**
```
lo = 0, hi = len(queries)
if not feasible(hi): return -1
binary search for minimum k in [0, hi] where feasible(k) is True
```

**Feasibility function `can_zero(k)`:**
```
for each index i in range(len(nums)):
    total = sum(val for [l, r, val] in queries[:k] if l <= i <= r)
    if total < nums[i]: return False
return True
```

Given constraints (n ≤ 10, queries ≤ 1000), a naive O(n × k) feasibility check is fast enough.

---

## 3. Required Imports

```python
from typing import List
```
No numpy/scipy needed. Pure Python suffices given the small constraints.

---

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| `nums` is already all zeros | `k=0` is valid; binary search should include `lo=0` |
| Impossible even with all queries | Check `feasible(len(queries))` first; return `-1` |
| Single element array | Works naturally with the general algorithm |
| Query covers only part of array | Only counts for indices in `[l, r]`, not globally |
| `nums[i] = 0` | Already zero; any non-negative total satisfies it trivially |

---

## 5. Common Pitfalls

- **Off-by-one in binary search bounds:** Use `lo=0, hi=len(queries)` inclusive. Skipping `k=0` misses the case where `nums` is already zero.
- **Binary search termination:** Use `lo < hi` with `mid = (lo + hi) // 2`; set `hi = mid` when feasible, `lo = mid + 1` when not. Return `lo` at the end.
- **Slicing queries:** `queries[:k]` with `k=0` returns `[]`, which correctly gives `total=0` — confirm `nums[i]==0` passes.
- **Greedy subset assumption:** You can always include any index in the subset, so the maximum possible decrement at index `i` from query `j` is exactly `val_j` (if `i` is in range). Don't mistakenly think you must share `val_j` across indices.
- **Integer overflow:** Not an issue here (values are tiny), but don't use float arithmetic.
- **Checking `feasible(0)` separately:** Handle by making binary search range start at 0 and letting the general check handle it.

---

## 6. Suggested Private Helper Functions

- **`_can_zero(nums, queries, k) -> bool`:** Takes the first `k` queries, iterates over each index, sums applicable `val`s, returns `False` early if any index can't reach zero. Keeps `minZeroArray` clean.