# Stochastic-Rate Merton Implementation Plan

> **Archived implementation plan — status reviewed 16 September 2026.**
> State-dependent PDE support and the Vasicek examples are implemented.
> This is the original plan, not a live checklist or a completion ledger.
> Further financial-application development is inactive. The branch, dirty-file
> snapshot, commands, and agent workflow below describe the original session.
> Navigation: [archive index](../README.md), [current research](../../research/README.md),
> [documentation map](../../documentation-map.md).

> **Original workflow metadata (inactive):** This plan originally requested
> superpowers:subagent-driven-development or superpowers:executing-plans.
> Its checkbox syntax is preserved as a historical planning record.

**Goal:** Implement stochastic-interest-rate Merton HJB support via a state-dependent coding-tree mechanism, provide exact closed-form benchmark controls, and deliver a two-stage evaluation pipeline (Stage 1: fast runnable smoke code; Stage 2: full quality/error evaluation script).

**Architecture:**
- Create `parabolab/state_dependent.py` introducing `StateDependentPDEnD` and `StateDependentMechanismND`, which extend the Faà di Bruno coding-tree mechanism to nonlinearities with explicit spatial coordinates \(f(x, z)\).
- Provide analytical benchmark solutions in `parabolab/library.py` (Vasicek no-consumption exact solution via Ornstein–Uhlenbeck integrated expectation).
- Support both the reduced 1D PDE \(F(t,y)\) and the full 2D PDE \(V(t,x,y)\).
- Deliver `examples/merton_stochastic_rate.py` with `--fast` (Stage 1: ~5s smoke run) and `--full` (Stage 2: quality evaluation).

**Tech Stack:** Python 3.11, NumPy, SymPy, PyTest, PyTorch (optional deep branching).

## Original execution constraints (historical)
- Target branch: `feature/stochastic-rate-merton`.
- Never touch, overwrite, or commit existing changes in `demo/merton.py`.
- No modification to existing `tree.py` RNG drawing order or `test_tree.py` golden expectations.
- All code must run in the `parabolab` conda environment.

---

### Task 1: Exact Closed-Form Benchmark for Stochastic Rate (No-Consumption)

**Files:**
- Modify: `parabolab/library.py`
- Test: `tests/test_state_dependent.py`

**Interfaces:**
- Produces: `vasicek_no_consumption_exact(t, y, T, kappa, theta, eta, lambda_, sigma, gamma, rho)` -> `float`

- [ ] **Step 1: Write unit test for the exact Vasicek formula**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement `vasicek_no_consumption_exact` in `parabolab/library.py`**
- [ ] **Step 4: Run test to verify pass**
- [ ] **Step 5: Commit task**

---

### Task 2: State-Dependent PDE and Mechanism Implementation

**Files:**
- Create: `parabolab/state_dependent.py`
- Modify: `parabolab/__init__.py`
- Test: `tests/test_state_dependent.py`

**Interfaces:**
- Produces: `StateDependentPDEnD`, `StateDependentMechanismND`, `StateFNu`

- [ ] **Step 1: Write test for state-dependent mechanism tuple construction and evaluation**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement `StateDependentPDEnD` and `StateDependentMechanismND`**
- [ ] **Step 4: Run test to verify pass**
- [ ] **Step 5: Commit task**

---

### Task 3: Reduced and Full Merton Stochastic-Rate PDE Factories

**Files:**
- Modify: `parabolab/library.py`
- Test: `tests/test_state_dependent.py`

**Interfaces:**
- Produces: `merton_vasicek_reduced() -> StateDependentPDEnD`, `merton_vasicek_2d() -> StateDependentPDEnD`

- [ ] **Step 1: Write tests for PDE creation, lambdification, and basic Monte Carlo evaluation**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement PDE builders in `parabolab/library.py`**
- [ ] **Step 4: Run test to verify pass**
- [ ] **Step 5: Commit task**

---

### Task 4: Two-Stage Runnable Experiment Script

**Files:**
- Create: `examples/merton_stochastic_rate.py`
- Test: execute via `python examples/merton_stochastic_rate.py --fast`

**Interfaces:**
- Produces: standalone CLI script supporting `--fast` (Stage 1: smoke ~5s) and `--full` (Stage 2: evaluation)

- [ ] **Step 1: Write `examples/merton_stochastic_rate.py`**
- [ ] **Step 2: Run in `--fast` mode to verify Stage 1 (跑通代码)**
- [ ] **Step 3: Commit task**
