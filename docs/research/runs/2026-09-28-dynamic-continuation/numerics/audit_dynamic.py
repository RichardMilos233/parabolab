"""Independent streaming audit of the dynamic-continuation primary artifacts.

The auditor intentionally does not import the producer, interface, sampler, or
reference Python modules.  It reads each stage archive once, recomputes the
statistics and six-segment metric projection, and writes a compact audit record.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time

import mpmath as mp
import numpy as np
from scipy import special


HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO = HERE.parents[4]
ARTIFACTS = RUN_DIR / "artifacts"
REFERENCE_NPZ = ARTIFACTS / "reference" / "reference.npz"
REFERENCE_JSON = ARTIFACTS / "reference" / "reference.json"
INITIAL_HASHES = RUN_DIR / "initial-source-hashes.json"

SEEDS = (2026092801, 2026092802, 2026092803)
STAGES = 200
ROOTS_PER_STAGE = 100_000
H = 0.08
GRID_SIZE = 16_384
TOTAL_ROOTS = 60_000_000
M = 0.05
A = 2.0 / 21.0
KAPPA = math.sqrt(40.0 / 21.0)
PERIOD = 4.0 * float(special.ellipk(M)) / KAPPA
LOWER = 0.9
UPPER = 1.0
SLOPE_WIDTH = 2.0 / 735.0
TERMINAL_CODES = ("Id", "Dx", "F0", "F1", "F2", "F3")
ERROR_NAMES = ("mc", "g", "0.95g", "0.9g")

STAGE_FIELDS = {
    "X",
    "H",
    "node_counts",
    "root_branch_flags",
    "terminal_counts",
    "terminal_code_order",
    "prior_c",
    "bhat",
    "raw_c",
    "projected_c",
    "gram",
    "stage",
    "time",
    "h",
    "seed",
    "scheduled_roots",
    "completed_roots",
    "complete",
    "sampling_seconds",
    "stage_seconds",
    "rng_bit_generator",
    "rng_state_before_stage_json",
    "rng_state_after_stage_json",
    "source_hashes_json",
    "reference_record_json",
    "error_names",
    "normalized_spatial_rms_errors",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def independent_gram() -> tuple[np.ndarray, dict[str, object]]:
    """Rebuild G from the elliptic-moment recurrence at 80 decimal digits."""

    with mp.workdps(80):
        m = mp.mpf(1) / 20
        a = mp.mpf(2) / 21
        constant = mp.mpf(80) / 441
        i1 = mp.mpf(40) / 21 * (1 - mp.ellipe(m) / mp.ellipk(m))
        i2 = (4 * i1 - constant) / 3
        i3 = (8 * i2 - 3 * constant * i1) / 5
        matrix_mp = (
            (i1 - 2 * i2 / a + i3 / a**2, i2 / a - i3 / a**2),
            (i2 / a - i3 / a**2, i3 / a**2),
        )
        decimal_values = [[mp.nstr(value, 60) for value in row] for row in matrix_mp]
        matrix = np.asarray(matrix_mp, dtype=np.float64)
    eigenvalues = np.linalg.eigvalsh(matrix)
    return matrix, {
        "method": "80-decimal elliptic-moment recurrence",
        "decimal_values": decimal_values,
        "binary64": matrix.tolist(),
        "eigenvalues": eigenvalues.tolist(),
        "condition_number": float(eigenvalues[-1] / eigenvalues[0]),
        "positive_definite": bool(np.all(eigenvalues > 0.0)),
    }


def g_values(x: np.ndarray) -> np.ndarray:
    sn, _, _, _ = special.ellipj(KAPPA * np.asarray(x, dtype=float), M)
    return math.sqrt(A) * sn


def basis_values(x: np.ndarray) -> np.ndarray:
    g = g_values(x)
    ratio = g * g / A
    return np.column_stack((g * (1.0 - ratio), g * ratio))


def interface_values(coefficients: np.ndarray, g: np.ndarray) -> np.ndarray:
    ratio = g * g / A
    return g * (coefficients[0] + (coefficients[1] - coefficients[0]) * ratio)


def feasible(coefficients: np.ndarray, tolerance: float = 2.0e-14) -> bool:
    return bool(
        coefficients.shape == (2,)
        and np.all(np.isfinite(coefficients))
        and np.all(coefficients >= LOWER - tolerance)
        and np.all(coefficients <= UPPER + tolerance)
        and abs(float(coefficients[1] - coefficients[0]))
        <= SLOPE_WIDTH + tolerance
    )


def independent_project(raw: np.ndarray, gram: np.ndarray) -> tuple[np.ndarray, dict]:
    """Project by the closed-form minimizer on each of six polygon segments."""

    vertices = np.asarray(
        (
            (LOWER, LOWER),
            (LOWER + SLOPE_WIDTH, LOWER),
            (UPPER, UPPER - SLOPE_WIDTH),
            (UPPER, UPPER),
            (UPPER - SLOPE_WIDTH, UPPER),
            (LOWER, LOWER + SLOPE_WIDTH),
        ),
        dtype=float,
    )
    candidates: list[tuple[str, np.ndarray]] = []
    if feasible(raw, tolerance=0.0):
        candidates.append(("interior", raw.copy()))
    for index in range(6):
        start = vertices[index]
        direction = vertices[(index + 1) % 6] - start
        denominator = float(direction @ gram @ direction)
        parameter = -float(direction @ gram @ (start - raw)) / denominator
        parameter = float(np.clip(parameter, 0.0, 1.0))
        candidates.append((f"edge_{index}", start + parameter * direction))

    def objective(candidate: np.ndarray) -> float:
        difference = candidate - raw
        return float(difference @ gram @ difference)

    label, projected = min(candidates, key=lambda item: objective(item[1]))
    vi = (vertices - projected) @ gram @ (projected - raw)
    return projected, {
        "active_candidate": label,
        "metric_squared_distance": objective(projected),
        "variational_inequality_minimum": float(np.min(vi)),
        "projected": label != "interior",
    }


def max_abs_difference(left: object, right: object) -> float:
    a = np.asarray(left, dtype=float)
    b = np.asarray(right, dtype=float)
    if a.shape != b.shape:
        return math.inf
    return float(np.max(np.abs(a - b))) if a.size else 0.0


def normalized_error(left: np.ndarray, right: np.ndarray) -> float:
    difference = left - right
    return float(np.sqrt(np.mean(difference * difference)))


def load_reference() -> tuple[dict, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    record = read_json(REFERENCE_JSON)
    assert isinstance(record, dict)
    with np.load(REFERENCE_NPZ, allow_pickle=False) as archive:
        times = np.asarray(archive["times"], dtype=float)
        modes = np.asarray(archive["odd_modes"], dtype=float)
        coefficients = np.asarray(archive["coefficients"], dtype=float)
        period = float(archive["period"])
        omega = float(archive["omega"])
    grid = np.arange(GRID_SIZE, dtype=float) * period / GRID_SIZE
    sine_basis = math.sqrt(2.0) * np.sin(grid[:, None] * omega * modes[None, :])
    values = coefficients @ sine_basis.T
    return record, times, grid, values, g_values(grid)


def audit(output: Path) -> dict[str, object]:
    started = time.perf_counter()
    checks: dict[str, bool] = {}
    counts: dict[str, int] = {}
    differences = {
        name: 0.0
        for name in (
            "gram",
            "bhat",
            "raw_c",
            "projected_c",
            "projection_metric",
            "projection_vi",
            "observation_covariance",
            "estimator_covariance",
            "observation_second_moments",
            "tree_value_mean",
            "tree_value_second_moment",
            "tree_value_sample_variance",
            "max_absolute_tree_value",
            "mean_nodes",
            "root_branch_fraction",
            "normalized_spatial_rms_errors",
        )
    }
    failures: list[str] = []

    def check(name: str, condition: bool, detail: str | None = None) -> None:
        checks[name] = checks.get(name, True) and bool(condition)
        if not condition and detail is not None and len(failures) < 100:
            failures.append(f"{name}: {detail}")

    gram, gram_record = independent_gram()
    check("independent_gram_positive_definite", gram_record["positive_definite"])

    reference_json, reference_times, grid, reference_values, grid_g = load_reference()
    reference_floor = np.asarray(reference_json.get("convergence_per_time"), dtype=float)
    reference_hashes = {
        "reference.npz": sha256(REFERENCE_NPZ),
        "reference.json": sha256(REFERENCE_JSON),
    }
    check("reference_acceptance", reference_json.get("passed") is True)
    check(
        "reference_npz_hash",
        reference_json.get("artifact_hashes_sha256", {}).get("reference.npz")
        == reference_hashes["reference.npz"],
    )
    check(
        "reference_time_grid",
        np.array_equal(reference_times, np.arange(STAGES + 1, dtype=float) * H),
    )
    check(
        "reference_floor_shape",
        reference_floor.shape == (STAGES + 1,) and np.all(np.isfinite(reference_floor)),
    )

    baseline_errors = {
        "g": [normalized_error(grid_g, value) for value in reference_values],
        "0.95g": [normalized_error(0.95 * grid_g, value) for value in reference_values],
        "0.9g": [normalized_error(0.9 * grid_g, value) for value in reference_values],
    }
    t0_proxy_discrepancy = baseline_errors["0.9g"][0]

    protected = read_json(INITIAL_HASHES)
    assert isinstance(protected, dict)
    protected_missing = 0
    protected_mismatch = 0
    for relative, expected_hash in protected.items():
        path = REPO / relative
        if not path.is_file():
            protected_missing += 1
        elif sha256(path) != expected_hash:
            protected_mismatch += 1
    counts["protected_expected"] = len(protected)
    counts["protected_missing"] = protected_missing
    counts["protected_hash_mismatch"] = protected_mismatch
    check("all_342_initial_files_present", len(protected) == 342 and protected_missing == 0)
    check("all_342_initial_hashes_match", protected_mismatch == 0)

    initial_hash_file_hash = sha256(INITIAL_HASHES)
    seed_outputs: list[dict[str, object]] = []
    total_roots = 0
    total_nodes = 0
    total_stages = 0
    total_manifest_files = 0
    total_projection_count = 0
    global_min_vi = math.inf
    manifest_hashes: dict[str, str] = {}

    for seed in SEEDS:
        seed_dir = ARTIFACTS / f"dynamic_seed_{seed}"
        progress_path = seed_dir / "progress.json"
        source_path = seed_dir / "source-record.json"
        manifest_path = seed_dir / "artifact-hashes.json"
        progress = read_json(progress_path)
        source = read_json(source_path)
        manifest = read_json(manifest_path)
        assert isinstance(progress, dict) and isinstance(source, dict)
        assert isinstance(manifest, dict)
        entries = progress.get("entries", [])
        manifest_files = manifest.get("files", {})
        assert isinstance(entries, list) and isinstance(manifest_files, dict)

        actual_files = {
            str(path.relative_to(seed_dir))
            for path in seed_dir.rglob("*")
            if path.is_file() and path != manifest_path
        }
        check(
            "manifest_file_sets_exact",
            actual_files == set(manifest_files),
            f"seed {seed}",
        )
        check(
            "manifest_metadata",
            manifest.get("algorithm") == "sha256"
            and manifest.get("manifest_excludes_itself") is True,
            f"seed {seed}",
        )
        total_manifest_files += len(manifest_files)
        manifest_hashes[str(seed)] = sha256(manifest_path)

        source_hashes = source.get("source_hashes_sha256", {})
        check(
            "source_record_contract",
            source.get("frozen_contract", {}).get("n_roots_per_stage") == ROOTS_PER_STAGE
            and source.get("frozen_contract", {}).get("stages") == STAGES
            and source.get("frozen_contract", {}).get("slab_h") == H
            and source.get("frozen_contract", {}).get("grid_points") == GRID_SIZE
            and source.get("frozen_contract", {}).get("initial_coefficients")
            == [0.9, 0.9],
            f"seed {seed}",
        )
        for name, expected_hash in source_hashes.items():
            copy_path = seed_dir / "source" / name
            check(
                "frozen_source_copy_hashes",
                copy_path.is_file() and sha256(copy_path) == expected_hash,
                f"seed {seed}, {name}",
            )
        check(
            "source_record_reference_hashes",
            source.get("reference", {}).get("npz_sha256")
            == reference_hashes["reference.npz"]
            and source.get("reference", {}).get("json_sha256")
            == reference_hashes["reference.json"],
            f"seed {seed}",
        )

        for relative in ("progress.json", "source-record.json"):
            check(
                "manifest_hashes_match",
                manifest_files.get(relative) == sha256(seed_dir / relative),
                f"seed {seed}, {relative}",
            )
        for relative in sorted(name for name in manifest_files if name.startswith("source/")):
            check(
                "manifest_hashes_match",
                manifest_files[relative] == sha256(seed_dir / relative),
                f"seed {seed}, {relative}",
            )

        check(
            "progress_primary_contract",
            progress.get("schema_version") == 1
            and progress.get("status") == "complete"
            and progress.get("seed") == seed
            and progress.get("scheduled_stages") == STAGES
            and progress.get("completed_stages") == STAGES
            and progress.get("n_roots_per_stage") == ROOTS_PER_STAGE
            and progress.get("slab_h") == H
            and progress.get("reference_npz_sha256") == reference_hashes["reference.npz"]
            and len(entries) == STAGES,
            f"seed {seed}",
        )
        check(
            "progress_source_hashes",
            progress.get("source_hashes_sha256") == source_hashes,
            f"seed {seed}",
        )

        previous_projected = np.asarray((0.9, 0.9), dtype=float)
        previous_rng_after: dict | None = None
        initial_rng_state = np.random.default_rng(seed).bit_generator.state
        coefficients = [previous_projected.tolist()]
        raw_coefficients: list[list[float] | None] = [None]
        errors = {name: [0.0 if name == "mc" else baseline_errors[name][0]] for name in ERROR_NAMES}
        projection_active = [False]
        projection_candidate = ["initial"]
        tree_second_moment: list[float | None] = [None]
        tree_sample_variance: list[float | None] = [None]
        tree_mean: list[float | None] = [None]
        max_abs_tree: list[float | None] = [None]
        stage_nodes = [0]
        max_nodes = [0]
        mean_nodes: list[float | None] = [None]
        branch_fraction: list[float | None] = [None]
        stage_roots = [0]
        sampling_seconds = [0.0]
        stage_seconds = [0.0]
        terminal_counts = [[0] * 6]
        seed_projection_count = 0
        seed_nodes = 0
        seed_roots = 0
        seed_sampling_seconds = 0.0
        seed_stage_seconds = 0.0

        for stage, row in enumerate(entries, start=1):
            stage_path = seed_dir / f"stage_{stage:03d}.npz"
            stage_hash = sha256(stage_path)
            check(
                "manifest_hashes_match",
                manifest_files.get(stage_path.name) == stage_hash,
                f"seed {seed}, stage {stage}",
            )
            check(
                "progress_archive_hashes_match",
                row.get("archive") == stage_path.name
                and row.get("archive_sha256") == stage_hash,
                f"seed {seed}, stage {stage}",
            )

            with np.load(stage_path, allow_pickle=False) as archive:
                check(
                    "stage_schema_exact",
                    set(archive.files) == STAGE_FIELDS,
                    f"seed {seed}, stage {stage}",
                )
                x = np.asarray(archive["X"], dtype=float)
                values = np.asarray(archive["H"], dtype=float)
                nodes = np.asarray(archive["node_counts"], dtype=np.int64)
                branched = np.asarray(archive["root_branch_flags"], dtype=bool)
                codes = np.asarray(archive["terminal_counts"], dtype=np.int64)
                archived_prior = np.asarray(archive["prior_c"], dtype=float)
                archived_bhat = np.asarray(archive["bhat"], dtype=float)
                archived_raw = np.asarray(archive["raw_c"], dtype=float)
                archived_projected = np.asarray(archive["projected_c"], dtype=float)
                archived_gram = np.asarray(archive["gram"], dtype=float)
                archived_errors = np.asarray(
                    archive["normalized_spatial_rms_errors"], dtype=float
                )
                rng_before = json.loads(str(archive["rng_state_before_stage_json"].item()))
                rng_after = json.loads(str(archive["rng_state_after_stage_json"].item()))
                archive_source_hashes = json.loads(str(archive["source_hashes_json"].item()))
                archive_reference = json.loads(str(archive["reference_record_json"].item()))

                scalar_ok = (
                    int(archive["stage"]) == stage
                    and float(archive["time"]) == stage * H
                    and float(archive["h"]) == H
                    and int(archive["seed"]) == seed
                    and int(archive["scheduled_roots"]) == ROOTS_PER_STAGE
                    and int(archive["completed_roots"]) == ROOTS_PER_STAGE
                    and bool(archive["complete"])
                    and str(archive["rng_bit_generator"]) == "PCG64"
                    and list(archive["terminal_code_order"]) == list(TERMINAL_CODES)
                    and list(archive["error_names"]) == list(ERROR_NAMES)
                )
                archived_sampling_seconds = float(archive["sampling_seconds"])
                archived_stage_seconds = float(archive["stage_seconds"])

            check("stage_scalar_contract", scalar_ok, f"seed {seed}, stage {stage}")
            check(
                "stage_array_shapes",
                x.shape == (ROOTS_PER_STAGE,)
                and values.shape == (ROOTS_PER_STAGE,)
                and nodes.shape == (ROOTS_PER_STAGE,)
                and branched.shape == (ROOTS_PER_STAGE,)
                and codes.shape == (6,)
                and archived_prior.shape == (2,)
                and archived_bhat.shape == (2,)
                and archived_raw.shape == (2,)
                and archived_projected.shape == (2,)
                and archived_gram.shape == (2, 2)
                and archived_errors.shape == (4,),
                f"seed {seed}, stage {stage}",
            )
            check(
                "raw_arrays_valid",
                np.all(np.isfinite(x))
                and np.all((x >= 0.0) & (x < PERIOD))
                and np.all(np.isfinite(values))
                and np.all(nodes >= 1)
                and np.all(codes >= 0),
                f"seed {seed}, stage {stage}",
            )
            check(
                "stage_source_hashes",
                archive_source_hashes == source_hashes,
                f"seed {seed}, stage {stage}",
            )
            check(
                "stage_reference_hashes",
                archive_reference.get("npz_sha256") == reference_hashes["reference.npz"]
                and archive_reference.get("json_sha256") == reference_hashes["reference.json"]
                and archive_reference.get("grid_points") == GRID_SIZE
                and archive_reference.get("convergence_max")
                == reference_json.get("convergence_max"),
                f"seed {seed}, stage {stage}",
            )
            check(
                "progress_stage_contract",
                row.get("stage") == stage
                and row.get("time") == stage * H
                and row.get("complete") is True
                and row.get("terminal_source")
                == "fixed_known_g_with_preceding_stored_coefficients"
                and row.get("errors", {}).get("grid_points") == GRID_SIZE,
                f"seed {seed}, stage {stage}",
            )
            check(
                "reference_floor_links",
                float(row.get("reference_convergence_floor"))
                == float(reference_floor[stage]),
                f"seed {seed}, stage {stage}",
            )

            differences["gram"] = max(
                differences["gram"], max_abs_difference(archived_gram, gram)
            )
            check(
                "independent_gram_matches_archives",
                np.array_equal(archived_gram, gram),
                f"seed {seed}, stage {stage}",
            )

            check(
                "exact_previous_coefficient_chain",
                np.array_equal(archived_prior, previous_projected)
                and row.get("prior_coefficients") == previous_projected.tolist(),
                f"seed {seed}, stage {stage}",
            )

            if stage == 1:
                check(
                    "rng_initial_states",
                    rng_before == initial_rng_state,
                    f"seed {seed}",
                )
            else:
                check(
                    "rng_after_before_links",
                    rng_before == previous_rng_after,
                    f"seed {seed}, stage {stage}",
                )
            replay = np.random.default_rng()
            replay.bit_generator.state = rng_before
            replayed_positions = replay.uniform(0.0, PERIOD, size=ROOTS_PER_STAGE)
            check(
                "rng_positions_replay_exact",
                np.array_equal(replayed_positions, x),
                f"seed {seed}, stage {stage}",
            )
            previous_rng_after = rng_after

            observations = values[:, None] * basis_values(x)
            bhat = np.mean(observations, axis=0)
            raw = np.linalg.solve(gram, bhat)
            projected, projection = independent_project(raw, gram)
            covariance = np.cov(observations, rowvar=False, ddof=1)
            estimator_covariance = covariance / ROOTS_PER_STAGE
            observation_second = np.mean(observations * observations, axis=0)
            moments = {
                "tree_value_mean": float(np.mean(values)),
                "tree_value_second_moment": float(np.mean(values * values)),
                "tree_value_sample_variance": float(np.var(values, ddof=1)),
                "max_absolute_tree_value": float(np.max(np.abs(values))),
                "mean_nodes": float(np.mean(nodes)),
                "root_branch_fraction": float(np.mean(branched)),
            }

            recomputed_error_values = np.asarray(
                (
                    normalized_error(
                        interface_values(projected, grid_g), reference_values[stage]
                    ),
                    baseline_errors["g"][stage],
                    baseline_errors["0.95g"][stage],
                    baseline_errors["0.9g"][stage],
                )
            )

            comparisons = {
                "bhat": (bhat, archived_bhat, row.get("bhat")),
                "raw_c": (raw, archived_raw, row.get("raw_coefficients")),
                "projected_c": (
                    projected,
                    archived_projected,
                    row.get("projected_coefficients"),
                ),
                "observation_covariance": (
                    covariance,
                    covariance,
                    row.get("coefficient_observation_covariance"),
                ),
                "estimator_covariance": (
                    estimator_covariance,
                    estimator_covariance,
                    row.get("coefficient_estimator_covariance"),
                ),
                "observation_second_moments": (
                    observation_second,
                    observation_second,
                    row.get("coefficient_observation_second_moments"),
                ),
                "normalized_spatial_rms_errors": (
                    recomputed_error_values,
                    archived_errors,
                    [row["errors"]["normalized_spatial_rms"][name] for name in ERROR_NAMES],
                ),
            }
            for name, (recomputed, archived, progress_value) in comparisons.items():
                difference = max(
                    max_abs_difference(recomputed, archived),
                    max_abs_difference(recomputed, progress_value),
                )
                differences[name] = max(differences[name], difference)

            for name, recomputed in moments.items():
                differences[name] = max(
                    differences[name],
                    abs(recomputed - float(row[name])),
                )
            differences["projection_metric"] = max(
                differences["projection_metric"],
                abs(
                    projection["metric_squared_distance"]
                    - float(row["projection"]["metric_squared_distance"])
                ),
            )
            differences["projection_vi"] = max(
                differences["projection_vi"],
                abs(
                    projection["variational_inequality_minimum"]
                    - float(row["projection"]["variational_inequality_minimum"])
                ),
            )
            global_min_vi = min(
                global_min_vi, projection["variational_inequality_minimum"]
            )

            check(
                "bhat_recomputed",
                max_abs_difference(bhat, archived_bhat) <= 5.0e-16,
                f"seed {seed}, stage {stage}",
            )
            check(
                "raw_coefficients_recomputed",
                max_abs_difference(raw, archived_raw) <= 5.0e-14,
                f"seed {seed}, stage {stage}",
            )
            check(
                "six_segment_projection_recomputed",
                max_abs_difference(projected, archived_projected) <= 5.0e-14
                and projection["active_candidate"]
                == row["projection"]["active_candidate"]
                and projection["projected"] == row["projection"]["projected"],
                f"seed {seed}, stage {stage}",
            )
            check(
                "projected_coefficients_feasible",
                feasible(projected),
                f"seed {seed}, stage {stage}",
            )
            check(
                "projection_variational_inequality",
                projection["variational_inequality_minimum"] >= -5.0e-15,
                f"seed {seed}, stage {stage}",
            )
            check(
                "summary_moments_recomputed",
                max(
                    differences["observation_covariance"],
                    differences["estimator_covariance"],
                    differences["observation_second_moments"],
                    differences["tree_value_mean"],
                    differences["tree_value_second_moment"],
                    differences["tree_value_sample_variance"],
                    differences["max_absolute_tree_value"],
                    differences["mean_nodes"],
                    differences["root_branch_fraction"],
                )
                <= 5.0e-14,
                f"seed {seed}, stage {stage}",
            )
            check(
                "four_errors_recomputed",
                max_abs_difference(recomputed_error_values, archived_errors) <= 5.0e-14,
                f"seed {seed}, stage {stage}",
            )

            exact_counts = (
                int(row["root_count"]) == ROOTS_PER_STAGE
                and int(row["total_nodes"]) == int(np.sum(nodes))
                and int(row["max_nodes"]) == int(np.max(nodes))
                and int(row["root_branch_count"]) == int(np.sum(branched))
                and row["terminal_code_counts"] == codes.tolist()
                and row["terminal_code_order"] == list(TERMINAL_CODES)
                and float(row["sampling_seconds"]) == archived_sampling_seconds
                and float(row["stage_seconds"]) == archived_stage_seconds
            )
            check("work_counts_recomputed", exact_counts, f"seed {seed}, stage {stage}")

            coefficients.append(projected.tolist())
            raw_coefficients.append(raw.tolist())
            for index, name in enumerate(ERROR_NAMES):
                errors[name].append(float(recomputed_error_values[index]))
            projection_active.append(bool(projection["projected"]))
            projection_candidate.append(str(projection["active_candidate"]))
            tree_second_moment.append(moments["tree_value_second_moment"])
            tree_sample_variance.append(moments["tree_value_sample_variance"])
            tree_mean.append(moments["tree_value_mean"])
            max_abs_tree.append(moments["max_absolute_tree_value"])
            stage_node_count = int(np.sum(nodes))
            stage_nodes.append(stage_node_count)
            max_nodes.append(int(np.max(nodes)))
            mean_nodes.append(moments["mean_nodes"])
            branch_fraction.append(moments["root_branch_fraction"])
            stage_roots.append(ROOTS_PER_STAGE)
            sampling_seconds.append(archived_sampling_seconds)
            stage_seconds.append(archived_stage_seconds)
            terminal_counts.append(codes.tolist())

            seed_projection_count += int(projection["projected"])
            seed_nodes += stage_node_count
            seed_roots += ROOTS_PER_STAGE
            seed_sampling_seconds += archived_sampling_seconds
            seed_stage_seconds += archived_stage_seconds
            previous_projected = projected

        check(
            "progress_aggregate_counts",
            progress.get("roots_completed") == seed_roots
            and progress.get("total_nodes") == seed_nodes,
            f"seed {seed}",
        )
        seed_outputs.append(
            {
                "seed": seed,
                "status": progress.get("status"),
                "completed_stages": len(entries),
                "root_count": seed_roots,
                "total_nodes": seed_nodes,
                "projection_count": seed_projection_count,
                "whole_run_elapsed_seconds": float(progress["elapsed_seconds"]),
                "sum_sampling_seconds": seed_sampling_seconds,
                "sum_stage_seconds": seed_stage_seconds,
                "times": reference_times.tolist(),
                "coefficients": coefficients,
                "raw_coefficients": raw_coefficients,
                "errors": errors,
                "projection_active": projection_active,
                "projection_candidate": projection_candidate,
                "tree_value_mean": tree_mean,
                "tree_value_second_moment": tree_second_moment,
                "tree_value_sample_variance": tree_sample_variance,
                "max_absolute_tree_value": max_abs_tree,
                "stage_roots": stage_roots,
                "stage_nodes": stage_nodes,
                "mean_nodes": mean_nodes,
                "max_nodes": max_nodes,
                "root_branch_fraction": branch_fraction,
                "sampling_seconds": sampling_seconds,
                "stage_seconds": stage_seconds,
                "terminal_code_counts": terminal_counts,
            }
        )
        total_stages += len(entries)
        total_roots += seed_roots
        total_nodes += seed_nodes
        total_projection_count += seed_projection_count

    counts.update(
        {
            "seeds": len(seed_outputs),
            "stages": total_stages,
            "roots": total_roots,
            "nodes": total_nodes,
            "manifest_files": total_manifest_files,
            "projections": total_projection_count,
        }
    )
    check("exactly_600_complete_stages", total_stages == 600)
    check("exactly_60_million_roots", total_roots == TOTAL_ROOTS)

    strict_tolerances = {
        "gram": 0.0,
        "bhat": 5.0e-16,
        "raw_c": 5.0e-14,
        "projected_c": 5.0e-14,
        "projection_metric": 5.0e-16,
        "projection_vi": 5.0e-16,
        "observation_covariance": 5.0e-16,
        "estimator_covariance": 5.0e-20,
        "observation_second_moments": 5.0e-16,
        "tree_value_mean": 5.0e-16,
        "tree_value_second_moment": 5.0e-16,
        "tree_value_sample_variance": 5.0e-16,
        "max_absolute_tree_value": 0.0,
        "mean_nodes": 0.0,
        "root_branch_fraction": 0.0,
        "normalized_spatial_rms_errors": 5.0e-14,
    }
    for name, tolerance in strict_tolerances.items():
        check(
            f"max_difference_{name}",
            differences[name] <= tolerance,
            f"{differences[name]} > {tolerance}",
        )

    source_hashes = {
        "audit_dynamic.py": sha256(HERE / "audit_dynamic.py"),
        "initial-source-hashes.json": initial_hash_file_hash,
        "reference.npz": reference_hashes["reference.npz"],
        "reference.json": reference_hashes["reference.json"],
        **{
            f"dynamic_seed_{seed}/artifact-hashes.json": digest
            for seed, digest in manifest_hashes.items()
        },
    }
    result: dict[str, object] = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "passed": bool(all(checks.values())),
        "description": "Independent streaming audit of all 600 primary archives",
        "independence": (
            "Does not import producer, interface, sampler, or reference Python modules"
        ),
        "command": [sys.executable, *sys.argv],
        "duration_seconds": time.perf_counter() - started,
        "checks": checks,
        "failures": failures,
        "counts": counts,
        "maximum_absolute_differences": differences,
        "minimum_projection_variational_inequality": global_min_vi,
        "independent_gram": gram_record,
        "reference": {
            "passed": reference_json.get("passed"),
            "convergence_max": reference_json.get("convergence_max"),
            "convergence_per_time": reference_json.get("convergence_per_time"),
            "finest_solve_seconds": reference_json.get("performance_costs", {}).get(
                "finest_reference_solve_seconds"
            ),
            "total_validation_seconds": reference_json.get("performance_costs", {}).get(
                "total_reference_setup_and_six_validation_solves_seconds"
            ),
            "numeric_proxy_discrepancy_at_t0_for_exact_0.9g": t0_proxy_discrepancy,
        },
        "source_and_data_hashes_sha256": source_hashes,
        "seeds": seed_outputs,
        "regeneration_command": (
            "/opt/miniconda3/envs/parabolab/bin/python "
            "docs/research/runs/2026-09-28-dynamic-continuation/numerics/"
            "audit_dynamic.py"
        ),
    }
    write_json(output, result)
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "audit_dynamic.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = audit(args.output.resolve())
    print(
        json.dumps(
            {
                "passed": result["passed"],
                "duration_seconds": result["duration_seconds"],
                "counts": result["counts"],
                "maximum_absolute_differences": result["maximum_absolute_differences"],
                "failures": result["failures"],
                "output": str(args.output.resolve()),
            },
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
    )
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
