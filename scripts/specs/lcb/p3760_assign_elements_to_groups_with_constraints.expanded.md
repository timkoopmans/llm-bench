# Implementation Guide: assignElements

## 1. Required Function Signatures

```python
class Solution:
    def assignElements(self, groups: List[int], elements: List[int]) -> List[int]:
```

## 2. Algorithm Steps

The naive O(N·M) approach (for each group, scan all elements) is too slow for 10^5 × 10^5. Use a precomputation via multiples:

1. Let `MAX_VAL = max(groups) + 1` (or 10^5 + 1).
2. Build a lookup table `best[v]` = smallest index `j` such that `elements[j] == v`, for all values `v` that appear in `elements`. Initialize all entries to `∞` (or `-1`).
   - Iterate `elements` **in reverse order** (index 0..len-1) so that after the loop, `best[v]` holds the **smallest** index.
   - Alternatively, iterate forward and only write if `best[v]` is still unset (i.e., first occurrence wins).
3. Build a divisor lookup `assign[g]` = best element index for group value `g`:
   - For each distinct element value `v` where `best[v]` is valid:
     - Iterate through all multiples of `v`: `v, 2v, 3v, ...` up to `MAX_VAL`.
     - For each multiple `m`, update `assign[m] = min(assign[m], best[v])` (smallest index wins).
4. For each group `i`, output `assign[groups[i]]` (or `-1` if no valid assignment).

**Complexity:** Step 3 is O(MAX_VAL · H) where H is the harmonic sum ≈ O(MAX_VAL · log(MAX_VAL)), which is ~10^5 · 17 ≈ 1.7M operations. Fast enough.

## 3. Required Imports

```python
from typing import List
```
No numpy/scipy needed. Pure stdlib.

## 4. Key Edge Cases

| Case | Strategy |
|------|----------|
| Duplicate elements (e.g., `[3,3]`) | First occurrence (index 0) must win — iterate forward, write only if unseen |
| Element value larger than all group values | Its multiples never appear in `groups`; harmlessly skipped |
| `elements[j] = 1` | Divides everything; all groups get index `j` (unless a smaller index also exists) |
| Multiple elements divide same group | `assign[m]` stores the minimum index across all valid element indices |
| Group value not divisible by any element | `assign[groups[i]]` remains `-1` |

## 5. Common Pitfalls

- **Off-by-one on MAX_VAL:** Groups can be up to 10^5, so size your arrays as `10^5 + 1` (index 100000 must be valid).
- **First-occurrence semantics:** When building `best[v]`, iterate forward and **skip if already set** — do NOT use reverse iteration followed by overwrite (that also works but is less obvious). Confirm: smallest index j, not largest.
- **`assign` array initialized to `∞` or a sentinel:** Use `float('inf')` or `len(elements)` as sentinel, then replace with `-1` at output time. Don't use `-1` during min-computation or `min()` will behave incorrectly.
- **Iterating multiples for every element index vs. every distinct value:** Build `best` (value→index) first, then iterate over distinct values only — avoids redundant work for duplicate elements.
- **Output type:** Return a plain `list` of `int`. If using `float('inf')` as sentinel, convert: `assign[g] if assign[g] != float('inf') else -1`.

## 6. Suggested Private Helper Functions

- `_build_best(elements, max_val) -> dict or list`: Maps each element value to its smallest index. Returns array of size `max_val+1`.
- `_build_assign(best, max_val) -> list`: Iterates multiples for each valid value in `best`; returns `assign` array mapping group-value → winning element index (or sentinel).