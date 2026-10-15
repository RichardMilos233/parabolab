"""Observed full-tree MC variance over a T-lambda grid for four flat PDEs."""

import argparse
from functools import partial
from pathlib import Path

from parabolab import compare_time_lambda_mc, sweep_time_lambda_mc
from parabolab.library import allen_cahn_flat, fisher_kpp_1d


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Full-tree MC T-lambda variance heatmaps")
    parser.add_argument("--mc-lambda-points", type=int, default=12)
    parser.add_argument("--mc-T-points", type=int, default=10)
    parser.add_argument("--samples-per-cell", type=int, default=128)
    parser.add_argument("--sampler", choices=("flat", "tree"), default="flat",
                        help="flat: vectorized flat-data sampler (same law of H); "
                             "tree: original recursive sample_tree")
    parser.add_argument("--n-jobs", type=int, default=1,
                        help="worker processes (1 = serial)")
    parser.add_argument("--chunk-size", type=int, default=None,
                        help="split each cell into seeded chunks of this many trees "
                             "(default: one chunk per cell, at most 100000 for flat)")
    parser.add_argument("--max-nodes", type=int, default=None,
                        help="per-tree node limit; a cell with any larger tree is "
                             "marked invalid (default: no limit)")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent,
                        help="where the NPZ data and PNG figures are written")
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
        sampler=args.sampler,
        n_jobs=args.n_jobs,
        chunk_size=args.chunk_size,
        max_nodes=args.max_nodes,
    )
    cases = [
        # Picklable factories (pde_factory(T)) so worker processes can rebuild PDEs.
        (partial(allen_cahn_flat, 0.5), 0.5, "Allen–Cahn, flat phi = 0.5"),
        (partial(allen_cahn_flat, 0.3), 0.3, "Allen–Cahn, flat phi = 0.3"),
        (partial(fisher_kpp_1d, phi0=0.5), 0.5, "Fisher–KPP, flat phi = 0.5"),
        (partial(fisher_kpp_1d, phi0=0.2), 0.2, "Fisher–KPP, flat phi = 0.2"),
    ]

    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    data_path = out_dir / "time_lambda_mc.npz"
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
    comparison.plot(out_dir / "time_lambda.png", save_individual=True)
    comparison.plot(out_dir / "time_lambda_max_share.png", statistic="max_share")
    comparison.plot(out_dir / "time_lambda_batch_cv.png", statistic="batch_cv")
    print(f"Saved MC data to: {data_path.resolve()}")
    print(f"Saved variance and diagnostic heatmaps in: {out_dir.resolve()}")
