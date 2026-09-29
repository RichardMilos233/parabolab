"""Independent odd-sine Galerkin reference for the dynamic continuation run.

This module deliberately imports no production driver, sampler, or terminal
implementation.  It computes a floating-point reference for

    u_t = u_xx / 2 + u - u^3,    u(0, x) = 0.9 g(x),

where g is the stationary Jacobi profile specified by the frozen protocol.
The result is validation evidence, not a rigorous discretization enclosure.
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
import subprocess
import sys
import time
from typing import Callable

import numpy as np
import scipy
from scipy import special
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO = HERE.parents[4]

ELLIPTIC_M = 0.05
AMPLITUDE = math.sqrt(2.0 / 21.0)
KAPPA = math.sqrt(40.0 / 21.0)
PERIOD = 4.0 * float(special.ellipk(ELLIPTIC_M)) / KAPPA
OMEGA = 2.0 * math.pi / PERIOD
TIMES = np.arange(201, dtype=np.float64) * 0.08
MAX_MODES = (15, 31, 63)
QUADRATURE_SIZES = {15: 128, 31: 256, 63: 512}
COMPARISON_GRID_SIZE = 16_384
TOLERANCES = {
    "default": {"rtol": 1.0e-12, "atol": 1.0e-14},
    "strict": {"rtol": 2.0e-13, "atol": 2.0e-15},
}
ACCEPTANCE_TOLERANCE = 1.0e-9


@dataclass(frozen=True)
class GalerkinSystem:
    """Precomputed matrices for one odd-sine Galerkin truncation."""

    max_mode: int
    n_grid: int
    modes: np.ndarray
    basis: np.ndarray
    linear_rates: np.ndarray

    def cubic_coefficients(self, coefficients: np.ndarray) -> np.ndarray:
        values = self.basis @ coefficients
        return (self.basis.T @ (values * values * values)) / self.n_grid

    def rhs(self, _time: float, coefficients: np.ndarray) -> np.ndarray:
        return self.linear_rates * coefficients - self.cubic_coefficients(coefficients)


@dataclass(frozen=True)
class SolveRecord:
    key: str
    max_mode: int
    n_grid: int
    tolerance_name: str
    rtol: float
    atol: float
    coefficients: np.ndarray
    success: bool
    status: int
    message: str
    nfev: int
    njev: int
    nlu: int
    solve_seconds: float


def odd_modes(max_mode: int) -> np.ndarray:
    if max_mode < 1 or max_mode % 2 == 0:
        raise ValueError("max_mode must be a positive odd integer")
    return np.arange(1, max_mode + 1, 2, dtype=np.int64)


def periodic_grid(size: int) -> np.ndarray:
    if size <= 0:
        raise ValueError("grid size must be positive")
    return np.arange(size, dtype=np.float64) * (PERIOD / size)


def sine_basis(x: np.ndarray, modes: np.ndarray) -> np.ndarray:
    return math.sqrt(2.0) * np.sin(np.asarray(x)[:, None] * OMEGA * modes[None, :])


def jacobi_g(x: np.ndarray) -> np.ndarray:
    sn, _, _, _ = special.ellipj(KAPPA * np.asarray(x), ELLIPTIC_M)
    return AMPLITUDE * sn


def make_system(max_mode: int, n_grid: int | None = None) -> GalerkinSystem:
    modes = odd_modes(max_mode)
    if n_grid is None:
        n_grid = QUADRATURE_SIZES[max_mode]
    if n_grid <= 4 * max_mode:
        raise ValueError("cubic projection requires n_grid > 4 * max_mode")
    basis = sine_basis(periodic_grid(n_grid), modes)
    linear_rates = 1.0 - 0.5 * (modes * OMEGA) ** 2
    return GalerkinSystem(max_mode, n_grid, modes, basis, linear_rates)


def project(values: np.ndarray, basis: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=np.float64)
    if values.shape != (basis.shape[0],):
        raise ValueError("values and basis grid dimensions do not agree")
    return (basis.T @ values) / basis.shape[0]


def comparison_data() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = periodic_grid(COMPARISON_GRID_SIZE)
    modes = odd_modes(63)
    basis = sine_basis(x, modes)
    return x, basis, jacobi_g(x)


def initial_coefficients(max_mode: int, basis_63: np.ndarray, g_values: np.ndarray) -> np.ndarray:
    count = odd_modes(max_mode).size
    return project(0.9 * g_values, basis_63[:, :count])


def solve_configuration(
    system: GalerkinSystem,
    initial: np.ndarray,
    tolerance_name: str,
    clock: Callable[[], float] = time.perf_counter,
) -> SolveRecord:
    tolerance = TOLERANCES[tolerance_name]
    started = clock()
    solution = solve_ivp(
        system.rhs,
        (float(TIMES[0]), float(TIMES[-1])),
        initial,
        method="DOP853",
        t_eval=TIMES,
        rtol=tolerance["rtol"],
        atol=tolerance["atol"],
    )
    elapsed = clock() - started
    coefficients = np.asarray(solution.y.T, dtype=np.float64)
    expected_shape = (TIMES.size, system.modes.size)
    if coefficients.shape != expected_shape:
        raise RuntimeError(
            f"solver returned shape {coefficients.shape}, expected {expected_shape}: "
            f"{solution.message}"
        )
    key = f"m{system.max_mode}_{tolerance_name}"
    return SolveRecord(
        key=key,
        max_mode=system.max_mode,
        n_grid=system.n_grid,
        tolerance_name=tolerance_name,
        rtol=tolerance["rtol"],
        atol=tolerance["atol"],
        coefficients=coefficients,
        success=bool(solution.success),
        status=int(solution.status),
        message=str(solution.message),
        nfev=int(solution.nfev),
        njev=int(solution.njev),
        nlu=int(solution.nlu),
        solve_seconds=float(elapsed),
    )


def pad_coefficients(coefficients: np.ndarray, width: int = 32) -> np.ndarray:
    if coefficients.ndim != 2 or coefficients.shape[1] > width:
        raise ValueError("invalid coefficient array for padding")
    result = np.zeros((coefficients.shape[0], width), dtype=np.float64)
    result[:, : coefficients.shape[1]] = coefficients
    return result


def normalized_l2_per_time(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    """Coefficient-space normalized L2 difference in an orthonormal basis."""

    return np.linalg.norm(left - right, axis=1)


def physical_l2_per_time(
    left: np.ndarray, right: np.ndarray, comparison_basis: np.ndarray
) -> np.ndarray:
    difference = (left - right) @ comparison_basis.T
    return np.sqrt(np.mean(difference * difference, axis=1))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _git_revision() -> str | None:
    result = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def _write_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _write_npz(path: Path, **arrays: np.ndarray) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("wb") as stream:
        np.savez_compressed(stream, **arrays)
    os.replace(temporary, path)


def _source_hashes() -> dict[str, str]:
    sources = {
        "reference.py": HERE / "reference.py",
        "test_reference.py": HERE / "test_reference.py",
        "02-plan.md": RUN_DIR / "02-plan.md",
        "04-theory.md": RUN_DIR / "04-theory.md",
        "06-lean.md": RUN_DIR / "06-lean.md",
        "lean/build.log": RUN_DIR / "lean" / "build.log",
        "lean/axioms.log": RUN_DIR / "lean" / "axioms.log",
    }
    return {name: _sha256(path) for name, path in sources.items()}


def _record_dict(record: SolveRecord) -> dict[str, object]:
    return {
        "key": record.key,
        "max_mode": record.max_mode,
        "retained_mode_count": int(record.coefficients.shape[1]),
        "quadrature_grid_size": record.n_grid,
        "quadrature_exactness_condition": bool(record.n_grid > 4 * record.max_mode),
        "tolerance_name": record.tolerance_name,
        "rtol": record.rtol,
        "atol": record.atol,
        "success": record.success,
        "status": record.status,
        "message": record.message,
        "nfev": record.nfev,
        "njev": record.njev,
        "nlu": record.nlu,
        "solve_seconds": record.solve_seconds,
        "output_shape": list(record.coefficients.shape),
        "all_finite": bool(np.isfinite(record.coefficients).all()),
    }


def run_reference(output_dir: Path) -> dict[str, object]:
    total_started = time.perf_counter()
    output_dir.mkdir(parents=True, exist_ok=True)

    setup_started = time.perf_counter()
    x_compare, basis_compare, g_compare = comparison_data()
    systems = {max_mode: make_system(max_mode) for max_mode in MAX_MODES}
    initials = {
        max_mode: initial_coefficients(max_mode, basis_compare, g_compare)
        for max_mode in MAX_MODES
    }
    setup_seconds = time.perf_counter() - setup_started

    records: dict[str, SolveRecord] = {}
    for tolerance_name in ("default", "strict"):
        for max_mode in MAX_MODES:
            record = solve_configuration(
                systems[max_mode], initials[max_mode], tolerance_name
            )
            records[record.key] = record
            if not record.success or not np.isfinite(record.coefficients).all():
                raise RuntimeError(f"failed reference solve {record.key}: {record.message}")

    padded = {key: pad_coefficients(record.coefficients) for key, record in records.items()}
    spatial_63_vs_31 = normalized_l2_per_time(
        padded["m63_strict"], padded["m31_strict"]
    )
    spatial_31_vs_15 = normalized_l2_per_time(
        padded["m31_strict"], padded["m15_strict"]
    )
    temporal_63 = normalized_l2_per_time(
        padded["m63_strict"], padded["m63_default"]
    )
    empirical_floor = np.maximum(spatial_63_vs_31, temporal_63)

    physical_spatial_63_vs_31 = physical_l2_per_time(
        padded["m63_strict"], padded["m31_strict"], basis_compare
    )
    physical_temporal_63 = physical_l2_per_time(
        padded["m63_strict"], padded["m63_default"], basis_compare
    )

    projection_tail: dict[str, dict[str, float]] = {}
    for max_mode in MAX_MODES:
        count = systems[max_mode].modes.size
        approximation = basis_compare[:, :count] @ initials[max_mode]
        error = 0.9 * g_compare - approximation
        projection_tail[str(max_mode)] = {
            "normalized_l2": float(np.sqrt(np.mean(error * error))),
            "max_absolute": float(np.max(np.abs(error))),
        }

    sn, _, _, _ = special.ellipj(KAPPA * x_compare, ELLIPTIC_M)
    g_xx = AMPLITUDE * KAPPA**2 * (
        -(1.0 + ELLIPTIC_M) * sn + 2.0 * ELLIPTIC_M * sn**3
    )
    physical_stationary_residual = 0.5 * g_xx + g_compare - g_compare**3
    stationary_diagnostics: dict[str, object] = {
        "physical_formula_normalized_l2": float(
            np.sqrt(np.mean(physical_stationary_residual**2))
        ),
        "physical_formula_max_absolute": float(
            np.max(np.abs(physical_stationary_residual))
        ),
        "galerkin_rhs_l2_by_max_mode": {},
    }
    for max_mode in MAX_MODES:
        count = systems[max_mode].modes.size
        projected_g = project(g_compare, basis_compare[:, :count])
        residual = systems[max_mode].rhs(0.0, projected_g)
        stationary_diagnostics["galerkin_rhs_l2_by_max_mode"][str(max_mode)] = float(
            np.linalg.norm(residual)
        )

    initial_rhs = systems[63].rhs(0.0, initials[63])
    identity_values = (0.9 - 0.9**3) * g_compare**3
    identity_projection = project(identity_values, basis_compare)
    identity_difference = initial_rhs - identity_projection
    initial_derivative_diagnostics = {
        "identity": "u_t(0) = (0.9 - 0.9^3) g^3",
        "coefficient_l2_difference": float(np.linalg.norm(identity_difference)),
        "coefficient_max_absolute_difference": float(
            np.max(np.abs(identity_difference))
        ),
        "physical_grid_l2_difference": float(
            np.sqrt(np.mean((basis_compare @ identity_difference) ** 2))
        ),
    }

    coefficient_vs_physical_checks = {
        "spatial_63_vs_31_max_absolute_disagreement": float(
            np.max(np.abs(spatial_63_vs_31 - physical_spatial_63_vs_31))
        ),
        "temporal_63_max_absolute_disagreement": float(
            np.max(np.abs(temporal_63 - physical_temporal_63))
        ),
    }

    convergence = {
        "normalized_l2_definition": "sqrt((1/L) integral_0^L |f|^2)",
        "comparison_grid_size": COMPARISON_GRID_SIZE,
        "spatial_63_strict_vs_31_strict_per_time": spatial_63_vs_31.tolist(),
        "spatial_31_strict_vs_15_strict_per_time": spatial_31_vs_15.tolist(),
        "temporal_63_strict_vs_default_per_time": temporal_63.tolist(),
        "empirical_reference_floor_per_time": empirical_floor.tolist(),
        "spatial_63_strict_vs_31_strict_max": float(np.max(spatial_63_vs_31)),
        "spatial_31_strict_vs_15_strict_max": float(np.max(spatial_31_vs_15)),
        "temporal_63_strict_vs_default_max": float(np.max(temporal_63)),
        "empirical_reference_floor_max": float(np.max(empirical_floor)),
        "acceptance_tolerance": ACCEPTANCE_TOLERANCE,
        "accepted": bool(
            np.max(spatial_63_vs_31) <= ACCEPTANCE_TOLERANCE
            and np.max(temporal_63) <= ACCEPTANCE_TOLERANCE
        ),
        "coefficient_vs_physical_grid_checks": coefficient_vs_physical_checks,
    }

    validation_coefficients = np.stack(
        [
            np.stack([padded[f"m{max_mode}_{tol}"] for max_mode in MAX_MODES])
            for tol in ("default", "strict")
        ]
    )
    finest = padded["m63_strict"]
    reference_npz = output_dir / "reference.npz"
    validation_npz = output_dir / "validation_runs.npz"
    _write_npz(
        reference_npz,
        times=TIMES,
        period=np.asarray(PERIOD),
        omega=np.asarray(OMEGA),
        odd_modes=odd_modes(63),
        coefficients=finest,
    )
    _write_npz(
        validation_npz,
        times=TIMES,
        max_modes=np.asarray(MAX_MODES, dtype=np.int64),
        tolerance_names=np.asarray(("default", "strict")),
        coefficients=validation_coefficients,
    )

    validation_seconds = time.perf_counter() - total_started
    finest_record = records["m63_strict"]
    metadata: dict[str, object] = {
        "schema_version": 1,
        "passed": convergence["accepted"],
        "acceptance": convergence["accepted"],
        "convergence_max": convergence["empirical_reference_floor_max"],
        "convergence_per_time": convergence["empirical_reference_floor_per_time"],
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "description": "Independent odd-sine Galerkin floating-point reference",
        "rigor_scope": (
            "Empirically converged deterministic reference; no rigorous PDE "
            "discretization or floating-point enclosure"
        ),
        "equation": "u_t = 0.5 u_xx + u - u^3",
        "initial_data": "0.9 * sqrt(2/21) * sn(sqrt(40/21) x | m=0.05)",
        "basis": "sqrt(2) sin(k omega x), positive odd k",
        "period": PERIOD,
        "omega": OMEGA,
        "times": {"count": int(TIMES.size), "step": 0.08, "final": 16.0},
        "method": "scipy.integrate.solve_ivp DOP853",
        "source_hashes_sha256": _source_hashes(),
        "artifact_hashes_sha256": {
            "reference.npz": _sha256(reference_npz),
            "validation_runs.npz": _sha256(validation_npz),
        },
        "git_revision": _git_revision(),
        "command": [sys.executable, *sys.argv],
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
            "thread_limits": {
                name: os.environ.get(name)
                for name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")
            },
        },
        "solver_runs": [_record_dict(records[key]) for key in sorted(records)],
        "initial_projection_tail": projection_tail,
        "stationary_g_residual": stationary_diagnostics,
        "initial_rhs_identity": initial_derivative_diagnostics,
        "convergence": convergence,
        "performance_costs": {
            "setup_seconds_before_solves": setup_seconds,
            "sum_of_six_solve_seconds": float(
                sum(record.solve_seconds for record in records.values())
            ),
            "total_reference_setup_and_six_validation_solves_seconds": float(
                validation_seconds
            ),
            "finest_reference_solve_seconds": finest_record.solve_seconds,
            "finest_reference_nfev": finest_record.nfev,
            "comparison_labels": {
                "total_reference_validation_cost": (
                    "setup, six complete validation solves, diagnostics, and NPZ serialization"
                ),
                "finest_reference_algorithm_cost": (
                    "one max-mode-63 strict DOP853 solve after shared setup"
                ),
            },
        },
        "artifacts": {
            "reference_npz": "reference.npz",
            "reference_npz_schema": {
                "times": [201],
                "period": [],
                "omega": [],
                "odd_modes": [32],
                "coefficients": [201, 32],
            },
            "validation_npz": "validation_runs.npz",
            "validation_coefficients_axes": [
                "tolerance(default,strict)",
                "max_mode(15,31,63)",
                "time",
                "zero_padded_odd_mode_index",
            ],
        },
    }
    _write_json(output_dir / "reference.json", metadata)
    return metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=RUN_DIR / "artifacts" / "reference",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metadata = run_reference(args.output_dir.resolve())
    summary = {
        "accepted": metadata["convergence"]["accepted"],
        "empirical_reference_floor_max": metadata["convergence"][
            "empirical_reference_floor_max"
        ],
        "total_validation_seconds": metadata["performance_costs"][
            "total_reference_setup_and_six_validation_solves_seconds"
        ],
        "finest_reference_solve_seconds": metadata["performance_costs"][
            "finest_reference_solve_seconds"
        ],
        "output_dir": str(args.output_dir.resolve()),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
