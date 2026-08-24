"""Reproduce JEQ2023 Figure 9 (d = 1): fully nonlinear 3rd-order log example (5.11).

    du/dt + alpha du/dx + log((u'')^2 + (u''')^2) = 0,  u(T, x) = cos(x),
    T = 0.02, alpha = 5, x in [-pi, pi];  paper budget 1e5 samples/point.
"""

import argparse
import math
import pathlib

import numpy as np

from parabolab import CodingTreeMC, compare
from parabolab.library import log_third_order_1d


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--samples", type=int, default=100_000,
                    help="MC samples per grid point (paper: 100000)")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    pde = log_third_order_1d()
    grid = np.linspace(-math.pi, math.pi, 11)
    mc = CodingTreeMC(n_samples=args.samples, seed=args.seed).solve(pde, grid)
    compare(pde, mc).table().plot(
        pathlib.Path(__file__).with_name("jeq_fig9_log.png"),
        "JEQ2023 Fig. 9: 3rd-order log example (5.11), $u(0,x)$")


if __name__ == "__main__":
    main()
