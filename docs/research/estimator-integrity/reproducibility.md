# Estimator Integrity Reproducibility and Audit Ledger

**Historical run record.** Paths, revisions, versions, test counts, and
experiment results below describe the original estimator-integrity worktree.
They are not a statement of the current checkout or a current test run.
For the active scope and later rate/proposal checkpoint, start at the
[research index](../README.md). Merton experiments remain evidence from that
historical investigation; the multifactor application is inactive.

**Audit update, 16 September 2026:** the integrated checkout at `c82d536`
includes the subsequent flat/wave/profile certificates and mean-identification
proof. The current non-slow suite passed 255 tests, with 14 deselected; the
current Lean build and witness checks are recorded in the
[integration record](../results/integration-2026-09-16.md). The
[proof registry](../proof-registry.md) is the current claim inventory.
Corrections below separate old diagnostics from mathematical guarantees;
no old experiment was rerun or its raw output replaced for this audit.

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
- **Historical reported output paths** (not present in the current checkout):
  - `examples/dym_nonintegrability.csv`
  - `examples/dym_nonintegrability.png`
- **Method**: Logarithmic substitution $x = e^u$ with 4097 trapezoidal quadrature nodes across 12 cutoffs $\epsilon \in [10^{-1}, 10^{-12}]$.
- **Asymptotic interpretation**:
  - The theoretical slope is $2g(0)$. For the script defaults
    `mean=0.5,std=1`, this is $2e^{-1/8}/\sqrt{2\pi}$; the old ledger's
    decimal `0.7053` was incorrect.
  - The historical ledger reported a numerical slope near `0.7046` and
    an inverse-4/3 integral near `21121.67` at $\epsilon=10^{-12}$.
    Without the raw output here, those run-specific decimals are not
    independently revalidated or used as certificate inputs.
  - The conventional divergence orders are logarithmic for inverse first
    power and $\epsilon^{-1/3}$ for inverse-4/3 power.
- **Claim Role**: Corroborates the analytic divergence proved in Theorem 4.1; does not replace the proof.

### Merton--Vasicek Adaptive Proposal Experiment (Task 8)
```bash
conda run --no-capture-output -n parabolab \
  python examples/proposal_merton_vasicek.py \
  --pilot-samples 10000 --evaluation-samples 100000
```
- **Script**: `examples/proposal_merton_vasicek.py`
- **Historical reported output paths** (not present in the current checkout):
  - `examples/proposal_merton_vasicek.csv`
  - `examples/proposal_merton_vasicek.png`
- **Benchmark Target**: Reduced Merton--Vasicek $T = 0.05$, exact solution $u(0, 0) = 1.002503$.
- **Seeds Used**:
  - Pilot seeds: `101`, `102`, `103`
  - Evaluation seeds: `201`, `202`, `203`, `204`, `205`
- **Observed Proposal Shifts**:
  - Uniform baseline: $q_i = 1/6 \approx 0.1667$ across all 6 tuples.
  - Pilot square-root proposal concentrates on the dominant low-derivative pairs ($Z_0, Z_1 \approx 49.3\% \text{ and } 46.2\%$), reducing allocation to high-derivative, zero-terminal codes ($Z_2, Z_3, Z_4, Z_5 \le 1.4\%$).
  - The historical run reported empirical variance $\times$ mean nodes
    changing from $\approx 0.049$ to $\approx 0.048$, and a mean near
    $1.0025 \pm 0.0003$. Agreement over five seeds does not prove unbiasedness,
    integrability, or a population variance reduction. The pilot/freeze
    theorem preserves the target only under its support and integrability
    hypotheses; those are not established by this finite-sample comparison.

### Exponential Rate Sweet-Spot Optimization Experiment (Task 5)
```bash
conda run --no-capture-output -n parabolab \
  python examples/exponential_rate_sweet_spot.py
```
- **Script**: `examples/exponential_rate_sweet_spot.py`
- **Generated Outputs**:
  - `examples/exponential_rate_sweet_spot.csv`
  - `examples/exponential_rate_sweet_spot.png`
- **Benchmark interpretation, corrected after the historical run**:
  - The original binary rows mixed a derivative-coded estimator for $u^2$
    with the standard-binary Riccati formula
    $V(T;\lambda)=\lambda^2e^{\lambda T}/(\lambda^2+1-e^{\lambda T})$.
    The original CSV and figure therefore do not verify that oracle.
    The [corrected binary audit](../results/binary-benchmark-audit.md) uses
    the explicit `Id → (Id,Id)` mechanism at $T\in\{0.05,0.10,0.15\}$,
    with matching deterministic and untruncated Monte Carlo checks.
  - The Allen–Cahn wave sweeps at $T\in\{0.05,0.10,0.20\}$ are
    finite-depth numerical diagnostics. At $x=0$, the short-time formula
    gives the limiting rate $0.75$, not $0.72$, under the stated expansion
    hypotheses. These three horizons alone do not prove that asymptotic
    law. The JCP rate $-\log(0.95)/T$ diverges as $T\downarrow0$.
  - The Dym panel uses $N\in\{1{,}000,10{,}000,50{,}000\}$ and the rates
    $\{0.2,0.5,1,2,5\}$. Its finite-sample fluctuations are diagnostics,
    not proof of divergence or absence of a sample minimum. The separate
    conventional theorem proves infinite absolute first moment and thus
    no finite-variance optimum for the specified nondegenerate estimator.

---

## 4. Formal Research Claim Ledger

This historical selection is not the complete current registry. “Proved”
below refers to conventional proofs under the hypotheses in each source;
the final column lists only the stated Lean subresults. Numerical witnesses,
Python correctness and stochastic representation are not thereby formalized.
Use the [current registry](../proof-registry.md) for the full categories and
later certificate/mean claims.

| Claim | Description | Formal Status | Evidence / Reference | Lean Formalization |
|---|---|---|---|---|
| **Deep Result 1** | Multitype Coding-Tree Exact $L^p$ System | **Proved Theorem** | `docs/research/estimator-integrity/notation-and-moment-theorem.md` (Theorems 2.2, 2.3) | `formal/EstimatorIntegrity/MomentIteration.lean` (`momentStep_mono`, `picard_iSup_least`, `momentStep_iSup_picard`) |
| **Deep Result 2** | Dym Coding-Tree Estimator Non-Integrability | **Proved Theorem** | `docs/research/estimator-integrity/dym-nonintegrability.md` (Theorem 4.1, Corollary 4.2) | Coefficient/integral subresults in `Dym.lean`: `dym_fz0_coefficient`, `one_div_not_intervalIntegrable`, `one_div_intervalIntegral_unbounded`, `continuous_density_intervalIntegral_unbounded`; random-tree argument omitted |
| **Deep Result 3** | Safe Adaptive Pilot/Frozen Branching Proposals | **Proved under support/integrability and, for the oracle bound, pilot-error hypotheses** | `docs/research/estimator-integrity/adaptive-proposals.md` (Theorems 6.1–6.4) | Finite algebra in `Proposal.lean`: `secondMoment_ge_oracle`, `oracle_ratio_of_relative_error`, `secondMoment_uniformMixture_le`; pilot randomness and tree composition omitted |
| **Candidate 4** | State-Dependent Arbitrary-Jet Representation | **Conditional Theorem** | `docs/research/estimator-integrity/secondary-candidates.md` (§Candidate 4) | N/A (Paper-level multitype continuous-time construction) |
| **Candidate 5** | Derivative-Code Sobolev Training | **Prior-Art Overlap** | `docs/research/estimator-integrity/secondary-candidates.md` (§Candidate 5) | N/A (Czarnecki et al. 2017, Huge--Savine 2020) |
| **Candidate 6** | Robust Deep Branching | **Prior-Art Overlap** | `docs/research/estimator-integrity/secondary-candidates.md` (§Candidate 6) | N/A (Holland--Ikeda 2019, Lugosi--Mendelson 2019) |
| **Candidate 7** | Coupled Multifidelity Control Variates | **Conjecture** | `docs/research/estimator-integrity/secondary-candidates.md` (§Candidate 7) | N/A ($L^2$ coupling contraction unproved) |
| **Candidate 8** | Coefficient Sensitivities and Policy Intervals | **Conditional Theorem** | `docs/research/estimator-integrity/secondary-candidates.md` (§Candidate 8) | N/A (Requires bounded denominators and non-vanishing Hessians) |
| **Candidate 9** | Monte Carlo Challenger-Model Certificate | **Proved Theorem** | `docs/research/estimator-integrity/secondary-candidates.md` (§Candidate 9) | None; conventional metric triangle-inequality argument |
| **Candidate 10** | Short-Time Wave Proposal Optimization | **Theorem under stated asymptotic hypotheses** | `docs/research/estimator-integrity/secondary-candidates.md` (§Candidate 10) | None; conventional asymptotic analysis |
| **PR-RATE-1** | Local Exponential Rate Strict Convexity | **Proved for fixed continuation coefficients** | `docs/research/estimator-integrity/exponential-rate-optimization.md` (Theorem 7.1) | Kernel positivity and model algebra in `ExponentialRate.lean`: `expKernelFactor_pos`, `modelRateObjective_ge_amgm`, `modelRateObjective_at_optimum`, `modelObjective_eq_lower_bound_iff`; integral differentiation omitted |
| **PR-RATE-2** | Full Tree Topology Rate Convexity | **Conditional full-tree theorem** | `docs/research/estimator-integrity/exponential-rate-optimization.md` (Theorem 7.2) | `topologyFactor_pos_of_pos` only; topology measure and unrestricted convexity not formalized |
| **PR-RATE-3** | Short-Horizon $O(1)$ Scaling Law | **Local theorem; full recursion requires uniform expansions** | `docs/research/estimator-integrity/exponential-rate-optimization.md` (Theorem 7.4) | None; conventional asymptotic analysis |
| **PR-RATE-4** | Exact Riccati Binary Second-Moment Oracle | **Proved for the standard binary representation** | `docs/research/estimator-integrity/exponential-rate-optimization.md` (Theorem 7.5) | None; conventional Riccati ODE proof |

---

## 5. Audit Checklists

These checkboxes record the original worktree checkpoint only. They do not
assert that demo files never changed later, that 173 is today's test count,
or that the historical claim inventory was exhaustive.

- [x] Zero uncommitted edits in demo files (`demo/merton.py`, `demo/merton_vasicek.py` remain untouched).
- [x] Python tests pass with zero failures (173 passed).
- [x] Lean 4 project builds cleanly without `sorry`, `admit`, or non-standard `axiom`.
- [x] The original ten-claim inventory was labelled; subsequent audit corrections and expanded claims are tracked in the current proof registry.
- [x] Outlier filtering, tail trimming, and clipping strictly excluded from research experiments.
- [x] RNG default draw orders byte-identical and validated.
