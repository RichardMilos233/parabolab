"""The general Faa-di-Bruno mechanism (JEQ2023 eqs. (2.4)-(2.5)).

Validated three ways:
  1. the n = 1 example tables written out in JEQ Section 2 are reproduced
     exactly;
  2. sympy identities: the tuple expansion of M(dx^k) equals d^k/dx^k of
     f(jet), and the expansion of M(g*) equals the drift identity behind
     eq. (2.3), for generic (undefined) f and u;
  3. the n = 0 tables coincide with the hand-coded semilinear mechanism
     (2.7).
"""

import sympy as sp

from parabolab.mechanism import (
    Dx,
    FNu,
    FullyNonlinearMechanism1D,
    Id,
    SemilinearMechanism,
    FDeriv,
)
from parabolab.pde import FullyNonlinearPDE1D, x_symbol, z_symbols


def generic_pde(n: int) -> FullyNonlinearPDE1D:
    """A PDE whose f has no identically-zero derivative of any order
    (so raw and reduced tables coincide)."""
    zs = z_symbols(n)
    f = sp.exp(sum(zs))
    return FullyNonlinearPDE1D(T=1.0, n=n, f_expr=f, phi_expr=sp.cos(x_symbol()),
                               name=f"generic(n={n})")


# ---------------------------------------------------------------------------
# 1. the paper's n = 1 tables
# ---------------------------------------------------------------------------

def test_n1_dx_table_matches_paper():
    mech = generic_pde(1).mechanism
    assert mech.tuples(Dx(1)) == (
        (FNu(1.0, (1, 0)), Dx(1)),
        (FNu(1.0, (0, 1)), Dx(2)),
    )


def test_n1_gstar_table_matches_paper():
    mech = generic_pde(1).mechanism
    tuples = mech.tuples(FNu(1.0, (0, 0)))
    assert len(tuples) == 7
    expected = {
        (FNu(1.0, (0, 0)), FNu(1.0, (1, 0))),
        (FNu(1.0, (0, 1)), FNu(1.0, (1, 0)), Dx(1)),
        (FNu(1.0, (0, 1)), FNu(1.0, (0, 1)), Dx(2)),
        (FNu(-0.5, (2, 0)), Dx(1), Dx(1)),
        (FNu(-0.5, (1, 1)), Dx(1), Dx(2)),
        (FNu(-0.5, (1, 1)), Dx(2), Dx(1)),
        (FNu(-0.5, (0, 2)), Dx(2), Dx(2)),
    }
    assert set(tuples) == expected


def test_n1_dx2_table_matches_paper_expansion():
    # The paper lists 6 tuples for M(dx^2), printing the mixed
    # (d_z0 d_z1 f, dx, dx^2) term twice with coefficient 1; we carry it
    # once with coefficient 2 (same expansion, see fdb.py docstring).
    mech = generic_pde(1).mechanism
    assert set(mech.tuples(Dx(2))) == {
        (FNu(1.0, (1, 0)), Dx(2)),
        (FNu(1.0, (0, 1)), Dx(3)),
        (FNu(1.0, (2, 0)), Dx(1), Dx(1)),
        (FNu(2.0, (1, 1)), Dx(1), Dx(2)),
        (FNu(1.0, (0, 2)), Dx(2), Dx(2)),
    }


def test_gstar_table_size_formula():
    # |M(g*)| = 1 + sum_k |fdb(n+1, k)| + (n+1)^2  (JEQ appendix, l1)
    from parabolab.fdb import fdb_terms

    for n in [0, 1, 2, 3, 4]:
        mech = generic_pde(n).mechanism
        got = len(mech.tuples(FNu(1.0, (0,) * (n + 1))))
        want = 1 + sum(len(fdb_terms(n + 1, k)) for k in range(1, n + 1)) \
            + (n + 1) ** 2
        assert got == want


# ---------------------------------------------------------------------------
# 2. sympy identities
# ---------------------------------------------------------------------------
# u stays a generic undefined function; for f we use the exponential family
#     f(z0, ..., zn) = exp(a0 z0 + ... + an zn),   a_q symbolic,
# for which d^nu f = (prod_q a_q^{nu_q}) f.  Distinct derivative
# multi-indices nu produce distinct monomials in the a_q, so the identity
# below must hold coefficient-by-coefficient in (a, u-jet) -- a strong check
# of the combinatorial constants.  (Undefined f would be even more generic,
# but sympy cannot reliably compare the two Subs normal forms it produces.)

X = x_symbol()
U = sp.Function("u")


def jet(n):
    return [sp.diff(U(X), X, q) for q in range(n + 1)]


def a_coeffs(n):
    return sp.symbols(f"a0:{n + 1}", positive=True)


def f_of_jet(n):
    a = a_coeffs(n)
    return sp.exp(sp.Add(*[ai * ji for ai, ji in zip(a, jet(n))]))


def code_expr(code, n):
    """The operator c(u) as a sympy expression, for the exponential f."""
    if isinstance(code, Id):
        return U(X)
    if isinstance(code, Dx):
        return sp.diff(U(X), X, code.order)
    if isinstance(code, FNu):
        a = a_coeffs(n)
        mono = sp.Mul(*[ai ** o for ai, o in zip(a, code.nu)])
        return sp.nsimplify(code.a) * mono * f_of_jet(n)
    raise TypeError(code)


def expansion(mech, code, n):
    return sp.Add(*[sp.Mul(*[code_expr(c, n) for c in tpl])
                    for tpl in mech._raw_tuples(code)])


def test_dx_mechanism_identity():
    # sum over M(dx^k) of products == d^k/dx^k f(u, u', ..., u^(n))
    for n, kmax in [(0, 4), (1, 3), (2, 2), (3, 2)]:
        mech = generic_pde(n).mechanism
        for k in range(1, kmax + 1):
            lhs = expansion(mech, Dx(k), n)
            rhs = sp.diff(f_of_jet(n), X, k)
            assert sp.simplify(lhs - rhs) == 0, (n, k)


def test_gstar_mechanism_identity():
    # sum over M(g*) of products == the drift expansion behind eq. (2.3):
    #   dz0(g) f + sum_k dzk(g) d^k/dx^k f(jet)
    #   - 1/2 sum_{j,l} dzj dzl g u^(j+1) u^(l+1)
    for n, nu in [(1, (0, 0)), (1, (1, 1)), (2, (0, 0, 0)), (2, (0, 2, 1))]:
        mech = generic_pde(n).mechanism
        g = FNu(1.0, nu)
        lhs = expansion(mech, g, n)

        def dz(code_nu, k):
            return code_nu[:k] + (code_nu[k] + 1,) + code_nu[k + 1:]

        rhs = code_expr(FNu(1.0, dz(nu, 0)), n) * f_of_jet(n)
        for k in range(1, n + 1):
            rhs += code_expr(FNu(1.0, dz(nu, k)), n) * sp.diff(f_of_jet(n), X, k)
        for j in range(n + 1):
            for l in range(n + 1):
                rhs -= sp.Rational(1, 2) * code_expr(FNu(1.0, dz(dz(nu, j), l)), n) \
                    * sp.diff(U(X), X, j + 1) * sp.diff(U(X), X, l + 1)
        assert sp.simplify(lhs - rhs) == 0, (n, nu)


# ---------------------------------------------------------------------------
# 3. n = 0 reduces to the semilinear mechanism; zero-tuple reduction
# ---------------------------------------------------------------------------

def test_n0_reduces_to_semilinear():
    # same tables up to the (irrelevant) order of codes within a tuple and
    # of tuples within the set
    mech = generic_pde(0).mechanism

    def to_semi(code):
        if isinstance(code, FNu):
            return FDeriv(code.a, code.nu[0])
        return code

    def normalize(tuples):
        return sorted(sorted(map(repr, tpl)) for tpl in tuples)

    for code_gen, code_semi in [
        (Id(), Id()),
        (FNu(1.0, (0,)), FDeriv(1.0, 0)),
        (FNu(-2.0, (3,)), FDeriv(-2.0, 3)),
        (Dx(1), Dx(1)),
    ]:
        got = [tuple(to_semi(c) for c in tpl)
               for tpl in mech.tuples(code_gen)]
        assert normalize(got) == normalize(SemilinearMechanism.tuples(code_semi))


def test_zero_tuple_reduction_drops_only_zero_codes():
    # f = z0^3 z3 - z2/2 (Dym): no z1 dependence, polynomial in z0
    from parabolab.library import dym_1d

    pde = dym_1d()
    mech = pde.mechanism
    f_star = FNu(1.0, (0, 0, 0, 0))
    raw = mech._raw_tuples(f_star)
    reduced = mech.tuples(f_star)
    assert set(reduced) <= set(raw)
    assert len(reduced) < len(raw)
    for tpl in reduced:
        assert not any(mech.is_identically_zero(c) for c in tpl)
    for tpl in set(raw) - set(reduced):
        assert any(mech.is_identically_zero(c) for c in tpl)


def test_reduction_never_returns_empty_table():
    # f = z1: (d_z0 f)* is identically zero, so the first tuple of M(f*)
    # dies, as do many others; the table must stay non-empty
    zs = z_symbols(1)
    pde = FullyNonlinearPDE1D(T=1.0, n=1, f_expr=zs[1],
                              phi_expr=sp.cos(x_symbol()), name="linear-z1")
    mech = pde.mechanism
    for code in [Id(), Dx(1), FNu(1.0, (0, 0)), FNu(1.0, (5, 5))]:
        assert len(mech.tuples(code)) >= 1


def test_mechanism_memoized_per_pde():
    pde = generic_pde(2)
    assert pde.mechanism is pde.mechanism
    assert pde.mechanism.tuples(Dx(1)) is pde.mechanism.tuples(Dx(1))
