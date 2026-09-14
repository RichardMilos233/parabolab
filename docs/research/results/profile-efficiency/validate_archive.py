"""Read-only numerical archive audit; draws no Monte Carlo samples."""

import csv
import hashlib
import json
import math
import statistics
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
metadata = json.loads((HERE / "metadata.json").read_text())
profiles = [json.loads(line) for line in (HERE / "profiles.jsonl").read_text().splitlines()]
workloads = [json.loads(line) for line in (HERE / "workloads.jsonl").read_text().splitlines()]
points = list(csv.DictReader((HERE / "points.csv").open()))
calibration = json.loads((HERE / "calibration.json").read_text())
setups = json.loads((HERE / "setup_traces.json").read_text())
summary = json.loads((HERE / "summary.json").read_text())
names = metadata["variants"]
checks = {}


def check(name, condition):
    checks[name] = bool(condition)
    if not condition:
        raise AssertionError(name)


def close(x, y):
    return math.isclose(x, y, rel_tol=2e-13, abs_tol=2e-15)


def profile_key(row):
    return row["phase"], row["reuse"], row["replicate"], row["variant_index"], row["curve_index"]


def workload_key(row):
    return row["phase"], row["reuse"], row["replicate"], row["variant_index"]


check("complete_status", metadata["status"] == "complete")
check("protocol_frozen_hash", metadata["source_sha256"][metadata["protocol"]]
      == "0df97adfa09e50921af026f7496b33426ca28aa614252e9c0a0b4301d6555da4")
check("driver_frozen_hash", hashlib.sha256((HERE / "driver_at_execution.py").read_bytes()).hexdigest()
      == "7a9091fe5446f3fc8abb1251dff954d41805ea1f61962e18ba57af9446c33aef")
check("all_source_hashes_match", all(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
      for path, digest in metadata["source_sha256"].items()))
check("no_recorded_deviations_or_failure", metadata["protocol_deviations"] == [] and not (HERE / "failure.json").exists())
check("complete_row_counts", (len(profiles), len(workloads), len(points), len(calibration), len(setups), len(summary))
      == (2200, 400, 11000, 25, 25, 20))
expected = {(phase, reuse, replicate, index, curve) for phase in (1, 2) for reuse in (1, 10)
            for replicate in range(20) for index in range(5) for curve in range(reuse)}
check("complete_unique_profile_keys", {profile_key(row) for row in profiles} == expected
      and len({profile_key(row) for row in profiles}) == len(profiles))
check("complete_unique_workload_keys", {workload_key(row) for row in workloads}
      == {key[:4] for key in expected} and len({workload_key(row) for row in workloads}) == len(workloads))
check("complete_unique_setup_calibration_keys", all(
      {(row["trial"], row["variant_index"]) for row in records} == {(trial, i) for trial in range(5) for i in range(5)}
      for records in (setups, calibration)))
for records, phase in ((setups, 3), (calibration, 4)):
    for trial in range(5):
        expected_order = np.random.default_rng(np.random.SeedSequence(202609143, spawn_key=(phase, trial))).permutation(5).tolist()
        actual_order = [row["variant_index"] for row in sorted((r for r in records if r["trial"] == trial), key=lambda r: r["execution_order"])]
        assert actual_order == expected_order
for phase in (1, 2):
    for replicate in range(20):
        combinations = [(reuse, index) for reuse in (1, 10) for index in range(5)]
        order = np.random.default_rng(np.random.SeedSequence(202609143, spawn_key=(5, phase, replicate))).permutation(10)
        actual = [(row["reuse"], row["variant_index"]) for row in sorted(
            (w for w in workloads if (w["phase"], w["replicate"]) == (phase, replicate)), key=lambda w: w["execution_order"])]
        assert actual == [combinations[i] for i in order]
check("predeclared_independent_execution_order", True)

h = [statistics.median(row["setup_seconds"] for row in setups if row["variant_index"] == index) for index in range(5)]
c = [statistics.median(row["solve_seconds"] for row in calibration if row["variant_index"] == index) / 10000
     for index in range(5)]
check("median_setup_and_calibration_recomputed", all(close(h[i], metadata["setup"][i]["setup_charge_seconds"])
      and close(c[i], metadata["calibration_coefficients"][i]) for i in range(5)))
check("stable_policy_setup_rates", all(max(row["rate"] for row in setups if row["variant_index"] == i)
      - min(row["rate"] for row in setups if row["variant_index"] == i) <= 1e-12 for i in range(5)))
for reuse in (1, 10):
    budget = max(h[i] + reuse * 10000 * c[i] for i in range(5))
    allocation = [math.floor((budget - h[i]) / (reuse * c[i])) for i in range(5)]
    check(f"frozen_budget_and_allocation_R{reuse}", close(budget, metadata["predicted_workload_budgets"][str(reuse)])
          and allocation == metadata["budget_samples_per_point"][str(reuse)])
    check(f"integer_floor_cost_bound_R{reuse}", all(h[i] + reuse * allocation[i] * c[i] <= budget + 2e-15
          and budget < h[i] + reuse * (allocation[i] + 1) * c[i] + 2e-15 for i in range(5)))

all_point_seeds = []
for row in profiles:
    key = profile_key(row)
    seed = int(np.random.SeedSequence(202609143, spawn_key=key).generate_state(1, dtype=np.uint64)[0])
    assert seed == row["seed"]
    all_point_seeds.extend(seed + i for i in range(5))
    phase, reuse, replicate, index, curve = key
    assert row["samples_per_point"] == (10000 if phase == 1 else metadata["budget_samples_per_point"][str(reuse)][index])
    truth = [-.5 - .5 * math.tanh(.75 * .05 - .5 * x) for x in (-2, -1, 0, 1, 2)]
    assert all(close(x, y) for x, y in zip(truth, row["exact"]))
    errors = [x-y for x, y in zip(row["values"], truth)]
    assert all(close(x, y) for x, y in zip(errors, row["errors"]))
    assert close(sum(e*e for e in errors) / 5, row["mse"])
    assert close(math.sqrt(row["mse"]), row["rmse"])
    assert close(max(map(abs, errors)), row["max_abs_error"])
    assert row["solve_seconds"] > 0 and all(math.isfinite(x) for x in row["empirical_stderr"])
for row in calibration:
    seed = int(np.random.SeedSequence(202609143, spawn_key=(0, 1, row["trial"], row["variant_index"], 0))
               .generate_state(1, dtype=np.uint64)[0])
    assert seed == row["seed"] and row["samples_per_point"] == 10000
    all_point_seeds.extend(seed+i for i in range(5))
check("seeds_allocations_analytic_truth_and_profile_errors", True)
check("calibration_evaluation_point_seeds_distinct", len(all_point_seeds) == len(set(all_point_seeds)) == 11125)

profile_map = {profile_key(row): row for row in profiles}
point_keys = set()
for row in points:
    key = tuple(int(row[field]) for field in ("phase", "reuse", "replicate")) + (names.index(row["variant"]), int(row["curve_index"]))
    curve = profile_map[key]
    point_index = metadata["grid"].index(float(row["x"]))
    point_keys.add(key + (point_index,))
    assert int(row["seed"]) == curve["seed"] + point_index
    assert int(row["samples"]) == curve["samples_per_point"]
    for point_field, curve_field in (("estimate", "values"), ("exact", "exact"), ("error", "errors"), ("empirical_stderr", "empirical_stderr")):
        assert close(float(row[point_field]), curve[curve_field][point_index])
check("point_csv_matches_complete_unique_curve_archive", len(point_keys) == len(points)
      and point_keys == {key + (i,) for key in expected for i in range(5)})
for row in workloads:
    key = workload_key(row)
    curves = [profile_map[key + (i,)] for i in range(row["reuse"])]
    mse = math.fsum(curve["mse"] for curve in curves) / row["reuse"]
    solve = math.fsum(curve["solve_seconds"] for curve in curves)
    assert close(mse, row["workload_mse"]) and close(math.sqrt(mse), row["workload_rmse"])
    assert close(solve, row["solve_seconds"])
    assert close(solve+h[row["variant_index"]], row["accounted_total_seconds"])
    assert close(row["accounted_total_seconds"] / row["reuse"], row["per_curve_accounted_seconds"])
check("workloads_average_unpooled_losses_and_charge_one_setup", True)

for row in summary:
    selected = [w for w in workloads if (w["phase"], w["reuse"], w["variant"]) == (row["phase"], row["reuse"], row["variant"])]
    curves = [p for p in profiles if (p["phase"], p["reuse"], p["variant"]) == (row["phase"], row["reuse"], row["variant"])]
    assert len(selected) == 20 and len(curves) == 20 * row["reuse"]
    assert close(math.fsum(w["workload_mse"] for w in selected) / 20, row["aggregate_mse"])
    assert close(math.sqrt(row["aggregate_mse"]), row["aggregate_rmse"])
    assert close(statistics.median(w["accounted_total_seconds"] for w in selected), row["median_accounted_total_seconds"])
    assert all(close(math.sqrt(math.fsum(p["errors"][i]**2 for p in curves) / len(curves)), row["pointwise_rmse"][i]) for i in range(5))
    for baseline in ("default_uniform", "point_short_uniform", "grid_short_uniform"):
        reference = next(r for r in summary if (r["phase"], r["reuse"], r["variant"]) == (row["phase"], row["reuse"], baseline))
        assert close(row["aggregate_mse"] / reference["aggregate_mse"], row[f"mse_ratio_to_{baseline}"])
        assert close(row["aggregate_rmse"] / reference["aggregate_rmse"], row[f"rmse_ratio_to_{baseline}"])
check("summary_losses_costs_point_profiles_and_baseline_ratios", True)
counts = {phase: sum(row["samples_per_point"]*5 for row in profiles if row["phase"] == phase) for phase in (1, 2)}
check("complete_recorded_sample_counts", counts[1] == metadata["fixed_evaluation_trees"] == 55000000
      and counts[2] == metadata["budget_evaluation_trees"])
result = dict(all_checks_pass=True, checks=checks, unique_point_seeds=len(all_point_seeds),
              profile_rows=len(profiles), workload_rows=len(workloads), point_rows=len(points),
              calibration_trees=25*5*10000, fixed_evaluation_trees=counts[1], budget_evaluation_trees=counts[2],
              scope="Archive arithmetic/provenance/count audit only; no statistical significance or hardware isolation claim")
(HERE / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
