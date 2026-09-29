"""Independent audit of every saved slab-continuation root artifact.

This script deliberately does not import the production driver or sampler.
It reads each manifest-referenced NPZ, checks provenance and complete-root
accounting, then independently rebuilds the three Fourier observations,
coordinate projection, covariances, and reported errors from X and H.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import shlex
import sys
import time

import numpy as np
from scipy import special


HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO = HERE.parents[4]
ARTIFACTS = HERE / "artifacts"
OUTPUT = HERE / "audit.json"
INITIAL_HASHES = RUN_DIR / "initial-source-hashes.json"

M = 0.05
A = math.sqrt(2.0 / 21.0)
KAPPA = math.sqrt(40.0 / 21.0)
MODES = np.array((1, 3, 5), dtype=np.int64)
CAPS = np.array((0.23, 0.003, 0.00005), dtype=float)
CODE_ORDER = ("Id", "Dx", "F0", "F1", "F2", "F3")
FLOAT_ATOL = 2.0e-14
FLOAT_RTOL = 2.0e-13

EXPECTED = {
    "slab": {
        "seeds": (2026092701, 2026092702, 2026092703),
        "rows": 50,
        "roots": 200_000,
        "kind": "stages",
    },
    "majority": {
        "seeds": (2026092711, 2026092712, 2026092713),
        "rows": 2,
        "roots": 8_000,
        "kind": "horizons",
    },
    "sensitivity": {
        "seeds": (2026092799,),
        "rows": 50,
        "roots": 50_000,
        "kind": "stages",
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class Audit:
    def __init__(self) -> None:
        self.checks = 0
        self.passed = 0
        self.failures: list[dict] = []
        self.max_numeric_deviation = 0.0
        self.max_numeric_deviation_check = None

    def check(self, name: str, condition: bool, **details) -> None:
        self.checks += 1
        if bool(condition):
            self.passed += 1
            return
        failure = {"check": name}
        failure.update(details)
        self.failures.append(failure)

    def numeric(self, name: str, actual, expected) -> None:
        actual_array = np.asarray(actual, dtype=float)
        expected_array = np.asarray(expected, dtype=float)
        same_shape = actual_array.shape == expected_array.shape
        if same_shape and actual_array.size:
            deviation = float(np.max(np.abs(actual_array - expected_array)))
        elif same_shape:
            deviation = 0.0
        else:
            deviation = None
        if deviation is not None and math.isfinite(deviation) and deviation > self.max_numeric_deviation:
            self.max_numeric_deviation = deviation
            self.max_numeric_deviation_check = name
        close = same_shape and bool(
            np.allclose(
                actual_array,
                expected_array,
                atol=FLOAT_ATOL,
                rtol=FLOAT_RTOL,
                equal_nan=False,
            )
        )
        self.check(
            name,
            close,
            actual=np.asarray(actual).tolist(),
            expected=np.asarray(expected).tolist(),
            absolute_deviation=deviation,
        )


def independent_reference() -> dict:
    complete_k = float(special.ellipk(M))
    complementary_k = float(special.ellipk(1.0 - M))
    period = 4.0 * complete_k / KAPPA
    omega = 2.0 * math.pi / period
    nome = math.exp(-math.pi * complementary_k / complete_k)
    scale = 2.0 * math.pi / (complete_k * math.sqrt(21.0 / 20.0))

    def coefficient(r: int) -> float:
        return scale * nome ** (r + 0.5) / (1.0 - nome ** (2 * r + 1))

    coefficients = np.array([coefficient(r) for r in range(3)])
    tail_squared = 0.0
    r = 3
    while True:
        term = coefficient(r) ** 2
        tail_squared += term
        if term < 1.0e-40:
            break
        r += 1
    return {
        "period": period,
        "omega": omega,
        "coefficients": coefficients,
        "tail_squared": tail_squared,
    }


def basis(points: np.ndarray, omega: float) -> np.ndarray:
    return math.sqrt(2.0) * np.sin(points[:, None] * omega * MODES)


def exact_grid(reference: dict, count: int) -> tuple[np.ndarray, np.ndarray]:
    points = np.arange(count, dtype=float) * reference["period"] / count
    sn, _, _, _ = special.ellipj(KAPPA * points, M)
    return A * sn, basis(points, reference["omega"])


def finite_json_numbers(value) -> bool:
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return True
    if isinstance(value, (int, float)):
        return math.isfinite(float(value))
    if isinstance(value, list):
        return all(finite_json_numbers(item) for item in value)
    if isinstance(value, dict):
        return all(finite_json_numbers(item) for item in value.values())
    return False


def audit_sources(audit: Audit, manifests: dict[str, dict]) -> dict:
    captured: dict[str, str] = {}
    for mode, manifest in manifests.items():
        source_hashes = manifest["provenance"].get("source_sha256", {})
        audit.check(f"{mode}: captured source hash set is nonempty", bool(source_hashes))
        for relative, expected_hash in source_hashes.items():
            path = REPO / relative
            audit.check(f"{mode}: source exists: {relative}", path.is_file())
            if path.is_file():
                actual_hash = sha256(path)
                audit.check(
                    f"{mode}: source hash: {relative}",
                    actual_hash == expected_hash,
                    actual=actual_hash,
                    expected=expected_hash,
                )
                previous = captured.setdefault(relative, expected_hash)
                audit.check(
                    f"{mode}: source capture agrees across manifests: {relative}",
                    previous == expected_hash,
                    first=previous,
                    current=expected_hash,
                )

    initial = json.loads(INITIAL_HASHES.read_text(encoding="utf-8"))
    audit.check("initial source list has 85 paths", len(initial) == 85, actual=len(initial))
    unchanged = 0
    missing = 0
    for relative, expected_hash in initial.items():
        path = REPO / relative
        if not path.is_file():
            missing += 1
            audit.check(f"initial source exists: {relative}", False)
            continue
        actual_hash = sha256(path)
        matches = actual_hash == expected_hash
        unchanged += int(matches)
        audit.check(
            f"initial source unchanged: {relative}",
            matches,
            actual=actual_hash,
            expected=expected_hash,
        )
    return {
        "captured_production_sources": captured,
        "initial_source_paths_expected": 85,
        "initial_source_paths_listed": len(initial),
        "initial_source_paths_unchanged": unchanged,
        "initial_source_paths_missing": missing,
    }


def audit_archive(
    audit: Audit,
    mode: str,
    manifest_row: dict,
    archive_dir: Path,
    expected_roots: int,
    reference: dict,
    cached_grids: dict[int, tuple[np.ndarray, np.ndarray]],
) -> tuple[dict, int]:
    archive = manifest_row["raw_archive"]
    path = archive_dir / archive["path"]
    prefix = f"{mode}:{archive['path']}"
    audit.check(f"{prefix}: file exists", path.is_file())
    if not path.is_file():
        return {}, 0
    disk_bytes = path.stat().st_size
    actual_hash = sha256(path)
    audit.check(
        f"{prefix}: sha256",
        actual_hash == archive["sha256"],
        actual=actual_hash,
        expected=archive["sha256"],
    )

    with np.load(path, allow_pickle=False) as raw:
        expected_keys = {
            "X",
            "H",
            "node_counts",
            "root_branched",
            "terminal_counts",
            "terminal_code_order",
            "scheduled_roots",
            "complete",
        }
        audit.check(
            f"{prefix}: exact NPZ fields", set(raw.files) == expected_keys,
            actual=sorted(raw.files), expected=sorted(expected_keys),
        )
        x = np.asarray(raw["X"])
        h_values = np.asarray(raw["H"])
        node_counts = np.asarray(raw["node_counts"])
        root_branched = np.asarray(raw["root_branched"])
        terminal_counts = np.asarray(raw["terminal_counts"])
        terminal_order = tuple(np.asarray(raw["terminal_code_order"]).tolist())
        scheduled_roots = int(np.asarray(raw["scheduled_roots"]).item())
        complete = bool(np.asarray(raw["complete"]).item())

    for name, array in (
        ("X", x),
        ("H", h_values),
        ("node_counts", node_counts),
        ("root_branched", root_branched),
    ):
        audit.check(
            f"{prefix}: {name} has every root",
            array.shape == (expected_roots,),
            actual=array.shape,
            expected=(expected_roots,),
        )
    audit.check(f"{prefix}: X floating dtype", np.issubdtype(x.dtype, np.floating))
    audit.check(f"{prefix}: H floating dtype", np.issubdtype(h_values.dtype, np.floating))
    audit.check(
        f"{prefix}: node_counts integer dtype", np.issubdtype(node_counts.dtype, np.integer)
    )
    audit.check(f"{prefix}: root_branched bool dtype", root_branched.dtype == np.bool_)
    audit.check(
        f"{prefix}: terminal_counts shape and integer dtype",
        terminal_counts.shape == (6,) and np.issubdtype(terminal_counts.dtype, np.integer),
    )
    audit.check(f"{prefix}: terminal code order", terminal_order == CODE_ORDER)
    audit.check(f"{prefix}: finite X", bool(np.all(np.isfinite(x))))
    audit.check(f"{prefix}: finite H", bool(np.all(np.isfinite(h_values))))
    audit.check(
        f"{prefix}: positions in one period",
        bool(np.all((x >= 0.0) & (x < reference["period"]))),
    )
    audit.check(f"{prefix}: every root has a node", bool(np.all(node_counts >= 1)))
    audit.check(f"{prefix}: terminal counts nonnegative", bool(np.all(terminal_counts >= 0)))
    audit.check(f"{prefix}: archive complete", complete)
    audit.check(
        f"{prefix}: scheduled root scalar", scheduled_roots == expected_roots,
        actual=scheduled_roots, expected=expected_roots,
    )
    audit.check(f"{prefix}: manifest archive complete", archive["complete"] is True)
    audit.check(
        f"{prefix}: manifest completed roots",
        archive["completed_roots"] == expected_roots,
        actual=archive["completed_roots"], expected=expected_roots,
    )
    audit.check(
        f"{prefix}: manifest scheduled roots",
        archive["scheduled_roots"] == expected_roots,
        actual=archive["scheduled_roots"], expected=expected_roots,
    )

    if x.shape != (expected_roots,) or h_values.shape != (expected_roots,):
        return {"path": archive["path"], "sha256": actual_hash}, disk_bytes

    observations = h_values[:, None] * basis(x, reference["omega"])
    raw_coefficients = observations.mean(axis=0)
    projected = np.clip(raw_coefficients, -CAPS, CAPS)
    projection_mask = projected != raw_coefficients
    projection_difference = raw_coefficients - projected
    observation_covariance = np.cov(observations, rowvar=False, ddof=1)
    coefficient_covariance = observation_covariance / expected_roots

    exact_error = math.sqrt(
        float(np.sum((projected - reference["coefficients"]) ** 2))
        + reference["tail_squared"]
    )
    raw_exact_error = math.sqrt(
        float(np.sum((raw_coefficients - reference["coefficients"]) ** 2))
        + reference["tail_squared"]
    )
    grid_count = int(manifest_row["error"]["grid_points"])
    if grid_count not in cached_grids:
        cached_grids[grid_count] = exact_grid(reference, grid_count)
    exact_values, grid_basis = cached_grids[grid_count]
    projected_values = grid_basis @ projected
    grid_error = math.sqrt(float(np.mean((projected_values - exact_values) ** 2)))

    value_bound = math.sqrt(2.0) * float(np.abs(projected).sum())
    derivative_bound = (
        math.sqrt(2.0)
        * reference["omega"]
        * float((MODES * np.abs(projected)).sum())
    )

    audit.numeric(f"{prefix}: raw coefficients", raw_coefficients, manifest_row["raw_coefficients"])
    audit.numeric(f"{prefix}: projected coefficients", projected, manifest_row["projected_coefficients"])
    audit.check(
        f"{prefix}: projection mask",
        projection_mask.tolist() == manifest_row["projection_mask"],
        actual=projection_mask.tolist(), expected=manifest_row["projection_mask"],
    )
    audit.numeric(
        f"{prefix}: projection difference",
        projection_difference,
        manifest_row["projection_difference_raw_minus_projected"],
    )
    audit.numeric(
        f"{prefix}: projection distortion",
        np.linalg.norm(projection_difference),
        manifest_row["projection_distortion_l2"],
    )
    audit.numeric(
        f"{prefix}: observation covariance",
        observation_covariance,
        manifest_row["coefficient_observation_covariance"],
    )
    audit.numeric(
        f"{prefix}: coefficient covariance",
        coefficient_covariance,
        manifest_row["coefficient_estimator_covariance"],
    )
    audit.numeric(
        f"{prefix}: tree mean", h_values.mean(), manifest_row["moments"]["tree_value_mean"]
    )
    audit.numeric(
        f"{prefix}: tree second moment",
        np.mean(h_values**2),
        manifest_row["moments"]["tree_value_second_moment"],
    )
    audit.numeric(
        f"{prefix}: tree sample variance",
        h_values.var(ddof=1),
        manifest_row["moments"]["tree_value_sample_variance"],
    )
    audit.numeric(
        f"{prefix}: observation second moments",
        np.mean(observations**2, axis=0),
        manifest_row["moments"]["coefficient_observation_second_moments"],
    )
    audit.numeric(
        f"{prefix}: exact Fourier error",
        exact_error,
        manifest_row["error"]["normalized_l2_exact_fourier_plus_tail"],
    )
    audit.numeric(
        f"{prefix}: raw exact Fourier error",
        raw_exact_error,
        manifest_row["error"]["normalized_l2_raw_coefficients_exact_fourier_plus_tail"],
    )
    audit.numeric(
        f"{prefix}: grid error",
        grid_error,
        manifest_row["error"]["normalized_l2_periodic_grid_crosscheck"],
    )
    audit.numeric(
        f"{prefix}: grid minus exact error",
        grid_error - exact_error,
        manifest_row["error"]["grid_crosscheck_minus_exact_fourier"],
    )
    audit.numeric(
        f"{prefix}: exact tail squared",
        reference["tail_squared"],
        manifest_row["error"]["exact_tail_squared"],
    )
    audit.numeric(
        f"{prefix}: interface value bound",
        value_bound,
        manifest_row["interface_bounds"]["analytic_sup_value_bound"],
    )
    audit.numeric(
        f"{prefix}: interface derivative bound",
        derivative_bound,
        manifest_row["interface_bounds"]["analytic_sup_derivative_bound"],
    )
    audit.check(
        f"{prefix}: interface value admissibility",
        (value_bound < 0.4) == manifest_row["interface_bounds"]["value_admissible_lt_0p4"],
    )
    audit.check(
        f"{prefix}: interface derivative admissibility",
        (derivative_bound < 0.5)
        == manifest_row["interface_bounds"]["derivative_admissible_lt_0p5"],
    )
    audit.check(f"{prefix}: reported root count", manifest_row["root_count"] == expected_roots)
    audit.check(
        f"{prefix}: total nodes",
        manifest_row["total_nodes"] == int(node_counts.sum()),
    )
    audit.check(
        f"{prefix}: max nodes", manifest_row["max_nodes"] == int(node_counts.max())
    )
    audit.numeric(
        f"{prefix}: mean nodes", node_counts.mean(), manifest_row["mean_nodes"]
    )
    audit.check(
        f"{prefix}: root branch count",
        manifest_row["root_branch_count"] == int(root_branched.sum()),
    )
    audit.numeric(
        f"{prefix}: root branch fraction",
        root_branched.mean(),
        manifest_row["root_branch_fraction"],
    )
    audit.check(
        f"{prefix}: terminal counts",
        terminal_counts.tolist() == manifest_row["terminal_code_counts"],
        actual=terminal_counts.tolist(), expected=manifest_row["terminal_code_counts"],
    )
    audit.check(f"{prefix}: JSON terminal order", tuple(manifest_row["terminal_code_order"]) == CODE_ORDER)
    audit.numeric(
        f"{prefix}: max absolute tree value",
        np.max(np.abs(h_values)),
        manifest_row["max_absolute_tree_value"],
    )
    audit.check(f"{prefix}: stage marked complete", manifest_row["complete"] is True)
    audit.check(
        f"{prefix}: raw-estimator declaration retained",
        manifest_row["local_tree_estimator_is_unbiased_conditional_on_frozen_interface"] is True,
    )
    audit.check(
        f"{prefix}: biased-projection declaration retained",
        manifest_row["projection_is_biased_interface_step"] is True,
    )

    if mode == "majority":
        total_nodes = int(node_counts.sum())
        leaves = int(terminal_counts[0])
        audit.check(
            f"{prefix}: majority only has Id leaves",
            bool(np.all(terminal_counts[1:] == 0)),
        )
        audit.check(
            f"{prefix}: every majority tree is full ternary",
            bool(np.all((node_counts - 1) % 3 == 0)),
        )
        audit.check(
            f"{prefix}: majority aggregate leaf identity",
            3 * leaves == 2 * total_nodes + expected_roots,
            leaves=leaves,
            total_nodes=total_nodes,
        )
    else:
        audit.check(
            f"{prefix}: raw terminal leaves do not exceed nodes",
            int(terminal_counts.sum()) <= int(node_counts.sum()),
        )

    return {
        "path": archive["path"],
        "sha256": actual_hash,
        "roots": expected_roots,
        "nodes": int(node_counts.sum()),
        "terminal_calls": int(terminal_counts.sum()),
        "disk_bytes": disk_bytes,
    }, disk_bytes


def audit_mode(
    audit: Audit,
    mode: str,
    manifest: dict,
    reference: dict,
    cached_grids: dict[int, tuple[np.ndarray, np.ndarray]],
) -> dict:
    expected = EXPECTED[mode]
    prefix = mode
    audit.check(f"{prefix}: schema version", manifest.get("schema_version") == 1)
    audit.check(f"{prefix}: status complete", manifest.get("status") == "complete")
    audit.check(f"{prefix}: finite JSON numbers", finite_json_numbers(manifest))
    runs = manifest.get("runs", [])
    audit.check(f"{prefix}: run count", len(runs) == len(expected["seeds"]))
    audit.check(
        f"{prefix}: seed order",
        tuple(run.get("seed") for run in runs) == expected["seeds"],
        actual=[run.get("seed") for run in runs], expected=list(expected["seeds"]),
    )
    audit.check(
        f"{prefix}: provenance seed schedule",
        tuple(manifest["provenance"]["seed_schedule"]) == expected["seeds"],
    )
    config = manifest["provenance"]["configuration"]
    audit.check(f"{prefix}: configured roots", int(config["n"]) == expected["roots"])
    audit.check(
        f"{prefix}: configured seeds", tuple(config["seeds"]) == expected["seeds"]
    )
    contract = manifest["provenance"]["algorithm_contract"]
    audit.check(f"{prefix}: no adaptive sample budget", contract["adaptive_sample_budget"] is False)
    audit.check(f"{prefix}: no failed-root deletion", contract["failed_root_deletion"] is False)
    audit.check(f"{prefix}: no tree cutoff", contract["tree_cutoff"] is None)
    audit.check(f"{prefix}: no tree-weight clipping", contract["tree_weight_clipping"] is False)

    archive_records = []
    disk_bytes = 0
    referenced_paths = []
    for run in runs:
        rows = run[expected["kind"]]
        audit.check(
            f"{prefix}: seed {run['seed']} status complete", run["status"] == "complete"
        )
        audit.check(
            f"{prefix}: seed {run['seed']} row count", len(rows) == expected["rows"]
        )
        count_key = "completed_stages" if expected["kind"] == "stages" else "completed_horizons"
        audit.check(
            f"{prefix}: seed {run['seed']} completed count",
            run[count_key] == expected["rows"],
        )
        if expected["kind"] == "stages":
            audit.check(
                f"{prefix}: seed {run['seed']} scheduled stages",
                run["scheduled_stages"] == expected["rows"],
            )
            audit.check(
                f"{prefix}: seed {run['seed']} roots per stage",
                run["n_roots_per_stage"] == expected["roots"],
            )
        else:
            audit.check(
                f"{prefix}: seed {run['seed']} roots per horizon",
                run["n_roots_per_horizon"] == expected["roots"],
            )
            audit.check(
                f"{prefix}: seed {run['seed']} horizon schedule",
                tuple(run["scheduled_horizons"]) == (0.8, 2.0),
            )

        summed_roots = 0
        summed_nodes = 0
        summed_branches = 0
        summed_terminal = np.zeros(6, dtype=np.int64)
        for row_index, row in enumerate(rows, start=1):
            if expected["kind"] == "stages":
                audit.check(
                    f"{prefix}: seed {run['seed']} stage numbering {row_index}",
                    row["stage"] == row_index,
                )
                expected_source = (
                    "exact_jacobi" if row_index == 1
                    else "frozen_previous_projected_coefficients"
                )
                audit.check(
                    f"{prefix}: seed {run['seed']} stage {row_index} terminal source",
                    row["terminal_source"] == expected_source,
                    actual=row["terminal_source"], expected=expected_source,
                )
                audit.numeric(
                    f"{prefix}: seed {run['seed']} stage {row_index} elapsed time",
                    row["elapsed_time"],
                    0.08 * row_index,
                )
            else:
                audit.check(
                    f"{prefix}: seed {run['seed']} horizon {row_index} value",
                    row["horizon"] == (0.8, 2.0)[row_index - 1],
                )
                audit.check(
                    f"{prefix}: seed {run['seed']} horizon terminal source",
                    row["terminal_source"] == "exact_jacobi_full_horizon_comparator",
                )

            record, archive_bytes = audit_archive(
                audit,
                mode,
                row,
                ARTIFACTS / mode,
                expected["roots"],
                reference,
                cached_grids,
            )
            archive_records.append(record)
            disk_bytes += archive_bytes
            referenced_paths.append(row["raw_archive"]["path"])
            summed_roots += int(row["root_count"])
            summed_nodes += int(row["total_nodes"])
            summed_branches += int(row["root_branch_count"])
            summed_terminal += np.asarray(row["terminal_code_counts"], dtype=np.int64)

        measured = run["measured_work"]
        audit.check(
            f"{prefix}: seed {run['seed']} measured roots", measured["roots_completed"] == summed_roots
        )
        audit.check(
            f"{prefix}: seed {run['seed']} measured nodes", measured["total_nodes"] == summed_nodes
        )
        audit.check(
            f"{prefix}: seed {run['seed']} measured root branches",
            measured["root_branches"] == summed_branches,
        )
        audit.check(
            f"{prefix}: seed {run['seed']} measured terminal counts",
            measured["terminal_code_counts"] == summed_terminal.tolist(),
        )
        audit.check(
            f"{prefix}: seed {run['seed']} measured terminal calls",
            measured["terminal_calls"] == int(summed_terminal.sum()),
        )
        audit.check(
            f"{prefix}: seed {run['seed']} all scheduled roots retained",
            summed_roots == expected["rows"] * expected["roots"],
        )

    actual_npz = {path.name for path in (ARTIFACTS / mode).glob("*.npz")}
    audit.check(
        f"{prefix}: no unreferenced or missing NPZ files",
        actual_npz == set(referenced_paths),
        unreferenced=sorted(actual_npz - set(referenced_paths)),
        missing=sorted(set(referenced_paths) - actual_npz),
    )
    return {
        "expected_seeds": list(expected["seeds"]),
        "audited_seeds": [run["seed"] for run in runs],
        "expected_archives": len(expected["seeds"]) * expected["rows"],
        "audited_archives": len(archive_records),
        "expected_roots_per_archive": expected["roots"],
        "audited_root_records": len(archive_records) * expected["roots"],
        "npz_disk_bytes": disk_bytes,
    }


def main() -> int:
    started = time.perf_counter()
    command = shlex.join([sys.executable, *sys.argv])
    audit = Audit()
    manifests = {}
    manifest_bytes = 0
    for mode in EXPECTED:
        path = ARTIFACTS / mode / "results.json"
        audit.check(f"{mode}: results manifest exists", path.is_file())
        if path.is_file():
            manifests[mode] = json.loads(path.read_text(encoding="utf-8"))
            manifest_bytes += path.stat().st_size

    reference = independent_reference()
    cached_grids = {}
    mode_records = {}
    for mode in EXPECTED:
        if mode in manifests:
            mode_records[mode] = audit_mode(
                audit, mode, manifests[mode], reference, cached_grids
            )
    source_record = audit_sources(audit, manifests)

    archive_count = sum(record["audited_archives"] for record in mode_records.values())
    expected_archive_count = sum(
        len(config["seeds"]) * config["rows"] for config in EXPECTED.values()
    )
    total_roots = sum(record["audited_root_records"] for record in mode_records.values())
    npz_disk_bytes = sum(record["npz_disk_bytes"] for record in mode_records.values())
    audit.check(
        "all 206 scheduled NPZ archives audited",
        archive_count == expected_archive_count == 206,
        actual=archive_count,
        expected=expected_archive_count,
    )
    audit.check(
        "all 32,548,000 scheduled root records audited",
        total_roots == 32_548_000,
        actual=total_roots,
        expected=32_548_000,
    )

    duration = time.perf_counter() - started
    record = {
        "schema_version": 1,
        "status": "passed" if not audit.failures else "failed",
        "scope": {
            "modes": list(EXPECTED),
            "population_moment_claim": False,
            "note": (
                "Saved sample moments and covariances are reproducibility diagnostics; "
                "this audit does not prove population moments or confidence guarantees."
            ),
        },
        "execution": {
            "command": command,
            "python_executable": sys.executable,
            "duration_seconds": duration,
        },
        "summary": {
            "checks": audit.checks,
            "passed_checks": audit.passed,
            "failed_checks": len(audit.failures),
            "expected_archives": expected_archive_count,
            "audited_archives": archive_count,
            "audited_root_records": total_roots,
            "npz_disk_bytes": npz_disk_bytes,
            "manifest_disk_bytes": manifest_bytes,
            "audited_artifact_disk_bytes": npz_disk_bytes + manifest_bytes,
            "max_numeric_absolute_deviation": audit.max_numeric_deviation,
            "max_numeric_deviation_check": audit.max_numeric_deviation_check,
            "all_scheduled_roots_present": total_roots == 32_548_000,
            "saved_root_deletion_detected": total_roots != 32_548_000,
        },
        "modes": mode_records,
        "source_integrity": source_record,
        "failures": audit.failures,
    }
    OUTPUT.write_text(
        json.dumps(record, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": record["status"],
                **record["summary"],
                "audit_json": str(OUTPUT),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if not audit.failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
