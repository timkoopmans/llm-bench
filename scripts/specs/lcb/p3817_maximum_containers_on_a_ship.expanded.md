# Implementation Guide: Maximum Containers on a Ship

## 1. Required Function Signatures

```python
class Solution:
    def maxContainers(self, n: int, w: int, maxWeight: int) -> int:
```

## 2. Algorithm Steps

1. Compute total deck capacity: `total_cells = n * n`
2. Compute max containers by weight: `weight_limit = maxWeight // w` (integer floor division)
3. Return the **minimum** of the two values: `min(total_cells, weight_limit)`

**Why:** You cannot exceed the physical deck space (`n*n` cells), and you cannot exceed the weight limit (`maxWeight // w` containers at weight `w` each). The answer is whichever constraint is more restrictive.

## 3. Required Imports

None required. Pure Python arithmetic suffices.

## 4. Key Edge Cases the Tests Exercise

| Case | Strategy |
|------|----------|
| All containers fit by weight (`n=2, w=3, maxWeight=15`: 12 ≤ 15) | Return `n*n` = 4 |
| Weight is the binding constraint (`n=3, w=5, maxWeight=20`: floor(20/5)=4 < 9) | Return `maxWeight // w` = 4 |
| `maxWeight` exactly divisible by `w` | Floor division gives exact integer, no rounding issue |
| `maxWeight` not divisible by `w` | Floor division correctly truncates partial container |

## 5. Common Pitfalls

- **Use floor division `//`, not `/`:** You cannot load a fractional container. Using `/` gives a float and the comparison or return will be wrong.
- **Do not use `math.floor(maxWeight / w)`:** For large values near 10^9 / 1, float precision is fine here, but `//` is cleaner and always correct for integers.
- **Don't forget the deck constraint:** A common mistake is returning only `maxWeight // w` without capping at `n*n`. Test 1 catches this — if `maxWeight` is very large, the deck is the binding constraint.
- **Don't forget the weight constraint:** Returning only `n*n` fails Test 2 where weight is limiting.
- **Argument order:** The method receives `(n, w, maxWeight)` — the spec parses them in that order from the JSON lines (`2`, `3`, `15`). Swapping `n` and `w` would give wrong `n*n` but tests would still pass here coincidentally — be deliberate.

## 6. Suggested Private Helper Functions

No helpers needed for this problem — it is a one-liner:

- **(Optional)** `_deck_capacity(n)` → returns `n * n`; useful if deck shape ever changes, but unnecessary here.
- **(Optional)** `_weight_capacity(w, maxWeight)` → returns `maxWeight // w`; isolates the weight constraint logic for readability.

In practice, inline both computations directly in `maxContainers` and return `min(n*n, maxWeight // w)`.