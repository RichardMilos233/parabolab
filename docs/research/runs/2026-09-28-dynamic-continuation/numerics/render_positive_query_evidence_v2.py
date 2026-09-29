"""Reproduce the accepted T66 positive-query evidence figure without oracle calls.

The plotting calls are the exact accepted layout-only recipe.  The only
packaging change is deterministic SVG serialization: a fixed SVG hash salt and
metadata date replace Matplotlib's process-random IDs and current timestamp.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import sys
import time
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO = HERE.parents[4]
SOURCE = Path(__file__).resolve()
AUDIT_DIR = RUN_DIR / "artifacts" / "positive-query-sampling" / "audit-v1"
STORED_AUDIT = AUDIT_DIR / "stored_audit.json"
REPLAY_RESULT = AUDIT_DIR / "replay_result.json"
ACCEPTED_PNG = AUDIT_DIR / "positive_query_audit.png"
ACCEPTED_SVG = AUDIT_DIR / "positive_query_audit.svg"
OUTPUT_DIR = RUN_DIR / "artifacts" / "positive-query-sampling" / "figure-v2"
OUTPUT_PNG = OUTPUT_DIR / "positive_query_evidence_v2.png"
OUTPUT_SVG = OUTPUT_DIR / "positive_query_evidence_v2.svg"
OUTPUT_RESULT = OUTPUT_DIR / "render_result.json"

EXPECTED = {
    "stored_audit": "f1f48b74996543a9f7de1aca6c0ffedbb54e34d251d046aa820b0cf9cea5f2da",
    "replay_result": "788394e129bebda45608a926b118cc405e515f2986f60a3acc7992713ea3ed2e",
    "accepted_png": "3c18c54eb64f89473cafef04760a2fb6ea2edba8371c353cc1f9a481daebef2f",
    "accepted_svg": "6832d357371ff8e6f86557746c13ccfc279ba9a386072830aedd1f049f279849",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return str(path.resolve().relative_to(REPO.resolve()))


def write_json_new(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    started = time.perf_counter()
    require(not OUTPUT_DIR.exists(), f"refusing to overwrite {OUTPUT_DIR}")
    actual_inputs = {
        "stored_audit": sha256(STORED_AUDIT),
        "replay_result": sha256(REPLAY_RESULT),
        "accepted_png": sha256(ACCEPTED_PNG),
        "accepted_svg": sha256(ACCEPTED_SVG),
    }
    require(actual_inputs == EXPECTED, f"frozen input mismatch: {actual_inputs}")
    stored = json.loads(STORED_AUDIT.read_text(encoding="utf-8"))
    replay = json.loads(REPLAY_RESULT.read_text(encoding="utf-8"))
    require(stored["status"] == replay["status"] == "PASS", "accepted audit gates are not PASS")
    statistics = stored["statistics"]
    per_seed = statistics["per_seed_cells"]
    pooled = statistics["pooled_cells"]
    baselines = statistics["zero_query_baselines"]

    levels = (0.0, 0.25, 1.0, 4.0)
    schedules = (
        ("growing_0p125", 128),
        ("growing_0p5", 128),
        ("growing_2", 128),
        ("theorem_96", 8),
        ("fixed_51", 128),
    )
    colors = {
        "growing_0p125": "#0072B2",
        "growing_0p5": "#009E73",
        "growing_2": "#E69F00",
        "theorem_96": "#D55E00",
        "fixed_51": "#CC79A7",
    }
    baseline_styles = {
        "constant_0": ("#222222", ":"),
        "constant_0.5": ("#666666", "--"),
        "constant_1": ("#999999", "-."),
    }
    pde_bias = 1 / 32

    # Exact accepted layout recipe begins here.
    figure, axes = plt.subplots(4, 2, figsize=(15.5, 18.5))
    figure.subplots_adjust(
        top=0.82,
        bottom=0.055,
        left=0.075,
        right=0.98,
        hspace=0.52,
        wspace=0.24,
    )
    for level_index, level in enumerate(levels):
        rms_axis, query_axis = axes[level_index]
        for schedule, repetitions in schedules:
            color = colors[schedule]
            pooled_rows = sorted(
                (
                    row
                    for row in pooled
                    if row["nominal_z"] == level and row["schedule"] == schedule
                ),
                key=lambda row: row["T"],
            )
            seed_rows = [
                row
                for row in per_seed
                if row["nominal_z"] == level and row["schedule"] == schedule
            ]
            horizons = [row["T"] for row in pooled_rows]
            rms_values = [row["rms"] for row in pooled_rows]
            rms_axis.scatter(
                [row["T"] for row in seed_rows],
                [row["rms"] for row in seed_rows],
                s=24,
                facecolors="none",
                edgecolors=color,
                alpha=0.5,
                linewidths=0.9,
            )
            rms_axis.plot(
                horizons,
                rms_values,
                color=color,
                marker="o",
                linewidth=2.1,
                label=f"{schedule} (R={repetitions}/seed)",
            )
            rms_axis.errorbar(
                horizons,
                rms_values,
                yerr=[
                    [min(pde_bias, value) for value in rms_values],
                    [pde_bias] * len(rms_values),
                ],
                fmt="none",
                ecolor=color,
                alpha=0.2,
                capsize=2,
            )
            queries = [row["actual_mean_queries_per_output"] for row in pooled_rows]
            for offset in (-0.14, 0.0, 0.14):
                query_axis.scatter(
                    [horizon + offset for horizon in horizons],
                    queries,
                    s=25,
                    facecolors="none",
                    edgecolors=color,
                    alpha=0.55,
                    linewidths=0.9,
                )
            query_axis.plot(
                horizons,
                queries,
                color=color,
                marker="o",
                linewidth=2.1,
                label=f"{schedule} (R={repetitions}/seed)",
            )
        for name, (color, linestyle) in baseline_styles.items():
            baseline_rows = sorted(
                (
                    row
                    for row in baselines
                    if row["nominal_z"] == level and row["name"] == name
                ),
                key=lambda row: row["T"],
            )
            horizons = [row["T"] for row in baseline_rows]
            rms_values = [row["rms"] for row in baseline_rows]
            rms_axis.plot(
                horizons,
                rms_values,
                color=color,
                linestyle=linestyle,
                marker="s",
                linewidth=1.6,
                label=f"{name} (0 queries)",
            )
            rms_axis.errorbar(
                horizons,
                rms_values,
                yerr=[
                    [min(pde_bias, value) for value in rms_values],
                    [pde_bias] * len(rms_values),
                ],
                fmt="none",
                ecolor=color,
                alpha=0.14,
                capsize=2,
            )
            query_axis.plot(
                horizons,
                [0] * len(horizons),
                color=color,
                linestyle=linestyle,
                marker="s",
                linewidth=1.6,
                label=f"{name} (0 queries)",
            )
        rms_axis.set(
            title=f"nominal z={level:g}: error against scalar surrogate",
            xlabel="horizon T",
            ylabel="empirical RMS",
        )
        rms_axis.set_xticks((12, 16, 20))
        rms_axis.set_yscale("symlog", linthresh=1e-5)
        rms_axis.set_ylim(bottom=0)
        rms_axis.grid(True, which="both", alpha=0.25)
        query_axis.set(
            title=f"nominal z={level:g}: actual query budget per output",
            xlabel="horizon T",
            ylabel="point queries",
        )
        query_axis.set_xticks((12, 16, 20))
        query_axis.set_yscale("symlog", linthresh=1)
        query_axis.set_ylim(bottom=0)
        query_axis.grid(True, which="both", alpha=0.25)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    figure.suptitle(
        "Frozen positive-query experiment — independent audit",
        fontsize=17,
        y=0.978,
    )
    figure.text(
        0.5,
        0.948,
        "RMS uses the computed binary64 scalar surrogate; no PDE was numerically solved and no float enclosure is claimed.",
        ha="center",
        fontsize=11,
    )
    figure.text(
        0.5,
        0.927,
        "Solid points/lines: pooled raw-square RMS · open points: individual seeds · whiskers: conventional PDE comparison ±1/32",
        ha="center",
        fontsize=11,
    )
    figure.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.905),
        ncol=4,
        fontsize=9,
        frameon=False,
    )
    # Exact accepted layout recipe ends here.

    OUTPUT_DIR.mkdir(parents=True, exist_ok=False)
    figure.savefig(
        OUTPUT_PNG,
        dpi=180,
        metadata={"Title": "Independent positive-query sampling audit"},
    )
    matplotlib.rcParams["svg.hashsalt"] = "T66-positive-query-evidence-v2"
    figure.savefig(
        OUTPUT_SVG,
        metadata={
            "Title": "Independent positive-query sampling audit",
            "Date": "2026-09-29T00:13:51.476287+07:00",
        },
    )
    plt.close(figure)

    png_hash = sha256(OUTPUT_PNG)
    svg_hash = sha256(OUTPUT_SVG)
    require(
        png_hash == EXPECTED["accepted_png"],
        f"PNG did not reproduce the accepted bytes: {png_hash}",
    )
    write_json_new(
        OUTPUT_RESULT,
        {
            "schema_version": 1,
            "status": "PASS",
            "completed_utc": datetime.now(timezone.utc).isoformat(),
            "renderer_source": relative(SOURCE),
            "renderer_source_sha256": sha256(SOURCE),
            "frozen_input_hashes_sha256": {
                relative(STORED_AUDIT): EXPECTED["stored_audit"],
                relative(REPLAY_RESULT): EXPECTED["replay_result"],
                relative(ACCEPTED_PNG): EXPECTED["accepted_png"],
                relative(ACCEPTED_SVG): EXPECTED["accepted_svg"],
            },
            "outputs_sha256": {
                relative(OUTPUT_PNG): png_hash,
                relative(OUTPUT_SVG): svg_hash,
            },
            "accepted_png_reproduced_byte_for_byte": True,
            "svg_serialization": {
                "visual_recipe": "exact accepted layout recipe",
                "deterministic_packaging_changes": [
                    "fixed matplotlib.rcParams['svg.hashsalt']",
                    "fixed SVG metadata Date",
                ],
                "accepted_svg_byte_identity_expected": False,
                "reason": "the accepted SVG used Matplotlib's process-random IDs and a live timestamp",
            },
            "scope": {
                "statistics_recomputed": False,
                "oracle_calls": 0,
                "ledger_changes": 0,
                "official_or_audit_evidence_modified": False,
            },
            "environment": {
                "python_executable": sys.executable,
                "python_version": sys.version,
                "matplotlib_version": importlib.metadata.version("matplotlib"),
                "platform": platform.platform(),
                "machine": platform.machine(),
            },
            "render_wall_seconds": time.perf_counter() - started,
            "timing_interpretation": "Wall time includes frozen-statistics parsing, rendering and serialization; no pure-compute claim.",
        },
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "accepted_png_reproduced_byte_for_byte": True,
                "png_sha256": png_hash,
                "svg_sha256": svg_hash,
                "oracle_calls": 0,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
