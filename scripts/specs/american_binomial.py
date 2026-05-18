"""Canonical spec for American option pricing via Cox-Ross-Rubinstein binomial tree.

Implement one module-level function:

    def crr_american(S, K, T, r, sigma, N, option_type='put') -> float

Inputs:
    S: spot price
    K: strike
    T: time to expiry in years
    r: continuous risk-free rate (e.g. 0.05 for 5%)
    sigma: annualised volatility (e.g. 0.2 for 20%)
    N: number of time steps in the binomial tree (>= 1)
    option_type: 'call' or 'put'

Output:
    The American option fair value as a float.

Algorithm (CRR):
    dt = T / N
    u  = exp(sigma * sqrt(dt))
    d  = 1 / u
    p  = (exp(r*dt) - d) / (u - d)        # risk-neutral up-prob
    disc = exp(-r*dt)
    Terminal stock prices: S_i = S * u^(N-i) * d^i for i = 0..N
    Terminal payoffs:
        call: max(S_i - K, 0)
        put:  max(K - S_i, 0)
    Backward induction (j = N-1 down to 0):
        continuation V_i = disc * (p * V_up_i + (1-p) * V_dn_i)
        exercise    E_i = intrinsic at node i
        V_i = max(continuation, E_i)            # American: early-exercise allowed
    Return V_0.

Edge cases:
    - T = 0 → return intrinsic value.
    - N = 1 → single-step tree.
"""
import math
import unittest


class TestCRRAmerican(unittest.TestCase):
    # ---- intrinsic at expiry ----
    def test_T_zero_call_itm(self):
        self.assertAlmostEqual(crr_american(110, 100, 0.0, 0.05, 0.2, 50, "call"), 10.0, places=6)

    def test_T_zero_call_otm(self):
        self.assertAlmostEqual(crr_american(90, 100, 0.0, 0.05, 0.2, 50, "call"), 0.0, places=6)

    def test_T_zero_put_itm(self):
        self.assertAlmostEqual(crr_american(90, 100, 0.0, 0.05, 0.2, 50, "put"), 10.0, places=6)

    # ---- American call on a non-dividend stock ≈ European call (BS) ----
    # BS call(100, 100, 1, 0.05, 0.2) ≈ 10.4506
    def test_american_call_no_div_matches_bs_atm(self):
        v = crr_american(100, 100, 1.0, 0.05, 0.2, 500, "call")
        self.assertAlmostEqual(v, 10.4506, places=1)

    def test_american_call_no_div_matches_bs_itm(self):
        # BS call(110, 100, 1, 0.05, 0.2) ≈ 17.6630
        v = crr_american(110, 100, 1.0, 0.05, 0.2, 500, "call")
        self.assertAlmostEqual(v, 17.6630, places=1)

    # ---- American put has early-exercise premium over European ----
    # BS put(100, 100, 1, 0.05, 0.2) ≈ 5.5735; American > European.
    def test_american_put_premium_over_european_atm(self):
        v_am = crr_american(100, 100, 1.0, 0.05, 0.2, 500, "put")
        v_eu = 5.5735
        self.assertGreater(v_am, v_eu - 0.01)
        # Premium is non-trivial but bounded.
        self.assertLess(v_am - v_eu, 1.0)

    # ---- Deep ITM American put ≈ intrinsic K - S (very small time value) ----
    def test_deep_itm_put_near_intrinsic(self):
        v = crr_american(50, 100, 1.0, 0.05, 0.2, 500, "put")
        intrinsic = 100 - 50
        self.assertGreaterEqual(v, intrinsic - 1e-6)
        self.assertLess(v - intrinsic, 2.0)   # close to intrinsic

    # ---- Deep OTM near zero ----
    def test_deep_otm_call_near_zero(self):
        v = crr_american(50, 100, 0.5, 0.05, 0.2, 200, "call")
        self.assertGreaterEqual(v, 0.0)
        self.assertLess(v, 0.5)

    # ---- Monotonicity ----
    def test_vega_monotonic_call(self):
        a = crr_american(100, 100, 1.0, 0.05, 0.15, 200, "call")
        b = crr_american(100, 100, 1.0, 0.05, 0.30, 200, "call")
        self.assertLess(a, b)

    def test_put_value_decreasing_in_S(self):
        a = crr_american(90,  100, 1.0, 0.05, 0.2, 200, "put")
        b = crr_american(100, 100, 1.0, 0.05, 0.2, 200, "put")
        c = crr_american(110, 100, 1.0, 0.05, 0.2, 200, "put")
        self.assertGreater(a, b)
        self.assertGreater(b, c)

    # ---- Convergence: doubling N should not move the answer much ----
    def test_convergence_doubling_steps(self):
        v1 = crr_american(100, 100, 1.0, 0.05, 0.2, 200, "put")
        v2 = crr_american(100, 100, 1.0, 0.05, 0.2, 400, "put")
        self.assertLess(abs(v1 - v2), 0.05)

    # ---- N=1 single-step tree exact analytic check ----
    def test_single_step_call(self):
        # S=100, K=100, T=1, r=0, sigma=0.2, N=1 (call has no early exercise advantage)
        S, K, T, r, sigma = 100, 100, 1.0, 0.0, 0.2
        N = 1
        dt = T / N
        u = math.exp(sigma * math.sqrt(dt))
        d = 1 / u
        p = (math.exp(r * dt) - d) / (u - d)
        disc = math.exp(-r * dt)
        # call payoff at expiry on each terminal node
        c_up = max(S * u - K, 0)
        c_dn = max(S * d - K, 0)
        expected = disc * (p * c_up + (1 - p) * c_dn)
        v = crr_american(S, K, T, r, sigma, N, "call")
        self.assertAlmostEqual(v, expected, places=6)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
