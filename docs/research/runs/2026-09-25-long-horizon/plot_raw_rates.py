"""Plot existing full-moment optimization results; performs no new optimization."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RUN = Path(__file__).resolve().parent


def main():
    rows = json.loads((RUN / "numerics/raw-results.json").read_text())["flat_rows"]
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.titleweight": "bold"})
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.3), constrained_layout=True)
    for p, color in [(0.5, "#285475"), (0.95, "#46856b")]:
        data = sorted([r for r in rows if float(r["policy"]) == p
                       and r["optimizer"]["status"] == "computed"],
                      key=lambda r: r["horizon"])
        times = [r["horizon"] for r in data]
        axes[0].plot(times, [r["optimizer"]["rate"] for r in data], "o-",
                     color=color, label=f"Common label probability p={p:g}")
        axes[1].semilogy(times, [r["optimizer"]["variance"] for r in data], "o-",
                         color=color, label=f"p={p:g}")
        for ax in axes:
            ax.axvline(data[0]["optimizer"]["interval"]["maximum_horizon"],
                       color=color, linestyle=":", alpha=.7)
    axes[0].axhline(.745, color="#B07131", linestyle="--", label="Fixed short-time rate 0.745")
    axes[0].set(xlabel="Horizon T", ylabel="Numerically minimizing common rate λ",
                title="A. The short-time rate does not stay optimal")
    axes[1].set(xlabel="Horizon T", ylabel="Full estimator variance at computed rate (log)",
                title="B. Tuning cannot remove the finite L2 ceiling")
    for ax in axes:
        ax.grid(color="#E5E9EB", alpha=.8)
        ax.legend(fontsize=8, loc="upper left")
    fig.suptitle("Raw flat Allen–Cahn, terminal value 1/2", fontsize=15, fontweight="bold")
    fig.text(.5, -.035,
             "Five-field moment ODE; floating optimization, not a certified global optimizer. "
             "Dotted lines: limiting feasible horizons (excluded).",
             ha="center", fontsize=8)
    for suffix in ["png", "pdf"]:
        fig.savefig(RUN / f"raw-rate-long-horizon.{suffix}", dpi=190, bbox_inches="tight")
    print(RUN / "raw-rate-long-horizon.png")


if __name__ == "__main__":
    main()
