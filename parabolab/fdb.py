"""Faa di Bruno combinatorics for the fully nonlinear mechanism (d = 1).

JEQ2023 Prop. 1.1 (one space dimension): for g in C^k(R^m) applied to the
jet (v, dv, ..., d^n v), m = n + 1,

    d^k/dx^k g(v, ..., d^n v)
      = sum over terms  coeff * (d^lam g)(v, ..., d^n v)
                              * prod over blocks (l, q) with multiplicity mult
                                    ( d^{q+l} v ) ^ mult ,

where a *term* is a multiset of blocks {(l, q): mult} with l >= 1 the block
size, q in {0..n} the argument hit by the block, and sum of l * mult = k.
Then lam_q = sum_l mult_{l,q} and

    coeff = k! / prod_{(l,q)} ( mult_{l,q}! * (l!)^{mult_{l,q}} )  (an integer).

This is the same enumeration as the authors' `deep_branching/fdb.py`
(`fdb_nd(m, (k,))`), against which we cross-check in the tests.  Unlike the
paper's displayed examples, equal tuples are NOT listed multiple times;
their multiplicity is carried by the integer coefficient (e.g. the
(d_{z0}d_{z1}f, dx, dx^2) term of M(dx^2) at n = 1 has coeff = 2, which the
paper prints as two coefficient-1 copies -- the branching expectation is
identical either way).
"""

from __future__ import annotations

import math
from functools import lru_cache
from typing import NamedTuple, Tuple


class FdBTerm(NamedTuple):
    """One term of the (d=1) multivariate Faa di Bruno expansion."""

    coeff: int
    lam: Tuple[int, ...]              # derivative multi-index on g, length m
    blocks: Tuple[Tuple[int, int, int], ...]  # sorted (l, q, mult), mult >= 1


@lru_cache(maxsize=None)
def fdb_terms(m: int, k: int) -> Tuple[FdBTerm, ...]:
    """All Faa di Bruno terms for d^k/dx^k g(v, dv, ..., d^{m-1} v), k >= 1.

    m is the number of arguments of g (= n + 1 for the jet up to order n).
    """
    if k < 1:
        raise ValueError("k must be >= 1")
    pairs = [(l, q) for l in range(1, k + 1) for q in range(m)]
    out = []

    def rec(idx: int, remaining: int, chosen):
        if remaining == 0:
            out.append(_make_term(m, k, chosen))
            return
        if idx == len(pairs):
            return
        l, q = pairs[idx]
        for mult in range(remaining // l, -1, -1):
            rec(idx + 1, remaining - mult * l,
                chosen + [(l, q, mult)] if mult else chosen)

    rec(0, k, [])
    return tuple(out)


def _make_term(m: int, k: int, blocks) -> FdBTerm:
    lam = [0] * m
    denom = 1
    for l, q, mult in blocks:
        lam[q] += mult
        denom *= math.factorial(mult) * math.factorial(l) ** mult
    coeff, rem = divmod(math.factorial(k), denom)
    assert rem == 0, "Faa di Bruno coefficient must be an integer"
    return FdBTerm(coeff=coeff, lam=tuple(lam), blocks=tuple(sorted(blocks)))
