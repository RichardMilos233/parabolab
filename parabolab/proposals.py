"""Adaptive and nonuniform tuple proposals for coding-tree Monte Carlo."""

from __future__ import annotations

import math
from dataclasses import dataclass
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


class TerminalTupleProposal:
    """Cheap state-local tuple proposal based on terminal-code magnitudes.

    For each labelled tuple ``Z`` supplied by the sampler callback, this
    computes the proxy ``A_Z = prod_{child in Z} |child(phi)(x)|^2`` at the
    parent particle's birth position ``x``.  It returns the uniform-floor
    mixture of probabilities proportional to ``sqrt(A_Z)``.  Products are
    evaluated in log space, so large finite terminal values do not overflow.

    This is a deterministic heuristic, not a conditional child-moment
    oracle.  It is initially supported for serial ``estimate``/``sample_tree``
    and the deterministic 1D moment tools; no multiprocessing support is
    promised.  The proxy deliberately ignores ``t``, ``tau``, and ``depth``.
    Since every probability is at least ``floor_mass / m``, a uniform-
    proposal local branching/majorant coefficient transfers conservatively
    with factor ``1 / floor_mass``.  This is not a claim that an entire
    full-tree moment bound is inflated by only that single factor.
    A nonfinite value at the parent-state proxy is rejected even when later
    Brownian leaf evaluations might be finite almost surely.
    """

    def __init__(self, pde, *, mechanism=None, floor_mass: float = 0.05) -> None:
        from .mechanism import SemilinearMechanism

        try:
            floor_mass = float(floor_mass)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(
                f"floor_mass must be finite and strictly between 0 and 1, got {floor_mass}"
            ) from exc
        if not math.isfinite(floor_mass) or not (0.0 < floor_mass < 1.0):
            raise ValueError(
                f"floor_mass must be finite and strictly between 0 and 1, got {floor_mass}"
            )
        self.pde = pde
        if mechanism is None:
            mechanism = getattr(pde, "mechanism", None) or SemilinearMechanism
        self.mechanism = mechanism
        self.floor_mass = floor_mass

    def __call__(
        self,
        code: Code,
        t: float,
        x: object,
        tau: float,
        depth: int,
        tuples: tuple,
    ) -> Sequence[float]:
        del code, t, tau, depth
        m = len(tuples)
        if m == 0:
            raise ValueError("TerminalTupleProposal requires at least one tuple")
        uniform_floor = self.floor_mass / m
        if uniform_floor == 0.0:
            raise ValueError(
                "floor_mass / number of tuples underflowed to zero; "
                "strict proposal support cannot be represented"
            )

        log_scores = np.full(m, -np.inf, dtype=float)
        for tuple_index, labelled_tuple in enumerate(tuples):
            log_score = 0.0
            for child_index, child in enumerate(labelled_tuple):
                try:
                    terminal = float(self.mechanism.terminal(child, self.pde, x))
                except Exception as exc:
                    raise ValueError(
                        "TerminalTupleProposal could not evaluate terminal value for "
                        f"tuple {tuple_index}, child {child_index}: {child!r}"
                    ) from exc
                if not math.isfinite(terminal):
                    raise ValueError(
                        "TerminalTupleProposal requires finite terminal values; "
                        f"tuple {tuple_index}, child {child_index} produced {terminal}"
                    )
                if terminal == 0.0:
                    log_score = -math.inf
                    break
                log_score += math.log(abs(terminal))
            log_scores[tuple_index] = log_score

        finite = np.isfinite(log_scores)
        if not np.any(finite):
            return tuple(1.0 / m for _ in range(m))

        max_log = float(np.max(log_scores[finite]))
        scaled_sqrt_scores = np.zeros(m, dtype=float)
        scaled_sqrt_scores[finite] = np.exp(log_scores[finite] - max_log)
        total = float(np.sum(scaled_sqrt_scores))
        if not math.isfinite(total) or total <= 0.0:
            raise ValueError("TerminalTupleProposal produced invalid scaled terminal scores")

        q_star = scaled_sqrt_scores / total
        probabilities = (
            (1.0 - self.floor_mass) * q_star + uniform_floor
        )
        return tuple(float(q) for q in probabilities)


@dataclass(frozen=True)
class TuplePilotResult:
    """Estimated second-moment contributions B_Z and standard errors for tuples of a code."""

    contributions: np.ndarray
    stderr: np.ndarray
    n_samples: int
    continuation_depth: int


def estimate_tuple_contributions(
    pde,
    t: float,
    x: object,
    code: Code,
    *,
    n_samples: int,
    seed: int,
    rate: float,
    continuation_depth: int,
    mechanism=None,
) -> TuplePilotResult:
    r"""Estimate tuple second-moment contributions via pilot continuation sampling:

    B_Z = \int_0^{T-t} \frac{1}{\rho(s)} \mathbb{E}\left[ \left|\prod_{z \in Z} H_z^{[d]}(t+s, X_s)\right|^2 \right] ds.
    """
    from .mechanism import SemilinearMechanism
    from .tree import sample_tree

    if mechanism is None:
        mechanism = getattr(pde, "mechanism", None) or SemilinearMechanism

    remaining = pde.T - t
    if remaining <= 0.0:
        raise ValueError(f"Remaining time pde.T - t must be positive, got T={pde.T}, t={t}")
    if n_samples < 1:
        raise ValueError(f"n_samples must be >= 1, got {n_samples}")
    if rate <= 0.0:
        raise ValueError(f"rate must be positive, got {rate}")

    tuples = mechanism.tuples(code)
    m = len(tuples)
    if m == 0:
        raise ValueError(f"No tuples for code {code}")

    sig = math.sqrt(getattr(pde, "sigma2", 1.0))
    size = x.shape if isinstance(x, np.ndarray) else None

    # Spawn independent RNG streams for each tuple
    streams = np.random.SeedSequence(seed).spawn(m)
    b_means = np.empty(m, dtype=float)
    b_stderrs = np.empty(m, dtype=float)

    for j, (Z_tuple, child_seed) in enumerate(zip(tuples, streams)):
        rng_j = np.random.default_rng(child_seed)
        samples = np.empty(n_samples, dtype=float)

        for i in range(n_samples):
            # 1. draw s uniformly on (0, remaining)
            s = float(rng_j.uniform(0.0, remaining))
            # 2. draw shared branch position using PDE diffusion
            xb = x + rng_j.normal(0.0, sig * math.sqrt(s), size=size)

            # 3. independently sample each child killed tree at continuation_depth
            prod_val = 1.0
            for child_code in Z_tuple:
                child_sample = sample_tree(
                    pde,
                    t + s,
                    xb,
                    rng=rng_j,
                    rate=rate,
                    code=child_code,
                    mechanism=mechanism,
                    prune_zero=True,
                    max_depth=continuation_depth,
                )
                prod_val *= child_sample.value

            # 4 & 5. importance weight: remaining * abs(product)^2 / rho(s)
            rho_s = rate * math.exp(-rate * s)
            term = remaining * (abs(prod_val) ** 2) / rho_s
            if not math.isfinite(term):
                raise ValueError(
                    f"Non-finite pilot observation encountered for tuple {Z_tuple}: {term}"
                )
            samples[i] = term

        b_means[j] = float(np.mean(samples))
        b_stderrs[j] = float(np.std(samples, ddof=1) / math.sqrt(n_samples))

    return TuplePilotResult(
        contributions=b_means,
        stderr=b_stderrs,
        n_samples=n_samples,
        continuation_depth=continuation_depth,
    )
