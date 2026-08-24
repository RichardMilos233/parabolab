"""Estimate u(t, .) on an x-grid, with the closed form for comparison.

The estimation machinery only.  Tables and figures live in
``parabolab.solve`` (``compare(...).table().plot(...)``), which wraps this
module and is what the examples and demos use.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional, Sequence

import numpy as np

from .mc import estimate


@dataclass
class ProfileResult:
    t: float
    xs: np.ndarray
    estimates: np.ndarray
    stderrs: np.ndarray
    exacts: Optional[np.ndarray]
    n_samples: int
    seconds: float
    mean_nodes: float
    max_nodes: int

    @property
    def max_abs_z(self) -> float:
        """max |estimate - exact| / stderr over the grid."""
        return float(np.max(np.abs(self.estimates - self.exacts) / self.stderrs))


def last_coordinate_embedding(d: int):
    """The authors' profile convention: grid point s -> (0, ..., 0, s)."""
    def embed(s: float) -> np.ndarray:
        x = np.zeros(d)
        x[-1] = s
        return x

    return embed


def estimate_profile(
    pde,
    t: float,
    xs: Sequence[float],
    n_samples: int,
    *,
    seed: int = 0,
    rate: Optional[float] = None,
    embed=None,
    pde_factory=None,
    n_jobs: int = 1,
) -> ProfileResult:
    """Pointwise coding-tree estimates of u(t, x) for x in xs.

    For d-dim problems pass ``embed`` mapping a scalar grid point to the
    point in R^d (e.g. last_coordinate_embedding(d), the convention of the
    authors' notebook plots).  With ``pde_factory``/``n_jobs`` > 1 the
    samples are computed by estimate_parallel over worker processes.
    """
    xs = np.asarray(xs, dtype=float)
    est = np.empty_like(xs)
    err = np.empty_like(xs)
    total_nodes = 0.0
    max_nodes = 0
    executor = None
    if n_jobs > 1:
        from concurrent.futures import ProcessPoolExecutor

        # one long-lived pool for all grid points, so the per-worker PDE
        # caches (mechanism tables, lambdified derivatives) stay warm
        executor = ProcessPoolExecutor(max_workers=n_jobs)
    start = time.perf_counter()
    try:
        for i, x in enumerate(xs):
            xpt = embed(float(x)) if embed is not None else float(x)
            if n_jobs > 1:
                from .parallel import estimate_parallel

                r = estimate_parallel(pde_factory, t, xpt, n_samples,
                                      seed=seed + i, rate=rate,
                                      n_jobs=n_jobs, executor=executor)
            else:
                r = estimate(pde, t, xpt, n_samples, seed=seed + i,
                             rate=rate)
            est[i], err[i] = r.estimate, r.stderr
            total_nodes += r.mean_nodes * r.n_samples
            max_nodes = max(max_nodes, r.max_nodes)
    finally:
        if executor is not None:
            executor.shutdown()
    seconds = time.perf_counter() - start
    exacts = None
    if pde.exact_solution is not None:
        exacts = np.array([
            pde.exact_solution(t, embed(float(x)) if embed is not None
                               else float(x))
            for x in xs
        ])
    return ProfileResult(
        t=t, xs=xs, estimates=est, stderrs=err, exacts=exacts,
        n_samples=n_samples, seconds=seconds,
        mean_nodes=total_nodes / (n_samples * len(xs)), max_nodes=max_nodes,
    )
