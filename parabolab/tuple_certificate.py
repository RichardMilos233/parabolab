"""Exact tuple-policy moment enclosures for raw 1D Allen--Cahn trees.

The normalized coordinates are ``(Id, D, F0, F1, F2, F3)``.  A policy
``q = (q0, q1, q2)`` assigns probability ``qk`` to the first labelled tuple
of ``FDeriv(a, k)`` for ``k = 0, 1, 2``.  All other raw labels retain their
uniform law.  In particular, ``F3`` uses ``(1/2, 1/2)`` because both of its
branches contain an identically zero Allen--Cahn derivative.

This module certifies that specific Allen--Cahn reduction.  The callback does
not inspect a PDE object, so callers are responsible for using the raw
``SemilinearMechanism`` with the Allen--Cahn nonlinearity ``f(u)=u-u^3``.
Certificates use exact rational policies; the production callback converts
them to binary floats, so its end-to-end sampler roundoff is not certified.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional, Sequence

from .mechanism import Code, Dx, FDeriv, Id, SemilinearMechanism
from .rate_certificate import (
    CertificateFailure,
    Rational,
    State,
    WAVE_TERMINAL_UPPER,
    _fraction,
    _round_grid,
    flat_terminal_state,
)


ProbabilityTriple = tuple[Fraction, Fraction, Fraction]
TUPLE_MECHANISM = "SemilinearMechanism/raw/static-AllenCahn-q/1d"


def _probabilities(q: Sequence[Rational]) -> ProbabilityTriple:
    if isinstance(q, (str, bytes)) or len(q) != 3:
        raise ValueError("q must contain exactly q0, q1, q2")
    values = tuple(_fraction(value) for value in q)
    if any(not 0 < value < 1 for value in values):
        raise ValueError("each tuple probability must satisfy 0 < qk < 1")
    return values  # type: ignore[return-value]


def tuple_policy_interval_gate(
    intervals: Sequence[tuple[Rational, Rational]],
    baseline: Sequence[Rational],
    candidate: Sequence[Rational],
) -> Fraction:
    """Exact robust gate for changing one normalized tuple distribution.

    If tuple contribution ``A_i`` is only known to lie in ``[L_i, U_i]``,
    this returns an upper bound for
    ``sum_i A_i * (1 / candidate_i - 1 / baseline_i)``.  Thus ``R <= 0``
    certifies that the candidate cannot increase that local objective over
    the whole product box.  This gate alone makes no full-tree claim.
    """
    if isinstance(intervals, (str, bytes)):
        raise ValueError("intervals must be a nonempty sequence")
    if len(intervals) == 0 or len(baseline) != len(intervals) or len(candidate) != len(intervals):
        raise ValueError("intervals, baseline, and candidate must have the same nonzero length")

    baseline_values = tuple(_fraction(value) for value in baseline)
    candidate_values = tuple(_fraction(value) for value in candidate)
    if (
        any(value <= 0 for value in (*baseline_values, *candidate_values))
        or sum(baseline_values) != 1
        or sum(candidate_values) != 1
    ):
        raise ValueError("baseline and candidate must be normalized positive probabilities")

    exact_intervals = []
    for lower, upper in intervals:
        lower_value, upper_value = _fraction(lower), _fraction(upper)
        if lower_value < 0 or upper_value < lower_value:
            raise ValueError("require rational contribution intervals 0 <= L_i <= U_i")
        exact_intervals.append((lower_value, upper_value))

    result = Fraction(0)
    for (lower, upper), old, new in zip(
        exact_intervals, baseline_values, candidate_values
    ):
        coefficient = 1 / new - 1 / old
        result += coefficient * (upper if coefficient >= 0 else lower)
    return result


def tuple_branch_polynomial(y: State, q: ProbabilityTriple) -> State:
    """Return the exact nonnegative branch polynomial ``G_q(y)``."""
    _, d, a, b, c, e = y
    q0, q1, q2 = q
    return (
        a,
        b * d,
        a * b / q0 + d * d * c / (4 * (1 - q0)),
        a * c / q1 + d * d * e / (4 * (1 - q1)),
        a * e / q2,
        Fraction(0),
    )


def tuple_moment_field(y: State, rate: Fraction, q: ProbabilityTriple) -> State:
    """The flat majorant ODE ``y' = rate*y + G_q(y)/rate``."""
    branch = tuple_branch_polynomial(y, q)
    return tuple(rate * value + source / rate for value, source in zip(y, branch))


@dataclass(frozen=True)
class AllenCahnStaticTupleProposal:
    """Static scalar-independent proposal for raw Allen--Cahn tuple labels.

    The existing sampler keeps the labels unchanged and applies the inverse
    probability weight.  This callback only supplies their probabilities and
    rejects reordered or substituted labels.
    """

    q: ProbabilityTriple

    def __init__(self, q: Sequence[Rational]) -> None:
        values = _probabilities(q)
        for value in values:
            represented = float(value)
            if not 0.0 < represented < 1.0 or not 0.0 < 1.0 - represented < 1.0:
                raise ValueError(
                    "tuple probability support is not representable by the float sampler"
                )
        object.__setattr__(self, "q", values)

    def __call__(
        self,
        code: Code,
        t: float,
        x: object,
        tau: float,
        depth: int,
        tuples: tuple,
    ) -> Sequence[float]:
        del t, x, tau, depth
        if not isinstance(code, (Id, Dx, FDeriv)):
            raise TypeError("AllenCahnStaticTupleProposal requires raw semilinear codes")
        expected = SemilinearMechanism.tuples(code)
        if tuple(tuples) != expected:
            raise ValueError("tuple labels do not match the raw Allen-Cahn mechanism")
        if isinstance(code, FDeriv) and 0 <= code.k <= 2:
            probability = float(self.q[code.k])
            return (probability, 1.0 - probability)
        count = len(expected)
        return tuple(1.0 / count for _ in range(count))


@dataclass(frozen=True)
class TupleBoxStep:
    """One exact postfixed-box witness, explicitly bound to its proposal."""

    duration: Fraction
    q: ProbabilityTriple
    upper_start: State
    upper_end: State
    lower_start: Optional[State]
    lower_end: Optional[State]


@dataclass(frozen=True)
class TupleMomentCertificate:
    """A rational full-tree moment enclosure for one fixed rate and policy."""

    family: str
    phi: Optional[Fraction]
    horizon: Fraction
    rate: Fraction
    q: ProbabilityTriple
    lower: Optional[State]
    upper: State
    witnesses: tuple[TupleBoxStep, ...]
    precision_bits: int
    mechanism: str = TUPLE_MECHANISM

    @property
    def root_lower(self) -> Optional[Fraction]:
        return None if self.lower is None else self.lower[0]

    @property
    def root_upper(self) -> Fraction:
        return self.upper[0]


def enclose_tuple_moment(
    *,
    horizon: Rational,
    rate: Rational,
    q: Sequence[Rational],
    family: str = "flat",
    phi: Rational = "0.5",
    steps: int = 200,
    precision_bits: int = 60,
    max_box_iterations: int = 100,
) -> TupleMomentCertificate:
    """Construct an exact rational postfixed-box enclosure.

    Flat terminal data receive two-sided bounds.  For the traveling wave, the
    result is only a spatially uniform upper envelope derived from
    ``rate_certificate.WAVE_TERMINAL_UPPER``.  Failure to find a finite box is
    inconclusive and raises :class:`CertificateFailure`.
    """
    horizon_value, rate_value = _fraction(horizon), _fraction(rate)
    q_value = _probabilities(q)
    if horizon_value < 0 or rate_value <= 0:
        raise ValueError("require horizon >= 0 and rate > 0")
    for name, value in (
        ("steps", steps),
        ("precision_bits", precision_bits),
        ("max_box_iterations", max_box_iterations),
    ):
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"{name} must be a positive integer")

    if family == "flat":
        phi_value = _fraction(phi)
        upper = lower = flat_terminal_state(phi_value)
    elif family == "wave":
        phi_value, lower, upper = None, None, WAVE_TERMINAL_UPPER
    else:
        raise ValueError("family must be 'flat' or 'wave'")

    denominator = 2**precision_bits
    duration = horizon_value / steps
    witnesses = []
    for step_index in range(steps if horizon_value else 0):
        upper_start = upper
        upper_end = upper_start
        for _ in range(max_box_iterations):
            candidate = tuple(
                _round_grid(start + duration * field, denominator, up=True)
                for start, field in zip(
                    upper_start, tuple_moment_field(upper_end, rate_value, q_value)
                )
            )
            if candidate == upper_end:
                break
            if any(
                value.numerator.bit_length() > precision_bits + 512
                for value in candidate
            ):
                raise CertificateFailure(
                    f"upper box grew too large at step {step_index}"
                )
            upper_end = candidate
        else:
            raise CertificateFailure(
                f"no postfixed upper box at step {step_index}; increase steps"
            )

        if any(
            start + duration * field > end
            for start, field, end in zip(
                upper_start,
                tuple_moment_field(upper_end, rate_value, q_value),
                upper_end,
            )
        ):
            raise CertificateFailure("internal postfixed witness check failed")

        lower_end = None
        if lower is not None:
            lower_end = tuple(
                _round_grid(start + duration * field, denominator, up=False)
                for start, field in zip(
                    lower, tuple_moment_field(lower, rate_value, q_value)
                )
            )
        witnesses.append(
            TupleBoxStep(
                duration,
                q_value,
                upper_start,
                upper_end,
                lower,
                lower_end,
            )
        )
        upper, lower = upper_end, lower_end

    return TupleMomentCertificate(
        family,
        phi_value,
        horizon_value,
        rate_value,
        q_value,
        lower,
        upper,
        tuple(witnesses),
        precision_bits,
    )


def verify_tuple_moment_certificate(certificate: TupleMomentCertificate) -> bool:
    """Independently re-evaluate every exact witness inequality.

    The checker intentionally spells out ``G_q`` rather than calling the
    generator's polynomial or field helpers.  It checks the finite numerical
    witness; the stochastic correspondence remains an analytical obligation.
    """
    c = certificate

    def rational_state(value: object) -> bool:
        return isinstance(value, tuple) and len(value) == 6 and all(
            isinstance(item, Fraction) for item in value
        )

    def checked_field(y: State) -> State:
        _, d, a, b, cc, e = y
        q0, q1, q2 = c.q
        branch = (
            a,
            b * d,
            a * b / q0 + d * d * cc / (4 * (1 - q0)),
            a * cc / q1 + d * d * e / (4 * (1 - q1)),
            a * e / q2,
            Fraction(0),
        )
        return tuple(
            c.rate * value + source / c.rate
            for value, source in zip(y, branch)
        )

    if not isinstance(c, TupleMomentCertificate):
        return False
    if (
        not isinstance(c.horizon, Fraction)
        or not isinstance(c.rate, Fraction)
        or not isinstance(c.q, tuple)
        or len(c.q) != 3
        or not all(isinstance(value, Fraction) and 0 < value < 1 for value in c.q)
        or c.horizon < 0
        or c.rate <= 0
        or not isinstance(c.precision_bits, int)
        or isinstance(c.precision_bits, bool)
        or c.precision_bits < 1
        or c.mechanism != TUPLE_MECHANISM
        or not rational_state(c.upper)
        or (c.lower is not None and not rational_state(c.lower))
    ):
        return False

    if c.family == "flat" and isinstance(c.phi, Fraction) and 0 < c.phi <= 1:
        p = c.phi
        upper = lower = (
            p * p,
            Fraction(0),
            (p - p**3) ** 2,
            (1 - 3 * p * p) ** 2,
            36 * p * p,
            Fraction(36),
        )
    elif c.family == "wave" and c.phi is None:
        upper, lower = (
            Fraction(1),
            Fraction(1, 16),
            Fraction(4, 27),
            Fraction(4),
            Fraction(36),
            Fraction(36),
        ), None
    else:
        return False

    elapsed = Fraction(0)
    for witness in c.witnesses:
        if (
            not isinstance(witness, TupleBoxStep)
            or not isinstance(witness.duration, Fraction)
            or witness.duration <= 0
            or witness.q != c.q
            or not rational_state(witness.upper_start)
            or not rational_state(witness.upper_end)
            or (
                witness.lower_start is not None
                and not rational_state(witness.lower_start)
            )
            or (
                witness.lower_end is not None
                and not rational_state(witness.lower_end)
            )
            or witness.upper_start != upper
            or witness.lower_start != lower
            or any(end < start for start, end in zip(upper, witness.upper_end))
        ):
            return False
        if any(
            start + witness.duration * field > end
            for start, field, end in zip(
                upper, checked_field(witness.upper_end), witness.upper_end
            )
        ):
            return False

        if lower is None:
            if witness.lower_end is not None:
                return False
        else:
            if witness.lower_end is None:
                return False
            lower_field = checked_field(lower)
            if any(
                not start <= end <= start + witness.duration * field
                for start, field, end in zip(lower, lower_field, witness.lower_end)
            ):
                return False

        elapsed += witness.duration
        upper, lower = witness.upper_end, witness.lower_end

    return (
        elapsed == c.horizon
        and upper == c.upper
        and lower == c.lower
        and ((c.horizon == 0 and not c.witnesses) or c.horizon > 0)
    )
