"""Single-knob ablation ladder for the deep branching network.

A RungConfig is (net knobs, training knobs) plus the name of the rung it
was derived from.  RUNG_DELTAS lists the ladder of the 2026-09-15 design
spec; `derive_rung(name, parent)` applies one delta to a parent rung so
that each rung differs from its parent in exactly the listed fields.
`run_rung` trains one net per training seed on a frozen dataset and
returns RunRecords; `summarise` turns records into the per-(rung,
benchmark) accuracy/robustness table.
"""

from __future__ import annotations

import csv
import dataclasses
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import torch

from .generator import TrainingData
from .net import DeepBranchNet
from .solver import _grid_inputs, grid_errors, net_on_grid, \
    train_deep_branching


@dataclass(frozen=True)
class NetConfig:
    hidden_layers: int = 6
    neurons: int = 20
    activation: str = "tanh"
    norm: str = "batch"
    fourier_features: int = 0
    fourier_sigma: float = 1.0
    scale_input: bool = False
    scale_output: bool = False


@dataclass(frozen=True)
class TrainConfig:
    epochs: int = 3000
    lr: float = 0.01
    loss: str = "mse"
    schedule: str = "multistep"
    grad_clip: Optional[float] = None
    lbfgs_steps: int = 0


@dataclass(frozen=True)
class RungConfig:
    name: str
    parent: Optional[str]
    net: NetConfig
    train: TrainConfig

    def to_json(self) -> str:
        return json.dumps(dataclasses.asdict(self), sort_keys=True)


BASELINE = RungConfig("R0", None, NetConfig(), TrainConfig())

# rung name -> {"net": {...}, "train": {...}} applied on top of the parent
RUNG_DELTAS: Dict[str, Dict[str, dict]] = {
    "R1": {"net": {"scale_input": True}},
    "R2": {"net": {"scale_output": True}},
    "R3a": {"net": {"norm": "none"}},
    "R3b": {"net": {"norm": "layer"}},
    "R4a": {"net": {"activation": "silu"}},
    "R4b": {"net": {"activation": "gelu"}},
    "R4c": {"net": {"activation": "sin"}},
    "R5a": {"net": {"neurons": 64}},
    "R5b": {"net": {"neurons": 128}},
    "R5c": {"net": {"hidden_layers": 4}},
    "R5d": {"net": {"hidden_layers": 8}},
    "R6": {"net": {"fourier_features": 32, "fourier_sigma": 1.0}},
    "R7": {"train": {"loss": "weighted_mse"}},
    "R8a": {"train": {"schedule": "cosine"}},
    "R8b": {"train": {"grad_clip": 1.0}},
    "R8c": {"train": {"lbfgs_steps": 200}},
}
# factorial cell norm x activation (R34_<norm>_<act>)
for _norm in ("batch", "layer", "none"):
    for _act in ("tanh", "silu", "gelu", "sin"):
        RUNG_DELTAS[f"R34_{_norm}_{_act}"] = {
            "net": {"norm": _norm, "activation": _act}}


def derive_rung(name: str, parent: RungConfig) -> RungConfig:
    delta = RUNG_DELTAS[name]
    net = dataclasses.replace(parent.net, **delta.get("net", {}))
    train = dataclasses.replace(parent.train, **delta.get("train", {}))
    return RungConfig(name, parent.name, net, train)


def build_net(cfg: NetConfig, d: int, seed: int) -> DeepBranchNet:
    torch.manual_seed(seed)
    return DeepBranchNet(d=d, **dataclasses.asdict(cfg))


@dataclass
class RunRecord:
    rung: str
    benchmark: str
    data_seed: int
    train_seed: int          # -1 for an ensemble record
    l1: float
    l2: float
    consistency: float
    final_loss: float
    seconds: float
    n_params: int
    config_json: str

    def key(self) -> Tuple[str, str, int, int]:
        return (self.rung, self.benchmark, self.data_seed, self.train_seed)


@torch.no_grad()
def consistency_statistic(net: DeepBranchNet, data: TrainingData,
                          device: str = "cpu") -> float:
    """JCP Fig. 7 as a number: mean of ((v(tau_i, X_i) - y_i) / stderr_i)^2
    over states with finite target and finite positive stderr.  About 1
    when the net sits inside the Monte Carlo scatter."""
    ok = np.isfinite(data.y) & np.isfinite(data.stderr) & (data.stderr > 0)
    if not ok.any():
        return float("nan")
    net.eval()
    tx = torch.tensor(np.column_stack([data.t[ok], data.x[ok]]),
                      dtype=torch.float32, device=device)
    pred = net(tx).cpu().numpy()
    z = (pred - data.y[ok]) / data.stderr[ok]
    return float(np.mean(z ** 2))


def _safe(x: float) -> float:
    return float(x) if np.isfinite(x) else float("inf")


def run_rung(
    rung: RungConfig,
    *,
    benchmark: str,
    data_seed: int,
    data: TrainingData,
    pde,
    x_lo: float,
    x_hi: float,
    train_seeds: Sequence[int],
    device: str = "cpu",
    verbose: bool = False,
) -> Tuple[List[RunRecord], List[DeepBranchNet]]:
    d = data.x.shape[1]
    records, nets = [], []
    for seed in train_seeds:
        net = build_net(rung.net, d, seed)
        start = time.perf_counter()
        res = train_deep_branching(
            net, data, device=device, **dataclasses.asdict(rung.train))
        seconds = time.perf_counter() - start
        try:
            l1, l2, *_ = grid_errors(net, pde, x_lo=x_lo, x_hi=x_hi,
                                     device=device)
        except (ValueError, RuntimeError):
            l1 = l2 = float("inf")
        rec = RunRecord(
            rung=rung.name, benchmark=benchmark, data_seed=data_seed,
            train_seed=int(seed), l1=_safe(l1), l2=_safe(l2),
            consistency=_safe(consistency_statistic(net, data, device)),
            final_loss=_safe(res.losses[-1]), seconds=seconds,
            n_params=net.n_params, config_json=rung.to_json(),
        )
        records.append(rec)
        nets.append(net)
        if verbose:
            print(f"  {rung.name} {benchmark} d{data_seed} s{seed}: "
                  f"L1 {rec.l1:.2e} L2 {rec.l2:.2e} "
                  f"cons {rec.consistency:.2f} ({seconds:.0f}s)", flush=True)
    return records, nets


def ensemble_record(
    rung: RungConfig,
    nets: Sequence[DeepBranchNet],
    *,
    benchmark: str,
    data_seed: int,
    data: TrainingData,
    pde,
    x_lo: float,
    x_hi: float,
    device: str = "cpu",
) -> RunRecord:
    """Median over the nets' grid predictions (spec rung R9)."""
    d = data.x.shape[1]
    grid, xs, tx = _grid_inputs(d, 0.0, x_lo, x_hi)
    preds = np.median([net_on_grid(n, tx, device=device) for n in nets],
                      axis=0)
    true = np.array([pde.exact_solution(0.0, xs[i]) for i in range(len(grid))])
    err = np.abs(preds - true)
    # consistency of the median net on the training states
    ok = np.isfinite(data.y) & np.isfinite(data.stderr) & (data.stderr > 0)
    ttx = np.column_stack([data.t[ok], data.x[ok]])
    tpred = np.median([net_on_grid(n, ttx, device=device) for n in nets],
                      axis=0)
    cons = float(np.mean(((tpred - data.y[ok]) / data.stderr[ok]) ** 2))
    return RunRecord(
        rung=rung.name, benchmark=benchmark, data_seed=data_seed,
        train_seed=-1, l1=_safe(err.mean()), l2=_safe((err ** 2).mean()),
        consistency=_safe(cons), final_loss=float("nan"), seconds=0.0,
        n_params=nets[0].n_params, config_json=rung.to_json(),
    )


_FIELDS = [f.name for f in dataclasses.fields(RunRecord)]


def read_records(path) -> List[RunRecord]:
    path = Path(path)
    if not path.exists():
        return []
    out = []
    with path.open(newline="") as fh:
        for row in csv.DictReader(fh):
            out.append(RunRecord(
                rung=row["rung"], benchmark=row["benchmark"],
                data_seed=int(row["data_seed"]),
                train_seed=int(row["train_seed"]),
                l1=float(row["l1"]), l2=float(row["l2"]),
                consistency=float(row["consistency"]),
                final_loss=float(row["final_loss"]),
                seconds=float(row["seconds"]),
                n_params=int(row["n_params"]),
                config_json=row["config_json"],
            ))
    return out


def append_records(path, records: Sequence[RunRecord]) -> int:
    """Append rows not already present (by rung/benchmark/data/train seed)."""
    path = Path(path)
    existing = {r.key() for r in read_records(path)}
    new = [r for r in records if r.key() not in existing]
    if not new:
        return 0
    write_header = not path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=_FIELDS)
        if write_header:
            w.writeheader()
        for r in new:
            w.writerow(dataclasses.asdict(r))
    return len(new)


def summarise(records: Sequence[RunRecord]) -> Dict[Tuple[str, str], dict]:
    groups: Dict[Tuple[str, str], List[RunRecord]] = {}
    for r in records:
        if r.train_seed == -1:
            key = (r.rung + "+ens", r.benchmark)
        else:
            key = (r.rung, r.benchmark)
        groups.setdefault(key, []).append(r)
    out = {}
    for key, recs in groups.items():
        l1 = np.array([r.l1 for r in recs])
        l2 = np.array([r.l2 for r in recs])
        cons = np.array([r.consistency for r in recs])
        med = float(np.median(l1))
        out[key] = {
            "n_runs": len(recs),
            "l1_median": med,
            "l2_median": float(np.median(l2)),
            "l1_max": float(l1.max()),
            "n_outliers": int(np.sum(l1 > 3.0 * med)),
            "consistency_median": float(np.median(cons)),
        }
    return out


def format_table(summary: Dict[Tuple[str, str], dict]) -> str:
    lines = ["| rung | benchmark | runs | L1 median | L2 median | L1 max "
             "| outliers | consistency |",
             "|---|---|---|---|---|---|---|---|"]
    for (rung, bench), s in sorted(summary.items()):
        lines.append(
            f"| {rung} | {bench} | {s['n_runs']} | {s['l1_median']:.2e} | "
            f"{s['l2_median']:.2e} | {s['l1_max']:.2e} | {s['n_outliers']} | "
            f"{s['consistency_median']:.2f} |")
    return "\n".join(lines)
