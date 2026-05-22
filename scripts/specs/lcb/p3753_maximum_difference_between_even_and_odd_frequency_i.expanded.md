# Implementation Guide

## 1. Required Function Signatures

```python
class Solution:
    def maxDifference(self, s: str) -> int:
```

## 2. Algorithm Steps

1. Count the frequency of every character in `s` using a frequency map.
2. Separate frequencies into two groups:
   - **odd_freqs**: all frequency values where `freq % 2 == 1`
   - **even_freqs**: all frequency values where `freq % 2 == 0`
3. The answer is: `max(odd_freqs) - min(even_freqs)`
4. Return that integer difference.

**Pseudocode:**
```
freq_map = count characters in s
odd_freqs  = [v for v in freq_map.values() if v % 2 == 1]
even_freqs = [v for v in freq_map.values() if v % 2 == 0]
return max(odd_freqs) - min(even_freqs)
```

## 3. Required Imports

```python
from collections import Counter
```
No numpy/scipy/pandas needed.

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| Single character dominates (e.g. `"aaaaabbc"`) | `max(odd)` naturally picks it; no special handling |
| Multiple even-frequency chars (pick smallest) | `min(even_freqs)` handles it |
| All but one char has frequency 1 (odd) | Still valid; constraints guarantee at least one even exists |
| Minimum-length string (len=3) | Counting still works; constraints guarantee both groups non-empty |

## 5. Common Pitfalls

- **Don't confuse the subtraction order**: the problem asks `odd_freq - even_freq` (NOT even minus odd). Getting this backwards gives a negative result.
- **Don't take `max(odd) - max(even)`**: to maximize the difference you want the *smallest* even frequency in the denominator, i.e., `min(even_freqs)`.
- **Don't assume only two distinct characters exist**: iterate over all character frequencies, not just the first two you encounter.
- **Don't use `s.count(c)` in a loop over `set(s)` without realizing it's O(n·k)**: fine here (n≤100), but `Counter` is cleaner and less error-prone.
- **Constraints guarantee both groups non-empty**: no need to guard against empty `odd_freqs` or `even_freqs`, but if you add that guard, make sure it doesn't silently return a wrong default like `0`.

## 6. Suggested Private Helper Functions

- **`_get_frequencies(s: str) -> dict`** — wraps `Counter(s)` and returns the frequency mapping; isolates the counting logic for clarity.
- **`_split_by_parity(freq_map: dict) -> tuple[list, list]`** — returns `(odd_freqs, even_freqs)` by partitioning `freq_map.values()` on `v % 2`; keeps the main method readable and makes each partition independently testable.