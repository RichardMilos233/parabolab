"""Exact rational moment enclosures for the raw 1D Allen--Cahn coding tree.

The six coordinates are Id, Dx(1), F0, F1, F2, F3; Fk^a moments are
normalized by a**2. This module certifies an explicitly specified mechanism,
not arbitrary PDEs or the finite-depth Gaussian quadrature optimizer.
See docs/research/estimator-integrity/allen-cahn-codewise-certificate.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial
from typing import Optional


Rational = Fraction | int | str
State = tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]
CODE_NAMES = ("Id", "D", "F0", "F1", "F2", "F3")
MECHANISM = "SemilinearMechanism/raw/uniform/1d"


class CertificateFailure(RuntimeError):
    """The finite enclosure computation was inconclusive, not proof of divergence."""


def _fraction(value: Rational) -> Fraction:
    if isinstance(value, (float, bool)):
        raise TypeError("use an exact Fraction, integer, or decimal string")
    return Fraction(value)


def branch_polynomial(y: State) -> State:
    """Nonnegative moment polynomial for the actual raw tuple probabilities."""
    _, d, f0, f1, f2, f3 = y
    return (f0, f1 * d, 2 * f0 * f1 + d * d * f2 / 2,
            2 * f0 * f2 + d * d * f3 / 2, 2 * f0 * f3, Fraction(0))


def _field(y: State, linear: Fraction, branch: Fraction) -> State:
    return tuple(linear * a + branch * b
                 for a, b in zip(y, branch_polynomial(y)))


def _round_grid(value: Fraction, denominator: int, *, up: bool) -> Fraction:
    scaled = value * denominator
    integer = (-(-scaled.numerator // scaled.denominator) if up
               else scaled.numerator // scaled.denominator)
    return Fraction(integer, denominator)


def flat_terminal_state(phi: Rational = "0.5") -> State:
    """Exact terminal squared factors for spatially constant 0 < phi <= 1."""
    p = _fraction(phi)
    if not 0 < p <= 1:
        raise ValueError("the certified flat family requires 0 < phi <= 1")
    return (p * p, Fraction(0), (p - p**3)**2, (1 - 3 * p * p)**2,
            36 * p * p, Fraction(36))


WAVE_TERMINAL_UPPER: State = (
    Fraction(1), Fraction(1, 16), Fraction(4, 27), Fraction(4),
    Fraction(36), Fraction(36),
)


@dataclass(frozen=True)
class BoxStep:
    """An exact rational witness for one continuous upper supersolution segment."""

    duration: Fraction
    upper_start: State
    upper_end: State
    lower_start: Optional[State]
    lower_end: Optional[State]


@dataclass(frozen=True)
class MomentEnclosure:
    family: str
    phi: Optional[Fraction]
    horizon: Fraction
    rates: tuple[Fraction, Fraction]
    tilt: Fraction
    lower: Optional[State]
    upper: State
    witnesses: tuple[BoxStep, ...]
    precision_bits: int
    mechanism: str = MECHANISM

    @property
    def root_upper(self) -> Fraction:
        return self.upper[0]

    @property
    def root_lower(self) -> Optional[Fraction]:
        return None if self.lower is None else self.lower[0]

    def depth_tail_upper(self, depth: int) -> Fraction:
        """Bound E[H² 1{depth > K}] using the certified E[r^N H²]."""
        if self.tilt <= 1:
            raise ValueError("a depth-tail certificate requires tilt > 1")
        if not isinstance(depth, int) or isinstance(depth, bool) or depth < 0:
            raise ValueError("depth must be a nonnegative integer")
        return self.root_upper / self.tilt**(depth + 1)


def enclose_allen_cahn_moment(
    *, horizon: Rational = "0.05", rates: tuple[Rational, Rational] = ("0.73", "0.73"),
    family: str = "flat", phi: Rational = "0.5", tilt: Rational = 1,
    steps: int = 100, precision_bits: int = 48, max_box_iterations: int = 100,
) -> MomentEnclosure:
    """Enclose full-tree E[r^N H²], uniformly over a rational rate interval.

    Flat data give two-sided enclosures. Wave data give spatially uniform
    upper bounds only. Every time step includes a checkable rational witness.
    The proposal is the raw SemilinearMechanism uniform law, including dead
    alternatives: in particular the live F2 tuple still has probability 1/2.
    """
    T, r = _fraction(horizon), _fraction(tilt)
    lo, hi = map(_fraction, rates)
    if T < 0 or not 0 < lo <= hi or r < 1:
        raise ValueError("require horizon >= 0, 0 < rate_lo <= rate_hi, tilt >= 1")
    for name, value in (("steps", steps), ("precision_bits", precision_bits),
                        ("max_box_iterations", max_box_iterations)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    if family == "flat":
        p = _fraction(phi)
        upper = lower = flat_terminal_state(p)
    elif family == "wave":
        p, lower, upper = None, None, WAVE_TERMINAL_UPPER
    else:
        raise ValueError("family must be 'flat' or 'wave'")
    grid = 2**precision_bits
    h = T / steps
    witnesses = []
    for step_index in range(steps if T else 0):
        start = upper
        end = start
        for _ in range(max_box_iterations):
            next_end = tuple(_round_grid(a + h * f, grid, up=True)
                             for a, f in zip(start, _field(end, hi, r / lo)))
            if next_end == end:
                break
            # Oversized exact integers indicate a failed box, not an infinite moment.
            if any(v.numerator.bit_length() > precision_bits + 512 for v in next_end):
                raise CertificateFailure(f"upper box grew too large at step {step_index}")
            end = next_end
        else:
            raise CertificateFailure(
                f"no postfixed upper box at step {step_index}; increase steps")
        if any(a + h * f > b for a, f, b in zip(start, _field(end, hi, r / lo), end)):
            raise CertificateFailure("internal postfixed witness check failed")
        low_end = (None if lower is None else
                   tuple(_round_grid(a + h * f, grid, up=False)
                         for a, f in zip(lower, _field(lower, lo, r / hi))))
        witnesses.append(BoxStep(h, start, end, lower, low_end))
        upper, lower = end, low_end
    return MomentEnclosure(family, p, T, (lo, hi), r, lower, upper,
                           tuple(witnesses), precision_bits)


def verify_moment_enclosure(certificate: MomentEnclosure) -> bool:
    """Recheck witness inequalities using exact rationals, without the box search.

    This checker verifies the finite numerical certificate. The correspondence
    to the stochastic tree uses the separately documented analytical theorem.
    """
    c = certificate
    def rational_state(value):
        return isinstance(value, tuple) and len(value) == 6 and all(
            isinstance(v, Fraction) for v in value)

    if not all(isinstance(v, Fraction) for v in (c.horizon, c.tilt, *c.rates)):
        return False
    if not rational_state(c.upper) or (c.lower is not None and not rational_state(c.lower)):
        return False
    lo, hi = c.rates
    if (c.mechanism != MECHANISM or c.horizon < 0 or c.tilt < 1 or not 0 < lo <= hi):
        return False
    if c.family == "flat" and c.phi is not None:
        try:
            upper = lower = flat_terminal_state(c.phi)
        except (ValueError, TypeError):
            return False
    elif c.family == "wave" and c.phi is None:
        upper, lower = WAVE_TERMINAL_UPPER, None
    else:
        return False
    elapsed = Fraction(0)
    for w in c.witnesses:
        if (not isinstance(w.duration, Fraction) or not rational_state(w.upper_start) or
                not rational_state(w.upper_end) or
                (w.lower_start is not None and not rational_state(w.lower_start)) or
                (w.lower_end is not None and not rational_state(w.lower_end))):
            return False
        if w.duration <= 0 or w.upper_start != upper or w.lower_start != lower:
            return False
        if len(w.upper_end) != 6 or any(b < a for a, b in zip(upper, w.upper_end)):
            return False
        if any(a + w.duration * f > b for a, f, b in
               zip(upper, _field(w.upper_end, hi, c.tilt / lo), w.upper_end)):
            return False
        if lower is None:
            if w.lower_end is not None:
                return False
        else:
            if w.lower_end is None or len(w.lower_end) != 6:
                return False
            if any(not 0 <= b <= a + w.duration * f for a, f, b in
                   zip(lower, _field(lower, lo, c.tilt / hi), w.lower_end)):
                return False
        elapsed += w.duration
        upper, lower = w.upper_end, w.lower_end
    return elapsed == c.horizon and upper == c.upper and lower == c.lower


def factorial_depth_tail_upper(certificate: MomentEnclosure, depth: int) -> Fraction:
    """Bound ordinary E[H² 1{depth > K}] by a Volterra/Jacobian factorial tail.

    The certificate's endpoint is a uniform box for all earlier times. Exact
    positive matrix products and e^x <= (1-x/m)^(-m), m>x, make the returned
    quantity rational. The analytical tail lemma is in the companion note.
    """
    if not isinstance(depth, int) or isinstance(depth, bool) or depth < 0:
        raise ValueError("depth must be a nonnegative integer")
    if not verify_moment_enclosure(certificate):
        raise ValueError("invalid moment enclosure")
    c = certificate
    _, d, f0, f1, f2, f3 = c.upper
    z = Fraction(0)
    jacobian = (
        (z, z, Fraction(1), z, z, z),
        (z, f1, z, d, z, z),
        (z, d*f2, 2*f1, 2*f0, d*d/2, z),
        (z, d*f3, 2*f2, z, 2*f0, d*d/2),
        (z, z, 2*f3, z, z, 2*f0),
        (z, z, z, z, z, z),
    )
    vector = branch_polynomial(c.upper)
    for _ in range(depth):
        vector = tuple(sum(a*b for a, b in zip(row, vector)) for row in jacobian)
    x = c.rates[1] * c.horizon
    m = max(64, 2 * (x.numerator // x.denominator + 1))
    exp_upper = (1 - x / m)**(-m)
    return exp_upper * (c.horizon / c.rates[0])**(depth+1) / factorial(depth+1) * vector[0]


@dataclass(frozen=True)
class FlatRateCertificate:
    """Full-tree rate certificate, with explicit bounds outside its search interval."""

    interval: tuple[Fraction, Fraction]
    selected_rate: Fraction
    incumbent: MomentEnclosure
    cells: tuple[MomentEnclosure, ...]
    lower_optimum: Fraction
    excess_bound: Fraction
    tolerance: Fraction
    tolerance_met: bool

    @property
    def outside_interval_lower(self) -> tuple[Fraction, Fraction]:
        """Global lower bounds for 0<lambda<=a and lambda>=b, respectively.

        Use root survival plus exactly one branch for small rates and root
        survival alone for large rates. This is specific to flat terminal data.
        """
        p, T = self.incumbent.phi, self.incumbent.horizon
        a, b = self.interval
        return (p*p + T * (p-p**3)**2 / a, p*p * (1 + b*T))

    @property
    def global_lower_optimum(self) -> Fraction:
        return min(self.lower_optimum, *self.outside_interval_lower)

    @property
    def global_excess_bound(self) -> Fraction:
        return self.incumbent.root_upper - self.global_lower_optimum

    @property
    def global_tolerance_met(self) -> bool:
        return self.global_excess_bound <= self.tolerance


def certify_flat_rate(
    *, horizon: Rational = "0.05", phi: Rational = "0.5",
    interval: tuple[Rational, Rational] = ("0.2", "2"),
    candidate: Rational = "0.73", tolerance: Rational = "0.0001",
    steps: int = 100, max_splits: int = 100, precision_bits: int = 48,
) -> FlatRateCertificate:
    """Adaptive interval search with exact lower bounds and a feasible upper bound.

    Exhausting max_splits returns a valid (possibly coarse) excess bound with
    tolerance_met=False. This never converts optimizer stationarity to a proof.
    """
    a, b = map(_fraction, interval)
    chosen, tol = _fraction(candidate), _fraction(tolerance)
    if not a < b or not a <= chosen <= b or tol <= 0:
        raise ValueError("require a < b, candidate in [a,b], tolerance > 0")
    if not isinstance(max_splits, int) or isinstance(max_splits, bool) or max_splits < 0:
        raise ValueError("max_splits must be a nonnegative integer")

    def enclose(l, u):
        return enclose_allen_cahn_moment(horizon=horizon, phi=phi, rates=(l, u),
                                        steps=steps, precision_bits=precision_bits)

    incumbent = enclose(chosen, chosen)
    cells = [enclose(a, b)]
    for _ in range(max_splits):
        index = min(range(len(cells)), key=lambda i: cells[i].root_lower)
        bound = cells[index].root_lower
        if incumbent.root_upper - bound <= tol:
            break
        cell = cells.pop(index)
        l, u = cell.rates
        mid = (l + u) / 2
        point = enclose(mid, mid)
        if point.root_upper < incumbent.root_upper:
            chosen, incumbent = mid, point
        cells.extend((enclose(l, mid), enclose(mid, u)))
    lower = min(c.root_lower for c in cells)
    excess = incumbent.root_upper - lower
    return FlatRateCertificate((a, b), chosen, incumbent,
                               tuple(sorted(cells, key=lambda c: c.rates)),
                               lower, excess, tol, excess <= tol)


def verify_flat_rate_certificate(certificate: FlatRateCertificate) -> bool:
    """Check interval coverage and every numerical witness behind the gap bound."""
    c = certificate
    if (not all(isinstance(v, Fraction) for v in
                (*c.interval, c.selected_rate, c.lower_optimum, c.excess_bound, c.tolerance))
            or c.tolerance <= 0 or c.tolerance_met != (c.excess_bound <= c.tolerance)):
        return False
    if not c.cells or not verify_moment_enclosure(c.incumbent):
        return False
    if c.incumbent.family != "flat" or c.incumbent.tilt != 1:
        return False
    if c.incumbent.rates != (c.selected_rate, c.selected_rate):
        return False
    if not c.interval[0] <= c.selected_rate <= c.interval[1]:
        return False
    left = c.interval[0]
    for cell in c.cells:
        if (cell.family != "flat" or cell.phi != c.incumbent.phi or
                cell.horizon != c.incumbent.horizon or cell.tilt != 1 or
                cell.rates[0] != left or not cell.rates[0] < cell.rates[1] or
                not verify_moment_enclosure(cell)):
            return False
        left = cell.rates[1]
    if left != c.interval[1]:
        return False
    lower = min(cell.root_lower for cell in c.cells)
    return c.lower_optimum == lower and c.excess_bound == c.incumbent.root_upper - lower
