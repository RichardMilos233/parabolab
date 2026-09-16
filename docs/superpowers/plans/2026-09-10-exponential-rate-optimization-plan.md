# Branching Clock Rate Optimization Implementation Plan

> **Archived implementation plan — status reviewed 16 September 2026.**
> Scalar-rate theory and finite-depth numerical selection are implemented.
> Later research added full-tree moment certificates and corrected the binary
> benchmark's estimator mismatch. This plan's unchecked boxes, model ownership,
> dirty-file exclusions, and formalization targets are historical; they are
> not a current task queue or a record of completed Lean coverage.
> Use the [binary audit](../../research/results/binary-benchmark-audit.md),
> [rate checkpoint](../../research/results/certified-rate-checkpoint.md), and
> [proof registry](../../research/proof-registry.md) for current evidence.
> Navigation: [archive index](../README.md), [current research](../../research/README.md),
> [documentation map](../../documentation-map.md).

> **Original workflow metadata (inactive):** This plan originally requested
> superpowers:subagent-driven-development or superpowers:executing-plans.
> Its checkbox syntax is preserved as a historical planning record.

**Goal:** Mathematically analyze, formalize in Lean 4, and numerically optimize the branching clock rate $\lambda > 0$ for coding-tree Monte Carlo, establishing strict convexity, unique interior sweet-spots for $L^2$-integrable PDEs, the $T \downarrow 0$ scaling law, and the pathology of non-integrable equations.

**Architecture:** The theory layer derives the local first-event objective $J_{\exp}(\lambda)$, proves its strict convexity and unique minimizer, proves the topology-level convexity of the full recursive moment $V(t, x; \lambda)$, and deduces the $O(1)$ short-horizon scaling $\lambda^*(T) \to |f(J\phi)|/|\phi|$. The Lean 4 layer mechanizes the strict convexity of the rate kernel and existence of the minimizer. The Python layer implements exact automatic derivatives $(\partial_\lambda V, \partial_\lambda^2 V)$ in numerical quadrature, a safeguarded bisection/Newton optimizer, and reproducible experiment scripts across semilinear binary controls, Allen--Cahn, and Harry Dym.

**Tech Stack:** Python 3.11, NumPy, SymPy, Matplotlib, PyTest, `conda run -n parabolab`, Lean 4.33.0, Mathlib `v4.33.0`.

## Original execution constraints (historical)

- Design document: `docs/superpowers/specs/2026-09-10-exponential-rate-optimization-design.md`.
- Mathematical derivation, theory documents, and Lean 4 formalization are owned by **GPT 5.6 Sol Max**.
- Python numerical implementations, test executions, and experiment scripts are owned by **Gemini / Execution Agent**.
- Lean proofs must compile cleanly via `lake build` with zero `sorry`, `admit`, or custom axioms.
- Preserve default `sample_tree` RNG sequence and exact reproducibility.
- Do not modify or commit user-owned uncommitted changes in `demo/merton.py` or `demo/merton_vasicek.py`.
- No percentile filtering, clipping, or tail-dropping in error or variance reporting.
- All Python commands run through `conda run -n parabolab`.

## File Map

### Theory & formalization
- Create: `docs/research/estimator-integrity/exponential-rate-optimization.md`
  Complete paper-level proofs of local $J_{\exp}(\lambda)$ convexity, full-tree topology convexity, Riccati analytic benchmark, and $T \downarrow 0$ scaling.
- Create: `formal/EstimatorIntegrity/ExponentialRate.lean`
  Lean 4 verification of the exponential rate kernel derivatives, strict convexity, and root existence.
- Modify: `formal/EstimatorIntegrity.lean`
  Import the new `ExponentialRate` module.

### Python implementation & tests
- Create: `parabolab/rate_optimization.py`
  Automatic derivatives of moment recursion with respect to rate $\lambda$, safeguarded root-finder on $\partial_\lambda V = 0$, and analytical Riccati benchmark.
- Modify: `parabolab/__init__.py`
  Export rate optimization utilities.
- Create: `tests/test_rate_optimization.py`
  Unit tests for automatic derivatives, convexity, bisection optimizer against Riccati ground truth, and finite-depth Monte Carlo validation.
- Create: `examples/exponential_rate_sweet_spot.py`
  Reproducible numerical experiments generating U-curves, short-horizon scaling comparisons against $\lambda_{\text{JCP}}$, and Dym divergence confirmation.
- Modify: `docs/research/proof-registry.md`
  Register formal proof entries `PR-RATE-1` through `PR-RATE-4`.
- Modify: `docs/research/estimator-integrity/reproducibility.md`
  Add the reproducibility audit for the rate-optimization experiment.

---

### Task 1: Mathematical Theory Note on Exponential Rate Optimization

**Files:**
- Create: `docs/research/estimator-integrity/exponential-rate-optimization.md`

**Interfaces:**
- Consumes: `docs/research/estimator-integrity/notation-and-moment-theorem.md`, `docs/research/estimator-integrity/adaptive-proposals.md`
- Produces: Proved theorems for local convexity, topology convexity, short-horizon scaling, and exact Riccati control.

- [ ] **Step 1: Write the formal mathematical note**

Document:
1. Local objective $J_{\exp}(\lambda) = A_0 e^{\lambda \Delta} + \frac{1}{\lambda} \int_0^\Delta A(s) e^{\lambda s} ds$, its first derivative, and its positive second derivative $J_{\exp}''(\lambda) = A_0 \Delta^2 e^{\lambda \Delta} + \frac{1}{\lambda^3} \int_0^\Delta A(s) e^{\lambda s} [(\lambda s - 1)^2 + 1] ds > 0$.
2. Proof of unique global minimizer $\lambda^* \in (0, \infty)$ via boundary asymptotics $\lambda \downarrow 0$ and $\lambda \to \infty$.
3. Full-tree topology decomposition $h_{B, L}(\lambda) = \lambda^{-B} e^{\lambda L}$, proving strict convexity of every finite-depth moment and lower-semicontinuous convexity of $V(t, x; \lambda)$.
4. Exact analytical Riccati ODE solution for $u_t + \frac{1}{2}u_{xx} + u^2 = 0$ with $\phi \equiv 1$: $V(T; \lambda) = \frac{\lambda^2 e^{\lambda T}}{\lambda^2 + 1 - e^{\lambda T}}$ and its transcendental optimality equation.
5. Short-horizon scaling $\lambda^*(T) \to |f(J\phi)|/|\phi| = O(1)$ vs $\lambda_{\text{JCP}}(T) = -\ln(0.95)/T = O(1/T)$.
6. Theorem showing Dym equation has $V \equiv +\infty$ for all $\lambda > 0$, proving absence of any finite sweet spot.

- [ ] **Step 2: Commit the theory documentation**

```bash
git add docs/research/estimator-integrity/exponential-rate-optimization.md
git commit -m "docs: write exponential clock rate optimization theory note"
```

---

### Task 2: Lean 4 Formalization of Rate Kernel Convexity

**Files:**
- Create: `formal/EstimatorIntegrity/ExponentialRate.lean`
- Modify: `formal/EstimatorIntegrity.lean`

**Interfaces:**
- Consumes: Mathlib analysis and calculus libraries.
- Produces: Mechanically verified proofs of rate kernel positivity, derivative identities, and strict convexity without `sorry`.

- [ ] **Step 1: Write `formal/EstimatorIntegrity/ExponentialRate.lean`**

Formalize:
1. `def expRateKernel (λ s : ℝ) : ℝ := Real.exp (λ * s) / λ`
2. `def topologyKernel (B : ℕ) (L : ℝ) (λ : ℝ) : ℝ := λ ^ (- (B : ℝ)) * Real.exp (λ * L)`
3. Lemma proving algebraic identity: for $\lambda > 0$, $[(\lambda s - 1)^2 + 1] \ge 1 > 0$.
4. Lemma proving topology second derivative positivity: for $L > 0, B \ge 0, \lambda > 0$:
   $[(L - B/\lambda)^2 + B/\lambda^2] > 0$.
5. Theorem proving `StrictConvexOn ℝ (Set.Ioi 0)` for the leading objective $a \lambda + b / \lambda$ with $a, b > 0$, and unique minimizer at $\sqrt{b/a}$.

- [ ] **Step 2: Add module to `formal/EstimatorIntegrity.lean` and build**

```bash
cd formal && lake build
```
Expected: Build succeeds with 0 errors and 0 warnings.

- [ ] **Step 3: Commit the Lean formalization**

```bash
git add formal/EstimatorIntegrity/ExponentialRate.lean formal/EstimatorIntegrity.lean
git commit -m "proof: formalize exponential rate kernel convexity in Lean 4"
```

---

### Task 3: Deterministic Derivatives and Scalar Rate Optimizer

**Files:**
- Create: `parabolab/rate_optimization.py`
- Modify: `parabolab/__init__.py`
- Test: `tests/test_rate_optimization.py`

**Interfaces:**
- Consumes: `parabolab.moments.MomentQuadrature`, `parabolab.pde.ParabolicPDE`
- Produces: `finite_depth_moment_derivatives_1d`, `optimize_exponential_rate_1d`, `riccati_binary_second_moment`

- [ ] **Step 1: Write failing tests in `tests/test_rate_optimization.py`**

Test automatic derivatives $(\partial_\lambda V, \partial^2_\lambda V)$ against centered finite differences:
```python
def test_leaf_rate_derivatives():
    pde = constant_terminal_pde(T=0.3)
    rate = 1.5
    res = finite_depth_moment_derivatives_1d(pde, 0.0, 0.0, max_depth=0, rate=rate)
    exact_val = math.exp(rate * 0.3)
    exact_d1 = 0.3 * math.exp(rate * 0.3)
    exact_d2 = 0.09 * math.exp(rate * 0.3)
    assert res.value == pytest.approx(exact_val, rel=1e-9)
    assert res.d_rate == pytest.approx(exact_d1, rel=1e-9)
    assert res.d2_rate == pytest.approx(exact_d2, rel=1e-9)
```

- [ ] **Step 2: Run test to verify failure**

```bash
conda run -n parabolab pytest tests/test_rate_optimization.py -v
```
Expected: FAIL with `ModuleNotFoundError` or `ImportError`.

- [ ] **Step 3: Implement `parabolab/rate_optimization.py`**

Implement:
1. `RateMomentDerivatives` dataclass holding `(value, d_rate, d2_rate)`.
2. `finite_depth_moment_derivatives_1d(...)`: recursive quadrature evaluating both moment and automatic derivatives without division by zero.
3. `riccati_binary_second_moment(T, rate)`: exact analytic formula for validation.
4. `optimize_exponential_rate_1d(pde, t, x, max_depth, ...)`: safeguarded bisection / Newton root-finder solving $\partial_\lambda V = 0$.

- [ ] **Step 4: Export utilities in `parabolab/__init__.py`**

Export `finite_depth_moment_derivatives_1d`, `optimize_exponential_rate_1d`, `riccati_binary_second_moment`.

- [ ] **Step 5: Run tests to verify pass**

```bash
conda run -n parabolab pytest tests/test_rate_optimization.py -v
```
Expected: PASS.

- [ ] **Step 6: Commit implementation**

```bash
git add parabolab/rate_optimization.py parabolab/__init__.py tests/test_rate_optimization.py
git commit -m "feat: implement deterministic rate derivatives and root optimizer"
```

---

### Task 4: Unit Testing Against Riccati Oracle and Monte Carlo

**Files:**
- Modify: `tests/test_rate_optimization.py`

**Interfaces:**
- Consumes: `riccati_binary_second_moment`, `optimize_exponential_rate_1d`, `sample_tree`
- Produces: Comprehensive test coverage for root finding, finite differences, and Monte Carlo agreement.

- [ ] **Step 1: Add oracle and MC validation tests**

1. Compare `optimize_exponential_rate_1d` against numerical solution of $2(e^{\lambda T} - 1) = T \lambda (\lambda^2 + 1)$ for $T \in \{0.05, 0.1, 0.2\}$ (agreement within $10^{-6}$).
2. Test centered finite difference validation of $d\_rate$ and $d2\_rate$ across depth $K \in \{0, 1, 2\}$.
3. Monte Carlo cross-check: for depth 1 binary model at $\lambda = \lambda^*$, empirical $\frac{1}{N}\sum H_i^2$ matches deterministic quadrature within 3 standard errors.
4. Test that non-integrable/diverging cases raise or fail to bracket rather than returning spurious roots.

- [ ] **Step 2: Run test suite**

```bash
conda run -n parabolab pytest tests/test_rate_optimization.py -v
```
Expected: All tests pass.

- [ ] **Step 3: Commit test suite**

```bash
git add tests/test_rate_optimization.py
git commit -m "test: add oracle benchmark and MC validation tests for rate optimizer"
```

---

### Task 5: Reproducible Numerical Experiments & Sweet-Spot Figures

**Files:**
- Create: `examples/exponential_rate_sweet_spot.py`
- Output: `examples/exponential_rate_sweet_spot.csv`, `examples/exponential_rate_sweet_spot.png`

**Interfaces:**
- Consumes: `parabolab.library.allen_cahn_nd`, `parabolab.library.dym_1d`, `parabolab.rate_optimization`
- Produces: 3-panel publication figure and numerical audit CSV.

- [ ] **Step 1: Implement `examples/exponential_rate_sweet_spot.py`**

Script structure:
1. **Panel 1 (Analytic Binary Control):** Plot deterministic $V(T; \lambda)$ U-curves for $T \in \{0.05, 0.1, 0.2\}$ across $\lambda \in [0.2, 4.0]$. Overlay ground-truth Riccati curves, markers at $\lambda^*(T)$, and markers at $\lambda_{\text{JCP}}(T)$.
2. **Panel 2 (Allen--Cahn $d=1$):** Evaluate deterministic second moments for Allen--Cahn across $\lambda \in [0.1, 3.0]$. Compute $\lambda^*(T)$ for $T \in \{0.02, 0.05, 0.1, 0.2\}$, verifying that $\lambda^*(T) \to 0.75$ as $T \to 0$ while $\lambda_{\text{JCP}}(T) \to \infty$. Compare sample variances under $\lambda^*$ vs $\lambda = 1.0$ vs $\lambda_{\text{JCP}}$.
3. **Panel 3 (Harry Dym Divergence):** Plot empirical second moment vs $\lambda$ across sample counts $N \in \{10^3, 10^4, 10^5\}$, showing that empirical variance fails to form a stable minimum and spikes without bound as $N$ increases.
4. Save structured CSV `examples/exponential_rate_sweet_spot.csv` and high-res plot `examples/exponential_rate_sweet_spot.png`.

- [ ] **Step 2: Execute script and verify artifacts**

```bash
conda run -n parabolab python examples/exponential_rate_sweet_spot.py
```
Expected: Generates CSV and PNG without errors.

- [ ] **Step 3: Commit experiment script**

```bash
git add examples/exponential_rate_sweet_spot.py
git commit -m "feat: add reproducible rate optimization experiment script"
```

---

### Task 6: Research Proof Registry and Documentation Audit

**Files:**
- Modify: `docs/research/proof-registry.md`
- Modify: `docs/research/estimator-integrity/reproducibility.md`

**Interfaces:**
- Consumes: Artifacts and outputs from Tasks 1–5.
- Produces: Complete audit ledger entries linking theorems, proofs, Lean files, and numerical outputs.

- [ ] **Step 1: Update `docs/research/proof-registry.md`**

Register:
- `PR-RATE-1`: Local Exponential Rate Convexity ($J_{\exp}''(\lambda) > 0$). Proved theorem & Lean verified.
- `PR-RATE-2`: Topology-Level Coding Tree Convexity ($h_{B, L}''(\lambda) > 0$). Proved theorem & Lean verified.
- `PR-RATE-3`: Short-Horizon Asymptotic Scaling $\lambda^*(T) \to |f(J\phi)|/|\phi|$. Proved theorem & empirical quadrature.
- `PR-RATE-4`: Exact Riccati Binary Second-Moment Benchmark. Proved analytic solution & machine-precision oracle.

- [ ] **Step 2: Update `docs/research/estimator-integrity/reproducibility.md`**

Document the exact environment, runtime, commands, seeds, and key quantitative findings for `examples/exponential_rate_sweet_spot.py`.

- [ ] **Step 3: Run full regression test suite**

```bash
conda run -n parabolab pytest
```
Expected: All tests pass.

- [ ] **Step 4: Commit documentation and registry updates**

```bash
git add docs/research/proof-registry.md docs/research/estimator-integrity/reproducibility.md
git commit -m "docs: register rate optimization theorems and update reproducibility ledger"
```
