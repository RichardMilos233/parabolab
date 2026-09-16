"""Rate sensitivity and variance convexity: generalizability across PDEs."""
from pathlib import Path

from parabolab import compare_rate_variance, sweep_rate_variance
from parabolab.library import allen_cahn_wave_1d, binary_control_1d, fisher_kpp_1d

if __name__ == "__main__":
    sweeps = [
        sweep_rate_variance(
            allen_cahn_wave_1d(T=0.05), x=0.0,
            title="(a) Allen–Cahn Wave (x = 0.0)",
        ),
        sweep_rate_variance(
            allen_cahn_wave_1d(T=0.05), x=-1.0, lambda_bracket=(0.12, 1.8),
            title="(b) Allen–Cahn Wave (x = -1.0)",
        ),
        sweep_rate_variance(
            fisher_kpp_1d(T=0.05, phi0=0.5), x=0.0, lambda_bracket=(0.12, 1.6),
            title="(c) Fisher–KPP Logistic Equation",
        ),
        sweep_rate_variance(
            binary_control_1d(T=0.05), x=0.0, use_riccati=True, lambda_bracket=(0.25, 2.3),
            title="(d) Binary Riccati Control",
        ),
    ]

    compare_rate_variance(*sweeps).table().plot(Path(__file__).with_suffix(".png"))
