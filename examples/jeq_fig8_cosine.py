"""Reproduce JEQ2023 Figure 8 (d = 1): fully nonlinear 4th-order example (5.10).

    du/dt + alpha du/dx + u - (u''/12)^2 + cos(pi u''''/24) = 0,
    u(T, x) = x^4 + x^3 + (3/8) x^2 + x/16 + 257/256,
    T = 0.04, alpha = 10, x in [-5, 5];  paper budget 1e5 samples/point.

NOTE: the quartic coefficients are the sympy-verified corrected ones; the
values printed in the paper (b = -36/47, c = 24b, d = 4b^2) do not solve
(5.10).  See parabolab/library.py.

This n = 4 example has the heaviest-tailed weights of the four (|M(f*)| = 23
after zero-tuple reduction); expect visibly larger error bars near the dip
of the quartic.  At the paper's 1e5 budget the worst grid point can sit
~4 stderr low because the rare large-weight branches are undersampled (and
stderr with them); at 4e5+ samples all points come within 2 stderr.
"""

import argparse
import pathlib

import numpy as np

from parabolab.library import cosine_fourth_order_1d
from parabolab.profiles import estimate_profile, plot_profile


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--samples", type=int, default=100_000,
                    help="MC samples per grid point (paper: 100000)")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    pde = cosine_fourth_order_1d()
    xs = np.linspace(-5.0, 5.0, 11)
    res = estimate_profile(pde, 0.0, xs, args.samples, seed=args.seed)
    res.print_table()

    out = pathlib.Path(__file__).with_name("jeq_fig8_cosine.png")
    plot_profile(res, pde, out,
                 "JEQ2023 Fig. 8: 4th-order cosine example (5.10), $u(0,x)$")
    print(f"figure saved to {out}")


if __name__ == "__main__":
    main()
