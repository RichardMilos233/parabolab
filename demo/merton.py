"""Merton HJB, d = 1 (JCP2024 eq. (4.6), Table 5) -- fully nonlinear f."""
import sys
from functools import partial
from pathlib import Path

import numpy as np

from parabolab import CodingTreeMC, compare
from parabolab.library import merton_hjb

# Deep branching trains a network; off by default, --deep adds it (about
# 22 s on a laptop CPU at the paper's own budget).  The other two baselines
# are NOT offered here -- see the note at the bottom of the file.
DEEP = "--deep" in sys.argv


def main():
    # u_t + (1/2) u_xx + f(u, u_x, u_xx) = 0  with
    #   f = -u_xx/2 - (mu^2/2 sigma^2) u_x^2/u_xx + (gamma/(1-gamma)) u_x^(1-1/gamma) - rho u
    # Non-polynomial in the jet: divides by u_xx and takes a fractional power.
    # The -u_xx/2 cancels the framework's own (1/2) u_xx: after the optimal
    # control is substituted back there is no uncontrolled diffusion left, so
    # the tree's Brownian motion here is purely a computational device.
    pde = partial(merton_hjb, T=0.1)
    grid = np.linspace(100.0, 200.0, 27)   # x is WEALTH, so it must stay positive

    curves = [CodingTreeMC(n_samples=10_000, seed=0).solve(pde, grid)]

    if DEEP:
        from parabolab import DeepBranching
        curves.append(DeepBranching(n_states=1000, m_samples=10_000,
                                    epochs=3000, n_jobs=8).solve(pde, grid))

    title = "Merton HJB $d=1$: " + ("MC and deep branching" if DEEP
                                    else "coding-tree Monte Carlo")
    compare(pde, *curves).table().plot(Path(__file__).with_suffix(".png"),
                                       title)


# Why only deep branching here:
#  * deep BSDE FAILS on this problem -- L1 ~ 1.6, reproduced in
#    examples/jcp_comparison_baselines.py.  That negative result is one of
#    the paper's points, not a bug in the adapter.
#  * deep Galerkin is judged inapplicable here by JCP2024 Sec. 4 (d): its
#    loss divides by the net's second derivative.  We follow that
#    judgement by declaration; the adapter itself builds fine.
#  * both baselines need the authors' regularized expressions to avoid NaN
#    -- pass them as f_expr=/phi_expr=, see merton_overrides() in
#    examples/jcp_comparison_baselines.py.
#
# The guard is mandatory: DeepBranching fans its training data out to worker
# processes, and under spawn (Windows, macOS) the child re-imports this file.
if __name__ == "__main__":
    main()
