# Estimator Integrity Reproducibility and Audit Ledger

This document details the exact environment, git revisions, dependencies, formal proofs, test suites, seeds, numerical experiments, and formal claim ledger for the Branching Estimator Integrity research programme.

---

## 1. Environment and Pinned Toolchains

### Git Environment
- **Repository**: `/Users/michael/Desktop/NTU/fyp/parabolab`
- **Worktree**: `/Users/michael/Desktop/NTU/fyp/parabolab-estimator-integrity`
- **Branch**: `research/estimator-integrity`
- **Base Commit**: `405cfc020f5f01920e3bad380cadb96730145cd4` (Parent: `697b62b04d83e44edcfdc84d32466df2caf25dc2`)

### Python Environment
- **Conda Environment**: `parabolab`
- **Python Version**: `3.11.15`
- **PyTest Version**: `9.0.3`
- **NumPy Version**: `2.2.3` (OpenBLAS, pip build avoiding MKL OpenMP collisions)
- **SymPy Version**: `1.13.3`
- **Torch Version**: `2.6.0` (CPU)
- **Matplotlib Version**: `3.10.1`

### Lean 4 Formal Environment
- **Lean Toolchain**: `leanprover/lean4:v4.33.0` (pin in `formal/lean-toolchain`)
- **Lake Version**: `5.0.0-src+819816b` (Lean 4.33.1 compatible)
- **Mathlib Revision**: `git "https://github.com/leanprover-community/mathlib4" @ "v4.33.0"`

---

## 2. Test Suites and Execution Commands

### Baseline Test Suite (Task 1)
```bash
cd /Users/michael/Desktop/NTU/fyp/parabolab-estimator-integrity
PYTHONDONTWRITEBYTECODE=1 conda run --no-capture-output -n parabolab \
  python -m pytest -q -p no:cacheprovider
```
- **Result**: `143 passed, 13 deselected in 27.12s` (zero failures).

### Full Python Verification Suite (Task 12)
```bash
cd /Users/michael/Desktop/NTU/fyp/parabolab-estimator-integrity
PYTHONDONTWRITEBYTECODE=1 conda run --no-capture-output -n parabolab \
  python -m pytest -m "slow or not slow" -p no:cacheprovider
```
- **Result**: `173 passed in 98.93s` (zero failures, all deterministic recursion, unit, baseline, and slow Monte Carlo tests green).

### Lean 4 Build and Placeholder Scan (Tasks 9, 10, 12)
```bash
cd /Users/michael/Desktop/NTU/fyp/parabolab-estimator-integrity/formal
lake build
rg -n "\bsorry\b|admit|axiom" EstimatorIntegrity*.lean EstimatorIntegrity
```
- **Result**: Build completed successfully (`3386 jobs`).
- **Placeholder Scan**: 0 matches (`sorry`, `admit`, and custom `axiom` completely absent).

---

## 3. Numerical Experiments and Deterministic Scripts

### Dym Truncated Singular Endpoint Experiment (Task 5)
```bash
conda run --no-capture-output -n parabolab python examples/dym_nonintegrability.py
```
- **Script**: `examples/dym_nonintegrability.py`
- **Generated Outputs**:
  - `examples/dym_nonintegrability.csv`
  - `examples/dym_nonintegrability.png`
- **Method**: Logarithmic substitution $x = e^u$ with 4097 trapezoidal quadrature nodes across 12 cutoffs $\epsilon \in [10^{-1}, 10^{-12}]$.
- **Observed Asymptotic**:
  - Theoretical slope: $2 g(0) = 0.7053$
  - Numerical slope $\Delta I_1 / \Delta \log(1/\epsilon) \to 0.7046$ (agreement within $<0.1\%$).
  - Inverse-4/3 integral scales algebraically: $I_{4/3}(\epsilon) \sim \epsilon^{-1/3}$, reaching $21121.67$ at $\epsilon = 10^{-12}$.
- **Claim Role**: Corroborates the analytic divergence proved in Theorem 4.1; does not replace the proof.

### Merton--Vasicek Adaptive Proposal Experiment (Task 8)
```bash
conda run --no-capture-output -n parabolab \
  python examples/proposal_merton_vasicek.py \
  --pilot-samples 10000 --evaluation-samples 100000
```
- **Script**: `examples/proposal_merton_vasicek.py`
- **Generated Outputs**:
  - `examples/proposal_merton_vasicek.csv`
  - `examples/proposal_merton_vasicek.png`
- **Benchmark Target**: Reduced Merton--Vasicek $T = 0.05$, exact solution $u(0, 0) = 1.002503$.
- **Seeds Used**:
  - Pilot seeds: `101`, `102`, `103`
  - Evaluation seeds: `201`, `202`, `203`, `204`, `205`
- **Observed Proposal Shifts**:
  - Uniform baseline: $q_i = 1/6 \approx 0.1667$ across all 6 tuples.
  - Pilot square-root proposal concentrates on the dominant low-derivative pairs ($Z_0, Z_1 \approx 49.3\% \text{ and } 46.2\%$), reducing allocation to high-derivative, zero-terminal codes ($Z_2, Z_3, Z_4, Z_5 \le 1.4\%$).
  - Achieves variance $\times$ mean nodes reduction from $\approx 0.049$ down to $\approx 0.048$ while preserving strict unbiasedness across all 5 evaluation seeds (mean estimate $1.0025 \pm 0.0003$).

### Exponential Rate Sweet-Spot Optimization Experiment (Task 5)
```bash
conda run --no-capture-output -n parabolab \
  python examples/exponential_rate_sweet_spot.py
```
- **Script**: `examples/exponential_rate_sweet_spot.py`
- **Generated Outputs**:
  - `examples/exponential_rate_sweet_spot.csv`
  - `examples/exponential_rate_sweet_spot.png`
- **Benchmark Targets**:
  - Binary Control ($u^2$) with $\phi \equiv 1$ across $T \in \{0.05, 0.10, 0.15\}$, verified against closed-form Riccati ground truth $V(T; \lambda) = \frac{\lambda^2 e^{\lambda T}}{\lambda^2 + 1 - e^{\lambda T}}$.
  - Allen--Cahn (1D) traveling wave across $T \in \{0.05, 0.10, 0.20\}$, confirming $O(1)$ scaling $\lambda^*(T) \to 0.72$ as $T \to 0$ vs. JCP heuristic $\lambda_{\text{JCP}}(T) = -\ln(0.95)/T \to \infty$.
  - Harry Dym equation across sample sizes $N \in \{10^3, 10^4, 50^5\}$ and rates $\lambda \in [0.2, 5.0]$, confirming catastrophic non-integrability and absence of any stable interior rate minimum.

---

## 4. Formal Research Claim Ledger

Every claim is categorized into one of the seven approved categories:

| Claim | Description | Formal Status | Evidence / Reference | Lean Formalization |
|---|---|---|---|---|
| **Deep Result 1** | Multitype Coding-Tree Exact $L^p$ System | **Proved Theorem** | `docs/research/estimator-integrity/notation-and-moment-theorem.md` (Theorems 2.2, 2.3) | `formal/EstimatorIntegrity/MomentIteration.lean` (`momentStep_mono`, `picard_iSup_least`, `momentStep_iSup_picard`) |
| **Deep Result 2** | Dym Coding-Tree Estimator Non-Integrability | **Proved Theorem** | `docs/research/estimator-integrity/dym-nonintegrability.md` (Theorem 4.1, Corollary 4.2) | `formal/EstimatorIntegrity/Dym.lean` (`dym_fz0_coefficient`, `not_intervalIntegrable_one_div`, `unbounded_integral_inv`) |
| **Deep Result 3** | Safe Adaptive Pilot/Frozen Branching Proposals | **Proved Theorem** | `docs/research/estimator-integrity/adaptive-proposals.md` (Theorems 6.1–6.4) | `formal/EstimatorIntegrity/Proposal.lean` (`secondMoment_ge_oracle`, `oracle_ratio_bound`, `secondMoment_mixture_floor`) |
| **Candidate 4** | State-Dependent Arbitrary-Jet Representation | **Conditional Theorem** | `docs/research/estimator-integrity/secondary-candidates.md` (§Candidate 4) | N/A (Paper-level multitype continuous-time construction) |
| **Candidate 5** | Derivative-Code Sobolev Training | **Prior-Art Overlap** | `docs/research/estimator-integrity/secondary-candidates.md` (§Candidate 5) | N/A (Czarnecki et al. 2017, Huge--Savine 2020) |
| **Candidate 6** | Robust Deep Branching | **Prior-Art Overlap** | `docs/research/estimator-integrity/secondary-candidates.md` (§Candidate 6) | N/A (Holland--Ikeda 2019, Lugosi--Mendelson 2019) |
| **Candidate 7** | Coupled Multifidelity Control Variates | **Conjecture** | `docs/research/estimator-integrity/secondary-candidates.md` (§Candidate 7) | N/A ($L^2$ coupling contraction unproved) |
| **Candidate 8** | Coefficient Sensitivities and Policy Intervals | **Conditional Theorem** | `docs/research/estimator-integrity/secondary-candidates.md` (§Candidate 8) | N/A (Requires bounded denominators and non-vanishing Hessians) |
| **Candidate 9** | Monte Carlo Challenger-Model Certificate | **Proved Theorem** | `docs/research/estimator-integrity/secondary-candidates.md` (§Candidate 9) | Algebraic metric triangle inequality derivation |
| **Candidate 10** | Short-Time Wave Proposal Optimization | **Proved Theorem** | `docs/research/estimator-integrity/secondary-candidates.md` (§Candidate 10) | Asymptotic variance expansion & joint $(\gamma, q)$ minimization |
| **PR-RATE-1** | Local Exponential Rate Strict Convexity | **Proved Theorem** | `docs/research/estimator-integrity/exponential-rate-optimization.md` (§Thm 1.1) | `formal/EstimatorIntegrity/ExponentialRate.lean` (`singleEventKernelFactor_pos`, `modelRateObjective_ge_amgm`, `modelRateObjective_at_optimum`, `modelObjective_eq_lower_bound_iff`) |
| **PR-RATE-2** | Full Tree Topology Rate Convexity | **Proved Theorem** | `docs/research/estimator-integrity/exponential-rate-optimization.md` (§Thm 2.1) | `formal/EstimatorIntegrity/ExponentialRate.lean` (`topologyFactor_pos_of_pos`) |
| **PR-RATE-3** | Short-Horizon $O(1)$ Scaling Law | **Proved Theorem** | `docs/research/estimator-integrity/exponential-rate-optimization.md` (§Thm 3.1) | N/A (Taylor asymptotic series) |
| **PR-RATE-4** | Exact Riccati Binary Second-Moment Oracle | **Proved Theorem** | `docs/research/estimator-integrity/exponential-rate-optimization.md` (§Thm 4.1) | N/A (Closed-form Riccati differential equation) |

---

## 5. Audit Checklists

- [x] Zero uncommitted edits in demo files (`demo/merton.py`, `demo/merton_vasicek.py` remain untouched).
- [x] Python tests pass with zero failures (173 passed).
- [x] Lean 4 project builds cleanly without `sorry`, `admit`, or non-standard `axiom`.
- [x] All 10 claims labelled with exact mathematical statuses.
- [x] Outlier filtering, tail trimming, and clipping strictly excluded from research experiments.
- [x] RNG default draw orders byte-identical and validated.
