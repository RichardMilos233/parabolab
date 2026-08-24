"""Reproduce JEQ2023 Figure 8 (d = 1): fully nonlinear 4th-order cosine example (5.10).

    du/dt + alpha du/dx + u - (u''/12)^2 + cos(pi u''''/24) = 0,
    u(T, x) = x^4 + x^3 + (3/8) x^2 + x/16 + 257/256
"""
import argparse
import pathlib

import numpy as np

from parabolab import CodingTreeMC, compare
from parabolab.library import cosine_fourth_order_1d

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--samples", type=int, default=100_000, help="MC samples per grid point")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    pde = cosine_fourth_order_1d()
    grid = np.linspace(-5.0, 5.0, 11)
    mc = CodingTreeMC(n_samples=args.samples, seed=args.seed).solve(pde, grid)
    compare(pde, mc).table().plot(
        pathlib.Path(__file__).with_name("jeq_fig8_cosine.png"),
        "JEQ2023 Fig. 8: 4th-order cosine example (5.10), $u(0,x)$",
    )
