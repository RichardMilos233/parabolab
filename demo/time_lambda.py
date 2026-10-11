"""Plot full-tree second-moment boundaries for five supported flat cases."""

import argparse
from pathlib import Path

from parabolab import compare_time_lambda, sweep_time_lambda
from parabolab.library import allen_cahn_flat, binary_control_1d, fisher_kpp_1d


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Full-tree second-moment T-lambda boundaries")
    parser.add_argument("--lambda-min", type=float, default=0.01)
    parser.add_argument("--lambda-max", type=float, default=12.0)
    parser.add_argument("--n-points", type=int, default=401)
    parser.add_argument("--T", type=float, default=0.5, help="reference horizontal (default: 0.5)")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_suffix(".png"))
    args = parser.parse_args()

    common = dict(lambda_min=args.lambda_min, lambda_max=args.lambda_max,
                  n_points=args.n_points, reference_T=args.T)
    sweeps = [
        sweep_time_lambda(allen_cahn_flat(0.5), flat_terminal=0.5,
                          title="Allen–Cahn, flat phi = 0.5", **common),
        sweep_time_lambda(allen_cahn_flat(0.3), flat_terminal=0.3,
                          title="Allen–Cahn, flat phi = 0.3", **common),
        sweep_time_lambda(fisher_kpp_1d(phi0=0.5), flat_terminal=0.5,
                          title="Fisher–KPP, flat phi = 0.5", **common),
        sweep_time_lambda(fisher_kpp_1d(phi0=0.2), flat_terminal=0.2,
                          title="Fisher–KPP, flat phi = 0.2", **common),
        sweep_time_lambda(binary_control_1d(), title="Binary control, phi = 1", **common),
    ]
    compare_time_lambda(*sweeps).table().plot(args.output, save_individual=True)
    print(f"Saved combined and individual figures next to {args.output.resolve()}")
