# Research plan after the approximate branching-rate sweet spot

The recommended next milestone is **a practically certified rate selector for the existing branching PDE estimator, evaluated by solution accuracy per total computation cost**. Start with the current Allen–Cahn family. Develop better tuple proposals as a controlled extension once the rate-only result is credible.

The central research question is: **Can we select a sampling policy that has a useful error guarantee and improves PDE estimation after paying for its own tuning?** Finding more decimal places of an approximate optimal rate is less valuable than answering that question.

This document proposes future work. Existing repository results and published literature supply the evidence; the proposed experiments, implementations and new mathematical arguments remain to be undertaken.

## Current evidence and its limits

Here, λ is the rate of the exponential particle lifetime distribution, not a PDE coefficient. Its optimum depends on the tree representation, tuple probabilities, root code, starting state and remaining time. The active project concerns branching estimation of nonlinear PDE solutions; the multifactor Merton application remains inactive.

The latest checkpoint selects λ ≈ 0.73055 for uniform tuples and λ ≈ 0.73049 for the terminal-data proposal, at the Allen–Cahn wave root `(t,x)=(0,0)` with `T=0.05`. This uses depth-2 moment quadrature of order 4 on `[0.2,2]`. The older sweep records approximately 0.72347 at the same horizon using a depth-1 objective. These are different approximations, not competing certified values of the unrestricted optimum. [Checkpoint](lambda-q-optimization-summary.md), [older sweep](../../examples/exponential_rate_sweet_spot.py).

On the latest 21-point grid diagnostic, the recorded mean empirical variances are 0.00745281 for the default, 0.00474964 for rate-only tuning, 0.00739695 for proposal-only tuning and 0.00458153 for combined tuning. These are one-seed observations. The earlier 2,000-tree, one-state comparison reports approximately 26% lower empirical variance for combined tuning, but explicitly establishes neither an incremental proposal benefit nor an end-to-end speedup. Both records are preliminary evidence, not population-moment certificates. [Recorded evidence](lambda-q-optimization-summary.md#repository-integration-check-14-september-2026).

The repository already contains conditional mathematical results on full-tree minimizer existence, convergence of exact cutoff minimizers, an all-code tilted-moment majorant and an additive rate-selection error bound. It also contains the classical local square-root proposal rule. These results should be treated as the starting point. The implementation does not yet certify its quadrature error or the unrestricted moment at its selected rate. [General rate-selection note](estimator-integrity/general-rate-selection.md), [proposal note](estimator-integrity/adaptive-proposals.md).

The distinction between estimator representations matters even for an exactly solvable PDE. The standard-binary Riccati formula is an oracle for its particular binary estimator. The historical `binary_control_optimum` rows instead optimize a depth-2 derivative-coded moment and place it alongside standard-binary Riccati values. Consequently, those rows are not exact binary optima and their columns do not isolate a rate effect. Correct the mechanism comparison and associated labels before using this artifact as oracle evidence. [Control script](../../examples/exponential_rate_sweet_spot.py), [moment implementation](../../parabolab/rate_optimization.py).

## Literature landscape

The literature supports a focused contribution around reliability and efficiency. Generic importance-sampling convexity and adaptive selection are established: Ryu–Boyd study exponential-family variance optimization, while Badouraly Kassim–Lelong–Loumrhari optimize jump intensities through sample-average approximation. Their results motivate methods, but do not automatically cover recursive coding-tree moments. [Ryu–Boyd][S4], [Badouraly Kassim et al.][S5].

The closest recent stability reference is Huang–Privault's **9 March 2026 revision**. It uses normalized derivative-composition codes, at most two offspring per branch, and specific code-dependent probabilities. Its displayed integrability bounds in Propositions 2.5–2.6 concern absolute first moments; they are not ready-made second-moment or rate-selection certificates for this repository. [Huang–Privault, v2][S3].

Other proposed extensions also have substantial precedent. General lifetime laws and particle cost appear in Henry-Labordère et al.; Warin studies modified differentiation, nesting and variance reduction. Pruned representations have a separate older literature. Consequently, a Gamma clock, a U-shaped variance curve, a square-root proposal, or a truncation argument alone would be a weak novelty claim. [Henry-Labordère et al.][S6], [Warin][S7], [Blömker–Romito–Tribe][S8].

For later solver comparisons, the field extends beyond the original deep BSDE and Galerkin baselines. Multilevel Picard methods have complexity guarantees under specified semilinear assumptions. A July 2026 preprint introduces D2SRM for Hessian-dependent equations under restrictive regularity and weak-coupling conditions. These are possible comparators on overlapping problem classes, not universal replacements. [Neufeld–Nguyen–Wu][S10], [Zhao–Long][S11].

## Ten potential directions

### 1. Make the approximate λ selector practically certifiable

**Priority: first; strongest candidate for the main mathematical contribution.**

The question is whether the computed rate is demonstrably near-optimal for the unrestricted estimator on a useful interval. The current scalar bound can be conservative because it pools very different code magnitudes and offspring products into one worst-case constant.

Proposed work: construct code-dependent upper bounds for the actual Allen–Cahn mechanism, retaining exact zero derivatives, scalar homogeneity and the actual tuple probabilities. Couple those bounds to validated time and Gaussian integration, including any spatial-tail error. A vector ODE or integral supersolution is a candidate route; whether it is sufficiently sharp remains open.

The existing theorem gives the target structure:

\[
M(\widehat\lambda)-\min_{\lambda\in I}M(\lambda)
\le C_I r^{-(K+1)}+2\delta+\eta,
\]

Here `M=E|H|²`, `K` is the killed depth, `r>1`, and `N` counts total branching clock expiries, not all sampled nodes. The constant `C_I` bounds `E[r^N|H|²]` uniformly on the rate interval. The required numerical error is `sup_{λ∈I}|M̃_K(λ)−M_K(λ)|≤δ`, and the optimization error is the objective gap `M̃_K(λ̂)−inf_I M̃_K≤η`. A derivative tolerance or bracket width alone does not supply either bound. Under mean invariance, the same additive gap applies to variance. The new work is making these quantities usable, not proving this displayed inequality again. [Existing theorem](estimator-integrity/general-rate-selection.md#5-quantitative-error-of-the-selected-rate).

**Success:** a nonvacuous certificate at a useful benchmark horizon, ideally the current `T=0.05`, with an error smaller than the performance differences being interpreted. Bound the objective gap first; closeness of λ itself additionally requires curvature control. Certification on an interval is not global certification without excluding better rates outside it.

**Risk and fallback:** if the bounds remain too loose, first certify constant-terminal Allen–Cahn or a shorter horizon and identify the particular code transition that prevents extension. The literature's majorant methods are starting tools, not a proof that this target is attainable. [S3][S3], [S6][S6].

### 2. Optimize total computational efficiency

**Priority: first, alongside Direction 1; most direct practical payoff.**

A rate that minimizes per-tree variance need not minimize time to an accurate solution. Larger trees, expensive proposal evaluations and deterministic tuning can reverse the apparent gain.

Proposed work: estimate variance and cost separately, compare the variance-optimal rate with a cost-aware choice, and determine the workload at which tuning pays for itself. For independent samples with finite moments and stable average cost, `Var(H) × E[cost per tree]` is a useful asymptotic objective. With available time `B` and tuning time `C_tune`, a planning approximation is

\[
\operatorname{MSE}\approx
\frac{\operatorname{Var}(H)\,\mathbb E[\text{cost per tree}]}{B-C_{\rm tune}}.
\]

This is not a universal finite-budget theorem, particularly when runtime and outputs are correlated. Use independently calibrated sample counts and complete scheduled batches; do not discard slow unfinished trees at a wall-clock deadline.

**Success:** lower independently evaluated solution RMSE at matched total budgets, with both one-off and amortized tuning costs reported. Include the short-time rate heuristic, λ=1 and the paper's rate rule as inexpensive comparators.

**Risk and fallback:** if no break-even workload is realistic, prefer the cheap heuristic or a reusable offline rate table. Sample reuse can be investigated for tuning, but production validation should initially remain independent. Jump-intensity optimization is relevant precedent; it does not justify naïvely recycling selected pilot outcomes into the final estimate. [S5][S5], [S6][S6]. Variance–cost tradeoffs also appear explicitly in nonlinear recursive Monte Carlo outside this PDE representation. [Dauchet et al.][S14].

### 3. Replace terminal tuple scores with continuation-aware proposals

**Priority: next algorithmic extension after the rate-only baseline.**

The present proposal scores alternatives using terminal products at the parent-birth state. It does not know the actual variability of their descendant trees. The local oracle is `q*(Z) ∝ sqrt(A_Z)`, where `A_Z` is the appropriate conditional continuation second moment, given the information available when the tuple is drawn.

Proposed work: approximate continuation moments with a small deterministic table or independent pilot, initially indexed by code and remaining-time bin. Such a table may average over spatial variation; it is an approximation to the local oracle unless its conditioning matches the actual tuple decision. Compare uniform, terminal-proxy and continuation-aware proposals at a common fixed λ. Then alternate proposal updates and rate optimization, freezing the proposal during each rate derivative calculation and during final evaluation.

**Success:** establish an incremental benefit over the tuned-rate, uniform-tuple baseline after charging pilot and lookup costs. Preserve positive probability for every live alternative, use its actual inverse probability, and reassess moment bounds under the changed proposal.

**Risk and fallback:** noisy estimates can allocate too little mass to rare but important alternatives; a floor preserves support but does not establish integrability. Joint global optimality does not follow from local square-root optimality. If the sophisticated proposal fails to pay for itself, retain the simpler rate-only result. The mathematical local oracle and pilot/freeze framework already exist in the [proposal note](estimator-integrity/adaptive-proposals.md). Gobet–Turkedjiev provide adjacent precedent for solution-dependent adaptive sampling in least-squares BSDE algorithms; extending that analysis to tuple choices in recursive trees remains open here. [Ryu–Boyd][S4], [Gobet–Turkedjiev][S12].

### 4. Let rates vary across root states, codes and remaining time

**Priority: medium; begin with root-state variation.**

The current demonstration selects λ at `x=0` and applies it to an entire profile. A rate useful at one point may be poor near a zero of the solution or in a region with different descendant activity.

Proposed work in increasing order of difficulty: choose one rate for a specified weighted grid objective; select a separate frozen global rate for each root; then consider code- and remaining-time-dependent rates at particle births. A birth-state rate remains constant during that particle's lifetime. A continuously state-dependent hazard is a separate, more demanding extension requiring an integrated hazard and correct conditional likelihood factors.

**Success:** reduce integrated profile error or worst-region error without excessive policy complexity. Evaluate on held-out root points and keep interpolation error separate from Monte Carlo uncertainty.

**Risk and fallback:** the short-time approximation `|f(Jφ)|/|φ|` becomes unsuitable at zeros and is not a finite-horizon guarantee. Start with a small code/time table rather than a learned continuous controller. Code-dependent lifetime choices have precedent in a different branching scheme. [S7][S7].

### 5. Explore lifetime distributions beyond the exponential family

**Priority: medium to long term.**

Even the best exponential rate can be suboptimal among all waiting-time distributions. Shape parameters could redistribute branch times in ways that changing the mean alone cannot achieve.

Proposed work: compare the tuned exponential clock with Gamma and a simple piecewise-hazard family on one integrable problem. Fix the tuple rule initially, charge the additional tuning cost and include correct density and survival weights at every node. Establish nonexplosion and moment assumptions for each family before interpreting its variance.

**Success:** a repeatable accuracy/cost gain over the best relevant exponential baseline, or a clear characterization of when changing lifetime shape has no benefit.

**Risk and fallback:** near-zero density and survival behavior can dominate inverse-weight moments. Conditions developed for Malliavin-weight estimators cannot be imported unchanged into derivative-coded trees. General clocks and Gamma choices are established methods; the contribution would need to be their analyzed application to this estimator and workload. [S6][S6], [S7][S7].

### 6. Compare and improve the tree representation itself

**Priority: early comparison of scope; larger implementation only after that review.**

Tuning can only improve the estimator being tuned. A different representation of the same PDE may have a better balance of derivative weights, branching frequency and computational cost.

Proposed work: compare the current derivative-coded mechanism, standard polynomial branching where applicable, and the revised Huang–Privault mechanism. The latter has a public implementation linked from the paper and reported comparisons up to dimension 1000. [S3][S3]. For each, first record the reachable code family, terminal assumptions, offspring law and moment claims. Later compare both common-rate settings and separately tuned settings, so representation effects can be separated from tuning effects.

**Success:** determine which representation offers the best useful certification and accuracy/cost combination for the chosen PDE family. Keep a representation-specific optimizer and certificate; an optimal λ is not transferable between mechanisms.

**Risk and fallback:** reducing offspring count may increase the complexity or size of terminal derivatives. The newer scheme is a comparator, not a presumed winner. This direction could redirect the main project if the present mechanism's limitations are structural.

### 7. Remove avoidable randomness with control variates and conditional expectation

**Priority: medium; attractive once the dominant variance sources are known.**

Importance sampling changes where randomness is spent. Another possibility is to remove analytically tractable random contributions or subtract a correlated estimator with known expectation.

Proposed work: identify constant-code subtrees or short conditional subtrees whose expected contribution is available exactly. Compare conditional integration with a simple heat-flow or linearized-PDE control variate. An antithetic pair of complete trees is another candidate; each member must retain a valid marginal law.

**Success:** reduce the variance remaining after λ tuning by more than the added evaluation cost. Estimate any control coefficient from independent training data and account for error in any approximate control expectation.

**Risk and fallback:** forcing sibling products to share randomness can change their expectation and bias the estimator. A control with unknown mean also introduces an extra estimation problem. Changes to the functional invalidate direct reuse of its old moment formulas. Related renormalization and antithetic constructions exist in branching methods, but their transfer must be checked. [S7][S7].

### 8. Extend the usable time horizon through restarting or multilevel methods

**Priority: long term; potentially large payoff and substantial analytical risk.**

A good short-horizon rate does not establish stability at longer maturities. Recursive products and tails can grow faster than tuning can compensate.

Proposed work: study short time slabs with controlled terminal approximation, or a coupled hierarchy of tree approximations. A multilevel construction would need an appropriate telescoping identity, bounds on level-difference variance, and level-cost estimates. Restarting would need stability estimates showing how local terminal errors propagate through the nonlinear evolution.

**Success:** reach a longer horizon at a declared overall error target, counting bias, sampling error and the cost of learning or interpolating intermediate terminal data.

**Risk and fallback:** plugging a noisy estimate into a nonlinear terminal expression can introduce bias; independent copies may be required for products. Killed-depth lower moments do not establish a convergent unbiased multilevel estimator. Nested schemes and pruned representations are prior art, with assumptions specific to their constructions. [S7][S7], [S8][S8]. Bouchard et al. combine local polynomial drivers and Picard iteration in a convergent branching BSDE scheme without a time-horizon restriction under their assumptions; this is a stronger reference for horizon extension than retuning λ alone. [Bouchard et al.][S13].

### 9. Develop honest uncertainty estimates for heavy-tailed tree outputs

**Priority: essential validation practice now; standalone method development later.**

Rare enormous tree weights can make empirical means and standard errors look stable before an important tail is observed. This matters both when choosing λ and when claiming an improvement.

Proposed work: separate the assumptions needed for estimating `E[H]`, estimating `E[H²]` and estimating expected runtime. Where finite variance is established, compare ordinary averages with a justified median-of-means procedure and examine interval coverage across independent batches. Maintain raw outputs, tail-contribution summaries and unfinished/failed-run counts.

**Success:** reliable uncertainty statements under explicitly stated moment conditions. A confidence procedure for `H²` may need a fourth moment of `H` or another valid envelope; an upper bound on `E[H²]` alone does not establish that requirement.

**Risk and fallback:** robust aggregation does not manufacture a missing expectation, and it need not be exactly unbiased at finite sample size. Do not silently clip rare samples. The specified Dym real-extension estimator remains a negative example with divergent absolute mean at every positive λ. [Dym result](estimator-integrity/dym-nonintegrability.md). Robust mean estimation is established statistical methodology. [S9][S9].

### 10. Transfer validated tuning to high dimensions and deep branching

**Priority: later validation and application track.**

The project already has multidimensional sampling and a deep branching solver. A reliable sampler could reduce the cost or noise of training targets across many states, where tuning overhead is more readily amortized.

Proposed work: extend the validated policy through a serializable interface, then compare training labels and final PDE predictions under default, rate-only and combined tuning. Keep network architecture and training effort fixed during the sampler ablation. Progress through small dimension before high-dimensional examples, and measure terminal-derivative and mechanism-table costs explicitly.

**Success:** lower held-out solution error or lower total time at a fixed error target, including policy construction, label generation and neural optimization. Neural regression adds approximation and optimization errors, so better tree variance alone is insufficient. The current deterministic rate evaluator is 1D and custom tuple proposals are serial-only; those are concrete dependencies.

**Risk and fallback:** high-dimensional deterministic moment quadrature can become more expensive than sampling. Use compact, validated approximations before attempting a large learned policy. Compare with deep branching's existing framework, MLP on compatible semilinear cases and, only if Hessian-dependent benchmarks enter scope, D2SRM. [S2][S2], [S10][S10], [S11][S11].

## Recommended sequence and decision criteria

Directions 1 and 2 should define the main milestone. Direction 9 supplies the evaluation discipline. Direction 3 is the first optional algorithmic extension. Direction 6 warrants an early compatibility review so that the project does not optimize an unsuitable representation by default. The remaining directions are alternatives for later work, not ten projects to undertake simultaneously.

This ordering is a research judgment based on current gaps, implementation readiness and the closeness of prior art. It is not a prediction that a certificate or speedup will be achieved. The primary reason to prioritize certification is that the project already has encouraging output and abstract theory, but cannot yet connect the approximate objective to a quantitatively reliable full-tree choice.

The proposed working title is **“Reliable and cost-effective sampling selection for recursive coding-tree PDE solvers.”** The narrow initial scope is one semilinear family, one explicitly fixed mechanism and scalar exponential rates. State-dependent hazards, high-dimensional applications and new financial models should not be prerequisites for completing that contribution.

## Proposed eight-week research plan

The schedule assumes one primary researcher using the existing codebase. It is an indicative sequence rather than a promised duration. All listed research and experiments are future work.

### Week 1: Lock the estimator, claims and evaluation protocol

- Record the exact mechanism, root codes, terminal functions, horizon and tuple law behind every reused result. Reconcile standard-binary control labels with the mechanism actually passed to the optimizer.
- Build a short claim-by-claim comparison with the primary references, especially the revised mechanism. Separate representation theorems, absolute moments, second moments, truncation bounds and numerical certificates.
- Define the initial rate interval and what would justify enlarging it. Specify a target excess-variance tolerance and whether the first claim is interval or global optimality.
- Freeze the later benchmark protocol: baselines, evaluation points, replicate count, metrics, cost accounting and failure reporting.

**Deliverable:** a two- to three-page mathematical specification and a predeclared experiment protocol. **Gate:** every proposed oracle must match its estimator; every theorem must have its applicable assumptions listed.

### Weeks 2–3: Develop sharper mechanism-specific bounds

- Start with constant-terminal Allen–Cahn, which removes spatial quadrature while retaining the coded mechanism.
- Retain separate normalized code classes and exact derivative zeros in a candidate vector majorant; then attempt the traveling wave.
- Seek a finite full-tree second-moment upper bound and a quantitative omitted-depth bound over the selected rate interval. Verify PDE identification separately.
- Diagnose whether conservatism comes from terminal bounds, offspring products, spatial envelopes or proposal floors.

**Deliverable:** a proof or a precise obstruction for the chosen benchmark class. **Gate:** obtain a useful finite bound at a stated horizon. If `T=0.05` is out of reach, explicitly narrow the horizon or class; do not replace the missing bound with empirical variance.

### Week 4: Make the numerical optimization error explicit

- Design validated integration or enclosure methods for the finite-depth recursion. Include Gaussian tails if spatial truncation is used.
- Allocate the permitted error among omitted depth, integration and optimization. Distinguish numerical integration error from insufficient tree depth.
- Return the selected rate together with an objective-gap bound, the certified interval and an explicit inconclusive outcome when tolerances cannot be met.
- Validate the components on the appropriate exact control and on constant-terminal cases before the wave.

**Deliverable:** a numerically verified rate-selection result or an explicit report identifying the unresolved error term. **Gate:** certificate resolution must be meaningful on the variance scale; a small relative error in a mean-dominated second moment can still be useless for detecting variance gains.

### Week 5: Establish the practical rate-only result

- Compare cheap fixed rates, the short-time heuristic and the selected rate using independent evaluation randomness.
- Run matched-sample and matched-total-budget comparisons over the profile. Include cold setup and amortized workloads.
- Report replicated solution RMSE, empirical variance, interval coverage where justified, tuning time, sampling time and tree-cost tails.
- Estimate a break-even workload and test whether conclusions are stable under numerical depth/order refinements.

**Deliverable:** an accuracy-versus-total-cost result with uncertainty and clearly identified failure cases. **Gate:** do not claim practical acceleration unless the total-budget comparison supports it. A useful certificate without a speedup is a different, narrower contribution.

### Week 6: Test whether continuation-aware q adds value

- Begin with a small frozen code/time proposal table and a positive support floor.
- At a common λ, compare it with uniform tuples and the terminal proxy; then reoptimize λ while holding each candidate proposal fixed.
- Include proposal training, storage and evaluation costs. Recheck moment bounds under the new probabilities.

**Deliverable:** a clean ablation of q's incremental effect. **Gate:** if the benefit cannot be distinguished from evaluation uncertainty or overhead, retain rate-only tuning as the principal method and document the limitation.

### Week 7: One conditional extension

Select **one** extension based on the earlier evidence: a representation comparison if tree structure dominates; a grid-weighted/root-dependent rate if spatial variation dominates; or a larger amortized sampling workload if tuning cost dominates. A deep-training extension is appropriate only after the sampler interface and scalar claims are stable.

**Deliverable:** one externally informative test of the core finding. This week may instead be used to resolve a failed earlier gate. No high-dimensional claim is required for the initial milestone.

### Week 8: Consolidate the research result

- Write the final claims around the completed evidence and the closest prior work.
- Separate proved guarantees, certified numerical results, empirical performance and unresolved conjectures.
- Package the benchmark specification, raw records, policy settings, seed provenance and cost accounting for reproduction.
- State what the method cannot certify and when a simpler sampler is preferable.

**Deliverable:** an FYP-ready chapter or paper-style report, one reproducible comparison workflow and a concrete continuation decision.

## Proposed benchmark protocol

The benchmark ladder should be intentionally small.

1. **Exact standard-binary control:** validate that estimator's analytic moment and rate calculations. Do not use the derivative-coded moment as a substitute.
2. **Constant-terminal Allen–Cahn:** isolate the actual coded recursion from spatial integration.
3. **Existing 1D traveling wave:** use the current `T=0.05` and grid as an anchor; add neighboring horizons only after specifying their analytical status.
4. **One bounded semilinear extension:** vary horizon, dimension or nonlinearity to test transfer after the anchor result works.
5. **Dym:** retain as a negative integrability diagnostic, outside averaged variance-reduction success metrics.

For the main ablation, compare λ=1/uniform q, the JCP rate/uniform q, the short-time heuristic/uniform q, selected λ/uniform q, λ=1/proxy q, and selected λ/proxy q. Add a continuation proposal only in its dedicated stage. The JCP rule is `−log(0.95)/T`; the short-time ratio is only used where its prerequisites hold. If a method needs a fallback, specify it before evaluation.

A feasible initial protocol is 20 independent end-to-end replications per anchor configuration, with production sample budgets calibrated separately from the evaluation streams. Twenty is a starting design, not a guarantee of statistical power: if uncertainty is too large, follow a predeclared expansion rule or report the result as inconclusive. Add horizons and methods sequentially rather than multiplying every option into a large initial grid. If tuning is random, each end-to-end replication includes fresh tuning and evaluation stages.

The primary performance metric should be replicated squared solution error averaged over the stated grid, with RMSE reported for readability. Include absolute errors near solution zeros; relative errors can be misleading there. Show the distribution of errors across independent replications, the proportion of failed or incomplete runs and the total cost. Use inferential methods only under their justified assumptions; repeated runs do not certify unseen tails.

Secondary diagnostics are per-point empirical variance, maximum observed weight, tail contributions, mean and extreme node counts, tuning/runtime breakdown and sensitivity to depth and quadrature order. Report these as diagnostics rather than population bounds. An analytic or certified reference should have smaller known error than the differences being assessed.

## Contribution boundary and fallback outcomes

A strong outcome would combine a useful full-tree certificate for an explicitly specified estimator with a reproducible performance benefit over inexpensive rate heuristics. A sharper certificate without speedup could still form a meaningful theoretical contribution. A careful empirical improvement without a certificate should be described as a heuristic algorithmic result. A proved obstruction or a demonstrated representation tradeoff could justify changing direction.

The following would not, by themselves, substantiate the proposed main contribution: another rate sweep; a local square-root derivation; a general adaptive-importance-sampling claim; optimizer convergence on the same uncertified quadrature objective; or a visually accurate profile from a nonintegrable estimator. Publication novelty requires a claim-level comparison, not the absence of a matching title in search results.

## Literature coverage and sources

The literature coverage includes original coding-tree representation and deep branching, weighted-progeny stability, adaptive importance sampling and intensity selection, lifetime laws and nesting, pruned representations, robust mean estimation, and competing high-dimensional PDE solvers. Recent searches included 2025–2026 material and version checks. Primary papers, author manuscripts and author publication pages were preferred; broader search hits served only as leads.

The evidence was reviewed on 14 September 2026. This is a targeted literature sweep for a research decision, not a systematic review with exhaustive database coverage. No exact counterpart to the complete proposed certified rate-selection procedure was identified among the inspected sources; that does not establish originality. Search-index dates were not treated as publication dates.

1. Jiang Yu Nguwi, Guillaume Penent and Nicolas Privault. **A fully nonlinear Feynman–Kac formula with derivatives of arbitrary orders.** *Journal of Evolution Equations* 23, article 22 (2023). [Paper][S1]; [published version](https://doi.org/10.1007/s00028-023-00873-3). Foundational representation, not a rate-tuning result.
2. Jiang Yu Nguwi, Guillaume Penent and Nicolas Privault. **A deep branching solver for fully nonlinear partial differential equations.** *Journal of Computational Physics* 499, 112712 (2024). [Paper][S2]; [published version](https://doi.org/10.1016/j.jcp.2023.112712). Source for the existing neural branching framework.
3. Qiao Huang and Nicolas Privault. **Stability analysis of a branching diffusion solver for semilinear heat equations.** arXiv:2502.17853v2, revised 9 March 2026. [Paper][S3]. The earlier version has a different title; the revised mechanism and hypotheses are the relevant comparison.
4. Ernest K. Ryu and Stephen P. Boyd. **Adaptive Importance Sampling via Stochastic Convex Programming.** Working paper, originally posted November 2014. [Author page and manuscript][S4]. Prior art for convex adaptive importance sampling.
5. Laetitia Badouraly Kassim, Jérôme Lelong and Imane Loumrhari. **Importance sampling for jump processes and applications to finance.** arXiv:1307.2218, 8 July 2013. [Paper][S5]. Intensity optimization using sample-average approximation.
6. Pierre Henry-Labordère, Nadia Oudjane, Xiaolu Tan, Nizar Touzi and Xavier Warin. **Branching diffusion representation of semilinear PDEs and Monte Carlo approximation.** *Annales de l’Institut Henri Poincaré, Probabilités et Statistiques* 55(1), 184–210 (2019); preprint 2016. [Paper][S6]; [published version](https://doi.org/10.1214/17-AIHP880). Moment majorants, lifetime distributions and cost.
7. Xavier Warin. **Variations on branching methods for non linear PDEs.** arXiv:1701.07660, initially 26 January 2017. [Paper][S7]. Modified differentiation, nested methods and variance reduction.
8. Dirk Blömker, Marco Romito and Roger Tribe. **A probabilistic representation for the solutions to some non-linear PDEs using pruned branching trees.** *Annales de l’Institut Henri Poincaré* 43 (2007), 175–192; preprint 2005. [Paper][S8]. Pruning and comparison equations in different representations.
9. Gábor Lugosi and Shahar Mendelson. **Mean estimation and regression under heavy-tailed distributions—a survey.** 2019. [Full paper][S9]. Statistical assumptions and robust estimators; no coding-tree integrability theorem.
10. Ariel Neufeld, Tuan Anh Nguyen and Sizhou Wu. **Multilevel Picard approximations overcome the curse of dimensionality in the numerical approximation of general semilinear PDEs with gradient-dependent nonlinearities.** *Journal of Complexity* 90, 101946 (2025). [Paper][S10]; [published version](https://doi.org/10.1016/j.jco.2025.101946). Comparator subject to its Lipschitz, growth and diffusion assumptions.
11. Zhenhua Zhao and Jihao Long. **A Deep Second-Order Stochastic Residual Method for Fully Nonlinear Parabolic PDEs.** arXiv:2607.16730, 18 July 2026, preprint. [Paper][S11]. Optional recent Hessian-dependent comparator; not evidence of dominance on the present benchmarks.
12. Emmanuel Gobet and Plamen Turkedjiev. **Adaptive importance sampling in least-squares Monte Carlo algorithms for backward stochastic differential equations.** *Stochastic Processes and their Applications* 127(4), 1171–1203 (2017). [Author manuscript][S12]; [published version](https://doi.org/10.1016/j.spa.2016.07.011). Adaptive conditional sampling, stability and concentration in a different solver framework.
13. Bruno Bouchard, Xiaolu Tan, Xavier Warin and Yiyi Zou. **Numerical approximation of BSDEs using local polynomial drivers and branching processes.** arXiv:1612.06790, submitted 20 December 2016, revised 28 July 2017. [Paper][S13]. Local polynomial approximation and Picard iteration for horizon extension.
14. Jérémi Dauchet et al. **Addressing nonlinearities in Monte Carlo.** *Scientific Reports* 8, 13302, 5 September 2018. [Paper][S14]. Explicit variance and computational-cost tradeoffs in nonlinear Monte Carlo.

[S1]: https://arxiv.org/html/2201.03882v3
[S2]: https://arxiv.org/abs/2203.03234
[S3]: https://arxiv.org/html/2502.17853v2
[S4]: https://stanford.edu/~boyd/papers/adaMC.html
[S5]: https://arxiv.org/abs/1307.2218
[S6]: https://arxiv.org/abs/1603.01727
[S7]: https://arxiv.org/abs/1701.07660
[S8]: https://arxiv.org/abs/math/0505449
[S9]: https://arxiv.org/html/1906.04280v1
[S10]: https://arxiv.org/abs/2311.11579
[S11]: https://arxiv.org/abs/2607.16730
[S12]: https://kclpure.kcl.ac.uk/ws/files/56329695/1_s2.0_S0304414916301235_main.pdf
[S13]: https://arxiv.org/abs/1612.06790
[S14]: https://www.nature.com/articles/s41598-018-31574-4
