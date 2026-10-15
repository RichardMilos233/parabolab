"""Vectorized full-tree sampler for flat polynomial semilinear PDEs.

For the raw uniform ``SemilinearMechanism`` with a globally constant terminal
value ``a`` (so ``phi' == 0``), a coding tree's value depends only on its codes
and branching times:

* the Brownian positions never enter, because every terminal factor is a
  constant ``f^(k)(a)`` or ``a``;
* the tuple ``(Dx, Dx, (-a/2 f^(k+2))*)`` yields ``H = 0`` pathwise, because
  a ``Dx`` subtree only reproduces ``Dx`` and ends in a leaf ``phi'(x) = 0``;
* ``H`` is the product of its node factors, so a tree needs no stored
  structure: each particle carries its sample index, its code and its birth
  time, and its factor is accumulated into that sample's ``log|H|`` and sign.

Under these assumptions the sampled ``H`` has the same distribution as
``sample_tree`` with ``prune_zero=True``; the random stream and the visit
order differ, so individual draws do not coincide. A sample is abandoned as
soon as it is known to be zero. Node counts therefore cover the particles
actually visited here (including pruned identically-zero codes, as in
``sample_tree``) and exclude ``Dx`` subtrees and the remainder of trees
already known to be zero. They are not comparable with ``sample_tree`` counts.
"""

from __future__ import annotations

import math
from typing import Optional, Tuple

import numpy as np

from .mechanism import SemilinearMechanism
from .pde import ParabolicPDE


def flat_semilinear_leaf_values(pde: ParabolicPDE, flat_terminal: float) -> np.ndarray:
    """Return ``[f(a), f'(a), ..., f^(K-1)(a)]`` after checking the assumptions.

    Codes ``f^(k)`` with ``k >= K`` are identically zero (the polynomial
    ``f_derivatives`` convention). The caller asserts that ``phi == a``
    globally; sampled values of ``phi`` and ``phi'`` can only reject obvious
    mismatches.
    """
    if not isinstance(pde, ParabolicPDE):
        raise TypeError("the flat sampler requires a semilinear ParabolicPDE")
    if getattr(pde, "_mechanism", None) not in (None, SemilinearMechanism):
        raise ValueError("the flat sampler requires the raw uniform SemilinearMechanism")
    if callable(pde.f_derivatives):
        raise TypeError("the flat sampler requires polynomial (sequence) f_derivatives")
    if flat_terminal is None or not math.isfinite(flat_terminal):
        raise ValueError("flat_terminal must declare the constant terminal value")
    a = float(flat_terminal)
    xs = (-1.0, 0.0, 1.0)
    if any(not math.isclose(float(pde.phi(x)), a, rel_tol=1e-10, abs_tol=1e-12) for x in xs):
        raise ValueError("phi samples disagree with the asserted flat_terminal")
    if not pde.phi_derivatives or any(
        not math.isclose(float(pde.phi_derivatives[0](x)), 0.0, abs_tol=1e-12) for x in xs
    ):
        raise ValueError("the flat sampler requires phi' provided and equal to zero")
    values = np.array([float(g(a)) for g in (pde.f, *pde.f_derivatives)])
    if not np.all(np.isfinite(values)):
        raise ValueError("f derivatives must be finite at flat_terminal")
    return values


def sample_flat_batch(
    leaf_values: np.ndarray,
    flat_terminal: float,
    T: float,
    rate: float,
    n: int,
    rng: np.random.Generator,
    max_nodes: Optional[int] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Draw ``n`` independent root-``Id`` trees started at ``t = 0``.

    Returns ``(values, nodes, exceeded)``. ``exceeded[i]`` marks a tree whose
    visited-node count passed ``max_nodes``; its value is NaN. Values that
    overflow are returned as non-finite numbers for the caller to classify.
    """
    leaf = np.append(np.asarray(leaf_values, dtype=float), float(flat_terminal))
    n_codes = len(leaf) - 1           # code -1 (Id) indexes the appended phi value
    log_rate = math.log(rate)
    log_abs = np.zeros(n)
    negatives = np.zeros(n, dtype=np.int64)
    nodes = np.zeros(n, dtype=np.int64)
    dead = np.zeros(n, dtype=bool)    # value known to be zero
    exceeded = np.zeros(n, dtype=bool)

    sid = np.arange(n)
    code = np.full(n, -1, dtype=np.int64)
    born = np.zeros(n)
    while sid.size:
        nodes += np.bincount(sid, minlength=n)
        if max_nodes is not None:
            exceeded |= nodes > max_nodes
        tau = rng.exponential(1.0 / rate, sid.size)
        remaining = T - born
        is_leaf = tau > remaining

        # Leaves: f^(k)(a) (or a for Id) times the survival weight e^{rate r}.
        ls = sid[is_leaf]
        factor = leaf[code[is_leaf]]
        zero = factor == 0.0
        dead[ls[zero]] = True
        ls, factor, r = ls[~zero], factor[~zero], remaining[is_leaf][~zero]
        log_abs += np.bincount(ls, weights=np.log(np.abs(factor)) + rate * r, minlength=n)
        negatives += np.bincount(ls[factor < 0.0], minlength=n)

        # Branches: Id -> (f*), weight e^{rate tau}/rate; f^(k) -> uniform over
        # {(f*, f^(k+1)), (Dx, Dx, ...)}, weight 2 e^{rate tau}/rate.
        bs, bc = sid[~is_leaf], code[~is_leaf]
        btau = tau[~is_leaf]
        child_t = born[~is_leaf] + btau
        is_id = bc < 0
        deriv = np.flatnonzero(~is_id)
        dx = deriv[rng.random(deriv.size) < 0.5]
        dead[bs[dx]] = True
        keep = np.ones(bs.size, dtype=bool)
        keep[dx] = False
        bs, bc, btau, child_t, is_id = bs[keep], bc[keep], btau[keep], child_t[keep], is_id[keep]
        log_abs += np.bincount(
            bs, weights=np.where(is_id, 0.0, math.log(2.0)) + rate * btau - log_rate,
            minlength=n,
        )
        second = ~is_id
        s_sid, s_code, s_t = bs[second], bc[second] + 1, child_t[second]
        pruned = s_code >= n_codes   # identically zero: one visited node, H = 0
        nodes += np.bincount(s_sid[pruned], minlength=n)
        dead[s_sid[pruned]] = True

        sid = np.concatenate((bs, s_sid[~pruned]))
        code = np.concatenate((np.zeros(bs.size, dtype=np.int64), s_code[~pruned]))
        born = np.concatenate((child_t, s_t[~pruned]))
        alive = ~(dead[sid] | exceeded[sid])
        sid, code, born = sid[alive], code[alive], born[alive]

    if max_nodes is not None:
        exceeded |= nodes > max_nodes
    with np.errstate(over="ignore"):
        magnitude = np.exp(log_abs)
    values = np.where(negatives % 2 == 1, -magnitude, magnitude)
    values[dead] = 0.0
    values[exceeded] = np.nan
    return values, nodes, exceeded
