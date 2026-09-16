"""Tests for parabolab.deep.benchmark (spec 2026-09-16-backbone-benchmark-design,
task 4) and examples/backbone_benchmark.py (task 5)."""

import numpy as np
import pytest

from parabolab.deep import benchmark


def _rec(family, backbone, n, l1s):
    return [{"family": family, "backbone": backbone, "n_train": n, "instance_seed": i,
             "l1": v, "seconds": 1.0}
            for i, v in enumerate(l1s)]


def test_scores_and_failures():
    # y's family-A values are [3, 3, 3] (not [2, 2, 2]) to make the ranking
    # decisive: with baseline A median 1, ratio_median(A, y, 1000) = 3.0, so
    # S_y = sqrt(3 * 0.5) ~= 1.22 > S_x = sqrt(0.5 * 2.0) = 1.0. x's only
    # failure family is B (ratio 2.0 > 1.5); y's only failure family is A
    # (ratio 3.0 > 1.5).
    recs = (_rec("A", "per_phi", 0, [1, 1, 1]) + _rec("A", "x", 1000, [0.5, 0.5, 2.0]) + _rec("A", "y", 1000, [3, 3, 3])
            + _rec("B", "per_phi", 0, [2, 2, 2]) + _rec("B", "x", 1000, [4, 4, 4]) + _rec("B", "y", 1000, [1, 1, 1])
            + _rec("A", "x", 250, [1, 1, 1]))
    r = benchmark.family_ratios(recs)
    assert r[("A", "x", 1000)]["ratio_median"] == 0.5 and r[("B", "x", 1000)]["ratio_median"] == 2.0
    assert r[("A", "y", 1000)]["ratio_median"] == 3.0 and r[("B", "y", 1000)]["ratio_median"] == 0.5

    ranked = benchmark.overall_scores(r)
    assert [b for b, *_ in ranked] == ["x", "y"]
    x_row, y_row = ranked
    assert x_row[1] == pytest.approx(1.0)
    assert y_row[1] == pytest.approx(np.sqrt(1.5))
    assert x_row[3] == ["B"]
    assert y_row[3] == ["A"]

    table = benchmark.report_table(r)
    assert "| A |" in table and "robustness" in table.lower()


def test_family_ratios_requires_baseline():
    recs = _rec("A", "x", 1000, [1.0, 1.0])
    with pytest.raises(ValueError):
        benchmark.family_ratios(recs)


def test_report_table_has_learning_curve_slope_section():
    recs = (_rec("A", "per_phi", 0, [1, 1, 1]) + _rec("A", "x", 250, [1, 1, 1])
            + _rec("A", "x", 1000, [0.5, 0.5, 0.5]))
    r = benchmark.family_ratios(recs)
    table = benchmark.report_table(r)
    assert "learning-curve slope" in table.lower()


def test_report_table_warns_on_uneven_family_coverage():
    # x is scored on both A and B, y only on A (e.g. a resumed run that
    # skipped B for y) -- ranking them against each other is comparing
    # geometric means over different family sets, so report_table must warn.
    recs = (_rec("A", "per_phi", 0, [1, 1, 1]) + _rec("B", "per_phi", 0, [1, 1, 1])
            + _rec("A", "x", 1000, [0.5, 0.5, 0.5]) + _rec("B", "x", 1000, [0.5, 0.5, 0.5])
            + _rec("A", "y", 1000, [0.5, 0.5, 0.5]))
    r = benchmark.family_ratios(recs)
    assert benchmark.family_coverage(r, n_train=1000) == {"x": 2, "y": 1}
    table = benchmark.report_table(r)
    assert "warning: backbones scored over different family sets" in table
    assert "x (2)" in table and "y (1)" in table


def test_report_table_no_warning_on_even_family_coverage():
    recs = (_rec("A", "per_phi", 0, [1, 1, 1]) + _rec("B", "per_phi", 0, [1, 1, 1])
            + _rec("A", "x", 1000, [0.5, 0.5, 0.5]) + _rec("B", "x", 1000, [0.5, 0.5, 0.5])
            + _rec("A", "y", 1000, [0.5, 0.5, 0.5]) + _rec("B", "y", 1000, [0.5, 0.5, 0.5]))
    r = benchmark.family_ratios(recs)
    table = benchmark.report_table(r)
    assert "warning" not in table.lower()


# ---------------------------------------------------------------------------
# driver (examples/backbone_benchmark.py)
# ---------------------------------------------------------------------------

import csv
import json
import subprocess
import sys
from pathlib import Path

pytest.importorskip("torch")

SCRIPT = Path(__file__).resolve().parents[1] / "examples" / "backbone_benchmark.py"


def test_backbone_benchmark_driver_tiny(tmp_path):
    out = tmp_path / "bb.csv"
    subprocess.run([sys.executable, str(SCRIPT), "--tiny", "--families", "heat_phi",
                    "--jobs", "1", "--corpus-root", str(tmp_path / "corpus"), "--out", str(out)],
                   check=True, capture_output=True, text=True)
    rows = list(csv.DictReader(out.open()))
    assert {r["backbone"] for r in rows} == {"per_phi", "deeponet", "fno", "attn", "coeffmlp"}
    assert {int(r["n_train"]) for r in rows if r["backbone"] != "per_phi"} == {2, 3}

    result = subprocess.run([sys.executable, str(SCRIPT), "--report", "--out", str(out)],
                            check=True, capture_output=True, text=True)
    assert "Ranked" in result.stdout


def test_backbone_benchmark_driver_precheck(tmp_path):
    pc_out = tmp_path / "pc.json"
    subprocess.run([sys.executable, str(SCRIPT), "--precheck", "--tiny", "--families", "heat_phi",
                    "--precheck-out", str(pc_out)],
                   check=True, capture_output=True, text=True)
    result = json.loads(pc_out.read_text())
    assert "heat_phi" in result
    assert isinstance(result["heat_phi"]["passed"], bool)
