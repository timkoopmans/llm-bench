# Implementation Guide: Maximum Sum with At Most K Elements

## 1. Required Function Signatures

```python
class Solution:
    def maxSum(self, grid: List[List[int]], limits: List[int], k: int) -> int:
```

## 2. Algorithm Steps

```
1. For each row i in grid:
     a. Sort the row's elements in DESCENDING order.
     b. Take the first min(limits[i], len(row)) elements (respecting the per-row cap).
     c. Add these candidate elements to a global candidate list.

2. Sort the global candidate list in DESCENDING order.

3. Take the first min(k, len(candidates)) elements from the global list.

4. Return their sum.
```

**Rationale:** Each row independently contributes at most `limits[i]` of its largest values as candidates. Then we greedily pick the top `k` values globally.

## 3. Required Imports

```python
from typing import List
```
Only stdlib needed — no numpy/scipy required.

## 4. Key Edge Cases

| Edge Case | Strategy |
|-----------|----------|
| `k = 0` | `min(k, len(candidates))` naturally returns 0 elements; sum of empty list = 0 ✓ |
| `limits[i] = 0` | Taking `min(0, m)` candidates from row i yields nothing from that row ✓ |
| `limits[i] > len(row)` | `min(limits[i], len(row))` caps correctly ✓ |
| Single-element grid | Standard path handles it; no special casing needed |
| All zeros in grid | Sum is 0; no special casing needed |

## 5. Common Pitfalls

1. **Forgetting `min(limits[i], len(row))`**: If `limits[i] > m`, naive slicing `row[:limits[i]]` on a sorted list still works in Python (no IndexError), but make it explicit for clarity.

2. **Not sorting row descending before slicing**: If you slice before sorting, you get arbitrary elements instead of the largest ones. Sort first, then slice.

3. **Mutating the original grid**: Call `sorted(row, reverse=True)` (returns new list) rather than `row.sort()` in-place if the caller may reuse `grid`. Not tested here, but good practice.

4. **Off-by-one on global k**: Use `candidates[:k]` — Python slicing is safe even if `k > len(candidates)` (returns all elements). However, the problem guarantees `k <= sum(limits)`, so this is a safety net only.

5. **Using `sum()` on the full unsorted candidate pool**: You must sort globally and take only the top `k`, not sum everything collected from rows.

6. **Type annotation import**: The starter code uses `List` from `typing`; ensure `from typing import List` is present or use Python 3.9+ `list[...]` syntax consistently.

## 6. Suggested Private Helper Functions

```python
def _row_top(row: List[int], limit: int) -> List[int]:
    """Return up to `limit` largest elements from a single row (sorted desc)."""
    # sorted(row, reverse=True)[:limit]

def _collect_candidates(grid, limits) -> List[int]:
    """Flatten all per-row top elements into one list."""
    # calls _row_top for each row i

def _global_top_k(candidates: List[int], k: int) -> int:
    """Sort candidates descending, sum first k."""
    # sorted(candidates, reverse=True)[:k] then sum
```

These three helpers keep each concern isolated and make the main `maxSum` body a clean three-liner.