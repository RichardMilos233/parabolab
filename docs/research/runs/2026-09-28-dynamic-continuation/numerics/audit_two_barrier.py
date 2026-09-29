"""Independent raw-evidence audit for the frozen two-barrier experiment.

The auditor reads JSON and NPZ artifacts directly.  It deliberately does not
import the sampler, producer driver, or deterministic reference modules.
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
from typing import Any

import numpy as np


HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO = HERE.parents[4]
TWO_BARRIER_ARTIFACTS = RUN_DIR / "artifacts" / "two-barrier"
SAMPLER_DIR = TWO_BARRIER_ARTIFACTS / "sampler-v1"
REFERENCE_DIR = TWO_BARRIER_ARTIFACTS / "reference-v1"
AUDIT_DIR = TWO_BARRIER_ARTIFACTS / "audit-v1"
PNG_PATH = RUN_DIR / "two-barrier-results.png"
SVG_PATH = RUN_DIR / "two-barrier-results.svg"
INITIAL_HASHES_PATH = RUN_DIR / "initial-source-hashes.json"
PROTOCOL_PATH = RUN_DIR / "02d-two-barrier-experiment-protocol.md"
PROTOCOL_SHA256 = "605eda24574bfb7e44dc997c185836d2a54311c18344e0be4c005674e00beda9"

TIMES = np.asarray((0.0, 0.25, 1.0, 4.0, 16.0, 64.0, 256.0), dtype=np.float64)
QUERIES = np.asarray((0.0, math.pi / 2.0, math.pi), dtype=np.float64)
SEEDS = (2026092831, 2026092832, 2026092833)
CLOCK_TIMES = np.asarray((0.25, 1.0, 4.0), dtype=np.float64)
ROOT_FIELDS = {
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
}
CLOCK_FIELDS = {
    "is_leaf",
    "accepted_time",
    "accepted_zeta",
    "proposals",
    "rejections",
    "zero_redraws",
}
RANGE_TOLERANCE = 1.0e-12
SUMMARY_TOLERANCE = 5.0e-13
REFINEMENT_THRESHOLD = 1.0e-8
DKW_THRESHOLD = math.sqrt(math.log(2.0 / 1.0e-6) / 200_000.0)
CONSTANT_THRESHOLD = 1.25 * DKW_THRESHOLD
THEORETICAL_MEAN_NODES = 25.0 * math.sqrt(6.0) / 16.0 - 1.0
THEORETICAL_MEAN_PROPOSALS = (15.0 / 8.0) * THEORETICAL_MEAN_NODES


class AuditError(RuntimeError):
    pass


class Checks:
    def __init__(self) -> None:
        self.records: list[dict[str, Any]] = []

    def add(self, name: str, passed: bool, **details: Any) -> None:
        self.records.append({"name": name, "passed": bool(passed), **jsonable(details)})

    @property
    def passed(self) -> bool:
        return all(record["passed"] for record in self.records)

    @property
    def failures(self) -> list[dict[str, Any]]:
        return [record for record in self.records if not record["passed"]]


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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json_new(path: Path, payload: Any) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(jsonable(payload), stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def relative_path(path: Path) -> str:
    return str(path.resolve().relative_to(REPO.resolve()))


def input_files() -> list[Path]:
    files = [PROTOCOL_PATH, INITIAL_HASHES_PATH, Path(__file__).resolve()]
    for root in (SAMPLER_DIR, REFERENCE_DIR):
        files.extend(sorted(path for path in root.rglob("*") if path.is_file()))
    return sorted(set(path.resolve() for path in files))


def input_hashes() -> dict[str, str]:
    return {relative_path(path): sha256(path) for path in input_files()}


def stable_scaled_defect(c: float, t: float | np.ndarray) -> np.ndarray:
    values = np.asarray(t, dtype=np.float64)
    alpha = c**-2 - 1.0
    root = np.sqrt(1.0 + alpha * np.exp(-2.0 * values))
    return alpha / (root * (root + 1.0))


def clock_cdf(horizon: float, points: np.ndarray) -> np.ndarray:
    points = np.asarray(points, dtype=np.float64)

    def ratio(t: np.ndarray) -> np.ndarray:
        exponential = np.exp(-2.0 * t)
        zeta = np.sqrt((1.0 + (7.0 / 9.0) * exponential) / (1.0 + 3.0 * exponential))
        return zeta**2 / (1.0 + zeta)

    return ratio(points) / ratio(np.asarray(horizon))


def clock_zeta(points: np.ndarray) -> np.ndarray:
    points = np.asarray(points, dtype=np.float64)
    exponential = np.exp(-2.0 * points)
    return np.sqrt((1.0 + (7.0 / 9.0) * exponential) / (1.0 + 3.0 * exponential))


def expected_initial_state(entropy: int, spawn_key: tuple[int, ...]) -> dict[str, Any]:
    sequence = np.random.SeedSequence(entropy=entropy, spawn_key=spawn_key)
    generator = np.random.Generator(np.random.PCG64(sequence))
    return jsonable(copy.deepcopy(generator.bit_generator.state))


def state_is_present(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and value.get("bit_generator") == "PCG64"
        and isinstance(value.get("state"), dict)
        and isinstance(value["state"].get("state"), int)
        and isinstance(value["state"].get("inc"), int)
    )


def prepare() -> None:
    summary_path = SAMPLER_DIR / "primary_summary.json"
    if not summary_path.is_file():
        raise AuditError("primary_summary.json is not ready")
    producer_summary = read_json(summary_path)
    if producer_summary.get("status") != "complete":
        raise AuditError(f"producer primary is not complete: {producer_summary.get('status')}")
    if AUDIT_DIR.exists() or PNG_PATH.exists() or SVG_PATH.exists():
        raise FileExistsError("refusing to overwrite an audit artifact or scientific figure")
    if sha256(PROTOCOL_PATH) != PROTOCOL_SHA256:
        raise AuditError("frozen protocol hash mismatch")
    AUDIT_DIR.mkdir(parents=True, exist_ok=False)
    hashes = input_hashes()
    manifest = {
        "schema_version": 1,
        "status": "prepared-before-audit",
        "created_utc": utc_now(),
        "immutable_after_creation": True,
        "auditor_source": relative_path(Path(__file__)),
        "auditor_source_sha256": sha256(Path(__file__)),
        "protocol_sha256": PROTOCOL_SHA256,
        "input_file_count": len(hashes),
        "input_hashes_sha256": hashes,
        "environment": {
            "python_executable": sys.executable,
            "python_version": sys.version,
            "numpy_version": np.__version__,
            "platform": platform.platform(),
            "machine": platform.machine(),
        },
        "fixed_cases": {
            "times": TIMES.tolist(),
            "queries": QUERIES.tolist(),
            "seeds": list(SEEDS),
            "primary_cells": 63,
            "primary_roots": 630_000,
            "official_diagnostic_archives": 18,
            "accepted_clocks": 300_000,
            "diagnostic_roots": 101_792,
            "protected_initial_hashes": 342,
        },
        "scope": {
            "imports_sampler_driver_or_reference": False,
            "replays_full_tree_rng_draws": False,
            "checks_fixed_stream_initial_states": True,
            "figures_use_all_prespecified_finite_points": True,
            "no_equal_accuracy_or_optimality_claim": True,
        },
    }
    write_json_new(AUDIT_DIR / "execution_manifest.json", manifest)
    print(json.dumps({"status": "prepared", "input_file_count": len(hashes), "output": str(AUDIT_DIR)}))


def verify_manifest() -> dict[str, Any]:
    path = AUDIT_DIR / "execution_manifest.json"
    if not path.is_file():
        raise AuditError("audit manifest has not been prepared")
    manifest = read_json(path)
    current = input_hashes()
    expected = manifest["input_hashes_sha256"]
    if current != expected:
        changed = sorted(set(current) | set(expected))
        mismatch = {
            item: {"expected": expected.get(item), "actual": current.get(item)}
            for item in changed
            if expected.get(item) != current.get(item)
        }
        raise AuditError(f"input changed after audit manifest freeze: {mismatch}")
    return manifest


def verify_initial_hashes(checks: Checks) -> dict[str, int]:
    mapping = read_json(INITIAL_HASHES_PATH)
    if not isinstance(mapping, dict):
        raise AuditError("initial-source-hashes.json must be an object")
    missing = 0
    mismatch = 0
    for relative, expected in mapping.items():
        path = REPO / relative
        if not path.is_file():
            missing += 1
        elif sha256(path) != expected:
            mismatch += 1
    checks.add("initial_hash_count_is_342", len(mapping) == 342, observed=len(mapping))
    checks.add("all_342_initial_files_present", missing == 0, missing=missing)
    checks.add("all_342_initial_hashes_match", mismatch == 0, mismatches=mismatch)
    return {"expected": len(mapping), "missing": missing, "mismatches": mismatch}


def verify_producer_hashes(checks: Checks) -> dict[str, int]:
    producer_manifest = read_json(SAMPLER_DIR / "execution_manifest.json")
    sources = producer_manifest["source_and_gate_hashes_sha256"]
    source_missing = 0
    source_mismatch = 0
    for relative, expected in sources.items():
        path = REPO / relative
        if not path.is_file():
            source_missing += 1
        elif sha256(path) != expected:
            source_mismatch += 1
    checks.add("producer_source_gate_hashes_match", source_missing == 0 and source_mismatch == 0,
               expected=len(sources), missing=source_missing, mismatches=source_mismatch)

    gate = read_json(SAMPLER_DIR / "primary_gate.json")
    gate_pairs = {
        "sampler_manifest_sha256": SAMPLER_DIR / "execution_manifest.json",
        "preflight_results_sha256": SAMPLER_DIR / "preflight_results.json",
        "diagnostics_summary_sha256": SAMPLER_DIR / "diagnostics_summary.json",
    }
    gate_mismatch = sum(sha256(path) != gate[field] for field, path in gate_pairs.items())
    checks.add("primary_gate_hashes_match", gate_mismatch == 0, checked=len(gate_pairs), mismatches=gate_mismatch)
    checks.add("primary_gate_status_passed", gate.get("status") == "passed")
    return {
        "source_gate_expected": len(sources),
        "source_gate_missing": source_missing,
        "source_gate_mismatches": source_mismatch,
        "primary_gate_hashes_checked": len(gate_pairs),
        "primary_gate_hash_mismatches": gate_mismatch,
    }


def audit_reference(checks: Checks) -> tuple[np.ndarray, dict[str, Any]]:
    summary = read_json(REFERENCE_DIR / "reference_summary.json")
    with np.load(REFERENCE_DIR / "reference.npz", allow_pickle=False) as archive:
        checks.add("reference_exact_keys", set(archive.files) == {"times", "queries", "scaled_values"},
                   keys=sorted(archive.files))
        times = archive["times"].copy()
        queries = archive["queries"].copy()
        reference = archive["scaled_values"].copy()
    checks.add("reference_shapes", times.shape == (7,) and queries.shape == (3,) and reference.shape == (7, 3),
               times_shape=times.shape, queries_shape=queries.shape, values_shape=reference.shape)
    checks.add("reference_fixed_grids", np.array_equal(times, TIMES) and np.array_equal(queries, QUERIES))
    checks.add("reference_finite_positive", bool(np.all(np.isfinite(reference)) and np.all(reference > 0.0)))
    checks.add("reference_summary_gate_passed", summary.get("status") == "PASS" and summary["gates"].get("passed") is True)

    discrepancies: dict[str, float] = {}
    reconstruction_max = 0.0
    strict_values: np.ndarray | None = None
    refinement_shapes: dict[str, list[int]] = {}
    for max_mode in (16, 32, 64):
        for tolerance in ("loose", "strict"):
            key = f"k{max_mode}_{tolerance}"
            with np.load(REFERENCE_DIR / f"refinement_{key}.npz", allow_pickle=False) as archive:
                coefficients = archive["coefficients"].copy()
                values = archive["scaled_values"].copy()
                run_times = archive["times"].copy()
                run_queries = archive["queries"].copy()
            expected_shape = (7, max_mode + 1)
            refinement_shapes[key] = list(coefficients.shape)
            checks.add(f"reference_{key}_shape", coefficients.shape == expected_shape and values.shape == (7, 3))
            checks.add(f"reference_{key}_grids", np.array_equal(run_times, TIMES) and np.array_equal(run_queries, QUERIES))
            basis = np.cos(QUERIES[:, None] * np.arange(max_mode + 1)[None, :])
            reconstruction = coefficients @ basis.T
            reconstruction_max = max(reconstruction_max, float(np.max(np.abs(reconstruction - values))))
            if key == "k64_strict":
                strict_values = values
    if strict_values is None:
        raise AuditError("strict reference refinement missing")
    for max_mode in (16, 32, 64):
        for tolerance in ("loose", "strict"):
            key = f"k{max_mode}_{tolerance}"
            with np.load(REFERENCE_DIR / f"refinement_{key}.npz", allow_pickle=False) as archive:
                values = archive["scaled_values"]
            discrepancies[key] = float(np.max(np.abs(values - strict_values)))
    maximum = max(discrepancies.values())
    checks.add("reference_query_reconstruction", reconstruction_max <= 5.0e-15, maximum=reconstruction_max)
    checks.add("reference_strict_array_identity", np.array_equal(reference, strict_values))
    checks.add("reference_refinement_gate", maximum < REFINEMENT_THRESHOLD,
               maximum=maximum, threshold=REFINEMENT_THRESHOLD)
    summary_differences = summary["gates"]["per_run_21_query_difference"]
    checks.add("reference_reported_discrepancies_match",
               max(abs(discrepancies[key] - summary_differences[key]) for key in discrepancies) <= 1.0e-18)
    return reference, {
        "refinement_shapes": refinement_shapes,
        "query_reconstruction_max_abs_difference": reconstruction_max,
        "per_run_difference_from_strict": discrepancies,
        "maximum_difference_from_strict": maximum,
        "threshold": REFINEMENT_THRESHOLD,
        "predesignated_comparator": summary["predesignated_comparator"],
        "six_run_timings": summary["timings_seconds"],
    }


def load_root_archive(path: Path, expected_size: int, checks: Checks, label: str) -> dict[str, np.ndarray]:
    with np.load(path, allow_pickle=False) as archive:
        checks.add(f"{label}_raw_fields", set(archive.files) == ROOT_FIELDS, keys=sorted(archive.files))
        arrays = {name: archive[name].copy() for name in archive.files}
    checks.add(f"{label}_lengths", all(array.shape == (expected_size,) for array in arrays.values()),
               expected_size=expected_size)
    return arrays


def root_invariants(
    arrays: dict[str, np.ndarray], horizon: float, checks: Checks, label: str
) -> dict[str, Any]:
    z = arrays["normalized_output"]
    w = arrays["scaled_output"]
    nodes = arrays["nodes"]
    leaves = arrays["leaves"]
    binary = arrays["binary_internal"]
    ternary = arrays["ternary_internal"]
    proposals = arrays["clock_proposals"]
    rejections = arrays["clock_rejections"]
    integer_arrays = (nodes, leaves, binary, ternary, proposals, rejections, arrays["zero_redraws"])
    rm = float(stable_scaled_defect(0.5, horizon))
    rM = float(stable_scaled_defect(0.75, horizon))
    reconstructed = rM * z + rm * (1.0 - z)
    w_error = float(np.max(np.abs(w - reconstructed))) if w.size else 0.0
    counts_ok = bool(
        np.all(nodes == leaves + binary + ternary)
        and np.all(nodes == 1 + 2 * binary + 3 * ternary)
        and np.all(leaves == 1 + binary + 2 * ternary)
    )
    if horizon == 0.0:
        proposal_ok = bool(np.all(proposals == 0) and np.all(rejections == 0))
    else:
        proposal_ok = bool(np.all(proposals == nodes + rejections))
    checks.add(f"{label}_finite", bool(np.all(np.isfinite(z)) and np.all(np.isfinite(w))))
    checks.add(f"{label}_integer_nonnegative", bool(all(np.all(array >= 0) for array in integer_arrays)))
    checks.add(
        f"{label}_indicator_ranges",
        bool(
            np.all((arrays["zero_redraws"] == 0) | (arrays["zero_redraws"] == 1))
            and np.all(
                (arrays["coefficient_limit_substitution"] == 0)
                | (arrays["coefficient_limit_substitution"] == 1)
            )
        ),
    )
    checks.add(f"{label}_count_identities", counts_ok)
    checks.add(f"{label}_proposal_identity", proposal_ok)
    checks.add(f"{label}_z_range", bool(np.all(z >= -RANGE_TOLERANCE) and np.all(z <= 1.0 + RANGE_TOLERANCE)))
    checks.add(f"{label}_w_range", bool(np.all(w >= rM - RANGE_TOLERANCE) and np.all(w <= rm + RANGE_TOLERANCE)))
    checks.add(f"{label}_w_from_z", w_error <= RANGE_TOLERANCE, maximum=w_error)
    return {
        "w_from_z_max_abs_difference": w_error,
        "zero_redraws": int(np.sum(arrays["zero_redraws"])),
        "coefficient_limit_substitutions": int(np.sum(arrays["coefficient_limit_substitution"])),
        "maximum_nodes": int(np.max(nodes)) if nodes.size else 0,
        "maximum_proposals": int(np.max(proposals)) if proposals.size else 0,
    }


def compare_float(checks: Checks, name: str, actual: float, expected: float, tolerance: float = SUMMARY_TOLERANCE) -> None:
    difference = abs(actual - expected)
    scale = max(1.0, abs(expected))
    checks.add(name, difference <= tolerance * scale, actual=actual, expected=expected, difference=difference)


def audit_diagnostics(checks: Checks) -> dict[str, Any]:
    summary = read_json(SAMPLER_DIR / "diagnostics_summary.json")
    checks.add("diagnostics_summary_passed", summary.get("status") == "passed")
    diagnostic_dir = SAMPLER_DIR / "diagnostics"
    archives = sorted(diagnostic_dir.glob("*.npz"))
    checks.add("official_diagnostic_archive_count", len(archives) == 18, observed=len(archives))
    hash_mismatch = 0
    state_mismatch = 0
    final_state_missing = 0
    clock_results: list[dict[str, Any]] = []

    for index, horizon in enumerate(CLOCK_TIMES):
        record = summary["clock_diagnostics"][index]
        path = diagnostic_dir / f"clock_t{index}.npz"
        hash_mismatch += int(sha256(path) != record["raw_npz_sha256"])
        expected_state = expected_initial_state(2026092891, (1, index))
        state_mismatch += int(record["initial_rng_state"] != expected_state)
        final_state_missing += int(not state_is_present(record.get("final_rng_state")))
        with np.load(path, allow_pickle=False) as archive:
            checks.add(f"clock_{index}_fields", set(archive.files) == CLOCK_FIELDS, keys=sorted(archive.files))
            arrays = {name: archive[name].copy() for name in archive.files}
        checks.add(f"clock_{index}_lengths", all(array.shape == (100_000,) for array in arrays.values()))
        leaf = arrays["is_leaf"]
        accepted = arrays["accepted_time"]
        zeta = arrays["accepted_zeta"]
        checks.add(f"clock_{index}_accounting", bool(np.all(arrays["proposals"] == arrays["rejections"] + 1)))
        checks.add(f"clock_{index}_support", bool(
            np.all(accepted[leaf] == 0.0)
            and np.all((accepted[~leaf] > 0.0) & (accepted[~leaf] < horizon))
            and np.all(np.isnan(zeta[leaf]))
            and np.all(np.isfinite(zeta[~leaf]))
        ))
        zeta_difference = float(
            np.max(np.abs(zeta[~leaf] - clock_zeta(accepted[~leaf])))
        ) if np.any(~leaf) else 0.0
        checks.add(
            f"clock_{index}_zeta_from_time",
            zeta_difference <= 5.0e-15,
            maximum=zeta_difference,
        )
        points = horizon * np.asarray((0.0, 0.25, 0.5, 0.75, 1.0))
        empirical = np.asarray([np.mean(accepted <= point) for point in points])
        theory = clock_cdf(float(horizon), points)
        discrepancies = np.abs(empirical - theory)
        maximum = float(np.max(discrepancies))
        checks.add(f"clock_{index}_cdf_gate", maximum <= DKW_THRESHOLD,
                   maximum=maximum, threshold=DKW_THRESHOLD)
        compare_float(checks, f"clock_{index}_reported_maximum", maximum, record["maximum_discrepancy"], 1.0e-14)
        clock_results.append({
            "horizon": float(horizon),
            "points": points,
            "empirical_cdf": empirical,
            "independent_theory_cdf": theory,
            "absolute_discrepancies": discrepancies,
            "maximum_discrepancy": maximum,
            "threshold": DKW_THRESHOLD,
            "leaf_count": int(np.sum(leaf)),
            "total_proposals": int(np.sum(arrays["proposals"])),
            "total_rejections": int(np.sum(arrays["rejections"])),
            "zeta_from_time_max_abs_difference": zeta_difference,
        })

    constant_record = summary["constant_nonendpoint_diagnostic"]
    constant_path = diagnostic_dir / "constant_nonendpoint.npz"
    hash_mismatch += int(sha256(constant_path) != constant_record["raw_npz_sha256"])
    state_mismatch += int(constant_record["initial_rng_state"] != expected_initial_state(2026092892, (2, 0)))
    final_state_missing += int(not state_is_present(constant_record.get("final_rng_state")))
    constant_arrays = load_root_archive(constant_path, 100_000, checks, "constant_nonendpoint")
    constant_invariants = root_invariants(constant_arrays, 4.0, checks, "constant_nonendpoint")
    constant_target = float(stable_scaled_defect(0.625, 4.0))
    constant_mean = float(np.mean(constant_arrays["scaled_output"]))
    constant_std = float(np.std(constant_arrays["scaled_output"], ddof=1))
    constant_error = abs(constant_mean - constant_target)
    checks.add("constant_nonendpoint_gate", constant_error <= CONSTANT_THRESHOLD,
               discrepancy=constant_error, threshold=CONSTANT_THRESHOLD)
    compare_float(checks, "constant_nonendpoint_reported_mean", constant_mean,
                  constant_record["sample_mean_scaled_output"])
    compare_float(checks, "constant_nonendpoint_reported_std", constant_std,
                  constant_record["sample_standard_deviation"])

    endpoint_results: list[dict[str, Any]] = []
    for endpoint in range(2):
        c = (0.5, 0.75)[endpoint]
        for time_index, horizon in enumerate(TIMES):
            flat_index = endpoint * len(TIMES) + time_index
            record = summary["endpoint_diagnostics"][flat_index]
            path = diagnostic_dir / f"endpoint_e{endpoint}_t{time_index}.npz"
            hash_mismatch += int(sha256(path) != record["raw_npz_sha256"])
            state_mismatch += int(
                record["initial_rng_state"]
                != expected_initial_state(2026092893, (3, endpoint, time_index))
            )
            final_state_missing += int(not state_is_present(record.get("final_rng_state")))
            arrays = load_root_archive(path, 128, checks, f"endpoint_{endpoint}_{time_index}")
            invariants = root_invariants(arrays, float(horizon), checks, f"endpoint_{endpoint}_{time_index}")
            target = float(stable_scaled_defect(c, float(horizon)))
            discrepancy = float(np.max(np.abs(arrays["scaled_output"] - target)))
            checks.add(f"endpoint_{endpoint}_{time_index}_pathwise_target", discrepancy <= RANGE_TOLERANCE,
                       maximum=discrepancy)
            endpoint_results.append({
                "endpoint_index": endpoint,
                "time_index": time_index,
                "horizon": float(horizon),
                "target": target,
                "maximum_absolute_discrepancy": discrepancy,
                **invariants,
            })

    checks.add("diagnostic_raw_hashes", hash_mismatch == 0, checked=18, mismatches=hash_mismatch)
    checks.add("diagnostic_initial_pcg64_states", state_mismatch == 0, checked=18, mismatches=state_mismatch)
    checks.add("diagnostic_final_states_present", final_state_missing == 0, checked=18, missing=final_state_missing)
    checks.add("diagnostic_workload", summary.get("official_standalone_accepted_clocks") == 300_000
               and summary.get("official_pde_roots") == 101_792)
    return {
        "clock_diagnostics": clock_results,
        "constant_nonendpoint": {
            "target": constant_target,
            "sample_mean": constant_mean,
            "sample_standard_deviation": constant_std,
            "absolute_discrepancy": constant_error,
            "threshold": CONSTANT_THRESHOLD,
            **constant_invariants,
        },
        "endpoint_diagnostics": endpoint_results,
        "raw_hash_mismatches": hash_mismatch,
        "initial_state_mismatches": state_mismatch,
        "final_states_missing": final_state_missing,
        "producer_elapsed_seconds": float(summary["elapsed_seconds"]),
    }


def audit_primary(checks: Checks, reference: np.ndarray) -> tuple[dict[str, Any], dict[str, Any]]:
    summary = read_json(SAMPLER_DIR / "primary_summary.json")
    checks.add("primary_summary_complete", summary.get("status") == "complete")
    checks.add("primary_declared_counts", summary.get("cells_complete") == 63
               and summary.get("roots_completed") == 630_000)
    cell_records = summary["cell_summaries"]
    checks.add("primary_cell_record_count", len(cell_records) == 63, observed=len(cell_records))

    means = np.empty((3, 7, 3), dtype=np.float64)
    standard_deviations = np.empty_like(means)
    signed_errors = np.empty_like(means)
    mean_nodes = np.empty_like(means)
    mean_proposals = np.empty_like(means)
    max_nodes = np.empty((3, 7, 3), dtype=np.int64)
    max_proposals = np.empty_like(max_nodes)
    sampling_seconds = np.empty_like(means)
    processing_seconds = np.empty_like(means)
    seen: set[tuple[int, int, int]] = set()
    chunk_count = 0
    chunk_hash_mismatches = 0
    chunk_continuity_failures = 0
    total_roots = 0
    initial_state_mismatches = 0
    final_state_missing = 0
    t0_state_mismatches = 0
    t0_value_mismatches = 0
    coefficient_limit_substitutions = 0
    zero_redraws = 0

    seed_to_index = {seed: index for index, seed in enumerate(SEEDS)}
    for cell in cell_records:
        seed = int(cell["seed"])
        ti = int(cell["horizon_index"])
        qi = int(cell["query_index"])
        key = (seed, ti, qi)
        checks.add(f"primary_cell_unique_{seed}_{ti}_{qi}", key not in seen)
        seen.add(key)
        si = seed_to_index[seed]
        horizon = float(TIMES[ti])
        expected_state = expected_initial_state(seed, (0, ti, qi))
        initial_state_mismatches += int(cell["initial_rng_state"] != expected_state)
        final_state_missing += int(not state_is_present(cell.get("final_rng_state")))
        if horizon == 0.0:
            t0_state_mismatches += int(cell["final_rng_state"] != cell["initial_rng_state"])

        chunks = cell["checkpoint_chunks"]
        expected_start = 0
        pieces: dict[str, list[np.ndarray]] = {field: [] for field in ROOT_FIELDS}
        for chunk in chunks:
            path = REPO / chunk["path"]
            chunk_count += 1
            chunk_hash_mismatches += int(sha256(path) != chunk["sha256"])
            start = int(chunk["start_root"])
            end = int(chunk["completed_roots"])
            if start != expected_start or end <= start or end - start > 1000:
                chunk_continuity_failures += 1
            with np.load(path, allow_pickle=False) as archive:
                if set(archive.files) != ROOT_FIELDS:
                    chunk_continuity_failures += 1
                for field in ROOT_FIELDS:
                    values = archive[field].copy()
                    if values.shape != (end - start,):
                        chunk_continuity_failures += 1
                    pieces[field].append(values)
            expected_start = end
        if expected_start != 10_000 or cell["completed_roots"] != 10_000 or cell["status"] != "complete":
            chunk_continuity_failures += 1
        arrays = {field: np.concatenate(values) for field, values in pieces.items()}
        total_roots += arrays["scaled_output"].size
        invariant_record = root_invariants(arrays, horizon, checks, f"primary_{seed}_{ti}_{qi}")
        coefficient_limit_substitutions += invariant_record["coefficient_limit_substitutions"]
        zero_redraws += invariant_record["zero_redraws"]

        if horizon == 0.0:
            expected_z = (1.0, 0.5, 0.0)[qi]
            expected_w = (0.25, 0.375, 0.5)[qi]
            t0_value_mismatches += int(
                not (
                    np.all(arrays["normalized_output"] == expected_z)
                    and np.all(arrays["scaled_output"] == expected_w)
                    and np.all(arrays["nodes"] == 1)
                    and np.all(arrays["leaves"] == 1)
                    and np.all(arrays["binary_internal"] == 0)
                    and np.all(arrays["ternary_internal"] == 0)
                    and np.all(arrays["clock_proposals"] == 0)
                    and np.all(arrays["clock_rejections"] == 0)
                    and np.all(arrays["zero_redraws"] == 0)
                    and np.all(arrays["coefficient_limit_substitution"] == 0)
                )
            )

        values = arrays["scaled_output"]
        means[si, ti, qi] = np.mean(values)
        standard_deviations[si, ti, qi] = np.std(values, ddof=1)
        signed_errors[si, ti, qi] = (means[si, ti, qi] - reference[ti, qi]) / reference[ti, qi]
        mean_nodes[si, ti, qi] = np.mean(arrays["nodes"])
        mean_proposals[si, ti, qi] = np.mean(arrays["clock_proposals"])
        max_nodes[si, ti, qi] = np.max(arrays["nodes"])
        max_proposals[si, ti, qi] = np.max(arrays["clock_proposals"])
        sampling_seconds[si, ti, qi] = float(cell["sampling_seconds"])
        processing_seconds[si, ti, qi] = float(cell["processing_and_io_seconds"])
        compare_float(checks, f"primary_{seed}_{ti}_{qi}_mean", means[si, ti, qi],
                      cell["sample_mean_scaled_output"])
        compare_float(checks, f"primary_{seed}_{ti}_{qi}_std", standard_deviations[si, ti, qi],
                      cell["within_root_standard_deviation"])
        compare_float(checks, f"primary_{seed}_{ti}_{qi}_signed_error", signed_errors[si, ti, qi],
                      cell["signed_relative_error"])

    checks.add("primary_unique_fixed_cells", len(seen) == 63)
    checks.add("primary_chunk_hashes", chunk_hash_mismatches == 0,
               checked=chunk_count, mismatches=chunk_hash_mismatches)
    checks.add("primary_chunk_continuity_and_size", chunk_continuity_failures == 0,
               chunks=chunk_count, failures=chunk_continuity_failures)
    checks.add("primary_total_roots", total_roots == 630_000, observed=total_roots)
    checks.add("primary_initial_pcg64_states", initial_state_mismatches == 0,
               checked=63, mismatches=initial_state_mismatches)
    checks.add("primary_final_states_present", final_state_missing == 0, checked=63, missing=final_state_missing)
    checks.add("primary_t0_no_rng_advance", t0_state_mismatches == 0, checked=9, mismatches=t0_state_mismatches)
    checks.add("primary_t0_exact_values_counts", t0_value_mismatches == 0, checked=9, mismatches=t0_value_mismatches)

    rms = np.sqrt(np.mean(signed_errors**2, axis=0))
    reported_rms = np.full((7, 3), np.nan)
    for row in summary["per_time_query_three_seed_errors"]:
        reported_rms[row["horizon_index"], row["query_index"]] = row["empirical_three_seed_rms"]
    rms_difference = float(np.max(np.abs(rms - reported_rms)))
    checks.add("primary_rms3_recomputed", rms_difference <= SUMMARY_TOLERANCE, maximum=rms_difference)

    sampling_by_seed = np.sum(sampling_seconds, axis=(1, 2))
    processing_by_seed = np.sum(processing_seconds, axis=(1, 2))
    reported_sampling = summary["sampling_seconds_by_seed_for_all_21_queries"]
    sampling_difference = max(
        abs(sampling_by_seed[index] - reported_sampling[str(seed)])
        for index, seed in enumerate(SEEDS)
    )
    checks.add("primary_seed_sampling_times", sampling_difference <= 1.0e-9, maximum=sampling_difference)

    rm = stable_scaled_defect(0.5, TIMES)
    rM = stable_scaled_defect(0.75, TIMES)
    harmonic = 2.0 * rm * rM / (rm + rM)
    mean_ode = stable_scaled_defect(0.625, TIMES)
    harmonic_signed = (harmonic[:, None] - reference) / reference
    mean_signed = (mean_ode[:, None] - reference) / reference
    baseline_rows = []
    for ti, horizon in enumerate(TIMES):
        for qi, query in enumerate(QUERIES):
            baseline_rows.append({
                "horizon_index": ti,
                "query_index": qi,
                "horizon": float(horizon),
                "query": float(query),
                "reference_scaled_value": reference[ti, qi],
                "harmonic_center_scaled_value": harmonic[ti],
                "harmonic_center_signed_relative_error": harmonic_signed[ti, qi],
                "mean_ode_scaled_value": mean_ode[ti],
                "mean_ode_signed_relative_error": mean_signed[ti, qi],
            })

    cell_rows = []
    for si, seed in enumerate(SEEDS):
        for ti, horizon in enumerate(TIMES):
            for qi, query in enumerate(QUERIES):
                cell_rows.append({
                    "seed": seed,
                    "horizon_index": ti,
                    "query_index": qi,
                    "horizon": float(horizon),
                    "query": float(query),
                    "sample_mean_scaled_output": means[si, ti, qi],
                    "within_root_standard_deviation": standard_deviations[si, ti, qi],
                    "signed_relative_error": signed_errors[si, ti, qi],
                    "mean_nodes": mean_nodes[si, ti, qi],
                    "mean_clock_proposals": mean_proposals[si, ti, qi],
                    "maximum_nodes": max_nodes[si, ti, qi],
                    "maximum_clock_proposals": max_proposals[si, ti, qi],
                    "sampling_seconds": sampling_seconds[si, ti, qi],
                    "processing_and_io_seconds": processing_seconds[si, ti, qi],
                })

    tables = {
        "times": TIMES,
        "queries": QUERIES,
        "seeds": list(SEEDS),
        "reference_scaled_values": reference,
        "mc_seed_means": means,
        "within_root_standard_deviations": standard_deviations,
        "signed_relative_errors": signed_errors,
        "empirical_three_seed_rms": rms,
        "per_time_max_of_three_query_rms_diagnostics": np.max(rms, axis=1),
        "mean_nodes_by_seed_time_query": mean_nodes,
        "mean_clock_proposals_by_seed_time_query": mean_proposals,
        "aggregate_mean_nodes_by_time": np.mean(mean_nodes, axis=(0, 2)),
        "aggregate_mean_clock_proposals_by_time": np.mean(mean_proposals, axis=(0, 2)),
        "harmonic_center_scaled_values": harmonic,
        "mean_ode_scaled_values": mean_ode,
        "harmonic_center_signed_relative_errors": harmonic_signed,
        "mean_ode_signed_relative_errors": mean_signed,
        "all_63_cell_rows": cell_rows,
        "all_21_baseline_rows": baseline_rows,
        "sampling_seconds_by_seed_all_21_queries": {
            str(seed): sampling_by_seed[index] for index, seed in enumerate(SEEDS)
        },
        "processing_and_io_seconds_by_seed_all_21_queries": {
            str(seed): processing_by_seed[index] for index, seed in enumerate(SEEDS)
        },
    }
    return tables, {
        "primary_cells": len(seen),
        "primary_roots": total_roots,
        "checkpoint_chunks": chunk_count,
        "chunk_hash_mismatches": chunk_hash_mismatches,
        "chunk_continuity_failures": chunk_continuity_failures,
        "initial_state_mismatches": initial_state_mismatches,
        "final_states_missing": final_state_missing,
        "full_tree_rng_draws_independently_replayed": False,
        "coefficient_limit_substitutions": coefficient_limit_substitutions,
        "zero_redraws": zero_redraws,
        "maximum_empirical_rms3": float(np.max(rms)),
        "maximum_absolute_signed_relative_error": float(np.max(np.abs(signed_errors))),
        "producer_primary_total_elapsed_seconds": float(summary["total_elapsed_seconds"]),
        "sampling_seconds_by_seed": {
            str(seed): sampling_by_seed[index] for index, seed in enumerate(SEEDS)
        },
        "processing_and_io_seconds_by_seed": {
            str(seed): processing_by_seed[index] for index, seed in enumerate(SEEDS)
        },
    }


def make_figures(tables: dict[str, Any]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    times = np.asarray(tables["times"])
    reference = np.asarray(tables["reference_scaled_values"])
    means = np.asarray(tables["mc_seed_means"])
    rms = np.asarray(tables["empirical_three_seed_rms"])
    harmonic_error = np.abs(np.asarray(tables["harmonic_center_signed_relative_errors"]))
    mean_error = np.abs(np.asarray(tables["mean_ode_signed_relative_errors"]))
    work_nodes = np.asarray(tables["aggregate_mean_nodes_by_time"])
    work_proposals = np.asarray(tables["aggregate_mean_clock_proposals_by_time"])

    colors = ("#006D77", "#D1495B", "#6A4C93")
    query_labels = ("x=0", "x=π/2", "x=π")
    seed_markers = ("o", "s", "^")
    fig, axes = plt.subplots(1, 3, figsize=(17.2, 5.4), constrained_layout=True)

    ax = axes[0]
    for qi, label in enumerate(query_labels):
        ax.plot(times, reference[:, qi], color=colors[qi], linewidth=2.4,
                label=f"reference {label}")
        for si, seed in enumerate(SEEDS):
            ax.plot(times, means[si, :, qi], linestyle="none", marker=seed_markers[si],
                    markersize=4.2, markerfacecolor="none", color=colors[qi], alpha=0.8,
                    label=f"MC {label}, seed {str(seed)[-2:]}" if qi == 0 else None)
    ax.set_xscale("symlog", linthresh=0.25)
    ax.set_xlabel("finite horizon T (symlog; includes 0)")
    ax.set_ylabel("scaled defect exp(2T)(1-u)")
    ax.set_title("Reference and 3×10,000-root means")
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=7.2, ncol=2)

    ax = axes[1]
    ax.plot(times, np.max(rms, axis=1), color="#111111", marker="o", linewidth=2.2,
            label="max of 3 query-wise RMS₃ diagnostics")
    for qi, label in enumerate(query_labels):
        ax.plot(times, harmonic_error[:, qi], color=colors[qi], linestyle="--", marker=".",
                label=f"|harmonic rel. error|, {label}")
        ax.plot(times, mean_error[:, qi], color=colors[qi], linestyle=":", marker="x",
                label=f"|mean-ODE rel. error|, {label}")
    ax.set_xscale("symlog", linthresh=0.25)
    ax.set_yscale("log")
    ax.set_xlabel("finite horizon T (symlog; includes 0)")
    ax.set_ylabel("relative diagnostic")
    ax.set_title("All fixed errors; all 21 values retained in JSON")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=6.8)

    ax = axes[2]
    ax.plot(times, work_nodes, color="#00798C", marker="o", linewidth=2.2,
            label="empirical mean nodes (90k roots/T)")
    ax.plot(times, work_proposals, color="#D1495B", marker="s", linewidth=2.2,
            label="empirical mean proposals (90k roots/T)")
    ax.axhline(THEORETICAL_MEAN_NODES, color="#00798C", linestyle="--", linewidth=1.5,
               label="theoretical E[nodes] upper bound")
    ax.axhline(THEORETICAL_MEAN_PROPOSALS, color="#D1495B", linestyle="--", linewidth=1.5,
               label="theoretical E[proposals] upper bound")
    ax.set_xscale("symlog", linthresh=0.25)
    ax.set_xlabel("finite horizon T (symlog; includes 0)")
    ax.set_ylabel("root work count")
    ax.set_title("Empirical work means vs expectation bounds")
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=7.2)

    fig.suptitle(
        "Two-barrier experiment — fixed v(x)=5/8+(1/8)cos x; 3 seeds; 10,000 roots/cell",
        fontsize=13,
    )
    fig.savefig(PNG_PATH, dpi=180)
    fig.savefig(SVG_PATH)
    plt.close(fig)


def run() -> int:
    manifest = verify_manifest()
    protected_outputs = (AUDIT_DIR / "audit_summary.json", AUDIT_DIR / "derived_tables.json",
                         AUDIT_DIR / "audit_failure.json", PNG_PATH, SVG_PATH)
    if any(path.exists() for path in protected_outputs):
        raise FileExistsError("refusing to overwrite an attempted or completed audit")
    started = time.monotonic()
    checks = Checks()
    try:
        initial_hashes = verify_initial_hashes(checks)
        producer_hashes = verify_producer_hashes(checks)
        reference, reference_audit = audit_reference(checks)
        diagnostics_audit = audit_diagnostics(checks)
        tables, primary_audit = audit_primary(checks, reference)

        comparator = reference_audit["predesignated_comparator"]
        comparator_seconds = float(comparator["solve_plus_all_queries_seconds"])
        timing_rows = []
        for seed in SEEDS:
            sampler_seconds = float(primary_audit["sampling_seconds_by_seed"][str(seed)])
            timing_rows.append({
                "seed": seed,
                "sampler_21_query_sampling_seconds": sampler_seconds,
                "fixed_k16_loose_solve_plus_21_queries_seconds": comparator_seconds,
                "ratio_sampler_sampling_to_fixed_comparator": sampler_seconds / comparator_seconds,
                "comparator_excludes_basis_system_construction": True,
                "comparison_is_not_equal_accuracy_or_optimized": True,
            })
        tables["fixed_timing_comparison"] = {
            "rows": timing_rows,
            "reference_validation_costs": reference_audit["six_run_timings"],
            "producer_processing_and_io_seconds_by_seed": primary_audit[
                "processing_and_io_seconds_by_seed"
            ],
            "producer_preflight_elapsed_seconds": float(
                read_json(SAMPLER_DIR / "preflight_results.json")["elapsed_seconds"]
            ),
            "producer_official_diagnostics_elapsed_seconds": diagnostics_audit[
                "producer_elapsed_seconds"
            ],
            "producer_primary_total_wall_seconds": primary_audit[
                "producer_primary_total_elapsed_seconds"
            ],
            "reference_comparator_scope": (
                "one k16-loose Radau solve plus all 21 fixed query evaluations; "
                "basis and system construction excluded"
            ),
            "scope": "fixed implementations; no equal-accuracy, optimality, speedup, or general superiority claim",
        }
        tables["theoretical_expectation_bounds"] = {
            "mean_nodes": THEORETICAL_MEAN_NODES,
            "mean_clock_proposals": THEORETICAL_MEAN_PROPOSALS,
            "not_per_root_caps": True,
        }
        tables["diagnostics"] = diagnostics_audit

        write_json_new(AUDIT_DIR / "derived_tables.json", tables)
        make_figures(tables)
        checks.add("png_created", PNG_PATH.is_file() and PNG_PATH.stat().st_size > 0)
        checks.add("svg_created", SVG_PATH.is_file() and SVG_PATH.stat().st_size > 0)
        result = {
            "schema_version": 1,
            "status": "PASS" if checks.passed else "FAIL",
            "created_utc": utc_now(),
            "elapsed_seconds": time.monotonic() - started,
            "manifest_sha256": sha256(AUDIT_DIR / "execution_manifest.json"),
            "manifest_input_file_count": manifest["input_file_count"],
            "checks_passed": sum(record["passed"] for record in checks.records),
            "checks_total": len(checks.records),
            "failures": checks.failures,
            "checks": checks.records,
            "initial_protected_hashes": initial_hashes,
            "producer_source_and_gate_hashes": producer_hashes,
            "reference_audit": reference_audit,
            "diagnostics_audit": diagnostics_audit,
            "primary_audit": primary_audit,
            "outputs": {
                "derived_tables": relative_path(AUDIT_DIR / "derived_tables.json"),
                "png": relative_path(PNG_PATH),
                "svg": relative_path(SVG_PATH),
            },
            "rng_scope": {
                "fixed_initial_pcg64_states_reconstructed": 81,
                "final_state_records_checked_present": 81,
                "full_tree_rng_draws_independently_replayed": False,
            },
            "interpretation": {
                "raw_evidence_recomputed": True,
                "finite_case_empirical_audit": True,
                "not_floating_unbiasedness_certificate": True,
                "not_all_horizon_proof": True,
                "not_equal_accuracy_or_optimality_comparison": True,
            },
        }
        write_json_new(AUDIT_DIR / "audit_summary.json", result)
        print(json.dumps({
            "status": result["status"],
            "checks": f"{result['checks_passed']}/{result['checks_total']}",
            "primary_roots": primary_audit["primary_roots"],
            "output": str(AUDIT_DIR),
        }))
        return 0 if checks.passed else 3
    except Exception as exc:
        failure = {
            "schema_version": 1,
            "status": "ERROR",
            "created_utc": utc_now(),
            "elapsed_seconds": time.monotonic() - started,
            "exception_type": type(exc).__name__,
            "exception": str(exc),
            "traceback": traceback.format_exc(),
            "checks": checks.records,
            "failures": checks.failures,
        }
        write_json_new(AUDIT_DIR / "audit_failure.json", failure)
        raise


def status() -> None:
    primary = SAMPLER_DIR / "primary_summary.json"
    payload: dict[str, Any] = {"primary_summary_exists": primary.is_file()}
    if primary.is_file():
        summary = read_json(primary)
        payload.update({
            "primary_status": summary.get("status"),
            "cells_complete": summary.get("cells_complete"),
            "roots_completed": summary.get("roots_completed"),
        })
    print(json.dumps(payload, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("status", "prepare", "run"))
    args = parser.parse_args()
    if args.action == "status":
        status()
        return 0
    if args.action == "prepare":
        prepare()
        return 0
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
