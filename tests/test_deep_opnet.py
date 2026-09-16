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
