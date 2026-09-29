"""Meaningful checks for the independent Galerkin reference."""

from __future__ import annotations

import math

import numpy as np

import reference


def _convolve(left: dict[int, complex], right: dict[int, complex]) -> dict[int, complex]:
    result: dict[int, complex] = {}
    for left_mode, left_value in left.items():
        for right_mode, right_value in right.items():
            mode = left_mode + right_mode
            result[mode] = result.get(mode, 0.0j) + left_value * right_value
    return result


def _exact_cubic_projection(coefficients: np.ndarray, modes: np.ndarray) -> np.ndarray:
    """Finite complex-Fourier convolution, independent of grid quadrature."""

    fourier: dict[int, complex] = {}
    for mode, coefficient in zip(modes, coefficients):
        fourier[int(mode)] = -1j * coefficient / math.sqrt(2.0)
        fourier[-int(mode)] = 1j * coefficient / math.sqrt(2.0)
    cubic = _convolve(_convolve(fourier, fourier), fourier)
    projected = []
    for mode in modes:
        positive = cubic.get(int(mode), 0.0j)
        negative = cubic.get(-int(mode), 0.0j)
        value = (-1j / math.sqrt(2.0)) * negative + (
            1j / math.sqrt(2.0)
        ) * positive
        projected.append(float(value.real))
        assert abs(value.imag) < 1.0e-14
    return np.asarray(projected)


def test_periodic_quadrature_matches_exact_cubic_convolution() -> None:
    rng = np.random.default_rng(20260928)
    for max_mode in reference.MAX_MODES:
        system = reference.make_system(max_mode)
        coefficients = rng.normal(scale=0.04, size=system.modes.size)
        exact = _exact_cubic_projection(coefficients, system.modes)
        actual = system.cubic_coefficients(coefficients)
        np.testing.assert_allclose(actual, exact, rtol=0.0, atol=2.0e-14)


def test_stationary_profile_has_small_rhs_and_solver_drift() -> None:
    _, basis, g_values = reference.comparison_data()
    system = reference.make_system(63)
    g_coefficients = reference.project(g_values, basis)
    assert np.linalg.norm(system.rhs(0.0, g_coefficients)) < 2.0e-12

    tolerance = reference.TOLERANCES["strict"]
    solution = reference.solve_ivp(
        system.rhs,
        (0.0, 0.4),
        g_coefficients,
        method="DOP853",
        t_eval=np.asarray((0.0, 0.08, 0.4)),
        rtol=tolerance["rtol"],
        atol=tolerance["atol"],
    )
    assert solution.success
    drift = np.linalg.norm(solution.y.T - g_coefficients, axis=1)
    assert float(np.max(drift)) < 2.0e-11


def test_initial_rhs_matches_exact_profile_identity() -> None:
    _, basis, g_values = reference.comparison_data()
    system = reference.make_system(63)
    initial = reference.initial_coefficients(63, basis, g_values)
    actual = system.rhs(0.0, initial)
    expected = reference.project((0.9 - 0.9**3) * g_values**3, basis)
    np.testing.assert_allclose(actual, expected, rtol=0.0, atol=2.0e-12)


def test_fixed_protocol_shapes_and_quadrature_conditions() -> None:
    assert reference.TIMES.shape == (201,)
    assert reference.TIMES[0] == 0.0
    assert reference.TIMES[-1] == 16.0
    np.testing.assert_array_equal(reference.odd_modes(63), np.arange(1, 64, 2))
    for max_mode in reference.MAX_MODES:
        system = reference.make_system(max_mode)
        assert system.n_grid > 4 * max_mode
        assert system.basis.shape == (
            reference.QUADRATURE_SIZES[max_mode],
            (max_mode + 1) // 2,
        )
