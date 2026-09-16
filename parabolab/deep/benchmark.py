"""Scoring for the phi -> u backbone benchmark (spec
2026-09-16-phi-operator-design, task 4).

A benchmark *record* is a plain dict with keys ``family``, ``backbone``,
``n_train``, ``instance_seed``, ``l1``, ``seconds``. Baseline (per-instance
MLP) rows have ``backbone == "per_phi"`` and ``n_train == 0``; every other
row is one pooled-operator backbone trained on ``n_train`` instances,
evaluated per held-out instance (``instance_seed`` distinguishes repeats).

``family_ratios`` normalizes every non-baseline (family, backbone, n_train)
cell against that family's own baseline L1 distribution -- a ratio < 1 means
the backbone beats per-instance training on that family. ``overall_scores``
and ``report_table`` build on those ratios; nothing here trains a network or
touches torch.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Sequence, Tuple

import numpy as np

# A backbone "fails" a family at a given n_train when its median L1 is more
# than this multiple of the per-instance baseline's median L1.
FAILURE_RATIO = 1.5

RatioKey = Tuple[str, str, int]


def family_ratios(records: Sequence[dict]) -> Dict[RatioKey, dict]:
    """Normalize each (family, backbone, n_train) L1 distribution against
    that family's per_phi baseline.

    Returns one entry per non-baseline key present in ``records``, with
    ``ratio_median``/``ratio_max`` = that key's median/max L1 divided by the
    same family's baseline median/max L1, plus the raw ``l1_median``,
    ``l1_max`` and sample count ``n``.
    """
    groups: Dict[RatioKey, List[float]] = defaultdict(list)
    baselines: Dict[str, List[float]] = defaultdict(list)
    for r in records:
        groups[(r["family"], r["backbone"], r["n_train"])].append(float(r["l1"]))
        if r["backbone"] == "per_phi":
            baselines[r["family"]].append(float(r["l1"]))

    out: Dict[RatioKey, dict] = {}
    for (family, backbone, n_train), l1s in groups.items():
        if backbone == "per_phi":
            continue
        base = baselines.get(family)
        if not base:
            raise ValueError(f"no per_phi baseline records for family {family!r}")
        base_median, base_max = float(np.median(base)), float(np.max(base))
        l1_median, l1_max = float(np.median(l1s)), float(np.max(l1s))
        out[(family, backbone, n_train)] = {
            "ratio_median": l1_median / base_median,
            "ratio_max": l1_max / base_max,
            "l1_median": l1_median,
            "l1_max": l1_max,
            "n": len(l1s),
        }
    return out


def _geomean(values: Sequence[float]) -> float:
    return float(np.exp(np.mean(np.log(np.asarray(values, dtype=float)))))


def overall_scores(ratios: Dict[RatioKey, dict], n_train: int = 1000
                    ) -> List[Tuple[str, float, float, List[str]]]:
    """Rank backbones at a given ``n_train`` by the geometric mean of their
    per-family ``ratio_median`` (S, ascending = better). Also reports the
    worst (max) ``ratio_median`` across families and the sorted list of
    families where ``ratio_median > FAILURE_RATIO``.
    """
    by_backbone: Dict[str, Dict[str, dict]] = defaultdict(dict)
    for (family, backbone, n), v in ratios.items():
        if n == n_train:
            by_backbone[backbone][family] = v

    out = []
    for backbone in sorted(by_backbone):
        entries = by_backbone[backbone]
        medians = [v["ratio_median"] for v in entries.values()]
        S = _geomean(medians)
        max_ratio = float(max(medians))
        failure_families = sorted(f for f, v in entries.items()
                                  if v["ratio_median"] > FAILURE_RATIO)
        out.append((backbone, S, max_ratio, failure_families))
    out.sort(key=lambda row: row[1])
    return out


def report_table(ratios: Dict[RatioKey, dict], *, n_train: int = 1000,
                  slope_n_lo: int = 250, slope_n_hi: int = 1000) -> str:
    """Markdown report: a per-family table of backbones at ``n_train``, the
    ranked list of overall scores, the robustness winner (lowest worst-case
    ratio_median across families) and a learning-curve-slope table of
    ``log(S(slope_n_lo) / S(slope_n_hi))`` per backbone present at both.
    """
    families = sorted({family for (family, _, _) in ratios})
    backbones = sorted({backbone for (_, backbone, n) in ratios if n == n_train})

    lines = ["| family | " + " | ".join(backbones) + " |",
             "| --- | " + " | ".join(["---"] * len(backbones)) + " |"]
    for family in families:
        cells = []
        for backbone in backbones:
            v = ratios.get((family, backbone, n_train))
            cells.append(f"{v['ratio_median']:.3g} ({v['ratio_max']:.3g})" if v else "-")
        lines.append(f"| {family} | " + " | ".join(cells) + " |")

    ranked = overall_scores(ratios, n_train=n_train)
    lines += ["", "## Ranked"]
    for backbone, S, max_ratio, failures in ranked:
        fail_str = ", ".join(failures) if failures else "none"
        lines.append(f"- {backbone}: S={S:.3g}, max_ratio={max_ratio:.3g}, failures={fail_str}")

    if ranked:
        winner, _, winner_max, _ = min(ranked, key=lambda row: row[2])
        lines += ["", f"**Robustness winner:** {winner} (max ratio_median = {winner_max:.3g})"]
    else:
        lines += ["", "**Robustness winner:** n/a (no backbones)"]

    scores_hi = {b: S for b, S, _, _ in overall_scores(ratios, n_train=slope_n_hi)}
    scores_lo = {b: S for b, S, _, _ in overall_scores(ratios, n_train=slope_n_lo)}
    lines += ["", "## Learning-curve slope", "| backbone | slope |", "| --- | --- |"]
    for backbone in sorted(set(scores_lo) & set(scores_hi)):
        slope = float(np.log(scores_lo[backbone] / scores_hi[backbone]))
        lines.append(f"| {backbone} | {slope:.3g} |")

    return "\n".join(lines)
