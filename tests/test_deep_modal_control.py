"""Smoke and invariant tests for exact-heat latent modal control."""

import csv
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from parabolab.deep import modal_control, modal_data, opnet


def test_exact_heat_basis_projection_and_perturbation():
    batch = modal_data.sample_heat_batch(5, 7, K=3, n_sensors=24, n_query=48)
    recovered = modal_data.project_coeffs(batch.u, batch.query_grid, batch.K)
    np.testing.assert_allclose(recovered, batch.output_coeffs, atol=1e-12)
    changed = modal_data.perturb_output_mode(batch, 2, 0.04)
    expected = batch.output_coeffs.copy()
    expected[:, 2] += 0.04
    np.testing.assert_allclose(changed.output_coeffs, expected)
    np.testing.assert_allclose(
        modal_data.project_coeffs(changed.u, changed.query_grid, changed.K),
        expected, atol=1e-12)
    assert batch.identity != changed.identity


@pytest.mark.parametrize("name", ["deeponet", "attn"])
def test_encode_decode_matches_forward(name):
    batch = modal_data.sample_heat_batch(3, 8, K=2, n_sensors=16, n_query=24)
    kw = {"p": 8, "width": 16} if name == "deeponet" else {
        "d_model": 16, "n_heads": 2, "n_layers": 1}
    net = opnet.make_operator(name, batch.sensor_grid, n_cond=0, **kw).eval()
    phi = torch.as_tensor(batch.phi, dtype=torch.float32)
    cond = torch.empty(len(phi), 0)
    q = torch.stack([
        torch.zeros(len(batch.query_grid)),
        torch.as_tensor(batch.query_grid, dtype=torch.float32)], dim=-1)
    q = q.expand(len(phi), -1, -1)
    with torch.no_grad():
        direct = net(phi, cond, q)
        state = net.encode(phi, cond)
        split = net.decode(state, q)
    torch.testing.assert_close(split, direct)
    assert state.latent.shape[0] == len(phi)
    assert state.physical_scale.shape == (len(phi), 1)


@pytest.mark.parametrize("name", ["deeponet", "attn"])
def test_modal_controller_smoke(name):
    train = modal_data.sample_heat_batch(8, 10, K=2, n_sensors=16, n_query=24)
    calib = modal_data.sample_heat_batch(8, 11, K=2, n_sensors=16, n_query=24)
    test = modal_data.sample_heat_batch(5, 12, K=2, n_sensors=16, n_query=24)
    kw = {"p": 8, "width": 16} if name == "deeponet" else {
        "d_model": 16, "n_heads": 2, "n_layers": 1}
    net = opnet.make_operator(name, train.sensor_grid, n_cond=0, **kw)
    modal_control.fit_exact_scalers(net, train)
    controller = modal_control.fit_modal_controller(net, calib, pca_dim=4)
    rows = modal_control.evaluate_modal_controller(
        net, controller, test, alphas=(0.0, 2.0))
    assert len(rows) == 2 * test.n_modes
    assert all(np.isfinite(v) for row in rows for v in row.values())


def test_latent_modal_control_driver_tiny(tmp_path):
    script = Path(__file__).resolve().parents[1] / "examples" / "latent_modal_control.py"
    out = tmp_path / "modal"
    subprocess.run(
        [sys.executable, str(script), "--tiny", "--device", "cpu",
         "--out-dir", str(out)],
        check=True, capture_output=True, text=True)
    rows = list(csv.DictReader((out / "metrics.csv").open()))
    assert {r["backbone"] for r in rows} == {"deeponet", "attn"}
    assert {r["variant"] for r in rows} == {
        "trained", "random_direction", "untrained"}
    assert (out / "deeponet-seed0.pt").exists()
    assert (out / "attn-seed0-controller.npz").exists()
    assert (out / "attn-seed0-untrained.pt").exists()
    assert (out / "config.json").exists() and (out / "summary.json").exists()
    checkpoint = torch.load(out / "deeponet-seed0.pt", map_location="cpu")
    restored = opnet.make_operator(
        checkpoint["backbone"], checkpoint["sensor_grid"], n_cond=0,
        **checkpoint["model_kwargs"])
    restored.load_state_dict(checkpoint["state_dict"])
