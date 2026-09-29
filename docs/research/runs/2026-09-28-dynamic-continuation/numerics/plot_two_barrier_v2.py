"""Render the versioned T38 figure with exact zero errors visible."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
from typing import Any

import numpy as np


HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO = HERE.parents[4]
AUDIT_DIR = RUN_DIR / "artifacts" / "two-barrier" / "audit-v1"
OUTPUT_DIR = RUN_DIR / "artifacts" / "two-barrier" / "figure-v2"
MANIFEST_PATH = OUTPUT_DIR / "execution_manifest.json"
QA_PATH = OUTPUT_DIR / "render_qa.json"
PNG_PATH = RUN_DIR / "two-barrier-results-v2.png"
SVG_PATH = RUN_DIR / "two-barrier-results-v2.svg"
TABLES_PATH = AUDIT_DIR / "derived_tables.json"
AUDIT_SUMMARY_PATH = AUDIT_DIR / "audit_summary.json"
AUDIT_MANIFEST_PATH = AUDIT_DIR / "execution_manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return str(path.resolve().relative_to(REPO.resolve()))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json_new(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def fixed_inputs() -> list[Path]:
    return [Path(__file__).resolve(), TABLES_PATH, AUDIT_SUMMARY_PATH, AUDIT_MANIFEST_PATH]


def prepare() -> None:
    if OUTPUT_DIR.exists() or PNG_PATH.exists() or SVG_PATH.exists():
        raise FileExistsError("refusing to overwrite versioned figure evidence")
    audit = json.loads(AUDIT_SUMMARY_PATH.read_text(encoding="utf-8"))
    if audit.get("status") != "PASS" or audit.get("checks_passed") != audit.get("checks_total"):
        raise RuntimeError("frozen audit-v1 is not a complete PASS")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=False)
    hashes = {relative(path): sha256(path) for path in fixed_inputs()}
    manifest = {
        "schema_version": 1,
        "status": "prepared-before-versioned-render",
        "created_utc": utc_now(),
        "source": relative(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
        "input_hashes_sha256": hashes,
        "environment": {
            "python_executable": sys.executable,
            "python_version": sys.version,
            "numpy_version": np.__version__,
            "platform": platform.platform(),
        },
        "scope": {
            "presentation_only": True,
            "reads_frozen_derived_tables": True,
            "resamples": False,
            "reruns_reference_solver": False,
            "changes_values": False,
            "preserves_v1_figures": True,
            "reason": "show exact zero diagnostics on a symmetric-log y axis",
        },
    }
    write_json_new(MANIFEST_PATH, manifest)
    print(json.dumps({"status": "prepared", "output": str(OUTPUT_DIR)}))


def verify_inputs() -> dict[str, Any]:
    if not MANIFEST_PATH.is_file():
        raise RuntimeError("versioned figure manifest is missing")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    current = {relative(path): sha256(path) for path in fixed_inputs()}
    if current != manifest["input_hashes_sha256"]:
        raise RuntimeError("figure inputs changed after manifest freeze")
    return manifest


def run() -> None:
    manifest = verify_inputs()
    if QA_PATH.exists() or PNG_PATH.exists() or SVG_PATH.exists():
        raise FileExistsError("refusing to overwrite versioned figure evidence")
    data = json.loads(TABLES_PATH.read_text(encoding="utf-8"))

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    times = np.asarray(data["times"], dtype=np.float64)
    reference = np.asarray(data["reference_scaled_values"], dtype=np.float64)
    means = np.asarray(data["mc_seed_means"], dtype=np.float64)
    rms = np.asarray(data["empirical_three_seed_rms"], dtype=np.float64)
    harmonic_error = np.abs(np.asarray(data["harmonic_center_signed_relative_errors"], dtype=np.float64))
    mean_error = np.abs(np.asarray(data["mean_ode_signed_relative_errors"], dtype=np.float64))
    work_nodes = np.asarray(data["aggregate_mean_nodes_by_time"], dtype=np.float64)
    work_proposals = np.asarray(data["aggregate_mean_clock_proposals_by_time"], dtype=np.float64)
    seeds = tuple(int(value) for value in data["seeds"])
    bounds = data["theoretical_expectation_bounds"]

    expected_shapes = (
        times.shape == (7,)
        and reference.shape == (7, 3)
        and means.shape == (3, 7, 3)
        and rms.shape == (7, 3)
        and harmonic_error.shape == (7, 3)
        and mean_error.shape == (7, 3)
    )
    if not expected_shapes:
        raise RuntimeError("frozen derived-table shapes do not match the fixed figure contract")
    if tuple(times) != (0.0, 0.25, 1.0, 4.0, 16.0, 64.0, 256.0):
        raise RuntimeError("frozen time grid changed")

    colors = ("#006D77", "#D1495B", "#6A4C93")
    query_labels = ("x=0", "x=π/2", "x=π")
    seed_markers = ("o", "s", "^")
    fig, axes = plt.subplots(1, 3, figsize=(17.2, 5.4), constrained_layout=True)

    ax = axes[0]
    for qi, label in enumerate(query_labels):
        ax.plot(times, reference[:, qi], color=colors[qi], linewidth=2.4,
                label=f"reference {label}")
        for si, seed in enumerate(seeds):
            ax.plot(times, means[si, :, qi], linestyle="none", marker=seed_markers[si],
                    markersize=4.2, markerfacecolor="none", color=colors[qi], alpha=0.8,
                    label=f"MC {label}, seed {str(seed)[-2:]}" if qi == 0 else None)
    ax.set_xscale("symlog", linthresh=0.25)
    ax.set_xlim(-0.02, 300.0)
    ax.set_xlabel("finite horizon T (symlog; includes 0)")
    ax.set_ylabel("scaled defect exp(2T)(1-u)")
    ax.set_title("Reference and 3×10,000-root means")
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=7.2, ncol=2)

    ax = axes[1]
    ax.plot(times, np.max(rms, axis=1), color="#111111", marker="o", linewidth=2.2,
            label="max of 3 query-wise RMS₃ diagnostics")
    for qi, label in enumerate(query_labels):
        ax.plot(times, harmonic_error[:, qi], color=colors[qi], linestyle="--", marker=".",
                label=f"|harmonic rel. error|, {label}")
        ax.plot(times, mean_error[:, qi], color=colors[qi], linestyle=":", marker="x",
                label=f"|mean-ODE rel. error|, {label}")
    ax.axhline(0.0, color="#777777", linewidth=0.8, alpha=0.65)
    ax.set_xscale("symlog", linthresh=0.25)
    ax.set_xlim(-0.02, 300.0)
    ax.set_yscale("symlog", linthresh=1.0e-4, linscale=0.8)
    ax.set_ylim(-3.0e-5, 0.8)
    ax.set_xlabel("finite horizon T (symlog; includes 0)")
    ax.set_ylabel("relative diagnostic (symlog; exact zeros shown)")
    ax.set_title("Fixed diagnostics; all 21 values retained in JSON")
    ax.annotate("exact T=0 zeros", xy=(0.0, 0.0), xytext=(0.4, 2.2e-4),
                arrowprops={"arrowstyle": "->", "color": "#444444"}, fontsize=7.5)
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=6.8, loc="upper right")

    ax = axes[2]
    ax.plot(times, work_nodes, color="#00798C", marker="o", linewidth=2.2,
            label="empirical mean nodes (90k roots/T)")
    ax.plot(times, work_proposals, color="#D1495B", marker="s", linewidth=2.2,
            label="empirical mean proposals (90k roots/T)")
    ax.axhline(float(bounds["mean_nodes"]), color="#00798C", linestyle="--", linewidth=1.5,
               label="theoretical E[nodes] upper bound")
    ax.axhline(float(bounds["mean_clock_proposals"]), color="#D1495B", linestyle="--", linewidth=1.5,
               label="theoretical E[proposals] upper bound")
    ax.set_xscale("symlog", linthresh=0.25)
    ax.set_xlim(-0.02, 300.0)
    ax.set_xlabel("finite horizon T (symlog; includes 0)")
    ax.set_ylabel("root work count")
    ax.set_title("Empirical work means vs expectation bounds")
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=7.2)

    fig.suptitle(
        "Two-barrier experiment — fixed v(x)=5/8+(1/8)cos x; 3 seeds; 10,000 roots/cell",
        fontsize=13,
    )
    fig.savefig(PNG_PATH, dpi=180)
    fig.savefig(SVG_PATH)
    plt.close(fig)

    qa = {
        "schema_version": 1,
        "status": "PASS",
        "created_utc": utc_now(),
        "manifest_sha256": sha256(MANIFEST_PATH),
        "source_sha256": manifest["source_sha256"],
        "input_derived_tables_sha256": sha256(TABLES_PATH),
        "no_values_changed": True,
        "resampled": False,
        "reference_solver_rerun": False,
        "exact_zero_counts": {
            "empirical_three_seed_rms": int(np.sum(rms == 0.0)),
            "harmonic_center_absolute_relative_errors": int(np.sum(harmonic_error == 0.0)),
            "mean_ode_absolute_relative_errors": int(np.sum(mean_error == 0.0)),
        },
        "error_axis": {"scale": "symlog", "linthresh": 1.0e-4, "exact_zeros_visible": True},
        "outputs": {
            relative(PNG_PATH): {"sha256": sha256(PNG_PATH), "bytes": PNG_PATH.stat().st_size},
            relative(SVG_PATH): {"sha256": sha256(SVG_PATH), "bytes": SVG_PATH.stat().st_size},
        },
    }
    write_json_new(QA_PATH, qa)
    print(json.dumps({"status": "PASS", "png": str(PNG_PATH), "svg": str(SVG_PATH)}))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "run"))
    args = parser.parse_args()
    if args.action == "prepare":
        prepare()
    else:
        run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
