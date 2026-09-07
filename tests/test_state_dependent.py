"""Tests for state-dependent coding tree and stochastic-rate Merton problems."""
import math
import pytest
import numpy as np

from parabolab.library import vasicek_no_consumption_exact


def test_vasicek_no_consumption_terminal():
    """At terminal time t=T, F(T, y) must equal 1.0 identically."""
    T = 0.1
    for y in [-2.0, 0.0, 1.5]:
        val = vasicek_no_consumption_exact(t=T, y=y, T=T)
        assert val == pytest.approx(1.0, abs=1e-12)


def test_vasicek_no_consumption_properties():
    """Value must be strictly positive and smoothly varying with y."""
    T = 0.1
    y_vals = np.linspace(-2.0, 2.0, 5)
    vals = [vasicek_no_consumption_exact(t=0.0, y=y, T=T) for y in y_vals]
    assert all(v > 0 for v in vals)
    # Since a1 = (1-gamma)*eta > 0, higher y (higher interest rate) gives higher terminal wealth utility
    for i in range(len(vals) - 1):
        assert vals[i + 1] > vals[i]


def test_state_dependent_linear_potential():
    """u_t + (1/2) u_xx + x * u = 0 with u(T, x) = 1.
    Exact solution: u(t, x) = exp(x*(T-t) + (T-t)^3 / 6).
    """
    import sympy as sp
    from parabolab.state_dependent import StateDependentPDEnD
    from parabolab.tree import sample_tree

    xs = sp.symbols("x0:1")
    zs = sp.symbols("z0:1")
    T = 0.2
    pde = StateDependentPDEnD(
        T=T,
        d=1,
        deriv_map=((0,),),
        f_expr=xs[0] * zs[0],
        phi_expr=sp.Integer(1),
        name="test_linear_potential",
    )

    t, x_val = 0.0, 1.0
    tau = T - t
    exact = math.exp(x_val * tau + (tau**3) / 6.0)

    rng = np.random.default_rng(42)
    n_samples = 4000
    samples = [sample_tree(pde, t, np.array([x_val]), rng=rng, rate=2.0).value for _ in range(n_samples)]
    mc_mean = float(np.mean(samples))
    stderr = float(np.std(samples, ddof=1) / math.sqrt(n_samples))

    assert abs(mc_mean - exact) < 3.0 * stderr


def test_merton_vasicek_reduced_no_consumption():
    """CodingTreeMC on merton_vasicek_reduced matches exact closed form within error bars."""
    from parabolab.library import merton_vasicek_reduced, vasicek_no_consumption_exact
    from parabolab.tree import sample_tree

    pde = merton_vasicek_reduced(T=0.05, consumption=False)
    t, y_val = 0.0, 0.5
    exact = vasicek_no_consumption_exact(t=t, y=y_val, T=pde.T)

    rng = np.random.default_rng(123)
    n_samples = 3000
    samples = [sample_tree(pde, t, np.array([y_val]), rng=rng, rate=1.5).value for _ in range(n_samples)]
    mc_mean = float(np.mean(samples))
    stderr = float(np.std(samples, ddof=1) / math.sqrt(n_samples))

    assert abs(mc_mean - exact) < 3.5 * stderr


def test_merton_vasicek_reduced_with_consumption():
    """Smoke test: consumption term adds utility, positive finite values."""
    from parabolab.library import merton_vasicek_reduced
    from parabolab.tree import sample_tree

    pde = merton_vasicek_reduced(T=0.05, consumption=True)
    rng = np.random.default_rng(456)
    n_samples = 500
    samples = [sample_tree(pde, 0.0, np.array([0.0]), rng=rng, rate=2.0).value for _ in range(n_samples)]
    mc_mean = float(np.mean(samples))
    assert np.isfinite(mc_mean)
    assert mc_mean > 1.0  # with consumption and terminal=1, total value > 1.0


def test_merton_vasicek_2d_smoke():
    """2D full Merton problem: runs, produces finite estimate."""
    from parabolab.library import merton_vasicek_2d
    from parabolab.tree import sample_tree

    pde = merton_vasicek_2d(T=0.05, consumption=False)
    rng = np.random.default_rng(789)
    # wealth x=100, normalized rate y=0.0
    pt = np.array([100.0, 0.0])
    sample = sample_tree(pde, 0.0, pt, rng=rng, rate=1.0)
    assert np.isfinite(sample.value)
    assert sample.n_nodes >= 1


