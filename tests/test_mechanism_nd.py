"""Validation of the d-dimensional mechanism (M3).

Three independent checks, as specced:
1. golden cross-check of the multivariate Faa di Bruno enumeration against
   the authors' deep_branching/fdb.py fdb_nd for genuinely multivariate mu;
2. sympy identity checks in d = 2 (small orders): the mechanism tables of
   M(d^mu) and M(g*) sum to the true spatial derivative / drift of f(jet),
   including the sigma2 factor;
3. consistency: d = 1 full-jet tables reproduce FullyNonlinearMechanism1D
   exactly, and a d-dim PDE with x-independent data reproduces the flat
   Allen-Cahn ODE closed form.
"""

import math
import pathlib
import sys

import numpy as np
import pytest
import sympy as sp

import parabolab as pl
from parabolab.fdb import fdb_terms_nd
from parabolab.mechanism import DxN, FNu, Id
from parabolab.parallel import estimate_parallel

AUTHORS_REPO = pathlib.Path("/Users/michael/Desktop/NTU/fyp/deep_branching")


# --------------------------------------------------------------------------
# 1. golden cross-check against the authors' fdb_nd (multivariate mu)
# --------------------------------------------------------------------------

def _normalize_ours(terms):
    return sorted((t.coeff, t.lam, t.blocks) for t in terms)


def _normalize_theirs(terms):
    out = []
    for t in terms:
        blocks = []
        for ll, k_arr in t.l_and_k.items():
            for q, mult in enumerate(k_arr):
                if mult:
                    blocks.append((tuple(ll), q, mult))
        out.append((t.coeff, tuple(t.lamb), tuple(sorted(blocks))))
    return sorted(out)


@pytest.mark.skipif(not AUTHORS_REPO.exists(),
                    reason="authors' deep_branching repo not available")
@pytest.mark.parametrize("m,mu", [
    (1, (1, 1)), (1, (2, 1)), (2, (1, 1)), (2, (2, 2)),
    (3, (2, 1)), (2, (1, 0, 1)), (1, (1, 1, 1)), (4, (0, 3)),
])
def test_golden_fdb_nd_multivariate(m, mu):
    sys.path.insert(0, str(AUTHORS_REPO))
    try:
        from fdb import fdb_nd
    finally:
        sys.path.pop(0)
    assert _normalize_ours(fdb_terms_nd(m, mu)) \
        == _normalize_theirs(fdb_nd(m, mu))


def test_fdb_nd_live_prunes_exactly():
    # pruning with a monotone predicate must equal filter-after-enumeration
    live = lambda lam: sum(lam) <= 2 and all(v <= 1 for v in lam)  # noqa: E731
    full = [t for t in fdb_terms_nd(3, (2, 1)) if live(t.lam)]
    pruned = list(fdb_terms_nd(3, (2, 1), live))
    assert full == pruned and len(pruned) < len(fdb_terms_nd(3, (2, 1)))


# --------------------------------------------------------------------------
# 2. sympy identity checks in d = 2
# --------------------------------------------------------------------------

def _generic_setup_d2():
    """d = 2 PDE with exp-family f (all derivatives distinct monomials in
    the a_q) and a generic smooth u to differentiate against."""
    d = 2
    deriv_map = ((0, 0), (1, 0), (0, 1), (1, 1))  # u, ux, uy, uxy
    m = len(deriv_map)
    zs = pl.z_symbols(m - 1)
    a = sp.symbols(f"a0:{m}")
    f_expr = sp.exp(sum(ai * zi for ai, zi in zip(a, zs)))
    xs = pl.x_symbols(d)
    pde = pl.FullyNonlinearPDEnD(
        T=1.0, d=d, deriv_map=deriv_map, f_expr=f_expr,
        phi_expr=xs[0] * xs[1], sigma2=3.0, name="generic-d2",
    )
    u = sp.Function("u")
    x0, x1 = xs
    jet = [sp.Derivative(u(x0, x1), *(
        [x0] * row[0] + [x1] * row[1])) if any(row) else u(x0, x1)
        for row in deriv_map]
    subs = {z: j for z, j in zip(zs, jet)}
    return pde, zs, a, f_expr, xs, jet, subs


def _code_expr(code, f_expr, zs, subs, xs, jet, deriv_map):
    """Symbolic value of a code applied to u."""
    if isinstance(code, FNu):
        expr = f_expr
        for z, order in zip(zs, code.nu):
            if order:
                expr = sp.diff(expr, z, order)
        return code.a * expr.subs(subs)
    if isinstance(code, DxN):
        u_expr = jet[0]
        return sp.diff(u_expr, *(
            [xs[0]] * code.mu[0] + [xs[1]] * code.mu[1]))
    raise TypeError(code)


def _table_sum(mech, code, f_expr, zs, subs, xs, jet, deriv_map):
    total = sp.Integer(0)
    for tpl in mech.tuples(code):
        prod = sp.Integer(1)
        for c in tpl:
            prod *= _code_expr(c, f_expr, zs, subs, xs, jet, deriv_map)
        total += prod
    return total


@pytest.mark.parametrize("mu", [(1, 0), (0, 1), (1, 1), (2, 0), (2, 1)])
def test_dx_mechanism_identity_d2(mu):
    """sum M(d^mu) == d^mu [f(jet)] for the generic d = 2 setup."""
    pde, zs, a, f_expr, xs, jet, subs = _generic_setup_d2()
    mech = pde.mechanism
    lhs = _table_sum(mech, DxN(mu), f_expr, zs, subs, xs, jet, pde.deriv_map)
    rhs = sp.diff(f_expr.subs(subs), *(
        [xs[0]] * mu[0] + [xs[1]] * mu[1]))
    assert sp.simplify(lhs - rhs.doit()) == 0


def test_gstar_mechanism_identity_d2():
    """sum M(g*) equals the drift  sum_p dz_p g d^{alpha_p}[f(jet)]
    - sigma2/2 sum_{i,j,k} dz_i dz_j g d^{alpha_i+e_k}u d^{alpha_j+e_k}u
    for g = a0-monomial-weighted exp family, including the sigma2 factor."""
    pde, zs, a, f_expr, xs, jet, subs = _generic_setup_d2()
    mech = pde.mechanism
    nu = (1, 0, 0, 0)
    g_code = FNu(2.0, nu)
    lhs = _table_sum(mech, g_code, f_expr, zs, subs, xs, jet, pde.deriv_map)

    g_expr = 2.0 * sp.diff(f_expr, zs[0])
    f_of_jet = f_expr.subs(subs)
    rhs = sp.Integer(0)
    for p, row in enumerate(pde.deriv_map):
        dxf = sp.diff(f_of_jet, *(
            [xs[0]] * row[0] + [xs[1]] * row[1])) if any(row) else f_of_jet
        rhs += sp.diff(g_expr, zs[p]).subs(subs) * dxf
    for i, row_i in enumerate(pde.deriv_map):
        for j, row_j in enumerate(pde.deriv_map):
            gij = sp.diff(g_expr, zs[i], zs[j]).subs(subs)
            for k in range(pde.d):
                bump = lambda row: tuple(  # noqa: E731
                    v + (1 if idx == k else 0) for idx, v in enumerate(row))
                ui = sp.diff(jet[0], *(
                    [xs[0]] * bump(row_i)[0] + [xs[1]] * bump(row_i)[1]))
                uj = sp.diff(jet[0], *(
                    [xs[0]] * bump(row_j)[0] + [xs[1]] * bump(row_j)[1]))
                rhs -= pde.sigma2 / 2 * gij * ui * uj
    assert sp.simplify(lhs - rhs.doit()) == 0


# --------------------------------------------------------------------------
# 3. consistency with the d = 1 implementation and flat data
# --------------------------------------------------------------------------

def _map_1d_code(c):
    if isinstance(c, pl.Dx):
        return DxN((c.order,))
    return c


def test_d1_full_jet_reproduces_1d_mechanism_tables():
    pde1 = pl.library.quasilinear_tan_1d()
    x0 = pl.x_symbols(1)[0]
    pdeN = pl.FullyNonlinearPDEnD(
        T=pde1.T, d=1, deriv_map=((0,), (1,), (2,)),
        f_expr=pde1.f_expr, phi_expr=pde1.phi_expr.subs(pl.x_symbol(), x0),
    )
    m1, mN = pde1.mechanism, pdeN.mechanism
    for code1, codeN in [
        (Id(), Id()),
        (FNu(1.0, (0, 0, 0)), FNu(1.0, (0, 0, 0))),
        (FNu(-0.5, (1, 0, 1)), FNu(-0.5, (1, 0, 1))),
        (pl.Dx(1), DxN((1,))),
        (pl.Dx(2), DxN((2,))),
        (pl.Dx(3), DxN((3,))),
    ]:
        mapped = tuple(tuple(_map_1d_code(c) for c in tpl)
                       for tpl in m1.tuples(code1))
        assert mapped == mN.tuples(codeN)


def test_flat_data_reproduces_ode_closed_form():
    """d = 3 Allen-Cahn with constant phi == 0.5 must match the flat ODE
    solution (5.4), like the d = 1 M1 test."""
    ref = pl.library.allen_cahn_flat(phi0=0.5, T=0.5)
    z = pl.z_symbols(0)
    pde = pl.FullyNonlinearPDEnD(
        T=0.5, d=3, deriv_map=((0, 0, 0),),
        f_expr=z[0] - z[0] ** 3,
        phi_expr=sp.Rational(1, 2) + 0 * pl.x_symbols(3)[0],
    )
    res = pl.estimate(pde, 0.0, np.zeros(3), 20_000, seed=7)
    exact = ref.exact_solution(0.0, 0.0)
    assert abs(res.estimate - exact) < 3.0 * res.stderr


def test_sigma2_heat_control():
    """f = 0, sigma2 = 2, phi = |x|^2: u(t,x) = |x|^2 + sigma2 d (T-t)/1...
    precisely E|x + sqrt(sigma2 (T-t)) Z|^2 = |x|^2 + sigma2 (T-t) d."""
    z = pl.z_symbols(0)
    xs = pl.x_symbols(2)
    pde = pl.FullyNonlinearPDEnD(
        T=0.25, d=2, deriv_map=((0, 0),), f_expr=0 * z[0],
        phi_expr=xs[0] ** 2 + xs[1] ** 2, sigma2=2.0,
    )
    x = np.array([0.5, -0.5])
    res = pl.estimate(pde, 0.0, x, 40_000, seed=2)
    exact = 0.5 + 2.0 * 0.25 * 2
    assert abs(res.estimate - exact) < 3.5 * res.stderr


def test_exponential_gradient_d2_matches_exact():
    pde = pl.library.exponential_gradient_nd(d=2)
    x = np.array([0.3, -0.1])
    res = pl.estimate(pde, 0.0, x, 30_000, seed=11)
    exact = pde.exact_solution(0.0, x)
    assert abs(res.estimate - exact) < 3.5 * res.stderr


def test_allen_cahn_nd_exact_satisfies_pde_symbolically():
    """The notebook closed form solves (5.2) exactly (checked in d = 3)."""
    d = 3
    xs = pl.x_symbols(d)
    t, T = sp.symbols("t T_")
    u = -sp.Rational(1, 2) - sp.tanh(
        sp.Rational(3, 4) * (T - t) - sum(xs) / (2 * sp.sqrt(d))) / 2
    residual = (sp.diff(u, t) + sp.diff(u, xs[0], 2) / 2
                + sp.diff(u, xs[1], 2) / 2 + sp.diff(u, xs[2], 2) / 2
                + u - u ** 3)
    assert sp.simplify(residual) == 0


def test_hjb_exact_u0_against_paper_error_bookkeeping():
    """JEQ Table 5 reports BSDE mean 4.5977 with mean rel. L1 error 0.0030
    and coding trees 4.580340 with 0.0021 -- both consistent with our
    Cole-Hopf quadrature value 4.590162 (sanity anchor, not a tautology)."""
    exact = pl.library.hjb_exact_u0(T=1.0, d=100)
    assert abs(exact - 4.590162) < 1e-4
    assert abs(abs(4.5977 - exact) / exact - 0.0016) < 6e-4
    assert abs(abs(4.580340 - exact) / exact - 0.0021) < 6e-4


def test_estimate_parallel_independent_of_n_jobs():
    import functools

    factory = functools.partial(pl.library.exponential_gradient_nd, d=2)
    x = np.array([0.0, 0.0])
    r1 = estimate_parallel(factory, 0.0, x, 2_000, seed=3, n_jobs=1,
                           n_chunks=8)
    r2 = estimate_parallel(factory, 0.0, x, 2_000, seed=3, n_jobs=4,
                           n_chunks=8)
    assert r1.estimate == r2.estimate and r1.stderr == r2.stderr


def test_estimate_parallel_agrees_with_reference_estimate():
    """Statistical agreement between the parallel driver and the pure
    single-process reference implementation."""
    import functools

    factory = functools.partial(pl.library.allen_cahn_nd, d=2, T=0.3)
    pde = factory()
    x = np.zeros(2)
    r_ref = pl.estimate(pde, 0.0, x, 20_000, seed=5)
    r_par = estimate_parallel(factory, 0.0, x, 20_000, seed=6, n_jobs=4)
    z = (r_ref.estimate - r_par.estimate) / math.hypot(r_ref.stderr,
                                                       r_par.stderr)
    assert abs(z) < 4.0
    exact = pde.exact_solution(0.0, x)
    assert abs(r_par.estimate - exact) < 3.5 * r_par.stderr
