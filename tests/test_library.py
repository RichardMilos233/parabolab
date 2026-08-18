"""Verify the library's closed-form solutions symbolically with sympy.

This protects against transcription errors from the paper: (5.3) must solve
the PDE (5.2) and (5.4) must solve the space-independent ODE, and the
hand-coded derivative callables must match sympy's derivatives.
"""

import math

import sympy as sp

from parabolab.library import allen_cahn_flat, allen_cahn_wave_1d

t, x, T = sp.symbols("t x T", real=True)


def test_traveling_wave_solves_allen_cahn():
    # u(t,x) = -1/2 - 1/2 tanh(3(T-t)/4 - x/2)  [JEQ2023 (5.3), d=1]
    u = -sp.Rational(1, 2) - sp.Rational(1, 2) * sp.tanh(
        3 * (T - t) / 4 - x / 2
    )
    residual = sp.diff(u, t) + sp.diff(u, x, 2) / 2 + u - u ** 3
    assert sp.simplify(residual) == 0


def test_flat_solution_solves_ode():
    # u(t) = (1 - (1 - phi0^-2) exp(-2(T-t)))^(-1/2)  [JEQ2023 (5.4)]
    phi0 = sp.Symbol("phi0", positive=True)
    u = 1 / sp.sqrt(1 - (1 - phi0 ** -2) * sp.exp(-2 * (T - t)))
    residual = sp.diff(u, t) + u - u ** 3
    assert sp.simplify(residual) == 0
    assert sp.simplify(u.subs(t, T) - phi0) == 0


def test_library_matches_symbolic_formulas():
    Tval = 0.5
    wave = allen_cahn_wave_1d(Tval)
    u = -sp.Rational(1, 2) - sp.Rational(1, 2) * sp.tanh(
        3 * (Tval - t) / 4 - x / 2
    )
    for tv, xv in [(0.0, 0.0), (0.1, -1.3), (0.4, 2.0)]:
        expected = float(u.subs({t: tv, x: xv}))
        assert math.isclose(wave.exact_solution(tv, xv), expected, rel_tol=1e-12)
        assert math.isclose(
            wave.phi(xv), float(u.subs({t: Tval, x: xv})), rel_tol=1e-12
        )
        assert math.isclose(
            wave.phi_derivative(1)(xv),
            float(sp.diff(u, x).subs({t: Tval, x: xv})),
            rel_tol=1e-12,
        )

    flat = allen_cahn_flat(0.5, Tval)
    uf = 1 / sp.sqrt(1 - (1 - sp.Rational(2) ** 2) * sp.exp(-2 * (Tval - t)))
    for tv in [0.0, 0.2, 0.5]:
        assert math.isclose(
            flat.exact_solution(tv, 0.0), float(uf.subs(t, tv)), rel_tol=1e-12
        )


def test_f_derivatives_match_sympy():
    z = sp.Symbol("z")
    f = z - z ** 3
    pde = allen_cahn_wave_1d(0.5)
    for k in range(0, 4):
        fk = pde.f_derivative(k)
        expected = sp.diff(f, z, k)
        for zv in [-1.5, -0.3, 0.0, 0.7, 2.0]:
            assert math.isclose(
                fk(zv), float(expected.subs(z, zv)), rel_tol=1e-12, abs_tol=1e-12
            )
    assert pde.f_derivative(4) is None  # f is a cubic polynomial
    assert pde.f_derivative(10) is None
