"""Deep branching solver, JCP2024 Algorithm 2 (milestone M4).

Functional estimation of u(., .): instead of one pointwise expectation,
train a neural network v(t, x; theta) to the L2 projection of the tree
functional H over random training states (tau_i, X_i):

    v* = argmin  N^{-1} sum_i ( M^{-1} sum_j H_{i,j} - v(tau_i, X_i) )^2.

This subpackage imports torch and is therefore NOT imported by the top
level ``parabolab`` package; ``import parabolab.deep`` explicitly.

All code is device-agnostic: pass device="cuda" (or "mps") to run on GPU;
everything defaults to CPU.
"""

from .experiments import ExperimentResult, run_experiment
from .generator import TrainingData, generate_training_data
from .net import DeepBranchNet
from .solver import (
    DeepBranchingResult,
    consistency_plot,
    grid_errors,
    train_deep_branching,
)

__all__ = [
    "TrainingData",
    "generate_training_data",
    "DeepBranchNet",
    "DeepBranchingResult",
    "train_deep_branching",
    "grid_errors",
    "consistency_plot",
    "ExperimentResult",
    "run_experiment",
]
