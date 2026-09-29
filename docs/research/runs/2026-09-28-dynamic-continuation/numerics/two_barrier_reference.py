"""Independent cosine-Galerkin reference for the frozen two-barrier experiment.

This module solves, without importing sampler code,

    w_t = w_xx / 2 + 3 exp(-2t) w^2 - exp(-4t) w^3,
    w(0, x) = 3/8 - (1/8) cos(x)

on the 2*pi torus.  Its six Galerkin/Radau runs are empirical refinement
evidence, not rigorous enclosures or independent numerical certificates.
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
from typing import Callable, Mapping

import numpy as np
import scipy
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO = HERE.parents[4]
DEFAULT_OUTPUT = RUN_DIR / "artifacts" / "two-barrier" / "reference-v1"

PROTOCOL_SHA256 = "605eda24574bfb7e44dc997c185836d2a54311c18344e0be4c005674e00beda9"
TIMES = np.asarray((0.0, 0.25, 1.0, 4.0, 16.0, 64.0, 256.0), dtype=np.float64)
QUERIES = np.asarray((0.0, math.pi / 2.0, math.pi), dtype=np.float64)
MAX_MODES = (16, 32, 64)
GRID_SIZES = {16: 128, 32: 256, 64: 512}
TOLERANCES = {
    "loose": {"rtol": 1.0e-10, "atol": 1.0e-12},
    "strict": {"rtol": 1.0e-12, "atol": 1.0e-14},
}
PROJECTION_TIMES = (0.0, 0.25, 4.0)
CONSTANT_PROFILES = (0.5, 0.625, 0.75)
PROJECTION_THRESHOLD = 1.0e-10
CONSTANT_THRESHOLD = 1.0e-8
REFINEMENT_THRESHOLD = 1.0e-8
STRICT_KEY = "k64_strict"
COMPARATOR_KEY = "k16_loose"


@dataclass(frozen=True)
class CosineGalerkinSystem:
    """Projected scaled-PDE system for cosine modes zero through K."""

    max_mode: int
    n_grid: int
    nodes: np.ndarray
    basis: np.ndarray
    projector: np.ndarray
    diffusion: np.ndarray

    def values(self, coefficients: np.ndarray) -> np.ndarray:
        return self.basis @ coefficients

    def project(self, values: np.ndarray) -> np.ndarray:
        values = np.asarray(values, dtype=np.float64)
        if values.shape != (self.n_grid,):
            raise ValueError(f"expected grid values shape {(self.n_grid,)}, got {values.shape}")
        return self.projector @ values

    def nonlinear_projection(self, t: float, coefficients: np.ndarray) -> np.ndarray:
        values = self.values(coefficients)
        return self.projector @ (
            3.0 * math.exp(-2.0 * t) * values**2
            - math.exp(-4.0 * t) * values**3
        )

    def rhs(self, t: float, coefficients: np.ndarray) -> np.ndarray:
        return self.diffusion * coefficients + self.nonlinear_projection(t, coefficients)

    def jacobian(self, t: float, coefficients: np.ndarray) -> np.ndarray:
        values = self.values(coefficients)
        multiplier = (
            6.0 * math.exp(-2.0 * t) * values
            - 3.0 * math.exp(-4.0 * t) * values**2
        )
        return np.diag(self.diffusion) + self.projector @ (
            multiplier[:, None] * self.basis
        )


@dataclass(frozen=True)
class SolveRecord:
    key: str
    max_mode: int
    n_grid: int
    tolerance_name: str
    rtol: float
    atol: float
    times: np.ndarray
    coefficients: np.ndarray
    scaled_values: np.ndarray
    success: bool
    status: int
    message: str
    nfev: int
    njev: int
    nlu: int
    solve_seconds: float
    query_seconds: float


def make_system(max_mode: int) -> CosineGalerkinSystem:
    if max_mode not in GRID_SIZES:
        raise ValueError(f"unsupported frozen maximum mode: {max_mode}")
    n_grid = GRID_SIZES[max_mode]
    nodes = 2.0 * math.pi * np.arange(n_grid, dtype=np.float64) / n_grid
    modes = np.arange(max_mode + 1, dtype=np.float64)
    basis = np.cos(nodes[:, None] * modes[None, :])
    projector = basis.T * (2.0 / n_grid)
    projector[0, :] = 1.0 / n_grid
    diffusion = -0.5 * modes**2
    return CosineGalerkinSystem(
        max_mode=max_mode,
        n_grid=n_grid,
        nodes=nodes,
        basis=basis,
        projector=projector,
        diffusion=diffusion,
    )


def frozen_initial_coefficients(max_mode: int) -> np.ndarray:
    coefficients = np.zeros(max_mode + 1, dtype=np.float64)
    coefficients[0] = 3.0 / 8.0
    coefficients[1] = -1.0 / 8.0
    return coefficients


def all_mode_preflight_coefficients(max_mode: int) -> np.ndarray:
    modes = np.arange(max_mode + 1, dtype=np.float64)
    coefficients = (-1.0) ** modes / (8.0 * (modes + 1.0) ** 2)
    coefficients[0] = 3.0 / 8.0
    return coefficients


def evaluate_queries(coefficients: np.ndarray, queries: np.ndarray = QUERIES) -> np.ndarray:
    coefficients = np.asarray(coefficients, dtype=np.float64)
    modes = np.arange(coefficients.shape[-1], dtype=np.float64)
    query_basis = np.cos(np.asarray(queries, dtype=np.float64)[:, None] * modes[None, :])
    return coefficients @ query_basis.T


def _convolve_fourier(
    left: Mapping[int, complex], right: Mapping[int, complex]
) -> dict[int, complex]:
    result: dict[int, complex] = {}
    for left_mode, left_value in left.items():
        for right_mode, right_value in right.items():
            mode = left_mode + right_mode
            result[mode] = result.get(mode, 0.0j) + left_value * right_value
    return result


def _cosine_to_fourier(coefficients: np.ndarray) -> dict[int, complex]:
    result: dict[int, complex] = {0: complex(float(coefficients[0]))}
    for mode in range(1, coefficients.size):
        value = complex(float(coefficients[mode]) / 2.0)
        result[mode] = value
        result[-mode] = value
    return result


def _fourier_to_cosine(fourier: Mapping[int, complex], max_mode: int) -> np.ndarray:
    result = np.empty(max_mode + 1, dtype=np.float64)
    zero = fourier.get(0, 0.0j)
    if abs(zero.imag) > 5.0e-13:
        raise RuntimeError(f"unexpected imaginary constant coefficient {zero}")
    result[0] = zero.real
    for mode in range(1, max_mode + 1):
        value = fourier.get(mode, 0.0j) + fourier.get(-mode, 0.0j)
        if abs(value.imag) > 5.0e-13:
            raise RuntimeError(f"unexpected imaginary cosine coefficient {mode}: {value}")
        result[mode] = value.real
    return result


def convolution_nonlinear_projection(
    t: float, coefficients: np.ndarray
) -> np.ndarray:
    """Independent finite complex-Fourier convolution for the reaction term."""

    base = _cosine_to_fourier(np.asarray(coefficients, dtype=np.float64))
    square = _convolve_fourier(base, base)
    cube = _convolve_fourier(square, base)
    factor2 = 3.0 * math.exp(-2.0 * t)
    factor3 = -math.exp(-4.0 * t)
    modes = set(square) | set(cube)
    nonlinear = {
        mode: factor2 * square.get(mode, 0.0j) + factor3 * cube.get(mode, 0.0j)
        for mode in modes
    }
    return _fourier_to_cosine(nonlinear, coefficients.size - 1)


def convolution_jacobian(t: float, coefficients: np.ndarray) -> np.ndarray:
    """Independent convolution derivative, including the diffusion diagonal."""

    coefficients = np.asarray(coefficients, dtype=np.float64)
    max_mode = coefficients.size - 1
    base = _cosine_to_fourier(coefficients)
    square = _convolve_fourier(base, base)
    modes = set(base) | set(square)
    derivative_field = {
        mode: 6.0 * math.exp(-2.0 * t) * base.get(mode, 0.0j)
        - 3.0 * math.exp(-4.0 * t) * square.get(mode, 0.0j)
        for mode in modes
    }
    result = np.empty((max_mode + 1, max_mode + 1), dtype=np.float64)
    for column in range(max_mode + 1):
        if column == 0:
            basis_column = {0: 1.0 + 0.0j}
        else:
            basis_column = {column: 0.5 + 0.0j, -column: 0.5 + 0.0j}
        product = _convolve_fourier(derivative_field, basis_column)
        result[:, column] = _fourier_to_cosine(product, max_mode)
    mode_numbers = np.arange(max_mode + 1, dtype=np.float64)
    result[np.diag_indices(max_mode + 1)] += -0.5 * mode_numbers**2
    return result


def exact_scaled_constant(profile: float, times: np.ndarray = TIMES) -> np.ndarray:
    """Stable independent scalar Allen--Cahn target for exp(2t)(1-u(t))."""

    if not 0.0 < profile < 1.0:
        raise ValueError("constant profile must lie strictly between zero and one")
    times = np.asarray(times, dtype=np.float64)
    alpha = profile**-2 - 1.0
    q = alpha * np.exp(-2.0 * times)
    root = np.sqrt(1.0 + q)
    return alpha / (root * (root + 1.0))


def _solve(
    system: CosineGalerkinSystem,
    initial: np.ndarray,
    tolerance_name: str,
    clock: Callable[[], float] = time.perf_counter,
) -> SolveRecord:
    tolerance = TOLERANCES[tolerance_name]
    started = clock()
    solution = solve_ivp(
        system.rhs,
        (0.0, float(TIMES[-1])),
        np.asarray(initial, dtype=np.float64),
        method="Radau",
        t_eval=TIMES,
        jac=system.jacobian,
        rtol=tolerance["rtol"],
        atol=tolerance["atol"],
    )
    solve_seconds = clock() - started
    coefficients = np.asarray(solution.y.T, dtype=np.float64)
    query_started = clock()
    scaled_values = evaluate_queries(coefficients)
    query_seconds = clock() - query_started
    return SolveRecord(
        key=f"k{system.max_mode}_{tolerance_name}",
        max_mode=system.max_mode,
        n_grid=system.n_grid,
        tolerance_name=tolerance_name,
        rtol=float(tolerance["rtol"]),
        atol=float(tolerance["atol"]),
        times=np.asarray(solution.t, dtype=np.float64),
        coefficients=coefficients,
        scaled_values=scaled_values,
        success=bool(solution.success),
        status=int(solution.status),
        message=str(solution.message),
        nfev=int(solution.nfev),
        njev=int(solution.njev),
        nlu=int(solution.nlu),
        solve_seconds=float(solve_seconds),
        query_seconds=float(query_seconds),
    )


def _projection_preflight() -> tuple[dict[str, object], dict[str, np.ndarray]]:
    cases: list[dict[str, object]] = []
    arrays: dict[str, np.ndarray] = {}
    maximum_nonlinear = 0.0
    maximum_jacobian = 0.0
    for max_mode in MAX_MODES:
        system = make_system(max_mode)
        coefficients = all_mode_preflight_coefficients(max_mode)
        for time_value in PROJECTION_TIMES:
            label = f"k{max_mode}_t{str(time_value).replace('.', 'p')}"
            nonlinear_actual = system.nonlinear_projection(time_value, coefficients)
            nonlinear_expected = convolution_nonlinear_projection(time_value, coefficients)
            jacobian_actual = system.jacobian(time_value, coefficients)
            jacobian_expected = convolution_jacobian(time_value, coefficients)
            nonlinear_error = float(np.max(np.abs(nonlinear_actual - nonlinear_expected)))
            jacobian_error = float(np.max(np.abs(jacobian_actual - jacobian_expected)))
            maximum_nonlinear = max(maximum_nonlinear, nonlinear_error)
            maximum_jacobian = max(maximum_jacobian, jacobian_error)
            cases.append(
                {
                    "max_mode": max_mode,
                    "time": time_value,
                    "nonlinear_max_abs_difference": nonlinear_error,
                    "jacobian_max_abs_difference": jacobian_error,
                }
            )
            arrays[f"{label}_coefficients"] = coefficients
            arrays[f"{label}_nonlinear_quadrature"] = nonlinear_actual
            arrays[f"{label}_nonlinear_convolution"] = nonlinear_expected
            arrays[f"{label}_jacobian_quadrature"] = jacobian_actual
            arrays[f"{label}_jacobian_convolution"] = jacobian_expected
    passed = maximum_nonlinear <= PROJECTION_THRESHOLD and maximum_jacobian <= PROJECTION_THRESHOLD
    return (
        {
            "passed": passed,
            "threshold": PROJECTION_THRESHOLD,
            "maximum_nonlinear_projection_difference": maximum_nonlinear,
            "maximum_jacobian_entry_difference": maximum_jacobian,
            "cases": cases,
        },
        arrays,
    )


def _constant_preflight() -> tuple[dict[str, object], dict[str, np.ndarray]]:
    system = make_system(16)
    cases: list[dict[str, object]] = []
    arrays: dict[str, np.ndarray] = {}
    maximum = 0.0
    for profile in CONSTANT_PROFILES:
        initial = np.zeros(17, dtype=np.float64)
        initial[0] = 1.0 - profile
        record = _solve(system, initial, "strict")
        target = exact_scaled_constant(profile)
        expected_coefficients = np.zeros_like(record.coefficients)
        if record.coefficients.shape == (TIMES.size, 17):
            expected_coefficients[:, 0] = target
            discrepancy = float(np.max(np.abs(record.coefficients - expected_coefficients)))
        else:
            discrepancy = None
        if discrepancy is not None:
            maximum = max(maximum, discrepancy)
        label = str(profile).replace(".", "p")
        arrays[f"constant_{label}_times"] = record.times
        arrays[f"constant_{label}_coefficients"] = record.coefficients
        arrays[f"constant_{label}_target"] = target
        cases.append(
            {
                "profile": profile,
                "solver_success": record.success,
                "solver_status": record.status,
                "solver_message": record.message,
                "nfev": record.nfev,
                "njev": record.njev,
                "nlu": record.nlu,
                "solve_seconds": record.solve_seconds,
                "max_scaled_coefficient_difference": discrepancy,
            }
        )
    passed = (
        all(bool(case["solver_success"]) for case in cases)
        and all(case["max_scaled_coefficient_difference"] is not None for case in cases)
        and maximum <= CONSTANT_THRESHOLD
    )
    return (
        {
            "passed": passed,
            "threshold": CONSTANT_THRESHOLD,
            "maximum_scaled_difference": maximum,
            "system": {"max_mode": 16, "n_grid": 128, "tolerance": "strict"},
            "cases": cases,
        },
        arrays,
    )


def run_preflight() -> tuple[dict[str, object], dict[str, np.ndarray]]:
    started = time.perf_counter()
    projection, projection_arrays = _projection_preflight()
    constants, constant_arrays = _constant_preflight()
    elapsed = time.perf_counter() - started
    return (
        {
            "passed": bool(projection["passed"] and constants["passed"]),
            "projection_and_jacobian": projection,
            "constant_profiles": constants,
            "elapsed_seconds": float(elapsed),
        },
        {**projection_arrays, **constant_arrays},
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _source_paths() -> dict[str, Path]:
    return {
        "numerics/two_barrier_reference.py": HERE / "two_barrier_reference.py",
        "numerics/test_two_barrier_reference.py": HERE / "test_two_barrier_reference.py",
        "02d-two-barrier-experiment-protocol.md": RUN_DIR / "02d-two-barrier-experiment-protocol.md",
        "04l-two-barrier-voting.md": RUN_DIR / "04l-two-barrier-voting.md",
        "06f-moving-barrier-lean.md": RUN_DIR / "06f-moving-barrier-lean.md",
        "reviews/T30-two-barrier-voting-audit.md": RUN_DIR / "reviews" / "T30-two-barrier-voting-audit.md",
        "reviews/T31-horizon-free-clock-audit.md": RUN_DIR / "reviews" / "T31-horizon-free-clock-audit.md",
        "reviews/T34-two-barrier-protocol-review.md": RUN_DIR / "reviews" / "T34-two-barrier-protocol-review.md",
        "reviews/T34b-protocol-freeze-check.md": RUN_DIR / "reviews" / "T34b-protocol-freeze-check.md",
        "formal/EstimatorIntegrity/MovingBarrierWidth.lean": REPO / "formal" / "EstimatorIntegrity" / "MovingBarrierWidth.lean",
    }


def _source_hashes() -> dict[str, str]:
    return {name: _sha256(path) for name, path in _source_paths().items()}


def _git_revision() -> str | None:
    result = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def _write_json_new(path: Path, value: object) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


def _write_npz_new(path: Path, **arrays: np.ndarray) -> None:
    with path.open("xb") as stream:
        np.savez_compressed(stream, **arrays)


def _manifest(output: Path, preparation_seconds: float) -> dict[str, object]:
    source_hashes = _source_hashes()
    if source_hashes["02d-two-barrier-experiment-protocol.md"] != PROTOCOL_SHA256:
        raise RuntimeError("frozen protocol hash mismatch")
    return {
        "schema_version": 1,
        "status": "prepared-before-deterministic-checks",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "artifact_directory": str(output.relative_to(REPO)),
        "git_revision": _git_revision(),
        "source_hashes_sha256": source_hashes,
        "environment": {
            "python_executable": sys.executable,
            "python_version": sys.version,
            "numpy_version": np.__version__,
            "scipy_version": scipy.__version__,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "byteorder": sys.byteorder,
            "float64_eps": float(np.finfo(np.float64).eps),
        },
        "pde": {
            "equation": "w_t = 0.5*w_xx + 3*exp(-2*t)*w^2 - exp(-4*t)*w^3",
            "initial_condition": "w(0,x) = 3/8 - (1/8)*cos(x)",
            "domain": "2*pi periodic torus",
            "coefficient_representation": "w = a_0 + sum_{k=1}^K a_k cos(k*x)",
        },
        "cases": {
            "times": TIMES.tolist(),
            "queries": QUERIES.tolist(),
            "maximum_modes": list(MAX_MODES),
            "quadrature_grid_sizes": {str(k): GRID_SIZES[k] for k in MAX_MODES},
            "quadrature_nodes": "2*pi*j/J for j=0,...,J-1",
            "projection_normalization": "a_0=mean; a_k=2*mean(f*cos(k*x)) for k>0",
            "all_mode_vector": "c_0=3/8; c_k=(-1)^k/(8*(k+1)^2), k=1,...,K",
            "projection_times": list(PROJECTION_TIMES),
            "constant_profiles": list(CONSTANT_PROFILES),
        },
        "solver": {
            "method": "scipy.integrate.solve_ivp Radau",
            "analytic_projected_jacobian": True,
            "single_solve_interval": [0.0, 256.0],
            "single_solve_evaluation_times": TIMES.tolist(),
            "tolerances": TOLERANCES,
            "run_order": [f"k{k}_{tol}" for k in MAX_MODES for tol in TOLERANCES],
            "strict_reference_key": STRICT_KEY,
            "predesignated_comparator_key": COMPARATOR_KEY,
        },
        "gates": {
            "projection_and_jacobian_max_abs_difference": PROJECTION_THRESHOLD,
            "constant_profile_max_scaled_difference": CONSTANT_THRESHOLD,
            "refinement_max_21_query_difference": REFINEMENT_THRESHOLD,
            "all_six_solver_runs_must_succeed": True,
        },
        "output_contract": {
            "reference.npz": {
                "times": [7],
                "queries": [3],
                "scaled_values": [7, 3],
                "producer": STRICT_KEY,
            },
            "refinement_k{K}_{tolerance}.npz": {
                "times": [7],
                "queries": [3],
                "coefficients": "[7,K+1]",
                "scaled_values": [7, 3],
            },
            "reference_summary.json": "self-contained gates, solver diagnostics, timings, and schema",
        },
        "interpretation": {
            "classification": "empirical convergence of six refinements of one method",
            "rigorous_enclosure": False,
            "independent_certificate_count": 0,
            "sampler_imports": False,
        },
        "manifest_preparation_seconds": preparation_seconds,
    }


def prepare_manifest(output: Path) -> None:
    started = time.perf_counter()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing artifact directory: {output}")
    output.mkdir(parents=True, exist_ok=False)
    manifest = _manifest(output, time.perf_counter() - started)
    _write_json_new(output / "execution_manifest.json", manifest)
    print(json.dumps({"status": "prepared", "output": str(output), "manifest": "execution_manifest.json"}))


def _verify_manifest(output: Path) -> dict[str, object]:
    path = output / "execution_manifest.json"
    if not path.is_file():
        raise FileNotFoundError("execution manifest must be prepared before checks")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    current = _source_hashes()
    if current != manifest["source_hashes_sha256"]:
        mismatches = {
            name: {"frozen": manifest["source_hashes_sha256"].get(name), "current": value}
            for name, value in current.items()
            if manifest["source_hashes_sha256"].get(name) != value
        }
        raise RuntimeError(f"source changed after manifest freeze: {mismatches}")
    return manifest


def _record_metadata(record: SolveRecord) -> dict[str, object]:
    return {
        "key": record.key,
        "max_mode": record.max_mode,
        "retained_mode_count": record.max_mode + 1,
        "n_grid": record.n_grid,
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
        "query_seconds": record.query_seconds,
        "returned_time_count": int(record.times.size),
        "coefficient_shape": list(record.coefficients.shape),
        "scaled_values_shape": list(record.scaled_values.shape),
        "output_file": f"refinement_{record.key}.npz",
    }


def run_reference(output: Path) -> int:
    run_started = time.perf_counter()
    manifest = _verify_manifest(output)
    protected = [
        "preflight.json",
        "preflight_arrays.npz",
        "reference.npz",
        "reference_summary.json",
        "failure.json",
    ]
    if any((output / name).exists() for name in protected):
        raise FileExistsError("refusing to overwrite an attempted or completed reference run")

    io_seconds = 0.0
    preflight, preflight_arrays = run_preflight()
    io_started = time.perf_counter()
    _write_npz_new(output / "preflight_arrays.npz", **preflight_arrays)
    _write_json_new(output / "preflight.json", preflight)
    io_seconds += time.perf_counter() - io_started
    if not preflight["passed"]:
        failure = {
            "status": "FAIL",
            "stage": "deterministic_preflight",
            "preflight": preflight,
            "manifest_sha256": _sha256(output / "execution_manifest.json"),
        }
        _write_json_new(output / "failure.json", failure)
        print(json.dumps(failure, allow_nan=False))
        return 2

    records: dict[str, SolveRecord] = {}
    for max_mode in MAX_MODES:
        system = make_system(max_mode)
        initial = frozen_initial_coefficients(max_mode)
        for tolerance_name in TOLERANCES:
            record = _solve(system, initial, tolerance_name)
            records[record.key] = record
            io_started = time.perf_counter()
            _write_npz_new(
                output / f"refinement_{record.key}.npz",
                times=record.times,
                queries=QUERIES,
                coefficients=record.coefficients,
                scaled_values=record.scaled_values,
            )
            io_seconds += time.perf_counter() - io_started

    strict = records[STRICT_KEY]
    all_expected_shapes = all(
        record.times.shape == TIMES.shape
        and record.coefficients.shape == (TIMES.size, record.max_mode + 1)
        and record.scaled_values.shape == (TIMES.size, QUERIES.size)
        for record in records.values()
    )
    solver_success = all(record.success for record in records.values()) and all_expected_shapes
    discrepancies: dict[str, float | None] = {}
    for key, record in records.items():
        if record.scaled_values.shape == strict.scaled_values.shape:
            discrepancies[key] = float(np.max(np.abs(record.scaled_values - strict.scaled_values)))
        else:
            discrepancies[key] = None
    finite_discrepancies = [value for value in discrepancies.values() if value is not None]
    maximum_discrepancy = max(finite_discrepancies) if finite_discrepancies else math.inf
    refinement_passed = (
        len(finite_discrepancies) == len(records)
        and maximum_discrepancy < REFINEMENT_THRESHOLD
    )
    gate_passed = bool(preflight["passed"] and solver_success and refinement_passed)

    io_started = time.perf_counter()
    _write_npz_new(
        output / "reference.npz",
        times=TIMES,
        queries=QUERIES,
        scaled_values=strict.scaled_values,
    )
    io_seconds += time.perf_counter() - io_started

    refinements = []
    for key in [f"k{k}_{tol}" for k in MAX_MODES for tol in TOLERANCES]:
        metadata = _record_metadata(records[key])
        metadata["max_21_query_difference_from_strict"] = discrepancies[key]
        metadata["passes_refinement_threshold"] = bool(
            discrepancies[key] is not None and discrepancies[key] < REFINEMENT_THRESHOLD
        )
        refinements.append(metadata)

    solve_sum = float(sum(record.solve_seconds for record in records.values()))
    query_sum = float(sum(record.query_seconds for record in records.values()))
    comparator = records[COMPARATOR_KEY]
    summary = {
        "schema_version": 1,
        "status": "PASS" if gate_passed else "FAIL",
        "classification": "empirical convergence of six Galerkin/Radau refinements of one method",
        "rigorous_enclosure": False,
        "independent_numerical_certificates": False,
        "manifest_file": "execution_manifest.json",
        "manifest_sha256": _sha256(output / "execution_manifest.json"),
        "source_hashes_sha256": manifest["source_hashes_sha256"],
        "reference": {
            "producer_key": STRICT_KEY,
            "file": "reference.npz",
            "times_shape": [7],
            "queries_shape": [3],
            "scaled_values_shape": [7, 3],
            "dtype": "float64",
            "times": TIMES.tolist(),
            "queries": QUERIES.tolist(),
            "scaled_values": strict.scaled_values.tolist(),
        },
        "gates": {
            "passed": gate_passed,
            "preflight_passed": bool(preflight["passed"]),
            "all_six_solver_runs_succeeded": solver_success,
            "all_output_shapes_match": all_expected_shapes,
            "refinement_threshold": REFINEMENT_THRESHOLD,
            "maximum_21_query_difference_from_strict": maximum_discrepancy,
            "refinement_passed": refinement_passed,
            "per_run_21_query_difference": discrepancies,
        },
        "preflight": preflight,
        "refinements": refinements,
        "predesignated_comparator": {
            "key": COMPARATOR_KEY,
            "eligible": bool(
                comparator.success
                and discrepancies[COMPARATOR_KEY] is not None
                and discrepancies[COMPARATOR_KEY] < REFINEMENT_THRESHOLD
            ),
            "one_solve_seconds": comparator.solve_seconds,
            "all_21_query_evaluations_seconds": comparator.query_seconds,
            "solve_plus_all_queries_seconds": comparator.solve_seconds + comparator.query_seconds,
            "max_21_query_difference_from_strict": discrepancies[COMPARATOR_KEY],
        },
        "timings_seconds": {
            "preflight": preflight["elapsed_seconds"],
            "six_run_solve_sum": solve_sum,
            "six_run_query_evaluation_sum": query_sum,
            "six_run_solve_plus_query_sum": solve_sum + query_sum,
            "artifact_io_before_summary": io_seconds,
            "validation_wall_before_summary": time.perf_counter() - run_started,
            "comparator_solve_plus_all_queries": comparator.solve_seconds + comparator.query_seconds,
        },
        "artifact_schema": {
            "reference.npz": {
                "times": [7],
                "queries": [3],
                "scaled_values": [7, 3],
            },
            "refinement_k{K}_{tolerance}.npz": {
                "times": [7],
                "queries": [3],
                "coefficients": "[7,K+1]",
                "scaled_values": [7, 3],
            },
            "preflight_arrays.npz": "all projection/Jacobian pairs and constant-profile coefficient traces",
        },
        "limitations": [
            "The six runs are refinements of one Galerkin/Radau method.",
            "The discrepancy gate is not a rigorous error enclosure.",
            "No sampler helper or stochastic implementation is imported.",
            "The fixed deterministic comparator is not an equal-accuracy optimization.",
        ],
    }
    _write_json_new(output / "reference_summary.json", summary)
    print(
        json.dumps(
            {
                "status": summary["status"],
                "maximum_21_query_difference_from_strict": maximum_discrepancy,
                "comparator_seconds": summary["predesignated_comparator"]["solve_plus_all_queries_seconds"],
                "output": str(output),
            },
            allow_nan=False,
        )
    )
    return 0 if gate_passed else 3


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    output = args.output.resolve()
    if args.action == "prepare":
        prepare_manifest(output)
        return 0
    return run_reference(output)


if __name__ == "__main__":
    raise SystemExit(main())
