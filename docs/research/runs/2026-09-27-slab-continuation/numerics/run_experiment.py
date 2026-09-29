"""Run the prespecified learned-slab and bounded-majority experiments.

The slab calculation uses the exact Jacobi datum only as the first terminal
input.  Every later slab freezes the preceding clipped three-sine interface.
Raw tree values are never clipped or discarded.  Each completed stage stores
the root position, tree value, node count, and branching diagnostics in its
own compressed archive so that long runs checkpoint at stage boundaries.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import shlex
import subprocess
import sys
import time
from typing import Callable, Sequence

import mpmath as mp
import numpy as np
from scipy import special

try:
    from slab_sampler import majority_sample, raw_sample
except ImportError:  # pragma: no cover - supports package-style test imports
    from .slab_sampler import majority_sample, raw_sample


HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO = HERE.parents[4]
THEORY = RUN_DIR / "04-theory.md"
PLAN = RUN_DIR / "02-plan.md"
SAMPLER_SOURCE = HERE / "slab_sampler.py"

M = 0.05
A = math.sqrt(2.0 / 21.0)
KAPPA = math.sqrt(40.0 / 21.0)
RATE = 2.0
SLAB_H = 0.08
MODES = np.array((1, 3, 5), dtype=np.int64)
CAPS = np.array((0.23, 0.003, 0.00005), dtype=float)
PRIMARY_N = 200_000
PRIMARY_SEEDS = (2026092701, 2026092702, 2026092703)
PRIMARY_STAGES = 50
MAJORITY_N = 8_000
MAJORITY_SEEDS = (2026092711, 2026092712, 2026092713)
MAJORITY_HORIZONS = (0.8, 2.0)
RAW_BATCH_SIZE = 10_000
MAJORITY_BATCH_SIZE = 32
GRID_POINTS = 16_384
REFERENCE_DPS = 80
MAX_SECONDS = 2.0 * 60.0 * 60.0
TERMINAL_CODE_ORDER = ("Id", "Dx", "F0", "F1", "F2", "F3")


@dataclass(frozen=True)
class ReferenceData:
    period: float
    omega: float
    nome: float
    coefficients: np.ndarray
    tail_squared: float
    record: dict


@dataclass(frozen=True)
class CollectedSamples:
    positions: np.ndarray
    values: np.ndarray
    node_counts: np.ndarray
    root_branched: np.ndarray
    terminal_counts: np.ndarray
    scheduled_roots: int
    complete: bool
    seconds: float


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _json_write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _git_revision() -> str | None:
    result = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def _mp_string(value: mp.mpf, digits: int = 50) -> str:
    return mp.nstr(value, digits, strip_zeros=False)


def compute_reference(dps: int = REFERENCE_DPS) -> ReferenceData:
    """Compute Jacobi/Fourier checks independently with high-precision mpmath."""
    if dps < 40:
        raise ValueError("reference precision must be at least 40 decimal digits")
    with mp.workdps(dps):
        m = mp.mpf(1) / 20
        amplitude = mp.sqrt(mp.mpf(2) / 21)
        kappa = mp.sqrt(mp.mpf(40) / 21)
        complete_k = mp.ellipk(m)
        complementary_k = mp.ellipk(1 - m)
        period = 4 * complete_k / kappa
        omega = 2 * mp.pi / period
        nome = mp.exp(-mp.pi * complementary_k / complete_k)
        fourier_scale = 2 * mp.pi / (complete_k * mp.sqrt(mp.mpf(21) / 20))

        def coefficient(index: int) -> mp.mpf:
            r = mp.mpf(index)
            return (
                fourier_scale
                * nome ** (r + mp.mpf("0.5"))
                / (1 - nome ** (2 * r + 1))
            )

        coefficients_mp = tuple(coefficient(index) for index in range(3))
        tail_squared = mp.nsum(lambda r: coefficient(r) ** 2, [3, mp.inf])

        def datum(x: mp.mpf) -> mp.mpf:
            return amplitude * mp.ellipfun("sn", kappa * x, m)

        quadrature_coefficients = []
        for mode in MODES:
            integrand = lambda x, n=int(mode): (
                datum(x) * mp.sqrt(2) * mp.sin(n * omega * x) / period
            )
            quadrature_coefficients.append(
                mp.quad(
                    integrand,
                    [0, period / 4, period / 2, 3 * period / 4, period],
                )
            )

        residuals = []
        for index in range(17):
            x = period * mp.mpf(index) / 17
            second = mp.diff(datum, x, 2)
            value = datum(x)
            residuals.append(abs(second / 2 + value - value**3))
        coefficient_differences = [
            abs(left - right)
            for left, right in zip(coefficients_mp, quadrature_coefficients)
        ]

        cap_value_bound = mp.sqrt(2) * sum(mp.mpf(str(cap)) for cap in CAPS)
        cap_derivative_bound = (
            mp.sqrt(2)
            * omega
            * sum(
                mp.mpf(int(mode)) * mp.mpf(str(cap))
                for mode, cap in zip(MODES, CAPS)
            )
        )
        analytical_tail_bound = (
            mp.mpf(320)
            / (mp.mpf(21) * 300**3 * 299**2 * 89999)
        )
        checks = {
            "nome_lt_1_over_300": bool(nome < mp.mpf(1) / 300),
            "coefficients_inside_caps": bool(
                all(
                    abs(value) < mp.mpf(str(cap))
                    for value, cap in zip(coefficients_mp, CAPS)
                )
            ),
            "tail_squared_lt_1e_16": bool(tail_squared < mp.mpf("1e-16")),
            "tail_within_analytic_bound": bool(tail_squared <= analytical_tail_bound),
            "coefficient_quadrature_max_difference_lt_1e_40": bool(
                max(coefficient_differences) < mp.mpf("1e-40")
            ),
            "stationarity_max_residual_lt_1e_40": bool(max(residuals) < mp.mpf("1e-40")),
            "coefficient_box_value_bound_lt_2_over_5": bool(cap_value_bound < mp.mpf(2) / 5),
            "coefficient_box_derivative_bound_lt_1_over_2": bool(
                cap_derivative_bound < mp.mpf(1) / 2
            ),
        }
        if not all(checks.values()):
            raise RuntimeError(f"independent Jacobi reference check failed: {checks}")

        record = {
            "method": "mpmath Jacobi functions, elliptic integrals, quadrature, and differentiation",
            "decimal_precision": dps,
            "parameter_m": "0.05",
            "amplitude": _mp_string(amplitude),
            "kappa": _mp_string(kappa),
            "complete_elliptic_k": _mp_string(complete_k),
            "complementary_complete_elliptic_k": _mp_string(complementary_k),
            "period": _mp_string(period),
            "omega": _mp_string(omega),
            "nome": _mp_string(nome),
            "fourier_coefficients_n_1_3_5": [_mp_string(value) for value in coefficients_mp],
            "quadrature_coefficients_n_1_3_5": [
                _mp_string(value) for value in quadrature_coefficients
            ],
            "coefficient_quadrature_absolute_differences": [
                _mp_string(value) for value in coefficient_differences
            ],
            "exact_fourier_tail_squared_after_n5": _mp_string(tail_squared),
            "analytical_tail_squared_upper_bound": _mp_string(analytical_tail_bound),
            "stationarity_max_absolute_residual": _mp_string(max(residuals)),
            "coefficient_box_value_upper_bound": _mp_string(cap_value_bound),
            "coefficient_box_derivative_upper_bound": _mp_string(cap_derivative_bound),
            "checks": checks,
        }
        return ReferenceData(
            period=float(period),
            omega=float(omega),
            nome=float(nome),
            coefficients=np.array([float(value) for value in coefficients_mp]),
            tail_squared=float(tail_squared),
            record=record,
        )


def jacobi_terminal(x):
    """Return the exact datum and derivative using scipy's parameter-m API."""
    points = np.asarray(x, dtype=float)
    sn, cn, dn, _ = special.ellipj(KAPPA * points, M)
    values = A * sn
    derivatives = A * KAPPA * cn * dn
    if points.ndim == 0:
        return float(values), float(derivatives)
    return values, derivatives


def basis_values(x: np.ndarray, omega: float) -> np.ndarray:
    points = np.asarray(x, dtype=float)
    return math.sqrt(2.0) * np.sin(points[..., None] * omega * MODES)


def polynomial_terminal(coefficients: Sequence[float], omega: float) -> Callable:
    """Freeze a coefficient vector and return its exact value/derivative callback."""
    frozen = np.array(coefficients, dtype=float, copy=True)
    if frozen.shape != (3,) or not np.all(np.isfinite(frozen)):
        raise ValueError("coefficients must be a finite vector of length three")
    frozen.setflags(write=False)

    def terminal(x):
        points = np.asarray(x, dtype=float)
        phases = points[..., None] * omega * MODES
        values = math.sqrt(2.0) * np.sum(frozen * np.sin(phases), axis=-1)
        derivatives = math.sqrt(2.0) * omega * np.sum(
            MODES * frozen * np.cos(phases), axis=-1
        )
        if points.ndim == 0:
            return float(values), float(derivatives)
        return values, derivatives

    return terminal


def stage_terminal(
    stage: int,
    previous_coefficients: Sequence[float] | None,
    omega: float,
    oracle: Callable = jacobi_terminal,
) -> Callable:
    """Select the actual continuation input; the oracle is reachable only at stage 1."""
    if stage < 1:
        raise ValueError("stage numbering starts at one")
    if stage == 1:
        return oracle
    if previous_coefficients is None:
        raise ValueError("a learned interface is required after stage one")
    return polynomial_terminal(previous_coefficients, omega)


def project_coefficients(raw_coefficients: Sequence[float]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    raw = np.asarray(raw_coefficients, dtype=float)
    if raw.shape != (3,) or not np.all(np.isfinite(raw)):
        raise ValueError("raw coefficients must be a finite vector of length three")
    projected = np.clip(raw, -CAPS, CAPS)
    mask = projected != raw
    return projected, mask, raw - projected


def interface_bounds(coefficients: Sequence[float], omega: float) -> dict[str, float | bool]:
    coeffs = np.asarray(coefficients, dtype=float)
    value_bound = math.sqrt(2.0) * float(np.abs(coeffs).sum())
    derivative_bound = (
        math.sqrt(2.0) * omega * float((MODES * np.abs(coeffs)).sum())
    )
    return {
        "analytic_sup_value_bound": value_bound,
        "analytic_sup_derivative_bound": derivative_bound,
        "value_admissible_lt_0p4": value_bound < 0.4,
        "derivative_admissible_lt_0p5": derivative_bound < 0.5,
    }


def _validate_sample_result(result, count: int) -> None:
    shapes = {
        "values": np.asarray(result.values).shape,
        "node_counts": np.asarray(result.node_counts).shape,
        "root_branched": np.asarray(result.root_branched).shape,
    }
    if any(shape != (count,) for shape in shapes.values()):
        raise RuntimeError(f"sampler returned misaligned root arrays: {shapes}")
    terminal_counts = np.asarray(result.terminal_counts)
    if terminal_counts.shape != (6,):
        raise RuntimeError("sampler terminal_counts must have fixed shape (6,)")
    if not np.all(np.isfinite(result.values)):
        raise FloatingPointError("nonfinite tree value; the stage is invalid and no root is discarded")
    if np.any(np.asarray(result.node_counts) < 1) or np.any(terminal_counts < 0):
        raise RuntimeError("sampler returned invalid cost counts")


def collect_samples(
    positions: np.ndarray,
    horizon: float,
    terminal: Callable,
    rng: np.random.Generator,
    sampler: Callable,
    batch_size: int,
    deadline: float | None,
    *,
    root_code: int | None,
) -> CollectedSamples:
    """Complete roots by fixed-size batches, stopping only between batches."""
    positions = np.asarray(positions, dtype=float)
    if positions.ndim != 1 or positions.size < 2 or not np.all(np.isfinite(positions)):
        raise ValueError("positions must contain at least two finite roots")
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    n_roots = positions.size
    values = np.empty(n_roots, dtype=float)
    nodes = np.empty(n_roots, dtype=np.int64)
    branched = np.empty(n_roots, dtype=bool)
    terminal_counts = np.zeros(6, dtype=np.int64)
    completed = 0
    started = time.perf_counter()
    while completed < n_roots:
        if deadline is not None and completed and time.perf_counter() >= deadline:
            break
        stop = min(completed + batch_size, n_roots)
        batch_positions = positions[completed:stop]
        if root_code is None:
            result = sampler(batch_positions, horizon, terminal, rng)
        else:
            result = sampler(
                batch_positions,
                horizon,
                terminal,
                rng,
                root_code=root_code,
            )
        _validate_sample_result(result, stop - completed)
        values[completed:stop] = result.values
        nodes[completed:stop] = result.node_counts
        branched[completed:stop] = result.root_branched
        terminal_counts += np.asarray(result.terminal_counts, dtype=np.int64)
        completed = stop
    return CollectedSamples(
        positions=positions[:completed].copy(),
        values=values[:completed].copy(),
        node_counts=nodes[:completed].copy(),
        root_branched=branched[:completed].copy(),
        terminal_counts=terminal_counts,
        scheduled_roots=n_roots,
        complete=completed == n_roots,
        seconds=time.perf_counter() - started,
    )


def _stage_statistics(
    samples: CollectedSamples,
    reference: ReferenceData,
    exact_grid: np.ndarray,
) -> tuple[np.ndarray, dict]:
    if not samples.complete:
        raise ValueError("partial stages cannot form coefficient estimates")
    observations = samples.values[:, None] * basis_values(samples.positions, reference.omega)
    raw_coefficients = observations.mean(axis=0)
    projected, projection_mask, projection_difference = project_coefficients(raw_coefficients)
    observation_covariance = np.cov(observations, rowvar=False, ddof=1)
    coefficient_covariance = observation_covariance / samples.values.size
    retained_error_squared = float(np.sum((projected - reference.coefficients) ** 2))
    raw_retained_error_squared = float(
        np.sum((raw_coefficients - reference.coefficients) ** 2)
    )
    grid = np.arange(exact_grid.size, dtype=float) * reference.period / exact_grid.size
    projected_grid = basis_values(grid, reference.omega) @ projected
    grid_l2 = float(np.sqrt(np.mean((projected_grid - exact_grid) ** 2)))
    exact_fourier_l2 = math.sqrt(retained_error_squared + reference.tail_squared)
    raw_exact_fourier_l2 = math.sqrt(raw_retained_error_squared + reference.tail_squared)
    stats = {
        "raw_coefficients": raw_coefficients.tolist(),
        "projected_coefficients": projected.tolist(),
        "projection_mask": projection_mask.tolist(),
        "projection_difference_raw_minus_projected": projection_difference.tolist(),
        "projection_distortion_l2": float(np.linalg.norm(projection_difference)),
        "projection_is_biased_interface_step": True,
        "local_tree_estimator_is_unbiased_conditional_on_frozen_interface": True,
        "coefficient_observation_covariance": observation_covariance.tolist(),
        "coefficient_estimator_covariance": coefficient_covariance.tolist(),
        "moments": {
            "tree_value_mean": float(samples.values.mean()),
            "tree_value_second_moment": float(np.mean(samples.values**2)),
            "tree_value_sample_variance": float(samples.values.var(ddof=1)),
            "coefficient_observation_second_moments": np.mean(observations**2, axis=0).tolist(),
        },
        "root_count": int(samples.values.size),
        "total_nodes": int(samples.node_counts.sum()),
        "mean_nodes": float(samples.node_counts.mean()),
        "max_nodes": int(samples.node_counts.max()),
        "root_branch_count": int(samples.root_branched.sum()),
        "root_branch_fraction": float(samples.root_branched.mean()),
        "terminal_code_order": list(TERMINAL_CODE_ORDER),
        "terminal_code_counts": samples.terminal_counts.tolist(),
        "max_absolute_tree_value": float(np.max(np.abs(samples.values))),
        "sampling_seconds": samples.seconds,
        "error": {
            "normalized_l2_exact_fourier_plus_tail": exact_fourier_l2,
            "normalized_l2_raw_coefficients_exact_fourier_plus_tail": raw_exact_fourier_l2,
            "normalized_l2_periodic_grid_crosscheck": grid_l2,
            "grid_crosscheck_minus_exact_fourier": grid_l2 - exact_fourier_l2,
            "exact_tail_squared": reference.tail_squared,
            "grid_points": int(exact_grid.size),
        },
        "interface_bounds": interface_bounds(projected, reference.omega),
    }
    if not all(
        (
            stats["interface_bounds"]["value_admissible_lt_0p4"],
            stats["interface_bounds"]["derivative_admissible_lt_0p5"],
        )
    ):
        raise RuntimeError("projected interface violated its analytical admissibility bounds")
    return projected, stats


def _archive_stage(
    output: Path,
    mode: str,
    seed: int,
    label: str,
    samples: CollectedSamples,
) -> dict:
    filename = f"{mode}-seed-{seed}-{label}.npz"
    path = output / filename
    np.savez_compressed(
        path,
        X=samples.positions,
        H=samples.values,
        node_counts=samples.node_counts,
        root_branched=samples.root_branched,
        terminal_counts=samples.terminal_counts,
        terminal_code_order=np.array(TERMINAL_CODE_ORDER),
        scheduled_roots=np.array(samples.scheduled_roots, dtype=np.int64),
        complete=np.array(samples.complete),
    )
    return {
        "path": filename,
        "sha256": _sha256(path),
        "completed_roots": int(samples.values.size),
        "scheduled_roots": samples.scheduled_roots,
        "complete": samples.complete,
    }


def _partial_cost_statistics(samples: CollectedSamples) -> dict:
    """Record expended work without treating a partial stage as an estimate."""
    return {
        "root_count": int(samples.values.size),
        "total_nodes": int(samples.node_counts.sum()),
        "root_branch_count": int(samples.root_branched.sum()),
        "terminal_code_order": list(TERMINAL_CODE_ORDER),
        "terminal_code_counts": samples.terminal_counts.tolist(),
        "sampling_seconds": samples.seconds,
    }


def _aggregate_work(rows: Sequence[dict]) -> dict:
    terminal_counts = np.zeros(6, dtype=np.int64)
    for row in rows:
        terminal_counts += np.asarray(
            row.get("terminal_code_counts", np.zeros(6)), dtype=np.int64
        )
    return {
        "roots_completed": sum(int(row.get("root_count", 0)) for row in rows),
        "total_nodes": sum(int(row.get("total_nodes", 0)) for row in rows),
        "root_branches": sum(int(row.get("root_branch_count", 0)) for row in rows),
        "terminal_code_order": list(TERMINAL_CODE_ORDER),
        "terminal_code_counts": terminal_counts.tolist(),
        "terminal_calls": int(terminal_counts.sum()),
    }


def _checkpoint_seed(
    output: Path,
    mode: str,
    seed: int,
    status: str,
    rows: list[dict],
    schedule: dict,
    started: float,
) -> None:
    """Persist completed stage diagnostics independently of the top-level manifest."""
    _json_write(
        output / f"{mode}-seed-{seed}-progress.json",
        {
            "schema_version": 1,
            "mode": mode,
            "seed": seed,
            "status": status,
            **schedule,
            "completed_entries": sum(bool(row["complete"]) for row in rows),
            "checkpointed_at_utc": _utc_now(),
            "elapsed_seconds": time.perf_counter() - started,
            "entries": rows,
        },
    )


def _exact_grid(reference: ReferenceData, count: int = GRID_POINTS) -> np.ndarray:
    grid = np.arange(count, dtype=float) * reference.period / count
    return np.asarray(jacobi_terminal(grid)[0], dtype=float)


def run_slab_seed(
    *,
    seed: int,
    n_roots: int,
    stages: int,
    batch_size: int,
    output: Path,
    reference: ReferenceData,
    sampler: Callable = raw_sample,
    oracle: Callable = jacobi_terminal,
    max_seconds: float = MAX_SECONDS,
    grid_points: int = GRID_POINTS,
) -> dict:
    """Run one continuation path; injectable sampler/oracle support correspondence tests."""
    if n_roots < 2 or stages < 1:
        raise ValueError("n_roots must be >= 2 and stages must be >= 1")
    output.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    exact_grid = _exact_grid(reference, grid_points)
    previous_coefficients = None
    stage_rows = []
    started = time.perf_counter()
    deadline = started + max_seconds if math.isfinite(max_seconds) else None
    status = "complete"
    for stage in range(1, stages + 1):
        if deadline is not None and time.perf_counter() >= deadline:
            status = "incomplete_time_cap_before_stage"
            break
        frozen_terminal = stage_terminal(
            stage,
            previous_coefficients,
            reference.omega,
            oracle=oracle,
        )
        positions = rng.uniform(0.0, reference.period, size=n_roots)
        samples = collect_samples(
            positions,
            SLAB_H,
            frozen_terminal,
            rng,
            sampler,
            batch_size,
            deadline,
            root_code=0,
        )
        archive = _archive_stage(output, "slab", seed, f"stage-{stage:03d}", samples)
        if not samples.complete:
            status = "incomplete_time_cap_during_stage"
            stage_rows.append(
                {
                    "stage": stage,
                    "elapsed_time": stage * SLAB_H,
                    "complete": False,
                    "raw_archive": archive,
                    **_partial_cost_statistics(samples),
                }
            )
            _checkpoint_seed(
                output,
                "slab",
                seed,
                status,
                stage_rows,
                {"scheduled_stages": stages, "n_roots_per_stage": n_roots, "slab_h": SLAB_H},
                started,
            )
            break
        previous_coefficients, stats = _stage_statistics(samples, reference, exact_grid)
        stage_rows.append(
            {
                "stage": stage,
                "elapsed_time": stage * SLAB_H,
                "terminal_source": "exact_jacobi" if stage == 1 else "frozen_previous_projected_coefficients",
                "complete": True,
                "raw_archive": archive,
                **stats,
            }
        )
        _checkpoint_seed(
            output,
            "slab",
            seed,
            "running" if stage < stages else "complete",
            stage_rows,
            {"scheduled_stages": stages, "n_roots_per_stage": n_roots, "slab_h": SLAB_H},
            started,
        )
    _checkpoint_seed(
        output,
        "slab",
        seed,
        status,
        stage_rows,
        {"scheduled_stages": stages, "n_roots_per_stage": n_roots, "slab_h": SLAB_H},
        started,
    )
    return {
        "seed": seed,
        "status": status,
        "scheduled_stages": stages,
        "completed_stages": sum(bool(row["complete"]) for row in stage_rows),
        "n_roots_per_stage": n_roots,
        "slab_h": SLAB_H,
        "measured_work": _aggregate_work(stage_rows),
        "total_seconds": time.perf_counter() - started,
        "stages": stage_rows,
    }


def run_majority_seed(
    *,
    seed: int,
    n_roots: int,
    horizons: Sequence[float],
    batch_size: int,
    output: Path,
    reference: ReferenceData,
    sampler: Callable = majority_sample,
    max_seconds: float = MAX_SECONDS,
    grid_points: int = GRID_POINTS,
) -> dict:
    """Run full-horizon bounded-majority coefficient observations."""
    if n_roots < 2:
        raise ValueError("n_roots must be >= 2")
    output.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    exact_grid = _exact_grid(reference, grid_points)
    rows = []
    started = time.perf_counter()
    deadline = started + max_seconds if math.isfinite(max_seconds) else None
    status = "complete"
    for horizon in horizons:
        horizon = float(horizon)
        if horizon <= 0.0 or not math.isfinite(horizon):
            raise ValueError("majority horizons must be finite and positive")
        if deadline is not None and time.perf_counter() >= deadline:
            status = "incomplete_time_cap_before_horizon"
            break
        positions = rng.uniform(0.0, reference.period, size=n_roots)
        samples = collect_samples(
            positions,
            horizon,
            lambda x: jacobi_terminal(x)[0],
            rng,
            sampler,
            batch_size,
            deadline,
            root_code=None,
        )
        horizon_label = str(horizon).replace(".", "p")
        archive = _archive_stage(output, "majority", seed, f"T-{horizon_label}", samples)
        if not samples.complete:
            status = "incomplete_time_cap_during_horizon"
            rows.append(
                {
                    "horizon": horizon,
                    "complete": False,
                    "raw_archive": archive,
                    **_partial_cost_statistics(samples),
                }
            )
            _checkpoint_seed(
                output,
                "majority",
                seed,
                status,
                rows,
                {
                    "scheduled_horizons": [float(value) for value in horizons],
                    "n_roots_per_horizon": n_roots,
                },
                started,
            )
            break
        _, stats = _stage_statistics(samples, reference, exact_grid)
        expected_nodes = (3.0 * math.exp(4.0 * horizon) - 1.0) / 2.0
        rows.append(
            {
                "horizon": horizon,
                "terminal_source": "exact_jacobi_full_horizon_comparator",
                "complete": True,
                "raw_archive": archive,
                "theoretical_expected_nodes_per_root": expected_nodes,
                **stats,
            }
        )
        _checkpoint_seed(
            output,
            "majority",
            seed,
            "running" if len(rows) < len(horizons) else "complete",
            rows,
            {
                "scheduled_horizons": [float(value) for value in horizons],
                "n_roots_per_horizon": n_roots,
            },
            started,
        )
    _checkpoint_seed(
        output,
        "majority",
        seed,
        status,
        rows,
        {
            "scheduled_horizons": [float(value) for value in horizons],
            "n_roots_per_horizon": n_roots,
        },
        started,
    )
    return {
        "seed": seed,
        "status": status,
        "scheduled_horizons": [float(value) for value in horizons],
        "completed_horizons": sum(bool(row["complete"]) for row in rows),
        "n_roots_per_horizon": n_roots,
        "measured_work": _aggregate_work(rows),
        "total_seconds": time.perf_counter() - started,
        "horizons": rows,
    }


def _provenance(mode: str, args: argparse.Namespace, reference: ReferenceData) -> dict:
    import scipy

    source_paths = [Path(__file__), PLAN, THEORY]
    if SAMPLER_SOURCE.exists():
        source_paths.append(SAMPLER_SOURCE)
    command = shlex.join((sys.executable, *sys.argv))
    return {
        "created_at_utc": _utc_now(),
        "mode": mode,
        "command": command,
        "configuration": {
            key: str(value) if isinstance(value, Path) else value
            for key, value in vars(args).items()
        },
        "seed_schedule": list(getattr(args, "seeds", ()) or ()),
        "git_revision": _git_revision(),
        "source_sha256": {
            str(path.relative_to(REPO)): _sha256(path) for path in source_paths
        },
        "environment": {
            "python_executable": sys.executable,
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "numpy_version": np.__version__,
            "scipy_version": scipy.__version__,
            "mpmath_version": mp.__version__,
        },
        "reference_checks": reference.record,
        "algorithm_contract": {
            "tree_cutoff": None,
            "tree_weight_clipping": False,
            "failed_root_deletion": False,
            "adaptive_sample_budget": False,
            "selected_structural_zero_short_circuit_allowed": True,
            "selected_label_probability_renormalized": False,
            "projection": "coordinatewise clipping of coefficient estimates",
            "projection_is_biased": True,
            "raw_local_trees_unbiased_conditional_on_interface": True,
        },
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="mode", required=True)

    reference = subparsers.add_parser("reference", help="run independent Jacobi checks")
    reference.add_argument("--output", type=Path, default=HERE / "artifacts" / "reference")

    slab = subparsers.add_parser("slab", help="run learned slab continuation")
    slab.add_argument("--output", type=Path, default=HERE / "artifacts" / "slab")
    slab.add_argument("--n", type=int, default=PRIMARY_N)
    slab.add_argument("--seeds", type=int, nargs="+", default=list(PRIMARY_SEEDS))
    slab.add_argument("--stages", type=int, default=PRIMARY_STAGES)
    slab.add_argument("--batch-size", type=int, default=RAW_BATCH_SIZE)
    slab.add_argument("--max-seconds", type=float, default=MAX_SECONDS)

    majority = subparsers.add_parser("majority", help="run full bounded-majority comparator")
    majority.add_argument("--output", type=Path, default=HERE / "artifacts" / "majority")
    majority.add_argument("--n", type=int, default=MAJORITY_N)
    majority.add_argument("--seeds", type=int, nargs="+", default=list(MAJORITY_SEEDS))
    majority.add_argument(
        "--horizons", type=float, nargs="+", default=list(MAJORITY_HORIZONS)
    )
    majority.add_argument("--batch-size", type=int, default=MAJORITY_BATCH_SIZE)
    majority.add_argument("--max-seconds", type=float, default=MAX_SECONDS)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.mode != "reference" and (
        not math.isfinite(args.max_seconds) or args.max_seconds <= 0.0
    ):
        raise ValueError("--max-seconds must be finite and positive")
    reference = compute_reference()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.mode == "reference":
        payload = {
            "schema_version": 1,
            "status": "complete",
            "provenance": _provenance(args.mode, args, reference),
        }
        _json_write(args.output / "results.json", payload)
        print(json.dumps({"status": "complete", "output": str(args.output / "results.json")}, indent=2))
        return 0

    run_started = time.perf_counter()
    runs = []
    for seed in args.seeds:
        remaining = args.max_seconds - (time.perf_counter() - run_started)
        if remaining <= 0.0:
            break
        if args.mode == "slab":
            row = run_slab_seed(
                seed=seed,
                n_roots=args.n,
                stages=args.stages,
                batch_size=args.batch_size,
                output=args.output,
                reference=reference,
                max_seconds=remaining,
            )
        else:
            row = run_majority_seed(
                seed=seed,
                n_roots=args.n,
                horizons=args.horizons,
                batch_size=args.batch_size,
                output=args.output,
                reference=reference,
                max_seconds=remaining,
            )
        runs.append(row)
        payload = {
            "schema_version": 1,
            "status": "complete" if len(runs) == len(args.seeds) and all(r["status"] == "complete" for r in runs) else "incomplete",
            "provenance": _provenance(args.mode, args, reference),
            "runs": runs,
        }
        _json_write(args.output / "results.json", payload)
        print(
            f"mode={args.mode} seed={seed} status={row['status']} "
            f"seconds={row['total_seconds']:.3f}",
            flush=True,
        )
        if row["status"] != "complete":
            break
    payload = {
        "schema_version": 1,
        "status": "complete" if len(runs) == len(args.seeds) and all(r["status"] == "complete" for r in runs) else "incomplete",
        "total_seconds": time.perf_counter() - run_started,
        "provenance": _provenance(args.mode, args, reference),
        "runs": runs,
    }
    _json_write(args.output / "results.json", payload)
    return 0 if payload["status"] == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
