"""Build the compact dynamic-continuation summary and scientific figure."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np


HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
AUDIT_JSON = HERE / "audit_dynamic.json"
SUMMARY_JSON = HERE / "summary_dynamic.json"
PNG = RUN_DIR / "dynamic-results.png"
SVG = RUN_DIR / "dynamic-results.svg"
SELECTED_TIMES = (0.08, 0.4, 1.04, 2.0, 4.0, 8.0, 16.0)
THEORY_ENVELOPE = 0.02


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def array(values: object, shape: tuple[int, ...] | None = None) -> np.ndarray:
    result = np.asarray(values, dtype=float)
    if shape is not None and result.shape != shape:
        raise ValueError(f"expected shape {shape}, got {result.shape}")
    return result


def make_figure(summary: dict, png: Path, svg: Path) -> None:
    times = array(summary["times"], (201,))
    seeds = summary["seeds"]
    colors = ("#0072B2", "#009E73", "#CC79A7")

    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.titlesize": 11,
            "axes.labelsize": 9,
            "legend.fontsize": 7.5,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.2))
    ax_error, ax_coeff, ax_moment, ax_work = axes.flat

    for color, seed in zip(colors, seeds):
        values = array(seed["errors"]["mc"], (201,))
        ax_error.plot(
            times[1:], values[1:], color=color, alpha=0.55, linewidth=0.85,
            label=f"MC seed {seed['seed']}",
        )
    aggregate = summary["aggregate"]
    empirical_rms = array(aggregate["mc_error_empirical_rms"], (201,))
    ax_error.plot(
        times[1:], empirical_rms[1:], color="#003B5C", linewidth=2.1,
        label="3-seed empirical RMS",
    )
    baseline_styles = {
        "g": ("#666666", "-"),
        "0.95g": ("#E69F00", "-"),
        "0.9g": ("#56B4E9", "--"),
    }
    for name, (color, style) in baseline_styles.items():
        values = array(summary["baselines"][name]["errors"], (201,))
        ax_error.plot(times, values, color=color, linestyle=style, linewidth=1.35, label=name)
    ax_error.axhline(
        THEORY_ENVELOPE, color="#D55E00", linestyle=(0, (5, 3)), linewidth=1.4,
        label="0.02 theorem envelope",
    )
    ax_error.set_yscale("log")
    ax_error.set_ylim(8.0e-5, 3.0e-2)
    ax_error.set_xlim(0.0, 16.0)
    ax_error.set_xlabel("time")
    ax_error.set_ylabel("normalized spatial RMS error")
    ax_error.set_title("A  Accuracy against the deterministic reference", loc="left")
    ax_error.grid(True, which="both", alpha=0.2)
    ax_error.legend(
        ncol=2, frameon=True, facecolor="white", edgecolor="#DDDDDD",
        framealpha=0.94, loc="lower right",
    )

    for color, seed in zip(colors, seeds):
        coefficients = array(seed["coefficients"], (201, 2))
        ax_coeff.plot(
            times, coefficients[:, 0], color=color, linewidth=1.25,
        )
        ax_coeff.plot(
            times, coefficients[:, 1], color=color, linewidth=1.1,
            linestyle="--",
        )
    ax_coeff.axhline(0.9, color="#777777", linewidth=0.8, linestyle=":")
    ax_coeff.axhline(1.0, color="#777777", linewidth=0.8, linestyle=":")
    ax_coeff.set_xlim(0.0, 16.0)
    ax_coeff.set_ylim(0.897, 1.003)
    ax_coeff.set_xlabel("time")
    ax_coeff.set_ylabel("projected coefficient")
    ax_coeff.set_title("B  Feasible two-coefficient trajectories", loc="left")
    ax_coeff.grid(True, alpha=0.2)
    coefficient_legend = [
        Line2D((0,), (0,), color=color, linewidth=1.5, label=str(seed["seed"]))
        for color, seed in zip(colors, seeds)
    ]
    ax_coeff.legend(
        handles=coefficient_legend, ncol=1, frameon=True, facecolor="white",
        edgecolor="#DDDDDD", framealpha=0.94, loc="lower right",
    )
    ax_coeff.text(
        0.02, 0.05, "solid $c_0$  ·  dashed $c_1$", transform=ax_coeff.transAxes,
        ha="left", va="bottom", fontsize=8, color="#444444",
    )

    for color, seed in zip(colors, seeds):
        second = array(seed["tree_value_second_moment"], (201,))
        ax_moment.plot(
            times[1:], second[1:], color=color, linewidth=1.05,
            label=str(seed["seed"]),
        )
    max_second = aggregate["maximum_observed_stage_tree_second_moment"]
    ax_moment.axhline(
        max_second, color="#333333", linewidth=0.8, linestyle=":",
    )
    ax_moment.set_xlim(0.0, 16.0)
    ax_moment.set_xlabel("time")
    ax_moment.set_ylabel("sample mean of $H^2$")
    ax_moment.set_title("C  Raw tree second-moment diagnostic", loc="left")
    ax_moment.grid(True, alpha=0.2)
    ax_moment.legend(
        frameon=True, facecolor="white", edgecolor="#DDDDDD", framealpha=0.94,
        ncol=1, loc="lower right",
    )
    ax_moment.text(
        0.98, 0.92, f"observed max {max_second:.4f}",
        transform=ax_moment.transAxes, ha="right", va="top", fontsize=8,
        color="#333333", bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.8},
    )
    ax_moment.text(
        0.02, 0.04, "diagnostic only; not an ensemble bound",
        transform=ax_moment.transAxes, color="#555555", fontsize=8,
    )

    cumulative_nodes = array(aggregate["cumulative_nodes_all_seeds"], (201,)) / 1.0e6
    cumulative_stage_seconds = array(
        aggregate["cumulative_recorded_stage_seconds_all_seeds"], (201,)
    )
    node_line = ax_work.plot(
        times, cumulative_nodes, color="#0072B2", linewidth=2.0,
        label="visited nodes",
    )[0]
    ax_work.set_xlim(0.0, 16.0)
    ax_work.set_xlabel("time")
    ax_work.set_ylabel("cumulative nodes (millions)", color="#0072B2")
    ax_work.tick_params(axis="y", colors="#0072B2")
    ax_work.grid(True, alpha=0.2)
    runtime_axis = ax_work.twinx()
    runtime_axis.spines["right"].set_visible(True)
    runtime_line = runtime_axis.plot(
        times, cumulative_stage_seconds, color="#D55E00", linewidth=1.7,
        linestyle="--", label="recorded stage time",
    )[0]
    runtime_axis.set_ylabel("cumulative recorded stage seconds", color="#D55E00")
    runtime_axis.tick_params(axis="y", colors="#D55E00")
    ax_work.set_title("D  Aggregate work across three paths", loc="left")
    ax_work.legend(
        (node_line, runtime_line), (node_line.get_label(), runtime_line.get_label()),
        frameon=False, loc="upper left",
    )
    ax_work.text(
        0.98,
        0.05,
        (
            f"sampling {summary['aggregate']['total_sampling_seconds']:.1f} s  ·  "
            f"stage {summary['aggregate']['total_recorded_stage_seconds']:.1f} s  ·  "
            f"three primary paths {summary['aggregate']['total_whole_run_elapsed_seconds']:.1f} s"
        ),
        transform=ax_work.transAxes,
        ha="right",
        va="bottom",
        fontsize=7.5,
        color="#444444",
    )

    fig.suptitle(
        "Dynamic continuation: accurate paths, but a cheaper midpoint already meets 0.02",
        fontsize=14,
        fontweight="bold",
        y=0.975,
    )
    fig.text(
        0.5,
        0.012,
        (
            "Three prescribed seeds are descriptive only. The 0.02 line is an ensemble RMS "
            "theorem at each endpoint, not a simultaneous pathwise confidence band. "
            f"Reference empirical floor: {summary['reference']['convergence_max']:.2e}."
        ),
        ha="center",
        va="bottom",
        fontsize=8,
        color="#444444",
    )
    fig.subplots_adjust(left=0.08, right=0.92, bottom=0.085, top=0.91, hspace=0.32, wspace=0.25)
    fig.savefig(png, dpi=300, facecolor="white")
    fig.savefig(svg, facecolor="white")
    plt.close(fig)


def summarize(audit_path: Path, output: Path, png: Path, svg: Path) -> dict:
    audit = read_json(audit_path)
    assert isinstance(audit, dict)
    if audit.get("passed") is not True:
        raise RuntimeError("refusing to summarize an audit that did not pass")
    seeds = audit["seeds"]
    if len(seeds) != 3:
        raise RuntimeError("expected exactly three seed records")
    times = array(seeds[0]["times"], (201,))
    if not all(np.array_equal(times, array(seed["times"], (201,))) for seed in seeds):
        raise RuntimeError("seed time grids disagree")

    mc_errors = np.stack([array(seed["errors"]["mc"], (201,)) for seed in seeds])
    empirical_rms = np.sqrt(np.mean(mc_errors * mc_errors, axis=0))
    empirical_mean = np.mean(mc_errors, axis=0)
    empirical_min = np.min(mc_errors, axis=0)
    empirical_max = np.max(mc_errors, axis=0)
    empirical_range = empirical_max - empirical_min
    empirical_sample_sd = np.std(mc_errors, axis=0, ddof=1)

    maximum_rms_index = int(np.argmax(empirical_rms))
    individual_index = np.unravel_index(int(np.argmax(mc_errors)), mc_errors.shape)
    stage_nodes = np.stack([array(seed["stage_nodes"], (201,)) for seed in seeds])
    stage_seconds = np.stack([array(seed["stage_seconds"], (201,)) for seed in seeds])
    sampling_seconds = np.stack(
        [array(seed["sampling_seconds"], (201,)) for seed in seeds]
    )
    cumulative_nodes = np.cumsum(np.sum(stage_nodes, axis=0))
    cumulative_stage_seconds = np.cumsum(np.sum(stage_seconds, axis=0))

    baseline_records: dict[str, dict] = {}
    for name in ("g", "0.95g", "0.9g"):
        values = array(seeds[0]["errors"][name], (201,))
        for seed in seeds[1:]:
            if not np.array_equal(values, array(seed["errors"][name], (201,))):
                raise RuntimeError(f"baseline {name} differs between seed records")
        max_index = int(np.argmax(values))
        poststage_index = int(np.argmax(values[1:])) + 1
        baseline_records[name] = {
            "errors": values.tolist(),
            "maximum_error": float(values[max_index]),
            "maximum_time": float(times[max_index]),
            "poststage_maximum_error": float(values[poststage_index]),
            "poststage_maximum_time": float(times[poststage_index]),
        }

    selected: list[dict] = []
    for selected_time in SELECTED_TIMES:
        indices = np.flatnonzero(np.isclose(times, selected_time, rtol=0.0, atol=1.0e-14))
        if indices.size != 1:
            raise RuntimeError(f"selected time {selected_time} is absent or ambiguous")
        index = int(indices[0])
        selected.append(
            {
                "time": float(times[index]),
                "stage": index,
                "mc_errors_by_seed": mc_errors[:, index].tolist(),
                "mc_empirical_rms": float(empirical_rms[index]),
                "mc_mean": float(empirical_mean[index]),
                "mc_min": float(empirical_min[index]),
                "mc_max": float(empirical_max[index]),
                "mc_range": float(empirical_range[index]),
                "mc_sample_standard_deviation": float(empirical_sample_sd[index]),
                "g_error": baseline_records["g"]["errors"][index],
                "0.95g_error": baseline_records["0.95g"]["errors"][index],
                "0.9g_error": baseline_records["0.9g"]["errors"][index],
            }
        )

    second_moment_values = np.asarray(
        [
            value
            for seed in seeds
            for value in seed["tree_value_second_moment"][1:]
        ],
        dtype=float,
    )
    total_sampling = float(np.sum(sampling_seconds))
    total_stage = float(np.sum(stage_seconds))
    total_whole = float(sum(seed["whole_run_elapsed_seconds"] for seed in seeds))
    per_seed_whole = [float(seed["whole_run_elapsed_seconds"]) for seed in seeds]
    reference = audit["reference"]
    finest_reference_seconds = float(reference["finest_solve_seconds"])
    validation_reference_seconds = float(reference["total_validation_seconds"])

    compact_seeds = []
    for seed in seeds:
        compact_seeds.append(
            {
                "seed": seed["seed"],
                "status": seed["status"],
                "root_count": seed["root_count"],
                "total_nodes": seed["total_nodes"],
                "projection_count": seed["projection_count"],
                "projection_frequency": seed["projection_count"] / 200.0,
                "whole_run_elapsed_seconds": seed["whole_run_elapsed_seconds"],
                "sum_sampling_seconds": seed["sum_sampling_seconds"],
                "sum_stage_seconds": seed["sum_stage_seconds"],
                "errors": seed["errors"],
                "coefficients": seed["coefficients"],
                "projection_active": seed["projection_active"],
                "tree_value_second_moment": seed["tree_value_second_moment"],
                "stage_roots": seed["stage_roots"],
                "stage_nodes": seed["stage_nodes"],
                "sampling_seconds": seed["sampling_seconds"],
                "stage_seconds": seed["stage_seconds"],
            }
        )

    result: dict[str, object] = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "passed": True,
        "audit_passed": True,
        "description": "Compact reproducible summary of the dynamic continuation experiment",
        "scope": {
            "three_seed_interpretation": (
                "Descriptive only; no confidence interval, rare-tail estimate, or "
                "simultaneous all-times probability statement"
            ),
            "theory_envelope": (
                "0.02 is a per-endpoint ensemble normalized-spatial RMS theorem, "
                "not a bound on the observed sample maximum"
            ),
            "reference": (
                "Floating-point deterministic proxy with empirical convergence floor; "
                "not a rigorous PDE enclosure"
            ),
        },
        "times": times.tolist(),
        "time_zero": {
            "exact_initialization": True,
            "mc_error_recorded_as_exact_zero": True,
            "reference_proxy_discrepancy_for_0.9g": reference[
                "numeric_proxy_discrepancy_at_t0_for_exact_0.9g"
            ],
        },
        "seeds": compact_seeds,
        "aggregate": {
            "mc_error_empirical_rms": empirical_rms.tolist(),
            "mc_error_mean": empirical_mean.tolist(),
            "mc_error_min": empirical_min.tolist(),
            "mc_error_max": empirical_max.tolist(),
            "mc_error_range": empirical_range.tolist(),
            "mc_error_sample_standard_deviation": empirical_sample_sd.tolist(),
            "maximum_empirical_rms": float(empirical_rms[maximum_rms_index]),
            "maximum_empirical_rms_time": float(times[maximum_rms_index]),
            "maximum_empirical_rms_stage": maximum_rms_index,
            "maximum_individual_mc_error": float(mc_errors[individual_index]),
            "maximum_individual_mc_error_seed": seeds[individual_index[0]]["seed"],
            "maximum_individual_mc_error_time": float(times[individual_index[1]]),
            "all_observed_mc_errors_below_0.02": bool(np.max(mc_errors) < THEORY_ENVELOPE),
            "projection_count": int(sum(seed["projection_count"] for seed in seeds)),
            "projection_frequency": float(
                sum(seed["projection_count"] for seed in seeds) / 600.0
            ),
            "maximum_observed_stage_tree_second_moment": float(
                np.max(second_moment_values)
            ),
            "sample_second_moment_is_not_an_ensemble_bound": True,
            "total_roots": int(sum(seed["root_count"] for seed in seeds)),
            "total_nodes": int(sum(seed["total_nodes"] for seed in seeds)),
            "total_sampling_seconds": total_sampling,
            "total_recorded_stage_seconds": total_stage,
            "total_whole_run_elapsed_seconds": total_whole,
            "whole_run_timing_scope": (
                "Sum of the three primary path elapsed times recorded in progress.json; "
                "excludes preflight checks, deterministic-reference validation, this "
                "independent audit, and summarization/plotting"
            ),
            "cumulative_nodes_all_seeds": cumulative_nodes.tolist(),
            "cumulative_recorded_stage_seconds_all_seeds": (
                cumulative_stage_seconds.tolist()
            ),
        },
        "baselines": baseline_records,
        "selected_endpoints": selected,
        "reference": {
            "convergence_max": reference["convergence_max"],
            "finest_solve_seconds": finest_reference_seconds,
            "total_validation_seconds": validation_reference_seconds,
            "mc_per_seed_whole_runtime_seconds": per_seed_whole,
            "per_seed_whole_runtime_over_finest_reference_solve": [
                value / finest_reference_seconds for value in per_seed_whole
            ],
            "mean_seed_whole_runtime_over_finest_reference_solve": (
                float(np.mean(per_seed_whole)) / finest_reference_seconds
            ),
            "per_seed_whole_runtime_over_full_reference_validation": [
                value / validation_reference_seconds for value in per_seed_whole
            ],
            "mc_whole_runtime_over_finest_reference_solve": (
                total_whole / finest_reference_seconds
            ),
            "mc_whole_runtime_over_full_reference_validation": (
                total_whole / validation_reference_seconds
            ),
        },
        "honest_comparison": {
            "midpoint_0.95g_maximum_error": baseline_records["0.95g"]["maximum_error"],
            "midpoint_already_below_0.02": bool(
                baseline_records["0.95g"]["maximum_error"] < THEORY_ENVELOPE
            ),
            "deterministic_reference_is_faster": bool(finest_reference_seconds < total_whole),
            "conclusion": (
                "The paths validate the continuation mechanism on this benchmark, "
                "while the pre-data midpoint 0.95g already meets 0.02 and the "
                "deterministic spectral reference is much faster."
            ),
        },
        "audit": {
            "path": str(audit_path.resolve()),
            "sha256": sha256(audit_path),
            "duration_seconds": audit["duration_seconds"],
            "counts": audit["counts"],
            "maximum_absolute_differences": audit["maximum_absolute_differences"],
            "source_and_data_hashes_sha256": audit["source_and_data_hashes_sha256"],
        },
        "regeneration_commands": [
            (
                "/opt/miniconda3/envs/parabolab/bin/python "
                "docs/research/runs/2026-09-28-dynamic-continuation/numerics/"
                "audit_dynamic.py"
            ),
            (
                "/opt/miniconda3/envs/parabolab/bin/python "
                "docs/research/runs/2026-09-28-dynamic-continuation/numerics/"
                "summarize_dynamic.py"
            ),
        ],
    }

    make_figure(result, png, svg)
    result["outputs"] = {
        "summary_json": str(output.resolve()),
        "figure_png": str(png.resolve()),
        "figure_svg": str(svg.resolve()),
        "figure_png_sha256": sha256(png),
        "figure_svg_sha256": sha256(svg),
    }
    result["source_hashes_sha256"] = {
        "audit_dynamic.py": sha256(HERE / "audit_dynamic.py"),
        "summarize_dynamic.py": sha256(HERE / "summarize_dynamic.py"),
    }
    write_json(output, result)
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, default=AUDIT_JSON)
    parser.add_argument("--output", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--png", type=Path, default=PNG)
    parser.add_argument("--svg", type=Path, default=SVG)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = summarize(
        args.audit.resolve(), args.output.resolve(), args.png.resolve(), args.svg.resolve()
    )
    print(
        json.dumps(
            {
                "passed": summary["passed"],
                "maximum_empirical_rms": summary["aggregate"]["maximum_empirical_rms"],
                "maximum_individual_mc_error": summary["aggregate"][
                    "maximum_individual_mc_error"
                ],
                "midpoint_0.95g_maximum_error": summary["honest_comparison"][
                    "midpoint_0.95g_maximum_error"
                ],
                "total_whole_run_elapsed_seconds": summary["aggregate"][
                    "total_whole_run_elapsed_seconds"
                ],
                "output": str(args.output.resolve()),
            },
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
    )


if __name__ == "__main__":
    main()
