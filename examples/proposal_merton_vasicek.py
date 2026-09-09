"""Merton-Vasicek proposal optimization study.

Evaluates uniform vs pilot/frozen square-root proposals on the reduced Merton-Vasicek
HJB benchmark with killed continuations at depths 0, 1, and 2.
"""

from __future__ import annotations

import argparse
import csv
import math
import pathlib
import sys

# Ensure worktree package is used
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
import numpy as np

from parabolab import Id, default_rate, jcp_rate, sample_tree
from parabolab.library import merton_vasicek_reduced
from parabolab.proposals import (
    FrozenTupleProposal,
    estimate_tuple_contributions,
    sqrt_optimal_probabilities,
)
from parabolab.state_dependent import StateFNu


def run_experiment(
    pilot_samples: int = 2000,
    evaluation_samples: int = 10000,
) -> None:
    pde = merton_vasicek_reduced(T=0.05, consumption=False)
    state = np.array([0.0])
    exact_val = pde.exact_solution(0.0, state)

    target_code = StateFNu(
        1.0,
        beta=(0,),
        nu=(0, 0),
    )

    tuples = pde.mechanism.tuples(target_code)
    n_tuples = len(tuples)
    tuple_labels = [f"Z_{j}" for j in range(n_tuples)]

    rates = [default_rate(pde.T), jcp_rate(pde.T)]
    rate_names = {rates[0]: "rate=1.0", rates[1]: f"jcp_rate={rates[1]:.4g}"}

    pilot_seeds = [101, 102, 103]
    eval_seeds = [201, 202, 203, 204, 205]
    continuation_depths = [0, 1, 2]
    floor_mass = 0.05

    print("=== Merton-Vasicek Reduced Proposal Experiment ===")
    print(f"Horizon T = {pde.T}")
    print(f"Exact solution u(0, 0) = {exact_val:.6f}")
    print(f"Target code: {target_code}")
    print(f"Number of tuples for target code: {n_tuples}")
    print(f"Pilot samples per tuple: {pilot_samples}, Evaluation samples: {evaluation_samples}")

    csv_rows = []

    # Structure to hold summary metrics for plotting
    # (rate, method, depth) -> list of variance_times_mean_nodes
    metric_summary: dict[tuple[float, str, int], list[float]] = {}
    # (rate, depth) -> average proposal probabilities across pilot seeds
    prob_summary: dict[tuple[float, int], np.ndarray] = {}

    for rate in rates:
        r_name = rate_names[rate]
        print(f"\n--- Testing rate: {r_name} ---")

        # 1. Baseline: Uniform proposal
        uniform_probs = tuple(1.0 / n_tuples for _ in range(n_tuples))
        for e_seed in eval_seeds:
            rng = np.random.default_rng(e_seed)
            vals = np.empty(evaluation_samples, dtype=float)
            nodes = np.empty(evaluation_samples, dtype=int)

            for i in range(evaluation_samples):
                s = sample_tree(pde, 0.0, state, rng=rng, rate=rate, code=Id())
                vals[i] = s.value
                nodes[i] = s.n_nodes

            mean_val = float(np.mean(vals))
            second_mom = float(np.mean(vals**2))
            var_val = float(np.var(vals, ddof=1))
            max_abs_val = float(np.max(np.abs(vals)))
            mean_nodes_val = float(np.mean(nodes))
            max_nodes_val = int(np.max(nodes))
            cost_var = var_val * mean_nodes_val

            metric_summary.setdefault((rate, "Uniform", -1), []).append(cost_var)

            for j, t_label in enumerate(tuple_labels):
                csv_rows.append({
                    "pilot_seed": "none",
                    "evaluation_seed": e_seed,
                    "rate": rate,
                    "continuation_depth": "none",
                    "floor_mass": 0.0,
                    "tuple_label": t_label,
                    "proposal_probability": uniform_probs[j],
                    "estimate": mean_val,
                    "empirical_second_moment": second_mom,
                    "max_abs": max_abs_val,
                    "mean_nodes": mean_nodes_val,
                    "max_nodes": max_nodes_val,
                    "variance_times_mean_nodes": cost_var,
                })

        # 2. Pilot-frozen proposals for continuation depths 0, 1, 2
        for depth in continuation_depths:
            collected_q = []
            for p_seed in pilot_seeds:
                # Estimate tuple contributions for target_code
                pilot_res = estimate_tuple_contributions(
                    pde,
                    0.0,
                    state,
                    target_code,
                    n_samples=pilot_samples,
                    seed=p_seed,
                    rate=rate,
                    continuation_depth=depth,
                )
                q_opt = sqrt_optimal_probabilities(pilot_res.contributions, floor_mass=floor_mass)
                collected_q.append(q_opt)
                frozen_dict = {(1, target_code): tuple(q_opt)}
                frozen_prop = FrozenTupleProposal(frozen_dict)

                for e_seed in eval_seeds:
                    rng = np.random.default_rng(e_seed)
                    vals = np.empty(evaluation_samples, dtype=float)
                    nodes = np.empty(evaluation_samples, dtype=int)

                    for i in range(evaluation_samples):
                        s = sample_tree(
                            pde,
                            0.0,
                            state,
                            rng=rng,
                            rate=rate,
                            code=Id(),
                            tuple_proposal=frozen_prop,
                        )
                        vals[i] = s.value
                        nodes[i] = s.n_nodes

                    mean_val = float(np.mean(vals))
                    second_mom = float(np.mean(vals**2))
                    var_val = float(np.var(vals, ddof=1))
                    max_abs_val = float(np.max(np.abs(vals)))
                    mean_nodes_val = float(np.mean(nodes))
                    max_nodes_val = int(np.max(nodes))
                    cost_var = var_val * mean_nodes_val

                    metric_summary.setdefault((rate, f"Pilot-depth-{depth}", depth), []).append(cost_var)

                    for j, t_label in enumerate(tuple_labels):
                        csv_rows.append({
                            "pilot_seed": p_seed,
                            "evaluation_seed": e_seed,
                            "rate": rate,
                            "continuation_depth": depth,
                            "floor_mass": floor_mass,
                            "tuple_label": t_label,
                            "proposal_probability": float(q_opt[j]),
                            "estimate": mean_val,
                            "empirical_second_moment": second_mom,
                            "max_abs": max_abs_val,
                            "mean_nodes": mean_nodes_val,
                            "max_nodes": max_nodes_val,
                            "variance_times_mean_nodes": cost_var,
                        })

            avg_q = np.mean(collected_q, axis=0)
            prob_summary[(rate, depth)] = avg_q
            print(f"  Continuation depth {depth}: avg q = {np.round(avg_q, 4)}")

    # Write CSV
    out_dir = pathlib.Path(__file__).parent
    csv_path = out_dir / "proposal_merton_vasicek.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "pilot_seed",
            "evaluation_seed",
            "rate",
            "continuation_depth",
            "floor_mass",
            "tuple_label",
            "proposal_probability",
            "estimate",
            "empirical_second_moment",
            "max_abs",
            "mean_nodes",
            "max_nodes",
            "variance_times_mean_nodes",
        ])
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"\nWrote CSV: {csv_path}")

    # Plot results
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=150)

    # Panel 1: Cost-adjusted variance (variance * mean_nodes)
    categories = ["Uniform", "Depth 0", "Depth 1", "Depth 2"]
    x_pos = np.arange(len(categories))
    width = 0.35

    for idx, rate in enumerate(rates):
        means = [
            float(np.mean(metric_summary[(rate, "Uniform", -1)])),
            float(np.mean(metric_summary[(rate, "Pilot-depth-0", 0)])),
            float(np.mean(metric_summary[(rate, "Pilot-depth-1", 1)])),
            float(np.mean(metric_summary[(rate, "Pilot-depth-2", 2)])),
        ]
        stds = [
            float(np.std(metric_summary[(rate, "Uniform", -1)], ddof=1)),
            float(np.std(metric_summary[(rate, "Pilot-depth-0", 0)], ddof=1)),
            float(np.std(metric_summary[(rate, "Pilot-depth-1", 1)], ddof=1)),
            float(np.std(metric_summary[(rate, "Pilot-depth-2", 2)], ddof=1)),
        ]
        offset = (idx - 0.5) * width
        ax1.bar(
            x_pos + offset,
            means,
            width,
            yerr=stds,
            capsize=4,
            label=f"Rate = {rate:.3g}",
            alpha=0.85,
        )

    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(categories)
    ax1.set_ylabel("Variance × Expected Node Count")
    ax1.set_title("Computational Cost-Adjusted Variance")
    ax1.grid(True, axis="y", linestyle=":", alpha=0.6)
    ax1.legend(frameon=True)

    # Panel 2: Proposal probabilities by tuple for rate 1.0
    r0 = rates[0]
    t_idx = np.arange(n_tuples)
    w_sub = 0.2
    ax2.bar(t_idx - 1.5 * w_sub, [1.0 / n_tuples] * n_tuples, w_sub, label="Uniform (1/6)", color="gray", alpha=0.7)
    for d_idx, depth in enumerate(continuation_depths):
        q_vals = prob_summary[(r0, depth)]
        ax2.bar(t_idx + (d_idx - 0.5) * w_sub, q_vals, w_sub, label=f"Pilot depth {depth}")

    ax2.set_xticks(t_idx)
    ax2.set_xticklabels(tuple_labels)
    ax2.set_xlabel("Target Code Tuples")
    ax2.set_ylabel("Proposal Probability")
    ax2.set_title(f"Tuple Proposal Probabilities ({rate_names[r0]})")
    ax2.grid(True, axis="y", linestyle=":", alpha=0.6)
    ax2.legend(frameon=True)

    fig.suptitle(
        f"Reduced Merton-Vasicek (T={pde.T}): Proposal Optimization Benchmark",
        fontsize=13,
        fontweight="bold",
    )
    fig.text(
        0.5, 0.01,
        "Comparison of uniform vs pilot-frozen square-root proposals without sample-filtering.",
        ha="center", fontsize=9, style="italic", color="gray",
    )
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    png_path = out_dir / "proposal_merton_vasicek.png"
    plt.savefig(png_path)
    plt.close(fig)
    print(f"Wrote plot: {png_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot-samples", type=int, default=2000)
    parser.add_argument("--evaluation-samples", type=int, default=10000)
    args = parser.parse_args()

    run_experiment(
        pilot_samples=args.pilot_samples,
        evaluation_samples=args.evaluation_samples,
    )
