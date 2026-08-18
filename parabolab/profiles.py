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


def estimate_profile(
    pde,
    t: float,
    xs: Sequence[float],
    n_samples: int,
    *,
    seed: int = 0,
    rate: Optional[float] = None,
) -> ProfileResult:
    """Pointwise coding-tree estimates of u(t, x) for x in xs."""
    xs = np.asarray(xs, dtype=float)
    est = np.empty_like(xs)
    err = np.empty_like(xs)
    total_nodes = 0.0
    max_nodes = 0
    start = time.perf_counter()
    for i, x in enumerate(xs):
        r = estimate(pde, t, float(x), n_samples, seed=seed + i, rate=rate)
        est[i], err[i] = r.estimate, r.stderr
        total_nodes += r.mean_nodes * r.n_samples
        max_nodes = max(max_nodes, r.max_nodes)
    seconds = time.perf_counter() - start
    exacts = None
    if pde.exact_solution is not None:
        exacts = np.array([pde.exact_solution(t, float(x)) for x in xs])
    return ProfileResult(
        t=t, xs=xs, estimates=est, stderrs=err, exacts=exacts,
        n_samples=n_samples, seconds=seconds,
        mean_nodes=total_nodes / (n_samples * len(xs)), max_nodes=max_nodes,
    )


def plot_profile(result: ProfileResult, pde, out_path, title: str) -> None:
    """Save a Fig-6-style plot: MC points with 3-stderr bars vs closed form."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 4.5))
    x_fine = np.linspace(result.xs[0], result.xs[-1], 300)
    if pde.exact_solution is not None:
        ax.plot(x_fine, [pde.exact_solution(result.t, v) for v in x_fine],
                "k-", label="exact")
    ax.plot(x_fine, [pde.exact_solution(pde.T, v) for v in x_fine],
            "k--", alpha=0.6, label=r"terminal $\phi$")
    ax.errorbar(result.xs, result.estimates, yerr=3 * result.stderrs,
                fmt="o", mfc="none", color="tab:blue", capsize=3,
                label=rf"MC ($N={result.n_samples}$, $\pm 3$ stderr)")
    ax.set_xlabel("$x$")
    ax.set_ylabel(f"$u({result.t}, x)$")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
