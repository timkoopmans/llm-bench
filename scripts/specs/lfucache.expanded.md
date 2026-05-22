# LFUCache Implementation Guide

## 1. Required Function Signatures

```python
class LFUCache:
    def __init__(self, capacity: int): ...
    def get(self, key: int) -> int: ...
    def put(self, key, value) -> None: ...
```

## 2. Algorithm Steps

**Data structures needed:**
- `key_to_val`: dict mapping key → value
- `key_to_freq`: dict mapping key → current frequency
- `freq_to_keys`: dict mapping frequency → **OrderedDict** of keys (insertion order = recency; oldest first)
- `min_freq`: integer tracking the current minimum frequency
- `capacity`: integer

**get(key):**
1. If key not in `key_to_val`, return -1
2. Call `_increment_freq(key)`
3. Return `key_to_val[key]`

**put(key, value):**
1. If capacity == 0, return immediately
2. If key exists in `key_to_val`: update `key_to_val[key] = value`, call `_increment_freq(key)`, return
3. If `len(key_to_val) >= capacity`: call `_evict()`
4. Insert: `key_to_val[key] = value`, `key_to_freq[key] = 1`
5. Append key to `freq_to_keys[1]` (create OrderedDict entry if needed)
6. Set `min_freq = 1`

**_increment_freq(key):**
1. Get `f = key_to_freq[key]`
2. Remove key from `freq_to_keys[f]`; if that OrderedDict is now empty, delete `freq_to_keys[f]`, and if `f == min_freq`, increment `min_freq`
3. Set `key_to_freq[key] = f + 1`
4. Append key to `freq_to_keys[f+1]`

**_evict():**
1. Look up `freq_to_keys[min_freq]`
2. Pop the **oldest** (first-inserted) key from that OrderedDict — this is the LRU among LFU
3. Delete that key from `key_to_val` and `key_to_freq`

## 3. Required Imports

```python
from collections import OrderedDict, defaultdict
```

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| `capacity=0` | Guard at top of `put`; never store anything |
| `capacity=1` | Evict the single existing key before every new insert |
| `put` on existing key | Update value + increment freq; do NOT change cache size |
| LRU tie-breaking within same freq | OrderedDict preserves insertion order; `popitem(last=False)` removes oldest |
| `min_freq` update on eviction | After eviction, `min_freq` will be reset to 1 on the next new insert anyway |
| `min_freq` update on `_increment_freq` | Only bump `min_freq` if the emptied bucket **was** `min_freq` |

## 5. Common Pitfalls

- **Wrong OrderedDict pop direction**: `popitem(last=False)` removes the oldest (LRU). `popitem(last=True)` removes newest — that's wrong.
- **Forgetting to delete empty freq buckets**: leaving empty `freq_to_keys[f]` causes stale `min_freq` logic to break.
- **`min_freq` after eviction**: do NOT try to recompute `min_freq` after eviction; the next `put` of a new key always resets it to 1 — just set it there.
- **`min_freq` in `_increment_freq`**: only increment `min_freq` when the old-frequency bucket becomes empty AND `old_freq == min_freq`. Never blindly increment.
- **Size growth on update**: calling `put` on an existing key must NOT add a new entry; check membership first.
- **Using plain `dict` instead of `OrderedDict`**: Python 3.7+ dicts preserve insertion order for iteration, but `popitem()` on a plain dict always removes the **last** item — you'd need `next(iter(d))` to get the first. Use `OrderedDict.popitem(last=False)` for clarity and correctness.
- **`defaultdict(OrderedDict)`**: safe to use; just ensure you don't accidentally create an empty bucket entry by mere lookup — always write before reading in eviction context.

## 6. Suggested Private Helper Functions

- **`_increment_freq(key)`**: removes key from its current freq bucket, increments freq, inserts into next bucket, conditionally updates `min_freq`. Called by both `get` and `put`.
- **`_evict()`**: pops the LRU key from `freq_to_keys[min_freq]`, cleans up all three dicts. Called only from `put` when at capacity with a new key.