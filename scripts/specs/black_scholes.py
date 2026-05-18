"""Canonical spec for Black-Scholes pricer + Greeks + implied vol solver.

The implementation must define these 5 module-level functions:

    def bs_price(S, K, T, r, sigma, option_type='call') -> float
    def bs_delta(S, K, T, r, sigma, option_type='call') -> float
    def bs_gamma(S, K, T, r, sigma) -> float
    def bs_vega(S, K, T, r, sigma) -> float
    def implied_vol(price, S, K, T, r, option_type='call') -> float

Conventions:
- All inputs are floats. S = spot, K = strike, T = time to expiry (years),
  r = risk-free rate (continuous, e.g. 0.05 for 5%), sigma = volatility
  (annualised stdev of log returns, e.g. 0.2 for 20%).
- option_type is the lowercase string 'call' or 'put'.
- vega is per unit change in sigma (NOT per 1%): a 0.01 bump in sigma
  changes price by approximately vega * 0.01.
- gamma and vega are identical for call and put at same params.
- implied_vol must solve to within 1e-6 absolute on sigma.
- T = 0 returns intrinsic value (S - K)+ for call, (K - S)+ for put.
"""
import math
import unittest


class TestBlackScholes(unittest.TestCase):
    # ---- canonical reference values (Hull, 9th ed, Chapter 14) ----
    def test_call_price_hull(self):
        # S=42, K=40, r=0.10, T=0.5, sigma=0.20 → call = 4.7594
        self.assertAlmostEqual(bs_price(42, 40, 0.5, 0.10, 0.20, "call"), 4.7594, places=3)

    def test_put_price_hull(self):
        # Same params → put = 0.8086
        self.assertAlmostEqual(bs_price(42, 40, 0.5, 0.10, 0.20, "put"), 0.8086, places=3)

    def test_atm_call_zero_rate(self):
        # S=K=100, r=0, T=1, sigma=0.2 → 7.9656 (standard textbook ATM)
        self.assertAlmostEqual(bs_price(100, 100, 1.0, 0.0, 0.2, "call"), 7.9656, places=3)

    def test_atm_put_equals_atm_call_when_r_zero(self):
        c = bs_price(100, 100, 1.0, 0.0, 0.2, "call")
        p = bs_price(100, 100, 1.0, 0.0, 0.2, "put")
        self.assertAlmostEqual(c, p, places=6)

    # ---- put-call parity: C - P = S - K * exp(-rT) ----
    def test_put_call_parity_1(self):
        S, K, T, r, s = 100, 95, 0.75, 0.05, 0.30
        c = bs_price(S, K, T, r, s, "call")
        p = bs_price(S, K, T, r, s, "put")
        self.assertAlmostEqual(c - p, S - K * math.exp(-r * T), places=6)

    def test_put_call_parity_2(self):
        S, K, T, r, s = 50, 60, 0.25, 0.02, 0.45
        c = bs_price(S, K, T, r, s, "call")
        p = bs_price(S, K, T, r, s, "put")
        self.assertAlmostEqual(c - p, S - K * math.exp(-r * T), places=6)

    # ---- intrinsic at expiry ----
    def test_call_at_expiry_itm(self):
        self.assertAlmostEqual(bs_price(110, 100, 0.0, 0.05, 0.2, "call"), 10.0, places=6)

    def test_call_at_expiry_otm(self):
        self.assertAlmostEqual(bs_price(90, 100, 0.0, 0.05, 0.2, "call"), 0.0, places=6)

    def test_put_at_expiry_itm(self):
        self.assertAlmostEqual(bs_price(90, 100, 0.0, 0.05, 0.2, "put"), 10.0, places=6)

    # ---- Greeks ----
    def test_call_delta_atm_zero_rate(self):
        # Φ(0.1) ≈ 0.539828
        self.assertAlmostEqual(bs_delta(100, 100, 1.0, 0.0, 0.2, "call"), 0.539828, places=4)

    def test_put_delta_equals_call_delta_minus_1(self):
        S, K, T, r, s = 100, 95, 0.5, 0.05, 0.25
        cd = bs_delta(S, K, T, r, s, "call")
        pd = bs_delta(S, K, T, r, s, "put")
        self.assertAlmostEqual(pd, cd - 1.0, places=6)

    def test_delta_bounds(self):
        self.assertTrue(0.0 < bs_delta(100, 100, 1.0, 0.05, 0.2, "call") < 1.0)
        self.assertTrue(-1.0 < bs_delta(100, 100, 1.0, 0.05, 0.2, "put") < 0.0)

    def test_gamma_positive_and_call_eq_put(self):
        S, K, T, r, s = 105, 100, 0.5, 0.03, 0.22
        g = bs_gamma(S, K, T, r, s)
        self.assertGreater(g, 0.0)

    def test_vega_positive_and_correct_scale(self):
        # Numerically: a 0.01 sigma bump should ≈ change price by vega * 0.01.
        S, K, T, r, s = 100, 100, 1.0, 0.0, 0.2
        v = bs_vega(S, K, T, r, s)
        eps = 1e-4
        dp = (
            bs_price(S, K, T, r, s + eps, "call")
            - bs_price(S, K, T, r, s - eps, "call")
        ) / (2 * eps)
        self.assertAlmostEqual(v, dp, places=2)

    # ---- implied vol round-trips ----
    def test_iv_roundtrip_atm_call(self):
        S, K, T, r, sigma = 100, 100, 1.0, 0.0, 0.2
        price = bs_price(S, K, T, r, sigma, "call")
        iv = implied_vol(price, S, K, T, r, "call")
        self.assertAlmostEqual(iv, sigma, places=4)

    def test_iv_roundtrip_high_vol_call(self):
        S, K, T, r, sigma = 100, 100, 0.5, 0.02, 0.80
        price = bs_price(S, K, T, r, sigma, "call")
        iv = implied_vol(price, S, K, T, r, "call")
        self.assertAlmostEqual(iv, sigma, places=4)

    def test_iv_roundtrip_otm_put(self):
        S, K, T, r, sigma = 95, 100, 0.5, 0.03, 0.30
        price = bs_price(S, K, T, r, sigma, "put")
        iv = implied_vol(price, S, K, T, r, "put")
        self.assertAlmostEqual(iv, sigma, places=4)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
