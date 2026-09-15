"""Tests for the parameter-conditioned net and its autograd derivatives."""

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from parabolab.deep.condnet import ConditionedNet, autograd_derivatives


def _inputs(B=7, d=1, P=3, seed=0):
    g = torch.Generator().manual_seed(seed)
    tx = torch.cat([torch.zeros(B, 1), 100 + 100 * torch.rand(B, d, generator=g)], -1)
    params = torch.rand(B, P, generator=g)
    return tx, params


@pytest.mark.parametrize("mode", ["concat", "film"])
def test_forward_shape_and_finite(mode):
    net = ConditionedNet(d=1, n_params=3, mode=mode, hidden_layers=2, neurons=8)
    tx, p = _inputs()
    out = net(tx, p)
    assert out.shape == (7,) and torch.isfinite(out).all()
    assert net.n_params_total > 0


def test_bad_mode_raises():
    with pytest.raises(ValueError):
        ConditionedNet(d=1, n_params=3, mode="hyper")


def test_film_head_is_zero_initialised_so_params_are_ignored_at_init():
    torch.manual_seed(0)
    net = ConditionedNet(d=1, n_params=3, mode="film", hidden_layers=3, neurons=8)
    tx, p = _inputs()
    a = net(tx, p)
    b = net(tx, torch.zeros_like(p))
    torch.testing.assert_close(a, b)


def test_concat_depends_on_params():
    torch.manual_seed(0)
    net = ConditionedNet(d=1, n_params=3, mode="concat", hidden_layers=3, neurons=8)
    tx, p = _inputs()
    assert not torch.allclose(net(tx, p), net(tx, torch.zeros_like(p)))


def test_scaler_buffers_exist_and_apply():
    net = ConditionedNet(d=1, n_params=2, hidden_layers=2, neurons=4,
                         param_mean=[0.5, 0.5], param_std=[0.25, 0.25])
    sd = net.state_dict()
    for key in ("in_mean", "in_std", "out_mean", "out_std", "param_mean", "param_std"):
        assert key in sd
    net.out_mean.fill_(3.0); net.out_std.fill_(2.0)
    tx, p = _inputs(P=2)
    a = net(tx, p)
    net.out_mean.fill_(0.0); net.out_std.fill_(1.0)
    b = net(tx, p)
    torch.testing.assert_close(a, 2 * b + 3)


@pytest.mark.parametrize("mode", ["concat", "film"])
def test_autograd_derivatives_match_finite_differences(mode):
    torch.manual_seed(1)
    net = ConditionedNet(d=1, n_params=3, mode=mode, hidden_layers=3, neurons=16).double()
    tx, p = _inputs()
    tx, p = tx.double(), p.double()
    fn = lambda z: net(z, p)
    u, ux, uxx = autograd_derivatives(fn, tx)
    assert u.shape == ux.shape == uxx.shape == (7,)
    # h = 1e-2, not the brief's 1e-3: at this net's init (unscaled inputs of
    # magnitude 100-200 saturate GELU into a near-affine regime) the true
    # curvature is O(1e-7), and central-difference float64 roundoff at
    # h = 1e-3 (~eps*|u|/h^2 ~ 1e-8) is the same order as the signal --
    # confirmed by an h-sweep where uxx sits at the bottom of the classic
    # truncation/roundoff V and the FD estimate converges to it as h grows.
    # h = 1e-2 keeps truncation error negligible while clearing the
    # roundoff floor with margin (see p3-task-2-report.md).
    h = 1e-2
    tp = tx.clone(); tp[:, 1] += h
    tm = tx.clone(); tm[:, 1] -= h
    with torch.no_grad():
        up, um, u0 = net(tp, p), net(tm, p), net(tx, p)
    torch.testing.assert_close(ux, (up - um) / (2 * h), rtol=1e-3, atol=1e-8)
    torch.testing.assert_close(uxx, (up - 2 * u0 + um) / h ** 2, rtol=1e-2, atol=1e-8)


def test_autograd_derivatives_create_graph_allows_backward():
    net = ConditionedNet(d=1, n_params=3, hidden_layers=2, neurons=8)
    tx, p = _inputs()
    _, ux, uxx = autograd_derivatives(lambda z: net(z, p), tx, create_graph=True)
    (ux.sum() + uxx.sum()).backward()
    assert any(q.grad is not None for q in net.parameters())
