# Implementation Guide: minMaxWeight

## 1. Required Function Signatures

```python
class Solution:
    def minMaxWeight(self, n: int, edges: List[List[int]], threshold: int) -> int:
```

## 2. Algorithm Steps

**Core insight:** Binary search on the answer (maximum weight W), then check feasibility.

**Feasibility check for a given weight W:**
- Keep only edges with weight ≤ W
- Each non-zero node must be able to reach node 0
- Each node may use at most `threshold` outgoing edges

**Key observation:** Reverse the graph. Node 0 must be reachable from all others ↔ all nodes reachable from node 0 in the *reversed* graph. In the reversed graph, each original node's outgoing degree constraint becomes an *incoming* degree constraint to that node in reverse — but what matters is: in the **reversed** graph, node 0 can reach every other node using edges with weight ≤ W, where each original node `u` contributes at most `threshold` reversed edges (i.e., in-degree of `u` in original = out-degree of `u` in reversed... careful here).

**Correct framing:**
- Reverse all edges: original edge `A→B` becomes `B→A`
- In the reversed graph, do BFS/DFS from node 0 using only edges with weight ≤ W
- For each node `u` (in original), it can have at most `threshold` outgoing edges chosen → in reversed graph, node `u` has at most `threshold` *incoming* edges available. But for reachability we just need *at least one* path; the threshold constraint means each original node `u ≠ 0` can contribute at most `threshold` reversed edges from `u`.
- Feasible if all `n` nodes are reached from 0 in the reversed graph.

**Binary search:**
1. Collect all unique weights, sort them.
2. Binary search on this sorted list: find minimum W such that feasibility holds.
3. If no W works, return -1.

**Feasibility (pseudocode):**
```
build reversed adjacency list using only edges with weight <= W
BFS from node 0 in reversed graph
return visited count == n
```

Note: threshold constraint on outgoing edges — since we only need reachability and can choose any subset ≤ threshold edges per node, and BFS naturally explores greedily, the threshold doesn't add extra constraint **beyond** checking: in the reversed graph, each node `u` has at most `threshold` outgoing edges (reversed from original). Since we can pick any one incoming edge per node in original to reach node 0, threshold ≥ 1 means each non-zero node just needs one usable outgoing edge → reachability in reversed graph suffices as long as threshold ≥ 1.

## 3. Required Imports

```python
from typing import List
from collections import deque
```

## 4. Key Edge Cases

| Case | Strategy |
|------|----------|
| No path exists to node 0 for some node | Return -1 |
| threshold=1, all outgoing from node 0 only | Reversed BFS from 0 fails → -1 |
| Multiple edges between same pair (unique weights) | Binary search handles naturally |
| Node 0 has no incoming edges in original | Return -1 immediately |

## 5. Common Pitfalls

- **Direction confusion**: You need all nodes to reach node 0 (→), so reverse edges and BFS *from* 0. Getting the direction backwards is the #1 bug here.
- **Threshold misinterpretation**: Threshold applies to outgoing edges of each node in the *original* graph. In the reversed graph this is outgoing degree of each node. Since threshold ≥ 1, any single reversed-edge path works; you don't need to track degree during BFS — just reachability.
- **Binary search bounds**: Search over *actual weight values* present in edges, not indices 1..10^6, to avoid TLE.
- **Node 0 itself**: It's always "reached" — initialize BFS with node 0 visited.
- **List import**: `List` must be imported from `typing` (Python < 3.9 compatibility).

## 6. Suggested Private Helper Functions

- `_build_reverse(edges, max_w, n)` — builds adjacency list of reversed edges filtered to weight ≤ max_w; returns `List[List[int]]`
- `_can_reach_all(rev_graph, n)` — BFS from node 0 on reversed graph; returns True if all n nodes visited
- `_binary_search(sorted_weights, n, edges, threshold)` — binary searches sorted_weights using feasibility check; returns minimum valid weight or -1