# Implementation Guide: CRR American Option Pricing

## 1. Required Function Signatures

```python
def crr_american(S, K, T, r, sigma, N, option_type='put') -> float
```

## 2. Algorithm Steps

```
1. Handle T=0 edge case: return intrinsic immediately.
2. dt = T / N
3. u = exp(sigma * sqrt(dt))
4. d = 1 / u
5. p = (exp(r*dt) - d) / (u - d)
6. disc = exp(-r*dt)
7. Build terminal stock prices array (length N+1):
       S_i = S * u^(N-i) * d^i  for i in 0..N
8. Compute terminal payoffs array V (length N+1):
       call: max(S_i - K, 0)
       put:  max(K - S_i, 0)
9. Backward induction: for j = N-1 downto 0:
       for i = 0..j:
           continuation = disc * (p * V[i] + (1-p) * V[i+1])
           stock_at_node = S * u^(j-i) * d^i
           exercise = intrinsic(stock_at_node)
           V[i] = max(continuation, exercise)
10. Return V[0].
```

## 3. Required Imports

```python
import math
```

No numpy required; pure Python is sufficient and avoids vectorization pitfalls.

## 4. Key Edge Cases

| Case | Strategy |
|---|---|
| `T=0` | Return `max(S-K, 0)` or `max(K-S, 0)` before computing `dt` (avoids `sqrt(0)` issues and division in `p`). |
| `N=1` | General algorithm handles it naturally; no special case needed. |
| Deep ITM put | Backward induction must enforce early-exercise at every interior node, not just the terminal layer. |
| OTM call/put | Payoff correctly floored at 0 via `max(..., 0)`. |

## 5. Common Pitfalls

1. **T=0 not handled first**: Computing `u = exp(sigma*sqrt(0))=1` gives `u=d=1`, making `(u-d)=0` → division by zero in `p`. Guard with `if T == 0` at the top.

2. **Wrong indexing direction in V**: The standard convention is `V[i]` = node with `i` down-moves. After one backward step, `V[i] = disc*(p*V[i] + (1-p)*V[i+1])`. If you reverse this, results are wrong silently.

3. **Forgetting early exercise at interior nodes**: Computing only `disc*(p*Vup + (1-p)*Vdn)` without `max(continuation, intrinsic)` gives a European price. The American premium test will fail.

4. **Recomputing stock price at interior nodes**: Don't reuse terminal stock prices for intrinsic during backward induction. At backward step `j`, node `i` has stock price `S * u^(j-i) * d^i`.

5. **Using numpy arrays carelessly**: If you use `np.maximum`, ensure shapes match. Pure Python `max()` on scalars is safer and equally fast for this algorithm.

6. **Float precision in `p`**: For extreme parameters, `p` can fall outside `(0,1)`. This is a model validity issue, not a bug—but don't add a clamp unless tests require it.

7. **American call early exercise**: For no-dividend stocks, early exercise is never optimal, so American call ≈ European call. The algorithm naturally produces this if implemented correctly—do not hard-code this assumption.

## 6. Suggested Private Helper Functions

```python
def _intrinsic(S_node, K, option_type):
    """Returns max(S-K,0) for call or max(K-S,0) for put at a given node."""

def _terminal_prices(S, u, d, N):
    """Returns list of N+1 terminal stock prices: S*u^(N-i)*d^i for i=0..N."""

def _terminal_payoffs(prices, K, option_type):
    """Applies _intrinsic to each terminal price, returns list of floats."""
```

These keep the main function's backward-induction loop clean and each piece independently testable.