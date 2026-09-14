"""Replicated Allen–Cahn sampling study with frozen independent cost calibration.

Protocol: docs/research/results/rate-cost-protocol.md. Run from the repository
root. This research driver reuses CodingTreeMC.solve without sampler changes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import subprocess
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from parabolab import CodingTreeMC, MomentQuadrature, TerminalTupleProposal
from parabolab.library import allen_cahn_wave_1d
from parabolab.rate_optimization import optimize_exponential_rate_1d
from parabolab.tree import jcp_rate


GRID = np.array([-2., -1., 0., 1., 2.])
HORIZON = 0.05
SAMPLES = 10000
REPLICATES = 20
CALIBRATION_REPLICATES = 3
ENTROPY = 202609142
PROTOCOL = Path("docs/research/results/rate-cost-protocol.md")
VARIANTS = (
    "default_uniform", "jcp_uniform", "short_time_uniform",
    "selected_uniform", "default_terminal", "selected_terminal",
)
LABELS = ("Default", "JCP", "Short time", "Selected rate", "Terminal q", "Selected + q")


def seed_for(phase, replicate, variant):
    sequence = np.random.SeedSequence(ENTROPY, spawn_key=(phase, replicate, variant))
    return int(sequence.generate_state(1, dtype=np.uint64)[0])


def order_for(phase, replicate):
    sequence = np.random.SeedSequence(ENTROPY, spawn_key=(3, phase, replicate))
    return np.random.default_rng(sequence).permutation(len(VARIANTS)).tolist()


def verify_seed_plan():
    seeds = [seed_for(phase, rep, variant) + point
             for phase, count in ((0, CALIBRATION_REPLICATES), (1, REPLICATES),
                                  (2, REPLICATES))
             for rep in range(count) for variant in range(len(VARIANTS))
             for point in range(len(GRID))]
    if len(set(seeds)) != len(seeds):
        raise RuntimeError("Point seed collision in the predeclared plan")


def setup_variant(index):
    started = time.perf_counter()
    pde = allen_cahn_wave_1d(T=HORIZON)
    pde_seconds = time.perf_counter() - started
    proposal_started = time.perf_counter()
    proposal = TerminalTupleProposal(pde, floor_mass=0.1) if index in (4, 5) else None
    proposal_seconds = time.perf_counter() - proposal_started
    tuning_started = time.perf_counter()
    optimizer_record = None
    if index in (3, 5):
        result = optimize_exponential_rate_1d(
            pde, 0., 0., max_depth=2, bracket=(0.2, 2.0), tol=1e-5,
            quadrature=MomentQuadrature(time_order=4, normal_order=4),
            tuple_proposal=proposal,
        )
        if not result.converged:
            raise RuntimeError(f"Rate selector did not converge for {VARIANTS[index]}")
        rate = result.rate
        optimizer_record = dict(second_moment=result.second_moment,
                                d_rate=result.d_rate, iterations=result.iterations,
                                bracket=list(result.bracket), converged=result.converged)
    elif index == 1:
        rate = jcp_rate(HORIZON)
    elif index == 2:
        terminal = pde.phi(0.)
        rate = abs(pde.f(terminal)) / abs(terminal)
    else:
        rate = 1.0
    tuning_seconds = time.perf_counter() - tuning_started
    setup_seconds = time.perf_counter() - started
    record = dict(variant=VARIANTS[index], index=index, rate=rate,
                  proposal_floor=0.1 if proposal is not None else None,
                  pde_seconds=pde_seconds, proposal_setup_seconds=proposal_seconds,
                  tuning_seconds=tuning_seconds, setup_seconds=setup_seconds,
                  optimizer=optimizer_record)
    return (pde, proposal, rate), record


def solve_profile(state, phase, replicate, index, samples):
    pde, proposal, rate = state
    seed = seed_for(phase, replicate, index)
    solver = CodingTreeMC(n_samples=samples, seed=seed, rate=rate,
                          tuple_proposal=proposal, label=VARIANTS[index], n_jobs=1)
    started = time.perf_counter()
    curve = solver.solve(pde, GRID, t=0.)
    seconds = time.perf_counter() - started
    if not (np.isfinite(curve.values).all() and np.isfinite(curve.stderr).all()):
        raise RuntimeError(f"Nonfinite curve for {VARIANTS[index]}, phase={phase}, rep={replicate}")
    return seed, curve, seconds


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def summarize(output_dir):
    metadata = json.loads((output_dir / "metadata.json").read_text())
    rows = [json.loads(line) for line in (output_dir / "profiles.jsonl").read_text().splitlines()]
    summary = []
    for phase in (1, 2):
        for index, name in enumerate(VARIANTS):
            selected = [row for row in rows if row["phase"] == phase and row["variant"] == name]
            if len(selected) != REPLICATES:
                raise RuntimeError(f"Expected {REPLICATES} completed curves for {phase}/{name}")
            rmse = np.array([row["rmse"] for row in selected])
            errors = np.array([row["errors"] for row in selected])
            costs = np.array([row["total_seconds"] for row in selected])
            sampling = np.array([row["solve_seconds"] for row in selected])
            summary.append(dict(
                phase=phase, variant=name, rate=metadata["setup"][index]["rate"],
                samples_per_point=selected[0]["samples_per_point"],
                rms_rmse=float(np.sqrt(np.mean(rmse**2))), median_rmse=float(np.median(rmse)),
                q25_rmse=float(np.quantile(rmse, .25)), q75_rmse=float(np.quantile(rmse, .75)),
                min_rmse=float(rmse.min()), max_rmse=float(rmse.max()),
                median_total_seconds=float(np.median(costs)), min_total_seconds=float(costs.min()),
                max_total_seconds=float(costs.max()), median_solve_seconds=float(np.median(sampling)),
                pointwise_rmse=np.sqrt(np.mean(errors**2, axis=0)).tolist(),
                pointwise_mean_error=np.mean(errors, axis=0).tolist(),
            ))
    write_json(output_dir / "summary.json", summary)
    scalar_fields = [field for field in summary[0] if not field.startswith("pointwise")]
    with (output_dir / "summary.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=scalar_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(summary)

    colors = plt.get_cmap("tab10").colors
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    for row_index, phase in enumerate((1, 2)):
        distributions = [[row["rmse"] for row in rows
                          if row["phase"] == phase and row["variant"] == name]
                         for name in VARIANTS]
        axes[row_index, 0].boxplot(distributions, tick_labels=LABELS, showfliers=False)
        for index, values in enumerate(distributions):
            jitter = np.linspace(-.15, .15, len(values))
            axes[row_index, 0].scatter(index + 1 + jitter, values, color=colors[index],
                                       s=16, alpha=.7)
        axes[row_index, 0].set_ylabel("Profile RMSE (all 20 replicates)")
        axes[row_index, 0].tick_params(axis="x", rotation=20)
        axes[row_index, 0].set_title("Fixed N=10,000 per point" if phase == 1
                                      else "Calibrated expected total budget")
        for index, name in enumerate(VARIANTS):
            selected = [row for row in rows if row["phase"] == phase and row["variant"] == name]
            axes[row_index, 1].scatter([row["total_seconds"] for row in selected],
                                       [row["rmse"] for row in selected], color=colors[index],
                                       label=LABELS[index], alpha=.65, s=20)
        axes[row_index, 1].set_xlabel("Realized solve seconds + one-time setup charge")
        axes[row_index, 1].set_ylabel("Profile RMSE")
        axes[row_index, 1].legend(fontsize=8)
        for axis in axes[row_index]:
            axis.grid(True, alpha=.25)
    fig.suptitle("Allen–Cahn wave, T=0.05; rates tuned at x=0, evaluated on five points")
    fig.tight_layout()
    fig.savefig(output_dir / "rmse_cost.png", dpi=180)
    plt.close(fig)
    return summary


def run(output_dir):
    if (output_dir / "metadata.json").exists():
        raise FileExistsError("Results already exist; use --report-only or a new output directory")
    output_dir.mkdir(parents=True, exist_ok=True)
    verify_seed_plan()
    started = time.perf_counter()
    source_paths = [PROTOCOL, Path(__file__), Path("parabolab/rate_optimization.py"),
                    Path("parabolab/tree.py"), Path("parabolab/proposals.py"),
                    Path("parabolab/solve.py"), Path("parabolab/profiles.py"), Path("parabolab/mc.py")]
    metadata = dict(
        status="started", date="2026-09-14", python=platform.python_version(),
        command=[sys.executable, *sys.argv],
        numpy=np.__version__, platform=platform.platform(),
        base_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        branch=subprocess.check_output(["git", "branch", "--show-current"], text=True).strip(),
        source_sha256={str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in source_paths},
        protocol=str(PROTOCOL), entropy=ENTROPY, grid=GRID.tolist(), horizon=HORIZON,
        replicates=REPLICATES, calibration_replicates=CALIBRATION_REPLICATES,
        fixed_samples_per_point=SAMPLES, variants=list(VARIANTS),
        exact_solution="-0.5 - 0.5*tanh(0.75*(T-t)-0.5*x)",
        seed_definition="uint64 SeedSequence(entropy, spawn_key=(phase,replicate,variant)); point seed = integer + grid index",
        cutoff=None, clipping=False, workers=1, protocol_deviations=[],
    )
    states, setup = [], []
    for index in range(len(VARIANTS)):
        state, record = setup_variant(index)
        states.append(state)
        setup.append(record)
    metadata["setup"] = setup
    write_json(output_dir / "metadata.json", metadata)
    calibration = []
    for rep in range(CALIBRATION_REPLICATES):
        for order_index, index in enumerate(order_for(0, rep)):
            seed, curve, seconds = solve_profile(states[index], 0, rep, index, SAMPLES)
            calibration.append(dict(variant=VARIANTS[index], variant_index=index, replicate=rep,
                                    execution_order=order_index, seed=seed, samples_per_point=SAMPLES,
                                    solve_seconds=seconds, sampler_reported_seconds=curve.seconds))
    write_json(output_dir / "calibration.json", calibration)
    coefficients = [float(np.median([row["solve_seconds"] for row in calibration
                                    if row["variant_index"] == index])) / SAMPLES
                    for index in range(len(VARIANTS))]
    target = max(row["setup_seconds"] + SAMPLES * coefficient
                 for row, coefficient in zip(setup, coefficients))
    allocations = [int(math.floor((target - row["setup_seconds"]) / coefficient))
                   for row, coefficient in zip(setup, coefficients)]
    if not all(value >= SAMPLES - 1 for value in allocations):
        raise RuntimeError("Invalid independently calibrated allocation")
    metadata.update(status="calibrated", calibration_seconds=sum(row["solve_seconds"] for row in calibration),
                    expected_budget_seconds=target, calibration_seconds_per_grid_sample=coefficients,
                    budget_samples_per_point=allocations,
                    predicted_budget_seconds=[row["setup_seconds"] + n * coefficient
                                              for row, n, coefficient in zip(setup, allocations, coefficients)])
    write_json(output_dir / "metadata.json", metadata)
    print(f"Frozen allocations: {allocations}; common expected total budget {target:.6f}s", flush=True)

    with (output_dir / "profiles.jsonl").open("w") as profiles, (output_dir / "points.csv").open("w", newline="") as points:
        writer = csv.DictWriter(points, fieldnames=["phase", "variant", "replicate", "x", "seed",
                                                      "samples", "estimate", "exact", "error", "empirical_stderr"])
        writer.writeheader()
        for phase in (1, 2):
            for rep in range(REPLICATES):
                for order_index, index in enumerate(order_for(phase, rep)):
                    samples = SAMPLES if phase == 1 else allocations[index]
                    seed, curve, seconds = solve_profile(states[index], phase, rep, index, samples)
                    exact = np.array([states[index][0].exact_solution(0., float(x)) for x in GRID])
                    errors = curve.values - exact
                    record = dict(phase=phase, variant=VARIANTS[index], variant_index=index, replicate=rep,
                                  execution_order=order_index, seed=seed, samples_per_point=samples,
                                  values=curve.values.tolist(), exact=exact.tolist(), errors=errors.tolist(),
                                  empirical_stderr=curve.stderr.tolist(), rmse=float(np.sqrt(np.mean(errors**2))),
                                  max_abs_error=float(np.max(np.abs(errors))), solve_seconds=seconds,
                                  sampler_reported_seconds=curve.seconds, setup_charge_seconds=setup[index]["setup_seconds"],
                                  total_seconds=seconds + setup[index]["setup_seconds"], tree_diagnostics=curve.note)
                    profiles.write(json.dumps(record, allow_nan=False) + "\n")
                    profiles.flush()
                    for point_index, x in enumerate(GRID):
                        writer.writerow(dict(phase=phase, variant=VARIANTS[index], replicate=rep, x=x,
                                             seed=seed + point_index, samples=samples,
                                             estimate=curve.values[point_index], exact=exact[point_index],
                                             error=errors[point_index], empirical_stderr=curve.stderr[point_index]))
                    points.flush()
                print(f"Completed phase {phase}, replicate {rep + 1}/{REPLICATES}", flush=True)
    metadata.update(status="complete", benchmark_wall_seconds=time.perf_counter() - started,
                    completed_profiles=2 * REPLICATES * len(VARIANTS),
                    fixed_evaluation_trees=REPLICATES * len(VARIANTS) * len(GRID) * SAMPLES,
                    budget_evaluation_trees=REPLICATES * len(GRID) * sum(allocations))
    write_json(output_dir / "metadata.json", metadata)
    summarize(output_dir)
    print(f"Completed results in {output_dir}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("docs/research/results/rate-cost-benchmark"))
    parser.add_argument("--report-only", action="store_true", help="Rebuild summaries and figure without sampling")
    arguments = parser.parse_args()
    if arguments.report_only:
        summarize(arguments.output_dir)
    else:
        try:
            run(arguments.output_dir)
        except Exception as error:
            if not isinstance(error, FileExistsError):
                arguments.output_dir.mkdir(parents=True, exist_ok=True)
                write_json(arguments.output_dir / "failure.json",
                           dict(error_type=type(error).__name__, message=str(error)))
            raise
