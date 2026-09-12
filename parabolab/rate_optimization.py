"""Deterministic rate derivatives and scalar rate optimizer for coding-tree Monte Carlo."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np

from .mechanism import Code, Id, SemilinearMechanism
from .moments import MomentQuadrature, TupleProposal, _validate_proposal
from .pde import ParabolicPDE


@dataclass(frozen=True)
class RateMomentDerivatives:
    """Second-moment value and its derivatives with respect to branching clock rate lambda."""

    value: float
    d_rate: float
    d2_rate: float


@dataclass(frozen=True)
class RateOptimizationResult:
    """Outcome of scalar branching clock rate optimization."""

    rate: float
    second_moment: float
    d_rate: float
    d2_rate: float
    converged: bool
    iterations: int
    bracket: tuple[float, float]


def riccati_binary_second_moment(
    T: float,
    rate: float,
) -> float:
    """Exact second moment for u_t + 1/2 u_xx + u^2 = 0 with phi == 1.

    The second moment satisfies Y'(r) = (e^{rate * r} / rate) * Y(r)^2 with Y(0) = 1,
    giving V(T; rate) = (rate^2 * e^{rate * T}) / (rate^2 + 1 - e^{rate * T}).
    Valid when rate^2 + 1 - e^{rate * T} > 0.
    """
    if T <= 0.0:
        return 1.0
    if rate <= 0.0:
        raise ValueError(f"rate must be positive, got {rate}")

    exp_term = math.exp(rate * T)
    denom = rate**2 + 1.0 - exp_term
    if denom <= 0.0:
        return float("inf")
    return (rate**2 * exp_term) / denom


def finite_depth_moment_derivatives_1d(
    pde: ParabolicPDE,
    t: float,
    x: float,
    *,
    code: Code = Id(),
    max_depth: int,
    rate: float,
    mechanism=None,
    tuple_proposal: Optional[TupleProposal] = None,
    quadrature: MomentQuadrature = MomentQuadrature(),
    prune_zero: bool = True,
) -> RateMomentDerivatives:
    """Evaluate V_{c, max_depth}^{(2)}(t, x) and its exact first and second derivatives wrt rate.

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
    max_depth : int
        Maximum branch depth (non-negative integer).
    rate : float
        Branching clock rate lambda > 0.
    mechanism : optional mechanism provider.
    tuple_proposal : optional proposal generator.
    quadrature : MomentQuadrature
        Quadrature orders for time and Gaussian integration.
    prune_zero : bool
        If True, return 0.0 immediately for identically zero codes.
    """
    if isinstance(x, (np.ndarray, list, tuple)):
        arr_x = np.asarray(x)
        if arr_x.ndim > 0 and arr_x.size > 1:
            raise ValueError(
                f"finite_depth_moment_derivatives_1d only supports scalar 1D problems, got {arr_x.shape}"
            )
        x_val = float(arr_x.item())
    else:
        x_val = float(x)

    if getattr(pde, "d", 1) > 1:
        raise ValueError(
            f"finite_depth_moment_derivatives_1d only supports 1D problems, got pde.d={pde.d}"
        )

    if max_depth < 0:
        raise ValueError(f"max_depth must be non-negative, got {max_depth}")
    if rate <= 0.0:
        raise ValueError(f"rate must be strictly positive, got {rate}")

    if mechanism is None:
        mechanism = getattr(pde, "mechanism", None) or SemilinearMechanism

    sig = math.sqrt(getattr(pde, "sigma2", 1.0))

    # Precompute Gauss-Hermite nodes/weights
    gh_nodes, gh_weights = np.polynomial.hermite.hermgauss(quadrature.normal_order)
    # Precompute Gauss-Legendre nodes/weights on [-1, 1]
    gl_nodes, gl_weights = np.polynomial.legendre.leggauss(quadrature.time_order)

    def _gaussian_expectation_triplet(
        func: Callable[[float], tuple[float, float, float]],
        loc: float,
        std: float,
    ) -> tuple[float, float, float]:
        if std <= 0.0:
            return func(loc)
        scale = std * math.sqrt(2.0)
        tot0 = 0.0
        tot1 = 0.0
        tot2 = 0.0
        for xi, w in zip(gh_nodes, gh_weights):
            v0, v1, v2 = func(loc + scale * xi)
            tot0 += w * v0
            tot1 += w * v1
            tot2 += w * v2
        c = 1.0 / math.sqrt(math.pi)
        return tot0 * c, tot1 * c, tot2 * c

    def _eval(c: Code, curr_t: float, curr_x: float, depth: int) -> tuple[float, float, float]:
        if prune_zero and mechanism.is_identically_zero(c, pde):
            return 0.0, 0.0, 0.0

        delta = pde.T - curr_t
        if delta < 0.0:
            return 0.0, 0.0, 0.0

        # Leaf term: e^{rate * delta} * E[|terminal|^2]
        def _terminal_sq(y: float) -> tuple[float, float, float]:
            term = float(mechanism.terminal(c, pde, y))
            return term * term, 0.0, 0.0

        exp_d = math.exp(rate * delta)
        leaf_spatial, _, _ = _gaussian_expectation_triplet(_terminal_sq, curr_x, sig * math.sqrt(delta))

        val_leaf = exp_d * leaf_spatial
        d1_leaf = delta * exp_d * leaf_spatial
        d2_leaf = (delta**2) * exp_d * leaf_spatial

        if depth >= max_depth or delta == 0.0:
            return val_leaf, d1_leaf, d2_leaf

        tuples = mechanism.tuples(c)
        if not tuples:
            return val_leaf, d1_leaf, d2_leaf

        val_branch = 0.0
        d1_branch = 0.0
        d2_branch = 0.0

        s_nodes = 0.5 * delta * (gl_nodes + 1.0)
        time_weights = 0.5 * delta * gl_weights

        # Weight factor w(rate, s) = e^{rate * s} / rate
        # dw/d_rate = (s * rate - 1) * e^{rate * s} / rate^2
        # d2w/d_rate^2 = [(s * rate - 1)^2 + 1] * e^{rate * s} / rate^3
        for s, w_t in zip(s_nodes, time_weights):
            if s <= 0.0 or s >= delta:
                continue

            if tuple_proposal is None:
                probs = np.full(len(tuples), 1.0 / len(tuples))
            else:
                raw_probs = tuple_proposal(c, curr_t, curr_x, s, depth, tuples)
                probs = _validate_proposal(raw_probs, len(tuples))

            exp_s = math.exp(rate * s)
            w_val = exp_s / rate
            w_d1 = (s * rate - 1.0) * exp_s / (rate**2)
            w_d2 = (((s * rate - 1.0) ** 2) + 1.0) * exp_s / (rate**3)

            def _spatial_triplet(y: float) -> tuple[float, float, float]:
                tot_v = 0.0
                tot_d1 = 0.0
                tot_d2 = 0.0

                for Z_tuple, prob in zip(tuples, probs):
                    inv_q = 1.0 / prob
                    # Product of child continuation values and its Leibniz product rule derivatives
                    # P = \prod_j V_j
                    # P' = P * \sum_j (V_j' / V_j)
                    # P'' = \sum_j V_j'' \prod_{k \ne j} V_k + 2 \sum_{j < k} V_j' V_k' \prod_{l \ne j, k} V_l
                    if len(Z_tuple) == 0:
                        tot_v += inv_q
                    elif len(Z_tuple) == 1:
                        child_res = _eval(Z_tuple[0], curr_t + s, y, depth + 1)
                        tot_v += inv_q * child_res[0]
                        tot_d1 += inv_q * child_res[1]
                        tot_d2 += inv_q * child_res[2]
                    elif len(Z_tuple) == 2:
                        c1 = _eval(Z_tuple[0], curr_t + s, y, depth + 1)
                        c2 = _eval(Z_tuple[1], curr_t + s, y, depth + 1)
                        prod_v = c1[0] * c2[0]
                        prod_d1 = c1[1] * c2[0] + c1[0] * c2[1]
                        prod_d2 = c1[2] * c2[0] + 2.0 * c1[1] * c2[1] + c1[0] * c2[2]
                        tot_v += inv_q * prod_v
                        tot_d1 += inv_q * prod_d1
                        tot_d2 += inv_q * prod_d2
                    else:
                        # General multitype branch product
                        child_results = [_eval(cz, curr_t + s, y, depth + 1) for cz in Z_tuple]
                        m = len(child_results)
                        # Compute prod_v
                        prod_v = 1.0
                        for cr in child_results:
                            prod_v *= cr[0]

                        # Compute prod_d1
                        prod_d1 = 0.0
                        for j in range(m):
                            term = child_results[j][1]
                            for k in range(m):
                                if k != j:
                                    term *= child_results[k][0]
                            prod_d1 += term

                        # Compute prod_d2
                        prod_d2 = 0.0
                        for j in range(m):
                            term2 = child_results[j][2]
                            for k in range(m):
                                if k != j:
                                    term2 *= child_results[k][0]
                            prod_d2 += term2

                        for j in range(m):
                            for k in range(j + 1, m):
                                term_cross = 2.0 * child_results[j][1] * child_results[k][1]
                                for l_idx in range(m):
                                    if l_idx != j and l_idx != k:
                                        term_cross *= child_results[l_idx][0]
                                prod_d2 += term_cross

                        tot_v += inv_q * prod_v
                        tot_d1 += inv_q * prod_d1
                        tot_d2 += inv_q * prod_d2

                return tot_v, tot_d1, tot_d2

            sp_v, sp_d1, sp_d2 = _gaussian_expectation_triplet(_spatial_triplet, curr_x, sig * math.sqrt(s))

            # Product w(rate, s) * S(rate, s)
            node_v = w_val * sp_v
            node_d1 = w_d1 * sp_v + w_val * sp_d1
            node_d2 = w_d2 * sp_v + 2.0 * w_d1 * sp_d1 + w_val * sp_d2

            val_branch += w_t * node_v
            d1_branch += w_t * node_d1
            d2_branch += w_t * node_d2

        return val_leaf + val_branch, d1_leaf + d1_branch, d2_leaf + d2_branch

    v, d1, d2 = _eval(code, t, x_val, 0)
    return RateMomentDerivatives(value=v, d_rate=d1, d2_rate=d2)


def optimize_exponential_rate_1d(
    pde: ParabolicPDE,
    t: float,
    x: float,
    *,
    code: Code = Id(),
    max_depth: int = 1,
    bracket: tuple[float, float] = (0.05, 10.0),
    tol: float = 1e-5,
    max_iter: int = 40,
    quadrature: MomentQuadrature = MomentQuadrature(),
    mechanism=None,
    tuple_proposal: Optional[TupleProposal] = None,
    prune_zero: bool = True,
) -> RateOptimizationResult:
    """Find a constrained branching-clock minimizer within ``bracket``.

    Uses safeguarded bisection combined with Newton-Raphson on ``d_rate == 0``.
    If the derivative has the appropriate monotone sign at an endpoint, that
    endpoint is returned as a valid converged constrained minimum.  This is
    not a claim of an unconstrained or global minimum.  ``tuple_proposal``
    must be fixed independently of the candidate rate; it and the mechanism
    and pruning choice are forwarded unchanged to every moment evaluation.
    """
    try:
        lo, hi = bracket
        lo = float(lo)
        hi = float(hi)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"Invalid bracket: {bracket!r}. Must contain finite 0 < lo < hi.") from exc
    if not (math.isfinite(lo) and math.isfinite(hi) and 0.0 < lo < hi):
        raise ValueError(f"Invalid bracket: {bracket}. Must satisfy 0 < lo < hi.")
    try:
        tol = float(tol)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"tol must be positive and finite, got {tol}") from exc
    if not math.isfinite(tol) or tol <= 0.0:
        raise ValueError(f"tol must be positive and finite, got {tol}")
    if isinstance(max_iter, bool) or not isinstance(max_iter, (int, np.integer)) or max_iter <= 0:
        raise ValueError(f"max_iter must be a positive integer, got {max_iter}")
    if isinstance(max_depth, bool) or not isinstance(max_depth, (int, np.integer)) or max_depth < 0:
        raise ValueError(f"max_depth must be a non-negative integer, got {max_depth}")
    max_iter = int(max_iter)
    max_depth = int(max_depth)

    def _checked_moment(rate: float) -> RateMomentDerivatives:
        result = finite_depth_moment_derivatives_1d(
            pde,
            t,
            x,
            code=code,
            max_depth=max_depth,
            rate=rate,
            mechanism=mechanism,
            tuple_proposal=tuple_proposal,
            quadrature=quadrature,
            prune_zero=prune_zero,
        )
        values = (result.value, result.d_rate, result.d2_rate)
        if not all(math.isfinite(value) for value in values):
            raise ValueError(
                f"Non-finite moment or derivative evaluation at rate={rate}: {values}"
            )
        return result

    res_lo = _checked_moment(lo)
    res_hi = _checked_moment(hi)

    if res_lo.d_rate >= 0.0:
        # Minimum is at or to the left of lo
        return RateOptimizationResult(
            rate=lo,
            second_moment=res_lo.value,
            d_rate=res_lo.d_rate,
            d2_rate=res_lo.d2_rate,
            converged=True,
            iterations=0,
            bracket=bracket,
        )

    if res_hi.d_rate <= 0.0:
        # Minimum is at or to the right of hi
        return RateOptimizationResult(
            rate=hi,
            second_moment=res_hi.value,
            d_rate=res_hi.d_rate,
            d2_rate=res_hi.d2_rate,
            converged=True,
            iterations=0,
            bracket=bracket,
        )

    curr_lo = lo
    curr_hi = hi
    curr_rate = 0.5 * (lo + hi)

    iterations = 0
    converged = False

    for i in range(1, max_iter + 1):
        iterations = i
        res = _checked_moment(curr_rate)

        if abs(res.d_rate) < tol or (curr_hi - curr_lo) < tol:
            converged = True
            break

        if res.d_rate < 0.0:
            curr_lo = curr_rate
        else:
            curr_hi = curr_rate

        # Try Newton step if second derivative is positive
        newton_success = False
        if res.d2_rate > 1e-12:
            step = -res.d_rate / res.d2_rate
            cand = curr_rate + step
            if curr_lo < cand < curr_hi:
                curr_rate = cand
                newton_success = True

        if not newton_success:
            curr_rate = 0.5 * (curr_lo + curr_hi)

    final_res = _checked_moment(curr_rate)

    return RateOptimizationResult(
        rate=curr_rate,
        second_moment=final_res.value,
        d_rate=final_res.d_rate,
        d2_rate=final_res.d2_rate,
        converged=converged or abs(final_res.d_rate) < 5.0 * tol,
        iterations=iterations,
        bracket=(curr_lo, curr_hi),
    )
