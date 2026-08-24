"""Variance vs branching rate for the Dym example (JEQ Fig. 6 setup).

The Dym terminal condition (6x)^{2/3} has factorially growing high-order
derivatives, so deep dx-chains produce enormous rare samples; the second
moment of H is (near-)infinite at rate 1 and sample means do not stabilize.
Raising the Exp rate lambda shrinks each branch weight |M(c)| e^{lambda tau}
/ lambda, which tames the tails at the cost of more (cheaper) branches.

Usage: python rate_study_dym.py [--samples N]
"""

import argparse

from parabolab import estimate
from parabolab.library import dym_1d
from parabolab.tree import jcp_rate


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--samples", type=int, default=100_000)
    args = ap.parse_args()

    pde = dym_1d()
    rates = [0.1, 0.25, 0.5, 1.0, 2.0, jcp_rate(pde.T)]
    xs = [1.2, 1.5]
    seeds = [0, 1, 2]
    for x in xs:
        exact = pde.exact_solution(0.0, x)
        print(f"x = {x}, exact = {exact:.6f}, N = {args.samples}")
        for rate in rates:
            line = f"  rate {rate:6.2f}: "
            for seed in seeds:
                r = estimate(pde, 0.0, x, args.samples, seed=seed, rate=rate)
                line += f"{r.estimate:+9.3f} +/-{r.stderr:8.3f}  "
            print(line)
