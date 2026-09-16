# Formal and Conventional Proof Registry

**Status:** navigation and claim inventory for the `parabolab` research programme; entries must be checked against their underlying proofs.
**Historical reviewed commit:** `ce2949330fcff1a3faf56c8a0ff36628586b242d`
**Certificate checkpoint review:** 14 September 2026; research commits
`05012ff` and `ff58620` originated on `codex/research-certified-rate` and
`codex/research-profile-efficiency` respectively.
**Integration status (16 September 2026):** both checkpoints are included
in local `main`, with user authorization to integrate confirmed. The
[integration record](results/integration-2026-09-16.md) records current
checks and historical source provenance. The earlier reviewed commit
above is retained as historical provenance; claim scopes remain below.
The 16 September documentation audit checks correspondence against integrated
revision `c82d536`; its 255 passing non-slow Python tests and 14 deselected
tests do not replace the stated mathematical assumptions.
**Scope:** all mathematical theorems, conditional representations, Lean-formalized lemmas, conjectures, and priority claims across estimator integrity and multifactor Merton research.

**Current decision (16 September 2026):** the active FYP improves branching
Monte Carlo PDE estimation through exponential-rate and tuple-proposal
selection. The existing solver/demo comparison workflow remains the same.
Algorithmic progress and mathematical guarantees are the primary goals;
measured runtime is supporting evidence rather than a gate for theoretical work.
Multidimensional Merton is inactive as a research application; its records
below are historical. See the [research index](README.md),
[certified-rate checkpoint](results/certified-rate-checkpoint.md),
[profile-efficiency checkpoint](results/profile-efficiency-checkpoint.md),
[sampling-method checkpoint](lambda-q-optimization-summary.md), and
[general rate-selection arguments](estimator-integrity/general-rate-selection.md).
The general stochastic moment/cutoff arguments remain conventional
mathematics. Separate six-code exact-rational verifiers now certify flat
Allen–Cahn, wave-root and weighted-profile global rate excess, plus wave
moment/depth bounds. Twenty-six public Lean theorems across the two
checkpoints and two private helpers verify deterministic
algebra/order/convexity substatements; they do not formalize the stochastic
correspondence or the certificate programs. The full build has passed.
The separate conventional Allen–Cahn mean-identification theorem now
discharges common-mean invariance for the saved flat/wave certificates;
their additive global moment gaps are therefore variance gaps as well.

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
| `PR-MOM-2` | Exact Multitype $p$-Moment Recursion | Conventional theorem under the stated model | `notation-and-moment-theorem.md` §Thm 2.2 | `FiniteTree.lean` defines only the finite algebraic `momentStep` | Analytic binary-depth controls and a slow Monte Carlo cross-check | Coding-tree specialization of branching identities; novelty unestablished |
| `PR-MOM-3` | Minimal Fixed Point & $L^p$ Criterion | Conventional theorem under nonexplosion | `notation-and-moment-theorem.md` §Thm 2.3 | Six public algebra/order lemmas and two private helpers in `MomentIteration.lean`; no random-tree identification | Finite-depth numerical controls, not proof of the infinite-depth limit | Established smoothing transform / branching theory |
| `PR-MEAN-1` | Allen–Cahn Rate-Invariant PDE Mean | Conventional theorem under an all-code envelope hypothesis, discharged for saved flat/wave benchmarks | `allen-cahn-mean-identification.md` | No Lean stochastic formalization | Verified six-code envelope supplies required hypothesis; explicit signed mild-system identities | Benchmark-specific closing of representation obligation; no universal mean theorem |
| `PR-DYM-1` | Dym $f_{z_0}$ Odd Singularity | Proved Theorem | `dym-nonintegrability.md` §Terminal Identities | `Dym.lean` (`dym_fz0_coefficient`) | SymPy jet differentiation | Benchmark-specific identity; priority unestablished |
| `PR-DYM-2` | Dym Absolute First-Moment Divergence | Conventional theorem for the specified real-extension estimator | `dym-nonintegrability.md` §Thm 4.1 | Singular-integral substatements only in `Dym.lean` | Trapezoidal log-quadrature (`examples/dym_nonintegrability.py`) | Historical scoped search found no matching proof; priority unestablished |
| `PR-DYM-3` | Dym Signed-Part Divergence ($\infty - \infty$) | Conventional theorem | `dym-nonintegrability.md` §Cor 4.2 | None (unformalized signed event decomposition) | Conventional principal-value comparison | Historical scoped search found no matching proof; priority unestablished |
| `PR-PROP-1` | Simplex Square-Root Tuple Optimizer | Proved Theorem | `adaptive-proposals.md` §Thm 6.1 | `Proposal.lean` (`secondMoment_ge_oracle`, `secondMoment_sqrtProposal_eq`) | Deterministic finite-vector tests in `tests/test_proposals.py` | Classical Cauchy-Schwarz / optimal sampling |
| `PR-PROP-2` | Unconstrained Event-Time Optimizer | Proved Theorem | `adaptive-proposals.md` §Thm 6.2 | None (continuous-time measure decomposition) | No executed unrestricted-event sampler registered | Classical importance-sampling square-root rule on a mixed measure |
| `PR-PROP-3` | Pilot/Frozen Proposal Exact Unbiasedness | Conventional theorem under conditional and unconditional integrability hypotheses | `adaptive-proposals.md` §Thm 6.3 | None (pilot $\sigma$-algebra / tower property) | Historical 5-seed Merton-Vasicek diagnostic does not prove unbiasedness | Established multi-stage Monte Carlo |
| `PR-PROP-4` | Multiplicative Finite-Depth Oracle Bound | Proved under the simultaneous relative-error hypotheses | `adaptive-proposals.md` §Thm 6.4 | Finite algebra in `Proposal.lean`; tree composition omitted | Unit controls for finite objectives and ratio formula; no certified pilot concentration event | Tree-depth composition specialization; novelty unestablished |
| `PR-RATE-1` | Local Exponential Rate Strict Convexity | Proved Theorem | `exponential-rate-optimization.md` §Thm 7.1 | `ExponentialRate.lean` (`expKernelFactor_pos`, `modelRateObjective_ge_amgm`, `modelRateObjective_at_optimum`, `modelObjective_eq_lower_bound_iff`) | Quadrature derivatives vs finite differences | Related to classical importance-sampling convexity |
| `PR-RATE-2` | Tree Topology Rate Convexity | Conditional full-tree theorem | `exponential-rate-optimization.md` §Thm 7.2 | `ExponentialRate.lean` (`topologyFactor_pos_of_pos`) only | Deterministic recursive derivatives | Topology-level coding tree convexity; finite variance separate |
| `PR-RATE-3` | Short-Horizon $O(1)$ Scaling Law | Local theorem; full recursion conditional | `exponential-rate-optimization.md` §Thm 7.4 | None (Taylor asymptotic analysis) | 1D Allen-Cahn / Riccati quadrature sweeps | Requires nonzero terminal terms and uniform expansions |
| `PR-RATE-4` | Exact Riccati Binary Second-Moment Oracle | Proved for standard binary representation | `exponential-rate-optimization.md` §Thm 7.5 | None (ODEs) | Corrected explicit standard-binary driver, first-event identity, cutoff convergence and untruncated MC; `results/binary-benchmark-audit.md` | Historical derivative-coded/oracle comparison was mismatched and is not oracle evidence |
| `PR-RATE-5` | General Rate Selection and Cutoff Certificates | Conventional theorems under stated hypotheses | `general-rate-selection.md` §§2–5 | Five deterministic transfer/coverage lemmas in `RateCertificate.lean`; general stochastic theory remains unformalized | Generic selector remains finite-depth quadrature; the separate flat verifier is `PR-RATE-7` | Explicit selection-gap specialization; novelty unestablished |
| `PR-RATE-6` | Six-Code Allen–Cahn Moment Enclosures | Conventional comparison theorem plus exact rational witnesses | `allen-cahn-codewise-certificate.md` §§1–4 | Six polynomial/field/order lemmas in `AllenCahnBounds.lean` | `results/rate-certificate/witnesses.json.gz`, rechecked; flat and wave envelopes | Established positive-system comparison tools specialized to the raw mechanism; novelty unestablished |
| `PR-RATE-7` | Flat Allen–Cahn Global Rate-Excess Certificate | Exact-rational numerical certificate with conventional estimator/ODE and exterior-bound proofs | `allen-cahn-codewise-certificate.md` §6; `results/certified-rate-checkpoint.md` | Conditional infimum, exterior coverage and variance-transfer algebra; concrete numbers/program not Lean-verified | At `phi=1/2,T=1/20`, selected `1907/2560`, global excess `<10^-4`; exact witnesses verified | Flat benchmark result does not transfer to the wave; no universal optimizer |
| `PR-RATE-8` | Factorial Omitted-Depth Bound | Conventional theorem requiring a finite moment box | `allen-cahn-codewise-certificate.md` §5 | No direct formalization of Volterra/Jacobian/simplex bound | Rational wave tail on `[0.7,0.8]`, e.g. depth 6 `<4.4445e-6` at `T=0.05` | Finite-dimensional positive closure specialization; novelty unestablished |
| `PR-RATE-9` | Wave Full-Moment Polynomial-Residual Enclosure | Conventional residual/comparison theorem plus exact rational certificates | `wave-numerical-certification-route.md` §§2–5; `results/wave-rate-certificate.md` | Existing field/order algebra only; residual and numerical soundness not formalized | Ten wave rates plus rate-one baseline, degree 5, exact Bernstein and error witnesses | Benchmark-specific validated numerics; not a quadrature-refinement or novelty claim |
| `PR-RATE-10` | Wave Global Rate-Excess via Convex Enclosures | Conventional full-moment convexity bridge plus exact rational objective certificate | `wave-numerical-certification-route.md` §6; `results/wave-certificate/summary.json` | Five public lemmas/two private helpers in `ConvexEnclosure.lean`; finite-real assumptions | At `T=0.05,x=0`, selected `59/80` gap `<5.688312e-6`; rounded historical `14611/20000` gap `<6.130773e-6`, globally over positive rates | Objective-excess guarantee; does not prove candidate ordering or rate-location accuracy |
| `PR-RATE-11` | Weighted Wave-Profile Rate Certificate | Conventional weighted-objective/mean argument plus exact rational certificate | `profile-rate-efficiency.md`; `results/profile-efficiency-checkpoint.md` | Six profile convexity/enclosure/variance/interpolation lemmas in `ProfileEfficiency.lean` | Five-point equal-weight profile, `T=1/20`: λ=1/2 global variance excess `<3.848558e-5`; actual cheap policy relative excess `<1.60%` | Benchmark-specific guarantee over common positive scalar rates; novelty unestablished |
| `PR-COST-1` | Replicated Rate/Proposal Accuracy–Cost Comparison | Conditional MSE/cost algebra and empirical evidence | `results/rate-cost-protocol.md`; `results/rate-cost-results.md` | None for stochastic MSE or timings | 240 profiles, 16,833,300 evaluation trees; no demonstrated one-profile tuning gain under calibrated predicted budget | Performance evidence, not theorem or population-significance claim |
| `PR-COST-2` | Profile Reuse and Frozen-Allocation Expected MSE | Conditional MSE identity, certified variance/count inequalities and separate empirical timings | `results/profile-efficiency-results.md`; `results/profile-certificate/summary.json` | Four continuous-budget algebra/break-even lemmas in `ProfileEfficiency.lean`; stochastic MSE and integer allocation remain conventional | 2,200 curves, 139,621,200 evaluation trees; all eight competing frozen predicted-budget allocations have larger certified expected MSE than cheap grid policy | Conditional ideal-estimator loss result; no wall-time or universal speedup theorem |
| `PR-SEC-4` | State-Dependent Arbitrary-Jet Representation | Conditional Theorem | `secondary-candidates.md` §Cand 4 | None (unformalized multi-index jet algebra) | SymPy jet chain-rule checks | Candidate contribution; nearby prior art |
| `PR-SEC-5` | Derivative-Code Sobolev Training | Prior-Art Overlap | `secondary-candidates.md` §Cand 5 | None | Generator supports non-Id roots; no completed Sobolev-training result registered | Overlap: Czarnecki (2017), Huge-Savine (2020) |
| `PR-SEC-6` | Robust Deep Branching Median-of-Means | Prior-Art Overlap | `secondary-candidates.md` §Cand 6 | None | Conventional clipping-bias examples; proposed comparison study | Overlap: Lugosi-Mendelson (2019), Catoni (2012) |
| `PR-SEC-7` | Coupled Multifidelity Control Variates | Conjecture | `secondary-candidates.md` §Cand 7 | None | No completed coupling experiment registered | Conjecture ($L^2$ contraction unproved) |
| `PR-SEC-8` | Pathwise Coefficient Greeks & Policy Bands | Conditional Theorem | `secondary-candidates.md` §Cand 8 | None | Conventional pathwise derivation; proposed checks are not completed experiments | Classical simulation sensitivity; conditional on denominators |
| `PR-SEC-9` | Challenger-Model $2r$ Selection Certificate | Proved Theorem | `secondary-candidates.md` §Cand 9 | None | Metric triangle inequality verification | Triangle inequality application; audit protocol |
| `PR-SEC-10` | Short-Time Wave Proposal Asymptotics | Conventional theorem under stated asymptotic hypotheses | `secondary-candidates.md` §Cand 10 | None | No executed wave-equation result registered in this repository | Specific asymptotic derivation; novelty unestablished |
| `PR-MM-1` | Optimized Factor Merton HJB Equation | Proved Algebraic Theorem | `multifactor-merton-proofs.md` §Thm MM-1 | None | SymPy Hamiltonian optimization | Classical dynamic programming (Merton 1971) |
| `PR-MM-2` | CRRA Wealth Homogeneity State Reduction | Proved Theorem | `multifactor-merton-proofs.md` §Thm MM-2 | None | SymPy power substitution | Classical scaling reduction |
| `PR-MM-2.1` | Asset Count vs PDE Dimension Decoupling | Proved Theorem | `multifactor-merton-proofs.md` §Cor MM-2.1 | None | Analytical matrix rank check | Classical financial insight |
| `PR-MM-3` | Short-Time No-One-Index Obstruction | Proved Theorem | `multifactor-merton-proofs.md` §Thm MM-3 | None | Hessian rank evaluations | Checkable benchmark condition; novelty unestablished |
| `PR-MM-4` | Exponential-Quadratic Matrix-Riccati Solution | Proved Theorem | `multifactor-merton-proofs.md` §Thm MM-4 | None | Historical symbolic/numerical checks in `milestone-1-checks.json` | Classical matrix-Riccati method specialized to the stated model |
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
- **Empirical / Symbolic Evidence:** `tests/test_tree.py` checks that depth-zero killing returns zero on a root branch without consuming continuation draws. The full pathwise killed-tree identity is proved conventionally, not exhaustively tested.
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
- **Implementation Correspondence:** `parabolab/moments.py::finite_depth_moment_1d`.
- **Empirical / Symbolic Evidence:** `tests/test_moments.py` checks exact analytic binary depth-zero and depth-one controls and includes a separately marked slow Monte Carlo check. The default 255-test run deselects slow tests.
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
    - `picard_iSup_least`: the Picard supremum lies below every pre-fixed point.
    - `momentStep_iSup_picard`: continuity from below ($\Phi(\sup V_n) = \sup \Phi(V_n)$).
  - *Omitted Obligations:* Identification of the abstract Picard limit with the continuous-time random tree functional $\mathbb E|H|^p$.
- **Implementation Correspondence:** `parabolab/moments.py::finite_depth_moment_1d` evaluates a finite-depth quadrature approximation; there is no `iterate_moments` API or exact infinite-depth solver.
- **Empirical / Symbolic Evidence:** Analytic binary-depth controls in `tests/test_moments.py` and corrected cutoff diagnostics in `results/binary-benchmark-audit.md`. Numerical agreement is not proof of the limiting identity.
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
- **Empirical / Symbolic Evidence:** Trapezoidal quadrature across 12 cutoffs $\varepsilon \in [10^{-1},10^{-12}]$ supports the conventional logarithmic-divergence argument. The theoretical slope is $2g(0)$; finite quadrature values do not prove its limit or the random-tree theorem.
- **Novelty / Prior Art:** Scoped search found no prior Dym-specific coding-tree proof; publication priority is not established (see safe-language standards in roadmap §10).
- **Dependencies & Open Obligations:** Explains why empirical Monte Carlo appears stable (rare origin visits) while formal variance and mean do not exist.

---

#### `PR-DYM-3`: Dym Signed-Part Divergence ($\mathbb E[H^+] = \mathbb E[H^-] = \infty$)
- **Exact Statement:** Under the hypotheses of `PR-DYM-2`, both positive and negative parts diverge: $\mathbb E[H^+] = \infty$ and $\mathbb E[H^-] = \infty$. The random variable has no extended-real expectation ($\infty - \infty$).
- **Source:** `docs/research/estimator-integrity/dym-nonintegrability.md`, Corollary 4.2, Eq. (4.34).
- **Assumptions:** Identical to `PR-DYM-2`, plus sign-preservation of auxiliary terminal factors ($\phi_\alpha''(r) < 0$ on $K = [1, 2]$).
- **Conventional Proof Status:** Proved theorem. Complete proof in `dym-nonintegrability.md` §4 showing $\operatorname{sgn}(H) = \operatorname{sgn}(X^{(0)})$ on $E_* \cap \{X^{(D)} \in K\}$.
- **Lean 4 Coverage:** None directly formalized for the signed half-line split (formalized unbounded integral applies to the one-sided case).
- **Implementation Correspondence:** `demo/dym.py` illustrates the specified estimator's behavior; it does not verify signed-part divergence from finite samples.
- **Empirical / Symbolic Evidence:** The source's conventional principal-value analysis explains why symmetric cancellation does not define the probabilistic expectation.
- **Novelty / Prior Art:** Benchmark-specific obstruction; no absolute priority or claim about every Dym representation.
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
- **Implementation Correspondence:** `parabolab/proposals.py::sqrt_optimal_probabilities` and `second_moment_objective`, with `floor_mass` support handling.
- **Empirical / Symbolic Evidence:** Deterministic finite-vector controls in `tests/test_proposals.py`; pilot estimates of continuation moments remain approximations.
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
- **Implementation Correspondence:** No general sampler for this unrestricted event-time law is implemented in `parabolab/proposals.py`; that module concerns tuple probabilities.
- **Empirical / Symbolic Evidence:** No executed event-time optimization experiment is registered for this theorem.
- **Novelty / Prior Art:** Clarifies why exponential clocks $\lambda e^{-\lambda s}$ are strictly constrained one-parameter subfamilies that cannot achieve $r^*(s)$ in general.
- **Dependencies & Open Obligations:** Prevents conflating optimal lifetime laws with scalar rate optimization.

---

#### `PR-PROP-3`: Pilot/Frozen Proposal Exact Unbiasedness
- **Exact Statement:** Let pilot $\sigma$-algebra $\mathcal P$ determine a frozen supported proposal. Under the source theorem's conditional $L^1$ and integrable conditional-norm assumptions, fresh evaluation randomness, valid likelihood cancellation, and the killed-depth passage to the finite target $u$, $\mathbb E[\widehat H \mid \mathcal P]=u$ a.s. and $\mathbb E[\widehat H]=u$. A probability floor alone does not establish these conclusions.
- **Source:** `docs/research/estimator-integrity/adaptive-proposals.md`, Theorem 6.3, Eq. (6.23).
- **Assumptions:**
  - *Structural:* Frozen proposal measurable with respect to pilot $\mathcal P$.
  - *Analytic:* Full conditional support $\widehat q_h(i) \ge q_{\min} > 0$.
  - *Probabilistic:* Fresh evaluation randomness; tower property of conditional expectation.
  - *Integrability:* Finite target mean $u$; conditional $L^1$ integrability $\mathbb E[|\widehat H| \mid \mathcal P] < \infty$ a.s.; integrable conditional norm $\mathbb E[\mathbb E(|\widehat H|\mid\mathcal P)]<\infty$; non-explosion and conditional $L^1$ killed-depth passage with target identification.
- **Conventional Proof Status:** Proved theorem. Complete finite-depth topology sum cancellation and $L^1$ limit in `adaptive-proposals.md` §6.
- **Lean 4 Coverage:** None (requires abstract probability spaces, conditional expectations, and $\sigma$-algebras).
- **Implementation Correspondence:** `examples/proposal_merton_vasicek.py`.
- **Empirical / Symbolic Evidence:** The historical five-seed Merton-Vasicek run reports mean $1.0025\pm0.0003$ against $1.002503$. This agreement does not prove its full-tree integrability or unbiasedness.
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
- **Implementation Correspondence:** `oracle_ratio_bound` in `parabolab/proposals.py` evaluates the finite-decision factor; the historical pilot example constructs frozen tables without certifying a simultaneous relative-error event.
- **Empirical / Symbolic Evidence:** Finite-objective tests do not certify the random-tree oracle inequality's hypotheses. The theorem bounds second moments, not the same multiplicative ratio of centered variances.
- **Novelty / Prior Art:** Multiplicative tree-depth specialization of importance-sampling bounds; novelty unestablished.
- **Dependencies & Open Obligations:** Explains why adaptive gains can degrade if pilot error compounds over deep trees.

---

### Rate-Certificate and Cost Checkpoint (14 September 2026)

The concrete numerical evidence in this subsection was read from
[the saved summary](results/rate-certificate/summary.json) and exact
[witness archive](results/rate-certificate/witnesses.json.gz), then the
archive was rechecked with `examples/certified_allen_cahn_rate.py --verify`.
All witnesses passed. The global gap/exterior comparisons and displayed
wave tails were also recomputed from the archived rational values.

#### `PR-RATE-4`: Standard-Binary Oracle Audit Amendment

- **Estimator:** `Id → (Id,Id)`, terminal value one and tuple probability
  one; this is not `FullyNonlinearPDE1D`'s default derivative-coded tree.
- **Exact claim:** the Riccati formula and stationary equation from
  [Theorem 7.5](estimator-integrity/exponential-rate-optimization.md) apply
  to that standard-binary estimator. Stored stationary rates are numerical
  roots, not exact algebraic values or interval-certified locations.
- **Correction:** historical `binary_control_optimum` rows mixed a
  derivative-coded cutoff objective with standard-binary oracle values.
  Those files are retained but cannot validate the binary optimum or
  isolate a pure rate effect.
- **Current evidence:** the [corrected audit](results/binary-benchmark-audit.md)
  includes matching first-event integral identities, analytic depth-one
  values, increasing-cutoff convergence and untruncated MC checks. At
  `T=0.15`, depth-2 selection leaves about 19.48% excess full-tree variance.
- **Lean boundary:** no Riccati ODE, full-tree identification or concrete
  binary optimum is formalized by this amendment.

#### `PR-RATE-5`: Deterministic Certificate-Transfer Formalization

- **Exact substatement:** for finite real-valued objectives `M`, `MK` and
  `numerical`, assume `MK≤M`, a selected-rate omitted-depth bound `tail`,
  a uniform absolute numerical error `δ`, and approximate minimization
  error `η`. Then the selected objective exceeds any comparison objective
  by at most `tail + 2δ + η`; the same bound holds above the infimum without
  requiring an attained minimum.
- **Formalized declarations:**
  [RateCertificate.lean](../../formal/EstimatorIntegrity/RateCertificate.lean)
  contains `rateSelection_excess_le`, `rateSelection_excess_le_inf`,
  `upperLower_excess_le_inf`, `commonMean_variance_excess_le`, and
  `global_lower_of_interval_and_exterior`.
- **Additional exact substatements:** an incumbent upper bound minus a
  global lower bound bounds objective excess; subtracting a common squared
  mean preserves an additive gap; interval and exterior lower bounds cover
  all positive rates.
- **Not formalized:** stochastic integrability, the killed-tree inequality,
  the value of a depth tail, uniform numerical error, the optimization
  guarantee, PDE identification and common-mean invariance. They are
  assumptions to the formal transfer lemmas. The Lean objectives are finite
  real-valued functions; treatment of infinite moments outside the finite
  domain remains part of the conventional application proof.
- **Priority:** the formal algebra is a verification component; no separate
  novelty claim is made for triangle/infimum/order reasoning.

#### `PR-RATE-6`: Six-Code Allen–Cahn Full-Moment Enclosure

- **Exact statement:** for raw one-dimensional `SemilinearMechanism`,
  uniform labelled tuple probabilities and `f(z)=z-z³`, normalized squared
  code moments are bounded by a nonnegative supersolution of
  `y'=λ*y+(r/λ)*G(y)`, with code order `(Id,D,F₀,F₁,F₂,F₃)`. The polynomial
  `G` and terminal bounds are given in
  [the codewise derivation](estimator-integrity/allen-cahn-codewise-certificate.md).
  Flat terminal data identify the exact moment with the ODE after
  finiteness and uniqueness are established conventionally.
- **Structural assumptions:** scalar-square homogeneity of derivative
  codes, raw tuple multiplicities including dead alternatives, shared
  branch positions and the fixed uniform tuple law. A nonuniform proposal
  or renormalized mechanism requires separate arguments.
- **Conventional proof:** polynomial positivity/monotonicity, an affine
  rational supersolution, induction over killed moments, nonexplosion and
  monotone convergence. A numerical trajectory without accepted exact
  inequalities is not sufficient.
- **Rational verification:** every step checks
  `b ≥ a + h*(upper_rate*b + (tilt/lower_rate)*G(b))`. Serialized fractions
  preserve exact values; accepted steps cover the whole horizon. Flat
  lower steps round downward. The checker is ordinary Python rational
  arithmetic, not a Lean-certified executable.
- **Formalized declarations:**
  [AllenCahnBounds.lean](../../formal/EstimatorIntegrity/AllenCahnBounds.lean)
  contains `allenCahnBranchPolynomial_nonneg`,
  `allenCahnBranchPolynomial_mono`, `allenCahnMomentField_nonneg`,
  `allenCahnMomentField_mono`, `allenCahnMomentField_interval_upper`, and
  `allenCahn_postfixed_box_slope`.
- **Not formalized:** the code-to-polynomial correspondence, scalar
  homogeneity of random trees, terminal suprema, ODE existence/comparison,
  stochastic domination, rational implementation/serialization and
  concrete numerical witnesses. The Lean field permits nonnegative rates
  algebraically; the probabilistic application still requires `λ>0`.
- **Saved evidence:** at `T=1/20`, wave rates `[7/10,4/5]`, the ordinary
  root moment is at most `297372020821519/281474976710656`; the `2^N`-tilted
  moment is at most `307426758639711/281474976710656`, uniformly in space.
  Tilt 4 was inconclusive at step 171, not proved divergent.

#### `PR-RATE-7`: Flat Global Rate-Excess Certificate

- **Scope:** `allen_cahn_flat(phi0=1/2,T=1/20)`, raw semilinear mechanism,
  uniform tuple probabilities and the ideal real-arithmetic estimator.
- **Verified result:** selected rate `1907/2560`; incumbent second-moment
  upper bound `75820673137583/281474976710656`; global infimum lower bound
  `18948168212961/70368744177664`. Their difference is
  `28000285739/281474976710656 < 1/10000`.
- **Global bridge:** 45 rate cells cover `[1/5,2]`. Root survival plus a
  single-branch topology gives exterior lower bounds `73/256` and `11/40`;
  both are above the incumbent upper bound in exact arithmetic. This
  excludes improvements outside the interval, without requiring an
  attained minimizing rate.
- **Meaning:** a bound on additive full-tree second-moment excess, not an
  error bound on the rate location. `PR-MEAN-1` supplies the common mean
  for this saved benchmark, so it is also an additive variance-excess
  certificate. Relative variance
  optimality and the traveling-wave selection are not certified here.
- **Baseline consequence:** the rate-one lower moment bound minus the
  selected upper bound is at least `30840997895/35184372088832`, a positive
  certified second-moment improvement. The discharged common-mean
  condition also makes it an additive variance reduction.
- **Lean boundary:** the generic infimum/exterior/variance algebra in
  `PR-RATE-5` supports this proof structure; it does not check the exact
  fractions, the rate partition, topology-derived exterior estimates,
  verifier implementation or stochastic correspondence.
- **Diagnostic only:** independent DOP853 integration and scalar numerical
  minimization locate a rate near `0.74367026`; that floating computation
  is not used as the mathematical certificate.

#### `PR-RATE-8`: Factorial Omitted-Depth Certificate

- **Exact statement:** a uniform finite ordinary-moment box `B`, its
  nonnegative Jacobian `J=DG(B)`, horizon `T` and rate interval `[ℓ,u]`
  imply, for the exact killed-depth moment `M_K`,
  `0 ≤ M-M_K ≤ exp(u*T)*(T/ℓ)^(K+1)/(K+1)! * [J^K G(B)]_Id`.
- **Conventional proof:** monotone polynomial Lipschitz bound on the box,
  repeated Volterra integration and the ordered-simplex volume. An exact
  rational upper bound for the exponential makes the saved calculation
  fully rational. Finiteness of `B` is a prerequisite, not a consequence
  of the factorial expression alone.
- **Evidence:** the verified ordinary wave box on `[0.7,0.8]` at `T=0.05`
  gives omitted-depth bounds below `4.4445e-6` at depth 6 and `6.50e-8` at
  depth 8. Values were recomputed from the saved rational witness.
- **Lean boundary:** neither the Jacobian tail estimate, simplex integral,
  exponential bound nor its stochastic application is formalized by the
  checkpoint theorems.
- **Remaining obligations:** the old recursive time/Gaussian quadrature
  still has no standalone verified error bound. `PR-RATE-9/10` instead
  certifies the full wave objective directly by a polynomial residual;
  it does not add this depth tail to its direct full-moment error.

#### `PR-RATE-9`: Wave Full-Moment Residual Certificate

- **Estimator and root:** `allen_cahn_wave_1d(T=1/20)`, `(t,x)=(0,0)`,
  raw one-dimensional semilinear mechanism and uniform tuple probabilities.
  The exact transformed coordinate `s=1/(1+exp(x))` maps the root to `1/2`
  and the whole spatial line into `(0,1)`, with absorbing endpoint limits.
  No finite Brownian spatial cutoff is imposed.
- **Conventional theorem:** a rational polynomial trial's global residual
  and initial mismatch, combined with a separately verified true-moment
  box, bound full-moment error through a positive linear system. The
  Jacobian is evaluated on a signed magnitude box containing both trial
  and true solution; trial positivity is not assumed.
- **Exact verification:** the complete residual retains `∂τ=(1/T)∂θ`
  and all high-degree coefficients. Bernstein coefficients bound trial
  magnitudes and residuals over the whole domain. The actual run uses
  time degree 5, two successive spatial bisections (four subintervals),
  100 verified error steps and a `2^-60` rational rounding grid. Taylor
  generation is not trusted as proof of an infinite series convergence.
- **Evidence:** ten exact rate points in `[0.7,0.8]`, including `14611/20000`,
  and an independent rate-one baseline. The
  [archive](results/wave-certificate/witnesses.json.gz) passes exact
  rechecking, and all point values agree with the
  [summary](results/wave-certificate/summary.json). Independent collocation
  at orders 24/36 lies within the certified intervals; its resolution
  agreement is diagnostic, not the proof.
- **Lean boundary:** the existing six-code field algebra is relevant, but
  the coordinate-change/semigroup argument, Bernstein identity and code,
  residual-to-error comparison, exact-program correctness and concrete
  fractions are not formalized by this checkpoint.
- **Limitations:** ideal real arithmetic, one horizon/root and uniform raw
  mechanism. `PR-RATE-11` separately covers the saved five-point objective.
  Further states/horizons, nonuniform proposals and production roundoff
  require their own certification.

#### `PR-RATE-10`: Global Wave Rate-Excess Certificate

- **Ten-point set:** `{0.7,0.7125,0.725,0.73055,0.7375,0.75,0.7625,0.775,0.7875,0.8}`,
  all interpreted as exact rational numbers in the witnesses.
- **Exact result:** at the stated wave root, `M(59/80)-inf_{λ>0}M(λ)` is
  at most the archived rational gap, approximately `5.6883117983770254e-6`,
  and strictly less than `5.688312e-6`. For the rounded historical rate
  `14611/20000`, the corresponding archived gap is approximately
  `6.130772565087558e-6`, strictly below `6.130773e-6`.
- **Lower-envelope argument:** extrapolate neighboring certified secants
  outside their defining pair to obtain cell lower bounds. Do not use a
  convex chord as a lower bound inside its own pair. Cell minima use exact
  endpoints and line intersections. Verified endpoint slope orientations
  give exterior lower bounds above the incumbent, excluding improvements
  outside `[0.7,0.8]`.
- **Extended-value boundary:** the conventional topology argument gives
  convexity of the nonnegative full moment. Infinite exterior moments
  automatically satisfy finite lower bounds; finite exterior values allow
  ordinary secant reasoning. Global moment finiteness and optimizer
  attainment are not assumed.
- **Formalized declarations:**
  [ConvexEnclosure.lean](../../formal/EstimatorIntegrity/ConvexEnclosure.lean)
  contains five public theorems: `convexEnclosure_right`,
  `convexEnclosure_left`, `convexEnclosure_right_exterior`,
  `convexEnclosure_left_exterior`, and
  `convexEnclosure_cell_lower_envelope`. Two private cross-multiplied
  helpers support them. These prove finite-real ray extrapolation,
  exterior constants and the pointwise cell envelope from assumed
  `ConvexOn` and correct endpoint bounds.
- **Not formalized:** the envelope-minimization algorithm, rational
  implementation, concrete input enclosures, stochastic/extended-valued
  convexity and the global stochastic objective certificate.
- **Meaning:** `59/80` has the smallest certified upper bound among the
  ten samples; overlapping intervals do not prove its true moment is
  smaller than that at `14611/20000`. The historical certificate uses
  exactly the rounded `0.73055`, not literally the earlier optimizer
  float `0.7305486297108235`. These are objective-gap bounds, not bounds
  on distance to a minimizing rate.
- **Variance and cost:** the selected second moment is below rate one's
  by at least the positive rational number reported in the summary
  (greater than `0.000955093206`). `PR-MEAN-1` identifies the common mean
  for all positive rates, so the global gap and baseline improvement also
  hold for variance. The approximately 30-second certificate run
  included checking and six optional collocation diagnostics; it was not
  one of the practical selector variants in `PR-COST-1`, so it establishes
  no amortized runtime gain.

#### `PR-MEAN-1`: Rate-Invariant Allen–Cahn PDE Mean

- **Source:** [Allen–Cahn mean identification](estimator-integrity/allen-cahn-mean-identification.md).
  This is a conventional stochastic/analytic proof, not a Lean theorem.
- **Scope and hypothesis:** the exact raw uniform one-dimensional
  semilinear estimator for the specified flat or traveling-wave data,
  with a finite all-six-code second-moment envelope at one reference rate,
  uniformly in starting state and remaining time. The saved certificates
  supply that hypothesis through `T=0.05`; a root-only bound would not.
- **Absolute integrability:** scalar normalization uses `|a|` for absolute
  first moments. In the killed absolute first-moment recursion the
  lifetime density, survival and tuple probabilities cancel. Thus the
  recursion and its monotone full-depth limit do not depend on positive
  `λ`. Cauchy–Schwarz at the reference rate supplies bounded absolute
  first moments at every positive rate, even if some second moments are
  infinite.
- **Mean identification:** justified first-event conditioning gives the
  bounded rate-free signed six-field mild system, with the negative
  diffusion terms retained. The explicit flat/wave PDE fields satisfy
  the same system. Polynomial Lipschitz bounds and heat-semigroup
  contraction give bounded mild uniqueness, identifying `Eλ H` with the
  PDE value for every positive rate.
- **Variance consequence:** at a fixed root,
  `Varλ(H)=M(λ)-μ²` in extended nonnegative values. The finite incumbent
  and common mean imply that its global variance excess equals its
  global second-moment excess exactly. No numerical evaluation of `μ`
  is needed for this gap transfer.
- **Coverage boundary:** no Lean probability/semigroup/conditional-
  expectation formalization is claimed. The theorem does not establish
  arbitrary-PDE identification, a changed/nonuniform mechanism's mean,
  finite second moments for every rate, or production floating-point
  unbiasedness. Numerical absolute/relative variance values need their
  own validated evaluation of the explicit mean.

#### `PR-COST-1`: Replicated Accuracy and Total-Cost Evidence

- **Conditional model:** independent unbiased `n`-sample point estimators
  with finite second moments have expected grid MSE `mean_x Var(H_x)/n`.
  Under the idealized cost model `C(n)=h+c*n`, the continuous-budget
  approximation is `c*meanVar/(B-h)` for `B>h`. Actual median calibration
  timing does not establish an expected-cost identity.
- **Predeclared experiment:** six existing sampling variants, wave
  `T=0.05`, five grid points, 20 independent replicates per variant in
  each phase, independent timing calibration, no clipping or timed
  stopping. All 6,000,000 fixed-size and 10,833,300 budget-phase trees
  completed. [Protocol](results/rate-cost-protocol.md),
  [results](results/rate-cost-results.md),
  [integrity audit](results/rate-cost-benchmark/validation.json).
- **Observed result:** combined tuning had 26.4% lower aggregate RMSE at
  fixed sample count but 2.22 times the one-profile total cost. Under the
  calibrated predicted budget, short-time rate `0.75` had the smallest
  observed aggregate RMSE; neither selected-rate variant demonstrated an
  end-to-end gain for that workload.
- **Boundary:** empirical outcome with complete recorded seeds and
  workloads, not a population-variance certificate, confidence theorem,
  statistically established ranking, exact hardware speed comparison or
  claim that tuning cannot pay off when amortized. Concurrent research
  processes and actual-vs-predicted timing differences are documented.
- **Lean coverage:** none for the stochastic MSE identity, cost model or
  experimental findings in this checkpoint.

---

#### `PR-RATE-11`: Weighted Wave-Profile Global Certificate

- **Specification:** raw uniform 1D Allen–Cahn wave, `T=1/20,t=0`,
  positions `[-2,-1,0,1,2]`, weights `1/5`, one positive scalar rate
  throughout all trees. Objective `Vbar(lambda)=sum_j w_j Var(H_lambda,x_j)`.
  This is the equal-sample profile-MSE objective; it differs from the
  point-root or unequal-allocation objectives.
- **Conventional derivation:** nonnegative weighted sums preserve convexity;
  rate-invariant means make moment and variance excess identical. The
  leading short-time minimizer is
  `sqrt(sum_j w_j f(phi_j)^2 / sum_j w_j phi_j^2)` under nondegeneracy and
  the stated small-time expansion. See
  [derivation](estimator-integrity/profile-rate-efficiency.md).
- **Verified numerical construction:** fourteen degree-seven polynomial
  residual witnesses, exact exponential/logistic coordinate intervals,
  signed interval Horner evaluation and convex global lower bounds.
  [Witnesses](results/profile-certificate/witnesses.json.gz) and
  [summary](results/profile-certificate/summary.json) retain exact fractions.
  The certificate establishes `Vbar(1/2)-inf Vbar < 3.848558e-5` and
  `inf Vbar > .0041421075`; relative excess is below 0.93%.
- **Actual policies:** convex upper interpolation at the exact rational
  representation of the benchmark's binary-float rates gives relative
  excess below 1.60% for grid short-time and 1.006% for grid selected.
  Off-node lower bounds are conservatively global; they do not establish
  a strict variance ordering of those two actual policies at equal n.
- **Lean coverage:** `weightedProfile_convexOn`, `weightedProfile_enclosure`,
  `weightedProfile_excess_le`, `weightedProfile_variance_shift`,
  `weightedProfile_variance_excess_eq`, `convexProfile_upper_interpolation`.
- **Omitted obligations:** stochastic correspondence, mild-PDE comparison,
  rational verifier correctness, concrete fractions, production floating
  arithmetic and transfer to other horizons, grids or tuple laws. Numerical
  collocation checks are corroboration only. No universal optimizer or
  publication-priority claim follows.

#### `PR-COST-2`: Profile Reuse and Conditional Allocation Comparison

- **Loss identity:** conditional on independently frozen rates and positive
  integer counts, independent unbiased point averages have expected grid
  MSE `Vbar/n`. Averaging this loss over R requested curves does not divide
  its expectation by R; the curves are not pooled.
- **Exact allocation comparison:** the matching certificate bounds the
  actual binary-float policy rates and divides variance intervals by the
  predicted-budget phase's frozen counts. At those allocations, all four
  alternatives have larger expected MSE than the cheap grid policy at
  each of R=1 and R=10; this ordering is not claimed for the fixed-n phase.
  Numerical grid selection's expected-MSE ratio is at least 5.0312 for R=1
  and 1.3873 for R=10. These are conditional ideal-real-estimator results,
  not inequalities for observed replicate losses or execution times.
- **Experiment:** [frozen protocol](results/profile-efficiency-protocol.md),
  20 workloads per group, five policies, two sample-allocation phases,
  reuse R=1/10, 2,200 curves and 139,621,200 evaluation trees. All 22
  independent archive checks passed. No timed stopping or outlier removal.
  [Report](results/profile-efficiency-results.md) records actual-vs-predicted
  cost, setup, calibration, seeds and empirical distributions.
- **Observed result:** numerical grid selection had 2.299 times the cheap
  grid policy's aggregate RMSE at R=1 and 1.146 times at R=10 under the
  predicted budgets. The numerical selector did not repay setup in these
  workloads. The certificate procedure itself was offline.
- **Lean coverage:** `amortizedProfileLoss_lt_iff`,
  `amortizedProfileLoss_break_even`, `amortizedProfileLoss_reuse_break_even`,
  `continuousBudget_profileLoss` prove real-valued cost-model algebra.
  They do not establish the sampling MSE identity, finite moments,
  calibration accuracy, integer floor rule or measured runtime model.
- **Continuation decision:** retain the cheap grid rule for this benchmark;
  continuation-aware q is optional and untested, not a failed experiment.

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
- **Empirical / Symbolic Evidence:** The source gives the population-loss identity and a proposed falsification test; no completed derivative-supervised training result is registered for this claim.
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
- **Empirical / Symbolic Evidence:** The source gives a pathwise product-rule derivation. Its proposed sensitivity experiment is not recorded as completed here.
- **Novelty / Prior Art:** Reiman & Weiss (1989); Glasserman (2003); Peng et al. (2018). Specialization to coding-tree node counts.
- **Dependencies & Open Obligations:** Singular at $a_r = 0$; requires second-moment certification for Gaussian intervals.

---

#### `PR-SEC-9`: Challenger-Model $2r$ Selection Certificate
- **Exact Statement:** Let $v_1, \dots, v_m$ be candidate solver outputs and $\widehat u$ an independent reference satisfying $\|\widehat u - u\| \le r$. Then the candidate minimizer $\widehat \ell = \arg\min_\ell \|v_\ell - \widehat u\|$ satisfies $\|v_{\widehat\ell} - u\| \le \min_\ell \|v_\ell - u\| + 2r$.
- **Source:** `docs/research/estimator-integrity/secondary-candidates.md` §Candidate 9, Eq. (9.3).
- **Assumptions:** Finitely many candidates; common norm and grid; certified radius $r$ holding with probability $\ge 1 - \delta$.
- **Conventional Proof Status:** Proved theorem. Two-step triangle inequality on normed space; sharpness of factor 2 established by 1D counterexample.
- **Lean 4 Coverage:** None.
- **Implementation Correspondence:** Ordinary solver comparison tables do not implement a certified reference radius automatically.
- **Empirical / Symbolic Evidence:** The source contains a conventional one-dimensional sharpness example; no executed certified solver-selection experiment is registered here.
- **Novelty / Prior Art:** Standard metric oracle inequality; a proposed audit protocol, with publication novelty unestablished.
- **Dependencies & Open Obligations:** Requires reference $\widehat u$ to possess certified error bound $r$ (needs finite variance).

---

#### `PR-SEC-10`: Short-Time Wave Proposal Optimization
- **Exact Statement:** For 1D nonlinear wave branching estimator $H_t$ with global clock rate $\lambda_t = \gamma t$, the asymptotic variance as $t \downarrow 0$ is $\operatorname{Var}(H_t) = t^2 [\gamma |b|^2 + \frac{1}{3\gamma} \sum_k \frac{|a_k|^2 |b|^{2k}}{q_k} - \operatorname{Re}(\bar b f(b))] + o(t^2)$. Minimized by $q_k^* = |a_k| |b|^k / A_b$ and $\gamma^* = A_b / (\sqrt{3} |b|)$.
- **Source:** `docs/research/estimator-integrity/secondary-candidates.md` §Candidate 10, Eq. (10.6)–(10.7).
- **Assumptions:** Local data $b = \phi(z) \ne 0$; $C^2/C^1$ initial data; finite polynomial $f$; small horizon $t \downarrow 0$.
- **Conventional Proof Status:** Proved theorem. Complete asymptotic Taylor and geometric branching tree expansion in `secondary-candidates.md` §10.
- **Lean 4 Coverage:** None.
- **Implementation Correspondence:** No executed wave-equation implementation is registered in this repository. A sibling-project reference alone is not validation evidence for this claim.
- **Empirical / Symbolic Evidence:** Conventional asymptotic derivation; no reproducible simulation artifact registered here.
- **Novelty / Prior Art:** Chan & Privault (2026); Henry-Labordère & Touzi (2021). Specific joint minimization is repo derivation.
- **Dependencies & Open Obligations:** Requires the source's nondegeneracy and uniform asymptotic control. This concerns a wave-equation estimator, not the parabolic Allen–Cahn traveling-wave certificate; it is outside the selected lambda checkpoint.

---

### Family 5: Multifactor Merton Theorems

Historical application records: implementation targets and open obligations
in this family are retained from the Merton programme, not assigned as
current variance-reduction work. Mathematical status is still governed by
each underlying proof.

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
- **Implementation Correspondence:** Design criterion for the historical two-factor benchmark; not an active implementation assignment.
- **Empirical / Symbolic Evidence:** Evaluated analytically for 2-factor OU specification.
- **Novelty / Prior Art:** Checkable algebraic condition for the proposed benchmark; publication novelty is unestablished.
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
- **Implementation Correspondence:** Historical multifactor reference proposal; the existing one-factor Merton examples do not constitute a general matrix-Riccati library implementation.
- **Empirical / Symbolic Evidence:** SymPy polynomial coefficient matching.
- **Novelty / Prior Art:** Matrix Riccati systems for affine term structure and portfolio choice are classical; Liu (2007), Kim & Omberg (1996). Their use as a benchmark is a specialization, not an established novelty claim.
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
- **Implementation Correspondence:** Historical implementation proposal; no claim that the generic full-covariance state-dependent mechanism is implemented in `parabolab/mechanism.py`.
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
- **Implementation Correspondence:** Historical proposed two-factor experiment; not a completed validation or an active research assignment.
- **Empirical / Symbolic Evidence:** Prototype Vasicek 1D smoke tests.
- **Novelty / Prior Art:** Candidate contribution; scoped literature search located no source combining full-covariance state-dependent coding with multifactor Riccati benchmarks.
- **Dependencies & Open Obligations:** Discharging hypotheses (especially $L^1/L^2$ integrability and mild uniqueness) is an open research problem.

---

## Omitted Lean Obligations Summary

For every claim touching Lean 4, the exact boundary between formalized mathematics and external paper obligations is recorded below:

| File | Formalized Lemmas | Omitted Probabilistic & Analytical Obligations |
|---|---|---|
| `formal/EstimatorIntegrity/FiniteTree.lean` | `FiniteMechanism`, `MomentVector`, `momentStep` | Continuous-time Poisson process, Brownian increments, standard Borel state space, spatial Markov transition semigroup. |
| `formal/EstimatorIntegrity/MomentIteration.lean` | `momentStep_mono`, `picard_mono`, `picard_le_prefixed`, `picard_iSup_least`, `list_prod_iSup_of_monotone`, `momentStep_iSup_picard`, plus two private helpers | Identification of abstract Picard supremum with continuous-time tree expectation $\mathbb E\|H\|^p$; almost-sure tree exhaustion; Fubini-Tonelli measure integration. |
| `formal/EstimatorIntegrity/Dym.lean` | `dym_fz0_coefficient`, `one_div_not_intervalIntegrable`, `one_div_intervalIntegral_unbounded`, `continuous_density_intervalIntegral_unbounded` | 5-particle random tree event probability; joint Gaussian density conditioning over $(\tau_1, \tau_2, Y)$; signed-part decomposition $\mathbb E[H^+] = \mathbb E[H^-] = \infty$. |
| `formal/EstimatorIntegrity/Proposal.lean` | `sqrtProposal_sum`, `sqrtProposal_pos`, `secondMoment_ge_oracle`, `secondMoment_sqrtProposal_eq`, `sqrtProposal_ratio_bounds`, `oracle_ratio_of_relative_error`, `secondMoment_uniformMixture_le` | Pilot $\sigma$-algebra $\mathcal P$; conditional expectation tower property; inductive composition over random trees with $B_n$ decisions; empirical concentration probabilities $1 - \delta$. |
| `formal/EstimatorIntegrity/ExponentialRate.lean` | Kernel/topology-factor positivity and model-objective AM–GM algebra, including `expKernelFactor_pos`, `topologyFactor_pos_of_pos`, `modelRateObjective_ge_amgm`, `modelRateObjective_at_optimum`, `modelObjective_eq_lower_bound_iff` | Differentiation of the stochastic full-tree objective, dominating integrable bounds, integral strict convexity and full-tree minimizer existence. |
| `formal/EstimatorIntegrity/RateCertificate.lean` | `rateSelection_excess_le`, `rateSelection_excess_le_inf`, `upperLower_excess_le_inf`, `commonMean_variance_excess_le`, `global_lower_of_interval_and_exterior` | Finiteness and rate-invariant mean, killed-tree domination, tail and quadrature estimates, optimizer error, exterior topology bounds, concrete witnesses and program correctness. |
| `formal/EstimatorIntegrity/AllenCahnBounds.lean` | `allenCahnBranchPolynomial_nonneg`, `allenCahnBranchPolynomial_mono`, `allenCahnMomentField_nonneg`, `allenCahnMomentField_mono`, `allenCahnMomentField_interval_upper`, `allenCahn_postfixed_box_slope` | Actual random-tree/code correspondence, terminal bounds, ODE existence/comparison, analytic integration, stochastic domination, rational-program soundness and concrete witness values. |
| `formal/EstimatorIntegrity/ConvexEnclosure.lean` | `convexEnclosure_right`, `convexEnclosure_left`, `convexEnclosure_right_exterior`, `convexEnclosure_left_exterior`, `convexEnclosure_cell_lower_envelope`, plus two private helpers | Finite-moment/extended-value stochastic convexity, valid numerical endpoint bounds, cell-envelope minimization algorithm, rational program correctness and concrete objective certificates. |
| `formal/EstimatorIntegrity/ProfileEfficiency.lean` | `amortizedProfileLoss_lt_iff`, `amortizedProfileLoss_break_even`, `amortizedProfileLoss_reuse_break_even`, `continuousBudget_profileLoss`, `weightedProfile_convexOn`, `weightedProfile_enclosure`, `weightedProfile_excess_le`, `weightedProfile_variance_shift`, `weightedProfile_variance_excess_eq`, `convexProfile_upper_interpolation` | Stochastic profile-MSE identity, independence, all integrability and analytic bridges, concrete rational bounds, integer sample allocation, measured cost model and production roundoff. |

The twenty-six public declarations in the last four rows, plus two private
convex-enclosure helpers, passed the full `lake build`: 3,391 jobs completed
without warnings. Reported axiom dependencies for all public declarations
were only `propext`, `Classical.choice` and `Quot.sound`; the public convex
declarations' audits transitively cover their private helpers. The profile
checkpoint records that historical Python verification; the
[integration record](results/integration-2026-09-16.md) records current
checkout checks. These checks verify
their specified scope and do not discharge the omitted stochastic/numerical
soundness obligations listed above.

---

## Audit Checklist

- [x] Every registered claim assigned a stable identifier (`PR-MOM-*`, `PR-MEAN-*`, `PR-DYM-*`, `PR-PROP-*`, `PR-RATE-*`, `PR-COST-*`, `PR-SEC-*`, `PR-MM-*`).
- [x] Clear demarcation between complete proofs, conditional theorems, prior-art overlaps, and conjectures.
- [x] Lean theorem names match exact declarations in `formal/EstimatorIntegrity/*.lean`.
- [x] Omitted obligations explicitly stated for every formalized item.
- [x] No claim described as proving more than it mathematically establishes.
