"""Tests for deterministic rate derivatives and scalar rate optimizer."""

import math
import numpy as np
import pytest

from examples.exponential_rate_sweet_spot import (
    BinaryControlMechanism,
    _binary_control_experiment,
    _binary_control_pde,
    _binary_oracle_optimum,
)
from parabolab.moments import MomentQuadrature, finite_depth_moment_1d
from parabolab.rate_optimization import (
    finite_depth_moment_derivatives_1d,
    optimize_exponential_rate_1d,
    riccati_binary_second_moment,
    short_time_rate_1d,
)


BINARY_SETTINGS = dict(
    mechanism=BinaryControlMechanism,
    quadrature=MomentQuadrature(time_order=8, normal_order=1),
)


def test_leaf_rate_derivatives():
    # Depth 0: only leaf term V = e^{rate * T} * 1^2 = e^{rate * T}
    T = 0.3
    pde = _binary_control_pde(T=T)
    rate = 1.5
    res = finite_depth_moment_derivatives_1d(
        pde, 0.0, 0.0, max_depth=0, rate=rate, **BINARY_SETTINGS)

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

    res = finite_depth_moment_derivatives_1d(
        pde, 0.0, 0.0, max_depth=1, rate=rate, **BINARY_SETTINGS)

    res_plus = finite_depth_moment_derivatives_1d(
        pde, 0.0, 0.0, max_depth=1, rate=rate + eps, **BINARY_SETTINGS)
    res_minus = finite_depth_moment_derivatives_1d(
        pde, 0.0, 0.0, max_depth=1, rate=rate - eps, **BINARY_SETTINGS)

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
            v_ref = finite_depth_moment_1d(
                pde, 0.0, 0.0, max_depth=depth, rate=rate, p=2.0, **BINARY_SETTINGS)
            res = finite_depth_moment_derivatives_1d(
                pde, 0.0, 0.0, max_depth=depth, rate=rate, **BINARY_SETTINGS)
            assert res.value == pytest.approx(v_ref, rel=1e-8)


def test_riccati_binary_oracle():
    # Test riccati_binary_second_moment against exact Riccati ODE solution
    T = 0.1
    # For small T, rate=1.0: denom = 1 + 1 - e^{0.1} = 2 - 1.10517 = 0.89483 > 0
    val = riccati_binary_second_moment(T, 1.0)
    exact = math.exp(0.1) / (2.0 - math.exp(0.1))
    assert val == pytest.approx(exact, rel=1e-10)


@pytest.mark.parametrize("rate", [0.6, 1.0, 2.0])
def test_riccati_oracle_satisfies_binary_first_event_identity(rate):
    # Independent first-event integral: the oracle must match this estimator's
    # binary continuation product, not merely the same PDE's solution.
    T = 0.15
    nodes, weights = np.polynomial.legendre.leggauss(32)
    lifetimes = T * (nodes + 1.0) / 2.0
    branch = T / 2.0 * sum(
        weight * math.exp(rate * s) / rate
        * riccati_binary_second_moment(T - s, rate)**2
        for s, weight in zip(lifetimes, weights)
    )
    assert riccati_binary_second_moment(T, rate) == pytest.approx(
        math.exp(rate * T) + branch, rel=1e-12)


def test_binary_depth_one_matches_closed_integral():
    T, rate = 0.15, 1.3
    result = finite_depth_moment_derivatives_1d(
        _binary_control_pde(T), 0.0, 0.0, max_depth=1, rate=rate,
        **BINARY_SETTINGS)
    exact = math.exp(rate * T) * (1.0 + math.expm1(rate * T) / rate**2)
    assert result.value == pytest.approx(exact, rel=1e-12)


@pytest.mark.parametrize("rate", [0.8, 1.3])
def test_binary_cutoff_moments_converge_upwards_to_full_tree(rate):
    T = 0.1
    oracle = riccati_binary_second_moment(T, rate)
    values = [finite_depth_moment_derivatives_1d(
        _binary_control_pde(T), 0.0, 0.0, max_depth=depth, rate=rate,
        mechanism=BinaryControlMechanism,
        quadrature=MomentQuadrature(time_order=4, normal_order=1),
    ).value for depth in range(5)]
    assert all(left < right < oracle for left, right in zip(values, values[1:]))
    assert oracle - values[-1] < 2e-5


def test_rate_optimizer_riccati_benchmark():
    # Test optimize_exponential_rate_1d against Riccati oracle for T = 0.05
    # For T = 0.05, the optimum satisfies 2(e^{rate * T} - 1) = T * rate * (rate^2 + 1)
    T = 0.05
    pde = _binary_control_pde(T=T)

    # Finite-depth optimization approximates, but does not equal, the optimum
    # of the exact full-tree second moment.
    opt_res = optimize_exponential_rate_1d(
        pde, 0.0, 0.0, max_depth=2, bracket=(0.2, 3.0), tol=1e-9,
        **BINARY_SETTINGS)
    oracle_rate = _binary_oracle_optimum(T)
    assert opt_res.converged
    assert opt_res.rate == pytest.approx(oracle_rate, abs=0.01)
    assert abs(opt_res.rate - oracle_rate) > 1e-5
    assert abs(opt_res.d_rate) < 1e-4

    # Verify that second derivative is strictly positive (strict convexity)
    assert opt_res.d2_rate > 0.0


def test_binary_report_compares_rates_on_the_same_objective():
    T = 0.15
    _, record = _binary_control_experiment(T)
    assert record["full_tree_jcp_second_moment"] == pytest.approx(
        riccati_binary_second_moment(T, record["jcp_rate"]))
    assert record["full_tree_at_finite_depth_rate"] == pytest.approx(
        riccati_binary_second_moment(T, record["finite_depth_optimal_rate"]))
    assert record["finite_depth_optimal_second_moment"] < record["full_tree_at_finite_depth_rate"]
    assert record["full_tree_optimal_second_moment"] < record["full_tree_at_finite_depth_rate"]
    assert record["full_tree_optimal_rate"] > record["finite_depth_optimal_rate"]


def test_rate_optimization_monte_carlo_agreement():
    # Compare deterministic second moment at rate* against Monte Carlo sample second moment
    from parabolab.tree import sample_tree

    T = 0.05
    pde = _binary_control_pde(T=T)
    rate = 1.05  # near the optimum
    det_res = finite_depth_moment_derivatives_1d(
        pde, 0.0, 0.0, max_depth=1, rate=rate, **BINARY_SETTINGS
    )

    n_samples = 40_000
    rng = np.random.default_rng(20260910)
    samples_sq = np.empty(n_samples)
    for i in range(n_samples):
        s = sample_tree(
            pde,
            0.0,
            0.0,
            rng=rng,
            rate=rate,
            mechanism=BinaryControlMechanism,
            max_depth=1,
        )
        samples_sq[i] = s.value**2

    emp_mean = float(np.mean(samples_sq))
    emp_stderr = float(np.std(samples_sq, ddof=1) / math.sqrt(n_samples))

    assert abs(emp_mean - det_res.value) <= 4.0 * emp_stderr


def test_rate_optimizer_short_horizon_asymptotics():
    # As T -> 0, lambda*(T) -> sqrt(B / G) = 1.0 for binary control u^2 with phi == 1
    pde_short = _binary_control_pde(T=0.01)
    opt = optimize_exponential_rate_1d(
        pde_short, 0.0, 0.0, max_depth=1, bracket=(0.5, 2.0), tol=1e-5,
        **BINARY_SETTINGS)
    assert opt.converged
    # Should be close to 1.0 within O(T)
    assert opt.rate == pytest.approx(1.0, abs=0.03)


def test_short_time_rate_1d_evaluations():
    from parabolab.library import allen_cahn_wave_1d, allen_cahn_flat

    # Binary control with phi == 1, f(u) = u^2: |f(phi)| / |phi| = 1/1 = 1.0
    pde_bin = _binary_control_pde(T=0.05)
    r_bin = short_time_rate_1d(pde_bin, 0.0, mechanism=BinaryControlMechanism)
    assert r_bin == pytest.approx(1.0, rel=1e-12)

    # Allen-Cahn wave at x = 0: phi(0) = -0.5, f(-0.5) = -0.375 => 0.375 / 0.5 = 0.75
    pde_ac = allen_cahn_wave_1d(T=0.05)
    r_ac = short_time_rate_1d(pde_ac, 0.0)
    assert r_ac == pytest.approx(0.75, rel=1e-12)

    # Check across multiple x points matches |f(phi(x))| / |phi(x)|
    for x in (-1.5, -0.5, 0.0, 0.5, 1.5):
        val_phi = float(pde_ac.phi(x))
        val_f = float(pde_ac.f(val_phi))
        expected = abs(val_f) / abs(val_phi)
        assert short_time_rate_1d(pde_ac, x) == pytest.approx(expected, rel=1e-12)

    # Allen-Cahn flat: phi == 0.5, f(0.5) = 0.375 => 0.75
    pde_flat = allen_cahn_flat(T=0.05)
    assert short_time_rate_1d(pde_flat, 0.0) == pytest.approx(0.75, rel=1e-12)


def test_short_time_rate_allen_cahn_convergence():
    from parabolab.library import allen_cahn_wave_1d

    # Verify that as T -> 0, the numerical optimizer converges to short_time_rate_1d(x=0) = 0.75
    theoretical_rate = 0.75
    rates = []
    for T in (0.1, 0.05, 0.02, 0.01):
        pde = allen_cahn_wave_1d(T=T)
        opt = optimize_exponential_rate_1d(
            pde, 0.0, 0.0, max_depth=2, bracket=(0.2, 2.0),
            quadrature=MomentQuadrature(time_order=6, normal_order=6),
        )
        assert opt.converged
        rates.append(opt.rate)

    # Errors should strictly decrease towards 0.75
    errors = [abs(r - theoretical_rate) for r in rates]
    for e1, e2 in zip(errors, errors[1:]):
        assert e2 < e1
    # At T=0.01, error is under 1%
    assert abs(rates[-1] - theoretical_rate) / theoretical_rate < 0.01


def test_short_time_rate_fisher_kpp():
    from parabolab.pde import ParabolicPDE

    # Fisher-KPP: f(u) = u(1 - u) = u - u^2, phi0 = 0.5
    # f(0.5) = 0.25 => lambda = 0.25 / 0.5 = 0.50
    pde_kpp = ParabolicPDE(
        T=0.05,
        f=lambda z: z - z**2,
        f_derivatives=[lambda z: 1.0 - 2.0 * z, lambda z: -2.0],
        phi=lambda x: 0.5,
        phi_derivatives=[lambda x: 0.0],
    )
    th_rate = short_time_rate_1d(pde_kpp, 0.0)
    assert th_rate == pytest.approx(0.5, rel=1e-12)

    opt = optimize_exponential_rate_1d(
        pde_kpp, 0.0, 0.0, max_depth=2, bracket=(0.1, 1.5),
        quadrature=MomentQuadrature(time_order=4, normal_order=4),
    )
    assert opt.converged
    # Discrepancy is within 2% at T = 0.05
    assert abs(opt.rate - th_rate) / th_rate < 0.02

