"""Tests for Dym mechanism verification and deterministic truncated inverse-power integrals."""

from __future__ import annotations

import math

import numpy as np
import pytest

from parabolab import Dx, FNu
from parabolab.integrability import truncated_normal_inverse_power
from parabolab.library import dym_1d


def test_dym_mechanism_exact_singular_tuple():
    pde = dym_1d(alpha=2.0)
    f_star = FNu(1.0, (0, 0, 0, 0))
    singular = (
        FNu(1.0, (0, 0, 1, 0)),
        FNu(1.0, (1, 0, 0, 0)),
        Dx(2),
    )
    assert singular in pde.mechanism.tuples(f_star)
    assert pde.mechanism.terminal(singular[0], pde, 1.25) == pytest.approx(-0.5)
    # f_{z0} = 8*alpha^2/x = 8*(4)/2 = 16.0
    assert pde.mechanism.terminal(singular[1], pde, 2.0) == pytest.approx(16.0)


def test_truncated_normal_inverse_first_power_logarithmic_slope():
    mean = 0.5
    std = 1.2
    # g(0) = 1/(std * sqrt(2*pi)) * exp(-mean^2 / (2*std^2))
    g0 = (1.0 / (std * math.sqrt(2.0 * math.pi))) * math.exp(-(mean**2) / (2.0 * std**2))
    expected_diff = 2.0 * g0 * math.log(100.0)

    eps = 1e-6
    i_coarse = truncated_normal_inverse_power(mean, std, power=1.0, epsilon=eps, outer=2.0)
    i_fine = truncated_normal_inverse_power(mean, std, power=1.0, epsilon=eps / 100.0, outer=2.0)
    actual_diff = i_fine - i_coarse

    assert actual_diff == pytest.approx(expected_diff, rel=1e-3)


def test_truncated_normal_inverse_power_four_thirds_monotone_growth():
    mean = 0.0
    std = 1.0
    cutoffs = [1e-2, 1e-3, 1e-4, 1e-5]
    vals = [
        truncated_normal_inverse_power(mean, std, power=4.0 / 3.0, epsilon=eps, outer=1.0)
        for eps in cutoffs
    ]
    # Check strict monotone increasing as cutoff decreases
    for v1, v2 in zip(vals[:-1], vals[1:]):
        assert v2 > v1


def test_truncated_normal_validation():
    with pytest.raises(ValueError, match="std must be positive"):
        truncated_normal_inverse_power(0.0, 0.0, 1.0, 1e-3)
    with pytest.raises(ValueError, match="power must be positive"):
        truncated_normal_inverse_power(0.0, 1.0, 0.0, 1e-3)
    with pytest.raises(ValueError, match="epsilon must be in"):
        truncated_normal_inverse_power(0.0, 1.0, 1.0, 2.0, outer=1.0)
    with pytest.raises(ValueError, match="log_points must be an odd integer >= 257"):
        truncated_normal_inverse_power(0.0, 1.0, 1.0, 1e-3, outer=1.0, log_points=256)
