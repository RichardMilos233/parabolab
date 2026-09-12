#!/usr/bin/env python3
"""Small opt-in comparison of branching-rate and terminal tuple tuning."""

from __future__ import annotations

import argparse
import json
import platform
import time
from pathlib import Path

import numpy as np
import sympy as sp

from parabolab import (
    MomentQuadrature,
    TerminalTupleProposal,
    estimate,
    finite_depth_moment_derivatives_1d,
    library,
    optimize_exponential_rate_1d,
)


def positive_int(text: str) -> int:
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=positive_int, default=2000)
    parser.add_argument("--seed", type=int, default=20260912)
    parser.add_argument("--quadrature-order", type=positive_int, default=4)
    parser.add_argument("--depth", type=positive_int, default=2)
    parser.add_argument("--floor-mass", type=float, default=0.1)
    parser.add_argument(
        "--output", type=Path,
        help="optional JSON output path; stdout is always printed",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    T = 0.05
    t = 0.0
    x = 0.0
    bracket = (0.2, 2.0)
    pde = library.allen_cahn_wave_1d(T=T)
    quadrature = MomentQuadrature(
        time_order=args.quadrature_order,
        normal_order=args.quadrature_order,
    )
    terminal_proposal = TerminalTupleProposal(
        pde, floor_mass=args.floor_mass)

    def fixed_rate_diagnostic(rate: float, proposal) -> dict:
        started = time.perf_counter()
        moment = finite_depth_moment_derivatives_1d(
            pde, t, x, max_depth=args.depth, rate=rate,
            tuple_proposal=proposal, quadrature=quadrature,
        )
        return {
            "kind": "fixed-rate finite-depth evaluation",
            "rate": rate,
            "second_moment": moment.value,
            "depth": args.depth,
            "converged": None,
            "seconds": time.perf_counter() - started,
        }

    def optimized_rate_diagnostic(proposal) -> dict:
        started = time.perf_counter()
        result = optimize_exponential_rate_1d(
            pde, t, x, max_depth=args.depth, bracket=bracket,
            tuple_proposal=proposal, quadrature=quadrature,
        )
        return {
            "kind": "bracket-constrained finite-depth optimization",
            "rate": result.rate,
            "second_moment": result.second_moment,
            "depth": args.depth,
            "converged": result.converged,
            "iterations": result.iterations,
            "final_bracket": list(result.bracket),
            "seconds": time.perf_counter() - started,
        }

    tuning = {
        "default_rate_1_uniform": fixed_rate_diagnostic(1.0, None),
        "rate_only": optimized_rate_diagnostic(None),
        "q_only": fixed_rate_diagnostic(1.0, terminal_proposal),
        "combined": optimized_rate_diagnostic(terminal_proposal),
    }

    configurations = (
        ("default_rate_1_uniform", None),
        ("rate_only", None),
        ("q_only", terminal_proposal),
        ("combined", terminal_proposal),
    )
    seed_sequences = np.random.SeedSequence(args.seed).spawn(len(configurations))
    exact = float(pde.exact_solution(t, x))
    runs = []
    for (name, proposal), seed_sequence in zip(configurations, seed_sequences):
        seed_for_record = int(seed_sequence.generate_state(1, dtype=np.uint64)[0])
        result = estimate(
            pde, t, x, args.samples,
            rng=np.random.default_rng(seed_sequence),
            rate=tuning[name]["rate"],
            tuple_proposal=proposal,
        )
        empirical_variance = result.stderr**2 * result.n_samples
        runs.append({
            "name": name,
            "seed_state_uint64": seed_for_record,
            "seed_spawn_key": list(seed_sequence.spawn_key),
            "lambda": result.rate,
            "optimizer_second_moment": tuning[name]["second_moment"],
            "optimizer_depth": tuning[name]["depth"],
            "optimizer_converged": tuning[name]["converged"],
            "tuning_kind": tuning[name]["kind"],
            "tuning_seconds": tuning[name]["seconds"],
            "sampling_seconds": result.seconds,
            "empirical_mean": result.estimate,
            "stderr": result.stderr,
            "exact": exact,
            "empirical_variance_stderr_squared_times_n": empirical_variance,
            "mean_nodes": result.mean_nodes,
            "variance_times_mean_nodes": empirical_variance * result.mean_nodes,
        })

    payload = {
        "benchmark": "library.allen_cahn_wave_1d",
        "parameters": {
            "T": T,
            "t": t,
            "x": x,
            "samples_per_run": args.samples,
            "root_seed": args.seed,
            "evaluation_rng": (
                "default_rng(SeedSequence(root_seed, spawn_key=seed_spawn_key)); "
                "seed_state_uint64 is a stream fingerprint, not the integer seed "
                "passed to default_rng"
            ),
            "quadrature_order": args.quadrature_order,
            "optimizer_depth": args.depth,
            "optimizer_bracket": list(bracket),
            "proposal_floor_mass": args.floor_mass,
            "evaluation_max_depth": None,
        },
        "versions": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "sympy": sp.__version__,
        },
        "runs": runs,
        "limitations": [
            "Rate selection minimizes a finite-depth quadrature objective; it is uncertified for the unrestricted tree used in evaluation.",
            "TerminalTupleProposal is a parent-state heuristic, not a conditional child-moment oracle.",
            "Empirical variance and timing are one-run diagnostics, not confidence certificates or universal performance claims.",
            "No full-tree moment bound is certified by this example.",
        ],
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output is not None:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
