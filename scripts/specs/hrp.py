"""Canonical spec for Hierarchical Risk Parity (Lopez de Prado 2016).

Implement a module-level function:

    def hrp_weights(cov: np.ndarray) -> np.ndarray

Inputs:
    cov: NxN positive-semidefinite covariance matrix (np.ndarray).

Output:
    1-D numpy array of length N. Weights must:
      - Be non-negative (no short selling).
      - Sum to 1.0 (long-only fully invested).

Algorithm (Lopez de Prado 2016):
    1) Build correlation matrix from cov.
    2) Distance d_ij = sqrt(0.5 * (1 - corr_ij)).
    3) Hierarchical clustering on the distance matrix using SINGLE linkage.
       (You may use scipy.cluster.hierarchy.linkage; scipy is available.)
    4) Quasi-diagonalisation: reorder assets by their position in the
       dendrogram (leaf order).
    5) Recursive bisection: split the sorted asset list in halves; allocate
       weight by inverse-variance between the two clusters using
       alpha = 1 - V_left / (V_left + V_right), where V_x is the cluster
       variance under the inverse-variance portfolio of cluster x; recurse
       into each half until clusters are singletons.

Notes:
    - For a single asset (N=1) return np.array([1.0]).
    - For a perfectly diagonal cov (no correlations), the algorithm must
      reduce to inverse-variance weighting regardless of ordering.
"""
import math
import unittest

import numpy as np


def _isclose(a, b, abs_tol=1e-6):
    return math.isclose(float(a), float(b), abs_tol=abs_tol, rel_tol=0)


class TestHRP(unittest.TestCase):
    # ---- basic invariants ----
    def test_single_asset_returns_one(self):
        w = hrp_weights(np.array([[4.0]]))
        self.assertEqual(len(w), 1)
        self.assertTrue(_isclose(w[0], 1.0))

    def test_sum_to_one_small(self):
        cov = np.array([[1.0, 0.2, 0.1], [0.2, 1.0, 0.3], [0.1, 0.3, 1.0]])
        w = hrp_weights(cov)
        self.assertEqual(len(w), 3)
        self.assertTrue(_isclose(w.sum(), 1.0))

    def test_sum_to_one_larger(self):
        rng = np.random.default_rng(42)
        a = rng.standard_normal((6, 6))
        cov = a @ a.T + 0.5 * np.eye(6)
        w = hrp_weights(cov)
        self.assertEqual(len(w), 6)
        self.assertTrue(_isclose(w.sum(), 1.0))

    def test_nonnegative_weights(self):
        rng = np.random.default_rng(7)
        a = rng.standard_normal((5, 5))
        cov = a @ a.T + 0.5 * np.eye(5)
        w = hrp_weights(cov)
        self.assertTrue(np.all(w >= -1e-9))

    # ---- diagonal-cov reductions ----
    def test_diagonal_equal_variance_equal_weights(self):
        cov = np.eye(4) * 0.04   # all variances equal
        w = hrp_weights(cov)
        for x in w:
            self.assertTrue(_isclose(x, 0.25, abs_tol=1e-3))

    def test_diagonal_two_assets_inverse_variance(self):
        # var = [1, 4] → inverse-var weights [4, 1] / 5 = [0.8, 0.2]
        cov = np.diag([1.0, 4.0])
        w = hrp_weights(cov)
        self.assertTrue(_isclose(w[0], 0.8, abs_tol=1e-3))
        self.assertTrue(_isclose(w[1], 0.2, abs_tol=1e-3))

    def test_diagonal_four_assets_inverse_variance(self):
        # var = [1, 2, 4, 8] → inverse-var weights ∝ [1, 0.5, 0.25, 0.125]
        cov = np.diag([1.0, 2.0, 4.0, 8.0])
        w = hrp_weights(cov)
        ivp = 1.0 / np.diag(cov)
        ivp /= ivp.sum()
        for got, want in zip(w, ivp):
            self.assertTrue(_isclose(got, want, abs_tol=1e-3))

    # ---- structural ----
    def test_length_matches_cov(self):
        cov = np.eye(7) * 0.1
        w = hrp_weights(cov)
        self.assertEqual(len(w), 7)

    def test_higher_variance_gets_smaller_weight_diagonal(self):
        cov = np.diag([0.04, 0.16])           # var 4% vs 16%
        w = hrp_weights(cov)
        self.assertGreater(w[0], w[1])

    def test_correlated_pair_shares_weight_vs_uncorrelated_singleton(self):
        # 3 assets: assets 0 and 1 highly correlated (sigma=1 each), asset 2
        # uncorrelated (sigma=1). HRP should not let the correlated pair
        # collectively dominate vs the singleton.
        cov = np.array([
            [1.0, 0.95, 0.0],
            [0.95, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ])
        w = hrp_weights(cov)
        self.assertTrue(_isclose(w.sum(), 1.0))
        self.assertTrue(np.all(w >= -1e-9))
        # asset 2 alone should hold ~0.5 (top-level bisection 0.5/0.5)
        self.assertGreater(w[2], 0.4)
        self.assertLess(w[2], 0.6)

    def test_two_correlated_pair_split_equally_within_pair(self):
        # Asset 0 and 1 identical variance and high correlation → roughly
        # equal split within their cluster.
        cov = np.array([
            [1.0, 0.95, 0.0],
            [0.95, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ])
        w = hrp_weights(cov)
        self.assertTrue(_isclose(w[0], w[1], abs_tol=1e-3))

    def test_block_diagonal_two_clusters_equal_split(self):
        # Two independent blocks of size 2, each block internally identical.
        cov = np.array([
            [1.0, 0.9, 0.0, 0.0],
            [0.9, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.9],
            [0.0, 0.0, 0.9, 1.0],
        ])
        w = hrp_weights(cov)
        # Top split puts 0.5 in each block; within each block equal split.
        for x in w:
            self.assertTrue(_isclose(x, 0.25, abs_tol=1e-2))


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
