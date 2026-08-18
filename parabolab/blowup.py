"""Blow-up study machinery (M5): pointwise MC diagnostics vs horizon T.

The branching representation u(t,x) = E[H] is only valid on a short-time
integrability window (JEQ2023 Prop. 4.2).  Past that window E[|H|] (and
eventually E[H] itself) is infinite, but a finite-sample Monte Carlo mean
still returns *finite, innocent-looking numbers*: the divergence
manifests as a systematic drift of the estimate away from the true
solution, with a reported stderr that stops being an honest confidence
band.  ``sweep_T`` measures this by re-solving the same PDE for a grid
of horizons T and recording, per T:

* estimate, stderr (from :func:`parabolab.parallel.estimate_parallel`),
* abs error against the exact solution,
* seed spread (several independent seeds, to separate noise from drift),
* tail diagnostics: max |H| among the samples and mean tree size.

Reproduces the spirit of JCP2024 Fig. 2; cross-check data lives in
``coding_trees/logs/final/allen_cahn_jeeq_dim_*_blow_up_analysis.csv``.
"""

from __future__ import annotations

import math
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from typing import Callable, Optional, Sequence, Union

import numpy as np

from .parallel import estimate_parallel
from .tree import jcp_rate


@dataclass
class TSweep:
    """Result arrays of a horizon sweep; all shaped (n_T,) unless noted."""

    T: np.ndarray
    estimate: np.ndarray        # mean over seeds
    seed_spread: np.ndarray     # max - min over seeds (0 for one seed)
    stderr: np.ndarray          # mean reported MC stderr over seeds
    exact: np.ndarray
    max_abs: np.ndarray         # largest |H| seen at this T (any seed)
    mean_nodes: np.ndarray
    seconds: np.ndarray         # total sampling time at this T
    rate: np.ndarray            # resolved rho rate used at this T
    n_samples: int
    seeds: tuple

    @property
    def abs_err(self) -> np.ndarray:
        return np.abs(self.estimate - self.exact)

    def rows(self):
        """Iterate printable per-T rows (for tables and tests)."""
        for i in range(len(self.T)):
            yield {
                "T": float(self.T[i]),
                "estimate": float(self.estimate[i]),
                "stderr": float(self.stderr[i]),
                "exact": float(self.exact[i]),
                "abs_err": float(self.abs_err[i]),
                "seed_spread": float(self.seed_spread[i]),
                "max_abs": float(self.max_abs[i]),
                "mean_nodes": float(self.mean_nodes[i]),
            }


def sweep_T(
    make_pde: Callable[[float], object],
    Ts: Sequence[float],
    *,
    x: Optional[np.ndarray] = None,
    n_samples: int = 100_000,
    rate: Union[str, float, None] = "jcp",
    seeds: Sequence[int] = (0, 1, 2),
    n_jobs: int = 4,
    exact: Optional[Callable[[float], float]] = None,
    verbose: bool = True,
) -> TSweep:
    """Estimate u(0, x) for each horizon T in ``Ts``.

    ``make_pde(T)`` must return the PDE with terminal time T (e.g.
    ``functools.partial(allen_cahn_nd, d=1)``).  ``rate``:

    * ``"jcp"``  -- the authors' choice -log(0.95)/T (tiny trees,
      heavy leaf weights; used by their blow_up_analysis notebooks),
    * a float   -- fixed rho rate for every T,
    * ``None``  -- parabolab's default_rate (currently 1.0).

    ``exact(T)`` overrides the PDE's own exact_solution at (0, x) --
    needed when exact_solution is missing.  One long-lived executor is
    shared across all (T, seed) estimates so worker PDE caches survive.
    """
    import functools

    Ts = np.asarray(list(Ts), dtype=float)
    pde0 = make_pde(float(Ts[0]))
    d = getattr(pde0, "d", 1)
    if x is None:
        # FullyNonlinearPDEnD expects an array even at d = 1
        x = np.zeros(d)

    est = np.empty(len(Ts))
    spread = np.empty(len(Ts))
    serr = np.empty(len(Ts))
    exa = np.empty(len(Ts))
    mabs = np.empty(len(Ts))
    mnodes = np.empty(len(Ts))
    secs = np.empty(len(Ts))
    rates = np.empty(len(Ts))

    executor = ProcessPoolExecutor(max_workers=n_jobs) if n_jobs > 1 \
        else None
    try:
        for i, T in enumerate(Ts):
            T = float(T)
            factory = functools.partial(make_pde, T)
            r = jcp_rate(T) if rate == "jcp" else rate
            per_seed = [
                estimate_parallel(
                    factory, 0.0, x, n_samples, seed=s, rate=r,
                    n_jobs=n_jobs, executor=executor,
                )
                for s in seeds
            ]
            vals = [p.estimate for p in per_seed]
            est[i] = float(np.mean(vals))
            spread[i] = float(np.max(vals) - np.min(vals))
            serr[i] = float(np.mean([p.stderr for p in per_seed]))
            mabs[i] = float(np.max([p.max_abs for p in per_seed]))
            mnodes[i] = float(np.mean([p.mean_nodes for p in per_seed]))
            secs[i] = float(np.sum([p.seconds for p in per_seed]))
            rates[i] = per_seed[0].rate
            if exact is not None:
                exa[i] = exact(T)
            else:
                exa[i] = make_pde(T).exact_solution(0.0, x)
            if verbose:
                print(
                    f"  T={T:.2f}  u^={est[i]:+.4f} +/- {serr[i]:.4f}  "
                    f"exact={exa[i]:+.4f}  |err|={abs(est[i]-exa[i]):.2e} "
                    f" spread={spread[i]:.2e}  max|H|={mabs[i]:.2e}  "
                    f"({secs[i]:.0f}s)", flush=True,
                )
    finally:
        if executor is not None:
            executor.shutdown()

    return TSweep(
        T=Ts, estimate=est, seed_spread=spread, stderr=serr, exact=exa,
        max_abs=mabs, mean_nodes=mnodes, seconds=secs, rate=rates,
        n_samples=n_samples, seeds=tuple(seeds),
    )


def integrability_edge(
    sweep: TSweep, *, k: float = 3.0, rel_tol: float = 0.05,
) -> Optional[float]:
    """First T from which the estimator PERSISTENTLY fails either test:

    * drift: |err| > k * max(stderr, seed_spread) -- the estimate is
      systematically off by more than its own uncertainty claims;
    * precision loss: stderr > rel_tol * |exact| -- the variance has
      grown so much that the fixed sample budget no longer resolves the
      solution (heavy tails; the practical end of the window even when
      the huge error bars still formally cover the truth).

    A one-off excursion is noise; only a condition that holds for ALL
    later T counts.  Returns None if neither criterion locks in.
    """
    drift = sweep.abs_err > k * np.maximum(sweep.stderr, sweep.seed_spread)
    imprecise = sweep.stderr > rel_tol * np.abs(sweep.exact)
    bad = drift | imprecise
    for i in range(len(bad)):
        if bad[i:].all():
            return float(sweep.T[i])
    return None
