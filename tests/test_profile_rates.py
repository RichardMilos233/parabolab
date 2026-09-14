"""Profile objective controls independent of the scalar optimization algorithm."""

import math
import numpy as np
import pytest

from parabolab.library import allen_cahn_wave_1d, allen_cahn_flat
from parabolab.moments import MomentQuadrature
from parabolab.profile_rates import (
    short_time_profile_rate, profile_moment_derivatives_1d, optimize_profile_rate_1d,
)
from parabolab.rate_optimization import (
    finite_depth_moment_derivatives_1d, optimize_exponential_rate_1d, RateMomentDerivatives,
)


def test_profile_short_time_matches_formula_and_differs_from_root():
    pde = allen_cahn_wave_1d(T=.05)
    grid = [-2,-1,0,1,2]
    expected = math.sqrt(sum(pde.f(pde.phi(x))**2 for x in grid)/sum(pde.phi(x)**2 for x in grid))
    assert short_time_profile_rate(pde,grid) == pytest.approx(expected)
    assert expected == pytest.approx(.47496956016576364)
    assert short_time_profile_rate(pde,[0]) == pytest.approx(.75)
    assert short_time_profile_rate(pde,grid,[0,0,1,0,0]) == pytest.approx(.75)


def test_weighted_moment_and_derivatives_equal_independent_point_sum():
    pde = allen_cahn_wave_1d(T=.05)
    options = dict(max_depth=1,rate=.5,quadrature=MomentQuadrature(3,3))
    result = profile_moment_derivatives_1d(pde,0,[-1,1],weights=[3,1],**options)
    a,b = [finite_depth_moment_derivatives_1d(pde,0,x,**options) for x in (-1,1)]
    for field in ('value','d_rate','d2_rate'):
        assert getattr(result,field) == pytest.approx((3*getattr(a,field)+getattr(b,field))/4)
    h=1e-4
    lower = profile_moment_derivatives_1d(pde,0,[-1,1],weights=[3,1],**{**options,'rate':.5-h})
    upper = profile_moment_derivatives_1d(pde,0,[-1,1],weights=[3,1],**{**options,'rate':.5+h})
    assert result.d_rate == pytest.approx((upper.value-lower.value)/(2*h),abs=1e-8)
    assert result.d2_rate == pytest.approx((upper.d_rate-lower.d_rate)/(2*h),abs=1e-7)


def test_singleton_and_constant_profile_agree_with_existing_selector():
    pde = allen_cahn_flat(T=.05)
    options = dict(max_depth=2,bracket=(.2,2),tol=1e-7,quadrature=MomentQuadrature(3,1))
    old = optimize_exponential_rate_1d(pde,0,0,**options)
    one = optimize_profile_rate_1d(pde,0,[0],**options)
    many = optimize_profile_rate_1d(pde,0,[-2,0,2],weights=[1e300,1e300,1e300],**options)
    assert one.rate == pytest.approx(old.rate,abs=1e-10)
    assert many.rate == pytest.approx(one.rate,abs=1e-10)
    assert many.second_moment == pytest.approx(one.second_moment)


def test_profile_quadratic_control_and_constrained_endpoints(monkeypatch):
    import parabolab.profile_rates as module
    def control(pde,t,x,*,rate,**kwargs):
        return RateMomentDerivatives(1+(rate-x)**2,2*(rate-x),2)
    monkeypatch.setattr(module,'finite_depth_moment_derivatives_1d',control)
    pde = allen_cahn_wave_1d()
    result = optimize_profile_rate_1d(pde,0,[.4,.8],weights=[3,1],bracket=(.1,2))
    assert result.rate == pytest.approx(.5)
    assert result.converged
    assert optimize_profile_rate_1d(pde,0,[.4,.8],bracket=(.9,2)).rate == .9
    assert optimize_profile_rate_1d(pde,0,[.4,.8],bracket=(.1,.3)).rate == .3
    assert not optimize_profile_rate_1d(pde,0,[.4,.8],max_iter=1).converged


@pytest.mark.parametrize('grid,weights', [([],None),([0,1],[1]),([0,1],[0,0]),
    ([0,1],[1,-1]),([0,float('nan')],None),([[0],[1]],None)])
def test_invalid_profiles_rejected(grid,weights):
    with pytest.raises(ValueError):
        short_time_profile_rate(allen_cahn_wave_1d(),grid,weights)


def test_degenerate_heuristic_requires_explicit_policy():
    with pytest.raises(ValueError,match='degenerate'):
        short_time_profile_rate(allen_cahn_flat(phi0=1),[0])
