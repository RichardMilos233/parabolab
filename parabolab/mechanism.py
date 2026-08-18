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
