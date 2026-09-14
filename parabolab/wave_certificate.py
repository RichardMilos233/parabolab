"""Exact polynomial residual certificates for the 1D Allen--Cahn wave.

The coordinate is s = 1/(1+exp(x)), time is z = (T-t)/T. All arithmetic
below is rational. The analytical link to full-tree moments is documented
in docs/research/estimator-integrity/wave-numerical-certification-route.md.
This is specific to the raw uniform semilinear mechanism, not custom q.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from math import comb

from parabolab.rate_certificate import (
    CertificateFailure, MomentEnclosure, Rational, State, _fraction, _round_grid,
    enclose_allen_cahn_moment, verify_moment_enclosure,
)


Polynomial = tuple[F, ...]  # ascending powers of s
Series = tuple[Polynomial, ...]  # ascending powers of z
ZERO = (F(0),)
WAVE_TERMINAL_POLYNOMIALS = tuple(tuple(map(F, p)) for p in (
    (0, 0, 1), (0, 0, 1, -2, 1), (0, 0, 1, 0, -2, 0, 1),
    (1, 0, -6, 0, 9), (0, 0, 36), (36,),
))


def _trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def _add(*polynomials):
    out = [F(0)] * max(map(len, polynomials))
    for p in polynomials:
        for j, value in enumerate(p):
            out[j] += value
    return _trim(out)


def _scale(p, factor):
    return _trim(value * factor for value in p)


def _mul(*polynomials):
    out = (F(1),)
    for p in polynomials:
        product = [F(0)] * (len(out) + len(p) - 1)
        for i, a in enumerate(out):
            for j, b in enumerate(p):
                product[i + j] += a * b
        out = _trim(product)
    return out


def _derivative(p):
    return tuple(j * p[j] for j in range(1, len(p))) or ZERO


def _diffusion(p):
    """Half the x-Laplacian after s=1/(1+exp(x))."""
    dp = _derivative(p)
    return _scale(_add(_mul((0, 1, -3, 2), dp),
                       _mul((0, 0, 1, -2, 1), _derivative(dp))), F(1, 2))


def _branch_coefficient(y, n):
    def get(i, j):
        return y[i][j] if j < len(y[i]) else ZERO

    def two(i, j):
        return _add(*(_mul(get(i, k), get(j, n-k)) for k in range(n+1)))

    def three(i, j, k):
        return _add(*(_mul(get(i, a), get(j, b), get(k, n-a-b))
                      for a in range(n+1) for b in range(n-a+1)))

    return (get(2, n), two(3, 1),
            _add(_scale(two(2, 3), 2), _scale(three(1, 1, 4), F(1, 2))),
            _add(_scale(two(2, 4), 2), _scale(three(1, 1, 5), F(1, 2))),
            _scale(two(2, 5), 2), ZERO)


def wave_trial_polynomial(rate: F, horizon: F, degree: int) -> tuple[Series, ...]:
    """Finite formal Taylor trial; no infinite-series convergence is assumed."""
    rate, horizon = _fraction(rate), _fraction(horizon)
    if rate <= 0 or horizon <= 0 or type(degree) is not int or degree < 0:
        raise ValueError('require positive rate/horizon and nonnegative integer degree')
    y = [[p] for p in WAVE_TERMINAL_POLYNOMIALS]
    for n in range(degree):
        branch = _branch_coefficient(y, n)
        for i in range(6):
            y[i].append(_scale(_add(_diffusion(y[i][n]), _scale(y[i][n], rate),
                                        _scale(branch[i], 1/rate)), horizon/(n+1)))
    return tuple(tuple(p) for p in y)


def wave_residual(polynomial: tuple[Series, ...], rate: F, horizon: F):
    """Return (1/T) P_z - L P - lambda P - G(P)/lambda exactly."""
    degree = max(len(p) for p in polynomial) - 1
    result = [[] for _ in range(6)]
    for n in range(3*degree + 1):
        branch = _branch_coefficient(polynomial, n)
        for i, series in enumerate(polynomial):
            current = series[n] if n < len(series) else ZERO
            dt = _scale(series[n+1], F(n+1)/horizon) if n+1 < len(series) else ZERO
            result[i].append(_add(dt, _scale(_diffusion(current), -1),
                                   _scale(current, -rate), _scale(branch[i], -1/rate)))
    for series in result:
        while len(series) > 1 and series[-1] == ZERO:
            series.pop()
    return tuple(tuple(p) for p in result)


def _bernstein(series: Series):
    """Tensor-product power-to-Bernstein conversion on [0,1]^2."""
    nt, ns = len(series)-1, max(map(len, series))-1
    ratios = [[F(comb(k, j), comb(ns, j)) for j in range(k+1)] for k in range(ns+1)]
    spatial = [[sum(p[j]*ratios[k][j] for j in range(min(k+1, len(p))))
                for k in range(ns+1)] for p in series]
    return tuple(tuple(sum(spatial[j][k]*F(comb(l, j), comb(nt, j))
                           for j in range(l+1)) for k in range(ns+1))
                 for l in range(nt+1))


def _bisect_bernstein_row(row):
    left, right = [row[0]], [row[-1]]
    while len(row) > 1:
        row = tuple((a+b)/2 for a, b in zip(row, row[1:]))
        left.append(row[0])
        right.append(row[-1])
    return tuple(left), tuple(reversed(right))


def bernstein_absolute_bound(series: Series, spatial_splits: int = 2) -> F:
    """Certified supremum bound after exact dyadic spatial subdivision."""
    if type(spatial_splits) is not int or spatial_splits < 0:
        raise ValueError('spatial_splits must be a nonnegative integer')
    cells = [_bernstein(series)]
    for _ in range(spatial_splits):
        children = []
        for cell in cells:
            rows = [_bisect_bernstein_row(row) for row in cell]
            children.extend((tuple(r[0] for r in rows), tuple(r[1] for r in rows)))
        cells = children
    return max(abs(value) for cell in cells for row in cell for value in row)


def _error_matrix(box: State, rate: F):
    _, d, a, b, c, e = box
    z = F(0)
    jacobian = ((z,z,1,z,z,z), (z,b,z,d,z,z), (z,d*c,2*b,2*a,d*d/2,z),
                (z,d*e,2*c,z,2*a,d*d/2), (z,z,2*e,z,z,2*a), (z,z,z,z,z,z))
    return tuple(tuple(v/rate + (rate if i == j else 0)
                       for j, v in enumerate(row)) for i, row in enumerate(jacobian))


def _error_field(matrix, residual, error):
    return tuple(rho + sum(a*v for a, v in zip(row, error))
                 for rho, row in zip(residual, matrix))


@dataclass(frozen=True)
class ErrorStep:
    duration: F
    start: State
    end: State


@dataclass(frozen=True)
class WaveMomentCertificate:
    rate: F
    moment_box: MomentEnclosure
    polynomial: tuple[Series, ...]
    magnitude: State
    residual: State
    error_steps: tuple[ErrorStep, ...]
    spatial_splits: int

    @property
    def error(self) -> State:
        return self.error_steps[-1].end

    def moment_at(self, coordinate: Rational = '0.5') -> tuple[F, F]:
        """Root moment enclosure at s=1/(1+exp(x)); x=0 means s=1/2."""
        s = _fraction(coordinate)
        if not 0 <= s <= 1:
            raise ValueError('wave coordinate must lie in [0,1]')
        value = sum(sum(a*s**j for j, a in enumerate(p)) for p in self.polynomial[0])
        return max(F(0), value-self.error[0]), value+self.error[0]


def enclose_wave_moment(
    *, rate: Rational = '0.73', horizon: Rational = '0.05', degree: int = 5,
    spatial_splits: int = 2, error_steps: int = 100, precision_bits: int = 60,
    moment_box: MomentEnclosure | None = None,
) -> WaveMomentCertificate:
    """Certify the full-tree moment with a finite polynomial and its residual."""
    lam, T = _fraction(rate), _fraction(horizon)
    for name, value in (('error_steps', error_steps), ('precision_bits', precision_bits)):
        if type(value) is not int or value < 1:
            raise ValueError(f'{name} must be a positive integer')
    if moment_box is None:
        moment_box = enclose_allen_cahn_moment(family='wave', horizon=T,
                                              rates=(lam, lam), steps=200)
    if (not verify_moment_enclosure(moment_box) or moment_box.family != 'wave'
            or moment_box.horizon != T or moment_box.tilt != 1
            or not moment_box.rates[0] <= lam <= moment_box.rates[1]):
        raise ValueError('moment_box must certify this wave, time, and rate')
    trial = wave_trial_polynomial(lam, T, degree)
    magnitude = tuple(bernstein_absolute_bound(p, spatial_splits) for p in trial)
    residual = tuple(bernstein_absolute_bound(p, spatial_splits)
                     for p in wave_residual(trial, lam, T))
    box = tuple(max(a,b) for a,b in zip(moment_box.upper, magnitude))
    matrix, h, error = _error_matrix(box, lam), T/error_steps, (F(0),)*6
    witnesses = []
    for _ in range(error_steps):
        end = error
        for _ in range(100):
            next_end = tuple(_round_grid(a+h*f, 2**precision_bits, up=True)
                             for a,f in zip(error, _error_field(matrix, residual, end)))
            if next_end == end:
                break
            end = next_end
        else:
            raise CertificateFailure('linear error box inconclusive; increase error_steps')
        witnesses.append(ErrorStep(h, error, end))
        error = end
    return WaveMomentCertificate(lam, moment_box, trial, magnitude, residual,
                                  tuple(witnesses), spatial_splits)


def verify_wave_moment_certificate(c: WaveMomentCertificate) -> bool:
    """Recompute residual bounds and recheck witnesses, without Taylor generation."""
    def state(value):
        return isinstance(value, tuple) and len(value) == 6 and all(type(v) is F for v in value)

    if (type(c.rate) is not F or type(c.spatial_splits) is not int or c.spatial_splits < 0
            or not verify_moment_enclosure(c.moment_box) or c.moment_box.family != 'wave'
            or c.moment_box.tilt != 1 or c.moment_box.horizon <= 0
            or not c.moment_box.rates[0] <= c.rate <= c.moment_box.rates[1]
            or not state(c.magnitude) or not state(c.residual) or not c.error_steps):
        return False
    if not isinstance(c.polynomial, tuple) or len(c.polynomial) != 6:
        return False
    for series, initial in zip(c.polynomial, WAVE_TERMINAL_POLYNOMIALS):
        if not isinstance(series, tuple) or not series:
            return False
        if any(not isinstance(p, tuple) or not p or any(type(v) is not F for v in p)
               for p in series) or series[0] != initial:
            return False
    if any(bound < bernstein_absolute_bound(p, c.spatial_splits)
           for bound, p in zip(c.magnitude, c.polynomial)):
        return False
    if any(bound < bernstein_absolute_bound(p, c.spatial_splits)
           for bound, p in zip(c.residual, wave_residual(c.polynomial, c.rate, c.moment_box.horizon))):
        return False
    box = tuple(max(a,b) for a,b in zip(c.moment_box.upper, c.magnitude))
    matrix = _error_matrix(box, c.rate)
    elapsed, error = F(0), (F(0),)*6
    for step in c.error_steps:
        if (type(step.duration) is not F or step.duration <= 0 or not state(step.start)
                or not state(step.end) or step.start != error):
            return False
        field = _error_field(matrix, c.residual, step.end)
        if any(b < a or b < a+step.duration*f for a,b,f in zip(error, step.end, field)):
            return False
        elapsed, error = elapsed+step.duration, step.end
    return elapsed == c.moment_box.horizon


def convex_moment_lower_bounds(points: tuple[tuple[F, F, F], ...]):
    """Exact lower bounds for a nonnegative convex function given (x, L, U).

    Secants are extrapolated only outside their two defining points. Returns
    one bound per consecutive cell and two bounds for the exterior rays.
    Convexity and interval validity are analytical assumptions of this helper.
    """
    if (len(points) < 2 or any(not all(type(v) is F for v in point) for point in points)
            or any(not 0 <= l <= u or x <= 0 for x,l,u in points)
            or any(a[0] >= b[0] for a,b in zip(points, points[1:]))):
        raise ValueError('require ordered positive nodes and nonnegative rational intervals')
    cells = []
    for i in range(len(points)-1):
        a, b = points[i][0], points[i+1][0]
        lines = [(F(0), F(0))]  # nonnegativity
        if i > 0:
            x0, _, u0 = points[i-1]
            x1, l1, _ = points[i]
            slope = (l1-u0)/(x1-x0)
            lines.append((slope, l1-slope*x1))
        if i+2 < len(points):
            x0, l0, _ = points[i+1]
            x1, _, u1 = points[i+2]
            slope = (u1-l0)/(x1-x0)
            lines.append((slope, l0-slope*x0))
        candidates = [a, b]
        for j,(m,c) in enumerate(lines):
            for n,d in lines[j+1:]:
                if m != n and a <= (d-c)/(m-n) <= b:
                    candidates.append((d-c)/(m-n))
        cells.append(min(max(m*x+c for m,c in lines) for x in candidates))
    left = points[0][1] if points[1][2] <= points[0][1] else F(0)
    right = points[-1][1] if points[-2][2] <= points[-1][1] else F(0)
    return tuple(cells), (left, right)


@dataclass(frozen=True)
class WaveRateCertificate:
    points: tuple[WaveMomentCertificate, ...]
    coordinate: F = F(1, 2)

    @property
    def incumbent(self) -> WaveMomentCertificate:
        return min(self.points, key=lambda c: c.moment_at(self.coordinate)[1])

    @property
    def lower_bounds(self):
        return convex_moment_lower_bounds(tuple((c.rate, *c.moment_at(self.coordinate))
                                                for c in self.points))

    @property
    def global_lower(self) -> F:
        cells, exterior = self.lower_bounds
        return min(*cells, *exterior)

    @property
    def global_gap(self) -> F:
        return self.incumbent.moment_at(self.coordinate)[1] - self.global_lower


def verify_wave_rate_certificate(c: WaveRateCertificate) -> bool:
    if (type(c.coordinate) is not F or not 0 <= c.coordinate <= 1 or len(c.points) < 2
            or any(not verify_wave_moment_certificate(p) for p in c.points)
            or any(p.moment_box.horizon != c.points[0].moment_box.horizon for p in c.points)
            or any(a.rate >= b.rate for a,b in zip(c.points, c.points[1:]))):
        return False
    return c.global_gap >= 0
