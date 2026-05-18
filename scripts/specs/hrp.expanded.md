# HRP Implementation Guide

## 1. Required Function Signatures

```python
def hrp_weights(cov: np.ndarray) -> np.ndarray
```

## 2. Algorithm Steps

**Step 1 – Correlation & Distance Matrix**
- `std = sqrt(diag(cov))`
- `corr[i,j] = cov[i,j] / (std[i] * std[j])`
- `dist[i,j] = sqrt(0.5 * (1 - corr[i,j]))` — result is symmetric, diagonal=0

**Step 2 – Hierarchical Clustering**
- Condense the NxN distance matrix to a 1-D condensed form via `squareform(dist)`
- Call `linkage(condensed, method='single')`

**Step 3 – Quasi-Diagonalisation (Leaf Order)**
- Extract the ordered leaf list from the linkage matrix using `leaves_list(Z)` (scipy)
- This gives a permutation `order` of asset indices [0..N-1]

**Step 4 – Recursive Bisection**
- Start with weights `w = np.ones(N)`; maintain the full weight array indexed by original asset indices
- Recursively bisect the `order` list:
  1. Split into `left = order[:mid]`, `right = order[mid:]` where `mid = len(order)//2`
  2. Compute `V_left = _cluster_var(cov, left)`, `V_right = _cluster_var(cov, right)`
  3. `alpha = 1 - V_left / (V_left + V_right)`
  4. Scale `w[left] *= alpha`, `w[right] *= (1 - alpha)`
  5. Recurse on left and right until singleton
- Base case: list length == 1, nothing to do

**Cluster Variance (`_cluster_var`):**
- Sub-covariance = `cov[np.ix_(cluster, cluster)]`
- IVP weights within cluster: `ivp = (1/diag) / sum(1/diag)`
- Cluster variance = `ivp.T @ subcov @ ivp`

## 3. Required Imports

```python
import numpy as np
from scipy.cluster.hierarchy import linkage, leaves_list
from scipy.spatial.distance import squareform
```

## 4. Key Edge Cases

| Case | Strategy |
|------|----------|
| N=1 | Return `np.array([1.0])` immediately before any clustering |
| Diagonal cov (no correlation) | All distances equal → arbitrary but consistent leaf order; bisection must still yield exact IVP — verify `_cluster_var` uses IVP correctly |
| Perfectly correlated pair | Distance ≈ 0; clustering correctly groups them first; equal variance → equal split within cluster |
| Block-diagonal | Two blocks cluster separately; top bisection splits 50/50 |

## 5. Common Pitfalls

- **`squareform` rejects non-zero diagonals**: `dist` diagonal should be exactly 0. Use `np.fill_diagonal(dist, 0.0)` before calling `squareform`.
- **`squareform` also rejects non-symmetric matrices**: ensure `dist = (dist + dist.T) / 2` if float noise creeps in.
- **Correlation clipping**: floating-point can push `corr[i,j]` slightly outside [-1,1], making `dist` imaginary. Clip: `np.clip(corr, -1.0, 1.0)`.
- **`leaves_list` not `to_tree`**: use `leaves_list(Z)` directly — it returns the leaf order as a flat array. Don't manually traverse the tree.
- **`alpha` formula direction**: `alpha = 1 - V_left/(V_left+V_right)` means LEFT gets `alpha` and RIGHT gets `1-alpha`. Verify sign: higher-variance cluster receives *less* weight (1-alpha < alpha when V_left > V_right). ✓
- **In-place weight scaling**: multiply `w[indices] *= factor` using original asset indices throughout recursion, not positional indices into the sub-list.
- **Zero variance asset**: if any diagonal entry is 0, IVP division blows up. Guard with `np.maximum(diag, 1e-12)`.

## 6. Suggested Private Helper Functions

```python
def _corr_from_cov(cov) -> np.ndarray
    # Returns NxN correlation matrix; clips to [-1,1]; zeros diagonal exactly

def _dist_matrix(corr) -> np.ndarray
    # Returns sqrt(0.5*(1-corr)); fills diagonal with 0; symmetrises

def _cluster_var(cov, cluster_indices) -> float
    # Extracts sub-cov, computes IVP weights, returns scalar portfolio variance

def _recursive_bisect(w, cov, order) -> None
    # Mutates w in-place; base case len(order)==1; splits and recurses
```