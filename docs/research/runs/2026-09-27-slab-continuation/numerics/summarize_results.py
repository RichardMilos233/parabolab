"""Summarize the frozen slab/majority artifacts and render the result figure.

This script is deterministic: it requires three complete prespecified runs
for each experiment, reads no raw roots, and derives every table and plotted
curve from the saved JSON records.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import special


HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
SLAB_RESULTS = HERE / "artifacts" / "slab" / "results.json"
MAJORITY_RESULTS = HERE / "artifacts" / "majority" / "results.json"
SENSITIVITY_RESULTS = HERE / "artifacts" / "sensitivity" / "results.json"
SUMMARY = HERE / "summary.json"
PNG = RUN_DIR / "slab-results.png"
SVG = RUN_DIR / "slab-results.svg"

SLAB_SEEDS = (2026092701, 2026092702, 2026092703)
MAJORITY_SEEDS = (2026092711, 2026092712, 2026092713)
SELECTED_TIMES = (0.8, 1.6, 2.0, 4.0)
MODES = np.array((1, 3, 5), dtype=float)
M = 0.05
A = math.sqrt(2.0 / 21.0)
KAPPA = math.sqrt(40.0 / 21.0)
MAJORITY_T4_EXPECTED_NODES = 8000 * (3.0 * math.exp(16.0) - 1.0) / 2.0


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_complete(path: Path, seeds: tuple[int, ...]) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"required production artifact is missing: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    actual_seeds = tuple(run["seed"] for run in payload.get("runs", ()))
    if payload.get("status") != "complete":
        raise RuntimeError(f"artifact is not complete: {path}")
    if actual_seeds != seeds:
        raise RuntimeError(f"unexpected seed schedule in {path}: {actual_seeds}")
    if any(run.get("status") != "complete" for run in payload["runs"]):
        raise RuntimeError(f"artifact contains an incomplete run: {path}")
    return payload


def _stage_at(run: dict, time_value: float) -> dict:
    matches = [
        stage
        for stage in run["stages"]
        if math.isclose(stage["elapsed_time"], time_value, abs_tol=1.0e-12)
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"seed {run['seed']} has {len(matches)} records at T={time_value}"
        )
    return matches[0]


def _projection_counts(rows: list[dict]) -> dict:
    mask = np.array([row["projection_mask"] for row in rows], dtype=bool)
    return {
        "stage_or_horizon_count_with_any_clipping": int(np.any(mask, axis=1).sum()),
        "coordinate_clip_count": int(mask.sum()),
        "coordinate_clip_counts_n_1_3_5": mask.sum(axis=0).astype(int).tolist(),
        "total_coordinate_estimates": int(mask.size),
    }


def _slab_run_summary(run: dict) -> dict:
    stages = run["stages"]
    if len(stages) != 50 or not all(stage["complete"] for stage in stages):
        raise RuntimeError(f"slab seed {run['seed']} does not contain 50 complete stages")
    sampling_seconds = sum(stage["sampling_seconds"] for stage in stages)
    maximum_grid_difference = max(
        abs(stage["error"]["grid_crosscheck_minus_exact_fourier"])
        for stage in stages
    )
    selected = {}
    for time_value in SELECTED_TIMES:
        stage = _stage_at(run, time_value)
        preceding = stages[: stage["stage"]]
        selected[str(time_value)] = {
            "stage": stage["stage"],
            "normalized_spatial_l2_error": stage["error"][
                "normalized_l2_exact_fourier_plus_tail"
            ],
            "periodic_grid_l2_crosscheck": stage["error"][
                "normalized_l2_periodic_grid_crosscheck"
            ],
            "grid_minus_fourier_error": stage["error"][
                "grid_crosscheck_minus_exact_fourier"
            ],
            "projected_coefficients": stage["projected_coefficients"],
            "projection_mask": stage["projection_mask"],
            "instantaneous_root_branch_fraction": stage["root_branch_fraction"],
            "cumulative_root_count": sum(row["root_count"] for row in preceding),
            "cumulative_node_count": sum(row["total_nodes"] for row in preceding),
            "cumulative_sampling_seconds": sum(
                row["sampling_seconds"] for row in preceding
            ),
        }
    final = stages[-1]
    measured = run["measured_work"]
    return {
        "seed": run["seed"],
        "status": run["status"],
        "selected_times": selected,
        "final": {
            "normalized_spatial_l2_error": final["error"][
                "normalized_l2_exact_fourier_plus_tail"
            ],
            "periodic_grid_l2_crosscheck": final["error"][
                "normalized_l2_periodic_grid_crosscheck"
            ],
            "grid_minus_fourier_error": final["error"][
                "grid_crosscheck_minus_exact_fourier"
            ],
            "projected_coefficients": final["projected_coefficients"],
        },
        "work": {
            "root_count": measured["roots_completed"],
            "node_count": measured["total_nodes"],
            "terminal_calls": measured["terminal_calls"],
            "root_branch_count": measured["root_branches"],
            "aggregate_root_branch_fraction": (
                measured["root_branches"] / measured["roots_completed"]
            ),
        },
        "timing_seconds": {
            "tree_sampling_only": sampling_seconds,
            "run_end_to_end_including_archives_and_stage_statistics": run[
                "total_seconds"
            ],
        },
        "projection": _projection_counts(stages),
        "grid_agreement": {
            "maximum_absolute_grid_minus_fourier_l2": maximum_grid_difference,
        },
    }


def _majority_run_summary(run: dict) -> dict:
    rows = run["horizons"]
    if len(rows) != 2 or not all(row["complete"] for row in rows):
        raise RuntimeError(
            f"majority seed {run['seed']} does not contain both complete horizons"
        )
    horizons = {}
    for row in rows:
        horizons[str(row["horizon"])] = {
            "normalized_spatial_l2_error": row["error"][
                "normalized_l2_exact_fourier_plus_tail"
            ],
            "periodic_grid_l2_crosscheck": row["error"][
                "normalized_l2_periodic_grid_crosscheck"
            ],
            "grid_minus_fourier_error": row["error"][
                "grid_crosscheck_minus_exact_fourier"
            ],
            "projected_coefficients": row["projected_coefficients"],
            "projection_mask": row["projection_mask"],
            "root_count": row["root_count"],
            "node_count": row["total_nodes"],
            "terminal_calls": int(sum(row["terminal_code_counts"])),
            "root_branch_fraction": row["root_branch_fraction"],
            "sampling_seconds": row["sampling_seconds"],
        }
    measured = run["measured_work"]
    return {
        "seed": run["seed"],
        "status": run["status"],
        "horizons": horizons,
        "work": {
            "root_count": measured["roots_completed"],
            "node_count": measured["total_nodes"],
            "terminal_calls": measured["terminal_calls"],
            "root_branch_count": measured["root_branches"],
            "aggregate_root_branch_fraction": (
                measured["root_branches"] / measured["roots_completed"]
            ),
        },
        "timing_seconds": {
            "tree_sampling_only": sum(row["sampling_seconds"] for row in rows),
            "run_end_to_end_including_archives_and_statistics": run["total_seconds"],
        },
        "projection": _projection_counts(rows),
        "grid_agreement": {
            "maximum_absolute_grid_minus_fourier_l2": max(
                abs(row["error"]["grid_crosscheck_minus_exact_fourier"])
                for row in rows
            ),
        },
    }


def build_summary(
    slab: dict, majority: dict, sensitivity: dict | None = None
) -> dict:
    slab_runs = [_slab_run_summary(run) for run in slab["runs"]]
    majority_runs = [_majority_run_summary(run) for run in majority["runs"]]
    selected_time_summary = {}
    for time_value in SELECTED_TIMES:
        key = str(time_value)
        errors = np.array(
            [run["selected_times"][key]["normalized_spatial_l2_error"] for run in slab_runs]
        )
        selected_time_summary[key] = {
            "per_seed_normalized_spatial_l2_errors": errors.tolist(),
            "empirical_rms_across_three_runs": float(np.sqrt(np.mean(errors**2))),
            "interpretation": "descriptive three-run RMS; not a confidence interval",
        }
    final_errors = np.array(
        [run["final"]["normalized_spatial_l2_error"] for run in slab_runs]
    )
    summary = {
        "schema_version": 1,
        "benchmark": (
            "stationary periodic Jacobi Allen-Cahn datum; three-sine learned "
            "slab continuation"
        ),
        "source_artifacts": {
            "slab": {
                "path": str(SLAB_RESULTS.relative_to(RUN_DIR)),
                "sha256": _sha256(SLAB_RESULTS),
            },
            "bounded_majority": {
                "path": str(MAJORITY_RESULTS.relative_to(RUN_DIR)),
                "sha256": _sha256(MAJORITY_RESULTS),
            },
        },
        "slab": {
            "prescribed_budget": "200000 roots per slab, 50 slabs of length 0.08",
            "runs": slab_runs,
            "selected_times": selected_time_summary,
            "final_errors": {
                "per_seed_normalized_spatial_l2_errors": final_errors.tolist(),
                "empirical_rms_across_three_runs": float(
                    np.sqrt(np.mean(final_errors**2))
                ),
                "interpretation": "descriptive three-run RMS; not a confidence interval",
            },
            "aggregate": {
                "root_count": sum(run["work"]["root_count"] for run in slab_runs),
                "node_count": sum(run["work"]["node_count"] for run in slab_runs),
                "tree_sampling_seconds": sum(
                    run["timing_seconds"]["tree_sampling_only"] for run in slab_runs
                ),
                "run_end_to_end_seconds": sum(
                    run["timing_seconds"][
                        "run_end_to_end_including_archives_and_stage_statistics"
                    ]
                    for run in slab_runs
                ),
                "maximum_absolute_grid_minus_fourier_l2": max(
                    run["grid_agreement"][
                        "maximum_absolute_grid_minus_fourier_l2"
                    ]
                    for run in slab_runs
                ),
                "coordinate_projection_count": sum(
                    run["projection"]["coordinate_clip_count"] for run in slab_runs
                ),
            },
        },
        "bounded_majority": {
            "prescribed_budget": "8000 full-horizon roots independently at T=0.8 and T=2",
            "runs": majority_runs,
            "aggregate": {
                "root_count": sum(
                    run["work"]["root_count"] for run in majority_runs
                ),
                "node_count": sum(
                    run["work"]["node_count"] for run in majority_runs
                ),
                "tree_sampling_seconds": sum(
                    run["timing_seconds"]["tree_sampling_only"]
                    for run in majority_runs
                ),
                "run_end_to_end_seconds": sum(
                    run["timing_seconds"][
                        "run_end_to_end_including_archives_and_statistics"
                    ]
                    for run in majority_runs
                ),
                "maximum_absolute_grid_minus_fourier_l2": max(
                    run["grid_agreement"][
                        "maximum_absolute_grid_minus_fourier_l2"
                    ]
                    for run in majority_runs
                ),
                "coordinate_projection_count": sum(
                    run["projection"]["coordinate_clip_count"]
                    for run in majority_runs
                ),
            },
            "unrun_T4_theoretical_work": {
                "roots": 8000,
                "expected_nodes": MAJORITY_T4_EXPECTED_NODES,
                "expected_nodes_billions": MAJORITY_T4_EXPECTED_NODES / 1.0e9,
                "measured": False,
                "note": "reported separately and omitted from the measured-node plot",
            },
        },
        "interpretation_limits": [
            "The benchmark is stationary, periodic, one-dimensional, and small-amplitude.",
            "Three-run empirical RMS values are descriptive and are not confidence intervals.",
            "The slab and majority node curves use different prescribed root budgets.",
            "Measured work does not establish speedup optimality.",
            "The population RMS theorem is not plotted as a pathwise confidence band.",
        ],
    }
    if sensitivity is not None:
        sensitivity_run = _slab_run_summary(sensitivity["runs"][0])
        summary["source_artifacts"]["optional_sensitivity"] = {
            "path": str(SENSITIVITY_RESULTS.relative_to(RUN_DIR)),
            "sha256": _sha256(SENSITIVITY_RESULTS),
        }
        summary["sensitivity_diagnostic"] = {
            "classification": "optional empirical budget diagnostic; excluded from the primary three-run RMS",
            "prescribed_budget": "50000 roots per slab, 50 slabs of length 0.08",
            "run": sensitivity_run,
        }
    return summary


def _plot(slab: dict, majority: dict) -> None:
    colors = ("#1769AA", "#D1495B", "#2A9D6F")
    figure, axes = plt.subplots(1, 3, figsize=(15.2, 4.5), constrained_layout=True)

    for color, run in zip(colors, slab["runs"]):
        times = np.array([stage["elapsed_time"] for stage in run["stages"]])
        errors = np.array(
            [
                stage["error"]["normalized_l2_exact_fourier_plus_tail"]
                for stage in run["stages"]
            ]
        )
        axes[0].plot(
            times,
            errors,
            color=color,
            linewidth=1.55,
            label=f"seed {run['seed']}",
        )
        selected_errors = [
            _stage_at(run, value)["error"][
                "normalized_l2_exact_fourier_plus_tail"
            ]
            for value in SELECTED_TIMES
        ]
        axes[0].scatter(SELECTED_TIMES, selected_errors, color=color, s=17, zorder=3)
    axes[0].set_xlabel("elapsed time T")
    axes[0].set_ylabel("normalized spatial $L^2$ error")
    axes[0].set_title("Realized continuation error")
    axes[0].set_xlim(0.0, 4.05)
    axes[0].set_ylim(bottom=0.0)
    axes[0].legend(frameon=False, fontsize=8)

    line_styles = ("-", (0, (5, 2)), (0, (1.5, 1.5)))
    for color, line_style, run in zip(colors, line_styles, slab["runs"]):
        times = np.array([stage["elapsed_time"] for stage in run["stages"]])
        cumulative_nodes = np.cumsum([stage["total_nodes"] for stage in run["stages"]])
        axes[1].plot(
            times,
            cumulative_nodes,
            color=color,
            linestyle=line_style,
            linewidth=1.35,
            alpha=0.9,
        )
    for run_index, run in enumerate(majority["runs"]):
        horizons = np.array([row["horizon"] for row in run["horizons"]])
        nodes = np.array([row["total_nodes"] for row in run["horizons"]])
        axes[1].scatter(
            horizons,
            nodes,
            marker="X",
            s=50,
            facecolor="#252525",
            edgecolor="white",
            linewidth=0.5,
            zorder=4,
            label="majority: 8k roots/horizon" if run_index == 0 else None,
        )
    axes[1].plot([], [], color="#1769AA", label="slab: 200k roots/slab")
    axes[1].set_yscale("log")
    axes[1].set_xlabel("elapsed time T")
    axes[1].set_ylabel("actual tree nodes")
    axes[1].set_title("Measured work (different budgets)")
    axes[1].set_xlim(0.0, 4.05)
    axes[1].legend(frameon=False, fontsize=8, loc="lower right")

    reference_record = slab["provenance"]["reference_checks"]
    period = float(reference_record["period"])
    omega = float(reference_record["omega"])
    x = np.linspace(0.0, period, 1200, endpoint=True)
    exact = A * special.ellipj(KAPPA * x, M)[0]
    for color, run in zip(colors, slab["runs"]):
        coefficients = np.array(run["stages"][-1]["projected_coefficients"])
        approximation = math.sqrt(2.0) * np.sum(
            coefficients * np.sin(x[:, None] * omega * MODES), axis=1
        )
        axes[2].plot(
            x / period,
            approximation - exact,
            color=color,
            linewidth=1.55,
            label=f"seed {run['seed']}",
        )
    axes[2].axhline(0.0, color="#252525", linewidth=0.9, linestyle="--", label="exact reference")
    axes[2].set_xlabel("period coordinate $x/L$")
    axes[2].set_ylabel("$v_{50}(x)-g(x)$")
    axes[2].set_title("Final error profile at T=4")
    axes[2].set_xlim(0.0, 1.0)
    axes[2].legend(frameon=False, fontsize=8)

    for axis in axes:
        axis.grid(True, color="#D8D8D8", linewidth=0.6, alpha=0.75)
        axis.tick_params(labelsize=8.5)
    figure.suptitle(
        "Stationary Jacobi Allen–Cahn benchmark: learned slab continuation",
        fontsize=12,
    )
    matplotlib.rcParams["svg.hashsalt"] = "2026-09-27-slab-continuation"
    figure.savefig(PNG, dpi=220, metadata={"Software": "matplotlib"})
    figure.savefig(SVG, metadata={"Date": None})
    plt.close(figure)


def main() -> None:
    slab = _read_complete(SLAB_RESULTS, SLAB_SEEDS)
    majority = _read_complete(MAJORITY_RESULTS, MAJORITY_SEEDS)
    sensitivity = (
        _read_complete(SENSITIVITY_RESULTS, (2026092799,))
        if SENSITIVITY_RESULTS.exists()
        else None
    )
    summary = build_summary(slab, majority, sensitivity)
    SUMMARY.write_text(
        json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    _plot(slab, majority)
    print(
        json.dumps(
            {
                "summary": str(SUMMARY),
                "figure_png": str(PNG),
                "figure_svg": str(SVG),
                "final_empirical_rms": summary["slab"]["final_errors"][
                    "empirical_rms_across_three_runs"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
