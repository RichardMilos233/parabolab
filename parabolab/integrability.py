"""Deterministic truncated inverse-power integrals for Gaussian random variables."""

from __future__ import annotations

import math
import numpy as np


def _trapezoid(y: np.ndarray, x: np.ndarray) -> float:
    """Trapezoidal integration compatible with NumPy 1.x and 2.x."""
    trap_fn = getattr(np, "trapezoid", getattr(np, "trapz", None))
    if trap_fn is None:
        raise RuntimeError("Neither np.trapezoid nor np.trapz is available")
    return float(trap_fn(y, x))


def truncated_normal_inverse_power(
    mean: float,
    std: float,
    power: float,
    epsilon: float,
    outer: float = 1.0,
    log_points: int = 4097,
) -> float:
    r"""Compute \int_{\epsilon < |x| < outer} |x|^{-power} g_{mean, std}(x) dx deterministically.

    Uses a logarithmic substitution x = e^u so that dx = e^u du, transforming the integral to:
        \int_{\log \epsilon}^{\log outer} [g(e^u) + g(-e^u)] e^{(1 - power) u} du.

    Parameters
    ----------
    mean : float
        Mean \mu of the Gaussian density.
    std : float
        Standard deviation \sigma of the Gaussian density (> 0).
    power : float
        Exponent a in |x|^{-a} (> 0).
    epsilon : float
        Inner truncation radius (0 < epsilon < outer).
    outer : float
        Outer truncation radius (> epsilon).
    log_points : int
        Number of quadrature points on [\log \epsilon, \log outer], must be an odd integer >= 257.
    """
    if std <= 0.0 or not math.isfinite(std):
        raise ValueError(f"std must be positive and finite, got {std}")
    if power <= 0.0 or not math.isfinite(power):
        raise ValueError(f"power must be positive and finite, got {power}")
    if not (0.0 < epsilon < outer):
        raise ValueError(f"epsilon must be in (0, outer), got epsilon={epsilon}, outer={outer}")
    if not isinstance(log_points, (int, np.integer)) or isinstance(log_points, bool) or log_points < 257 or log_points % 2 == 0:
        raise ValueError(f"log_points must be an odd integer >= 257, got {log_points}")

    u = np.linspace(math.log(epsilon), math.log(outer), log_points)
    x_pos = np.exp(u)
    x_neg = -x_pos

    inv_norm = 1.0 / (std * math.sqrt(2.0 * math.pi))
    var = std * std

    g_pos = inv_norm * np.exp(-((x_pos - mean) ** 2) / (2.0 * var))
    g_neg = inv_norm * np.exp(-((x_neg - mean) ** 2) / (2.0 * var))

    # Weight factor: e^{(1 - power) * u}
    weight = np.exp((1.0 - power) * u)
    integrand = (g_pos + g_neg) * weight

    return _trapezoid(integrand, u)
