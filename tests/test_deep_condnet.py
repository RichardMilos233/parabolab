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


# ---------------------------------------------------------------------------
# training / evaluation / referee
# ---------------------------------------------------------------------------

from parabolab.deep import condtrain, corpus


def _toy(n=3, n_states=30, m=20, seed=31, deriv=False):
    specs = corpus.sample_instances("merton", n, seed, n_states=n_states, m_samples=m,
                                    n_draws=1)
    if deriv:
        import dataclasses
        specs = [dataclasses.replace(s, deriv_codes=("Dx1", "Dx2")) for s in specs]
    return [corpus.generate_instance(s, n_jobs=2) for s in specs]


def test_merton_policy_referee():
    assert condtrain.merton_policy_exact((0.5, 0.03, 0.1)) == pytest.approx(6.0)
    from parabolab.library import merton_hjb_derivatives
    ux, uxx = merton_hjb_derivatives(T=0.1, mu=0.03, sigma=0.1, gamma=0.5, rho=0.01)
    x = np.array([120.0, 150.0])
    pol = condtrain.policy_from_derivatives(
        np.array([ux(0.0, [v]) for v in x]), np.array([uxx(0.0, [v]) for v in x]),
        x, 0.03, 0.1)
    np.testing.assert_allclose(pol, 6.0, rtol=1e-12)


def test_pooled_rows_and_scalers():
    insts = _toy()
    rows = condtrain.pooled_rows(insts)
    assert rows["tx"].shape[1] == 2 and rows["params"].shape[1] == 3
    assert rows["u"].shape[0] == rows["tx"].shape[0] <= 90
    assert "ux" not in rows
    from parabolab.deep.condnet import ConditionedNet
    net = ConditionedNet(d=1, n_params=3, hidden_layers=2, neurons=8)
    stats = condtrain.fit_conditioned_scalers(net, rows)
    assert float(net.in_std[0]) == 1.0                # t == 0 has no spread
    assert float(net.in_mean[1]) == pytest.approx(rows["tx"][:, 1].mean())
    assert float(net.out_std) == pytest.approx(rows["u"].std())
    assert stats == {"ux_std": 1.0, "uxx_std": 1.0}


def test_train_conditioned_u_only_and_evaluate():
    insts = _toy()
    from parabolab.deep.condnet import ConditionedNet
    torch.manual_seed(0)
    net = ConditionedNet(d=1, n_params=3, hidden_layers=2, neurons=8)
    res = condtrain.train_conditioned(net, insts, steps=30, batch_states=32,
                                      log_every=10, lr=3e-3)
    assert np.isfinite(res.losses).all() and res.losses[-1] < res.losses[0]
    out = condtrain.evaluate_conditioned(net, insts)
    assert len(out) == 3
    for m in out:
        assert set(m) == {"l1_u", "policy_err_interior", "policy_err_full"}
        assert all(np.isfinite(v) for v in m.values())


def test_train_conditioned_with_derivative_labels():
    insts = _toy(n=2, n_states=20, m=10, seed=32, deriv=True)
    rows = condtrain.pooled_rows(insts)
    assert "ux" in rows and "uxx" in rows
    from parabolab.deep.condnet import ConditionedNet
    net = ConditionedNet(d=1, n_params=3, hidden_layers=2, neurons=8)
    res = condtrain.train_conditioned(net, insts, steps=5, batch_states=16,
                                      loss_weights=(1.0, 1.0, 1.0))
    assert np.isfinite(res.losses).all()
    with pytest.raises(ValueError):
        condtrain.train_conditioned(net, _toy(n=1), steps=1,
                                    loss_weights=(1.0, 1.0, 0.0))


def test_per_instance_baseline_metrics():
    inst = _toy(n=1, n_states=60, m=20, seed=33)[0]
    m = condtrain.per_instance_baseline(inst, epochs=50)
    assert set(m) == {"l1_u", "policy_err_interior", "policy_err_full"}
    assert np.isfinite(m["l1_u"])
