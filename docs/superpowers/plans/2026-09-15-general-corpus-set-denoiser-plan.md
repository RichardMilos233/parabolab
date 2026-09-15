# General Corpus + Set-to-Field Denoiser Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a multi-instance training corpus on top of the coding-tree sampler (Stage 0) and run the D04 go/no-go: does a transformer over a *set* of noisy estimates, trained across instances with Noise2Noise targets, beat a per-instance MLP on held-out instances?

**Architecture:** Two small hooks in existing code (`allen_cahn_nd(shift=)`, `generate_training_data(states=)`), then three new units under `parabolab/deep/`: `corpus.py` (families, instance specs, generation, on-disk cache, batch collation), `setnet.py` (the `SetDenoiser` transformer with per-instance scaling inside the model), `settrain.py` (training loop, grid evaluation, the two baselines). One driver `examples/set_denoiser_gonogo.py`. The ablation harness on this branch (`deep.ablation.build_net`, `deep.solver.train_deep_branching`, `grid_errors`) supplies the per-instance MLP baseline unchanged.

**Tech Stack:** Python 3.11, numpy, torch 2.13 (CUDA wheel installed in Task 5), pytest. Conda env `parabolab`; run everything as `conda run -n parabolab --no-capture-output python ...` (PowerShell; plain `python`/`conda` may be missing from the Git-Bash PATH).

## Global Constraints

- Spec: `docs/superpowers/specs/2026-09-15-general-corpus-set-denoiser-design.md`. Branch: `research/nn-architecture` (continue on it; do not merge).
- Default behaviour of every existing function stays byte-identical: `allen_cahn_nd(d, T)` with the default `shift=0.0` must produce the same `name`, `phi_expr` and `exact_solution` values; `generate_training_data` with `states=None` must draw the same `y` as before for the same seed. Existing tests (`tests/test_deep.py`, `tests/test_deep_ablation.py`, `tests/test_library.py`) stay green.
- Families and ranges (verbatim): `ac1` = `allen_cahn_nd(d=1, T, shift)`, \(T \in [0.1, 0.5]\), shift \(\in [-3, 3]\), segment \([-8, 8]\); `merton` = `merton_hjb(T=0.1, mu, sigma, gamma, rho=0.01)`, \(\gamma \in [0.3, 0.8]\), \(\mu \in [0.02, 0.06]\), \(\sigma \in [0.08, 0.2]\), segment \([100, 200]\). States uniform on the 10 %-overtrained segment, \(\tau \equiv 0\), jcp rate, two independent draws at the same states.
- Per-instance scaling lives **inside** `SetDenoiser` (context mean/std of `y` and of `(t,x)`); `stderr` is never a loss weight.
- Go/no-go rule (fixed before running): D04-n2n median held-out grid L1 **<** per-instance MLP at \(M\) median. Pass → Stage 1; fail → D04 stops.
- Scripts that start worker pools run under `if __name__ == "__main__":` (gotcha 37).
- Corpus files are git-ignored (`examples/nn_corpus/`); the results CSV is un-ignored explicitly (`.gitignore` already has `examples/*.csv`; add `!examples/set_denoiser_gonogo.csv`).
- Commit after every task; commit messages end with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.

---

## File structure

| File | Responsibility |
|---|---|
| `parabolab/library.py` (modify `allen_cahn_nd`) | translated Allen–Cahn wave |
| `parabolab/deep/generator.py` (modify `generate_training_data`) | `states=` hook |
| `parabolab/deep/corpus.py` (new) | `Family`, `FAMILIES`, `InstanceSpec`, `sample_instances`, `Instance`, `generate_instance`, `instance_path`, `load_or_generate_corpus`, `collate` |
| `parabolab/deep/setnet.py` (new) | `SetDenoiser` |
| `parabolab/deep/settrain.py` (new) | `train_set_denoiser`, `evaluate_set_denoiser`, `per_instance_mlp_l1`, `kernel_smoother_l1`, `SetTrainResult` |
| `parabolab/deep/__init__.py` (modify) | export `corpus`, `setnet`, `settrain` |
| `examples/set_denoiser_gonogo.py` (new) | the experiment |
| `tests/test_deep_corpus.py`, `tests/test_deep_setnet.py` (new) | fast tests |
| `.gitignore` (modify) | `examples/nn_corpus/`, `!examples/set_denoiser_gonogo.csv` |
| spec `## Results` section; `CLAUDE.md` gotchas | write-up |

---

### Task 1: Library and generator hooks

**Files:**
- Modify: `parabolab/library.py:232-268` (`allen_cahn_nd`)
- Modify: `parabolab/deep/generator.py:81-140` (`generate_training_data`)
- Test: `tests/test_deep_corpus.py` (new file)

**Interfaces:**
- Produces: `allen_cahn_nd(d: int, T: float = 0.5, shift: float = 0.0) -> FullyNonlinearPDEnD` with exact solution \(u(t,x) = -\tfrac12 - \tfrac12\tanh(\tfrac34(T-t) - (\text{inv}\sum x_i - \text{shift}))\), \(\text{inv} = 0.5/\sqrt d\); `name` unchanged when `shift == 0.0`, else `f"allen_cahn_nd(d={d}, T={T}, shift={shift})"`.
- Produces: `generate_training_data(..., states: Optional[Tuple[np.ndarray, np.ndarray]] = None)` — when given `(ts, xs)` with shapes `(N,)` and `(N, d)`, those states are used and `n_states` is ignored; tree seeds still come from `seed`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_deep_corpus.py`:

```python
"""Tests for the multi-instance corpus (Stage 0) and its library hooks."""

import functools

import numpy as np
import pytest

torch = pytest.importorskip("torch")

import parabolab.deep as deep
from parabolab.library import allen_cahn_nd


# ---------------------------------------------------------------------------
# library hook: translated Allen-Cahn wave
# ---------------------------------------------------------------------------

def test_allen_cahn_shift_zero_is_unchanged():
    old = allen_cahn_nd(d=1, T=0.4)
    new = allen_cahn_nd(d=1, T=0.4, shift=0.0)
    assert new.name == old.name == "allen_cahn_nd(d=1, T=0.4)"
    assert new.phi_expr == old.phi_expr
    for x in (-3.0, 0.0, 2.5):
        assert new.exact_solution(0.1, np.array([x])) == old.exact_solution(0.1, np.array([x]))


def test_allen_cahn_shift_is_a_translation():
    base = allen_cahn_nd(d=1, T=0.3)
    moved = allen_cahn_nd(d=1, T=0.3, shift=1.5)
    assert moved.name == "allen_cahn_nd(d=1, T=0.3, shift=1.5)"
    for t in (0.0, 0.2):
        for x in (-2.0, 0.7, 4.0):
            # inv = 0.5 for d = 1, so shift s moves the wave by 2 s in x
            assert moved.exact_solution(t, np.array([x])) == pytest.approx(
                base.exact_solution(t, np.array([x - 3.0])), abs=1e-12)
    # terminal condition matches the exact solution at T
    phi = moved.phi_mu((0,))(0.7)          # numeric phi(x) on a FullyNonlinearPDEnD
    assert float(phi) == pytest.approx(moved.exact_solution(0.3, np.array([0.7])), abs=1e-9)


# ---------------------------------------------------------------------------
# generator hook: fixed states
# ---------------------------------------------------------------------------

AC1 = functools.partial(allen_cahn_nd, d=1, T=0.5)


def test_generator_states_hook_reproduces_default_draw():
    kw = dict(n_states=6, m_samples=20, x_lo=-2.0, x_hi=2.0)
    default = deep.generate_training_data(AC1, seed=3, **kw)
    fixed = deep.generate_training_data(
        AC1, seed=3, states=(default.t, default.x), **kw)
    np.testing.assert_array_equal(fixed.x, default.x)
    np.testing.assert_array_equal(fixed.y, default.y)
    other = deep.generate_training_data(
        AC1, seed=4, states=(default.t, default.x), **kw)
    np.testing.assert_array_equal(other.x, default.x)
    assert not np.array_equal(other.y, default.y)


def test_generator_states_hook_validates_shapes():
    with pytest.raises(ValueError):
        deep.generate_training_data(
            AC1, n_states=3, m_samples=2, x_lo=-1.0, x_hi=1.0,
            states=(np.zeros(3), np.zeros((4, 1))))
```

(`FullyNonlinearPDEnD.phi_mu(mu)` returns the lambdified \(\partial^\mu\phi\); `mu = (0,)` is \(\phi\) itself, called with the scalar coordinates.)

- [ ] **Step 2: Run tests to verify they fail**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_corpus.py -v`
Expected: all four FAIL with `TypeError: ... unexpected keyword argument` (`shift` for the first two, `states` for the last two).

- [ ] **Step 3: Implement the two hooks**

In `parabolab/library.py`, change the signature and body of `allen_cahn_nd`:

```python
def allen_cahn_nd(d: int, T: float = 0.5, shift: float = 0.0) -> FullyNonlinearPDEnD:
    """Allen-Cahn traveling wave in d dimensions, JEQ2023 eqs. (5.2)-(5.3):

        du/dt + (1/2) Lap u + u - u^3 = 0,
        u(t, x) = -1/2 - (1/2) tanh( (3/4)(T-t) - (sum_i x_i / (2 sqrt d) - shift) ).

    ``shift`` translates the wave (the PDE is translation invariant); the
    default 0 is the paper's wave.  Used by deep.corpus to build a family of
    instances with different fronts.

    (rest of the original docstring unchanged)
    """
    import sympy as sp

    z = z_symbols(0)
    xs = x_symbols(d)
    inv = 0.5 / math.sqrt(d)

    def exact(t: float, xv) -> float:
        return -0.5 - 0.5 * math.tanh(
            0.75 * (T - t) - (inv * float(sum(xv)) - shift)
        )

    name = (f"allen_cahn_nd(d={d}, T={T})" if shift == 0.0
            else f"allen_cahn_nd(d={d}, T={T}, shift={shift})")
    return FullyNonlinearPDEnD(
        T=T, d=d, deriv_map=((0,) * d,),
        f_expr=z[0] - z[0] ** 3,
        phi_expr=-1 + 1 / (1 + sp.exp(-2 * (inv * sum(xs) - shift))),
        exact_solution=exact,
        name=name,
    )
```

For `shift == 0.0` the expression `-2 * (inv * sum(xs) - 0.0)` must simplify to the old `-2 * inv * sum(xs)`; if the sympy `==` comparison in the first test fails because of the extra `- 0.0`, build `phi_expr` as `-1 + 1 / (1 + sp.exp(-2 * inv * sum(xs)))` when `shift == 0.0` and the shifted form otherwise (write it as an `if`, not a subtraction of zero).

In `parabolab/deep/generator.py`, add the keyword to `generate_training_data` (after `executor`):

```python
    states: Optional[tuple] = None,
```

and replace the state-drawing block

```python
    rng = np.random.default_rng(seed)
    t_lo, t_hi = t_range
    ts = rng.uniform(t_lo, t_hi, size=n_states) if t_hi > t_lo \
        else np.full(n_states, float(t_lo))
    margin = overtrain_rate * (x_hi - x_lo)
    x_mid = 0.5 * (x_lo + x_hi)
    xs = np.full((n_states, d), x_mid)
    xs[:, 0] = rng.uniform(x_lo - margin, x_hi + margin, size=n_states)
```

with

```python
    if states is None:
        rng = np.random.default_rng(seed)
        t_lo, t_hi = t_range
        ts = rng.uniform(t_lo, t_hi, size=n_states) if t_hi > t_lo \
            else np.full(n_states, float(t_lo))
        margin = overtrain_rate * (x_hi - x_lo)
        x_mid = 0.5 * (x_lo + x_hi)
        xs = np.full((n_states, d), x_mid)
        xs[:, 0] = rng.uniform(x_lo - margin, x_hi + margin, size=n_states)
    else:
        ts, xs = states
        ts = np.asarray(ts, dtype=float)
        xs = np.asarray(xs, dtype=float)
        if ts.ndim != 1 or xs.ndim != 2 or xs.shape[0] != ts.shape[0] \
                or xs.shape[1] != d:
            raise ValueError(
                f"states must be (ts (N,), xs (N, {d})); got "
                f"{ts.shape} and {xs.shape}")
        n_states = len(ts)
```

Add to the docstring: "``states=(ts, xs)`` skips the state draw and uses the given states (tree seeds still derive from ``seed``); ``n_states`` is then ignored."

- [ ] **Step 4: Run tests to verify they pass**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_corpus.py tests/test_deep.py tests/test_deep_ablation.py tests/test_library.py -q`
Expected: all PASS (the ablation's `test_default_training_is_unchanged` and `tests/test_deep.py::test_generator_independent_of_n_jobs` guard the default path).

- [ ] **Step 5: Commit**

```bash
git add parabolab/library.py parabolab/deep/generator.py tests/test_deep_corpus.py
git commit -m "feat: allen_cahn_nd(shift=) and generate_training_data(states=) hooks for the corpus

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 2: Corpus (`corpus.py`)

**Files:**
- Create: `parabolab/deep/corpus.py`
- Modify: `parabolab/deep/__init__.py`, `.gitignore`
- Test: `tests/test_deep_corpus.py`

**Interfaces:**
- Consumes: Task 1 hooks; `parabolab.deep.generator.generate_training_data`; `parabolab.deep.solver._grid_inputs(d, t_val, x_lo, x_hi, n_grid=101)`; `parabolab.tree.jcp_rate`.
- Produces:
  - `Family(key, param_names: tuple[str,...], ranges: tuple[tuple[float,float],...], x_lo, x_hi, d, factory_name, fixed_kwargs: tuple[tuple[str, float],...])` with `.make_factory(params) -> functools.partial`.
  - `FAMILIES: dict[str, Family]` keys `ac1`, `merton`.
  - `InstanceSpec(family: str, params: tuple[float,...], n_states: int, m_samples: int, seed: int, n_draws: int = 2)` frozen; `.to_json()`.
  - `sample_instances(family: str, n: int, seed: int, *, n_states, m_samples, n_draws=2) -> list[InstanceSpec]` (instance `seed = 1_000_000 * seed + i`).
  - `Instance` dataclass: `spec, t (N,), x (N,d), y (n_draws,N), stderr (n_draws,N), u_exact (N,), grid (101,), u_grid (101,), rate: float`; property `finite -> np.ndarray bool (N,)` (all draws finite in `y` and `stderr`).
  - `generate_instance(spec, *, executor=None, n_jobs=1) -> Instance`.
  - `instance_path(spec, root) -> Path` = `root/spec.family/f"{spec.seed}.npz"`.
  - `load_or_generate_corpus(specs, root, *, n_jobs=1, verbose=False, min_finite=50) -> list[Instance]` (skips and prints instances with fewer than `min_finite` finite rows).
  - `collate(instances, *, n_context, n_query, rng) -> dict[str, np.ndarray]` with keys `ctx_tx (B,Nc,d+1)`, `ctx_y (B,Nc)`, `ctx_se (B,Nc)`, `params (B,P)`, `q_tx (B,Q,d+1)`, `q_y (B,Q)` (draw-1 `y` at the query states), `q_u (B,Q)` (exact).

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_deep_corpus.py`:

```python
# ---------------------------------------------------------------------------
# corpus
# ---------------------------------------------------------------------------

import dataclasses
import json

from parabolab.deep import corpus


def test_families_build_picklable_factories():
    import pickle
    for key, fam in corpus.FAMILIES.items():
        assert fam.key == key
        params = tuple(0.5 * (lo + hi) for lo, hi in fam.ranges)
        factory = fam.make_factory(params)
        pickle.dumps(factory)
        pde = factory()
        assert pde.exact_solution is not None and pde.d == fam.d


def test_sample_instances_is_deterministic_and_in_range():
    a = corpus.sample_instances("merton", 5, seed=2, n_states=8, m_samples=4)
    b = corpus.sample_instances("merton", 5, seed=2, n_states=8, m_samples=4)
    assert a == b
    assert [s.seed for s in a] == [2_000_000 + i for i in range(5)]
    fam = corpus.FAMILIES["merton"]
    for s in a:
        assert s.family == "merton" and s.n_draws == 2
        for p, (lo, hi) in zip(s.params, fam.ranges):
            assert lo <= p <= hi
    assert json.loads(a[0].to_json())["params"] == list(a[0].params)


def _tiny_spec(seed=7, m=4, n=8, n_draws=2):
    return corpus.InstanceSpec("ac1", (0.3, 0.5), n, m, seed, n_draws)


def test_generate_instance_shapes_and_two_independent_draws():
    inst = corpus.generate_instance(_tiny_spec())
    assert inst.t.shape == (8,) and inst.x.shape == (8, 1)
    assert inst.y.shape == (2, 8) and inst.stderr.shape == (2, 8)
    assert inst.u_exact.shape == (8,) and inst.grid.shape == (101,) \
        and inst.u_grid.shape == (101,)
    assert not np.array_equal(inst.y[0], inst.y[1])      # independent draws
    assert inst.grid[0] == -8.0 and inst.grid[-1] == 8.0
    pde = corpus.FAMILIES["ac1"].make_factory((0.3, 0.5))()
    assert inst.u_grid[50] == pytest.approx(pde.exact_solution(0.0, np.array([0.0])))
    assert inst.finite.sum() == 8
    assert inst.rate > 0


def test_corpus_roundtrip_and_mismatch(tmp_path):
    specs = [_tiny_spec(seed=1), _tiny_spec(seed=2)]
    a = corpus.load_or_generate_corpus(specs, tmp_path)
    assert corpus.instance_path(specs[0], tmp_path).exists()
    b = corpus.load_or_generate_corpus(specs, tmp_path)
    for ia, ib in zip(a, b):
        np.testing.assert_array_equal(ia.y, ib.y)
        np.testing.assert_array_equal(ia.u_grid, ib.u_grid)
        assert ia.spec == ib.spec and ia.rate == ib.rate
    bad = dataclasses.replace(specs[0], m_samples=5)   # same seed -> same file
    with pytest.raises(ValueError, match="spec"):
        corpus.load_or_generate_corpus([bad], tmp_path)


def test_corpus_skips_instances_with_too_few_finite_rows(tmp_path, capsys):
    inst = corpus.generate_instance(_tiny_spec(seed=3))
    inst.y[0, :6] = np.nan
    path = corpus.instance_path(inst.spec, tmp_path)
    path.parent.mkdir(parents=True)
    corpus._save_instance(inst, path)
    out = corpus.load_or_generate_corpus([inst.spec], tmp_path, min_finite=5)
    assert out == []
    assert "finite" in capsys.readouterr().out


def test_collate_shapes_and_nan_masking():
    inst = corpus.generate_instance(_tiny_spec(seed=4))
    inst.y[1, 2] = np.nan
    rng = np.random.default_rng(0)
    batch = corpus.collate([inst, inst], n_context=5, n_query=3, rng=rng)
    assert batch["ctx_tx"].shape == (2, 5, 2) and batch["ctx_y"].shape == (2, 5)
    assert batch["ctx_se"].shape == (2, 5) and batch["params"].shape == (2, 2)
    assert batch["q_tx"].shape == (2, 3, 2) and batch["q_y"].shape == (2, 3) \
        and batch["q_u"].shape == (2, 3)
    for key in ("ctx_tx", "ctx_y", "ctx_se", "q_tx", "q_y", "q_u"):
        assert np.isfinite(batch[key]).all()
    assert batch["params"][0].tolist() == [0.3, 0.5]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_corpus.py -v -k "families or sample_instances or generate_instance or corpus or collate"`
Expected: FAIL with `ImportError: cannot import name 'corpus'`.

- [ ] **Step 3: Implement `corpus.py`**

```python
"""Multi-instance training corpora on top of the coding-tree sampler.

An *instance* is one PDE from a parametrised family (its parameters are
its identity) together with the sampler's noisy point estimates at N
states, drawn ``n_draws`` times independently at the SAME states: draw 0
is what a model sees, draw 1 is a Noise2Noise target.  The exact solution
is stored for evaluation only.  The ablation's single-PDE datasets
(deep.datasets) are the one-instance, one-draw special case.
"""

from __future__ import annotations

import dataclasses
import functools
import json
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from .. import library
from .generator import generate_training_data
from .solver import _grid_inputs


@dataclass(frozen=True)
class Family:
    key: str
    param_names: Tuple[str, ...]
    ranges: Tuple[Tuple[float, float], ...]
    x_lo: float
    x_hi: float
    d: int
    factory_name: str
    fixed_kwargs: Tuple[Tuple[str, float], ...]

    def make_factory(self, params: Sequence[float]) -> functools.partial:
        kwargs = dict(self.fixed_kwargs)
        kwargs.update(zip(self.param_names, (float(p) for p in params)))
        return functools.partial(getattr(library, self.factory_name), **kwargs)


FAMILIES: Dict[str, Family] = {
    "ac1": Family("ac1", ("T", "shift"), ((0.1, 0.5), (-3.0, 3.0)),
                  -8.0, 8.0, 1, "allen_cahn_nd", (("d", 1),)),
    "merton": Family("merton", ("gamma", "mu", "sigma"),
                     ((0.3, 0.8), (0.02, 0.06), (0.08, 0.2)),
                     100.0, 200.0, 1, "merton_hjb",
                     (("T", 0.1), ("rho", 0.01))),
}


@dataclass(frozen=True)
class InstanceSpec:
    family: str
    params: Tuple[float, ...]
    n_states: int
    m_samples: int
    seed: int
    n_draws: int = 2

    def to_json(self) -> str:
        return json.dumps(dataclasses.asdict(self), sort_keys=True)


def sample_instances(family: str, n: int, seed: int, *, n_states: int,
                     m_samples: int, n_draws: int = 2) -> List[InstanceSpec]:
    fam = FAMILIES[family]
    rng = np.random.default_rng(seed)
    specs = []
    for i in range(n):
        params = tuple(float(rng.uniform(lo, hi)) for lo, hi in fam.ranges)
        specs.append(InstanceSpec(family, params, n_states, m_samples,
                                  1_000_000 * seed + i, n_draws))
    return specs


@dataclass
class Instance:
    spec: InstanceSpec
    t: np.ndarray          # (N,)
    x: np.ndarray          # (N, d)
    y: np.ndarray          # (n_draws, N)
    stderr: np.ndarray     # (n_draws, N)
    u_exact: np.ndarray    # (N,)
    grid: np.ndarray       # (101,)
    u_grid: np.ndarray     # (101,)
    rate: float

    @property
    def finite(self) -> np.ndarray:
        return np.isfinite(self.y).all(axis=0) & np.isfinite(self.stderr).all(axis=0)


def _draw_states(spec: InstanceSpec, fam: Family):
    rng = np.random.default_rng(spec.seed)
    margin = 0.1 * (fam.x_hi - fam.x_lo)
    xs = np.full((spec.n_states, fam.d), 0.5 * (fam.x_lo + fam.x_hi))
    xs[:, 0] = rng.uniform(fam.x_lo - margin, fam.x_hi + margin,
                           size=spec.n_states)
    return np.zeros(spec.n_states), xs


def generate_instance(spec: InstanceSpec, *,
                      executor: Optional[ProcessPoolExecutor] = None,
                      n_jobs: int = 1) -> Instance:
    fam = FAMILIES[spec.family]
    factory = fam.make_factory(spec.params)
    pde = factory()
    ts, xs = _draw_states(spec, fam)
    ys, ses, rate = [], [], None
    for draw in range(spec.n_draws):
        data = generate_training_data(
            factory, n_states=spec.n_states, m_samples=spec.m_samples,
            seed=1000 * spec.seed + draw, x_lo=fam.x_lo, x_hi=fam.x_hi,
            states=(ts, xs), executor=executor, n_jobs=n_jobs)
        ys.append(data.y)
        ses.append(data.stderr)
        rate = data.rate
    u_exact = np.array([pde.exact_solution(0.0, xs[i])
                        for i in range(spec.n_states)])
    grid, xg, _ = _grid_inputs(fam.d, 0.0, fam.x_lo, fam.x_hi)
    u_grid = np.array([pde.exact_solution(0.0, xg[i]) for i in range(len(grid))])
    return Instance(spec, ts, xs, np.array(ys), np.array(ses), u_exact,
                    grid, u_grid, float(rate))


def instance_path(spec: InstanceSpec, root) -> Path:
    return Path(root) / spec.family / f"{spec.seed}.npz"


def _save_instance(inst: Instance, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, spec=inst.spec.to_json(), t=inst.t, x=inst.x, y=inst.y,
             stderr=inst.stderr, u_exact=inst.u_exact, grid=inst.grid,
             u_grid=inst.u_grid, rate=inst.rate)


def _load_instance(spec: InstanceSpec, path: Path) -> Optional[Instance]:
    """Return the cached instance, None if unreadable, raise on spec mismatch."""
    try:
        with np.load(path, allow_pickle=False) as f:
            stored = str(f["spec"])
            if stored != spec.to_json():
                raise ValueError(f"{path} holds spec {stored}, requested "
                                 f"{spec.to_json()}")
            return Instance(spec, f["t"], f["x"], f["y"], f["stderr"],
                            f["u_exact"], f["grid"], f["u_grid"],
                            float(f["rate"]))
    except ValueError as exc:
        if "spec" in str(exc):
            raise
        print(f"{path} unreadable ({exc}); regenerating", flush=True)
    except (OSError, KeyError) as exc:
        print(f"{path} unreadable ({exc}); regenerating", flush=True)
    return None


def load_or_generate_corpus(specs: Sequence[InstanceSpec], root, *,
                            n_jobs: int = 1, verbose: bool = False,
                            min_finite: int = 50) -> List[Instance]:
    executor = ProcessPoolExecutor(max_workers=n_jobs) if n_jobs > 1 else None
    out = []
    try:
        for k, spec in enumerate(specs):
            path = instance_path(spec, root)
            inst = _load_instance(spec, path) if path.exists() else None
            if inst is None:
                if verbose:
                    print(f"[{k + 1}/{len(specs)}] generating {path}", flush=True)
                inst = generate_instance(spec, executor=executor, n_jobs=n_jobs)
                _save_instance(inst, path)
            n_ok = int(inst.finite.sum())
            if n_ok < min_finite:
                print(f"skipping {path}: only {n_ok} finite rows "
                      f"(< {min_finite})", flush=True)
                continue
            out.append(inst)
    finally:
        if executor is not None:
            executor.shutdown()
    return out


def collate(instances: Sequence[Instance], *, n_context: int, n_query: int,
            rng: np.random.Generator) -> Dict[str, np.ndarray]:
    """Random context/query subsets of each instance's finite rows.

    Context = draw-0 rows; query targets = draw-1 rows (Noise2Noise) and the
    exact solution.  Rows are sampled with replacement when an instance has
    fewer finite rows than requested.
    """
    B = len(instances)
    d = instances[0].x.shape[1]
    P = len(instances[0].spec.params)
    ctx_tx = np.empty((B, n_context, d + 1)); ctx_y = np.empty((B, n_context))
    ctx_se = np.empty((B, n_context)); params = np.empty((B, P))
    q_tx = np.empty((B, n_query, d + 1)); q_y = np.empty((B, n_query))
    q_u = np.empty((B, n_query))
    for b, inst in enumerate(instances):
        ok = np.flatnonzero(inst.finite)
        ci = rng.choice(ok, size=n_context, replace=len(ok) < n_context)
        qi = rng.choice(ok, size=n_query, replace=len(ok) < n_query)
        tx = np.column_stack([inst.t, inst.x])
        ctx_tx[b] = tx[ci]; ctx_y[b] = inst.y[0, ci]; ctx_se[b] = inst.stderr[0, ci]
        params[b] = inst.spec.params
        q_tx[b] = tx[qi]; q_y[b] = inst.y[min(1, inst.y.shape[0] - 1), qi]
        q_u[b] = inst.u_exact[qi]
    return {"ctx_tx": ctx_tx, "ctx_y": ctx_y, "ctx_se": ctx_se,
            "params": params, "q_tx": q_tx, "q_y": q_y, "q_u": q_u}
```

Add `from . import corpus` and `"corpus"` to `__all__` in `parabolab/deep/__init__.py`. Append to `.gitignore`:

```
examples/nn_corpus/
!examples/set_denoiser_gonogo.csv
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_corpus.py -v`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add parabolab/deep/corpus.py parabolab/deep/__init__.py .gitignore tests/test_deep_corpus.py
git commit -m "feat(deep): multi-instance corpus (families, specs, two-draw instances, cache, collate)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 3: `SetDenoiser` (`setnet.py`)

**Files:**
- Create: `parabolab/deep/setnet.py`
- Modify: `parabolab/deep/__init__.py`
- Test: `tests/test_deep_setnet.py` (new)

**Interfaces:**
- Produces: `SetDenoiser(d: int, n_params: int, d_model: int = 128, n_heads: int = 4, n_layers: int = 4, dropout: float = 0.0, param_mean=None, param_std=None)`; buffers `param_mean`, `param_std` (shape `(n_params,)`, default zeros/ones); `context_stats(ctx_y) -> (mu (B,1), s (B,1))`; `forward(ctx_tx (B,N,d+1), ctx_y (B,N), ctx_se (B,N), params (B,P), q_tx (B,Q,d+1)) -> (B,Q)` in the original `y` units; property `n_params_total`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_deep_setnet.py`:

```python
"""Tests for the set-to-field denoiser."""

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from parabolab.deep.setnet import SetDenoiser


def _batch(B=2, N=12, Q=5, d=1, P=2, seed=0):
    g = torch.Generator().manual_seed(seed)
    ctx_tx = torch.cat([torch.zeros(B, N, 1), torch.randn(B, N, d, generator=g)], -1)
    ctx_y = torch.randn(B, N, generator=g) * 3 + 20
    ctx_se = torch.rand(B, N, generator=g) * 0.1
    params = torch.rand(B, P, generator=g)
    q_tx = torch.cat([torch.zeros(B, Q, 1), torch.randn(B, Q, d, generator=g)], -1)
    return ctx_tx, ctx_y, ctx_se, params, q_tx


def test_output_shape_and_finite():
    torch.manual_seed(0)
    net = SetDenoiser(d=1, n_params=2, d_model=16, n_heads=2, n_layers=1)
    out = net(*_batch())
    assert out.shape == (2, 5)
    assert torch.isfinite(out).all()
    assert net.n_params_total > 0


def test_context_permutation_invariance():
    torch.manual_seed(0)
    net = SetDenoiser(d=1, n_params=2, d_model=16, n_heads=2, n_layers=2).eval()
    ctx_tx, ctx_y, ctx_se, params, q_tx = _batch()
    perm = torch.randperm(ctx_tx.shape[1])
    with torch.no_grad():
        a = net(ctx_tx, ctx_y, ctx_se, params, q_tx)
        b = net(ctx_tx[:, perm], ctx_y[:, perm], ctx_se[:, perm], params, q_tx)
    torch.testing.assert_close(a, b, atol=1e-5, rtol=1e-5)


def test_scale_and_shift_equivariance_in_y():
    torch.manual_seed(0)
    net = SetDenoiser(d=1, n_params=2, d_model=16, n_heads=2, n_layers=2).eval()
    ctx_tx, ctx_y, ctx_se, params, q_tx = _batch()
    with torch.no_grad():
        a = net(ctx_tx, ctx_y, ctx_se, params, q_tx)
        b = net(ctx_tx, 7 * ctx_y + 3, 7 * ctx_se, params, q_tx)
    torch.testing.assert_close(b, 7 * a + 3, atol=1e-4, rtol=1e-4)


def test_context_stats_and_param_buffers():
    net = SetDenoiser(d=1, n_params=2, d_model=16, n_heads=2, n_layers=1,
                      param_mean=[0.5, 1.0], param_std=[0.25, 2.0])
    assert net.param_mean.tolist() == [0.5, 1.0]
    assert "param_std" in net.state_dict()
    _, ctx_y, *_ = _batch()
    mu, s = net.context_stats(ctx_y)
    assert mu.shape == (2, 1) and s.shape == (2, 1)
    torch.testing.assert_close(mu[:, 0], ctx_y.mean(1))


def test_constant_t_column_does_not_produce_nan():
    net = SetDenoiser(d=1, n_params=1, d_model=16, n_heads=2, n_layers=1)
    ctx_tx, ctx_y, ctx_se, _, q_tx = _batch(P=1)
    out = net(ctx_tx, ctx_y, ctx_se, torch.zeros(2, 1), q_tx)   # t == 0 everywhere
    assert torch.isfinite(out).all()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_setnet.py -v`
Expected: FAIL with `ModuleNotFoundError: parabolab.deep.setnet`.

- [ ] **Step 3: Implement `setnet.py`**

```python
"""Set-to-field denoiser: attention over a set of noisy coding-tree estimates.

Input  : a context set {(t_i, x_i, y_i, stderr_i)} of one PDE instance plus
         that instance's parameters, and query points (t, x).
Output : u(t, x) at the queries, in the units of y.

All per-instance scaling happens inside the model (the decisive lesson of
the 2026-09-15 ablation): (t, x) are standardised with the context's mean
and std per coordinate, y and stderr with the context's y mean and std,
parameters with fixed family constants; the output is un-scaled with the
context y statistics.  The model is therefore invariant to permutations
of the context and equivariant to affine changes of the y scale.
"""

from __future__ import annotations

import torch
from torch import nn


class SetDenoiser(nn.Module):
    def __init__(self, d: int, n_params: int, d_model: int = 128,
                 n_heads: int = 4, n_layers: int = 4, dropout: float = 0.0,
                 param_mean=None, param_std=None) -> None:
        super().__init__()
        self.d = d
        self.n_params = n_params
        pm = torch.zeros(n_params) if param_mean is None \
            else torch.as_tensor(param_mean, dtype=torch.float32)
        ps = torch.ones(n_params) if param_std is None \
            else torch.as_tensor(param_std, dtype=torch.float32)
        self.register_buffer("param_mean", pm)
        self.register_buffer("param_std", ps)

        self.ctx_embed = nn.Sequential(
            nn.Linear(d + 1 + 2 + n_params, d_model), nn.GELU(),
            nn.Linear(d_model, d_model))
        layer = nn.TransformerEncoderLayer(
            d_model, n_heads, dim_feedforward=4 * d_model, dropout=dropout,
            activation="gelu", batch_first=True, norm_first=True)
        self.encoder = nn.TransformerEncoder(layer, n_layers)
        self.q_embed = nn.Sequential(
            nn.Linear(d + 1 + n_params, d_model), nn.GELU(),
            nn.Linear(d_model, d_model))
        self.norm_q = nn.LayerNorm(d_model)
        self.norm_c = nn.LayerNorm(d_model)
        self.cross = nn.MultiheadAttention(d_model, n_heads, dropout=dropout,
                                           batch_first=True)
        self.head = nn.Sequential(nn.Linear(d_model, d_model), nn.GELU(),
                                  nn.Linear(d_model, 1))

    @property
    def n_params_total(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    @staticmethod
    def context_stats(ctx_y: torch.Tensor):
        """Per-instance mean and std of the context targets, shapes (B, 1)."""
        mu = ctx_y.mean(dim=1, keepdim=True)
        s = ctx_y.std(dim=1, keepdim=True).clamp_min(1e-8)
        return mu, s

    def forward(self, ctx_tx, ctx_y, ctx_se, params, q_tx):
        B, N, _ = ctx_tx.shape
        Q = q_tx.shape[1]
        mu_x = ctx_tx.mean(dim=1, keepdim=True)
        s_x = ctx_tx.std(dim=1, keepdim=True).clamp_min(1e-6)   # (B,1,d+1)
        mu_y, s_y = self.context_stats(ctx_y)                    # (B,1)
        p = (params - self.param_mean) / self.param_std           # (B,P)

        ctx = torch.cat([
            (ctx_tx - mu_x) / s_x,
            ((ctx_y - mu_y) / s_y).unsqueeze(-1),
            (ctx_se / s_y).unsqueeze(-1),
            p.unsqueeze(1).expand(B, N, -1),
        ], dim=-1)
        h = self.encoder(self.ctx_embed(ctx))                    # (B,N,D)

        q = self.q_embed(torch.cat([(q_tx - mu_x) / s_x,
                                    p.unsqueeze(1).expand(B, Q, -1)], dim=-1))
        hn = self.norm_c(h)
        attn, _ = self.cross(self.norm_q(q), hn, hn)
        q = q + attn
        out = self.head(q).squeeze(-1)                           # (B,Q) scaled
        return out * s_y + mu_y
```

Add `from . import setnet` and `"setnet"` to `__all__` in `parabolab/deep/__init__.py`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_setnet.py -v`
Expected: all PASS. (Permutation invariance holds because the encoder has no positional encoding and attention is permutation-equivariant; the pooling into the query is attention over the set, hence invariant.)

- [ ] **Step 5: Commit**

```bash
git add parabolab/deep/setnet.py parabolab/deep/__init__.py tests/test_deep_setnet.py
git commit -m "feat(deep): SetDenoiser -- transformer over noisy estimate sets with in-model scaling

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 4: Training, evaluation, baselines (`settrain.py`)

**Files:**
- Create: `parabolab/deep/settrain.py`
- Modify: `parabolab/deep/__init__.py`
- Test: `tests/test_deep_setnet.py`

**Interfaces:**
- Consumes: `corpus.Instance`, `corpus.collate`, `corpus.FAMILIES`; `setnet.SetDenoiser`; `ablation.NetConfig`, `ablation.build_net`; `solver.train_deep_branching`, `solver.grid_errors`, `solver._grid_inputs`; `generator.TrainingData`.
- Produces:
  - `SetTrainResult(net, losses: np.ndarray, seconds: float)`.
  - `train_set_denoiser(net, instances, *, steps=20000, lr=3e-4, weight_decay=1e-4, batch_instances=16, n_context=500, n_query=128, target="n2n", device="cpu", seed=0, log_every=100, verbose=False) -> SetTrainResult`; `target ∈ {"n2n", "exact"}`; raises `RuntimeError` naming the step on a non-finite loss.
  - `evaluate_set_denoiser(net, instances, *, n_context=500, device="cpu") -> np.ndarray` (L1 per instance on its 101-grid; `inf` for non-finite predictions).
  - `per_instance_mlp_l1(instance, *, draw=0, device="cpu", seed=0) -> float` (R5a config).
  - `kernel_smoother_l1(instance, *, draw=0) -> float`.
  - `R5A = NetConfig(neurons=64, activation="gelu", norm="none", scale_input=True, scale_output=True)`.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_deep_setnet.py`:

```python
# ---------------------------------------------------------------------------
# training / evaluation / baselines
# ---------------------------------------------------------------------------

from parabolab.deep import corpus, settrain


def _toy_corpus(n=4, n_states=40, m=4, seed=11):
    specs = corpus.sample_instances("ac1", n, seed, n_states=n_states, m_samples=m)
    return [corpus.generate_instance(s) for s in specs]


def test_train_set_denoiser_decreases_loss_and_evaluates():
    insts = _toy_corpus()
    torch.manual_seed(0)
    net = SetDenoiser(d=1, n_params=2, d_model=16, n_heads=2, n_layers=1)
    res = settrain.train_set_denoiser(
        net, insts, steps=30, batch_instances=2, n_context=16, n_query=8,
        log_every=10, lr=1e-3)
    assert np.isfinite(res.losses).all()
    assert res.losses[-1] < res.losses[0]
    l1 = settrain.evaluate_set_denoiser(net, insts, n_context=16)
    assert l1.shape == (4,) and np.isfinite(l1).all()


def test_train_set_denoiser_exact_target_and_bad_target():
    insts = _toy_corpus(n=2)
    net = SetDenoiser(d=1, n_params=2, d_model=16, n_heads=2, n_layers=1)
    res = settrain.train_set_denoiser(net, insts, steps=3, batch_instances=2,
                                      n_context=8, n_query=4, target="exact")
    assert np.isfinite(res.losses).all()
    with pytest.raises(ValueError):
        settrain.train_set_denoiser(net, insts, steps=1, target="mse")


def test_per_instance_mlp_baseline_runs():
    inst = _toy_corpus(n=1, n_states=60, m=20)[0]
    l1 = settrain.per_instance_mlp_l1(inst, epochs=50)
    assert np.isfinite(l1) and l1 < 1.0


def test_kernel_smoother_recovers_noiseless_instance():
    inst = _toy_corpus(n=1, n_states=1000, m=2)[0]
    inst.y[0] = inst.u_exact                     # no noise
    inst.stderr[0] = 1e-3
    assert settrain.kernel_smoother_l1(inst) < 5e-3
```

`per_instance_mlp_l1` needs an `epochs` override for the fast test: signature `per_instance_mlp_l1(instance, *, draw=0, device="cpu", seed=0, epochs=3000)`.

- [ ] **Step 2: Run tests to verify they fail**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_setnet.py -v -k "train or baseline or smoother"`
Expected: FAIL with `ImportError: cannot import name 'settrain'`.

- [ ] **Step 3: Implement `settrain.py`**

```python
"""Training, grid evaluation and baselines for the set-to-field denoiser."""

from __future__ import annotations

import dataclasses
import time
from dataclasses import dataclass
from typing import Sequence

import numpy as np
import torch

from . import corpus
from .ablation import NetConfig, build_net
from .generator import TrainingData
from .setnet import SetDenoiser
from .solver import _grid_inputs, grid_errors, train_deep_branching

# the ablation's kept configuration (spec 2026-09-15-nn-architecture-ablation)
R5A = NetConfig(neurons=64, activation="gelu", norm="none",
                scale_input=True, scale_output=True)


@dataclass
class SetTrainResult:
    net: SetDenoiser
    losses: np.ndarray
    seconds: float


def _to_t(batch, device):
    return {k: torch.as_tensor(v, dtype=torch.float32, device=device)
            for k, v in batch.items()}


def train_set_denoiser(
    net: SetDenoiser,
    instances: Sequence[corpus.Instance],
    *,
    steps: int = 20_000,
    lr: float = 3e-4,
    weight_decay: float = 1e-4,
    batch_instances: int = 16,
    n_context: int = 500,
    n_query: int = 128,
    target: str = "n2n",
    device: str = "cpu",
    seed: int = 0,
    log_every: int = 100,
    verbose: bool = False,
) -> SetTrainResult:
    """AdamW + cosine schedule + grad-clip 1.0 on the MSE in scaled y units.

    target="n2n": the query target is the instance's independent second
    draw (unbiased for MSE, Noise2Noise); "exact": the closed-form solution
    (an upper bound, only for families with one).
    """
    if target not in ("n2n", "exact"):
        raise ValueError(f"unknown target {target!r}; use 'n2n' or 'exact'")
    rng = np.random.default_rng(seed)
    torch.manual_seed(seed)
    net = net.to(device).train()
    opt = torch.optim.AdamW(net.parameters(), lr=lr, weight_decay=weight_decay)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=steps)
    key = "q_y" if target == "n2n" else "q_u"
    losses, start = [], time.perf_counter()
    instances = list(instances)
    for step in range(steps):
        idx = rng.choice(len(instances), size=min(batch_instances, len(instances)),
                         replace=False)
        batch = _to_t(corpus.collate([instances[i] for i in idx],
                                     n_context=n_context, n_query=n_query,
                                     rng=rng), device)
        mu, s = net.context_stats(batch["ctx_y"])
        pred = net(batch["ctx_tx"], batch["ctx_y"], batch["ctx_se"],
                   batch["params"], batch["q_tx"])
        loss = torch.mean(((pred - batch[key]) / s) ** 2)
        if not torch.isfinite(loss):
            raise RuntimeError(f"non-finite loss at step {step}")
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
        opt.step()
        sched.step()
        if step % log_every == 0 or step == steps - 1:
            losses.append(float(loss.detach()))
            if verbose:
                print(f"  step {step}: loss {losses[-1]:.4e}", flush=True)
    net.eval()
    return SetTrainResult(net, np.array(losses), time.perf_counter() - start)


@torch.no_grad()
def evaluate_set_denoiser(net: SetDenoiser, instances: Sequence[corpus.Instance],
                          *, n_context: int = 500, device: str = "cpu") -> np.ndarray:
    """L1 on each instance's 101-point grid; the context is (up to n_context of)
    the instance's finite draw-0 rows in a fixed order."""
    net = net.to(device).eval()
    out = []
    for inst in instances:
        ok = np.flatnonzero(inst.finite)
        ok = np.random.default_rng(0).permutation(ok)[:n_context]
        tx = np.column_stack([inst.t, inst.x])[ok]
        _, _, q = _grid_inputs(inst.x.shape[1], 0.0,
                               corpus.FAMILIES[inst.spec.family].x_lo,
                               corpus.FAMILIES[inst.spec.family].x_hi)
        batch = _to_t({"ctx_tx": tx[None], "ctx_y": inst.y[0, ok][None],
                       "ctx_se": inst.stderr[0, ok][None],
                       "params": np.array(inst.spec.params)[None],
                       "q_tx": q[None]}, device)
        pred = net(**batch)[0].cpu().numpy()
        err = np.abs(pred - inst.u_grid)
        out.append(float(err.mean()) if np.isfinite(err).all() else float("inf"))
    return np.array(out)


def _as_training_data(inst: corpus.Instance, draw: int) -> TrainingData:
    return TrainingData(t=inst.t, x=inst.x, y=inst.y[draw],
                        stderr=inst.stderr[draw],
                        n_kept=np.full(len(inst.t), inst.spec.m_samples),
                        m_samples=inst.spec.m_samples, rate=inst.rate,
                        seconds=0.0)


def per_instance_mlp_l1(inst: corpus.Instance, *, draw: int = 0,
                        device: str = "cpu", seed: int = 0,
                        epochs: int = 3000) -> float:
    """The ablation's kept net (R5A) trained on this instance alone."""
    fam = corpus.FAMILIES[inst.spec.family]
    pde = fam.make_factory(inst.spec.params)()
    net = build_net(R5A, d=fam.d, seed=seed)
    train_deep_branching(net, _as_training_data(inst, draw), epochs=epochs,
                         device=device)
    try:
        l1, *_ = grid_errors(net, pde, x_lo=fam.x_lo, x_hi=fam.x_hi, device=device)
    except (ValueError, RuntimeError):
        return float("inf")
    return float(l1) if np.isfinite(l1) else float("inf")


def kernel_smoother_l1(inst: corpus.Instance, *, draw: int = 0) -> float:
    """Nadaraya-Watson (Gaussian kernel on x_1) with the bandwidth chosen by
    leave-one-out on the context: the 'is attention more than smoothing'
    control."""
    ok = inst.finite
    x = inst.x[ok, 0]; y = inst.y[draw, ok]
    span = x.max() - x.min()
    bandwidths = span * np.logspace(-2.5, -0.5, 20)

    def predict(xq, h, loo=False):
        w = np.exp(-0.5 * ((xq[:, None] - x[None, :]) / h) ** 2)
        if loo:
            np.fill_diagonal(w, 0.0)
        return (w @ y) / np.maximum(w.sum(axis=1), 1e-300)

    loo = [np.mean((predict(x, h, loo=True) - y) ** 2) for h in bandwidths]
    h = bandwidths[int(np.argmin(loo))]
    pred = predict(inst.grid, h)
    return float(np.mean(np.abs(pred - inst.u_grid)))
```

Add `from . import settrain` and `"settrain"` to `__all__` in `parabolab/deep/__init__.py`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_setnet.py tests/test_deep_corpus.py -v`
Expected: all PASS (the training test takes ~10 s).

- [ ] **Step 5: Commit**

```bash
git add parabolab/deep/settrain.py parabolab/deep/__init__.py tests/test_deep_setnet.py
git commit -m "feat(deep): set-denoiser training/evaluation and per-instance MLP + kernel baselines

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 5: Driver script and CUDA torch

**Files:**
- Create: `examples/set_denoiser_gonogo.py`
- Modify: `environment.yml` (comment only, see step 4), `CLAUDE.md` Env line
- Test: `tests/test_deep_setnet.py` (driver `--tiny` smoke test)

**Interfaces:**
- Consumes: everything from Tasks 2–4.
- Produces: CLI
  `python examples/set_denoiser_gonogo.py --family ac1 --n-train 500 --n-test 50 --n-states 500 --m-samples 1000 --steps 20000 --device cuda --jobs 16 --corpus-root examples/nn_corpus --out examples/set_denoiser_gonogo.csv [--d-model 128 --n-layers 4 --tiny]`.
  CSV columns: `method, family, instance_seed, l1, seconds`; methods `d04_n2n`, `d04_exact`, `mlp_M`, `mlp_10M`, `kernel`.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_deep_setnet.py`:

```python
# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------

import csv
import subprocess
import sys
from pathlib import Path


def test_gonogo_driver_tiny(tmp_path):
    script = Path(__file__).resolve().parents[1] / "examples" / "set_denoiser_gonogo.py"
    out = tmp_path / "res.csv"
    subprocess.run(
        [sys.executable, str(script), "--family", "ac1", "--tiny",
         "--corpus-root", str(tmp_path / "corpus"), "--out", str(out),
         "--jobs", "1"],
        check=True, capture_output=True, text=True)
    rows = list(csv.DictReader(out.open()))
    methods = {r["method"] for r in rows}
    assert methods == {"d04_n2n", "d04_exact", "mlp_M", "mlp_10M", "kernel"}
    assert all(float(r["l1"]) >= 0 for r in rows)
    assert sum(r["method"] == "kernel" for r in rows) == 2   # 2 test instances
```

- [ ] **Step 2: Run test to verify it fails**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_setnet.py -v -k gonogo`
Expected: FAIL (script missing → `CalledProcessError`).

- [ ] **Step 3: Implement the driver**

```python
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
    train = corpus.load_or_generate_corpus(train_specs, root, n_jobs=args.jobs, verbose=True)
    test = corpus.load_or_generate_corpus(test_specs, root, n_jobs=args.jobs, verbose=True)
    test10 = corpus.load_or_generate_corpus(test10_specs, root / "x10", n_jobs=args.jobs,
                                            verbose=True)
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
```

- [ ] **Step 4: Install the CUDA torch wheel and record it**

Run (PowerShell):
```
conda run -n parabolab --no-capture-output pip install --force-reinstall --no-deps torch --index-url https://download.pytorch.org/whl/cu124
conda run -n parabolab --no-capture-output python -c "import torch, numpy; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else '-')"
```
Expected: a `+cu124` version string and `True`. If the installed version is not 2.13.x, pin it: `pip install --force-reinstall --no-deps torch==2.13.0 --index-url ...`. Then run `conda run -n parabolab --no-capture-output python -m pytest tests/test_solve.py tests/test_deep.py -q` — must stay green (gotcha 36: the pip numpy is OpenBLAS, so no OpenMP clash). If CUDA is not available on this machine after the install, keep the CPU wheel (reinstall from PyPI) and run the experiment with `--device cpu`; record which in the report.

In `environment.yml`, extend the comment above `- torch` with: `# GPU: pip install --force-reinstall --no-deps torch --index-url https://download.pytorch.org/whl/cu124 (same version pin; numpy stays the pip build, gotcha 36).` In `CLAUDE.md`'s Env bullet replace "Torch CPU build" with "Torch: CPU wheel by default, CUDA wheel via the one-liner in environment.yml".

- [ ] **Step 5: Run the driver test and the fast suite**

Run: `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_setnet.py -v -k gonogo` then `conda run -n parabolab --no-capture-output python -m pytest -q`
Expected: driver test PASS (~30 s: tiny corpus + 2 tiny trainings + 4 tiny MLP fits); full suite zero failures.

- [ ] **Step 6: Commit**

```bash
git add examples/set_denoiser_gonogo.py tests/test_deep_setnet.py environment.yml CLAUDE.md
git commit -m "feat: D04 go/no-go driver; CUDA torch install note

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 6: Run the go/no-go and record it

**Files:**
- Create: `examples/set_denoiser_gonogo.csv`, `examples/nn_corpus/` (git-ignored)
- Modify: spec `## Results`, `CLAUDE.md` gotchas

- [ ] **Step 1: Generate the corpus and run**

```
conda run -n parabolab --no-capture-output python -u examples/set_denoiser_gonogo.py --family ac1 --n-train 500 --n-test 50 --n-states 500 --m-samples 1000 --steps 20000 --device cuda --jobs 16
```
(≈ 20 min corpus + minutes of GPU training + ≈ 15 min of per-instance MLP baselines on CPU/GPU.) Use `--device cpu` if Task 5 found no CUDA. Capture the printed table and the verdict line.

- [ ] **Step 2: Sanity checks before believing the verdict**

- `d04_exact` ≤ `d04_n2n` (exact targets are an upper bound on what N2N can reach); if not, training is under-fitted — raise `--steps` to 50 000 once and rerun, noting it.
- `mlp_10M` < `mlp_M` (more samples must help the per-instance net); if not, the baseline is broken — stop and investigate `per_instance_mlp_l1`.
- `kernel` vs `d04_n2n`: if the kernel smoother matches D04, attention is only smoothing — record it as such even on a PASS.

- [ ] **Step 3: Write the results**

Append to `docs/superpowers/specs/2026-09-15-general-corpus-set-denoiser-design.md`:

```markdown
## Results

### D04 go/no-go — family ac1

Corpus: 500 train / 50 test instances, 500 states, M = 1000, two draws;
test instances also at M = 10 000. Model: SetDenoiser d_model 128, 4
layers, <n> parameters; 20 000 steps of 16 instances × 500 context ×
128 queries; device <cuda/cpu>.

<the printed table>

Verdict: <PASS/FAIL> (d04_n2n <x> vs mlp_M <y>). Sanity: d04_exact <=
d04_n2n? <yes/no>; mlp_10M < mlp_M? <yes/no>; kernel <z>.

Reading: <one paragraph — what the numbers say about whether attention
over the set learns transferable structure, how far N2N is from the
exact-target upper bound, and what Stage 1 should do next>.
```

Add a CLAUDE.md gotcha under the NN-ablation heading if anything non-obvious appeared (N2N-vs-exact gap, kernel matching D04, CUDA install caveats).

- [ ] **Step 4: Commit**

```bash
git add examples/set_denoiser_gonogo.csv docs/superpowers/specs/2026-09-15-general-corpus-set-denoiser-design.md CLAUDE.md
git commit -m "exp: D04 set-denoiser go/no-go on the ac1 family -- <PASS|FAIL>

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```
