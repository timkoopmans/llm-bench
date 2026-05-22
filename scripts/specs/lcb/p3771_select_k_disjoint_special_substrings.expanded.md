# Implementation Guide: select-k-disjoint-special-substrings

## 1. Required Function Signatures

```python
class Solution:
    def maxSubstringLength(self, s: str, k: int) -> bool:
```

## 2. Algorithm Steps

**Core insight:** A "special substring" s[l..r] is valid when every character that appears in s[l..r] appears *nowhere* outside that range. This means the substring "owns" all its characters globally.

**Step 1 – Precompute first/last occurrence of each character:**
- `first[c]` = smallest index where character `c` appears
- `last[c]` = largest index where character `c` appears

**Step 2 – Find all valid special substrings as intervals [l, r]:**
- For each possible left boundary `l` (0 to n-1):
  - Initialize `r = last[s[l]]`
  - Expand `r` by scanning characters in `s[l..r]`: for each char `c` in the window, set `r = max(r, last[c])`
  - Once the window is stable (no more expansions needed), check validity:
    - Every character `c` in `s[l..r]` must have `first[c] >= l` (doesn't appear before `l`)
    - The interval must not be the entire string: `r - l + 1 < n`
  - If valid, record interval `(l, r)` and advance `l` past `r` (optimization, not required)

**Step 3 – Greedily count maximum disjoint intervals:**
- Sort valid intervals by their right endpoint `r` (classic interval scheduling)
- Greedily pick intervals: maintain `end = -1`; for each interval `(l, r)` in sorted order, if `l > end`, pick it, increment count, set `end = r`

**Step 4 – Return `count >= k`**

**Special case:** If `k == 0`, return `True` immediately.

## 3. Required Imports

```python
# No imports needed beyond builtins
```

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| `k = 0` | Always return `True` before any computation |
| Entire string is one "special" block | Reject: rule says substring ≠ entire string |
| Characters appearing only once | Each is its own valid special substring of length 1 (if not contaminated) |
| `s = "cdefdc"` — overlapping first/last ranges | Expansion logic merges `c`-containing regions, limiting count to 2 |

## 5. Common Pitfalls

- **Expansion must be iterative, not one-pass:** When you expand `r`, newly included characters may push `r` further. Use a loop or pointer scan until stable.
- **first[c] check is mandatory:** Don't forget to verify `first[s[i]] >= l` for all `i` in `[l, r]`; a character in the window may have appeared *before* `l`, invalidating the substring.
- **Off-by-one on "not entire string":** Check `(r - l + 1) < len(s)`, not `r < len(s) - 1`.
- **Greedy sort key:** Sort by *right* endpoint for interval scheduling, not left. Sorting by left gives wrong count.
- **k=0 edge case:** The loop may produce 0 valid intervals yet `0 >= 0` is true — handle explicitly or rely on the count comparison, but verify it returns `True` not `False`.
- **Duplicate interval starts:** Multiple `l` values may produce the same `(l, r)` interval; deduplication isn't required for correctness but keeping them doesn't hurt since greedy handles it.

## 6. Suggested Private Helper Functions

- `_compute_first_last(s)` → two dicts mapping each character to its first and last index in `s`.
- `_find_valid_intervals(s, first, last)` → returns list of `(l, r)` tuples for all valid special substrings.
- `_max_disjoint(intervals)` → greedy interval scheduling, returns maximum count of non-overlapping intervals.