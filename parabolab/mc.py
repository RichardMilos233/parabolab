"""Pointwise Monte Carlo estimation of u(t, x) = E[H(T_{t,x,Id})]."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Optional

import numpy as np

from .mechanism import Code, Id, SemilinearMechanism
from .pde import ParabolicPDE
from .tree import sample_tree


@dataclass
class MCResult:
    """Monte Carlo estimate of code(u)(t, x) with diagnostics."""

    estimate: float
    stderr: float
    n_samples: int
    rate: float
    mean_nodes: float
    max_nodes: int
    seconds: float
    # tail diagnostic: largest |H| among the samples.  When max_abs/n
    # rivals stderr, the empirical mean is dominated by single trees and
    # the integrability window is closing (M5 blow-up study).
    max_abs: float = float("nan")

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        return (
            f"{self.estimate:+.6f} +/- {self.stderr:.6f} "
            f"(N={self.n_samples}, rate={self.rate:.4g}, "
            f"nodes mean={self.mean_nodes:.2f} max={self.max_nodes}, "
            f"{self.seconds:.1f}s)"
        )


def estimate(
    pde: ParabolicPDE,
    t: float,
    x: float,
    n_samples: int,
    *,
    rng: Optional[np.random.Generator] = None,
    seed: Optional[int] = None,
    rate: Optional[float] = None,
    code: Code = Id(),
    mechanism=None,
    prune_zero: bool = True,
) -> MCResult:
    """Estimate code(u)(t, x) by averaging n_samples coding-tree samples.

    Pass either ``rng`` (a numpy Generator) or ``seed``; ``seed`` creates a
    fresh ``np.random.default_rng(seed)`` so runs are reproducible.
    ``mechanism=None`` picks the PDE's own mechanism if it has one.
    """
    if mechanism is None:
        mechanism = getattr(pde, "mechanism", None) or SemilinearMechanism
    if rng is None:
        rng = np.random.default_rng(seed)
    if rate is None:
        from .tree import default_rate

        rate = default_rate(pde.T)

    values = np.empty(n_samples)
    total_nodes = 0
    max_nodes = 0
    start = time.perf_counter()
    for i in range(n_samples):
        s = sample_tree(
            pde, t, x, rng=rng, rate=rate, code=code,
            mechanism=mechanism, prune_zero=prune_zero,
        )
        values[i] = s.value
        total_nodes += s.n_nodes
        max_nodes = max(max_nodes, s.n_nodes)
    seconds = time.perf_counter() - start

    mean = float(values.mean())
    stderr = float(values.std(ddof=1) / math.sqrt(n_samples))
    return MCResult(
        estimate=mean,
        stderr=stderr,
        n_samples=n_samples,
        rate=rate,
        mean_nodes=total_nodes / n_samples,
        max_nodes=max_nodes,
        seconds=seconds,
        max_abs=float(np.abs(values).max()),
    )
