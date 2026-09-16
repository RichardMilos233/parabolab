"""Tests for rate variance analysis tools and PDE benchmark library entries."""

import math
from pathlib import Path

import pytest
import numpy as np

from parabolab import (
    compare_rate_variance,
    riccati_binary_optimal_rate,
    short_time_rate_1d,
    sweep_rate_variance,
)
from parabolab.library import (
    allen_cahn_wave_1d,
    binary_control_1d,
    fisher_kpp_1d,
)
from parabolab.moments import MomentQuadrature


def test_fisher_kpp_1d():
    pde = fisher_kpp_1d(T=0.05, phi0=0.5)
    assert pde.T == 0.05
    assert pde.phi(0.0) == 0.5
    # Exact solution at t=0
    # tau = 0.05, c = 1.0, u(0) = e^{0.05} / (1 + e^{0.05})
    expected_u0 = math.exp(0.05) / (1.0 + math.exp(0.05))
    assert pde.exact_solution(0.0, 0.0) == pytest.approx(expected_u0, rel=1e-12)

    # Theoretical rate: |f(0.5)| / |0.5| = (0.5 - 0.25) / 0.5 = 0.50
    rate_th = short_time_rate_1d(pde, 0.0)
    assert rate_th == pytest.approx(0.50, rel=1e-12)


def test_binary_control_1d():
    pde = binary_control_1d(T=0.05)
    assert pde.T == 0.05
    assert pde.exact_solution(0.0, 0.0) == pytest.approx(1.0 / (1.0 - 0.05), rel=1e-12)
    assert short_time_rate_1d(pde, 0.0) == pytest.approx(1.0, rel=1e-12)

    # Test riccati_binary_optimal_rate
    r_opt = riccati_binary_optimal_rate(0.05)
    assert r_opt == pytest.approx(1.025756, rel=1e-4)


def test_sweep_rate_variance_fast(tmp_path):
    pde = allen_cahn_wave_1d(T=0.05)
    sweep = sweep_rate_variance(
        pde,
        x=0.0,
        n_samples=200,
        n_mc_points=3,
        n_quad_points=6,
        quadrature=MomentQuadrature(time_order=2, normal_order=2),
        title="(a) Fast Test",
    )

    assert sweep.x == 0.0
    assert sweep.lambda_theory == pytest.approx(0.75, rel=1e-6)
    assert sweep.optimal_rate > 0.0
    assert len(sweep.quad_rates) == 6
    assert len(sweep.mc_rates) == 3
    assert len(sweep.mc_variance) == 3
    assert all(v >= 0.0 for v in sweep.mc_variance)

    # Test single-panel plot
    out_single = tmp_path / "single.png"
    sweep.plot(path=out_single)
    assert out_single.exists() and out_single.stat().st_size > 0


def test_compare_rate_variance_table_and_plot(tmp_path):
    pde1 = allen_cahn_wave_1d(T=0.05)
    pde2 = binary_control_1d(T=0.05)

    s1 = sweep_rate_variance(
        pde1, x=0.0, n_samples=100, n_mc_points=2, n_quad_points=5,
        quadrature=MomentQuadrature(time_order=2, normal_order=2),
        title="(a) AC Fast",
    )
    s2 = sweep_rate_variance(
        pde2, x=0.0, use_riccati=True, n_samples=100, n_mc_points=2, n_quad_points=5,
        title="(b) Binary Fast",
    )

    comp = compare_rate_variance(s1, s2)
    # Check chaining table and plot
    out_comp = tmp_path / "comp.png"
    comp.table().plot(path=out_comp)

    assert out_comp.exists() and out_comp.stat().st_size > 0
