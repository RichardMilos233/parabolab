"""Independent coordinate controls and weighted certificate consistency checks."""

from dataclasses import replace
from decimal import Decimal, localcontext
from fractions import Fraction as F

import pytest

from parabolab.profile_certificate import (
    ProfileRateCertificate, _polynomial_interval, exponential_interval,
    logistic_coordinate_interval, verify_profile_rate_certificate, wave_profile_interval,
    wave_profile_mean_square_interval,
)
from parabolab.wave_certificate import enclose_wave_moment


@pytest.fixture(scope='module')
def point():
    return enclose_wave_moment(degree=3,spatial_splits=1,error_steps=40)


@pytest.mark.parametrize('x', [-2,-1,0,1,2])
def test_exponential_enclosures_contain_high_precision_reference(x):
    lo,hi = exponential_interval(x)
    with localcontext() as context:
        context.prec = 80
        actual = Decimal(x).exp()
        convert = lambda q:Decimal(q.numerator)/Decimal(q.denominator)
        assert convert(lo) <= actual <= convert(hi)
        a,b = logistic_coordinate_interval(x)
        actual_s = 1/(1+actual)
        assert convert(a) <= actual_s <= convert(b)
    assert hi-lo < F(1,10**26)


def test_reciprocal_and_zero_controls():
    assert exponential_interval(0) == (1,1)
    assert logistic_coordinate_interval(0) == (F(1,2),F(1,2))
    lo,hi = exponential_interval(2,terms=8)
    assert exponential_interval(-2,terms=8) == (1/hi,1/lo)
    with pytest.raises(ValueError):
        exponential_interval(2,terms=0)
    with pytest.raises(TypeError):
        logistic_coordinate_interval(0.5)


def test_signed_interval_horner_covers_polynomial_extremum():
    # The extremum of s-s² is interior; checking endpoints alone is unsound.
    lo,hi = _polynomial_interval((F(0),F(1),F(-1)),(F(1,4),F(3,4)))
    assert lo <= F(3,16) <= F(1,4) <= hi
    assert _polynomial_interval((F(2),F(-3)),(F(-1),F(2))) == (-4,5)


def test_profile_interval_matches_singleton_and_weighted_point_enclosures(point):
    assert wave_profile_interval(point,[0]) == point.moment_at()
    intervals = [wave_profile_interval(point,[x]) for x in (-1,1)]
    profile = wave_profile_interval(point,[-1,1],weights=[3,1])
    assert profile == tuple((3*a+b)/4 for a,b in zip(*intervals))
    assert wave_profile_interval(point,[-1,1],weights=[30,10]) == profile
    assert wave_profile_interval(point,[-1,0,1],weights=[0,1,0]) == point.moment_at()


def test_profile_verifier_checks_weights_rate_order_and_coordinate_precision(point):
    right = enclose_wave_moment(rate='.8',degree=3,spatial_splits=1,error_steps=40)
    c = ProfileRateCertificate((point,right),(F(-1),F(1)),(F(1,2),F(1,2)))
    assert verify_profile_rate_certificate(c)
    assert c.global_gap >= 0
    assert not verify_profile_rate_certificate(replace(c,weights=(F(1),F(1))))
    assert not verify_profile_rate_certificate(replace(c,positions=(F(35),F(1))))
    assert not verify_profile_rate_certificate(replace(c,points=(right,point)))
    assert not verify_profile_rate_certificate(replace(c,positions=(0.0,F(1))))
    midpoint=(point.rate+right.rate)/2
    assert c.interpolated_moment_upper(midpoint)==sum(c.moment_interval(p)[1] for p in c.points)/2
    assert c.interpolated_moment_upper(F.from_float(.75))>=0
    with pytest.raises(ValueError,match='between'):
        c.interpolated_moment_upper(F(1))


def test_exact_wave_mean_control_and_variance_subtraction(point):
    assert wave_profile_mean_square_interval(0,[0]) == (F(1,4),F(1,4))
    assert wave_profile_mean_square_interval(F(1,20),[F(3,40)]) == (F(1,4),F(1,4))
    c = ProfileRateCertificate((point,),(F(0),),(F(1),))
    lo,hi = c.variance_interval(point)
    mlo,mhi = c.moment_interval(point)
    alo,ahi = c.mean_square_interval
    assert lo == max(0,mlo-ahi) and hi == mhi-alo


def test_different_horizon_cannot_be_used_with_profile_mean(point):
    c = ProfileRateCertificate((point,),(F(0),),(F(1),))
    other = enclose_wave_moment(horizon='.001',degree=1,spatial_splits=0,error_steps=20)
    with pytest.raises(ValueError,match='same horizon'):
        c.variance_interval(other)
    with pytest.raises(ValueError,match='same horizon'):
        c.moment_interval(other)
