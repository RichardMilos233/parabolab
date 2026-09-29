"""Frozen E5 cells, references, preflight, and gated execution harness.

The sampler in :mod:`smooth_field` receives only a known evaluator and an
opaque callback.  Synthetic direction formulas and high-precision analytic
references live in this outer harness and are never passed into sampler code.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import shutil
import sys
import time
import traceback
from typing import Any, Callable, Iterable

import mpmath as mp
import numpy as np

from budget import BudgetLedger, ORACLE_CAPS, canonical_json, sha256_path
from fixtures import (
    COVARIANCE_ATOL,
    COVARIANCE_RTOL,
    EXACT_ATOL,
    EXACT_RTOL,
    PARTIAL_ATOL,
    PARTIAL_RTOL,
    run_fixtures,
)
from smooth_field import (
    COEFFICIENT_COUNT,
    COEFFICIENT_LAYOUT,
    MAX_FREQUENCY,
    OutputFiniteError,
    PREFIX_LENGTHS,
    ProtocolAbort,
    SamplerSpec,
    make_generator,
    sample_field,
    stream_identifier,
)


MODULE_ROOT = Path(__file__).resolve().parent
RUN_ROOT = MODULE_ROOT.parents[1]
ARTIFACT_ROOT = RUN_ROOT / "artifacts" / "smooth-field-component"
PREFLIGHT_ROOT = ARTIFACT_ROOT / "preflight-v1"
PROTOCOL_PATH = RUN_ROOT / "02h-smooth-field-component-experiment-protocol.md"
T98_PATH = RUN_ROOT / "reviews" / "T98-smooth-field-protocol-independent-audit.md"
T98_ROOT_PATH = RUN_ROOT / "reviews" / "T98-root-correspondence.json"
ACCEPTED_04AA_PATH = RUN_ROOT / "04aa-polynomial-fields-and-linear-gaussian-preparation.md"
R21_PATH = RUN_ROOT / "reviews" / "R21-linear-tree-common-gaussian-candidate.md"
PROTOCOL_SHA256 = "1866585a86fcfceb0f9b05f632dae093d3c6e03f4ab005b4eae02fbfa5b27612"
T98_SHA256 = "4684093695d5c116355d95be79d1fc0701d79b3671b1de889f938eccacd3a227"
T98_ROOT_SHA256 = "cf5485f00bbd7ff0ea24465f85e6b5457acd54cdf952b8da7606b2f117586fe4"
ACCEPTED_04AA_SHA256 = "433c699d951c74fa6ba19166e159069130e1340a7a319aa0334b0ba4f8a1b8a1"
R21_SHA256 = "99f8a23c98332b6797ee1ecc9f0929d94950cd047acb17bcbea0df9052ff7461"

SEEDS = (2026092901, 2026092902, 2026092903)
PREFLIGHT_SAMPLE_INDICES = (0, 1, 2, 3)
REPLAY_SAMPLE_INDICES = tuple(range(8))
OFFICIAL_SAMPLES_PER_SEED_CELL = 4096
OFFICIAL_TIME_LIMIT_SECONDS = 1800.0
OFFICIAL_CHUNK_SIZE = 64
DELTA = 0.1
REFERENCE_DPS = 100
REFERENCE_LIBRARY = "mpmath"
REFERENCE_ROUNDING = "Python float conversion of a 100-decimal-digit mpmath mpf"
IMPLEMENTATION_SCHEMA_VERSION = "smooth-field-implementation-v1"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Cell:
    index: int
    kappa: float
    degree: int
    tau: float
    base: float
    derivative_order: int
    direction: str

    @property
    def branching(self) -> int:
        return self.degree

    @property
    def rate(self) -> float:
        return 2.0 if self.degree == 3 else 5.0

    @property
    def label(self) -> str:
        return (
            f"cell={self.index};D={self.degree};tau={self.tau:g};base={self.base:g};"
            f"j={self.derivative_order};direction={self.direction};kappa={self.kappa:g}"
        )

    def spec(self) -> SamplerSpec:
        return SamplerSpec(
            self.branching,
            self.rate,
            self.tau,
            self.kappa,
            self.derivative_order,
        )


def frozen_cells() -> tuple[Cell, ...]:
    configurations = (
        (3, 0.5, 0.0, 1, "cosine_mode_1"),
        (3, 0.5, 0.25, 1, "cosine_mode_1"),
        (3, 0.5, 0.25, 2, "constant"),
        (3, 0.5, 0.0, 3, "constant"),
        (5, 0.1, 0.25, 1, "cosine_mode_1"),
        (5, 0.1, 0.25, 2, "constant"),
    )
    cells: list[Cell] = []
    for kappa in (0.01, 0.1):
        for degree, tau, base, derivative_order, direction in configurations:
            cells.append(
                Cell(
                    len(cells),
                    kappa,
                    degree,
                    tau,
                    base,
                    derivative_order,
                    direction,
                )
            )
    return tuple(cells)


CELLS = frozen_cells()


def verify_frozen_sources() -> dict[str, str]:
    expected = {
        PROTOCOL_PATH: PROTOCOL_SHA256,
        T98_PATH: T98_SHA256,
        T98_ROOT_PATH: T98_ROOT_SHA256,
        ACCEPTED_04AA_PATH: ACCEPTED_04AA_SHA256,
        R21_PATH: R21_SHA256,
    }
    checked: dict[str, str] = {}
    for path, digest in expected.items():
        actual = sha256_path(path)
        if actual != digest:
            raise ProtocolAbort(f"frozen source hash mismatch: {path}: {actual} != {digest}")
        checked[str(path.relative_to(RUN_ROOT))] = actual
    return checked


def source_hashes() -> dict[str, str]:
    return {
        path.name: sha256_path(path)
        for path in sorted(MODULE_ROOT.glob("*.py"))
        if path.is_file()
    }


def environment_record() -> dict[str, Any]:
    config_lines: list[str] = []
    try:
        from contextlib import redirect_stdout
        from io import StringIO

        output = StringIO()
        with redirect_stdout(output):
            np.show_config()
        config_lines = output.getvalue().splitlines()
    except Exception as exc:  # environment evidence, not sampler logic
        config_lines = [f"np.show_config failed: {type(exc).__name__}: {exc}"]
    return {
        "python_executable": sys.executable,
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "numpy_version": np.__version__,
        "numpy_config": config_lines,
        "mpmath_version": mp.__version__,
        "float_info": {
            "mantissa_bits": sys.float_info.mant_dig,
            "max_exp": sys.float_info.max_exp,
            "radix": sys.float_info.radix,
        },
    }


def implementation_manifest() -> dict[str, Any]:
    return {
        "schema_version": IMPLEMENTATION_SCHEMA_VERSION,
        "created_utc": utc_now(),
        "status": "implementation_and_preflight_only; official_not_executed",
        "frozen_sources": verify_frozen_sources(),
        "source_hashes": source_hashes(),
        "environment": environment_record(),
        "cells": [asdict(cell) | {"label": cell.label} for cell in CELLS],
        "seeds": list(SEEDS),
        "stream_mapping": (
            "Generator(PCG64DXSM(SeedSequence([seed,cell_index,sample_index,tag])))"
        ),
        "tags": {"official_and_replay": 0, "preflight": 1},
        "rng_calls_in_order": [
            "one scalar Generator.exponential(scale=1/rate) per DFS-preorder segment",
            "one Generator.standard_normal(size=(segment_count,),dtype=float64) vector call",
            "one scalar Generator.random() for U",
            (
                "if n>=j, one Generator.choice(n,size=(j,),replace=False,shuffle=True) "
                "for the ordered distinct tuple"
            ),
        ],
        "tree_order": "root first DFS preorder; children pushed right-to-left and visited left-to-right",
        "zero_length_edge_policy": (
            "draw one binary64 standard normal for every segment, including zero-length segments; "
            "multiply by sqrt(kappa*length), yielding exact zero on a zero edge"
        ),
        "arithmetic_dtype": "numpy.float64 / Python binary64",
        "output": {
            "max_frequency": MAX_FREQUENCY,
            "shape": [COEFFICIENT_COUNT],
            "layout": COEFFICIENT_LAYOUT,
            "prefix_lengths": {str(key): value for key, value in PREFIX_LENGTHS.items()},
            "prefixes": "views/copies of the single N=64 output; no new sampler or query",
        },
        "schema": {
            "sample_arrays": "NumPy .npy float64, shape (129,) per preflight output",
            "official_arrays": "atomic .npy float64 chunks, shape (completed_in_chunk,129)",
            "metadata": "UTF-8 JSONL, one fsynced record per completed output",
            "failure": "JSON plus raw attempted .npy coefficients when OutputFiniteError supplies them",
        },
        "timer_boundaries": {
            "tree_generation": "complete clock-tree generation and persistent segment accounting",
            "gaussian_preparation": "work-charge plus edge-normal draw and common-component passes",
            "known_and_corner": "cached known-leaf evaluation and complete signed corner passes",
            "acquisition": "opaque callback loop, known cache lookup, and direction product",
            "output": "single full N=64 Fourier array construction",
            "prefix_extraction": "copy exact N=4,N=16,N=64 prefixes from the full array",
            "sample_after_tree": "all sample work after tree generation, before artifact serialization",
            "sample_including_tree": "tree_generation plus sample_after_tree",
            "array_serialization": (
                "atomic .npy write per preflight output; for official output, measured once per "
                "64-row chunk and stored in chunk_metadata.jsonl"
            ),
            "official_suite": (
                "wall clock begins after source/preflight acceptance gates and includes sampling, "
                "journal fsyncs, serialization, and metadata records"
            ),
        },
        "official_time_limit_seconds": OFFICIAL_TIME_LIMIT_SECONDS,
        "official_loop_order": "cell index, then listed seed, then sample index 0..4095",
        "official_chunk_size": OFFICIAL_CHUNK_SIZE,
        "preflight_schedule": {
            "primary_indices": list(PREFLIGHT_SAMPLE_INDICES),
            "repeat_indices": [0],
            "loop_order": "cell index, then listed seed, then primary indices; then repeats in same order",
            "maximum_opaque_calls": 300,
        },
        "reference": {
            "library": REFERENCE_LIBRARY,
            "decimal_precision": REFERENCE_DPS,
            "conversion": REFERENCE_ROUNDING,
            "not_interval_certified": True,
        },
        "tolerances": {
            "covariance_rtol": COVARIANCE_RTOL,
            "covariance_atol": COVARIANCE_ATOL,
            "partial_rtol": PARTIAL_RTOL,
            "partial_atol": PARTIAL_ATOL,
            "exact_rtol": EXACT_RTOL,
            "exact_atol": EXACT_ATOL,
            "preflight_replay": "bitwise equality of coefficients and deterministic metadata",
        },
        "hard_limits": {
            "oracle_calls": ORACLE_CAPS,
            "global_oracle_calls": 300000,
            "single_tree_segments": 100000,
            "global_generated_segments": 10000000,
        },
        "accounting": {
            "opaque": "persistent atomic capacity-check-and-charge fsynced before callback entry",
            "known_evaluator": (
                "all distinct binary64 positions in the deterministic known pass are persistently "
                "reserved before callback entry; a failure conservatively retains unused reservation"
            ),
            "hard_crash_segments": (
                "unresolved reserved block remains conservatively charged and blocks continuation"
            ),
            "failure_work_reservations": (
                "Gaussian, U, tuple, and known-evaluator scheduled work is precharged; after a "
                "failure these counters are conservative reservations and are not asserted to be "
                "exact realized-call counts. Exponential attempts are incremented before each draw, "
                "while generated segments remain the exact appended-node count."
            ),
            "all_versions": "one shared journal for preflight, official, replay, failures, and repeats",
        },
        "scope_exclusions": [
            "no official acquisition before root implementation/preflight acceptance",
            "no sparse D48 estimator",
            "no long-time recursion or PDE certificate",
            "no universal Hilbert moment or minimax theorem",
            "no finite-bit guarantee",
        ],
    }


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + f".tmp-{os.getpid()}-{time.time_ns()}")
    with temp.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, sort_keys=True, indent=2, allow_nan=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)
    directory_fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def atomic_npy(path: Path, array: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + f".tmp-{os.getpid()}-{time.time_ns()}")
    with temp.open("wb") as handle:
        np.save(handle, np.asarray(array, dtype=np.float64), allow_pickle=False)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)
    directory_fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def append_jsonl(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = (canonical_json(value) + "\n").encode()
    with path.open("ab", buffering=0) as handle:
        handle.write(line)
        os.fsync(handle.fileno())


def next_attempt_directory(root: Path, stem: str) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    indices: list[int] = []
    for path in root.glob(f"{stem}-*"):
        try:
            indices.append(int(path.name.rsplit("-", 1)[1]))
        except ValueError:
            continue
    directory = root / f"{stem}-{max(indices, default=0) + 1:04d}"
    directory.mkdir(parents=False, exist_ok=False)
    return directory


def snapshot_sources(destination: Path) -> dict[str, str]:
    destination.mkdir(parents=True, exist_ok=False)
    hashes: dict[str, str] = {}
    for source in sorted(MODULE_ROOT.glob("*.py")):
        target = destination / source.name
        shutil.copyfile(source, target)
        hashes[source.name] = sha256_path(target)
    atomic_json(destination / "source_hashes.json", hashes)
    return hashes


class ChargedOpaque:
    """Only acquisition boundary exposed to the core sampler."""

    def __init__(
        self,
        raw_callback: Callable[[float], float],
        ledger: BudgetLedger,
        phase: str,
        identifier: dict[str, Any],
    ):
        self.__raw_callback = raw_callback
        self.__ledger = ledger
        self.__phase = phase
        self.__identifier = identifier
        self.attempts = 0
        self.successes = 0

    def __call__(self, x: float) -> float:
        x = float(x)
        # The durable charge is complete before entering user callback code.
        self.__ledger.charge_oracle(self.__phase, self.__identifier, x.hex())
        self.attempts += 1
        value = float(self.__raw_callback(x))
        self.successes += 1
        return value


def cell_evaluators(cell: Cell) -> tuple[Callable[[float], float], Callable[[float], float]]:
    base = float(cell.base)

    def known(_x: float) -> float:
        return base

    if cell.direction == "constant":
        def raw_unknown(_x: float) -> float:
            return base + DELTA
    elif cell.direction == "cosine_mode_1":
        def raw_unknown(x: float) -> float:
            return base + DELTA * math.cos(2.0 * math.pi * x)
    else:
        raise ValueError(f"unknown direction {cell.direction!r}")
    return known, raw_unknown


def reference_for_cell(cell: Cell) -> tuple[mp.mpf, int, str]:
    mp.mp.dps = REFERENCE_DPS
    kappa = mp.mpf(str(cell.kappa))
    tau = mp.mpf(str(cell.tau))
    base = mp.mpf(str(cell.base))
    delta = mp.mpf("0.1")
    m = cell.degree - 1
    c_tau = mp.exp(m * tau) - 1
    denominator = 1 + c_tau * base**m
    if cell.derivative_order == 1:
        derivative = mp.exp(tau) * denominator ** (-1 - mp.mpf(1) / m)
        value = delta * derivative * mp.exp(-2 * mp.pi**2 * kappa * tau)
        return value, 1, (
            "delta*exp(tau)*(1+(exp((D-1)tau)-1)*base^(D-1))^(-1-1/(D-1))"
            "*exp(-2*pi^2*kappa*tau)"
        )
    if cell.derivative_order == 2:
        derivative = (
            -(m + 1)
            * mp.exp(tau)
            * c_tau
            * base ** (m - 1)
            * denominator ** (-2 - mp.mpf(1) / m)
        )
        return delta**2 * derivative, 0, "delta^2*phi_tau''(base)"
    if cell.degree == 3 and cell.derivative_order == 3 and cell.base == 0.0:
        value = -3 * delta**3 * mp.exp(tau) * (mp.exp(2 * tau) - 1)
        return value, 0, "-3*delta^3*exp(tau)*(exp(2*tau)-1)"
    raise ValueError(f"no frozen reference for cell {cell.index}")


def reference_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for cell in CELLS:
        value, coefficient_index, expression = reference_for_cell(cell)
        binary = float(value)
        target = np.zeros(COEFFICIENT_COUNT, dtype=np.float64)
        target[coefficient_index] = binary
        records.append(
            {
                "cell": asdict(cell),
                "label": cell.label,
                "expression": expression,
                "mpmath_decimal_dps": REFERENCE_DPS,
                "high_precision_decimal": mp.nstr(value, n=REFERENCE_DPS),
                "binary64": binary,
                "binary64_hex": binary.hex(),
                "nonzero_coefficient_index": coefficient_index,
                "nonzero_coefficient_name": (
                    "constant" if coefficient_index == 0 else "cosine_mode_1"
                ),
                "full_target_array_sha256": hashlib.sha256(target.tobytes()).hexdigest(),
            }
        )
    return records


def write_manifest_and_references() -> tuple[Path, Path]:
    PREFLIGHT_ROOT.mkdir(parents=True, exist_ok=True)
    manifest_path = PREFLIGHT_ROOT / "implementation_manifest.json"
    reference_path = PREFLIGHT_ROOT / "analytic_references.json"
    atomic_json(manifest_path, implementation_manifest())
    atomic_json(
        reference_path,
        {
            "library": REFERENCE_LIBRARY,
            "precision_decimal_digits": REFERENCE_DPS,
            "binary64_conversion": REFERENCE_ROUNDING,
            "certified_intervals": False,
            "coefficient_layout": COEFFICIENT_LAYOUT,
            "records": reference_records(),
        },
    )
    return manifest_path, reference_path


def deterministic_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    excluded = {"timers_seconds", "serialization_seconds", "array_path", "array_sha256"}
    return deepcopy({key: value for key, value in metadata.items() if key not in excluded})


def sample_once(
    *,
    cell: Cell,
    seed: int,
    sample_index: int,
    tag: int,
    phase: str,
    run_kind: str,
    ledger: BudgetLedger,
) -> tuple[np.ndarray, dict[str, Any]]:
    rng_identifier = stream_identifier(seed, cell.index, sample_index, tag)
    operation_identifier: dict[str, Any] = {
        "phase": phase,
        "run_kind": run_kind,
        "rng_stream_identifier": rng_identifier,
    }
    known, raw_unknown = cell_evaluators(cell)
    opaque = ChargedOpaque(raw_unknown, ledger, phase, operation_identifier)
    rng = make_generator(rng_identifier)
    result = sample_field(
        cell.spec(),
        rng,
        ledger,
        phase,
        operation_identifier,
        known,
        opaque,
    )
    if opaque.attempts != result.metadata["opaque_calls"]:
        raise ProtocolAbort("local opaque attempt count disagrees with sample metadata")
    if opaque.attempts > cell.derivative_order:
        raise ProtocolAbort("realized opaque calls exceed derivative order")
    result.metadata["rng_stream_identifier"] = rng_identifier
    result.metadata["cell"] = asdict(cell)
    result.metadata["cell_label"] = cell.label
    result.metadata["phase"] = phase
    result.metadata["run_kind"] = run_kind
    result.metadata["opaque_attempts"] = opaque.attempts
    result.metadata["opaque_successes"] = opaque.successes
    if result.coefficients.shape != (COEFFICIENT_COUNT,) or np.any(
        ~np.isfinite(result.coefficients)
    ):
        raise OutputFiniteError("completed sampler returned invalid full array", result.coefficients)
    return result.coefficients, result.metadata


def retain_failure(
    run_directory: Path,
    ledger: BudgetLedger,
    identifier: dict[str, Any],
    exc: BaseException,
) -> Path:
    failures = run_directory / "failures"
    failure_directory = next_attempt_directory(failures, "failure")
    raw_path: str | None = None
    if isinstance(exc, OutputFiniteError):
        raw_file = failure_directory / "raw_attempted_coefficients.npy"
        atomic_npy(raw_file, exc.coefficients)
        raw_path = str(raw_file.relative_to(run_directory))
    failure = {
        "utc": utc_now(),
        "identifier": identifier,
        "exception_type": type(exc).__name__,
        "exception_message": str(exc),
        "traceback": traceback.format_exc(),
        "raw_attempted_coefficients": raw_path,
        "budget_snapshot": ledger.snapshot(),
        "semantics": "incomplete/failed output; never replaced, redrawn, dropped, or zero-filled",
        "failure_counter_semantics": (
            "opaque calls and exponential attempts are charged before individual callback/draw "
            "entry; generated nodes are exact; Gaussian/U/tuple/known counters may include "
            "conservatively precharged scheduled work not reached after the failure"
        ),
    }
    atomic_json(failure_directory / "failure.json", failure)
    return failure_directory


def run_preflight() -> dict[str, Any]:
    verify_frozen_sources()
    manifest_path, reference_path = write_manifest_and_references()
    ledger = BudgetLedger(ARTIFACT_ROOT)
    ledger.assert_no_unresolved_reservations()
    before = ledger.snapshot()
    run_directory = next_attempt_directory(PREFLIGHT_ROOT / "runs", "preflight")
    source_snapshot_hashes = snapshot_sources(run_directory / "source_snapshot")
    atomic_json(
        run_directory / "start.json",
        {
            "utc": utc_now(),
            "phase": "preflight",
            "status": "started",
            "budget_before": before,
            "implementation_manifest_sha256": sha256_path(manifest_path),
            "analytic_references_sha256": sha256_path(reference_path),
            "source_snapshot_hashes": source_snapshot_hashes,
        },
    )
    records_path = run_directory / "sample_metadata.jsonl"
    primary: dict[tuple[int, int], tuple[np.ndarray, dict[str, Any]]] = {}
    completed = 0
    reproducibility_records: list[dict[str, Any]] = []
    current_identifier: dict[str, Any] = {"stage": "fixtures"}
    try:
        fixtures = run_fixtures(ledger)
        atomic_json(run_directory / "fixture_results.json", fixtures)
        for cell in CELLS:
            for seed in SEEDS:
                for sample_index in PREFLIGHT_SAMPLE_INDICES:
                    current_identifier = {
                        "stage": "primary",
                        "cell_index": cell.index,
                        "seed": seed,
                        "sample_index": sample_index,
                        "tag": 1,
                    }
                    coefficients, metadata = sample_once(
                        cell=cell,
                        seed=seed,
                        sample_index=sample_index,
                        tag=1,
                        phase="preflight",
                        run_kind="primary",
                        ledger=ledger,
                    )
                    serialization_start = time.perf_counter()
                    array_name = (
                        f"primary-cell-{cell.index:02d}-seed-{seed}-sample-{sample_index:04d}.npy"
                    )
                    atomic_npy(run_directory / "arrays" / array_name, coefficients)
                    metadata["serialization_seconds"] = time.perf_counter() - serialization_start
                    metadata["array_path"] = f"arrays/{array_name}"
                    metadata["array_sha256"] = sha256_path(run_directory / "arrays" / array_name)
                    append_jsonl(records_path, metadata)
                    ledger.record_sample_status("preflight", current_identifier, True)
                    completed += 1
                    if sample_index == 0:
                        primary[(cell.index, seed)] = (coefficients.copy(), metadata.copy())

        for cell in CELLS:
            for seed in SEEDS:
                sample_index = 0
                current_identifier = {
                    "stage": "reproducibility_repeat",
                    "cell_index": cell.index,
                    "seed": seed,
                    "sample_index": sample_index,
                    "tag": 1,
                }
                coefficients, metadata = sample_once(
                    cell=cell,
                    seed=seed,
                    sample_index=sample_index,
                    tag=1,
                    phase="preflight",
                    run_kind="reproducibility_repeat",
                    ledger=ledger,
                )
                original_coefficients, original_metadata = primary[(cell.index, seed)]
                arrays_equal = bool(np.array_equal(coefficients, original_coefficients))
                repeat_deterministic = deterministic_metadata(metadata)
                original_deterministic = deterministic_metadata(original_metadata)
                # run_kind and the operation identifier distinguish the audit invocation.
                for record in (repeat_deterministic, original_deterministic):
                    record.pop("run_kind", None)
                    identifier = record.get("identifier")
                    if isinstance(identifier, dict):
                        identifier.pop("run_kind", None)
                metadata_equal = repeat_deterministic == original_deterministic
                if not arrays_equal or not metadata_equal:
                    raise ProtocolAbort(
                        f"preflight reproducibility failed for cell={cell.index}, seed={seed}"
                    )
                serialization_start = time.perf_counter()
                array_name = f"repeat-cell-{cell.index:02d}-seed-{seed}-sample-0000.npy"
                atomic_npy(run_directory / "arrays" / array_name, coefficients)
                metadata["serialization_seconds"] = time.perf_counter() - serialization_start
                metadata["array_path"] = f"arrays/{array_name}"
                metadata["array_sha256"] = sha256_path(run_directory / "arrays" / array_name)
                append_jsonl(records_path, metadata)
                ledger.record_sample_status("preflight", current_identifier, True)
                completed += 1
                reproducibility_records.append(
                    {
                        "cell_index": cell.index,
                        "seed": seed,
                        "sample_index": 0,
                        "tag": 1,
                        "coefficients_bitwise_equal": arrays_equal,
                        "deterministic_metadata_equal": metadata_equal,
                    }
                )
        after = ledger.snapshot()
        opaque_delta = after["oracle_calls"]["preflight"] - before["oracle_calls"]["preflight"]
        if opaque_delta > 300 or opaque_delta > ORACLE_CAPS["preflight"]:
            raise ProtocolAbort(f"preflight opaque-call count {opaque_delta} exceeded frozen bound")
        if completed != 180:
            raise ProtocolAbort(f"preflight completed {completed} outputs rather than 180")
        result = {
            "utc": utc_now(),
            "status": "passed_implementation_preflight; official_not_executed",
            "run_directory": str(run_directory.relative_to(RUN_ROOT)),
            "completed_outputs": completed,
            "planned_outputs": 180,
            "primary_outputs": 144,
            "reproducibility_repeat_outputs": 36,
            "opaque_calls_this_attempt": opaque_delta,
            "opaque_call_maximum_this_attempt": 300,
            "fixture_all_passed": fixtures["all_passed"],
            "reproducibility_all_passed": all(
                row["coefficients_bitwise_equal"] and row["deterministic_metadata_equal"]
                for row in reproducibility_records
            ),
            "reproducibility_records": reproducibility_records,
            "budget_before": before,
            "budget_after": after,
            "implementation_manifest_sha256": sha256_path(manifest_path),
            "analytic_references_sha256": sha256_path(reference_path),
            "sample_metadata_sha256": sha256_path(records_path),
            "source_snapshot_hashes": source_snapshot_hashes,
            "claims": [
                "bounded deterministic fixtures and preflight only",
                "no official tag-0 acquisition was executed",
                "no statistical or PDE theorem follows from this preflight",
            ],
        }
        atomic_json(run_directory / "preflight_result.json", result)
        atomic_json(
            PREFLIGHT_ROOT / "latest_preflight.json",
            {
                "run_directory": str(run_directory.relative_to(PREFLIGHT_ROOT)),
                "preflight_result_sha256": sha256_path(run_directory / "preflight_result.json"),
                "status": result["status"],
            },
        )
        ledger.refresh_manifest()
        return result
    except BaseException as exc:
        try:
            ledger.record_sample_status("preflight", current_identifier, False)
        finally:
            failure_directory = retain_failure(run_directory, ledger, current_identifier, exc)
            atomic_json(
                run_directory / "preflight_result.json",
                {
                    "utc": utc_now(),
                    "status": "failed_incomplete",
                    "completed_outputs_before_failure": completed,
                    "failure_directory": str(failure_directory.relative_to(run_directory)),
                    "budget_before": before,
                    "budget_after": ledger.snapshot(),
                    "official_executed": False,
                },
            )
            ledger.refresh_manifest()
        raise


def verify_official_acceptance(acceptance_path: Path) -> dict[str, Any]:
    """Require a root-created source/preflight acceptance record, not user approval."""
    verify_frozen_sources()
    manifest_path = PREFLIGHT_ROOT / "implementation_manifest.json"
    latest_path = PREFLIGHT_ROOT / "latest_preflight.json"
    if not (manifest_path.exists() and latest_path.exists() and acceptance_path.exists()):
        raise ProtocolAbort("official gate files are incomplete")
    manifest = json.loads(manifest_path.read_text())
    if manifest["source_hashes"] != source_hashes():
        raise ProtocolAbort("current implementation bytes differ from preflight manifest")
    latest = json.loads(latest_path.read_text())
    if not str(latest.get("status", "")).startswith("passed_implementation_preflight"):
        raise ProtocolAbort("latest preflight is not passed")
    acceptance = json.loads(acceptance_path.read_text())
    required = {
        "verdict": "accepted_for_official",
        "protocol_sha256": PROTOCOL_SHA256,
        "implementation_manifest_sha256": sha256_path(manifest_path),
        "preflight_result_sha256": latest["preflight_result_sha256"],
    }
    for key, expected in required.items():
        if acceptance.get(key) != expected:
            raise ProtocolAbort(f"official acceptance field {key!r} does not match frozen evidence")
    return acceptance


def _save_partial_chunk(
    output_directory: Path,
    cell: Cell,
    seed: int,
    start_index: int,
    rows: list[np.ndarray],
    *,
    partial: bool,
) -> tuple[Path | None, float]:
    if not rows:
        return None, 0.0
    end_index = start_index + len(rows) - 1
    status = "partial" if partial else "complete"
    path = output_directory / "arrays" / (
        f"cell-{cell.index:02d}-seed-{seed}-samples-{start_index:04d}-{end_index:04d}-{status}.npy"
    )
    serialization_start = time.perf_counter()
    atomic_npy(path, np.stack(rows, axis=0))
    return path, time.perf_counter() - serialization_start


def _record_chunk(
    output_directory: Path,
    cell: Cell,
    seed: int,
    start_index: int,
    rows: list[np.ndarray],
    *,
    partial: bool,
) -> Path | None:
    path, serialization_seconds = _save_partial_chunk(
        output_directory,
        cell,
        seed,
        start_index,
        rows,
        partial=partial,
    )
    if path is None:
        return None
    append_jsonl(
        output_directory / "chunk_metadata.jsonl",
        {
            "cell_index": cell.index,
            "seed": seed,
            "start_sample_index": start_index,
            "end_sample_index": start_index + len(rows) - 1,
            "row_count": len(rows),
            "partial": partial,
            "array_path": str(path.relative_to(output_directory)),
            "array_sha256": sha256_path(path),
            "array_serialization_seconds": serialization_seconds,
        },
    )
    return path


def run_official(acceptance_path: Path, output_root: Path) -> dict[str, Any]:
    """Prepared official driver. T99 must not call this function."""
    acceptance = verify_official_acceptance(acceptance_path)
    ledger = BudgetLedger(ARTIFACT_ROOT)
    ledger.assert_no_unresolved_reservations()
    output_directory = next_attempt_directory(output_root, "official")
    snapshot_sources(output_directory / "source_snapshot")
    atomic_json(output_directory / "acceptance_snapshot.json", acceptance)
    records_path = output_directory / "sample_metadata.jsonl"
    before = ledger.snapshot()
    suite_start = time.perf_counter()
    completed = 0
    current_identifier: dict[str, Any] = {"stage": "not_started"}
    current_rows: list[np.ndarray] = []
    current_cell: Cell | None = None
    current_seed = 0
    current_chunk_start = 0
    try:
        for cell in CELLS:
            for seed in SEEDS:
                current_cell = cell
                current_seed = seed
                current_rows = []
                current_chunk_start = 0
                for sample_index in range(OFFICIAL_SAMPLES_PER_SEED_CELL):
                    if time.perf_counter() - suite_start >= OFFICIAL_TIME_LIMIT_SECONDS:
                        raise ProtocolAbort("official 30-minute wall-time cap reached before sample")
                    current_identifier = {
                        "stage": "official",
                        "cell_index": cell.index,
                        "seed": seed,
                        "sample_index": sample_index,
                        "tag": 0,
                    }
                    coefficients, metadata = sample_once(
                        cell=cell,
                        seed=seed,
                        sample_index=sample_index,
                        tag=0,
                        phase="official",
                        run_kind="official",
                        ledger=ledger,
                    )
                    current_rows.append(coefficients)
                    metadata["official_elapsed_seconds_before_record"] = (
                        time.perf_counter() - suite_start
                    )
                    append_jsonl(records_path, metadata)
                    ledger.record_sample_status("official", current_identifier, True)
                    completed += 1
                    if len(current_rows) == OFFICIAL_CHUNK_SIZE:
                        _record_chunk(
                            output_directory,
                            cell,
                            seed,
                            current_chunk_start,
                            current_rows,
                            partial=False,
                        )
                        current_rows = []
                        current_chunk_start = sample_index + 1
                    if time.perf_counter() - suite_start >= OFFICIAL_TIME_LIMIT_SECONDS:
                        raise ProtocolAbort("official 30-minute wall-time cap reached after output")
        after = ledger.snapshot()
        result = {
            "utc": utc_now(),
            "status": "complete",
            "completed_outputs": completed,
            "planned_outputs": len(CELLS) * len(SEEDS) * OFFICIAL_SAMPLES_PER_SEED_CELL,
            "official_elapsed_seconds": time.perf_counter() - suite_start,
            "budget_before": before,
            "budget_after": after,
        }
        atomic_json(output_directory / "official_result.json", result)
        ledger.refresh_manifest()
        return result
    except BaseException as exc:
        if current_cell is not None:
            _record_chunk(
                output_directory,
                current_cell,
                current_seed,
                current_chunk_start,
                current_rows,
                partial=True,
            )
        try:
            ledger.record_sample_status("official", current_identifier, False)
        finally:
            failure_directory = retain_failure(output_directory, ledger, current_identifier, exc)
            atomic_json(
                output_directory / "official_result.json",
                {
                    "utc": utc_now(),
                    "status": "failed_incomplete",
                    "completed_outputs_before_failure": completed,
                    "official_elapsed_seconds": time.perf_counter() - suite_start,
                    "failure_directory": str(failure_directory.relative_to(output_directory)),
                    "budget_before": before,
                    "budget_after": ledger.snapshot(),
                    "semantics": "not a complete unbiased suite; no redraw/drop/zero-fill",
                },
            )
            ledger.refresh_manifest()
        raise


def run_replay(acceptance_path: Path, official_directory: Path, output_root: Path) -> dict[str, Any]:
    """Replay precisely indices 0..7 on original tag-0 streams and charge anew."""
    verify_official_acceptance(acceptance_path)
    official_result_path = official_directory / "official_result.json"
    if not official_result_path.exists():
        raise ProtocolAbort("official result is unavailable for replay")
    official_result = json.loads(official_result_path.read_text())
    if official_result.get("status") != "complete":
        raise ProtocolAbort("incomplete official output cannot be replay-certified")
    ledger = BudgetLedger(ARTIFACT_ROOT)
    ledger.assert_no_unresolved_reservations()
    output_directory = next_attempt_directory(output_root, "replay")
    snapshot_sources(output_directory / "source_snapshot")
    before = ledger.snapshot()
    records: list[dict[str, Any]] = []
    current_identifier: dict[str, Any] = {"stage": "replay_not_started"}
    try:
        for cell in CELLS:
            for seed in SEEDS:
                official_chunk = official_directory / "arrays" / (
                    f"cell-{cell.index:02d}-seed-{seed}-samples-0000-0063-complete.npy"
                )
                original = np.load(official_chunk, allow_pickle=False)
                for sample_index in REPLAY_SAMPLE_INDICES:
                    current_identifier = {
                        "stage": "replay",
                        "cell_index": cell.index,
                        "seed": seed,
                        "sample_index": sample_index,
                        "tag": 0,
                    }
                    coefficients, metadata = sample_once(
                        cell=cell,
                        seed=seed,
                        sample_index=sample_index,
                        tag=0,
                        phase="replay",
                        run_kind="replay",
                        ledger=ledger,
                    )
                    matches = bool(np.array_equal(coefficients, original[sample_index]))
                    record = current_identifier | {"coefficients_bitwise_equal": matches}
                    append_jsonl(output_directory / "replay_records.jsonl", record)
                    if not matches:
                        atomic_npy(output_directory / "mismatch_replay.npy", coefficients)
                        atomic_npy(output_directory / "mismatch_original.npy", original[sample_index])
                        raise ProtocolAbort("replay coefficient mismatch")
                    ledger.record_sample_status("replay", current_identifier, True)
                    records.append(record)
        after = ledger.snapshot()
        result = {
            "utc": utc_now(),
            "status": "complete",
            "completed_outputs": len(records),
            "planned_outputs": 288,
            "all_bitwise_equal": all(row["coefficients_bitwise_equal"] for row in records),
            "budget_before": before,
            "budget_after": after,
        }
        atomic_json(output_directory / "replay_result.json", result)
        ledger.refresh_manifest()
        return result
    except BaseException as exc:
        try:
            ledger.record_sample_status("replay", current_identifier, False)
        finally:
            failure_directory = retain_failure(output_directory, ledger, current_identifier, exc)
            atomic_json(
                output_directory / "replay_result.json",
                {
                    "utc": utc_now(),
                    "status": "failed_incomplete",
                    "completed_outputs_before_failure": len(records),
                    "failure_directory": str(failure_directory.relative_to(output_directory)),
                    "budget_before": before,
                    "budget_after": ledger.snapshot(),
                },
            )
            ledger.refresh_manifest()
        raise
