"""Frozen training datasets for the network ablation study.

The ablation ladder trains many network variants on the SAME Monte Carlo
data.  `load_or_generate` generates a dataset once with
`generate_training_data`, saves it as .npz together with its spec, and
reloads it on later calls; a stored spec that disagrees with the requested
one is an error, never a silent overwrite.
"""

from __future__ import annotations

import dataclasses
import functools
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Tuple

import numpy as np

from .. import library
from .generator import TrainingData, generate_training_data


@dataclass(frozen=True)
class DatasetSpec:
    key: str
    factory_name: str                         # attribute of parabolab.library
    factory_kwargs: Tuple[Tuple[str, float], ...]
    x_lo: float
    x_hi: float
    n_states: int
    m_samples: int
    seed: int

    def factory(self) -> Callable[[], object]:
        # functools.partial, not a lambda: the factory is shipped to worker
        # processes by generate_training_data and must pickle.
        return functools.partial(getattr(library, self.factory_name),
                                 **dict(self.factory_kwargs))

    def to_json(self) -> str:
        return json.dumps(dataclasses.asdict(self), sort_keys=True)


BENCHMARKS = {
    "ac1": DatasetSpec("ac1", "allen_cahn_nd", (("d", 1), ("T", 0.5)),
                       -8.0, 8.0, 1000, 100_000, 0),
    "exp1": DatasetSpec("exp1", "exponential_gradient_nd",
                        (("d", 1), ("T", 0.05), ("alpha", 10.0)),
                        -4.0, 4.0, 1000, 30_000, 0),
    "merton": DatasetSpec("merton", "merton_hjb", (),
                          100.0, 200.0, 1000, 10_000, 0),
}


def dataset_path(spec: DatasetSpec, root) -> Path:
    return Path(root) / f"{spec.key}_s{spec.seed}.npz"


def load_or_generate(spec: DatasetSpec, root, *, n_jobs: int = 1,
                     verbose: bool = False) -> TrainingData:
    path = dataset_path(spec, root)
    if path.exists():
        try:
            with np.load(path, allow_pickle=False) as f:
                stored = str(f["spec"])
                if stored != spec.to_json():
                    raise ValueError(
                        f"{path} was generated from spec {stored}, "
                        f"requested {spec.to_json()}")
                return TrainingData(
                    t=f["t"], x=f["x"], y=f["y"], stderr=f["stderr"],
                    n_kept=f["n_kept"], m_samples=int(f["m_samples"]),
                    rate=float(f["rate"]), seconds=float(f["seconds"]),
                )
        except ValueError as exc:
            if "spec" in str(exc):
                raise
            print(f"{path} unreadable ({exc}); regenerating", flush=True)
        except (OSError, KeyError) as exc:
            print(f"{path} unreadable ({exc}); regenerating", flush=True)
    if verbose:
        print(f"generating {path} ...", flush=True)
    data = generate_training_data(
        spec.factory(), n_states=spec.n_states, m_samples=spec.m_samples,
        seed=spec.seed, x_lo=spec.x_lo, x_hi=spec.x_hi, n_jobs=n_jobs,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, spec=spec.to_json(), t=data.t, x=data.x, y=data.y,
             stderr=data.stderr, n_kept=data.n_kept,
             m_samples=data.m_samples, rate=data.rate,
             seconds=data.seconds)
    return data
