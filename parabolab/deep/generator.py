"""Batched training-data generator for the deep branching solver.

For each of N training states (tau_i, X_i) we draw M independent tree
samples H_{i,1..M} with Algorithm 1 (the M3 sampler) and store the
outlier-filtered mean as the regression target y_i, following the
authors' branch.py convention: with (lo, hi) the (p, 100-p) percentiles
of the M values, samples outside [lo - c(hi-lo), hi + c(hi-lo)]
(default p = 1, c = 1000) and non-finite samples are dropped.  Because
minimizing sum_j (H_{i,j} - v)^2 over v and minimizing (mean_j H_{i,j}
- v)^2 have the same argmin, regressing on the per-state mean is
equivalent to the paper's eq. (3.6) up to a v-independent constant.

Training states follow JCP2024 Remark 3.1 (vi): tau_i in a (possibly
degenerate) interval [t_lo, t_hi] (default {0}), X_i uniform on the
segment [x_lo, x_hi] x {x_mid}^{d-1} widened by ``overtrain_rate``
(authors' 10% overtrain of the x-domain).

The per-state Monte Carlo work is fanned out over worker processes,
reusing parallel.py's per-process PDE cache.
"""

from __future__ import annotations

import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np

from ..parallel import _PDE_CACHE, _factory_key
from ..tree import jcp_rate, sample_tree


@dataclass
class TrainingData:
    """N training states with their MC regression targets."""

    t: np.ndarray          # (N,)   tau_i
    x: np.ndarray          # (N, d) X_i
    y: np.ndarray          # (N,)   outlier-filtered mean of M tree samples
    stderr: np.ndarray     # (N,)   stderr of the filtered mean
    n_kept: np.ndarray     # (N,)   samples kept by the outlier filter
    m_samples: int
    rate: float
    seconds: float

    def __len__(self) -> int:
        return len(self.t)


def _state_target(args):
    """Worker: M tree samples at one state -> filtered mean + diagnostics."""
    (factory, t, x, m, seed, rate, code,
     outlier_percentile, outlier_multiplier) = args
    key = _factory_key(factory)
    pde = _PDE_CACHE.get(key)
    if pde is None:
        pde = _PDE_CACHE[key] = factory()
    rng = np.random.default_rng(seed)
    kwargs = {} if code is None else {"code": code}
    vals = np.empty(m)
    for j in range(m):
        vals[j] = sample_tree(pde, t, x, rng=rng, rate=rate, **kwargs).value

    finite = np.isfinite(vals)
    v = vals[finite]
    if len(v) == 0:
        return np.nan, np.nan, 0
    lo, hi = np.percentile(
        v, [outlier_percentile, 100.0 - outlier_percentile]
    )
    lo, hi = (lo - outlier_multiplier * (hi - lo),
              hi + outlier_multiplier * (hi - lo))
    keep = v[(v >= lo) & (v <= hi)]
    stderr = (keep.std(ddof=1) / np.sqrt(len(keep))
              if len(keep) > 1 else np.inf)
    return float(keep.mean()), float(stderr), int(len(keep))


def generate_training_data(
    pde_factory: Callable[[], object],
    *,
    n_states: int = 1000,
    m_samples: int = 1000,
    seed: int = 0,
    rate: Optional[float] = None,
    code=None,
    t_range: tuple = (0.0, 0.0),
    x_lo: float = -1.0,
    x_hi: float = 1.0,
    overtrain_rate: float = 0.1,
    outlier_percentile: float = 1.0,
    outlier_multiplier: float = 1000.0,
    n_jobs: int = 1,
    executor: Optional[ProcessPoolExecutor] = None,
) -> TrainingData:
    """Draw N states and their M-sample MC targets (JCP2024 Alg. 2 input).

    rate=None uses the paper's jcp_rate(T) = -log(0.95)/T (Remark 3.1 v),
    NOT the package-wide default of 1: functional estimation touches the
    whole domain, where the paper-tuned sparse clock is the safer choice.

    ``code`` optionally roots every tree at a non-Id code (e.g. DxN(mu) to
    learn d^mu u instead of u) -- the authors' repo trains u only, but the
    generator supports per-root-code families for free.
    """
    pde = pde_factory()
    if rate is None:
        rate = jcp_rate(pde.T)
    d = getattr(pde, "d", 1)

    rng = np.random.default_rng(seed)
    t_lo, t_hi = t_range
    ts = rng.uniform(t_lo, t_hi, size=n_states) if t_hi > t_lo \
        else np.full(n_states, float(t_lo))
    margin = overtrain_rate * (x_hi - x_lo)
    x_mid = 0.5 * (x_lo + x_hi)
    xs = np.full((n_states, d), x_mid)
    xs[:, 0] = rng.uniform(x_lo - margin, x_hi + margin, size=n_states)

    seeds = np.random.SeedSequence(seed).spawn(n_states)
    jobs = [
        (pde_factory, float(ts[i]),
         xs[i] if d > 1 else np.array([xs[i, 0]]),
         m_samples, seeds[i], rate, code,
         outlier_percentile, outlier_multiplier)
        for i in range(n_states)
    ]

    start = time.perf_counter()
    if executor is not None:
        results = list(executor.map(_state_target, jobs))
    elif n_jobs > 1:
        with ProcessPoolExecutor(max_workers=n_jobs) as ex:
            results = list(ex.map(_state_target, jobs))
    else:
        results = [_state_target(j) for j in jobs]
    seconds = time.perf_counter() - start

    y = np.array([r[0] for r in results])
    stderr = np.array([r[1] for r in results])
    n_kept = np.array([r[2] for r in results])
    return TrainingData(
        t=ts, x=xs, y=y, stderr=stderr, n_kept=n_kept,
        m_samples=m_samples, rate=rate, seconds=seconds,
    )
