"""Reproduce JEQ2023 Figure 6 (d = 1): Dym equation (5.7).

    du/dt + u^3 d^3u/dx^3 = 0,  u(T, x) = (6x)^{2/3},
    T = 0.01, alpha = 2, x in [1, 2];  paper budget 1e5 samples/point.

Usage: python jeq_fig6_dym.py [--samples N] [--seed S]
"""

import argparse
import pathlib

import numpy as np

from parabolab import CodingTreeMC, compare
from parabolab.library import dym_1d


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--samples", type=int, default=100_000,
                    help="MC samples per grid point (paper: 100000)")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    pde = dym_1d()
    grid = np.linspace(1.0, 2.0, 11)
    mc = CodingTreeMC(n_samples=args.samples, seed=args.seed).solve(pde, grid)
    compare(pde, mc).table().plot(
        pathlib.Path(__file__).with_name("jeq_fig6_dym.png"),
        "JEQ2023 Fig. 6: Dym equation (5.7), $u(0,x)$")


if __name__ == "__main__":
    main()
