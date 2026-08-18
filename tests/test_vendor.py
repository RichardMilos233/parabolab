"""Tests for the vendored baselines (M5): thin adapters + smoke training.

The vendored solvers themselves (bsde.py, galerkin.py @ c06bef2) are the
authors' code and are not unit-tested line by line; these tests pin down
OUR adapter layer: index mapping, sympy->torch lambdify, applicability
checks, and that both baselines train to finite (and roughly sane)
values on a smoke budget.
"""

import functools

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from parabolab.library import (
    allen_cahn_bsde,
    allen_cahn_nd,
    cosine_fourth_order_1d,
    exponential_gradient_nd,
    merton_hjb,
)
from parabolab.vendor import (
    BSDENet,
    DGMNet,
    BaselineInapplicable,
    bsde_functions,
    dgm_functions,
    eval_bsde_grid,
    eval_dgm_grid,
    torch_phi,
)


# ---------------------------------------------------------------------------
# adapter mapping
# ---------------------------------------------------------------------------

def test_bsde_layout_allen_cahn():
    kw = bsde_functions(allen_cahn_nd(d=1, T=0.5))
    assert kw["second_order"] is False
    y = torch.tensor([[0.5, -1.0], [9.0, 9.0]])  # u rows; z row unused
    out = kw["f_fun"](y)
    np.testing.assert_allclose(out.numpy(),
                               [0.5 - 0.5**3, -1.0 + 1.0], atol=1e-6)


def test_bsde_layout_gradient_and_second_order():
    # exponential: rows (u, du/dx) -> positions (0, 1), classical BSDE
    kw = bsde_functions(exponential_gradient_nd(d=1, T=0.05))
    assert kw["second_order"] is False
    # merton: rows (u, ux, uxx) -> needs the 2BSDE input layout
    kw = bsde_functions(merton_hjb())
    assert kw["second_order"] is True
    # f(u, ux, uxx) at u=1, ux=0.5, uxx=-0.2 (gamma=0.5 => power is -1)
    y = torch.tensor([[1.0], [0.5], [-0.2]])
    mu, sigma, gamma, rho = 0.03, 0.1, 0.5, 0.01
    expected = (0.2 / 2 - mu**2 / (2 * sigma**2) * 0.25 / (-0.2)
                + gamma / (1 - gamma) / 0.5 - rho)
    np.testing.assert_allclose(kw["f_fun"](y).numpy(), [expected],
                               rtol=1e-6)


def test_bsde_inapplicable_cases():
    # 4th-order derivative row has no slot in the (u, grad, Hess) layout
    pde4 = cosine_fourth_order_1d()

    class FakeND:
        d, T, sigma2 = 1, pde4.T, 1.0
        deriv_map = ((0,), (1,), (2,), (4,))
        f_expr = pde4.f_expr
        phi_expr = pde4.phi_expr

    with pytest.raises(BaselineInapplicable):
        bsde_functions(FakeND())
    # sigma2 != 1 (full-Laplacian conventions) does not fit BSDENet's BM
    with pytest.raises(BaselineInapplicable):
        bsde_functions(allen_cahn_bsde(d=2))


def test_dgm_appends_missing_laplacian_rows():
    kw = dgm_functions(allen_cahn_nd(d=2, T=0.5))
    rows = kw["dgm_deriv_map"].tolist()
    assert rows == [[0, 0], [2, 0], [0, 2]]
    # f_dgm = u - u^3 + (1/2)(uxx + uyy)
    y = torch.tensor([[0.5], [0.2], [-0.4]])
    np.testing.assert_allclose(kw["dgm_f_fun"](y).numpy(),
                               [0.5 - 0.125 + 0.5 * (0.2 - 0.4)],
                               rtol=1e-6)


def test_dgm_reuses_existing_second_order_row():
    kw = dgm_functions(merton_hjb())
    rows = kw["dgm_deriv_map"].tolist()
    assert rows == [[0], [1], [2]]  # (2,) row reused, nothing appended
    # our f contains -z2/2, DGM adds +z2/2: net second-order term is 0
    y = torch.tensor([[1.0], [0.5], [0.3]])
    mu, sigma, gamma, rho = 0.03, 0.1, 0.5, 0.01
    expected = (-mu**2 / (2 * sigma**2) * 0.25 / 0.3
                + gamma / (1 - gamma) / 0.5 - rho)
    np.testing.assert_allclose(kw["dgm_f_fun"](y).numpy(), [expected],
                               rtol=1e-6)


def test_torch_phi_matches_sympy():
    pde = exponential_gradient_nd(d=3, T=0.05)
    phi = torch_phi(pde)
    x = torch.tensor([[0.3, -1.0], [0.1, 0.5], [-0.2, 2.0]])
    expected = np.log(1 + x.sum(dim=0).numpy() ** 2)
    np.testing.assert_allclose(phi(x).numpy(), expected, rtol=1e-6)


# ---------------------------------------------------------------------------
# smoke training: finite results on tiny budgets
# ---------------------------------------------------------------------------

def _grid(pde, x_lo, x_hi, n=11):
    grid = np.linspace(x_lo, x_hi, n)
    xs = np.full((n, pde.d), 0.5 * (x_lo + x_hi))
    xs[:, 0] = grid
    return xs


def test_bsde_smoke_allen_cahn():
    pde = allen_cahn_nd(d=1, T=0.5)
    torch.manual_seed(0)
    model = BSDENet(x_lo=-8.0, x_hi=8.0, epochs=30, bsde_nb_states=200,
                    **bsde_functions(pde))
    model.train_and_eval()
    pred = eval_bsde_grid(model, _grid(pde, -8.0, 8.0))
    assert np.isfinite(pred).all()
    assert np.abs(pred).max() < 10.0  # solution is in [-1, 0]


def test_dgm_smoke_allen_cahn():
    pde = allen_cahn_nd(d=1, T=0.5)
    torch.manual_seed(0)
    model = DGMNet(x_lo=-8.0, x_hi=8.0, epochs=30, dgm_nb_states=200,
                   **dgm_functions(pde))
    model.train_and_eval()
    xs = _grid(pde, -8.0, 8.0)
    pred = eval_dgm_grid(model, np.column_stack([np.zeros(len(xs)), xs]))
    assert np.isfinite(pred).all()


def test_bsde_smoke_merton_second_order():
    import sympy as sp

    from parabolab.pde import x_symbols, z_symbols

    pde = merton_hjb()
    mu, sigma, gamma, rho = 0.03, 0.1, 0.5, 0.01
    z = z_symbols(2)
    (x0,) = x_symbols(1)
    f_reg = (-z[2] / 2 - mu**2 / (2 * sigma**2) * z[1] ** 2 / z[2]
             + gamma / (1 - gamma) * sp.Abs(z[1]) ** (1 - 1 / gamma)
             - rho * z[0])
    phi_reg = sp.Abs(x0) ** (1 - gamma) / (1 - gamma)
    torch.manual_seed(0)
    model = BSDENet(x_lo=100.0, x_hi=200.0, epochs=30, bsde_nb_states=200,
                    y_lo=0.0, y_hi=100.0,
                    **bsde_functions(pde, f_expr=f_reg, phi_expr=phi_reg))
    model.train_and_eval()
    pred = eval_bsde_grid(model, _grid(pde, 100.0, 200.0))
    assert np.isfinite(pred).all()
