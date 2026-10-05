"""Plot the saved uniform-policy finite-second-moment boundary.

This is an explanatory rendering of frozen numerical evidence. It performs no
ODE solve, optimization, or Monte Carlo sampling. The boundary formula is the
proved identity; the plotted decimals use the stored floating quadrature value
of C and the stored floating optimizer output.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "raw-results.json"
OUTPUT = HERE / "lambda-boundary.png"
POLICY = 0.5
FIXED_RATE = 0.745


def boundary(rate: np.ndarray | float, c_value: float) -> np.ndarray | float:
    return np.log1p(np.asarray(rate) ** 2 * POLICY * c_value) / np.asarray(rate)


def main() -> None:
    saved = json.loads(RESULTS.read_text())
    c_value = float(saved["thresholds"]["C_quadrature"])
    row = next(
        item
        for item in saved["flat_rows"]
        if item["policy"] == POLICY and item["horizon"] == 0.5
    )
    retuned_rate = float(row["optimizer"]["rate"])
    lower_rate = float(row["optimizer"]["interval"]["lower_rate"])
    upper_rate = float(row["optimizer"]["interval"]["upper_rate"])
    maximum_rate = float(row["optimizer"]["interval"]["maximum_rate"])
    maximum_horizon = float(row["optimizer"]["interval"]["maximum_horizon"])
    fixed_horizon = float(
        next(item for item in row["baselines"] if item["kind"] == "rate-0.745")[
            "threshold"
        ]
    )

    rates = np.linspace(0.05, 5.0, 1200)
    horizons = boundary(rates, c_value)
    retuned_boundary = float(boundary(retuned_rate, c_value))

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(9.2, 6.2), constrained_layout=True)
    ax.fill_between(
        rates,
        0.0,
        horizons,
        color="#d8efe5",
        alpha=0.9,
        label=r"Finite second moment: $T<T_2(\lambda)$",
    )
    ax.fill_between(rates, horizons, 0.8, color="#f8e1df", alpha=0.60)
    ax.plot(
        rates,
        horizons,
        color="#176b5b",
        linewidth=2.8,
        label=r"Feasibility boundary $T_2(\lambda)$",
    )

    ax.scatter([FIXED_RATE], [0.05], s=85, color="#176b5b", edgecolor="white", zorder=5)
    ax.annotate(
        "fixed λ = 0.745\nT = 0.05: inside",
        (FIXED_RATE, 0.05),
        xytext=(0.18, 0.13),
        textcoords="data",
        arrowprops={"arrowstyle": "->", "color": "#176b5b"},
        fontsize=10,
    )

    ax.scatter([FIXED_RATE], [0.5], marker="X", s=125, color="#b6403a", zorder=6)
    ax.annotate(
        f"fixed λ = 0.745\nT = 0.50: outside\n(boundary {fixed_horizon:.5f})",
        (FIXED_RATE, 0.5),
        xytext=(0.13, 0.60),
        textcoords="data",
        arrowprops={"arrowstyle": "->", "color": "#b6403a"},
        fontsize=10,
        color="#7c2925",
    )

    ax.scatter([retuned_rate], [0.5], marker="o", s=105, color="#3158a5", edgecolor="white", zorder=6)
    ax.annotate(
        f"stored floating optimizer λ = {retuned_rate:.4f}\nT = 0.50: inside\n(boundary {retuned_boundary:.5f})",
        (retuned_rate, 0.5),
        xytext=(1.48, 0.40),
        textcoords="data",
        arrowprops={"arrowstyle": "->", "color": "#3158a5"},
        fontsize=10,
        color="#253f78",
    )
    ax.annotate(
        "",
        xy=(retuned_rate, 0.5),
        xytext=(FIXED_RATE, 0.5),
        arrowprops={"arrowstyle": "-|>", "linewidth": 2.0, "color": "#3158a5"},
        zorder=5,
    )
    ax.text(
        (FIXED_RATE + retuned_rate) / 2,
        0.515,
        "retune λ",
        ha="center",
        va="bottom",
        color="#3158a5",
        fontsize=9,
    )

    ax.scatter(
        [maximum_rate],
        [maximum_horizon],
        marker="D",
        s=85,
        facecolor="white",
        edgecolor="#6a3d9a",
        linewidth=2.2,
        zorder=6,
    )
    ax.annotate(
        f"finite-variance horizon ceiling ≈ {maximum_horizon:.5f}\n"
        f"(supremum; boundary excluded) at λ ≈ {maximum_rate:.4f}",
        (maximum_rate, maximum_horizon),
        xytext=(2.72, 0.735),
        textcoords="data",
        arrowprops={"arrowstyle": "->", "color": "#6a3d9a"},
        fontsize=10,
        color="#55317c",
    )

    ax.set_xlim(0.05, 5.0)
    ax.set_ylim(0.0, 0.8)
    ax.set_xlabel(r"Exponential rate $\lambda$")
    ax.set_ylabel(r"Horizon $T$")
    ax.set_title("Uniform policy: changing λ can restore a finite second moment", pad=18, fontsize=15)
    ax.text(
        0.5,
        1.012,
        r"$T_2(\lambda)=\log(1+\lambda^2\,0.5\,C)/\lambda$; decimals evaluate the proved boundary using saved $C$",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=10,
        color="#444444",
    )
    ax.text(
        0.985,
        0.065,
        f"At T = 0.50, the stored floating open interval is {lower_rate:.5f} < λ < {upper_rate:.5f}.",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=9.5,
        color="#444444",
    )
    ax.text(
        0.985,
        0.015,
        "The curve is a feasibility boundary, not a variance-minimizer curve.",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=9.5,
        color="#444444",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#bbbbbb", "alpha": 0.92},
    )
    ax.legend(loc="upper left", frameon=True, framealpha=0.96)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(OUTPUT, dpi=180)


if __name__ == "__main__":
    main()
