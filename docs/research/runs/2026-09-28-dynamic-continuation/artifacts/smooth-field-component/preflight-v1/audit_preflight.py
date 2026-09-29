"""Read-only independent consistency audit of the bounded T99 preflight."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np


THIS = Path(__file__).resolve()
PREFLIGHT_ROOT = THIS.parent
ARTIFACT_ROOT = PREFLIGHT_ROOT.parent
RUN_ROOT = ARTIFACT_ROOT.parents[1]
CODE_ROOT = RUN_ROOT / "code" / "smooth-field-component-v1"
sys.path.insert(0, str(CODE_ROOT))

from budget import sha256_path  # noqa: E402
from smooth_field import COEFFICIENT_COUNT, h2_norm_squared  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    latest = json.loads((PREFLIGHT_ROOT / "latest_preflight.json").read_text())
    run_directory = PREFLIGHT_ROOT / latest["run_directory"]
    result_path = run_directory / "preflight_result.json"
    require(sha256_path(result_path) == latest["preflight_result_sha256"], "latest hash mismatch")
    result = json.loads(result_path.read_text())
    require(result["status"].startswith("passed_implementation_preflight"), "preflight did not pass")

    metadata = [json.loads(line) for line in (run_directory / "sample_metadata.jsonl").read_text().splitlines()]
    require(len(metadata) == 180, "metadata row count is not 180")
    require(result["completed_outputs"] == 180, "result output count differs")
    arrays = sorted((run_directory / "arrays").glob("*.npy"))
    require(len(arrays) == 180, "raw array count is not 180")
    require(not (run_directory / "failures").exists(), "preflight contains a failure directory")

    arrays_by_name: dict[str, np.ndarray] = {}
    total_metadata_queries = 0
    total_metadata_segments = 0
    tags: set[int] = set()
    for row in metadata:
        path = run_directory / row["array_path"]
        require(path.exists(), f"missing array {path}")
        require(sha256_path(path) == row["array_sha256"], f"array hash mismatch {path.name}")
        array = np.load(path, allow_pickle=False)
        require(array.shape == (COEFFICIENT_COUNT,), f"wrong shape {path.name}")
        require(array.dtype == np.float64, f"wrong dtype {path.name}")
        require(bool(np.all(np.isfinite(array))), f"nonfinite array {path.name}")
        require(math.isfinite(h2_norm_squared(array)), f"nonfinite H2 norm {path.name}")
        require(row["opaque_calls"] <= row["cell"]["derivative_order"], "query cap violated")
        require(row["opaque_calls"] == row["opaque_attempts"], "opaque count mismatch")
        total_metadata_queries += row["opaque_calls"]
        total_metadata_segments += row["segment_count"]
        tags.add(row["rng_stream_identifier"]["tag"])
        arrays_by_name[path.name] = array
    require(tags == {1}, f"preflight contains non-tag-1 samples: {tags}")
    require(total_metadata_queries == 215, "metadata opaque total is not 215")
    require(total_metadata_segments == 1701, "random tree segment total is not 1701")

    for cell in range(12):
        for seed in (2026092901, 2026092902, 2026092903):
            primary = arrays_by_name[f"primary-cell-{cell:02d}-seed-{seed}-sample-0000.npy"]
            repeat = arrays_by_name[f"repeat-cell-{cell:02d}-seed-{seed}-sample-0000.npy"]
            require(np.array_equal(primary, repeat), "tag-1 reproducibility mismatch")

    fixture = json.loads((run_directory / "fixture_results.json").read_text())
    require(fixture["all_passed"] is True, "fixture aggregate is not passed")
    for record in fixture["covariance_fixtures"]:
        require(all(record["checks"].values()), f"covariance fixture failed: {record['label']}")
        edge = np.asarray(record["actual_edge_gaussians"], dtype=np.float64)
        require(np.all(np.isfinite(edge)), f"fixture edge array nonfinite: {record['label']}")
    require(all(record["passed"] for record in fixture["derivative_fixtures"]), "derivative fixture failed")
    require(fixture["fourier_sign_fixture"]["passed"], "Fourier sign fixture failed")
    require(fixture["n_less_than_j_fixture"]["passed"], "n<j fixture failed")
    require(fixture["h2_fixture"]["passed"], "H2 fixture failed")

    references = json.loads((PREFLIGHT_ROOT / "analytic_references.json").read_text())
    require(references["precision_decimal_digits"] == 100, "reference precision changed")
    require(len(references["records"]) == 12, "reference count is not 12")
    for record in references["records"]:
        value = float.fromhex(record["binary64_hex"])
        require(value == record["binary64"], "binary64 reference hex mismatch")
        expected_sign = 1 if record["nonzero_coefficient_index"] == 1 else -1
        require(math.copysign(1.0, value) == expected_sign, "reference sign mismatch")

    state = json.loads((ARTIFACT_ROOT / "budget_state.json").read_text())
    journal_events = []
    with (ARTIFACT_ROOT / "budget_journal.jsonl").open() as handle:
        for line_number, line in enumerate(handle, 1):
            require(line.endswith("\n"), f"partial journal line {line_number}")
            event = json.loads(line)
            require(event["sequence"] == line_number - 1, "journal sequence gap")
            journal_events.append(event)
    require(journal_events[-1]["state_after"] == state, "journal/state final snapshot mismatch")
    oracle_events = [event for event in journal_events if event["kind"] == "oracle_charge_before_evaluation"]
    require(
        len(oracle_events) == state["oracle_calls"]["preflight"],
        "journal opaque event count differs from persistent state",
    )
    require(all(event["detail"]["phase"] == "preflight" for event in oracle_events), "non-preflight oracle event")
    require(state == result["budget_after"], "latest result budget_after differs from persistent state")
    require(state["oracle_calls"]["official"] == 0, "official oracle calls are not zero")
    require(state["oracle_calls"]["replay"] == 0, "replay oracle calls are not zero")
    require(
        state["oracle_calls"]["total"] == state["oracle_calls"]["preflight"],
        "global oracle total does not equal preflight total",
    )
    before = result["budget_before"]
    require(
        state["oracle_calls"]["preflight"] - before["oracle_calls"]["preflight"] == 215,
        "latest preflight opaque delta is not 215",
    )
    require(state["active_segment_reservations"] == {}, "unresolved segment reservation")
    require(state["segments_reserved"] == 0, "reserved segment capacity remains")
    expected_deltas = {
        "segments_generated": 1728,
        "exponential_draws": 1701,
        "gaussian_draws": 1718,
        "uniform_draws": 181,
        "tuple_draw_calls": 143,
        "tuple_indices_drawn": 215,
        "known_evaluator_calls": 1221,
    }
    for counter, expected_delta in expected_deltas.items():
        require(state[counter] - before[counter] == expected_delta, f"latest {counter} delta differs")
    require(
        state["completed_samples"]["preflight"]
        - before["completed_samples"]["preflight"]
        == 180,
        "latest sample completion delta differs",
    )
    require(state["completed_samples"]["official"] == 0, "official completed samples are not zero")
    require(state["completed_samples"]["replay"] == 0, "replay completed samples are not zero")
    require(state["failed_samples"] == {"preflight": 0, "official": 0, "replay": 0}, "sample failure totals differ")

    manifest = json.loads((PREFLIGHT_ROOT / "implementation_manifest.json").read_text())
    for name, digest in manifest["source_hashes"].items():
        require(sha256_path(CODE_ROOT / name) == digest, f"current source differs: {name}")
    payload = {
        "status": "passed",
        "read_only": True,
        "official_executed": False,
        "opaque_calls_made_by_audit": 0,
        "raw_arrays_checked": len(arrays),
        "metadata_rows_checked": len(metadata),
        "journal_events_checked": len(journal_events),
        "cumulative_generated_segments_reconciled": state["segments_generated"],
        "latest_generated_segment_delta": state["segments_generated"] - before["segments_generated"],
        "cumulative_preflight_opaque_calls_reconciled": len(oracle_events),
        "implementation_manifest_sha256": sha256_path(PREFLIGHT_ROOT / "implementation_manifest.json"),
        "preflight_result_sha256": sha256_path(result_path),
        "audit_source_sha256": hashlib.sha256(THIS.read_bytes()).hexdigest(),
    }
    print(json.dumps(payload, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
