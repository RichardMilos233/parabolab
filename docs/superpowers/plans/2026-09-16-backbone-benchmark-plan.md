# Universal-Backbone Benchmark Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run the same four backbones (DeepONet, FNO-1D, cross-attention operator, coefficient-conditioned MLP) on eight PDE families with one pre-registered score, and produce a ranked list plus a results document.

**Architecture:** Extend `parabolab/deep/families.py` with nD-class builders for the five new families and two reference solvers; extend `corpus.py` with `Family.rate`, `Instance.ref_stderr`; give every backbone in `opnet.py` a `cond` input (plus a `CoeffMLP` wrapper around `ConditionedNet`); extend `optrain.py` to pass `cond` and to run the calibration pre-check; one driver `examples/backbone_benchmark.py` with `--precheck`, per-family runs and `--report`.

**Tech Stack:** Python 3.11, numpy, sympy, torch 2.11+cu128, pytest; `conda run -n parabolab --no-capture-output python ...` (PowerShell).

## Global Constraints

- Spec: `docs/superpowers/specs/2026-09-16-backbone-benchmark-design.md` (incl. its Amendments). Branch `research/nn-backbone-benchmark`. All code under `parabolab/deep/`, `examples/`, `tests/`; **no edits to `parabolab/library.py`, `tree.py`, `mechanism.py`, `parallel.py`**.
- Families verbatim (all d = 1, Fourier φ with K = 4, max|φ| = 0.9, segment [−8, 8]; convention \(u_t + \tfrac12 u_{xx} + f = 0\)): `kpp_phi` \(f = z_0 - z_0^2\), T = 0.3, FD; `expgrad_phi` \(f = 10 z_1 + e^{-z_0} - 2e^{-2z_0}\), T = 0.05, FD with first-order term; `tan_phi` \(f = -z_2/2 + 10 z_1 + z_2/(1+z_0^2) - 2z_0\), T = 0.01, rate 1, MC reference; `cosine_phi` \(f = -z_2/2 + 10 z_1 + z_0 - (z_2/12)^2 + \cos(\pi z_4/24)\), T = 0.04, rate 1, MC; `log_phi` \(f = -z_2/2 + 5 z_1 + \log(z_2^2 + z_3^2)\), T = 0.02, rate 1, MC, conditional on the pre-check; `merton_theta` = existing `merton` family. Existing `heat_phi`, `ac_phi` unchanged.
- Corpus per family: 1000 train (seed 0) / 50 held-out (seed 1), 500 states, M = 1000, one draw; curve at n_train ∈ {250, 1000}; MC references at M = 10⁵ on the 101-grid with stored stderr.
- Pre-check (fixed): 20 instances at M = 1000 and M = 10⁴ at the same states; ≥ 95 % of states agree within 4 (combined) stderr; empirical stderr ratio within 2× of √10.
- Scores (fixed): \(r_{f,b}\) = median L1 / baseline median at n = 1000; \(S_b\) = geometric mean over families; failure family = \(r > 1.5\); robustness winner = lowest \(\max_f r\).
- Every backbone: `net(phi_grid (B,S), cond (B,P), q_tx (B,Q,2)) -> (B,Q)`; `cond` = `Instance.spec.params`.
- Existing tests green; commit trailer `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.

---

## File structure

| File | Responsibility |
|---|---|
| `parabolab/deep/families.py` (modify) | `kpp_fourier_1d`, `expgrad_fourier_1d`, `tan_fourier_1d`, `cosine_fourier_1d`, `log_fourier_1d`; `fd_reference_1d` with first-order terms; `mc_reference_1d` |
| `parabolab/deep/corpus.py` (modify) | `Family.rate`, `Family.reference_name` may name an MC reference, `Instance.ref_stderr`, five new `FAMILIES` entries |
| `parabolab/deep/opnet.py` (modify) | `cond` input on all operators; `CoeffMLP`; `make_operator(name, grid, n_cond, **kw)` |
| `parabolab/deep/optrain.py` (modify) | rows carry `cond`; `calibration_precheck` |
| `parabolab/deep/benchmark.py` (new) | scoring: `family_ratios`, `overall_scores`, `report_table` |
| `examples/backbone_benchmark.py` (new) | driver |
| `tests/test_deep_corpus.py`, `tests/test_deep_opnet.py`, `tests/test_deep_benchmark.py` (new) | tests |
| `docs/research/nn-fitting/backbone-benchmark.md` (new) | results |

---

### Task 1: Families and references

**Files:** modify `parabolab/deep/families.py`; test `tests/test_deep_corpus.py`.

**Interfaces — Produces:**
- `kpp_fourier_1d(T, coeffs)`, `expgrad_fourier_1d(T, coeffs, alpha=10.0)`, `tan_fourier_1d(T, coeffs, alpha=10.0)`, `cosine_fourier_1d(T, coeffs, alpha=10.0)`, `log_fourier_1d(T, coeffs, alpha=5.0)` → `FullyNonlinearPDEnD` with `d=1`, `phi_expr = fourier_phi_expr(coeffs)`, `exact_solution=None`, `deriv_map` `((0,),)` / `((0,),(1,))` / `((0,),(1,),(2,))` / up to `(4,)` / up to `(3,)`, `f_expr` exactly as in Global Constraints, names `f"<key>(T={T}, K={K})"`.
- `fd_reference_1d(pde, xq, ...)` accepts `deriv_map == ((0,),)` **or** `((0,), (1,))`; for the latter, `f(v, v_x)` with central-difference `v_x` (zero-flux ghost points), same time step.
- `mc_reference_1d(pde, xq, *, m_samples=100_000, seed=0, rate=None, n_jobs=1, executor=None) -> (u (Q,), stderr (Q,))` via `generate_training_data(factory, states=(zeros, xq[:,None]), m_samples, seed, rate, ...)`. Because `generate_training_data` needs a picklable factory, the function takes `factory` (a `functools.partial`) rather than a PDE: signature `mc_reference_1d(factory, xq, *, ...)`.

- [ ] **Step 1: Failing tests** — append to `tests/test_deep_corpus.py`:

```python
# ---------------------------------------------------------------------------
# benchmark families and references
# ---------------------------------------------------------------------------

from parabolab.deep import families as fam_mod


def test_new_fourier_families_build_with_expected_jets():
    expect = {"kpp_fourier_1d": 1, "expgrad_fourier_1d": 2, "tan_fourier_1d": 3,
              "cosine_fourier_1d": 5, "log_fourier_1d": 4}
    for name, n_jet in expect.items():
        pde = getattr(fam_mod, name)(0.02, COEFFS)
        assert pde.d == 1 and len(pde.deriv_map) == n_jet and pde.exact_solution is None
        assert float(pde.phi_mu((0,))(0.3)) == pytest.approx(fourier_phi_numpy(COEFFS, np.array([0.3]))[0])


def test_fd_reference_with_gradient_term_matches_advected_heat():
    """f = a u_x on the heat equation: u(0, x) = E phi(x + a T + W_T), i.e. the
    heat solution shifted by a T (check against heat_fourier_1d's closed form)."""
    import sympy as sp
    from parabolab.pde import FullyNonlinearPDEnD, z_symbols
    z = z_symbols(1)
    a, T = 3.0, 0.05
    pde = FullyNonlinearPDEnD(T=T, d=1, deriv_map=((0,), (1,)), f_expr=a * z[1],
                              phi_expr=fourier_phi_expr(COEFFS), exact_solution=None, name="adv")
    heat = heat_fourier_1d(T, COEFFS)
    xq = np.linspace(-6, 6, 61)
    ref = fd_reference_1d(pde, xq, dx=0.01)
    exact = np.array([heat.exact_solution(0.0, np.array([x + a * T])) for x in xq])
    assert np.abs(ref - exact).max() < 2e-3


def test_mc_reference_matches_closed_form():
    import functools
    factory = functools.partial(fam_mod.heat_fourier_1d, 0.3, COEFFS)
    xq = np.linspace(-8, 8, 5)
    u, se = fam_mod.mc_reference_1d(factory, xq, m_samples=4000, seed=1, n_jobs=2)
    exact = np.array([factory().exact_solution(0.0, np.array([x])) for x in xq])
    assert u.shape == se.shape == (5,)
    assert np.all(np.abs(u - exact) < 4.5 * se)
```

- [ ] **Step 2: Run to fail** — `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_corpus.py -v -k "new_fourier or gradient_term or mc_reference"` → `AttributeError`.

- [ ] **Step 3: Implement** — append to `parabolab/deep/families.py` (it already imports `math`, `np`, `FullyNonlinearPDEnD`, `x_symbols`, `z_symbols`; add `import functools` and `from .generator import generate_training_data` — note the import is *inside* `deep`, so no cycle with `corpus`):

```python
def _fourier_pde(name, T, coeffs, deriv_map, f_expr, x_lo=-8.0, x_hi=8.0):
    K = (len(coeffs) - 1) // 2
    return FullyNonlinearPDEnD(
        T=T, d=1, deriv_map=deriv_map, f_expr=f_expr,
        phi_expr=fourier_phi_expr(coeffs, x_lo, x_hi), exact_solution=None,
        name=f"{name}(T={T}, K={K})")


def kpp_fourier_1d(T: float, coeffs) -> FullyNonlinearPDEnD:
    """Fisher-KPP du/dt + (1/2) u_xx + u - u^2 = 0, Fourier terminal condition."""
    z = z_symbols(0)
    return _fourier_pde("kpp_fourier_1d", T, coeffs, ((0,),), z[0] - z[0] ** 2)


def expgrad_fourier_1d(T: float, coeffs, alpha: float = 10.0) -> FullyNonlinearPDEnD:
    """JEQ (5.5) at d = 1: f = alpha u_x + e^{-u} - 2 e^{-2u}."""
    import sympy as sp
    z = z_symbols(1)
    return _fourier_pde("expgrad_fourier_1d", T, coeffs, ((0,), (1,)),
                        alpha * z[1] + sp.exp(-z[0]) - 2 * sp.exp(-2 * z[0]))


def tan_fourier_1d(T: float, coeffs, alpha: float = 10.0) -> FullyNonlinearPDEnD:
    """JEQ (5.9) nonlinearity with a Fourier terminal condition."""
    z = z_symbols(2)
    return _fourier_pde("tan_fourier_1d", T, coeffs, ((0,), (1,), (2,)),
                        -z[2] / 2 + alpha * z[1] + z[2] / (1 + z[0] ** 2) - 2 * z[0])


def cosine_fourier_1d(T: float, coeffs, alpha: float = 10.0) -> FullyNonlinearPDEnD:
    """JEQ (5.10) nonlinearity (fourth order) with a Fourier terminal condition."""
    import sympy as sp
    z = z_symbols(4)
    return _fourier_pde("cosine_fourier_1d", T, coeffs, ((0,), (1,), (2,), (3,), (4,)),
                        -z[2] / 2 + alpha * z[1] + z[0] - (z[2] / 12) ** 2
                        + sp.cos(sp.pi * z[4] / 24))


def log_fourier_1d(T: float, coeffs, alpha: float = 5.0) -> FullyNonlinearPDEnD:
    """JEQ (5.11) nonlinearity (third order) with a Fourier terminal condition."""
    import sympy as sp
    z = z_symbols(3)
    return _fourier_pde("log_fourier_1d", T, coeffs, ((0,), (1,), (2,), (3,)),
                        -z[2] / 2 + alpha * z[1] + sp.log(z[2] ** 2 + z[3] ** 2))


def mc_reference_1d(factory, xq, *, m_samples: int = 100_000, seed: int = 0,
                    rate=None, n_jobs: int = 1, executor=None):
    """u(0, xq) and its standard error by the sampler itself (M trees per
    point, the generator's outlier filter as for every label in this line)."""
    xq = np.asarray(xq, dtype=float)
    data = generate_training_data(
        factory, n_states=len(xq), m_samples=m_samples, seed=seed, rate=rate,
        x_lo=float(xq.min()), x_hi=float(xq.max()),
        states=(np.zeros(len(xq)), xq[:, None]), n_jobs=n_jobs, executor=executor)
    return data.y, data.stderr
```

and modify `fd_reference_1d`: accept `deriv_map in (((0,),), ((0,), (1,)))`, lambdify `f` over `z_symbols(1)` when two rows, and in the loop compute `vx` by central differences with ghost points (`vx[1:-1] = (v[2:]-v[:-2])/(2dx)`, `vx[0] = vx[-1] = 0`) and call `f(v, vx)`; keep the one-argument path byte-identical for `((0,),)`. Update the `ValueError` message to name both accepted maps.

- [ ] **Step 4: Run** → pass (the MC test takes ~10 s). Also `pytest tests/test_deep_corpus.py -q` fully green.
- [ ] **Step 5: Commit** — `feat(deep): benchmark families (kpp, expgrad, tan, cosine, log) and MC/FD references` + trailer.

---

### Task 2: Corpus — rate, MC references, new families

**Files:** modify `parabolab/deep/corpus.py`; test `tests/test_deep_corpus.py`.

**Interfaces — Produces:**
- `Family` gains `rate: Optional[float] = None` (trailing) — passed to every `generate_training_data` call in `generate_instance`.
- `Instance` gains `ref_stderr: Optional[np.ndarray] = None` (101,), saved/loaded like `phi_grid`.
- Reference dispatch in `generate_instance`: if `fam.reference_name == "mc_reference_1d"`, call `families.mc_reference_1d(factory, grid, m_samples=100_000, seed=1000*spec.seed + 999, rate=fam.rate, executor=executor, n_jobs=n_jobs)` for `u_grid`/`ref_stderr`, and for the states' `u_exact` interpolate `np.interp(xs[:,0], grid, u_grid)` (the states are only used for training-time `q_u` and evaluation never reads them for these families); otherwise as now.
- `FAMILIES` gains `kpp_phi`, `expgrad_phi`, `tan_phi`, `cosine_phi`, `log_phi` with `param_sampler="fourier"`, `fixed_kwargs=(("T", …),)` per the constraints, `reference_name` = `"fd_reference_1d"` (kpp, expgrad) / `"mc_reference_1d"` (tan, cosine, log), `rate` = `None` / `None` / `1.0` / `1.0` / `1.0`.

- [ ] **Step 1: Failing tests** — append to `tests/test_deep_corpus.py`:

```python
def test_benchmark_families_registered():
    for key, ref, rate in (("kpp_phi", "fd_reference_1d", None), ("expgrad_phi", "fd_reference_1d", None),
                           ("tan_phi", "mc_reference_1d", 1.0), ("cosine_phi", "mc_reference_1d", 1.0),
                           ("log_phi", "mc_reference_1d", 1.0)):
        fam = corpus.FAMILIES[key]
        assert fam.param_sampler == "fourier" and fam.reference_name == ref and fam.rate == rate


def test_mc_reference_family_instance(tmp_path):
    spec = corpus.sample_instances("tan_phi", 1, 6, n_states=8, m_samples=4, n_draws=1)[0]
    # small reference budget for the test: patch via the module constant
    corpus.MC_REFERENCE_SAMPLES, saved = 200, corpus.MC_REFERENCE_SAMPLES
    try:
        inst = corpus.generate_instance(spec, n_jobs=2)
    finally:
        corpus.MC_REFERENCE_SAMPLES = saved
    assert inst.ref_stderr is not None and inst.ref_stderr.shape == (101,)
    assert np.isfinite(inst.u_grid).all() and inst.rate == 1.0
    a = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)   # cached? no: generate again is slow
    # instead round-trip the instance we have
    corpus._save_instance(inst, corpus.instance_path(spec, tmp_path))
    b = corpus._load_instance(spec, corpus.instance_path(spec, tmp_path))
    np.testing.assert_array_equal(b.ref_stderr, inst.ref_stderr)


def test_family_rate_reaches_the_generator():
    spec = corpus.sample_instances("tan_phi", 1, 7, n_states=4, m_samples=2, n_draws=1)[0]
    corpus.MC_REFERENCE_SAMPLES, saved = 50, corpus.MC_REFERENCE_SAMPLES
    try:
        inst = corpus.generate_instance(spec)
    finally:
        corpus.MC_REFERENCE_SAMPLES = saved
    assert inst.rate == 1.0
```

(Remove the stray `a = corpus.load_or_generate_corpus(...)` line in the second test before running — it is a note, not a step: use only the explicit save/load round trip. `MC_REFERENCE_SAMPLES = 100_000` is a module-level constant so tests can shrink it.)

- [ ] **Step 2: Run to fail.**
- [ ] **Step 3: Implement** as specified: `MC_REFERENCE_SAMPLES = 100_000`; `Family.rate`; `Instance.ref_stderr`; `generate_instance` passes `rate=fam.rate` to all label draws and branches on `reference_name == "mc_reference_1d"` (factory-based call) vs. other references (pde-based call, unchanged); `_save_instance`/`_load_instance` handle `ref_stderr`; register the five families (fixed kwargs: kpp `T=0.3`; expgrad `T=0.05`; tan `T=0.01`; cosine `T=0.04`; log `T=0.02`).
- [ ] **Step 4: Run** `pytest tests/test_deep_corpus.py tests/test_deep_opnet.py -q` → green.
- [ ] **Step 5: Commit** — `feat(deep): benchmark families in the corpus; Family.rate; MC grid references with stderr` + trailer.

---

### Task 3: Backbones take `cond`; `CoeffMLP`

**Files:** modify `parabolab/deep/opnet.py`; test `tests/test_deep_opnet.py`.

**Interfaces — Produces (all backbones):** `forward(phi_grid (B,S), cond (B,P), q_tx (B,Q,2)) -> (B,Q)`; buffers `cond_mean/cond_std (P,)` (identity defaults) on every backbone; constructors gain `n_cond: int` (required keyword): `DeepONet(n_sensors, n_cond, p, width)` branch input `n_sensors + n_cond`; `FNO1d(grid, n_cond, width, modes, n_layers)` lift input `2 + n_cond` (cond broadcast along the grid); `AttnOperator(grid, n_cond, d_model, n_heads, n_layers)` with `SetDenoiser(n_params=max(n_cond, 1))` (zero-pad when `n_cond == 0`); `CoeffMLP(n_cond, hidden_layers=6, neurons=64)` wrapping `ConditionedNet(d=1, n_params=n_cond, mode="film")`, ignoring `phi_grid`; `make_operator(name, grid, n_cond, **kw)` adds `"coeffmlp"`. Scaled `cond` = `(cond - cond_mean)/cond_std` inside each forward.

- [ ] **Step 1: Failing tests** — rewrite the existing opnet tests to pass `cond` (update `_batch` to also return `cond = torch.randn(B, 3)`, add `n_cond=3` to every constructor/`make_operator` call in `tests/test_deep_opnet.py`, including the training tests which use `n_cond=len(inst.spec.params)`), and add:

```python
def test_coeffmlp_ignores_phi_and_uses_cond():
    torch.manual_seed(0)
    net = opnet.CoeffMLP(n_cond=3, hidden_layers=2, neurons=8).eval()
    phi, q = _batch(B=2)[0], _batch(B=2)[1]
    cond = torch.randn(2, 3)
    with torch.no_grad():
        a = net(phi, cond, q); b = net(torch.zeros_like(phi), cond, q)
        c = net(phi, cond + 1.0, q)
    torch.testing.assert_close(a, b)
    assert not torch.allclose(a, c)


@pytest.mark.parametrize("name", ["deeponet", "fno", "attn"])
def test_operators_depend_on_cond(name):
    torch.manual_seed(0)
    kw = {"attn": {"d_model": 16, "n_layers": 1}, "fno": {"width": 8, "modes": 4, "n_layers": 2},
          "deeponet": {"p": 8, "width": 16}}[name]
    net = opnet.make_operator(name, GRID, n_cond=2, **kw).eval()
    phi, q = _batch(B=2)[0], _batch(B=2)[1]
    with torch.no_grad():
        a = net(phi, torch.zeros(2, 2), q); b = net(phi, torch.ones(2, 2), q)
    assert not torch.allclose(a, b)


def test_operators_accept_zero_cond():
    net = opnet.make_operator("attn", GRID, n_cond=0, d_model=16, n_layers=1)
    phi, q = _batch(B=2)[0], _batch(B=2)[1]
    assert torch.isfinite(net(phi, torch.zeros(2, 0), q)).all()
```

- [ ] **Step 2: Run to fail.** - [ ] **Step 3: Implement** (DeepONet: `branch(cat([phi/phi_scale, c], -1))`; FNO: `lift(cat([phi/phi_scale, xs, c.unsqueeze(1).expand(B,S,-1)], -1))`; Attn: `core(ctx_tx, phi, zeros, c_padded, q_tx)`; CoeffMLP: `self.core(q_tx.reshape(-1,2), c.repeat_interleave(Q,0)).view(B,Q)` — `ConditionedNet` already scales params through its own buffers, so `CoeffMLP` keeps `cond_mean/cond_std` as pass-through identity and forwards raw `cond`). - [ ] **Step 4: Run** `pytest tests/test_deep_opnet.py -q` → green. - [ ] **Step 5: Commit** — `feat(deep): operators take a conditioning vector; CoeffMLP backbone` + trailer.

---

### Task 4: Training with `cond`; calibration pre-check; scoring module

**Files:** modify `parabolab/deep/optrain.py`; create `parabolab/deep/benchmark.py`; tests `tests/test_deep_opnet.py`, `tests/test_deep_benchmark.py` (new).

**Interfaces — Produces:**
- `pooled_operator_rows` adds `cond (I,P)` (= `spec.params`); `fit_operator_scalers` fills `cond_mean/cond_std` when present (std floor 1e-12→1, and for `CoeffMLP` fill `core.param_mean/param_std` instead); `train_operator`/`evaluate_operator` pass `cond`.
- `calibration_precheck(family, *, n=20, n_states=200, m_lo=1000, m_hi=10_000, seed=123, n_jobs=1) -> dict` with keys `frac_within_4se`, `stderr_ratio`, `passed` (rule: `frac ≥ 0.95` and `ratio` within `[√10/2, 2√10]`), generating each instance twice via `generate_instance` on specs differing only in `m_samples` (same `seed` ⇒ same states; the label seeds differ by construction only through `m_samples`, fine).
- `benchmark.py`: `family_ratios(records) -> dict[(family, backbone, n_train)] -> {"ratio_median", "ratio_max", "l1_median", "l1_max"}` (baseline rows have `backbone == "per_phi"`), `overall_scores(ratios, n_train=1000) -> list[(backbone, S, max_ratio, failure_families)]` sorted by S, `report_table(...) -> str` (Markdown: per-family table + ranked list + robustness winner + slopes).

- [ ] **Step 1: Failing tests** — `tests/test_deep_benchmark.py`:

```python
import numpy as np, pytest
from parabolab.deep import benchmark

def _rec(family, backbone, n, l1s):
    return [{"family": family, "backbone": backbone, "n_train": n, "instance_seed": i, "l1": v, "seconds": 1.0}
            for i, v in enumerate(l1s)]

def test_scores_and_failures():
    recs = (_rec("A", "per_phi", 0, [1, 1, 1]) + _rec("A", "x", 1000, [0.5, 0.5, 2.0]) + _rec("A", "y", 1000, [2, 2, 2])
            + _rec("B", "per_phi", 0, [2, 2, 2]) + _rec("B", "x", 1000, [4, 4, 4]) + _rec("B", "y", 1000, [1, 1, 1])
            + _rec("A", "x", 250, [1, 1, 1]))
    r = benchmark.family_ratios(recs)
    assert r[("A", "x", 1000)]["ratio_median"] == 0.5 and r[("B", "x", 1000)]["ratio_median"] == 2.0
    ranked = benchmark.overall_scores(r)
    assert [b for b, *_ in ranked] == ["x", "y"]            # S_x = 1.0, S_y = sqrt(2*0.5) = 1.0 -> tie broken by name? see below
    table = benchmark.report_table(r)
    assert "| A |" in table and "robustness" in table.lower()
```

Fix the tie in the test so it is decisive: make `y`'s A-values `[3, 3, 3]` → `S_y = sqrt(3·0.5) ≈ 1.22 > S_x = 1.0`; `x` has failure family B (ratio 2 > 1.5), `y` has failure family A; the ranked list is `["x", "y"]` and `x`'s failure list is `["B"]`. Add asserts accordingly. Plus, in `tests/test_deep_opnet.py`, a `calibration_precheck` smoke test on `heat_phi` with `n=2, n_states=10, m_lo=20, m_hi=200` asserting the three keys exist and `passed` is a bool.

- [ ] **Step 2: Run to fail.** - [ ] **Step 3: Implement.** - [ ] **Step 4: Run** `pytest tests/test_deep_opnet.py tests/test_deep_benchmark.py -q` → green. - [ ] **Step 5: Commit** — `feat(deep): cond-aware operator training, calibration pre-check, benchmark scoring` + trailer.

---

### Task 5: Driver

**Files:** create `examples/backbone_benchmark.py`; `.gitignore` (`!examples/backbone_benchmark.csv`); test in `tests/test_deep_benchmark.py`.

CLI: `--families kpp_phi ...` (default: all eight), `--backbones` (default all four), `--curve 250 1000`, `--n-train 1000 --n-test 50 --n-states 500 --m-samples 1000 --steps 20000 --device cuda --jobs 16 --corpus-root examples/nn_corpus --out examples/backbone_benchmark.csv`, `--precheck` (run `calibration_precheck` for the listed families, print and write `examples/backbone_benchmark_precheck.json`, exit), `--report` (print `benchmark.report_table` from the CSV, exit), `--tiny`. Per family: load/generate corpora; baseline once (`backbone="per_phi"`, `n_train=0`); for each `n` in curve and each backbone: train, evaluate, append rows (skip rows already present, like the earlier drivers). Under `if __name__ == "__main__"`.

- [ ] **Step 1: Failing test** — `test_backbone_benchmark_driver_tiny(tmp_path)` runs `--tiny --families heat_phi --jobs 1` and asserts rows for `{"per_phi","deeponet","fno","attn","coeffmlp"}` and that `--report` prints "Ranked". - [ ] **Step 2–4** as usual, then the full fast suite. - [ ] **Step 5: Commit** — `feat: backbone benchmark driver` + trailer.

---

### Task 6: Run

- [ ] `--precheck --families kpp_phi expgrad_phi tan_phi cosine_phi log_phi --jobs 16`; record outcomes; exclude any failing family (expected candidate: `log_phi`).
- [ ] For each passing family, `python examples/backbone_benchmark.py --families <f> --steps 20000 --device cuda --jobs 16` (resumable); run the existing `heat_phi`, `ac_phi`, `merton` too so all eight share one CSV and one protocol (the D03 rows are in a different CSV/protocol — do not mix).
- [ ] `--report`; write `docs/research/nn-fitting/backbone-benchmark.md` (pre-check outcomes, per-family table, ranked list, robustness winner, slopes, one learning-curve figure `docs/research/nn-fitting/backbone-benchmark.png` made with matplotlib from the CSV, chosen backbone for tuning); add a CLAUDE.md gotcha; commit `exp: backbone benchmark -- <winner>` + trailer with the CSV, JSON and figure.
