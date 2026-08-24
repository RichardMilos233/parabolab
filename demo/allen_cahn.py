"""Allen-Cahn, d = 1 (JCP2024 Table 1 / Fig. 1) -- one PDE, several methods."""
from functools import partial
from pathlib import Path

import numpy as np

from parabolab import CodingTreeMC, compare
from parabolab.library import allen_cahn_nd

# u_t + (1/2) u_xx + u - u^3 = 0,  u(T, x) = -1/2 - (1/2) tanh(-x/2)
# A factory, not an instance: the parallel and network solvers rebuild the
# PDE inside worker processes (PDE objects are not picklable).
pde = partial(allen_cahn_nd, d=1, T=0.5)
grid = np.linspace(-8.0, 8.0, 27)

mc = CodingTreeMC(n_samples=10_000, seed=0).solve(pde, grid)

# The paper's other three methods have the same shape.  They train a
# network, so they need a real budget (JCP2024 quotes 28-101 GPU-minutes
# per run); uncomment on a fast machine and add them to compare().
# from parabolab import DeepBranching, DeepBSDE, DeepGalerkin
# deep = DeepBranching(n_states=1000, m_samples=10_000, epochs=3000).solve(pde, grid)
# bsde = DeepBSDE(epochs=3000, n_states=1000).solve(pde, grid)
# dgm  = DeepGalerkin(epochs=3000, n_states=1000).solve(pde, grid)

compare(pde, mc).table().plot(Path(__file__).with_suffix(".png"),
                              "Allen-Cahn $d=1$: coding-tree Monte Carlo")
