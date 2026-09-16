"""Exact weighted-profile evaluation of existing Allen--Cahn wave certificates."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F

from .rate_certificate import Rational, _fraction
from .wave_certificate import (
    WaveMomentCertificate, convex_moment_lower_bounds, verify_wave_moment_certificate,
)


def exponential_interval(value: Rational, *, terms: int = 32) -> tuple[F,F]:
    """Rational bounds from a positive Taylor sum and geometric remainder.

    For r>=0, the terms after r**(N+1)/(N+1)! have successive ratios at
    most r/(N+2). Negative arguments use reciprocal bounds. This is an
    exact enclosure, not rounding a floating-point exponential.
    """
    x = _fraction(value)
    if type(terms) is not int or terms < 0 or abs(x) >= terms+2:
        raise ValueError('require nonnegative integer terms and abs(value) < terms+2')
    if x < 0:
        lo,hi = exponential_interval(-x, terms=terms)
        return 1/hi,1/lo
    term,total = F(1),F(1)
    for k in range(1,terms+1):
        term *= x/k
        total += term
    next_term = term*x/(terms+1)
    return total,total+next_term/(1-x/(terms+2))


def logistic_coordinate_interval(position: Rational, *, terms: int = 32) -> tuple[F,F]:
    """Enclose the wave coordinate s=1/(1+exp(x)) at an exact rational x."""
    lower,upper = exponential_interval(position,terms=terms)
    return 1/(1+upper),1/(1+lower)


def _polynomial_interval(coefficients, interval):
    """Exact interval Horner evaluation, allowing signed coefficients."""
    lo,hi = F(0),F(0)
    left,right = interval
    for coefficient in reversed(coefficients):
        products = (lo*left,lo*right,hi*left,hi*right)
        lo,hi = min(products)+coefficient,max(products)+coefficient
    return lo,hi


def _profile_spec(positions,weights=None):
    positions = tuple(map(_fraction,positions))
    weights = (F(1),)*len(positions) if weights is None else tuple(map(_fraction,weights))
    if (not positions or len(positions) != len(weights)
            or any(w < 0 for w in weights) or sum(weights) <= 0):
        raise ValueError('require a nonempty rational profile and nonnegative nonzero matching weights')
    return positions,tuple(w/sum(weights) for w in weights)


def wave_profile_interval(
    certificate: WaveMomentCertificate, positions, *, weights=None, exp_terms: int = 32,
) -> tuple[F,F]:
    """Evaluate an already verified uniform wave certificate on rational x's.

    The supplied certificate must be valid; use the complete profile verifier
    when reading untrusted stored evidence. Exact coordinate enclosures and
    interval polynomial evaluation supplement its uniform residual bound.
    """
    positions,weights = _profile_spec(positions,weights)
    trial = certificate.polynomial[0]
    coefficients = tuple(sum(p[j] if j < len(p) else F(0) for p in trial)
                         for j in range(max(map(len,trial))))
    lower,upper = F(0),F(0)
    for x,w in zip(positions,weights):
        if not w:
            continue
        lo,hi = _polynomial_interval(coefficients,logistic_coordinate_interval(x,terms=exp_terms))
        lower += w*max(F(0),lo-certificate.error[0])
        upper += w*(hi+certificate.error[0])
    return lower,upper


def wave_profile_mean_square_interval(horizon: Rational, positions, *, weights=None, exp_terms=32):
    """Enclose the weighted squared mean at the given remaining horizon.

    The squared mean is [1/(1+exp(x-3*horizon/2))]^2. Identification with
    the tree mean uses the conventional Allen--Cahn mean theorem.
    """
    T = _fraction(horizon)
    if T < 0:
        raise ValueError('horizon must be nonnegative')
    positions,weights = _profile_spec(positions,weights)
    lower,upper = F(0),F(0)
    for x,w in zip(positions,weights):
        lo,hi = logistic_coordinate_interval(x-3*T/2,terms=exp_terms)
        lower,upper = lower+w*lo*lo,upper+w*hi*hi
    return lower,upper


@dataclass(frozen=True)
class ProfileRateCertificate:
    """Full-tree weighted-profile gap for a common positive rate at every root."""

    points: tuple[WaveMomentCertificate,...]
    positions: tuple[F,...]
    weights: tuple[F,...]
    exp_terms: int = 32

    def moment_interval(self,point: WaveMomentCertificate):
        if not self.points or point.moment_box.horizon != self.points[0].moment_box.horizon:
            raise ValueError('point certificate must have the same horizon as the profile')
        return wave_profile_interval(point,self.positions,weights=self.weights,exp_terms=self.exp_terms)

    @property
    def incumbent(self):
        return min(self.points,key=lambda p:self.moment_interval(p)[1])

    @property
    def lower_bounds(self):
        return convex_moment_lower_bounds(tuple((p.rate,*self.moment_interval(p)) for p in self.points))

    @property
    def global_lower(self):
        cells,exterior = self.lower_bounds
        return min(*cells,*exterior)

    @property
    def global_gap(self):
        return self.moment_interval(self.incumbent)[1]-self.global_lower


    def interpolated_moment_upper(self,rate: Rational):
        """Upper-bound an intermediate rate by convex interpolation.

        This covers exact binary-float policy rates supplied explicitly as
        Fraction.from_float(value), using certified endpoint moments. Unlike
        secant lower bounds, this upper bound is valid inside a sampled pair.
        """
        rate = _fraction(rate)
        if not self.points[0].rate <= rate <= self.points[-1].rate:
            raise ValueError('interpolated rate must lie between certified samples')
        for left,right in zip(self.points,self.points[1:]):
            if left.rate <= rate <= right.rate:
                weight = (rate-left.rate)/(right.rate-left.rate)
                return ((1-weight)*self.moment_interval(left)[1]
                        +weight*self.moment_interval(right)[1])
        raise ValueError('require at least two ordered certificate points')


    @property
    def mean_square_interval(self):
        return wave_profile_mean_square_interval(self.points[0].moment_box.horizon,
            self.positions,weights=self.weights,exp_terms=self.exp_terms)

    def variance_interval(self,point):
        lo,hi = self.moment_interval(point)
        mean_lo,mean_hi = self.mean_square_interval
        return max(F(0),lo-mean_hi),hi-mean_lo

    @property
    def variance_optimum_lower(self):
        return max(F(0),self.global_lower-self.mean_square_interval[1])

    @property
    def relative_gap_upper(self):
        lower = self.variance_optimum_lower
        return None if lower <= 0 else self.global_gap/lower


def verify_profile_rate_certificate(c: ProfileRateCertificate) -> bool:
    if (len(c.points) < 2 or type(c.exp_terms) is not int or c.exp_terms < 0
            or not isinstance(c.positions,tuple) or not isinstance(c.weights,tuple)
            or not c.positions or len(c.positions) != len(c.weights)
            or any(type(v) is not F for v in (*c.positions,*c.weights))
            or any(w < 0 for w in c.weights) or sum(c.weights) != 1
            or any(abs(x) >= c.exp_terms+2 for x in c.positions)
            or any(not verify_wave_moment_certificate(p) for p in c.points)
            or any(p.moment_box.horizon != c.points[0].moment_box.horizon for p in c.points)
            or any(abs(x-3*c.points[0].moment_box.horizon/2) >= c.exp_terms+2 for x in c.positions)
            or any(a.rate >= b.rate for a,b in zip(c.points,c.points[1:]))):
        return False
    return c.global_gap >= 0
