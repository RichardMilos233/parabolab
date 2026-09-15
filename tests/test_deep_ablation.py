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
