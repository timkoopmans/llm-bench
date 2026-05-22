# Implementation Guide: Properties Graph

## 1. Required Function Signatures

```python
class Solution:
    def numberOfComponents(self, properties: List[List[int]], k: int) -> int:
```

## 2. Algorithm Steps

```
1. Convert each row properties[i] to a set (deduplicated).
2. For each pair (i, j) where i < j:
   a. Compute |set_i ∩ set_j| (size of intersection)
   b. If >= k, union nodes i and j in a Union-Find structure.
3. Return the number of distinct roots in the Union-Find.
```

**Union-Find operations:**
- `find(x)`: return root of x with path compression
- `union(x, y)`: merge the components of x and y; if already same root, do nothing
- Count components = number of indices i where `find(i) == i`

## 3. Required Imports

```python
from typing import List
```
No numpy/scipy needed. Pure stdlib is sufficient.

## 4. Key Edge Cases

| Test | Scenario | Strategy |
|------|----------|----------|
| test_public_1 | k=1, multiple components | Standard UF; check all pairs |
| test_public_2 | k=2, all connected transitively | UF merges chain A-B, B-C → one component |
| test_public_3 | Duplicate values in a row (`[1,1]`), k=2 | **Convert to set first**; `{1}` has size 1, intersection size = 1 < 2 → no edge → 2 components |

## 5. Common Pitfalls

1. **Distinct integers = set semantics**: `intersect` counts *distinct* common values. Using raw lists/multisets gives wrong counts. Always convert rows to sets before intersecting.

2. **`len(set_a & set_b)` vs `len(set_a.intersection(set_b))`**: Both work; just be consistent. Don't accidentally compare list overlaps with `count()`.

3. **Off-by-one in pair iteration**: Loop `for i in range(n): for j in range(i+1, n)` — don't include `i == j` (self-loops not needed) and don't double-count.

4. **Union-Find root count**: Count components as `sum(1 for i in range(n) if find(i) == i)` *after* all unions. Counting during union is error-prone.

5. **Path compression side effect**: `find` must update `parent[x]` recursively or iteratively, otherwise large inputs slow down but don't break correctness for n≤100.

6. **`List` import**: The starter code uses `List[List[int]]` — must import from `typing` (Python < 3.9 requires this; safe to always include).

## 6. Suggested Private Helper Functions

```
_make_sets(parent):     Initialize parent[i] = i for i in range(n).

_find(parent, x):       Return root of x using path compression
                        (set parent[x] = root recursively).

_union(parent, x, y):   Call find on both; if roots differ, set one
                        root's parent to the other.

_intersect_size(a, b):  Takes two pre-built sets, returns len(a & b).
                        Call this once per pair inside the main loop.
```

Keep sets pre-computed (convert all rows to sets before the double loop) to avoid redundant set construction inside O(n²) iterations.