"""Reproduce JEQ2023 Figure 1: Allen-Cahn (5.2) profiles in d dimensions.

    du/dt + (1/2) Lap u + u - u^3 = 0,
    exact (5.3): u(t,x) = -1/2 - tanh(3(T-t)/4 - sum x_i/(2 sqrt d))/2.

Authors' notebook settings (coding_trees, cells allen_cahn_jeeq_dim_*):
d = 5 with T = 0.5 and d = 100 with T = 0.3, profile along
x = (0, ..., 0, s), s in [-8, 8], 10 grid points, 1e5 MC samples/point.
Their published grid values (logs/final/plt_allen_cahn_jeeq_dim_*_coarse.csv)
are overlaid when available.

Usage: python jeq_fig1_allen_cahn_nd.py [--samples N] [--seed S]
       [--dims 5 100] [--jobs J]
"""

import argparse
import functools
import pathlib

import numpy as np

from parabolab.library import allen_cahn_nd
from parabolab.profiles import (
    estimate_profile,
    last_coordinate_embedding,
    plot_profile,
)

AUTHORS_LOGS = (pathlib.Path(__file__).resolve().parents[2]
                / "coding_trees" / "logs" / "final")
T_BY_DIM = {5: 0.5, 100: 0.3}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--samples", type=int, default=100_000,
                    help="MC samples per grid point (paper: 100000)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--dims", type=int, nargs="+", default=[5, 100])
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()

    for d in args.dims:
        T = T_BY_DIM.get(d, 0.5)
        factory = functools.partial(allen_cahn_nd, d=d, T=T)
        pde = factory()
        xs = np.linspace(-8.0, 8.0, 10)
        print(f"=== Allen-Cahn (5.2), d={d}, T={T} ===")
        res = estimate_profile(
            pde, 0.0, xs, args.samples, seed=args.seed,
            embed=last_coordinate_embedding(d),
            pde_factory=factory, n_jobs=args.jobs,
        )
        res.print_table()

        reference = None
        csv = AUTHORS_LOGS / f"plt_allen_cahn_jeeq_dim_{d}_coarse.csv"
        if csv.exists():
            data = np.loadtxt(csv, delimiter=",", skiprows=1)
            reference = (data[:, 0], data[:, 1], "authors' coding_trees")
            ours_interp = np.interp(data[:, 0], xs, res.estimates)
            print(f"max |ours - authors| on their grid: "
                  f"{np.max(np.abs(ours_interp - data[:, 1])):.4f}")

        out = pathlib.Path(__file__).with_name(
            f"jeq_fig1_allen_cahn_d{d}.png")
        plot_profile(res, pde, out,
                     f"JEQ2023 Fig. 1: Allen-Cahn (5.2), $d={d}$, $T={T}$",
                     embed=last_coordinate_embedding(d), reference=reference)
        print(f"figure saved to {out}\n")


if __name__ == "__main__":
    main()
