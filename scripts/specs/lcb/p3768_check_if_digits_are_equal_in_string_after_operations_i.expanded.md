# Implementation Guide: `hasSameDigits`

---

## 1. Required Function Signatures

```python
class Solution:
    def hasSameDigits(self, s: str) -> bool:
```

---

## 2. Algorithm Steps

1. Convert the string `s` into a list of integers (each character → its digit value).
2. **Loop** while the length of the list is greater than 2:
   - Build a new list where each element `i` = `(current[i] + current[i+1]) % 10`
   - The new list has length `len(current) - 1`
   - Replace current list with new list
3. After the loop, the list has exactly 2 elements.
4. Return `True` if `list[0] == list[1]`, else `False`.

**Pseudocode:**
```
digits = [int(c) for c in s]
while len(digits) > 2:
    digits = [(digits[i] + digits[i+1]) % 10 for i in range(len(digits) - 1)]
return digits[0] == digits[1]
```

---

## 3. Required Imports

None required. Pure Python stdlib only (no numpy/scipy needed).

---

## 4. Key Edge Cases

| Case | Strategy |
|------|----------|
| Length exactly 3 (minimum input) | One iteration produces a 2-element list; loop runs once and exits correctly |
| All same digits (e.g. `"111"`) | Sum pairs: `(1+1)%10=2`, result `"22"` → `True` |
| Result digits differ (e.g. `"34789"`) | Standard iteration; trust the mod-10 arithmetic |
| Digits summing to ≥ 10 (e.g. `9+9=18 → 8`) | Modulo 10 handles this; ensure `% 10` is always applied |

---

## 5. Common Pitfalls

- **Forgetting `% 10`**: Simply summing pairs without modulo gives wrong results when sum ≥ 10. Always apply `% 10` at each step.
- **Off-by-one in the inner loop**: The new list has `len - 1` elements. Range must be `range(len(digits) - 1)`, NOT `range(len(digits))` — the latter causes an `IndexError` on `digits[i+1]`.
- **String vs int confusion**: `s` is a string of digit *characters*. You must convert with `int(c)` before arithmetic; `'3' + '9'` is string concatenation `'39'`, not `12`.
- **Mutating while iterating**: Do NOT modify the list in-place during the reduction step. Always construct a **new** list each iteration, then reassign.
- **Wrong termination condition**: Loop condition is `> 2` (stop when exactly 2 remain). Using `>= 2` would consume the final pair and leave an empty or 1-element list.
- **Returning string comparison instead of int comparison**: If you forget to convert characters to ints and instead keep strings, `'1' == '1'` happens to work, but arithmetic will break earlier in the pipeline. Convert up front.

---

## 6. Suggested Private Helper Functions

- **`_to_digits(s: str) -> list[int]`** — converts the input string to a list of integer digits; isolates the string-to-int conversion so the main loop is clean.
- **`_reduce_once(digits: list[int]) -> list[int]`** — takes a digit list and returns one shorter list by applying `(a + b) % 10` to each consecutive pair; makes the while loop body a single readable call and easy to unit-test independently.