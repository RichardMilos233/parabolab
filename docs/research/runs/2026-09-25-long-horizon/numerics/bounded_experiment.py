"""Execute the frozen 60-row bounded-majority sampling protocol.

Run from the repository root with the project Python.  Every scheduled root
is completed without a depth/node cutoff, clipping, or outlier removal.  The
sampler's root batches limit working memory only.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from parabolab.library import allen_cahn_flat, allen_cahn_wave_1d
from parabolab.majority import sample_majority


HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "protocol.json"
AMENDMENT = HERE / "protocol-amendment-before-code.md"
RAW_OUTPUT = HERE / "bounded-raw.npz"
RESULT_OUTPUT = HERE / "bounded-results.json"
LOG_OUTPUT = HERE / "bounded-execution.log"
REPO = HERE.parents[4]
SAMPLER_SOURCE = REPO / "parabolab" / "majority.py"

ALPHA = 0.05
BATCH_SIZE = 32


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _log(message: str) -> None:
    line = f"{datetime.now(timezone.utc).isoformat()} {message}"
    print(line, flush=True)
    with LOG_OUTPUT.open("a", encoding="utf-8") as stream:
        stream.write(line + "\n")


def _schedule(spec: dict) -> list[dict]:
    bounded = spec["bounded_sampling"]
    rates_and_horizons = [(2.0, bounded["rate2_horizons"])]
    rates_and_horizons.extend(
        (float(rate), bounded["additional_rate_horizons"])
        for rate in bounded["additional_rates"]
    )
    schedule = []
    for rate, horizons in rates_and_horizons:
        for horizon in horizons:
            horizon = float(horizon)
            schedule.append(
                {
                    "problem": "flat",
                    "state_kind": "flat",
                    "horizon": horizon,
                    "rate": rate,
                    "x": float(bounded["flat_grid"][0]),
                }
            )
            for x in bounded["wave_grid"]:
                schedule.append(
                    {
                        "problem": "wave",
                        "state_kind": "fixed",
                        "horizon": horizon,
                        "rate": rate,
                        "x": float(x),
                    }
                )
            schedule.append(
                {
                    "problem": "wave",
                    "state_kind": "moving_front",
                    "horizon": horizon,
                    "rate": rate,
                    "x": 1.5 * horizon,
                }
            )
    return schedule


def main() -> None:
    spec = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    if not spec.get("frozen_before_numerical_implementation"):
        raise RuntimeError("protocol.json was not frozen before implementation")
    bounded = spec["bounded_sampling"]
    schedule = _schedule(spec)
    scheduled_rows = int(bounded["scheduled_rows"])
    if len(schedule) != scheduled_rows or scheduled_rows != 60:
        raise RuntimeError(
            f"schedule has {len(schedule)} rows, expected {scheduled_rows} == 60"
        )

    n_samples = int(bounded["n_samples_per_point"])
    seed_base = int(bounded["seed_base"])
    point_radius = math.sqrt(2.0 * math.log(2.0 / ALPHA) / n_samples)
    simultaneous_radius = math.sqrt(
        2.0 * math.log(2.0 * scheduled_rows / ALPHA) / n_samples
    )
    raw_values = np.empty((scheduled_rows, n_samples), dtype=float)
    raw_nodes = np.empty((scheduled_rows, n_samples), dtype=np.int64)
    raw_root_branched = np.empty((scheduled_rows, n_samples), dtype=bool)
    rows = []

    LOG_OUTPUT.write_text("", encoding="utf-8")
    started_at = datetime.now(timezone.utc).isoformat()
    whole_start = time.perf_counter()
    _log(
        f"start rows={scheduled_rows} samples_per_row={n_samples} "
        f"batch_size={BATCH_SIZE}"
    )
    try:
        for index, scheduled in enumerate(schedule):
            horizon = scheduled["horizon"]
            rate = scheduled["rate"]
            x = scheduled["x"]
            seed = seed_base + index
            pde = (
                allen_cahn_flat(phi0=0.5, T=horizon)
                if scheduled["problem"] == "flat"
                else allen_cahn_wave_1d(T=horizon)
            )
            result = sample_majority(
                pde,
                0.0,
                x,
                n_samples,
                rate=rate,
                seed=seed,
                batch_size=BATCH_SIZE,
            )
            raw_values[index] = result.values
            raw_nodes[index] = result.node_counts
            raw_root_branched[index] = result.root_branched

            mean = result.estimate
            variance = result.sample_variance
            exact = float(pde.exact_solution(0.0, x))
            expected_nodes = (3.0 * math.exp(2.0 * rate * horizon) - 1.0) / 2.0
            expected_root_branch_fraction = 1.0 - math.exp(-rate * horizon)
            row = {
                **scheduled,
                "row_index": index,
                "seed": seed,
                "n_samples": n_samples,
                "mean": mean,
                "variance": variance,
                "stderr": result.stderr,
                "normal_stderr_diagnostic": result.stderr,
                "exact": exact,
                "error": mean - exact,
                "hoeffding_95_radius": point_radius,
                "hoeffding_95_interval": [mean - point_radius, mean + point_radius],
                "hoeffding_95_covers_exact": abs(mean - exact) <= point_radius,
                "simultaneous_95_radius": simultaneous_radius,
                "simultaneous_95_interval": [
                    mean - simultaneous_radius,
                    mean + simultaneous_radius,
                ],
                "simultaneous_95_covers_exact": (
                    abs(mean - exact) <= simultaneous_radius
                ),
                "root_branch_fraction": float(result.root_branched.mean()),
                "expected_root_branch_fraction": expected_root_branch_fraction,
                "mean_nodes": result.mean_nodes,
                "max_nodes": result.max_nodes,
                "expected_nodes": expected_nodes,
                "node_mean_relative_error": result.mean_nodes / expected_nodes - 1.0,
                "variance_times_expected_nodes": variance * expected_nodes,
                "seconds": result.seconds,
            }
            rows.append(row)
            _log(
                f"row={index:02d} problem={row['problem']} "
                f"state={row['state_kind']} T={horizon:g} r={rate:g} x={x:g} "
                f"mean={mean:+.8f} exact={exact:+.8f} "
                f"nodes={result.mean_nodes:.2f}/{expected_nodes:.2f} "
                f"seconds={result.seconds:.3f}"
            )
    except BaseException as exc:
        _log(f"FAILED after_completed_rows={len(rows)} error={exc!r}")
        raise

    np.savez_compressed(
        RAW_OUTPUT,
        values=raw_values,
        node_counts=raw_nodes,
        root_branched=raw_root_branched,
        problem=np.array([row["problem"] for row in rows]),
        state_kind=np.array([row["state_kind"] for row in rows]),
        horizon=np.array([row["horizon"] for row in rows]),
        rate=np.array([row["rate"] for row in rows]),
        x=np.array([row["x"] for row in rows]),
        seed=np.array([row["seed"] for row in rows], dtype=np.int64),
    )
    elapsed = time.perf_counter() - whole_start
    source_hashes = {
        str(path.relative_to(REPO)): _sha256(path)
        for path in (PROTOCOL, AMENDMENT, Path(__file__), SAMPLER_SOURCE)
    }
    payload = {
        "protocol": str(PROTOCOL.relative_to(REPO)),
        "protocol_sha256": _sha256(PROTOCOL),
        "protocol_amendment": str(AMENDMENT.relative_to(REPO)),
        "raw_file": RAW_OUTPUT.name,
        "raw_sha256": _sha256(RAW_OUTPUT),
        "source_sha256": source_hashes,
        "started_at_utc": started_at,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_seconds": elapsed,
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "n_rows": scheduled_rows,
        "n_samples_per_row": n_samples,
        "batch_size": BATCH_SIZE,
        "alpha": ALPHA,
        "pointwise_hoeffding_radius": point_radius,
        "simultaneous_hoeffding_radius": simultaneous_radius,
        "floating_evaluation_error_enclosed": False,
        "depth_or_node_cutoff": None,
        "clipping": False,
        "outlier_removal": False,
        "discarded_roots": 0,
        "rows": rows,
    }
    RESULT_OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _log(
        f"complete rows={scheduled_rows} roots={scheduled_rows * n_samples} "
        f"total_seconds={elapsed:.3f} raw_sha256={payload['raw_sha256']}"
    )


if __name__ == "__main__":
    main()
