"""Estimate u(t, .) on an x-grid and compare/plot against a closed form.

Shared by the examples/jeq_fig*.py scripts that reproduce JEQ2023 Figs 1
and 6-9.
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

    def print_table(self) -> None:
        header = f"{'x':>8} {'estimate':>13} {'stderr':>10}"
        if self.exacts is not None:
            header += f" {'exact':>13} {'|err|/stderr':>12}"
        print(header)
        for i, x in enumerate(self.xs):
            line = f"{x:8.3f} {self.estimates[i]:13.6f} {self.stderrs[i]:10.6f}"
            if self.exacts is not None:
                z = abs(self.estimates[i] - self.exacts[i]) / self.stderrs[i]
                line += f" {self.exacts[i]:13.6f} {z:12.2f}"
            print(line)
        print(f"# {self.n_samples} samples/point, {self.seconds:.1f}s total, "
              f"tree nodes mean={self.mean_nodes:.2f} max={self.max_nodes}"
              + (f", max |err|/stderr = {self.max_abs_z:.2f}"
                 if self.exacts is not None else ""))


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


def plot_profile(result: ProfileResult, pde, out_path, title: str,
                 embed=None, reference=None) -> None:
    """Save a Fig-6-style plot: MC points with 3-stderr bars vs closed form.

    ``embed`` as in estimate_profile; ``reference`` optionally overlays
    third-party values as (xs, values, label) (e.g. the authors' CSV).
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    def ex(t, v):
        return pde.exact_solution(t, embed(v) if embed is not None else v)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    x_fine = np.linspace(result.xs[0], result.xs[-1], 300)
    if pde.exact_solution is not None:
        ax.plot(x_fine, [ex(result.t, v) for v in x_fine],
                "k-", label="exact")
        ax.plot(x_fine, [ex(pde.T, v) for v in x_fine],
                "k--", alpha=0.6, label=r"terminal $\phi$")
    ax.errorbar(result.xs, result.estimates, yerr=3 * result.stderrs,
                fmt="o", mfc="none", color="tab:blue", capsize=3,
                label=rf"MC ($N={result.n_samples}$, $\pm 3$ stderr)")
    if reference is not None:
        rx, rv, rlabel = reference
        ax.plot(rx, rv, "x", color="tab:red", label=rlabel)
    ax.set_xlabel("$x$")
    ax.set_ylabel(f"$u({result.t}, x)$")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
