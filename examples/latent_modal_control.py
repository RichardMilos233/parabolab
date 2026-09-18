"""Exact-heat latent modal-control experiment.

Smoke test::

    python examples/latent_modal_control.py --tiny --device cpu --out-dir /tmp/modal-smoke

Formal run::

    python examples/latent_modal_control.py --device cuda \
        --out-dir examples/latent_modal_control_run
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
import torch

from parabolab.deep import modal_control, modal_data, opnet


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--backbones", nargs="+", default=["deeponet", "attn"],
                   choices=["deeponet", "attn"])
    p.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    p.add_argument("--data-seed", type=int, default=1729)
    p.add_argument("--n-train", type=int, default=1024)
    p.add_argument("--n-valid", type=int, default=128)
    p.add_argument("--n-calib", type=int, default=256)
    p.add_argument("--n-test", type=int, default=256)
    p.add_argument("--K", type=int, default=4)
    p.add_argument("--n-sensors", type=int, default=128)
    p.add_argument("--n-query", type=int, default=256)
    p.add_argument("--steps", type=int, default=20_000)
    p.add_argument("--batch-size", type=int, default=32)
    p.add_argument("--queries-per-step", type=int, default=64)
    p.add_argument("--pca-dim", type=int, default=32)
    p.add_argument("--ridge", type=float, default=1e-4)
    p.add_argument("--calibration-delta", type=float, default=0.05)
    p.add_argument("--alphas", nargs="+", type=float, default=[0.0, 0.5, 1.5, 2.0])
    p.add_argument("--device", default="cpu")
    p.add_argument("--out-dir", default="examples/latent_modal_control_run")
    p.add_argument("--skip-controls", action="store_true",
                   help="skip random-direction and untrained-network controls")
    p.add_argument("--tiny", action="store_true")
    a = p.parse_args()
    if a.tiny:
        a.seeds = [0]
        a.n_train, a.n_valid, a.n_calib, a.n_test = 12, 4, 8, 6
        a.K, a.n_sensors, a.n_query = 2, 16, 32
        a.steps, a.batch_size, a.queries_per_step = 4, 4, 8
        a.pca_dim = 4
        a.alphas = [0.0, 2.0]
    return a


def make_batches(a):
    common = dict(K=a.K, n_sensors=a.n_sensors, n_query=a.n_query)
    return {
        "train": modal_data.sample_heat_batch(a.n_train, a.data_seed, **common),
        "valid": modal_data.sample_heat_batch(a.n_valid, a.data_seed + 1, **common),
        "calib": modal_data.sample_heat_batch(a.n_calib, a.data_seed + 2, **common),
        "test": modal_data.sample_heat_batch(a.n_test, a.data_seed + 3, **common),
        "edit": modal_data.sample_heat_batch(
            a.n_test, a.data_seed + 4, coefficient_scale=0.125, **common),
    }


def model_kwargs(name: str, tiny: bool):
    if name == "deeponet":
        return {"p": 8, "width": 16} if tiny else {"p": 64, "width": 128}
    return {"d_model": 16, "n_heads": 2, "n_layers": 1} if tiny else {
        "d_model": 128, "n_heads": 4, "n_layers": 4}


def write_metrics(path: Path, rows):
    fields = list(rows[0])
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def save_checkpoint(path, net, *, name, kw, sensor_grid, config, result=None):
    torch.save({
        "backbone": name,
        "model_kwargs": kw,
        "sensor_grid": sensor_grid.tolist(),
        "state_dict": net.cpu().state_dict(),
        "train_loss": [] if result is None else result.train_loss,
        "validation_loss": [] if result is None else result.validation_loss,
        "config": config,
    }, path)


def main(a):
    if a.device.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but torch.cuda.is_available() is false")
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    batches = make_batches(a)
    config = vars(a).copy()
    config["split_hashes"] = {name: batch.identity for name, batch in batches.items()}
    (out / "config.json").write_text(json.dumps(config, indent=2, sort_keys=True))
    all_rows = []

    for name in a.backbones:
        kw = model_kwargs(name, a.tiny)
        for seed in a.seeds:
            torch.manual_seed(seed)
            net = opnet.make_operator(name, batches["train"].sensor_grid, n_cond=0, **kw)
            print(f"train {name} seed={seed}: {net.n_params_total} parameters", flush=True)
            result = modal_control.train_exact_operator(
                net, batches["train"], batches["valid"], steps=a.steps,
                batch_size=a.batch_size, n_query=a.queries_per_step,
                device=a.device, seed=seed, check_every=max(1, min(100, a.steps)))
            checkpoint = out / f"{name}-seed{seed}.pt"
            save_checkpoint(
                checkpoint, net, name=name, kw=kw,
                sensor_grid=batches["train"].sensor_grid,
                config=config, result=result)
            net.to(a.device)
            controller = modal_control.fit_modal_controller(
                net, batches["calib"], pca_dim=a.pca_dim, ridge=a.ridge,
                calibration_delta=a.calibration_delta, device=a.device)
            controller.save(out / f"{name}-seed{seed}-controller.npz")
            rows = modal_control.evaluate_modal_controller(
                net, controller, batches["edit"], alphas=a.alphas, device=a.device)
            for row in rows:
                row.update(backbone=name, seed=seed, variant="trained")
            all_rows.extend(rows)

            if not a.skip_controls:
                random_controller = modal_control.random_direction_controller(
                    net, controller, batches["calib"], seed=seed + 10_000,
                    device=a.device)
                random_controller.save(out / f"{name}-seed{seed}-random-controller.npz")
                random_rows = modal_control.evaluate_modal_controller(
                    net, random_controller, batches["edit"],
                    alphas=a.alphas, device=a.device)
                for row in random_rows:
                    row.update(backbone=name, seed=seed, variant="random_direction")
                all_rows.extend(random_rows)

                torch.manual_seed(seed + 100_000)
                untrained = opnet.make_operator(
                    name, batches["train"].sensor_grid, n_cond=0, **kw)
                modal_control.fit_exact_scalers(untrained, batches["train"])
                save_checkpoint(
                    out / f"{name}-seed{seed}-untrained.pt", untrained,
                    name=name, kw=kw, sensor_grid=batches["train"].sensor_grid,
                    config=config)
                untrained.to(a.device)
                untrained_controller = modal_control.fit_modal_controller(
                    untrained, batches["calib"], pca_dim=a.pca_dim,
                    ridge=a.ridge, calibration_delta=a.calibration_delta,
                    device=a.device)
                untrained_controller.save(
                    out / f"{name}-seed{seed}-untrained-controller.npz")
                untrained_rows = modal_control.evaluate_modal_controller(
                    untrained, untrained_controller, batches["edit"],
                    alphas=a.alphas, device=a.device)
                for row in untrained_rows:
                    row.update(backbone=name, seed=seed, variant="untrained")
                all_rows.extend(untrained_rows)
            median_control = float(np.median([r["control_rel_rms"] for r in rows]))
            print(f"finished {name} seed={seed}: median control error={median_control:.3g}", flush=True)

    write_metrics(out / "metrics.csv", all_rows)
    summary = {
        "runs": len(a.backbones) * len(a.seeds),
        "rows": len(all_rows),
        "note": "Smoke runs verify execution only; metrics are not scientific results." if a.tiny else
                "Evaluate against the pre-registered gates before drawing conclusions.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    print(f"wrote {out / 'metrics.csv'} for {summary['runs']} trained runs", flush=True)


if __name__ == "__main__":
    main(parse_args())
