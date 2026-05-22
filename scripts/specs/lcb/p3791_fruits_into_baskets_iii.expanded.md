# Implementation Guide: `numOfUnplacedFruits`

---

## 1. Required Function Signatures

```python
class Solution:
    def numOfUnplacedFruits(self, fruits: List[int], baskets: List[int]) -> int:
```

---

## 2. Algorithm Steps

**Naïve O(n²) approach** (correct for n ≤ 10⁵, acceptable if tight):

```
unplaced = 0
available = list of (capacity, original_index) for each basket, marked as used/free
used = boolean array of length n, all False

For each fruit quantity f in fruits (left to right):
    Scan baskets left to right (j = 0..n-1):
        If basket j is not used AND baskets[j] >= f:
            Mark basket j as used
            Break
    Else (no basket found):
        unplaced += 1

Return unplaced
```

**Efficient O(n log n) approach** using a segment tree or sorted structure:

```
Build a segment tree over the baskets array where each node stores
the maximum capacity in its range.

For each fruit f (left to right):
    Query the segment tree for the leftmost index where capacity >= f
    If found:
        Remove that basket (set its value to 0 in the segment tree)
    Else:
        unplaced += 1

Return unplaced
```

**Segment tree query**: recurse left-child first; only go right if left subtree max < f.

---

## 3. Required Imports

```python
from typing import List
```

No numpy/scipy needed. Standard library only.

---

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| All fruits unplaceable (all baskets too small) | Every fruit increments counter; return n |
| All fruits placed | Return 0 |
| Multiple fruits compete for same basket | Mark basket used immediately upon assignment |
| Fruit skips insufficient baskets to find a later valid one | Always scan left-to-right, don't stop at first basket seen |
| n = 1 | Single fruit, single basket; standard comparison |

---

## 5. Common Pitfalls

- **Left-to-right basket order is mandatory**: Never sort baskets. The problem requires the *leftmost* valid basket, not the smallest or best-fit.
- **Basket marked used immediately**: Mark a basket used as soon as a fruit is assigned, before processing the next fruit.
- **O(n²) TLE risk**: For n = 10⁵, naïve scanning may TLE on a real judge. The two public tests are small, but prefer the segment tree if you want robustness.
- **Segment tree off-by-one**: Use 1-indexed segment tree internally; leaf `i` maps to `baskets[i-1]`. Mixing 0- and 1-indexed is the #1 bug source.
- **Not resetting segment tree node to 0**: When a basket is used, set its leaf value to 0 (not -infinity) so the max propagates correctly and it is never selected again.
- **`List` not imported**: The starter code uses `List[int]`; add `from typing import List`.

---

## 6. Suggested Private Helper Functions

- `_build(node, lo, hi, baskets)` — Recursively builds the segment tree; each node holds the max capacity in `[lo, hi]`.
- `_update(node, lo, hi, idx)` — Sets `baskets[idx]` to 0 in the segment tree and updates all ancestor max values.
- `_query(node, lo, hi, f)` — Returns the leftmost index in `[lo, hi]` where capacity ≥ `f`; returns -1 if none exists. Always recurse left child first; only enter right child if left subtree's max ≥ `f`.