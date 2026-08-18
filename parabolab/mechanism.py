"""Codes and the semilinear branching mechanism (JEQ2023 Section 2).

A *code* is an operator applied to the (unknown) solution u.  For the
semilinear case n = 0 (f depends on u only), the code set is

    C = { Id,  d/dx (and higher powers),  (a f^{(k)})*  } ,

see JEQ2023 below eq. (2.6).  The mechanism M maps a code c to the family
of code tuples M(c) used to create children when a particle carrying c
branches (JEQ2023 eq. (2.7)):

    M(Id)   = { (f*,) }
    M(g*)   = { (f*, (g')*) ,  (d/dx, d/dx, -1/2 (g'')*) }   for g = a f^{(k)}
    M(d/dx) = { ((f')*, d/dx) }

Real coefficients (like the -1/2) are absorbed into the ``a`` parameter of
the child code, NOT into the sampling weight; the tuple is drawn uniformly,
q_c = 1/|M(c)|.

At the tree horizon T a leaf carrying code c contributes c(u)(T, x):

    Id -> phi(x),   d^m/dx^m -> phi^{(m)}(x),   (a f^{(k)})* -> a f^{(k)}(phi(x)).

The tree sampler (tree.py) only relies on the small protocol
``tuples`` / ``terminal`` / ``is_identically_zero``, so the general fully
nonlinear mechanism (Faa di Bruno, milestone M2) can be swapped in later.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Tuple

from .pde import ParabolicPDE


class Code:
    """Base class for codes (operators carried by tree particles)."""

    __slots__ = ()


@dataclass(frozen=True)
class Id(Code):
    """The identity code; the root of the tree for representing u itself."""

    __slots__ = ()


@dataclass(frozen=True)
class Dx(Code):
    """The spatial derivative code d^order/dx^order (order >= 1)."""

    order: int = 1


@dataclass(frozen=True)
class FDeriv(Code):
    """The code (a f^{(k)})*, i.e. evaluate a * f^{(k)} at u.

    JEQ2023 writes this g* with g = a f^{(k)}, a != 0, k >= 0.
    """

    a: float = 1.0
    k: int = 0


@dataclass(frozen=True)
class FNu(Code):
    """The general code (a d^nu f)*, nu a multi-index over (z0, ..., zn).

    Evaluate a * (d_{z0}^{nu_0} ... d_{zn}^{nu_n} f) at the solution jet
    (u, du/dx, ..., d^n u/dx^n).  Generalizes FDeriv (which is the n = 0
    case with nu = (k,)).
    """

    a: float
    nu: Tuple[int, ...]


CodeTuple = Tuple[Code, ...]
F_STAR = FDeriv(1.0, 0)  # the plain code f*


class SemilinearMechanism:
    """Hand-coded mechanism for semilinear PDEs, JEQ2023 eq. (2.7), d = 1."""

    @staticmethod
    @lru_cache(maxsize=None)
    def tuples(code: Code) -> Tuple[CodeTuple, ...]:
        """The family M(code) of code tuples; drawn uniformly at branching."""
        if isinstance(code, Id):
            return ((F_STAR,),)
        if isinstance(code, FDeriv):
            a, k = code.a, code.k
            return (
                (F_STAR, FDeriv(a, k + 1)),
                (Dx(1), Dx(1), FDeriv(-a / 2.0, k + 2)),
            )
        if isinstance(code, Dx):
            if code.order != 1:
                # Never produced by (2.7); general d^k/dx^k arrives with the
                # fully nonlinear mechanism (M2), eq. (2.5).
                raise NotImplementedError(
                    "semilinear mechanism only produces first derivatives"
                )
            return ((FDeriv(1.0, 1), Dx(1)),)
        raise TypeError(f"unknown code {code!r}")

    @staticmethod
    def terminal(code: Code, pde: ParabolicPDE, x: float) -> float:
        """Evaluate c(u)(T, x) on the terminal condition phi."""
        if isinstance(code, Id):
            return pde.phi(x)
        if isinstance(code, Dx):
            return pde.phi_derivative(code.order)(x)
        if isinstance(code, FDeriv):
            fk = pde.f_derivative(code.k)
            if fk is None:
                return 0.0
            return code.a * fk(pde.phi(x))
        raise TypeError(f"unknown code {code!r}")

    @staticmethod
    def is_identically_zero(code: Code, pde: ParabolicPDE) -> bool:
        """True if the code operator is identically zero (exact pruning).

        If g = a f^{(k)} with f^{(k)} == 0, the whole subtree rooted at g*
        contributes H = 0 almost surely: if the particle reaches the horizon
        its leaf factor is g(phi) = 0; if it branches, every tuple in M(g*)
        contains a descendant of g ((g')* or (g'')*), which is again
        identically zero -- by induction some leaf factor in the subtree
        always vanishes.  Returning 0 immediately is therefore exact (it
        removes zero-valued samples, not just their expectation).
        """
        return isinstance(code, FDeriv) and pde.f_derivative(code.k) is None


class FullyNonlinearMechanism1D:
    """General mechanism for fully nonlinear PDEs, JEQ2023 eqs. (2.4)-(2.5).

    Bound to one FullyNonlinearPDE1D instance (memoized per PDE).  Raw code
    tables depend only on n; with ``reduce_zero_tuples`` (default) any tuple
    containing a code (a d^nu f)* with d^nu f identically zero is dropped
    from M(c).  This is exact: such a code spawns a subtree whose H vanishes
    almost surely (every tuple in its mechanism contains a further
    derivative of it, so by induction a zero leaf factor always occurs),
    hence the dropped tuples contribute zero-valued samples only.  The
    uniform probability q_c adapts to the reduced set |M(c)| -- the mean is
    unchanged, the variance is smaller.  If reduction would empty M(c), one
    zero tuple is kept so the sampler still returns a (zero) sample.

    Structure of the raw tables (m = n + 1 arguments of f):

        M(Id)     = { (f*,) }
        M(d^k)    = { (c * (d^lam f)*,  d^{q+l} repeated mult times ...) }
                    over the Faa di Bruno terms of order k (fdb_terms(m, k))
        M(g*),    g = a d^nu f:
            { (f*, (a d^{nu+e0} f)*) }
          U { ((a d^{nu+ek} f)*, c*(d^lam f)*, d^{q+l}...) : k = 1..n,
              FdB terms of order k }
          U { ((-a/2 d^{nu+ej+el} f)*, d^{j+1}, d^{l+1}) : j, l = 0..n }

    where the FdB integer constant c and all real coefficients live in the
    ``a`` of the produced FNu codes, never in the sampling weights.
    """

    def __init__(self, pde, reduce_zero_tuples: bool = True) -> None:
        self.pde = pde
        self.n = pde.n
        self.reduce_zero_tuples = reduce_zero_tuples
        self._tuples_cache: dict = {}

    # -- raw tables ---------------------------------------------------------
    def _fdb_tuple(self, term, f_coeff: float, prefix: Tuple[Code, ...]) -> CodeTuple:
        from .fdb import FdBTerm  # noqa: F401  (documentation import)

        codes = list(prefix)
        codes.append(FNu(f_coeff * term.coeff, term.lam))
        for l, q, mult in term.blocks:
            codes.extend([Dx(q + l)] * mult)
        return tuple(codes)

    def _raw_tuples(self, code: Code) -> Tuple[CodeTuple, ...]:
        from .fdb import fdb_terms

        m = self.n + 1
        zero_nu = (0,) * m
        if isinstance(code, Id):
            return ((FNu(1.0, zero_nu),),)
        if isinstance(code, Dx):
            return tuple(
                self._fdb_tuple(term, 1.0, ())
                for term in fdb_terms(m, code.order)
            )
        if isinstance(code, FNu):
            a, nu = code.a, code.nu
            out = [(FNu(1.0, zero_nu), FNu(a, _bump(nu, 0)))]
            for k in range(1, self.n + 1):
                prefix = (FNu(a, _bump(nu, k)),)
                for term in fdb_terms(m, k):
                    out.append(self._fdb_tuple(term, 1.0, prefix))
            for j in range(self.n + 1):
                for l in range(self.n + 1):
                    out.append(
                        (FNu(-a / 2.0, _bump(_bump(nu, j), l)),
                         Dx(j + 1), Dx(l + 1))
                    )
            return tuple(out)
        raise TypeError(f"unknown code {code!r}")

    # -- protocol -----------------------------------------------------------
    def tuples(self, code: Code) -> Tuple[CodeTuple, ...]:
        if code not in self._tuples_cache:
            raw = self._raw_tuples(code)
            if self.reduce_zero_tuples:
                reduced = tuple(
                    tpl for tpl in raw
                    if not any(self.is_identically_zero(c, self.pde)
                               for c in tpl)
                )
                # keep one zero tuple if everything vanished, so the sampler
                # still produces a (zero-valued) sample instead of crashing
                raw = reduced if reduced else raw[:1]
            self._tuples_cache[code] = raw
        return self._tuples_cache[code]

    def terminal(self, code: Code, pde, x: float) -> float:
        """Evaluate c(u)(T, x) on the terminal condition phi."""
        if isinstance(code, Id):
            return pde.phi_k(0)(x)
        if isinstance(code, Dx):
            return pde.phi_k(code.order)(x)
        if isinstance(code, FNu):
            fn = pde.f_nu(code.nu)
            if fn is None:
                return 0.0
            return code.a * fn(*pde.phi_jet(x))
        raise TypeError(f"unknown code {code!r}")

    def is_identically_zero(self, code: Code, pde=None) -> bool:
        """True iff code = (a d^nu f)* with d^nu f identically zero.

        Dx codes are never pruned: phi^{(m)} == 0 does NOT imply that
        d^m u(t, .) vanishes at earlier times t < T.
        """
        return isinstance(code, FNu) and self.pde.f_nu(code.nu) is None


def _bump(nu: Tuple[int, ...], k: int) -> Tuple[int, ...]:
    """nu + e_k."""
    return nu[:k] + (nu[k] + 1,) + nu[k + 1:]
