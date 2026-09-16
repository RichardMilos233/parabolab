"""D02: one net for the Merton family (t, x, theta) -> u, policies by autograd.

    python examples/parametric_merton.py --rungs C0 C1 C2 C3 C4 C5 --steps 20000 \
        --device cuda --jobs 16

Rungs: C0 per-instance R5A baseline; C1 concat conditioning; C2 FiLM;
C3 best of C1/C2 (--c3-mode) plus derivative labels (weights 1, 1), pooled-std
weighting; C4 same as C3 but with per-row inverse-variance weighting of the
derivative terms (weights 1, 1, 1); C5 like C4 with u_x labels only
(weights 1, 1, 0) -- both C4/C5 reuse the C3 derivative corpus.
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import time
from pathlib import Path

import numpy as np

from parabolab.deep import condtrain, corpus
from parabolab.deep.condnet import ConditionedNet

FIELDS = ["rung", "instance_seed", "l1_u", "policy_err_interior",
          "policy_err_full", "seconds"]


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--rungs", nargs="*", default=["C0", "C1", "C2", "C3", "C4", "C5"])
    p.add_argument("--c3-mode", default="concat", choices=["concat", "film"])
    p.add_argument("--n-train", type=int, default=500)
    p.add_argument("--n-test", type=int, default=50)
    p.add_argument("--n-states", type=int, default=500)
    p.add_argument("--m-samples", type=int, default=1000)
    p.add_argument("--steps", type=int, default=20_000)
    p.add_argument("--batch-states", type=int, default=4096)
    p.add_argument("--device", default="cpu")
    p.add_argument("--jobs", type=int, default=8)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--corpus-root", default="examples/nn_corpus")
    p.add_argument("--out", default="examples/parametric_merton.csv")
    p.add_argument("--tiny", action="store_true")
    a = p.parse_args()
    if a.tiny:
        a.n_train, a.n_test, a.n_states, a.m_samples, a.steps, a.batch_states = 3, 2, 12, 4, 5, 16
    return a


def write_rows(path, rows):
    path = Path(path); new = not path.exists()
    with path.open("a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if new: w.writeheader()
        w.writerows(rows)


def main(a):
    fam = corpus.FAMILIES["merton"]
    root = Path(a.corpus_root)
    kw = dict(n_states=a.n_states, m_samples=a.m_samples, n_draws=1)
    train_specs = corpus.sample_instances("merton", a.n_train, a.seed, **kw)
    test_specs = corpus.sample_instances("merton", a.n_test, a.seed + 1, **kw)
    mf = min(50, a.n_states)
    train = corpus.load_or_generate_corpus(train_specs, root, n_jobs=a.jobs, verbose=True, min_finite=mf)
    test = corpus.load_or_generate_corpus(test_specs, root, n_jobs=a.jobs, verbose=True, min_finite=mf)
    p_mean = np.array([0.5 * (lo + hi) for lo, hi in fam.ranges])
    p_std = np.array([0.5 * (hi - lo) for lo, hi in fam.ranges])
    mlp_epochs = 5 if a.tiny else 3000
    rows = []

    def record(rung, metrics, seconds):
        for inst, m in zip(test, metrics):
            rows.append({"rung": rung, "instance_seed": inst.spec.seed, **m,
                         "seconds": seconds})

    if "C0" in a.rungs:
        ms = []
        t0 = time.perf_counter()
        for inst in test:
            ms.append(condtrain.per_instance_baseline(inst, device=a.device, seed=a.seed, epochs=mlp_epochs))
        record("C0", ms, (time.perf_counter() - t0) / len(test))

    def run_cond(rung, mode, instances, weights, deriv_weighting="pooled"):
        import torch
        torch.manual_seed(a.seed)
        net = ConditionedNet(d=fam.d, n_params=len(fam.ranges), mode=mode,
                             param_mean=p_mean, param_std=p_std)
        print(f"{rung}: {mode}, weights {weights}, deriv_weighting {deriv_weighting}, "
              f"{net.n_params_total} params", flush=True)
        res = condtrain.train_conditioned(net, instances, steps=a.steps,
                                          batch_states=a.batch_states, loss_weights=weights,
                                          device=a.device, seed=a.seed, verbose=True,
                                          deriv_weighting=deriv_weighting)
        record(rung, condtrain.evaluate_conditioned(net, test, device=a.device),
               res.seconds / len(test))

    if "C1" in a.rungs: run_cond("C1", "concat", train, (1.0, 0.0, 0.0))
    if "C2" in a.rungs: run_cond("C2", "film", train, (1.0, 0.0, 0.0))
    if "C3" in a.rungs or "C4" in a.rungs or "C5" in a.rungs:
        dspecs = [dataclasses.replace(s, deriv_codes=("Dx1", "Dx2")) for s in train_specs]
        dtrain = corpus.load_or_generate_corpus(dspecs, root / "deriv", n_jobs=a.jobs, verbose=True, min_finite=mf)
    if "C3" in a.rungs: run_cond("C3", a.c3_mode, dtrain, (1.0, 1.0, 1.0))
    if "C4" in a.rungs: run_cond("C4", a.c3_mode, dtrain, (1.0, 1.0, 1.0), deriv_weighting="inverse_variance")
    if "C5" in a.rungs: run_cond("C5", a.c3_mode, dtrain, (1.0, 1.0, 0.0), deriv_weighting="inverse_variance")

    write_rows(a.out, rows)
    print("\n| rung | n | u-L1 median | u-L1 max | policy err interior (median) | policy err full | s/instance |")
    print("|---|---|---|---|---|---|---|")
    for rung in ("C0", "C1", "C2", "C3", "C4", "C5"):
        rr = [r for r in rows if r["rung"] == rung]
        if not rr:
            continue
        l1 = np.array([r["l1_u"] for r in rr]); pi = np.array([r["policy_err_interior"] for r in rr])
        pf = np.array([r["policy_err_full"] for r in rr]); s = np.mean([r["seconds"] for r in rr])
        print(f"| {rung} | {len(rr)} | {np.median(l1):.2e} | {l1.max():.2e} | "
              f"{100*np.median(pi):.2f} % | {100*np.median(pf):.2f} % | {s:.1f} |")


if __name__ == "__main__":
    main(parse_args())
