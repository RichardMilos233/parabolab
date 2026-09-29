"""Bounded ternary branching Monte Carlo for scalar Allen--Cahn PDEs.

The sampler constructs the complete continuous-time ternary tree.  At a
branch all children share the parent's Brownian death position, then evolve
independently.  Leaves return ``phi(X_T)`` and branches use the bounded rule

    B_r = (2/r) B_2 + (1 - 2/r) (a+b+c)/3,
    B_2 = (a+b+c-abc)/2.

There are no likelihood weights, depth or node cutoffs, clipping, or rejected
roots.  Root batches bound ordinary working memory without changing a tree.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Optional

import numpy as np

from .solve import Curve, Solver, _points

__all__ = [
    "AllenCahnMajorityMC",
    "MajoritySamples",
    "majority_branch",
    "sample_majority",
]


def _validate_rate(rate: float) -> float:
    rate = float(rate)
    if not math.isfinite(rate) or rate < 2.0:
        raise ValueError("rate must be finite and >= 2")
    return rate


def _validate_count(value: int, name: str) -> int:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise TypeError(f"{name} must be an integer")
    value = int(value)
    if value < 1:
        raise ValueError(f"{name} must be >= 1")
    return value


def _validate_pde(pde) -> None:
    if getattr(pde, "reaction_kind", None) != "allen_cahn":
        raise ValueError(
            "AllenCahnMajorityMC requires reaction_kind='allen_cahn'; "
            "arbitrary reaction callbacks are not inferred by sampling"
        )
    if getattr(pde, "d", None) != 1:
        raise NotImplementedError("AllenCahnMajorityMC supports only d = 1")
    try:
        horizon = float(pde.T)
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError("PDE terminal time T must be finite and positive") from exc
    if not math.isfinite(horizon) or horizon <= 0.0:
        raise ValueError("PDE terminal time T must be finite and positive")


def majority_branch(a, b, c, rate: float = 2.0):
    """Apply the bounded ternary branch rule, elementwise for arrays."""
    rate = _validate_rate(rate)
    mean = (a + b + c) / 3.0
    b2 = (a + b + c - a * b * c) / 2.0
    return (2.0 / rate) * b2 + (1.0 - 2.0 / rate) * mean


@dataclass(frozen=True)
class MajoritySamples:
    """Complete per-root output and cost records from the bounded sampler."""

    values: np.ndarray
    node_counts: np.ndarray
    root_branched: np.ndarray
    rate: float
    seconds: float

    @property
    def estimate(self) -> float:
        return float(self.values.mean())

    @property
    def sample_variance(self) -> float:
        if self.values.size < 2:
            return float("nan")
        return float(self.values.var(ddof=1))

    @property
    def stderr(self) -> float:
        return math.sqrt(self.sample_variance / self.values.size)

    @property
    def mean_nodes(self) -> float:
        return float(self.node_counts.mean())

    @property
    def max_nodes(self) -> int:
        return int(self.node_counts.max())


def _terminal_values(phi, positions: np.ndarray) -> np.ndarray:
    values = np.fromiter(
        (float(phi(float(x))) for x in positions),
        dtype=float,
        count=positions.size,
    )
    if not np.all(np.isfinite(values)):
        raise ValueError("terminal phi must return finite values in [-1, 1]")
    if np.any(values < -1.0) or np.any(values > 1.0):
        raise ValueError("terminal phi must return values in [-1, 1]")
    return values


def _sample_batch(pde, t: float, x: float, n_roots: int, rate: float, rng):
    times = np.full(n_roots, t, dtype=float)
    positions = np.full(n_roots, x, dtype=float)
    root_ids = np.arange(n_roots, dtype=np.int64)
    node_counts = np.zeros(n_roots, dtype=np.int64)
    root_branched = None
    generations = []

    while True:
        node_counts += np.bincount(root_ids, minlength=n_roots)
        remaining = pde.T - times
        lifetimes = np.asarray(
            rng.exponential(scale=1.0 / rate, size=times.size), dtype=float
        )
        if lifetimes.shape != times.shape:
            raise ValueError("rng.exponential returned an unexpected shape")
        branched = lifetimes < remaining
        if root_branched is None:
            root_branched = branched.copy()

        durations = np.where(branched, lifetimes, remaining)
        normals = np.asarray(rng.normal(size=times.size), dtype=float)
        if normals.shape != times.shape:
            raise ValueError("rng.normal returned an unexpected shape")
        death_positions = positions + np.sqrt(durations) * normals

        values = np.empty(times.size, dtype=float)
        leaf = ~branched
        values[leaf] = _terminal_values(pde.phi, death_positions[leaf])
        generations.append((branched, values))
        if not np.any(branched):
            break

        # One death position per parent is repeated for its three children.
        # Their independent clocks and Brownian draws occur next iteration.
        child_times = times[branched] + lifetimes[branched]
        times = np.repeat(child_times, 3)
        positions = np.repeat(death_positions[branched], 3)
        root_ids = np.repeat(root_ids[branched], 3)

    child_values = None
    for branched, values in reversed(generations):
        if child_values is not None:
            triples = child_values.reshape(-1, 3)
            values[branched] = majority_branch(
                triples[:, 0], triples[:, 1], triples[:, 2], rate
            )
        child_values = values

    return child_values, node_counts, root_branched


def sample_majority(
    pde,
    t: float,
    x: float,
    n_samples: int,
    *,
    rate: float = 2.0,
    seed: Optional[int] = None,
    rng=None,
    batch_size: int = 32,
) -> MajoritySamples:
    """Sample complete bounded ternary trees for ``u(t, x)``.

    ``batch_size`` controls only how many independent roots are held in
    memory together.  Every started root is completed and retained.
    """
    _validate_pde(pde)
    rate = _validate_rate(rate)
    n_samples = _validate_count(n_samples, "n_samples")
    batch_size = _validate_count(batch_size, "batch_size")
    t, x = float(t), float(x)
    if not math.isfinite(t) or t < 0.0 or t > pde.T:
        raise ValueError("t must be finite and satisfy 0 <= t <= T")
    if not math.isfinite(x):
        raise ValueError("x must be finite")
    if rng is not None and seed is not None:
        raise ValueError("pass either rng or seed, not both")
    if rng is None:
        rng = np.random.default_rng(seed)

    values = np.empty(n_samples, dtype=float)
    node_counts = np.empty(n_samples, dtype=np.int64)
    root_branched = np.empty(n_samples, dtype=bool)
    start = time.perf_counter()
    for lo in range(0, n_samples, batch_size):
        hi = min(lo + batch_size, n_samples)
        batch = _sample_batch(pde, t, x, hi - lo, rate, rng)
        values[lo:hi], node_counts[lo:hi], root_branched[lo:hi] = batch
    seconds = time.perf_counter() - start
    return MajoritySamples(values, node_counts, root_branched, rate, seconds)


class AllenCahnMajorityMC(Solver):
    """Pointwise bounded ternary Monte Carlo for tagged scalar Allen--Cahn.

    The ``reaction_kind='allen_cahn'`` marker is a trusted declaration that
    the callback is exactly ``u - u**3``; the solver never infers this from
    sampled callback values.  The caller likewise declares that ``phi`` is
    globally valued in ``[-1, 1]``.  Sampled leaf values are checked, but
    finite sampling cannot establish that global terminal-data contract.
    """

    label = "bounded majority MC"

    def __init__(
        self,
        n_samples: int = 10_000,
        seed: int = 0,
        rate: float = 2.0,
        batch_size: int = 32,
        label: Optional[str] = None,
    ):
        self.n_samples = _validate_count(n_samples, "n_samples")
        self.batch_size = _validate_count(batch_size, "batch_size")
        self.rate = _validate_rate(rate)
        self.seed = seed
        if label is not None:
            self.label = label

    def solve(self, pde, grid, t: float = 0.0, embed=None) -> Curve:
        instance, _ = self._resolve(pde)
        _validate_pde(instance)
        grid = np.asarray(grid, dtype=float)
        if grid.ndim != 1 or grid.size == 0 or not np.all(np.isfinite(grid)):
            raise ValueError("grid must be a nonempty finite one-dimensional array")
        points = _points(instance, grid, embed)
        values = np.empty(grid.size, dtype=float)
        stderrs = np.empty(grid.size, dtype=float)
        total_nodes = 0
        max_nodes = 0
        start = time.perf_counter()
        for i, point in enumerate(points):
            result = sample_majority(
                instance,
                t,
                point,
                self.n_samples,
                rate=self.rate,
                seed=self.seed + i,
                batch_size=self.batch_size,
            )
            values[i] = result.estimate
            stderrs[i] = result.stderr
            total_nodes += int(result.node_counts.sum())
            max_nodes = max(max_nodes, result.max_nodes)
        seconds = time.perf_counter() - start
        return Curve(
            label=self.label,
            grid=grid,
            values=values,
            seconds=seconds,
            stderr=stderrs,
            note=(
                f"{self.n_samples} samples/point, rate={self.rate:g}, "
                f"tree nodes mean={total_nodes / (self.n_samples * grid.size):.2f} "
                f"max={max_nodes}"
            ),
            t=t,
            points=points,
            embedding=embed,
        )
