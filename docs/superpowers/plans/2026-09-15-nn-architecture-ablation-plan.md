# Deep-Branching Network Ablation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a harness that trains single-knob variants of the JCP2024 deep-branching network on frozen Monte Carlo data and reports accuracy (grid L1/L2) and robustness (outlier count, Fig-7 consistency statistic) per variant, then run the ladder R0–R9 from the spec.

**Architecture:** Four units under `parabolab/deep/` — `datasets.py` (frozen `.npz` training data), backwards-compatible extensions of `net.py` (norm / activation / Fourier features / scaler buffers) and `solver.py` (weighted loss, schedule, grad-clip, L-BFGS polish, scaler fitting), and `ablation.py` (configs, rung derivation, run records, metrics, CSV). One driver script `examples/nn_ablation.py`. Existing signatures and defaults stay byte-for-byte equivalent so `tests/test_deep.py` and the M4 reproductions are untouched.

**Tech Stack:** Python 3.11, numpy, torch 2.13 (CPU), pytest. Conda env `parabolab`; on Windows run Python as `conda run -n parabolab --no-capture-output python ...` and pytest as `conda run -n parabolab --no-capture-output python -m pytest ...`.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-09-15-nn-architecture-ablation-design.md`. Branch: `research/nn-architecture`.
- Default behaviour of `DeepBranchNet(...)` and `train_deep_branching(...)` must be unchanged: same outputs for the same seed (regression tests in Tasks 2 and 3 enforce this).
- Evaluation referee is `parabolab.deep.solver.grid_errors` (101 points, t = 0). Do not change it.
- No outlier trimming of runs: non-finite results are recorded with `l1 = inf` and counted as outliers.
- Scripts that start worker pools need `if __name__ == "__main__":` (CLAUDE.md gotcha 37).
- Benchmarks and paper budgets (verbatim from the spec): `ac1` = `allen_cahn_nd(d=1, T=0.5)`, segment [-8, 8], M = 100 000; `exp1` = `exponential_gradient_nd(d=1, T=0.05, alpha=10.0)`, segment [-4, 4], M = 30 000; `merton` = `merton_hjb()`, segment [100, 200], M = 10 000. N = 1000 states, data seeds 0, 1, 2, jcp rate, τ ≡ 0, 10 % overtrain.
- Commit after every task with the attribution line `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.

---

## File structure

| File | Responsibility |
|---|---|
| `parabolab/deep/datasets.py` (new) | `DatasetSpec`, `BENCHMARKS`, `dataset_path`, `load_or_generate` — frozen training data on disk |
| `parabolab/deep/net.py` (modify) | `DeepBranchNet` gains `norm`, new activations, Fourier features, scaler buffers |
| `parabolab/deep/solver.py` (modify) | `fit_scalers`; `train_deep_branching` gains `loss`, `schedule`, `grad_clip`, `lbfgs_steps` |
| `parabolab/deep/ablation.py` (new) | `NetConfig`, `TrainConfig`, `RungConfig`, `RUNG_DELTAS`, `derive_rung`, `build_net`, `RunRecord`, `consistency_statistic`, `run_rung`, `ensemble_record`, `append_records`, `read_records`, `summarise`, `format_table` |
| `parabolab/deep/__init__.py` (modify) | export the new names |
| `examples/nn_ablation.py` (new) | CLI driver |
| `tests/test_deep_ablation.py` (new) | fast tests for all of the above |
| `examples/nn_ablation_data/` (new, git-ignored) | the nine `.npz` datasets |
| `examples/nn_ablation_results.csv` (new, checked in) | one row per training run |
| `docs/superpowers/specs/2026-09-15-nn-architecture-ablation-design.md` | results section appended at the end |

---

### Task 1: Frozen datasets (`datasets.py`)

**Files:**
- Create: `parabolab/deep/datasets.py`
- Modify: `parabolab/deep/__init__.py`
- Modify: `.gitignore` (add `examples/nn_ablation_data/`)
- Test: `tests/test_deep_ablation.py`

**Interfaces:**
- Consumes: `parabolab.deep.generator.generate_training_data`, `TrainingData`; `parabolab.library` factories.
- Produces:
  - `DatasetSpec(key: str, factory_name: str, factory_kwargs: tuple[tuple[str, float], ...], x_lo: float, x_hi: float, n_states: int, m_samples: int, seed: int)` frozen dataclass with `.factory()` returning a zero-arg callable.
  - `BENCHMARKS: dict[str, DatasetSpec]` for keys `ac1`, `exp1`, `merton` (seed 0; use `dataclasses.replace(spec, seed=s)` for other seeds).
  - `dataset_path(spec, root) -> pathlib.Path` = `root / f"{spec.key}_s{spec.seed}.npz"`.
  - `load_or_generate(spec, root, *, n_jobs=1, verbose=False) -> TrainingData`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_deep_ablation.py`:

```python
"""Tests for the deep-branching network ablation harness."""

import dataclasses
import functools

import numpy as np
import pytest

torch = pytest.importorskip("torch")

import parabolab.deep as deep
from parabolab.deep import datasets
from parabolab.library import allen_cahn_nd

AC1 = functools.partial(allen_cahn_nd, d=1, T=0.5)

TINY = datasets.DatasetSpec(
    key="tiny", factory_name="allen_cahn_nd",
    factory_kwargs=(("d", 1), ("T", 0.5)),
    x_lo=-1.0, x_hi=1.0, n_states=8, m_samples=4, seed=0,
)


# ---------------------------------------------------------------------------
# datasets
# ---------------------------------------------------------------------------

def test_benchmarks_resolve_to_library_factories():
    for key, spec in datasets.BENCHMARKS.items():
        assert spec.key == key
        pde = spec.factory()()
        assert getattr(pde, "d", 1) == 1
        assert spec.x_lo < spec.x_hi


def test_load_or_generate_roundtrips_bit_identically(tmp_path):
    a = datasets.load_or_generate(TINY, tmp_path)
    assert datasets.dataset_path(TINY, tmp_path).exists()
    b = datasets.load_or_generate(TINY, tmp_path)
    for field in ("t", "x", "y", "stderr", "n_kept"):
        np.testing.assert_array_equal(getattr(a, field), getattr(b, field))
    assert b.m_samples == a.m_samples and b.rate == a.rate
    direct = deep.generate_training_data(
        AC1, n_states=8, m_samples=4, seed=0, x_lo=-1.0, x_hi=1.0)
    np.testing.assert_array_equal(a.y, direct.y)


def test_load_rejects_mismatched_spec(tmp_path):
    datasets.load_or_generate(TINY, tmp_path)
    other = dataclasses.replace(TINY, m_samples=5)   # same key/seed -> same file
    with pytest.raises(ValueError, match="spec"):
        datasets.load_or_generate(other, tmp_path)


def test_corrupt_file_is_regenerated(tmp_path):
    a = datasets.load_or_generate(TINY, tmp_path)
    datasets.dataset_path(TINY, tmp_path).write_bytes(b"not an npz")
    b = datasets.load_or_generate(TINY, tmp_path)
    np.testing.assert_array_equal(a.y, b.y)


def test_factory_is_picklable():
    import pickle
    pickle.dumps(TINY.factory())
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_ablation.py -v`
Expected: FAIL with `ImportError: cannot import name 'datasets'`.

- [ ] **Step 3: Implement `datasets.py`**

```python
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
```

Then in `parabolab/deep/__init__.py` add `from . import datasets` and `"datasets"` to `__all__`. Add the line `examples/nn_ablation_data/` to `.gitignore`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_ablation.py -v`
Expected: 5 PASS.

- [ ] **Step 5: Commit**

```bash
git add parabolab/deep/datasets.py parabolab/deep/__init__.py .gitignore tests/test_deep_ablation.py
git commit -m "feat(deep): frozen .npz training datasets for the ablation study

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 2: Configurable network (`net.py`)

**Files:**
- Modify: `parabolab/deep/net.py`
- Test: `tests/test_deep_ablation.py`

**Interfaces:**
- Produces: `DeepBranchNet(d, hidden_layers=6, neurons=20, activation="tanh", batch_norm=True, device=None, *, norm=None, fourier_features=0, fourier_sigma=1.0, scale_input=False, scale_output=False)`. `norm ∈ {"batch", "layer", "none"}`; `None` means `"batch" if batch_norm else "none"`. `activation ∈ {"tanh", "relu", "id", "silu", "gelu", "sin"}`. Buffers `in_mean`, `in_std` (shape `(d+1,)`), `out_mean`, `out_std` (shape `()`), `fourier_B` (shape `(d, fourier_features)`, only when `fourier_features > 0`). Attributes `scale_input`, `scale_output` (bool), `n_params` property.

- [ ] **Step 1: Record the reference output of the current net**

Run:
```bash
conda run -n parabolab --no-capture-output python -c "
import torch, parabolab.deep as deep
torch.manual_seed(123); net = deep.DeepBranchNet(d=2); net.eval()
x = torch.tensor([[0.0, 0.3, -1.2],[0.1, 2.0, 0.5]])
print([round(float(v), 8) for v in net(x)])"
```
Copy the two printed numbers; they go into the regression test below as `REF_NET_OUT`.

- [ ] **Step 2: Write the failing tests**

Append to `tests/test_deep_ablation.py`:

```python
# ---------------------------------------------------------------------------
# net
# ---------------------------------------------------------------------------

REF_NET_OUT = [<number 1>, <number 2>]   # from Step 1, current main net


def _ref_input():
    return torch.tensor([[0.0, 0.3, -1.2], [0.1, 2.0, 0.5]])


def test_default_net_is_unchanged():
    torch.manual_seed(123)
    net = deep.DeepBranchNet(d=2)
    net.eval()
    out = net(_ref_input())
    np.testing.assert_allclose(out.detach().numpy(), REF_NET_OUT, rtol=0,
                               atol=1e-7)


@pytest.mark.parametrize("norm", ["batch", "layer", "none"])
@pytest.mark.parametrize("act", ["tanh", "relu", "id", "silu", "gelu", "sin"])
def test_net_variants_forward(norm, act):
    net = deep.DeepBranchNet(d=1, hidden_layers=3, neurons=8, norm=norm,
                             activation=act)
    out = net(torch.randn(5, 2))
    assert out.shape == (5,)
    assert torch.isfinite(out).all()
    net.eval()
    assert torch.isfinite(net(torch.zeros(1, 2))).all()


def test_norm_none_matches_batch_norm_false():
    torch.manual_seed(1)
    a = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=4, batch_norm=False)
    torch.manual_seed(1)
    b = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=4, norm="none")
    x = torch.randn(3, 2)
    torch.testing.assert_close(a(x), b(x))


def test_fourier_features_change_input_width():
    net = deep.DeepBranchNet(d=2, hidden_layers=2, neurons=4,
                             fourier_features=8)
    assert net.linears[0].in_features == 1 + 2 * 8
    assert net.fourier_B.shape == (2, 8)
    assert torch.isfinite(net(torch.randn(3, 3))).all()


def test_scalers_are_buffers_and_roundtrip():
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=4,
                             scale_input=True, scale_output=True)
    net.in_mean.copy_(torch.tensor([0.0, 150.0]))
    net.in_std.copy_(torch.tensor([1.0, 30.0]))
    net.out_mean.fill_(2.0)
    net.out_std.fill_(0.5)
    sd = net.state_dict()
    for key in ("in_mean", "in_std", "out_mean", "out_std"):
        assert key in sd
    other = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=4,
                               scale_input=True, scale_output=True)
    other.load_state_dict(sd)
    x = torch.tensor([[0.0, 120.0], [0.0, 180.0]])
    net.eval(); other.eval()
    torch.testing.assert_close(net(x), other(x))


def test_n_params_counts_trainable():
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=4, norm="none")
    # Linear(2,4)=12, Linear(4,4)=20, Linear(4,1)=5
    assert net.n_params == 37
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_ablation.py -v -k "net or norm or fourier or scalers or n_params"`
Expected: `test_default_net_is_unchanged` PASS (nothing changed yet); the rest FAIL with `TypeError: __init__() got an unexpected keyword argument`.

- [ ] **Step 4: Implement**

Replace `parabolab/deep/net.py` with:

```python
"""The feed-forward residual network of JCP2024 eq. (3.2)-(3.3), plus the
knobs of the 2026-09-15 ablation study.

Paper architecture (matching NN^zeta_{d+1,l,m} and the authors' branch.py):

    input (t, x) in R^{d+1}
    -> Linear(d+1, m) -> zeta -> BatchNorm            (first hidden layer)
    -> [ Linear(m, m) -> zeta -> BatchNorm, + skip ]  x (l - 1)  (residual)
    -> Linear(m, 1)                                   (identity output)

Defaults l = 6 hidden layers of m = 20 neurons, zeta = tanh, batch
normalization AFTER the activation (Remark 3.1 iv / branch.py order).
The paper counts the first (non-residual) hidden layer in l, i.e. l = 6
means 1 plain + 5 residual hidden layers, like the authors' layers=5.

Ablation knobs (all default to the paper's behaviour):

    norm              "batch" | "layer" | "none"   (after the activation)
    activation        + "silu" | "gelu" | "sin"
    fourier_features  F > 0 maps x -> [cos(2 pi B x), sin(2 pi B x)],
                      B ~ N(0, fourier_sigma^2) fixed at construction;
                      t is passed through unchanged
    scale_input /     fixed affine maps stored as buffers (in_mean, in_std,
    scale_output      out_mean, out_std); identity until fit_scalers() in
                      solver.py fills them from the training data
"""

from __future__ import annotations

import math

import torch


class Sine(torch.nn.Module):
    def forward(self, x):
        return torch.sin(x)


_ACTIVATIONS = {
    "tanh": torch.nn.Tanh,
    "relu": torch.nn.ReLU,
    "id": torch.nn.Identity,
    "silu": torch.nn.SiLU,
    "gelu": torch.nn.GELU,
    "sin": Sine,
}


def _make_norm(kind: str, neurons: int, device):
    if kind == "batch":
        return torch.nn.BatchNorm1d(neurons, device=device)
    if kind == "layer":
        return torch.nn.LayerNorm(neurons, device=device)
    if kind == "none":
        return torch.nn.Identity()
    raise ValueError(f"unknown norm {kind!r}; use batch, layer or none")


class DeepBranchNet(torch.nn.Module):
    def __init__(
        self,
        d: int,
        hidden_layers: int = 6,
        neurons: int = 20,
        activation: str = "tanh",
        batch_norm: bool = True,
        device=None,
        *,
        norm: str | None = None,
        fourier_features: int = 0,
        fourier_sigma: float = 1.0,
        scale_input: bool = False,
        scale_output: bool = False,
    ) -> None:
        super().__init__()
        if hidden_layers < 1:
            raise ValueError("need at least one hidden layer")
        if fourier_features < 0:
            raise ValueError("fourier_features must be >= 0")
        if norm is None:
            norm = "batch" if batch_norm else "none"
        self.d = d
        self.norm = norm
        self.batch_norm = norm == "batch"      # kept for callers of the flag
        self.fourier_features = fourier_features
        self.scale_input = scale_input
        self.scale_output = scale_output
        self.activation = _ACTIVATIONS[activation]()

        in_dim = d + 1
        if fourier_features > 0:
            self.register_buffer(
                "fourier_B",
                fourier_sigma * torch.randn(d, fourier_features, device=device))
            in_dim = 1 + 2 * fourier_features
        self.register_buffer("in_mean", torch.zeros(d + 1, device=device))
        self.register_buffer("in_std", torch.ones(d + 1, device=device))
        self.register_buffer("out_mean", torch.zeros((), device=device))
        self.register_buffer("out_std", torch.ones((), device=device))

        self.linears = torch.nn.ModuleList(
            [torch.nn.Linear(in_dim, neurons, device=device)]
            + [torch.nn.Linear(neurons, neurons, device=device)
               for _ in range(hidden_layers - 1)]
            + [torch.nn.Linear(neurons, 1, device=device)]
        )
        self.bns = torch.nn.ModuleList(
            [_make_norm(norm, neurons, device) for _ in range(hidden_layers)]
        )

    @property
    def n_params(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def forward(self, tx: torch.Tensor) -> torch.Tensor:
        """tx of shape (batch, d+1) = (t, x_1..x_d) -> (batch,)."""
        z = (tx - self.in_mean) / self.in_std
        if self.fourier_features > 0:
            proj = 2.0 * math.pi * (z[:, 1:] @ self.fourier_B)
            z = torch.cat([z[:, :1], torch.cos(proj), torch.sin(proj)], dim=1)
        y = z
        for idx, (lin, bn) in enumerate(zip(self.linears[:-1], self.bns)):
            tmp = bn(self.activation(lin(y)))
            y = tmp if idx == 0 else tmp + y   # residual skip after layer 0
        out = self.linears[-1](y).reshape(-1)
        return out * self.out_std + self.out_mean
```

Byte-identity of the default path: `(tx - 0) / 1` and `out * 1 + 0` are exact in IEEE arithmetic, `Identity` norm is a no-op, and the buffer registrations do not consume the torch RNG (`zeros`/`ones`), so the Linear initialisation draws are unchanged. The default `norm="batch"` builds the same `BatchNorm1d` modules under the same `bns` names, so existing state dicts still load.

- [ ] **Step 5: Run tests to verify they pass**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_ablation.py tests/test_deep.py -v`
Expected: all PASS, including `test_default_net_is_unchanged` and the existing `test_net_*` tests.

- [ ] **Step 6: Commit**

```bash
git add parabolab/deep/net.py tests/test_deep_ablation.py
git commit -m "feat(deep): norm/activation/Fourier/scaler knobs on DeepBranchNet

Defaults stay byte-identical to the JCP2024 architecture (regression test).

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 3: Training options (`solver.py`)

**Files:**
- Modify: `parabolab/deep/solver.py:37-78`
- Modify: `parabolab/deep/__init__.py` (export `fit_scalers`)
- Test: `tests/test_deep_ablation.py`

**Interfaces:**
- Consumes: `DeepBranchNet` buffers/flags from Task 2; `TrainingData.stderr`.
- Produces:
  - `fit_scalers(net: DeepBranchNet, data: TrainingData) -> None` — fills `in_mean/in_std` if `net.scale_input`, `out_mean/out_std` if `net.scale_output`, from the finite-target rows; a coordinate with std < 1e-12 (τ ≡ 0) gets std 1.
  - `train_deep_branching(net, data, *, epochs=3000, lr=0.01, device="cpu", log_every=100, verbose=False, loss="mse", schedule="multistep", grad_clip=None, lbfgs_steps=0) -> DeepBranchingResult`. `loss ∈ {"mse", "weighted_mse"}`, `schedule ∈ {"multistep", "cosine"}`. `DeepBranchingResult.losses[-1]` is the loss after the L-BFGS polish when `lbfgs_steps > 0`.

- [ ] **Step 1: Record the reference losses of the current trainer**

Run:
```bash
conda run -n parabolab --no-capture-output python -c "
import functools, torch, numpy as np, parabolab.deep as deep
from parabolab.library import allen_cahn_nd
AC1 = functools.partial(allen_cahn_nd, d=1, T=0.5)
data = deep.generate_training_data(AC1, n_states=16, m_samples=8, seed=5, x_lo=-2.0, x_hi=2.0)
torch.manual_seed(7); net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
res = deep.train_deep_branching(net, data, epochs=30, log_every=10)
print([round(float(v), 8) for v in res.losses])"
```
Copy the printed list (4 numbers: epochs 0, 10, 20, 29) into `REF_LOSSES` below.

- [ ] **Step 2: Write the failing tests**

Append to `tests/test_deep_ablation.py`:

```python
# ---------------------------------------------------------------------------
# trainer
# ---------------------------------------------------------------------------

REF_LOSSES = [<n0>, <n1>, <n2>, <n3>]   # from Step 1, current main trainer


def _small_data(seed=5):
    return deep.generate_training_data(
        AC1, n_states=16, m_samples=8, seed=seed, x_lo=-2.0, x_hi=2.0)


def test_default_training_is_unchanged():
    data = _small_data()
    torch.manual_seed(7)
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
    res = deep.train_deep_branching(net, data, epochs=30, log_every=10)
    np.testing.assert_allclose(res.losses, REF_LOSSES, rtol=0, atol=1e-7)


def test_fit_scalers_fills_buffers_and_leaves_t_alone():
    data = _small_data()
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6,
                             scale_input=True, scale_output=True)
    deep.fit_scalers(net, data)
    assert float(net.in_std[0]) == 1.0          # tau == 0 has zero spread
    assert float(net.in_mean[1]) == pytest.approx(data.x[:, 0].mean())
    assert float(net.in_std[1]) == pytest.approx(data.x[:, 0].std())
    assert float(net.out_mean) == pytest.approx(data.y.mean())
    assert float(net.out_std) == pytest.approx(data.y.std())


def test_fit_scalers_is_noop_without_flags():
    data = _small_data()
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
    deep.fit_scalers(net, data)
    assert torch.all(net.in_mean == 0) and torch.all(net.in_std == 1)


def test_weighted_mse_with_equal_stderr_equals_mse():
    data = _small_data()
    data.stderr[:] = 0.3
    torch.manual_seed(7)
    a = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
    ra = deep.train_deep_branching(a, data, epochs=20, log_every=5,
                                   loss="mse")
    torch.manual_seed(7)
    b = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
    rb = deep.train_deep_branching(b, data, epochs=20, log_every=5,
                                   loss="weighted_mse")
    np.testing.assert_allclose(ra.losses, rb.losses, rtol=1e-6)


def test_weighted_mse_ignores_infinite_stderr_rows():
    data = _small_data()
    data.stderr[3] = np.inf
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
    res = deep.train_deep_branching(net, data, epochs=10, loss="weighted_mse")
    assert np.isfinite(res.losses).all()


def test_cosine_schedule_and_grad_clip_run():
    data = _small_data()
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
    res = deep.train_deep_branching(net, data, epochs=10, schedule="cosine",
                                    grad_clip=1.0)
    assert np.isfinite(res.losses).all()


def test_lbfgs_polish_does_not_increase_loss():
    data = _small_data()
    torch.manual_seed(7)
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6, norm="none")
    res = deep.train_deep_branching(net, data, epochs=30, log_every=10,
                                    lbfgs_steps=20)
    assert len(res.losses) == 5                 # 4 Adam logs + 1 L-BFGS
    assert res.losses[-1] <= res.losses[-2] + 1e-12


def test_unknown_loss_or_schedule_raises():
    data = _small_data()
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=6)
    with pytest.raises(ValueError):
        deep.train_deep_branching(net, data, epochs=1, loss="huber")
    with pytest.raises(ValueError):
        deep.train_deep_branching(net, data, epochs=1, schedule="step")
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_ablation.py -v -k "training or scalers or mse or cosine or lbfgs or unknown"`
Expected: `test_default_training_is_unchanged` PASS; others FAIL (`AttributeError: module has no attribute fit_scalers` / `TypeError` unexpected keyword).

- [ ] **Step 4: Implement**

In `parabolab/deep/solver.py`, replace the `train_deep_branching` function (lines 37–78) with:

```python
def fit_scalers(net: DeepBranchNet, data: TrainingData) -> None:
    """Fill the net's input/output scaler buffers from the training data.

    No-op unless the net was built with scale_input / scale_output.  A
    coordinate with no spread (tau == 0 in the paper's protocol) keeps
    std = 1 so it is passed through unchanged.
    """
    finite = np.isfinite(data.y)
    with torch.no_grad():
        if net.scale_input:
            tx = np.column_stack([data.t[finite], data.x[finite]])
            mean = tx.mean(axis=0)
            std = tx.std(axis=0)
            std[std < 1e-12] = 1.0
            net.in_mean.copy_(torch.as_tensor(mean, dtype=torch.float32))
            net.in_std.copy_(torch.as_tensor(std, dtype=torch.float32))
        if net.scale_output:
            y = data.y[finite]
            std = float(y.std())
            net.out_mean.fill_(float(y.mean()))
            net.out_std.fill_(std if std >= 1e-12 else 1.0)


def train_deep_branching(
    net: DeepBranchNet,
    data: TrainingData,
    *,
    epochs: int = 3000,
    lr: float = 0.01,
    device: str = "cpu",
    log_every: int = 100,
    verbose: bool = False,
    loss: str = "mse",
    schedule: str = "multistep",
    grad_clip: Optional[float] = None,
    lbfgs_steps: int = 0,
) -> DeepBranchingResult:
    """Algorithm 2: fit net to the MC targets by full-batch Adam.

    Ablation options (defaults = the paper):
      loss        "mse" | "weighted_mse" (weights 1/stderr^2, mean 1;
                  rows with infinite stderr get weight 0)
      schedule    "multistep" (lr / 10 at P/3, 2P/3) | "cosine"
      grad_clip   clip the gradient norm before every Adam step
      lbfgs_steps full-batch L-BFGS iterations after the Adam epochs
    """
    if loss not in ("mse", "weighted_mse"):
        raise ValueError(f"unknown loss {loss!r}")
    if schedule not in ("multistep", "cosine"):
        raise ValueError(f"unknown schedule {schedule!r}")

    fit_scalers(net, data)
    net = net.to(device)
    finite = np.isfinite(data.y)
    tx = torch.tensor(
        np.column_stack([data.t[finite], data.x[finite]]),
        dtype=torch.float32, device=device,
    )
    y = torch.tensor(data.y[finite], dtype=torch.float32, device=device)

    if loss == "weighted_mse":
        se = data.stderr[finite].astype(float)
        ok = np.isfinite(se)
        eps = 1e-3 * np.median(se[ok]) if ok.any() else 1.0
        w = np.zeros_like(se)
        w[ok] = 1.0 / np.maximum(se[ok], eps) ** 2
        w /= w.mean()
        weights = torch.tensor(w, dtype=torch.float32, device=device)

        def loss_fn(pred, target):
            return torch.mean(weights * (pred - target) ** 2)
    else:
        loss_fn = torch.nn.MSELoss()

    optimizer = torch.optim.Adam(net.parameters(), lr=lr)
    if schedule == "multistep":
        scheduler = torch.optim.lr_scheduler.MultiStepLR(
            optimizer, milestones=[epochs // 3, 2 * epochs // 3], gamma=0.1
        )
    else:
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=epochs
        )

    losses = []
    start = time.perf_counter()
    net.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        loss_val = loss_fn(net(tx), y)
        loss_val.backward()
        if grad_clip is not None:
            torch.nn.utils.clip_grad_norm_(net.parameters(), grad_clip)
        optimizer.step()
        scheduler.step()
        if epoch % log_every == 0 or epoch == epochs - 1:
            losses.append(float(loss_val.detach()))
            if verbose:
                print(f"  epoch {epoch}: loss {losses[-1]:.6f}", flush=True)

    if lbfgs_steps > 0:
        lbfgs = torch.optim.LBFGS(
            net.parameters(), lr=1.0, max_iter=lbfgs_steps,
            history_size=50, line_search_fn="strong_wolfe",
        )

        def closure():
            lbfgs.zero_grad()
            l = loss_fn(net(tx), y)
            l.backward()
            return l

        lbfgs.step(closure)
        with torch.no_grad():
            losses.append(float(loss_fn(net(tx), y)))
        if verbose:
            print(f"  L-BFGS: loss {losses[-1]:.6f}", flush=True)

    seconds = time.perf_counter() - start
    net.eval()
    return DeepBranchingResult(net=net, losses=np.array(losses),
                               seconds=seconds)
```

Note on the byte-identity guard: for `loss="mse"` the code path is identical to the old one except `loss_fn` is the same `MSELoss`, `fit_scalers` is a no-op, `grad_clip` is skipped, and `MultiStepLR` is constructed with the same arguments, so `REF_LOSSES` must match exactly. If they don't, the change is wrong — do not loosen the tolerance.

In `parabolab/deep/__init__.py` add `fit_scalers` to the `from .solver import (...)` list and to `__all__`.

- [ ] **Step 5: Run tests to verify they pass**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_ablation.py tests/test_deep.py -v`
Expected: all PASS.

- [ ] **Step 6: Commit**

```bash
git add parabolab/deep/solver.py parabolab/deep/__init__.py tests/test_deep_ablation.py
git commit -m "feat(deep): weighted loss, cosine schedule, grad clip, L-BFGS polish, scaler fitting

Default path byte-identical to Algorithm 2 (regression test on logged losses).

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 4: Ablation configs, runs, metrics (`ablation.py`)

**Files:**
- Create: `parabolab/deep/ablation.py`
- Modify: `parabolab/deep/__init__.py`
- Test: `tests/test_deep_ablation.py`

**Interfaces:**
- Consumes: Task 2 `DeepBranchNet(...)` keyword arguments; Task 3 `train_deep_branching(...)` keyword arguments; `grid_errors`, `net_on_grid`, `_grid_inputs` from `solver.py`; `TrainingData`.
- Produces:
  - `NetConfig(hidden_layers=6, neurons=20, activation="tanh", norm="batch", fourier_features=0, fourier_sigma=1.0, scale_input=False, scale_output=False)` frozen dataclass.
  - `TrainConfig(epochs=3000, lr=0.01, loss="mse", schedule="multistep", grad_clip=None, lbfgs_steps=0)` frozen dataclass.
  - `RungConfig(name: str, parent: Optional[str], net: NetConfig, train: TrainConfig)` frozen; `.to_json() -> str`.
  - `BASELINE: RungConfig` (name `"R0"`, parent `None`).
  - `RUNG_DELTAS: dict[str, dict[str, dict]]` — rung name → `{"net": {...}, "train": {...}}` overrides.
  - `derive_rung(name: str, parent: RungConfig) -> RungConfig`.
  - `build_net(cfg: NetConfig, d: int, seed: int) -> DeepBranchNet` (seeds torch, constructs).
  - `RunRecord` dataclass: `rung, benchmark, data_seed, train_seed, l1, l2, consistency, final_loss, seconds, n_params, config_json`.
  - `consistency_statistic(net, data, device="cpu") -> float`.
  - `run_rung(rung, *, benchmark: str, data_seed: int, data: TrainingData, pde, x_lo: float, x_hi: float, train_seeds: Sequence[int], device="cpu", verbose=False) -> tuple[list[RunRecord], list[DeepBranchNet]]`.
  - `ensemble_record(rung, nets, *, benchmark, data_seed, data, pde, x_lo, x_hi, device="cpu") -> RunRecord` (train_seed = -1; median over nets of grid predictions).
  - `append_records(path, records) -> int` (rows written; skips duplicates on `(rung, benchmark, data_seed, train_seed)`), `read_records(path) -> list[RunRecord]`.
  - `summarise(records) -> dict[tuple[str, str], dict]` with keys `n_runs, l1_median, l2_median, l1_max, n_outliers, consistency_median`.
  - `format_table(summary) -> str` (Markdown).

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_deep_ablation.py`:

```python
# ---------------------------------------------------------------------------
# ablation harness
# ---------------------------------------------------------------------------

from parabolab.deep import ablation


def test_derive_rung_applies_one_delta_and_records_parent():
    r1 = ablation.derive_rung("R1", ablation.BASELINE)
    assert r1.parent == "R0"
    assert r1.net.scale_input is True
    assert r1.net == dataclasses.replace(ablation.BASELINE.net,
                                         scale_input=True)
    assert r1.train == ablation.BASELINE.train
    r2 = ablation.derive_rung("R2", r1)
    assert r2.parent == "R1" and r2.net.scale_input and r2.net.scale_output


def test_every_delta_names_only_known_fields():
    for name, delta in ablation.RUNG_DELTAS.items():
        rung = ablation.derive_rung(name, ablation.BASELINE)
        assert rung.name == name
        for section, fields in delta.items():
            assert section in ("net", "train")
            cfg = getattr(rung, section)
            for key, val in fields.items():
                assert getattr(cfg, key) == val


def test_build_net_is_seed_deterministic():
    cfg = ablation.NetConfig(hidden_layers=2, neurons=4, norm="none")
    a = ablation.build_net(cfg, d=1, seed=3)
    b = ablation.build_net(cfg, d=1, seed=3)
    x = torch.randn(2, 2)
    torch.testing.assert_close(a(x), b(x))
    assert a.n_params == 4 * 2 + 4 + 4 * 4 + 4 + 4 + 1


def test_consistency_statistic_is_one_for_perfect_net_plus_noise():
    data = _small_data()
    net = deep.DeepBranchNet(d=1, hidden_layers=2, neurons=4, norm="none")
    net.eval()
    tx = torch.tensor(np.column_stack([data.t, data.x]), dtype=torch.float32)
    with torch.no_grad():
        pred = net(tx).numpy()
    rng = np.random.default_rng(0)
    data.stderr[:] = 0.2
    data.y[:] = pred + 0.2 * rng.standard_normal(len(data))
    stat = ablation.consistency_statistic(net, data)
    assert 0.3 < stat < 3.0


def test_run_rung_returns_one_record_per_seed(tmp_path):
    data = _small_data()
    cfg = ablation.RungConfig(
        "T", None,
        ablation.NetConfig(hidden_layers=2, neurons=4),
        ablation.TrainConfig(epochs=5),
    )
    records, nets = ablation.run_rung(
        cfg, benchmark="tiny", data_seed=5, data=data, pde=AC1(),
        x_lo=-2.0, x_hi=2.0, train_seeds=[0, 1])
    assert [r.train_seed for r in records] == [0, 1]
    assert len(nets) == 2
    for r in records:
        assert r.rung == "T" and r.benchmark == "tiny" and r.data_seed == 5
        assert np.isfinite([r.l1, r.l2, r.consistency, r.final_loss]).all()
        assert r.n_params == nets[0].n_params
        assert '"epochs": 5' in r.config_json
    ens = ablation.ensemble_record(
        cfg, nets, benchmark="tiny", data_seed=5, data=data, pde=AC1(),
        x_lo=-2.0, x_hi=2.0)
    assert ens.train_seed == -1 and np.isfinite(ens.l1)


def test_append_records_is_idempotent(tmp_path):
    path = tmp_path / "r.csv"
    rec = ablation.RunRecord("R0", "ac1", 0, 0, 1e-3, 1e-6, 1.1, 2e-3,
                             10.0, 100, "{}")
    assert ablation.append_records(path, [rec]) == 1
    assert ablation.append_records(path, [rec]) == 0
    rec2 = dataclasses.replace(rec, train_seed=1, l1=np.inf)
    assert ablation.append_records(path, [rec, rec2]) == 1
    back = ablation.read_records(path)
    assert len(back) == 2
    assert back[1].l1 == np.inf and back[1].n_params == 100


def test_summarise_counts_outliers_by_three_times_median():
    def rec(seed, l1):
        return ablation.RunRecord("R0", "ac1", 0, seed, l1, l1 ** 2, 1.0,
                                  0.0, 1.0, 10, "{}")
    recs = [rec(0, 1.0), rec(1, 1.0), rec(2, 1.2), rec(3, 4.0),
            rec(4, np.inf)]
    s = ablation.summarise(recs)[("R0", "ac1")]
    assert s["n_runs"] == 5
    assert s["l1_median"] == pytest.approx(1.2)
    assert s["l1_max"] == np.inf
    assert s["n_outliers"] == 2            # 4.0 and inf exceed 3 * 1.2
    assert s["consistency_median"] == 1.0
    table = ablation.format_table(ablation.summarise(recs))
    assert "| R0 | ac1 |" in table
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_ablation.py -v -k "rung or delta or build_net or consistency or records or summarise"`
Expected: FAIL with `ImportError: cannot import name 'ablation'`.

- [ ] **Step 3: Implement `ablation.py`**

```python
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
```

Add `from . import ablation` and `"ablation"` to `__all__` in `parabolab/deep/__init__.py`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_ablation.py tests/test_deep.py -v`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add parabolab/deep/ablation.py parabolab/deep/__init__.py tests/test_deep_ablation.py
git commit -m "feat(deep): ablation ladder configs, run records, metrics and CSV

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 5: Driver script (`examples/nn_ablation.py`)

**Files:**
- Create: `examples/nn_ablation.py`
- Test: `tests/test_deep_ablation.py` (one subprocess smoke test on the tiny spec)

**Interfaces:**
- Consumes: everything from Tasks 1 and 4.
- Produces: CLI
  `python examples/nn_ablation.py --rungs R1 R2 --parent R0 --benchmarks ac1 merton --data-seeds 0 1 2 --train-seeds 5 --data-root examples/nn_ablation_data --out examples/nn_ablation_results.csv --jobs 8 [--ensemble] [--report] [--tiny]`.
  `--parent` names the rung whose config each listed rung is derived from; `R0` needs no parent. `--tiny` swaps the benchmark specs for 8-state/4-sample versions (test hook). `--report` prints the Markdown table of everything in `--out` and exits.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_deep_ablation.py`:

```python
# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------

import subprocess
import sys
from pathlib import Path


def test_driver_tiny_end_to_end(tmp_path):
    script = Path(__file__).resolve().parents[1] / "examples" / "nn_ablation.py"
    out = tmp_path / "res.csv"
    cmd = [sys.executable, str(script), "--rungs", "R0", "R1",
           "--parent", "R0", "--benchmarks", "ac1", "--data-seeds", "0",
           "--train-seeds", "2", "--data-root", str(tmp_path / "data"),
           "--out", str(out), "--tiny", "--epochs", "5", "--ensemble",
           "--jobs", "1"]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    recs = ablation.read_records(out)
    assert {r.rung for r in recs} == {"R0", "R1"}
    assert sum(r.train_seed == -1 for r in recs) == 2   # one ensemble per rung
    assert len(recs) == 2 * (2 + 1)
    report = subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--report"],
        check=True, capture_output=True, text=True).stdout
    assert "| R1 | ac1 |" in report and "| R0+ens | ac1 |" in report
```

- [ ] **Step 2: Run test to verify it fails**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_ablation.py -v -k driver`
Expected: FAIL (`FileNotFoundError` / non-zero exit: script does not exist).

- [ ] **Step 3: Implement the driver**

```python
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
                n = ablation.append_records(args.out, recs)
                print(f"wrote {n} rows to {args.out}", flush=True)

    print(ablation.format_table(ablation.summarise(
        ablation.read_records(args.out))))


if __name__ == "__main__":
    main(parse_args())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_ablation.py -v -k driver`
Expected: PASS (takes ~10–20 s: two tiny datasets are generated and 2 rungs × 2 seeds × 5 epochs trained).

- [ ] **Step 5: Run the whole fast suite**

Run: `conda run -n parabolab --no-capture-output python -m pytest -q`
Expected: all green (previous count 143 + the new tests), zero failures.

- [ ] **Step 6: Commit**

```bash
git add examples/nn_ablation.py tests/test_deep_ablation.py
git commit -m "feat: nn_ablation driver script

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 6: Generate the frozen datasets and run R0

**Files:**
- Create: `examples/nn_ablation_data/*.npz` (git-ignored), `examples/nn_ablation_results.csv`
- Modify: `docs/superpowers/specs/2026-09-15-nn-architecture-ablation-design.md` (append `## Results` with the R0 table)

- [ ] **Step 1: Generate data and run the baseline**

Run (≈ 10 min data generation + 45 trainings ≈ 15 min on 8+ cores):
```bash
conda run -n parabolab --no-capture-output python examples/nn_ablation.py --rungs R0 --benchmarks ac1 exp1 merton --data-seeds 0 1 2 --train-seeds 5 --jobs 8 --ensemble
```
Expected: nine `.npz` files under `examples/nn_ablation_data/`, 54 rows in `examples/nn_ablation_results.csv` (45 runs + 9 ensembles), and a printed table.

- [ ] **Step 2: Check the reproduction criterion**

Compare the R0 `L1 median` per benchmark with the spec table: `ac1` ≤ 2 × 1.32e-3, `exp1` ≤ 2 × 1.17e-2, `merton` ≤ 2 × 8.49e-3. If any fails, stop and investigate (data seeds, rate = jcp_rate, overtrain margin, `--full` settings of the `jcp_table*_deep.py` scripts) before running further rungs; record the finding in the spec's Results section either way.

- [ ] **Step 3: Record**

Append to the spec:

```markdown
## Results

### R0 — paper baseline on frozen data

<paste `--report` table rows for R0 and R0+ens>

Reading: <one paragraph: reproduction criterion met / not met per
benchmark; number of outlier runs on merton; consistency statistic>.
```

- [ ] **Step 4: Commit**

```bash
git add examples/nn_ablation_results.csv docs/superpowers/specs/2026-09-15-nn-architecture-ablation-design.md
git commit -m "exp: ablation R0 baseline on frozen data

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 7: Climb the ladder (R1 … R9), one rung per commit

**Files:**
- Modify: `examples/nn_ablation_results.csv`, the spec's `## Results` section, `CLAUDE.md` (gotchas, if any).

Repeat the following for each rung in the spec's order — R1; R2; R3a, R3b; R4a, R4b, R4c; the R34 cell; R5a–R5d; R6; R7; R8a–R8c — using the **kept** rung so far as `--parent`. The kept rung is the one with the lowest total `outliers` over the three benchmarks, ties broken by lower total `L1 median`; a rung that improves one benchmark and worsens another is not kept. R9 (ensemble) is already produced by `--ensemble` on every rung and is read off the `+ens` rows.

- [ ] **Step 1: Run the rung(s)**

```bash
conda run -n parabolab --no-capture-output python examples/nn_ablation.py --rungs <names> --parent <kept rung> --train-seeds 5 --jobs 8 --ensemble
```
(For the R34 cell pass only the names not already covered by R3/R4 with the same parent, e.g. `R34_layer_silu R34_none_silu R34_layer_gelu ...`.)

- [ ] **Step 2: Report and decide**

```bash
conda run -n parabolab --no-capture-output python examples/nn_ablation.py --report
```
Apply the kept-rung rule. Append to the spec's Results section:

```markdown
### <rung> — <one-line change> (parent <kept>)

<table rows for this rung and its parent, all benchmarks>

Reading: helped / hurt / no effect, with the numbers; kept: yes/no.
```

- [ ] **Step 3: Commit**

```bash
git add examples/nn_ablation_results.csv docs/superpowers/specs/2026-09-15-nn-architecture-ablation-design.md
git commit -m "exp: ablation <rung> (<change>) — <kept|not kept>

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

- [ ] **Step 4: After the last rung — summary and gotchas**

Append a `### Kept path` subsection to the spec listing the chain R0 → … and the final numbers vs the paper; if anything non-obvious emerged (e.g. input scaling alone removing the Merton anomaly, L-BFGS diverging with BatchNorm, sin activation needing a smaller lr), add a numbered gotcha to `CLAUDE.md` under a new `## Gotchas discovered (NN ablation)` heading. Commit:

```bash
git add docs/superpowers/specs/2026-09-15-nn-architecture-ablation-design.md CLAUDE.md
git commit -m "docs: ablation ladder results and gotchas

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```
