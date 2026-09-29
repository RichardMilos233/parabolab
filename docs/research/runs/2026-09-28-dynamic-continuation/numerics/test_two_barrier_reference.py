"""Checks for the frozen independent two-barrier deterministic reference."""

from __future__ import annotations

import math

import numpy as np

import two_barrier_reference as reference


def test_frozen_shapes_and_normalization() -> None:
    assert reference.TIMES.shape == (7,)
    assert reference.QUERIES.shape == (3,)
    assert reference.STRICT_KEY == "k64_strict"
    assert reference.COMPARATOR_KEY == "k16_loose"
    for max_mode in reference.MAX_MODES:
        system = reference.make_system(max_mode)
        assert system.basis.shape == (8 * max_mode, max_mode + 1)
        assert system.projector.shape == (max_mode + 1, 8 * max_mode)
        coefficients = reference.all_mode_preflight_coefficients(max_mode)
        np.testing.assert_allclose(
            system.project(system.values(coefficients)),
            coefficients,
            rtol=0.0,
            atol=2.0e-14,
        )


def test_all_mode_projection_and_analytic_jacobian_against_convolution() -> None:
    projection, arrays = reference._projection_preflight()
    assert projection["passed"]
    assert projection["maximum_nonlinear_projection_difference"] <= 1.0e-10
    assert projection["maximum_jacobian_entry_difference"] <= 1.0e-10
    assert len(projection["cases"]) == 9
    assert len(arrays) == 45


def test_analytic_jacobian_directional_derivative() -> None:
    system = reference.make_system(16)
    coefficients = reference.all_mode_preflight_coefficients(16)
    direction = np.linspace(-0.2, 0.3, 17)
    epsilon = 1.0e-6
    for time_value in reference.PROJECTION_TIMES:
        finite_difference = (
            system.rhs(time_value, coefficients + epsilon * direction)
            - system.rhs(time_value, coefficients - epsilon * direction)
        ) / (2.0 * epsilon)
        analytic = system.jacobian(time_value, coefficients) @ direction
        np.testing.assert_allclose(finite_difference, analytic, rtol=0.0, atol=2.0e-8)


def test_constant_target_is_stable_and_has_correct_endpoints() -> None:
    for profile in reference.CONSTANT_PROFILES:
        target = reference.exact_scaled_constant(profile)
        assert target.shape == (7,)
        assert math.isclose(target[0], 1.0 - profile, rel_tol=0.0, abs_tol=2.0e-16)
        alpha = profile**-2 - 1.0
        assert abs(target[-1] - alpha / 2.0) < 1.0e-14
        assert np.all(target > 0.0)


def test_frozen_initial_query_values_are_exact() -> None:
    values = reference.evaluate_queries(reference.frozen_initial_coefficients(64))
    np.testing.assert_allclose(values, np.asarray((0.25, 0.375, 0.5)), rtol=0.0, atol=1.0e-16)
    assert math.isclose(reference.QUERIES[1], math.pi / 2.0)
