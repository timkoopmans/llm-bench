# Implementation Guide: Closest Equal Element Queries

## 1. Required Function Signatures

```python
class Solution:
    def solveQueries(self, nums: List[int], queries: List[int]) -> List[int]:
```

## 2. Algorithm Steps

**Preprocessing phase — group indices by value:**
1. Build a dict mapping each value → sorted list of indices where it appears.
2. For each value that appears only once, any query on that index returns -1.

**For each query index `q`:**
1. Look up `val = nums[q]`.
2. Get the sorted list `positions` of all indices with that value.
3. If `len(positions) == 1`, answer is -1.
4. Otherwise, find the position of `q` within `positions` (it will be there exactly).
5. Check the **previous** neighbor: `prev = positions[(pos_idx - 1) % len(positions)]`
6. Check the **next** neighbor: `next_ = positions[(pos_idx + 1) % len(positions)]`
7. Circular distance from `q` to index `j` in array of length `n`:  
   `dist(q, j) = min(|q - j|, n - |q - j|)`
8. Answer for this query = `min(dist(q, prev), dist(q, next_))`.

**Why only neighbors?** The positions list is sorted; the minimum circular distance to any other occurrence must be one of the two neighbors in the circular order of that sorted list. Non-adjacent entries are always farther.

**Build and return the answer list** in the same order as queries.

## 3. Required Imports

```python
from typing import List
from collections import defaultdict
import bisect
```

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| All elements unique (Example 2) | Dict entries all have length 1 → return -1 for all |
| Element appears exactly twice | Both neighbors are the same single other index; both wrap to it |
| Query index is first or last in sorted positions list | Use modular indexing `(i ± 1) % len(positions)` to wrap correctly |
| Circular distance wraps around array end | Always use `min(d, n - d)` |
| Multiple queries on the same index | Precompute a `best[index]` map to avoid redundant work |

## 5. Common Pitfalls

- **Don't use `index()` in a loop without care** — `list.index()` is O(k) per call; use `bisect.bisect_left` on the sorted positions list for O(log k) lookup, keeping overall complexity O(n log n).
- **Modular neighbor wrap**: `(pos_idx - 1) % len(positions)` works correctly in Python even when `pos_idx == 0` (gives last element). Don't use `if pos_idx == 0: prev = positions[-1]` style — modulo is cleaner and less error-prone.
- **Circular distance formula**: `abs(q - j)` alone is wrong for circular arrays. Always `min(abs(q-j), n - abs(q-j))`.
- **Only check immediate neighbors, not all pairs**: Checking all pairs for each query is O(n²) and will TLE on 10⁵ inputs.
- **`queries[i]` is an index, not a value** — a common misread. `nums[queries[i]]` gives the value to look up.

## 6. Suggested Private Helper Functions

- `_build_index_map(nums)` → `dict[int, list[int]]`: Iterates nums once, appends each index to the appropriate value's list. Returns the completed dict.
- `_circular_dist(i, j, n)` → `int`: Returns `min(abs(i-j), n - abs(i-j))`. Keeps distance logic centralized and testable.
- `_best_for_index(idx, positions, n)` → `int`: Given a query index and its value's sorted positions list, uses bisect to find the index's rank, checks both circular neighbors, returns the minimum distance (or -1 if list has length 1).