"""Reproduce JEQ2023 Figure 7 (d = 1): quasilinear tan example (5.8).

    du/dt + alpha du/dx + u''/(1 + u^2) - 2u = 0,  u(T, x) = tan(x),
    T = 0.01, alpha = 10, x in [-pi/4, pi/4];  paper budget 1e6 samples/point.

The default here is 1e5 samples (about 10 s); pass --samples 1000000 for the
full paper budget (about 1-2 min in pure Python).
"""

import argparse
import math
import pathlib

import numpy as np

from parabolab import CodingTreeMC, compare
from parabolab.library import quasilinear_tan_1d


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--samples", type=int, default=100_000,
                    help="MC samples per grid point (paper: 1000000)")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    pde = quasilinear_tan_1d()
    grid = np.linspace(-math.pi / 4, math.pi / 4, 11)
    mc = CodingTreeMC(n_samples=args.samples, seed=args.seed).solve(pde, grid)
    compare(pde, mc).table().plot(
        pathlib.Path(__file__).with_name("jeq_fig7_tan.png"),
        "JEQ2023 Fig. 7: quasilinear tan example (5.8), $u(0,x)$")
