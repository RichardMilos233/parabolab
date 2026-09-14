"""Rate selection for a prescribed weighted 1D solution profile.

The deterministic selector minimizes a finite-depth quadrature objective.
Its convergence flag is not a full-tree or global variance certificate.
"""

from __future__ import annotations

import math
import numpy as np

from .moments import MomentQuadrature
from .pde import ParabolicPDE
from .rate_optimization import (
    RateMomentDerivatives, RateOptimizationResult, finite_depth_moment_derivatives_1d,
)


def _weighted_grid(grid, weights=None):
    x = np.asarray(grid, dtype=float)
    w = np.ones(len(x)) if weights is None and x.ndim == 1 else np.asarray(weights, dtype=float)
    if (x.ndim != 1 or x.size == 0 or not np.isfinite(x).all()
            or w.shape != x.shape or not np.isfinite(w).all()
            or np.any(w < 0) or not np.any(w > 0)):
        raise ValueError('require a finite nonempty 1D grid and nonnegative, nonzero matching weights')
    # Scaling first prevents overflow when valid unnormalized weights are large.
    w = w / w.max()
    return x, w / w.sum()


def short_time_profile_rate(pde: ParabolicPDE, grid, weights=None) -> float:
    """Leading small-horizon rate sqrt(sum w*f(phi)^2 / sum w*phi^2).

    This uses terminal factors for the semilinear Id root, with the same
    positive rate used throughout each tree. It is not a finite-horizon
    optimum or a cost optimum. The supplied weights are normalized to sum 1.
    A zero numerator/denominator is a degenerate case requiring an explicit
    policy choice, rather than an automatically valid positive rate.
    """
    if not isinstance(pde, ParabolicPDE) or getattr(pde, 'd', 1) != 1:
        raise ValueError('the terminal heuristic requires a 1D semilinear ParabolicPDE')
    x,w = _weighted_grid(grid, weights)
    terminal = [float(pde.phi(v)) for v in x]
    source = [float(pde.f(v)) for v in terminal]
    if not all(math.isfinite(v) for v in (*terminal,*source)):
        raise ValueError('terminal factors must be finite')
    a = math.hypot(*(math.sqrt(weight)*v for weight,v in zip(w,terminal)))
    b = math.hypot(*(math.sqrt(weight)*v for weight,v in zip(w,source)))
    if not a > 0 or not b > 0 or not math.isfinite(b/a):
        raise ValueError('degenerate terminal objective has no selected positive finite rate')
    return b/a


def profile_moment_derivatives_1d(
    pde, t, grid, *, weights=None, max_depth, rate,
    quadrature=MomentQuadrature(), mechanism=None, tuple_proposal=None, prune_zero=True,
) -> RateMomentDerivatives:
    """Weighted sum of killed-moment quadrature values and rate derivatives."""
    x,w = _weighted_grid(grid, weights)
    moments = [finite_depth_moment_derivatives_1d(
        pde,t,float(position),max_depth=max_depth,rate=rate,quadrature=quadrature,
        mechanism=mechanism,tuple_proposal=tuple_proposal,prune_zero=prune_zero,
    ) for position,weight in zip(x,w) if weight > 0]
    positive = w[w > 0]
    return RateMomentDerivatives(*(math.fsum(weight*getattr(moment, field)
        for weight,moment in zip(positive,moments)) for field in ('value','d_rate','d2_rate')))


def optimize_profile_rate_1d(
    pde, t, grid, *, weights=None, max_depth=2, bracket=(0.2,2.0), tol=1e-5,
    max_iter=40, quadrature=MomentQuadrature(), mechanism=None, tuple_proposal=None,
    prune_zero=True,
) -> RateOptimizationResult:
    """Minimize the weighted finite-depth objective on a fixed rate interval.

    Positive quadrature weights preserve convexity for a fixed proposal.
    Safeguarded Newton/bisection solves the derivative equation; ``tol``
    controls the derivative or bracket-width stopping test, as in the
    pointwise selector. Endpoint optima are allowed. Unlike the pointwise
    selector, this objective explicitly represents the supplied profile.
    It assumes equal numbers of samples per point when interpreted as MSE.
    """
    x,w = _weighted_grid(grid, weights)
    lo,hi = map(float,bracket)
    if not (math.isfinite(lo) and math.isfinite(hi) and 0 < lo < hi):
        raise ValueError('require finite 0 < bracket[0] < bracket[1]')
    if not math.isfinite(tol) or tol <= 0:
        raise ValueError('tol must be finite and positive')
    if type(max_iter) is not int or max_iter < 1 or type(max_depth) is not int or max_depth < 0:
        raise ValueError('require positive integer max_iter and nonnegative integer max_depth')

    def evaluate(rate):
        result = profile_moment_derivatives_1d(
            pde,t,x,weights=w,max_depth=max_depth,rate=rate,quadrature=quadrature,
            mechanism=mechanism,tuple_proposal=tuple_proposal,prune_zero=prune_zero)
        if not all(math.isfinite(v) for v in (result.value,result.d_rate,result.d2_rate)):
            raise ValueError(f'nonfinite weighted moment evaluation at rate {rate}')
        return result

    left,right = evaluate(lo),evaluate(hi)
    if left.d_rate >= 0:
        rate,iterations,converged = lo,0,True
    elif right.d_rate <= 0:
        rate,iterations,converged = hi,0,True
    else:
        rate,converged = (lo+hi)/2,False
        for iterations in range(1,max_iter+1):
            moment = evaluate(rate)
            if abs(moment.d_rate) <= tol or hi-lo <= tol:
                converged = True
                break
            if moment.d_rate < 0:
                lo = rate
            else:
                hi = rate
            proposal = rate-moment.d_rate/moment.d2_rate if moment.d2_rate > 0 else math.nan
            rate = proposal if lo < proposal < hi else (lo+hi)/2
    result = evaluate(rate)
    return RateOptimizationResult(rate,result.value,result.d_rate,result.d2_rate,
                                   converged,iterations,(lo,hi))
