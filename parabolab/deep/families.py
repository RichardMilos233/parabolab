"""PDE families used only by the deep-learning corpus (parameterised /
Fourier-terminal-condition builders and a 1-D finite-difference reference).
Kept out of parabolab.library so the NN research line does not touch the
shared Monte Carlo library.
"""

from __future__ import annotations

import math

import numpy as np

from ..pde import FullyNonlinearPDEnD, x_symbols, z_symbols


def merton_hjb_derivatives(
    T: float = 0.1,
    mu: float = 0.03,
    sigma: float = 0.1,
    gamma: float = 0.5,
    rho: float = 0.01,
):
    """(u_x, u_xx) of merton_hjb's closed form, same argument convention as
    its exact_solution: u = x^{1-gamma} g(t) with
    g = base^gamma / (1 - gamma), base = (1 + (a-1) e^{-a(T-t)}) / a."""
    a = (2 * sigma**2 * gamma * rho - (1 - gamma) * mu**2) / (
        2 * sigma**2 * gamma**2
    )

    def _g(t: float) -> float:
        base = (1 + (a - 1) * math.exp(-a * (T - t))) / a
        return base**gamma / (1 - gamma)

    def _x(xv) -> float:
        return float(xv[0]) if hasattr(xv, "__len__") else float(xv)

    def ux(t: float, xv) -> float:
        return (1 - gamma) * _x(xv) ** (-gamma) * _g(t)

    def uxx(t: float, xv) -> float:
        return -gamma * (1 - gamma) * _x(xv) ** (-gamma - 1) * _g(t)

    return ux, uxx


# ---------------------------------------------------------------------------
# Random Fourier terminal conditions (D03 operator learning)
# ---------------------------------------------------------------------------

def _fourier_omega(x_lo: float, x_hi: float) -> float:
    return 2.0 * math.pi / (x_hi - x_lo)


def fourier_phi_expr(coeffs, x_lo: float = -8.0, x_hi: float = 8.0):
    """phi(x) = A sum_k (a_k cos(k w x) + b_k sin(k w x)), w = 2 pi / (x_hi - x_lo),
    coeffs = (A, a_1..a_K, b_1..b_K)."""
    import sympy as sp

    (x,) = x_symbols(1)
    A, rest = float(coeffs[0]), [float(c) for c in coeffs[1:]]
    K = len(rest) // 2
    w = _fourier_omega(x_lo, x_hi)
    expr = sum(rest[k - 1] * sp.cos(k * w * x) + rest[K + k - 1] * sp.sin(k * w * x)
               for k in range(1, K + 1))
    return A * expr


def fourier_phi_numpy(coeffs, x, x_lo: float = -8.0, x_hi: float = 8.0) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    A, rest = float(coeffs[0]), [float(c) for c in coeffs[1:]]
    K = len(rest) // 2
    w = _fourier_omega(x_lo, x_hi)
    out = np.zeros_like(x)
    for k in range(1, K + 1):
        out += rest[k - 1] * np.cos(k * w * x) + rest[K + k - 1] * np.sin(k * w * x)
    return A * out


def heat_fourier_1d(T: float, coeffs, x_lo: float = -8.0, x_hi: float = 8.0) -> FullyNonlinearPDEnD:
    """Linear heat equation du/dt + (1/2) u_xx = 0 with a Fourier-series
    terminal condition; each mode is damped by exp(-k^2 w^2 (T - t) / 2)."""
    z = z_symbols(0)
    A, rest = float(coeffs[0]), [float(c) for c in coeffs[1:]]
    K = len(rest) // 2
    w = _fourier_omega(x_lo, x_hi)

    def exact(t: float, xv) -> float:
        x = float(xv[0]) if hasattr(xv, "__len__") else float(xv)
        return A * sum(
            math.exp(-0.5 * (k * w) ** 2 * (T - t))
            * (rest[k - 1] * math.cos(k * w * x) + rest[K + k - 1] * math.sin(k * w * x))
            for k in range(1, K + 1))

    return FullyNonlinearPDEnD(
        T=T, d=1, deriv_map=((0,),), f_expr=0 * z[0],
        phi_expr=fourier_phi_expr(coeffs, x_lo, x_hi), exact_solution=exact,
        name=f"heat_fourier_1d(T={T}, K={K})")


def allen_cahn_fourier_1d(T: float, coeffs, x_lo: float = -8.0, x_hi: float = 8.0) -> FullyNonlinearPDEnD:
    """Allen-Cahn du/dt + (1/2) u_xx + u - u^3 = 0 with a Fourier-series
    terminal condition; no closed form (use fd_reference_1d)."""
    z = z_symbols(0)
    K = (len(coeffs) - 1) // 2
    return FullyNonlinearPDEnD(
        T=T, d=1, deriv_map=((0,),), f_expr=z[0] - z[0] ** 3,
        phi_expr=fourier_phi_expr(coeffs, x_lo, x_hi), exact_solution=None,
        name=f"allen_cahn_fourier_1d(T={T}, K={K})")


def fd_reference_1d(pde, xq, *, dx: float = 0.02, x_pad: float = 4.0,
                    x_lo: float = -8.0, x_hi: float = 8.0) -> np.ndarray:
    """u(0, xq) for a 1-D semilinear problem du/dt + (sigma2/2) u_xx + f(u) = 0
    by explicit Euler on v(s, x) = u(T - s, x) (zero-flux boundaries)."""
    import sympy as sp

    if tuple(pde.deriv_map) != ((0,),):
        raise ValueError("fd_reference_1d needs deriv_map == ((0,),) (f a function of u only)")
    z = z_symbols(0)
    f = sp.lambdify(z, pde.f_expr, "numpy")
    sigma2 = float(getattr(pde, "sigma2", 1.0))
    grid = np.arange(x_lo - x_pad, x_hi + x_pad + dx / 2, dx)
    phi = pde.phi_mu((0,))
    v = np.array([float(phi(x)) for x in grid])
    dt = 0.4 * dx**2 / sigma2
    s, T = 0.0, float(pde.T)
    while s < T - 1e-15:
        h = min(dt, T - s)
        lap = np.empty_like(v)
        lap[1:-1] = (v[2:] - 2 * v[1:-1] + v[:-2]) / dx**2
        lap[0] = (v[1] - v[0]) / dx**2 * 2      # zero-flux: ghost = v[1]
        lap[-1] = (v[-2] - v[-1]) / dx**2 * 2
        v = v + h * (0.5 * sigma2 * lap + np.asarray(f(v), dtype=float))
        s += h
    return np.interp(np.asarray(xq, dtype=float), grid, v)
