# Implementation Guide: eat-pizzas (`maxWeight`)

---

## 1. Required Function Signatures

```python
class Solution:
    def maxWeight(self, pizzas: List[int]) -> int:
```

---

## 2. Algorithm Steps

**Key insight:** Sort the pizzas descending. You have `n/4` total days. Count odd days = `ceil(days/2)`, even days = `floor(days/2)`.

On odd days you gain the **maximum** (Z) of the 4 eaten. On even days you gain the **second maximum** (Y). To maximize total gain, greedily assign the largest pizzas to odd days (they give you the top element), and the next largest to even days (they give you the second element, so you "waste" one more).

**Step-by-step:**

1. Sort `pizzas` in **descending** order.
2. Compute `days = n // 4`, `odd_days = (days + 1) // 2`, `even_days = days // 2`.
3. **Odd days:** For each of the `odd_days` days, pick the best group. The top pizza of each group of 4 is taken greedily. Since we pick the absolute largest available each odd day, we take `pizzas[0], pizzas[1], ..., pizzas[odd_days - 1]` — i.e., the first `odd_days` elements of the sorted-descending array (one per odd day, each contributes its index directly as the max).
4. **Even days:** For even days you gain Y (second largest). After committing the top `odd_days` to odd days, the pointer moves. For each even day, you skip one pizza (the Z that you won't gain weight from) and take the next. Starting at index `odd_days`, for even day `i` (0-indexed): gain = `pizzas[odd_days + 1 + 2*i]`.
5. Sum all gained weights.

**Concrete pointer arithmetic (0-indexed, sorted descending):**
- Odd day gains: indices `0, 1, 2, ..., odd_days - 1`
- Even day gains: indices `odd_days + 1, odd_days + 3, odd_days + 5, ...` (every other, skipping one between)

Return the total sum.

---

## 3. Required Imports

```python
from typing import List
import math  # optional, (days+1)//2 suffices without math
```

---

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| All pizzas equal weight (Example 2) | Greedy still works; sum is deterministic |
| `n = 4` (single day, odd) | `odd_days=1, even_days=0`; just return max pizza |
| Large `n` (2×10⁵) | Pure index arithmetic, O(n log n) sort is fine |
| Odd total days (days not divisible by 2) | `odd_days > even_days` by 1; ceiling formula handles it |

---

## 5. Common Pitfalls

- **Off-by-one in even-day pointer:** The even day gain starts at `odd_days + 1`, NOT `odd_days`. Index `odd_days` is the Z (wasted) for the first even-day group.
- **Sorting direction:** Must sort **descending** (largest first). Using `sort()` ascending and reading from the end works too, but be consistent — mixing up direction causes wrong index offsets.
- **Integer division for day counts:** Use `(days + 1) // 2` for odd days; do not use `math.ceil` with floats to avoid floating-point rounding surprises on large inputs.
- **Assuming even/odd days are equal:** When `days` is odd, there is one more odd day than even day — forgetting this leads to index miscalculation.
- **Re-using pizzas:** The greedy assignment is purely index-based on the sorted array; no pizza is double-counted as long as your index ranges don't overlap.

---

## 6. Suggested Private Helper Functions

- `_count_days(n)` → returns `(odd_days, even_days)` given total pizza count `n`. Encapsulates the ceiling/floor arithmetic cleanly.
- `_odd_day_sum(sorted_desc, odd_days)` → sums `sorted_desc[0:odd_days]`.
- `_even_day_sum(sorted_desc, odd_days, even_days)` → sums elements at indices `odd_days + 1, odd_days + 3, ...` for `even_days` terms.