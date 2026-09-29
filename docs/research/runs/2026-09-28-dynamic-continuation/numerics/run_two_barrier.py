"""Fixed, no-overwrite driver for the frozen two-barrier experiment.

Stages are intentionally separate:

``prepare`` freezes source/environment/RNG state, reruns development tests,
and executes deterministic preflight cases. ``diagnostics`` performs the
prespecified official diagnostics once. ``primary`` is gated on both those
diagnostics and the independent ``reference-v1`` artifact.
"""

from __future__ import annotations

import argparse
import contextlib
import copy
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import io
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback
from typing import Any

import mpmath as mp
import numpy as np

import two_barrier_sampler as sampler


NUMERICS_DIR = Path(__file__).resolve().parent
RUN_ROOT = NUMERICS_DIR.parent
PROJECT_ROOT = NUMERICS_DIR.parents[4]
ARTIFACTS_ROOT = RUN_ROOT / "artifacts" / "two-barrier"
SAMPLER_ARTIFACT = ARTIFACTS_ROOT / "sampler-v1"
REFERENCE_ARTIFACT = ARTIFACTS_ROOT / "reference-v1"

PROTOCOL_PATH = RUN_ROOT / "02d-two-barrier-experiment-protocol.md"
PROTOCOL_SHA256 = "605eda24574bfb7e44dc997c185836d2a54311c18344e0be4c005674e00beda9"

HORIZONS = np.array([0.0, 0.25, 1.0, 4.0, 16.0, 64.0, 256.0])
QUERIES = np.array([0.0, math.pi / 2.0, math.pi])
PRIMARY_SEEDS = (2026092831, 2026092832, 2026092833)
PRIMARY_ROOTS = 10_000
PRIMARY_CELL_SECONDS = 120.0
CHECKPOINT_ROOTS = 1_000

CLOCK_DIAGNOSTIC_SEED = 2026092891
CLOCK_DIAGNOSTIC_HORIZONS = np.array([0.25, 1.0, 4.0])
CLOCK_DIAGNOSTIC_ROOTS = 100_000
CONSTANT_DIAGNOSTIC_SEED = 2026092892
CONSTANT_DIAGNOSTIC_ROOTS = 100_000
ENDPOINT_DIAGNOSTIC_SEED = 2026092893
ENDPOINT_DIAGNOSTIC_ROOTS = 128
STATISTICAL_ALPHA = 1.0e-6
DKW_THRESHOLD = math.sqrt(
    math.log(2.0 / STATISTICAL_ALPHA) / (2.0 * CLOCK_DIAGNOSTIC_ROOTS)
)
CONSTANT_MEAN_THRESHOLD = 1.25 * DKW_THRESHOLD

PREFLIGHT_SEED = 2026092890
PREFLIGHT_ROOTS_PER_CASE = 16
PREFLIGHT_HORIZONS = (0.0, 0.25, 4.0, 256.0)
PREFLIGHT_QUERIES = (0.0, math.pi / 2.0, math.pi)
PREFLIGHT_INVERSE_UNIFORMS = (
    math.nextafter(8.0 / 15.0, 1.0),
    0.75,
    0.99,
    math.nextafter(1.0, 0.0),
)
PREFLIGHT_ABSOLUTE_TOLERANCE = 5.0e-14
PREFLIGHT_RELATIVE_TOLERANCE = 5.0e-14

ROOT_FIELDS = (
    "scaled_output",
    "normalized_output",
    "nodes",
    "leaves",
    "binary_internal",
    "ternary_internal",
    "clock_proposals",
    "clock_rejections",
    "zero_redraws",
    "coefficient_limit_substitution",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


def write_json_exclusive(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(jsonable(payload), handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


def write_npz_exclusive(path: Path, **arrays: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        np.savez_compressed(handle, **arrays)
        handle.flush()
        os.fsync(handle.fileno())


def make_rng(entropy: int, spawn_key: tuple[int, ...]) -> np.random.Generator:
    seed_sequence = np.random.SeedSequence(entropy=entropy, spawn_key=spawn_key)
    return np.random.Generator(np.random.PCG64(seed_sequence))


def stream_record(label: str, entropy: int, spawn_key: tuple[int, ...]) -> dict[str, Any]:
    rng = make_rng(entropy, spawn_key)
    return {
        "label": label,
        "entropy": entropy,
        "spawn_key": list(spawn_key),
        "seed_sequence_state": jsonable(
            np.random.SeedSequence(entropy=entropy, spawn_key=spawn_key).state
        ),
        "initial_pcg64_state": jsonable(rng.bit_generator.state),
    }


def all_frozen_streams() -> list[dict[str, Any]]:
    streams: list[dict[str, Any]] = []
    for seed in PRIMARY_SEEDS:
        for horizon_index in range(len(HORIZONS)):
            for query_index in range(len(QUERIES)):
                key = (0, horizon_index, query_index)
                streams.append(stream_record(f"primary/{seed}/{horizon_index}/{query_index}", seed, key))
    for horizon_index in range(len(CLOCK_DIAGNOSTIC_HORIZONS)):
        key = (1, horizon_index)
        streams.append(stream_record(f"clock/{horizon_index}", CLOCK_DIAGNOSTIC_SEED, key))
    streams.append(stream_record("constant/nonendpoint", CONSTANT_DIAGNOSTIC_SEED, (2, 0)))
    for endpoint_index in range(2):
        for horizon_index in range(len(HORIZONS)):
            key = (3, endpoint_index, horizon_index)
            streams.append(
                stream_record(
                    f"constant/endpoint/{endpoint_index}/{horizon_index}",
                    ENDPOINT_DIAGNOSTIC_SEED,
                    key,
                )
            )
    for horizon_index in range(len(PREFLIGHT_HORIZONS)):
        for query_index in range(len(PREFLIGHT_QUERIES)):
            key = (4, horizon_index, query_index)
            streams.append(stream_record(f"preflight/{horizon_index}/{query_index}", PREFLIGHT_SEED, key))
    return streams


def source_paths() -> list[Path]:
    relative = [
        "docs/research/runs/2026-09-28-dynamic-continuation/02d-two-barrier-experiment-protocol.md",
        "docs/research/runs/2026-09-28-dynamic-continuation/04l-two-barrier-voting.md",
        "docs/research/runs/2026-09-28-dynamic-continuation/04m-horizon-free-clock-proposal.md",
        "docs/research/runs/2026-09-28-dynamic-continuation/06f-moving-barrier-lean.md",
        "docs/research/runs/2026-09-28-dynamic-continuation/reviews/T30-two-barrier-voting-audit.md",
        "docs/research/runs/2026-09-28-dynamic-continuation/reviews/T31-horizon-free-clock-audit.md",
        "docs/research/runs/2026-09-28-dynamic-continuation/reviews/T34-two-barrier-protocol-review.md",
        "docs/research/runs/2026-09-28-dynamic-continuation/reviews/T34b-protocol-freeze-check.md",
        "docs/research/runs/2026-09-28-dynamic-continuation/numerics/two_barrier_sampler.py",
        "docs/research/runs/2026-09-28-dynamic-continuation/numerics/run_two_barrier.py",
        "docs/research/runs/2026-09-28-dynamic-continuation/numerics/test_two_barrier_sampler.py",
        "docs/research/runs/2026-09-28-dynamic-continuation/numerics/two_barrier_reference.py",
        "docs/research/runs/2026-09-28-dynamic-continuation/numerics/test_two_barrier_reference.py",
        "docs/research/runs/2026-09-28-dynamic-continuation/artifacts/two-barrier/reference-v1/execution_manifest.json",
        "docs/research/runs/2026-09-28-dynamic-continuation/artifacts/two-barrier/reference-v1/preflight.json",
        "docs/research/runs/2026-09-28-dynamic-continuation/artifacts/two-barrier/reference-v1/reference.npz",
        "docs/research/runs/2026-09-28-dynamic-continuation/artifacts/two-barrier/reference-v1/reference_summary.json",
        "docs/research/runs/2026-09-28-dynamic-continuation/artifacts/two-barrier/reference-v1/tests.log",
        "formal/EstimatorIntegrity/MovingBarrierWidth.lean",
        "docs/research/runs/2026-09-28-dynamic-continuation/lean/moving-barrier-width/build.log",
        "docs/research/runs/2026-09-28-dynamic-continuation/lean/moving-barrier-width/axioms.log",
        "docs/research/runs/2026-09-28-dynamic-continuation/lean/moving-barrier-width/source-scan.log",
    ]
    return [PROJECT_ROOT / item for item in relative]


def source_hashes() -> dict[str, str]:
    result: dict[str, str] = {}
    for path in source_paths():
        if not path.is_file():
            raise FileNotFoundError(f"required source/gate file is missing: {path}")
        result[str(path.relative_to(PROJECT_ROOT))] = sha256(path)
    return result


def verify_frozen_sources(manifest: dict[str, Any]) -> None:
    expected = manifest["source_and_gate_hashes_sha256"]
    actual = source_hashes()
    if actual != expected:
        changed = sorted(set(actual) | set(expected))
        detail = {
            key: {"expected": expected.get(key), "actual": actual.get(key)}
            for key in changed
            if expected.get(key) != actual.get(key)
        }
        raise RuntimeError(f"frozen source hash mismatch: {detail}")


def environment_record() -> dict[str, Any]:
    config_stream = io.StringIO()
    with contextlib.redirect_stdout(config_stream):
        np.show_config()
    clock_info = time.get_clock_info("monotonic")
    return {
        "python_executable": sys.executable,
        "python_version": sys.version,
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "byteorder": sys.byteorder,
        "numpy_version": np.__version__,
        "mpmath_version": mp.__version__,
        "numpy_float64": {
            "eps": np.finfo(np.float64).eps,
            "tiny": np.finfo(np.float64).tiny,
            "smallest_subnormal": np.nextafter(np.float64(0.0), np.float64(1.0)),
            "max": np.finfo(np.float64).max,
        },
        "numpy_configuration": config_stream.getvalue(),
        "monotonic_clock": {
            "implementation": clock_info.implementation,
            "monotonic": clock_info.monotonic,
            "adjustable": clock_info.adjustable,
            "resolution": clock_info.resolution,
        },
    }


def manifest_payload(unit_test: dict[str, Any]) -> dict[str, Any]:
    reference_files = [
        REFERENCE_ARTIFACT / "reference.npz",
        REFERENCE_ARTIFACT / "reference_summary.json",
    ]
    reference_snapshot = {
        str(path.relative_to(PROJECT_ROOT)): sha256(path)
        for path in reference_files
        if path.is_file()
    }
    return {
        "schema_version": 1,
        "artifact_version": "sampler-v1",
        "created_utc": utc_now(),
        "status": "frozen_before_diagnostics",
        "immutable_after_creation": True,
        "purpose": "fixed floating approximation of the reviewed two-barrier ideal sampler",
        "protocol": {
            "path": str(PROTOCOL_PATH.relative_to(PROJECT_ROOT)),
            "sha256": PROTOCOL_SHA256,
            "primary_horizons": HORIZONS.tolist(),
            "primary_queries": QUERIES.tolist(),
            "primary_seeds": list(PRIMARY_SEEDS),
            "roots_per_primary_cell": PRIMARY_ROOTS,
            "primary_cells": 63,
            "primary_roots": 630_000,
            "primary_cell_sampling_deadline_seconds": PRIMARY_CELL_SECONDS,
            "checkpoint_max_completed_roots": CHECKPOINT_ROOTS,
            "clock_diagnostic_horizons": CLOCK_DIAGNOSTIC_HORIZONS.tolist(),
            "clock_diagnostic_accepted_outcomes_per_horizon": CLOCK_DIAGNOSTIC_ROOTS,
            "constant_nonendpoint_roots": CONSTANT_DIAGNOSTIC_ROOTS,
            "constant_endpoint_roots_per_cell": ENDPOINT_DIAGNOSTIC_ROOTS,
            "fixed_full_pde_root_workload": 731_792,
            "fixed_standalone_accepted_clocks": 300_000,
            "range_tolerance": sampler.DEFAULT_RANGE_TOLERANCE,
            "dkw_threshold": DKW_THRESHOLD,
            "constant_mean_threshold": CONSTANT_MEAN_THRESHOLD,
            "statistical_diagnostic_alpha_each": STATISTICAL_ALPHA,
        },
        "rng_contract": {
            "seed_sequence": "numpy.random.SeedSequence(entropy=seed, spawn_key=key)",
            "bit_generator": "numpy.random.PCG64",
            "generator_uniform": "Generator.random binary64 in [0,1)",
            "open_interval_rule": "redraw exact zero and record it separately",
            "indices": "zero-based in the frozen listed orders",
            "streams": all_frozen_streams(),
        },
        "floating_contract": {
            "working_precision": "IEEE-754 binary64 through Python float/numpy.float64",
            "limiting_leaf_atom": "8/15",
            "limiting_event_probability": "7/15",
            "stable_d": "(1-U)*(1+zeta)/(1+zeta-U/2)",
            "event_q": "d/(20/9-3*d)",
            "finite_horizon_acceptance": "leaf or strict event s<T",
            "rounded_zeta_endpoint_tolerance": sampler.FLOAT_DOMAIN_TOLERANCE,
            "rounded_zeta_policy": "retain event; no clipping or dropping",
            "coefficient_limit_policy": "use A_c/2 only if exp(-2T) equals binary64 zero; record every use",
            "fixed_grid_has_representable_exp_minus_2T": True,
        },
        "preflight_contract": {
            "inverse_uniforms_decimal": [repr(value) for value in PREFLIGHT_INVERSE_UNIFORMS],
            "inverse_uniforms_hex": [value.hex() for value in PREFLIGHT_INVERSE_UNIFORMS],
            "independent_precision_decimal_digits": 100,
            "absolute_tolerance": PREFLIGHT_ABSOLUTE_TOLERANCE,
            "relative_tolerance": PREFLIGHT_RELATIVE_TOLERANCE,
            "acceptance": "for each inverse quantity, abs(error) <= atol + rtol*abs(high_precision_target)",
            "near_zero_note": "relative error is recorded but is not a standalone gate for the event time tending to zero at the leaf threshold",
            "remaining_time_direction": "nextafter(s,0) rejects; nextafter(s,+inf) accepts",
            "root_horizons": list(PREFLIGHT_HORIZONS),
            "root_queries": list(PREFLIGHT_QUERIES),
            "roots_per_case": PREFLIGHT_ROOTS_PER_CASE,
            "root_seed": PREFLIGHT_SEED,
            "root_spawn_keys": "(4,horizon_index,query_index)",
        },
        "source_and_gate_hashes_sha256": source_hashes(),
        "reference_snapshot_if_present_before_diagnostics": reference_snapshot,
        "reference_primary_gate": "required and separately frozen before primary execution",
        "development_unit_tests": unit_test,
        "commands": {
            "prepare": f"{sys.executable} {Path(__file__).name} prepare",
            "diagnostics": f"{sys.executable} {Path(__file__).name} diagnostics",
            "primary": f"{sys.executable} {Path(__file__).name} primary",
        },
        "scope": {
            "not_finite_bit_unbiasedness_certificate": True,
            "no_node_or_depth_cutoff": True,
            "no_clipping": True,
            "no_speedup_or_global_finite_bit_claim": True,
            "smooth_one_dimensional_datum_only": True,
        },
    }


def load_manifest() -> dict[str, Any]:
    path = SAMPLER_ARTIFACT / "execution_manifest.json"
    if not path.is_file():
        raise FileNotFoundError("prepare stage has not produced execution_manifest.json")
    with path.open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    if manifest["protocol"]["sha256"] != PROTOCOL_SHA256:
        raise RuntimeError("manifest protocol hash is not the immutable 02d hash")
    return manifest


def independent_scaled_defect(c: float, horizon: float) -> float:
    with mp.workdps(100):
        c_mp = mp.mpf(str(c))
        t_mp = mp.mpf(str(horizon))
        a_mp = c_mp**-2 - 1
        q_mp = mp.exp(-2 * t_mp)
        root_mp = mp.sqrt(1 + a_mp * q_mp)
        return float(a_mp / (root_mp * (1 + root_mp)))


def independent_clock_cdf(horizon: float, s: float) -> float:
    with mp.workdps(100):
        a_mp = mp.mpf(3)
        b_mp = mp.mpf(7) / 9

        def z_at(value: float) -> mp.mpf:
            q_mp = mp.exp(-2 * mp.mpf(str(value)))
            return mp.sqrt((1 + b_mp * q_mp) / (1 + a_mp * q_mp))

        def r_at(zeta: mp.mpf) -> mp.mpf:
            return zeta * zeta / (1 + zeta)

        return float(r_at(z_at(s)) / r_at(z_at(horizon)))


def _relative_error(actual: float, expected: float) -> float:
    if expected == 0.0:
        return abs(actual - expected)
    return abs(actual - expected) / abs(expected)


def run_preflight() -> dict[str, Any]:
    manifest = load_manifest()
    verify_frozen_sources(manifest)
    success_path = SAMPLER_ARTIFACT / "preflight_results.json"
    failure_path = SAMPLER_ARTIFACT / "preflight_failure.json"
    if success_path.exists() or failure_path.exists():
        raise FileExistsError("preflight evidence already exists; refusing rerun")

    started = time.monotonic()
    result: dict[str, Any] = {
        "schema_version": 1,
        "started_utc": utc_now(),
        "status": "running",
        "inverse_checks": [],
        "root_invariant_cases": [],
    }
    try:
        mp.mp.dps = 100
        for u in PREFLIGHT_INVERSE_UNIFORMS:
            actual = sampler.event_inverse_from_uniform(u)
            u_mp = mp.mpf(u)
            y_mp = u_mp / 2
            zeta_mp = (y_mp + mp.sqrt(y_mp * y_mp + 4 * y_mp)) / 2
            d_mp = (1 - u_mp) * (1 + zeta_mp) / (1 + zeta_mp - y_mp)
            q_mp = d_mp / (mp.mpf(20) / 9 - 3 * d_mp)
            s_mp = -mp.log(q_mp) / 2
            expected = {
                "zeta": float(zeta_mp),
                "stable_d": float(d_mp),
                "q_event": float(q_mp),
                "remaining_time": float(s_mp),
            }
            absolute_errors = {
                key: abs(getattr(actual, key) - value) for key, value in expected.items()
            }
            relative_errors = {
                key: _relative_error(getattr(actual, key), value)
                for key, value in expected.items()
            }
            forward_zeta = math.sqrt(
                (1.0 + (7.0 / 9.0) * math.exp(-2.0 * actual.remaining_time))
                / (1.0 + 3.0 * math.exp(-2.0 * actual.remaining_time))
            )
            below = math.nextafter(actual.remaining_time, 0.0)
            above = math.nextafter(actual.remaining_time, math.inf)
            combined_tolerance_passed = all(
                absolute_errors[key]
                <= PREFLIGHT_ABSOLUTE_TOLERANCE
                + PREFLIGHT_RELATIVE_TOLERANCE * abs(expected[key])
                for key in expected
            )
            passed = (
                combined_tolerance_passed
                and abs(forward_zeta - actual.zeta) <= PREFLIGHT_ABSOLUTE_TOLERANCE
                and not (actual.remaining_time < below)
                and actual.remaining_time < above
            )
            record = {
                "u_decimal": repr(u),
                "u_hex": u.hex(),
                "actual": asdict(actual),
                "independent_high_precision_rounded": expected,
                "absolute_errors": absolute_errors,
                "relative_errors": relative_errors,
                "combined_absolute_plus_relative_tolerance_passed": combined_tolerance_passed,
                "forward_reconstructed_zeta": forward_zeta,
                "strict_direction_below_rejects": not (actual.remaining_time < below),
                "strict_direction_above_accepts": actual.remaining_time < above,
                "passed": passed,
            }
            result["inverse_checks"].append(record)
            if not passed:
                raise RuntimeError(f"inverse preflight failed for U={u!r}")

        for horizon_index, horizon in enumerate(PREFLIGHT_HORIZONS):
            for query_index, query in enumerate(PREFLIGHT_QUERIES):
                key = (4, horizon_index, query_index)
                rng = make_rng(PREFLIGHT_SEED, key)
                initial_state = copy.deepcopy(rng.bit_generator.state)
                maxima = {field: 0 for field in ("nodes", "clock_proposals")}
                coefficient_limit_uses = 0
                for _ in range(PREFLIGHT_ROOTS_PER_CASE):
                    root = sampler.sample_root(rng, horizon, query)
                    sampler.validate_root_sample(root, horizon)
                    maxima["nodes"] = max(maxima["nodes"], root.nodes)
                    maxima["clock_proposals"] = max(
                        maxima["clock_proposals"], root.clock_proposals
                    )
                    coefficient_limit_uses += int(root.coefficient_limit_substitution)
                case = {
                    "horizon_index": horizon_index,
                    "query_index": query_index,
                    "horizon": horizon,
                    "query": query,
                    "entropy": PREFLIGHT_SEED,
                    "spawn_key": list(key),
                    "roots": PREFLIGHT_ROOTS_PER_CASE,
                    "initial_rng_state": initial_state,
                    "final_rng_state": copy.deepcopy(rng.bit_generator.state),
                    "maximum_nodes": maxima["nodes"],
                    "maximum_clock_proposals": maxima["clock_proposals"],
                    "coefficient_limit_substitutions": coefficient_limit_uses,
                    "passed": coefficient_limit_uses == 0,
                }
                result["root_invariant_cases"].append(case)
                if not case["passed"]:
                    raise RuntimeError("unexpected coefficient-limit use on frozen horizon grid")

        result.update(
            {
                "status": "passed",
                "finished_utc": utc_now(),
                "elapsed_seconds": time.monotonic() - started,
                "root_cases": len(result["root_invariant_cases"]),
                "roots_checked": len(result["root_invariant_cases"])
                * PREFLIGHT_ROOTS_PER_CASE,
            }
        )
        write_json_exclusive(success_path, result)
        return result
    except Exception as exc:
        result.update(
            {
                "status": "failed",
                "finished_utc": utc_now(),
                "elapsed_seconds": time.monotonic() - started,
                "exception_type": type(exc).__name__,
                "exception": str(exc),
                "traceback": traceback.format_exc(),
            }
        )
        write_json_exclusive(failure_path, result)
        raise


def prepare() -> None:
    if sha256(PROTOCOL_PATH) != PROTOCOL_SHA256:
        raise RuntimeError("immutable 02d protocol hash mismatch")
    if SAMPLER_ARTIFACT.exists():
        raise FileExistsError(f"refusing to overwrite {SAMPLER_ARTIFACT}")
    SAMPLER_ARTIFACT.mkdir(parents=True, exist_ok=False)

    command = [sys.executable, "-m", "unittest", "-v", "test_two_barrier_sampler.py"]
    completed = subprocess.run(
        command,
        cwd=NUMERICS_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    unit_log_path = SAMPLER_ARTIFACT / "development_unit_tests.log"
    with unit_log_path.open("x", encoding="utf-8") as handle:
        handle.write(completed.stdout)
        handle.flush()
        os.fsync(handle.fileno())
    unit_record = {
        "command": command,
        "exit_code": completed.returncode,
        "log": str(unit_log_path.relative_to(PROJECT_ROOT)),
        "log_sha256": sha256(unit_log_path),
    }
    if completed.returncode != 0:
        write_json_exclusive(
            SAMPLER_ARTIFACT / "prepare_failure.json",
            {
                "status": "failed",
                "stage": "development_unit_tests",
                "created_utc": utc_now(),
                "unit_test": unit_record,
            },
        )
        raise RuntimeError("development unit tests failed; evidence preserved")

    manifest = manifest_payload(unit_record)
    write_json_exclusive(SAMPLER_ARTIFACT / "execution_manifest.json", manifest)
    preflight = run_preflight()
    print(
        json.dumps(
            {
                "status": "prepared",
                "manifest": str(SAMPLER_ARTIFACT / "execution_manifest.json"),
                "preflight_status": preflight["status"],
                "preflight_roots": preflight["roots_checked"],
            },
            sort_keys=True,
        )
    )


def allocate_root_arrays(size: int) -> dict[str, np.ndarray]:
    return {
        "scaled_output": np.empty(size, dtype=np.float64),
        "normalized_output": np.empty(size, dtype=np.float64),
        "nodes": np.empty(size, dtype=np.int64),
        "leaves": np.empty(size, dtype=np.int64),
        "binary_internal": np.empty(size, dtype=np.int64),
        "ternary_internal": np.empty(size, dtype=np.int64),
        "clock_proposals": np.empty(size, dtype=np.int64),
        "clock_rejections": np.empty(size, dtype=np.int64),
        "zero_redraws": np.empty(size, dtype=np.int64),
        "coefficient_limit_substitution": np.empty(size, dtype=np.bool_),
    }


def store_root(arrays: dict[str, np.ndarray], index: int, root: sampler.RootSample) -> None:
    for field in ROOT_FIELDS:
        arrays[field][index] = getattr(root, field)


def root_array_prefix(arrays: dict[str, np.ndarray], completed: int) -> dict[str, np.ndarray]:
    return {field: values[:completed].copy() for field, values in arrays.items()}


def run_clock_diagnostic(
    diagnostics_dir: Path, horizon_index: int, horizon: float
) -> dict[str, Any]:
    rng = make_rng(CLOCK_DIAGNOSTIC_SEED, (1, horizon_index))
    initial_state = copy.deepcopy(rng.bit_generator.state)
    is_leaf = np.empty(CLOCK_DIAGNOSTIC_ROOTS, dtype=np.bool_)
    accepted_time = np.empty(CLOCK_DIAGNOSTIC_ROOTS, dtype=np.float64)
    accepted_zeta = np.empty(CLOCK_DIAGNOSTIC_ROOTS, dtype=np.float64)
    proposals = np.empty(CLOCK_DIAGNOSTIC_ROOTS, dtype=np.int64)
    rejections = np.empty(CLOCK_DIAGNOSTIC_ROOTS, dtype=np.int64)
    zero_redraws = np.empty(CLOCK_DIAGNOSTIC_ROOTS, dtype=np.int64)
    completed = 0
    started = time.monotonic()
    path = diagnostics_dir / f"clock_t{horizon_index}.npz"
    try:
        for index in range(CLOCK_DIAGNOSTIC_ROOTS):
            outcome = sampler.sample_finite_clock(rng, horizon)
            is_leaf[index] = outcome.is_leaf
            accepted_time[index] = outcome.remaining_time
            accepted_zeta[index] = outcome.zeta
            proposals[index] = outcome.proposals
            rejections[index] = outcome.rejections
            zero_redraws[index] = outcome.zero_redraws
            completed += 1
    except Exception:
        write_npz_exclusive(
            diagnostics_dir / f"clock_t{horizon_index}_failed_prefix.npz",
            is_leaf=is_leaf[:completed],
            accepted_time=accepted_time[:completed],
            accepted_zeta=accepted_zeta[:completed],
            proposals=proposals[:completed],
            rejections=rejections[:completed],
            zero_redraws=zero_redraws[:completed],
        )
        raise

    write_npz_exclusive(
        path,
        is_leaf=is_leaf,
        accepted_time=accepted_time,
        accepted_zeta=accepted_zeta,
        proposals=proposals,
        rejections=rejections,
        zero_redraws=zero_redraws,
    )
    fractions = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    points = horizon * fractions
    empirical = np.array([np.mean(accepted_time <= point) for point in points])
    theory = np.array([independent_clock_cdf(horizon, float(point)) for point in points])
    discrepancies = np.abs(empirical - theory)
    maximum = float(np.max(discrepancies))
    return {
        "horizon_index": horizon_index,
        "horizon": horizon,
        "entropy": CLOCK_DIAGNOSTIC_SEED,
        "spawn_key": [1, horizon_index],
        "roots": CLOCK_DIAGNOSTIC_ROOTS,
        "raw_npz": str(path.relative_to(PROJECT_ROOT)),
        "raw_npz_sha256": sha256(path),
        "initial_rng_state": initial_state,
        "final_rng_state": copy.deepcopy(rng.bit_generator.state),
        "zero_redraws": int(np.sum(zero_redraws)),
        "total_proposals": int(np.sum(proposals)),
        "total_rejections": int(np.sum(rejections)),
        "leaf_count": int(np.sum(is_leaf)),
        "cdf_fractions_of_horizon": fractions.tolist(),
        "cdf_points": points.tolist(),
        "empirical_cdf": empirical.tolist(),
        "independent_theory_cdf": theory.tolist(),
        "absolute_discrepancies": discrepancies.tolist(),
        "maximum_discrepancy": maximum,
        "threshold": DKW_THRESHOLD,
        "passed": maximum <= DKW_THRESHOLD,
        "elapsed_seconds": time.monotonic() - started,
    }


def run_constant_nonendpoint(diagnostics_dir: Path) -> dict[str, Any]:
    rng = make_rng(CONSTANT_DIAGNOSTIC_SEED, (2, 0))
    initial_state = copy.deepcopy(rng.bit_generator.state)
    arrays = allocate_root_arrays(CONSTANT_DIAGNOSTIC_ROOTS)
    oracle = sampler.constant_initial_value(5.0 / 8.0)
    completed = 0
    started = time.monotonic()
    path = diagnostics_dir / "constant_nonendpoint.npz"
    try:
        for index in range(CONSTANT_DIAGNOSTIC_ROOTS):
            root = sampler.sample_root(rng, 4.0, 0.0, initial_value=oracle)
            store_root(arrays, index, root)
            completed += 1
    except Exception:
        write_npz_exclusive(
            diagnostics_dir / "constant_nonendpoint_failed_prefix.npz",
            **root_array_prefix(arrays, completed),
        )
        raise

    write_npz_exclusive(path, **arrays)
    target = independent_scaled_defect(5.0 / 8.0, 4.0)
    mean = float(np.mean(arrays["scaled_output"]))
    discrepancy = abs(mean - target)
    return {
        "horizon": 4.0,
        "query": 0.0,
        "constant_initial_value": 5.0 / 8.0,
        "entropy": CONSTANT_DIAGNOSTIC_SEED,
        "spawn_key": [2, 0],
        "roots": CONSTANT_DIAGNOSTIC_ROOTS,
        "raw_npz": str(path.relative_to(PROJECT_ROOT)),
        "raw_npz_sha256": sha256(path),
        "initial_rng_state": initial_state,
        "final_rng_state": copy.deepcopy(rng.bit_generator.state),
        "sample_mean_scaled_output": mean,
        "sample_standard_deviation": float(np.std(arrays["scaled_output"], ddof=1)),
        "independent_scalar_target": target,
        "absolute_discrepancy": discrepancy,
        "threshold": CONSTANT_MEAN_THRESHOLD,
        "zero_redraws": int(np.sum(arrays["zero_redraws"])),
        "coefficient_limit_substitutions": int(
            np.sum(arrays["coefficient_limit_substitution"])
        ),
        "passed": discrepancy <= CONSTANT_MEAN_THRESHOLD,
        "elapsed_seconds": time.monotonic() - started,
    }


def run_endpoint_cell(
    diagnostics_dir: Path,
    endpoint_index: int,
    horizon_index: int,
    horizon: float,
) -> dict[str, Any]:
    value = (sampler.LOWER_BARRIER, sampler.UPPER_BARRIER)[endpoint_index]
    key = (3, endpoint_index, horizon_index)
    rng = make_rng(ENDPOINT_DIAGNOSTIC_SEED, key)
    initial_state = copy.deepcopy(rng.bit_generator.state)
    arrays = allocate_root_arrays(ENDPOINT_DIAGNOSTIC_ROOTS)
    oracle = sampler.constant_initial_value(value)
    completed = 0
    started = time.monotonic()
    path = diagnostics_dir / f"endpoint_e{endpoint_index}_t{horizon_index}.npz"
    try:
        for index in range(ENDPOINT_DIAGNOSTIC_ROOTS):
            root = sampler.sample_root(rng, horizon, 0.0, initial_value=oracle)
            store_root(arrays, index, root)
            completed += 1
    except Exception:
        write_npz_exclusive(
            diagnostics_dir / f"endpoint_e{endpoint_index}_t{horizon_index}_failed_prefix.npz",
            **root_array_prefix(arrays, completed),
        )
        raise

    write_npz_exclusive(path, **arrays)
    target = independent_scaled_defect(value, horizon)
    discrepancies = np.abs(arrays["scaled_output"] - target)
    maximum = float(np.max(discrepancies))
    return {
        "endpoint_index": endpoint_index,
        "horizon_index": horizon_index,
        "horizon": horizon,
        "query": 0.0,
        "constant_initial_value": value,
        "entropy": ENDPOINT_DIAGNOSTIC_SEED,
        "spawn_key": list(key),
        "roots": ENDPOINT_DIAGNOSTIC_ROOTS,
        "raw_npz": str(path.relative_to(PROJECT_ROOT)),
        "raw_npz_sha256": sha256(path),
        "initial_rng_state": initial_state,
        "final_rng_state": copy.deepcopy(rng.bit_generator.state),
        "independent_scalar_target": target,
        "maximum_absolute_discrepancy": maximum,
        "threshold": sampler.DEFAULT_RANGE_TOLERANCE,
        "zero_redraws": int(np.sum(arrays["zero_redraws"])),
        "coefficient_limit_substitutions": int(
            np.sum(arrays["coefficient_limit_substitution"])
        ),
        "passed": maximum <= sampler.DEFAULT_RANGE_TOLERANCE,
        "elapsed_seconds": time.monotonic() - started,
    }


def diagnostics() -> None:
    manifest = load_manifest()
    verify_frozen_sources(manifest)
    preflight_path = SAMPLER_ARTIFACT / "preflight_results.json"
    if not preflight_path.is_file():
        raise RuntimeError("passed deterministic preflight is required")
    with preflight_path.open(encoding="utf-8") as handle:
        if json.load(handle).get("status") != "passed":
            raise RuntimeError("deterministic preflight did not pass")

    diagnostics_dir = SAMPLER_ARTIFACT / "diagnostics"
    if diagnostics_dir.exists():
        raise FileExistsError("diagnostic artifact exists; refusing rerun")
    diagnostics_dir.mkdir(parents=False, exist_ok=False)
    started = time.monotonic()
    result: dict[str, Any] = {
        "schema_version": 1,
        "started_utc": utc_now(),
        "status": "running",
        "clock_diagnostics": [],
        "endpoint_diagnostics": [],
    }
    try:
        for horizon_index, horizon in enumerate(CLOCK_DIAGNOSTIC_HORIZONS):
            clock_result = run_clock_diagnostic(
                diagnostics_dir, horizon_index, float(horizon)
            )
            result["clock_diagnostics"].append(clock_result)
            if not clock_result["passed"]:
                raise RuntimeError(
                    f"prespecified clock diagnostic failed at T={horizon}"
                )

        constant_result = run_constant_nonendpoint(diagnostics_dir)
        result["constant_nonendpoint_diagnostic"] = constant_result
        if not constant_result["passed"]:
            raise RuntimeError("prespecified nonendpoint constant diagnostic failed")

        for endpoint_index in range(2):
            for horizon_index, horizon in enumerate(HORIZONS):
                endpoint_result = run_endpoint_cell(
                    diagnostics_dir,
                    endpoint_index,
                    horizon_index,
                    float(horizon),
                )
                result["endpoint_diagnostics"].append(endpoint_result)
                if not endpoint_result["passed"]:
                    raise RuntimeError(
                        "prespecified pathwise endpoint diagnostic failed at "
                        f"endpoint={endpoint_index}, T={horizon}"
                    )

        result.update(
            {
                "status": "passed",
                "finished_utc": utc_now(),
                "elapsed_seconds": time.monotonic() - started,
                "official_pde_roots": CONSTANT_DIAGNOSTIC_ROOTS
                + 2 * len(HORIZONS) * ENDPOINT_DIAGNOSTIC_ROOTS,
                "official_standalone_accepted_clocks": len(CLOCK_DIAGNOSTIC_HORIZONS)
                * CLOCK_DIAGNOSTIC_ROOTS,
                "ideal_union_false_alarm_bound": 4.0e-6,
                "scope": {
                    "finite_grid_diagnostic_not_distributional_proof": True,
                    "not_floating_bias_certificate": True,
                },
            }
        )
        write_json_exclusive(SAMPLER_ARTIFACT / "diagnostics_summary.json", result)
        print(json.dumps({"status": "diagnostics_passed", "elapsed_seconds": result["elapsed_seconds"]}, sort_keys=True))
    except Exception as exc:
        result.update(
            {
                "status": "failed",
                "finished_utc": utc_now(),
                "elapsed_seconds": time.monotonic() - started,
                "exception_type": type(exc).__name__,
                "exception": str(exc),
                "traceback": traceback.format_exc(),
            }
        )
        write_json_exclusive(SAMPLER_ARTIFACT / "diagnostics_failure.json", result)
        raise


def load_reference_gate() -> tuple[np.ndarray, dict[str, Any]]:
    summary_path = REFERENCE_ARTIFACT / "reference_summary.json"
    array_path = REFERENCE_ARTIFACT / "reference.npz"
    if not summary_path.is_file() or not array_path.is_file():
        raise FileNotFoundError("independent reference-v1 artifact is incomplete")
    with summary_path.open(encoding="utf-8") as handle:
        summary = json.load(handle)
    gates = summary.get("gates", {})
    required_gates = (
        "passed",
        "all_six_solver_runs_succeeded",
        "refinement_passed",
        "preflight_passed",
        "all_output_shapes_match",
    )
    if summary.get("status") != "PASS" or not all(
        gates.get(name) is True for name in required_gates
    ):
        raise RuntimeError("independent reference summary does not satisfy every frozen gate")
    with np.load(array_path, allow_pickle=False) as archive:
        required = {"times", "queries", "scaled_values"}
        if not required.issubset(archive.files):
            raise RuntimeError(f"reference.npz lacks keys {sorted(required - set(archive.files))}")
        times = archive["times"]
        queries = archive["queries"]
        scaled_values = archive["scaled_values"]
    if times.shape != (7,) or queries.shape != (3,) or scaled_values.shape != (7, 3):
        raise RuntimeError("reference.npz does not satisfy the frozen shape interface")
    if not np.array_equal(times, HORIZONS) or not np.array_equal(queries, QUERIES):
        raise RuntimeError("reference.npz grids differ from the frozen protocol")
    if not (np.all(np.isfinite(scaled_values)) and np.all(scaled_values > 0.0)):
        raise RuntimeError("strict reference values are not finite positive")
    reference_record = summary.get("reference", {})
    if not (
        np.array_equal(np.asarray(reference_record.get("times")), times)
        and np.array_equal(np.asarray(reference_record.get("queries")), queries)
        and np.array_equal(
            np.asarray(reference_record.get("scaled_values")), scaled_values
        )
        and reference_record.get("producer_key") == "k64_strict"
    ):
        raise RuntimeError("reference summary arrays do not match reference.npz")
    return scaled_values.copy(), {
        "summary_path": str(summary_path.relative_to(PROJECT_ROOT)),
        "summary_sha256": sha256(summary_path),
        "array_path": str(array_path.relative_to(PROJECT_ROOT)),
        "array_sha256": sha256(array_path),
        "summary_status": summary.get("status"),
        "gates": gates,
        "predesignated_comparator": summary.get("predesignated_comparator"),
        "interface_shapes": {"times": [7], "queries": [3], "scaled_values": [7, 3]},
    }


def flush_checkpoint(
    cell_dir: Path,
    chunk_index: int,
    start_root: int,
    arrays: dict[str, list[Any]],
) -> tuple[Path, float]:
    processing_started = time.monotonic()
    path = cell_dir / f"chunk_{chunk_index:03d}_{start_root:05d}_{start_root + len(arrays['scaled_output']):05d}.npz"
    payload = {
        field: np.asarray(
            values,
            dtype=np.bool_ if field == "coefficient_limit_substitution" else (
                np.float64 if field in ("scaled_output", "normalized_output") else np.int64
            ),
        )
        for field, values in arrays.items()
    }
    write_npz_exclusive(path, **payload)
    return path, time.monotonic() - processing_started


def sample_primary_cell(
    primary_dir: Path,
    reference_value: float,
    seed: int,
    horizon_index: int,
    query_index: int,
) -> dict[str, Any]:
    horizon = float(HORIZONS[horizon_index])
    query = float(QUERIES[query_index])
    key = (0, horizon_index, query_index)
    rng = make_rng(seed, key)
    initial_state = copy.deepcopy(rng.bit_generator.state)
    cell_dir = primary_dir / f"seed_{seed}" / f"t{horizon_index}_x{query_index}"
    cell_dir.mkdir(parents=True, exist_ok=False)

    buffer: dict[str, list[Any]] = {field: [] for field in ROOT_FIELDS}
    completed = 0
    chunk_index = 0
    sampling_seconds = 0.0
    processing_io_seconds = 0.0
    chunk_records: list[dict[str, Any]] = []
    status = "running"
    unfinished_root_index: int | None = None
    exception_record: dict[str, str] | None = None

    while completed < PRIMARY_ROOTS:
        remaining_budget = PRIMARY_CELL_SECONDS - sampling_seconds
        if remaining_budget <= 0.0:
            status = "incomplete_deadline"
            unfinished_root_index = completed
            break
        segment_start = time.monotonic()
        try:
            root = sampler.sample_root(
                rng,
                horizon,
                query,
                deadline=segment_start + remaining_budget,
            )
        except sampler.SamplingDeadlineExceeded:
            sampling_seconds += time.monotonic() - segment_start
            status = "incomplete_deadline"
            unfinished_root_index = completed
            break
        except Exception as exc:
            sampling_seconds += time.monotonic() - segment_start
            status = "failed"
            unfinished_root_index = completed
            exception_record = {
                "exception_type": type(exc).__name__,
                "exception": str(exc),
                "traceback": traceback.format_exc(),
            }
            break
        sampling_seconds += time.monotonic() - segment_start
        for field in ROOT_FIELDS:
            buffer[field].append(getattr(root, field))
        completed += 1

        if len(buffer["scaled_output"]) == CHECKPOINT_ROOTS:
            start_root = completed - len(buffer["scaled_output"])
            path, elapsed = flush_checkpoint(
                cell_dir, chunk_index, start_root, buffer
            )
            processing_io_seconds += elapsed
            chunk_records.append(
                {
                    "path": str(path.relative_to(PROJECT_ROOT)),
                    "sha256": sha256(path),
                    "start_root": start_root,
                    "completed_roots": completed,
                }
            )
            chunk_index += 1
            buffer = {field: [] for field in ROOT_FIELDS}

    if buffer["scaled_output"]:
        start_root = completed - len(buffer["scaled_output"])
        path, elapsed = flush_checkpoint(cell_dir, chunk_index, start_root, buffer)
        processing_io_seconds += elapsed
        chunk_records.append(
            {
                "path": str(path.relative_to(PROJECT_ROOT)),
                "sha256": sha256(path),
                "start_root": start_root,
                "completed_roots": completed,
            }
        )

    if status == "running":
        status = "complete"

    # Reading the completed chunks is post-sampling processing and cannot
    # consume the 120-second operational sampling budget.
    processing_started = time.monotonic()
    collected = {field: [] for field in ROOT_FIELDS}
    for record in chunk_records:
        with np.load(PROJECT_ROOT / record["path"], allow_pickle=False) as archive:
            for field in ROOT_FIELDS:
                collected[field].append(archive[field])
    merged = {
        field: np.concatenate(parts) if parts else np.empty(0)
        for field, parts in collected.items()
    }
    processing_io_seconds += time.monotonic() - processing_started

    summary: dict[str, Any] = {
        "status": status,
        "seed": seed,
        "horizon_index": horizon_index,
        "query_index": query_index,
        "horizon": horizon,
        "query": query,
        "entropy": seed,
        "spawn_key": list(key),
        "requested_roots": PRIMARY_ROOTS,
        "completed_roots": completed,
        "unfinished_root_index": unfinished_root_index,
        "initial_rng_state": initial_state,
        "final_rng_state": copy.deepcopy(rng.bit_generator.state),
        "checkpoint_chunks": chunk_records,
        "sampling_seconds": sampling_seconds,
        "processing_and_io_seconds": processing_io_seconds,
        "sampling_deadline_seconds": PRIMARY_CELL_SECONDS,
        "sampling_deadline_excludes_processing_and_io": True,
        "reference_scaled_value": reference_value,
    }
    if completed:
        scaled = merged["scaled_output"]
        mean = float(np.mean(scaled))
        std = float(np.std(scaled, ddof=1)) if completed > 1 else 0.0
        summary.update(
            {
                "sample_mean_scaled_output": mean,
                "within_root_standard_deviation": std,
                "within_root_relative_standard_deviation": std / mean,
                "signed_relative_error": (mean - reference_value) / reference_value,
                "physical_defect": math.exp(-2.0 * horizon) * mean,
                "physical_defect_log": math.log(mean) - 2.0 * horizon,
                "mean_nodes": float(np.mean(merged["nodes"])),
                "maximum_nodes": int(np.max(merged["nodes"])),
                "mean_clock_proposals": float(np.mean(merged["clock_proposals"])),
                "maximum_clock_proposals": int(np.max(merged["clock_proposals"])),
                "total_zero_redraws": int(np.sum(merged["zero_redraws"])),
                "coefficient_limit_substitutions": int(
                    np.sum(merged["coefficient_limit_substitution"])
                ),
            }
        )
    if exception_record is not None:
        summary.update(exception_record)
    write_json_exclusive(cell_dir / "cell_summary.json", summary)
    return summary


def primary() -> None:
    manifest = load_manifest()
    verify_frozen_sources(manifest)
    diagnostics_path = SAMPLER_ARTIFACT / "diagnostics_summary.json"
    if not diagnostics_path.is_file():
        raise RuntimeError("passed official diagnostics are required before primary")
    with diagnostics_path.open(encoding="utf-8") as handle:
        diagnostic_summary = json.load(handle)
    if diagnostic_summary.get("status") != "passed":
        raise RuntimeError("official diagnostics did not pass")

    reference_values, reference_gate = load_reference_gate()
    primary_dir = SAMPLER_ARTIFACT / "primary"
    if primary_dir.exists():
        raise FileExistsError("primary artifact exists; refusing rerun")
    gate_path = SAMPLER_ARTIFACT / "primary_gate.json"
    if gate_path.exists():
        raise FileExistsError("primary gate artifact already exists; refusing rerun")
    gate = {
        "schema_version": 1,
        "created_utc": utc_now(),
        "status": "passed",
        "protocol_sha256": PROTOCOL_SHA256,
        "sampler_manifest_sha256": sha256(SAMPLER_ARTIFACT / "execution_manifest.json"),
        "preflight_results_sha256": sha256(SAMPLER_ARTIFACT / "preflight_results.json"),
        "diagnostics_summary_sha256": sha256(diagnostics_path),
        "frozen_source_hashes_verified": True,
        "reference": reference_gate,
    }
    write_json_exclusive(gate_path, gate)

    primary_dir.mkdir(parents=False, exist_ok=False)
    started_utc = utc_now()
    started = time.monotonic()
    summaries: list[dict[str, Any]] = []
    failure: dict[str, Any] | None = None
    try:
        for seed in PRIMARY_SEEDS:
            for horizon_index in range(len(HORIZONS)):
                for query_index in range(len(QUERIES)):
                    summary = sample_primary_cell(
                        primary_dir,
                        float(reference_values[horizon_index, query_index]),
                        seed,
                        horizon_index,
                        query_index,
                    )
                    summaries.append(summary)
                    if summary["status"] == "failed":
                        raise RuntimeError(
                            "primary cell failed; affected execution stopped with evidence preserved"
                        )

        complete = [item for item in summaries if item["status"] == "complete"]
        rms_rows: list[dict[str, Any]] = []
        for horizon_index, horizon in enumerate(HORIZONS):
            for query_index, query in enumerate(QUERIES):
                cells = [
                    item
                    for item in complete
                    if item["horizon_index"] == horizon_index
                    and item["query_index"] == query_index
                ]
                if len(cells) == len(PRIMARY_SEEDS):
                    errors = [item["signed_relative_error"] for item in cells]
                    rms_rows.append(
                        {
                            "horizon_index": horizon_index,
                            "query_index": query_index,
                            "horizon": float(horizon),
                            "query": float(query),
                            "signed_relative_errors_by_seed": {
                                str(item["seed"]): item["signed_relative_error"]
                                for item in cells
                            },
                            "empirical_three_seed_rms": math.sqrt(
                                sum(error * error for error in errors) / 3.0
                            ),
                        }
                    )

        seed_sampling_times = {
            str(seed): sum(
                item["sampling_seconds"] for item in summaries if item["seed"] == seed
            )
            for seed in PRIMARY_SEEDS
        }
        result = {
            "schema_version": 1,
            "status": "complete" if len(complete) == 63 else "incomplete",
            "started_utc": started_utc,
            "finished_utc": utc_now(),
            "total_elapsed_seconds": time.monotonic() - started,
            "cells_requested": 63,
            "cells_complete": len(complete),
            "cells_incomplete": 63 - len(complete),
            "roots_requested": 630_000,
            "roots_completed": sum(item["completed_roots"] for item in summaries),
            "cell_summaries": summaries,
            "per_time_query_three_seed_errors": rms_rows,
            "sampling_seconds_by_seed_for_all_21_queries": seed_sampling_times,
            "fixed_timing_comparison": {
                "predesignated_reference_comparator": reference_gate[
                    "predesignated_comparator"
                ],
                "sampler_sampling_seconds_by_seed_for_all_21_queries": seed_sampling_times,
                "reference_validation_costs_remain_separate": True,
                "not_equal_accuracy_optimization": True,
                "no_speedup_or_general_superiority_inference": True,
            },
            "theoretical_ideal_bounds": {
                "relative_variance": 100.0 / 189.0,
                "ensemble_relative_rms_N_10000": math.sqrt(100.0 / (189.0 * 10_000.0)),
                "mean_nodes": 25.0 * math.sqrt(6.0) / 16.0 - 1.0,
                "mean_clock_proposals": (15.0 / 8.0)
                * (25.0 * math.sqrt(6.0) / 16.0 - 1.0),
                "expectations_not_sample_caps": True,
            },
            "scope": {
                "three_seed_rms_is_diagnostic_only": True,
                "not_equal_accuracy_optimization": True,
                "no_speedup_claim": True,
                "no_all_horizon_numerical_proof": True,
                "no_floating_unbiasedness_certificate": True,
            },
        }
        write_json_exclusive(SAMPLER_ARTIFACT / "primary_summary.json", result)
        print(json.dumps({"status": result["status"], "roots_completed": result["roots_completed"]}, sort_keys=True))
    except Exception as exc:
        failure = {
            "schema_version": 1,
            "status": "failed",
            "finished_utc": utc_now(),
            "elapsed_seconds": time.monotonic() - started,
            "cells_recorded": len(summaries),
            "roots_completed": sum(item["completed_roots"] for item in summaries),
            "cell_summaries": summaries,
            "exception_type": type(exc).__name__,
            "exception": str(exc),
            "traceback": traceback.format_exc(),
        }
        write_json_exclusive(SAMPLER_ARTIFACT / "primary_failure.json", failure)
        raise


def status() -> None:
    payload: dict[str, Any] = {
        "artifact": str(SAMPLER_ARTIFACT),
        "exists": SAMPLER_ARTIFACT.exists(),
    }
    if SAMPLER_ARTIFACT.exists():
        payload["files"] = sorted(
            str(path.relative_to(SAMPLER_ARTIFACT))
            for path in SAMPLER_ARTIFACT.rglob("*")
            if path.is_file()
        )
    print(json.dumps(payload, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("prepare", "diagnostics", "primary", "status"))
    args = parser.parse_args()
    if args.stage == "prepare":
        prepare()
    elif args.stage == "diagnostics":
        diagnostics()
    elif args.stage == "primary":
        primary()
    else:
        status()


if __name__ == "__main__":
    main()
