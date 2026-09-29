"""Run the prespecified two-coefficient dynamic continuation experiment."""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time
from typing import Callable, Sequence

import numpy as np
import scipy

try:
    import dynamic_interface as interface
except ImportError:  # pragma: no cover - supports package-style imports in tests
    from . import dynamic_interface as interface


HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO = HERE.parents[4]
OLD_SAMPLER = (
    HERE.parents[1]
    / "2026-09-27-slab-continuation"
    / "numerics"
    / "slab_sampler.py"
)
REFERENCE_NPZ = RUN_DIR / "artifacts" / "reference" / "reference.npz"
REFERENCE_JSON = RUN_DIR / "artifacts" / "reference" / "reference.json"
ARTIFACT_ROOT = RUN_DIR / "artifacts"

EXPECTED_SAMPLER_SHA256 = (
    "994e892784f36930fa63649aa749985448df75887f9096f6c40c142b46ff108a"
)
PRIMARY_SEEDS = (2026092801, 2026092802, 2026092803)
PRIMARY_N = 100_000
PRIMARY_STAGES = 200
SLAB_H = 0.08
PRIMARY_TOTAL_ROOTS = 60_000_000
MAX_SECONDS = 2.0 * 60.0 * 60.0
BATCH_SIZE = 10_000
GRID_POINTS = 16_384
INITIAL_COEFFICIENTS = np.array((0.9, 0.9), dtype=float)
TERMINAL_CODE_ORDER = ("Id", "Dx", "F0", "F1", "F2", "F3")
ERROR_NAMES = ("mc", "g", "0.95g", "0.9g")


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


def _load_raw_sampler(path: Path = OLD_SAMPLER):
    actual_hash = _sha256(path)
    if actual_hash != EXPECTED_SAMPLER_SHA256:
        raise RuntimeError(
            f"old sampler SHA-256 mismatch: expected {EXPECTED_SAMPLER_SHA256}, "
            f"got {actual_hash}"
        )
    module_name = "dynamic_continuation_frozen_slab_sampler"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load sampler from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module.raw_sample


def validate_reference(
    npz_path: Path = REFERENCE_NPZ,
    json_path: Path = REFERENCE_JSON,
) -> dict:
    """Validate the independent artifact without exposing it to a terminal."""
    record = json.loads(json_path.read_text(encoding="utf-8"))
    if record.get("passed") is not True or record.get("acceptance") is not True:
        raise RuntimeError("independent reference did not pass its acceptance gate")
    convergence_max = float(record["convergence_max"])
    convergence_per_time = np.asarray(record["convergence_per_time"], dtype=float)
    if (
        not math.isfinite(convergence_max)
        or convergence_max > 1.0e-9
        or convergence_per_time.shape != (PRIMARY_STAGES + 1,)
        or not np.all(np.isfinite(convergence_per_time))
    ):
        raise RuntimeError("independent reference convergence record is invalid")
    with np.load(npz_path, allow_pickle=False) as data:
        expected = {
            "times": (PRIMARY_STAGES + 1,),
            "period": (),
            "omega": (),
            "odd_modes": (32,),
            "coefficients": (PRIMARY_STAGES + 1, 32),
        }
        if set(data.files) != set(expected):
            raise RuntimeError(f"unexpected reference fields: {data.files}")
        for name, shape in expected.items():
            if data[name].shape != shape:
                raise RuntimeError(f"reference {name} has shape {data[name].shape}")
        times = np.asarray(data["times"], dtype=float)
        odd_modes = np.asarray(data["odd_modes"], dtype=np.int64)
        coefficients = np.asarray(data["coefficients"], dtype=float)
        period = float(data["period"])
        omega = float(data["omega"])
        if not np.array_equal(times, np.arange(PRIMARY_STAGES + 1) * SLAB_H):
            raise RuntimeError("reference times do not equal arange(201) * 0.08")
        if not np.array_equal(odd_modes, np.arange(1, 64, 2)):
            raise RuntimeError("reference modes are not the positive odd modes 1,...,63")
        if not np.all(np.isfinite(coefficients)):
            raise RuntimeError("reference coefficients are nonfinite")
        if not math.isclose(period, interface.PERIOD, rel_tol=0.0, abs_tol=2.0e-14):
            raise RuntimeError("reference period disagrees with the producer datum")
        if not math.isclose(
            omega, 2.0 * math.pi / interface.PERIOD, rel_tol=0.0, abs_tol=2.0e-14
        ):
            raise RuntimeError("reference omega disagrees with the producer datum")
    npz_hash = _sha256(npz_path)
    expected_npz_hash = record.get("artifact_hashes_sha256", {}).get("reference.npz")
    if expected_npz_hash != npz_hash:
        raise RuntimeError("reference NPZ hash disagrees with its companion JSON")
    return {
        "npz_path": str(npz_path.resolve()),
        "json_path": str(json_path.resolve()),
        "npz_sha256": npz_hash,
        "json_sha256": _sha256(json_path),
        "convergence_max": convergence_max,
        "convergence_per_time": convergence_per_time.tolist(),
        "grid_points": GRID_POINTS,
    }


def _validate_sample_result(result, count: int) -> None:
    arrays = {
        "values": np.asarray(result.values),
        "node_counts": np.asarray(result.node_counts),
        "root_branched": np.asarray(result.root_branched),
    }
    if any(value.shape != (count,) for value in arrays.values()):
        raise RuntimeError("sampler returned misaligned per-root arrays")
    terminal_counts = np.asarray(result.terminal_counts)
    if terminal_counts.shape != (6,):
        raise RuntimeError("sampler terminal_counts must have shape (6,)")
    if not np.all(np.isfinite(arrays["values"])):
        raise FloatingPointError("a complete raw tree returned a nonfinite value")
    if np.any(arrays["node_counts"] < 1) or np.any(terminal_counts < 0):
        raise RuntimeError("sampler returned invalid work counts")


def collect_samples(
    positions: np.ndarray,
    terminal: Callable,
    rng: np.random.Generator,
    sampler: Callable,
    batch_size: int,
    deadline: float | None,
) -> CollectedSamples:
    """Complete fixed batches and check a time cap only between batches."""
    positions = np.asarray(positions, dtype=float)
    if positions.ndim != 1 or positions.size < 2 or not np.all(np.isfinite(positions)):
        raise ValueError("positions must be a one-dimensional finite root array")
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    values = np.empty(positions.size, dtype=float)
    node_counts = np.empty(positions.size, dtype=np.int64)
    root_branched = np.empty(positions.size, dtype=bool)
    terminal_counts = np.zeros(6, dtype=np.int64)
    completed = 0
    started = time.perf_counter()
    while completed < positions.size:
        if deadline is not None and completed and time.perf_counter() >= deadline:
            break
        stop = min(completed + batch_size, positions.size)
        result = sampler(
            positions[completed:stop],
            SLAB_H,
            terminal,
            rng,
            root_code=0,
        )
        _validate_sample_result(result, stop - completed)
        values[completed:stop] = result.values
        node_counts[completed:stop] = result.node_counts
        root_branched[completed:stop] = result.root_branched
        terminal_counts += np.asarray(result.terminal_counts, dtype=np.int64)
        completed = stop
    return CollectedSamples(
        positions=positions[:completed].copy(),
        values=values[:completed].copy(),
        node_counts=node_counts[:completed].copy(),
        root_branched=root_branched[:completed].copy(),
        terminal_counts=terminal_counts,
        scheduled_roots=int(positions.size),
        complete=completed == positions.size,
        seconds=time.perf_counter() - started,
    )


def _poststage_errors(
    stage: int,
    projected_coefficients: np.ndarray,
    reference_npz: Path,
    expected_reference_hash: str,
    grid_points: int,
) -> dict:
    """Load the true trajectory only after sampling and return scalar errors."""
    if _sha256(reference_npz) != expected_reference_hash:
        raise RuntimeError("reference artifact changed during the producer run")
    with np.load(reference_npz, allow_pickle=False) as data:
        if float(data["times"][stage]) != stage * SLAB_H:
            raise RuntimeError("reference time does not match the completed stage")
        period = float(data["period"])
        omega = float(data["omega"])
        modes = np.asarray(data["odd_modes"], dtype=float)
        coefficients = np.asarray(data["coefficients"][stage], dtype=float)
    grid = np.arange(grid_points, dtype=float) * period / grid_points
    reference_values = (
        math.sqrt(2.0) * np.sin(grid[:, None] * omega * modes) @ coefficients
    )
    g = np.asarray(interface.g_and_derivative(grid)[0], dtype=float)
    mc = np.asarray(interface.interface_terminal(projected_coefficients)(grid)[0])
    values = (mc, g, 0.95 * g, 0.9 * g)
    errors = {
        name: float(np.sqrt(np.mean((value - reference_values) ** 2)))
        for name, value in zip(ERROR_NAMES, values)
    }
    return {"normalized_spatial_rms": errors, "grid_points": grid_points}


def _complete_stage_statistics(samples: CollectedSamples) -> tuple[np.ndarray, dict]:
    if not samples.complete:
        raise ValueError("partial stages cannot form coefficient estimates")
    observations = samples.values[:, None] * interface.basis_values(samples.positions)
    bhat = observations.mean(axis=0)
    raw_coefficients = np.linalg.solve(interface.GRAM, bhat)
    projected, projection = interface.project_gram(raw_coefficients)
    covariance = np.cov(observations, rowvar=False, ddof=1)
    stats = {
        "bhat": bhat.tolist(),
        "raw_coefficients": raw_coefficients.tolist(),
        "projected_coefficients": projected.tolist(),
        "projection": projection,
        "coefficient_observation_covariance": covariance.tolist(),
        "coefficient_estimator_covariance": (
            covariance / samples.values.size
        ).tolist(),
        "coefficient_observation_second_moments": np.mean(
            observations**2, axis=0
        ).tolist(),
        "tree_value_mean": float(np.mean(samples.values)),
        "tree_value_second_moment": float(np.mean(samples.values**2)),
        "tree_value_sample_variance": float(np.var(samples.values, ddof=1)),
        "max_absolute_tree_value": float(np.max(np.abs(samples.values))),
        "root_count": int(samples.values.size),
        "total_nodes": int(samples.node_counts.sum()),
        "mean_nodes": float(samples.node_counts.mean()),
        "max_nodes": int(samples.node_counts.max()),
        "root_branch_count": int(samples.root_branched.sum()),
        "root_branch_fraction": float(samples.root_branched.mean()),
        "terminal_code_order": list(TERMINAL_CODE_ORDER),
        "terminal_code_counts": samples.terminal_counts.tolist(),
        "sampling_seconds": samples.seconds,
    }
    return projected, stats


def _save_stage_archive(path: Path, arrays: dict[str, object]) -> str:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite stage archive {path}")
    temporary = path.with_suffix(".npz.tmp")
    if temporary.exists():
        raise FileExistsError(f"refusing to overwrite temporary archive {temporary}")
    try:
        with temporary.open("xb") as stream:
            np.savez_compressed(stream, **arrays)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
    return _sha256(path)


def _archive_arrays(
    *,
    stage: int,
    seed: int,
    prior: np.ndarray,
    samples: CollectedSamples,
    rng_before: dict,
    rng_after: dict,
    source_hashes: dict,
    reference_record: dict,
    stats: dict | None,
    errors: dict | None,
    stage_seconds: float,
) -> dict[str, object]:
    raw = np.asarray(stats["raw_coefficients"] if stats else [], dtype=float)
    projected = np.asarray(
        stats["projected_coefficients"] if stats else [], dtype=float
    )
    bhat = np.asarray(stats["bhat"] if stats else [], dtype=float)
    error_values = np.asarray(
        [errors["normalized_spatial_rms"][name] for name in ERROR_NAMES]
        if errors
        else [],
        dtype=float,
    )
    return {
        "X": samples.positions,
        "H": samples.values,
        "node_counts": samples.node_counts,
        "root_branch_flags": samples.root_branched,
        "terminal_counts": samples.terminal_counts,
        "terminal_code_order": np.asarray(TERMINAL_CODE_ORDER),
        "prior_c": prior,
        "bhat": bhat,
        "raw_c": raw,
        "projected_c": projected,
        "gram": interface.GRAM,
        "stage": np.array(stage, dtype=np.int64),
        "time": np.array(stage * SLAB_H),
        "h": np.array(SLAB_H),
        "seed": np.array(seed, dtype=np.int64),
        "scheduled_roots": np.array(samples.scheduled_roots, dtype=np.int64),
        "completed_roots": np.array(samples.values.size, dtype=np.int64),
        "complete": np.array(samples.complete),
        "sampling_seconds": np.array(samples.seconds),
        "stage_seconds": np.array(stage_seconds),
        "rng_bit_generator": np.array("PCG64"),
        "rng_state_before_stage_json": np.array(json.dumps(rng_before, sort_keys=True)),
        "rng_state_after_stage_json": np.array(json.dumps(rng_after, sort_keys=True)),
        "source_hashes_json": np.array(json.dumps(source_hashes, sort_keys=True)),
        "reference_record_json": np.array(
            json.dumps(
                {
                    key: reference_record[key]
                    for key in (
                        "npz_sha256",
                        "json_sha256",
                        "convergence_max",
                        "grid_points",
                    )
                },
                sort_keys=True,
            )
        ),
        "error_names": np.asarray(ERROR_NAMES),
        "normalized_spatial_rms_errors": error_values,
    }


def _prepare_output(output: Path, reference_record: dict) -> dict:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing run directory {output}")
    output.mkdir(parents=True)
    source_dir = output / "source"
    source_dir.mkdir()
    sources = {
        "dynamic_interface.py": HERE / "dynamic_interface.py",
        "run_dynamic.py": HERE / "run_dynamic.py",
        "test_dynamic.py": HERE / "test_dynamic.py",
        "slab_sampler.py": OLD_SAMPLER,
    }
    source_hashes = {name: _sha256(path) for name, path in sources.items()}
    if source_hashes["slab_sampler.py"] != EXPECTED_SAMPLER_SHA256:
        raise RuntimeError("sampler changed before source freeze")
    for name, path in sources.items():
        shutil.copyfile(path, source_dir / name)
        if _sha256(source_dir / name) != source_hashes[name]:
            raise RuntimeError(f"source copy hash mismatch for {name}")
    record = {
        "created_before_sampling_utc": _utc_now(),
        "command": sys.argv,
        "git_revision": _git_revision(),
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "source_hashes_sha256": source_hashes,
        "source_copy_directory": "source",
        "old_sampler_explicit_path": str(OLD_SAMPLER.resolve()),
        "reference": reference_record,
        "frozen_contract": {
            "n_roots_per_stage": PRIMARY_N,
            "stages": PRIMARY_STAGES,
            "slab_h": SLAB_H,
            "batch_size": BATCH_SIZE,
            "max_seconds_per_seed": MAX_SECONDS,
            "grid_points": GRID_POINTS,
            "initial_coefficients": INITIAL_COEFFICIENTS.tolist(),
        },
    }
    _json_write(output / "source-record.json", record)
    return source_hashes


def _checkpoint(
    output: Path,
    seed: int,
    status: str,
    rows: Sequence[dict],
    started: float,
    source_hashes: dict,
    reference_record: dict,
) -> None:
    _json_write(
        output / "progress.json",
        {
            "schema_version": 1,
            "seed": seed,
            "status": status,
            "scheduled_stages": PRIMARY_STAGES,
            "n_roots_per_stage": PRIMARY_N,
            "slab_h": SLAB_H,
            "completed_stages": sum(row["complete"] for row in rows),
            "roots_completed": sum(row["root_count"] for row in rows),
            "total_nodes": sum(row["total_nodes"] for row in rows),
            "elapsed_seconds": time.perf_counter() - started,
            "checkpointed_at_utc": _utc_now(),
            "source_hashes_sha256": source_hashes,
            "reference_npz_sha256": reference_record["npz_sha256"],
            "entries": list(rows),
        },
    )


def _finalize_hashes(output: Path) -> None:
    """Hash every completed run artifact except the manifest containing the hashes."""
    manifest_path = output / "artifact-hashes.json"
    hashes = {
        str(path.relative_to(output)): _sha256(path)
        for path in sorted(output.rglob("*"))
        if path.is_file() and path != manifest_path
    }
    _json_write(
        manifest_path,
        {
            "algorithm": "sha256",
            "manifest_excludes_itself": True,
            "files": hashes,
        },
    )


def run_seed(
    *,
    seed: int,
    output: Path,
    n_roots: int = PRIMARY_N,
    stages: int = PRIMARY_STAGES,
    batch_size: int = BATCH_SIZE,
    max_seconds: float = MAX_SECONDS,
    grid_points: int = GRID_POINTS,
    sampler: Callable | None = None,
    reference_npz: Path = REFERENCE_NPZ,
    reference_json: Path = REFERENCE_JSON,
    enforce_primary: bool = True,
) -> dict:
    """Run one path. Primary CLI calls cannot alter the frozen experiment."""
    if enforce_primary and (
        seed not in PRIMARY_SEEDS
        or n_roots != PRIMARY_N
        or stages != PRIMARY_STAGES
        or batch_size != BATCH_SIZE
        or max_seconds != MAX_SECONDS
        or grid_points != GRID_POINTS
    ):
        raise ValueError("primary execution parameters differ from the frozen contract")
    if n_roots < 2 or stages < 1 or batch_size < 1:
        raise ValueError("invalid run dimensions")
    reference_record = validate_reference(reference_npz, reference_json)
    source_hashes = _prepare_output(output, reference_record)
    if sampler is None:
        sampler = _load_raw_sampler()

    rng = np.random.default_rng(seed)
    previous = INITIAL_COEFFICIENTS.copy()
    rows: list[dict] = []
    started = time.perf_counter()
    deadline = started + max_seconds if math.isfinite(max_seconds) else None
    status = "complete"
    for stage in range(1, stages + 1):
        if deadline is not None and time.perf_counter() >= deadline:
            status = "incomplete_time_cap_before_stage"
            break
        stage_started = time.perf_counter()
        rng_before = copy.deepcopy(rng.bit_generator.state)
        positions = rng.uniform(0.0, interface.PERIOD, size=n_roots)
        terminal = interface.interface_terminal(previous)
        samples = collect_samples(
            positions, terminal, rng, sampler, batch_size, deadline
        )
        rng_after = copy.deepcopy(rng.bit_generator.state)
        archive_path = output / f"stage_{stage:03d}.npz"
        if not samples.complete:
            status = "incomplete_time_cap_during_stage"
            archive_hash = _save_stage_archive(
                archive_path,
                _archive_arrays(
                    stage=stage,
                    seed=seed,
                    prior=previous,
                    samples=samples,
                    rng_before=rng_before,
                    rng_after=rng_after,
                    source_hashes=source_hashes,
                    reference_record=reference_record,
                    stats=None,
                    errors=None,
                    stage_seconds=time.perf_counter() - stage_started,
                ),
            )
            rows.append(
                {
                    "stage": stage,
                    "time": stage * SLAB_H,
                    "complete": False,
                    "root_count": int(samples.values.size),
                    "scheduled_roots": samples.scheduled_roots,
                    "total_nodes": int(samples.node_counts.sum()),
                    "sampling_seconds": samples.seconds,
                    "archive": archive_path.name,
                    "archive_sha256": archive_hash,
                }
            )
            _checkpoint(
                output,
                seed,
                status,
                rows,
                started,
                source_hashes,
                reference_record,
            )
            break

        projected, stats = _complete_stage_statistics(samples)
        errors = _poststage_errors(
            stage,
            projected,
            reference_npz,
            reference_record["npz_sha256"],
            grid_points,
        )
        stage_seconds = time.perf_counter() - stage_started
        archive_hash = _save_stage_archive(
            archive_path,
            _archive_arrays(
                stage=stage,
                seed=seed,
                prior=previous,
                samples=samples,
                rng_before=rng_before,
                rng_after=rng_after,
                source_hashes=source_hashes,
                reference_record=reference_record,
                stats=stats,
                errors=errors,
                stage_seconds=stage_seconds,
            ),
        )
        row = {
            "stage": stage,
            "time": stage * SLAB_H,
            "terminal_source": "fixed_known_g_with_preceding_stored_coefficients",
            "prior_coefficients": previous.tolist(),
            "complete": True,
            **stats,
            "errors": errors,
            "reference_convergence_floor": reference_record[
                "convergence_per_time"
            ][stage],
            "stage_seconds": stage_seconds,
            "archive": archive_path.name,
            "archive_sha256": archive_hash,
        }
        rows.append(row)
        previous = projected
        _checkpoint(
            output,
            seed,
            "running" if stage < stages else "complete",
            rows,
            started,
            source_hashes,
            reference_record,
        )

    _checkpoint(
        output,
        seed,
        status,
        rows,
        started,
        source_hashes,
        reference_record,
    )
    _finalize_hashes(output)
    return {
        "seed": seed,
        "status": status,
        "completed_stages": sum(row["complete"] for row in rows),
        "roots_completed": sum(row["root_count"] for row in rows),
        "total_seconds": time.perf_counter() - started,
        "output": str(output),
    }


def preflight() -> dict:
    reference = validate_reference()
    sampler = _load_raw_sampler()
    del sampler
    gram = interface.compute_gram_audit()
    if (
        not gram["positive_definite"]
        or gram["identity_quadrature_max_abs_difference"] > 1.0e-15
        or gram["identity_grid_max_abs_difference"] > 1.0e-14
        or not np.allclose(gram["elliptic_identity"], interface.GRAM, rtol=0, atol=1e-17)
    ):
        raise RuntimeError("Gram preflight failed")
    return {
        "sampler_sha256": EXPECTED_SAMPLER_SHA256,
        "reference": reference,
        "gram": gram,
        "primary_total_roots": PRIMARY_TOTAL_ROOTS,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("preflight")
    primary_parser = subparsers.add_parser("primary")
    primary_parser.add_argument("--seed", required=True, type=int, choices=PRIMARY_SEEDS)
    args = parser.parse_args(argv)
    if args.command == "preflight":
        print(json.dumps(preflight(), indent=2, sort_keys=True, allow_nan=False))
        return 0
    output = ARTIFACT_ROOT / f"dynamic_seed_{args.seed}"
    result = run_seed(seed=args.seed, output=output)
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return 0 if result["status"] == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
