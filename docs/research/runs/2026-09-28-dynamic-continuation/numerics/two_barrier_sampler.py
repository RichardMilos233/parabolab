"""Floating implementation of the frozen two-barrier Allen--Cahn sampler.

This module contains only the stochastic mechanism.  It does not import the
independent deterministic reference.  The implementation approximates the
reviewed ideal-real construction in binary64; it is not a finite-bit
unbiasedness certificate.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import time
from typing import Callable

import numpy as np


LOWER_BARRIER = 0.5
UPPER_BARRIER = 0.75
DOMAIN_PERIOD = 2.0 * math.pi
Z0 = LOWER_BARRIER / UPPER_BARRIER
LOWER_A = LOWER_BARRIER**-2 - 1.0
UPPER_A = UPPER_BARRIER**-2 - 1.0
LEAF_PROPOSAL_PROBABILITY = 8.0 / 15.0
INVERSE_DENOMINATOR_CONSTANT = 20.0 / 9.0
DEFAULT_RANGE_TOLERANCE = 1.0e-12
FLOAT_DOMAIN_TOLERANCE = 8.0 * math.ulp(1.0)


class SamplingDeadlineExceeded(RuntimeError):
    """Raised when a root is unfinished at the fixed sampling deadline."""


class SamplerInvariantError(RuntimeError):
    """Raised when a completed root violates a frozen pathwise invariant."""


@dataclass(frozen=True)
class LimitingClockProposal:
    """One proposal from the horizon-free limiting clock."""

    is_leaf: bool
    remaining_time: float
    zeta: float
    zero_redraws: int


@dataclass(frozen=True)
class EventInverse:
    """Binary64 intermediates of the stable limiting-event inverse."""

    zeta: float
    stable_d: float
    q_event: float
    remaining_time: float


@dataclass(frozen=True)
class FiniteClockOutcome:
    """One accepted finite-horizon clock after rejecting events at or beyond T."""

    is_leaf: bool
    remaining_time: float
    zeta: float
    proposals: int
    rejections: int
    zero_redraws: int


@dataclass(frozen=True)
class RootSample:
    """A completed root and every pathwise quantity required by the protocol."""

    scaled_output: float
    normalized_output: float
    nodes: int
    leaves: int
    binary_internal: int
    ternary_internal: int
    clock_proposals: int
    clock_rejections: int
    zero_redraws: int
    coefficient_limit_substitution: bool


InitialValueOracle = Callable[[float], float]


def _check_deadline(deadline: float | None) -> None:
    if deadline is not None and time.monotonic() >= deadline:
        raise SamplingDeadlineExceeded("unfinished root reached sampling deadline")


def _open_unit_uniform(rng: np.random.Generator) -> tuple[float, int]:
    """Draw from (0,1), redrawing the possible exact zero as frozen in 02d."""

    zero_redraws = 0
    while True:
        u = float(rng.random())
        if u != 0.0:
            return u, zero_redraws
        zero_redraws += 1


def limiting_clock_proposal(rng: np.random.Generator) -> LimitingClockProposal:
    """Draw one limiting-clock leaf or event proposal.

    The stable numerator is evaluated as
    ``(1-U)(1+zeta)/(1+zeta-U/2)``.  No clipping or finite-horizon value of
    ``z(T)`` is used.
    """

    u, zero_redraws = _open_unit_uniform(rng)
    if u <= LEAF_PROPOSAL_PROBABILITY:
        return LimitingClockProposal(True, 0.0, math.nan, zero_redraws)

    inverse = event_inverse_from_uniform(u)
    return LimitingClockProposal(
        False,
        inverse.remaining_time,
        inverse.zeta,
        zero_redraws,
    )


def event_inverse_from_uniform(u: float) -> EventInverse:
    """Evaluate the stable event inverse for one binary64 ``u``.

    Exact-real event draws satisfy ``z0 < zeta < 1``.  At the nearest
    binary64 inputs, the rounded intermediate may equal an endpoint, so the
    endpoint check uses an explicit ulp-scale diagnostic tolerance.  The
    value is never clipped and the event is never discarded.  Positivity of
    ``d``, the denominator, ``q_event`` and the event time remains mandatory.
    """

    if not (LEAF_PROPOSAL_PROBABILITY < u < 1.0):
        raise ValueError("event inverse requires leaf_threshold < u < 1")

    y = 0.5 * u
    zeta = 0.5 * (y + math.sqrt(y * y + 4.0 * y))
    d = (1.0 - u) * (1.0 + zeta) / (1.0 + zeta - y)
    denominator = INVERSE_DENOMINATOR_CONSTANT - LOWER_A * d
    q_event = d / denominator

    if not (
        math.isfinite(zeta)
        and Z0 - FLOAT_DOMAIN_TOLERANCE
        <= zeta
        <= 1.0 + FLOAT_DOMAIN_TOLERANCE
        and 0.0 < d <= 1.0 - Z0 * Z0 + FLOAT_DOMAIN_TOLERANCE
        and denominator > 0.0
        and 0.0 < q_event < 1.0
    ):
        raise SamplerInvariantError(
            "limiting-clock inverse left its reviewed binary64 domain"
        )

    remaining_time = -0.5 * math.log(q_event)
    if not (math.isfinite(remaining_time) and remaining_time > 0.0):
        raise SamplerInvariantError("limiting-clock event time is not finite positive")
    return EventInverse(zeta, d, q_event, remaining_time)


def sample_finite_clock(
    rng: np.random.Generator,
    horizon: float,
    *,
    deadline: float | None = None,
) -> FiniteClockOutcome:
    """Sample the accepted finite-horizon clock through limiting rejection."""

    if not (math.isfinite(horizon) and horizon > 0.0):
        raise ValueError("finite-clock horizon must be finite and positive")

    proposals = 0
    rejections = 0
    zero_redraws = 0
    while True:
        _check_deadline(deadline)
        proposal = limiting_clock_proposal(rng)
        proposals += 1
        zero_redraws += proposal.zero_redraws
        if proposal.is_leaf or proposal.remaining_time < horizon:
            return FiniteClockOutcome(
                proposal.is_leaf,
                proposal.remaining_time,
                proposal.zeta,
                proposals,
                rejections,
                zero_redraws,
            )
        rejections += 1


def branch_binary_probability(zeta: float) -> float:
    """Return the OR2 mixture probability at an accepted event time."""

    p = 3.0 * (1.0 + zeta) / (2.0 * (2.0 + zeta))
    if not (0.75 <= p <= 1.0):
        raise SamplerInvariantError("branch-mixture probability left [3/4,1]")
    return p


def scaled_barrier_defect(c: float, horizon: float) -> tuple[float, bool]:
    """Compute R_c(T), using its q=0 limit only on actual exponential underflow."""

    if not (0.0 < c < 1.0):
        raise ValueError("barrier value must lie in (0,1)")
    if not (math.isfinite(horizon) and horizon >= 0.0):
        raise ValueError("horizon must be finite and nonnegative")

    a_c = c**-2 - 1.0
    q = math.exp(-2.0 * horizon)
    if q == 0.0:
        return 0.5 * a_c, True
    square_root = math.sqrt(1.0 + a_c * q)
    return a_c / (square_root * (1.0 + square_root)), False


def cosine_initial_value(x: float) -> float:
    """The frozen smooth 2pi-periodic initial datum."""

    reduced = x % DOMAIN_PERIOD
    return 5.0 / 8.0 + math.cos(reduced) / 8.0


def constant_initial_value(value: float) -> InitialValueOracle:
    """Create a constant diagnostic oracle without importing reference code."""

    constant = float(value)

    def oracle(_: float) -> float:
        return constant

    return oracle


def _normalized_leaf_value(value: float, tolerance: float) -> float:
    z = (value - LOWER_BARRIER) / (UPPER_BARRIER - LOWER_BARRIER)
    if not (-tolerance <= z <= 1.0 + tolerance):
        raise SamplerInvariantError("leaf oracle left the frozen barrier interval")
    return z


def _or2(left: float, right: float) -> float:
    return left + right - left * right


def _majority3(first: float, second: float, third: float) -> float:
    return (
        first * second
        + first * third
        + second * third
        - 2.0 * first * second * third
    )


def validate_root_sample(
    sample: RootSample,
    horizon: float,
    *,
    tolerance: float = DEFAULT_RANGE_TOLERANCE,
) -> None:
    """Check every frozen pathwise count and range identity for one root."""

    n = sample.nodes
    leaves = sample.leaves
    binary = sample.binary_internal
    ternary = sample.ternary_internal
    if n != leaves + binary + ternary:
        raise SamplerInvariantError("N != L + I2 + I3")
    if n != 1 + 2 * binary + 3 * ternary:
        raise SamplerInvariantError("N != 1 + 2 I2 + 3 I3")
    if leaves != 1 + binary + 2 * ternary:
        raise SamplerInvariantError("L != 1 + I2 + 2 I3")

    if horizon == 0.0:
        if sample.clock_proposals != 0 or sample.clock_rejections != 0:
            raise SamplerInvariantError("time-zero shortcut used a clock proposal")
    elif sample.clock_proposals != n + sample.clock_rejections:
        raise SamplerInvariantError("clock proposals != nodes + rejections")

    if not (-tolerance <= sample.normalized_output <= 1.0 + tolerance):
        raise SamplerInvariantError("completed Z left [0,1] beyond tolerance")
    r_upper, upper_limit = scaled_barrier_defect(UPPER_BARRIER, horizon)
    r_lower, lower_limit = scaled_barrier_defect(LOWER_BARRIER, horizon)
    if not (
        r_upper - tolerance
        <= sample.scaled_output
        <= r_lower + tolerance
    ):
        raise SamplerInvariantError("completed W left its local barrier interval")
    if not (0.25 - tolerance <= sample.scaled_output <= 1.5 + tolerance):
        raise SamplerInvariantError("completed W left the global [1/4,3/2] interval")
    if sample.coefficient_limit_substitution != (upper_limit or lower_limit):
        raise SamplerInvariantError("coefficient-limit flag is inconsistent")


def sample_root(
    rng: np.random.Generator,
    horizon: float,
    x: float,
    *,
    initial_value: InitialValueOracle = cosine_initial_value,
    deadline: float | None = None,
    tolerance: float = DEFAULT_RANGE_TOLERANCE,
) -> RootSample:
    """Evaluate one completed mixed OR2/MAJ3 tree with an explicit stack.

    At an accepted branch event the mixture parameter is evaluated from that
    proposal's ``zeta``.  Its children all have remaining time ``s`` and the
    same Brownian branch location, while all descendant random draws are fresh.
    No node or depth cutoff is present.
    """

    if not (math.isfinite(horizon) and horizon >= 0.0):
        raise ValueError("horizon must be finite and nonnegative")
    if not math.isfinite(x):
        raise ValueError("query location must be finite")

    if horizon == 0.0:
        initial = initial_value(x % DOMAIN_PERIOD)
        z = _normalized_leaf_value(initial, tolerance)
        sample = RootSample(
            scaled_output=1.0 - initial,
            normalized_output=z,
            nodes=1,
            leaves=1,
            binary_internal=0,
            ternary_internal=0,
            clock_proposals=0,
            clock_rejections=0,
            zero_redraws=0,
            coefficient_limit_substitution=False,
        )
        validate_root_sample(sample, horizon, tolerance=tolerance)
        return sample

    # Frames are (kind, remaining time or arity, location or operation).
    # kind=0 visits a stochastic node; kind=1 combines already computed children.
    stack: list[tuple[int, float | int, float | int]] = [(0, horizon, x)]
    values: list[float] = []
    nodes = 0
    leaves = 0
    binary_internal = 0
    ternary_internal = 0
    clock_proposals = 0
    clock_rejections = 0
    zero_redraws = 0

    while stack:
        _check_deadline(deadline)
        kind, first, second = stack.pop()
        if kind == 1:
            arity = int(first)
            if arity == 2:
                left, right = values[-2:]
                del values[-2:]
                combined = _or2(left, right)
            elif arity == 3:
                child_a, child_b, child_c = values[-3:]
                del values[-3:]
                combined = _majority3(child_a, child_b, child_c)
            else:
                raise SamplerInvariantError("unknown combination arity")
            if not (-tolerance <= combined <= 1.0 + tolerance):
                raise SamplerInvariantError("multiaffine vote left [0,1]")
            values.append(combined)
            continue

        remaining = float(first)
        location = float(second)
        nodes += 1
        clock = sample_finite_clock(rng, remaining, deadline=deadline)
        clock_proposals += clock.proposals
        clock_rejections += clock.rejections
        zero_redraws += clock.zero_redraws

        if clock.is_leaf:
            _check_deadline(deadline)
            leaf_location = (
                location + math.sqrt(remaining) * float(rng.standard_normal())
            ) % DOMAIN_PERIOD
            z_leaf = _normalized_leaf_value(initial_value(leaf_location), tolerance)
            values.append(z_leaf)
            leaves += 1
            continue

        branch_remaining = clock.remaining_time
        edge_variance = remaining - branch_remaining
        if not edge_variance > 0.0:
            raise SamplerInvariantError("accepted branch did not reduce remaining time")
        _check_deadline(deadline)
        branch_location = (
            location + math.sqrt(edge_variance) * float(rng.standard_normal())
        ) % DOMAIN_PERIOD
        binary_probability = branch_binary_probability(clock.zeta)
        if float(rng.random()) < binary_probability:
            arity = 2
            binary_internal += 1
        else:
            arity = 3
            ternary_internal += 1

        stack.append((1, arity, arity))
        for _ in range(arity):
            stack.append((0, branch_remaining, branch_location))

    if len(values) != 1:
        raise SamplerInvariantError("explicit evaluation stack did not produce one root")
    z = values[0]
    r_upper, upper_limit = scaled_barrier_defect(UPPER_BARRIER, horizon)
    r_lower, lower_limit = scaled_barrier_defect(LOWER_BARRIER, horizon)
    scaled_output = r_upper * z + r_lower * (1.0 - z)
    sample = RootSample(
        scaled_output=scaled_output,
        normalized_output=z,
        nodes=nodes,
        leaves=leaves,
        binary_internal=binary_internal,
        ternary_internal=ternary_internal,
        clock_proposals=clock_proposals,
        clock_rejections=clock_rejections,
        zero_redraws=zero_redraws,
        coefficient_limit_substitution=upper_limit or lower_limit,
    )
    validate_root_sample(sample, horizon, tolerance=tolerance)
    return sample
