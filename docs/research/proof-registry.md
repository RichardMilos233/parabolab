# Formal and Conventional Proof Registry

**Status:** navigation and claim inventory for the `parabolab` research programme; entries must be checked against their underlying proofs.
**Last-reviewed commit:** `ce2949330fcff1a3faf56c8a0ff36628586b242d`
**Scope:** all mathematical theorems, conditional representations, Lean-formalized lemmas, conjectures, and priority claims across estimator integrity and multifactor Merton research.

**Current decision (12 September 2026):** the active FYP concerns reliable
exponential-rate and tuple-proposal selection. Multidimensional Merton is not
the selected application; its records below are historical. See the
[research checkpoint](lambda-q-optimization-summary.md) and the new
[general rate-selection arguments](estimator-integrity/general-rate-selection.md).
The new all-code moment/cutoff arguments are conventional mathematics, not
additional Lean-checked statements or an implemented certified optimizer.

---

## Registry Design and Category Discipline

This registry provides a durable, atomic record of every mathematical claim across the project. It enforces strict category discipline:

1. **Complete conventional proof:** mathematically established on paper from explicitly stated axioms or hypotheses; all analytical and probabilistic steps complete.
2. **Conditional theorem / representation:** algebraic or formal identity proved completely; equivalence to the infinite random functional or PDE solution requires explicit unverified hypotheses (e.g., non-explosion, $L^1/L^2$ integrability, mild-system uniqueness, or boundary regularity).
3. **Proof sketch / proof route:** structural outline indicating intermediate steps without a complete analytical closing.
4. **Lean-formalized substatement:** mechanically verified in Lean 4 without `sorry`, `admit`, or non-standard `axiom`; linked *strictly* to the finite algebraic or order-theoretic substatement proved, with omitted probabilistic and analytical obligations explicitly listed.
5. **Symbolic, deterministic, or Monte Carlo evidence:** numerical simulations, computer-algebra validations, or quadrature; corroborates a claim but is explicitly distinguished from proof.
6. **Conjecture:** formulated hypothesis without complete mathematical proof.
7. **Engineering contribution:** software architecture, algorithmic pipeline, test suite, or numerical optimization.
8. **Novelty claim with literature boundary:** scoped literature review finding no prior combination; never asserted as absolute historical priority.

---

## Master Table of Claims

| Claim ID | Title / Short Name | Mathematical Status | Primary Proof Location | Lean 4 Coverage | Numerical / Symbolic Evidence | Novelty / Priority Status |
|---|---|---|---|---|---|---|
| `PR-MOM-1` | Finite-Depth Killed Tree Identity | Proved Theorem | `notation-and-moment-theorem.md` §Def 2.1 | None (related algebraic definitions in `FiniteTree.lean`) | Python unit tests (`test_moments.py`) | Classical tree killing |
| `PR-MOM-2` | Exact Multitype $p$-Moment Recursion | Proved Theorem | `notation-and-moment-theorem.md` §Thm 2.2 | `FiniteTree.lean` (`momentStep`) | Gauss-Legendre quadrature match | Coding-tree extension of branching identities |
| `PR-MOM-3` | Minimal Fixed Point & $L^p$ Criterion | Proved Theorem | `notation-and-moment-theorem.md` §Thm 2.3 | `MomentIteration.lean` (5 lemmas) | Fixed-point Picard iteration tests | Established smoothing transform / branching theory |
| `PR-DYM-1` | Dym $f_{z_0}$ Odd Singularity | Proved Theorem | `dym-nonintegrability.md` §Terminal Identities | `Dym.lean` (`dym_fz0_coefficient`) | SymPy jet differentiation | Novel verification for JEQ Fig 6 instance |
| `PR-DYM-2` | Dym Absolute First-Moment Divergence | Proved Theorem | `dym-nonintegrability.md` §Thm 4.1 | `Dym.lean` (`one_div_not_intervalIntegrable`, `continuous_density_intervalIntegral_unbounded`) | Trapezoidal log-quadrature (`examples/dym_nonintegrability.py`) | Scoped search: first Dym-specific coding-tree proof |
| `PR-DYM-3` | Dym Signed-Part Divergence ($\infty - \infty$) | Proved Theorem | `dym-nonintegrability.md` §Cor 4.2 | None (unformalized signed event decomposition) | Bounded Cauchy principal-value analysis | Scoped search: first Dym-specific coding-tree proof |
| `PR-PROP-1` | Simplex Square-Root Tuple Optimizer | Proved Theorem | `adaptive-proposals.md` §Thm 6.1 | `Proposal.lean` (`secondMoment_ge_oracle`, `secondMoment_sqrtProposal_eq`) | Matrix-Riccati proposal comparison | Classical Cauchy-Schwarz / optimal sampling |
| `PR-PROP-2` | Unconstrained Event-Time Optimizer | Proved Theorem | `adaptive-proposals.md` §Thm 6.2 | None (continuous-time measure decomposition) | 1D numerical quadrature on $(0, \Delta)$ | Generalization of Poisson split |
| `PR-PROP-3` | Pilot/Frozen Proposal Exact Unbiasedness | Proved Theorem | `adaptive-proposals.md` §Thm 6.3 | None (pilot $\sigma$-algebra / tower property) | 5-seed Merton-Vasicek MC experiment | Established multi-stage Monte Carlo |
| `PR-PROP-4` | Multiplicative Finite-Depth Oracle Bound | Proved Theorem | `adaptive-proposals.md` §Thm 6.4 | `Proposal.lean` (`sqrtProposal_ratio_bounds`, `oracle_ratio_of_relative_error`, `secondMoment_uniformMixture_le`) | Simulated pilot error runs | Branching tree-depth composition theorem |
| `PR-RATE-1` | Local Exponential Rate Strict Convexity | Proved Theorem | `exponential-rate-optimization.md` §Thm 7.1 | `ExponentialRate.lean` (`singleEventKernelFactor_pos`, `modelRateObjective_ge_amgm`, `modelRateObjective_at_optimum`, `modelObjective_eq_lower_bound_iff`) | Quadrature derivatives vs finite differences | Related to classical importance-sampling convexity |
| `PR-RATE-2` | Tree Topology Rate Convexity | Conditional full-tree theorem | `exponential-rate-optimization.md` §Thm 7.2 | `ExponentialRate.lean` (`topologyFactor_pos_of_pos`) only | Deterministic recursive derivatives | Topology-level coding tree convexity; finite variance separate |
| `PR-RATE-3` | Short-Horizon $O(1)$ Scaling Law | Local theorem; full recursion conditional | `exponential-rate-optimization.md` §Thm 7.4 | None (Taylor asymptotic analysis) | 1D Allen-Cahn / Riccati quadrature sweeps | Requires nonzero terminal terms and uniform expansions |
| `PR-RATE-4` | Exact Riccati Binary Second-Moment Oracle | Proved for standard binary representation | `exponential-rate-optimization.md` §Thm 7.5 | None (ODEs) | Analytic formula (`riccati_binary_second_moment`) | Not the derivative-coded estimator of the same PDE |
| `PR-RATE-5` | General Rate Selection and Cutoff Certificates | Conventional theorems under stated hypotheses | `general-rate-selection.md` §§2–5 | None | `test_sampling_tuning.py` checks engineering only | Explicit all-code bound and selection gap; novelty unestablished; certified numerics not implemented |
| `PR-SEC-4` | State-Dependent Arbitrary-Jet Representation | Conditional Theorem | `secondary-candidates.md` §Cand 4 | None (unformalized multi-index jet algebra) | SymPy jet chain-rule checks | Candidate contribution; nearby prior art |
| `PR-SEC-5` | Derivative-Code Sobolev Training | Prior-Art Overlap | `secondary-candidates.md` §Cand 5 | None | Deep branching gradient supervision | Overlap: Czarnecki (2017), Huge-Savine (2020) |
| `PR-SEC-6` | Robust Deep Branching Median-of-Means | Prior-Art Overlap | `secondary-candidates.md` §Cand 6 | None | Outlier filter comparison study | Overlap: Lugosi-Mendelson (2019), Catoni (2012) |
| `PR-SEC-7` | Coupled Multifidelity Control Variates | Conjecture | `secondary-candidates.md` §Cand 7 | None | Correlated shared-clock simulations | Conjecture ($L^2$ contraction unproved) |
| `PR-SEC-8` | Pathwise Coefficient Greeks & Policy Bands | Conditional Theorem | `secondary-candidates.md` §Cand 8 | None | Pathwise count vs finite differences | Classical simulation sensitivity; conditional on denominators |
| `PR-SEC-9` | Challenger-Model $2r$ Selection Certificate | Proved Theorem | `secondary-candidates.md` §Cand 9 | None | Metric triangle inequality verification | Triangle inequality application; audit protocol |
| `PR-SEC-10` | Short-Time Wave Proposal Asymptotics | Proved Theorem | `secondary-candidates.md` §Cand 10 | None | d'Alembert branch simulator in `wavelab` | Specific joint asymptotic minimization |
| `PR-MM-1` | Optimized Factor Merton HJB Equation | Proved Algebraic Theorem | `multifactor-merton-proofs.md` §Thm MM-1 | None | SymPy Hamiltonian optimization | Classical dynamic programming (Merton 1971) |
| `PR-MM-2` | CRRA Wealth Homogeneity State Reduction | Proved Theorem | `multifactor-merton-proofs.md` §Thm MM-2 | None | SymPy power substitution | Classical scaling reduction |
| `PR-MM-2.1` | Asset Count vs PDE Dimension Decoupling | Proved Theorem | `multifactor-merton-proofs.md` §Cor MM-2.1 | None | Analytical matrix rank check | Classical financial insight |
| `PR-MM-3` | Short-Time No-One-Index Obstruction | Proved Theorem | `multifactor-merton-proofs.md` §Thm MM-3 | None | Hessian rank evaluations | New checkable rank condition for 2D benchmarks |
| `PR-MM-4` | Exponential-Quadratic Matrix-Riccati Solution | Proved Theorem | `multifactor-merton-proofs.md` §Thm MM-4 | None | SciPy matrix Riccati integrator | Extends Liu (2007) / Kim-Omberg (1996) |
| `PR-MM-5` | CRRA Artificial Wealth Diffusion Obstruction | Proved Theorem | `multifactor-merton-proofs.md` §Thm MM-5 | None | Gaussian negative-tail calculation | Identifies invalidity of Gaussian wealth in trees |
| `PR-MM-6` | Full-Covariance State-Dependent Mechanism | Proved Theorem | `multifactor-merton-proofs.md` §Thm MM-6 | None | SymPy Duhamel source expansion | Core algebraic mechanism identity |
| `PR-MM-7` | Conditional Full-Covariance Representation | Conditional Theorem | `multifactor-merton-proofs.md` §Thm MM-7 | None | Prototype Vasicek tree tests | Conditional on 7 stated analytical hypotheses |

---

## Detailed Claim Records

### Family 1: Moment Iteration and Integrability

#### `PR-MOM-1`: Finite-Depth Killed Tree Identity
- **Exact Statement:** On every nonexplosive realization of a continuous-time coding tree $\mathcal T$, the generation-killed functional satisfies $|H_{t,x,c}^{[n]}|^p = |H_{t,x,c}|^p \mathbf 1_{\{\operatorname{depth}(\mathcal T)\le n\}}$, and $|H_{t,x,c}^{[n]}|^p \uparrow |H_{t,x,c}|^p$ almost surely as $n \to \infty$.
- **Source:** `docs/research/estimator-integrity/notation-and-moment-theorem.md`, Definition 2.1 & Eq. (2.1)–(2.2).
- **Assumptions:**
  - *Structural:* Finite branching arity per tuple ($k_\ell \ge 1$); non-explosive particle generation.
  - *Analytic:* Measurable tree evaluators; $p > 0$.
  - *Probabilistic:* Realized factors finite almost surely.
  - *Integrability:* None (identity holds pointwise in $[0, \infty]$).
  - *Uniqueness:* None.
  - *Domain:* Standard Borel state space $E$.
- **Conventional Proof Status:** Proved theorem. Complete combinatorial induction on generation paths in `notation-and-moment-theorem.md` §2.
- **Lean 4 Coverage:**
  - *Formalized:* Algebraic step definition `EstimatorIntegrity.FiniteMechanism` and `momentStep` in `formal/EstimatorIntegrity/FiniteTree.lean`.
  - *Omitted Obligations:* Probability space $(\Omega, \mathcal F, \mathbb P)$, continuous-time Poisson clocks, Brownian paths, almost-sure convergence of random indicators.
- **Implementation Correspondence:** `parabolab/tree.py::_tree` with `max_depth` parameter.
- **Empirical / Symbolic Evidence:** Python unit tests verifying exact sample equality when $\operatorname{depth} \le n$ and zero return otherwise.
- **Novelty / Prior Art:** Standard probabilistic technique for branching processes; adapted to operator-coded trees.
- **Dependencies & Open Obligations:** Basis for `PR-MOM-2` and `PR-MOM-3`.

---

#### `PR-MOM-2`: Exact Multitype $p$-Moment Recursion
- **Exact Statement:** The shifted finite-depth moments $V_{c,n+1}^{(p)}(t,x) = \mathbb E|H_{t,x,c}^{[n]}|^p$ satisfy the closed integral recursion:
  $$V_{c,n+1}^{(p)}(t,x) = \bar F_c(\Delta)^{1-p}P_\Delta|g_c|^p(x) + \sum_{\ell\in L_c} q_c(Z_{c,\ell})^{1-p} \int_0^\Delta \rho_c(s)^{1-p} P_s\left[\prod_{z\in Z_{c,\ell}} V_{z,n}^{(p)}(t+s,\cdot)\right](x)\,ds.$$
- **Source:** `docs/research/estimator-integrity/notation-and-moment-theorem.md`, Theorem 2.2, Eq. (2.4).
- **Assumptions:**
  - *Structural:* Countable code space $\mathcal C$; finite non-empty mechanism tables $\mathcal M(c)$; coefficient-encoded convention.
  - *Analytic:* Positive lifetime density $\rho_c(s) > 0$ a.e.; positive survival tail $\bar F_c(\Delta) > 0$.
  - *Probabilistic:* (H5) Children share the Markov branch position; (H6) Conditional child independence given branch position and first event.
  - *Integrability:* None (identities take values in $[0, \infty]$; Tonelli applied to nonnegative integrands).
  - *Uniqueness:* None.
  - *Domain:* Transition kernel on standard Borel space $E$.
- **Conventional Proof Status:** Proved theorem. Rigorous Tonelli integration over shared position and independent child subtrees in `notation-and-moment-theorem.md` §2.
- **Lean 4 Coverage:**
  - *Formalized:* Finite algebraic sum and product step `momentStep` in `formal/EstimatorIntegrity/FiniteTree.lean`.
  - *Omitted Obligations:* Spatial Markov semigroup $P_s$, continuous time integral $\int_0^\Delta ds$, Tonelli theorem on product measure.
- **Implementation Correspondence:** `parabolab/moments.py::MomentSystem`.
- **Empirical / Symbolic Evidence:** Gauss-Legendre quadrature of recursion matches sample empirical moments for low-order polynomial semilinear equations.
- **Novelty / Prior Art:** Generalizes classical branching moment equations to multitype arbitrary-jet operator codes.
- **Dependencies & Open Obligations:** Requires (H5) shared-position property (JCP Alg 1 violation trap).

---

#### `PR-MOM-3`: Minimal Fixed Point and Pointwise $L^p$ Criterion
- **Exact Statement:** The sequence $V_n = \Phi_p^n(0)$ increases monotonically to $V_c(t,x) = \mathbb E|H_{t,x,c}|^p \in [0, \infty]$, which is the minimal nonnegative fixed point of $\Phi_p$. Hence $H_{t,x,c} \in L^p \iff V_c(t,x) < \infty$.
- **Source:** `docs/research/estimator-integrity/notation-and-moment-theorem.md`, Theorem 2.3, Eq. (2.6)–(2.9).
- **Assumptions:**
  - *Structural:* Hypotheses (H1)–(H7), including almost-sure non-explosion.
  - *Analytic:* Monotone continuity from below of polynomial products on $[0, \infty]$.
  - *Probabilistic:* Monotone convergence theorem for nonnegative indicators.
  - *Integrability:* None assumed; finite moment is the conclusion.
  - *Uniqueness:* Minimal fixed point; non-minimal fixed points can exist.
  - *Domain:* Standard Borel state space $E$.
- **Conventional Proof Status:** Proved theorem. Complete fixed-point proof in `notation-and-moment-theorem.md` §2.
- **Lean 4 Coverage:**
  - *Formalized:* Mechanically verified in `formal/EstimatorIntegrity/MomentIteration.lean`:
    - `momentStep_mono`: operator monotonicity on `ENNReal`.
    - `picard_iSup_least`: least fixed-point property over all pre-fixed points.
    - `momentStep_iSup_picard`: continuity from below ($\Phi(\sup V_n) = \sup \Phi(V_n)$).
  - *Omitted Obligations:* Identification of the abstract Picard limit with the continuous-time random tree functional $\mathbb E|H|^p$.
- **Implementation Correspondence:** `parabolab/moments.py::iterate_moments`.
- **Empirical / Symbolic Evidence:** Monotone convergence observed in numerical iteration for Allen-Cahn and Merton models.
- **Novelty / Prior Art:** Well-known fixed-point structure for branching diffusions; explicit multitype coding formulation is repo-specific.
- **Dependencies & Open Obligations:** Foundation for proposal optimization and moment explosion boundaries.

---

### Family 2: Dym Equation Non-Integrability

#### `PR-DYM-1`: Dym Mechanism Terminal Derivative Singularities
- **Exact Statement:** For the Dym equation $u_t + u^3 u_{xxx} = 0$ with terminal condition $\phi_\alpha(x) = |3\alpha x|^{2/3}$, the reduced mechanism contains the live tuple $Z_* = ((f_{z_2})^*, (f_{z_0})^*, D^2)$ with exact terminal evaluations:
  $$f_{z_2} = -\frac12, \qquad f_{z_0}(\phi_\alpha, J\phi_\alpha) = \frac{8\alpha^2}{x}, \qquad \phi_\alpha''(x) = -\frac{2|3\alpha|^{2/3}}{9}|x|^{-4/3}.$$
- **Source:** `docs/research/estimator-integrity/dym-nonintegrability.md` §Terminal identities, Eq. (4.14).
- **Assumptions:**
  - *Structural:* Full-jet mechanism expansion with zero-tuple reduction.
  - *Analytic:* Two-sided symmetric extension of fractional power $|x|^{2/3}$; nonzero parameter $\alpha \ne 0$.
  - *Domain:* $x \in \mathbb R \setminus \{0\}$.
- **Conventional Proof Status:** Proved theorem. Verified on both positive and negative half-lines with exact sign tracking.
- **Lean 4 Coverage:**
  - *Formalized:* `EstimatorIntegrity.Dym.dym_fz0_coefficient` in `formal/EstimatorIntegrity/Dym.lean` verifies $(3 C^2 (8 C / 27)) / x = 8\alpha^2 / x$ given $C^3 = 9\alpha^2$.
  - *Omitted Obligations:* Derivative of $|x|^{2/3}$ on $\mathbb R \setminus \{0\}$; Faà di Bruno multitype table expansion.
- **Implementation Correspondence:** `parabolab/library.py::dym_1d`.
- **Empirical / Symbolic Evidence:** SymPy symbolic differentiation in test suite.
- **Novelty / Prior Art:** Specific to JEQ2023 §5.1 / Figure 6 benchmark.
- **Dependencies & Open Obligations:** Feeds directly into `PR-DYM-2`.

---

#### `PR-DYM-2`: Dym Absolute First-Moment Divergence ($L^1$ Explosion)
- **Exact Statement:** For every starting state $x \in \mathbb R$, positive horizon $T - t > 0$, rate $\lambda > 0$, and non-zero parameter $\alpha \ne 0$, the uniform full-support coding-tree functional satisfies $\mathbb E|H_{t,x,\mathrm{Id}}| = \infty$.
- **Source:** `docs/research/estimator-integrity/dym-nonintegrability.md`, Theorem 4.1, Eq. (4.27).
- **Assumptions:**
  - *Structural:* Full-support proposal assigning positive probability $q_* > 0$ to $Z_*$.
  - *Analytic:* Horizon $h = T - t > 0$; $\alpha \ne 0$.
  - *Probabilistic:* Continuous Gaussian transition density $g_{y,\delta}(0) > 0$ across zero.
  - *Integrability:* Not integrable.
  - *Domain:* $x \in \mathbb R$.
- **Conventional Proof Status:** Proved theorem. Complete proof isolating the 5-particle topology $E_*$ and proving divergence via continuous lower-bounding of Gaussian density in `dym-nonintegrability.md` §4.
- **Lean 4 Coverage:**
  - *Formalized:* In `formal/EstimatorIntegrity/Dym.lean`:
    - `one_div_not_intervalIntegrable`: non-integrability of $1/x$ across origin.
    - `one_div_intervalIntegral_unbounded`: truncated integrals $\int_\delta^\varepsilon x^{-1} dx$ exceed any bound.
    - `continuous_density_intervalIntegral_unbounded`: preserves divergence when multiplied by continuous positive density $g(x) > 0$.
  - *Omitted Obligations:* 5-particle tree probability measure, Brownian bridge conditioning, Tonelli over $(\tau_1, \tau_2, Y)$.
- **Implementation Correspondence:** `examples/dym_nonintegrability.py`.
- **Empirical / Symbolic Evidence:** Trapezoidal quadrature across 12 cutoffs $\varepsilon \in [10^{-1}, 10^{-12}]$ confirms $\Delta I_1 / \Delta \log(1/\varepsilon) \to 2 g(0) = 0.7046$ ($<0.1\%$ error).
- **Novelty / Prior Art:** Scoped search found no prior Dym-specific coding-tree proof; publication priority is not established (see safe-language standards in roadmap §10).
- **Dependencies & Open Obligations:** Explains why empirical Monte Carlo appears stable (rare origin visits) while formal variance and mean do not exist.

---

#### `PR-DYM-3`: Dym Signed-Part Divergence ($\mathbb E[H^+] = \mathbb E[H^-] = \infty$)
- **Exact Statement:** Under the hypotheses of `PR-DYM-2`, both positive and negative parts diverge: $\mathbb E[H^+] = \infty$ and $\mathbb E[H^-] = \infty$. The random variable has no extended-real expectation ($\infty - \infty$).
- **Source:** `docs/research/estimator-integrity/dym-nonintegrability.md`, Corollary 4.2, Eq. (4.34).
- **Assumptions:** Identical to `PR-DYM-2`, plus sign-preservation of auxiliary terminal factors ($\phi_\alpha''(r) < 0$ on $K = [1, 2]$).
- **Conventional Proof Status:** Proved theorem. Complete proof in `dym-nonintegrability.md` §4 showing $\operatorname{sgn}(H) = \operatorname{sgn}(X^{(0)})$ on $E_* \cap \{X^{(D)} \in K\}$.
- **Lean 4 Coverage:** None directly formalized for the signed half-line split (formalized unbounded integral applies to the one-sided case).
- **Implementation Correspondence:** Evaluated in `demo/dym.py`.
- **Empirical / Symbolic Evidence:** Cauchy principal-value convergence observed under symmetric truncation, but Lebesgue integral is undefined.
- **Novelty / Prior Art:** Rigorous refutation of apparent convergence claims for Dym branching trees.
- **Dependencies & Open Obligations:** Prevents unjustified claims of unbiasedness for Dym.

---

### Family 3: Adaptive Proposals and Variance Reduction

#### `PR-PROP-1`: Simplex Square-Root Tuple Optimizer
- **Exact Statement:** For finite positive continuation second moments $A_i > 0$, the objective $J(q) = \sum_{i=1}^m A_i / q_i$ on the open probability simplex is uniquely minimized by $q_i^* = \sqrt{A_i} / \sum_j \sqrt{A_j}$, with minimal value $(\sum_i \sqrt{A_i})^2$.
- **Source:** `docs/research/estimator-integrity/adaptive-proposals.md`, Theorem 6.1, Eq. (6.3)–(6.4).
- **Assumptions:**
  - *Structural:* Finite mechanism table $m \ge 1$.
  - *Analytic:* Continuation second moments $A_i > 0$.
  - *Domain:* Probability simplex $\sum q_i = 1, q_i > 0$.
- **Conventional Proof Status:** Proved theorem. Cauchy-Schwarz on $\mathbb R^m$ with equality condition in `adaptive-proposals.md` §6.
- **Lean 4 Coverage:**
  - *Formalized:* In `formal/EstimatorIntegrity/Proposal.lean`:
    - `secondMoment_ge_oracle`: Cauchy-Schwarz inequality $(\sum \sqrt{A_i})^2 \le \sum A_i / q_i$.
    - `secondMoment_sqrtProposal_eq`: attainment of lower bound by `sqrtProposal`.
  - *Omitted Obligations:* None for the finite algebraic statement.
- **Implementation Correspondence:** `parabolab/proposals.py::optimal_tuple_proposal`.
- **Empirical / Symbolic Evidence:** Verified numerically in Merton-Vasicek pilot experiments.
- **Novelty / Prior Art:** Classical Neyman-style optimal allocation adapted to branching tree tuples.
- **Dependencies & Open Obligations:** Core building block for `PR-PROP-4`.

---

#### `PR-PROP-2`: First-Event Unconstrained Leaf/Branch Optimizer
- **Exact Statement:** On horizon $\Delta = T - t$, for leaf second moment $A_0 \ge 0$ and branch second-moment density $A(s)$, the unconstrained distribution $(r_0, r(s))$ minimizing $A_0 / r_0 + \int_0^\Delta (A(s)/r(s)) ds$ is $r_0^* = \sqrt{A_0}/C$, $r^*(s) = \sqrt{A(s)}/C$ where $C = \sqrt{A_0} + \int_0^\Delta \sqrt{A(s)} ds$.
- **Source:** `docs/research/estimator-integrity/adaptive-proposals.md`, Theorem 6.2, Eq. (6.13)–(6.14).
- **Assumptions:**
  - *Structural:* Single first-event horizon $\Delta > 0$.
  - *Analytic:* Measurable density $A(s)$; finite normalizing constant $0 < C < \infty$.
  - *Domain:* Probability measure on $\{\text{leaf}\} \cup (0, \Delta)$.
- **Conventional Proof Status:** Proved theorem. $L^2(\nu)$ Cauchy-Schwarz with measure $\nu = \delta_{\text{leaf}} + \operatorname{Leb}|_{(0, \Delta)}$.
- **Lean 4 Coverage:** None (requires measure spaces with mixed atom and Lebesgue component).
- **Implementation Correspondence:** Prototyped in `parabolab/proposals.py`.
- **Empirical / Symbolic Evidence:** Quadrature confirmation on 1D test functions.
- **Novelty / Prior Art:** Clarifies why exponential clocks $\lambda e^{-\lambda s}$ are strictly constrained one-parameter subfamilies that cannot achieve $r^*(s)$ in general.
- **Dependencies & Open Obligations:** Prevents conflating optimal lifetime laws with scalar rate optimization.

---

#### `PR-PROP-3`: Pilot/Frozen Proposal Exact Unbiasedness
- **Exact Statement:** Let pilot $\sigma$-algebra $\mathcal P$ determine frozen proposal $\widehat q \ge q_{\min} > 0$. If evaluation trees use fresh randomness conditional on $\mathcal P$ and target mean $u$ is finite with conditional $L^1$ integrability, then $\mathbb E[\widehat H \mid \mathcal P] = u$ a.s. and $\mathbb E[\widehat H] = u$.
- **Source:** `docs/research/estimator-integrity/adaptive-proposals.md`, Theorem 6.3, Eq. (6.23).
- **Assumptions:**
  - *Structural:* Frozen proposal measurable with respect to pilot $\mathcal P$.
  - *Analytic:* Full conditional support $\widehat q_h(i) \ge q_{\min} > 0$.
  - *Probabilistic:* Fresh evaluation randomness; tower property of conditional expectation.
  - *Integrability:* Finite target mean $u$; conditional $L^1$ integrability $\mathbb E[|\widehat H| \mid \mathcal P] < \infty$ a.s.; non-explosion and $L^1$ killed-depth passage.
- **Conventional Proof Status:** Proved theorem. Complete finite-depth topology sum cancellation and $L^1$ limit in `adaptive-proposals.md` §6.
- **Lean 4 Coverage:** None (requires abstract probability spaces, conditional expectations, and $\sigma$-algebras).
- **Implementation Correspondence:** `examples/proposal_merton_vasicek.py`.
- **Empirical / Symbolic Evidence:** 5 evaluation seeds on Merton-Vasicek $T = 0.05$ yield mean $1.0025 \pm 0.0003$ vs exact $1.002503$.
- **Novelty / Prior Art:** Standard adaptive Monte Carlo principle rigorously documented for branching mechanisms to forbid within-sample unweighted adaptation.
- **Dependencies & Open Obligations:** Essential safety rule for any machine-learning or adaptive proposal scheme.

---

#### `PR-PROP-4`: Multiplicative Finite-Depth Oracle Bound
- **Exact Statement:** If pilot estimates satisfy $(1-\eta) A_i \le \widehat A_i \le (1+\eta) A_i$ with $\eta \in [0, 1)$, then the plug-in square-root proposal satisfies $J(\widehat q) \le \kappa_\eta J(q^*)$ where $\kappa_\eta = \sqrt{(1+\eta)/(1-\eta)}$. With uniform mixture floor $\varepsilon$, $J(\widetilde q) \le \frac{\kappa_\eta}{1-\varepsilon} J(q^*)$. For a tree of depth $n$ with at most $B_n$ decisions, $\mathbb E_{\widetilde q}|H^{[n]}|^2 \le \left(\frac{\kappa_\eta}{1-\varepsilon}\right)^{B_n} \mathbb E_{q^*}|H^{[n]}|^2$.
- **Source:** `docs/research/estimator-integrity/adaptive-proposals.md`, Theorem 6.4, Eq. (6.38), (6.40), (6.50).
- **Assumptions:**
  - *Structural:* Finite depth $n < \infty$; bounded tuple branching factor $B_n < \infty$.
  - *Analytic:* Componentwise relative pilot error $\eta < 1$; mixture floor $\varepsilon < 1$.
  - *Probabilistic:* Simultaneous concentration event $\mathcal E_{\eta,n}$.
- **Conventional Proof Status:** Proved theorem. Complete algebraic derivation and topology-product induction in `adaptive-proposals.md` §6.
- **Lean 4 Coverage:**
  - *Formalized:* In `formal/EstimatorIntegrity/Proposal.lean`:
    - `sqrtProposal_ratio_bounds`: proposal ratio bounded in $[\kappa_\eta^{-1}, \kappa_\eta]$.
    - `oracle_ratio_of_relative_error`: $J(\widehat q) \le \kappa_\eta J(q^*)$.
    - `secondMoment_uniformMixture_le`: mixture penalty bounded by $1/(1-\varepsilon)$.
  - *Omitted Obligations:* Inductive tree composition exponent $B_n$; probability of concentration event $\mathbb P(\mathcal E_{\eta, n}) \ge 1 - \delta$.
- **Implementation Correspondence:** Evaluated in `examples/proposal_merton_vasicek.py`.
- **Empirical / Symbolic Evidence:** Pilot experiments confirm variance stays within oracle multiplier.
- **Novelty / Prior Art:** Multiplicative error propagation specific to branching coding trees.
- **Dependencies & Open Obligations:** Explains why adaptive gains can degrade if pilot error compounds over deep trees.

---

### Family 4: Secondary Estimator-Integrity Candidates

#### `PR-SEC-4`: State-Dependent Arbitrary-Jet Representation
- **Exact Statement:** A coding-tree mechanism with codes $G_{a,\beta,\nu} = (a \partial_x^\beta \partial_z^\nu f)^*$ representing $\partial_t u + \frac{\sigma^2}{2} \Delta u + f(x, Ju) = 0$ via explicit spatial and jet product expansions.
- **Source:** `docs/research/estimator-integrity/secondary-candidates.md` §Candidate 4, Eq. (4.7)–(4.9).
- **Assumptions:** Smoothness $C^{1,\infty}$; constant isotropic diffusion $\sigma^2 I$; commuting spatial derivatives; positive proposal probabilities; non-explosion; absolute integrability; mild system uniqueness.
- **Conventional Proof Status:** Conditional theorem. Mechanism algebra proved by multivariate chain rule; stochastic representation conditional on 7 stated hypotheses.
- **Lean 4 Coverage:** None.
- **Implementation Correspondence:** Isotropic prototype in `parabolab/library.py`.
- **Empirical / Symbolic Evidence:** SymPy differentiation checks for low-degree polynomials.
- **Novelty / Prior Art:** Henry-Labordère et al. (2019) treat semilinear gradient diffusions; Nguwi et al. (2023) treat state-independent arbitrary jets. Intersection is candidate novelty.
- **Dependencies & Open Obligations:** Predecessor to full-covariance Merton mechanism `PR-MM-6`.

---

#### `PR-SEC-5`: Derivative-Code Sobolev Training
- **Exact Statement:** Training a neural network against direct derivative tree labels $Y_\mu$ minimizes the population Sobolev projection: $\mathcal R(v) = \sum_\mu w_\mu \|D^\mu u - D^\mu v\|_{L^2(P_X)}^2 + \text{irreducible noise}$.
- **Source:** `docs/research/estimator-integrity/secondary-candidates.md` §Candidate 5, Eq. (5.3).
- **Assumptions:** Finite multi-index set $\mathcal A$; $Y_\mu \in L^2$; network smooth to required order; unbiased labels $\mathbb E[Y_\mu \mid X] = D^\mu u(X)$.
- **Conventional Proof Status:** Prior-art overlap. Orthogonal projection identity complete on paper.
- **Lean 4 Coverage:** None.
- **Implementation Correspondence:** Supported by `parabolab/deep/generator.py` (draws $D^\mu$ roots).
- **Empirical / Symbolic Evidence:** Deep branching training on Allen-Cahn gradient.
- **Novelty / Prior Art:** Czarnecki et al. (2017) (Sobolev training); Huge & Savine (2020) (Differential ML). Direct tree root generation is convenient, but loss structure has full prior art.
- **Dependencies & Open Obligations:** Requires $L^2$ label certification to prevent infinite population risk.

---

#### `PR-SEC-6`: Robust Deep Branching Median-of-Means
- **Exact Statement:** For independent tree labels with finite variance $\sigma^2$, median-of-means with $K$ blocks satisfies $\mathbb P(|\widehat m_{\rm MOM} - m| > 2\sigma \sqrt{K/n}) \le e^{-K/8}$.
- **Source:** `docs/research/estimator-integrity/secondary-candidates.md` §Candidate 6, Eq. (6.2).
- **Assumptions:** Independent labels; finite second moment $\operatorname{Var}(Y) \le \sigma^2 < \infty$.
- **Conventional Proof Status:** Prior-art overlap. Classical Chebyshev + Hoeffding derivation.
- **Lean 4 Coverage:** None.
- **Implementation Correspondence:** Contrasted with authors' heuristic percentile filter in `parabolab/deep/generator.py`.
- **Empirical / Symbolic Evidence:** Analytical bias calculations for fixed clipping vs median-of-means.
- **Novelty / Prior Art:** Lugosi & Mendelson (2019); Catoni (2012). Contribution is auditing target bias of existing deep branching filters.
- **Dependencies & Open Obligations:** Cannot restore a mean if $\mathbb E|Y| = \infty$ (e.g. Dym).

---

#### `PR-SEC-7`: Coupled Multifidelity Control Variates
- **Exact Statement:** For coupled estimators $(H^\theta, H^0)$ with known $u^0$, the optimal control-variate weight $\beta^*$ achieves variance reduction $(1 - \operatorname{Corr}^2)$. If a common-tree coupling satisfies $\|(H^\theta - u^\theta) - (H^0 - u^0)\|_{L^2} \le C \varepsilon$, the variance is $O(\varepsilon^2 / N)$.
- **Source:** `docs/research/estimator-integrity/secondary-candidates.md` §Candidate 7, Eq. (7.4), (7.6).
- **Assumptions:** Real $L^2$ pair; known $u^0$; parameter-uniform $L^2$ coupling bound.
- **Conventional Proof Status:** Conjecture. Control variate algebra is proved; $L^2$ branching tree coupling contraction is unproved conjecture.
- **Lean 4 Coverage:** None.
- **Implementation Correspondence:** None.
- **Empirical / Symbolic Evidence:** None.
- **Novelty / Prior Art:** Peherstorfer et al. (2016, 2018); Glasserman (2003). Coupling theorem for branching trees remains open.
- **Dependencies & Open Obligations:** Needs explicit proof of $L^2$ pathwise tree contraction under parameter shifts.

---

#### `PR-SEC-8`: Pathwise Coefficient Greeks and Policy Intervals
- **Exact Statement:** For a coefficient-monomial tree $H(a) = R \prod a_s^{N_s}$, the pathwise derivative is $\partial_{a_r} H = H (N_r / a_r)$. Under uniform domination $\mathbb E[\sup |H| N_r / |s|] < \infty$, $\partial_{a_r} \mathbb E[H] = \mathbb E[H N_r / a_r]$. Delta method gives asymptotic policy confidence intervals if denominators are bounded away from zero.
- **Source:** `docs/research/estimator-integrity/secondary-candidates.md` §Candidate 8, Eq. (8.2), (8.4), (8.9).
- **Assumptions:** Coefficient-labelled tree; non-zero parameter $a_r \ne 0$; fixed proposal law; integrable domination; non-vanishing policy denominators.
- **Conventional Proof Status:** Conditional theorem. Pathwise product rule complete; differentiation under expectation conditional on domination and non-zero denominators.
- **Lean 4 Coverage:** None.
- **Implementation Correspondence:** None.
- **Empirical / Symbolic Evidence:** Symbolic checks on polynomial test cases.
- **Novelty / Prior Art:** Reiman & Weiss (1989); Glasserman (2003); Peng et al. (2018). Specialization to coding-tree node counts.
- **Dependencies & Open Obligations:** Singular at $a_r = 0$; requires second-moment certification for Gaussian intervals.

---

#### `PR-SEC-9`: Challenger-Model $2r$ Selection Certificate
- **Exact Statement:** Let $v_1, \dots, v_m$ be candidate solver outputs and $\widehat u$ an independent reference satisfying $\|\widehat u - u\| \le r$. Then the candidate minimizer $\widehat \ell = \arg\min_\ell \|v_\ell - \widehat u\|$ satisfies $\|v_{\widehat\ell} - u\| \le \min_\ell \|v_\ell - u\| + 2r$.
- **Source:** `docs/research/estimator-integrity/secondary-candidates.md` §Candidate 9, Eq. (9.3).
- **Assumptions:** Finitely many candidates; common norm and grid; certified radius $r$ holding with probability $\ge 1 - \delta$.
- **Conventional Proof Status:** Proved theorem. Two-step triangle inequality on normed space; sharpness of factor 2 established by 1D counterexample.
- **Lean 4 Coverage:** None.
- **Implementation Correspondence:** Audited in cross-solver comparison tables.
- **Empirical / Symbolic Evidence:** Unit test of 1D worst-case configuration in Python.
- **Novelty / Prior Art:** Standard metric oracle inequality; novelty is protocol establishing certified comparison between Monte Carlo and deep neural solvers.
- **Dependencies & Open Obligations:** Requires reference $\widehat u$ to possess certified error bound $r$ (needs finite variance).

---

#### `PR-SEC-10`: Short-Time Wave Proposal Optimization
- **Exact Statement:** For 1D nonlinear wave branching estimator $H_t$ with global clock rate $\lambda_t = \gamma t$, the asymptotic variance as $t \downarrow 0$ is $\operatorname{Var}(H_t) = t^2 [\gamma |b|^2 + \frac{1}{3\gamma} \sum_k \frac{|a_k|^2 |b|^{2k}}{q_k} - \operatorname{Re}(\bar b f(b))] + o(t^2)$. Minimized by $q_k^* = |a_k| |b|^k / A_b$ and $\gamma^* = A_b / (\sqrt{3} |b|)$.
- **Source:** `docs/research/estimator-integrity/secondary-candidates.md` §Candidate 10, Eq. (10.6)–(10.7).
- **Assumptions:** Local data $b = \phi(z) \ne 0$; $C^2/C^1$ initial data; finite polynomial $f$; small horizon $t \downarrow 0$.
- **Conventional Proof Status:** Proved theorem. Complete asymptotic Taylor and geometric branching tree expansion in `secondary-candidates.md` §10.
- **Lean 4 Coverage:** None.
- **Implementation Correspondence:** Validated in sibling project `wavelab`.
- **Empirical / Symbolic Evidence:** Variance scaling $O(t^2)$ corroborated in short-time simulations.
- **Novelty / Prior Art:** Chan & Privault (2026); Henry-Labordère & Touzi (2021). Specific joint minimization is repo derivation.
- **Dependencies & Open Obligations:** Singular when $\phi(z) = 0$; supporting FYP wave-equation result.

---

### Family 5: Multifactor Merton Theorems

#### `PR-MM-1`: Optimized Factor Merton HJB Equation
- **Exact Statement:** For observable factor $dY = b(Y)ds + \beta dW^Y$, asset excess returns $\lambda(Y)$, covariance $\Sigma \succ 0$, cross-covariance $C$, and CRRA parameter $a = 1 - \gamma \in (0, 1)$, the value function satisfies the optimized HJB:
  $$V_t + b\cdot\nabla_y V + \frac12 A:D_y^2 V + rxV_x - \delta V - \frac{(\lambda V_x + C\nabla_y V_x)^\top \Sigma^{-1} (\lambda V_x + C\nabla_y V_x)}{2V_{xx}} + \frac{\gamma}{a} V_x^{-a/\gamma} = 0.$$
- **Source:** `docs/research/multifactor-merton-proofs.md`, Theorem MM-1, Eq. (2.5).
- **Assumptions:**
  - *Structural:* Joint covariance block $\begin{pmatrix} \Sigma & C \\ C^\top & A \end{pmatrix} \succeq 0$; $\Sigma \succ 0$.
  - *Analytic:* $V \in C^{1,2}$; $V_x > 0$; $V_{xx} < 0$ (strict concavity in wealth).
  - *Domain:* $x > 0, y \in \mathbb R^m$.
- **Conventional Proof Status:** Proved algebraic theorem. Complete pointwise maximization of strictly concave Hamiltonians in `multifactor-merton-proofs.md` §2.
- **Lean 4 Coverage:** None.
- **Implementation Correspondence:** Analytical foundation for Merton solvers.
- **Empirical / Symbolic Evidence:** SymPy symbolic maximization of quadratic portfolio Hamiltonian.
- **Novelty / Prior Art:** Classical stochastic control; Merton (1971).
- **Dependencies & Open Obligations:** Algebraic step of verification theorem; does not prove existence or admissibility of controls.

---

#### `PR-MM-2`: CRRA Wealth Homogeneity State Reduction
- **Exact Statement:** The ansatz $V(t,x,y) = \frac{x^a}{a} F(t,y)$ with $F > 0$ reduces the $(m+1)$-dimensional HJB to the $m$-dimensional factor PDE:
  $$F_t + b\cdot\nabla F + \frac12 A:D^2 F + (ar(y) - \delta)F + \frac{a}{2\gamma F} (\lambda F + C\nabla F)^\top \Sigma^{-1} (\lambda F + C\nabla F) + \gamma F^{-a/\gamma} = 0,$$
  with terminal condition $F(T,y) = 1$ and optimal controls $\pi^* = \frac{1}{\gamma} \Sigma^{-1} (\lambda + C\nabla \log F)$ and $c^*/x = F^{-1/\gamma}$.
- **Source:** `docs/research/multifactor-merton-proofs.md`, Theorem MM-2, Eq. (3.2), (3.4)–(3.5).
- **Assumptions:** CRRA utility $U(c) = c^a/a$; strictly positive factor solution $F(t,y) > 0$; positive wealth $x > 0$.
- **Conventional Proof Status:** Proved algebraic theorem. Complete substitution and cancellation of $x^a/a$ in `multifactor-merton-proofs.md` §3.
- **Lean 4 Coverage:** None.
- **Implementation Correspondence:** Implemented in `parabolab/library.py::merton_vasicek_reduced`.
- **Empirical / Symbolic Evidence:** SymPy substitution verified algebraically.
- **Novelty / Prior Art:** Classical scaling property of CRRA utility; Merton (1971).
- **Dependencies & Open Obligations:** Removes wealth coordinate, eliminating artificial negative-wealth boundary issues.

---

#### `PR-MM-2.1`: Asset Count vs Spatial PDE Dimension Decoupling
- **Exact Statement:** When market opportunity parameters $(r, \lambda, \Sigma)$ are constant ($m = 0$), the reduced value $F(t)$ satisfies an ODE. The number of risky assets $n$ affects the equation solely through the scalar quadratic Sharpe ratio $\lambda^\top \Sigma^{-1} \lambda$ and does not increase the spatial dimension of the PDE.
- **Source:** `docs/research/multifactor-merton-proofs.md`, Corollary MM-2.1, Eq. (3.9)–(3.10).
- **Assumptions:** Constant market coefficients; CRRA terminal utility.
- **Conventional Proof Status:** Proved theorem. Direct specialization $m = 0$ in `multifactor-merton-proofs.md` §3.
- **Lean 4 Coverage:** None.
- **Implementation Correspondence:** Handled in baseline 1D Merton benchmarks.
- **Empirical / Symbolic Evidence:** Vector matrix multiplications in NumPy.
- **Novelty / Prior Art:** Fundamental financial economics fact; documented to prevent false claims that vector controls $\pi \in \mathbb R^n$ imply multidimensional PDEs.
- **Dependencies & Open Obligations:** Proves that genuinely multidimensional Merton requires stochastic opportunity factors $Y \in \mathbb R^m$ with $m \ge 2$.

---

#### `PR-MM-3`: Short-Time No-One-Index Obstruction
- **Exact Statement:** In the no-consumption linear-affine factor model $r(y) = r_0 + r_1^\top y$, $\lambda(y) = \ell + Ly$, if $F(T-\tau, y) = \widetilde F(\tau, v^\top y)$ on a short-time interval, then $G(y) = \partial_\tau F(0,y)$ must depend on $v^\top y$. Sufficient conditions ruling out single-index collapse are: (1) $\operatorname{rank}(L^\top \Sigma^{-1} L) \ge 2$, or (2) for a single asset, $r_1 \notin \operatorname{span}\{\ell_1\}$.
- **Source:** `docs/research/multifactor-merton-proofs.md`, Theorem MM-3, Eq. (4.3)–(4.8).
- **Assumptions:** Linear-affine drift and returns; $C^1([0, \varepsilon]; C^2(\mathbb R^m))$ short-time solution; terminal condition $F(T,y) = 1$.
- **Conventional Proof Status:** Proved theorem. Hessian rank and gradient collinearity analysis at terminal face $\tau = 0$ in `multifactor-merton-proofs.md` §4.
- **Lean 4 Coverage:** None.
- **Implementation Correspondence:** Design criterion for the recommended two-factor benchmark.
- **Empirical / Symbolic Evidence:** Evaluated analytically for 2-factor OU specification.
- **Novelty / Prior Art:** New checkable algebraic condition confirming that a proposed multi-factor benchmark cannot be collapsed to 1D by linear rotation.
- **Dependencies & Open Obligations:** Proves the two-factor OU model is genuinely multidimensional.

---

#### `PR-MM-4`: Exponential-Quadratic Matrix-Riccati Solution
- **Exact Statement:** In the no-consumption affine factor model, $F(T-\tau, y) = \exp(\alpha(\tau) + \beta(\tau)^\top y + \frac12 y^\top P(\tau) y)$ is an exact classical solution on any interval where the symmetric matrix Riccati ODE system for $(P, \beta, \alpha)$ remains finite:
  $$P' = -(K^\top P + PK) + PAP + \frac{a}{\gamma} H^\top R H, \qquad P(0) = 0,$$
  $$\beta' = Pk - K^\top \beta + PA\beta + ar_1 + \frac{a}{\gamma} H^\top Rh, \qquad \beta(0) = 0,$$
  $$\alpha' = k^\top \beta + \frac12 \operatorname{tr}(AP) + \frac12 \beta^\top A\beta + ar_0 - \delta + \frac{a}{2\gamma} h^\top Rh, \qquad \alpha(0) = 0,$$
  with $R = \Sigma^{-1}$, $h = \ell + C\beta$, and $H = L + CP$.
- **Source:** `docs/research/multifactor-merton-proofs.md`, Theorem MM-4, Eq. (5.5)–(5.8).
- **Assumptions:** Affine drift $b(y) = k - Ky$; constant factor covariance $A$; no intermediate consumption ($c \equiv 0$).
- **Conventional Proof Status:** Proved PDE theorem. Complete coefficient matching of constant, linear, and quadratic forms in `multifactor-merton-proofs.md` §5.
- **Lean 4 Coverage:** None.
- **Implementation Correspondence:** To be implemented as the analytical ground truth in `parabolab/library.py`.
- **Empirical / Symbolic Evidence:** SymPy polynomial coefficient matching.
- **Novelty / Prior Art:** Matrix Riccati systems for affine term structure and portfolio choice are classical; Liu (2007), Kim & Omberg (1996). Novelty is providing exact multi-dimensional ground truth for branching trees.
- **Dependencies & Open Obligations:** Provides ground-truth benchmark without Monte Carlo uncertainty; does not extend to intermediate consumption where non-polynomial exponential terms enter.

---

#### `PR-MM-5`: CRRA Artificial Wealth Diffusion Obstruction
- **Exact Statement:** If an unreduced coding tree for CRRA utility $\phi(x,y) = x^a/a$ ($x > 0, 0 < a < 1$) uses a reference Brownian motion with non-degenerate wealth variance $A_{xx} > 0$ and independent survival clock $\bar F_{\rm life}(h) > 0$, then:
  $$\mathbb P(\text{root survives and } X_T^{\rm ref} \le 0) = \bar F_{\rm life}(h) \Phi\left(-\frac{x}{\sqrt{h A_{xx}}}\right) > 0.$$
  The tree functional is outside the financial domain with positive probability and is not an almost-surely real-valued random variable.
- **Source:** `docs/research/multifactor-merton-proofs.md`, Theorem MM-5, Eq. (6.4).
- **Assumptions:** Nonzero reference diffusion in wealth $A_{xx} > 0$; horizon $h > 0$; positive clock survival; fractional power $a \in (0, 1)$.
- **Conventional Proof Status:** Proved theorem. Gaussian tail probability calculation in `multifactor-merton-proofs.md` §6.
- **Lean 4 Coverage:** None.
- **Implementation Correspondence:** Explains why unreduced Merton-Vasicek trees cannot be globally valid on $\mathbb R$.
- **Empirical / Symbolic Evidence:** Failure probability is astronomically small for $x = 100$ at short horizon, which explains why naive smoke tests pass while the theorem is violated.
- **Novelty / Prior Art:** Rigorous domain-integrity result; shows why replacing $x^a$ with $|x|^a$ alters the PDE problem and why CRRA reduction or degenerate diffusion is mathematically required.
- **Dependencies & Open Obligations:** Mandates CRRA reduction or singular diffusion $A_{xx} = 0$ for sound multifactor benchmarks.

---

#### `PR-MM-6`: Full-Covariance State-Dependent Mechanism Identity
- **Exact Statement:** For $\partial_t u + \frac12 A : D^2 u + f(x, Ju) = 0$ with constant $A = A^\top \succeq 0$, the backward Duhamel source for $G_{a_0,\beta,\nu} = (a_0 \partial_x^\beta \partial_z^\nu f)^*$ is represented by the labelled union of:
  1. $(G_{a_0,\beta,\nu+e_p}, G_{c,\beta',\nu'}, D^{\lambda_1}, \dots, D^{\lambda_s})$ from $\mathscr E_{\alpha_p}$;
  2. $(G_{-a_0 A_{kl}/2, \beta+e_k+e_l, \nu})$ for all $k,l$;
  3. $(G_{-a_0 A_{kl}, \beta+e_k, \nu+e_p}, D^{\alpha_p+e_l})$ for all $p,k,l$;
  4. $(G_{-a_0 A_{kl}/2, \beta, \nu+e_p+e_q}, D^{\alpha_p+e_k}, D^{\alpha_q+e_l})$ for all $p,q,k,l$.
- **Source:** `docs/research/multifactor-merton-proofs.md`, Theorem MM-6, Eq. (7.6)–(7.9).
- **Assumptions:** Constant symmetric covariance $A \succeq 0$; commuting mixed space-time derivatives; chain-rule licensing on classical solution.
- **Conventional Proof Status:** Proved algebraic theorem. Complete second-order multivariate chain rule expansion in `multifactor-merton-proofs.md` §7.
- **Lean 4 Coverage:** None.
- **Implementation Correspondence:** To be implemented in `parabolab/mechanism.py`.
- **Empirical / Symbolic Evidence:** Reduces to isotropic mechanism when $A = \sigma^2 I$.
- **Novelty / Prior Art:** Generalizes JEQ2023 / JCP2024 isotropic mechanism to full, possibly singular anisotropic covariance matrices $A$.
- **Dependencies & Open Obligations:** Core mathematical mechanism for multifactor Merton coding trees.

---

#### `PR-MM-7`: Conditional Full-Covariance Coding-Tree Representation
- **Exact Statement:** Under the full-covariance mechanism of `PR-MM-6` with reference Markov semigroup $P_s g(x) = \mathbb E[g(x + BW_s)]$ ($BB^\top = A$), the tree functional satisfies $\mathbb E H_{t,x,\mathrm{Id}} = u(t,x)$, $\mathbb E H_{t,x,D^\mu} = D^\mu u(t,x)$, and $\mathbb E H_{t,x,G_{a_0,\beta,\nu}} = a_0 (\partial_x^\beta \partial_z^\nu f)(x, Ju(t,x))$.
- **Source:** `docs/research/multifactor-merton-proofs.md`, Theorem MM-7, Eq. (7.16)–(7.18).
- **Assumptions:** Seven explicit hypotheses:
  1. Classical differentiability of Duhamel system;
  2. Positive lifetime density and survival tails;
  3. Positive proposal probabilities on live tuples;
  4. Shared branch position and conditional child independence;
  5. Non-explosive continuous-time tree;
  6. Absolute integrability ($L^1$) of all reached functionals;
  7. Uniqueness of the infinite code-indexed mild solution.
- **Conventional Proof Status:** Conditional representation theorem. Algebra proved; equivalence to tree expectation conditional on the 7 stated hypotheses.
- **Lean 4 Coverage:** None.
- **Implementation Correspondence:** To be verified numerically on two-factor Riccati benchmark.
- **Empirical / Symbolic Evidence:** Prototype Vasicek 1D smoke tests.
- **Novelty / Prior Art:** Candidate contribution; scoped literature search located no source combining full-covariance state-dependent coding with multifactor Riccati benchmarks.
- **Dependencies & Open Obligations:** Discharging hypotheses (especially $L^1/L^2$ integrability and mild uniqueness) is an open research problem.

---

## Omitted Lean Obligations Summary

For every claim touching Lean 4, the exact boundary between formalized mathematics and external paper obligations is recorded below:

| File | Formalized Lemmas | Omitted Probabilistic & Analytical Obligations |
|---|---|---|
| `formal/EstimatorIntegrity/FiniteTree.lean` | `FiniteMechanism`, `MomentVector`, `momentStep` | Continuous-time Poisson process, Brownian increments, standard Borel state space, spatial Markov transition semigroup. |
| `formal/EstimatorIntegrity/MomentIteration.lean` | `momentStep_mono`, `picard_mono`, `picard_le_prefixed`, `picard_iSup_least`, `momentStep_iSup_picard` | Identification of abstract Picard supremum with continuous-time tree expectation $\mathbb E\|H\|^p$; almost-sure tree exhaustion; Fubini-Tonelli measure integration. |
| `formal/EstimatorIntegrity/Dym.lean` | `dym_fz0_coefficient`, `one_div_not_intervalIntegrable`, `one_div_intervalIntegral_unbounded`, `continuous_density_intervalIntegral_unbounded` | 5-particle random tree event probability; joint Gaussian density conditioning over $(\tau_1, \tau_2, Y)$; signed-part decomposition $\mathbb E[H^+] = \mathbb E[H^-] = \infty$. |
| `formal/EstimatorIntegrity/Proposal.lean` | `sqrtProposal_sum`, `sqrtProposal_pos`, `secondMoment_ge_oracle`, `secondMoment_sqrtProposal_eq`, `sqrtProposal_ratio_bounds`, `oracle_ratio_of_relative_error`, `secondMoment_uniformMixture_le` | Pilot $\sigma$-algebra $\mathcal P$; conditional expectation tower property; inductive composition over random trees with $B_n$ decisions; empirical concentration probabilities $1 - \delta$. |

---

## Audit Checklist

- [x] Every claim assigned a stable identifier (`PR-MOM-*`, `PR-DYM-*`, `PR-PROP-*`, `PR-SEC-*`, `PR-MM-*`).
- [x] Clear demarcation between complete proofs, conditional theorems, prior-art overlaps, and conjectures.
- [x] Lean theorem names match exact declarations in `formal/EstimatorIntegrity/*.lean`.
- [x] Omitted obligations explicitly stated for every formalized item.
- [x] No claim described as proving more than it mathematically establishes.
