# Ten prior avenues, reassessed

This run resumes the existing plan rather than claiming ten fresh ideas. The original detailed cards and 14 September literature sweep remain in [future-directions-after-lambda.md](../../future-directions-after-lambda.md). These scores assess the next unresolved increment, not the value of already completed work.

The exact rubric is novelty × impact × effect, each in {1,10,100}; high value requires **strictly greater than 1000**. No avenue earns an exceptional 100 on current evidence. Consequently there is no confirmed high-value shortlist. D03 is continued as a bounded feasibility investigation under the resumed programme; it is not advertised as a demonstrated breakthrough.

## D01. Extend full-tree certificates beyond saved cases

Current exact witnesses are short-horizon and uniform-q. Codewise residual and nonuniform envelopes can cover more parameters.

Feasibility: feasible. Positive polynomial closure and exact boxes already exist. First rejection test: Check the nonuniform closure against raw labelled tuples.

Score: 10 × 10 × 10 = 1000. Joint certificate construction is a specific extension; no new generic comparison principle. Baseline: Current raw-uniform short-horizon certificates. Target: A useful bound for a genuinely changed supported tuple policy; a research target, not an observed speedup.

Evidence: searched. [Primary source 1](https://arxiv.org/html/2502.17853v2)

## D02. Optimize total computation cost

Variance improvement does not determine cost at fixed error. Cost-aware selection can beat a variance-only policy after setup.

Feasibility: conditional. A stable cost model and new useful policy are needed. First rejection test: Measure setup and complete-batch sampling separately.

Score: 1 × 10 × 1 = 10. Cost/variance tradeoffs are established. Baseline: Two completed cost studies. Target: Lower total cost at matched error, magnitude unknown; a research target, not an observed speedup.

Evidence: provisional. [Primary source 1](https://arxiv.org/abs/1603.01727)

## D03. Certify continuation-aware tuple improvements

Proxy scores lack a full-tree no-worsening guarantee. Signed interval gates on old continuation moments yield unrestricted-tree improvement.

Feasibility: feasible. The order comparison and exact binary control have a bounded proof/verification path. First rejection test: Attempt a counterexample to the gate; verify supported nonuniform flat controls.

Score: 10 × 10 × 10 = 1000. The derivative-coded interval gate and recursive bridge are a scoped extension; classical optimal importance sampling is prior art. Baseline: Terminal proxy and raw uniform q. Target: Replace heuristic acceptance with a useful sufficient variance-dominance certificate; a research target, not an observed speedup.

Evidence: searched. [Primary source 1](https://stanford.edu/~boyd/papers/pdf/adaMC.pdf) [Primary source 2](https://web.stanford.edu/~glynn/papers/2013/AwadGRubinstein13.pdf)

## D04. Rates varying by code or time within a tree

One shared scalar rate cannot adapt to local continuation needs. A supported local-rate policy can reduce moments in heterogeneous code regimes.

Feasibility: conditional. Sampler and nonexplosion/moment proof need a new clock contract. First rejection test: Solve a two-code exact control before modifying the production sampler.

Score: 10 × 10 × 10 = 1000. Specific coded extension possible; general adaptive intensity sampling is known. Baseline: One common rate. Target: Material reduction from within-tree rate allocation, unmeasured; a research target, not an observed speedup.

Evidence: provisional. [Primary source 1](https://arxiv.org/abs/1307.2218)

## D05. Alternative lifetime distributions

Exponential clocks may poorly match branch-time contributions. A bounded clock family can improve the measured moment at a fixed representation.

Feasibility: conditional. Density/survival likelihood and integrability comparison need rederivation. First rejection test: Compare a non-exponential exact control with its matching oracle.

Score: 1 × 10 × 1 = 10. Other lifetime distributions are already standard branching literature. Baseline: Exponential clock. Target: Magnitude unknown; require improvement at equal estimator target; a research target, not an observed speedup.

Evidence: provisional. [Primary source 1](https://arxiv.org/abs/1603.01727)

## D06. Change tree representation

Raw derivatives can create expensive or high-weight alternatives. Normalized or reduced mechanisms can enlarge the finite-moment regime.

Feasibility: conditional. New representation must be distinguished from changing sampling of the old one. First rejection test: Compare one polynomial PDE using matched explicit moment systems.

Score: 10 × 10 × 10 = 1000. Recent normalized-code stability work is close; difference needs a fresh detailed comparison. Baseline: Raw semilinear coding tree. Target: A materially larger certifiable horizon; a research target, not an observed speedup.

Evidence: provisional. [Primary source 1](https://arxiv.org/html/2502.17853v2)

## D07. Conditional expectation or control variates

Random choices with computable conditionals add avoidable variance. Integrating selected branch randomness can lower variance with explicit weights.

Feasibility: conditional. An economical conditional expectation and matched implementation are needed. First rejection test: One-step exact control with unbiased conditional replacement.

Score: 1 × 10 × 10 = 100. Rao–Blackwellization and branching variance reduction are established. Baseline: Current raw tree draw. Target: Material variance decrease, total cost unresolved; a research target, not an observed speedup.

Evidence: provisional. [Primary source 1](https://arxiv.org/abs/1701.07660)

## D08. Extend horizon with controlled restarting

Current certificates do not establish a broad useful time window. Certified local solves and controlled restart can extend usable horizons.

Feasibility: conditional. Boundary-value approximation errors must propagate with controlled bias. First rejection test: Two-slab exact control with explicitly tracked interface error.

Score: 10 × 10 × 10 = 1000. Local polynomial/Picard branching extensions already exist. Baseline: Single-horizon branching estimator. Target: Material longer horizon with a rigorous error budget; a research target, not an observed speedup.

Evidence: provisional. [Primary source 1](https://arxiv.org/abs/1612.06790)

## D09. Honest uncertainty under heavy tails

Empirical standard errors can miss rare weights. Moment certificates plus robust estimation can yield honest finite-sample bounds.

Feasibility: feasible. Existing finite second-moment bounds support standard robust-mean constructions. First rejection test: Check confidence radius against a certified heavy-tail control.

Score: 1 × 10 × 10 = 100. Robust mean bounds are well-established; coding-tree packaging alone is modest. Baseline: Uncertified empirical standard error. Target: A useful coverage guarantee rather than merely narrower bars; a research target, not an observed speedup.

Evidence: provisional. [Primary source 1](https://arxiv.org/html/1906.04280v1)

## D10. Transfer tuned trees into high-dimensional deep training

Short-horizon 1D guarantees have not transferred to training labels. Certified or safer labels can improve deep-branching accuracy under matched budgets.

Feasibility: conditional. Dimensional moment bounds and training-error separation are missing. First rejection test: Small fixed network with independent tuning/evaluation labels.

Score: 10 × 10 × 1 = 100. Potential specific combination, but no broad novelty claim is justified. Baseline: Existing reproduced deep-branching baseline. Target: Effect is presently unknown; a research target, not an observed speedup.

Evidence: provisional. [Primary source 1](https://arxiv.org/abs/2203.03234)

## New bounded literature check — 16 September 2026

Queries included “Ryu Boyd adaptive importance sampling convex optimization exponential family variance”, “branching diffusion optimal offspring probabilities second moment importance sampling policy improvement”, and searches for Huang–Privault stability, Lyapunov importance-sampling inequalities and adaptive Markov-chain samplers. Read the primary Ryu–Boyd theorem and Huang–Privault v2; independent review examined intensity optimization and Lyapunov importance-sampling precedents. Full links and overlap/difference analysis are in [09-independent-review.md](09-independent-review.md).

Convex importance sampling, greedy square-root proposals and Lyapunov/supersolution methods have close prior art. The specific contribution examined here is a support-preserving interval acceptance gate linked to unrestricted derivative-coded-tree moment comparison, plus concrete nonuniform rational witnesses. No worldwide novelty claim is made. Other avenues retain provisional literature status: their earlier references were read in the project plan, but this run did not repeat an exhaustive ten-topic search.


## Post-result reassessment

The initial scores remain unchanged in `ideas.json` and `scores.json`. C8 subsequently established a concrete infinite-to-finite variance transition in the flat control, and an exact sqrt(1.9) increase in the best horizon threshold after clock reoptimization. The revised D03 effect score is therefore 100: a capability change against an explicit baseline, not an inferred speedup. Novelty remains 10 (specific scoped extension, substantial classical precedent), and impact 10 refers to the general recursive policy-safety framework. Revised value: **10 × 10 × 100 = 10000**.

`ideas-after-results.json` retains all ten avenues; `scores-after-results.json` records the recalculated shortlist. The score supports further investigation of D03. It is not a publication-novelty certificate, a claim that the flat sampler is new, or evidence of a similar effect on nonconstant PDE data. The existing terminal proxy already realizes the flat candidate at floor_mass=.1; the new result is its proved full-tree threshold and certified effect.
