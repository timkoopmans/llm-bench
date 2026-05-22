# Implementation Guide: Zigzag Grid Traversal with Skip

## 1. Required Function Signatures

```python
class Solution:
    def zigzagTraversal(self, grid: List[List[int]]) -> List[int]:
```

## 2. Algorithm Steps

```
1. Initialize result = [], skip_flag = False (tracks whether to skip current cell)
2. For each row index i in 0..m-1:
   a. If i is even: columns = [0, 1, 2, ..., n-1]  (left to right)
   b. If i is odd:  columns = [n-1, n-2, ..., 0]   (right to left)
3. For each column index j in the column order:
   a. If skip_flag is False: append grid[i][j] to result
   b. Toggle skip_flag (True→False, False→True)
4. Return result
```

**Key insight:** The skip alternation is **global** across the entire traversal, not reset per row. The flag carries over from one row to the next.

Verify with Example 1 (`[[1,2],[3,4]]`):
- Row 0 LTR: cell(0,0)=1 → skip=False → take; cell(0,1)=2 → skip=True → skip
- Row 1 RTL: cell(1,1)=4 → skip=False → take; cell(1,0)=3 → skip=True → skip
- Result: [1, 4] ✓

## 3. Required Imports

```python
from typing import List
```
No numpy/scipy/pandas needed. Only stdlib `typing`.

## 4. Key Edge Cases

| Test | Grid Shape | Strategy |
|------|-----------|----------|
| 2×2 grid | `[[1,2],[3,4]]` → `[1,4]` | Skip flag carries into row 1, picks last cell |
| 3×2 grid | `[[2,1],[2,1],[2,1]]` → `[2,1,2]` | Odd number of rows; flag state entering each row matters |
| 3×3 grid | `[[1..9]]` → `[1,3,5,7,9]` | All diagonal cells; skip resets naturally each 2-cell row segment |

## 5. Common Pitfalls

- **Resetting skip per row:** Do NOT reset `skip_flag = False` at the start of each row. The flag is continuous across the entire traversal. This is the #1 mistake — Example 2 breaks if you reset it.
- **Direction confusion:** Row parity (even/odd row index) controls direction, not a separate alternating variable. Use `i % 2 == 0` for LTR.
- **List reversal:** Use `reversed(range(n))` or `range(n-1, -1, -1)` for RTL rows. Do not mutate the grid row.
- **Off-by-one in reversed range:** `range(n-1, -1, -1)` gives indices `n-1` down to `0` inclusive — double-check the stop value is `-1`.
- **Type of result:** Return a plain Python `List[int]`. Don't accidentally return a generator or tuple.

## 6. Suggested Private Helper Functions

- **`_row_order(i, n) -> list`**: Given row index `i` and width `n`, returns the ordered list of column indices for that row (LTR if even, RTL if odd). Keeps main loop clean.
- **`_flatten_zigzag(grid) -> iterator`**: Yields `(value, position_index)` tuples in zigzag order (before skipping), so the main method simply filters by even position index if preferred as an alternative design.