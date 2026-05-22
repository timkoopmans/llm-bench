# Implementation Guide: `hasSpecialSubstring`

---

## 1. Required Function Signatures

```python
class Solution:
    def hasSpecialSubstring(self, s: str, k: int) -> bool:
```

---

## 2. Algorithm Steps

1. Iterate over every possible starting index `i` from `0` to `len(s) - k` (inclusive).
2. Extract the candidate substring `sub = s[i : i+k]`.
3. Check that `sub` consists of exactly one distinct character: `len(set(sub)) == 1`.
4. Check the left boundary: if `i > 0`, the character `s[i-1]` must differ from `sub[0]`.
5. Check the right boundary: if `i+k < len(s)`, the character `s[i+k]` must differ from `sub[0]`.
6. If all checks pass for any `i`, return `True`.
7. If no valid window found after the loop, return `False`.

---

## 3. Required Imports

None required. Pure Python, no stdlib or third-party imports needed.

---

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| Substring touches the **start** of `s` (no left neighbor) | Skip left boundary check when `i == 0` |
| Substring touches the **end** of `s` (no right neighbor) | Skip right boundary check when `i+k == len(s)` |
| `k == len(s)` (whole string) | Both boundary checks are skipped; only uniformity check matters |
| `k == 1` | Single character; neighbors just must differ (or not exist) |
| Repeated runs of same char with wrong length (e.g., `"aaaa"`, `k=3`) | The run of 4 `a`s has no valid window of exactly 3 because neighbors are also `a` |

---

## 5. Common Pitfalls

- **Off-by-one in loop range**: Use `range(len(s) - k + 1)`. Using `range(len(s) - k)` misses the last valid window.
- **Forgetting the boundary character must be DIFFERENT, not absent**: Both conditions (left ≠ char AND right ≠ char) must be checked *only when the neighbor exists*; absence counts as valid.
- **Using `set(sub) == 1` (integer comparison)**: You must use `len(set(sub)) == 1`, not `set(sub) == 1`.
- **Checking `s[i-1]` without guarding `i > 0`**: In Python, `s[-1]` silently accesses the last character, giving a wrong result rather than an error — always guard with `i > 0`.
- **Mutating or slicing beyond string bounds**: `s[i+k]` when `i+k >= len(s)` raises `IndexError` — always guard with `i+k < len(s)`.

---

## 6. Suggested Private Helper Functions

- `_is_uniform(sub: str) -> bool`: Returns `True` if all characters in `sub` are identical (`len(set(sub)) == 1`). Keeps the main loop readable.
- `_valid_left(s: str, i: int, c: str) -> bool`: Returns `True` if there is no left neighbor (`i == 0`) or `s[i-1] != c`. Encapsulates the left boundary guard.
- `_valid_right(s: str, i: int, k: int, c: str) -> bool`: Returns `True` if there is no right neighbor (`i+k == len(s)`) or `s[i+k] != c`. Encapsulates the right boundary guard.