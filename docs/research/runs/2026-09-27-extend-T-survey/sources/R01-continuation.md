# R01 — Continuation, local polynomial branching, and nested interfaces

Research date/cutoff: **27 September 2026**. Ideation only: no solver, experiment, or Lean changes were made. The initial working tree was already dirty; its files were preserved. This note is the only file written by R01. Sources below were opened and their stated assumptions inspected. Search coverage is bounded, not a claim of worldwide novelty. Requested role/model: research / `gpt-6-astra`, max; independent serving-model verification is unavailable.

## Main finding

**Longer-T branching is already possible through continuation in important semilinear classes.** A project contribution should address a missing guarantee or a measurable capability beyond those results, rather than present slab splitting as new. The strongest MC-side candidate in this cluster is **independent estimation of terminal codes at interfaces, with a composable second-moment certificate**. A complementary, practically cheaper route is **controlled approximation of the entire code family at each interface**. Generic fully nonlinear coding trees make this harder than controlling a fixed finite jet.

The four candidates below are research proposals, not established project results. R01-C is a scheduling refinement of continuation; merge it into R01-B if the overall ten-direction list has stronger independent alternatives. R01-A is a valuable known-method baseline, with limited novelty by itself.

## Primary-source evidence

### S1 — Local polynomial / projected Picard continuation is established

Bouchard, Tan, Warin, Zou, *Numerical approximation of BSDEs using local polynomial drivers and branching processes*, arXiv:1612.06790, 2017 journal version. [Author PDF](https://www.ceremade.dauphine.fr/~bouchard/pdf/BTWZ17.pdf), [arXiv record](https://arxiv.org/abs/1612.06790).

**Read:** §§2.1–2.4, Theorem 2.4, Proposition 2.5, Assumption 2.6, Proposition 2.8, Remarks 2.9–2.10, Appendix Lemma A.1.

The setup is a BSDE driver `f(x,y)` without gradient dependence: bounded terminal data; driver Lipschitz in `y` with linear growth; Lipschitz diffusion coefficients localized to compact support. A known bound `M` controls the solution. The diagonal local-polynomial driver must be globally Lipschitz, and its solution also bounded by `M`. Intervals satisfy `h<h₀`, with `h₀` a polynomial explosion-time lower bound. Grid-point projection into `[-M,M]` and Picard iteration yield Theorem 2.4 for any finite global `T`; Proposition 2.5 establishes integrable local tree representations. Proposition 2.8 propagates approximation-operator errors under Assumption 2.6. Its constants depend strongly on slab and iteration counts. Remark 2.10 separates fixed admissible slabs from the accuracy of interface/interior functional approximation. This is convergence of an approximation scheme, not an unbiased finite-cost estimator of the original BSDE for arbitrary `T`.

### S2 — Gradient control requires modifying the function coherently

Bouchard, Tan, Warin, *Numerical approximation of general Lipschitz BSDEs with branching processes*, arXiv:1710.10933; ESAIM Proceedings and Surveys 65 (2019), 309–329. [Full primary HTML](https://arxiv.org/html/1710.10933), [journal DOI](https://doi.org/10.1051/proc/201965309).

**Read:** §2 hypotheses, §2.2, Theorem 2.1, Proposition 3.1, Remark 3.1, Appendix A.1–A.2.

Here `f,g` are bounded and Lipschitz, `σσᵀ≥a₀²I`, and `μ,σ,Dμ,Dσ` are bounded continuous. A priori value and gradient bounds underpin function-level face-lifting plus value truncation. Theorem 2.1 gives geometric Picard convergence for arbitrary finite `T`, with an integral-in-time gradient error. Proposition 3.1 supplies uniform local `L²` bounds for value/gradient branching estimators when `h<min(h₀,h₀′)`, using the explicit lifetime density `ρ(t)=t^(-2/3)/3` on `(0,1)` and coefficient-based offspring probabilities. The paper explains why clipping a gradient at isolated times is insufficient. Its scope is semilinear `f(x,u,Duσ)`; it does not establish an analogous projection or continuation theorem for nonlinear Hessians or arbitrary spatial derivative codes. Its theoretical lifetime law also differs from the project's common exponential clock.

### S3 — The NPP deep branching paper supplies local representation and regression

Nguwi, Penent, Privault, *A deep branching solver for fully nonlinear partial differential equations*, JCP 499 (2024), 112695; arXiv:2203.03234. [Full primary HTML](https://arxiv.org/html/2203.03234).

**Read:** Definition 2.1, mechanism in §2, Algorithm 1, equation (2.2), §3 equation (3.1).

The terminal object is **`c(u)(T,x)` for each code**, which may be a derivative of the terminal function or a nonlinear function of its derivatives. The code set includes arbitrary multi-indices. Equation (2.2) requires the underlying integrability/smoothness conditions; the population least-squares identity (3.1) requires square-integrable labels. Neither identity makes a fitted function's derivatives accurate merely because its value loss is small. No slab-interface error theorem was located in the inspected sections. The article links the original `deep_branching` repository, while the successor code inspected below implements patching. These are separate pieces of evidence.

### S4 — Successor code already implements equal-width neural patches

[Author successor repository](https://github.com/nguwijy/deep_branching_with_domain). Local read-only checkout: `/Users/michael/Desktop/NTU/fyp/deep_branching_with_domain`, commit **`2ccfd1d5ca4aa11273ed206db67de23ba1d70c93`**.

- [`branch.py:568`](https://github.com/nguwijy/deep_branching_with_domain/blob/2ccfd1d5ca4aa11273ed206db67de23ba1d70c93/branch/branch.py#L568) explains backward patching; line 678 sets equal widths `(T-t_lo)/branch_patches`.
- [`adjusted_phi`, line 1034](https://github.com/nguwijy/deep_branching_with_domain/blob/2ccfd1d5ca4aa11273ed206db67de23ba1d70c93/branch/branch.py#L1034) uses the true terminal function on patch zero and the previous network on later patches.
- [`code_to_function`, line 1080](https://github.com/nguwijy/deep_branching_with_domain/blob/2ccfd1d5ca4aa11273ed206db67de23ba1d70c93/branch/branch.py#L1080) differentiates that function and evaluates nonlinear codes on its derivatives.
- [`gen_sample`, line 1953](https://github.com/nguwijy/deep_branching_with_domain/blob/2ccfd1d5ca4aa11273ed206db67de23ba1d70c93/branch/branch.py#L1953) additionally filters samples using empirical quantiles before averaging (lines 2007–2018). A direct reproduction therefore needs its filtering bias disclosed.

This source demonstrates implementation precedent, not validated continuation error or unbiasedness. It was inspected, not executed. New NN work remains outside this checkout's responsibility.

### S5 — Branchwise nesting has demonstrated horizon gains, but costs grow

Warin, *Variations on branching methods for non linear PDEs*, arXiv:1701.07660. [Primary HTML](https://arxiv.org/html/1701.07660), [author PDF](https://www.fime-lab.org/wp-content/uploads/2016/07/VariationsOnBranching-1.pdf).

**Read:** §§2.1.3, 2.2.3, 3.5.

Section 2.1.3 averages multiple independent estimates for each `u` or `Du` factor at a branching event. Experiments extend successful maturities, including a case where the original estimator performs poorly at `T=2.5`. Re-sampling more heavily near the root was tried but abandoned as too case-dependent. Sections 2.2.2–2.2.3 combine nesting with ghost/antithetic representations; §2.2.3 reports substantial practical gains, but warns about exploding memory or work at large maturities. Section 3.5 reports that nesting did not improve its fully nonlinear examples much. These are numerical observations, not a universal arbitrary-T theorem. The HTML displays a recent document date despite labeling the arXiv source v1 from January 2017; this note treats it as the 2017 work, not a newly established 2026 result.

### S6 — Finite-depth nested nonlinear evaluation has a bias/error theory

Warin, *Nesting Monte Carlo for high-dimensional Non Linear PDEs*, arXiv:1804.08432; MCMA 24(4) (2018), 225–247. [Primary PDF](https://arxiv.org/pdf/1804.08432).

**Read:** Assumptions 2.1–2.2 and Proposition 2.3; Assumptions 3.1–3.3 and Proposition 3.5.

Proposition 2.3 treats globally Lipschitz dependence on `u`, a classical `C^(1,2)` solution, uniform temporal Hölder regularity, and at-most-quadratic spatial growth. Its mean-square bound separates the finite nesting-depth contribution from Monte Carlo contributions. Proposition 3.5 treats gradient dependence with additional regularity and Lipschitz terminal data, using a Gamma lifetime shape below one. Its truncation at a finite nesting depth is explicit and biased; convergence means controlling depth and all relevant sample counts. These results are useful comparator/error-analysis templates, rather than a proof for the untruncated NPP estimator with arbitrary derivative codes.

### S7 — Fully nonlinear nesting claims need careful scope

Warin, *Monte Carlo for high-dimensional degenerated Semi Linear and Full Non Linear PDEs*, arXiv:1805.05078. [Primary PDF](https://arxiv.org/pdf/1805.05078).

**Read:** §4, Propositions 4.2/4.4, Assumptions A2/A3, opening of §6, §7.

Proposition 4.4 concerns a degenerate **semilinear** equation rewritten using an artificial nondegenerate diffusion and a compensating term linear in the Hessian. It assumes Lipschitz dependence on value/gradient and `C^(1,2p)` solutions with bounded derivatives and temporal Hölder regularity of the `2p`th derivative. The error contains a depth term plus sampling terms. Section 6 explicitly distinguishes its general nonlinear-Hessian numerical examples from the proved linear-Hessian case. Therefore this paper cannot be cited as a proven arbitrary-derivative, arbitrary-T extension of NPP trees.

### S8 — Generic nonlinear plug-in nesting is not automatically unbiased

Rainforth et al., *On Nesting Monte Carlo Estimators*, arXiv:1709.06181; ICML 2018. [Primary full text](https://arxiv.org/html/1709.06181).

**Read:** Theorems 1 and 3; Appendix B, Theorems 6–7.

Theorem 1 gives a mean-square rate `O(1/N+1/M)` for one level of nesting under Lipschitz and square-integrability assumptions. Theorem 3 shows deterioration with repeated nesting. Appendix B proves that imperfect inner estimates can cause bias under nonlinear outer evaluation; strict convexity/concavity gives a direct Jensen argument. This supports a specific distinction below: directly estimating each terminal code and multiplying conditionally independent factors differs from evaluating a nonlinear code on a noisy estimated jet. The latter generally retains bias even when outer sample count tends to infinity with fixed inner count.

## R01-A — Projected local-polynomial continuation as a reliable semilinear baseline

**Mechanism for larger T.** Replace a single long tree by short solves, with bounded interface functions and local polynomial/Picard updates. The baseline could first target Allen–Cahn on an invariant interval, using a globally Lipschitz extension that agrees with the original reaction throughout the proved solution range. Short-slab guarantees then apply repeatedly even after the original raw estimator's global moment window has ended.

**Prior art and applicability.** S1 Theorem 2.4/Propositions 2.5–2.8 already provide the basic result; S2 covers first derivatives. This is semilinear work. A nonlinear-Hessian or arbitrary-derivative claim would require new arguments.

**Bias status.** Invariant-region-preserving extension can avoid changing the exact target within that region. Finite polynomial approximation, finite Picard iteration, interface interpolation, finite-sample projection, and any fitted representation each need their own error term. The final finite computation is generally biased, although an individual local tree can be unbiased for its specified local problem before projection.

**Missing project guarantee / plausible contribution.** Make the continuation error computable in the existing estimator framework, including nonconstant interface data, local tree moment bounds, and the approximation error from the selected function representation. The contribution is a certified capability in this project, not a new invention of global semilinear continuation. Finite-basis implementation should be a transparent low-dimensional reference; NN implementation belongs in the sibling checkout.

**First falsifiable two-slab test, after theory.** Propose flat Allen–Cahn `phi=1/2`, total `T=0.8`, split at `0.4`. Before sampling, certify each slab with its *actual* terminal bound, including the enlarged intermediate value. Compare against `u(0)=(1+3 exp(-2T))^(-1/2)`. Require error to follow the derived interface/Picard/sampling bound as budgets increase. `T=0.8` is deliberately beyond the recorded raw-uniform scalar L² maximum (~0.704); this does not cross the raw all-proposal L¹ ceiling. The subsequent useful target is `T≥1.6`, then `T=2`, using as many certified slabs as necessary. Reject an apparent extension based on unaccounted projection/filtering bias.

**Risk / feasibility.** High feasibility for a 1D scalar baseline; moderate for gradient-dependent equations. The interface approximation can bring back dimension-dependent cost, and stability constants can grow rapidly with T. Novelty alone is low; use this as the comparator every more ambitious continuation proposal must beat or generalize.

## R01-B — Continuation controlled in code observables, not just values

**Mechanism for larger T.** Keep the NPP local tree but require each interface approximation to carry certified bounds for every terminal observable needed by the next slab. Use those bounds to choose an admissible next width and to propagate approximation error. This could make the author's existing patching construction reviewable as an error-controlled method.

**Prior art and applicability.** S3 Definition 2.1 and S4 identify the required interface data; S2 supplies a first-derivative precedent for coherent function projection. A fixed finite jet is enough only if a finite reachable-code closure is proved for the selected problem. In generic gradient/fully nonlinear NPP systems, reachable derivative orders can grow indefinitely. Merely controlling derivatives up to the PDE's displayed order does not close the tree. Candidate contracts include a weighted analytic/Gevrey code norm, a structural finite closure, or an explicitly bounded approximation of a code hierarchy.

**Bias status.** Approximate interfaces produce controlled bias. Exact interfaces give exact semigroup composition under the local representation assumptions. Differentiating a fitted function does not by itself establish either derivative accuracy or unbiasedness.

**Missing guarantee / plausible contribution.** Prove a two-slab perturbation theorem of the form `error at t0 ≤ local MC error + L_slab × interface code error`, in a norm that the mechanism actually preserves; separately show that the perturbed terminal data keep the next tree in L². The difficult part is avoiding unbounded derivative loss. For higher-order problems, additional well-posedness/analytic-regularity assumptions must be stated; no universal all-PDE continuation claim is justified. The project-owned deliverable is the code-observable contract and its moment/stability certificate.

**First falsifiable two-slab test, after theory.** Start with the known Allen–Cahn traveling wave at a proposed total `T=0.8`, using an exact intermediate function and then a deterministic smooth approximation. Inject `epsilon cos(kx)` into the interface for several k while fixing the value error epsilon. Predict the next-slab error using the code norm before testing it. A bound depending only on value error should be deliberately challenged. Next apply the same protocol to a manufactured/known smooth Burgers case, where derivative closure is more demanding. Passing a smaller-T perturbation test alone is not evidence of long-horizon capability; require a later certified run beyond the same PDE's single-slab range.

**Risk / feasibility.** Medium for finite-code semilinear cases; low-to-medium for an analytic restricted family; low for arbitrary smooth fully nonlinear equations. A promising high-value guarantee, but not yet a theorem. If the analytic radius shrinks too quickly or terminal-code norms explode under approximation, stop before implementing a general solver.

## R01-C — Adaptive admissible slabs coupled to λ, q and interface accuracy

**Mechanism for larger T.** Make the accumulated horizon the output of a sequence of locally certified decisions. At each interface, use its code envelope to select the next slab length and local `lambda,q`, while assigning tighter approximation tolerances where error amplification is strongest. This addresses the practical issue that later interface data need not satisfy the original terminal envelope.

**Prior art and applicability.** S1 uses an admissible fixed grid and tracks accumulated approximation error; S2 supplies explicit local moment constraints; S4 uses equal widths. S5 already tried a different adaptive ingredient—varying resampling by generation—so that alone is not a fresh idea. No joint code-envelope/slab/proposal certificate was located in this bounded search. This absence is a search result, not a novelty proof. The idea depends on R01-A or R01-B for its interface theorem.

**Bias status.** A frozen schedule chosen from independent pilot data retains the base method's target/bias status. A schedule selected using the same production samples requires a separate conditional argument. A small empirical variance cannot certify finite moments or the safety of a chosen width.

**Missing guarantee / plausible contribution.** A verifiable controller that returns `(slab width, terminal envelope, local L² bound, propagated error bound)` and a proof of coverage up to the requested T under explicit regularity/invariant-region assumptions. Rate/proposal optimization then serves actual continuation rather than only a shorter-time variance improvement. A termination theorem should rule out infinitely many shrinking slabs before reaching T.

**First falsifiable two-slab test, after theory.** Fix total `T=0.8` and the same flat/nonconstant Allen–Cahn data as R01-A/B. Compare an equal split with candidate interfaces at `0.2,0.3,0.4,0.5,0.6`, using the actual interface bounds and including pilot costs. Require both local certificates and the same global error target. Failure means no admissible split, a predicted error bound violated, or an alleged improvement caused by incomparable terminal data. Only after this test should one target `T≥1.6` with an adaptive number of slabs.

**Risk / feasibility.** Medium once an interface contract exists; otherwise blocked on that contract. Global worst-case envelopes can be too conservative. The controller is closely related to R01-B, so avoid counting it as an independent breakthrough merely because it changes a scheduling parameter.

## R01-D — Independent terminal-code nesting with certified variance budgets

**Mechanism for larger T.** Stop an outer tree at an interface and, for each terminal code `c` at location x, launch fresh inner trees targeting `c(u)(s,x)`. Average `K_c` inner samples. Different factors of the outer product receive conditionally independent inner samples, including repeated occurrences of the same code. This can suppress continuation noise without fitting a global interface function. It changes the estimator by grouping conditional expectations; it is not another choice of λ for the same original long tree.

For an integrable, conditionally unbiased inner code estimator `Z_c`, the elementary identity to exploit is

`E[average(Z_c)^2 | x] = c(u)(s,x)^2 + Var(Z_c | x)/K_c`.

The proposal is to insert certified versions of those boundary moments into the project's nonnegative full-tree moment equations, then choose codewise `K_c` and slab widths that leave a finite outer moment margin. Establish random-tree integrability before using the tower property; a per-leaf finite variance statement alone is insufficient.

**Prior art and applicability.** Branch-factor averaging is already in S5 §2.1.3. S6 provides a different finite-depth nonlinear nesting error analysis; S7 limits what its fully nonlinear results prove. The project-specific opportunity is terminal **code** composition and a certificate for it, especially in the existing finite flat Allen–Cahn closure. Extension to arbitrary derivatives inherits R01-B's closure problem.

**Bias status.** Conditional independence plus exact inner code expectations can preserve unbiasedness at a deterministic interface if the composed tree is absolutely integrable. In contrast, `c(estimated u)` is generally biased for nonlinear c; S8 makes the generic obstruction explicit. For polynomial codes, independent replicas for every factor can estimate that code without nonlinear plug-in bias. For nonpolynomial codes, one needs a direct code estimator or a separately justified unbiased construction. Reusing one estimated interface field across multiplicative factors is not automatically valid.

**Missing guarantee / plausible contribution.** A recursive finite-L² composition theorem, explicit replication budgets, and a work bound proving a nonempty useful regime beyond the original uniform second-moment ceiling. The theorem must not assume access to an exact intermediate solution. Ideally establish a finite multislab estimator past the raw L¹ ceiling; the old ceiling concerns the original ungrouped representation and cannot simply be transferred to this new one.

**First falsifiable two-slab test, after theory.** For flat Allen–Cahn, propose `T=0.8`, equal slabs, and `K_c∈{1,2,4,8,16}`. First certify local moments of every required inner code and then the composite root; failure at `K_c=16` is evidence against that schedule, not proof no schedule exists. Compare against the exact ODE and an oracle-interface experiment used only as a diagnostic. Verify that increasing K changes variance as predicted while retaining the mean. Then extend to nonconstant data and `T≥1.6` using more slabs. Compare total root work and error to the already implemented bounded-majority solver at `T=2`; reimplementing that solver is unnecessary.

**Risk / feasibility.** Medium-to-high for two slabs in a proved finite-code closure; medium-to-low for many slabs. Expected inner work multiplies by the number of outer leaves and by each replication budget, potentially exponential in slab count. This could establish real longer-T unbiased capability yet remain less practical than controlled biased continuation. Do not promise a cost advantage before measuring all nested work.

## Suggested research ordering

1. Use R01-A as the established-method baseline; its novelty score should remain modest.
2. Investigate R01-D's two-slab finite-code theorem first if the priority is an unbiased MC method within this checkout. It fits the current moment machinery and has a clear failure criterion.
3. Investigate R01-B if controlled approximation is acceptable and a meaningful restricted derivative class can be chosen. R01-C becomes useful once that theorem exists.

The first proof obligations are **interface composition, full-tree moment control, and an explicit global error/cost target**. Subsequent work should follow the parent task's requested theory → Lean → code sequence; none of those phases was executed here.

## Search record and limitations

All searches below were issued on 2026-09-27; the review cutoff is that date. Exact phrases/queries included:

- `Bouchard Tan Warin Zou 1612.06790 numerical approximation BSDE local polynomial branching time discretization`
- `Nguwi Penent Privault deep branching domain time patching PDE`
- `"Warin" "branching" "nested" PDE`
- `"Nguwi" "time" "patching"`
- `"deep_branching_with_domain"`
- `"Nesting Monte Carlo for high-dimensional non-linear PDEs" Warin arxiv`
- `branching Monte Carlo time adaptive restart error estimates fully nonlinear PDE 2025 2026`
- `"branching" "time patching" PDE`
- `"Warin" "fully non" "Nesting"`
- `"branching" "continuation" "jet" PDE Monte Carlo`
- `"branching" "adaptive" "slabs" PDE`
- `site.arxiv.org "Warin" "full non-linear" nesting`
- `site.arxiv.org "branching" "patching" differential`
- `site.arxiv.org "branching" "continuation" "Monte Carlo" PDE`
- `"branching" "time horizon" "PDEs" 2025 2026 Privault`
- `"deep branching" "patch" PDE`
- `"branching Monte Carlo" "restart" PDE`
- `"branching" "a posteriori" PDE Monte Carlo`
- `site.nprivaul.github.io "branch" "patch"`
- `site.arxiv.org "branching" "adaptive" "nonlinear PDE"`
- `site.arxiv.org "branching" "time horizon" "2026" Privault`

Many literal `patch`/`branching` queries returned unrelated software or bifurcation work; those were discarded. Searches also surfaced a 2026 primary conference abstract by Huang/Privault on stability of branching semilinear heat solvers, forwarded to the parent for the integrability cluster: [AIMS 2026 abstract](https://aimsconference.org/AIMS-Conference/conf-reg2026/ss/detail1all.php?ssid=37). It was not treated as an established continuation theorem. The Navier–Stokes deep branching paper [arXiv:2212.13010](https://arxiv.org/pdf/2212.13010), Proposition 2.3 and §3, was checked as adjacent NPP work; it requires integrability of its code family and uniqueness of its integral system, rather than proving a general patching error result. Its extra pressure/Poisson machinery is outside this proposed first experiment.

Open bibliographic gap: a systematic forward-citation search for newer certified arbitrary-code interface results remains worthwhile before claiming novelty. No paywalled-only theorem or search abstract has been promoted into positive theorem evidence here.
