"""Universal-backbone benchmark (spec 2026-09-16-backbone-benchmark-design):
four backbones over the PDE families that pass the calibration pre-check.

    python examples/backbone_benchmark.py --curve 250 1000 --steps 20000 \
        --device cuda --jobs 16
    python examples/backbone_benchmark.py --families heat_phi ac_phi
    python examples/backbone_benchmark.py --precheck --families heat_phi merton
    python examples/backbone_benchmark.py --report

Rows: one per (backbone, n_train, held-out instance) per family; the
per_phi baseline (R5A net on that phi's own labels) once per instance with
n_train = 0. Rows already present in --out are skipped, so a run can be
resumed (baseline: skipped per held-out instance once its row exists;
operator backbones: skipped for a whole (family, backbone, n_train) group
once any row for it exists) -- see examples/nn_ablation.py for the same
pattern. --precheck runs the sampler calibration check per family and
exits; --report prints the benchmark.report_table ranking from --out and
exits.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

from parabolab.deep import benchmark, corpus, opnet, optrain

FIELDS = ["family", "backbone", "n_train", "instance_seed", "l1", "seconds"]
FAMILIES = ("heat_phi", "ac_phi", "kpp_phi", "expgrad_phi", "tan_phi", "cosine_phi", "log_phi", "merton")
BACKBONES = ("deeponet", "fno", "attn", "coeffmlp")


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--families", nargs="*", default=list(FAMILIES))
    p.add_argument("--backbones", nargs="*", default=list(BACKBONES))
    p.add_argument("--n-train", type=int, default=1000)
    p.add_argument("--n-test", type=int, default=50)
    p.add_argument("--curve", nargs="*", type=int, default=[250, 1000])
    p.add_argument("--n-states", type=int, default=500)
    p.add_argument("--m-samples", type=int, default=1000)
    p.add_argument("--steps", type=int, default=20_000)
    p.add_argument("--device", default="cpu")
    p.add_argument("--jobs", type=int, default=8)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--corpus-root", default="examples/nn_corpus")
    p.add_argument("--out", default="examples/backbone_benchmark.csv")
    p.add_argument("--precheck", action="store_true")
    p.add_argument("--precheck-out", default="examples/backbone_benchmark_precheck.json")
    p.add_argument("--report", action="store_true")
    p.add_argument("--figure", default=None, help="with --report: write the per-family learning-curve figure here")
    p.add_argument("--tiny", action="store_true")
    a = p.parse_args()
    if a.tiny:
        a.n_train, a.n_test, a.curve, a.n_states, a.m_samples, a.steps = 3, 2, [2, 3], 12, 4, 5
    return a


def write_rows(path, rows):
    path = Path(path); new = not path.exists()
    with path.open("a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if new: w.writeheader()
        w.writerows(rows)


def read_existing(path):
    path = Path(path)
    if not path.exists():
        return []
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh))


def run_precheck(a):
    kw = dict(n=2, n_states=10, m_lo=20, m_hi=200) if a.tiny else {}
    results = {}
    for family in a.families:
        res = optrain.calibration_precheck(family, n_jobs=a.jobs, **kw)
        results[family] = res
        print(f"{family}: frac_within_4se={res['frac_within_4se']:.3f} "
              f"stderr_ratio={res['stderr_ratio']:.3f} passed={res['passed']}", flush=True)
    out = Path(a.precheck_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2))


def run_report(a):
    records = [r for r in read_existing(a.out)
               if r["family"] in a.families
               and (r["backbone"] == "per_phi" or r["backbone"] in a.backbones)]
    for r in records:
        r["n_train"] = int(r["n_train"])
        r["l1"] = float(r["l1"])
    ratios = benchmark.family_ratios(records)
    print(benchmark.report_table(ratios))
    if a.figure:
        plot_curves(ratios, a.figure)


def plot_curves(ratios, path):
    """One panel per family: median L1 ratio to the per-instance baseline vs
    n_train, one line per backbone (log-log; the dashed line is the baseline)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    families = sorted({f for (f, _, _) in ratios})
    backbones = sorted({b for (_, b, _) in ratios})
    ncol = min(3, len(families))
    nrow = (len(families) + ncol - 1) // ncol
    fig, axes = plt.subplots(nrow, ncol, figsize=(4 * ncol, 3 * nrow), squeeze=False)
    for ax, family in zip(axes.flat, families):
        for b in backbones:
            pts = sorted((n, v["ratio_median"]) for (f, bb, n), v in ratios.items() if f == family and bb == b)
            if pts:
                ax.plot([p[0] for p in pts], [p[1] for p in pts], "o-", label=b)
        ax.axhline(1.0, color="k", ls="--", lw=0.8)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_title(family); ax.set_xlabel("n_train"); ax.set_ylabel("median L1 / per-instance")
    for ax in list(axes.flat)[len(families):]:
        ax.axis("off")
    axes.flat[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    print(f"wrote {path}", flush=True)


def main(a):
    if a.report:
        run_report(a)
        return
    if a.precheck:
        run_precheck(a)
        return

    root = Path(a.corpus_root)
    kw = dict(n_states=a.n_states, m_samples=a.m_samples, n_draws=1)
    mf = min(50, a.n_states)
    tiny_kw = {"attn": {"d_model": 16, "n_layers": 1}, "fno": {"width": 8, "modes": 4, "n_layers": 2},
               "deeponet": {"p": 8, "width": 16}, "coeffmlp": {"hidden_layers": 2, "neurons": 8}} if a.tiny else {}

    import torch

    for family in a.families:
        train_specs = corpus.sample_instances(family, a.n_train, a.seed, **kw)
        test_specs = corpus.sample_instances(family, a.n_test, a.seed + 1, **kw)
        train = corpus.load_or_generate_corpus(train_specs, root, n_jobs=a.jobs, verbose=True, min_finite=mf)
        test = corpus.load_or_generate_corpus(test_specs, root, n_jobs=a.jobs, verbose=True, min_finite=mf)
        if not test:
            print(f"skip {family}: no finite test instances", flush=True)
            continue
        grid = test[0].grid
        n_cond = len(test[0].spec.params)

        existing = read_existing(a.out)
        done_baseline = {(r["family"], int(r["instance_seed"])) for r in existing if r["backbone"] == "per_phi"}
        done_ops = {(r["family"], r["backbone"], int(r["n_train"])) for r in existing if r["backbone"] != "per_phi"}

        rows = []
        t0 = time.perf_counter()
        for inst in test:
            if (family, inst.spec.seed) in done_baseline:
                continue
            l1 = optrain.per_phi_baseline(inst, device=a.device, seed=a.seed, epochs=5 if a.tiny else 3000)
            rows.append({"family": family, "backbone": "per_phi", "n_train": 0,
                         "instance_seed": inst.spec.seed, "l1": l1,
                         "seconds": (time.perf_counter() - t0) / len(test)})
        if rows:
            write_rows(a.out, rows)
            done_baseline |= {(r["family"], r["instance_seed"]) for r in rows}

        for n in a.curve:
            subset = train[:n]
            if len(subset) < n:
                print(f"warning: {family} has only {len(subset)} usable training instances for n_train={n}", flush=True)
            for name in a.backbones:
                if (family, name, n) in done_ops:
                    print(f"skip {family} {name} n_train={n}: already in {a.out}", flush=True)
                    continue
                torch.manual_seed(a.seed)
                net = opnet.make_operator(name, grid, n_cond=n_cond, **tiny_kw.get(name.replace("_nocond", ""), {}))
                print(f"{family} {name} n_train={len(subset)}: {net.n_params_total} params", flush=True)
                res = optrain.train_operator(net, subset, steps=a.steps, device=a.device, seed=a.seed, verbose=True)
                l1 = optrain.evaluate_operator(net, test, device=a.device)
                new_rows = [{"family": family, "backbone": name, "n_train": n,
                             "instance_seed": inst.spec.seed, "l1": v, "seconds": res.seconds / len(test)}
                            for inst, v in zip(test, l1)]
                write_rows(a.out, new_rows)
                done_ops.add((family, name, n))


if __name__ == "__main__":
    main(parse_args())
