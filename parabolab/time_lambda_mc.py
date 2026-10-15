"""Empirical full-tree Monte Carlo variance grids for T-lambda plots.

Every completed cell contains ordinary ``sample_tree`` realizations at that
cell's PDE horizon and branching rate. Sampling is sequential unless
``n_jobs > 1``, which distributes cells (or fixed-size sample chunks of a
cell) over worker processes. By default there is no per-tree or per-cell
total-work limit; callers may opt into those guards explicitly. Invalid cells are retained as status data rather than
filtered or replaced. A finite batch cannot establish that the population
second moment is finite or infinite.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
import json
import math
from pathlib import Path
import time
from typing import Callable, Optional, Sequence, Union

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, SymLogNorm
import numpy as np

from .flat_batch import flat_semilinear_leaf_values, sample_flat_batch
from .time_lambda import _boundary, flat_exact_variance, sweep_time_lambda
from .tree import TreeNodeLimitExceeded, sample_tree


_PENDING = "pending"
_COMPLETE = "complete"
_NODE_LIMIT = "node_limit"
_CELL_BUDGET = "cell_budget"
_NONFINITE = "nonfinite"
_ERROR = "error"
_INTERRUPTED = "interrupted"
_CANCELLED = object()
_SAMPLERS = ("tree", "flat")
_DIAGNOSTICS = ("n_nonzero", "max_share", "batch_variance")
_CONTOUR_LEVELS = (0.1, 1.0, 10.0, 100.0)
_FLAT_DEFAULT_CHUNK = 100_000
_STATISTICS = {
    "variance": ("Observed full-tree MC sample variance with theoretical boundary",
                 "Sample variance (symlog, ddof=1)",
                 "Thin lines: sample variance equals the labelled value. Ordered below T₂, "
                 "broken up above it. An all-zero batch shows 0, which is not stability."),
    "max_share": ("Largest sample's share of the sum of squares, max H² / ΣH²",
                  "max H² / ΣH²  (→ 0 iff E[H²] < ∞)",
                  "Dark ≈ 0: many samples contribute (finite second moment expected below T₂). "
                  "Bright ≈ 1: one sample is the variance."),
    "batch_cv": ("Spread of sub-batch sample variances",
                 "CV of batch variances (std / mean)",
                 "0: ten repeated variance estimates agree; 3: all variance in one batch. "
                 "Driven by the fourth moment, so it may light up below T₂."),
}


def _cell_rng(seed: int, t_index: int, lambda_index: int) -> np.random.Generator:
    return np.random.default_rng(np.random.SeedSequence([seed, t_index, lambda_index]))


def _chunk_rng(seed: int, t_index: int, lambda_index: int, chunk: int,
               n_chunks: int) -> np.random.Generator:
    # A single chunk reuses the serial cell stream, so results match n_jobs=1.
    if n_chunks == 1:
        return _cell_rng(seed, t_index, lambda_index)
    return np.random.default_rng(
        np.random.SeedSequence([seed, t_index, lambda_index, chunk]))


_WORKER_FACTORY: Optional[Callable[[float], object]] = None
_WORKER_PDES: dict = {}


def _worker_init(factory: Callable[[float], object]) -> None:
    global _WORKER_FACTORY
    _WORKER_FACTORY = factory
    _WORKER_PDES.clear()


def _worker_pde(horizon: float):
    pde = _WORKER_PDES.get(horizon)
    if pde is None:
        pde = _WORKER_FACTORY(horizon)
        _WORKER_PDES[horizon] = pde
    return pde


def _run_chunk(ti: int, li: int, chunk: int, n_chunks: int, n: int,
               horizon: float, rate: float, seed: int,
               max_nodes: Optional[int], flat: Optional[tuple] = None) -> tuple:
    """Sample ``n`` trees of one cell chunk; stop at the first failure.

    Returns ``(ti, li, chunk, values, nodes, status, reason)`` where
    ``values`` holds the completed samples and ``status`` is ``None`` when
    every requested tree completed with a finite value. ``flat`` is
    ``(leaf_values, flat_terminal)`` for the vectorized flat sampler.
    """
    rng = _chunk_rng(seed, ti, li, chunk, n_chunks)
    if flat is not None:
        return _run_flat_chunk(ti, li, chunk, n, horizon, rate, rng, max_nodes, flat)
    pde = _worker_pde(horizon)
    values = np.empty(n)
    nodes = 0
    for si in range(n):
        try:
            sample = sample_tree(pde, 0.0, 0.0, rng=rng, rate=rate,
                                 max_nodes=max_nodes)
        except TreeNodeLimitExceeded as exc:
            return ti, li, chunk, values[:si], nodes + exc.n_nodes, _NODE_LIMIT, str(exc)
        except (FloatingPointError, OverflowError, RecursionError) as exc:
            return (ti, li, chunk, values[:si], nodes, _ERROR,
                    f"{type(exc).__name__}: {exc}")
        nodes += sample.n_nodes
        if not math.isfinite(sample.value):
            return (ti, li, chunk, values[:si + 1], nodes, _NONFINITE,
                    "sample_tree returned a non-finite value")
        values[si] = sample.value
    return ti, li, chunk, values, nodes, None, ""


def _run_flat_chunk(ti, li, chunk, n, horizon, rate, rng, max_nodes, flat) -> tuple:
    leaf_values, flat_terminal = flat
    try:
        values, nodes, exceeded = sample_flat_batch(
            np.asarray(leaf_values), flat_terminal, horizon, rate, n, rng,
            max_nodes=max_nodes,
        )
    except MemoryError as exc:
        return ti, li, chunk, np.empty(0), 0, _ERROR, f"MemoryError: {exc}"
    bad = exceeded | ~np.isfinite(values)
    if not bad.any():
        return ti, li, chunk, values, int(nodes.sum()), None, ""
    # Report the first failing tree in sample order, as the serial loop would.
    i = int(np.argmax(bad))
    used = int(nodes[:i + 1].sum())
    if exceeded[i]:
        return (ti, li, chunk, values[:i], used, _NODE_LIMIT,
                f"a tree exceeded max_nodes={max_nodes} visited nodes (flat sampler)")
    return (ti, li, chunk, values[:i + 1], used, _NONFINITE,
            "flat sampler returned a non-finite value")


def _nan_box_mean(values: np.ndarray) -> np.ndarray:
    """3x3 mean that ignores NaN entries (used only to draw contours)."""
    finite = np.isfinite(values)
    padded = np.pad(np.where(finite, values, 0.0), 1)
    weight = np.pad(finite.astype(float), 1)
    rows, cols = values.shape
    total = sum(padded[i:i + rows, j:j + cols] for i in range(3) for j in range(3))
    count = sum(weight[i:i + rows, j:j + cols] for i in range(3) for j in range(3))
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(count > 0, total / count, np.nan)


def _grid_edges(points: np.ndarray) -> np.ndarray:
    if len(points) == 1:
        width = max(abs(float(points[0])) * 0.05, 0.05)
        return np.array([points[0] - width, points[0] + width])
    mid = (points[:-1] + points[1:]) / 2.0
    return np.concatenate(([points[0] - (mid[0] - points[0])], mid,
                           [points[-1] + (points[-1] - mid[-1])]))


@dataclass
class TimeLambdaMCSweep:
    """Observed sample statistics and cell statuses for one PDE family."""

    title: str
    flat_terminal: float
    K: float
    lambdas: np.ndarray
    horizons: np.ndarray
    variance: np.ndarray
    mean: np.ndarray
    second_moment: np.ndarray
    completed_samples: np.ndarray
    total_nodes: np.ndarray
    status: np.ndarray
    reason: np.ndarray
    seed: int
    n_samples: int
    max_nodes: Optional[int]
    max_cell_nodes: Optional[int]
    reference_T: float
    theory_points: int
    chunk_size: Optional[int] = None
    sampler: str = "tree"
    n_nonzero: Optional[np.ndarray] = None
    max_share: Optional[np.ndarray] = None
    batch_variance: Optional[np.ndarray] = None

    @property
    def batch_cv(self) -> Optional[np.ndarray]:
        """Coefficient of variation of the per-batch sample variances."""
        if self.batch_variance is None:
            return None
        with np.errstate(invalid="ignore", divide="ignore"):
            mean = np.mean(self.batch_variance, axis=2)
            return np.where(mean > 0.0, np.std(self.batch_variance, axis=2) / mean, np.nan)

    def statistic(self, name: str) -> np.ndarray:
        if name not in _STATISTICS:
            raise ValueError(f"statistic must be one of {sorted(_STATISTICS)}")
        values = self.variance if name == "variance" else getattr(self, name)
        if values is None:
            raise ValueError(f"this sweep has no {name!r} data (recorded before diagnostics)")
        return values

    def save(self, path: Union[str, Path]) -> "TimeLambdaMCSweep":
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        metadata = json.dumps({
            "version": 1,
            "title": self.title,
            "flat_terminal": self.flat_terminal,
            "K": self.K,
            "seed": self.seed,
            "n_samples": self.n_samples,
            "max_nodes": self.max_nodes,
            "max_cell_nodes": self.max_cell_nodes,
            "reference_T": self.reference_T,
            "theory_points": self.theory_points,
            "chunk_size": self.chunk_size,
            "sampler": self.sampler,
            "kind": "sweep",
        }, sort_keys=True)
        extra = {name: getattr(self, name) for name in _DIAGNOSTICS
                 if getattr(self, name) is not None}
        np.savez_compressed(
            out, metadata=np.asarray(metadata), lambdas=self.lambdas,
            horizons=self.horizons, variance=self.variance, mean=self.mean,
            second_moment=self.second_moment,
            completed_samples=self.completed_samples, total_nodes=self.total_nodes,
            status=self.status, reason=self.reason, **extra,
        )
        return self

    @classmethod
    def load(cls, path: Union[str, Path]) -> "TimeLambdaMCSweep":
        with np.load(path, allow_pickle=False) as data:
            meta = json.loads(str(data["metadata"].item()))
            return cls(
                title=meta["title"], flat_terminal=float(meta["flat_terminal"]),
                K=float(meta["K"]), lambdas=data["lambdas"].copy(),
                horizons=data["horizons"].copy(), variance=data["variance"].copy(),
                mean=data["mean"].copy(), second_moment=data["second_moment"].copy(),
                completed_samples=data["completed_samples"].copy(),
                total_nodes=data["total_nodes"].copy(), status=data["status"].copy(),
                reason=data["reason"].copy(), seed=int(meta["seed"]),
                n_samples=int(meta["n_samples"]), max_nodes=meta["max_nodes"],
                max_cell_nodes=meta["max_cell_nodes"],
                reference_T=float(meta["reference_T"]),
                theory_points=int(meta.get("theory_points", 401)),
                chunk_size=meta.get("chunk_size"),
                sampler=meta.get("sampler", "tree"),
                **{name: data[name].copy() if name in data.files else None
                   for name in _DIAGNOSTICS},
            )

    def _plot_on(self, ax: plt.Axes, norm, statistic: str = "variance",
                 contour_levels: Sequence[float] = _CONTOUR_LEVELS):
        data = self.statistic(statistic)
        valid = (self.status == _COMPLETE) & np.isfinite(data)
        values = np.ma.array(data, mask=~valid)
        cmap = plt.get_cmap("viridis").with_extremes(bad="#B8BEC7")
        mesh = ax.pcolormesh(
            _grid_edges(self.lambdas), _grid_edges(self.horizons), values,
            shading="flat", cmap=cmap, norm=norm,
        )
        theory_lambda = np.linspace(
            self.lambdas[0], self.lambdas[-1], self.theory_points,
        )
        if math.isfinite(self.K):
            ax.plot(theory_lambda, _boundary(theory_lambda, self.K), color="white",
                    linewidth=2.8, label=r"theory $T_2(\lambda)$")
            ax.plot(theory_lambda, _boundary(theory_lambda, self.K), color="#172033",
                    linewidth=1.2)
        if statistic == "variance" and contour_levels:
            # Iso-variance lines of the 3x3-averaged log10 sample variance,
            # each labelled with its level.
            with np.errstate(divide="ignore", invalid="ignore"):
                logs = np.where(valid & (data > 0), np.log10(data), np.nan)
            if np.count_nonzero(np.isfinite(logs)) > 4:
                cs = ax.contour(self.lambdas, self.horizons, _nan_box_mean(logs),
                                levels=np.log10(sorted(contour_levels)),
                                colors="#f4f4f4", linewidths=0.9, linestyles="-")
                for text in ax.clabel(cs, fmt=lambda v: f"{10 ** v:g}", fontsize=8):
                    text.set_color("#f4f4f4")
        ax.set_xlim(self.lambdas[0], self.lambdas[-1])
        ax.set_ylim(self.horizons[0], self.horizons[-1])
        ax.set_title(
            f"{self.title}\n{len(self.horizons)}×{len(self.lambdas)} cells, "
            f"n={self.n_samples:,}/cell\n"
            + ("flat-data sampler (special case)" if self.sampler == "flat"
               else "general sample_tree"),
            fontweight="bold", fontsize=10,
        )
        ax.set_xlabel(r"branching rate $\lambda$")
        ax.set_ylabel(r"horizon $T$")
        invalid = int(np.size(valid) - np.count_nonzero(valid))
        if invalid:
            what = ("invalid/uncompleted" if statistic == "variance"
                    else "invalid or all-zero")
            ax.text(0.02, 0.02, f"{invalid} {what} cells (grey)",
                    transform=ax.transAxes, fontsize=7.5,
                    bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none"})
        ax.legend(loc="upper right", fontsize=7.5)
        return mesh


class TimeLambdaMCComparison:
    """Several empirical grids sharing one variance color scale."""

    def __init__(self, sweeps: Sequence[TimeLambdaMCSweep]):
        self.sweeps = list(sweeps)

    def _norm(self, statistic: str = "variance"):
        if statistic == "max_share":
            return Normalize(vmin=0.0, vmax=1.0)
        if statistic == "batch_cv":
            batches = max(s.batch_variance.shape[2] for s in self.sweeps
                          if s.batch_variance is not None)
            return Normalize(vmin=0.0, vmax=math.sqrt(batches - 1))
        finite = [
            sweep.variance[(sweep.status == _COMPLETE) & np.isfinite(sweep.variance)]
            for sweep in self.sweeps
        ]
        values = np.concatenate([v for v in finite if v.size]) if any(v.size for v in finite) else np.array([0.0])
        positive = values[values > 0.0]
        linthresh = (
            max(float(np.min(positive) / 10.0), np.finfo(float).tiny)
            if positive.size else 1.0
        )
        vmax = max(float(np.max(values)), linthresh)
        return SymLogNorm(linthresh=linthresh, vmin=0.0, vmax=vmax, base=10)

    def plot(
        self,
        path: Optional[Union[str, Path]] = None,
        *,
        save_individual: bool = False,
        figsize: Optional[tuple[float, float]] = None,
        statistic: str = "variance",
        contour_levels: Sequence[float] = _CONTOUR_LEVELS,
    ) -> "TimeLambdaMCComparison":
        """Plot one statistic: ``variance``, ``max_share`` or ``batch_cv``.

        The variance plot overlays thin iso-variance lines at
        ``contour_levels``, each labelled with its value (drawn from a 3x3
        mean of log10 variance); ``contour_levels=()`` disables them.
        """
        if not self.sweeps:
            raise ValueError("at least one MC sweep is required")
        title, label, hint = _STATISTICS[statistic]
        n = len(self.sweeps)
        ncols = 2 if n == 4 else min(3, n)
        nrows = (n + ncols - 1) // ncols
        fig, axes = plt.subplots(nrows, ncols, figsize=figsize or (5.3 * ncols, 4.4 * nrows))
        flat_axes = np.atleast_1d(axes).ravel()
        norm = self._norm(statistic)
        mesh = None
        for ax, sweep in zip(flat_axes, self.sweeps):
            mesh = sweep._plot_on(ax, norm, statistic, contour_levels)
        for ax in flat_axes[n:]:
            ax.set_visible(False)
        fig.suptitle(title, fontsize=15, fontweight="bold")
        fig.text(0.5, 0.925, hint, ha="center", fontsize=9.5, style="italic", wrap=True)
        fig.subplots_adjust(left=0.06, right=0.88, bottom=0.08, top=0.85,
                            wspace=0.27, hspace=0.45)
        fig.colorbar(mesh, ax=list(flat_axes[:n]), label=label,
                     shrink=0.86, fraction=0.025, pad=0.03)
        if path is not None:
            out = Path(path)
            out.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(out, dpi=180)
            plt.close(fig)
            if save_individual:
                for i, sweep in enumerate(self.sweeps, start=1):
                    one, ax = plt.subplots(figsize=(7.0, 5.2))
                    one_mesh = sweep._plot_on(ax, norm, statistic, contour_levels)
                    one.colorbar(one_mesh, ax=ax, label=label)
                    one.tight_layout()
                    one.savefig(out.with_name(f"{out.stem}_{i}.png"), dpi=180)
                    plt.close(one)
        return self

    def plot_slices(
        self,
        path: Optional[Union[str, Path]],
        pdes: Sequence[object],
        lambdas: Sequence[float] = (1.0, 2.0, 6.0),
    ) -> "TimeLambdaMCComparison":
        """Variance along ``T`` at fixed rates: exact flat-data theory vs MC.

        One row per sweep (``pdes[i]`` is any-horizon PDE of sweep ``i``;
        flat polynomial semilinear data only), one column per rate (the
        nearest grid rate is used). The exact ``Var(H)`` is drawn up to
        ``T_2``, where it diverges.
        """
        if len(pdes) != len(self.sweeps):
            raise ValueError("pdes must give one PDE per sweep")
        rows, cols = len(self.sweeps), len(lambdas)
        fig, axes = plt.subplots(rows, cols, figsize=(4.6 * cols, 3.3 * rows), squeeze=False)
        for sweep, pde, row in zip(self.sweeps, pdes, axes):
            leaf = flat_semilinear_leaf_values(pde, sweep.flat_terminal)
            for ax, target in zip(row, lambdas):
                j = int(np.argmin(np.abs(sweep.lambdas - target)))
                rate = float(sweep.lambdas[j])
                t2 = float(_boundary(rate, sweep.K)) if math.isfinite(sweep.K) else math.inf
                end = min(t2 * (1.0 - 1e-4), float(sweep.horizons[-1]))
                ok = (sweep.status[:, j] == _COMPLETE) & (sweep.variance[:, j] > 0)
                ax.semilogy(sweep.horizons[ok], sweep.variance[ok, j], "o", ms=2.8,
                            color="tab:blue", label=f"MC sample variance, N={sweep.n_samples:,}")
                if end > sweep.horizons[0]:   # some horizons lie below T_2
                    fine = np.linspace(float(sweep.horizons[0]), end, 400)
                    ax.semilogy(fine, flat_exact_variance(leaf, sweep.flat_terminal, rate, fine),
                                color="black", linewidth=1.6, label="exact Var(H)")
                if t2 <= sweep.horizons[-1]:
                    ax.axvline(t2, color="red", linestyle="--", linewidth=1.3,
                               label=r"$T_2(\lambda)$")
                ax.set_title(f"{sweep.title}, λ = {rate:.2f}", fontsize=9.5, fontweight="bold")
                ax.set_xlabel(r"horizon $T$")
                ax.set_ylabel("variance")
        axes[0, 0].legend(fontsize=7.5, loc="upper left")
        fig.suptitle("Variance along T at fixed λ: exact theory vs Monte Carlo",
                     fontsize=14, fontweight="bold")
        fig.text(0.5, 1 - 0.55 / (3.3 * rows), "MC agrees with the exact variance below T₂; "
                 "the exact variance diverges at T₂, which a finite batch cannot follow.",
                 ha="center", fontsize=9.5, style="italic")
        fig.tight_layout(rect=(0, 0, 1, 1 - 0.75 / (3.3 * rows)))
        if path is not None:
            out = Path(path)
            out.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(out, dpi=150)
            plt.close(fig)
        return self

    def save(self, path: Union[str, Path]) -> "TimeLambdaMCComparison":
        """Save sweeps with a common array shape to one pickle-free NPZ."""
        shapes = {(len(s.horizons), len(s.lambdas)) for s in self.sweeps}
        if len(shapes) > 1:
            raise ValueError("combined NPZ requires all MC sweeps to have the same grid shape")
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        metadata = json.dumps({
            "version": 1,
            "titles": [s.title for s in self.sweeps],
            "flat_terminal": [s.flat_terminal for s in self.sweeps],
            "K": [s.K for s in self.sweeps],
            "seed": [s.seed for s in self.sweeps],
            "n_samples": [s.n_samples for s in self.sweeps],
            "max_nodes": [s.max_nodes for s in self.sweeps],
            "max_cell_nodes": [s.max_cell_nodes for s in self.sweeps],
            "reference_T": [s.reference_T for s in self.sweeps],
            "theory_points": [s.theory_points for s in self.sweeps],
            "chunk_size": [s.chunk_size for s in self.sweeps],
            "sampler": [s.sampler for s in self.sweeps],
            "kind": "comparison",
        }, sort_keys=True)
        extra = {
            name: np.stack([getattr(s, name) for s in self.sweeps])
            for name in _DIAGNOSTICS
            if all(getattr(s, name) is not None for s in self.sweeps)
        }
        np.savez_compressed(
            out, metadata=np.asarray(metadata),
            lambdas=np.stack([s.lambdas for s in self.sweeps]),
            horizons=np.stack([s.horizons for s in self.sweeps]),
            variance=np.stack([s.variance for s in self.sweeps]),
            mean=np.stack([s.mean for s in self.sweeps]),
            second_moment=np.stack([s.second_moment for s in self.sweeps]),
            completed_samples=np.stack([s.completed_samples for s in self.sweeps]),
            total_nodes=np.stack([s.total_nodes for s in self.sweeps]),
            status=np.stack([s.status for s in self.sweeps]),
            reason=np.stack([s.reason for s in self.sweeps]),
            **extra,
        )
        return self

    @classmethod
    def load(cls, path: Union[str, Path]) -> "TimeLambdaMCComparison":
        with np.load(path, allow_pickle=False) as data:
            meta = json.loads(str(data["metadata"].item()))
            if meta.get("kind") == "sweep" or "titles" not in meta:
                return cls([TimeLambdaMCSweep.load(path)])
            arrays = {name: data[name].copy() for name in (
                "lambdas", "horizons", "variance", "mean", "second_moment",
                "completed_samples", "total_nodes", "status", "reason",
            )}
            arrays.update({name: data[name].copy() for name in _DIAGNOSTICS
                           if name in data.files})
        sweeps = []
        for i, title in enumerate(meta["titles"]):
            sweeps.append(TimeLambdaMCSweep(
                title=title, flat_terminal=float(meta["flat_terminal"][i]),
                K=float(meta["K"][i]), lambdas=arrays["lambdas"][i],
                horizons=arrays["horizons"][i], variance=arrays["variance"][i],
                mean=arrays["mean"][i], second_moment=arrays["second_moment"][i],
                completed_samples=arrays["completed_samples"][i],
                total_nodes=arrays["total_nodes"][i], status=arrays["status"][i],
                reason=arrays["reason"][i], seed=int(meta["seed"][i]),
                n_samples=int(meta["n_samples"][i]), max_nodes=meta["max_nodes"][i],
                max_cell_nodes=meta["max_cell_nodes"][i],
                reference_T=float(meta["reference_T"][i]),
                theory_points=int(meta.get("theory_points", [401] * len(meta["titles"]))[i]),
                chunk_size=meta.get("chunk_size", [None] * len(meta["titles"]))[i],
                sampler=meta.get("sampler", ["tree"] * len(meta["titles"]))[i],
                **{name: arrays[name][i] if name in arrays else None
                   for name in _DIAGNOSTICS},
            ))
        return cls(sweeps)


def sweep_time_lambda_mc(
    pde_factory: Callable[[float], object],
    *,
    flat_terminal: Optional[float] = None,
    title: Optional[str] = None,
    lambda_min: float = 0.01,
    lambda_max: float = 12.0,
    n_lambda: int = 12,
    T_min: float = 0.05,
    T_max: float = 1.3,
    n_T: int = 10,
    n_samples: int = 128,
    seed: int = 20261012,
    max_nodes: Optional[int] = None,
    max_cell_nodes: Optional[int] = None,
    reference_T: float = 0.5,
    theory_points: int = 401,
    checkpoint_path: Optional[Union[str, Path]] = None,
    progress: bool = True,
    n_jobs: int = 1,
    chunk_size: Optional[int] = None,
    checkpoint_every: float = 300.0,
    sampler: str = "tree",
    n_batches: int = 10,
) -> TimeLambdaMCSweep:
    """Sample one full-tree batch at every ``(T, lambda)`` cell.

    The default has no cumulative node budget. ``max_nodes`` and
    ``max_cell_nodes`` are optional work guards; they mark an affected cell
    invalid rather than returning a truncated estimator.

    ``n_jobs > 1`` samples in that many worker processes; ``pde_factory``
    must then be picklable (a module-level function or ``functools.partial``).
    ``chunk_size`` splits each cell into independently seeded chunks of at
    most that many trees, so one expensive cell can use several workers.
    Results depend on ``seed`` and ``chunk_size`` but not on ``n_jobs``; with
    ``chunk_size=None`` (one chunk per cell) they equal the serial results.
    A failing chunk invalidates the cell exactly as a failing tree does in
    the serial loop. ``max_cell_nodes`` is a cumulative serial budget and
    requires ``n_jobs=1``. In parallel mode, checkpoints are written every
    ``checkpoint_every`` seconds.

    ``sampler="flat"`` uses the vectorized sampler of ``flat_batch`` (same
    distribution of ``H`` for a flat polynomial semilinear PDE; different
    random stream and node counts); it requires ``flat_terminal`` and
    defaults to chunks of at most 100 000 trees, serial or parallel.

    Every completed cell also records instability diagnostics: the number
    of nonzero samples, the largest sample's share ``max H^2 / sum H^2`` of
    the sum of squares, and the sample variances of ``n_batches`` equal
    consecutive sub-batches.
    """
    values = (lambda_min, lambda_max, T_min, T_max, reference_T)
    if not all(math.isfinite(v) and v > 0.0 for v in values):
        raise ValueError("lambda/T bounds and reference_T must be finite and positive")
    if lambda_max <= lambda_min or T_max <= T_min:
        raise ValueError("maximum grid bounds must exceed minimum bounds")
    for name, count in (("n_lambda", n_lambda), ("n_T", n_T),
                        ("n_samples", n_samples), ("theory_points", theory_points)):
        if (not isinstance(count, (int, np.integer)) or isinstance(count, bool)
                or count < 2):
            raise ValueError(f"{name} must be an integer at least 2")
    if not isinstance(seed, (int, np.integer)) or isinstance(seed, bool) or seed < 0:
        raise ValueError("seed must be a non-negative integer")
    for name, limit in (("max_nodes", max_nodes), ("max_cell_nodes", max_cell_nodes)):
        if limit is not None and (not isinstance(limit, (int, np.integer)) or isinstance(limit, bool) or limit < 1):
            raise ValueError(f"{name} must be None or a positive integer")
    for name, count in (("n_jobs", n_jobs), ("chunk_size", chunk_size)):
        if count is not None and (not isinstance(count, (int, np.integer))
                                  or isinstance(count, bool) or count < 1):
            raise ValueError(f"{name} must be a positive integer")
    if n_jobs is None:
        raise ValueError("n_jobs must be a positive integer")
    if n_jobs > 1 and max_cell_nodes is not None:
        raise ValueError("max_cell_nodes is a serial cumulative budget; use n_jobs=1")
    if sampler not in _SAMPLERS:
        raise ValueError(f"sampler must be one of {_SAMPLERS}")
    if sampler == "tree" and chunk_size is not None and chunk_size < n_samples and n_jobs == 1:
        raise ValueError("chunk_size applies to parallel sampling; use n_jobs > 1")
    if sampler == "flat" and max_cell_nodes is not None:
        raise ValueError("max_cell_nodes is a serial cumulative budget of the tree sampler")
    if (not isinstance(n_batches, (int, np.integer)) or isinstance(n_batches, bool)
            or n_batches < 2):
        raise ValueError("n_batches must be an integer at least 2")

    lambdas = np.linspace(lambda_min, lambda_max, n_lambda)
    horizons = np.linspace(T_min, T_max, n_T)
    theory_pde = pde_factory(reference_T)
    theory = sweep_time_lambda(
        theory_pde, flat_terminal=flat_terminal, title=title,
        lambda_min=lambda_min, lambda_max=lambda_max, n_points=theory_points,
        reference_T=reference_T,
    )
    shape = (n_T, n_lambda)
    result = TimeLambdaMCSweep(
        title=theory.title, flat_terminal=theory.flat_terminal, K=theory.K,
        lambdas=lambdas, horizons=horizons,
        variance=np.full(shape, np.nan), mean=np.full(shape, np.nan),
        second_moment=np.full(shape, np.nan),
        completed_samples=np.zeros(shape, dtype=np.int32),
        total_nodes=np.zeros(shape, dtype=np.int64),
        status=np.full(shape, _PENDING, dtype="<U16"),
        reason=np.full(shape, "", dtype="<U160"), seed=int(seed),
        n_samples=int(n_samples), max_nodes=None if max_nodes is None else int(max_nodes),
        max_cell_nodes=None if max_cell_nodes is None else int(max_cell_nodes),
        reference_T=reference_T,
        theory_points=int(theory_points),
        sampler=sampler,
        n_nonzero=np.zeros(shape, dtype=np.int64),
        max_share=np.full(shape, np.nan),
        batch_variance=np.full(shape + (min(int(n_batches), n_samples // 2),), np.nan),
    )

    flat = None
    if sampler == "flat":
        flat = (tuple(flat_semilinear_leaf_values(theory_pde, flat_terminal)),
                float(flat_terminal))
        if chunk_size is None and n_samples > _FLAT_DEFAULT_CHUNK:
            chunk_size = _FLAT_DEFAULT_CHUNK
    if n_jobs > 1 or flat is not None:
        if chunk_size is not None and chunk_size < n_samples:
            result.chunk_size = int(chunk_size)
        return _fill_chunks(
            result, pde_factory, n_jobs=int(n_jobs),
            chunk_size=int(n_samples if result.chunk_size is None else result.chunk_size),
            checkpoint_path=checkpoint_path, progress=progress,
            checkpoint_every=checkpoint_every, flat=flat,
        )

    current = None
    try:
        for ti, horizon in enumerate(horizons):
            pde = pde_factory(float(horizon))
            if not math.isclose(float(pde.T), float(horizon), rel_tol=0.0, abs_tol=1e-14):
                raise ValueError("pde_factory must construct a PDE with the requested horizon")
            for li, rate in enumerate(lambdas):
                current = (ti, li)
                rng = _cell_rng(int(seed), ti, li)
                samples = np.empty(n_samples)
                for si in range(n_samples):
                    remaining_nodes = (
                        None if max_cell_nodes is None
                        else max_cell_nodes - int(result.total_nodes[ti, li])
                    )
                    if remaining_nodes is not None and remaining_nodes < 1:
                        result.status[ti, li] = _CELL_BUDGET
                        result.reason[ti, li] = f"cell reached max_cell_nodes={max_cell_nodes}"
                        break
                    budget_limited = (
                        remaining_nodes is not None
                        and (max_nodes is None or remaining_nodes < max_nodes)
                    )
                    tree_limit = max_nodes
                    if remaining_nodes is not None:
                        tree_limit = remaining_nodes if tree_limit is None else min(tree_limit, remaining_nodes)
                    try:
                        sample = sample_tree(
                            pde, 0.0, 0.0, rng=rng, rate=float(rate),
                            max_nodes=tree_limit,
                        )
                    except TreeNodeLimitExceeded as exc:
                        result.total_nodes[ti, li] += exc.n_nodes
                        result.status[ti, li] = _CELL_BUDGET if budget_limited else _NODE_LIMIT
                        result.reason[ti, li] = str(exc)
                        break
                    except (FloatingPointError, OverflowError, RecursionError) as exc:
                        result.status[ti, li] = _ERROR
                        result.reason[ti, li] = f"{type(exc).__name__}: {exc}"
                        break
                    result.completed_samples[ti, li] = si + 1
                    result.total_nodes[ti, li] += sample.n_nodes
                    if not math.isfinite(sample.value):
                        result.status[ti, li] = _NONFINITE
                        result.reason[ti, li] = "sample_tree returned a non-finite value"
                        break
                    samples[si] = sample.value
                else:
                    _store_statistics(result, ti, li, samples)
            if checkpoint_path is not None:
                result.save(checkpoint_path)
            if progress:
                complete = int(np.count_nonzero(result.status[ti] == _COMPLETE))
                invalid = n_lambda - complete
                print(f"{result.title}: row {ti + 1}/{n_T}, T={horizon:.6g}, "
                      f"complete={complete}, invalid={invalid}", flush=True)
    except KeyboardInterrupt:
        if current is not None and result.status[current] == _PENDING:
            result.status[current] = _INTERRUPTED
            result.reason[current] = "interrupted by user"
        if checkpoint_path is not None:
            result.save(checkpoint_path)
            print(f"Partial MC grid saved to {Path(checkpoint_path).resolve()}", flush=True)
        raise
    return result


def _sample_variance(samples: np.ndarray) -> float:
    return 0.0 if np.all(samples == samples[0]) else float(np.var(samples, ddof=1))


def _cell_summary(samples: np.ndarray, n_batches: int) -> dict:
    """Statistics and instability diagnostics of one completed cell.

    Computed where the samples live (a worker process in parallel runs), so
    only this small summary has to be sent back.
    """
    with np.errstate(over="ignore", invalid="ignore"):
        mean = float(np.mean(samples))
        variance = _sample_variance(samples)
        squares = samples * samples
        second_moment = float(np.mean(squares))
        total = float(np.sum(squares))
        batches = np.array([_sample_variance(b) for b in np.array_split(samples, n_batches)])
    return {
        "n_nonzero": int(np.count_nonzero(samples)),
        "finite": all(math.isfinite(v) for v in (mean, variance, second_moment)),
        "mean": mean, "variance": variance, "second_moment": second_moment,
        "max_share": float(np.max(squares)) / total if 0.0 < total < math.inf else np.nan,
        "batch_variance": batches,
    }


def _apply_summary(result: TimeLambdaMCSweep, ti: int, li: int, summary: dict) -> None:
    result.n_nonzero[ti, li] = summary["n_nonzero"]
    if not summary["finite"]:
        result.status[ti, li] = _NONFINITE
        result.reason[ti, li] = "batch statistic was non-finite"
        return
    for name in ("mean", "variance", "second_moment", "max_share", "batch_variance"):
        getattr(result, name)[ti, li] = summary[name]
    result.status[ti, li] = _COMPLETE


def _store_statistics(result: TimeLambdaMCSweep, ti: int, li: int,
                      samples: np.ndarray) -> None:
    """Fill one completed cell's statistics and instability diagnostics."""
    _apply_summary(result, ti, li, _cell_summary(samples, result.batch_variance.shape[2]))


def _run_cell(ti: int, li: int, sizes: Sequence[int], horizon: float, rate: float,
              seed: int, max_nodes: Optional[int], flat: Optional[tuple],
              n_batches: int) -> tuple:
    """Sample a whole cell chunk by chunk and summarize it in place.

    Returns ``(ti, li, completed, nodes, status, reason, summary)``; the
    chunk seeds and the stop-at-first-failure rule match ``_finish_cell``.
    """
    values, nodes = [], 0
    for c, size in enumerate(sizes):
        _, _, _, chunk_values, chunk_nodes, status, reason = _run_chunk(
            ti, li, c, len(sizes), size, horizon, rate, seed, max_nodes, flat)
        values.append(chunk_values)
        nodes += chunk_nodes
        if status is not None:
            return ti, li, sum(len(v) for v in values), nodes, status, reason, None
    samples = np.concatenate(values)
    return (ti, li, len(samples), nodes, None, "",
            _cell_summary(samples, n_batches))


def _finish_cell(result: TimeLambdaMCSweep, ti: int, li: int, chunks: list) -> None:
    """Combine a cell's chunk results in chunk order, as the serial loop would."""
    values, nodes = [], 0
    for _, _, _, chunk_values, chunk_nodes, status, reason in chunks:
        values.append(chunk_values)
        nodes += chunk_nodes
        if status is not None:
            result.completed_samples[ti, li] = sum(len(v) for v in values)
            result.total_nodes[ti, li] = nodes
            result.status[ti, li] = status
            result.reason[ti, li] = reason
            return
    samples = np.concatenate(values)
    result.completed_samples[ti, li] = len(samples)
    result.total_nodes[ti, li] = nodes
    _store_statistics(result, ti, li, samples)


def _fill_chunks(
    result: TimeLambdaMCSweep,
    pde_factory: Callable[[float], object],
    *,
    n_jobs: int,
    chunk_size: int,
    checkpoint_path: Optional[Union[str, Path]],
    progress: bool,
    checkpoint_every: float,
    flat: Optional[tuple] = None,
) -> TimeLambdaMCSweep:
    for horizon in result.horizons:
        pde = pde_factory(float(horizon))
        if not math.isclose(float(pde.T), float(horizon), rel_tol=0.0, abs_tol=1e-14):
            raise ValueError("pde_factory must construct a PDE with the requested horizon")
        if flat is not None and tuple(flat_semilinear_leaf_values(pde, flat[1])) != flat[0]:
            raise ValueError("pde_factory must give the same flat data at every horizon")

    n = result.n_samples
    n_chunks = -(-n // chunk_size)
    sizes = [min(chunk_size, n - c * chunk_size) for c in range(n_chunks)]
    # Run the presumably most expensive cells (large lambda*T) first to
    # shorten the tail; results do not depend on the order.
    cells = sorted(
        ((ti, li) for ti in range(len(result.horizons)) for li in range(len(result.lambdas))),
        key=lambda c: -result.horizons[c[0]] * result.lambdas[c[1]],
    )
    n_cells = len(cells)
    received: dict = {}
    start = last_save = time.monotonic()

    def task(ti: int, li: int, c: int) -> tuple:
        return (_run_chunk, ti, li, c, n_chunks, sizes[c],
                float(result.horizons[ti]), float(result.lambdas[li]),
                result.seed, result.max_nodes, flat)

    def report_and_save(final: bool = False) -> None:
        if checkpoint_path is not None:
            result.save(checkpoint_path)
        if progress:
            complete = int(np.count_nonzero(result.status == _COMPLETE))
            finished = int(np.count_nonzero(result.status != _PENDING))
            print(f"{result.title}: {finished}/{n_cells} cells finished "
                  f"(complete={complete}, invalid={finished - complete}), "
                  f"elapsed {time.monotonic() - start:.0f}s"
                  + (" [done]" if final else ""), flush=True)

    def maybe_report() -> None:
        nonlocal last_save
        if time.monotonic() - last_save >= checkpoint_every:
            report_and_save()
            last_save = time.monotonic()

    if progress:
        print(f"{result.title}: {n_cells} cells x {n_chunks} chunk(s) of <= {chunk_size} "
              f"trees, {result.sampler} sampler, {n_jobs} worker(s); progress every "
              f"{checkpoint_every:.0f}s", flush=True)

    if flat is not None:
        return _fill_cells(result, sizes, cells, n_jobs, pde_factory, flat,
                           report_and_save, maybe_report, received)

    if n_jobs == 1:
        _worker_init(pde_factory)
        try:
            for ti, li in cells:
                received[ti, li] = True
                ordered = []
                for c in range(n_chunks):
                    fn, *args = task(ti, li, c)
                    out = fn(*args)
                    ordered.append(out)
                    if out[5] is not None:
                        break
                _finish_cell(result, ti, li, ordered)
                del received[ti, li]
                maybe_report()
        except KeyboardInterrupt:
            _mark_interrupted(result, received, checkpoint_path)
            raise
        report_and_save(final=True)
        return result

    futures: dict = {}
    cell_futures: dict = {}
    executor = ProcessPoolExecutor(max_workers=n_jobs, initializer=_worker_init,
                                   initargs=(pde_factory,))
    try:
        for ti, li in cells:
            cell_futures[ti, li] = []
            for c in range(n_chunks):
                fut = executor.submit(*task(ti, li, c))
                futures[fut] = (ti, li, c)
                cell_futures[ti, li].append(fut)
        for fut in as_completed(futures):
            # Drop our references so finished chunk arrays can be freed.
            ti, li, c = futures.pop(fut)
            chunks = received.setdefault((ti, li), [None] * n_chunks)
            if fut.cancelled():
                chunks[c] = _CANCELLED
            else:
                out = fut.result()
                chunks[c] = out
                if out[5] is not None:
                    # Later chunks of a failed cell cannot affect it.
                    for other in cell_futures[ti, li][c + 1:]:
                        other.cancel()
            if all(x is not None for x in chunks):
                ordered = []
                for x in chunks:
                    if x is _CANCELLED:
                        break
                    ordered.append(x)
                    if x[5] is not None:
                        break
                _finish_cell(result, ti, li, ordered)
                del received[ti, li], cell_futures[ti, li]
            maybe_report()
    except KeyboardInterrupt:
        executor.shutdown(wait=False, cancel_futures=True)
        _mark_interrupted(result, received, checkpoint_path)
        raise
    executor.shutdown()
    report_and_save(final=True)
    return result


def _fill_cells(result, sizes, cells, n_jobs, pde_factory, flat,
                report_and_save, maybe_report, received) -> TimeLambdaMCSweep:
    """One task per cell; workers return summaries, not raw samples."""
    n_batches = result.batch_variance.shape[2]

    def args(ti, li):
        return (ti, li, sizes, float(result.horizons[ti]), float(result.lambdas[li]),
                result.seed, result.max_nodes, flat, n_batches)

    def apply(out) -> None:
        ti, li, completed, nodes, status, reason, summary = out
        result.completed_samples[ti, li] = completed
        result.total_nodes[ti, li] = nodes
        if status is not None:
            result.status[ti, li] = status
            result.reason[ti, li] = reason
        else:
            _apply_summary(result, ti, li, summary)
        received.pop((ti, li), None)

    executor = None
    try:
        if n_jobs == 1:
            for ti, li in cells:
                received[ti, li] = True
                apply(_run_cell(*args(ti, li)))
                maybe_report()
        else:
            executor = ProcessPoolExecutor(max_workers=n_jobs, initializer=_worker_init,
                                           initargs=(pde_factory,))
            futures = {}
            for ti, li in cells:   # unstarted cells stay "pending" on interrupt
                futures[executor.submit(_run_cell, *args(ti, li))] = (ti, li)
            for fut in as_completed(futures):
                del futures[fut]
                apply(fut.result())
                maybe_report()
    except KeyboardInterrupt:
        if executor is not None:
            executor.shutdown(wait=False, cancel_futures=True)
        _mark_interrupted(result, received, None)
        report_and_save(final=False)
        raise
    if executor is not None:
        executor.shutdown()
    report_and_save(final=True)
    return result


def _mark_interrupted(result: TimeLambdaMCSweep, in_progress,
                      checkpoint_path: Optional[Union[str, Path]]) -> None:
    for ti, li in in_progress:
        result.status[ti, li] = _INTERRUPTED
        result.reason[ti, li] = "interrupted by user"
    if checkpoint_path is not None:
        result.save(checkpoint_path)
        print(f"Partial MC grid saved to {Path(checkpoint_path).resolve()}", flush=True)


def compare_time_lambda_mc(*sweeps: TimeLambdaMCSweep) -> TimeLambdaMCComparison:
    return TimeLambdaMCComparison(sweeps)
