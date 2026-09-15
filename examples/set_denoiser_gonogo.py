"""D04 go/no-go: does a set-to-field denoiser trained across instances beat
a per-instance MLP on held-out instances?

    python examples/set_denoiser_gonogo.py --family ac1 --n-train 500 --n-test 50 \
        --n-states 500 --m-samples 1000 --steps 20000 --device cuda --jobs 16

Rule (fixed in the spec before running): d04_n2n median held-out L1 must be
below mlp_M's median.  Methods: d04_n2n (Noise2Noise targets), d04_exact
(exact targets, upper bound), mlp_M / mlp_10M (per-instance R5A net on the
instance's labels at M and at 10 M samples), kernel (Nadaraya-Watson).
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import time
from pathlib import Path

import numpy as np

from parabolab.deep import corpus, settrain
from parabolab.deep.setnet import SetDenoiser


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--family", default="ac1", choices=sorted(corpus.FAMILIES))
    p.add_argument("--n-train", type=int, default=500)
    p.add_argument("--n-test", type=int, default=50)
    p.add_argument("--n-states", type=int, default=500)
    p.add_argument("--m-samples", type=int, default=1000)
    p.add_argument("--steps", type=int, default=20_000)
    p.add_argument("--d-model", type=int, default=128)
    p.add_argument("--n-layers", type=int, default=4)
    p.add_argument("--n-context", type=int, default=500)
    p.add_argument("--device", default="cpu")
    p.add_argument("--jobs", type=int, default=8)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--corpus-root", default="examples/nn_corpus")
    p.add_argument("--out", default="examples/set_denoiser_gonogo.csv")
    p.add_argument("--tiny", action="store_true",
                   help="4/2 instances, 8 states, 4 trees, 5 steps (tests)")
    args = p.parse_args()
    if args.tiny:
        args.n_train, args.n_test, args.n_states, args.m_samples = 4, 2, 8, 4
        args.steps, args.d_model, args.n_layers, args.n_context = 5, 16, 1, 8
    return args


def write_rows(path, rows):
    path = Path(path)
    new = not path.exists()
    with path.open("a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["method", "family", "instance_seed",
                                           "l1", "seconds"])
        if new:
            w.writeheader()
        w.writerows(rows)


def main(args):
    fam = corpus.FAMILIES[args.family]
    train_specs = corpus.sample_instances(args.family, args.n_train, args.seed,
                                          n_states=args.n_states,
                                          m_samples=args.m_samples)
    test_specs = corpus.sample_instances(args.family, args.n_test, args.seed + 1,
                                         n_states=args.n_states,
                                         m_samples=args.m_samples)
    test10_specs = [dataclasses.replace(s, m_samples=10 * s.m_samples, n_draws=1)
                    for s in test_specs]
    root = Path(args.corpus_root)
    # load_or_generate_corpus's default min_finite=50 assumes the full-scale
    # n_states=500; --tiny draws only n_states=8 states, so cap the floor at
    # n_states or every tiny instance gets filtered out before training ever
    # sees one (not present in the brief's snippet -- see task-5 report).
    min_finite = min(50, args.n_states)
    train = corpus.load_or_generate_corpus(train_specs, root, n_jobs=args.jobs,
                                           verbose=True, min_finite=min_finite)
    test = corpus.load_or_generate_corpus(test_specs, root, n_jobs=args.jobs,
                                          verbose=True, min_finite=min_finite)
    test10 = corpus.load_or_generate_corpus(test10_specs, root / "x10", n_jobs=args.jobs,
                                            verbose=True, min_finite=min_finite)
    print(f"corpus: {len(train)} train, {len(test)} test, {len(test10)} test@10M")

    p_mean = np.array([0.5 * (lo + hi) for lo, hi in fam.ranges])
    p_std = np.array([0.5 * (hi - lo) for lo, hi in fam.ranges])
    rows = []
    for target in ("n2n", "exact"):
        import torch
        torch.manual_seed(args.seed)
        net = SetDenoiser(d=fam.d, n_params=len(fam.ranges), d_model=args.d_model,
                          n_layers=args.n_layers, param_mean=p_mean, param_std=p_std)
        print(f"training d04_{target}: {net.n_params_total} parameters", flush=True)
        res = settrain.train_set_denoiser(
            net, train, steps=args.steps, n_context=args.n_context,
            target=target, device=args.device, seed=args.seed, verbose=True)
        l1 = settrain.evaluate_set_denoiser(net, test, n_context=args.n_context,
                                            device=args.device)
        rows += [{"method": f"d04_{target}", "family": args.family,
                  "instance_seed": inst.spec.seed, "l1": v,
                  "seconds": res.seconds / len(test)}
                 for inst, v in zip(test, l1)]

    mlp_epochs = 5 if args.tiny else 3000
    for name, insts in (("mlp_M", test), ("mlp_10M", test10)):
        for inst in insts:
            t0 = time.perf_counter()
            v = settrain.per_instance_mlp_l1(inst, device=args.device, seed=args.seed,
                                             epochs=mlp_epochs)
            rows.append({"method": name, "family": args.family,
                         "instance_seed": inst.spec.seed, "l1": v,
                         "seconds": time.perf_counter() - t0})
    for inst in test:
        t0 = time.perf_counter()
        rows.append({"method": "kernel", "family": args.family,
                     "instance_seed": inst.spec.seed,
                     "l1": settrain.kernel_smoother_l1(inst),
                     "seconds": time.perf_counter() - t0})
    write_rows(args.out, rows)

    print("\n| method | n | L1 median | L1 max | s/instance |")
    print("|---|---|---|---|---|")
    summary = {}
    for m in ("d04_n2n", "d04_exact", "mlp_M", "mlp_10M", "kernel"):
        v = np.array([r["l1"] for r in rows if r["method"] == m])
        s = np.array([r["seconds"] for r in rows if r["method"] == m])
        summary[m] = float(np.median(v))
        print(f"| {m} | {len(v)} | {np.median(v):.2e} | {v.max():.2e} | {s.mean():.1f} |")
    verdict = "PASS" if summary["d04_n2n"] < summary["mlp_M"] else "FAIL"
    print(f"\ngo/no-go: d04_n2n {summary['d04_n2n']:.2e} vs mlp_M "
          f"{summary['mlp_M']:.2e} -> {verdict}")


if __name__ == "__main__":
    main(parse_args())
