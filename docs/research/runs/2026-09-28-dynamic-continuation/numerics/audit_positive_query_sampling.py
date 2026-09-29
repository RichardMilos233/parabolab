"""Independent audit of the frozen positive-query sampling experiment.

This module deliberately does not import the producer.  Its phases are ordered:

1. ``prepare`` freezes this source, every audit input, and the exact replay set.
2. ``stored`` audits all archived outputs and computes statistics without calls.
3. ``replay`` executes only replicate 0 of all 180 cells, once.
4. ``plot`` creates the prespecified scientific figure after a passing replay.
5. ``finalize`` hashes every audit output and the independent review.
"""

from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import time
import traceback
from typing import Any, Iterable

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO = HERE.parents[4]
SOURCE = Path(__file__).resolve()
PRODUCER = HERE / "positive_query_sampling.py"
PROTOCOL = RUN_DIR / "02g-positive-query-sampling-protocol.md"
IMPLEMENTATION_REPORT = RUN_DIR / "reviews" / "T63v2-positive-sampling-implementation.md"
CLEARANCE = RUN_DIR / "reviews" / "T63v2-root-official-clearance.json"
INITIAL_HASHES = RUN_DIR / "initial-source-hashes.json"
V2 = RUN_DIR / "artifacts" / "positive-query-sampling" / "v2"
V1 = RUN_DIR / "artifacts" / "positive-query-sampling" / "v1"
MANIFEST = V2 / "execution_manifest.json"
PREFLIGHT = V2 / "preflight_result.json"
OFFICIAL = V2 / "official"
OFFICIAL_RESULT = OFFICIAL / "official_result.json"
OFFICIAL_LEDGER = OFFICIAL / "activity.jsonl"

AUDIT_DIR = RUN_DIR / "artifacts" / "positive-query-sampling" / "audit-v1"
AUDIT_MANIFEST = AUDIT_DIR / "audit_manifest.json"
STORED_RESULT = AUDIT_DIR / "stored_audit.json"
STORED_FAILURE = AUDIT_DIR / "stored_audit_failure.json"
RAW_STATS = AUDIT_DIR / "statistics_raw.npz"
REPLAY_LEDGER = AUDIT_DIR / "replay_activity.jsonl"
REPLAY_JOURNAL = AUDIT_DIR / "replay_journal.jsonl"
REPLAY_RESULT = AUDIT_DIR / "replay_result.json"
REPLAY_FAILURE = AUDIT_DIR / "replay_failure.json"
PLOT_PNG = AUDIT_DIR / "positive_query_audit.png"
PLOT_SVG = AUDIT_DIR / "positive_query_audit.svg"
PLOT_RESULT = AUDIT_DIR / "plot_result.json"
FINAL_AUDIT = AUDIT_DIR / "audit_result.json"
REVIEW = RUN_DIR / "reviews" / "T66-positive-query-independent-audit.md"

EXPECTED = {
    "producer_sha256": "81eb2b122d325eca97d144adc00380114558c5ad35a830d9d4062fa95f63df08",
    "manifest_sha256": "9417c6dc18b3c761ee7cdf38c4cc8ececbfc048c0869b0fea5b96acaaae47bd5",
    "preflight_sha256": "ae85c9f1712ada9697bedc472ea273bf692b2cc7c4f0813f58a63ce085380c1c",
    "protocol_sha256": "8713593424011f0cb713e19125bccfff1dacf25e9ce401c68ff6867aa8c9fe9b",
    "implementation_report_sha256": "4f7959a3b673bf1af78ade163ae13276afb72d243d2b85b72a232731c9b9839d",
    "clearance_sha256": "bec557a2ac4333151c40b04c69a62b3b422ffdb6b94873c57048b6f150e8b9a9",
    "official_result_sha256": "818f4f54da86417d1d3df139bbe717d58e371fc8c97acbffcdf73e6bbb064ac3",
}
HORIZONS = (12, 16, 20)
LEVELS = (0.0, 0.25, 1.0, 4.0)
SEEDS = (20260928, 20260929, 20260930)
SCHEDULES = (
    ("growing_0p125", 128),
    ("growing_0p5", 128),
    ("growing_2", 128),
    ("theorem_96", 8),
    ("fixed_51", 128),
)
N_TABLE = {
    12: (51, 202, 807, 38_730, 51),
    16: (373, 1_491, 5_962, 286_172, 51),
    20: (2_754, 11_014, 44_053, 2_114_541, 51),
}
BATCH = 131_072
EXPECTED_CELLS = 180
EXPECTED_OUTPUTS = 18_720
EXPECTED_OFFICIAL_CALLS = 336_883_488
EXPECTED_PRIOR_CALLS = 1_311_266
EXPECTED_SPENT_BEFORE_REPLAY = 338_194_754
EXPECTED_REPLAY_CALLS = 30_075_636
EXPECTED_SPENT_AFTER_REPLAY = 368_270_390
CAP = 500_000_000
SHIFT = 17.0 / 20.0
PDE_BIAS = 1.0 / 32.0


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def rel(path: Path) -> str:
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


def append_json(stream: Any, value: Any) -> None:
    stream.write(json.dumps(jsonable(value), sort_keys=True, allow_nan=False) + "\n")
    stream.flush()
    os.fsync(stream.fileno())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def json_lines(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                yield json.loads(line)
            except json.JSONDecodeError as error:
                raise AuditFailure(f"invalid JSON at {path}:{line_number}: {error}") from error


def same_float(left: float, right: float) -> bool:
    return np.float64(left).view(np.uint64).item() == np.float64(right).view(np.uint64).item()


def state_of(bit_generator: np.random.PCG64) -> dict[str, Any]:
    return copy.deepcopy(jsonable(bit_generator.state))


def cell_name(si: int, ti: int, zi: int, qi: int) -> str:
    return f"seed-{si:02d}_T-{ti:02d}_z-{zi:02d}_schedule-{qi:02d}"


def batches(n: int) -> tuple[int, ...]:
    return tuple([BATCH] * (n // BATCH) + ([n % BATCH] if n % BATCH else []))


def fixed_inputs() -> list[Path]:
    paths = {
        PRODUCER,
        PROTOCOL,
        IMPLEMENTATION_REPORT,
        CLEARANCE,
        INITIAL_HASHES,
        MANIFEST,
        PREFLIGHT,
    }
    paths.update(path for path in V1.rglob("*") if path.is_file())
    paths.update(path for path in V2.iterdir() if path.is_file())
    paths.update(path for path in OFFICIAL.rglob("*") if path.is_file())
    return sorted(paths)


def cumulative_ledger(path: Path, expected_phase: str) -> dict[str, int]:
    rows = 0
    total = 0
    for row in json_lines(path):
        rows += 1
        increment = int(row["point_calls"])
        require(increment >= 0, f"negative ledger increment: {path}:{rows}")
        total += increment
        require(row["phase"] == expected_phase, f"ledger phase: {path}:{rows}")
        require(int(row["cumulative_point_calls"]) == total, f"ledger cumulative: {path}:{rows}")
    return {"rows": rows, "point_calls": total}


def verify_declared_bindings() -> dict[str, Any]:
    actual = {
        "producer_sha256": sha256(PRODUCER),
        "manifest_sha256": sha256(MANIFEST),
        "preflight_sha256": sha256(PREFLIGHT),
        "protocol_sha256": sha256(PROTOCOL),
        "implementation_report_sha256": sha256(IMPLEMENTATION_REPORT),
        "clearance_sha256": sha256(CLEARANCE),
        "official_result_sha256": sha256(OFFICIAL_RESULT),
    }
    require(actual == EXPECTED, f"declared hash mismatch: {actual}")
    manifest = load_json(MANIFEST)
    preflight = load_json(PREFLIGHT)
    clearance = load_json(CLEARANCE)
    official = load_json(OFFICIAL_RESULT)
    require(preflight["status"] == "PASS", "preflight is not PASS")
    require(clearance["status"] == "CLEARED for official positive-query run", "clearance absent")
    require(official["status"] == "PASS", "official result is not PASS")
    require(clearance["manifest_sha256"] == actual["manifest_sha256"], "clearance manifest binding")
    require(clearance["implementation_source_sha256"] == actual["producer_sha256"], "clearance source binding")
    require(clearance["preflight_result_sha256"] == actual["preflight_sha256"], "clearance preflight binding")
    require(official["manifest_sha256"] == actual["manifest_sha256"], "official manifest binding")
    require(official["implementation_source_sha256"] == actual["producer_sha256"], "official source binding")
    require(official["preflight_result_sha256"] == actual["preflight_sha256"], "official preflight binding")
    require(official["clearance_sha256"] == actual["clearance_sha256"], "official clearance binding")
    require(official["completed_cells"] == EXPECTED_CELLS, "official cell total")
    require(official["completed_outputs"] == EXPECTED_OUTPUTS, "official output total")
    require(official["actual_point_calls"] == EXPECTED_OFFICIAL_CALLS, "official call total")
    require(manifest["protected_initial_sources"]["passed"] is True, "manifest protected-source result")
    require(manifest["protected_initial_sources"]["recorded_count"] == 342, "manifest protected-source count")
    activity = {
        "v1_preflight": cumulative_ledger(V1 / "preflight_activity.jsonl", "preflight"),
        "v2_preflight": cumulative_ledger(V2 / "preflight_activity.jsonl", "preflight"),
        "v2_official": cumulative_ledger(OFFICIAL_LEDGER, "official"),
    }
    require(activity["v1_preflight"] == {"rows": 220, "point_calls": 655_633}, "v1 activity ledger")
    require(activity["v2_preflight"] == {"rows": 220, "point_calls": 655_633}, "v2 activity ledger")
    require(activity["v2_official"]["point_calls"] == EXPECTED_OFFICIAL_CALLS, "official activity ledger")
    require(sum(row["point_calls"] for row in activity.values()) == EXPECTED_SPENT_BEFORE_REPLAY, "all-version activity before replay")
    return {"actual_hashes": actual, "manifest": manifest, "official": official, "activity": activity}


def verify_protected_inputs() -> dict[str, Any]:
    expected = load_json(INITIAL_HASHES)
    require(len(expected) == 342, "protected source list does not contain 342 entries")
    mismatches = []
    missing = []
    for name, expected_hash in expected.items():
        path = REPO / name
        if not path.is_file():
            missing.append(name)
        else:
            actual = sha256(path)
            if actual != expected_hash:
                mismatches.append({"path": name, "expected": expected_hash, "actual": actual})
    require(not missing and not mismatches, f"protected source failure: missing={missing}, mismatches={mismatches}")
    return {"recorded_count": len(expected), "missing": missing, "mismatches": mismatches, "passed": True}


def prepare() -> None:
    require(not AUDIT_DIR.exists(), f"audit directory already exists: {AUDIT_DIR}")
    bindings = verify_declared_bindings()
    protected = verify_protected_inputs()
    files = fixed_inputs()
    require(len(files) == len(set(files)), "duplicate audit input")
    replay = []
    replay_calls = 0
    for si, seed in enumerate(SEEDS):
        for ti, horizon in enumerate(HORIZONS):
            for zi, level in enumerate(LEVELS):
                for qi, (schedule, repetitions) in enumerate(SCHEDULES):
                    n = N_TABLE[horizon][qi]
                    replay.append({
                        "cell": cell_name(si, ti, zi, qi),
                        "seed_root": seed,
                        "T": horizon,
                        "nominal_z": level,
                        "schedule": schedule,
                        "repetitions_in_official_cell": repetitions,
                        "replicate_index": 0,
                        "spawn_key": [ti, zi, qi, 0],
                        "n": n,
                    })
                    replay_calls += n
    require(len(replay) == EXPECTED_CELLS, "replay cell count")
    require(replay_calls == EXPECTED_REPLAY_CALLS, "replay call count")
    require(EXPECTED_SPENT_BEFORE_REPLAY + replay_calls == EXPECTED_SPENT_AFTER_REPLAY <= CAP, "activity cap")
    AUDIT_DIR.mkdir(parents=True, exist_ok=False)
    write_json_new(AUDIT_MANIFEST, {
        "schema_version": 1,
        "status": "FROZEN BEFORE ANY AUDIT REPLAY ORACLE CALL",
        "created_utc": utc_now(),
        "audit_source": rel(SOURCE),
        "audit_source_sha256": sha256(SOURCE),
        "input_hashes_sha256": {rel(path): sha256(path) for path in files},
        "declared_bindings": bindings["actual_hashes"],
        "protected_initial_sources": protected,
        "exact_replay_subset": replay,
        "replay_selection_rule": "replicate_index=0 of every one of the 180 frozen cells; fixed before results",
        "replay_cells": len(replay),
        "replay_point_calls": replay_calls,
        "actual_spent_before_replay": EXPECTED_SPENT_BEFORE_REPLAY,
        "planned_spent_after_replay": EXPECTED_SPENT_AFTER_REPLAY,
        "whole_activity_cap": CAP,
        "full_replay_authorized": False,
        "automatic_retry_authorized": False,
        "environment": {
            "python_executable": sys.executable,
            "python_version": sys.version,
            "numpy_version": np.__version__,
            "matplotlib_version": matplotlib.__version__,
            "platform": platform.platform(),
            "machine": platform.machine(),
        },
    })
    print(json.dumps({"status": "PREPARED", "audit_manifest_sha256": sha256(AUDIT_MANIFEST), "replay_calls_so_far": 0}, indent=2))


def verify_frozen() -> dict[str, Any]:
    frozen = load_json(AUDIT_MANIFEST)
    require(frozen["status"] == "FROZEN BEFORE ANY AUDIT REPLAY ORACLE CALL", "audit manifest status")
    require(frozen["audit_source_sha256"] == sha256(SOURCE), "audit source changed after freeze")
    for name, expected_hash in frozen["input_hashes_sha256"].items():
        require(sha256(REPO / name) == expected_hash, f"frozen audit input changed: {name}")
    require(frozen["replay_cells"] == EXPECTED_CELLS, "frozen replay cell count")
    require(frozen["replay_point_calls"] == EXPECTED_REPLAY_CALLS, "frozen replay calls")
    return frozen


def expected_rng_states(seed_root: int, key: tuple[int, int, int, int], n: int) -> tuple[dict[str, Any], dict[str, Any]]:
    bitgen = np.random.PCG64(np.random.SeedSequence(seed_root, spawn_key=key))
    before = state_of(bitgen)
    bitgen.advance(n)
    after = state_of(bitgen)
    return before, after


def stats(outputs: list[float], reference: float) -> dict[str, Any]:
    errors = [value - reference for value in outputs]
    squares = [error * error for error in errors]
    mse = math.fsum(squares) / len(squares)
    rms = math.sqrt(mse)
    return {
        "replications": len(outputs),
        "bias": math.fsum(errors) / len(errors),
        "sum_squared_error": math.fsum(squares),
        "mse": mse,
        "rms": rms,
        "zero_count": sum(value == 0.0 for value in outputs),
        "zero_frequency": sum(value == 0.0 for value in outputs) / len(outputs),
        "pde_rms_interval_from_conventional_bias_1_over_32": [max(0.0, rms - PDE_BIAS), rms + PDE_BIAS],
    }


def stored() -> None:
    phase_start = time.perf_counter()
    require(not STORED_RESULT.exists() and not RAW_STATS.exists(), "stored audit already attempted")
    frozen = verify_frozen()
    bindings = verify_declared_bindings()
    protected = verify_protected_inputs()
    manifest = bindings["manifest"]
    cases = {(row["T"], row["nominal_z"]): row for row in manifest["input_cases"]}
    ledger_iter = iter(json_lines(OFFICIAL_LEDGER))
    ledger_rows = 0
    ledger_total = 0
    output_total = 0
    per_seed = []
    raw_seed_index = []
    raw_horizon_index = []
    raw_level_index = []
    raw_schedule_index = []
    raw_replicate_index = []
    raw_outputs = []
    raw_references = []
    raw_errors = []
    raw_squared_errors = []
    timing_cells = []
    pooled_outputs: dict[tuple[int, int, int], list[float]] = {}
    expected_directories = set()

    for si, seed_root in enumerate(SEEDS):
        for ti, horizon in enumerate(HORIZONS):
            for zi, level in enumerate(LEVELS):
                reference = float.fromhex(cases[(horizon, level)]["reference_primary"]["psi_binary64"]["hex"])
                width = cases[(horizon, level)]["stored_width"]
                for qi, (schedule, repetitions) in enumerate(SCHEDULES):
                    name = cell_name(si, ti, zi, qi)
                    expected_directories.add(name)
                    n = N_TABLE[horizon][qi]
                    cell_dir = OFFICIAL / name
                    metadata_path = cell_dir / "cell_complete.json"
                    journal_path = cell_dir / "replicates.jsonl"
                    arrays_path = cell_dir / "cell_arrays.npz"
                    require(cell_dir.is_dir(), f"missing cell {name}")
                    metadata = load_json(metadata_path)
                    require(metadata["status"] == "PASS", f"cell not PASS: {name}")
                    require(metadata["cell"] == name and metadata["seed_root"] == seed_root, f"cell identity: {name}")
                    require(metadata["T"] == horizon and metadata["nominal_z"] == level, f"case identity: {name}")
                    require(metadata["schedule"] == schedule and metadata["n"] == n, f"schedule identity: {name}")
                    require(metadata["repetitions"] == repetitions, f"repetitions: {name}")
                    require(metadata["width"] == width, f"width: {name}")
                    require(metadata["journal_sha256"] == sha256(journal_path), f"journal hash: {name}")
                    require(metadata["arrays_sha256"] == sha256(arrays_path), f"array hash: {name}")
                    timing_cells.append({"cell": name, **metadata["timing_measurements_seconds"]})
                    with np.load(arrays_path, allow_pickle=False) as arrays:
                        require(set(arrays.files) == {"sample_mean", "output", "positive_return_count", "actual_query_count"}, f"NPZ keys: {name}")
                        means = arrays["sample_mean"]
                        outputs = arrays["output"]
                        positives = arrays["positive_return_count"]
                        counts = arrays["actual_query_count"]
                        require(means.dtype == outputs.dtype == np.float64, f"float dtype: {name}")
                        require(positives.dtype == counts.dtype == np.int64, f"integer dtype: {name}")
                        require(means.shape == outputs.shape == positives.shape == counts.shape == (repetitions,), f"array shape: {name}")
                        cell_outputs = []
                        records = list(json_lines(journal_path))
                        require(len(records) == repetitions, f"journal length: {name}")
                        for ri, record in enumerate(records):
                            key = (ti, zi, qi, ri)
                            expected_before, expected_after = expected_rng_states(seed_root, key, n)
                            require(record["status"] == "PASS", f"replicate status: {name}/{ri}")
                            require(record["seed_root"] == seed_root and record["spawn_key"] == list(key), f"stream identity: {name}/{ri}")
                            require(record["replicate_index"] == ri and record["n"] == n, f"replicate identity: {name}/{ri}")
                            require(record["rng_before"] == expected_before, f"RNG before: {name}/{ri}")
                            require(record["rng_after"] == expected_after, f"RNG after: {name}/{ri}")
                            estimate = record["estimate"]
                            expected_batches = batches(n)
                            require(tuple(estimate["batch_counts"]) == expected_batches, f"batch counts: {name}/{ri}")
                            require(len(estimate["batch_sums"]) == len(expected_batches), f"batch sums length: {name}/{ri}")
                            require(all(math.isfinite(value) for value in estimate["batch_sums"]), f"batch sum finite: {name}/{ri}")
                            recomputed_mean = math.fsum(estimate["batch_sums"]) / n
                            require(same_float(estimate["sample_mean"], recomputed_mean), f"sample mean arithmetic: {name}/{ri}")
                            scaled = math.exp(horizon) * estimate["sample_mean"]
                            recomputed_output = scaled / math.hypot(1.0, scaled)
                            require(same_float(estimate["output"], recomputed_output), f"output arithmetic: {name}/{ri}")
                            require(0 <= estimate["positive_return_count"] <= n, f"positive count range: {name}/{ri}")
                            require(estimate["observation_count"] == n, f"observation count: {name}/{ri}")
                            require(record["oracle_attempted_count"] == record["oracle_returned_count"] == n, f"oracle counts: {name}/{ri}")
                            require(record["oracle_positive_count"] == estimate["positive_return_count"], f"oracle positive count: {name}/{ri}")
                            require(same_float(means[ri], estimate["sample_mean"]), f"NPZ mean: {name}/{ri}")
                            require(same_float(outputs[ri], estimate["output"]), f"NPZ output: {name}/{ri}")
                            require(int(positives[ri]) == estimate["positive_return_count"], f"NPZ positive count: {name}/{ri}")
                            require(int(counts[ri]) == n, f"NPZ query count: {name}/{ri}")
                            for batch_count in expected_batches:
                                try:
                                    ledger = next(ledger_iter)
                                except StopIteration as error:
                                    raise AuditFailure(f"official ledger ended at {name}/{ri}") from error
                                ledger_rows += 1
                                ledger_total += batch_count
                                require(ledger["phase"] == "official", f"ledger phase row {ledger_rows}")
                                require(ledger["label"] == f"{name}/replicate-{ri:03d}", f"ledger label row {ledger_rows}")
                                require(ledger["point_calls"] == batch_count, f"ledger increment row {ledger_rows}")
                                require(ledger["cumulative_point_calls"] == ledger_total, f"ledger cumulative row {ledger_rows}")
                            value = float(outputs[ri])
                            error = value - reference
                            cell_outputs.append(value)
                            raw_seed_index.append(si)
                            raw_horizon_index.append(ti)
                            raw_level_index.append(zi)
                            raw_schedule_index.append(qi)
                            raw_replicate_index.append(ri)
                            raw_outputs.append(value)
                            raw_references.append(reference)
                            raw_errors.append(error)
                            raw_squared_errors.append(error * error)
                            output_total += 1
                        pooled_outputs.setdefault((ti, zi, qi), []).extend(cell_outputs)
                        row_stats = stats(cell_outputs, reference)
                        per_seed.append({
                            "cell": name,
                            "seed_root": seed_root,
                            "T": horizon,
                            "nominal_z": level,
                            "schedule": schedule,
                            "n_per_output": n,
                            "actual_total_queries": repetitions * n,
                            "reference_kind": "binary64 scalar surrogate Psi(exp(T)*stored-width mass)",
                            "reference": reference,
                            **row_stats,
                        })
    try:
        extra = next(ledger_iter)
        raise AuditFailure(f"official ledger has extra row after expected sequence: {extra}")
    except StopIteration:
        pass
    actual_directories = {path.name for path in OFFICIAL.iterdir() if path.is_dir()}
    require(actual_directories == expected_directories, "official cell directory set mismatch")
    require(output_total == EXPECTED_OUTPUTS, "stored output total")
    require(ledger_total == EXPECTED_OFFICIAL_CALLS, "official ledger total")
    require(ledger_rows == 20_448, "official ledger row count")

    pooled = []
    for ti, horizon in enumerate(HORIZONS):
        for zi, level in enumerate(LEVELS):
            reference = float.fromhex(cases[(horizon, level)]["reference_primary"]["psi_binary64"]["hex"])
            for qi, (schedule, repetitions) in enumerate(SCHEDULES):
                values = pooled_outputs[(ti, zi, qi)]
                pooled.append({
                    "T": horizon,
                    "nominal_z": level,
                    "schedule": schedule,
                    "seeds": list(SEEDS),
                    "replications_per_seed": repetitions,
                    "pooled_replications": len(values),
                    "n_per_output": N_TABLE[horizon][qi],
                    "actual_mean_queries_per_output": N_TABLE[horizon][qi],
                    "actual_total_queries": len(values) * N_TABLE[horizon][qi],
                    "reference_kind": "binary64 scalar surrogate Psi(exp(T)*stored-width mass)",
                    "reference": reference,
                    "pooling_rule": "math.fsum of every raw squared error across seeds, divided by pooled count, then sqrt",
                    **stats(values, reference),
                })

    baselines = []
    for horizon in HORIZONS:
        for level in LEVELS:
            reference = float.fromhex(cases[(horizon, level)]["reference_primary"]["psi_binary64"]["hex"])
            for value in (0.0, 0.5, 1.0):
                baseline_stats = stats([value], reference)
                baselines.append({
                    "T": horizon,
                    "nominal_z": level,
                    "name": f"constant_{value:g}",
                    "output": value,
                    "actual_queries": 0,
                    "per_seed_and_pooled_identical": True,
                    "reference_kind": "binary64 scalar surrogate Psi(exp(T)*stored-width mass)",
                    "reference": reference,
                    **baseline_stats,
                })

    with RAW_STATS.open("xb") as stream:
        np.savez(
            stream,
            seed_index=np.asarray(raw_seed_index, dtype=np.int64),
            horizon_index=np.asarray(raw_horizon_index, dtype=np.int64),
            level_index=np.asarray(raw_level_index, dtype=np.int64),
            schedule_index=np.asarray(raw_schedule_index, dtype=np.int64),
            replicate_index=np.asarray(raw_replicate_index, dtype=np.int64),
            output=np.asarray(raw_outputs, dtype=np.float64),
            reference=np.asarray(raw_references, dtype=np.float64),
            error=np.asarray(raw_errors, dtype=np.float64),
            squared_error=np.asarray(raw_squared_errors, dtype=np.float64),
        )
        stream.flush()
        os.fsync(stream.fileno())

    official_timing = bindings["official"]["timing_seconds"]
    elapsed = time.perf_counter() - phase_start
    result = {
        "schema_version": 1,
        "status": "PASS",
        "completed_utc": utc_now(),
        "audit_manifest_sha256": sha256(AUDIT_MANIFEST),
        "audit_source_sha256": sha256(SOURCE),
        "frozen_inputs_reverified": len(frozen["input_hashes_sha256"]),
        "protected_initial_sources": protected,
        "official_cells_verified": len(per_seed),
        "official_outputs_verified": output_total,
        "official_ledger_rows_verified": ledger_rows,
        "official_point_calls_verified": ledger_total,
        "all_version_activity_ledgers_verified": bindings["activity"],
        "all_version_point_calls_before_replay": sum(row["point_calls"] for row in bindings["activity"].values()),
        "all_npz_journal_means_outputs_counts_verified_bitwise": True,
        "all_batch_counts_and_sums_arithmetic_verified": True,
        "all_rng_before_and_advanced_after_states_verified": True,
        "rng_after_verification_method": "independent PCG64 SeedSequence construction followed by PCG64.advance(n); no oracle calls",
        "statistics_raw_sha256": sha256(RAW_STATS),
        "statistics": {
            "per_seed_cells": per_seed,
            "pooled_cells": pooled,
            "zero_query_baselines": baselines,
            "raw_squared_errors_archived": rel(RAW_STATS),
            "pde_interpretation": "Each scalar-surrogate RMS r maps to [max(0,r-1/32),r+1/32] by the conventional PDE bias statement; this is not an actual PDE solve or a floating-point enclosure.",
        },
        "producer_timing_labels_as_recorded": official_timing,
        "producer_timing_interpretation": "Measured wall and accounting-subtracted labels only; no pure-compute claim.",
        "audit_timing": {
            "stored_evidence_and_statistics_wall_seconds": elapsed,
            "interpretation": "Wall time for read-only hashes, parsing, independent arithmetic/RNG checks, and statistics; not pure compute.",
        },
        "oracle_calls_in_this_phase": 0,
        "actual_spent_before_replay": EXPECTED_SPENT_BEFORE_REPLAY,
    }
    write_json_new(STORED_RESULT, result)
    print(json.dumps({"status": "PASS", "stored_audit_sha256": sha256(STORED_RESULT), "oracle_calls": 0}, indent=2))


def bump_values(points: np.ndarray, width: float) -> np.ndarray:
    if width == 0.0:
        return np.zeros(points.shape, dtype=np.float64)
    remainder = np.remainder(points - SHIFT, 1.0)
    r = remainder / width
    mask = (r > 0.0) & (r < 1.0)
    values = np.zeros(points.shape, dtype=np.float64)
    inside = r[mask]
    values[mask] = (width / 8.0) * np.exp(-1.0 / (inside * (1.0 - inside)))
    return values


def replay() -> None:
    phase_start = time.perf_counter()
    require(not REPLAY_LEDGER.exists() and not REPLAY_JOURNAL.exists() and not REPLAY_RESULT.exists() and not REPLAY_FAILURE.exists(), "replay already attempted; automatic retry forbidden")
    frozen = verify_frozen()
    stored_result = load_json(STORED_RESULT)
    require(stored_result["status"] == "PASS", "stored audit did not pass")
    require(stored_result["audit_manifest_sha256"] == sha256(AUDIT_MANIFEST), "stored audit manifest binding")
    require(stored_result["audit_source_sha256"] == sha256(SOURCE), "stored audit source binding")
    require(stored_result["official_cells_verified"] == EXPECTED_CELLS, "stored cell gate")
    require(stored_result["official_outputs_verified"] == EXPECTED_OUTPUTS, "stored output gate")
    require(stored_result["official_point_calls_verified"] == EXPECTED_OFFICIAL_CALLS, "stored call gate")
    manifest = load_json(MANIFEST)
    cases = {(row["T"], row["nominal_z"]): row for row in manifest["input_cases"]}
    replay_plan = frozen["exact_replay_subset"]
    total = 0
    cells_done = 0
    ledger_rows = 0
    failure_context: dict[str, Any] = {"stage": "setup", "actual_replay_calls": 0}
    with REPLAY_LEDGER.open("x", encoding="utf-8") as ledger_stream, REPLAY_JOURNAL.open("x", encoding="utf-8") as journal_stream:
        try:
            for plan in replay_plan:
                name = plan["cell"]
                horizon = plan["T"]
                level = plan["nominal_z"]
                n = plan["n"]
                seed_root = plan["seed_root"]
                key = tuple(plan["spawn_key"])
                width = float.fromhex(cases[(horizon, level)]["stored_width"]["hex"])
                archived = next(json_lines(OFFICIAL / name / "replicates.jsonl"))
                with np.load(OFFICIAL / name / "cell_arrays.npz", allow_pickle=False) as arrays:
                    archived_npz = {
                        "sample_mean": float(arrays["sample_mean"][0]),
                        "output": float(arrays["output"][0]),
                        "positive_return_count": int(arrays["positive_return_count"][0]),
                        "actual_query_count": int(arrays["actual_query_count"][0]),
                    }
                rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence(seed_root, spawn_key=key)))
                rng_before = copy.deepcopy(jsonable(rng.bit_generator.state))
                batch_sums = []
                batch_counts = []
                positive_count = 0
                observation_count = 0
                failure_context = {
                    "stage": "replicate",
                    "cell": name,
                    "seed_root": seed_root,
                    "spawn_key": list(key),
                    "replicate_index": 0,
                    "T": horizon,
                    "nominal_z": level,
                    "schedule": plan["schedule"],
                    "n": n,
                    "rng_before": rng_before,
                    "batch_sums": batch_sums,
                    "batch_counts": batch_counts,
                    "positive_return_count": positive_count,
                    "observation_count": observation_count,
                    "actual_replay_calls": total,
                }
                for batch_index, count in enumerate(batches(n)):
                    points = rng.random(count, dtype=np.float64)
                    append_json(ledger_stream, {
                        "utc": utc_now(),
                        "phase": "independent_subset_replay",
                        "cell": name,
                        "replicate_index": 0,
                        "batch_index": batch_index,
                        "point_calls": count,
                        "audit_cumulative_point_calls": total + count,
                        "all_versions_cumulative_point_calls": EXPECTED_SPENT_BEFORE_REPLAY + total + count,
                    })
                    ledger_rows += 1
                    total += count
                    failure_context["actual_replay_calls"] = total
                    values = bump_values(points, width)
                    require(values.shape == points.shape and bool(np.all(np.isfinite(values))), f"replay oracle values: {name}")
                    batch_sums.append(float(np.sum(values, dtype=np.float64)))
                    batch_counts.append(count)
                    positive_count += int(np.count_nonzero(values > 0.0))
                    observation_count += count
                    failure_context.update({
                        "rng_after_partial": copy.deepcopy(jsonable(rng.bit_generator.state)),
                        "batch_sums": batch_sums,
                        "batch_counts": batch_counts,
                        "positive_return_count": positive_count,
                        "observation_count": observation_count,
                    })
                mean = math.fsum(batch_sums) / n
                scaled = math.exp(horizon) * mean
                output = scaled / math.hypot(1.0, scaled)
                rng_after = copy.deepcopy(jsonable(rng.bit_generator.state))
                match = {
                    "rng_before": rng_before == archived["rng_before"],
                    "rng_after": rng_after == archived["rng_after"],
                    "sample_mean": same_float(mean, archived["estimate"]["sample_mean"]) and same_float(mean, archived_npz["sample_mean"]),
                    "output": same_float(output, archived["estimate"]["output"]) and same_float(output, archived_npz["output"]),
                    "positive_return_count": positive_count == archived["estimate"]["positive_return_count"] == archived_npz["positive_return_count"],
                    "observation_and_query_count": observation_count == archived["estimate"]["observation_count"] == archived_npz["actual_query_count"] == n,
                    "batch_counts": batch_counts == archived["estimate"]["batch_counts"],
                    "batch_sums": len(batch_sums) == len(archived["estimate"]["batch_sums"]) and all(same_float(a, b) for a, b in zip(batch_sums, archived["estimate"]["batch_sums"])),
                }
                record = {
                    "status": "PASS" if all(match.values()) else "FAIL",
                    **plan,
                    "rng_before": rng_before,
                    "rng_after": rng_after,
                    "estimate": {
                        "sample_mean": mean,
                        "output": output,
                        "positive_return_count": positive_count,
                        "observation_count": observation_count,
                        "batch_sums": batch_sums,
                        "batch_counts": batch_counts,
                    },
                    "bitwise_matches": match,
                    "audit_cumulative_point_calls": total,
                    "all_versions_cumulative_point_calls": EXPECTED_SPENT_BEFORE_REPLAY + total,
                }
                append_json(journal_stream, record)
                require(all(match.values()), f"replay mismatch: {name}: {match}")
                cells_done += 1
            require(cells_done == EXPECTED_CELLS, "replay completed cells")
            require(total == EXPECTED_REPLAY_CALLS, "replay total calls")
            require(EXPECTED_SPENT_BEFORE_REPLAY + total == EXPECTED_SPENT_AFTER_REPLAY, "cross-version replay total")
        except BaseException as error:
            failure_context.update({
                "rng_after_failure": failure_context.get("rng_after_partial"),
                "actual_replay_calls": total,
                "all_versions_cumulative_point_calls": EXPECTED_SPENT_BEFORE_REPLAY + total,
                "completed_cells": cells_done,
                "ledger_rows": ledger_rows,
                "error_type": type(error).__name__,
                "error": str(error),
                "traceback": traceback.format_exc(),
                "automatic_retry_permitted": False,
                "partial_evidence_preserved": True,
            })
            write_json_new(REPLAY_FAILURE, failure_context)
            raise
    elapsed = time.perf_counter() - phase_start
    write_json_new(REPLAY_RESULT, {
        "schema_version": 1,
        "status": "PASS",
        "completed_utc": utc_now(),
        "audit_manifest_sha256": sha256(AUDIT_MANIFEST),
        "audit_source_sha256": sha256(SOURCE),
        "stored_audit_sha256": sha256(STORED_RESULT),
        "selection_rule": "replicate_index=0 of all 180 cells, frozen before replay",
        "completed_cells": cells_done,
        "actual_point_calls": total,
        "ledger_rows": ledger_rows,
        "all_mean_output_positive_count_query_count_batch_and_rng_matches": True,
        "activity_ledger_sha256": sha256(REPLAY_LEDGER),
        "replay_journal_sha256": sha256(REPLAY_JOURNAL),
        "actual_spent_before_replay": EXPECTED_SPENT_BEFORE_REPLAY,
        "actual_spent_after_replay": EXPECTED_SPENT_AFTER_REPLAY,
        "whole_activity_cap": CAP,
        "timing": {
            "replay_wall_seconds": elapsed,
            "interpretation": "Wall time includes RNG, oracle evaluation, arithmetic, durable JSONL writes, and fsync; no pure-compute claim.",
        },
        "full_replay_executed": False,
        "automatic_retry_executed": False,
    })
    print(json.dumps({"status": "PASS", "replay_result_sha256": sha256(REPLAY_RESULT), "actual_point_calls": total}, indent=2))


def plot() -> None:
    phase_start = time.perf_counter()
    require(not PLOT_PNG.exists() and not PLOT_SVG.exists() and not PLOT_RESULT.exists(), "plot already created")
    verify_frozen()
    stored_result = load_json(STORED_RESULT)
    replay_result = load_json(REPLAY_RESULT)
    require(stored_result["status"] == replay_result["status"] == "PASS", "plot gates")
    per_seed = stored_result["statistics"]["per_seed_cells"]
    pooled = stored_result["statistics"]["pooled_cells"]
    baselines = stored_result["statistics"]["zero_query_baselines"]
    schedule_colors = {
        "growing_0p125": "#0072B2",
        "growing_0p5": "#009E73",
        "growing_2": "#E69F00",
        "theorem_96": "#D55E00",
        "fixed_51": "#CC79A7",
    }
    baseline_styles = {"constant_0": ("#333333", ":"), "constant_0.5": ("#666666", "--"), "constant_1": ("#999999", "-.")}
    fig, axes = plt.subplots(4, 2, figsize=(14, 17), constrained_layout=True)
    for zi, level in enumerate(LEVELS):
        ax_rms, ax_q = axes[zi]
        for schedule, repetitions in SCHEDULES:
            color = schedule_colors[schedule]
            pool_rows = [row for row in pooled if row["nominal_z"] == level and row["schedule"] == schedule]
            pool_rows.sort(key=lambda row: row["T"])
            xs = [row["T"] for row in pool_rows]
            ys = [row["rms"] for row in pool_rows]
            seed_rows = [row for row in per_seed if row["nominal_z"] == level and row["schedule"] == schedule]
            ax_rms.scatter([row["T"] for row in seed_rows], [row["rms"] for row in seed_rows], s=18, facecolors="none", edgecolors=color, alpha=0.45, linewidths=0.8)
            ax_rms.plot(xs, ys, color=color, marker="o", linewidth=2.0, label=f"{schedule} (R={repetitions}/seed)")
            ax_rms.errorbar(xs, ys, yerr=[[min(PDE_BIAS, value) for value in ys], [PDE_BIAS] * len(ys)], fmt="none", ecolor=color, alpha=0.22, capsize=2)
            qs = [row["actual_mean_queries_per_output"] for row in pool_rows]
            for seed_offset in (-0.14, 0.0, 0.14):
                ax_q.scatter([value + seed_offset for value in xs], qs, s=22, facecolors="none", edgecolors=color, alpha=0.55, linewidths=0.8)
            ax_q.plot(xs, qs, color=color, marker="o", linewidth=2.0, label=f"{schedule} (R={repetitions}/seed)")
        for name, (color, linestyle) in baseline_styles.items():
            rows = [row for row in baselines if row["nominal_z"] == level and row["name"] == name]
            rows.sort(key=lambda row: row["T"])
            xs = [row["T"] for row in rows]
            ys = [row["rms"] for row in rows]
            ax_rms.plot(xs, ys, color=color, linestyle=linestyle, marker="s", linewidth=1.5, label=f"{name} (0 queries)")
            ax_rms.errorbar(xs, ys, yerr=[[min(PDE_BIAS, value) for value in ys], [PDE_BIAS] * len(ys)], fmt="none", ecolor=color, alpha=0.15, capsize=2)
            ax_q.plot(xs, [0.0] * len(xs), color=color, linestyle=linestyle, marker="s", linewidth=1.5, label=f"{name} (0 queries)")
        ax_rms.set_title(f"nominal z={level:g}: RMS against scalar surrogate")
        ax_rms.set_xlabel("horizon T")
        ax_rms.set_ylabel("empirical RMS")
        ax_rms.set_xticks(HORIZONS)
        ax_rms.set_yscale("symlog", linthresh=1e-5)
        ax_rms.grid(True, which="both", alpha=0.25)
        ax_q.set_title(f"nominal z={level:g}: actual query budget per output")
        ax_q.set_xlabel("horizon T")
        ax_q.set_ylabel("point queries")
        ax_q.set_xticks(HORIZONS)
        ax_q.set_yscale("symlog", linthresh=1.0)
        ax_q.grid(True, which="both", alpha=0.25)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="outside upper center", ncol=4, fontsize=9, frameon=False)
    fig.suptitle(
        "Frozen positive-query experiment — independent audit\n"
        "solid points/lines: pooled; open points: individual seeds; whiskers: conventional PDE comparison ±1/32\n"
        "RMS reference is the computed scalar surrogate, not an actual PDE numerical solve or a rigorous float enclosure",
        fontsize=14,
    )
    fig.savefig(PLOT_PNG, dpi=180, metadata={"Title": "Independent positive-query sampling audit"})
    fig.savefig(PLOT_SVG, metadata={"Title": "Independent positive-query sampling audit"})
    plt.close(fig)
    elapsed = time.perf_counter() - phase_start
    write_json_new(PLOT_RESULT, {
        "schema_version": 1,
        "status": "PASS",
        "completed_utc": utc_now(),
        "source_statistics_sha256": sha256(STORED_RESULT),
        "replay_gate_sha256": sha256(REPLAY_RESULT),
        "png_sha256": sha256(PLOT_PNG),
        "svg_sha256": sha256(PLOT_SVG),
        "visible_series": [name for name, _ in SCHEDULES] + ["constant_0", "constant_0.5", "constant_1"],
        "per_seed_and_pool_distinction": "Open markers are per-seed RMS; solid markers and lines are pooled raw-square RMS.",
        "query_budget_visibility": "Right column shows actual n per output including zero-query baselines; legends show R per seed.",
        "reference_scope": "Left column uses the binary64 scalar surrogate. Whiskers show only the conventional ±1/32 PDE-bias interpretation.",
        "plotting_wall_seconds": elapsed,
        "timing_interpretation": "Wall time includes rendering and file serialization; no pure-compute claim.",
        "oracle_calls": 0,
    })
    print(json.dumps({"status": "PASS", "png": rel(PLOT_PNG), "svg": rel(PLOT_SVG)}, indent=2))


def finalize() -> None:
    require(not FINAL_AUDIT.exists(), "final audit already exists")
    verify_frozen()
    required = [AUDIT_MANIFEST, STORED_RESULT, RAW_STATS, REPLAY_LEDGER, REPLAY_JOURNAL, REPLAY_RESULT, PLOT_PNG, PLOT_SVG, PLOT_RESULT, REVIEW]
    for path in required:
        require(path.is_file(), f"missing final audit output: {path}")
    require(load_json(STORED_RESULT)["status"] == "PASS", "stored final gate")
    require(load_json(REPLAY_RESULT)["status"] == "PASS", "replay final gate")
    require(load_json(PLOT_RESULT)["status"] == "PASS", "plot final gate")
    require(not REPLAY_FAILURE.exists(), "replay failure evidence exists")
    write_json_new(FINAL_AUDIT, {
        "schema_version": 1,
        "status": "PASS",
        "completed_utc": utc_now(),
        "task": "T66 independent frozen positive-query audit and prespecified subset replay",
        "output_hashes_sha256": {rel(path): sha256(path) for path in required},
        "official_verified": {"cells": EXPECTED_CELLS, "outputs": EXPECTED_OUTPUTS, "point_calls": EXPECTED_OFFICIAL_CALLS},
        "subset_replay_verified": {"selection": "replicate 0 of every cell", "cells": EXPECTED_CELLS, "point_calls": EXPECTED_REPLAY_CALLS, "bitwise_agreement": True},
        "activity": {"spent_before_replay": EXPECTED_SPENT_BEFORE_REPLAY, "spent_after_replay": EXPECTED_SPENT_AFTER_REPLAY, "cap": CAP},
        "claims": {
            "actual_pde_numerical_solve": False,
            "rigorous_float_enclosure": False,
            "iid_machine_to_real_bridge": False,
            "minimax_empirical_proof": False,
            "novelty_claim": False,
            "full_replay": False,
        },
        "residual_limitations": [
            "The replay covers only the prespecified replicate-0 subset, 180 of 18720 outputs.",
            "The scalar reference and reported statistics use ordinary binary64 and are not rigorous enclosures.",
            "The ±1/32 PDE comparison comes from the conventional theorem; no PDE was numerically solved here.",
            "PCG64/binary64 sampling is reproducible numerical evidence, not a certified iid-real-law bridge.",
            "The finite experiment does not establish a minimax theorem, asymptotic optimality, or novelty.",
        ],
        "self_hash_note": "This file hashes every other audit output; as usual, it cannot contain its own SHA256 without changing it.",
    })
    print(json.dumps({"status": "PASS", "final_audit_sha256": sha256(FINAL_AUDIT)}, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "stored", "replay", "plot", "finalize"))
    return parser.parse_args()


def main() -> None:
    phase = parse_args().phase
    try:
        {"prepare": prepare, "stored": stored, "replay": replay, "plot": plot, "finalize": finalize}[phase]()
    except BaseException as error:
        if phase == "stored" and AUDIT_DIR.is_dir() and not STORED_RESULT.exists() and not STORED_FAILURE.exists():
            write_json_new(STORED_FAILURE, {
                "status": "FAIL",
                "failed_utc": utc_now(),
                "error_type": type(error).__name__,
                "error": str(error),
                "traceback": traceback.format_exc(),
                "oracle_calls": 0,
                "partial_evidence_preserved": True,
                "automatic_retry_permitted": False,
            })
        raise


if __name__ == "__main__":
    main()
