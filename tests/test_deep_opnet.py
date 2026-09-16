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
    cond = torch.randn(B, 3)
    return phi, q, cond


@pytest.mark.parametrize("name", ["deeponet", "fno", "attn"])
def test_operator_shapes_and_finite(name):
    torch.manual_seed(0)
    net = opnet.make_operator(name, GRID, n_cond=3, **({"d_model": 16, "n_layers": 1} if name == "attn" else
                                            {"width": 8, "modes": 4, "n_layers": 2} if name == "fno" else
                                            {"p": 8, "width": 16}))
    phi, q, cond = _batch()
    out = net(phi, cond, q)
    assert out.shape == (3, 7) and torch.isfinite(out).all()
    assert net.n_params_total > 0


def test_fno_interpolation_reproduces_grid_values():
    torch.manual_seed(0)
    net = opnet.FNO1d(GRID, n_cond=3, width=8, modes=4, n_layers=2).eval()
    phi, _, cond = _batch(B=2)
    q = torch.cat([torch.zeros(2, 101, 1), torch.as_tensor(GRID, dtype=torch.float32).expand(2, 101).unsqueeze(-1)], -1)
    with torch.no_grad():
        at_grid = net(phi, cond, q)
        direct = net.on_grid(phi, cond)
    torch.testing.assert_close(at_grid, direct, atol=1e-5, rtol=1e-5)


def test_attn_operator_permutation_invariant_in_phi_tokens():
    torch.manual_seed(0)
    net = opnet.AttnOperator(n_cond=3, d_model=16, n_heads=2, n_layers=1).eval()
    phi, q, cond = _batch(B=2)
    perm = torch.randperm(101)
    with torch.no_grad():
        a = net(phi, cond, q)
        b = net.forward_tokens(torch.as_tensor(GRID, dtype=torch.float32)[perm].expand(2, 101), phi[:, perm], cond, q)
    torch.testing.assert_close(a, b, atol=1e-5, rtol=1e-5)


@pytest.mark.parametrize("name", ["deeponet", "fno"])
def test_output_scaler_applies(name):
    torch.manual_seed(0)
    net = opnet.make_operator(name, GRID, n_cond=3, **({"width": 8, "modes": 4, "n_layers": 2} if name == "fno" else {"p": 8, "width": 16})).eval()
    phi, q, cond = _batch(B=2)
    with torch.no_grad():
        a = net(phi, cond, q)
        net.out_mean.fill_(3.0); net.out_std.fill_(2.0)
        b = net(phi, cond, q)
    torch.testing.assert_close(b, 2 * a + 3)


def test_make_operator_rejects_unknown():
    with pytest.raises(ValueError):
        opnet.make_operator("unet", GRID, n_cond=0)


def test_coeffmlp_ignores_phi_and_uses_cond():
    # ConditionedNet zero-inits its FiLM output layer (see condnet.py), so a
    # freshly constructed CoeffMLP is exactly cond-invariant (that's covered
    # separately below). Perturb the FiLM output layer by hand to exercise
    # the cond-dependent path this test is actually about.
    torch.manual_seed(0)
    net = opnet.CoeffMLP(n_cond=3, hidden_layers=2, neurons=8).eval()
    with torch.no_grad():
        torch.nn.init.normal_(net.core.film[-1].weight)
    phi, q = _batch(B=2)[0], _batch(B=2)[1]
    cond = torch.randn(2, 3)
    with torch.no_grad():
        a = net(phi, cond, q); b = net(torch.zeros_like(phi), cond, q)
        c = net(phi, cond + 1.0, q)
    torch.testing.assert_close(a, b)
    assert not torch.allclose(a, c)


def test_coeffmlp_fresh_is_cond_invariant():
    # ConditionedNet's zero-initialised FiLM output layer means a freshly
    # constructed CoeffMLP starts as the plain, cond-invariant trunk -- it
    # only starts depending on cond once trained (or, as in the test above,
    # once the FiLM layer is perturbed by hand).
    torch.manual_seed(0)
    net = opnet.CoeffMLP(n_cond=3, hidden_layers=2, neurons=8).eval()
    phi, q = _batch(B=2)[0], _batch(B=2)[1]
    with torch.no_grad():
        a = net(phi, torch.zeros(2, 3), q)
        b = net(phi, torch.randn(2, 3), q)
    torch.testing.assert_close(a, b)


@pytest.mark.parametrize("name", ["deeponet", "fno", "attn", "coeffmlp"])
def test_operators_depend_on_cond(name):
    torch.manual_seed(0)
    kw = {"attn": {"d_model": 16, "n_layers": 1}, "fno": {"width": 8, "modes": 4, "n_layers": 2},
          "deeponet": {"p": 8, "width": 16}, "coeffmlp": {"hidden_layers": 2, "neurons": 8}}[name]
    net = opnet.make_operator(name, GRID, n_cond=2, **kw).eval()
    if name == "coeffmlp":
        # see test_coeffmlp_fresh_is_cond_invariant: a fresh CoeffMLP is
        # cond-invariant by construction, so perturb the FiLM output layer
        # to exercise the cond-dependent path.
        with torch.no_grad():
            torch.nn.init.normal_(net.core.film[-1].weight)
    phi, q = _batch(B=2)[0], _batch(B=2)[1]
    with torch.no_grad():
        a = net(phi, torch.zeros(2, 2), q); b = net(phi, torch.ones(2, 2), q)
    assert not torch.allclose(a, b)


def test_operators_accept_zero_cond():
    net = opnet.make_operator("attn", GRID, n_cond=0, d_model=16, n_layers=1)
    phi, q = _batch(B=2)[0], _batch(B=2)[1]
    assert torch.isfinite(net(phi, torch.zeros(2, 0), q)).all()


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
    n_cond = len(insts[0].spec.params)
    assert rows["cond"].shape == (3, n_cond)
    net = opnet.DeepONet(n_cond=n_cond, p=8, width=16)
    optrain.fit_operator_scalers(net, rows)
    assert float(net.phi_scale) == pytest.approx(rows["phi"].std())
    assert float(net.in_std[0]) == 1.0 and float(net.out_std) == pytest.approx(rows["u"].std())


def test_fit_operator_scalers_fills_coeffmlp_core():
    # CoeffMLP.forward ignores its own outer cond_*/in_*/out_*/phi_scale
    # buffers (ConditionedNet scales (t, x)/u/cond through its own core.*
    # buffers instead), so fit_operator_scalers must land the fitted
    # statistics in net.core.* and leave the outer buffers at identity.
    insts = _toy()
    rows = optrain.pooled_operator_rows(insts)
    n_cond = len(insts[0].spec.params)
    net = opnet.CoeffMLP(n_cond=n_cond, hidden_layers=2, neurons=8)
    optrain.fit_operator_scalers(net, rows)
    assert not torch.allclose(net.core.param_std, torch.ones(n_cond))
    assert torch.allclose(net.cond_std, torch.ones(n_cond))


def test_pooled_operator_rows_stays_within_sensor_grid():
    insts = _toy()
    rows = optrain.pooled_operator_rows(insts)
    grid = insts[0].grid
    assert rows["tx"][:, 1].min() >= grid[0] and rows["tx"][:, 1].max() <= grid[-1]


@pytest.mark.parametrize("name", ["deeponet", "fno", "attn", "coeffmlp"])
def test_train_operator_decreases_loss_and_evaluates(name):
    insts = _toy()
    torch.manual_seed(0)
    kw = {"attn": {"d_model": 16, "n_layers": 1}, "fno": {"width": 8, "modes": 4, "n_layers": 2},
          "deeponet": {"p": 8, "width": 16}, "coeffmlp": {"hidden_layers": 2, "neurons": 8}}[name]
    n_cond = len(insts[0].spec.params)
    net = opnet.make_operator(name, insts[0].grid, n_cond=n_cond, **kw)
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


def test_per_phi_baseline_works_without_closed_form():
    """ac_phi has no exact_solution; the baseline must score against u_grid."""
    inst = _toy(n=1, seed=43, family="ac_phi")[0]
    assert np.isfinite(optrain.per_phi_baseline(inst, epochs=30))


# ---------------------------------------------------------------------------
# calibration pre-check
# ---------------------------------------------------------------------------


def test_calibration_precheck_smoke():
    result = optrain.calibration_precheck("heat_phi", n=2, n_states=10, m_lo=20, m_hi=200)
    assert {"frac_within_4se", "stderr_ratio", "passed"} <= result.keys()
    assert isinstance(result["passed"], bool)


def test_precheck_draws_are_independent():
    # Regression test for the nested-sample bug: calling generate_instance
    # twice with the same seed and different m_samples gave the SAME label
    # seed (1000*spec.seed + draw 0) for both budgets, so the hi-budget run
    # started with the lo-budget run's samples verbatim. _precheck_draws
    # must use two distinct label seeds even when m_lo == m_hi, so the two
    # draws differ despite drawing on the identical shared states.
    fam = corpus.FAMILIES["heat_phi"]
    [spec] = corpus.sample_instances("heat_phi", 1, seed=7, n_states=6, m_samples=20, n_draws=1)
    data_lo, data_hi = optrain._precheck_draws(spec, fam, m_lo=20, m_hi=20, n_jobs=1)
    assert np.array_equal(data_lo.t, data_hi.t) and np.array_equal(data_lo.x, data_hi.x)
    assert not np.array_equal(data_lo.y, data_hi.y)


def test_calibration_precheck_stderr_ratio_not_degenerate():
    # With the nested-sample bug, m_lo == m_hi runs (through the old
    # generate_instance path) would compare a draw against an exact copy of
    # itself: z == 0 everywhere and stderr_ratio == 1.0 exactly. With
    # independent draws that degeneracy disappears.
    result = optrain.calibration_precheck("heat_phi", n=1, n_states=6, m_lo=20, m_hi=20, seed=11)
    assert result["stderr_ratio"] != 1.0
