"""Tests for the deep branching solver (M4, JCP2024 Algorithm 2)."""

import functools

import numpy as np
import pytest

torch = pytest.importorskip("torch")

import parabolab as pl
import parabolab.deep as deep
from parabolab.library import allen_cahn_nd, merton_hjb


AC1 = functools.partial(allen_cahn_nd, d=1, T=0.5)


# ---------------------------------------------------------------------------
# batched generator
# ---------------------------------------------------------------------------

def test_generator_targets_are_unbiased_estimates():
    """Every MC target must agree with the exact solution within CLT error,
    and the outlier filter must keep essentially all Allen-Cahn samples."""
    data = deep.generate_training_data(
        AC1, n_states=20, m_samples=4000, seed=7, x_lo=-8.0, x_hi=8.0)
    pde = AC1()
    z = np.array([
        (data.y[i] - pde.exact_solution(data.t[i], data.x[i]))
        / data.stderr[i]
        for i in range(len(data))
    ])
    assert np.all(np.abs(z) < 4.5)
    assert abs(z.mean()) < 1.5  # ~N(0, 1/sqrt(20)) if unbiased
    assert np.all(data.n_kept >= 0.99 * data.m_samples)
    # states follow Remark 3.1 (vi): tau = 0, x in the overtrained segment
    assert np.all(data.t == 0.0)
    assert data.x[:, 0].min() >= -8.0 - 0.1 * 16.0
    assert data.x[:, 0].max() <= 8.0 + 0.1 * 16.0


def test_generator_independent_of_n_jobs():
    kw = dict(n_states=6, m_samples=50, seed=3, x_lo=-2.0, x_hi=2.0)
    a = deep.generate_training_data(AC1, n_jobs=1, **kw)
    b = deep.generate_training_data(AC1, n_jobs=2, **kw)
    np.testing.assert_array_equal(a.y, b.y)
    np.testing.assert_array_equal(a.x, b.x)


def test_generator_default_rate_is_jcp():
    data = deep.generate_training_data(
        AC1, n_states=2, m_samples=10, seed=0, x_lo=-1.0, x_hi=1.0)
    assert data.rate == pytest.approx(pl.jcp_rate(0.5))


def test_generator_supports_root_codes():
    """Rooting the trees at DxN(mu) yields E[H] = d^mu u -- checked on the
    Allen-Cahn traveling wave whose du/dx is known exactly."""
    import math

    from parabolab import DxN

    pde = AC1()
    data = deep.generate_training_data(
        AC1, n_states=8, m_samples=4000, seed=11, x_lo=-2.0, x_hi=2.0,
        code=DxN((1,)))

    def exact_dx(t, x):
        # u = -1/2 - tanh(3(T-t)/4 - x/2)/2 -> du/dx = sech^2(.)/4
        arg = 0.75 * (0.5 - t) - 0.5 * float(x[0])
        return 1.0 / (4.0 * math.cosh(arg) ** 2)

    z = np.array([
        (data.y[i] - exact_dx(data.t[i], data.x[i])) / data.stderr[i]
        for i in range(len(data))
    ])
    assert np.all(np.abs(z) < 4.5)


# ---------------------------------------------------------------------------
# network
# ---------------------------------------------------------------------------

def test_net_forward_shapes():
    net = deep.DeepBranchNet(d=3)
    out = net(torch.randn(7, 4))
    assert out.shape == (7,)
    # paper architecture: 6 hidden layers + output = 7 linears, 6 batchnorms
    assert len(net.linears) == 7
    assert len(net.bns) == 6


def test_net_eval_mode_single_point():
    net = deep.DeepBranchNet(d=1)
    net.eval()  # batchnorm must use running stats -> batch of 1 works
    out = net(torch.zeros(1, 2))
    assert out.shape == (1,)
    assert torch.isfinite(out).all()


def test_net_relu_variant():
    net = deep.DeepBranchNet(d=1, activation="relu", hidden_layers=3,
                             neurons=8)
    assert torch.isfinite(net(torch.randn(5, 2))).all()


# ---------------------------------------------------------------------------
# training loop
# ---------------------------------------------------------------------------

def test_training_smoke_allen_cahn():
    """Tiny-budget end-to-end run: loss must collapse and the net must be a
    reasonable u(0, .) on the grid."""
    torch.manual_seed(0)
    data = deep.generate_training_data(
        AC1, n_states=200, m_samples=400, seed=1, x_lo=-8.0, x_hi=8.0)
    net = deep.DeepBranchNet(d=1)
    res = deep.train_deep_branching(net, data, epochs=400)
    assert res.losses[-1] < 0.1 * res.losses[0]
    l1, l2, *_ = deep.grid_errors(net, AC1(), x_lo=-8.0, x_hi=8.0)
    assert l1 < 0.05


def test_training_skips_nonfinite_targets():
    data = deep.generate_training_data(
        AC1, n_states=30, m_samples=50, seed=2, x_lo=-2.0, x_hi=2.0)
    data.y[5] = np.nan
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=8)
    res = deep.train_deep_branching(net, data, epochs=20)
    assert np.isfinite(res.losses).all()


# ---------------------------------------------------------------------------
# Merton HJB (new library entry, non-polynomial f)
# ---------------------------------------------------------------------------

def test_merton_terminal_matches_exact():
    pde = merton_hjb()
    for x in (100.0, 150.0, 200.0):
        assert pde.exact_solution(pde.T, [x]) == pytest.approx(
            pde.phi_mu((0,))(x), rel=1e-12)


def test_merton_mc_vs_exact():
    pde = merton_hjb()
    for t, x in [(0.0, 150.0), (0.05, 120.0)]:
        r = pl.estimate(pde, t, np.array([x]), 8000, seed=5,
                        rate=pl.jcp_rate(pde.T))
        exact = pde.exact_solution(t, [x])
        assert abs(r.estimate - exact) < 4 * r.stderr


# ---------------------------------------------------------------------------
# slow reduced-budget reproductions
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_table1_allen_cahn_d1_reduced():
    res = deep.run_experiment(
        AC1, x_lo=-8.0, x_hi=8.0, n_states=1000, m_samples=10_000,
        epochs=3000, n_runs=1, n_jobs=4, seed0=10, verbose=False)
    # paper (M=100,000): L1 1.32e-3; reduced budget must stay within 10x
    assert res.l1[0] < 1.5e-2


@pytest.mark.slow
def test_table5_merton_reduced_and_consistency(tmp_path):
    res = deep.run_experiment(
        merton_hjb, x_lo=100.0, x_hi=200.0, n_states=1000,
        m_samples=1000, epochs=3000, n_runs=1, n_jobs=4, seed0=50,
        verbose=False)
    # paper (M=10,000): L1 8.49e-3; reduced budget must stay within ~20x
    assert res.l1[0] < 1.5e-1
    out = tmp_path / "fig7.png"
    deep.consistency_plot(res.data[0], res.nets[0], merton_hjb(), out,
                          title="fig7 smoke", x_lo=100.0, x_hi=200.0)
    assert out.exists()
