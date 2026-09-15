"""Tests for the deep-branching network ablation harness."""

import dataclasses
import functools

import numpy as np
import pytest

torch = pytest.importorskip("torch")

import parabolab.deep as deep
from parabolab.deep import datasets
from parabolab.library import allen_cahn_nd

AC1 = functools.partial(allen_cahn_nd, d=1, T=0.5)

TINY = datasets.DatasetSpec(
    key="tiny", factory_name="allen_cahn_nd",
    factory_kwargs=(("d", 1), ("T", 0.5)),
    x_lo=-1.0, x_hi=1.0, n_states=8, m_samples=4, seed=0,
)


# ---------------------------------------------------------------------------
# datasets
# ---------------------------------------------------------------------------

def test_benchmarks_resolve_to_library_factories():
    for key, spec in datasets.BENCHMARKS.items():
        assert spec.key == key
        pde = spec.factory()()
        assert getattr(pde, "d", 1) == 1
        assert spec.x_lo < spec.x_hi


def test_load_or_generate_roundtrips_bit_identically(tmp_path):
    a = datasets.load_or_generate(TINY, tmp_path)
    assert datasets.dataset_path(TINY, tmp_path).exists()
    b = datasets.load_or_generate(TINY, tmp_path)
    for field in ("t", "x", "y", "stderr", "n_kept"):
        np.testing.assert_array_equal(getattr(a, field), getattr(b, field))
    assert b.m_samples == a.m_samples and b.rate == a.rate
    direct = deep.generate_training_data(
        AC1, n_states=8, m_samples=4, seed=0, x_lo=-1.0, x_hi=1.0)
    np.testing.assert_array_equal(a.y, direct.y)


def test_load_rejects_mismatched_spec(tmp_path):
    datasets.load_or_generate(TINY, tmp_path)
    other = dataclasses.replace(TINY, m_samples=5)   # same key/seed -> same file
    with pytest.raises(ValueError, match="spec"):
        datasets.load_or_generate(other, tmp_path)


def test_corrupt_file_is_regenerated(tmp_path):
    a = datasets.load_or_generate(TINY, tmp_path)
    datasets.dataset_path(TINY, tmp_path).write_bytes(b"not an npz")
    b = datasets.load_or_generate(TINY, tmp_path)
    np.testing.assert_array_equal(a.y, b.y)


def test_factory_is_picklable():
    import pickle
    pickle.dumps(TINY.factory())


# ---------------------------------------------------------------------------
# net
# ---------------------------------------------------------------------------

REF_NET_OUT = [-0.99196023, -0.75105441]   # from Step 1, current main net


def _ref_input():
    return torch.tensor([[0.0, 0.3, -1.2], [0.1, 2.0, 0.5]])


def test_default_net_is_unchanged():
    torch.manual_seed(123)
    net = deep.DeepBranchNet(d=2)
    net.eval()
    out = net(_ref_input())
    np.testing.assert_allclose(out.detach().numpy(), REF_NET_OUT, rtol=0,
                               atol=1e-7)


@pytest.mark.parametrize("norm", ["batch", "layer", "none"])
@pytest.mark.parametrize("act", ["tanh", "relu", "id", "silu", "gelu", "sin"])
def test_net_variants_forward(norm, act):
    net = deep.DeepBranchNet(d=1, hidden_layers=3, neurons=8, norm=norm,
                             activation=act)
    out = net(torch.randn(5, 2))
    assert out.shape == (5,)
    assert torch.isfinite(out).all()
    net.eval()
    assert torch.isfinite(net(torch.zeros(1, 2))).all()


def test_norm_none_matches_batch_norm_false():
    torch.manual_seed(1)
    a = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=4, batch_norm=False)
    torch.manual_seed(1)
    b = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=4, norm="none")
    x = torch.randn(3, 2)
    torch.testing.assert_close(a(x), b(x))


def test_fourier_features_change_input_width():
    net = deep.DeepBranchNet(d=2, hidden_layers=2, neurons=4,
                             fourier_features=8)
    assert net.linears[0].in_features == 1 + 2 * 8
    assert net.fourier_B.shape == (2, 8)
    assert torch.isfinite(net(torch.randn(3, 3))).all()


def test_scalers_are_buffers_and_roundtrip():
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=4,
                             scale_input=True, scale_output=True)
    net.in_mean.copy_(torch.tensor([0.0, 150.0]))
    net.in_std.copy_(torch.tensor([1.0, 30.0]))
    net.out_mean.fill_(2.0)
    net.out_std.fill_(0.5)
    sd = net.state_dict()
    for key in ("in_mean", "in_std", "out_mean", "out_std"):
        assert key in sd
    other = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=4,
                               scale_input=True, scale_output=True)
    other.load_state_dict(sd)
    x = torch.tensor([[0.0, 120.0], [0.0, 180.0]])
    net.eval(); other.eval()
    torch.testing.assert_close(net(x), other(x))


def test_n_params_counts_trainable():
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=4, norm="none")
    # Linear(2,4)=12, Linear(4,4)=20, Linear(4,1)=5
    assert net.n_params == 37


# ---------------------------------------------------------------------------
# trainer
# ---------------------------------------------------------------------------

REF_LOSSES = [0.36384511, 0.09250513, 0.0514994, 0.04659879]   # from Step 1, current main trainer


def _small_data(seed=5):
    return deep.generate_training_data(
        AC1, n_states=16, m_samples=8, seed=seed, x_lo=-2.0, x_hi=2.0)


def test_default_training_is_unchanged():
    data = _small_data()
    torch.manual_seed(7)
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
    res = deep.train_deep_branching(net, data, epochs=30, log_every=10)
    np.testing.assert_allclose(res.losses, REF_LOSSES, rtol=0, atol=1e-7)


def test_fit_scalers_fills_buffers_and_leaves_t_alone():
    data = _small_data()
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6,
                             scale_input=True, scale_output=True)
    deep.fit_scalers(net, data)
    assert float(net.in_std[0]) == 1.0          # tau == 0 has zero spread
    assert float(net.in_mean[1]) == pytest.approx(data.x[:, 0].mean())
    assert float(net.in_std[1]) == pytest.approx(data.x[:, 0].std())
    assert float(net.out_mean) == pytest.approx(data.y.mean())
    assert float(net.out_std) == pytest.approx(data.y.std())


def test_fit_scalers_is_noop_without_flags():
    data = _small_data()
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
    deep.fit_scalers(net, data)
    assert torch.all(net.in_mean == 0) and torch.all(net.in_std == 1)


def test_weighted_mse_with_equal_stderr_equals_mse():
    data = _small_data()
    data.stderr[:] = 0.3
    torch.manual_seed(7)
    a = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
    ra = deep.train_deep_branching(a, data, epochs=20, log_every=5,
                                   loss="mse")
    torch.manual_seed(7)
    b = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
    rb = deep.train_deep_branching(b, data, epochs=20, log_every=5,
                                   loss="weighted_mse")
    np.testing.assert_allclose(ra.losses, rb.losses, rtol=1e-6)


def test_weighted_mse_ignores_infinite_stderr_rows():
    data = _small_data()
    data.stderr[3] = np.inf
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
    res = deep.train_deep_branching(net, data, epochs=10, loss="weighted_mse")
    assert np.isfinite(res.losses).all()


def test_weighted_mse_requires_a_finite_stderr():
    data = _small_data()
    data.stderr[:] = np.inf
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
    with pytest.raises(ValueError, match="finite stderr"):
        deep.train_deep_branching(net, data, epochs=1, loss="weighted_mse")


def test_weighted_mse_zero_stderr_rows_get_finite_weight():
    data = _small_data()
    data.stderr[:] = 0.0
    data.stderr[-2:] = 0.5
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
    res = deep.train_deep_branching(net, data, epochs=5, loss="weighted_mse")
    assert np.isfinite(res.losses).all()


def test_cosine_schedule_and_grad_clip_run():
    data = _small_data()
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
    res = deep.train_deep_branching(net, data, epochs=10, schedule="cosine",
                                    grad_clip=1.0)
    assert np.isfinite(res.losses).all()


def test_lbfgs_polish_does_not_increase_loss():
    data = _small_data()
    torch.manual_seed(7)
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6, norm="none")
    res = deep.train_deep_branching(net, data, epochs=30, log_every=10,
                                    lbfgs_steps=20)
    assert len(res.losses) == 5                 # 4 Adam logs + 1 L-BFGS
    assert res.losses[-1] <= res.losses[-2] + 1e-12


def test_lbfgs_polish_leaves_batchnorm_running_stats_alone():
    data = _small_data()

    def train(lbfgs_steps):
        torch.manual_seed(7)
        net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
        deep.train_deep_branching(net, data, epochs=30, lbfgs_steps=lbfgs_steps)
        return net

    plain, polished = train(0), train(20)
    for a, b in zip(plain.bns, polished.bns):
        torch.testing.assert_close(a.running_mean, b.running_mean)
        torch.testing.assert_close(a.running_var, b.running_var)
    finite = np.isfinite(data.y)
    tx = torch.tensor(np.column_stack([data.t[finite], data.x[finite]]),
                      dtype=torch.float32)
    y = torch.tensor(data.y[finite], dtype=torch.float32)
    with torch.no_grad():
        plain.eval(); polished.eval()
        before = float(torch.mean((plain(tx) - y) ** 2))
        after = float(torch.mean((polished(tx) - y) ** 2))
    assert after <= before + 1e-12


def test_unknown_loss_or_schedule_raises():
    data = _small_data()
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
    with pytest.raises(ValueError):
        deep.train_deep_branching(net, data, epochs=1, loss="huber")
    with pytest.raises(ValueError):
        deep.train_deep_branching(net, data, epochs=1, schedule="step")
