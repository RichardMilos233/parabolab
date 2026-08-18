"""Repeated-run experiment driver reproducing JCP2024's error protocol.

For each of ``n_runs`` independent runs: generate N states x M tree
samples, train a fresh net (Algorithm 2), record the L1/L2 error on the
101-point evaluation grid at t = 0.  Reports mean and stdev over runs,
like the paper's Tables 1/3/5.
"""

from __future__ import annotations

import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from typing import Callable, Optional

import numpy as np

from .generator import TrainingData, generate_training_data
from .net import DeepBranchNet
from .solver import grid_errors, train_deep_branching


@dataclass
class ExperimentResult:
    l1: np.ndarray             # (n_runs,)
    l2: np.ndarray             # (n_runs,)
    datagen_seconds: np.ndarray
    train_seconds: np.ndarray
    nets: list = field(default_factory=list)
    data: list = field(default_factory=list)   # TrainingData per run

    def summary(self) -> str:
        sd1 = f"{self.l1.std(ddof=1):.2e}" if len(self.l1) > 1 else "n/a"
        sd2 = f"{self.l2.std(ddof=1):.2e}" if len(self.l2) > 1 else "n/a"
        return (
            f"L1 {self.l1.mean():.2e} (SD {sd1})  "
            f"L2 {self.l2.mean():.2e} (SD {sd2})  "
            f"[datagen {self.datagen_seconds.mean():.0f}s + "
            f"train {self.train_seconds.mean():.0f}s per run]"
        )


def run_experiment(
    pde_factory: Callable[[], object],
    *,
    x_lo: float,
    x_hi: float,
    n_states: int = 1000,
    m_samples: int = 1000,
    epochs: int = 3000,
    n_runs: int = 3,
    seed0: int = 0,
    n_jobs: int = 1,
    device: str = "cpu",
    activation: str = "tanh",
    hidden_layers: int = 6,
    neurons: int = 20,
    rate: Optional[float] = None,
    keep_nets: bool = True,
    verbose: bool = True,
) -> ExperimentResult:
    pde = pde_factory()
    d = getattr(pde, "d", 1)

    l1s, l2s, gsecs, tsecs, nets, datas = [], [], [], [], [], []
    executor = ProcessPoolExecutor(max_workers=n_jobs) if n_jobs > 1 \
        else None
    try:
        for run in range(n_runs):
            data = generate_training_data(
                pde_factory, n_states=n_states, m_samples=m_samples,
                seed=seed0 + run, rate=rate, x_lo=x_lo, x_hi=x_hi,
                n_jobs=n_jobs, executor=executor,
            )
            import torch

            torch.manual_seed(seed0 + run)
            net = DeepBranchNet(d=d, hidden_layers=hidden_layers,
                                neurons=neurons, activation=activation)
            res = train_deep_branching(net, data, epochs=epochs,
                                       device=device)
            l1, l2, *_ = grid_errors(net, pde, x_lo=x_lo, x_hi=x_hi,
                                     device=device)
            l1s.append(l1)
            l2s.append(l2)
            gsecs.append(data.seconds)
            tsecs.append(res.seconds)
            if keep_nets:
                nets.append(net)
                datas.append(data)
            if verbose:
                print(f"  run {run}: L1 {l1:.2e}  L2 {l2:.2e}  "
                      f"(datagen {data.seconds:.0f}s, "
                      f"train {res.seconds:.0f}s)", flush=True)
    finally:
        if executor is not None:
            executor.shutdown()

    return ExperimentResult(
        l1=np.array(l1s), l2=np.array(l2s),
        datagen_seconds=np.array(gsecs), train_seconds=np.array(tsecs),
        nets=nets, data=datas,
    )
