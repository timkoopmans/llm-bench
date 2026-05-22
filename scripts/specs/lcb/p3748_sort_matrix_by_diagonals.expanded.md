# Implementation Guide: Sort Matrix by Diagonals

## 1. Required Function Signatures

```python
class Solution:
    def sortMatrix(self, grid: List[List[int]]) -> List[List[int]]:
```

## 2. Algorithm Steps

Each diagonal is identified by the constant `d = row - col`.

- **Bottom-left triangle** (including main diagonal): `d >= 0`. Sort **descending** (non-increasing), placing largest element at top-left of diagonal.
- **Top-right triangle**: `d < 0`. Sort **ascending** (non-decreasing), placing smallest element at top-left of diagonal.

**Steps:**

1. Copy the grid into a 2D list (avoid mutating input).
2. For each diagonal offset `d` from `-(n-1)` to `+(n-1)`:
   a. Collect all `(row, col)` pairs where `row - col == d` and both indices are in `[0, n)`.
   b. Pairs naturally enumerate top-to-bottom along the diagonal.
   c. Extract the values at those positions.
   d. If `d >= 0`: sort values **descending**; else sort values **ascending**.
   e. Write sorted values back into the grid at the same `(row, col)` positions (top-to-bottom order).
3. Return the modified grid.

## 3. Required Imports

```python
from typing import List
```
No numpy/scipy needed. Pure stdlib.

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| `n=1` (single cell) | One diagonal `d=0`; sort of one element is trivial; just return as-is. |
| `n=2` main diagonal `[0,2]` → `[2,0]` | Confirm descending sort is applied for `d=0`. |
| Negative values allowed (`-10^5`) | Python's sort handles negatives correctly; no special handling needed. |
| Single-element diagonals (corners) | Sorting a length-1 list is a no-op; no special case required. |

## 5. Common Pitfalls

- **Wrong triangle assignment for `d=0`**: The main diagonal (`d=0`) belongs to the bottom-left triangle and must be sorted **descending**, not ascending. The condition is `d >= 0` for descending.
- **Direction of write-back**: Always write sorted values back in the same top-to-bottom (increasing row) order you collected them. Reversing the write order instead of the sort order will silently produce wrong results.
- **Mutating the input grid**: Collect all diagonals and sort them before writing back, or work on a deep copy. Since diagonals don't overlap, in-place is safe if you process one diagonal at a time—but copying is safer and clearer.
- **Off-by-one in diagonal enumeration**: Offsets run from `-(n-1)` to `+(n-1)` inclusive (that's `2n-1` diagonals total). Missing the boundary diagonals drops corner elements.
- **List vs. returning original reference**: `assertEqual` checks value equality, but returning the original mutated grid is fine as long as values are correct.

## 6. Suggested Private Helper Functions

- `_get_diagonal_cells(n, d)` → list of `(row, col)` pairs for diagonal offset `d` in an `n×n` grid, enumerated top-to-bottom (i.e., in order of increasing row).
- `_sort_diagonal(grid, cells, descending)` → extracts values at `cells`, sorts them (ascending or descending), writes back to `grid` in the same positional order.