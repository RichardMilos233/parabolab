"""Frozen positive-class point-sampling experiment producer.

``prepare`` creates the immutable current-version manifest before any diagnostic oracle
observation. ``preflight`` performs exactly the bounded checks frozen in 02g.
``run`` exists for the later official execution, but requires a root clearance
record binding the source, manifest, and successful preflight hashes.

The sampling algorithm is intentionally restricted to the public interface
``(oracle, T, n, rng)``.  It has no profile, support, mass, or reference access.
"""

from __future__ import annotations

import argparse
import copy
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.metadata
import inspect
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback
from typing import Any, Callable

import mpmath as mp
import numpy as np


HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO = HERE.parents[4]
IMPLEMENTATION_PATH = Path(__file__).resolve()
ARTIFACT_VERSION = "v2"
ARTIFACT_ROOT = RUN_DIR / "artifacts" / "positive-query-sampling"
ARTIFACT_DIR = ARTIFACT_ROOT / ARTIFACT_VERSION
MANIFEST_PATH = ARTIFACT_DIR / "execution_manifest.json"
PREFLIGHT_LOG_PATH = ARTIFACT_DIR / "preflight.log"
PREFLIGHT_JOURNAL_PATH = ARTIFACT_DIR / "preflight_journal.jsonl"
PREFLIGHT_LEDGER_PATH = ARTIFACT_DIR / "preflight_activity.jsonl"
PREFLIGHT_RESULT_PATH = ARTIFACT_DIR / "preflight_result.json"
PREFLIGHT_FAILURE_PATH = ARTIFACT_DIR / "preflight_failure.json"
OFFICIAL_DIR = ARTIFACT_DIR / "official"

PROTOCOL_PATH = RUN_DIR / "02g-positive-query-sampling-protocol.md"
AUDIT_PATH = RUN_DIR / "reviews" / "T58-positive-sampling-protocol-audit.md"
INITIAL_HASHES_PATH = RUN_DIR / "initial-source-hashes.json"
SCALAR_INPUT_PATH = (
    RUN_DIR / "artifacts" / "query-information" / "checks-v1" / "scalar_checks.json"
)
V1_DIR = ARTIFACT_ROOT / "v1"
V1_ARCHIVED_SOURCE_PATH = V1_DIR / "source" / "positive_query_sampling.py"
V1_REPORT_PATH = RUN_DIR / "reviews" / "T63-positive-sampling-implementation.md"

HORIZONS = (12, 16, 20)
LEVELS = (0.0, 0.25, 1.0, 4.0)
SCHEDULES = (
    ("growing_0p125", 128),
    ("growing_0p5", 128),
    ("growing_2", 128),
    ("theorem_96", 8),
    ("fixed_51", 128),
)
OFFICIAL_SEEDS = (20260928, 20260929, 20260930)
DIAGNOSTIC_ENTROPY = 20260927
BATCH_SIZE = 131072
MAX_REPLICATE_QUERIES = 3_000_000
WHOLE_ACTIVITY_CAP = 500_000_000
EXPECTED_OFFICIAL_CELLS = 180
EXPECTED_OFFICIAL_OUTPUTS = 18_720
EXPECTED_OFFICIAL_CALLS = 336_883_488
EXPECTED_PREFLIGHT_CALLS = 655_633
EXPECTED_REPLAY_CALLS = 30_075_636

SCHEDULE_TABLE = {
    12: (51, 202, 807, 38_730, 51),
    16: (373, 1_491, 5_962, 286_172, 51),
    20: (2_754, 11_014, 44_053, 2_114_541, 51),
}

SHIFT = 17.0 / 20.0
SHIFT_FRACTION = Fraction(*SHIFT.as_integer_ratio())
PRIMARY_I = (
    "0.0070298584066096562392412705303539560761553994753572487961297388286445458695463593"
)
CROSSCHECK_I = (
    "0.007029858406609656239241270530353956076155399475357248796129738828644545869546359346285080438977033932"
)

FROZEN_INPUTS = (
    IMPLEMENTATION_PATH,
    PROTOCOL_PATH,
    AUDIT_PATH,
    RUN_DIR / "02f-positive-query-sampling-protocol-draft.md",
    RUN_DIR / "04q-matching-positive-query-complexity.md",
    RUN_DIR / "05h-positive-upper-bound-lean-contract.md",
    RUN_DIR / "06i-positive-sigmoid-lean.md",
    RUN_DIR / "06j-positive-sample-mean-lean.md",
    RUN_DIR / "reviews" / "T46-positive-class-upper-bound.md",
    RUN_DIR / "reviews" / "T48-matching-upper-bound-audit.md",
    RUN_DIR / "reviews" / "T51-root-correspondence.json",
    RUN_DIR / "reviews" / "T52-root-correspondence.json",
    REPO / "formal" / "EstimatorIntegrity" / "PositiveSigmoidRisk.lean",
    REPO / "formal" / "EstimatorIntegrity" / "PositiveSampleMean.lean",
    SCALAR_INPUT_PATH,
    INITIAL_HASHES_PATH,
    V1_ARCHIVED_SOURCE_PATH,
    V1_DIR / "execution_manifest.json",
    V1_DIR / "preflight_activity.jsonl",
    V1_DIR / "preflight_journal.jsonl",
    V1_DIR / "preflight_result.json",
    V1_DIR / "preflight.log",
    V1_REPORT_PATH,
)


class ProtocolFailure(RuntimeError):
    """A frozen protocol check failed."""


class SamplingFailure(RuntimeError):
    """An estimator batch failed after preserving its partial arithmetic."""

    def __init__(self, message: str, partial: dict[str, Any]) -> None:
        super().__init__(message)
        self.partial = partial


@dataclass(frozen=True)
class Estimate:
    sample_mean: float
    output: float
    positive_return_count: int
    observation_count: int
    batch_sums: tuple[float, ...]
    batch_counts: tuple[int, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return str(path.resolve().relative_to(REPO.resolve()))


def jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    if isinstance(value, np.generic):
        return value.item()
    return value


def write_json_new(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(jsonable(value), stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def append_json(stream: Any, value: Any) -> float:
    started = time.perf_counter()
    stream.write(json.dumps(jsonable(value), sort_keys=True, allow_nan=False) + "\n")
    stream.flush()
    os.fsync(stream.fileno())
    return time.perf_counter() - started


class DurableJsonl:
    """Append-only JSONL writer with measured serialization wall time."""

    def __init__(self, path: Path) -> None:
        self.stream = path.open("x", encoding="utf-8")
        self.serialization_elapsed_seconds = 0.0
        self.record_count = 0

    def append(self, value: Any) -> None:
        self.serialization_elapsed_seconds += append_json(self.stream, value)
        self.record_count += 1

    def close(self) -> None:
        if not self.stream.closed:
            self.stream.close()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProtocolFailure(message)


def mp_string(value: mp.mpf, digits: int = 100) -> str:
    return mp.nstr(value, n=digits, strip_zeros=False, min_fixed=-1000, max_fixed=1000)


def mp_from_float(value: float) -> mp.mpf:
    numerator, denominator = value.as_integer_ratio()
    return mp.mpf(numerator) / denominator


def float_record(value: float) -> dict[str, Any]:
    numerator, denominator = value.as_integer_ratio()
    return {
        "decimal": repr(value),
        "hex": value.hex(),
        "integer_ratio": [numerator, denominator],
    }


def git_text(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=REPO, check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def protected_hash_status() -> dict[str, Any]:
    expected = json.loads(INITIAL_HASHES_PATH.read_text(encoding="utf-8"))
    missing: list[str] = []
    mismatches: list[dict[str, str]] = []
    for name, expected_hash in expected.items():
        path = REPO / name
        if not path.is_file():
            missing.append(name)
            continue
        actual_hash = sha256(path)
        if actual_hash != expected_hash:
            mismatches.append(
                {"path": name, "expected": expected_hash, "actual": actual_hash}
            )
    return {
        "recorded_count": len(expected),
        "missing": missing,
        "mismatches": mismatches,
        "passed": len(expected) == 342 and not missing and not mismatches,
    }


def activity_ledger_record(path: Path) -> dict[str, Any]:
    total = 0
    entries = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        charge = int(row["point_calls"])
        require(charge >= 0, f"negative prior activity charge in {path}")
        total += charge
        entries += 1
        require(
            int(row["cumulative_point_calls"]) == total,
            f"noncumulative prior activity ledger {path}",
        )
    return {
        "path": relative(path),
        "sha256": sha256(path),
        "entries": entries,
        "charged_point_calls": total,
    }


def prior_activity_contract() -> dict[str, Any]:
    ledgers: list[dict[str, Any]] = []
    if ARTIFACT_ROOT.is_dir():
        for version_dir in sorted(ARTIFACT_ROOT.iterdir()):
            if not version_dir.is_dir() or version_dir.name == ARTIFACT_VERSION:
                continue
            for path in sorted(version_dir.rglob("*activity.jsonl")):
                ledgers.append(activity_ledger_record(path))
    return {
        "source": "all prior positive-query-sampling *activity.jsonl ledgers",
        "ledgers": ledgers,
        "charged_point_calls": sum(row["charged_point_calls"] for row in ledgers),
    }


def schedule_formula(name: str, horizon: int) -> mp.mpf:
    if name == "growing_0p125":
        return mp.mpf(1) / 8 * mp.exp(mp.mpf(horizon) / 2)
    if name == "growing_0p5":
        return mp.mpf(1) / 2 * mp.exp(mp.mpf(horizon) / 2)
    if name == "growing_2":
        return 2 * mp.exp(mp.mpf(horizon) / 2)
    if name == "theorem_96":
        return 96 * mp.exp(mp.mpf(horizon) / 2)
    if name == "fixed_51":
        return mp.mpf(1) / 8 * mp.exp(mp.mpf(12) / 2)
    raise ProtocolFailure(f"unknown schedule {name}")


def schedule_contract() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    official_calls = 0
    official_outputs = 0
    max_n = 0
    for horizon in HORIZONS:
        integers: list[int] = []
        formula_rows: list[dict[str, Any]] = []
        for (name, repetitions), frozen_n in zip(SCHEDULES, SCHEDULE_TABLE[horizon]):
            evaluated = schedule_formula(name, horizon)
            high_precision_n = int(mp.ceil(evaluated))
            binary64_n = math.ceil(float({
                "growing_0p125": 0.125,
                "growing_0p5": 0.5,
                "growing_2": 2.0,
                "theorem_96": 96.0,
                "fixed_51": 0.125,
            }[name]) * math.exp((12 if name == "fixed_51" else horizon) / 2.0))
            require(high_precision_n == frozen_n, f"100-digit n mismatch for {horizon}/{name}")
            require(binary64_n == frozen_n, f"binary64 n mismatch for {horizon}/{name}")
            integers.append(frozen_n)
            max_n = max(max_n, frozen_n)
            official_calls += len(OFFICIAL_SEEDS) * len(LEVELS) * repetitions * frozen_n
            official_outputs += len(OFFICIAL_SEEDS) * len(LEVELS) * repetitions
            formula_rows.append(
                {
                    "name": name,
                    "repetitions_per_seed": repetitions,
                    "formula_value_100_digits": mp_string(evaluated),
                    "ceil_100_digits": high_precision_n,
                    "ceil_binary64_crosscheck": binary64_n,
                }
            )
        rows.append({"T": horizon, "n": integers, "checks": formula_rows})
    require(official_calls == EXPECTED_OFFICIAL_CALLS, "official call total mismatch")
    require(official_outputs == EXPECTED_OFFICIAL_OUTPUTS, "official output total mismatch")
    require(max_n == 2_114_541, "maximum n mismatch")
    require(max_n <= MAX_REPLICATE_QUERIES, "per-replicate cap exceeded")
    return {
        "rows": rows,
        "cells": len(OFFICIAL_SEEDS) * len(HORIZONS) * len(LEVELS) * len(SCHEDULES),
        "outputs": official_outputs,
        "point_calls": official_calls,
        "max_n": max_n,
    }


def load_integrals() -> dict[str, Any]:
    source = json.loads(SCALAR_INPUT_PATH.read_text(encoding="utf-8"))
    primary = source["constants"]["primary_I"]
    crosscheck = source["quadrature"]["gauss_legendre"]["value"]
    require(primary == PRIMARY_I, "E3 primary integral string changed")
    require(crosscheck == CROSSCHECK_I, "E3 cross-check integral string changed")
    require(source["quadrature"]["rigorous_enclosure"] is False, "E3 scope changed")
    return {
        "source": relative(SCALAR_INPUT_PATH),
        "source_sha256": sha256(SCALAR_INPUT_PATH),
        "primary_80_digit": primary,
        "crosscheck_100_digit": crosscheck,
        "rigorous_enclosure": False,
        "quadrature_rerun": False,
    }


def reference_for(horizon: int, width: float, integral_string: str) -> dict[str, Any]:
    if width == 0.0:
        return {
            "mass_100_digits": mp_string(mp.mpf(0)),
            "z_h_100_digits": mp_string(mp.mpf(0)),
            "psi_100_digits": mp_string(mp.mpf(0)),
            "psi_binary64": float_record(0.0),
        }
    width_mp = mp_from_float(width)
    mass = mp.mpf(1) / 8 * width_mp * width_mp * mp.mpf(integral_string)
    z_h = mp.exp(horizon) * mass
    psi = z_h / mp.sqrt(1 + z_h * z_h)
    return {
        "mass_100_digits": mp_string(mass),
        "z_h_100_digits": mp_string(z_h),
        "psi_100_digits": mp_string(psi),
        "psi_binary64": float_record(float(psi)),
    }


def input_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    primary_i = mp.mpf(PRIMARY_I)
    for horizon in HORIZONS:
        for level in LEVELS:
            if level == 0.0:
                construction = mp.mpf(0)
                width = 0.0
            else:
                construction = mp.sqrt(
                    mp.mpf(str(level)) / (mp.mpf(1) / 8 * primary_i * mp.exp(horizon))
                )
                width = float(construction)
                require(0.0 < width < 1.0, f"stored width outside (0,1): T={horizon}, z={level}")
            primary = reference_for(horizon, width, PRIMARY_I)
            crosscheck = reference_for(horizon, width, CROSSCHECK_I)
            difference = abs(
                mp.mpf(primary["psi_100_digits"]) - mp.mpf(crosscheck["psi_100_digits"])
            )
            cases.append(
                {
                    "T": horizon,
                    "nominal_z": level,
                    "width_construction_100_digits": mp_string(construction),
                    "stored_width": float_record(width),
                    "reference_primary": primary,
                    "reference_crosscheck": crosscheck,
                    "reference_absolute_difference_100_digits": mp_string(difference),
                }
            )
    widest = next(c for c in cases if c["T"] == 12 and c["nominal_z"] == 4.0)
    require(float.fromhex(widest["stored_width"]["hex"]) > 3.0 / 20.0, "widest case does not wrap")
    return cases


def make_manifest() -> dict[str, Any]:
    mp.mp.dps = 100
    protected = protected_hash_status()
    require(protected["passed"], "one or more of the 342 protected hashes changed")
    require(
        sha256(V1_ARCHIVED_SOURCE_PATH)
        == "cbfda29abd7e4d62e4131502cea5d96fbfaba05c6d0eaf74a9af329f78b458b0",
        "archived v1 source does not match the frozen v1 implementation",
    )
    require(tuple(inspect.signature(sample_estimator).parameters) == ("oracle", "T", "n", "rng"), "opaque estimator signature changed")
    schedule = schedule_contract()
    require(schedule["cells"] == EXPECTED_OFFICIAL_CELLS, "cell count mismatch")
    cases = input_cases()
    require(len(cases) == 12, "input case count mismatch")
    derived_preflight_calls = 3 * (1 + 17 + 131075) + 2 * 131075 + 12 * 17
    require(derived_preflight_calls == EXPECTED_PREFLIGHT_CALLS, "preflight call total mismatch")
    derived_replay_calls = len(OFFICIAL_SEEDS) * len(LEVELS) * sum(
        sum(SCHEDULE_TABLE[horizon]) for horizon in HORIZONS
    )
    require(derived_replay_calls == EXPECTED_REPLAY_CALLS, "subset replay call total mismatch")
    prior_activity = prior_activity_contract()
    require(prior_activity["charged_point_calls"] == 655_633, "unexpected prior-version activity total")
    planned_total = (
        prior_activity["charged_point_calls"]
        + EXPECTED_PREFLIGHT_CALLS
        + EXPECTED_OFFICIAL_CALLS
        + EXPECTED_REPLAY_CALLS
    )
    require(planned_total == 368_270_390, "planned cross-version activity total mismatch")
    require(planned_total <= WHOLE_ACTIVITY_CAP, "whole-activity cap exceeded")
    return {
        "schema_version": 1,
        "artifact_version": ARTIFACT_VERSION,
        "status": "prepared-before-diagnostic-observations",
        "created_utc": utc_now(),
        "immutable_after_creation": True,
        "git_head": git_text("rev-parse", "HEAD"),
        "implementation_source": relative(IMPLEMENTATION_PATH),
        "implementation_source_sha256": sha256(IMPLEMENTATION_PATH),
        "frozen_input_hashes_sha256": {relative(path): sha256(path) for path in FROZEN_INPUTS},
        "protected_initial_sources": protected,
        "environment": {
            "python_executable": sys.executable,
            "python_version": sys.version,
            "numpy_version": np.__version__,
            "mpmath_version": importlib.metadata.version("mpmath"),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "numeric_scope": "NumPy binary64; mpmath mp.dps=100",
        },
        "integral_inputs": load_integrals(),
        "shift": {
            "mathematical": "17/20",
            "implementation": float_record(SHIFT),
        },
        "input_cases": cases,
        "stream_convention": {
            "official": "Generator(PCG64(SeedSequence(seed_root, spawn_key=(T_index,z_index,schedule_index,replicate_index))))",
            "official_seed_roots": list(OFFICIAL_SEEDS),
            "diagnostic_entropy": DIAGNOSTIC_ENTROPY,
            "diagnostic_constant_key": "(0,c_index,n_index)",
            "diagnostic_wrap_key": "(1,0), reconstructed twice from the same initial state",
            "indices": "zero-based, in displayed HORIZONS/LEVELS/SCHEDULES order",
            "claim": "reproducible distinct PCG64 keys; not a proof of independence or continuous laws",
        },
        "sampler": {
            "opaque_api": ["oracle", "T", "n", "rng"],
            "batch_size": BATCH_SIZE,
            "batch_rule": "exactly 131072 except final remainder",
            "batch_sum": "numpy.sum(values,dtype=float64) once per batch",
            "total_sum": "math.fsum of ordered batch sums",
            "division": "once by exact total n",
            "transform": "(exp(T)*mean)/hypot(1,exp(T)*mean)",
            "zero_shortcut": False,
            "every_draw_charged": True,
        },
        "timing_evidence": {
            "raw_estimator_duration": "wall time around sample_estimator, including CountingOracle ledger accounting",
            "accounting_overhead": "wall time measured inside ActivityLedger.charge, including JSON encoding, flush and fsync",
            "accounting_excluded_duration": "max(0, raw estimator duration - measured ledger accounting duration)",
            "claim": "measured subtraction only; not an exact pure-compute certificate",
            "separate_aggregates": [
                "setup",
                "ledger accounting",
                "ledger JSONL serialization",
                "diagnostic/replicate journal JSONL serialization",
                "cell array and metadata serialization",
                "run-log serialization",
            ],
        },
        "failure_evidence": {
            "preflight": "current diagnostic identity, RNG before/after when applicable, oracle attempted/returned/positive counts, estimate or sampling partial, timing and traceback",
            "official": "same replicate context, including successful estimate when a post-estimator count check fails",
            "wrapped_flush_rule": "flush each completed wrapped replay record before starting the next replay",
        },
        "official_design": schedule,
        "preflight_contract": {
            "expected_point_calls": EXPECTED_PREFLIGHT_CALLS,
            "constant_calls": 393_279,
            "wrapped_replay_calls": 262_150,
            "bump_value_calls": 204,
            "constant_mean_absolute_tolerance": 1e-15,
            "constant_output_absolute_tolerance": 2e-15,
            "bump_absolute_tolerance": 1e-14,
            "bump_relative_tolerance": 1e-11,
            "psi_absolute_tolerance": 2e-15,
            "reference_crosscheck_absolute_tolerance": 1e-14,
            "bump_y_values": [0.001, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 0.999, 1.0, 1.001],
            "psi_z_values": [0.0, 1e-300, 1e-12, 0.25, 1.0, 4.0, 1e100, 1e300],
        },
        "activity_budget": {
            "whole_activity_cap": WHOLE_ACTIVITY_CAP,
            "prior_activity": prior_activity,
            "prior_version_calls": prior_activity["charged_point_calls"],
            "preflight_calls": EXPECTED_PREFLIGHT_CALLS,
            "official_calls": EXPECTED_OFFICIAL_CALLS,
            "fixed_later_subset_replay_calls": EXPECTED_REPLAY_CALLS,
            "planned_total": planned_total,
            "failure_revision_headroom": WHOLE_ACTIVITY_CAP - planned_total,
            "full_replay_authorized": False,
        },
        "analysis_contract": {
            "bias": "math.fsum(output-reference)/R",
            "mse": "math.fsum((output-reference)**2)/R",
            "rms": "sqrt(mse)",
            "zero_frequency": "count(output==0)/R",
            "pooling": "pool raw squared errors across seeds, then sqrt",
            "pde_interpretation": "computed surrogate RMS plus/minus 1/32; uncertified for numerical roundoff",
        },
        "commands": {
            "prepare": f"{sys.executable} {relative(IMPLEMENTATION_PATH)} prepare",
            "preflight": f"{sys.executable} {relative(IMPLEMENTATION_PATH)} preflight",
            "run": f"{sys.executable} {relative(IMPLEMENTATION_PATH)} run --clearance ROOT_CLEARANCE.json",
        },
        "scope": {
            "actual_pde_solution_computed": False,
            "floating_reference_certified": False,
            "exact_iid_real_bridge_certified": False,
            "novelty_or_prize_claim": False,
        },
    }


def prepare() -> None:
    require(sys.executable == "/opt/miniconda3/envs/parabolab/bin/python", "wrong Python executable")
    require(not ARTIFACT_DIR.exists(), f"artifact version already exists: {ARTIFACT_DIR}")
    manifest = make_manifest()
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=False)
    write_json_new(MANIFEST_PATH, manifest)
    print(json.dumps({
        "status": "prepared",
        "manifest": relative(MANIFEST_PATH),
        "manifest_sha256": sha256(MANIFEST_PATH),
        "source_sha256": sha256(IMPLEMENTATION_PATH),
        "diagnostic_oracle_calls": 0,
    }, indent=2))


class ActivityLedger:
    def __init__(self, path: Path, phase: str) -> None:
        self.writer = DurableJsonl(path)
        self.phase = phase
        self.total = 0
        self.accounting_elapsed_seconds = 0.0
        self.charge_count = 0

    def charge(self, label: str, count: int) -> None:
        started = time.perf_counter()
        require(count >= 0, "negative activity charge")
        self.total += count
        self.writer.append({
            "utc": utc_now(),
            "phase": self.phase,
            "label": label,
            "point_calls": count,
            "cumulative_point_calls": self.total,
        })
        self.charge_count += 1
        self.accounting_elapsed_seconds += time.perf_counter() - started

    @property
    def serialization_elapsed_seconds(self) -> float:
        return self.writer.serialization_elapsed_seconds

    def close(self) -> None:
        self.writer.close()


class CountingOracle:
    def __init__(self, function: Callable[[np.ndarray], np.ndarray], ledger: ActivityLedger, label: str) -> None:
        self.function = function
        self.ledger = ledger
        self.label = label
        self.attempted_count = 0
        self.returned_count = 0
        self.positive_count = 0

    def __call__(self, points: np.ndarray) -> np.ndarray:
        array = np.asarray(points, dtype=np.float64)
        require(array.ndim == 1, "oracle points must be a one-dimensional vector")
        count = int(array.size)
        self.attempted_count += count
        self.ledger.charge(self.label, count)
        values = np.asarray(self.function(array), dtype=np.float64)
        require(values.shape == array.shape, "oracle returned the wrong shape")
        require(bool(np.all(np.isfinite(values))), "oracle returned a nonfinite value")
        self.returned_count += int(values.size)
        self.positive_count += int(np.count_nonzero(values > 0.0))
        return values


def sample_estimator(oracle: Callable[[np.ndarray], np.ndarray], T: int, n: int, rng: np.random.Generator) -> Estimate:
    """Query only ``oracle`` using public ``T``, ``n`` and ``rng``."""
    if n <= 0:
        raise ValueError("n must be positive")
    batch_sums: list[float] = []
    batch_counts: list[int] = []
    positive_return_count = 0
    observation_count = 0
    try:
        while observation_count < n:
            batch_count = min(BATCH_SIZE, n - observation_count)
            points = rng.random(batch_count, dtype=np.float64)
            values = np.asarray(oracle(points), dtype=np.float64)
            if values.shape != points.shape:
                raise ValueError("oracle returned the wrong shape")
            batch_sums.append(float(np.sum(values, dtype=np.float64)))
            batch_counts.append(batch_count)
            positive_return_count += int(np.count_nonzero(values > 0.0))
            observation_count += batch_count
    except BaseException as error:
        raise SamplingFailure(
            str(error),
            {
                "batch_sums": batch_sums,
                "batch_counts": batch_counts,
                "positive_return_count": positive_return_count,
                "observation_count": observation_count,
            },
        ) from error
    sample_mean = math.fsum(batch_sums) / n
    scaled = math.exp(T) * sample_mean
    output = scaled / math.hypot(1.0, scaled)
    return Estimate(
        sample_mean=sample_mean,
        output=output,
        positive_return_count=positive_return_count,
        observation_count=observation_count,
        batch_sums=tuple(batch_sums),
        batch_counts=tuple(batch_counts),
    )


def measured_estimate(
    oracle: CountingOracle,
    T: int,
    n: int,
    rng: np.random.Generator,
    ledger: ActivityLedger,
    failure_context: dict[str, Any],
) -> tuple[Estimate, dict[str, Any]]:
    """Measure a sampler call and subtract only measured ledger accounting time."""
    accounting_before = ledger.accounting_elapsed_seconds
    started = time.perf_counter()
    try:
        estimate = sample_estimator(oracle, T, n, rng)
    except BaseException as error:
        raw_elapsed = time.perf_counter() - started
        accounting_elapsed = ledger.accounting_elapsed_seconds - accounting_before
        failure_context.update(
            {
                "rng_after_failure": copy.deepcopy(jsonable(rng.bit_generator.state)),
                "oracle_attempted_count": oracle.attempted_count,
                "oracle_returned_count": oracle.returned_count,
                "oracle_positive_count": oracle.positive_count,
                "sampling_partial": getattr(error, "partial", None),
                "timing": {
                    "raw_inclusive_estimator_call_seconds": raw_elapsed,
                    "measured_ledger_accounting_seconds_during_call": accounting_elapsed,
                    "measured_estimator_call_excluding_ledger_accounting_seconds": max(
                        0.0, raw_elapsed - accounting_elapsed
                    ),
                    "interpretation": "measured subtraction of ledger accounting only; not an exact pure-compute certificate",
                },
            }
        )
        raise
    raw_elapsed = time.perf_counter() - started
    accounting_elapsed = ledger.accounting_elapsed_seconds - accounting_before
    timing = {
        "raw_inclusive_estimator_call_seconds": raw_elapsed,
        "measured_ledger_accounting_seconds_during_call": accounting_elapsed,
        "measured_estimator_call_excluding_ledger_accounting_seconds": max(
            0.0, raw_elapsed - accounting_elapsed
        ),
        "interpretation": "measured subtraction of ledger accounting only; not an exact pure-compute certificate",
    }
    failure_context.update(
        {
            "rng_after": copy.deepcopy(jsonable(rng.bit_generator.state)),
            "oracle_attempted_count": oracle.attempted_count,
            "oracle_returned_count": oracle.returned_count,
            "oracle_positive_count": oracle.positive_count,
            "estimate": asdict(estimate),
            "timing": timing,
        }
    )
    return estimate, timing


def bump_oracle(width: float) -> Callable[[np.ndarray], np.ndarray]:
    def evaluate(points: np.ndarray) -> np.ndarray:
        if width == 0.0:
            return np.zeros(points.shape, dtype=np.float64)
        remainder = np.remainder(points - SHIFT, 1.0)
        r = remainder / width
        mask = (r > 0.0) & (r < 1.0)
        values = np.zeros(points.shape, dtype=np.float64)
        masked = r[mask]
        values[mask] = (width / 8.0) * np.exp(-1.0 / (masked * (1.0 - masked)))
        return values
    return evaluate


def constant_oracle(constant: float) -> Callable[[np.ndarray], np.ndarray]:
    def evaluate(points: np.ndarray) -> np.ndarray:
        return np.full(points.shape, constant, dtype=np.float64)
    return evaluate


def stable_psi(value: float) -> float:
    return value / math.hypot(1.0, value)


def mp_psi_of_float(value: float) -> mp.mpf:
    exact = mp_from_float(value)
    return exact / mp.sqrt(1 + exact * exact)


def load_and_verify_manifest() -> dict[str, Any]:
    require(MANIFEST_PATH.is_file(), "prepare manifest is missing")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    require(manifest["artifact_version"] == ARTIFACT_VERSION, "artifact version mismatch")
    require(manifest["implementation_source_sha256"] == sha256(IMPLEMENTATION_PATH), "implementation source changed after prepare")
    for name, frozen_hash in manifest["frozen_input_hashes_sha256"].items():
        require(sha256(REPO / name) == frozen_hash, f"frozen input changed: {name}")
    protected = protected_hash_status()
    require(protected["passed"], "protected source hashes changed after prepare")
    return manifest


class RunLog:
    def __init__(self, path: Path) -> None:
        self.stream = path.open("x", encoding="utf-8")
        self.serialization_elapsed_seconds = 0.0

    def write(self, message: str) -> None:
        started = time.perf_counter()
        line = f"{utc_now()} {message}"
        self.stream.write(line + "\n")
        self.stream.flush()
        os.fsync(self.stream.fileno())
        self.serialization_elapsed_seconds += time.perf_counter() - started
        print(line, flush=True)

    def close(self) -> None:
        if not self.stream.closed:
            self.stream.close()


def diagnostic_points(width: float) -> list[tuple[str, float]]:
    points = [
        ("zero", 0.0),
        ("nextafter_zero_positive", float(np.nextafter(0.0, math.inf))),
        ("nextafter_shift_negative", float(np.nextafter(SHIFT, -math.inf))),
        ("shift", SHIFT),
        ("nextafter_shift_positive", float(np.nextafter(SHIFT, math.inf))),
        ("nextafter_one_negative", float(np.nextafter(1.0, -math.inf))),
    ]
    for y in (0.001, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 0.999, 1.0, 1.001):
        point = float(np.remainder(np.float64(SHIFT + width * y), np.float64(1.0)))
        points.append((f"wrapped_shift_plus_h_times_{repr(y)}", point))
    require(len(points) == 17, "diagnostic point count mismatch")
    return points


def exact_bump_reference(point: float, width: float) -> mp.mpf:
    if width == 0.0:
        return mp.mpf(0)
    point_q = Fraction(*point.as_integer_ratio())
    width_q = Fraction(*width.as_integer_ratio())
    remainder_q = (point_q - SHIFT_FRACTION) % 1
    r_q = remainder_q / width_q
    if not (0 < r_q < 1):
        return mp.mpf(0)
    r = mp.mpf(r_q.numerator) / r_q.denominator
    width_mp = mp.mpf(width_q.numerator) / width_q.denominator
    return width_mp / 8 * mp.exp(-1 / (r * (1 - r)))


def run_preflight() -> None:
    require(sys.executable == "/opt/miniconda3/envs/parabolab/bin/python", "wrong Python executable")
    phase_started = time.perf_counter()
    require(not PREFLIGHT_LOG_PATH.exists(), "preflight already attempted for this version")
    manifest = load_and_verify_manifest()
    mp.mp.dps = 100
    log = RunLog(PREFLIGHT_LOG_PATH)
    journal = DurableJsonl(PREFLIGHT_JOURNAL_PATH)
    ledger = ActivityLedger(PREFLIGHT_LEDGER_PATH, "preflight")
    failure_context: dict[str, Any] = {"diagnostic_identity": {"kind": "setup"}}
    setup_elapsed = 0.0
    diagnostics_started = 0.0
    try:
        log.write(f"START manifest_sha256={sha256(MANIFEST_PATH)} source_sha256={sha256(IMPLEMENTATION_PATH)}")
        setup_elapsed = time.perf_counter() - phase_started
        diagnostics_started = time.perf_counter()
        constants = (0.0, 0.125, 0.5)
        sizes = (1, 17, 131075)
        for c_index, constant in enumerate(constants):
            for n_index, n in enumerate(sizes):
                label = f"constant/c{c_index}/n{n_index}"
                seed = np.random.SeedSequence(DIAGNOSTIC_ENTROPY, spawn_key=(0, c_index, n_index))
                rng = np.random.Generator(np.random.PCG64(seed))
                before = copy.deepcopy(jsonable(rng.bit_generator.state))
                failure_context = {
                    "diagnostic_identity": {
                        "kind": "opaque_constant",
                        "label": label,
                        "c_index": c_index,
                        "n_index": n_index,
                        "constant": float_record(constant),
                        "n": n,
                        "T": 12,
                    },
                    "rng_before": before,
                }
                oracle = CountingOracle(constant_oracle(constant), ledger, label)
                estimate, timing = measured_estimate(
                    oracle, 12, n, rng, ledger, failure_context
                )
                after = failure_context["rng_after"]
                expected_scaled = mp.exp(12) * mp_from_float(constant)
                expected_output = expected_scaled / mp.sqrt(1 + expected_scaled * expected_scaled)
                mean_error = abs(estimate.sample_mean - constant)
                output_error = abs(estimate.output - float(expected_output))
                passed = (
                    oracle.attempted_count == n
                    and oracle.returned_count == n
                    and estimate.observation_count == n
                    and mean_error <= 1e-15
                    and output_error <= 2e-15
                    and estimate.positive_return_count == (n if constant > 0.0 else 0)
                    and oracle.positive_count == estimate.positive_return_count
                )
                record = {
                    "kind": "opaque_constant",
                    "label": label,
                    "constant": float_record(constant),
                    "n": n,
                    "T": 12,
                    "spawn_key": [0, c_index, n_index],
                    "rng_before": before,
                    "rng_after": after,
                    "estimate": asdict(estimate),
                    "oracle_attempted_count": oracle.attempted_count,
                    "oracle_returned_count": oracle.returned_count,
                    "oracle_positive_count": oracle.positive_count,
                    "timing": timing,
                    "expected_output_100_digits": mp_string(expected_output),
                    "mean_absolute_error": mean_error,
                    "output_absolute_error": output_error,
                    "passed": passed,
                }
                failure_context.update({
                    "mean_absolute_error": mean_error,
                    "output_absolute_error": output_error,
                    "passed": passed,
                })
                journal.append(record)
                require(passed, f"constant diagnostic failed: {label}")

        widest = next(case for case in manifest["input_cases"] if case["T"] == 12 and case["nominal_z"] == 4.0)
        widest_h = float.fromhex(widest["stored_width"]["hex"])
        wrapped_records: list[dict[str, Any]] = []
        for replay_index in range(2):
            label = f"wrapped_replay/{replay_index}"
            seed = np.random.SeedSequence(DIAGNOSTIC_ENTROPY, spawn_key=(1, 0))
            rng = np.random.Generator(np.random.PCG64(seed))
            before = copy.deepcopy(jsonable(rng.bit_generator.state))
            failure_context = {
                "diagnostic_identity": {
                    "kind": "wrapped_seeded_replay",
                    "label": label,
                    "replay_index": replay_index,
                    "T": 12,
                    "nominal_z": 4.0,
                    "n": 131075,
                },
                "rng_before": before,
            }
            oracle = CountingOracle(bump_oracle(widest_h), ledger, label)
            estimate, timing = measured_estimate(
                oracle, 12, 131075, rng, ledger, failure_context
            )
            after = failure_context["rng_after"]
            individual_passed = (
                oracle.attempted_count == 131075
                and oracle.returned_count == 131075
                and estimate.observation_count == 131075
                and oracle.positive_count == estimate.positive_return_count
            )
            record = {
                "kind": "wrapped_seeded_replay",
                "label": label,
                "T": 12,
                "nominal_z": 4.0,
                "width": float_record(widest_h),
                "n": 131075,
                "spawn_key": [1, 0],
                "rng_before": before,
                "rng_after": after,
                "estimate": asdict(estimate),
                "oracle_attempted_count": oracle.attempted_count,
                "oracle_returned_count": oracle.returned_count,
                "oracle_positive_count": oracle.positive_count,
                "timing": timing,
                "passed": individual_passed,
            }
            failure_context["passed"] = individual_passed
            journal.append(record)
            wrapped_records.append(record)
            require(individual_passed, f"wrapped replay count check failed: {label}")
        replay_equal = (
            wrapped_records[0]["rng_before"] == wrapped_records[1]["rng_before"]
            and wrapped_records[0]["rng_after"] == wrapped_records[1]["rng_after"]
            and wrapped_records[0]["estimate"] == wrapped_records[1]["estimate"]
            and wrapped_records[0]["oracle_attempted_count"] == wrapped_records[1]["oracle_attempted_count"] == 131075
            and wrapped_records[0]["oracle_returned_count"] == wrapped_records[1]["oracle_returned_count"] == 131075
            and wrapped_records[0]["oracle_positive_count"] == wrapped_records[1]["oracle_positive_count"]
        )
        failure_context = {
            "diagnostic_identity": {"kind": "wrapped_seeded_replay_pair"},
            "runs": wrapped_records,
            "passed": replay_equal,
        }
        journal.append({"kind": "wrapped_seeded_replay_pair", "runs": wrapped_records, "passed": replay_equal})
        require(replay_equal, "wrapped seeded replay was not bitwise identical")

        point_pass_count = 0
        underflow_count = 0
        for case_index, case in enumerate(manifest["input_cases"]):
            width = float.fromhex(case["stored_width"]["hex"])
            failure_context = {
                "diagnostic_identity": {
                    "kind": "input_case_width_check",
                    "case_index": case_index,
                    "T": case["T"],
                    "nominal_z": case["nominal_z"],
                    "width": case["stored_width"],
                }
            }
            require(width == 0.0 or 0.0 < width < 1.0, "stored width range check failed")
            if case["T"] == 12 and case["nominal_z"] == 4.0:
                require(width > 3.0 / 20.0, "stored widest width wrap check failed")
            oracle_function = bump_oracle(width)
            for point_index, (point_name, point) in enumerate(diagnostic_points(width)):
                label = f"bump_value/case{case_index}/point{point_index}"
                failure_context = {
                    "diagnostic_identity": {
                        "kind": "bump_value",
                        "label": label,
                        "case_index": case_index,
                        "T": case["T"],
                        "nominal_z": case["nominal_z"],
                        "point_index": point_index,
                        "point_name": point_name,
                        "point": float_record(point),
                    }
                }
                oracle = CountingOracle(oracle_function, ledger, label)
                try:
                    actual = float(oracle(np.asarray([point], dtype=np.float64))[0])
                except BaseException:
                    failure_context.update({
                        "oracle_attempted_count": oracle.attempted_count,
                        "oracle_returned_count": oracle.returned_count,
                        "oracle_positive_count": oracle.positive_count,
                    })
                    raise
                failure_context.update({
                    "actual": float_record(actual),
                    "oracle_attempted_count": oracle.attempted_count,
                    "oracle_returned_count": oracle.returned_count,
                    "oracle_positive_count": oracle.positive_count,
                })
                reference = exact_bump_reference(point, width)
                reference_float = float(reference)
                absolute_error = abs(actual - reference_float)
                tolerance = 1e-14 + 1e-11 * abs(reference_float)
                passed = (
                    oracle.attempted_count == 1
                    and oracle.returned_count == 1
                    and absolute_error <= tolerance
                )
                is_underflow = actual == 0.0 and reference > 0
                underflow_count += int(is_underflow)
                point_pass_count += int(passed)
                record = {
                    "kind": "bump_value",
                    "case_index": case_index,
                    "T": case["T"],
                    "nominal_z": case["nominal_z"],
                    "width": case["stored_width"],
                    "point_index": point_index,
                    "point_name": point_name,
                    "point": float_record(point),
                    "actual": float_record(actual),
                    "reference_100_digits": mp_string(reference),
                    "reference_binary64": float_record(reference_float),
                    "absolute_error": absolute_error,
                    "combined_tolerance": tolerance,
                    "underflow_to_zero": is_underflow,
                    "passed": passed,
                }
                failure_context.update({
                    "reference_100_digits": mp_string(reference),
                    "absolute_error": absolute_error,
                    "combined_tolerance": tolerance,
                    "underflow_to_zero": is_underflow,
                    "passed": passed,
                })
                journal.append(record)
                require(passed, f"bump value diagnostic failed: case {case_index}, point {point_index}")

        psi_pass_count = 0
        for index, value in enumerate((0.0, 1e-300, 1e-12, 0.25, 1.0, 4.0, 1e100, 1e300)):
            failure_context = {
                "diagnostic_identity": {
                    "kind": "stable_psi",
                    "index": index,
                    "z": float_record(value),
                }
            }
            actual = stable_psi(value)
            reference = mp_psi_of_float(value)
            error = abs(actual - float(reference))
            passed = error <= 2e-15
            psi_pass_count += int(passed)
            record = {
                "kind": "stable_psi",
                "index": index,
                "z": float_record(value),
                "actual": float_record(actual),
                "reference_100_digits": mp_string(reference),
                "absolute_error": error,
                "passed": passed,
            }
            failure_context.update(record)
            journal.append(record)
            require(passed, f"stable Psi diagnostic failed at index {index}")

        reference_pass_count = 0
        for case_index, case in enumerate(manifest["input_cases"]):
            failure_context = {
                "diagnostic_identity": {
                    "kind": "stored_width_reference_crosscheck",
                    "case_index": case_index,
                    "T": case["T"],
                    "nominal_z": case["nominal_z"],
                }
            }
            difference = mp.mpf(case["reference_absolute_difference_100_digits"])
            passed = difference <= mp.mpf("1e-14")
            reference_pass_count += int(passed)
            record = {
                "kind": "stored_width_reference_crosscheck",
                "case_index": case_index,
                "T": case["T"],
                "nominal_z": case["nominal_z"],
                "absolute_difference_100_digits": case["reference_absolute_difference_100_digits"],
                "absolute_tolerance": "1e-14",
                "passed": passed,
            }
            failure_context.update(record)
            journal.append(record)
            require(passed, f"stored-width reference cross-check failed: case {case_index}")

        failure_context = {
            "diagnostic_identity": {"kind": "official_design_recalculation"}
        }
        schedule = schedule_contract()
        schema_passed = (
            schedule["cells"] == EXPECTED_OFFICIAL_CELLS
            and schedule["outputs"] == EXPECTED_OFFICIAL_OUTPUTS
            and schedule["point_calls"] == EXPECTED_OFFICIAL_CALLS
            and schedule["max_n"] == 2_114_541
        )
        failure_context.update({"result": schedule, "passed": schema_passed})
        journal.append({"kind": "official_design_recalculation", "result": schedule, "passed": schema_passed})
        require(schema_passed, "official design recalculation failed")
        require(ledger.total == EXPECTED_PREFLIGHT_CALLS, "preflight oracle-call total mismatch")

        diagnostics_elapsed = time.perf_counter() - diagnostics_started
        result = {
            "schema_version": 1,
            "artifact_version": ARTIFACT_VERSION,
            "status": "PASS",
            "completed_utc": utc_now(),
            "manifest_sha256": sha256(MANIFEST_PATH),
            "implementation_source_sha256": sha256(IMPLEMENTATION_PATH),
            "actual_point_calls": ledger.total,
            "expected_point_calls": EXPECTED_PREFLIGHT_CALLS,
            "constant_tests_passed": 9,
            "wrapped_replay_passed": True,
            "bump_value_tests_passed": point_pass_count,
            "bump_value_tests_total": 204,
            "underflow_to_zero_count": underflow_count,
            "psi_tests_passed": psi_pass_count,
            "psi_tests_total": 8,
            "reference_crosschecks_passed": reference_pass_count,
            "reference_crosschecks_total": 12,
            "official_design_recalculation_passed": schema_passed,
            "official_run_executed": False,
            "independent_replay_executed": False,
            "actual_pde_solution_computed": False,
            "cross_version_charged_calls_after_preflight": (
                manifest["activity_budget"]["prior_version_calls"] + ledger.total
            ),
            "timing_measurements_seconds": {
                "setup_before_diagnostics": setup_elapsed,
                "diagnostics_raw_wall_before_result_write": diagnostics_elapsed,
                "ledger_accounting": ledger.accounting_elapsed_seconds,
                "ledger_jsonl_serialization": ledger.serialization_elapsed_seconds,
                "diagnostic_journal_jsonl_serialization": journal.serialization_elapsed_seconds,
                "run_log_serialization_before_result_write": log.serialization_elapsed_seconds,
                "interpretation": "raw wall durations overlap measured serialization counters; estimator records subtract only measured ledger accounting and are not exact pure-compute certificates",
            },
            "evidence_sha256": {
                relative(PREFLIGHT_JOURNAL_PATH): sha256(PREFLIGHT_JOURNAL_PATH),
                relative(PREFLIGHT_LEDGER_PATH): sha256(PREFLIGHT_LEDGER_PATH),
            },
        }
        write_json_new(PREFLIGHT_RESULT_PATH, result)
        log.write(f"PASS actual_point_calls={ledger.total} result_sha256={sha256(PREFLIGHT_RESULT_PATH)}")
    except BaseException as error:
        failure = {
            "schema_version": 1,
            "artifact_version": ARTIFACT_VERSION,
            "status": "FAIL",
            "failed_utc": utc_now(),
            "manifest_sha256": sha256(MANIFEST_PATH),
            "implementation_source_sha256": sha256(IMPLEMENTATION_PATH),
            "charged_point_calls": ledger.total,
            "cross_version_charged_calls": (
                manifest["activity_budget"]["prior_version_calls"] + ledger.total
            ),
            "failure_context": failure_context,
            "sampling_partial": getattr(error, "partial", None),
            "timing_measurements_seconds": {
                "setup_before_diagnostics": setup_elapsed,
                "diagnostics_raw_wall_before_failure": (
                    time.perf_counter() - diagnostics_started if diagnostics_started else 0.0
                ),
                "ledger_accounting": ledger.accounting_elapsed_seconds,
                "ledger_jsonl_serialization": ledger.serialization_elapsed_seconds,
                "diagnostic_journal_jsonl_serialization": journal.serialization_elapsed_seconds,
                "run_log_serialization_before_failure_record": log.serialization_elapsed_seconds,
            },
            "error_type": type(error).__name__,
            "error": str(error),
            "traceback": traceback.format_exc(),
            "rerun_same_version_permitted": False,
        }
        write_json_new(PREFLIGHT_FAILURE_PATH, failure)
        log.write(f"FAIL charged_point_calls={ledger.total} error={type(error).__name__}: {error}")
        raise
    finally:
        journal.close()
        ledger.close()
        log.close()


def publish_file_without_overwrite(temporary: Path, final: Path) -> None:
    os.link(temporary, final)
    temporary.unlink()


def verify_clearance(clearance_path: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    require(PREFLIGHT_RESULT_PATH.is_file(), "successful preflight evidence is missing")
    preflight = json.loads(PREFLIGHT_RESULT_PATH.read_text(encoding="utf-8"))
    require(preflight["status"] == "PASS", "preflight did not pass")
    clearance = json.loads(clearance_path.read_text(encoding="utf-8"))
    require(clearance.get("status") == "CLEARED for official positive-query run", "root clearance status is absent")
    require(clearance.get("artifact_version") == ARTIFACT_VERSION, "clearance version mismatch")
    require(clearance.get("manifest_sha256") == sha256(MANIFEST_PATH), "clearance manifest hash mismatch")
    require(clearance.get("implementation_source_sha256") == sha256(IMPLEMENTATION_PATH), "clearance source hash mismatch")
    require(clearance.get("preflight_result_sha256") == sha256(PREFLIGHT_RESULT_PATH), "clearance preflight hash mismatch")
    require(manifest["activity_budget"]["planned_total"] <= WHOLE_ACTIVITY_CAP, "whole-activity cap exceeded")
    return clearance


def cell_name(seed_index: int, horizon_index: int, level_index: int, schedule_index: int) -> str:
    return f"seed-{seed_index:02d}_T-{horizon_index:02d}_z-{level_index:02d}_schedule-{schedule_index:02d}"


def run_official(clearance_path: Path) -> None:
    require(sys.executable == "/opt/miniconda3/envs/parabolab/bin/python", "wrong Python executable")
    run_started = time.perf_counter()
    manifest = load_and_verify_manifest()
    clearance = verify_clearance(clearance_path, manifest)
    require(not OFFICIAL_DIR.exists(), "official execution was already started; root must review partial state")
    OFFICIAL_DIR.mkdir(parents=True, exist_ok=False)
    ledger = ActivityLedger(OFFICIAL_DIR / "activity.jsonl", "official")
    run_log = RunLog(OFFICIAL_DIR / "run.log")
    setup_elapsed = 0.0
    artifact_serialization_elapsed = 0.0
    journal_serialization_elapsed = 0.0
    raw_inclusive_estimator_elapsed = 0.0
    measured_accounting_during_estimator_elapsed = 0.0
    measured_estimator_excluding_accounting_elapsed = 0.0
    completed_cells = 0
    completed_outputs = 0
    failure_context: dict[str, Any] = {"official_identity": {"kind": "setup"}}
    try:
        run_log.write(
            f"START clearance_sha256={sha256(clearance_path)} manifest_sha256={sha256(MANIFEST_PATH)}"
        )
        cases = {(case["T"], case["nominal_z"]): case for case in manifest["input_cases"]}
        setup_elapsed = time.perf_counter() - run_started
        for seed_index, seed_root in enumerate(OFFICIAL_SEEDS):
            for horizon_index, horizon in enumerate(HORIZONS):
                for level_index, level in enumerate(LEVELS):
                    case = cases[(horizon, level)]
                    width = float.fromhex(case["stored_width"]["hex"])
                    oracle_function = bump_oracle(width)
                    for schedule_index, ((schedule_name, repetitions), n) in enumerate(
                        zip(SCHEDULES, SCHEDULE_TABLE[horizon])
                    ):
                        name = cell_name(seed_index, horizon_index, level_index, schedule_index)
                        failure_context = {
                            "official_identity": {
                                "kind": "cell_setup",
                                "cell": name,
                                "seed_root": seed_root,
                                "T": horizon,
                                "nominal_z": level,
                                "schedule": schedule_name,
                                "n": n,
                                "repetitions": repetitions,
                            }
                        }
                        cell_dir = OFFICIAL_DIR / name
                        cell_dir.mkdir(exist_ok=False)
                        journal_path = cell_dir / "replicates.jsonl"
                        journal = DurableJsonl(journal_path)
                        outputs: list[float] = []
                        means: list[float] = []
                        positives: list[int] = []
                        counts: list[int] = []
                        cell_raw_inclusive_estimator_elapsed = 0.0
                        cell_accounting_during_estimator_elapsed = 0.0
                        cell_estimator_excluding_accounting_elapsed = 0.0
                        try:
                            for replicate_index in range(repetitions):
                                spawn_key = (horizon_index, level_index, schedule_index, replicate_index)
                                seed = np.random.SeedSequence(seed_root, spawn_key=spawn_key)
                                rng = np.random.Generator(np.random.PCG64(seed))
                                before = copy.deepcopy(jsonable(rng.bit_generator.state))
                                label = f"{name}/replicate-{replicate_index:03d}"
                                failure_context = {
                                    "official_identity": {
                                        "kind": "replicate",
                                        "cell": name,
                                        "seed_root": seed_root,
                                        "spawn_key": list(spawn_key),
                                        "replicate_index": replicate_index,
                                        "T": horizon,
                                        "nominal_z": level,
                                        "schedule": schedule_name,
                                        "n": n,
                                    },
                                    "rng_before": before,
                                }
                                oracle = CountingOracle(oracle_function, ledger, label)
                                try:
                                    estimate, timing = measured_estimate(
                                        oracle,
                                        horizon,
                                        n,
                                        rng,
                                        ledger,
                                        failure_context,
                                    )
                                    require(
                                        oracle.attempted_count
                                        == oracle.returned_count
                                        == estimate.observation_count
                                        == n,
                                        "official query/observation count mismatch",
                                    )
                                    require(
                                        oracle.positive_count
                                        == estimate.positive_return_count,
                                        "official positive-count mismatch",
                                    )
                                    record = {
                                        "status": "PASS",
                                        "seed_root": seed_root,
                                        "spawn_key": list(spawn_key),
                                        "replicate_index": replicate_index,
                                        "n": n,
                                        "rng_before": before,
                                        "rng_after": failure_context["rng_after"],
                                        "estimate": asdict(estimate),
                                        "oracle_attempted_count": oracle.attempted_count,
                                        "oracle_returned_count": oracle.returned_count,
                                        "oracle_positive_count": oracle.positive_count,
                                        "timing": timing,
                                    }
                                    journal.append(record)
                                except BaseException as error:
                                    failure_context.update({
                                        "rng_after_failure": copy.deepcopy(
                                            jsonable(rng.bit_generator.state)
                                        ),
                                        "oracle_attempted_count": oracle.attempted_count,
                                        "oracle_returned_count": oracle.returned_count,
                                        "oracle_positive_count": oracle.positive_count,
                                        "estimate": failure_context.get("estimate"),
                                        "sampling_partial": getattr(error, "partial", None)
                                        or failure_context.get("sampling_partial"),
                                    })
                                    journal.append({
                                        "status": "FAIL",
                                        "failure_context": failure_context,
                                        "error_type": type(error).__name__,
                                        "error": str(error),
                                        "traceback": traceback.format_exc(),
                                    })
                                    raise
                                cell_raw_inclusive_estimator_elapsed += timing[
                                    "raw_inclusive_estimator_call_seconds"
                                ]
                                cell_accounting_during_estimator_elapsed += timing[
                                    "measured_ledger_accounting_seconds_during_call"
                                ]
                                cell_estimator_excluding_accounting_elapsed += timing[
                                    "measured_estimator_call_excluding_ledger_accounting_seconds"
                                ]
                                raw_inclusive_estimator_elapsed += timing[
                                    "raw_inclusive_estimator_call_seconds"
                                ]
                                measured_accounting_during_estimator_elapsed += timing[
                                    "measured_ledger_accounting_seconds_during_call"
                                ]
                                measured_estimator_excluding_accounting_elapsed += timing[
                                    "measured_estimator_call_excluding_ledger_accounting_seconds"
                                ]
                                means.append(estimate.sample_mean)
                                outputs.append(estimate.output)
                                positives.append(estimate.positive_return_count)
                                counts.append(estimate.observation_count)
                                completed_outputs += 1
                        finally:
                            journal_serialization_elapsed += (
                                journal.serialization_elapsed_seconds
                            )
                            journal.close()

                        serialization_started = time.perf_counter()
                        arrays_tmp = cell_dir / "cell_arrays.tmp"
                        arrays_final = cell_dir / "cell_arrays.npz"
                        with arrays_tmp.open("xb") as stream:
                            np.savez(
                                stream,
                                sample_mean=np.asarray(means, dtype=np.float64),
                                output=np.asarray(outputs, dtype=np.float64),
                                positive_return_count=np.asarray(positives, dtype=np.int64),
                                actual_query_count=np.asarray(counts, dtype=np.int64),
                            )
                            stream.flush()
                            os.fsync(stream.fileno())
                        publish_file_without_overwrite(arrays_tmp, arrays_final)
                        metadata_tmp = cell_dir / "cell_complete.tmp"
                        metadata_final = cell_dir / "cell_complete.json"
                        write_json_new(metadata_tmp, {
                            "status": "PASS",
                            "cell": name,
                            "seed_root": seed_root,
                            "T": horizon,
                            "nominal_z": level,
                            "schedule": schedule_name,
                            "n": n,
                            "repetitions": repetitions,
                            "width": case["stored_width"],
                            "reference_primary": case["reference_primary"],
                            "journal_sha256": sha256(journal_path),
                            "arrays_sha256": sha256(arrays_final),
                            "timing_measurements_seconds": {
                                "raw_inclusive_estimator_calls": cell_raw_inclusive_estimator_elapsed,
                                "measured_ledger_accounting_during_estimator_calls": cell_accounting_during_estimator_elapsed,
                                "measured_estimator_calls_excluding_ledger_accounting": cell_estimator_excluding_accounting_elapsed,
                                "replicate_journal_jsonl_serialization": journal.serialization_elapsed_seconds,
                                "interpretation": "measured subtraction of ledger accounting only; not an exact pure-compute certificate",
                            },
                        })
                        publish_file_without_overwrite(metadata_tmp, metadata_final)
                        artifact_serialization_elapsed += time.perf_counter() - serialization_started
                        completed_cells += 1
                        run_log.write(f"CELL PASS {name} calls={repetitions*n}")

        require(completed_cells == EXPECTED_OFFICIAL_CELLS, "official completed-cell count mismatch")
        require(completed_outputs == EXPECTED_OFFICIAL_OUTPUTS, "official output count mismatch")
        require(ledger.total == EXPECTED_OFFICIAL_CALLS, "official point-call count mismatch")
        result = {
            "schema_version": 1,
            "artifact_version": ARTIFACT_VERSION,
            "status": "PASS",
            "completed_utc": utc_now(),
            "manifest_sha256": sha256(MANIFEST_PATH),
            "preflight_result_sha256": sha256(PREFLIGHT_RESULT_PATH),
            "clearance_sha256": sha256(clearance_path),
            "implementation_source_sha256": sha256(IMPLEMENTATION_PATH),
            "completed_cells": completed_cells,
            "completed_outputs": completed_outputs,
            "actual_point_calls": ledger.total,
            "timing_seconds": {
                "setup_before_first_cell": setup_elapsed,
                "raw_inclusive_estimator_calls": raw_inclusive_estimator_elapsed,
                "measured_ledger_accounting_during_estimator_calls": measured_accounting_during_estimator_elapsed,
                "measured_estimator_calls_excluding_ledger_accounting": measured_estimator_excluding_accounting_elapsed,
                "ledger_accounting_all_official_calls": ledger.accounting_elapsed_seconds,
                "ledger_jsonl_serialization": ledger.serialization_elapsed_seconds,
                "replicate_journal_jsonl_serialization": journal_serialization_elapsed,
                "cell_array_and_metadata_serialization": artifact_serialization_elapsed,
                "run_log_serialization_before_result_write": run_log.serialization_elapsed_seconds,
                "total_wall_before_result_write": time.perf_counter() - run_started,
                "reference": 0.0,
                "diagnostics": 0.0,
                "plotting": 0.0,
                "interpretation": "raw wall durations overlap measured serialization counters; accounting-excluded estimator time subtracts only measured ledger accounting",
            },
            "actual_pde_solution_computed": False,
            "plots_created": False,
            "independent_replay_executed": False,
        }
        write_json_new(OFFICIAL_DIR / "official_result.json", result)
        run_log.write(f"PASS actual_point_calls={ledger.total}")
    except BaseException as error:
        write_json_new(OFFICIAL_DIR / "official_failure.json", {
            "schema_version": 1,
            "artifact_version": ARTIFACT_VERSION,
            "status": "FAIL",
            "failed_utc": utc_now(),
            "manifest_sha256": sha256(MANIFEST_PATH),
            "implementation_source_sha256": sha256(IMPLEMENTATION_PATH),
            "clearance": jsonable(clearance),
            "charged_point_calls": ledger.total,
            "cross_version_charged_calls": (
                manifest["activity_budget"]["prior_version_calls"]
                + EXPECTED_PREFLIGHT_CALLS
                + ledger.total
            ),
            "completed_cells": completed_cells,
            "completed_outputs": completed_outputs,
            "failure_context": failure_context,
            "sampling_partial": getattr(error, "partial", None)
            or failure_context.get("sampling_partial"),
            "timing_measurements_seconds": {
                "setup_before_first_cell": setup_elapsed,
                "raw_inclusive_estimator_calls": raw_inclusive_estimator_elapsed,
                "measured_ledger_accounting_during_estimator_calls": measured_accounting_during_estimator_elapsed,
                "measured_estimator_calls_excluding_ledger_accounting": measured_estimator_excluding_accounting_elapsed,
                "ledger_accounting_all_official_calls": ledger.accounting_elapsed_seconds,
                "ledger_jsonl_serialization": ledger.serialization_elapsed_seconds,
                "replicate_journal_jsonl_serialization": journal_serialization_elapsed,
                "cell_array_and_metadata_serialization": artifact_serialization_elapsed,
                "run_log_serialization_before_failure_record": run_log.serialization_elapsed_seconds,
                "total_wall_before_failure_record": time.perf_counter() - run_started,
            },
            "error_type": type(error).__name__,
            "error": str(error),
            "traceback": traceback.format_exc(),
            "automatic_retry_permitted": False,
        })
        run_log.write(f"FAIL charged_point_calls={ledger.total} error={type(error).__name__}: {error}")
        raise
    finally:
        ledger.close()
        run_log.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="phase", required=True)
    subparsers.add_parser("prepare")
    subparsers.add_parser("preflight")
    official = subparsers.add_parser("run")
    official.add_argument("--clearance", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.phase == "prepare":
        prepare()
    elif args.phase == "preflight":
        run_preflight()
    elif args.phase == "run":
        run_official(args.clearance)
    else:
        raise AssertionError(args.phase)


if __name__ == "__main__":
    main()
