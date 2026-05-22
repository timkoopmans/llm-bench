# Implementation Guide: minimum-cost-to-reach-every-position

## 1. Required Function Signatures

```python
class Solution:
    def minCosts(self, cost: List[int]) -> List[int]:
```

## 2. Algorithm Steps

The key insight: once you've paid to swap with person `i`, all people behind you (indices > i) can swap with you **for free**, meaning you can slide forward past them at no extra cost.

So the minimum cost to reach position `i` is the **minimum value in `cost[0..i]`** (inclusive).

**Pseudocode:**
```
result = empty list of size n
running_min = infinity
for i from 0 to n-1:
    running_min = min(running_min, cost[i])
    result[i] = running_min
return result
```

Single left-to-right pass, tracking the running minimum.

## 3. Required Imports

```python
from typing import List
```

No numpy/scipy needed. Pure Python stdlib suffices.

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| Strictly decreasing costs (e.g., `[5,3,4,1,3,2]`) | Running min naturally captures the best paid swap so far |
| Strictly increasing costs (e.g., `[1,2,4,6,7]`) | First element is cheapest; running min stays at `cost[0]` for all positions |
| Single-element array (`n=1`) | Return `[cost[0]]`; loop runs once, no issue |
| All equal costs | Running min equals that constant; result is uniform array |

## 5. Common Pitfalls

1. **Off-by-one on range**: The loop must go `range(len(cost))` — all `n` positions need an answer. Don't accidentally do `range(1, n)` and miss index 0.

2. **Wrong interpretation of "free swap"**: Free swaps go *backward-to-forward* for the people behind you, meaning after paying for position `i` you can reach `i+1, i+2, ...` for free — NOT that you get free movement in general. The minimum prefix cost formula captures this exactly; don't overcomplicate with DP tables.

3. **Returning `cost` mutated in place vs. new list**: Build a fresh result list. Mutating the input `cost` array could cause subtle bugs if the grader reuses input objects.

4. **Using `min(cost[:i+1])` in a loop**: Correct but O(n²). Use the running minimum variable for O(n). Not a correctness bug here (n≤100) but shows misunderstanding.

5. **`List` import missing**: The starter code uses `List[int]` type hint. If `from typing import List` is absent, the class definition raises `NameError` at parse time.

## 6. Suggested Private Helper Functions

None strictly necessary given the simplicity, but optionally:

- **`_prefix_min(arr)`**: Takes a list, returns a new list where each element is the running minimum up to that index. Keeps `minCosts` clean and makes the logic unit-testable in isolation.

```
def _prefix_min(arr):
    result, cur_min = [], float('inf')
    for x in arr:
        cur_min = min(cur_min, x)
        result.append(cur_min)
    return result
```

`minCosts` then simply calls `return self._prefix_min(cost)`.