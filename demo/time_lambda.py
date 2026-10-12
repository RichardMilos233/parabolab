"""Observed full-tree MC variance over a T-lambda grid for five flat PDEs."""

import argparse
from pathlib import Path

from parabolab import compare_time_lambda_mc, sweep_time_lambda_mc
from parabolab.library import allen_cahn_flat, binary_control_1d, fisher_kpp_1d


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Full-tree MC T-lambda variance heatmaps")
    parser.add_argument("--mc-lambda-points", type=int, default=12)
    parser.add_argument("--mc-T-points", type=int, default=10)
    parser.add_argument("--samples-per-cell", type=int, default=128)
    args = parser.parse_args()

    common = dict(
        lambda_min=0.01,
        lambda_max=12.0,
        T_min=0.05,
        T_max=1.3,
        reference_T=0.5,
        theory_points=401,
        n_lambda=args.mc_lambda_points,
        n_T=args.mc_T_points,
        n_samples=args.samples_per_cell,
    )
    cases = [
        (lambda T: allen_cahn_flat(0.5, T=T), 0.5, "Allen–Cahn, flat phi = 0.5"),
        (lambda T: allen_cahn_flat(0.3, T=T), 0.3, "Allen–Cahn, flat phi = 0.3"),
        (lambda T: fisher_kpp_1d(T=T, phi0=0.5), 0.5, "Fisher–KPP, flat phi = 0.5"),
        (lambda T: fisher_kpp_1d(T=T, phi0=0.2), 0.2, "Fisher–KPP, flat phi = 0.2"),
        (lambda T: binary_control_1d(T=T), None, "Binary control, phi = 1"),
    ]

    data_path = Path(__file__).with_name("time_lambda_mc.npz")
    sweeps = []
    for i, (factory, flat_terminal, title) in enumerate(cases, start=1):
        sweeps.append(sweep_time_lambda_mc(
            factory,
            flat_terminal=flat_terminal,
            title=title,
            seed=20261012 + (i - 1) * 1_000_003,
            checkpoint_path=data_path.with_name(f"{data_path.stem}_case{i}.npz"),
            **common,
        ))

    comparison = compare_time_lambda_mc(*sweeps).save(data_path)
    output = Path(__file__).with_suffix(".png")
    comparison.plot(output, save_individual=True)
    print(f"Saved MC data to: {data_path.resolve()}")
    print(f"Saved combined and individual heatmaps next to: {output.resolve()}")
