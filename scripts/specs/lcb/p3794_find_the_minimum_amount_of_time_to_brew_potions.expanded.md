# Implementation Guide: Minimum Time to Brew Potions

## 1. Required Function Signatures

```python
class Solution:
    def minTime(self, skill: List[int], mana: List[int]) -> int:
```

## 2. Algorithm Steps

This is a scheduling / pipeline simulation problem.

**Key insight:** Potions flow through wizards like a pipeline. Each wizard `i` works on potion `j` for `skill[i] * mana[j]` time. A wizard cannot start the next potion until they finish the current one, AND the previous wizard must have already finished the next potion (so it's ready to pass).

**Per-potion simulation (O(n*m)):**

For each potion `j` (in order), compute `finish[i]` = the time wizard `i` finishes potion `j`.

- `start_j` = the earliest time wizard 0 can begin potion `j`
- For potion `j=0`: `start_0 = 0`; then `finish[i] = finish[i-1] + skill[i]*mana[0]`
- For potion `j > 0`:
  - Wizard 0's start is constrained: it must not begin potion `j` before wizard 0 finishes potion `j-1` (trivially sequential for wizard 0)
  - But also, for each wizard `i`, `finish[i]` on potion `j` must be `>= prev_finish[i+1]` (wizard `i+1` must be free when wizard `i` hands off)
  - **Derive start time:** Try `start = prev_finish[0]` (wizard 0 finishes previous potion). Then walk forward: after wizard `i` finishes at `start + prefix_skill[i+1] * mana[j]`, check if wizard `i+1` is free. If `prev_finish[i+1] > computed_finish_of_i`, push the start time right by the deficit.
  - Formally: `start = max(start, prev_finish[i+1] - prefix_skill[i+1] * mana[j])` for each `i` from 0 to n-2, where `prefix_skill[i+1]` = sum of `skill[0..i]`.
  - After computing `start`, set `finish[i] = start + prefix_skill[i+1] * mana[j]` for all `i`.

**Return `finish[n-1]` after processing all potions.**

**Pseudocode:**
```
prefix[i] = skill[0] + ... + skill[i]   # 1-indexed prefix sums
prev_finish = [prefix[i] * mana[0] for i in 0..n-1]
for j in 1..m-1:
    start = prev_finish[0]
    for i in 0..n-2:
        start = max(start, prev_finish[i+1] - prefix[i+1] * mana[j])
    new_finish = [start + prefix[i+1] * mana[j] for i in 0..n-1]
    prev_finish = new_finish
return prev_finish[n-1]
```

## 3. Required Imports

```python
from typing import List
```
No numpy/scipy needed; pure Python suffices.

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| Single wizard (`n=1`) | No handoff constraints; answer = sum of all `skill[0]*mana[j]` |
| Single potion (`m=1`) | One pass; answer = `skill_total * mana[0]` |
| All equal skills/mana (test 2) | Pipeline overlaps maximally; verify pipelining logic |
| Mixed large/small mana after large (test 1) | Start time pushback must be computed correctly |

## 5. Common Pitfalls

- **Off-by-one in prefix sums:** `prefix[i+1]` covers wizards 0 through i (i+1 wizards). Index carefully.
- **Start constraint loop direction:** Must iterate `i = 0` to `n-2` (not `n-1`); you're checking wizard `i+1`'s availability.
- **Initializing `start` for `j=0`:** Don't apply the constraint loop for the first potion — it starts at 0.
- **Reusing `prev_finish[0]` as initial start:** For `j>0`, wizard 0 can only start after finishing the previous potion, so `start = prev_finish[0]` is the floor before tightening.
- **Integer arithmetic:** All values are integers; avoid float division or float comparisons.

## 6. Suggested Private Helper Functions

- `_prefix_skills(skill)` → list of prefix sums `[skill[0], skill[0]+skill[1], ...]` of length `n`; used repeatedly in inner loop.
- `_brew_first(prefix, mana0)` → returns initial `prev_finish` list for potion 0 without any constraint checking.
- `_compute_start(prev_finish, prefix, mana_j)` → given previous finish times and current mana, returns the earliest valid start for the current potion by iterating the tightening loop.