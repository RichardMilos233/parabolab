# R03 — Sampling, nesting, and population methods for a longer horizon

Research date and search cutoff: **27 September 2026**. This is a bounded primary-source survey and paper-based screening, not an implementation, numerical experiment, or new formalized theorem. Research role requested by the parent: `gpt-6-astra`, maximum reasoning; the runtime model identity is not independently observable here. Only this report was written.

The most promising sampling-related escape route is **recursive averaging before nonlinear multiplication**, possibly combined with analytically justified ghost cancellation. Merely averaging complete raw trees, changing their proposal law, or reducing the maximum offspring count does not establish a longer integrable horizon. Whole-tree particle resampling is already direct prior art for nonlinear branching PDEs; it is not a new consequence of applying a generic particle filter.

## Project baseline and scope

The project represents arbitrary derivative nonlinearities through Nguwi–Penent–Privault coding trees. Its exact constant-data Allen–Cahn baseline has a raw-tree absolute first-moment ceiling

\[
T_{\rm abs}=(3\pi-2\log3)/5\simeq1.44551068.
\]

For uniform raw tuples and one common exponential rate, the optimized second-moment horizon is approximately `0.703890`; the saved rigorous upper certificate is `<0.705`. The earlier report establishes these under its stated support, reciprocal-weight, and completion assumptions. Those are **existing local results**, not results rerun here. Sources: [long-horizon theory](../../2026-09-25-long-horizon/04-theory.md), [raw codewise moment system](../../../estimator-integrity/allen-cahn-codewise-certificate.md), and [adaptive proposal results](../../../estimator-integrity/adaptive-proposals.md).

The first ceiling concerns the same completed-tree expansion under supported nonexplosive importance proposals. It is not a theorem about every possible regrouping of signed trees. Any new algorithm must separately establish: its target identity; existence of its required moments; almost-sure completion; and expected work. A low sample variance or a fixed count of outer particles proves none of the others.

## Primary sources examined

| ID | Exact source | Sections examined and relevance |
|---|---|---|
| S1 | Huang–Privault, [Stability analysis of a branching diffusion solver for semilinear heat equations, arXiv:2502.17853v2](https://arxiv.org/html/2502.17853v2), revised 9 March 2026 | Definition 2.2, (2.3), (2.4a–b), Assumption Hρ, Propositions 2.5–2.6, Theorems 2.8/2.10, Sections 6–7; changed coding mechanism and sufficient integrability criteria. |
| S2 | Huang–Privault, [Probabilistic representation of ODE solutions with quantitative estimates, arXiv:2502.10644v3](https://arxiv.org/html/2502.10644v3), revised 9 November 2025 | Theorems 4.1–4.2, Sections 6–7, Assumption 5.2, Lemma 8.1; quantitative moment conditions and a nonexponential clock construction. |
| S3 | Warin, [Variations on branching methods for non linear PDEs, arXiv:1701.07660](https://arxiv.org/pdf/1701.07660) | Sections 2.1.2–2.1.3, 2.2.1–2.2.3 and 3; nesting and ghost/antithetic representations with longer-maturity numerical examples. |
| S4 | Henry-Labordère–Oudjane–Tan–Touzi–Warin, [Branching diffusion representation of semilinear PDEs and Monte Carlo approximation, arXiv:1603.01727](https://arxiv.org/pdf/1603.01727) | Theorem 3.5, Assumption 3.10, Theorem 3.12, Section 5.1 and Appendix A, (A.1)–(A.2), printed pp. 27–28; derivative weights, lifetime laws, and **nonlinear tree-state resampling**. |
| S5 | Kuntz–Crucinio–Johansen, [The divide-and-conquer sequential Monte Carlo algorithm: theoretical properties and limit theorems, arXiv:2110.15782](https://arxiv.org/pdf/2110.15782) | Assumptions 1–2, Theorems 3–6, Appendix D; unnormalized unbiasedness, normalized bias, and independent child populations. |
| S6 | Heine–Burrows, [Multilevel bootstrap particle filter, arXiv:2104.08198](https://arxiv.org/pdf/2104.08198), Bernoulli 29(1), 2023 | Algorithm 1, Assumptions 1–2, Theorems 1–3 and discussion; signed resampling already exists, with fixed-time asymptotic guarantees. |
| S7 | Blanchet–Glynn, [Unbiased Monte Carlo for optimization and functions of expectations via multilevel randomization](https://web.stanford.edu/~glynn/papers/2015/BlanchetG15.pdf), WSC 2015 | Sections 2–3, Assumptions 1–3 and Theorem 1; randomized nested estimation under smoothness, growth and moment assumptions. |
| S8 | Blanchet–Glynn–Pei, [Unbiased multilevel Monte Carlo: stochastic optimization, steady-state simulation, quantiles, and other applications, arXiv:1904.09929](https://arxiv.org/pdf/1904.09929) | Section 2, Assumption 1, equations (2)–(8), and Section 3/Theorem 1; level-difference variance versus sampling cost and split-sample antithetic cancellation. |

The source summaries below are deliberately short. Subsequent transfer arguments, screening calculations, and proposed tests are this survey's analysis, not claims established by the cited papers.

## Candidate 1 — The 2026 binary normalized coding mechanism

**Closest result.** S1 studies the semilinear equation with nonlinearity `f(u)`. Its factorial-normalized spatial derivative/composite codes support at most binary branching. Propositions 2.5–2.6 supply sufficient L1 bounds under derivative growth assumptions; the representation results retain integrability/regularity conditions. These are not a general theorem for `f(u, Du, …, D^n u)` or unlimited T. [S1](https://arxiv.org/html/2502.17853v2)

The exact α=0 specialization of Definition 2.2, equation (2.3), is

\[
\mathcal M(\mathrm{Id})=\{(1,f)\},\qquad
\mathcal M(f^{(j)})=
\{(1,f,f^{(j+1)})\}
\cup\{(-\tfrac12,\partial_i,\partial_i\circ f^{(j+1)}):1\le i\le d\}.
\]

Equations (2.4a–b) assign probability `1/(d+1)` to each displayed α=0 alternative. In one dimension both probabilities are `1/2`. This is a representation change; it must be assessed separately from proposal tuning.

**Paper-based negative screen on the project's flat case.** Let `φ=1/2` and `f(z)=z−z³`. A code with positive spatial derivative order has zero terminal value. Every positive binary split preserves total spatial derivative order across its children, while a diffusion split increases it by two. Thus any finite completed tree started with positive derivative order contains a positive-order terminal leaf and contributes zero. Subject to the stated nonexplosion and exact raw-label conventions, only the `F_j → (F_0,F_{j+1})` alternatives contribute.

Consequently the proposed new absolute-moment reduction is again

\[
J'=a,\quad a'=ab,\quad b'=ac,\quad c'=ae,\quad e'=0,
\qquad (J,a,b,c,e)(0)=(1/2,3/8,1/4,3,6).
\]

Writing `s=J−1/2` gives

\[
s'=3/8+s/4+(3/2)s^2+s^3.
\]

This is the existing raw L1 system, with the same `1.44551068` ceiling. With the paper's one-dimensional probabilities, a common exponential clock, and identical treatment of zero labels and surviving constant-source leaves, the nonzero second-moment terms are also unchanged: the predicted uniform L2 ceiling remains `0.703890`. In particular, `F_3` surviving leaves still carry survival weights; replacing them by a deterministic constant would be another change.

**Status of this calculation:** a hand-derived inference for independent review, not a theorem added to the proof registry, not a verified correspondence, and not a numerical or Lean result. The parent was given the exact mechanism/probability formulas for independent checking.

**Remaining opportunity and why T might improve elsewhere.** For nonconstant data, the two representations can group composite derivative terms differently before taking absolute values. This may alter continuation moments or reduce the number of generated codes. A smaller maximum number of children alone gives no moment ordering: additional composite codes, derivative growth and weights can offset it.

**First falsification gate.** Independently reproduce the flat L1/L2 identity above. If it holds, reject this route as a flat-horizon cure. Only then compare nonconstant waves or a single spatial mode with matched terminal data, clock, tuple support, zero policy, derivative evaluation cost and node budget. Compare complete moment bounds and work, not just offspring arity.

**Feasibility and novelty.** High feasibility for the flat screen; conditional for nonconstant full-tree certification. Reimplementing S1 is reproduction. A credible extension would be a proved moment/cost comparison on nonconstant data, or a new binary construction for genuine higher-jet nonlinearities with its own representation theorem. No such extension is established here.

## Candidate 2 — Continuation-aware joint clock and tuple control

**Closest results.** Arbitrary positive lifetime densities already appear in S1; Hρ requires a positive lower density on the relevant interval and an exponential survival lower bound. S2, Lemma 8.1, constructs a uniform-on-the-working-interval/exponential-tail law under its stated `T<1` condition. Neither result proves that a nonexponential law universally enlarges T. [S1](https://arxiv.org/html/2502.17853v2), [S2](https://arxiv.org/html/2502.10644v3)

The project itself already proves the first-event optimizer in its adaptive-proposal Theorem 6.2. For a terminal contribution with second moment `A0` and branch-time/tuple contributions `B_z(s)`, unconstrained event masses formally minimize

\[
\frac{A_0}{r_0}+\sum_z\int_0^T\frac{B_z(s)}{r_z(s)}\,ds
\quad\text{subject to}\quad r_0+\sum_z\int_0^T r_z(s)\,ds=1.
\]

The optimizer assigns mass proportional to the square roots of the continuation second moments. Computing and certifying those moments, with a useful cost constraint, is the missing part; the square-root identity is not a new research contribution.

**Mechanism for extending T.** A code/time/state-aware policy could avoid oversampling expensive low-value branches while allocating enough probability to large contributions. It may enlarge the L2-admissible interval beyond the current common-rate family, within the same raw L1 envelope. Nonexponential clocks belong in this joint optimization rather than being assumed intrinsically superior.

**Hard limits and correctness.** The local flat `T_abs` remains binding for supported proposals on the same expansion. Learned proposals require exact actual likelihoods and an independent frozen pilot or a proved predictable conditional construction. State-dependent hazards require path survival factors `exp(−∫h_s ds)` and event density factors, not simply substituting `λ(x)` into an exponential-clock formula. Unbounded code-dependent rates can destroy nonexplosion; a probability floor is not a completion proof. Gamma near-zero singularity remedies from Malliavin-weight methods address a different issue from direct derivative-code terminal singularities.

**First falsification gate.** Use the exact flat finite-code moment system to compare the best bounded code/time policy with the optimized common-rate baseline, including expected nodes. If its best certified horizon/cost tradeoff is negligible, stop before state-dependent learning. For a nonconstant extension, use continuation bounds rather than training-set sample variance.

**Feasibility and novelty.** Feasible as a bounded control/certification problem on a finite code set; conditional for arbitrary jets. A defensible contribution is an attainable horizon-versus-work guarantee with nonexplosion and learned-policy error control. Generic importance sampling, nonexponential clocks, and code-dependent sampling are already established ideas. This is a useful within-envelope route, not the leading answer for `T>T_abs`.

## Candidate 3 — Recursive independent subtree averaging, with a conditional multilevel extension

**Closest result.** Warin's Section 2.1.3 uses multiple independent estimates of each continuation factor at a branch. Sections 2.2.1–2.2.3 combine nesting with renormalization; longer-maturity examples improve, but cost and memory become severe. This is numerical evidence for selected semilinear problems, not a global higher-jet theorem. [S3](https://arxiv.org/pdf/1701.07660)

**Proposed project version.** For code `c`, form a recursively defined estimate

\[
S_c=\frac1{m_c}\sum_{r=1}^{m_c}Y_c^{(r)},
\]

where each `Y_c` samples its parent event and, on a branch, multiplies **independent** child estimates `S_child`. Different replicas and different child groups are independent conditional on the birth time/state. Repeated identical codes still receive separate groups. The mean of a product is then the product of the appropriate conditional means. Reusing one average to estimate a square gives `E[bar Y²]=μ²+Var(bar Y)` and changes the target.

**Why this could change the horizon.** Averaging before multiplication groups many signed expansions. It is not a new probability law for one raw tree, so the existing same-expansion proposal no-go cannot simply be applied. With finite child moments,

\[
E[S_c^2]=(1-m_c^{-1})\mu_c^2+m_c^{-1}\mathcal R_c(M),
\]

where `M_c=E[S_c²]`, `μ_c=E[S_c]`, and `R_c` is the parent-event second-moment operator using the new child moments. This suppression acts at every recursive level. Averaging a finite number of already completed raw trees only at the outermost level is a different operation and does not repair an infinite absolute first moment.

For the flat finite-code model, a candidate common-exponential moment equation is

\[
M'_c=\lambda M_c+(1-m_c^{-1})(2\mu_c\mu'_c-\lambda\mu_c^2)
+\frac1{m_c\lambda}G_c(M),\qquad M_c(0)=\mu_c(0)^2,
\]

using the existing polynomial `G`, including the raw tuple probabilities. As all `m_c` grow, the formal limiting solution is `M_c=μ_c²`. On a fixed finite horizon, bounded exact code means therefore suggest an approach through continuous dependence and a moment supersolution. This is a **proposed proof route**, not a proved assertion that finite nesting works for every T. Mean identification is a separate obligation; using exact-solution boundary values in generation-stopped trees is one possible analysis device, though those values would not be used in the eventual algorithm.

**Hard limits.** Finite averaging cannot repair a conditional terminal random variable already outside L1, such as the raw Dym singularity, without first changing that singular representation. Recursive nesting can make the generated computation tree much larger: each branch may initiate `m_c` replicas per child. With bounded replication and bounded rates, a dominating branching argument is available, but the work bound can grow exponentially in both the replication factor and T. Moment finiteness without feasible work is not an acceptable win. Resource caps, early abandonment and failed-tree deletion bias the output unless corrected.

**First falsification gate.** Derive and independently check the five-dimensional flat moment system for `m=1,2,4,…`, with `m=1` reproducing the baseline. Pair its first predicted finite-moment extension with the exact expected-work recursion. Reject allocations whose cost explodes before the target accuracy is reached. Only after that should nonconstant conditional means or higher-jet branches be attempted. A relevant success criterion is a certified finite L2 interval beyond the current raw L2 limit, preferably beyond raw `T_abs`, at a stated total error/work budget.

**Novelty and feasibility.** Nesting itself is known. The plausible gap is a continuation-sensitive allocation rule and an exact moment/cost theorem for derivative-coded sums-before-products, separating it from outer averaging. The flat audit is feasible; a useful nonconstant/arbitrary-jet theorem is conditional on a tractable conditional moment bound.

### Where randomized multilevel debiasing can help — and where it cannot

Blanchet–Glynn's Theorem 1 assumes growth control, local twice differentiability and a finite sixth moment in the displayed sufficient conditions. Blanchet–Glynn–Pei's Section 2 instead states the general level-difference and cost contract; its split-sample difference cancels first-order terms. These are existing debiasing methods, not new branching-PDE results. [S7](https://web.stanford.edu/~glynn/papers/2015/BlanchetG15.pdf), [S8](https://arxiv.org/pdf/1904.09929)

For a proposed convergent approximation hierarchy, let `Δ_l` telescope to the desired target, `V_l=E[Δ_l²]`, and `C_l` be expected cost. A single-term estimator samples level `L` with mass `p_l` and uses `Δ_L/p_L`. It needs both

\[
\sum_l V_l/p_l<\infty,\qquad\sum_l p_l C_l<\infty.
\]

Their product is at least `(Σ_l sqrt(V_l C_l))²` by Cauchy–Schwarz. Thus a hierarchy with geometric variance decay `2^(−βl)` and cost growth `2^(γl)` has the usual admissible gap only when `β>γ`; this is a sufficient rate test under the target-convergence and integrability conditions, not a result already known for coding trees.

The first rejection test is precisely that variance/cost gap. Doubling replication at every nested branch can have much worse than geometric cost in the level, so ordinary nested-MC rates cannot be imported. Randomizing a depth cap does not magically create an integrable raw target, and polynomial nonlinearities do not automatically satisfy a generic theorem's linear-growth hypothesis. A bounded or otherwise stabilized hierarchy is needed before debiasing is credible.

## Candidate 4 — Ghost and antithetic cancellation at derivative branches

**Closest result.** Warin Sections 2.2.1–2.2.2, equations (2.12)–(2.16), subtract coupled ghost continuations and use Brownian antithetics. Section 3 treats second-derivative nonlinearities through alternative representations. The method reduces short-lifetime derivative-weight problems; its reported memory burden rises with maturity. [S3](https://arxiv.org/pdf/1701.07660)

**Possible transfer.** A local signed grouping may reduce the magnitude of a branch contribution before the outer product, potentially changing the absolute-moment equation. This is more promising for crossing a raw integrability boundary than merely reallocating probability to unchanged signed terms. Pairing compatible codes or deriving a low-order derivative representation that replaces singular direct terminal derivatives are possible bounded starting points.

**Applicability audit.** The project uses direct derivative-coded terminal factors rather than automatically inheriting Warin's Malliavin weights. Therefore neither its small-time cancellation estimate nor its variance result transfers by changing a switch in the sampler. One needs a new code identity, exact zero-expectation control term, coupling and moment proof. Antithetic pairing must happen within a contribution while preserving independence between distinct factors in a nonlinear product; sharing a ghost across factors can change the mean. For derivative order `r`, cancellation of too few terms leaves short-time powers singular, while enough cancellation can demand high regularity and many ghost evaluations.

The project's raw Dym example has both signed parts infinite on a fixed finite topology. A symmetric-looking sample or principal-value pairing is not an unbiased expectation of that raw variable. Any rescue must define and justify a different integral identity/PDE solution concept before it is called an estimator.

**First falsification gate.** Select one first- or second-order derivative code with a smooth manufactured solution. Derive the coupled identity and the small-time power of its conditional second moment. If the weighted time integral still diverges, reject it before full trees. Check the same identity for a nonlinear product of two derivative factors with separate couplings. Then compare moment growth and all ghost work against the matched raw code.

**Feasibility and novelty.** Conditional for a small code family; low confidence for arbitrary high-order derivatives. A credible gap is a finite-jet cancellation calculus with provable moment regularization and explicit work scaling. Generic antithetics, ghost particles and subtraction of a baseline are known; applying those names is not a contribution. This direction should be shortlisted only after one actual singularity or horizon bottleneck is shown to disappear algebraically.

## Candidate 5 — Interacting populations over whole trees, or independent child populations

**Direct nonlinear prior art.** S4 Appendix A already lifts the complete branching history to a Markov state, writes the estimator as generation factors `(A.1)`, and resamples by their absolute values, retaining normalization factors and the accumulated sign in `(A.2)`. Its particles are partial **trees**, not isolated live descendants. Section 6 gives numerical resampling comparisons. [S4](https://arxiv.org/pdf/1603.01727)

**Related guarantees.** DaC-SMC Theorem 3 gives unbiased unnormalized estimates under its positive bounded-weight assumptions; Theorem 4 controls bias of normalized estimates. Independent populations in different child subproblems are structural. Heine–Burrows already supplies signed resampling (Algorithm 1), a strong law (Theorem 1) and CLTs (Theorems 2–3) for its filtering setup. These are not ready-made guarantees for an unrestricted coding tree. [S5](https://arxiv.org/pdf/2110.15782), [S6](https://arxiv.org/pdf/2104.08198)

**Two honest formulations.**

1. Treat a whole partial forest, including codes, birth times, spatial states and accumulated signs, as one particle. Resample a fixed number of these forest replicas using exact generation potentials. This preserves the nonlinear child product inside each Markov transition and exposes a Feynman–Kac interpretation. It fixes the number of replicas, not the number of live branches inside each replica.
2. Build independent particle populations for separate child factors and combine their unnormalized estimates. Reusing one population requires an explicit unbiased product/U-statistic construction and a genealogy analysis. Distinct indices from an already interacting population need not be independent; omitting diagonal terms alone does not remove ancestral correlations.

**Why usable T might increase.** Resampling may reduce weight degeneracy and redistribute a work budget toward important partial trees. Exact cancellation of identical signed contributions can lower total variation. These mechanisms can improve practical variance before the raw ceiling; crossing it would require a separately proved regrouping/cancellation, not just the original absolute-value target.

**Hard limits and bias.** A linear Feynman–Kac functional is an expectation of a product along one Markov state trajectory. Nonlinear branching becomes such a problem only after a valid enlarged-state construction. Killing or cloning individual descendants while retaining the old product formula generally changes the nonlinear estimator. A self-normalized signed average is not the unnormalized PDE value. Nearby continuous states are not identical contributions: binning or merging them introduces an approximation. Beyond the raw L1 boundary the original absolute tree measure cannot be normalized into the proposed terminal target, so the standard absolute-weight SMC argument no longer justifies the answer. This does not prove an impossibility theorem for every redesigned signed population method.

Fixed population size also does not settle completion or expected work with random tree depth. The infinite-generation limit, genealogical sign cancellation, all-zero weight cases and any random stopping rule need explicit treatment. A fixed-generation SMC identity alone does not certify the final unrestricted algorithm.

**First falsification gate.** On a finite exact toy tree with signed coefficients, compare the exact target to: whole-tree resampling with all normalizers; independent child populations; and the tempting shared-pool product. The third should expose its covariance bias unless specifically corrected. Then use the flat Allen–Cahn baseline below its L1 ceiling to test variance times *total branch work*, not particle count. Reject the claim of fixed computational population if tree-state size still grows uncontrollably.

**Feasibility and novelty.** Feasible as a reproduction and finite-depth correctness audit; conditional as a longer-T method. Generic nonlinear tree-state resampling already exists in S4, and generic signed resampling in S6. A defensible new contribution would be a code-aware compression/cancellation scheme with a proved target identity, moment bound and total-work advantage. Mere transfer to a new code class is a narrower extension. Do not rank this as a proven cure for the project's raw integrability obstruction.

## Comparative recommendation

| Candidate | Can change the existing raw L1 boundary in principle? | Current assessment |
|---|---|---|
| 2026 binary coding | A changed representation can; flat reduction predicts **no change here** | Retain for nonconstant matched comparison; no flat-horizon claim |
| Joint clock/tuple control | No for the supported same-expansion flat class | Useful L2/cost optimization below the existing L1 ceiling |
| Recursive sums before products | Potentially, because it groups signed expansions | Best bounded mathematical feasibility study in this cluster; work may defeat it |
| Ghost/antithetic identities | Potentially, if cancellation precedes absolute values | Require one explicit transferable low-order identity before promotion |
| Whole-tree/child-population SMC | Ordinary absolute-weight version does not establish an escape | Known nonlinear prior art; conditional research case only with additional compression or cancellation |

None of these has been implemented, measured, or certified in this survey. The source-backed opportunity is more specific than “better sampling”: alter the random functional where necessary, then certify the new moment and work recursions. Claims of novelty remain bounded by the search below.

## Query and source-access log

All actions below were performed on 27 September 2026. Search snippets were used for discovery only; technical claims rely on the primary documents linked above. Search dates are not paper publication dates.

### Queries issued

1. `branching diffusion nested Monte Carlo Warin variance reduction interacting particle nonlinear PDE 2025 2026`
2. `branching Monte Carlo nonlinear PDE importance sampling non exponential lifetime antithetic multilevel branching 2024 2025 2026`
3. `Huang Privault Monte Carlo stability coded branching trees 2026 2502.17853`
4. `"branching" "PDE" "importance sampling" "adaptive" Monte Carlo Warin`
5. `"Divide-and-Conquer Sequential Monte Carlo" Lindsten unbiased normalizing constant`
6. `"signed" "sequential Monte Carlo" negative weights paper`
7. `Blanchet Glynn unbiased multilevel estimation expectations function expectation antithetic 2015 2018`
8. `"branching" "PDE" "Monte Carlo" "2026" variance reduction`
9. `"branching" "nonlinear PDEs" "2025" Monte Carlo variance`
10. `"signed particle" "annihilation" "Monte Carlo" arxiv`
11. `"negative weights" "particle filter" arxiv resampling`
12. `site.arxiv.org "branching" "PDE" "adaptive" importance sampling`
13. `site.arxiv.org "branching" "Monte Carlo" "long" "2025" PDE`
14. `"Multilevel bootstrap particle filter" Heine Burrows`
15. `"SCaSML" branching Monte Carlo`
16. `"unbiased" "nonlinear PDE" "multilevel" branching`
17. `"branching" "antithetic" "PDE" "2024"`
18. `"branching" "antithetic" "PDE" "2025"`
19. `"branching" "variance reduction" "Privault"`
20. `"branching diffusion" "variance reduction" after:2024-01-01 before:2026-09-28`
21. `"coding trees" "sampling" "Privault" after:2024-01-01 before:2026-09-28`
22. `"nested branching" "PDE" after:2020-01-01 before:2026-09-28`
23. `"Truncation and renormalization techniques" "branching"`

### Accesses and limits

- Opened the arXiv abstract pages for `2502.17853`, `2502.10644`, `1701.07660`; then opened the versioned full HTML for the first two and the full PDF for the third. Checked the revised versions instead of treating the 2025 abstract/title as current.
- Read the relevant full-text passages of S1–S8 using open/find. Exact anchors are the displayed definition/theorem/equation/section numbers above, rather than unverified URL fragments.
- Opened the arXiv abstract and six-page PDF of [Rhee–Glynn, arXiv:1207.2452](https://arxiv.org/pdf/1207.2452). It was supporting discovery; no theorem number from it is asserted here.
- Discovery also returned [SCaSML, arXiv:2504.16172](https://arxiv.org/abs/2504.16172) and the authors' [repository](https://github.com/Francis-Fan-create/SCaSML). Only search-result/author-readme information was examined; its defect-correction claims are outside this report's conclusions and require a full-paper audit in the residual-method workstream.
- S4 Appendix A was read in full parsed PDF text. Requests for screenshots of PDF pages with zero-based indices 26 and 27 failed with `Cache miss`; text access succeeded. This is a display-access failure, not a missing appendix.
- Warin's bibliography refers to “Truncation and renormalization techniques …” as forthcoming. Searches did not supply a verified standalone final paper; no independent theorem is attributed to that reference.
- Broad 2024–2026 searches returned many unrelated branching/particle papers. Their absence of a close match does not establish priority. No claim of an exhaustive literature search is made.
- Local read-only grounding: skill defaults/routing/ideation/profile, Git status, adaptive-proposal theorem, Allen–Cahn raw codewise certificate, prior long-horizon theory/report, Dym nonintegrability note, sampling diagnostics and `parabolab/mechanism.py`. The working tree already contained user/research changes; none were modified.

The five candidate assessments are `searched`; the proposed higher-jet and beyond-ceiling improvements remain `conditional`, except where a negative flat screen is stated explicitly. There are no new measured gains, test results, or Lean coverage to report.
