"""Fixed two-coefficient interface for the dynamic continuation experiment."""

from __future__ import annotations

import math
from typing import Sequence

import mpmath as mp
import numpy as np
from scipy import special


PARAMETER_M = 1.0 / 20.0
A = 2.0 / 21.0
AMPLITUDE = math.sqrt(A)
KAPPA = math.sqrt(40.0 / 21.0)
PERIOD = 4.0 * float(special.ellipk(PARAMETER_M)) / KAPPA
SLOPE_WIDTH = 2.0 / 735.0
LOWER = 0.9
UPPER = 1.0

# Rounded only after the independent 80-decimal elliptic-identity and quadrature
# calculations.  compute_gram_audit reproduces both calculations.
GRAM = np.array(
    [
        [0.0059329342220773405, 0.0059710936464823295],
        [0.0059710936464823295, 0.030049232873579173],
    ],
    dtype=float,
)

VERTICES = np.array(
    [
        (LOWER, LOWER),
        (LOWER + SLOPE_WIDTH, LOWER),
        (UPPER, UPPER - SLOPE_WIDTH),
        (UPPER, UPPER),
        (UPPER - SLOPE_WIDTH, UPPER),
        (LOWER, LOWER + SLOPE_WIDTH),
    ],
    dtype=float,
)


def g_and_derivative(x):
    """Evaluate the fixed Jacobi profile and its analytic derivative."""
    points = np.asarray(x, dtype=float)
    sn, cn, dn, _ = special.ellipj(KAPPA * points, PARAMETER_M)
    values = AMPLITUDE * sn
    derivatives = AMPLITUDE * KAPPA * cn * dn
    if points.ndim == 0:
        return float(values), float(derivatives)
    return values, derivatives


def basis_values(x) -> np.ndarray:
    """Return (b0,b1) at x, with the coefficient normalization from the plan."""
    values = np.asarray(g_and_derivative(x)[0], dtype=float)
    ratio = values**2 / A
    return np.stack((values * (1.0 - ratio), values * ratio), axis=-1)


def is_feasible(coefficients: Sequence[float], tolerance: float = 0.0) -> bool:
    c = np.asarray(coefficients, dtype=float)
    return bool(
        c.shape == (2,)
        and np.all(np.isfinite(c))
        and np.all(c >= LOWER - tolerance)
        and np.all(c <= UPPER + tolerance)
        and abs(float(c[1] - c[0])) <= SLOPE_WIDTH + tolerance
    )


def interface_terminal(coefficients: Sequence[float]):
    """Freeze one feasible coefficient pair into a value/derivative callback."""
    frozen = np.array(coefficients, dtype=float, copy=True)
    if not is_feasible(frozen, tolerance=2.0e-14):
        raise ValueError("coefficients must lie in the fixed admissible hexagon")
    frozen.setflags(write=False)

    def terminal(x):
        g, gp = g_and_derivative(x)
        g_array = np.asarray(g, dtype=float)
        gp_array = np.asarray(gp, dtype=float)
        ratio = g_array**2 / A
        value = g_array * (frozen[0] + (frozen[1] - frozen[0]) * ratio)
        derivative = gp_array * (
            frozen[0] + 3.0 * (frozen[1] - frozen[0]) * ratio
        )
        if g_array.ndim == 0:
            return float(value), float(derivative)
        return value, derivative

    return terminal


def _metric_squared(left: np.ndarray, right: np.ndarray) -> float:
    difference = left - right
    return float(difference @ GRAM @ difference)


def project_gram(raw_coefficients: Sequence[float]) -> tuple[np.ndarray, dict]:
    """Project onto the hexagon by checking the interior and all six edges."""
    raw = np.asarray(raw_coefficients, dtype=float)
    if raw.shape != (2,) or not np.all(np.isfinite(raw)):
        raise ValueError("raw_coefficients must be a finite vector of length two")

    candidates: list[tuple[str, np.ndarray]] = []
    if is_feasible(raw):
        candidates.append(("interior", raw.copy()))
    for index in range(VERTICES.shape[0]):
        start = VERTICES[index]
        direction = VERTICES[(index + 1) % VERTICES.shape[0]] - start
        denominator = float(direction @ GRAM @ direction)
        parameter = -float(direction @ GRAM @ (start - raw)) / denominator
        parameter = min(1.0, max(0.0, parameter))
        candidates.append((f"edge_{index}", start + parameter * direction))

    label, projected = min(candidates, key=lambda pair: _metric_squared(pair[1], raw))
    projected = np.asarray(projected, dtype=float)
    if not is_feasible(projected, tolerance=2.0e-14):
        raise RuntimeError("metric projection produced an infeasible coefficient pair")
    objective = _metric_squared(projected, raw)
    vi_values = (VERTICES - projected) @ GRAM @ (projected - raw)
    diagnostics = {
        "active_candidate": label,
        "metric_squared_distance": objective,
        "variational_inequality_minimum": float(np.min(vi_values)),
        "projected": label != "interior",
    }
    return projected, diagnostics


def compute_gram_audit(dps: int = 80, grid_points: int = 262_144) -> dict:
    """Independently evaluate G by an elliptic identity, quadrature, and a grid."""
    if dps < 50 or grid_points < 1024:
        raise ValueError("Gram audit requires dps >= 50 and at least 1024 grid points")
    with mp.workdps(dps):
        m = mp.mpf(1) / 20
        a = mp.mpf(2) / 21
        constant = mp.mpf(80) / 441
        complete_k = mp.ellipk(m)
        complete_e = mp.ellipe(m)
        i1 = mp.mpf(40) / 21 * (1 - complete_e / complete_k)
        i2 = (4 * i1 - constant) / 3
        i3 = (8 * i2 - 3 * constant * i1) / 5
        identity = mp.matrix(
            [
                [i1 - 2 * i2 / a + i3 / a**2, i2 / a - i3 / a**2],
                [i2 / a - i3 / a**2, i3 / a**2],
            ]
        )
        kappa = mp.sqrt(mp.mpf(40) / 21)
        period = 4 * complete_k / kappa

        def basis(index: int, x: mp.mpf) -> mp.mpf:
            g = mp.sqrt(a) * mp.ellipfun("sn", kappa * x, m)
            return g * (1 - g**2 / a) if index == 0 else g**3 / a

        quadrature = mp.matrix(2)
        intervals = [0, period / 4, period / 2, 3 * period / 4, period]
        for row in range(2):
            for column in range(2):
                quadrature[row, column] = (
                    mp.quad(
                        lambda x, i=row, j=column: basis(i, x) * basis(j, x),
                        intervals,
                    )
                    / period
                )
        identity_float = np.array(identity.tolist(), dtype=float)
        quadrature_float = np.array(quadrature.tolist(), dtype=float)

    grid = np.arange(grid_points, dtype=float) * PERIOD / grid_points
    grid_basis = basis_values(grid)
    grid_matrix = grid_basis.T @ grid_basis / grid_points
    eigenvalues = np.linalg.eigvalsh(identity_float)
    return {
        "decimal_precision": dps,
        "grid_points": grid_points,
        "elliptic_identity": identity_float.tolist(),
        "high_precision_quadrature": quadrature_float.tolist(),
        "periodic_grid": grid_matrix.tolist(),
        "identity_quadrature_max_abs_difference": float(
            np.max(np.abs(identity_float - quadrature_float))
        ),
        "identity_grid_max_abs_difference": float(
            np.max(np.abs(identity_float - grid_matrix))
        ),
        "eigenvalues": eigenvalues.tolist(),
        "positive_definite": bool(np.all(eigenvalues > 0.0)),
        "condition_number": float(eigenvalues[-1] / eigenvalues[0]),
        "not_a_rigorous_rounding_enclosure": True,
    }
