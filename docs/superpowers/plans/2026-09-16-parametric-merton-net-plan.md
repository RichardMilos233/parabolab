# Parameter-Conditioned Merton Net (D02) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** One network for the Merton family, input \((t,x,\theta)\), output \(u\), with the optimal portfolio fraction from its autograd derivatives; compare concat vs FiLM conditioning and test whether derivative labels are needed for accurate policies.

**Architecture:** Extend the corpus with optional derivative labels (`DxN` root codes, separate `Instance.deriv*` arrays); add `condnet.py` (`ConditionedNet`, R5A trunk with concat or FiLM conditioning and autograd derivatives), `condtrain.py` (pooled mini-batch training, evaluation with the closed-form Merton policy as referee, the per-instance baseline), a driver with rungs C0–C3.

**Tech Stack:** Python 3.11, numpy, torch 2.11+cu128, pytest; `conda run -n parabolab --no-capture-output python ...` on PowerShell.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-09-15-parametric-merton-net-design.md`. Branch `research/nn-architecture`.
- Existing behaviour byte-identical: `InstanceSpec` default `deriv_codes=()` keeps every `.npz` loadable and `tests/test_deep_corpus.py`, `tests/test_deep_setnet.py`, `tests/test_deep_ablation.py`, `tests/test_deep.py` green.
- Family `merton` (verbatim): \(\gamma\in[0.3,0.8]\), \(\mu\in[0.02,0.06]\), \(\sigma\in[0.08,0.2]\), \(T=0.1\), \(\rho=0.01\), segment \([100,200]\); 500 train (seed 0) / 50 held-out (seed 1), 500 states, \(M=1000\).
- Policy referee: \(\pi^* = -\frac{\mu}{\sigma^2}\frac{u_x}{x\,u_{xx}}\), exact value \(\mu/(\gamma\sigma^2)\). Relative error reported on the interior grid \(x\in[110,190]\) and on the full grid.
- Rungs C0 (per-instance R5A), C1 (concat, u only), C2 (film, u only), C3 (best of C1/C2 + derivative labels, \(w_1=w_2=1\)). Kept rung: lower held-out u-L1 median, then lower policy error. Success (fixed): C1 or C2 u-L1 median ≤ 1.5× C0's; policy error ≤ 2 % for the kept rung.
- Driver under `if __name__ == "__main__"`; `examples/parametric_merton.csv` un-ignored in `.gitignore`.
- Commit messages end with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.

---

## File structure

| File | Responsibility |
|---|---|
| `parabolab/library.py` (add `merton_hjb_derivatives`) | closed-form \(u_x, u_{xx}\) |
| `parabolab/deep/corpus.py` (modify) | `deriv_codes`, `Family.deriv_factory_name`, `Instance.deriv/deriv_stderr/deriv_exact`, generation/save/load |
| `parabolab/deep/condnet.py` (new) | `ConditionedNet`, `autograd_derivatives` |
| `parabolab/deep/condtrain.py` (new) | `pooled_rows`, `fit_conditioned_scalers`, `train_conditioned`, `merton_policy_exact`, `policy_from_derivatives`, `evaluate_conditioned`, `per_instance_baseline` |
| `parabolab/deep/__init__.py` (modify) | exports |
| `examples/parametric_merton.py` (new) | driver |
| `tests/test_deep_corpus.py`, `tests/test_deep_condnet.py` (new) | tests |
| `.gitignore`, spec `## Results`, `CLAUDE.md` | bookkeeping |

---

### Task 1: Derivative labels in the corpus

**Files:**
- Modify: `parabolab/library.py` (after `merton_hjb`), `parabolab/deep/corpus.py`
- Test: `tests/test_deep_corpus.py`

**Interfaces:**
- Produces: `library.merton_hjb_derivatives(T=0.1, mu=0.03, sigma=0.1, gamma=0.5, rho=0.01) -> tuple[Callable, Callable]` — `(ux, uxx)`, each `(t: float, xv) -> float` with the same argument convention as `merton_hjb().exact_solution`.
- `Family` gains `deriv_factory_name: Optional[str] = None` (set to `"merton_hjb_derivatives"` for `merton`, `None` for `ac1`).
- `InstanceSpec` gains `deriv_codes: Tuple[str, ...] = ()`; `DERIV_CODES = {"Dx1": DxN((1,)), "Dx2": DxN((2,))}` in `corpus.py`.
- `Instance` gains `deriv: Optional[np.ndarray] = None` `(n_codes, N)`, `deriv_stderr`, `deriv_exact` (same shape); `finite` also requires finite `deriv`/`deriv_stderr` when present.
- `generate_instance` draws one extra `generate_training_data(..., code=DERIV_CODES[name], seed=1000*spec.seed + 100 + k)` per code; save/load handle the optional arrays (absent keys ⇒ `None`).

- [ ] **Step 1: Failing tests** — append to `tests/test_deep_corpus.py`:

```python
# ---------------------------------------------------------------------------
# derivative labels
# ---------------------------------------------------------------------------

from parabolab.library import merton_hjb, merton_hjb_derivatives


def test_merton_derivatives_match_finite_differences():
    kw = dict(T=0.1, mu=0.04, sigma=0.15, gamma=0.6, rho=0.01)
    pde = merton_hjb(**kw)
    ux, uxx = merton_hjb_derivatives(**kw)
    h = 1e-3
    for t in (0.0, 0.05):
        for x in (110.0, 150.0, 190.0):
            u = lambda z: pde.exact_solution(t, np.array([z]))
            fd1 = (u(x + h) - u(x - h)) / (2 * h)
            fd2 = (u(x + h) - 2 * u(x) + u(x - h)) / h ** 2
            assert ux(t, np.array([x])) == pytest.approx(fd1, rel=1e-5)
            assert uxx(t, np.array([x])) == pytest.approx(fd2, rel=1e-3)


def test_instance_with_derivative_labels():
    spec = corpus.InstanceSpec("merton", (0.5, 0.03, 0.1), 40, 400, 21,
                               n_draws=1, deriv_codes=("Dx1", "Dx2"))
    inst = corpus.generate_instance(spec, n_jobs=2)
    assert inst.y.shape == (1, 40) and inst.deriv.shape == (2, 40)
    assert inst.deriv_stderr.shape == (2, 40) and inst.deriv_exact.shape == (2, 40)
    ok = inst.finite
    assert ok.sum() >= 38
    z = (inst.deriv[:, ok] - inst.deriv_exact[:, ok]) / inst.deriv_stderr[:, ok]
    assert np.abs(z).max() < 5.0   # heavy-ish tails at M = 400 (gotcha 15)
    # the labels are the right size: u_x ~ 0.1..0.3 for these parameters
    assert 0.05 < np.median(np.abs(inst.deriv_exact[0])) < 0.5


def test_default_spec_has_no_derivatives_and_roundtrips(tmp_path):
    spec = corpus.InstanceSpec("merton", (0.5, 0.03, 0.1), 8, 4, 22)
    inst = corpus.generate_instance(spec)
    assert inst.deriv is None and inst.deriv_exact is None
    assert '"deriv_codes": []' in spec.to_json()
    a = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    b = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    assert b.deriv is None
    np.testing.assert_array_equal(a.y, b.y)


def test_derivative_instance_roundtrips(tmp_path):
    spec = corpus.InstanceSpec("merton", (0.5, 0.03, 0.1), 8, 4, 23,
                               n_draws=1, deriv_codes=("Dx1",))
    a = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    b = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    np.testing.assert_array_equal(a.deriv, b.deriv)
    np.testing.assert_array_equal(a.deriv_exact, b.deriv_exact)
```

- [ ] **Step 2: Run to see them fail** — `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_corpus.py -v -k "deriv or default_spec"` → `ImportError` / `TypeError`.

- [ ] **Step 3: Implement.** In `parabolab/library.py`, after `merton_hjb`:

```python
def merton_hjb_derivatives(
    T: float = 0.1,
    mu: float = 0.03,
    sigma: float = 0.1,
    gamma: float = 0.5,
    rho: float = 0.01,
):
    """(u_x, u_xx) of merton_hjb's closed form, same argument convention as
    its exact_solution: u = x^{1-gamma} g(t) with
    g = base^gamma / (1 - gamma), base = (1 + (a-1) e^{-a(T-t)}) / a."""
    a = (2 * sigma**2 * gamma * rho - (1 - gamma) * mu**2) / (
        2 * sigma**2 * gamma**2
    )

    def _g(t: float) -> float:
        base = (1 + (a - 1) * math.exp(-a * (T - t))) / a
        return base**gamma / (1 - gamma)

    def _x(xv) -> float:
        return float(xv[0]) if hasattr(xv, "__len__") else float(xv)

    def ux(t: float, xv) -> float:
        return (1 - gamma) * _x(xv) ** (-gamma) * _g(t)

    def uxx(t: float, xv) -> float:
        return -gamma * (1 - gamma) * _x(xv) ** (-gamma - 1) * _g(t)

    return ux, uxx
```

In `parabolab/deep/corpus.py`:

```python
from ..mechanism import DxN

DERIV_CODES = {"Dx1": DxN((1,)), "Dx2": DxN((2,))}
```

`Family`: add field `deriv_factory_name: Optional[str] = None` (last field) and set `"merton_hjb_derivatives"` in `FAMILIES["merton"]` (pass it as the ninth positional argument or by keyword). `InstanceSpec`: add `deriv_codes: Tuple[str, ...] = ()` after `n_draws`. `Instance`: add
```python
    deriv: Optional[np.ndarray] = None          # (n_codes, N)
    deriv_stderr: Optional[np.ndarray] = None
    deriv_exact: Optional[np.ndarray] = None
```
and extend `finite`:
```python
    @property
    def finite(self) -> np.ndarray:
        ok = np.isfinite(self.y).all(axis=0) & np.isfinite(self.stderr).all(axis=0)
        if self.deriv is not None:
            ok &= np.isfinite(self.deriv).all(axis=0) & np.isfinite(self.deriv_stderr).all(axis=0)
        return ok
```
`generate_instance`: after the `y` draws,
```python
    deriv = deriv_se = deriv_exact = None
    if spec.deriv_codes:
        if fam.deriv_factory_name is None:
            raise ValueError(f"family {fam.key!r} has no exact derivatives")
        kwargs = dict(fam.fixed_kwargs); kwargs.update(zip(fam.param_names, spec.params))
        dfuns = getattr(library, fam.deriv_factory_name)(**kwargs)
        dvals, dses, dex = [], [], []
        for k, name in enumerate(spec.deriv_codes):
            data = generate_training_data(
                factory, n_states=spec.n_states, m_samples=spec.m_samples,
                seed=1000 * spec.seed + 100 + k, x_lo=fam.x_lo, x_hi=fam.x_hi,
                states=(ts, xs), code=DERIV_CODES[name], executor=executor,
                n_jobs=n_jobs)
            dvals.append(data.y); dses.append(data.stderr)
            fn = dfuns[k]
            dex.append(np.array([fn(0.0, xs[i]) for i in range(spec.n_states)]))
        deriv, deriv_se, deriv_exact = np.array(dvals), np.array(dses), np.array(dex)
```
and pass them to the `Instance(...)` constructor. `DERIV_CODES[name]` maps `"Dx1"` → `dfuns[0]` (u_x), `"Dx2"` → `dfuns[1]` (u_xx): index `dfuns` by `("Dx1", "Dx2").index(name)`, not by `k`, so the order of `deriv_codes` does not matter. `_save_instance`: add `deriv=..., deriv_stderr=..., deriv_exact=...` only when not `None`. `_load_instance`: read them with `f["deriv"] if "deriv" in f else None` (same for the other two).

- [ ] **Step 4: Run** — `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_corpus.py tests/test_deep_setnet.py -q` → all pass (the derivative-label test takes ~30 s: 2 codes × 40 states × 400 trees).

- [ ] **Step 5: Commit** — `git add parabolab/library.py parabolab/deep/corpus.py tests/test_deep_corpus.py` / `git commit -m "feat(deep): derivative labels (DxN roots) and closed-form Merton derivatives in the corpus"` + trailer.

---

### Task 2: `ConditionedNet` (`condnet.py`)

**Files:** Create `parabolab/deep/condnet.py`; modify `parabolab/deep/__init__.py`; test `tests/test_deep_condnet.py` (new).

**Interfaces — Produces:**
- `ConditionedNet(d, n_params, mode="concat", hidden_layers=6, neurons=64, param_mean=None, param_std=None)`; buffers `in_mean, in_std (d+1,)`, `out_mean, out_std ()`, `param_mean, param_std (n_params,)`; `forward(tx (B,d+1), params (B,P)) -> (B,)` in `y` units; `mode ∈ {"concat","film"}` else `ValueError`; `n_params_total`.
- `autograd_derivatives(fn, tx, *, create_graph=False) -> (u, u_x, u_xx)` — generic: `fn(tx) -> (B,)`, differentiates w.r.t. column 1 of `tx` (the first spatial coordinate); works for `DeepBranchNet` (`fn = net`) and `ConditionedNet` (`fn = lambda tx: net(tx, params)`).

- [ ] **Step 1: Failing tests** — create `tests/test_deep_condnet.py`:

```python
"""Tests for the parameter-conditioned net and its autograd derivatives."""

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from parabolab.deep.condnet import ConditionedNet, autograd_derivatives


def _inputs(B=7, d=1, P=3, seed=0):
    g = torch.Generator().manual_seed(seed)
    tx = torch.cat([torch.zeros(B, 1), 100 + 100 * torch.rand(B, d, generator=g)], -1)
    params = torch.rand(B, P, generator=g)
    return tx, params


@pytest.mark.parametrize("mode", ["concat", "film"])
def test_forward_shape_and_finite(mode):
    net = ConditionedNet(d=1, n_params=3, mode=mode, hidden_layers=2, neurons=8)
    tx, p = _inputs()
    out = net(tx, p)
    assert out.shape == (7,) and torch.isfinite(out).all()
    assert net.n_params_total > 0


def test_bad_mode_raises():
    with pytest.raises(ValueError):
        ConditionedNet(d=1, n_params=3, mode="hyper")


def test_film_head_is_zero_initialised_so_params_are_ignored_at_init():
    torch.manual_seed(0)
    net = ConditionedNet(d=1, n_params=3, mode="film", hidden_layers=3, neurons=8)
    tx, p = _inputs()
    a = net(tx, p)
    b = net(tx, torch.zeros_like(p))
    torch.testing.assert_close(a, b)


def test_concat_depends_on_params():
    torch.manual_seed(0)
    net = ConditionedNet(d=1, n_params=3, mode="concat", hidden_layers=3, neurons=8)
    tx, p = _inputs()
    assert not torch.allclose(net(tx, p), net(tx, torch.zeros_like(p)))


def test_scaler_buffers_exist_and_apply():
    net = ConditionedNet(d=1, n_params=2, hidden_layers=2, neurons=4,
                         param_mean=[0.5, 0.5], param_std=[0.25, 0.25])
    sd = net.state_dict()
    for key in ("in_mean", "in_std", "out_mean", "out_std", "param_mean", "param_std"):
        assert key in sd
    net.out_mean.fill_(3.0); net.out_std.fill_(2.0)
    tx, p = _inputs(P=2)
    a = net(tx, p)
    net.out_mean.fill_(0.0); net.out_std.fill_(1.0)
    b = net(tx, p)
    torch.testing.assert_close(a, 2 * b + 3)


@pytest.mark.parametrize("mode", ["concat", "film"])
def test_autograd_derivatives_match_finite_differences(mode):
    torch.manual_seed(1)
    net = ConditionedNet(d=1, n_params=3, mode=mode, hidden_layers=3, neurons=16).double()
    tx, p = _inputs()
    tx, p = tx.double(), p.double()
    fn = lambda z: net(z, p)
    u, ux, uxx = autograd_derivatives(fn, tx)
    assert u.shape == ux.shape == uxx.shape == (7,)
    h = 1e-3
    tp = tx.clone(); tp[:, 1] += h
    tm = tx.clone(); tm[:, 1] -= h
    with torch.no_grad():
        up, um, u0 = net(tp, p), net(tm, p), net(tx, p)
    torch.testing.assert_close(ux, (up - um) / (2 * h), rtol=1e-3, atol=1e-8)
    torch.testing.assert_close(uxx, (up - 2 * u0 + um) / h ** 2, rtol=1e-2, atol=1e-8)


def test_autograd_derivatives_create_graph_allows_backward():
    net = ConditionedNet(d=1, n_params=3, hidden_layers=2, neurons=8)
    tx, p = _inputs()
    _, ux, uxx = autograd_derivatives(lambda z: net(z, p), tx, create_graph=True)
    (ux.sum() + uxx.sum()).backward()
    assert any(q.grad is not None for q in net.parameters())
```

- [ ] **Step 2: Run to fail** — `... -m pytest tests/test_deep_condnet.py -v` → `ModuleNotFoundError`.

- [ ] **Step 3: Implement `condnet.py`:**

```python
"""Parameter-conditioned network u(t, x; theta) on the ablation's R5A trunk.

mode="concat": theta (scaled) is appended to the (t, x) input.
mode="film":   theta drives per-layer scale/shift of the trunk's hidden
               activations, h -> h * (1 + alpha_l) + beta_l, from a small MLP
               whose last layer is zero-initialised (so the net equals the
               plain trunk at initialisation).
Scalers (in_mean/in_std for (t, x), out_mean/out_std for u, param_mean/
param_std for theta) are buffers; condtrain.fit_conditioned_scalers fills
the first two from the pooled corpus.
"""

from __future__ import annotations

import torch
from torch import nn


def autograd_derivatives(fn, tx: torch.Tensor, *, create_graph: bool = False):
    """(u, u_x, u_xx) of fn(tx) w.r.t. column 1 of tx (first spatial coord)."""
    tx = tx.detach().requires_grad_(True)
    u = fn(tx)
    (g,) = torch.autograd.grad(u.sum(), tx, create_graph=True)
    ux = g[:, 1]
    (g2,) = torch.autograd.grad(ux.sum(), tx, create_graph=create_graph)
    uxx = g2[:, 1]
    if not create_graph:
        u, ux, uxx = u.detach(), ux.detach(), uxx.detach()
    return u, ux, uxx


class ConditionedNet(nn.Module):
    def __init__(self, d: int, n_params: int, mode: str = "concat",
                 hidden_layers: int = 6, neurons: int = 64,
                 param_mean=None, param_std=None) -> None:
        super().__init__()
        if mode not in ("concat", "film"):
            raise ValueError(f"mode must be 'concat' or 'film', got {mode!r}")
        self.d, self.n_params, self.mode = d, n_params, mode
        self.hidden_layers, self.neurons = hidden_layers, neurons
        self.register_buffer("in_mean", torch.zeros(d + 1))
        self.register_buffer("in_std", torch.ones(d + 1))
        self.register_buffer("out_mean", torch.zeros(()))
        self.register_buffer("out_std", torch.ones(()))
        pm = torch.zeros(n_params) if param_mean is None else torch.as_tensor(param_mean, dtype=torch.float32)
        ps = torch.ones(n_params) if param_std is None else torch.as_tensor(param_std, dtype=torch.float32)
        self.register_buffer("param_mean", pm)
        self.register_buffer("param_std", ps)
        in_dim = d + 1 + (n_params if mode == "concat" else 0)
        self.linears = nn.ModuleList(
            [nn.Linear(in_dim, neurons)]
            + [nn.Linear(neurons, neurons) for _ in range(hidden_layers - 1)]
            + [nn.Linear(neurons, 1)])
        self.act = nn.GELU()
        if mode == "film":
            self.film = nn.Sequential(nn.Linear(n_params, 64), nn.GELU(),
                                      nn.Linear(64, 2 * hidden_layers * neurons))
            nn.init.zeros_(self.film[-1].weight)
            nn.init.zeros_(self.film[-1].bias)

    @property
    def n_params_total(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def forward(self, tx: torch.Tensor, params: torch.Tensor) -> torch.Tensor:
        z = (tx - self.in_mean) / self.in_std
        p = (params - self.param_mean) / self.param_std
        y = torch.cat([z, p], dim=-1) if self.mode == "concat" else z
        ab = None
        if self.mode == "film":
            ab = self.film(p).view(-1, self.hidden_layers, 2, self.neurons)
        for idx, lin in enumerate(self.linears[:-1]):
            h = self.act(lin(y))
            if ab is not None:
                h = h * (1 + ab[:, idx, 0]) + ab[:, idx, 1]
            y = h if idx == 0 else h + y
        return self.linears[-1](y).squeeze(-1) * self.out_std + self.out_mean
```

Add `from . import condnet` + `"condnet"` to `__init__.py`.

- [ ] **Step 4: Run** — `... -m pytest tests/test_deep_condnet.py -v` → all pass.
- [ ] **Step 5: Commit** — `feat(deep): ConditionedNet (concat/FiLM) with autograd derivatives` + trailer.

---

### Task 3: Training, evaluation, referee, baseline (`condtrain.py`)

**Files:** Create `parabolab/deep/condtrain.py`; modify `__init__.py`; test `tests/test_deep_condnet.py`.

**Interfaces — Produces:**
- `pooled_rows(instances) -> dict` with `tx (R,d+1)`, `params (R,P)`, `u (R,)`, and `ux, uxx (R,)` when every instance has `deriv` (else absent); only finite rows.
- `fit_conditioned_scalers(net, rows) -> dict` fills `in_mean/in_std` (std floor 1e-12 → 1) and `out_mean/out_std` from `rows`; returns `{"ux_std": float, "uxx_std": float}` (pooled stds, 1.0 if absent).
- `CondTrainResult(net, losses, seconds)`.
- `train_conditioned(net, instances, *, steps=20000, batch_states=4096, lr=1e-3, loss_weights=(1.0, 0.0, 0.0), device="cpu", seed=0, log_every=100, verbose=False) -> CondTrainResult`; raises `ValueError` if a derivative weight is > 0 but the corpus has no derivative labels; `RuntimeError` on non-finite loss.
- `merton_policy_exact(params) -> float` = `mu / (gamma * sigma**2)` for `params = (gamma, mu, sigma)`.
- `policy_from_derivatives(ux, uxx, x, mu, sigma) -> np.ndarray` = `-(mu/sigma**2) * ux / (x * uxx)`.
- `evaluate_conditioned(net, instances, *, device="cpu") -> list[dict]` per instance: `l1_u`, `policy_err_interior`, `policy_err_full` (median relative error over grid points with \(x\in[110,190]\) / all).
- `per_instance_baseline(instance, *, device="cpu", seed=0, epochs=3000) -> dict` — same three metrics for the R5A `DeepBranchNet` trained on that instance's `y[0]`.

- [ ] **Step 1: Failing tests** — append to `tests/test_deep_condnet.py`:

```python
# ---------------------------------------------------------------------------
# training / evaluation / referee
# ---------------------------------------------------------------------------

from parabolab.deep import condtrain, corpus


def _toy(n=3, n_states=30, m=20, seed=31, deriv=False):
    specs = corpus.sample_instances("merton", n, seed, n_states=n_states, m_samples=m,
                                    n_draws=1)
    if deriv:
        import dataclasses
        specs = [dataclasses.replace(s, deriv_codes=("Dx1", "Dx2")) for s in specs]
    return [corpus.generate_instance(s, n_jobs=2) for s in specs]


def test_merton_policy_referee():
    assert condtrain.merton_policy_exact((0.5, 0.03, 0.1)) == pytest.approx(6.0)
    from parabolab.library import merton_hjb_derivatives
    ux, uxx = merton_hjb_derivatives(T=0.1, mu=0.03, sigma=0.1, gamma=0.5, rho=0.01)
    x = np.array([120.0, 150.0])
    pol = condtrain.policy_from_derivatives(
        np.array([ux(0.0, [v]) for v in x]), np.array([uxx(0.0, [v]) for v in x]),
        x, 0.03, 0.1)
    np.testing.assert_allclose(pol, 6.0, rtol=1e-12)


def test_pooled_rows_and_scalers():
    insts = _toy()
    rows = condtrain.pooled_rows(insts)
    assert rows["tx"].shape[1] == 2 and rows["params"].shape[1] == 3
    assert rows["u"].shape[0] == rows["tx"].shape[0] <= 90
    assert "ux" not in rows
    from parabolab.deep.condnet import ConditionedNet
    net = ConditionedNet(d=1, n_params=3, hidden_layers=2, neurons=8)
    stats = condtrain.fit_conditioned_scalers(net, rows)
    assert float(net.in_std[0]) == 1.0                # t == 0 has no spread
    assert float(net.in_mean[1]) == pytest.approx(rows["tx"][:, 1].mean())
    assert float(net.out_std) == pytest.approx(rows["u"].std())
    assert stats == {"ux_std": 1.0, "uxx_std": 1.0}


def test_train_conditioned_u_only_and_evaluate():
    insts = _toy()
    from parabolab.deep.condnet import ConditionedNet
    torch.manual_seed(0)
    net = ConditionedNet(d=1, n_params=3, hidden_layers=2, neurons=8)
    res = condtrain.train_conditioned(net, insts, steps=30, batch_states=32,
                                      log_every=10, lr=3e-3)
    assert np.isfinite(res.losses).all() and res.losses[-1] < res.losses[0]
    out = condtrain.evaluate_conditioned(net, insts)
    assert len(out) == 3
    for m in out:
        assert set(m) == {"l1_u", "policy_err_interior", "policy_err_full"}
        assert all(np.isfinite(v) for v in m.values())


def test_train_conditioned_with_derivative_labels():
    insts = _toy(n=2, n_states=20, m=10, seed=32, deriv=True)
    rows = condtrain.pooled_rows(insts)
    assert "ux" in rows and "uxx" in rows
    from parabolab.deep.condnet import ConditionedNet
    net = ConditionedNet(d=1, n_params=3, hidden_layers=2, neurons=8)
    res = condtrain.train_conditioned(net, insts, steps=5, batch_states=16,
                                      loss_weights=(1.0, 1.0, 1.0))
    assert np.isfinite(res.losses).all()
    with pytest.raises(ValueError):
        condtrain.train_conditioned(net, _toy(n=1), steps=1,
                                    loss_weights=(1.0, 1.0, 0.0))


def test_per_instance_baseline_metrics():
    inst = _toy(n=1, n_states=60, m=20, seed=33)[0]
    m = condtrain.per_instance_baseline(inst, epochs=50)
    assert set(m) == {"l1_u", "policy_err_interior", "policy_err_full"}
    assert np.isfinite(m["l1_u"])
```

- [ ] **Step 2: Run to fail** → `ImportError: condtrain`.

- [ ] **Step 3: Implement `condtrain.py`:**

```python
"""Pooled training, evaluation and the closed-form policy referee for the
parameter-conditioned Merton net (spec 2026-09-15-parametric-merton-net)."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, List, Sequence

import numpy as np
import torch

from . import corpus
from .ablation import build_net
from .condnet import ConditionedNet, autograd_derivatives
from .settrain import R5A, _as_training_data
from .solver import _grid_inputs, train_deep_branching

INTERIOR = (110.0, 190.0)


def pooled_rows(instances: Sequence[corpus.Instance]) -> Dict[str, np.ndarray]:
    tx, params, u, ux, uxx = [], [], [], [], []
    has_deriv = all(inst.deriv is not None for inst in instances)
    for inst in instances:
        ok = inst.finite
        tx.append(np.column_stack([inst.t, inst.x])[ok])
        params.append(np.tile(np.asarray(inst.spec.params, dtype=float), (ok.sum(), 1)))
        u.append(inst.y[0, ok])
        if has_deriv:
            ux.append(inst.deriv[0, ok]); uxx.append(inst.deriv[1, ok])
    rows = {"tx": np.concatenate(tx), "params": np.concatenate(params),
            "u": np.concatenate(u)}
    if has_deriv:
        rows["ux"], rows["uxx"] = np.concatenate(ux), np.concatenate(uxx)
    return rows


def fit_conditioned_scalers(net: ConditionedNet, rows) -> Dict[str, float]:
    with torch.no_grad():
        mean, std = rows["tx"].mean(0), rows["tx"].std(0)
        std[std < 1e-12] = 1.0
        net.in_mean.copy_(torch.as_tensor(mean, dtype=torch.float32))
        net.in_std.copy_(torch.as_tensor(std, dtype=torch.float32))
        net.out_mean.fill_(float(rows["u"].mean()))
        s = float(rows["u"].std()); net.out_std.fill_(s if s > 1e-12 else 1.0)
    return {"ux_std": float(rows["ux"].std()) if "ux" in rows else 1.0,
            "uxx_std": float(rows["uxx"].std()) if "uxx" in rows else 1.0}


@dataclass
class CondTrainResult:
    net: ConditionedNet
    losses: np.ndarray
    seconds: float


def train_conditioned(net, instances, *, steps=20_000, batch_states=4096,
                      lr=1e-3, loss_weights=(1.0, 0.0, 0.0), device="cpu",
                      seed=0, log_every=100, verbose=False) -> CondTrainResult:
    w_u, w1, w2 = loss_weights
    rows = pooled_rows(instances)
    if (w1 > 0 or w2 > 0) and "ux" not in rows:
        raise ValueError("derivative loss weights need a corpus with deriv_codes")
    stats = fit_conditioned_scalers(net, rows)
    net = net.to(device).train()
    T = {k: torch.as_tensor(v, dtype=torch.float32, device=device) for k, v in rows.items()}
    out_std = net.out_std.clone()
    rng = np.random.default_rng(seed); torch.manual_seed(seed)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=steps)
    R = len(rows["u"]); losses, start = [], time.perf_counter()
    for step in range(steps):
        idx = torch.as_tensor(rng.integers(0, R, size=min(batch_states, R)), device=device)
        tx, p = T["tx"][idx], T["params"][idx]
        if w1 > 0 or w2 > 0:
            u, ux, uxx = autograd_derivatives(lambda z: net(z, p), tx, create_graph=True)
            loss = w_u * torch.mean(((u - T["u"][idx]) / out_std) ** 2)
            loss = loss + w1 * torch.mean(((ux - T["ux"][idx]) / stats["ux_std"]) ** 2)
            loss = loss + w2 * torch.mean(((uxx - T["uxx"][idx]) / stats["uxx_std"]) ** 2)
        else:
            loss = w_u * torch.mean(((net(tx, p) - T["u"][idx]) / out_std) ** 2)
        if not torch.isfinite(loss):
            raise RuntimeError(f"non-finite loss at step {step}")
        opt.zero_grad(); loss.backward(); opt.step(); sched.step()
        if step % log_every == 0 or step == steps - 1:
            losses.append(float(loss.detach()))
            if verbose:
                print(f"  step {step}: loss {losses[-1]:.4e}", flush=True)
    net.eval()
    return CondTrainResult(net, np.array(losses), time.perf_counter() - start)


def merton_policy_exact(params) -> float:
    gamma, mu, sigma = params[:3]
    return mu / (gamma * sigma**2)


def policy_from_derivatives(ux, uxx, x, mu, sigma):
    return -(mu / sigma**2) * np.asarray(ux) / (np.asarray(x) * np.asarray(uxx))


def _policy_metrics(fn, inst: corpus.Instance, device: str) -> Dict[str, float]:
    fam = corpus.FAMILIES[inst.spec.family]
    grid, xg, tx = _grid_inputs(fam.d, 0.0, fam.x_lo, fam.x_hi)
    txt = torch.as_tensor(tx, dtype=torch.float32, device=device)
    u, ux, uxx = autograd_derivatives(fn, txt)
    u, ux, uxx = (v.cpu().numpy() for v in (u, ux, uxx))
    gamma, mu, sigma = inst.spec.params[:3]
    pol = policy_from_derivatives(ux, uxx, grid, mu, sigma)
    rel = np.abs(pol - merton_policy_exact(inst.spec.params)) / merton_policy_exact(inst.spec.params)
    interior = (grid >= INTERIOR[0]) & (grid <= INTERIOR[1])
    l1 = float(np.mean(np.abs(u - inst.u_grid)))
    f = lambda v: float(v) if np.isfinite(v) else float("inf")
    return {"l1_u": f(l1), "policy_err_interior": f(np.median(rel[interior])),
            "policy_err_full": f(np.median(rel))}


def evaluate_conditioned(net: ConditionedNet, instances, *, device="cpu") -> List[Dict[str, float]]:
    net = net.to(device).eval()
    out = []
    for inst in instances:
        p = torch.as_tensor(np.asarray(inst.spec.params, dtype=np.float32), device=device)
        fn = lambda z, p=p: net(z, p.expand(z.shape[0], -1))
        out.append(_policy_metrics(fn, inst, device))
    return out


def per_instance_baseline(inst: corpus.Instance, *, device="cpu", seed=0,
                          epochs=3000) -> Dict[str, float]:
    fam = corpus.FAMILIES[inst.spec.family]
    net = build_net(R5A, d=fam.d, seed=seed)
    train_deep_branching(net, _as_training_data(inst, 0), epochs=epochs, device=device)
    net.eval()
    return _policy_metrics(net, inst, device)
```

Add `from . import condtrain` + `"condtrain"` to `__init__.py`.

- [ ] **Step 4: Run** — `... -m pytest tests/test_deep_condnet.py -q` → all pass (~40 s: derivative toy corpus).
- [ ] **Step 5: Commit** — `feat(deep): conditioned-net training, policy referee, per-instance baseline` + trailer.

---

### Task 4: Driver

**Files:** Create `examples/parametric_merton.py`; modify `.gitignore` (`!examples/parametric_merton.csv`); test `tests/test_deep_condnet.py`.

- [ ] **Step 1: Failing test** — append:

```python
# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------

import csv
import subprocess
import sys
from pathlib import Path


def test_parametric_merton_driver_tiny(tmp_path):
    script = Path(__file__).resolve().parents[1] / "examples" / "parametric_merton.py"
    out = tmp_path / "res.csv"
    subprocess.run([sys.executable, str(script), "--tiny", "--jobs", "1",
                    "--corpus-root", str(tmp_path / "corpus"), "--out", str(out)],
                   check=True, capture_output=True, text=True)
    rows = list(csv.DictReader(out.open()))
    assert {r["rung"] for r in rows} == {"C0", "C1", "C2", "C3"}
    assert all(float(r["l1_u"]) >= 0 for r in rows)
```

- [ ] **Step 2: Run to fail** → `CalledProcessError`.

- [ ] **Step 3: Implement `examples/parametric_merton.py`:**

```python
"""D02: one net for the Merton family (t, x, theta) -> u, policies by autograd.

    python examples/parametric_merton.py --rungs C0 C1 C2 C3 --steps 20000 \
        --device cuda --jobs 16

Rungs: C0 per-instance R5A baseline; C1 concat conditioning; C2 FiLM;
C3 best of C1/C2 (--c3-mode) plus derivative labels (weights 1, 1).
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
    p.add_argument("--rungs", nargs="*", default=["C0", "C1", "C2", "C3"])
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

    def run_cond(rung, mode, instances, weights):
        import torch
        torch.manual_seed(a.seed)
        net = ConditionedNet(d=fam.d, n_params=len(fam.ranges), mode=mode,
                             param_mean=p_mean, param_std=p_std)
        print(f"{rung}: {mode}, weights {weights}, {net.n_params_total} params", flush=True)
        res = condtrain.train_conditioned(net, instances, steps=a.steps,
                                          batch_states=a.batch_states, loss_weights=weights,
                                          device=a.device, seed=a.seed, verbose=True)
        record(rung, condtrain.evaluate_conditioned(net, test, device=a.device),
               res.seconds / len(test))

    if "C1" in a.rungs: run_cond("C1", "concat", train, (1.0, 0.0, 0.0))
    if "C2" in a.rungs: run_cond("C2", "film", train, (1.0, 0.0, 0.0))
    if "C3" in a.rungs:
        dspecs = [dataclasses.replace(s, deriv_codes=("Dx1", "Dx2")) for s in train_specs]
        dtrain = corpus.load_or_generate_corpus(dspecs, root / "deriv", n_jobs=a.jobs, verbose=True, min_finite=mf)
        run_cond("C3", a.c3_mode, dtrain, (1.0, 1.0, 1.0))

    write_rows(a.out, rows)
    print("\n| rung | n | u-L1 median | u-L1 max | policy err interior (median) | policy err full | s/instance |")
    print("|---|---|---|---|---|---|---|")
    for rung in ("C0", "C1", "C2", "C3"):
        rr = [r for r in rows if r["rung"] == rung]
        if not rr:
            continue
        l1 = np.array([r["l1_u"] for r in rr]); pi = np.array([r["policy_err_interior"] for r in rr])
        pf = np.array([r["policy_err_full"] for r in rr]); s = np.mean([r["seconds"] for r in rr])
        print(f"| {rung} | {len(rr)} | {np.median(l1):.2e} | {l1.max():.2e} | "
              f"{100*np.median(pi):.2f} % | {100*np.median(pf):.2f} % | {s:.1f} |")


if __name__ == "__main__":
    main(parse_args())
```

- [ ] **Step 4: Run** — driver test then `... -m pytest -q` (full fast suite, zero failures).
- [ ] **Step 5: Commit** — `feat: parametric Merton driver (C0-C3)` + trailer, with `.gitignore`.

---

### Task 5: Run C0–C2, decide C3's mode, run C3, record

- [ ] **Step 1:** `conda run -n parabolab --no-capture-output python -u examples/parametric_merton.py --rungs C0 C1 C2 --steps 20000 --device cuda --jobs 16` (corpus ≈ 5 min; C0 ≈ 50 × 8 s; C1/C2 minutes each on GPU).
- [ ] **Step 2:** pick `--c3-mode` = the better of C1/C2 by the kept-rung rule; `... --rungs C3 --c3-mode <mode> --steps 20000 --device cuda --jobs 16` (derivative corpus ≈ 10 min: two extra codes).
- [ ] **Step 3:** append `## Results` to the spec: the printed table, the kept rung, the success/failure verdict against the fixed criteria, one paragraph per rung (C0: what per-instance autograd policies look like; C1 vs C2; C3 effect of derivative labels), and cost. Add a CLAUDE.md gotcha if anything non-obvious.
- [ ] **Step 4:** commit `exp: parametric Merton net C0-C3 -- <verdict>` + trailer with the CSV and docs.
