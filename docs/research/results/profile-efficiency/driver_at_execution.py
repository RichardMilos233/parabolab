"""Prespecified profile-rate and policy-reuse benchmark; requires explicit --run.

Protocol: docs/research/results/profile-efficiency-protocol.md. The default
solver interface and complete-tree sampling are preserved. Do not start a
run until coordinated heavy work has stopped and the profile API is ready.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from parabolab import CodingTreeMC, MomentQuadrature
from parabolab.library import allen_cahn_wave_1d
from parabolab.rate_optimization import optimize_exponential_rate_1d


GRID = np.array([-2., -1., 0., 1., 2.])
WEIGHTS = np.full(5, 1 / 5)
HORIZON = 0.05
SAMPLES = 10000
REPLICATES = 20
SETUP_TRIALS = 5
CALIBRATION_TRIALS = 5
REUSE_COUNTS = (1, 10)
ENTROPY = 202609143
PROTOCOL = Path("docs/research/results/profile-efficiency-protocol.md")
VARIANTS = (
    "default_uniform", "point_short_uniform", "point_selected_uniform",
    "grid_short_uniform", "grid_selected_uniform",
)
LABELS = ("Default", "Point short", "Point selected", "Grid short", "Grid selected")


def profile_seed(phase, reuse, replicate, variant, curve_index):
    sequence = np.random.SeedSequence(
        ENTROPY, spawn_key=(phase, reuse, replicate, variant, curve_index))
    return int(sequence.generate_state(1, dtype=np.uint64)[0])


def permutation(key, size):
    return np.random.default_rng(np.random.SeedSequence(ENTROPY, spawn_key=key)).permutation(size).tolist()


def workload_order(phase, replicate):
    combinations = [(reuse, index) for reuse in REUSE_COUNTS for index in range(len(VARIANTS))]
    return [combinations[index] for index in permutation((5, phase, replicate), len(combinations))]


def verify_seed_plan():
    seeds = []
    for trial in range(CALIBRATION_TRIALS):
        for index in range(len(VARIANTS)):
            seed = profile_seed(0, 1, trial, index, 0)
            seeds.extend(seed + point for point in range(len(GRID)))
    for phase in (1, 2):
        for reuse in REUSE_COUNTS:
            for rep in range(REPLICATES):
                for index in range(len(VARIANTS)):
                    for curve_index in range(reuse):
                        seed = profile_seed(phase, reuse, rep, index, curve_index)
                        seeds.extend(seed + point for point in range(len(GRID)))
    if len(set(seeds)) != len(seeds):
        raise RuntimeError("Point-seed collision in the planned calibration/evaluation streams")
    return dict(unique_point_seeds=len(seeds), setup_constructions=SETUP_TRIALS * len(VARIANTS),
                calibration_profiles=CALIBRATION_TRIALS * len(VARIANTS),
                evaluation_workloads=2 * len(REUSE_COUNTS) * REPLICATES * len(VARIANTS),
                evaluation_profiles=2 * sum(REUSE_COUNTS) * REPLICATES * len(VARIANTS),
                fixed_evaluation_trees=sum(REUSE_COUNTS) * REPLICATES * len(VARIANTS) * len(GRID) * SAMPLES)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def construct_policy(index):
    # Imports are a shared application cost, excluded from every setup trace.
    from parabolab.profile_rates import optimize_profile_rate_1d, short_time_profile_rate

    started = time.perf_counter()
    pde = allen_cahn_wave_1d(T=HORIZON)
    pde_seconds = time.perf_counter() - started
    tune_started = time.perf_counter()
    optimizer = None
    settings = dict(max_depth=2, bracket=(0.2, 2.0), tol=1e-5,
                    quadrature=MomentQuadrature(time_order=4, normal_order=4))
    if index == 2:
        result = optimize_exponential_rate_1d(pde, 0., 0., **settings)
    elif index == 4:
        result = optimize_profile_rate_1d(pde, 0., GRID, weights=WEIGHTS, **settings)
    elif index == 3:
        rate = float(short_time_profile_rate(pde, GRID, weights=WEIGHTS))
    elif index == 1:
        value = pde.phi(0.)
        rate = abs(pde.f(value)) / abs(value)
    else:
        rate = 1.0
    if index in (2, 4):
        if not result.converged:
            raise RuntimeError(f"Deterministic selector did not converge: {VARIANTS[index]}")
        rate = result.rate
        optimizer = dict(second_moment=result.second_moment, d_rate=result.d_rate,
                         d2_rate=result.d2_rate, iterations=result.iterations,
                         final_bracket=list(result.bracket), converged=result.converged)
    tuning_seconds = time.perf_counter() - tune_started
    total = time.perf_counter() - started
    if not math.isfinite(rate) or rate <= 0:
        raise RuntimeError(f"Invalid constructed rate: {VARIANTS[index]} {rate}")
    return (pde, rate), dict(variant=VARIANTS[index], variant_index=index, rate=rate,
                            pde_seconds=pde_seconds, tuning_seconds=tuning_seconds,
                            setup_seconds=total, optimizer=optimizer)


def solve_profile(state, phase, reuse, replicate, index, curve_index, samples):
    pde, rate = state
    seed = profile_seed(phase, reuse, replicate, index, curve_index)
    solver = CodingTreeMC(n_samples=samples, seed=seed, rate=rate,
                          n_jobs=1, label=VARIANTS[index])
    started = time.perf_counter()
    curve = solver.solve(pde, GRID, t=0.)
    seconds = time.perf_counter() - started
    if not (np.isfinite(curve.values).all() and np.isfinite(curve.stderr).all()):
        raise RuntimeError(f"Nonfinite curve: phase={phase},R={reuse},rep={replicate},variant={index},curve={curve_index}")
    return seed, curve, seconds


def load_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def summarize(output):
    metadata = json.loads((output / "metadata.json").read_text())
    workloads = load_jsonl(output / "workloads.jsonl")
    profiles = load_jsonl(output / "profiles.jsonl")
    summary = []
    for phase in (1, 2):
        for reuse in REUSE_COUNTS:
            for index, name in enumerate(VARIANTS):
                selected = [row for row in workloads if (row["phase"], row["reuse"], row["variant"]) == (phase, reuse, name)]
                curves = [row for row in profiles if (row["phase"], row["reuse"], row["variant"]) == (phase, reuse, name)]
                if len(selected) != REPLICATES or len(curves) != reuse * REPLICATES:
                    raise RuntimeError(f"Incomplete scheduled group {phase}/{reuse}/{name}")
                mse = np.array([row["workload_mse"] for row in selected])
                rmse = np.sqrt(mse)
                costs = np.array([row["accounted_total_seconds"] for row in selected])
                solves = np.array([row["solve_seconds"] for row in selected])
                errors = np.array([row["errors"] for row in curves])
                summary.append(dict(
                    phase=phase, reuse=reuse, variant=name, rate=metadata["setup"][index]["rate"],
                    samples_per_point=selected[0]["samples_per_point"], workloads=REPLICATES,
                    requested_curves=len(curves), aggregate_mse=float(np.mean(mse)),
                    aggregate_rmse=float(np.sqrt(np.mean(mse))), median_rmse=float(np.median(rmse)),
                    q25_rmse=float(np.quantile(rmse, .25)), q75_rmse=float(np.quantile(rmse, .75)),
                    min_rmse=float(rmse.min()), max_rmse=float(rmse.max()),
                    median_accounted_total_seconds=float(np.median(costs)),
                    min_accounted_total_seconds=float(costs.min()), max_accounted_total_seconds=float(costs.max()),
                    median_solve_seconds=float(np.median(solves)),
                    min_solve_seconds=float(solves.min()), max_solve_seconds=float(solves.max()),
                    median_per_curve_seconds=float(np.median(costs) / reuse),
                    min_per_curve_seconds=float(costs.min() / reuse),
                    max_per_curve_seconds=float(costs.max() / reuse),
                    predicted_total_seconds=(None if phase == 1 else
                                             metadata["predicted_allocated_costs"][str(reuse)][index]),
                    median_cost_ratio_to_predicted=(None if phase == 1 else
                        float(np.median(costs)) / metadata["predicted_allocated_costs"][str(reuse)][index]),
                    pointwise_rmse=np.sqrt(np.mean(errors**2, axis=0)).tolist(),
                    pointwise_mean_error=np.mean(errors, axis=0).tolist(),
                ))
    for row in summary:
        for baseline in ("default_uniform", "point_short_uniform", "grid_short_uniform"):
            reference = next(r for r in summary if (r["phase"], r["reuse"], r["variant"]) == (row["phase"], row["reuse"], baseline))
            row[f"mse_ratio_to_{baseline}"] = row["aggregate_mse"] / reference["aggregate_mse"]
            row[f"rmse_ratio_to_{baseline}"] = row["aggregate_rmse"] / reference["aggregate_rmse"]
    write_json(output / "summary.json", summary)
    fields = [name for name in summary[0] if not name.startswith("pointwise")]
    with (output / "summary.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(summary)
    colors = plt.get_cmap("tab10").colors
    for phase, stem in ((1, "fixed_n"), (2, "predicted_budget")):
        fig, axes = plt.subplots(2, 2, figsize=(14, 9))
        for row_index, reuse in enumerate(REUSE_COUNTS):
            distributions = [[row["workload_rmse"] for row in workloads
                              if (row["phase"], row["reuse"], row["variant"]) == (phase, reuse, name)] for name in VARIANTS]
            axes[row_index, 0].boxplot(distributions, tick_labels=LABELS, showfliers=False)
            for index, values in enumerate(distributions):
                axes[row_index, 0].scatter(index + 1 + np.linspace(-.15, .15, len(values)), values,
                                           s=16, alpha=.7, color=colors[index])
                selected = [row for row in workloads if (row["phase"], row["reuse"], row["variant"]) == (phase, reuse, VARIANTS[index])]
                axes[row_index, 1].scatter([row["accounted_total_seconds"] / reuse for row in selected],
                                           [row["workload_rmse"] for row in selected],
                                           s=20, alpha=.65, color=colors[index], label=LABELS[index])
            axes[row_index, 0].set_title(f"R={reuse} independently requested curve(s) per workload")
            axes[row_index, 0].set_ylabel("Workload RMSE; predictions are not pooled")
            axes[row_index, 0].tick_params(axis="x", rotation=20)
            axes[row_index, 1].set_xlabel("(Recorded solve time + median setup charge) / R, seconds")
            axes[row_index, 1].set_ylabel("Workload RMSE")
            axes[row_index, 1].legend(fontsize=8)
            for axis in axes[row_index]:
                axis.grid(True, alpha=.25)
        fig.suptitle("Profile-rate efficiency: " + ("fixed N=10,000/point" if phase == 1 else "calibrated predicted budget"))
        fig.tight_layout()
        fig.savefig(output / f"{stem}.png", dpi=180)
        plt.close(fig)
    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    for row_index, phase in enumerate((1, 2)):
        for column, reuse in enumerate(REUSE_COUNTS):
            for index, name in enumerate(VARIANTS):
                row = next(r for r in summary if (r["phase"], r["reuse"], r["variant"]) == (phase, reuse, name))
                axes[row_index, column].plot(GRID, row["pointwise_rmse"], marker="o", color=colors[index], label=LABELS[index])
            axes[row_index, column].set_title(f"{'Fixed N' if phase == 1 else 'Predicted budget'}, R={reuse}")
            axes[row_index, column].set_xlabel("Spatial point x")
            axes[row_index, column].set_ylabel("Pointwise RMSE across all requested curves")
            axes[row_index, column].grid(True, alpha=.25)
            axes[row_index, column].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(output / "pointwise_rmse.png", dpi=180)
    plt.close(fig)
    return summary


def run(output, base_commit, timing_context):
    if output.exists() and any(output.iterdir()):
        raise FileExistsError("Run directory must be new or empty; use --report-only for existing results")
    output.mkdir(parents=True, exist_ok=True)
    plan = verify_seed_plan()
    started = time.perf_counter()
    source = Path(__file__).resolve()
    paths = [source, PROTOCOL, Path("parabolab/profile_rates.py"), Path("parabolab/rate_optimization.py"),
             Path("parabolab/tree.py"), Path("parabolab/solve.py"), Path("parabolab/profiles.py"),
             Path("parabolab/mc.py"), Path("parabolab/mechanism.py"), Path("parabolab/library.py")]
    metadata = dict(
        status="started", date="2026-09-14", declared_branch="codex/research-profile-efficiency",
        base_commit_from_coordinator=base_commit, python=platform.python_version(), numpy=np.__version__,
        platform=platform.platform(), command=[sys.executable, *sys.argv], timing_context=timing_context,
        source_sha256={str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
        protocol=str(PROTOCOL), entropy=ENTROPY, grid=GRID.tolist(), weights=WEIGHTS.tolist(),
        horizon=HORIZON, replicates=REPLICATES, setup_trials=SETUP_TRIALS,
        calibration_trials=CALIBRATION_TRIALS, reuse_counts=list(REUSE_COUNTS),
        fixed_samples_per_point=SAMPLES, variants=list(VARIANTS), seed_plan=plan,
        selector=dict(depth=2, time_order=4, normal_order=4, bracket=[.2, 2.], tol=1e-5),
        seed_definition="uint64 SeedSequence(entropy,spawn_key=(phase,R,replicate,variant,curve)); point seed = integer + grid index",
        cost_definition="sum of actual .solve wall times + one median policy setup charge per workload",
        budget_rule="B_R=max_i(h_i+R*N*c_i); n_i,R=floor((B_R-h_i)/(R*c_i))",
        offline_certificate_included=False, max_depth=None, clipping=False, workers=1, protocol_deviations=[],
    )
    (output / "driver_at_execution.py").write_bytes(source.read_bytes())
    write_json(output / "metadata.json", metadata)

    states, setup_traces = [None] * len(VARIANTS), []
    for trial in range(SETUP_TRIALS):
        for execution_order, index in enumerate(permutation((3, trial), len(VARIANTS))):
            state, record = construct_policy(index)
            record.update(trial=trial, execution_order=execution_order)
            if states[index] is None:
                states[index] = state
            elif abs(state[1] - states[index][1]) > 1e-12:
                raise RuntimeError(f"Deterministic policy changed across setup trials: {VARIANTS[index]}")
            setup_traces.append(record)
    write_json(output / "setup_traces.json", setup_traces)
    setup = []
    for index, name in enumerate(VARIANTS):
        times = [row["setup_seconds"] for row in setup_traces if row["variant_index"] == index]
        setup.append(dict(variant=name, variant_index=index, rate=states[index][1],
                          setup_charge_seconds=float(np.median(times)), min_setup_seconds=min(times),
                          max_setup_seconds=max(times)))
    metadata["setup"] = setup
    write_json(output / "metadata.json", metadata)

    calibration = []
    for trial in range(CALIBRATION_TRIALS):
        for execution_order, index in enumerate(permutation((4, trial), len(VARIANTS))):
            seed, curve, seconds = solve_profile(states[index], 0, 1, trial, index, 0, SAMPLES)
            calibration.append(dict(variant=VARIANTS[index], variant_index=index, trial=trial,
                                    execution_order=execution_order, seed=seed, samples_per_point=SAMPLES,
                                    solve_seconds=seconds, sampler_reported_seconds=curve.seconds))
    write_json(output / "calibration.json", calibration)
    coefficients = [float(np.median([row["solve_seconds"] for row in calibration
                                    if row["variant_index"] == index])) / SAMPLES for index in range(len(VARIANTS))]
    budgets, allocations = {}, {}
    for reuse in REUSE_COUNTS:
        budget = max(row["setup_charge_seconds"] + reuse * SAMPLES * c for row, c in zip(setup, coefficients))
        counts = [math.floor((budget - row["setup_charge_seconds"]) / (reuse * c)) for row, c in zip(setup, coefficients)]
        if not all(n >= SAMPLES - 1 for n in counts):
            raise RuntimeError(f"Invalid predicted-budget allocation for R={reuse}")
        budgets[str(reuse)] = budget
        allocations[str(reuse)] = counts
    metadata.update(status="calibrated", calibration_coefficients=coefficients,
                    predicted_workload_budgets=budgets, budget_samples_per_point=allocations,
                    predicted_allocated_costs={str(reuse): [row["setup_charge_seconds"] + reuse * n * c
                                                          for row, n, c in zip(setup, allocations[str(reuse)], coefficients)]
                                               for reuse in REUSE_COUNTS},
                    calibration_solve_seconds=sum(row["solve_seconds"] for row in calibration),
                    repeated_setup_measurement_seconds=sum(row["setup_seconds"] for row in setup_traces))
    write_json(output / "metadata.json", metadata)
    print(f"Frozen rates: {[row['rate'] for row in setup]}", flush=True)
    print(f"Frozen predicted budgets: {budgets}; counts: {allocations}", flush=True)

    with (output / "profiles.jsonl").open("w") as profiles, (output / "workloads.jsonl").open("w") as workloads, (output / "points.csv").open("w", newline="") as points:
        writer = csv.DictWriter(points, fieldnames=["phase", "reuse", "replicate", "variant", "curve_index",
                                                      "x", "seed", "samples", "estimate", "exact", "error", "empirical_stderr"])
        writer.writeheader()
        for phase in (1, 2):
            for rep in range(REPLICATES):
                for execution_order, (reuse, index) in enumerate(workload_order(phase, rep)):
                    samples = SAMPLES if phase == 1 else allocations[str(reuse)][index]
                    workload_started = time.perf_counter()
                    curve_mses, solve_times, max_errors = [], [], []
                    for curve_index in range(reuse):
                        seed, curve, seconds = solve_profile(states[index], phase, reuse, rep, index, curve_index, samples)
                        exact = np.array([states[index][0].exact_solution(0., float(x)) for x in GRID])
                        errors = curve.values - exact
                        mse = float(np.dot(WEIGHTS, errors**2))
                        maximum = float(np.max(np.abs(errors)))
                        record = dict(phase=phase, reuse=reuse, replicate=rep, variant=VARIANTS[index],
                                      variant_index=index, curve_index=curve_index, workload_execution_order=execution_order,
                                      samples_per_point=samples, seed=seed, values=curve.values.tolist(), exact=exact.tolist(),
                                      errors=errors.tolist(), empirical_stderr=curve.stderr.tolist(),
                                      mse=mse, rmse=math.sqrt(mse), max_abs_error=maximum,
                                      solve_seconds=seconds, sampler_reported_seconds=curve.seconds, tree_diagnostics=curve.note)
                        profiles.write(json.dumps(record, allow_nan=False) + "\n")
                        profiles.flush()
                        for point_index, x in enumerate(GRID):
                            writer.writerow(dict(phase=phase, reuse=reuse, replicate=rep, variant=VARIANTS[index],
                                                 curve_index=curve_index, x=x, seed=seed + point_index, samples=samples,
                                                 estimate=curve.values[point_index], exact=exact[point_index], error=errors[point_index],
                                                 empirical_stderr=curve.stderr[point_index]))
                        points.flush()
                        curve_mses.append(mse)
                        solve_times.append(seconds)
                        max_errors.append(maximum)
                    elapsed = time.perf_counter() - workload_started
                    mse = math.fsum(curve_mses) / reuse
                    solve_seconds = math.fsum(solve_times)
                    total = solve_seconds + setup[index]["setup_charge_seconds"]
                    workloads.write(json.dumps(dict(
                        phase=phase, reuse=reuse, replicate=rep, variant=VARIANTS[index], variant_index=index,
                        execution_order=execution_order, samples_per_point=samples, requested_curves=reuse,
                        workload_mse=mse, workload_rmse=math.sqrt(mse), max_abs_error=max(max_errors),
                        solve_seconds=solve_seconds, setup_charge_seconds=setup[index]["setup_charge_seconds"],
                        accounted_total_seconds=total, per_curve_accounted_seconds=total / reuse,
                        elapsed_with_artifact_io_seconds=elapsed,
                    ), allow_nan=False) + "\n")
                    workloads.flush()
                print(f"Completed phase {phase}, workload replicate {rep + 1}/{REPLICATES}", flush=True)
    metadata.update(status="complete", benchmark_wall_seconds=time.perf_counter() - started,
                    completed_workloads=plan["evaluation_workloads"], completed_profiles=plan["evaluation_profiles"],
                    fixed_evaluation_trees=plan["fixed_evaluation_trees"],
                    budget_evaluation_trees=REPLICATES * len(GRID) * sum(reuse * sum(allocations[str(reuse)]) for reuse in REUSE_COUNTS))
    write_json(output / "metadata.json", metadata)
    summarize(output)
    print(f"Completed profile-efficiency artifacts: {output}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--run", action="store_true", help="Execute only after the coordinator's timing-ready signal")
    modes.add_argument("--check-plan", action="store_true", help="Audit seeds/counts without setup, calibration or evaluation")
    modes.add_argument("--report-only", action="store_true", help="Rebuild summaries/figures without drawing samples")
    parser.add_argument("--output-dir", type=Path, default=Path("docs/research/results/profile-efficiency"))
    parser.add_argument("--base-commit", default=None, help="Optional provenance supplied by the coordinator; no git commands are run")
    parser.add_argument("--timing-context", default="Coordinator confirmed other heavy research jobs had stopped before this run")
    arguments = parser.parse_args()
    if arguments.check_plan:
        print(json.dumps(verify_seed_plan(), indent=2))
    elif arguments.report_only:
        summarize(arguments.output_dir)
    else:
        try:
            run(arguments.output_dir, arguments.base_commit, arguments.timing_context)
        except Exception as error:
            if not isinstance(error, FileExistsError):
                arguments.output_dir.mkdir(parents=True, exist_ok=True)
                write_json(arguments.output_dir / "failure.json", dict(error_type=type(error).__name__, message=str(error)))
            raise
