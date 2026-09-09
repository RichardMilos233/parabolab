"""Adaptive and nonuniform tuple proposals for coding-tree Monte Carlo."""

from __future__ import annotations

import math
from typing import Any, Callable, Mapping, Sequence, Tuple

import numpy as np

from .mechanism import Code

TupleProposal = Callable[[Code, float, object, float, int, tuple], Sequence[float]]


def validate_probabilities(probs: Any, n_tuples: int) -> np.ndarray:
    """Validate and return normalized 1D probability array."""
    try:
        arr = np.asarray(probs, dtype=float)
    except Exception as exc:
        raise ValueError(f"Proposal probabilities must be numeric, got {probs!r}") from exc
    if arr.ndim != 1 or len(arr) != n_tuples:
        raise ValueError(
            f"Proposal probabilities must be 1D array of length {n_tuples}, got shape {arr.shape}"
        )
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"Proposal probabilities must be finite, got {arr}")
    if np.any(arr <= 0.0):
        raise ValueError(f"Proposal probabilities must be strictly positive, got {arr}")
    if not np.isclose(float(np.sum(arr)), 1.0, atol=1e-12):
        raise ValueError(f"Proposal probabilities must sum to 1.0 within 1e-12, sum is {np.sum(arr)}")
    return arr


def sqrt_optimal_probabilities(contributions: Any, *, floor_mass: float = 0.0) -> np.ndarray:
    """Compute optimal Cauchy-Schwarz square-root probabilities with an optional uniform floor.

    q_i^* = sqrt(A_i) / sum_j sqrt(A_j)
    With floor_mass eps in [0, 1), the mixture is (1 - eps) * q^* + eps / m.
    """
    if not (0.0 <= floor_mass < 1.0):
        raise ValueError(f"floor_mass must be in [0, 1), got {floor_mass}")

    try:
        arr = np.asarray(contributions, dtype=float)
    except Exception as exc:
        raise ValueError(f"Contributions must be numeric, got {contributions!r}") from exc

    if arr.ndim != 1 or arr.size == 0:
        raise ValueError(f"contributions cannot be empty and must be 1D, got shape {arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"contributions must be finite, got {arr}")
    if np.any(arr < 0.0):
        raise ValueError(f"contributions must be non-negative, got {arr}")
    if np.all(arr == 0.0):
        raise ValueError("contributions cannot be all zero")
    if floor_mass == 0.0 and np.any(arr == 0.0):
        raise ValueError(
            "contributions must be strictly positive when floor_mass == 0.0 (got zero entry)"
        )

    sqrt_a = np.sqrt(arr)
    sum_sqrt = float(np.sum(sqrt_a))
    if sum_sqrt == 0.0:
        raise ValueError("Sum of square-root contributions is zero")
    q_star = sqrt_a / sum_sqrt

    m = len(arr)
    if floor_mass > 0.0:
        q_mix = (1.0 - floor_mass) * q_star + (floor_mass / m)
        return q_mix
    return q_star


def second_moment_objective(contributions: Any, probabilities: Any) -> float:
    """Evaluate J(q) = sum_i A_i / q_i."""
    a = np.asarray(contributions, dtype=float)
    q = validate_probabilities(probabilities, len(a))
    if np.any(a < 0.0):
        raise ValueError(f"contributions must be non-negative, got {a}")
    return float(np.sum(a / q))


def oracle_ratio_bound(relative_error: float, floor_mass: float = 0.0) -> float:
    r"""Compute the theoretical oracle ratio bound:

    J(\widetilde{q}) <= \frac{1}{1 - \varepsilon} \sqrt{\frac{1 + \eta}{1 - \eta}} J(q^*).
    """
    if not (0.0 <= relative_error < 1.0):
        raise ValueError(f"relative_error must be in [0, 1), got {relative_error}")
    if not (0.0 <= floor_mass < 1.0):
        raise ValueError(f"floor_mass must be in [0, 1), got {floor_mass}")

    ratio = math.sqrt((1.0 + relative_error) / (1.0 - relative_error))
    return (1.0 / (1.0 - floor_mass)) * ratio


class FrozenTupleProposal:
    """Frozen tuple proposal table keyed by (depth, code).

    Falls back to uniform proposal for unkeyed (depth, code) combinations.
    """

    def __init__(
        self,
        probabilities_by_key: Mapping[Tuple[int, Code], Sequence[float]],
    ) -> None:
        self.probabilities_by_key = {
            k: tuple(float(x) for x in v) for k, v in probabilities_by_key.items()
        }

    def __call__(
        self,
        code: Code,
        t: float,
        x: object,
        tau: float,
        depth: int,
        tuples: tuple,
    ) -> Sequence[float]:
        key = (depth, code)
        if key in self.probabilities_by_key:
            return self.probabilities_by_key[key]
        n = len(tuples)
        return tuple(1.0 / n for _ in range(n))
