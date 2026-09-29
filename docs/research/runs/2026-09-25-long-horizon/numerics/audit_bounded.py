"""Reproduce the immutable bounded-majority raw-data audit.

This script reads the existing result JSON and NPZ archive, performs strict
assertions, and writes separate reproducible audit outputs.  It never edits
the experiment evidence and never clips floating-point samples.
"""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
RESULTS = HERE / "bounded-results.json"
RAW = HERE / "bounded-raw.npz"
REFERENCE_AUDIT = HERE / "bounded-audit.json"
OUTPUT = HERE / "bounded-audit-reproducible.json"
LOG = HERE / "bounded-audit-reproducible.log"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def log(message: str) -> None:
    line = f"{datetime.now(timezone.utc).isoformat()} {message}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as stream:
        stream.write(line + "\n")


def main() -> None:
    LOG.write_text("", encoding="utf-8")
    log("start strict bounded raw-data audit")

    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    reference = json.loads(REFERENCE_AUDIT.read_text(encoding="utf-8"))
    with np.load(RAW, allow_pickle=False) as archive:
        required = {
            "values",
            "node_counts",
            "root_branched",
            "problem",
            "state_kind",
            "horizon",
            "rate",
            "x",
            "seed",
        }
        assert set(archive.files) == required, archive.files
        values = archive["values"]
        nodes = archive["node_counts"]
        branched = archive["root_branched"]
        raw_problem = archive["problem"]
        raw_state_kind = archive["state_kind"]
        raw_horizon = archive["horizon"]
        raw_rate = archive["rate"]
        raw_x = archive["x"]
        raw_seed = archive["seed"]

    n_rows = 60
    n_samples = 2048
    rows = results["rows"]
    assert results["n_rows"] == n_rows
    assert results["n_samples_per_row"] == n_samples
    assert len(rows) == n_rows
    assert values.shape == (n_rows, n_samples)
    assert nodes.shape == (n_rows, n_samples)
    assert branched.shape == (n_rows, n_samples)
    assert values.dtype == np.dtype("float64")
    assert nodes.dtype == np.dtype("int64")
    assert branched.dtype == np.dtype("bool")

    expected_seeds = np.arange(20260925, 20260925 + n_rows, dtype=np.int64)
    np.testing.assert_array_equal(raw_seed, expected_seeds)
    np.testing.assert_array_equal(
        np.array([row["seed"] for row in rows], dtype=np.int64), expected_seeds
    )
    np.testing.assert_array_equal(raw_problem, [row["problem"] for row in rows])
    np.testing.assert_array_equal(
        raw_state_kind, [row["state_kind"] for row in rows]
    )
    np.testing.assert_array_equal(raw_horizon, [row["horizon"] for row in rows])
    np.testing.assert_array_equal(raw_rate, [row["rate"] for row in rows])
    np.testing.assert_array_equal(raw_x, [row["x"] for row in rows])
    assert [row["row_index"] for row in rows] == list(range(n_rows))

    assert np.all(np.isfinite(values))
    assert np.all(nodes >= 1)
    assert np.all((nodes - 1) % 3 == 0)
    np.testing.assert_array_equal(branched, nodes > 1)

    alpha = float(results["alpha"])
    point_radius = math.sqrt(2.0 * math.log(2.0 / alpha) / n_samples)
    simultaneous_radius = math.sqrt(
        2.0 * math.log(2.0 * n_rows / alpha) / n_samples
    )
    assert results["pointwise_hoeffding_radius"] == point_radius
    assert results["simultaneous_hoeffding_radius"] == simultaneous_radius

    pointwise_cover = []
    simultaneous_cover = []
    for index, row in enumerate(rows):
        row_values = values[index]
        row_nodes = nodes[index]
        row_branched = branched[index]
        mean = float(row_values.mean())
        variance = float(row_values.var(ddof=1))
        stderr = math.sqrt(variance / n_samples)
        mean_nodes = float(row_nodes.mean())
        max_nodes = int(row_nodes.max())
        root_fraction = float(row_branched.mean())
        expected_nodes = (
            3.0 * math.exp(2.0 * row["rate"] * row["horizon"]) - 1.0
        ) / 2.0

        assert row["n_samples"] == n_samples
        assert row["mean"] == mean
        assert row["variance"] == variance
        assert row["stderr"] == stderr
        assert row["normal_stderr_diagnostic"] == stderr
        assert row["mean_nodes"] == mean_nodes
        assert row["max_nodes"] == max_nodes
        assert row["root_branch_fraction"] == root_fraction
        assert row["expected_nodes"] == expected_nodes
        assert row["node_mean_relative_error"] == mean_nodes / expected_nodes - 1.0
        assert row["variance_times_expected_nodes"] == variance * expected_nodes
        assert row["error"] == mean - row["exact"]
        assert row["hoeffding_95_radius"] == point_radius
        assert row["simultaneous_95_radius"] == simultaneous_radius
        assert row["hoeffding_95_interval"] == [
            mean - point_radius,
            mean + point_radius,
        ]
        assert row["simultaneous_95_interval"] == [
            mean - simultaneous_radius,
            mean + simultaneous_radius,
        ]

        point_covers = abs(mean - row["exact"]) <= point_radius
        simultaneous_covers = abs(mean - row["exact"]) <= simultaneous_radius
        assert row["hoeffding_95_covers_exact"] is point_covers
        assert row["simultaneous_95_covers_exact"] is simultaneous_covers
        pointwise_cover.append(point_covers)
        simultaneous_cover.append(simultaneous_covers)

    assert len(pointwise_cover) == n_rows and all(pointwise_cover)
    assert len(simultaneous_cover) == n_rows and all(simultaneous_cover)

    outside_mask = (values < -1.0) | (values > 1.0)
    outside_samples = np.argwhere(outside_mask).tolist()
    expected_outside = [[26, 472], [26, 536], [26, 918]]
    assert outside_samples == expected_outside
    assert int(outside_mask.sum()) == 3
    one_ulp_below_minus_one = np.nextafter(-1.0, -math.inf)
    np.testing.assert_array_equal(values[outside_mask], one_ulp_below_minus_one)
    max_overshoot = float(
        max(max(0.0, -1.0 - values.min()), max(0.0, values.max() - 1.0))
    )
    assert max_overshoot == float(np.spacing(1.0))

    raw_hash = sha256(RAW)
    assert raw_hash == results["raw_sha256"]
    assert raw_hash == reference["raw_sha256"]
    assert sha256(REPO / results["protocol"]) == results["protocol_sha256"]
    for relative_path, expected_hash in results["source_sha256"].items():
        assert sha256(REPO / relative_path) == expected_hash, relative_path

    reproduced = {
        "rows": n_rows,
        "roots": int(values.size),
        "sampled_nodes": int(nodes.sum()),
        "stats_recomputed_exactly": True,
        "finite_values": True,
        "full_ternary_node_counts": True,
        "root_branch_flags_match_counts": True,
        "outside_exact_interval_count": int(outside_mask.sum()),
        "outside_samples": outside_samples,
        "min_value": float(values.min()),
        "max_value": float(values.max()),
        "max_interval_overshoot": max_overshoot,
        "roundoff_note": (
            "Floating branch evaluation can exceed the ideal interval by one "
            "ulp; no clipping was applied. Exact-arithmetic Hoeffding theory "
            "does not itself certify floating error."
        ),
        "all_pointwise_95_cover_exact": all(pointwise_cover),
        "all_simultaneous_95_cover_exact": all(simultaneous_cover),
        "max_realized_mean_error": max(abs(row["error"]) for row in rows),
        "raw_sha256": raw_hash,
    }
    assert reproduced == reference

    output = {
        **reproduced,
        "all_strict_assertions_passed": True,
        "input_results": RESULTS.name,
        "input_results_sha256": sha256(RESULTS),
        "input_raw": RAW.name,
        "reference_audit": REFERENCE_AUDIT.name,
        "reference_audit_sha256": sha256(REFERENCE_AUDIT),
        "audit_script": Path(__file__).name,
        "audit_script_sha256": sha256(Path(__file__)),
        "verified_source_sha256": results["source_sha256"],
        "clipping_applied_by_audit": False,
    }
    OUTPUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    log(
        "PASS rows=60 roots=122880 sampled_nodes=60696849 "
        "pointwise_cover=60/60 simultaneous_cover=60/60 "
        "one_ulp_outside=3 source_hashes=4 raw_hash=verified"
    )


if __name__ == "__main__":
    main()
