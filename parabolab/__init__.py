"""parabolab: coding-tree Monte Carlo for fully nonlinear parabolic PDEs.

From-scratch reproduction of Nguwi, Penent & Privault:
- "A fully nonlinear Feynman-Kac formula with derivatives of arbitrary
  orders", J. Evol. Equ. 23:22 (2023)  [JEQ2023]
- "A deep branching solver for fully nonlinear partial differential
  equations", J. Comput. Phys. 499 (2024) 112712  [JCP2024]
"""

from .mc import MCResult, estimate
from .parallel import estimate_parallel
from .mechanism import (
    Code,
    Dx,
    DxN,
    FDeriv,
    FNu,
    FullyNonlinearMechanism1D,
    FullyNonlinearMechanismND,
    Id,
    SemilinearMechanism,
)
from .pde import (
    FullyNonlinearPDE1D,
    FullyNonlinearPDEnD,
    ParabolicPDE,
    x_symbol,
    x_symbols,
    z_symbols,
)
from .solve import (
    CodingTreeMC,
    Comparison,
    Curve,
    DeepBSDE,
    DeepBranching,
    DeepGalerkin,
    Solver,
    compare,
    exact_on,
    grid_states,
)
from .tree import TreeSample, default_rate, jcp_rate, sample_tree
from .blowup import TSweep, integrability_edge, sweep_T
from . import library

__all__ = [
    "Code",
    "CodingTreeMC",
    "Comparison",
    "Curve",
    "DeepBSDE",
    "DeepBranching",
    "DeepGalerkin",
    "Dx",
    "DxN",
    "FDeriv",
    "FNu",
    "FullyNonlinearMechanism1D",
    "FullyNonlinearMechanismND",
    "FullyNonlinearPDE1D",
    "FullyNonlinearPDEnD",
    "Id",
    "MCResult",
    "ParabolicPDE",
    "SemilinearMechanism",
    "Solver",
    "TSweep",
    "TreeSample",
    "compare",
    "default_rate",
    "estimate",
    "estimate_parallel",
    "exact_on",
    "grid_states",
    "integrability_edge",
    "jcp_rate",
    "library",
    "sample_tree",
    "sweep_T",
    "x_symbol",
    "x_symbols",
    "z_symbols",
]
