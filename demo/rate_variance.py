"""Rate sensitivity and variance convexity: generalizability across PDEs."""
import argparse
from pathlib import Path

from parabolab import compare_rate_variance, sweep_rate_variance
from parabolab.library import (
    allen_cahn_flat,
    allen_cahn_wave_1d,
    binary_control_1d,
    fisher_kpp_1d,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rate sensitivity and variance convexity demo")
    parser.add_argument("--T", type=float, default=0.05, help="Terminal horizon T (default: 0.05)")
    args = parser.parse_args()
    T = args.T

    sweeps = [
        sweep_rate_variance(
            allen_cahn_wave_1d(T=T), x=0.0,
            title="(a) Allen–Cahn Wave (x = 0.0)",
        ),
        sweep_rate_variance(
            allen_cahn_wave_1d(T=T), x=-1.0, lambda_bracket=(0.12, 1.8),
            title="(b) Allen–Cahn Wave (x = -1.0)",
        ),
        sweep_rate_variance(
            fisher_kpp_1d(T=T, phi0=0.5), x=0.0, lambda_bracket=(0.12, 1.6),
            title="(c) Fisher–KPP Logistic Equation (phi0 = 0.5)",
        ),
        sweep_rate_variance(
            binary_control_1d(T=T), x=0.0, use_riccati=True,
            title="(d) Binary Riccati Control (phi0 = 1.0)",
        ),
        sweep_rate_variance(
            allen_cahn_flat(phi0=0.3, T=T), x=0.0, lambda_bracket=(0.20, 2.2),
            title="(e) Allen–Cahn Flat State (phi0 = 0.3)",
        ),
        sweep_rate_variance(
            fisher_kpp_1d(T=T, phi0=0.2), x=0.0, lambda_bracket=(0.20, 2.0),
            title="(f) Fisher–KPP Logistic State (phi0 = 0.2)",
        ),
    ]

    compare_rate_variance(*sweeps).table().plot(
        Path(__file__).with_suffix(".png"),
        save_individual=True,
    )
