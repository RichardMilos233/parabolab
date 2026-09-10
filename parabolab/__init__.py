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
from .state_dependent import (
    StateDependentPDEnD,
    StateDependentMechanismND,
    StateFNu,
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
from .moments import MomentQuadrature, finite_depth_moment_1d
from .rate_optimization import (
    RateMomentDerivatives,
    RateOptimizationResult,
    finite_depth_moment_derivatives_1d,
    optimize_exponential_rate_1d,
    riccati_binary_second_moment,
)
from .integrability import truncated_normal_inverse_power
from .proposals import (
    FrozenTupleProposal,
    TuplePilotResult,
    estimate_tuple_contributions,
    oracle_ratio_bound,
    second_moment_objective,
    sqrt_optimal_probabilities,
    validate_probabilities,
)
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
    "FrozenTupleProposal",
    "FullyNonlinearMechanism1D",
    "FullyNonlinearMechanismND",
    "FullyNonlinearPDE1D",
    "FullyNonlinearPDEnD",
    "Id",
    "MCResult",
    "MomentQuadrature",
    "ParabolicPDE",
    "SemilinearMechanism",
    "Solver",
    "TSweep",
    "TreeSample",
    "TuplePilotResult",
    "compare",
    "default_rate",
    "estimate",
    "estimate_parallel",
    "estimate_tuple_contributions",
    "exact_on",
    "finite_depth_moment_1d",
    "finite_depth_moment_derivatives_1d",
    "grid_states",
    "integrability_edge",
    "jcp_rate",
    "library",
    "oracle_ratio_bound",
    "optimize_exponential_rate_1d",
    "RateMomentDerivatives",
    "RateOptimizationResult",
    "riccati_binary_second_moment",
    "sample_tree",
    "second_moment_objective",
    "sqrt_optimal_probabilities",
    "sweep_T",
    "truncated_normal_inverse_power",
    "validate_probabilities",
    "x_symbol",
    "x_symbols",
    "z_symbols",
]
