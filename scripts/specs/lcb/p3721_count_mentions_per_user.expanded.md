# Implementation Guide: count-mentions-per-user

## 1. Required Function Signatures

```python
class Solution:
    def countMentions(self, numberOfUsers: int, events: List[List[str]]) -> List[int]:
```

## 2. Algorithm Steps

1. **Sort events** by timestamp (integer). Tie-break: OFFLINE events must come **before** MESSAGE events at the same timestamp (per problem statement: status changes processed before messages).
2. **Initialize** `mentions[0..numberOfUsers-1] = 0` and `offline_until[0..numberOfUsers-1] = -1` (tracks when each user comes back online).
3. **Process events in sorted order**:
   - For each event, extract `timestamp = int(events[i][1])`.
   - **OFFLINE event**: Set `offline_until[int(id)] = timestamp + 60`.
   - **MESSAGE event** with token `ALL`: Add 1 to every user's mention count.
   - **MESSAGE event** with token `HERE`:
     - For each user `u`, check if `timestamp >= offline_until[u]` (they are online). If yes, increment `mentions[u]`.
   - **MESSAGE event** with specific ids (space-separated `id<number>` tokens):
     - Parse each token, strip `"id"` prefix, convert to int, increment that user's `mentions`.
4. **Return** `mentions` list.

## 3. Required Imports

```python
from typing import List
```
No numpy/scipy needed.

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| OFFLINE and MESSAGE at same timestamp (e.g., t=11 offline, t=11 HERE) | Sort OFFLINE before MESSAGE at equal timestamps |
| User comes back exactly at timestamp+60 (e.g., offline at 11, message at 71) | Use `>=`: online if `timestamp >= offline_until[u]` |
| `ALL` includes offline users | Don't check `offline_until` for ALL, always count everyone |
| Duplicate ids in one message (e.g., `"id1 id1"`) | Count each occurrence separately — just iterate and increment |
| User never went offline (`offline_until` default) | Initialize `offline_until[u] = -1`; any timestamp ≥ -1, so they're online |

## 5. Common Pitfalls

- **Sort tie-breaking**: Python's `sort` is stable but you must explicitly encode OFFLINE < MESSAGE in the sort key. Use key `(int(e[1]), 0 if e[0]=="OFFLINE" else 1)`.
- **Off-by-one on re-online time**: The user is offline for 60 units, meaning they return at `timestamp + 60` exactly. Use `>=` not `>` when checking if online.
- **String parsing**: Tokens are `"id0"`, `"id1"`, etc. Strip the literal prefix `"id"` (2 chars), don't use split on `"id"` which could fail for multi-digit numbers — use `token[2:]`.
- **ALL vs HERE confusion**: `ALL` ignores online status entirely; `HERE` respects it. Don't reuse the same branch.
- **`offline_until` initialization**: If initialized to `0`, users appear offline at timestamp 0 (impossible per constraints, but safe to use `-1` or `0` since events start at t≥1 — use `-1` to be explicit).
- **Mutating while iterating**: Don't modify the original events list; sort a copy or sort in-place before processing.

## 6. Suggested Private Helper Functions

- `_sort_key(event)`: Returns `(int(event[1]), 0 if event[0]=="OFFLINE" else 1)` — used as the sort key to enforce correct ordering.
- `_parse_ids(mention_str)`: Takes a space-separated string of `id<n>` tokens, returns a list of integers. Handles duplicates by returning all (not a set).
- `_is_online(u, timestamp, offline_until)`: Returns `True` if `timestamp >= offline_until[u]` — centralizes the online-check logic used for HERE events.