"""Exact periodic heat-equation data for latent modal-control experiments.

Coefficient order is ``cos(1)..cos(K), sin(1)..sin(K)``.  Grids use
``endpoint=False`` so every period is sampled once.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, replace

import numpy as np


@dataclass(frozen=True)
class HeatBatch:
    sensor_grid: np.ndarray
    query_grid: np.ndarray
    terminal_coeffs: np.ndarray
    output_coeffs: np.ndarray
    phi: np.ndarray
    u: np.ndarray
    T: float
    x_lo: float
    x_hi: float

    @property
    def n_modes(self) -> int:
        return self.terminal_coeffs.shape[1]

    @property
    def K(self) -> int:
        return self.n_modes // 2

    @property
    def identity(self) -> str:
        payload = np.ascontiguousarray(self.terminal_coeffs).view(np.uint8)
        return hashlib.sha256(payload).hexdigest()


def periodic_grid(n: int, x_lo: float = -8.0, x_hi: float = 8.0) -> np.ndarray:
    if n < 2:
        raise ValueError("periodic grid needs at least two points")
    return np.linspace(x_lo, x_hi, n, endpoint=False, dtype=float)


def fourier_basis(x, K: int, x_lo: float = -8.0,
                  x_hi: float = 8.0) -> np.ndarray:
    """Return ``(len(x), 2K)`` real Fourier basis values."""
    x = np.asarray(x, dtype=float)
    omega = 2.0 * np.pi / (x_hi - x_lo)
    ks = np.arange(1, K + 1, dtype=float)
    phase = np.outer(x, omega * ks)
    return np.concatenate([np.cos(phase), np.sin(phase)], axis=1)


def evaluate_coeffs(coeffs, x, *, x_lo: float = -8.0,
                    x_hi: float = 8.0) -> np.ndarray:
    coeffs = np.asarray(coeffs, dtype=float)
    if coeffs.ndim == 1:
        coeffs = coeffs[None]
    if coeffs.shape[1] % 2:
        raise ValueError("real Fourier coefficient count must be even")
    return coeffs @ fourier_basis(x, coeffs.shape[1] // 2, x_lo, x_hi).T


def project_coeffs(values, x, K: int, *, x_lo: float = -8.0,
                   x_hi: float = 8.0) -> np.ndarray:
    """Least-squares real Fourier coefficients on an arbitrary query grid."""
    values = np.asarray(values, dtype=float)
    one = values.ndim == 1
    if one:
        values = values[None]
    basis = fourier_basis(x, K, x_lo, x_hi)
    coeffs = np.linalg.lstsq(basis, values.T, rcond=None)[0].T
    return coeffs[0] if one else coeffs


def heat_decay(K: int, T: float, *, x_lo: float = -8.0,
               x_hi: float = 8.0) -> np.ndarray:
    omega = 2.0 * np.pi / (x_hi - x_lo)
    rho = np.exp(-0.5 * (omega * np.arange(1, K + 1)) ** 2 * T)
    return np.concatenate([rho, rho])


def sample_heat_batch(n: int, seed: int, *, K: int = 4,
                      coefficient_scale: float = 0.25,
                      n_sensors: int = 128, n_query: int = 256,
                      T: float = 0.3, x_lo: float = -8.0,
                      x_hi: float = 8.0) -> HeatBatch:
    rng = np.random.default_rng(seed)
    terminal = rng.uniform(-coefficient_scale, coefficient_scale, size=(n, 2 * K))
    output = terminal * heat_decay(K, T, x_lo=x_lo, x_hi=x_hi)
    sensors = periodic_grid(n_sensors, x_lo, x_hi)
    query = periodic_grid(n_query, x_lo, x_hi)
    return HeatBatch(
        sensors, query, terminal, output,
        evaluate_coeffs(terminal, sensors, x_lo=x_lo, x_hi=x_hi),
        evaluate_coeffs(output, query, x_lo=x_lo, x_hi=x_hi),
        T, x_lo, x_hi)


def perturb_output_mode(batch: HeatBatch, mode: int, delta) -> HeatBatch:
    """Return exact data after adding ``delta`` to one t=0 output mode."""
    if not 0 <= mode < batch.n_modes:
        raise IndexError(f"mode {mode} outside [0, {batch.n_modes})")
    delta = np.asarray(delta, dtype=float)
    if delta.ndim == 0:
        delta = np.full(len(batch.terminal_coeffs), float(delta))
    if delta.shape != (len(batch.terminal_coeffs),):
        raise ValueError("delta must be scalar or have one value per function")
    terminal = batch.terminal_coeffs.copy()
    output = batch.output_coeffs.copy()
    rho = heat_decay(batch.K, batch.T, x_lo=batch.x_lo, x_hi=batch.x_hi)
    terminal[:, mode] += delta / rho[mode]
    output[:, mode] += delta
    return replace(
        batch, terminal_coeffs=terminal, output_coeffs=output,
        phi=evaluate_coeffs(terminal, batch.sensor_grid,
                            x_lo=batch.x_lo, x_hi=batch.x_hi),
        u=evaluate_coeffs(output, batch.query_grid,
                          x_lo=batch.x_lo, x_hi=batch.x_hi))
