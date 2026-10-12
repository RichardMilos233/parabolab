"""Empirical full-tree Monte Carlo variance grids for T-lambda plots.

Every completed cell contains ordinary ``sample_tree`` realizations at that
cell's PDE horizon and branching rate.  Invalid cells are retained as status
data rather than filtered or replaced.  A finite batch cannot establish that
the population second moment is finite or infinite.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Callable, Optional, Sequence, Union

import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm
import numpy as np

from .time_lambda import _boundary, sweep_time_lambda
from .tree import TreeNodeLimitExceeded, sample_tree


_PENDING = "pending"
_COMPLETE = "complete"
_NODE_LIMIT = "node_limit"
_CELL_BUDGET = "cell_budget"
_NONFINITE = "nonfinite"
_ERROR = "error"
_INTERRUPTED = "interrupted"


def _cell_rng(seed: int, t_index: int, lambda_index: int) -> np.random.Generator:
    return np.random.default_rng(np.random.SeedSequence([seed, t_index, lambda_index]))


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
            "kind": "sweep",
        }, sort_keys=True)
        np.savez_compressed(
            out, metadata=np.asarray(metadata), lambdas=self.lambdas,
            horizons=self.horizons, variance=self.variance, mean=self.mean,
            second_moment=self.second_moment,
            completed_samples=self.completed_samples, total_nodes=self.total_nodes,
            status=self.status, reason=self.reason,
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
            )

    def _plot_on(self, ax: plt.Axes, norm: SymLogNorm):
        valid = (self.status == _COMPLETE) & np.isfinite(self.variance)
        values = np.ma.array(self.variance, mask=~valid)
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
        ax.axhline(self.reference_T, color="white", linestyle="--", linewidth=1.4,
                   label=rf"reference $T={self.reference_T:g}$")
        ax.set_xlim(self.lambdas[0], self.lambdas[-1])
        ax.set_ylim(self.horizons[0], self.horizons[-1])
        ax.set_title(
            f"{self.title}\n{len(self.horizons)}×{len(self.lambdas)} cells, "
            f"n={self.n_samples}/cell",
            fontweight="bold",
        )
        ax.set_xlabel(r"branching rate $\lambda$")
        ax.set_ylabel(r"horizon $T$")
        invalid = int(np.size(valid) - np.count_nonzero(valid))
        if invalid:
            ax.text(0.02, 0.02, f"{invalid} invalid/uncompleted cells (grey)",
                    transform=ax.transAxes, fontsize=7.5,
                    bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none"})
        ax.legend(loc="upper right", fontsize=7.5)
        return mesh


class TimeLambdaMCComparison:
    """Several empirical grids sharing one variance color scale."""

    def __init__(self, sweeps: Sequence[TimeLambdaMCSweep]):
        self.sweeps = list(sweeps)

    def _norm(self) -> SymLogNorm:
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
    ) -> "TimeLambdaMCComparison":
        if not self.sweeps:
            raise ValueError("at least one MC sweep is required")
        n = len(self.sweeps)
        ncols, nrows = min(3, n), (n + min(3, n) - 1) // min(3, n)
        fig, axes = plt.subplots(nrows, ncols, figsize=figsize or (5.3 * ncols, 4.4 * nrows))
        flat_axes = np.atleast_1d(axes).ravel()
        norm = self._norm()
        mesh = None
        for ax, sweep in zip(flat_axes, self.sweeps):
            mesh = sweep._plot_on(ax, norm)
        for ax in flat_axes[n:]:
            ax.set_visible(False)
        fig.suptitle("Observed full-tree MC sample variance with theoretical boundary",
                     fontsize=15, fontweight="bold")
        fig.subplots_adjust(left=0.06, right=0.88, bottom=0.08, top=0.90,
                            wspace=0.27, hspace=0.32)
        fig.colorbar(mesh, ax=list(flat_axes[:n]), label="Sample variance (symlog, ddof=1)",
                     shrink=0.86, fraction=0.025, pad=0.03)
        if path is not None:
            out = Path(path)
            out.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(out, dpi=180)
            plt.close(fig)
            if save_individual:
                for i, sweep in enumerate(self.sweeps, start=1):
                    one, ax = plt.subplots(figsize=(7.0, 5.2))
                    one_mesh = sweep._plot_on(ax, norm)
                    one.colorbar(one_mesh, ax=ax, label="Sample variance (symlog, ddof=1)")
                    one.tight_layout()
                    one.savefig(out.with_name(f"{out.stem}_{i}.png"), dpi=180)
                    plt.close(one)
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
            "kind": "comparison",
        }, sort_keys=True)
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
    max_nodes: Optional[int] = 5_000,
    max_cell_nodes: Optional[int] = 100_000,
    reference_T: float = 0.5,
    theory_points: int = 401,
    checkpoint_path: Optional[Union[str, Path]] = None,
    progress: bool = True,
) -> TimeLambdaMCSweep:
    """Sample one independent full-tree batch at every ``(T, lambda)`` cell."""
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
                    with np.errstate(over="ignore", invalid="ignore"):
                        mean = float(np.mean(samples))
                        variance = (
                            0.0 if np.all(samples == samples[0])
                            else float(np.var(samples, ddof=1))
                        )
                        second_moment = float(np.mean(samples * samples))
                    if all(math.isfinite(v) for v in (mean, variance, second_moment)):
                        result.mean[ti, li] = mean
                        result.variance[ti, li] = variance
                        result.second_moment[ti, li] = second_moment
                        result.status[ti, li] = _COMPLETE
                    else:
                        result.status[ti, li] = _NONFINITE
                        result.reason[ti, li] = "batch statistic was non-finite"
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


def compare_time_lambda_mc(*sweeps: TimeLambdaMCSweep) -> TimeLambdaMCComparison:
    return TimeLambdaMCComparison(sweeps)
