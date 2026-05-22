# Implementation Guide: `findMaxSum`

## 1. Required Function Signatures

```python
class Solution:
    def findMaxSum(self, nums1: List[int], nums2: List[int], k: int) -> List[int]:
```

---

## 2. Algorithm Steps

**Core idea:** Sort indices by `nums1` value, then sweep in increasing order, maintaining a fixed-size max-heap of the top-k `nums2` values seen so far (all with strictly smaller `nums1`).

1. Create a list of `(nums1[i], nums2[i], i)` for all `i`, sorted ascending by `nums1[i]`.
2. Initialize: `answer = [0] * n`, a min-heap `heap = []`, `heap_sum = 0`.
3. Group the sorted list into **buckets of equal `nums1` value** (critical — ties must be handled together).
4. For each group of ties:
   - For every element `(v1, v2, orig_i)` in the group, **record** `answer[orig_i] = heap_sum` (the sum accumulated *before* this group is processed).
   - After recording all answers for this group, **then** add each `v2` in the group to the heap.
   - When adding `v2` to the heap: `heappush(heap, v2)`, `heap_sum += v2`. If `len(heap) > k`: `heap_sum -= heappop(heap)`.
5. Return `answer`.

**Why group ties first?** Elements with equal `nums1[i]` must not see each other; record answers before inserting any of the group's `nums2` values.

---

## 3. Required Imports

```python
from typing import List
import heapq
```

---

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| All `nums1` equal (Example 2) | Process entire array as one group; all answers stay 0 before insertion |
| `k` larger than available candidates | Heap naturally holds ≤ k items; no special handling needed |
| `k=1` | Min-heap of size 1 keeps only the single largest seen |
| `n=1` | One element, no `j` satisfies `nums1[j] < nums1[0]`; answer is `[0]` |
| Duplicate `nums2` values | Min-heap handles duplicates correctly by value |

---

## 5. Common Pitfalls

- **Tie handling is the #1 bug:** If you insert `v2` before recording `answer[i]` for the same `nums1` value, elements will incorrectly count peers. Always record *all* answers in a group first, insert *after*.
- **Python's `heapq` is a min-heap:** Pushing raw values keeps the smallest at top — this is correct here (we want to evict the smallest when size exceeds k).
- **Sorting stability:** When sorting by `nums1[i]`, ties in `nums1` can land in any order; since you group all ties together and process them uniformly, order within a group doesn't matter.
- **`heap_sum` drift:** Recomputing `sum(heap)` each time is O(k) — maintain a running `heap_sum` variable instead for O(n log k) overall.
- **`List` import:** LeetCode-style stubs use `List` from `typing`; ensure it's imported or use `list` (Python 3.9+).

---

## 6. Suggested Private Helper Functions

- **`_sorted_groups(nums1, nums2)`** → yields lists of `(v1, v2, original_index)` grouped by equal `nums1` value in ascending order. Encapsulates the sort + groupby logic cleanly using `itertools.groupby` or a manual pointer scan.
- **`_push_bounded(heap, val, k, current_sum)`** → pushes `val` onto min-heap, evicts minimum if `len > k`, returns updated sum. Keeps heap-management logic reusable and testable in isolation.