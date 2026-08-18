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
from itertools import product
from typing import Callable, NamedTuple, Optional, Tuple


class FdBTerm(NamedTuple):
    """One term of the (d=1) multivariate Faa di Bruno expansion."""

    coeff: int
    lam: Tuple[int, ...]              # derivative multi-index on g, length m
    blocks: Tuple[Tuple[int, int, int], ...]  # sorted (l, q, mult), mult >= 1


class FdBTermND(NamedTuple):
    """One term of the d-dimensional multivariate Faa di Bruno expansion.

    Block sizes l are now multi-indices over the d space dimensions:

        d^mu g(w_1, ..., w_m) = sum coeff * (d^lam g)(w)
                                    * prod_{(l, q, mult)} (d^l w_q)^mult,

    over multisets of blocks {(l, q): mult}, 0 < l <= mu componentwise
    is NOT required individually but sum(mult * l) = mu is; coefficient

        coeff = mu! / prod_{(l,q)} (mult! * (l!)^mult),   x! := prod x_i!.
    """

    coeff: int
    lam: Tuple[int, ...]                       # multi-index on g, length m
    blocks: Tuple[Tuple[Tuple[int, ...], int, int], ...]  # (l, q, mult)


@lru_cache(maxsize=None)
def fdb_terms(m: int, k: int) -> Tuple[FdBTerm, ...]:
    """All Faa di Bruno terms for d^k/dx^k g(v, dv, ..., d^{m-1} v), k >= 1.

    m is the number of arguments of g (= n + 1 for the jet up to order n).
    Kept as the 1-d interface; implemented via fdb_terms_nd with d = 1.
    """
    if k < 1:
        raise ValueError("k must be >= 1")
    return tuple(
        FdBTerm(t.coeff, t.lam,
                tuple((l[0], q, mult) for l, q, mult in t.blocks))
        for t in fdb_terms_nd(m, (k,))
    )


def fdb_terms_nd(
    m: int,
    mu: Tuple[int, ...],
    live: Optional[Callable[[Tuple[int, ...]], bool]] = None,
) -> Tuple[FdBTermND, ...]:
    """All Faa di Bruno terms for d^mu g(w_1, ..., w_m), |mu| >= 1.

    ``live`` is an optional MONOTONE predicate on the partial derivative
    multi-index lam of g: if live(lam) is False then live(lam') must be
    False for every lam' >= lam componentwise.  Recursion subtrees whose
    partial lam is dead are pruned, so with a polynomial-support predicate
    the enumeration cost is proportional to the *reduced* term set (the key
    to d = 100 tractability), not to the raw one.

    Results for live=None are cached; predicate-filtered calls are not
    (the caller caches its mechanism tables instead).
    """
    if live is None:
        return _fdb_terms_nd_cached(m, mu)
    return _fdb_terms_nd(m, mu, live)


@lru_cache(maxsize=None)
def _fdb_terms_nd_cached(m: int, mu: Tuple[int, ...]) -> Tuple[FdBTermND, ...]:
    return _fdb_terms_nd(m, mu, None)


def _fdb_terms_nd(m, mu, live) -> Tuple[FdBTermND, ...]:
    if sum(mu) < 1:
        raise ValueError("|mu| must be >= 1")
    d = len(mu)
    # candidate block sizes: 0 < l <= mu componentwise, lexicographic order
    # (matches the historical 1-d enumeration order for d = 1)
    ls = [l for l in product(*[range(mi + 1) for mi in mu]) if any(l)]
    ls.sort()
    pairs = [(l, q) for l in ls for q in range(m)]
    out = []
    lam = [0] * m

    def rec(idx: int, remaining: Tuple[int, ...], chosen):
        if not any(remaining):
            out.append(_make_term_nd(m, mu, chosen))
            return
        if idx == len(pairs):
            return
        l, q = pairs[idx]
        max_mult = min(
            (r // li for r, li in zip(remaining, l) if li), default=0
        )
        for mult in range(max_mult, -1, -1):
            if mult:
                lam[q] += mult
                if live is not None and not live(tuple(lam)):
                    lam[q] -= mult
                    continue
                rec(idx + 1,
                    tuple(r - mult * li for r, li in zip(remaining, l)),
                    chosen + [(l, q, mult)])
                lam[q] -= mult
            else:
                rec(idx + 1, remaining, chosen)

    rec(0, tuple(mu), [])
    return tuple(out)


def _multifactorial(v) -> int:
    out = 1
    for vi in v:
        out *= math.factorial(vi)
    return out


def _make_term_nd(m: int, mu, blocks) -> FdBTermND:
    lam = [0] * m
    denom = 1
    for l, q, mult in blocks:
        lam[q] += mult
        denom *= math.factorial(mult) * _multifactorial(l) ** mult
    coeff, rem = divmod(_multifactorial(mu), denom)
    assert rem == 0, "Faa di Bruno coefficient must be an integer"
    return FdBTermND(coeff=coeff, lam=tuple(lam), blocks=tuple(sorted(blocks)))
