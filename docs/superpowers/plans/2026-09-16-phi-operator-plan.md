# φ-Operator Learning (D03) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Train operators \(\phi \mapsto u(0,\cdot)\) from coding-tree labels for two 1-D families (linear heat, Allen–Cahn) with random Fourier-series terminal conditions, compare DeepONet / FNO-1D / cross-attention on identical corpora, and record the learning curve against a per-φ baseline.

**Architecture:** New library builders (`fourier_phi_expr`, `heat_fourier_1d`, `allen_cahn_fourier_1d`, `fd_reference_1d`); corpus extensions (`Family.param_sampler`, `Family.reference_name`, `Instance.phi_grid`, families `heat_phi`/`ac_phi`); `opnet.py` (three backbones sharing `forward(phi_grid, q_tx)`); `optrain.py` (pooled training, grid evaluation); driver `examples/phi_operator.py`.

**Tech Stack:** Python 3.11, numpy, sympy, torch 2.11+cu128, pytest; `conda run -n parabolab --no-capture-output python ...` (PowerShell).

## Global Constraints

- Spec: `docs/superpowers/specs/2026-09-16-phi-operator-design.md`. Branch `research/nn-architecture`.
- φ-family verbatim: segment \([-8, 8]\), \(\omega = \pi/8\), \(K = 4\), \(a_k, b_k \sim N(0, (1+k)^{-2})\), amplitude \(A\) such that \(\max|\phi| = 0.9\) on a 1001-point grid; `params = (A, a_1..a_4, b_1..b_4)` (9 floats). `heat_phi`: \(f \equiv 0\), \(T = 0.3\), exact \(u(t,x) = A\sum_k e^{-k^2\omega^2 (T-t)/2}(a_k\cos k\omega x + b_k \sin k\omega x)\). `ac_phi`: \(f(u) = u - u^3\), \(T = 0.3\), reference by explicit FD (\(\Delta x = 0.02\), \(\Delta t = 0.4\Delta x^2\), zero-flux on \([-12, 12]\)).
- Corpus: 1000 train φ (seed 0) / 50 held-out (seed 1), 500 states, \(M = 1000\), `n_draws = 1`; learning curve at `n_train ∈ {250, 500, 1000}` (prefixes of the seed-0 list).
- Existing behaviour byte-identical: `Family`/`InstanceSpec` defaults unchanged; old `.npz` files (no `phi_grid`) still load; all existing tests green.
- Gates (fixed): Step 1 (`heat_phi`) — some backbone at `n_train = 1000` reaches median held-out L1 ≤ 1.5× the per-φ baseline; Step 2 (`ac_phi`) same criterion; kept backbone = lowest median L1 at 1000, ties by max.
- Driver under `if __name__ == "__main__"`; `!examples/phi_operator.csv` in `.gitignore`; commit trailer `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.

---

## File structure

| File | Responsibility |
|---|---|
| `parabolab/library.py` (add 4 functions) | Fourier φ, the two PDE builders, FD reference |
| `parabolab/deep/corpus.py` (modify) | `param_sampler`, `reference_name`, `phi_grid`, two families |
| `parabolab/deep/opnet.py` (new) | `DeepONet`, `FNO1d`, `AttnOperator` |
| `parabolab/deep/optrain.py` (new) | `pooled_operator_rows`, `fit_operator_scalers`, `train_operator`, `evaluate_operator`, `per_phi_baseline` |
| `parabolab/deep/__init__.py` (modify) | exports |
| `examples/phi_operator.py` (new) | driver |
| `tests/test_deep_corpus.py`, `tests/test_deep_opnet.py` (new) | tests |
| `.gitignore`, spec `## Results`, `CLAUDE.md` | bookkeeping |

---

### Task 1: Library — Fourier φ, heat/AC builders, FD reference

**Files:** modify `parabolab/library.py` (append at end); test `tests/test_deep_corpus.py`.

**Interfaces — Produces:**
- `fourier_phi_expr(coeffs, x_lo=-8.0, x_hi=8.0) -> sympy.Expr` in `x_symbols(1)[0]`; `coeffs = (A, a_1..a_K, b_1..b_K)`, \(\omega = 2\pi/(x_{hi}-x_{lo})\) (= π/8 on the default segment), \(K = (\text{len}-1)/2\).
- `fourier_phi_numpy(coeffs, x, x_lo=-8.0, x_hi=8.0) -> np.ndarray` (same function, vectorised).
- `heat_fourier_1d(T, coeffs) -> FullyNonlinearPDEnD` (`d=1`, `deriv_map=((0,),)`, `f_expr = 0*z0`, exact solution as above, `name=f"heat_fourier_1d(T={T}, K={K})"`).
- `allen_cahn_fourier_1d(T, coeffs) -> FullyNonlinearPDEnD` (`f_expr = z0 - z0**3`, `exact_solution=None`).
- `fd_reference_1d(pde, xq, *, dx=0.02, x_pad=4.0, x_lo=-8.0, x_hi=8.0) -> np.ndarray`: \(u(0, x_q)\) for `deriv_map == ((0,),)` PDEs by explicit Euler on \(v(s,x) = u(T-s,x)\): \(v_s = \tfrac{\sigma^2}{2}v_{xx} + f(v)\), \(v(0)=\phi\), domain \([x_{lo}-x_{pad}, x_{hi}+x_{pad}]\), zero-flux (copy neighbour) boundaries, \(\Delta t = 0.4\,\Delta x^2/\sigma^2\) (last step shortened to land on \(T\)); `np.interp` onto `xq`. Raises `ValueError` if `pde.deriv_map != ((0,),)`.

- [ ] **Step 1: Failing tests** — append to `tests/test_deep_corpus.py`:

```python
# ---------------------------------------------------------------------------
# Fourier terminal conditions and the FD reference
# ---------------------------------------------------------------------------

from parabolab.library import (allen_cahn_fourier_1d, fd_reference_1d,
                               fourier_phi_expr, fourier_phi_numpy,
                               heat_fourier_1d)

COEFFS = (0.7, 0.5, -0.3, 0.2, 0.1, -0.4, 0.25, 0.0, 0.05)   # A, a1..a4, b1..b4


def test_fourier_phi_expr_matches_numpy():
    import sympy as sp
    from parabolab.pde import x_symbols
    expr = fourier_phi_expr(COEFFS)
    fn = sp.lambdify(x_symbols(1), expr, "math")
    xs = np.linspace(-8, 8, 7)
    np.testing.assert_allclose([fn(x) for x in xs], fourier_phi_numpy(COEFFS, xs), rtol=1e-12)


def test_heat_fourier_exact_matches_fd_reference():
    pde = heat_fourier_1d(0.3, COEFFS)
    xq = np.linspace(-8, 8, 101)
    exact = np.array([pde.exact_solution(0.0, np.array([x])) for x in xq])
    fd = fd_reference_1d(pde, xq)
    assert np.abs(fd - exact).max() < 1e-3
    assert np.abs(exact - fourier_phi_numpy(COEFFS, xq)).max() > 1e-2   # T = 0.3 actually damps


def test_fd_reference_matches_allen_cahn_wave():
    from parabolab.library import allen_cahn_nd
    pde = allen_cahn_nd(d=1, T=0.3)
    xq = np.linspace(-8, 8, 101)
    exact = np.array([pde.exact_solution(0.0, np.array([x])) for x in xq])
    assert np.abs(fd_reference_1d(pde, xq) - exact).max() < 1e-4


def test_fd_reference_rejects_gradient_nonlinearity():
    from parabolab.library import merton_hjb
    with pytest.raises(ValueError, match="deriv_map"):
        fd_reference_1d(merton_hjb(), np.linspace(100, 200, 5))


def test_allen_cahn_fourier_builder():
    pde = allen_cahn_fourier_1d(0.3, COEFFS)
    assert pde.exact_solution is None and pde.d == 1 and pde.T == 0.3
    assert float(pde.phi_mu((0,))(1.0)) == pytest.approx(fourier_phi_numpy(COEFFS, np.array([1.0]))[0])
```

- [ ] **Step 2: Run to fail** — `conda run -n parabolab --no-capture-output python -m pytest tests/test_deep_corpus.py -v -k "fourier or fd_reference"` → `ImportError`.

- [ ] **Step 3: Implement** — append to `parabolab/library.py`:

```python
# ---------------------------------------------------------------------------
# Random Fourier terminal conditions (D03 operator learning)
# ---------------------------------------------------------------------------

def _fourier_omega(x_lo: float, x_hi: float) -> float:
    return 2.0 * math.pi / (x_hi - x_lo)


def fourier_phi_expr(coeffs, x_lo: float = -8.0, x_hi: float = 8.0):
    """phi(x) = A sum_k (a_k cos(k w x) + b_k sin(k w x)), w = 2 pi / (x_hi - x_lo),
    coeffs = (A, a_1..a_K, b_1..b_K)."""
    import sympy as sp

    (x,) = x_symbols(1)
    A, rest = float(coeffs[0]), [float(c) for c in coeffs[1:]]
    K = len(rest) // 2
    w = _fourier_omega(x_lo, x_hi)
    expr = sum(rest[k - 1] * sp.cos(k * w * x) + rest[K + k - 1] * sp.sin(k * w * x)
               for k in range(1, K + 1))
    return A * expr


def fourier_phi_numpy(coeffs, x, x_lo: float = -8.0, x_hi: float = 8.0) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    A, rest = float(coeffs[0]), [float(c) for c in coeffs[1:]]
    K = len(rest) // 2
    w = _fourier_omega(x_lo, x_hi)
    out = np.zeros_like(x)
    for k in range(1, K + 1):
        out += rest[k - 1] * np.cos(k * w * x) + rest[K + k - 1] * np.sin(k * w * x)
    return A * out


def heat_fourier_1d(T: float, coeffs, x_lo: float = -8.0, x_hi: float = 8.0) -> FullyNonlinearPDEnD:
    """Linear heat equation du/dt + (1/2) u_xx = 0 with a Fourier-series
    terminal condition; each mode is damped by exp(-k^2 w^2 (T - t) / 2)."""
    z = z_symbols(0)
    A, rest = float(coeffs[0]), [float(c) for c in coeffs[1:]]
    K = len(rest) // 2
    w = _fourier_omega(x_lo, x_hi)

    def exact(t: float, xv) -> float:
        x = float(xv[0]) if hasattr(xv, "__len__") else float(xv)
        return A * sum(
            math.exp(-0.5 * (k * w) ** 2 * (T - t))
            * (rest[k - 1] * math.cos(k * w * x) + rest[K + k - 1] * math.sin(k * w * x))
            for k in range(1, K + 1))

    return FullyNonlinearPDEnD(
        T=T, d=1, deriv_map=((0,),), f_expr=0 * z[0],
        phi_expr=fourier_phi_expr(coeffs, x_lo, x_hi), exact_solution=exact,
        name=f"heat_fourier_1d(T={T}, K={K})")


def allen_cahn_fourier_1d(T: float, coeffs, x_lo: float = -8.0, x_hi: float = 8.0) -> FullyNonlinearPDEnD:
    """Allen-Cahn du/dt + (1/2) u_xx + u - u^3 = 0 with a Fourier-series
    terminal condition; no closed form (use fd_reference_1d)."""
    z = z_symbols(0)
    K = (len(coeffs) - 1) // 2
    return FullyNonlinearPDEnD(
        T=T, d=1, deriv_map=((0,),), f_expr=z[0] - z[0] ** 3,
        phi_expr=fourier_phi_expr(coeffs, x_lo, x_hi), exact_solution=None,
        name=f"allen_cahn_fourier_1d(T={T}, K={K})")


def fd_reference_1d(pde, xq, *, dx: float = 0.02, x_pad: float = 4.0,
                    x_lo: float = -8.0, x_hi: float = 8.0) -> np.ndarray:
    """u(0, xq) for a 1-D semilinear problem du/dt + (sigma2/2) u_xx + f(u) = 0
    by explicit Euler on v(s, x) = u(T - s, x) (zero-flux boundaries)."""
    import sympy as sp

    if tuple(pde.deriv_map) != ((0,),):
        raise ValueError("fd_reference_1d needs deriv_map == ((0,),) (f a function of u only)")
    z = z_symbols(0)
    f = sp.lambdify(z, pde.f_expr, "numpy")
    sigma2 = float(getattr(pde, "sigma2", 1.0))
    grid = np.arange(x_lo - x_pad, x_hi + x_pad + dx / 2, dx)
    phi = pde.phi_mu((0,))
    v = np.array([float(phi(x)) for x in grid])
    dt = 0.4 * dx**2 / sigma2
    s, T = 0.0, float(pde.T)
    while s < T - 1e-15:
        h = min(dt, T - s)
        lap = np.empty_like(v)
        lap[1:-1] = (v[2:] - 2 * v[1:-1] + v[:-2]) / dx**2
        lap[0] = (v[1] - v[0]) / dx**2 * 2      # zero-flux: ghost = v[1]
        lap[-1] = (v[-2] - v[-1]) / dx**2 * 2
        v = v + h * (0.5 * sigma2 * lap + np.asarray(f(v), dtype=float))
        s += h
    return np.interp(np.asarray(xq, dtype=float), grid, v)
```

(`f(v)` for `f_expr = 0*z0` lambdifies to a scalar 0 for array input — `np.asarray(..., dtype=float)` broadcasting with `+` handles it; if it returns a Python `0`, `v + h*(... + 0)` is still fine.)

- [ ] **Step 4: Run** → all pass (the FD tests take a few seconds each).
- [ ] **Step 5: Commit** — `feat: Fourier terminal conditions, heat/Allen-Cahn builders, 1-D FD reference` + trailer.

---

### Task 2: Corpus — φ-families

**Files:** modify `parabolab/deep/corpus.py`; test `tests/test_deep_corpus.py`.

**Interfaces — Produces:**
- `Family` gains `param_sampler: Optional[str] = None` and `reference_name: Optional[str] = None` (trailing fields).
- `FAMILIES["heat_phi"] = Family("heat_phi", ("A","a1","a2","a3","a4","b1","b2","b3","b4"), (), -8.0, 8.0, 1, "heat_fourier_1d", (("T", 0.3),), None, "fourier", None)`; `FAMILIES["ac_phi"]` likewise with `"allen_cahn_fourier_1d"` and `reference_name="fd_reference_1d"`. Their `make_factory(params)` passes `coeffs=tuple(params)` (special-case: when `param_sampler == "fourier"` the factory kwargs are `{**fixed, "coeffs": tuple(params)}`).
- `sample_fourier_params(rng, K=4, target_amp=0.9, x_lo=-8.0, x_hi=8.0) -> tuple` (draws \(a_k, b_k \sim N(0, (1+k)^{-2})\), sets \(A = 0.9 / \max|\phi_{A=1}|\) on a 1001-point grid).
- `sample_instances` uses it when `fam.param_sampler == "fourier"`.
- `Instance.phi_grid: Optional[np.ndarray] = None` (101,), filled by `generate_instance` for every family from `pde.phi_mu((0,))` on `grid`; saved/loaded like `deriv` (absent ⇒ `None`).
- `generate_instance`: when `pde.exact_solution is None`, `u_exact` and `u_grid` come from `getattr(library, fam.reference_name)(pde, xs[:, 0])` / `(pde, grid)`; raises `ValueError` if neither exists.

- [ ] **Step 1: Failing tests** — append to `tests/test_deep_corpus.py`:

```python
# ---------------------------------------------------------------------------
# phi-families
# ---------------------------------------------------------------------------

def test_sample_fourier_params_normalises_amplitude():
    rng = np.random.default_rng(0)
    p = corpus.sample_fourier_params(rng)
    assert len(p) == 9
    xs = np.linspace(-8, 8, 1001)
    assert np.abs(fourier_phi_numpy(p, xs)).max() == pytest.approx(0.9, rel=1e-9)


def test_phi_family_instances_have_phi_grid_and_reference():
    specs = corpus.sample_instances("heat_phi", 2, 3, n_states=30, m_samples=200, n_draws=1)
    assert specs[0].params != specs[1].params and len(specs[0].params) == 9
    inst = corpus.generate_instance(specs[0], n_jobs=2)
    assert inst.phi_grid.shape == (101,)
    np.testing.assert_allclose(inst.phi_grid, fourier_phi_numpy(specs[0].params, inst.grid), rtol=1e-10)
    ok = inst.finite
    z = (inst.y[0, ok] - inst.u_exact[ok]) / inst.stderr[0, ok]
    assert np.mean(np.abs(z) < 4.0) >= 0.95


def test_ac_phi_uses_fd_reference():
    spec = corpus.sample_instances("ac_phi", 1, 4, n_states=8, m_samples=4, n_draws=1)[0]
    inst = corpus.generate_instance(spec)
    pde = corpus.FAMILIES["ac_phi"].make_factory(spec.params)()
    assert pde.exact_solution is None
    np.testing.assert_allclose(inst.u_grid, fd_reference_1d(pde, inst.grid), rtol=1e-12)
    np.testing.assert_allclose(inst.u_exact, fd_reference_1d(pde, inst.x[:, 0]), rtol=1e-12)


def test_phi_grid_roundtrips_and_old_files_load(tmp_path):
    spec = corpus.sample_instances("heat_phi", 1, 5, n_states=8, m_samples=4, n_draws=1)[0]
    a = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    b = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    np.testing.assert_array_equal(a.phi_grid, b.phi_grid)
    # a file without phi_grid (pre-field) still loads with phi_grid None
    path = corpus.instance_path(spec, tmp_path)
    with np.load(path, allow_pickle=False) as f:
        keep = {k: f[k] for k in f.files if k != "phi_grid"}
    np.savez(path, **keep)
    c = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    assert c.phi_grid is None
```

- [ ] **Step 2: Run to fail** → `AttributeError: sample_fourier_params` / `KeyError: 'heat_phi'`.

- [ ] **Step 3: Implement.** In `corpus.py`:

```python
def sample_fourier_params(rng: np.random.Generator, K: int = 4, target_amp: float = 0.9,
                          x_lo: float = -8.0, x_hi: float = 8.0) -> Tuple[float, ...]:
    a = [float(rng.normal(0.0, 1.0 / (1 + k))) for k in range(1, K + 1)]
    b = [float(rng.normal(0.0, 1.0 / (1 + k))) for k in range(1, K + 1)]
    xs = np.linspace(x_lo, x_hi, 1001)
    peak = np.abs(library.fourier_phi_numpy((1.0, *a, *b), xs, x_lo, x_hi)).max()
    return (float(target_amp / peak), *a, *b)
```
`Family`: add `param_sampler: Optional[str] = None`, `reference_name: Optional[str] = None`; in `make_factory`, if `self.param_sampler == "fourier"`: `kwargs["coeffs"] = tuple(float(p) for p in params)` instead of zipping `param_names`. Families:
```python
    "heat_phi": Family("heat_phi", ("A", "a1", "a2", "a3", "a4", "b1", "b2", "b3", "b4"), (),
                       -8.0, 8.0, 1, "heat_fourier_1d", (("T", 0.3),), None, "fourier", None),
    "ac_phi": Family("ac_phi", ("A", "a1", "a2", "a3", "a4", "b1", "b2", "b3", "b4"), (),
                     -8.0, 8.0, 1, "allen_cahn_fourier_1d", (("T", 0.3),), None, "fourier",
                     "fd_reference_1d"),
```
`sample_instances`: `params = sample_fourier_params(rng) if fam.param_sampler == "fourier" else tuple(...)`. `Instance`: add `phi_grid: Optional[np.ndarray] = None` (after `deriv_exact`). `generate_instance`: after `grid, xg, _ = _grid_inputs(...)`:
```python
    phi = pde.phi_mu((0,))
    phi_grid = np.array([float(phi(xg[i][0])) for i in range(len(grid))])
    if pde.exact_solution is not None:
        u_exact = np.array([pde.exact_solution(0.0, xs[i]) for i in range(spec.n_states)])
        u_grid = np.array([pde.exact_solution(0.0, xg[i]) for i in range(len(grid))])
    elif fam.reference_name is not None:
        ref = getattr(library, fam.reference_name)
        u_exact = ref(pde, xs[:, 0]); u_grid = ref(pde, grid)
    else:
        raise ValueError(f"family {fam.key!r} has neither exact_solution nor reference_name")
```
(replace the existing two `u_exact`/`u_grid` lines; `phi(xg[i][0])` uses the scalar-coordinate call convention of `phi_mu` for `d = 1`). Pass `phi_grid=phi_grid` to `Instance(...)`; save it in `_save_instance` (always) and load with `f["phi_grid"] if "phi_grid" in f else None`.

- [ ] **Step 4: Run** `pytest tests/test_deep_corpus.py tests/test_deep_setnet.py tests/test_deep_condnet.py -q` → all pass.
- [ ] **Step 5: Commit** — `feat(deep): phi-families (heat_phi, ac_phi) with Fourier sampling, FD reference and phi_grid` + trailer.

---

### Task 3: Backbones (`opnet.py`)

**Files:** create `parabolab/deep/opnet.py`; modify `__init__.py`; test `tests/test_deep_opnet.py` (new).

**Interfaces — Produces:** every backbone is an `nn.Module` with `forward(phi_grid (B,S), q_tx (B,Q,2)) -> (B,Q)`, buffers `phi_scale ()`, `in_mean/in_std (2,)`, `out_mean/out_std ()` (identity defaults), property `n_params_total`, and a class attribute `needs_grid` (`FNO1d` needs the sensor grid as a constructor argument `grid (S,)`).
- `DeepONet(n_sensors=101, p=64, width=128)`.
- `FNO1d(grid, width=32, modes=16, n_layers=4)`; queries answered by linear interpolation of the grid output along `grid` (uniform spacing assumed; asserts it).
- `AttnOperator(d_model=128, n_heads=4, n_layers=4)` wrapping `SetDenoiser(d=1, n_params=1, ...)`; context = \((0, x_j, \phi_j, 0)\), params = zeros. Its `in_*`/`out_*` buffers exist but are unused (scaling is inside `SetDenoiser`); `phi_scale` unused too — documented.
- `make_operator(name, grid, **kw)` factory for `"deeponet" | "fno" | "attn"`.

- [ ] **Step 1: Failing tests** — create `tests/test_deep_opnet.py`:

```python
"""Tests for the phi -> u operator backbones."""

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from parabolab.deep import opnet

GRID = np.linspace(-8.0, 8.0, 101)


def _batch(B=3, Q=7, seed=0):
    g = torch.Generator().manual_seed(seed)
    phi = torch.randn(B, 101, generator=g) * 0.5
    q = torch.cat([torch.zeros(B, Q, 1), -8 + 16 * torch.rand(B, Q, 1, generator=g)], -1)
    return phi, q


@pytest.mark.parametrize("name", ["deeponet", "fno", "attn"])
def test_operator_shapes_and_finite(name):
    torch.manual_seed(0)
    net = opnet.make_operator(name, GRID, **({"d_model": 16, "n_layers": 1} if name == "attn" else
                                            {"width": 8, "modes": 4, "n_layers": 2} if name == "fno" else
                                            {"p": 8, "width": 16}))
    phi, q = _batch()
    out = net(phi, q)
    assert out.shape == (3, 7) and torch.isfinite(out).all()
    assert net.n_params_total > 0


def test_fno_interpolation_reproduces_grid_values():
    torch.manual_seed(0)
    net = opnet.FNO1d(GRID, width=8, modes=4, n_layers=2).eval()
    phi, _ = _batch(B=2)
    q = torch.cat([torch.zeros(2, 101, 1), torch.as_tensor(GRID, dtype=torch.float32).expand(2, 101).unsqueeze(-1)], -1)
    with torch.no_grad():
        at_grid = net(phi, q)
        direct = net.on_grid(phi)
    torch.testing.assert_close(at_grid, direct, atol=1e-5, rtol=1e-5)


def test_attn_operator_permutation_invariant_in_phi_tokens():
    torch.manual_seed(0)
    net = opnet.AttnOperator(d_model=16, n_heads=2, n_layers=1).eval()
    phi, q = _batch(B=2)
    perm = torch.randperm(101)
    with torch.no_grad():
        a = net(phi, q)
        b = net.forward_tokens(torch.as_tensor(GRID, dtype=torch.float32)[perm].expand(2, 101), phi[:, perm], q)
    torch.testing.assert_close(a, b, atol=1e-5, rtol=1e-5)


@pytest.mark.parametrize("name", ["deeponet", "fno"])
def test_output_scaler_applies(name):
    torch.manual_seed(0)
    net = opnet.make_operator(name, GRID, **({"width": 8, "modes": 4, "n_layers": 2} if name == "fno" else {"p": 8, "width": 16})).eval()
    phi, q = _batch(B=2)
    with torch.no_grad():
        a = net(phi, q)
        net.out_mean.fill_(3.0); net.out_std.fill_(2.0)
        b = net(phi, q)
    torch.testing.assert_close(b, 2 * a + 3)


def test_make_operator_rejects_unknown():
    with pytest.raises(ValueError):
        opnet.make_operator("unet", GRID)
```

- [ ] **Step 2: Run to fail** → `ModuleNotFoundError`.

- [ ] **Step 3: Implement `opnet.py`:**

```python
"""phi -> u operator backbones sharing forward(phi_grid (B,S), q_tx (B,Q,2)) -> (B,Q).

DeepONet   branch(phi) . trunk(t, x)
FNO1d      spectral convolutions on the sensor grid, queries by linear
           interpolation along the grid
AttnOperator  SetDenoiser reused: phi samples are the context tokens
           (x_j, phi_j, se=0), the query attends to them
Scalers phi_scale / in_* / out_* are buffers filled by optrain.fit_operator_scalers
(AttnOperator scales internally and ignores them).
"""

from __future__ import annotations

import numpy as np
import torch
from torch import nn

from .setnet import SetDenoiser


class _OperatorBase(nn.Module):
    needs_grid = False

    def _register_scalers(self):
        self.register_buffer("phi_scale", torch.ones(()))
        self.register_buffer("in_mean", torch.zeros(2))
        self.register_buffer("in_std", torch.ones(2))
        self.register_buffer("out_mean", torch.zeros(()))
        self.register_buffer("out_std", torch.ones(()))

    @property
    def n_params_total(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


def _mlp(sizes):
    layers = []
    for a, b in zip(sizes[:-1], sizes[1:]):
        layers += [nn.Linear(a, b), nn.GELU()]
    return nn.Sequential(*layers[:-1])


class DeepONet(_OperatorBase):
    def __init__(self, n_sensors: int = 101, p: int = 64, width: int = 128) -> None:
        super().__init__()
        self._register_scalers()
        self.branch = _mlp([n_sensors, width, width, p])
        self.trunk = _mlp([2, width, width, p])
        self.bias = nn.Parameter(torch.zeros(()))

    def forward(self, phi_grid, q_tx):
        b = self.branch(phi_grid / self.phi_scale)                       # (B,p)
        t = torch.nn.functional.gelu(self.trunk((q_tx - self.in_mean) / self.in_std))  # (B,Q,p)
        out = (t * b.unsqueeze(1)).sum(-1) + self.bias
        return out * self.out_std + self.out_mean


class SpectralConv1d(nn.Module):
    def __init__(self, width: int, modes: int) -> None:
        super().__init__()
        self.modes = modes
        scale = 1.0 / (width * width)
        self.weight = nn.Parameter(scale * torch.randn(width, width, modes, dtype=torch.cfloat))

    def forward(self, x):                        # x (B, width, S)
        xf = torch.fft.rfft(x)
        m = min(self.modes, xf.shape[-1])
        out = torch.zeros_like(xf)
        out[..., :m] = torch.einsum("bim,iom->bom", xf[..., :m], self.weight[..., :m])
        return torch.fft.irfft(out, n=x.shape[-1])


class FNO1d(_OperatorBase):
    needs_grid = True

    def __init__(self, grid, width: int = 32, modes: int = 16, n_layers: int = 4) -> None:
        super().__init__()
        self._register_scalers()
        grid = np.asarray(grid, dtype=float)
        steps = np.diff(grid)
        assert np.allclose(steps, steps[0]), "FNO1d needs a uniform sensor grid"
        self.register_buffer("grid", torch.as_tensor(grid, dtype=torch.float32))
        self.lift = nn.Linear(2, width)
        self.spectral = nn.ModuleList([SpectralConv1d(width, modes) for _ in range(n_layers)])
        self.pointwise = nn.ModuleList([nn.Conv1d(width, width, 1) for _ in range(n_layers)])
        self.proj = nn.Sequential(nn.Linear(width, 128), nn.GELU(), nn.Linear(128, 1))

    def on_grid(self, phi_grid):                 # (B,S) -> (B,S) scaled-output units
        B, S = phi_grid.shape
        xs = (self.grid / self.grid.abs().max()).expand(B, S)
        h = self.lift(torch.stack([phi_grid / self.phi_scale, xs], -1)).permute(0, 2, 1)  # (B,W,S)
        for spec, pw in zip(self.spectral, self.pointwise):
            h = torch.nn.functional.gelu(spec(h) + pw(h))
        return self.proj(h.permute(0, 2, 1)).squeeze(-1) * self.out_std + self.out_mean

    def forward(self, phi_grid, q_tx):
        vals = self.on_grid(phi_grid)            # (B,S)
        x = q_tx[..., 1]
        lo, hi, S = self.grid[0], self.grid[-1], self.grid.shape[0]
        pos = (x - lo) / (hi - lo) * (S - 1)
        i0 = pos.floor().clamp(0, S - 2).long()
        w = (pos - i0.float()).clamp(0.0, 1.0)
        v0 = torch.gather(vals, 1, i0)
        v1 = torch.gather(vals, 1, i0 + 1)
        return v0 * (1 - w) + v1 * w


class AttnOperator(_OperatorBase):
    needs_grid = True

    def __init__(self, grid=None, d_model: int = 128, n_heads: int = 4, n_layers: int = 4) -> None:
        super().__init__()
        self._register_scalers()
        self.core = SetDenoiser(d=1, n_params=1, d_model=d_model, n_heads=n_heads, n_layers=n_layers)
        grid = np.linspace(-8.0, 8.0, 101) if grid is None else np.asarray(grid, dtype=float)
        self.register_buffer("grid", torch.as_tensor(grid, dtype=torch.float32))

    def forward_tokens(self, xs, phi, q_tx):     # xs (B,S), phi (B,S)
        B, S = phi.shape
        ctx_tx = torch.stack([torch.zeros_like(xs), xs], -1)
        params = torch.zeros(B, 1, dtype=phi.dtype, device=phi.device)
        return self.core(ctx_tx, phi, torch.zeros_like(phi), params, q_tx)

    def forward(self, phi_grid, q_tx):
        xs = self.grid.expand(phi_grid.shape[0], -1)
        return self.forward_tokens(xs, phi_grid, q_tx)


def make_operator(name: str, grid, **kw):
    if name == "deeponet":
        return DeepONet(n_sensors=len(grid), **kw)
    if name == "fno":
        return FNO1d(grid, **kw)
    if name == "attn":
        return AttnOperator(grid, **kw)
    raise ValueError(f"unknown operator {name!r}; use deeponet, fno or attn")
```

Add `from . import opnet` + `"opnet"` to `__init__.py`. Note for the `test_output_scaler_applies` test on FNO: `on_grid` applies the output scaler before interpolation, so a change of `out_mean/out_std` is affine on the interpolated value as well — the test holds.

- [ ] **Step 4: Run** → all pass.
- [ ] **Step 5: Commit** — `feat(deep): operator backbones DeepONet / FNO1d / AttnOperator` + trailer.

---

### Task 4: Training and evaluation (`optrain.py`)

**Files:** create `parabolab/deep/optrain.py`; modify `__init__.py`; test `tests/test_deep_opnet.py`.

**Interfaces — Produces:**
- `pooled_operator_rows(instances) -> dict` with `phi (I,S)`, `tx (R,2)`, `u (R,)`, `inst_idx (R,)` (row → instance index), finite rows only.
- `fit_operator_scalers(net, rows)`: `phi_scale = std of all phi`, `in_mean/in_std` from `tx` (std floor as before), `out_mean/out_std` from `u`; no-op for attributes the net lacks.
- `OpTrainResult(net, losses, seconds)`; `train_operator(net, instances, *, steps=20000, batch_instances=32, n_query=64, lr=1e-3, device="cpu", seed=0, log_every=100, verbose=False)`: per step sample `batch_instances` instances, `n_query` finite rows each (with replacement), loss = MSE in scaled units (`((pred-u)/out_std)^2`; for `AttnOperator` use the pooled `u` std computed by the trainer since its buffers are unused); Adam + cosine + clip 1.0; `RuntimeError` on non-finite loss.
- `evaluate_operator(net, instances, *, device="cpu") -> np.ndarray` L1 per instance on `grid` vs `u_grid` (`inf` if non-finite).
- `per_phi_baseline(instance, *, device, seed, epochs=3000) -> float` = `settrain.per_instance_mlp_l1(instance, ...)` (re-exported for the driver).

- [ ] **Step 1: Failing tests** — append to `tests/test_deep_opnet.py`:

```python
# ---------------------------------------------------------------------------
# training / evaluation
# ---------------------------------------------------------------------------

from parabolab.deep import corpus, optrain


def _toy(n=3, seed=41, family="heat_phi"):
    specs = corpus.sample_instances(family, n, seed, n_states=40, m_samples=20, n_draws=1)
    return [corpus.generate_instance(s, n_jobs=2) for s in specs]


def test_pooled_operator_rows_and_scalers():
    insts = _toy()
    rows = optrain.pooled_operator_rows(insts)
    assert rows["phi"].shape == (3, 101) and rows["tx"].shape[1] == 2
    assert rows["u"].shape == rows["inst_idx"].shape and rows["inst_idx"].max() == 2
    net = opnet.DeepONet(p=8, width=16)
    optrain.fit_operator_scalers(net, rows)
    assert float(net.phi_scale) == pytest.approx(rows["phi"].std())
    assert float(net.in_std[0]) == 1.0 and float(net.out_std) == pytest.approx(rows["u"].std())


@pytest.mark.parametrize("name", ["deeponet", "fno", "attn"])
def test_train_operator_decreases_loss_and_evaluates(name):
    insts = _toy()
    torch.manual_seed(0)
    kw = {"attn": {"d_model": 16, "n_layers": 1}, "fno": {"width": 8, "modes": 4, "n_layers": 2},
          "deeponet": {"p": 8, "width": 16}}[name]
    net = opnet.make_operator(name, insts[0].grid, **kw)
    res = optrain.train_operator(net, insts, steps=40, batch_instances=2, n_query=8,
                                 lr=3e-3, log_every=10)
    assert np.isfinite(res.losses).all() and res.losses[-1] < res.losses[0]
    l1 = optrain.evaluate_operator(net, insts)
    assert l1.shape == (3,) and np.isfinite(l1).all()


def test_per_phi_baseline_runs():
    inst = _toy(n=1, seed=42)[0]
    assert np.isfinite(optrain.per_phi_baseline(inst, epochs=30))
```

- [ ] **Step 2: Run to fail** → `ImportError: optrain`.

- [ ] **Step 3: Implement `optrain.py`:**

```python
"""Pooled training and grid evaluation for phi -> u operators (spec
2026-09-16-phi-operator-design)."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, Sequence

import numpy as np
import torch

from . import corpus
from .settrain import per_instance_mlp_l1


def pooled_operator_rows(instances: Sequence[corpus.Instance]) -> Dict[str, np.ndarray]:
    phi = np.stack([inst.phi_grid for inst in instances])
    tx, u, idx = [], [], []
    for i, inst in enumerate(instances):
        ok = inst.finite
        tx.append(np.column_stack([inst.t, inst.x])[ok])
        u.append(inst.y[0, ok])
        idx.append(np.full(int(ok.sum()), i))
    return {"phi": phi, "tx": np.concatenate(tx), "u": np.concatenate(u),
            "inst_idx": np.concatenate(idx)}


def fit_operator_scalers(net, rows) -> float:
    """Fill the buffers the net has; return the pooled u std (used for the loss)."""
    u_std = float(rows["u"].std()) or 1.0
    with torch.no_grad():
        if hasattr(net, "phi_scale"):
            net.phi_scale.fill_(float(rows["phi"].std()) or 1.0)
        if hasattr(net, "in_mean"):
            mean, std = rows["tx"].mean(0), rows["tx"].std(0)
            std[std < 1e-12] = 1.0
            net.in_mean.copy_(torch.as_tensor(mean, dtype=torch.float32))
            net.in_std.copy_(torch.as_tensor(std, dtype=torch.float32))
        if hasattr(net, "out_mean"):
            net.out_mean.fill_(float(rows["u"].mean()))
            net.out_std.fill_(u_std)
    return u_std


@dataclass
class OpTrainResult:
    net: torch.nn.Module
    losses: np.ndarray
    seconds: float


def train_operator(net, instances, *, steps=20_000, batch_instances=32, n_query=64,
                   lr=1e-3, device="cpu", seed=0, log_every=100, verbose=False) -> OpTrainResult:
    rows = pooled_operator_rows(instances)
    u_std = fit_operator_scalers(net, rows)
    net = net.to(device).train()
    phi = torch.as_tensor(rows["phi"], dtype=torch.float32, device=device)
    tx = torch.as_tensor(rows["tx"], dtype=torch.float32, device=device)
    u = torch.as_tensor(rows["u"], dtype=torch.float32, device=device)
    per_inst = [np.flatnonzero(rows["inst_idx"] == i) for i in range(len(instances))]
    rng = np.random.default_rng(seed); torch.manual_seed(seed)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=steps)
    losses, start = [], time.perf_counter()
    for step in range(steps):
        bi = rng.choice(len(instances), size=min(batch_instances, len(instances)), replace=False)
        qi = np.stack([rng.choice(per_inst[i], size=n_query, replace=len(per_inst[i]) < n_query) for i in bi])
        qi_t = torch.as_tensor(qi, device=device)
        pred = net(phi[torch.as_tensor(bi, device=device)], tx[qi_t])
        loss = torch.mean(((pred - u[qi_t]) / u_std) ** 2)
        if not torch.isfinite(loss):
            raise RuntimeError(f"non-finite loss at step {step}")
        opt.zero_grad(); loss.backward()
        torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
        opt.step(); sched.step()
        if step % log_every == 0 or step == steps - 1:
            losses.append(float(loss.detach()))
            if verbose:
                print(f"  step {step}: loss {losses[-1]:.4e}", flush=True)
    net.eval()
    return OpTrainResult(net, np.array(losses), time.perf_counter() - start)


@torch.no_grad()
def evaluate_operator(net, instances, *, device="cpu") -> np.ndarray:
    net = net.to(device).eval()
    out = []
    for inst in instances:
        phi = torch.as_tensor(inst.phi_grid, dtype=torch.float32, device=device)[None]
        q = torch.as_tensor(np.column_stack([np.zeros_like(inst.grid), inst.grid]),
                            dtype=torch.float32, device=device)[None]
        pred = net(phi, q)[0].cpu().numpy()
        err = np.abs(pred - inst.u_grid)
        out.append(float(err.mean()) if np.isfinite(err).all() else float("inf"))
    return np.array(out)


def per_phi_baseline(inst: corpus.Instance, *, device="cpu", seed=0, epochs=3000) -> float:
    return per_instance_mlp_l1(inst, device=device, seed=seed, epochs=epochs)
```

Add `from . import optrain` + `"optrain"` to `__init__.py`.

- [ ] **Step 4: Run** `pytest tests/test_deep_opnet.py -q` → all pass.
- [ ] **Step 5: Commit** — `feat(deep): operator training/evaluation and per-phi baseline` + trailer.

---

### Task 5: Driver

**Files:** create `examples/phi_operator.py`; modify `.gitignore` (`!examples/phi_operator.csv`); test `tests/test_deep_opnet.py`.

- [ ] **Step 1: Failing test** — append:

```python
# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------

import csv
import subprocess
import sys
from pathlib import Path


def test_phi_operator_driver_tiny(tmp_path):
    script = Path(__file__).resolve().parents[1] / "examples" / "phi_operator.py"
    out = tmp_path / "res.csv"
    subprocess.run([sys.executable, str(script), "--family", "heat_phi", "--tiny", "--jobs", "1",
                    "--corpus-root", str(tmp_path / "corpus"), "--out", str(out)],
                   check=True, capture_output=True, text=True)
    rows = list(csv.DictReader(out.open()))
    assert {r["backbone"] for r in rows} == {"deeponet", "fno", "attn", "per_phi"}
    assert {int(r["n_train"]) for r in rows if r["backbone"] != "per_phi"} == {2, 3}
```

- [ ] **Step 2: Run to fail.**

- [ ] **Step 3: Implement `examples/phi_operator.py`:**

```python
"""D03: learn phi -> u(0, .) from coding-tree labels; compare three backbones.

    python examples/phi_operator.py --family heat_phi --n-train 1000 --n-test 50 \
        --curve 250 500 1000 --steps 20000 --device cuda --jobs 16
    python examples/phi_operator.py --family ac_phi ...

Rows: one per (backbone, n_train, held-out instance); the per_phi baseline
(R5A net on that phi's own labels) once per instance with n_train = 0.
"""

from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

import numpy as np

from parabolab.deep import corpus, opnet, optrain

FIELDS = ["family", "backbone", "n_train", "instance_seed", "l1", "seconds"]
BACKBONES = ("deeponet", "fno", "attn")


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--family", default="heat_phi", choices=["heat_phi", "ac_phi"])
    p.add_argument("--n-train", type=int, default=1000)
    p.add_argument("--n-test", type=int, default=50)
    p.add_argument("--curve", nargs="*", type=int, default=[250, 500, 1000])
    p.add_argument("--n-states", type=int, default=500)
    p.add_argument("--m-samples", type=int, default=1000)
    p.add_argument("--steps", type=int, default=20_000)
    p.add_argument("--backbones", nargs="*", default=list(BACKBONES))
    p.add_argument("--device", default="cpu")
    p.add_argument("--jobs", type=int, default=8)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--corpus-root", default="examples/nn_corpus")
    p.add_argument("--out", default="examples/phi_operator.csv")
    p.add_argument("--tiny", action="store_true")
    a = p.parse_args()
    if a.tiny:
        a.n_train, a.n_test, a.curve, a.n_states, a.m_samples, a.steps = 3, 2, [2, 3], 12, 4, 5
    return a


def write_rows(path, rows):
    path = Path(path); new = not path.exists()
    with path.open("a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if new: w.writeheader()
        w.writerows(rows)


def main(a):
    root = Path(a.corpus_root)
    kw = dict(n_states=a.n_states, m_samples=a.m_samples, n_draws=1)
    mf = min(50, a.n_states)
    train_specs = corpus.sample_instances(a.family, a.n_train, a.seed, **kw)
    test_specs = corpus.sample_instances(a.family, a.n_test, a.seed + 1, **kw)
    train = corpus.load_or_generate_corpus(train_specs, root, n_jobs=a.jobs, verbose=True, min_finite=mf)
    test = corpus.load_or_generate_corpus(test_specs, root, n_jobs=a.jobs, verbose=True, min_finite=mf)
    grid = test[0].grid
    tiny_kw = {"attn": {"d_model": 16, "n_layers": 1}, "fno": {"width": 8, "modes": 4, "n_layers": 2},
               "deeponet": {"p": 8, "width": 16}} if a.tiny else {}
    rows = []

    t0 = time.perf_counter()
    for inst in test:
        l1 = optrain.per_phi_baseline(inst, device=a.device, seed=a.seed, epochs=5 if a.tiny else 3000)
        rows.append({"family": a.family, "backbone": "per_phi", "n_train": 0,
                     "instance_seed": inst.spec.seed, "l1": l1,
                     "seconds": (time.perf_counter() - t0) / len(test)})

    import torch
    for n in a.curve:
        subset = train[:n]
        for name in a.backbones:
            torch.manual_seed(a.seed)
            net = opnet.make_operator(name, grid, **tiny_kw.get(name, {}))
            print(f"{a.family} {name} n_train={len(subset)}: {net.n_params_total} params", flush=True)
            res = optrain.train_operator(net, subset, steps=a.steps, device=a.device, seed=a.seed, verbose=True)
            l1 = optrain.evaluate_operator(net, test, device=a.device)
            rows += [{"family": a.family, "backbone": name, "n_train": len(subset),
                      "instance_seed": inst.spec.seed, "l1": v, "seconds": res.seconds / len(test)}
                     for inst, v in zip(test, l1)]
    write_rows(a.out, rows)

    print("\n| backbone | n_train | L1 median | L1 max |")
    print("|---|---|---|---|")
    keys = sorted({(r["backbone"], r["n_train"]) for r in rows}, key=lambda k: (k[0] != "per_phi", k))
    for name, n in keys:
        v = np.array([r["l1"] for r in rows if r["backbone"] == name and r["n_train"] == n])
        print(f"| {name} | {n} | {np.median(v):.2e} | {v.max():.2e} |")


if __name__ == "__main__":
    main(parse_args())
```

- [ ] **Step 4: Run** the driver test, then the full fast suite (zero failures).
- [ ] **Step 5: Commit** — `feat: phi-operator driver (three backbones, learning curve, per-phi baseline)` + trailer, with `.gitignore`.

---

### Task 6: Run Step 1 (heat_phi), gate, Step 2 (ac_phi), record

- [ ] `python examples/phi_operator.py --family heat_phi --steps 20000 --device cuda --jobs 16` (corpus: 1050 heat instances — trees die at the first branch, fast; baseline 50 × ~8 s; 9 trainings).
- [ ] Apply the Step 1 gate (spec). If it passes: `--family ac_phi ...` (corpus ≈ 15 min; FD references ≈ 1 s each).
- [ ] Append `## Results` to the spec: Step 1 table + gate, Step 2 table + learning curve (median L1 vs n_train per backbone), kept backbone, one paragraph per backbone, cost. CLAUDE.md gotcha if warranted. Commit `exp: phi-operator learning (heat_phi, ac_phi) -- <kept backbone>` + trailer with the CSV.
