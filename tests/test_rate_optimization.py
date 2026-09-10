"""Tests for deterministic rate derivatives and scalar rate optimizer."""

import math
import numpy as np
import pytest

from parabolab.mechanism import SemilinearMechanism
from parabolab.moments import finite_depth_moment_1d
from parabolab.pde import FullyNonlinearPDE1D, ParabolicPDE, x_symbol, z_symbols
from parabolab.rate_optimization import (
    finite_depth_moment_derivatives_1d,
    optimize_exponential_rate_1d,
    riccati_binary_second_moment,
)


def _binary_control_pde(T: float = 0.2) -> ParabolicPDE:
    # u_t + 1/2 u_xx + u^2 = 0 with phi == 1
    # Terminal phi = 1, f(u) = u^2
    # Leaf terminal = 1, tuples(Id()) = ((Id(), Id()),)
    import sympy as sp
    z = z_symbols(0)
    return FullyNonlinearPDE1D(
        n=0,
        f_expr=z[0] ** 2,
        phi_expr=sp.Integer(1),
        T=T,
    )


def test_leaf_rate_derivatives():
    # Depth 0: only leaf term V = e^{rate * T} * 1^2 = e^{rate * T}
    T = 0.3
    pde = _binary_control_pde(T=T)
    rate = 1.5
    res = finite_depth_moment_derivatives_1d(pde, 0.0, 0.0, max_depth=0, rate=rate)

    exact_val = math.exp(rate * T)
    exact_d1 = T * math.exp(rate * T)
    exact_d2 = (T**2) * math.exp(rate * T)

    assert res.value == pytest.approx(exact_val, rel=1e-8)
    assert res.d_rate == pytest.approx(exact_d1, rel=1e-8)
    assert res.d2_rate == pytest.approx(exact_d2, rel=1e-8)


def test_rate_derivatives_finite_difference():
    # Depth 1: check automatic derivatives against centered finite differences
    T = 0.15
    pde = _binary_control_pde(T=T)
    rate = 1.2
    eps = 1e-5

    res = finite_depth_moment_derivatives_1d(pde, 0.0, 0.0, max_depth=1, rate=rate)

    res_plus = finite_depth_moment_derivatives_1d(pde, 0.0, 0.0, max_depth=1, rate=rate + eps)
    res_minus = finite_depth_moment_derivatives_1d(pde, 0.0, 0.0, max_depth=1, rate=rate - eps)

    # First derivative central difference
    fd_d1 = (res_plus.value - res_minus.value) / (2.0 * eps)
    assert res.d_rate == pytest.approx(fd_d1, rel=1e-4)

    # Second derivative central difference
    fd_d2 = (res_plus.value - 2.0 * res.value + res_minus.value) / (eps**2)
    assert res.d2_rate == pytest.approx(fd_d2, rel=1e-4)


def test_rate_derivatives_match_moment_quadrature():
    # Verify that the value returned by finite_depth_moment_derivatives_1d
    # matches finite_depth_moment_1d(p=2.0)
    T = 0.2
    pde = _binary_control_pde(T=T)
    for depth in (0, 1, 2):
        for rate in (0.8, 1.4):
            v_ref = finite_depth_moment_1d(pde, 0.0, 0.0, max_depth=depth, rate=rate, p=2.0)
            res = finite_depth_moment_derivatives_1d(pde, 0.0, 0.0, max_depth=depth, rate=rate)
            assert res.value == pytest.approx(v_ref, rel=1e-8)


def test_riccati_binary_oracle():
    # Test riccati_binary_second_moment against exact Riccati ODE solution
    T = 0.1
    # For small T, rate=1.0: denom = 1 + 1 - e^{0.1} = 2 - 1.10517 = 0.89483 > 0
    val = riccati_binary_second_moment(T, 1.0)
    exact = math.exp(0.1) / (2.0 - math.exp(0.1))
    assert val == pytest.approx(exact, rel=1e-10)


def test_rate_optimizer_riccati_benchmark():
    # Test optimize_exponential_rate_1d against Riccati oracle for T = 0.05
    # For T = 0.05, the optimum satisfies 2(e^{rate * T} - 1) = T * rate * (rate^2 + 1)
    T = 0.05
    pde = _binary_control_pde(T=T)

    # Depth 1 optimization
    opt_res = optimize_exponential_rate_1d(pde, 0.0, 0.0, max_depth=1, bracket=(0.2, 3.0), tol=1e-6)
    assert opt_res.converged
    assert 0.8 < opt_res.rate < 1.3
    assert abs(opt_res.d_rate) < 1e-4

    # Verify that second derivative is strictly positive (strict convexity)
    assert opt_res.d2_rate > 0.0
