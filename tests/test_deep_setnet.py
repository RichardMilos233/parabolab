"""Tests for the set-to-field denoiser."""

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from parabolab.deep.setnet import SetDenoiser


def _batch(B=2, N=12, Q=5, d=1, P=2, seed=0):
    g = torch.Generator().manual_seed(seed)
    ctx_tx = torch.cat([torch.zeros(B, N, 1), torch.randn(B, N, d, generator=g)], -1)
    ctx_y = torch.randn(B, N, generator=g) * 3 + 20
    ctx_se = torch.rand(B, N, generator=g) * 0.1
    params = torch.rand(B, P, generator=g)
    q_tx = torch.cat([torch.zeros(B, Q, 1), torch.randn(B, Q, d, generator=g)], -1)
    return ctx_tx, ctx_y, ctx_se, params, q_tx


def test_output_shape_and_finite():
    torch.manual_seed(0)
    net = SetDenoiser(d=1, n_params=2, d_model=16, n_heads=2, n_layers=1)
    out = net(*_batch())
    assert out.shape == (2, 5)
    assert torch.isfinite(out).all()
    assert net.n_params_total > 0


def test_context_permutation_invariance():
    torch.manual_seed(0)
    net = SetDenoiser(d=1, n_params=2, d_model=16, n_heads=2, n_layers=2).eval()
    ctx_tx, ctx_y, ctx_se, params, q_tx = _batch()
    perm = torch.randperm(ctx_tx.shape[1])
    with torch.no_grad():
        a = net(ctx_tx, ctx_y, ctx_se, params, q_tx)
        b = net(ctx_tx[:, perm], ctx_y[:, perm], ctx_se[:, perm], params, q_tx)
    torch.testing.assert_close(a, b, atol=1e-5, rtol=1e-5)


def test_scale_and_shift_equivariance_in_y():
    torch.manual_seed(0)
    net = SetDenoiser(d=1, n_params=2, d_model=16, n_heads=2, n_layers=2).eval()
    ctx_tx, ctx_y, ctx_se, params, q_tx = _batch()
    with torch.no_grad():
        a = net(ctx_tx, ctx_y, ctx_se, params, q_tx)
        b = net(ctx_tx, 7 * ctx_y + 3, 7 * ctx_se, params, q_tx)
    torch.testing.assert_close(b, 7 * a + 3, atol=1e-4, rtol=1e-4)


def test_context_stats_and_param_buffers():
    net = SetDenoiser(d=1, n_params=2, d_model=16, n_heads=2, n_layers=1,
                      param_mean=[0.5, 1.0], param_std=[0.25, 2.0])
    assert net.param_mean.tolist() == [0.5, 1.0]
    assert "param_std" in net.state_dict()
    _, ctx_y, *_ = _batch()
    mu, s = net.context_stats(ctx_y)
    assert mu.shape == (2, 1) and s.shape == (2, 1)
    torch.testing.assert_close(mu[:, 0], ctx_y.mean(1))


def test_constant_t_column_does_not_produce_nan():
    net = SetDenoiser(d=1, n_params=1, d_model=16, n_heads=2, n_layers=1)
    ctx_tx, ctx_y, ctx_se, _, q_tx = _batch(P=1)
    out = net(ctx_tx, ctx_y, ctx_se, torch.zeros(2, 1), q_tx)   # t == 0 everywhere
    assert torch.isfinite(out).all()


# ---------------------------------------------------------------------------
# training / evaluation / baselines
# ---------------------------------------------------------------------------

from parabolab.deep import corpus, settrain


def _toy_corpus(n=4, n_states=40, m=4, seed=11):
    specs = corpus.sample_instances("ac1", n, seed, n_states=n_states, m_samples=m)
    return [corpus.generate_instance(s) for s in specs]


def test_train_set_denoiser_decreases_loss_and_evaluates():
    insts = _toy_corpus()
    torch.manual_seed(0)
    net = SetDenoiser(d=1, n_params=2, d_model=16, n_heads=2, n_layers=1)
    res = settrain.train_set_denoiser(
        net, insts, steps=30, batch_instances=2, n_context=16, n_query=8,
        log_every=10, lr=1e-3)
    assert np.isfinite(res.losses).all()
    assert res.losses[-1] < res.losses[0]
    l1 = settrain.evaluate_set_denoiser(net, insts, n_context=16)
    assert l1.shape == (4,) and np.isfinite(l1).all()


def test_train_set_denoiser_exact_target_and_bad_target():
    insts = _toy_corpus(n=2)
    net = SetDenoiser(d=1, n_params=2, d_model=16, n_heads=2, n_layers=1)
    res = settrain.train_set_denoiser(net, insts, steps=3, batch_instances=2,
                                      n_context=8, n_query=4, target="exact")
    assert np.isfinite(res.losses).all()
    with pytest.raises(ValueError):
        settrain.train_set_denoiser(net, insts, steps=1, target="mse")


def test_per_instance_mlp_baseline_runs():
    inst = _toy_corpus(n=1, n_states=60, m=20)[0]
    l1 = settrain.per_instance_mlp_l1(inst, epochs=50)
    assert np.isfinite(l1) and l1 < 1.0


def test_kernel_smoother_recovers_noiseless_instance():
    inst = _toy_corpus(n=1, n_states=1000, m=2)[0]
    inst.y[0] = inst.u_exact                     # no noise
    inst.stderr[0] = 1e-3
    assert settrain.kernel_smoother_l1(inst) < 5e-3


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------

import csv
import subprocess
import sys
from pathlib import Path


def test_gonogo_driver_tiny(tmp_path):
    script = Path(__file__).resolve().parents[1] / "examples" / "set_denoiser_gonogo.py"
    out = tmp_path / "res.csv"
    subprocess.run(
        [sys.executable, str(script), "--family", "ac1", "--tiny",
         "--corpus-root", str(tmp_path / "corpus"), "--out", str(out),
         "--jobs", "1"],
        check=True, capture_output=True, text=True)
    rows = list(csv.DictReader(out.open()))
    methods = {r["method"] for r in rows}
    assert methods == {"d04_n2n", "d04_exact", "mlp_M", "mlp_10M", "kernel"}
    assert all(float(r["l1"]) >= 0 for r in rows)
    assert sum(r["method"] == "kernel" for r in rows) == 2   # 2 test instances
