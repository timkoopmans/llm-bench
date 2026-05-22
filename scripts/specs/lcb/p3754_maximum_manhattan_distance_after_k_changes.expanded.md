# Implementation Guide: Maximum Manhattan Distance After K Changes

## 1. Required Function Signatures

```python
class Solution:
    def maxDistance(self, s: str, k: int) -> int:
```

## 2. Algorithm Steps

**Key Insight:** Manhattan distance = |x| + |y|. At each step i, to maximize this, we want to be moving in one of four diagonal "quadrant" directions: NE, NW, SE, SW. For a fixed quadrant (e.g., NE = positive x, positive y), count how many moves in the prefix disagree with that quadrant and can be flipped.

**For each of the 4 quadrants (NE, NW, SE, SW):**
- Define two "good" directions for that quadrant (e.g., NE → 'N' and 'E' are good, 'S' and 'W' are bad).
- Sweep through the string left to right, tracking:
  - `good`: count of moves matching the target quadrant directions
  - `bad`: count of moves opposing the quadrant
- At position i (1-indexed), the total moves so far = `i`. The net displacement in this quadrant = `good - bad + min(bad, k)` → but we can flip up to `min(bad, k)` bad moves to good.
- Manhattan distance at step i with best flips = `good + min(bad, k) - (bad - min(bad, k))` = `good - bad + 2 * min(bad, k)`
- Clamp to `i` (can't exceed total steps taken).
- Track the global maximum across all positions and all quadrants.

**Pseudocode:**
```
ans = 0
for each quadrant in [(N,E), (N,W), (S,E), (S,W)]:
    good = 0, bad = 0
    for i, ch in enumerate(s, 1):
        if ch in quadrant_dirs:
            good += 1
        else:
            bad += 1
        dist = good - bad + 2 * min(bad, k)
        dist = min(dist, i)   # can't exceed steps taken
        ans = max(ans, dist)
return ans
```

## 3. Required Imports

None required beyond built-ins.

## 4. Key Edge Cases

| Case | Strategy |
|------|----------|
| `k = 0` | No flips; formula still works since `min(bad, 0) = 0` |
| `k >= len(s)` | All moves can be flipped; clamp to `i` prevents overcounting |
| All same direction | All 4 quadrant sweeps handle it; one will score maximum |
| Single character | Loop runs once, returns 1 (or k-boosted, clamped to 1) |

## 5. Common Pitfalls

- **Forgetting to clamp to `i`:** The formula `good - bad + 2*min(bad,k)` can exceed `i` when `k` is large. Always apply `min(dist, i)`.
- **Trying to track actual coordinates:** Don't simulate x/y separately — work with the combined Manhattan distance formula directly per quadrant.
- **Using only 2 quadrants:** All 4 diagonal quadrants must be tried. Omitting any will miss cases where the optimal path heads SW or SE.
- **Off-by-one in counting:** Use 1-indexed step count `i` matching enumerate(s, 1) so the clamp `min(dist, i)` is correct.
- **Reusing bad/good across quadrants:** Reset `good = bad = 0` for each new quadrant sweep.

## 6. Suggested Private Helper Functions

- `_sweep(s, dirs, k)` — given a 2-character set `dirs` of "good" directions and integer `k`, sweeps the string and returns the max achievable distance for that quadrant orientation. Keeps the main method clean with 4 calls.