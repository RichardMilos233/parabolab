"""D03: learn phi -> u(0, .) from coding-tree labels; compare three backbones.

    python examples/phi_operator.py --family heat_phi --n-train 1000 --n-test 50 \
        --curve 250 500 1000 --steps 20000 --device cuda --jobs 16
    python examples/phi_operator.py --family ac_phi ...

Rows: one per (backbone, n_train, held-out instance); the per_phi baseline
(R5A net on that phi's own labels) once per instance with n_train = 0.
"""

from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

import numpy as np

from parabolab.deep import corpus, opnet, optrain

FIELDS = ["family", "backbone", "n_train", "instance_seed", "l1", "seconds"]
BACKBONES = ("deeponet", "fno", "attn")


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--family", default="heat_phi", choices=["heat_phi", "ac_phi"])
    p.add_argument("--n-train", type=int, default=1000)
    p.add_argument("--n-test", type=int, default=50)
    p.add_argument("--curve", nargs="*", type=int, default=[250, 500, 1000])
    p.add_argument("--n-states", type=int, default=500)
    p.add_argument("--m-samples", type=int, default=1000)
    p.add_argument("--steps", type=int, default=20_000)
    p.add_argument("--backbones", nargs="*", default=list(BACKBONES))
    p.add_argument("--device", default="cpu")
    p.add_argument("--jobs", type=int, default=8)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--corpus-root", default="examples/nn_corpus")
    p.add_argument("--out", default="examples/phi_operator.csv")
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


def main(a):
    root = Path(a.corpus_root)
    kw = dict(n_states=a.n_states, m_samples=a.m_samples, n_draws=1)
    mf = min(50, a.n_states)
    train_specs = corpus.sample_instances(a.family, a.n_train, a.seed, **kw)
    test_specs = corpus.sample_instances(a.family, a.n_test, a.seed + 1, **kw)
    train = corpus.load_or_generate_corpus(train_specs, root, n_jobs=a.jobs, verbose=True, min_finite=mf)
    test = corpus.load_or_generate_corpus(test_specs, root, n_jobs=a.jobs, verbose=True, min_finite=mf)
    grid = test[0].grid
    tiny_kw = {"attn": {"d_model": 16, "n_layers": 1}, "fno": {"width": 8, "modes": 4, "n_layers": 2},
               "deeponet": {"p": 8, "width": 16}} if a.tiny else {}
    rows = []

    t0 = time.perf_counter()
    for inst in test:
        l1 = optrain.per_phi_baseline(inst, device=a.device, seed=a.seed, epochs=5 if a.tiny else 3000)
        rows.append({"family": a.family, "backbone": "per_phi", "n_train": 0,
                     "instance_seed": inst.spec.seed, "l1": l1,
                     "seconds": (time.perf_counter() - t0) / len(test)})

    import torch
    for n in a.curve:
        subset = train[:n]
        for name in a.backbones:
            torch.manual_seed(a.seed)
            net = opnet.make_operator(name, grid, **tiny_kw.get(name, {}))
            print(f"{a.family} {name} n_train={len(subset)}: {net.n_params_total} params", flush=True)
            res = optrain.train_operator(net, subset, steps=a.steps, device=a.device, seed=a.seed, verbose=True)
            l1 = optrain.evaluate_operator(net, test, device=a.device)
            rows += [{"family": a.family, "backbone": name, "n_train": len(subset),
                      "instance_seed": inst.spec.seed, "l1": v, "seconds": res.seconds / len(test)}
                     for inst, v in zip(test, l1)]
    write_rows(a.out, rows)

    print("\n| backbone | n_train | L1 median | L1 max |")
    print("|---|---|---|---|")
    keys = sorted({(r["backbone"], r["n_train"]) for r in rows}, key=lambda k: (k[0] != "per_phi", k))
    for name, n in keys:
        v = np.array([r["l1"] for r in rows if r["backbone"] == name and r["n_train"] == n])
        print(f"| {name} | {n} | {np.median(v):.2e} | {v.max():.2e} |")


if __name__ == "__main__":
    main(parse_args())
