"""Network ablation ladder (docs/superpowers/specs/2026-09-15-nn-architecture-
ablation-design.md): train single-knob variants of the JCP2024 deep
branching net on frozen Monte Carlo data and append one CSV row per run.

    python examples/nn_ablation.py --rungs R0 --benchmarks ac1 exp1 merton
    python examples/nn_ablation.py --rungs R1 --parent R0 ...
    python examples/nn_ablation.py --report

Rung names and their single-knob deltas are in
parabolab.deep.ablation.RUNG_DELTAS; --parent picks the kept rung a new
rung builds on (the researcher's decision, recorded in the spec).
"""

from __future__ import annotations

import argparse
import dataclasses
import json

from parabolab.deep import ablation, datasets


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--rungs", nargs="*", default=[])
    p.add_argument("--parent", default=None,
                   help="rung name the listed rungs are derived from "
                        "(config read back from --out; R0 needs none)")
    p.add_argument("--benchmarks", nargs="*", default=["ac1", "exp1", "merton"])
    p.add_argument("--data-seeds", nargs="*", type=int, default=[0, 1, 2])
    p.add_argument("--train-seeds", type=int, default=5)
    p.add_argument("--data-root", default="examples/nn_ablation_data")
    p.add_argument("--out", default="examples/nn_ablation_results.csv")
    p.add_argument("--jobs", type=int, default=8)
    p.add_argument("--device", default="cpu")
    p.add_argument("--epochs", type=int, default=None,
                   help="override the rung's epochs (smoke tests only)")
    p.add_argument("--ensemble", action="store_true",
                   help="also record the median-of-seeds ensemble (R9)")
    p.add_argument("--tiny", action="store_true",
                   help="8 states x 4 samples per benchmark (tests)")
    p.add_argument("--report", action="store_true")
    return p.parse_args()


def resolve_parent(name, records):
    """Rebuild a RungConfig from the config_json stored with its runs."""
    if name == "R0":
        return ablation.BASELINE
    for r in records:
        if r.rung == name:
            cfg = json.loads(r.config_json)
            return ablation.RungConfig(
                cfg["name"], cfg["parent"],
                ablation.NetConfig(**cfg["net"]),
                ablation.TrainConfig(**cfg["train"]))
    raise SystemExit(f"parent rung {name!r} has no rows in the results file")


def main(args):
    records = ablation.read_records(args.out)
    if args.report:
        print(ablation.format_table(ablation.summarise(records)))
        return
    if not args.rungs:
        raise SystemExit("nothing to do: pass --rungs or --report")

    rungs = []
    for name in args.rungs:
        if name == "R0":
            rungs.append(ablation.BASELINE)
        else:
            if name not in ablation.RUNG_DELTAS:
                raise SystemExit(f"unknown rung {name!r}; known: {', '.join(sorted(ablation.RUNG_DELTAS))}")
            if args.parent is None:
                raise SystemExit(f"--parent is required to derive {name}")
            rungs.append(ablation.derive_rung(
                name, resolve_parent(args.parent, records)))
    if args.epochs is not None:
        rungs = [dataclasses.replace(
            r, train=dataclasses.replace(r.train, epochs=args.epochs))
            for r in rungs]

    train_seeds = list(range(args.train_seeds))
    for key in args.benchmarks:
        spec0 = datasets.BENCHMARKS[key]
        if args.tiny:
            spec0 = dataclasses.replace(spec0, n_states=8, m_samples=4)
        pde = spec0.factory()()
        for ds in args.data_seeds:
            spec = dataclasses.replace(spec0, seed=ds)
            data = datasets.load_or_generate(spec, args.data_root,
                                             n_jobs=args.jobs, verbose=True)
            for rung in rungs:
                done = {r.key() for r in ablation.read_records(args.out)}
                todo = [s for s in train_seeds
                        if (rung.name, key, ds, s) not in done]
                if not todo:
                    print(f"skip {rung.name} {key} d{ds}: already in {args.out}")
                    if args.ensemble:
                        print(f"ensemble not written for {rung.name} {key} d{ds}: nets are not in memory on a resumed rung", flush=True)
                    continue
                recs, nets = ablation.run_rung(
                    rung, benchmark=key, data_seed=ds, data=data, pde=pde,
                    x_lo=spec.x_lo, x_hi=spec.x_hi, train_seeds=todo,
                    device=args.device, verbose=True)
                if args.ensemble and len(nets) == len(train_seeds):
                    recs.append(ablation.ensemble_record(
                        rung, nets, benchmark=key, data_seed=ds, data=data,
                        pde=pde, x_lo=spec.x_lo, x_hi=spec.x_hi,
                        device=args.device))
                elif args.ensemble:
                    print(f"ensemble not written for {rung.name} {key} d{ds}: only {len(nets)}/{len(train_seeds)} seeds trained in this invocation", flush=True)
                n = ablation.append_records(args.out, recs)
                print(f"wrote {n} rows to {args.out}", flush=True)

    print(ablation.format_table(ablation.summarise(
        ablation.read_records(args.out))))


if __name__ == "__main__":
    main(parse_args())
