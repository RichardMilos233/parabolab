"""Deterministic finite-depth p-moment quadrature for coding trees in 1D."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Callable, Optional, Sequence

import numpy as np

from .mechanism import Code, Id, SemilinearMechanism
from .pde import ParabolicPDE

TupleProposal = Callable[[Code, float, object, float, int, tuple], Sequence[float]]


@dataclass(frozen=True)
class MomentQuadrature:
    """Quadrature orders for time and Gaussian integration."""

    time_order: int = 12
    normal_order: int = 12

    def __post_init__(self):
        if self.time_order < 1:
            raise ValueError(f"time_order must be >= 1, got {self.time_order}")
        if self.normal_order < 1:
            raise ValueError(f"normal_order must be >= 1, got {self.normal_order}")


def _validate_proposal(probs: Any, n_tuples: int) -> np.ndarray:
    try:
        arr = np.asarray(probs, dtype=float)
    except Exception as exc:
        raise ValueError(f"Proposal probabilities must be numeric, got {probs!r}") from exc
    if arr.ndim != 1 or len(arr) != n_tuples:
        raise ValueError(
            f"Proposal probabilities must be 1D array of length {n_tuples}, got shape {arr.shape}"
        )
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"Proposal probabilities must be finite, got {arr}")
    if np.any(arr <= 0.0):
        raise ValueError(f"Proposal probabilities must be strictly positive, got {arr}")
    if not np.isclose(float(np.sum(arr)), 1.0, atol=1e-12):
        raise ValueError(f"Proposal probabilities must sum to 1.0 within 1e-12, sum is {np.sum(arr)}")
    return arr


def finite_depth_moment_1d(
    pde: ParabolicPDE,
    t: float,
    x: float,
    *,
    code: Code = Id(),
    p: float = 2.0,
    max_depth: int,
    rate: float = 1.0,
    mechanism=None,
    tuple_proposal: Optional[TupleProposal] = None,
    quadrature: MomentQuadrature = MomentQuadrature(),
    prune_zero: bool = True,
) -> float:
    """Compute V_{c, max_depth}^{(p)}(t, x) deterministically via quadrature in 1D.

    Parameters
    ----------
    pde : ParabolicPDE
        The 1D parabolic PDE instance.
    t : float
        Current time in [0, pde.T].
    x : float
        Spatial state (must be scalar).
    code : Code
        Root code (default Id()).
    p : float
        Moment exponent (p > 0, default 2.0).
    max_depth : int
        Maximum branch depth (non-negative integer).
    rate : float
        Exponential jump rate rho(s) = rate * exp(-rate * s).
    mechanism : optional mechanism provider.
    tuple_proposal : optional callable or proposal generator.
    quadrature : MomentQuadrature
        Quadrature orders for Gauss-Legendre (time) and Gauss-Hermite (space).
    prune_zero : bool
        If True, return 0.0 immediately for identically zero codes.
    """
    if isinstance(x, (np.ndarray, list, tuple)):
        arr_x = np.asarray(x)
        if arr_x.ndim > 0 and arr_x.size > 1:
            raise ValueError(
                f"finite_depth_moment_1d only supports scalar 1D problems, got state of shape {arr_x.shape}"
            )
        x_val = float(arr_x.item())
    else:
        x_val = float(x)

    if getattr(pde, "d", 1) > 1:
        raise ValueError(
            f"finite_depth_moment_1d only supports 1D problems, got pde.d={pde.d}"
        )

    if max_depth < 0:
        raise ValueError(f"max_depth must be non-negative, got {max_depth}")
    if p <= 0:
        raise ValueError(f"p must be positive, got {p}")
    if rate <= 0:
        raise ValueError(f"rate must be positive, got {rate}")

    if mechanism is None:
        mechanism = getattr(pde, "mechanism", None) or SemilinearMechanism

    sig = math.sqrt(getattr(pde, "sigma2", 1.0))

    # Precompute Gauss-Hermite nodes/weights for Gaussian expectation
    # int_{-inf}^{inf} e^{-xi^2} g(xi) dxi approx sum w_j g(xi_j)
    gh_nodes, gh_weights = np.polynomial.hermite.hermgauss(quadrature.normal_order)
    # Precompute Gauss-Legendre nodes/weights on [-1, 1]
    gl_nodes, gl_weights = np.polynomial.legendre.leggauss(quadrature.time_order)

    def _gaussian_expectation(func: Callable[[float], float], loc: float, std: float) -> float:
        if std <= 0.0:
            return func(loc)
        # E[h(loc + std * Z)] = pi^{-1/2} sum w_j h(loc + std * sqrt(2) * xi_j)
        scale = std * math.sqrt(2.0)
        total = 0.0
        for xi, w in zip(gh_nodes, gh_weights):
            val = func(loc + scale * xi)
            total += w * val
        return total / math.sqrt(math.pi)

    def _eval_moment(c: Code, curr_t: float, curr_x: float, depth: int) -> float:
        if prune_zero and mechanism.is_identically_zero(c, pde):
            return 0.0

        delta = pde.T - curr_t
        if delta < 0.0:
            return 0.0

        # Leaf term: Fbar(delta)^{1-p} * E[|terminal|^p]
        # Fbar(delta) = exp(-rate * delta) => Fbar(delta)^{1-p} = exp(rate * (p - 1) * delta)
        def _terminal_p(y: float) -> float:
            term = mechanism.terminal(c, pde, y)
            return float(abs(term) ** p)

        leaf_spatial = _gaussian_expectation(_terminal_p, curr_x, sig * math.sqrt(delta))
        leaf_term = math.exp(rate * (p - 1.0) * delta) * leaf_spatial

        if depth >= max_depth or delta == 0.0:
            return leaf_term

        # Branch term:
        # sum_{Z in M(c)} q_c(Z)^{1-p} int_0^delta rho(s)^{1-p} P_s[ prod_{z in Z} V_z^{(p)} ] ds
        tuples = mechanism.tuples(c)
        if not tuples:
            return leaf_term

        # Time integral over [0, delta] via Gauss-Legendre
        # s_i = (delta / 2) * (u_i + 1)
        # ds = (delta / 2) du
        branch_sum = 0.0

        # Compute time nodes
        s_nodes = 0.5 * delta * (gl_nodes + 1.0)
        time_weights = 0.5 * delta * gl_weights

        for s, w_t in zip(s_nodes, time_weights):
            if s <= 0.0 or s >= delta:
                continue

            # Proposal probabilities at this time/state/depth
            if tuple_proposal is None:
                probs = np.full(len(tuples), 1.0 / len(tuples))
            else:
                raw_probs = tuple_proposal(c, curr_t, curr_x, s, depth, tuples)
                probs = _validate_proposal(raw_probs, len(tuples))

            # rho(s)^{1-p} = (rate * exp(-rate * s))^{1-p} = rate^{1-p} * exp(rate * (p - 1) * s)
            rho_factor = (rate ** (1.0 - p)) * math.exp(rate * (p - 1.0) * s)

            # Spatial integrand at branch position y:
            # P_s[ sum_Z q_c(Z)^{1-p} prod_{z in Z} V_z^{(p)}(curr_t + s, y) ]
            def _spatial_integrand(y: float) -> float:
                tot = 0.0
                for Z_tuple, prob in zip(tuples, probs):
                    inv_q = prob ** (1.0 - p)
                    prod_children = 1.0
                    for child_code in Z_tuple:
                        prod_children *= _eval_moment(child_code, curr_t + s, y, depth + 1)
                    tot += inv_q * prod_children
                return tot

            p_s_val = _gaussian_expectation(_spatial_integrand, curr_x, sig * math.sqrt(s))
            branch_sum += w_t * rho_factor * p_s_val

        return leaf_term + branch_sum

    return _eval_moment(code, t, x_val, 0)
