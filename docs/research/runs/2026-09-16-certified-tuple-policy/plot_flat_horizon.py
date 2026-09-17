"""Plot the C8 flat Allen--Cahn second-moment explosion threshold."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


RUN = Path(__file__).resolve().parent
SOURCE = RUN / "numerics" / "flat-explosion-checks.json"
OUTPUT = RUN / "flat-horizon.png"


def threshold(rate: np.ndarray | float, probability: float, c_value: float):
    return np.log1p(np.asarray(rate) ** 2 * probability * c_value) / rate


def main() -> None:
    record = json.loads(SOURCE.read_text())
    enclosure = record["exact_certificate"]["integral_enclosure"]
    c_lower = float(Fraction(enclosure["C_lower"]["exact"]))
    c_upper = float(Fraction(enclosure["C_upper"]["exact"]))
    c_midpoint = 0.5 * (c_lower + c_upper)
    cases = {
        (case["policy"], case["rate"]): case
        for case in record["exact_certificate"]["cases"]
    }

    rates = np.linspace(0.1, 4.0, 1000)
    policies = (
        ("p = 0.50 (uniform)", 0.5, "#3569a8"),
        ("p = 0.95", 0.95, "#d87813"),
    )

    fig, ax = plt.subplots(figsize=(13.0, 6.8))
    # Draw the larger finite region first so the overlap remains legible.
    for label, probability, color in reversed(policies):
        lower = threshold(rates, probability, c_lower)
        upper = threshold(rates, probability, c_upper)
        midpoint = threshold(rates, probability, c_midpoint)
        ax.fill_between(
            rates, 0.0, lower, color=color, alpha=0.075,
            label=f"{label}: finite only for T < τ*",
        )
        ax.fill_between(
            rates, lower, upper, color=color, alpha=0.5,
            label=f"{label}: exact-C bound band",
        )
        ax.plot(rates, midpoint, color=color, linewidth=2.4, label=f"{label}: midpoint guide")

    ax.axhline(0.5, color="#454545", linestyle="--", linewidth=1.25)
    ax.axvline(0.75, color="#454545", linestyle=":", linewidth=1.25)
    ax.text(3.96, 0.514, "T = 0.5", ha="right", va="bottom", color="#353535")
    ax.text(0.77, 0.045, "λ = 0.75", ha="left", va="bottom", color="#353535", rotation=90)

    marker_x = 0.75
    annotations = (
        ("1/2", "3/4", "uniform threshold [0.477, 0.478]", "#3569a8", (-0.47, -0.13)),
        ("19/20", "3/4", "p = 0.95 threshold [0.796, 0.797]", "#d87813", (0.28, 0.10)),
    )
    for policy, rate, text, color, offset in annotations:
        case = cases[(policy, rate)]
        y0 = float(Fraction(case["explosion_time_lower"]["exact"]))
        y1 = float(Fraction(case["explosion_time_upper"]["exact"]))
        center = 0.5 * (y0 + y1)
        ax.errorbar(
            marker_x, center, yerr=[[center - y0], [y1 - center]],
            fmt="o", color=color, markeredgecolor="white", markeredgewidth=0.8,
            capsize=5, linewidth=2.0, zorder=6,
        )
        ax.annotate(
            text,
            xy=(marker_x, center), xytext=(marker_x + offset[0], center + offset[1]),
            color=color, fontsize=10.5, weight="bold",
            arrowprops={"arrowstyle": "->", "color": color, "linewidth": 1.1},
            bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": color, "alpha": 0.94},
        )

    fig.text(
        0.855, 0.46,
        "After reoptimizing λ separately:\n"
        "optimized horizon ratio = √1.9 = 1.3784\n"
        "(horizon ratio; not a variance percentage)",
        fontsize=10.5, ha="center", va="center",
        bbox={"boxstyle": "round,pad=0.4", "facecolor": "white", "edgecolor": "#777777", "alpha": 0.95},
    )
    ax.text(
        2.95, 0.19,
        "Shaded regions are finite only strictly below\n"
        "their policy's threshold; the boundary diverges.",
        fontsize=10, ha="center", va="center", color="#303030",
    )

    ax.set_xlim(0.1, 4.0)
    ax.set_ylim(0.0, 1.08)
    ax.set_xlabel("clock rate λ (dimensionless)", fontsize=11.5)
    ax.set_ylabel("threshold horizon τ*(λ, p) (dimensionless)", fontsize=11.5)
    ax.set_title("Flat Allen–Cahn φ=1/2; raw labelled mechanism", fontsize=15, pad=12)
    ax.grid(alpha=0.22)
    handles, labels = ax.get_legend_handles_labels()
    order = [3, 5, 4, 0, 2, 1]
    ax.legend(
        [handles[index] for index in order], [labels[index] for index in order],
        loc="upper left", bbox_to_anchor=(1.015, 1.0), borderaxespad=0.0,
        fontsize=8.8, frameon=True, framealpha=0.96,
    )

    fig.text(
        0.5, 0.018,
        "Exact rational C bracket from 2026-09-16; guide curves use floating midpoints. "
        "Threshold formula: conventional theorem + C rational certificate.",
        ha="center", va="bottom", fontsize=9.2, color="#3f3f3f",
    )
    fig.subplots_adjust(left=0.08, right=0.72, bottom=0.16, top=0.89)
    fig.savefig(OUTPUT, dpi=190)
    plt.close(fig)
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
