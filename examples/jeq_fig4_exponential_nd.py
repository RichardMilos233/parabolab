"""Reproduce JEQ2023 Figures 4/5: exponential gradient nonlinearity (5.5).

    du/dt + (alpha/d) sum_i du/dx_i + (1/2) Lap u
          + d e^{-u} (1 - 2 e^{-u}) = 0,
    exact (5.6): u(t,x) = log(1 + (alpha (T-t) + sum x_i)^2),
    T = 0.05, alpha = 10, d = 5 and 10 (Fig 4 = coding trees; Fig 5 is the
    multilevel Picard comparison, not reproduced here).

Authors' settings: profile along x = (0, ..., 0, s), s in [-4, 4],
10 grid points, 1e5 MC samples/point; their published values
(logs/final/plt_exponential_nonlinearity_jeeq_dim_*_coarse.csv) overlaid.

Usage: python jeq_fig4_exponential_nd.py [--samples N] [--seed S]
       [--dims 5 10] [--jobs J]
"""

import argparse
import functools
import pathlib

import numpy as np

from parabolab.library import exponential_gradient_nd
from parabolab.profiles import (
    estimate_profile,
    last_coordinate_embedding,
    plot_profile,
)

AUTHORS_LOGS = (pathlib.Path(__file__).resolve().parents[2]
                / "coding_trees" / "logs" / "final")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--samples", type=int, default=100_000,
                    help="MC samples per grid point (paper: 100000)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--dims", type=int, nargs="+", default=[5, 10])
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()

    for d in args.dims:
        factory = functools.partial(exponential_gradient_nd, d=d)
        pde = factory()
        xs = np.linspace(-4.0, 4.0, 10)
        print(f"=== exponential nonlinearity (5.5), d={d}, T={pde.T} ===")
        res = estimate_profile(
            pde, 0.0, xs, args.samples, seed=args.seed,
            embed=last_coordinate_embedding(d),
            pde_factory=factory, n_jobs=args.jobs,
        )
        res.print_table()

        reference = None
        csv = (AUTHORS_LOGS /
               f"plt_exponential_nonlinearity_jeeq_dim_{d}_coarse.csv")
        if csv.exists():
            data = np.loadtxt(csv, delimiter=",", skiprows=1)
            reference = (data[:, 0], data[:, 1], "authors' coding_trees")
            ours_interp = np.interp(data[:, 0], xs, res.estimates)
            print(f"max |ours - authors| on their grid: "
                  f"{np.max(np.abs(ours_interp - data[:, 1])):.4f}")

        out = pathlib.Path(__file__).with_name(
            f"jeq_fig4_exponential_d{d}.png")
        plot_profile(res, pde, out,
                     f"JEQ2023 Fig. 4: exp nonlinearity (5.5), $d={d}$",
                     embed=last_coordinate_embedding(d), reference=reference)
        print(f"figure saved to {out}\n")


if __name__ == "__main__":
    main()
