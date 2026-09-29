# R02 — Representation changes that can extend usable time horizons

Research date: 2026-09-27. Scope: primary-source survey and proposed first checks only. No solver, experiment, numerical proof, or Lean work was performed. This subtask owns only this file. Research role requested by the task: `gpt-6-astra` / `max`, following the math-auto-research configuration; the parent dispatch ledger records the actual selection.

The strongest project-facing family is **estimate a correction around a known reference, while retaining any known linear damping in the propagator**. Bounded voting is a second, already-established route for scalar reactions on invariant intervals. Ghost/antithetic constructions address derivative singularities and offer a more conditional route toward the fully nonlinear part of the project. These are changes of representation; none implies that tuning the old tree's proposal can cross its absolute-integrability ceiling.

The first two cards below are separate mechanisms but should be combined as one residual/resummation family in the ten-direction synthesis. The plausible contribution is a code-compatible construction with moment and total-work certificates, not discovery of Feynman–Kac absorption, residual correction, or bounded polynomial voting.

## Project baseline and interpretation

The existing [long-horizon report](../../2026-09-25-long-horizon/07-report.md) supplies the historical baseline: the flat raw derivative-coded Allen–Cahn estimator has an absolute-integrability ceiling about 1.44551068, and the common-rate, uniform-tuple second-moment horizon is about 0.703890. These are properties of the specified raw expansion and assumptions, not of every branching representation. The existing soft majority estimator already handles finite horizons with bounded samples and was tested through T=2; its expected tree work remains exponential. This survey does not present that estimator as a new direction or rerun those results.

Local read-only inspection also found a practical constraint: `ParabolicPDE.f` currently takes only the solution value, and `FullyNonlinearPDE1D.f_expr` is expressed in jet variables. A generic reference v(t,x) introduces explicit space/time coefficient functions and their derivatives. Therefore, “subtract a reference” is not currently a generic callback substitution. Constant-reference residuals are a much smaller first interface target.

## Primary-source findings

| Source inspected | Precise result relevant here | Scope and limit |
| --- | --- | --- |
| [Henry-Labordère–Tan–Touzi, arXiv:1302.4624v3](https://arxiv.org/pdf/1302.4624), §2.1, (2.4)–(2.7), Assumption 2.2, Lemma 2.5; §2.3, Theorem 2.13 and Remark 2.14 | Uses the generator β(Σ a_k y^k − y), retaining the negative linear contribution in the branching clock. The absolute majorant contains the corresponding negative linear term. Its equilibrium alternatives can allow arbitrary finite horizons; otherwise an explosion integral restricts T. The representation is conditional on those assumptions. Remark 2.14 explicitly separates proposal-independent integrability from proposal-dependent variance. | Polynomial/power-series dependence on the value; also path dependence. This does not prove stability for arbitrary derivative-coded or Hessian-dependent nonlinearities. |
| [Gobet–Labart, SIAM J. Numer. Anal. 48 (2010)](https://doi.org/10.1137/090755060), and the inspected primary follow-up [Labart–Lelong, arXiv:1102.4666](https://arxiv.org/pdf/1102.4666), §2 Hypothesis 1 and §3.1 | The follow-up explicitly derives an error-correction expectation around an approximate solution and describes Picard plus adaptive control variates. Its assumptions include a bounded Lipschitz driver, ellipticity, and smooth terminal/diffusion data. The approximation includes iteration, extrapolation and, where used, Euler errors. | This is direct prior art for residual/control-variate thinking, not a theorem that an exact residual coding tree has globally finite moments. The original journal metadata and abstract were inspected; detailed formulas were checked in the accessible follow-up. |
| [An–Henderson–Ryzhik, arXiv:2209.03435](https://arxiv.org/html/2209.03435), §§3.2–3.3, Theorems 3.2–3.3 | Every polynomial f with f(0)=f(1)=0 has a random-outcome and a random-threshold voting representation for continuous initial data in [0,1]. Its construction uses Bernstein coefficients; the threshold version requires monotone voting probabilities and can use a larger rate. | Scalar reaction–diffusion, in arbitrary spatial dimension; no dependence on Du or D²u. Section 3.4's general recursive construction is not an all-T boundedness/finite-moment theorem for arbitrary polynomials. |
| [O’Dowd, Oxford MMath dissertation, 2019](https://www.stats.ox.ac.uk/~etheridg/odowd.pdf), §4.4 Proposition 4.4.2, Theorem 4.4.5 and Corollary 4.4.6; §4.5 | Generalized voting already covers real polynomials P with P(0)≥0 and P(1)≤0. It also considers arbitrary offspring distributions. Thus allowing inward-pointing, nonzero endpoint reactions is already prior art. | The thesis presents this in one spatial dimension. Its scalar polynomial algebra transfers to higher-dimensional diffusion, but a project theorem must state the corresponding diffusion and uniqueness assumptions. Do not cite the thesis as a fully nonlinear result. |
| [Etheridge–Freeman–Penington, arXiv:1607.07563](https://arxiv.org/pdf/1607.07563), §2.1 Theorem 2.2 | The majority-vote root probability represents the specified Allen–Cahn reaction, with leaf probabilities in [0,1]. | This is the existing project's comparison baseline after normalization. Mean-curvature scaling results later in the paper are distinct from numerical cost guarantees. |
| [Warin, arXiv:1701.07660](https://arxiv.org/pdf/1701.07660), §§2.2.1–2.2.3, (2.12)–(2.16); §3 | Coupled ghost subtraction and antithetic increments cancel low-order spatial contributions before derivative weights are applied. The paper demonstrates longer numerical maturities and describes Hessian constructions. It explicitly treats the fully nonlinear performance as numerical, without a general convergence proof. | Constant, nondegenerate diffusion is the clean setting. §2.3 uses Euler simulation for variable coefficients, introducing discretization bias. Ghost memory and nesting work can grow rapidly. The arXiv record is v1, January 2017; a later date printed in the rendered PDF is not evidence of a new version. |
| [Henry-Labordère–Oudjane–Tan–Touzi–Warin, arXiv:1603.01727](https://arxiv.org/pdf/1603.01727), §§2–3 | Marked branching handles polynomial dependence on (u,Du), with automatic differentiation and integrability conditions restricting maturity/nonlinearity. | Useful derivative-tree baseline; it does not establish a universal fully nonlinear or all-T result. |
| [Nguwi–Penent–Privault, arXiv:2201.03882](https://arxiv.org/pdf/2201.03882), introduction and §4 | Coding trees carry differential/function codes to known terminal data and avoid relying solely on repeated Malliavin weights; the representation requires integrability assumptions. | A ghost construction is an alternative/hybrid representation, not automatically an improvement obtained by attaching antithetics to this existing sampler. |

The bounded current-date search also checked [Huang–Privault, arXiv:2502.17853v2](https://arxiv.org/abs/2502.17853), revised 2026-03-09: its abstract identifies sufficient weighted-progeny integrability criteria and mild-solution uniqueness under uniform integrability. The parent survey covers its binary recoding in detail. [Kriechbaum–Ryzhik–Zeitouni, published November 2025](https://link.springer.com/article/10.1007/s11854-025-0402-3), studies discrete nonlocal recursion and front tightness; its abstract does not supply a continuous-PDE Monte Carlo cost theorem. No absence-of-prior-art claim follows from this bounded search.

## Candidate A — Absorb exactly known source and unary/linear contributions

**Mechanism and baseline.** Start from the PDE or its closed code equations, identify an exactly known linear operator, and use its semigroup/Feynman–Kac propagator. Branch only on the remaining nonlinear terms. This can preserve negative linear damping that is destroyed by taking the absolute values of individual unary histories. HLTT's killed branching formulation above is a strong existing baseline, not merely adjacent literature.

**What can change L1.** A scalar linear coefficient c contributes an exponential propagator exp(∫c); separately sampled unary terms are controlled by exp(∫|c|). For negative c, absorption can change the total variation of the expansion. For a nonnegative scalar coefficient and fixed-sign remaining skeleton, the unary terms already have the same sign: eliminating them primarily reduces sampling noise and cost, with no automatic improvement to the L1 horizon. Simply changing the lifetime and adding the reciprocal density weight is only a proposal change.

**Scope and exactness.** A known scalar potential can be retained exactly in principle. A known first-derivative coefficient can enter the drift. A known second-order coefficient can enter the diffusion only if the resulting principal matrix is admissible and simulable. Arbitrary higher-order derivative operators cannot generally be absorbed into an ordinary diffusion. Matrix/code couplings may require a coupled semigroup, whose closure and positivity cannot be assumed. Approximate path-integral quadrature or Euler transitions add bias unless separately corrected.

**Plausible project gap.** Certify exactly which unary chains can be eliminated from the project's code system, prove that the resulting recursive estimator represents the same mild equation, and compare its complete moment/cost system with the existing raw baseline. A generic “exponential integrator” label is insufficient.

**First falsifiable step.** On a scalar constant-coefficient reaction, derive both old and absorbed absolute-moment equations before implementing anything. Reject the horizon claim if the absorption only removes same-sign histories or the residual majorant still explodes at the same time. A useful sanity model is u′=−κu+bu², κ,b>0: the unabsorbed absolute expansion replaces −κ by +κ, whereas the killed nonlinear expansion retains −κ. This is a mechanism illustration for ordinary monomial branching, not the current NPP flat moment system.

**Obstacle, feasibility, cost.** Feasible for a constant scalar potential; conditional for spatially varying or infinite code systems. The inexpensive first target needs days rather than a general solver rewrite; a general closure/certificate study is plausibly several weeks. Total work may decrease through fewer unary events, but nonlinear population growth can remain exponential. These are planning estimates, not measured costs.

## Candidate B — Exact residual correction with damping-aware moment certificates

Use the project's backward convention

\[
u_t+Lu+F(t,x,J u)=0,\qquad u(T)=g,
\]

where J denotes the required jet. For a fixed, explicitly differentiable reference v, define

\[
w=u-v,\quad \eta=g-v(T),\quad
R_v=v_t+Lv+F(t,x,Jv).
\]

The exact correction equation is

\[
w_t+Lw+\{F(t,x,Jv+Jw)-F(t,x,Jv)\}+R_v=0,
\qquad w(T)=\eta.
\]

These identities define a proposed new expansion for w; they are not an estimate obtained by subtracting v after generating the old tree. For Allen–Cahn,

\[
w_t+Lw+(1-3v^2)w-3vw^2-w^3+R_v=0,
\quad R_v=v_t+Lv+v-v^3.
\]

If a=1−3v² is known and absorbed as in Candidate A, the exact mild equation uses the positive factor exp(∫a). Negative a therefore damps the residual branching; replacing it by |a| at unary events loses this effect. The remaining forcing R_v and terminal discrepancy η must both be retained. In forward time s=T−t, the forcing is Lv+F(v)−v_s, which is the same expression after the change of variables.

**Why small residual does not imply small tree moments.** Small R_v alone says nothing about η. Small deterministic errors do not control the total variation of their signed tree expansions. Large Jacobians and higher Taylor coefficients remain in the residual equation. For coding trees, all required derivatives of R_v, η, and the coefficient fields matter: a small-amplitude high-frequency perturbation can have large high-order derivatives. Finally, a negative Jacobian helps only if its sign survives the chosen representation. Pointwise comparison bounds on w are useful but do not prove the random correction lies in L1 or L2.

**Concrete initial screening target, not a completed theorem.** Use the known equilibrium v≡1, not the unknown full solution. Then R_v=0 and

\[
w_t+Lw-2w-3w^2-w^3=0.
\]

For an ordinary monomial residual tree retaining −2w as killing, the candidate value majorant is

\[
y'=-2y+3y^2+y^3,\qquad y(0)=\|g-1\|_\infty.
\]

Its nonnegative stationary threshold is (√17−3)/2≈0.56155. Thus the existing flat datum g=1/2 is a useful first algebraic screen; the sign-changing full wave is outside this uniform neighborhood. The proposed research step is to verify the precise tree identity, domination, L2 condition and work cost, then compare a deliberately imperfect constant reference with nonzero R_v. No new moment theorem or numerical gain is claimed here. This is closely related to HLTT's existing equilibrium-majorant criteria.

**Scope and exactness.** Exact for any fixed reference only when the full correction is represented and integrable, with exact coefficient evaluation/transitions. A trained or random reference can be frozen and conditioned upon; correction children must retain the independence required by nonlinear products. Ignoring forcing, terminating correction at a finite depth, clipping it, or using biased continuation gives an approximation that needs a stated error budget. The equation-level identity extends to fully nonlinear F, but an admissible stochastic linearization and control of every relevant jet remain unresolved.

**Plausible project gap.** A certificate that combines signed linear propagation, terminal/forcing jet norms and a full-code moment majorant, together with a truthful cost comparison. The accessible PACV work already establishes residual correction as a numerical idea; it does not establish this particular exact branching certificate.

**First falsifiable step.** Compare three representations for one nonzero correction: uncentered raw tree, centered tree that still branches on the linear term, and centered tree with that term absorbed. Derive the moment equations first. A failure of the derivative norms or of the absorbed majorant is a valid rejection; a small observed sample variance is not acceptance.

**Obstacle, feasibility, cost.** Constant references are a credible small first project. General v(t,x) is conditional on a new coefficient/jet interface and global bounds, particularly difficult in high dimension. Expect several days for the scalar screening and weeks for a defensible nonconstant extension; count reference construction and evaluation in the total work. The strongest initial target is a stable-phase neighborhood, not arbitrary fully nonlinear long-time dynamics.

## Candidate C — A certified, cost-aware bounded-voting compiler

**Established mechanism.** Normalize a known invariant interval [a,b] to [0,1]. The normalized reaction f has inward endpoint signs. In Bernstein degree N, write f=Σ b_k B_{k,N}; a rate β and voting probabilities α_k=k/N+b_k/β reproduce the reaction when 0≤α_k≤1. AHR covers equilibrium endpoints; O’Dowd already covers the general inward case. The leaf/parent votes remain bounded. This is an actual change of representation and can remove the old raw L1 ceiling for the covered scalar problem class.

**Project gap.** Automate a verified conversion and compare feasible degrees, offspring mixtures, rates, hard votes and conditional soft votes by total cost at a target error. Existing majority is the cubic example, not a new invention. Enlarging the class beyond Allen–Cahn is useful integration work; a genuinely new result would need a sharper, established distinction such as an optimality/cost certificate in a stated representation family.

**Why “usable T” still needs research.** Bounded samples control moments, but a full N-ary tree at rate β has expected total nodes

\[
\frac{N e^{\beta(N-1)T}-1}{N-1}\quad(N>1).
\]

A smaller sufficient rate or alternative arity can materially affect this exponent. Conditional soft voting may lower variance while requiring all children; hard threshold votes may permit exact early determination of some parent outcomes. Neither option universally minimizes variance times work. Any proposed lazy evaluation must preserve the exact vote, rather than omit inconvenient branches.

**Scope and exactness.** Scalar polynomial reactions with certified interval data; the algebra does not cover gradient/Hessian nonlinearities. Exact in the finite-tree model under the diffusion/uniqueness assumptions. A polynomial approximation to a nonpolynomial reaction changes the PDE and requires approximation-error control. Invariance of the PDE solution alone is not a boundedness proof for the raw coding-tree output. For general recursive polynomials without an invariant interval, even deterministic scalar solutions can blow up, so no all-T conclusion is available.

**First falsifiable step.** Choose a non-Allen–Cahn polynomial already covered by the theorem, verify all Bernstein probabilities symbolically, and compute the certified rate–arity work exponent before sampling. Require a predeclared work/error gain over a straightforward fixed-degree construction; do not claim success just from boundedness or from reimplementing majority.

**Obstacle, feasibility, cost.** Feasible for a small polynomial catalogue, with low-to-moderate integration cost and a clear exactness test. Cost optimization is conditional on the comparison family and moment/work analysis. Several days can establish a bounded prototype contract; a novel optimization theorem could take weeks. High degree and stiff reactions can make the guaranteed representation computationally unusable despite finite moments.

## Candidate D — Ghost/antithetic cancellation for derivative subtrees

**Established mechanism.** Couple subtrees at positive, negative, and/or zero Brownian increments, and combine them before multiplying by derivative weights. For a smooth payoff, first differences scale as √h and centered second differences as h, offsetting the h^(−1/2) and h^(−1) singular weights. Warin's §§2.2 and 3 give concrete constructions. These local cancellations change the random integrand; they are more than a new lifetime proposal.

**Project gap.** Investigate a hybrid representation that uses these cancellations only for selected derivative codes where they reduce the total moment/cost bound. This requires comparing with NPP's code propagation, which already avoids the original repeated-Malliavin-weight obstruction. The task is not “add antithetic Brownian motion everywhere.” In particular, spatial antithetics do not explain or remove the flat Allen–Cahn sign problem where spatial derivatives vanish.

**Scope and exactness.** The first target is constant nondegenerate diffusion with polynomial value/gradient dependence and sufficient regularity. Hessian variants exist in the cited numerical paper, but a general nonlinear recursive integrability theorem is not supplied there. Exact identities for smooth fixed payoffs do not automatically imply exact, finite-variance recursive estimators: the coupled random subtrees need the corresponding increment estimates. Variable-coefficient Euler implementations are biased.

**First falsifiable step.** For one genuinely spatial derivative nonlinearity, formulate coupled subtree bounds such as an L2 first-difference bound proportional to h, uniformly over all recursively encountered states/codes. Check whether a closed moment inequality survives the multiplication of independent children and the correlated ghost copies. If only a one-step smooth-payoff calculation closes, the claimed full-tree horizon extension fails. Proposed experiments should compare full work and derivative accuracy; empirical slopes alone cannot certify finite population moments.

**Obstacle, feasibility, cost.** Conditional, with greater theory cost than scalar residuals or voting. Ghost copies introduce covariance bookkeeping and potentially severe memory growth; using independent ghosts can destroy cancellation. A narrow two-code example is a plausible several-week study. Arbitrary-order jet support is a longer and higher-risk extension. Nesting from Warin §2.1.3 is separate prior art and should be scored elsewhere in the parent survey.

## What conditioning can and cannot justify

1. Removing a term known identically zero saves work but does not reduce a positive absolute-moment measure: its contribution was already zero. A finite sample that happens to vanish is not such a symbolic certificate.
2. Exact conditioning of an integrable estimator H gives E|E[H|G]|≤E|H| and can improve L2. A strict L1 improvement requires cancellation inside the conditioned groups. Integrating only same-sign contributions can reduce variance while leaving L1 unchanged.
3. A known source convolution can reduce total variation if spatial/time integration produces cancellation before a branch weight is formed. Merely evaluating a nonnegative known source more accurately is not an L1-horizon extension.
4. If C is integrable and E|H| is infinite, ordinary terminal control-variate subtraction H−C still cannot be integrable. A residual PDE changes the recursively sampled expansion and avoids that obstruction; it is not the same as a final additive subtraction.
5. Once the old H is outside L1, ordinary conditional expectation/Rao–Blackwell arguments cannot be invoked to define its mean. Justify the new representation directly from its mild equation, or from finite truncations with a proved uniform-integrability/dominating limit. Do not regroup an arbitrary divergent signed series and declare it unbiased.

The proposed first research gate is therefore: **does the new, precisely specified representation have a strictly better complete moment bound at a useful total cost?** An identity for the PDE, a bounded deterministic solution, or smaller Monte Carlo samples alone does not settle that gate.

## Query and access log

All queries below were run on 2026-09-27 using web search; arXiv/author/publisher full texts were then opened as indicated above. Search was bounded and stopped at the parent task's request. Secondary search hits were used only to locate primary sources, not as authority for mathematical claims.

- `An Henderson Ryzhik 2209.03435 voting branching reaction diffusion`
- `Etheridge Freeman Penington 1607.07563 branching Brownian motion majority voting`
- `Warin branching diffusion ghost particles renormalization semilinear nonlinear PDE antithetic`
- `site.arxiv.org "Variations on branching methods for non linear PDEs"`
- `"Truncation and renormalization techniques" branching`
- `"branching" "PDEs" "control variates"`
- `"branching" "residual" "semilinear" Monte Carlo`
- `branching nonlinear PDE deterministic approximation residual control variate arxiv`
- `"Solving BSDE with adaptive control variate" Gobet Labart`
- `"Solving BSDE with adaptive control variate" filetype:pdf -site:researchgate.net -site:citeseerx.ist.psu.edu`
- `"Solving BSDE with adaptive control variate" "hal"`
- `"branching" "defect correction" PDE` and `"branching" "residual centering" PDE` — no direct exact residual-tree theorem identified.
- `branching Monte Carlo semilinear PDE "resummation"` — many unrelated physics hits; not evidence against relevant prior art.
- `"A Numerical Algorithm for a Class of BSDEs via the Branching Process" arxiv`
- `"branching" "linear term" "semilinear"` and `"branching" "dissipative" "PDE" Monte Carlo`
- `"branching diffusion" "2025" "variance"`; `"branching" "PDE" "2026" "renormalization"`; `site.arxiv.org "stability" "branching diffusion" "2026"`
- `"O'Dowd" "Branching Brownian" thesis`; author-hosted dissertation opened, §4.4 inspected.
- `"voting models" "semilinear" "2025"`; `"Bernstein" "branching Brownian" "2026"`
- `"Voting models and tightness for a family of recursion equations" arxiv` — primary publisher abstract checked; discrete-recursion scope recorded.

Access caveat: the attempted Gobet research-page URL returned HTTP 403. The exact residual-correction formulas were instead read in Labart–Lelong's primary arXiv paper. The standalone work cited by Warin as “Truncation and renormalization techniques…” was not independently located and is not treated here as a verified separate theorem source. The broad residual-tree novelty comparison remains provisional even though its main classical ingredients are well established.
