"""Plot empirical full-tree MC variance grids and theoretical T-lambda boundaries."""

import argparse
from pathlib import Path

from parabolab import (
    TimeLambdaMCComparison,
    compare_time_lambda,
    compare_time_lambda_mc,
    sweep_time_lambda,
    sweep_time_lambda_mc,
)
from parabolab.library import allen_cahn_flat, binary_control_1d, fisher_kpp_1d


def _factories():
    return [
        (lambda T: allen_cahn_flat(0.5, T=T), 0.5, "Allen–Cahn, flat phi = 0.5"),
        (lambda T: allen_cahn_flat(0.3, T=T), 0.3, "Allen–Cahn, flat phi = 0.3"),
        (lambda T: fisher_kpp_1d(T=T, phi0=0.5), 0.5, "Fisher–KPP, flat phi = 0.5"),
        (lambda T: fisher_kpp_1d(T=T, phi0=0.2), 0.2, "Fisher–KPP, flat phi = 0.2"),
        (lambda T: binary_control_1d(T=T), None, "Binary control, phi = 1"),
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Full-tree MC variance and T-lambda boundaries")
    parser.add_argument("--lambda-min", type=float, default=0.01)
    parser.add_argument("--lambda-max", type=float, default=12.0)
    parser.add_argument("--n-points", type=int, default=401,
                        help="points on the theoretical boundary (default: 401)")
    parser.add_argument("--T", type=float, default=0.5,
                        help="reference horizontal (default: 0.5)")
    parser.add_argument("--mc-lambda-points", type=int, default=12)
    parser.add_argument("--mc-T-points", type=int, default=10)
    parser.add_argument("--T-min", type=float, default=0.05)
    parser.add_argument("--T-max", type=float, default=1.3)
    parser.add_argument("--samples-per-cell", type=int, default=128)
    parser.add_argument("--seed", type=int, default=20261012)
    parser.add_argument("--max-nodes", type=int, default=5_000,
                        help="per-tree node guard; 0 disables (default: 5000)")
    parser.add_argument("--max-cell-nodes", type=int, default=100_000,
                        help="per-cell total-node guard; 0 disables (default: 100000)")
    parser.add_argument("--mc-data", type=Path,
                        default=Path(__file__).with_name("time_lambda_mc.npz"))
    parser.add_argument("--load-mc", type=Path,
                        help="redraw a combined or per-case checkpoint NPZ without sampling")
    parser.add_argument("--no-mc", action="store_true",
                        help="draw the original theory-only figure")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_suffix(".png"))
    args = parser.parse_args()

    if args.no_mc and args.load_mc is not None:
        parser.error("--no-mc and --load-mc cannot be used together")

    factories = _factories()
    if args.no_mc:
        common = dict(lambda_min=args.lambda_min, lambda_max=args.lambda_max,
                      n_points=args.n_points, reference_T=args.T)
        sweeps = [
            sweep_time_lambda(factory(args.T), flat_terminal=flat, title=title, **common)
            for factory, flat, title in factories
        ]
        compare_time_lambda(*sweeps).table().plot(args.output, save_individual=True)
        print(f"Saved theory-only combined and individual figures next to {args.output.resolve()}")
    else:
        if args.load_mc is not None:
            comparison = TimeLambdaMCComparison.load(args.load_mc)
            print(f"Loaded MC grid without resampling: {args.load_mc.resolve()}")
        else:
            max_nodes = None if args.max_nodes == 0 else args.max_nodes
            max_cell_nodes = None if args.max_cell_nodes == 0 else args.max_cell_nodes
            sweeps = []
            for i, (factory, flat, title) in enumerate(factories, start=1):
                checkpoint = args.mc_data.with_name(f"{args.mc_data.stem}_case{i}.npz")
                sweeps.append(sweep_time_lambda_mc(
                    factory, flat_terminal=flat, title=title,
                    lambda_min=args.lambda_min, lambda_max=args.lambda_max,
                    n_lambda=args.mc_lambda_points,
                    T_min=args.T_min, T_max=args.T_max, n_T=args.mc_T_points,
                    n_samples=args.samples_per_cell,
                    seed=args.seed + (i - 1) * 1_000_003,
                    max_nodes=max_nodes, max_cell_nodes=max_cell_nodes,
                    reference_T=args.T, theory_points=args.n_points,
                    checkpoint_path=checkpoint,
                ))
            comparison = compare_time_lambda_mc(*sweeps).save(args.mc_data)
            print(f"Saved MC grid data to: {args.mc_data.resolve()}")
        comparison.plot(args.output, save_individual=True)
        print(f"Saved MC heatmap and individual figures next to {args.output.resolve()}")
