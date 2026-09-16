"""Tests for the phi -> u operator backbones."""

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from parabolab.deep import opnet

GRID = np.linspace(-8.0, 8.0, 101)


def _batch(B=3, Q=7, seed=0):
    g = torch.Generator().manual_seed(seed)
    phi = torch.randn(B, 101, generator=g) * 0.5
    q = torch.cat([torch.zeros(B, Q, 1), -8 + 16 * torch.rand(B, Q, 1, generator=g)], -1)
    return phi, q


@pytest.mark.parametrize("name", ["deeponet", "fno", "attn"])
def test_operator_shapes_and_finite(name):
    torch.manual_seed(0)
    net = opnet.make_operator(name, GRID, **({"d_model": 16, "n_layers": 1} if name == "attn" else
                                            {"width": 8, "modes": 4, "n_layers": 2} if name == "fno" else
                                            {"p": 8, "width": 16}))
    phi, q = _batch()
    out = net(phi, q)
    assert out.shape == (3, 7) and torch.isfinite(out).all()
    assert net.n_params_total > 0


def test_fno_interpolation_reproduces_grid_values():
    torch.manual_seed(0)
    net = opnet.FNO1d(GRID, width=8, modes=4, n_layers=2).eval()
    phi, _ = _batch(B=2)
    q = torch.cat([torch.zeros(2, 101, 1), torch.as_tensor(GRID, dtype=torch.float32).expand(2, 101).unsqueeze(-1)], -1)
    with torch.no_grad():
        at_grid = net(phi, q)
        direct = net.on_grid(phi)
    torch.testing.assert_close(at_grid, direct, atol=1e-5, rtol=1e-5)


def test_attn_operator_permutation_invariant_in_phi_tokens():
    torch.manual_seed(0)
    net = opnet.AttnOperator(d_model=16, n_heads=2, n_layers=1).eval()
    phi, q = _batch(B=2)
    perm = torch.randperm(101)
    with torch.no_grad():
        a = net(phi, q)
        b = net.forward_tokens(torch.as_tensor(GRID, dtype=torch.float32)[perm].expand(2, 101), phi[:, perm], q)
    torch.testing.assert_close(a, b, atol=1e-5, rtol=1e-5)


@pytest.mark.parametrize("name", ["deeponet", "fno"])
def test_output_scaler_applies(name):
    torch.manual_seed(0)
    net = opnet.make_operator(name, GRID, **({"width": 8, "modes": 4, "n_layers": 2} if name == "fno" else {"p": 8, "width": 16})).eval()
    phi, q = _batch(B=2)
    with torch.no_grad():
        a = net(phi, q)
        net.out_mean.fill_(3.0); net.out_std.fill_(2.0)
        b = net(phi, q)
    torch.testing.assert_close(b, 2 * a + 3)


def test_make_operator_rejects_unknown():
    with pytest.raises(ValueError):
        opnet.make_operator("unet", GRID)


# ---------------------------------------------------------------------------
# training / evaluation
# ---------------------------------------------------------------------------

from parabolab.deep import corpus, optrain


def _toy(n=3, seed=41, family="heat_phi"):
    specs = corpus.sample_instances(family, n, seed, n_states=40, m_samples=20, n_draws=1)
    return [corpus.generate_instance(s, n_jobs=2) for s in specs]


def test_pooled_operator_rows_and_scalers():
    insts = _toy()
    rows = optrain.pooled_operator_rows(insts)
    assert rows["phi"].shape == (3, 101) and rows["tx"].shape[1] == 2
    assert rows["u"].shape == rows["inst_idx"].shape and rows["inst_idx"].max() == 2
    net = opnet.DeepONet(p=8, width=16)
    optrain.fit_operator_scalers(net, rows)
    assert float(net.phi_scale) == pytest.approx(rows["phi"].std())
    assert float(net.in_std[0]) == 1.0 and float(net.out_std) == pytest.approx(rows["u"].std())


def test_pooled_operator_rows_stays_within_sensor_grid():
    insts = _toy()
    rows = optrain.pooled_operator_rows(insts)
    grid = insts[0].grid
    assert rows["tx"][:, 1].min() >= grid[0] and rows["tx"][:, 1].max() <= grid[-1]


@pytest.mark.parametrize("name", ["deeponet", "fno", "attn"])
def test_train_operator_decreases_loss_and_evaluates(name):
    insts = _toy()
    torch.manual_seed(0)
    kw = {"attn": {"d_model": 16, "n_layers": 1}, "fno": {"width": 8, "modes": 4, "n_layers": 2},
          "deeponet": {"p": 8, "width": 16}}[name]
    net = opnet.make_operator(name, insts[0].grid, **kw)
    # steps=500, not the brief's 40: with only 3 toy instances and 16
    # samples/step, the raw per-step training-batch loss is dominated by
    # which 2-instance/8-query subset got drawn (batch-selection noise), not
    # by optimization progress -- AttnOperator in particular needs several
    # hundred steps before its loss (logged pre-update on that step's own
    # noisy batch) reliably drops below the initial value. 500 steps stays
    # under 2s/backbone and gives every backbone a comfortable margin.
    res = optrain.train_operator(net, insts, steps=500, batch_instances=2, n_query=8,
                                 lr=3e-3, log_every=10)
    assert np.isfinite(res.losses).all() and res.losses[-1] < res.losses[0]
    l1 = optrain.evaluate_operator(net, insts)
    assert l1.shape == (3,) and np.isfinite(l1).all()


def test_per_phi_baseline_runs():
    inst = _toy(n=1, seed=42)[0]
    assert np.isfinite(optrain.per_phi_baseline(inst, epochs=30))


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------

import csv
import subprocess
import sys
from pathlib import Path


def test_phi_operator_driver_tiny(tmp_path):
    script = Path(__file__).resolve().parents[1] / "examples" / "phi_operator.py"
    out = tmp_path / "res.csv"
    subprocess.run([sys.executable, str(script), "--family", "heat_phi", "--tiny", "--jobs", "1",
                    "--corpus-root", str(tmp_path / "corpus"), "--out", str(out)],
                   check=True, capture_output=True, text=True)
    rows = list(csv.DictReader(out.open()))
    assert {r["backbone"] for r in rows} == {"deeponet", "fno", "attn", "per_phi"}
    assert {int(r["n_train"]) for r in rows if r["backbone"] != "per_phi"} == {2, 3}
