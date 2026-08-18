"""Thin adapters from parabolab PDE definitions to the vendored baselines.

The vendored solvers (``vendor/bsde.py``, ``vendor/galerkin.py``, from
https://github.com/nguwijy/deep_branching @ c06bef2, MIT) expect torch
callables in their own conventions:

* **Deep BSDE** (``BSDENet``): the input of ``f_fun`` is a FIXED layout
  ``(u, du/dx_1..du/dx_d[, d2u/dx_1^2..d2u/dx_d^2])`` -- index 0 is u,
  1..d the gradient, d+1..2d the diagonal Hessian (``second_order=True``
  only).  The Brownian dynamics already account for the (1/2) Laplacian,
  so ``f_fun`` is exactly our ``f_expr`` (which is written for
  du/dt + (1/2) Lap u + f = 0).  Only PDEs whose ``deriv_map`` consists
  of {0, e_k, 2 e_k} rows and whose ``sigma2 == 1`` fit this layout.

* **Deep Galerkin** (``DGMNet``): the residual is ``du/dt + f(jet)``
  where f is evaluated on the CALLER-supplied ``dgm_deriv_map`` jet and
  must contain the full spatial operator.  We therefore extend our
  ``deriv_map`` with the Laplacian rows 2 e_k and supply
  ``f_dgm = f_ours + (sigma2/2) sum_k d^2 u/dx_k^2``.

Both use ``phi_fun(x)`` with ``x`` of shape ``(d, batch)``.

Everything here is a mapping of indices plus a sympy->torch lambdify;
no solver logic is duplicated.
"""

from __future__ import annotations

import math
from typing import Callable, Optional

import numpy as np
import sympy as sp
import torch

from ..pde import x_symbols, z_symbols


class BaselineInapplicable(ValueError):
    """The PDE does not fit the baseline's input convention."""


_TORCH_MODULES = [
    {
        "exp": torch.exp, "log": torch.log,
        "sin": torch.sin, "cos": torch.cos, "tan": torch.tan,
        "sinh": torch.sinh, "cosh": torch.cosh, "tanh": torch.tanh,
        "sqrt": torch.sqrt, "Abs": torch.abs, "sign": torch.sign,
        "pi": math.pi,
    },
    "math",
]


def _lambdify_torch(args, expr) -> Callable:
    return sp.lambdify(args, expr, modules=_TORCH_MODULES)


def torch_phi(pde, phi_expr=None) -> Callable:
    """``phi_fun(x)`` with x of shape (d, batch), the baselines' layout."""
    xs = x_symbols(pde.d)
    fn = _lambdify_torch(xs, phi_expr if phi_expr is not None
                         else pde.phi_expr)
    return lambda x: fn(*x)


def _classify_rows(deriv_map, d):
    """Map each deriv_map row to its position in the BSDE input layout.

    Returns (positions, second_order).  Raises BaselineInapplicable for
    rows other than 0, e_k, 2 e_k (mixed or higher derivatives).
    """
    positions, second_order = [], False
    for row in deriv_map:
        nz = [(k, o) for k, o in enumerate(row) if o]
        if not nz:
            positions.append(0)
        elif len(nz) == 1 and nz[0][1] == 1:
            positions.append(1 + nz[0][0])
        elif len(nz) == 1 and nz[0][1] == 2:
            positions.append(1 + d + nz[0][0])
            second_order = True
        else:
            raise BaselineInapplicable(
                f"deriv_map row {row} has no slot in the deep BSDE "
                f"(u, grad u, diag Hess u) input layout")
    return positions, second_order


def bsde_functions(pde, f_expr=None, phi_expr=None) -> dict:
    """Kwargs for ``vendor.bsde.BSDENet`` built from a parabolab PDE.

    ``f_expr``/``phi_expr`` optionally override the PDE's expressions
    (e.g. |z|-regularized variants for training stability, as in the
    authors' comparison notebook).
    """
    if pde.sigma2 != 1.0:
        raise BaselineInapplicable(
            f"BSDENet hard-codes standard BM (sigma2=1); PDE has "
            f"sigma2={pde.sigma2}")
    d, m = pde.d, len(pde.deriv_map)
    positions, second_order = _classify_rows(pde.deriv_map, d)
    zs = z_symbols(m - 1)
    f_lam = _lambdify_torch(zs, f_expr if f_expr is not None
                            else pde.f_expr)

    def f_fun(y):
        # y: (1 + d [+ d], batch) in the fixed BSDE layout
        return f_lam(*(y[p] for p in positions))

    return dict(
        f_fun=f_fun,
        deriv_map=np.array(pde.deriv_map),
        phi_fun=torch_phi(pde, phi_expr),
        second_order=second_order,
        T=pde.T, t_hi=pde.T,
    )


def dgm_functions(pde, f_expr=None, phi_expr=None) -> dict:
    """Kwargs for ``vendor.galerkin.DGMNet`` built from a parabolab PDE."""
    d, m = pde.d, len(pde.deriv_map)
    rows = [tuple(r) for r in pde.deriv_map]
    lap_pos = []
    for k in range(d):
        row = tuple(2 if j == k else 0 for j in range(d))
        if row not in rows:
            rows.append(row)
        lap_pos.append(rows.index(row))
    half_sig2 = 0.5 * pde.sigma2

    zs = z_symbols(m - 1)
    f_lam = _lambdify_torch(zs, f_expr if f_expr is not None
                            else pde.f_expr)

    def dgm_f_fun(y):
        # y: (len(rows), batch) in dgm_deriv_map order
        val = f_lam(*(y[i] for i in range(m)))
        return val + half_sig2 * sum(y[p] for p in lap_pos)

    return dict(
        dgm_f_fun=dgm_f_fun,
        dgm_deriv_map=np.array(rows),
        phi_fun=torch_phi(pde, phi_expr),
        t_hi=pde.T,
    )


def eval_bsde_grid(model, xs: np.ndarray) -> np.ndarray:
    """u(0, x) from a trained BSDENet on points xs of shape (n, d)."""
    model.eval()
    with torch.no_grad():
        out = model(
            torch.tensor(xs, dtype=torch.float32, device=model.device),
            variable="y",
        )
    return out.squeeze(-1).cpu().numpy()


def eval_dgm_grid(model, tx: np.ndarray) -> np.ndarray:
    """u(t, x) from a trained DGMNet on points tx of shape (n, 1 + d)."""
    model.eval()
    with torch.no_grad():
        out = model(torch.tensor(tx, dtype=torch.float32,
                                 device=model.device))
    return out.cpu().numpy()
