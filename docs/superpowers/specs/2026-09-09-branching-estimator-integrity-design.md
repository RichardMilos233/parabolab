# Branching estimator integrity research programme

> **Archived design — status reviewed 16 September 2026.**
> The moment, Dym, proposal, and finite Lean foundations were developed under
> this design. Current research centers on branching-PDE estimator algorithms,
> scalar lambda, tuple probabilities q, and their mathematical guarantees.
> The finance-led twelve-week programme and secondary-candidate ranking below
> are historical proposals, not the current work plan. Refer to the proof
> registry for what was actually proved and formalized.
> Navigation: [archive index](../README.md), [current research](../../research/README.md),
> [documentation map](../../documentation-map.md).

Original approval date: 2026-09-09.

## Goal

Develop a twelve-week, theorem-led final-year-project extension of `parabolab`
that studies when branching and coding-tree Monte Carlo estimators are
mathematically well defined, how moment failure can be detected, and how
branching proposals should be chosen to minimize simulation risk.

The project is aimed at quantitative-research roles. Its finance narrative is
unbiased simulation, moment explosions, importance sampling, confidence
guarantees, and model validation. A reduced Merton--Vasicek HJB problem is the
controlled finance benchmark; the project does not claim to produce trading
alpha or a production pricing engine.

The final deliverable contains ten ranked candidate contributions. Three
receive complete paper-level proofs and numerical studies. The other seven
receive precise theorem statements, prior-art boundaries, and either proof
plans, conditional results, or counterexamples.

## Terminology and novelty policy

Use **candidate contribution**, not **breakthrough**, until a complete
literature review and expert assessment establish priority.

Every result must be labelled as exactly one of:

- proved theorem;
- conditional theorem, with every unproved assumption stated;
- conjecture;
- counterexample or impossibility result;
- empirical result;
- prior-art overlap.

Numerical agreement is evidence about an implementation or a falsification
test. It is never a mathematical proof. An apparently stable finite Monte
Carlo sample is not evidence that the sampled functional is integrable.

The bounded literature audit found close prior art for general branching
representations, semilinear stability bounds, adaptive importance sampling,
Sobolev training, and semilinear elliptic regularization. It did not locate
the exact arbitrary-jet moment system or a Dym-specific non-integrability
proof. Absence from that audit does not establish global novelty.

## The ten candidate contributions

### Deep result 1: exact multitype moment system

For each coding-tree code \(c\) and \(p>0\), derive the exact equation for

\[
V_c^{(p)}(t,x)=\mathbb E\left[|H_{t,x,c}|^p\right]
\in[0,\infty].
\]

For a remaining horizon \(\Delta=T-t\), lifetime density \(\rho_c\), survival
function \(\bar F_c\), Markov semigroup \(P_s\), finite mechanism
\(\mathcal M(c)\), and proposal \(q_c\), the target equation has the form

\[
\begin{aligned}
V_c^{(p)}(t,x)
={}&
\bar F_c(\Delta)^{1-p}
P_\Delta |g_c|^p(x)\\
&+
\sum_{Z\in\mathcal M(c)}
q_c(Z)^{1-p}
\int_0^\Delta
\rho_c(s)^{1-p}
P_s\left[
\prod_{z\in Z}V_z^{(p)}(t+s,\cdot)
\right](x)\,ds.
\end{aligned}
\]

Any deterministic mechanism coefficient not already encoded in a child code
must appear through its absolute \(p\)-th power in the corresponding term.
The implementation and theorem must use one convention consistently.

Define a depth-\(n\) killed tree by assigning value zero when an interior
branch would exceed depth \(n\). Prove:

1. first-event conditioning gives the finite-depth recursion;
2. the nonnegative Picard iterates are monotone in \(n\);
3. under almost-sure tree nonexplosion they converge to
   \(V_c^{(p)}\), possibly \(+\infty\);
4. their supremum is the minimal nonnegative fixed point;
5. \(H_{t,x,c}\in L^p\) if and only if that component is finite.

This sharpens sufficient dominating-tree criteria by characterizing the
actual multitype coding-tree functional.

### Deep result 2: Dym non-integrability

For the Dym example used in JEQ2023 and implemented by
`parabolab.library.dym_1d`, use

\[
f(z_0,z_1,z_2,z_3)
=-\frac12z_2+z_0^3z_3,
\qquad
\phi(x)=|6x|^{2/3}.
\]

The live \(f^*\)-mechanism contains the tuple

\[
\bigl((f_{z_2})^*,(f_{z_0})^*,D^2\bigr).
\]

Verify

\[
f_{z_2}=-\frac12,\qquad
f_{z_0}(\phi,J\phi)=\frac{32}{x}
\quad (x\ne0),\qquad
|\phi''(x)|\asymp |x|^{-4/3}.
\]

For every positive horizon and the repository's exponential clock and
full-support uniform tuple proposal, isolate the event that:

1. the root branches to \(f^*\);
2. the \(f^*\) particle branches and selects the displayed tuple;
3. the resulting children survive to the terminal time.

Condition on branch times and the shared branch position. Restrict all
nonsingular factors to positive-probability compact sets. A nondegenerate
Gaussian endpoint has a density bounded below near zero, so the conditional
absolute expectation contains

\[
\int_{-\varepsilon}^{\varepsilon}\frac{g(y)}{|y|}\,dy
=\infty.
\]

Conclude

\[
\mathbb E|H_{t,x,\mathrm{Id}}|=\infty.
\]

When the singular tuple has positive proposal probability, control the signs
on the other factors and prove separately that

\[
\mathbb EH^+=\mathbb EH^-=\infty.
\]

The theorem must not be stated for an arbitrary lifetime law that cannot
branch before the horizon, for a proposal that removes all singular live
tuples, for zero horizon, or for a degenerate zero terminal parameter. A
Cauchy principal value is not a probabilistic expectation.

### Deep result 3: safe adaptive branching proposals

Suppose all relevant continuation second moments are finite. Conditional on
a code, branch time, and branch position, write the second-moment contribution
of tuple \(Z\) as \(A_Z\ge0\). Prove by Cauchy--Schwarz that

\[
q^*(Z)
=\frac{\sqrt{A_Z}}{\sum_Y\sqrt{A_Y}}
\]

minimizes

\[
\sum_Z\frac{A_Z}{q(Z)}
\]

over supported proposals.

For a fixed horizon, treat "survive to the leaf" and "branch at time \(s\)"
as alternatives in one first-event proposal. If the proposal assigns leaf
probability \(r_0\) and branch-time density \(r(s)\), its second-moment
objective contains

\[
\frac{A_0}{r_0}+\int_0^\Delta\frac{A(s)}{r(s)}\,ds,
\qquad
r_0+\int_0^\Delta r(s)\,ds=1.
\]

Derive the joint optimum

\[
r_0^*\propto\sqrt{A_0},
\qquad
r^*(s)\propto\sqrt{A(s)}.
\]

This fixed-horizon result must not be presented as the unconstrained optimum
over exponential rates: changing an exponential lifetime law also changes
its survival probability, so the leaf and branch terms are coupled.

The practical method must use two independent stages:

1. estimate continuation moments from pilot samples;
2. apply an explicit positive probability floor, freeze the proposal, and
   evaluate with fresh random samples and exact likelihood ratios.

Conditional on the pilot, prove that the evaluation estimator remains
unbiased. For finite depth and bounded mechanism tables, assume that every
live oracle probability is at least a stated constant \(q_{\min}>0\) and
that pilot continuation-moment estimates satisfy a stated uniform additive
or multiplicative error bound. Under those assumptions, prove a
high-probability excess second-moment bound relative to the oracle proposal.
Report efficiency as variance times expected tree-node cost, not variance
alone.

Extending the oracle bound to the unrestricted tree is optional and may only
be claimed after proving uniform integrability and expected-cost control.

### Secondary result 4: state-dependent arbitrary-jet representation

For

\[
u_t+\frac{\sigma^2}{2}\Delta u+
f(x,D^{\alpha_1}u,\ldots,D^{\alpha_m}u)=0,
\]

derive the mechanism for codes
\((a\,\partial_x^\beta\partial_z^\nu f)^*\), including explicit spatial,
mixed spatial--jet, and jet-Hessian terms. State a representation theorem
under smoothness, nonexplosion, integrability, and uniqueness assumptions.
This formalizes the extension already implemented in `state_dependent.py`.

### Secondary result 5: derivative-code Sobolev training

Use direct code labels \(Y_\mu\) satisfying

\[
\mathbb E[Y_\mu\mid X]=D^\mu u(X)
\]

to derive the population identity

\[
\sum_\mu w_\mu\mathbb E
\left(Y_\mu-D^\mu v(X)\right)^2
=
\sum_\mu w_\mu
\left\|D^\mu u-D^\mu v\right\|_{L^2}^2
+\text{a constant independent of }v.
\]

State the additional moment and denominator-separation assumptions needed to
infer Greeks or HJB controls. Heavy-tailed derivative labels and unstable
ratios are first-class failure modes.

### Secondary result 6: robust deep branching

Develop a finite-sample regression statement for heavy-tailed tree labels
using an explicit robust mean or robust risk construction. Contrast it with
the current percentile filter, which can remove genuine rare events and
change the target expectation. Any robustness-induced bias must be stated.

### Secondary result 7: coupled multifidelity control variates

For a high-fidelity functional \(H^\theta\), a coupled control \(H^0\), and
known \(u^0=\mathbb EH^0\), analyze

\[
\widehat u_\beta
=\frac1N\sum_{i=1}^N
\left[H_i^\theta-\beta(H_i^0-u^0)\right].
\]

The nontrivial target is a stable common-tree coupling for the reduced
Merton--Vasicek model and a perturbative \(L^2\) bound. A deterministic
approximation without a correlated random control is not a variance-reduction
result.

### Secondary result 8: coefficient sensitivities and policy intervals

For a nonzero polynomial coefficient \(a_r\), derive the finite-tree identity

\[
\partial_{a_r}u
=
\mathbb E\left[H\,N_r/a_r\right],
\]

under a justified differentiation--expectation interchange. Combine direct
jet estimators with a multivariate central limit theorem and the delta method
only where second moments exist and HJB policy denominators are bounded away
from zero.

### Secondary result 9: Monte Carlo challenger-model certificate

For finitely many deterministic solver outputs \(v_\ell\), use an independent
robust Monte Carlo reference \(\widehat u\). On
\(\|\widehat u-u\|\le r\), prove that nearest-candidate selection satisfies

\[
\|v_{\widehat\ell}-u\|
\le
\min_\ell\|v_\ell-u\|+2r.
\]

This is a model-validation theorem, not a claim that branching Monte Carlo
is immune to ill-conditioning or moment failure.

### Secondary result 10: short-time wave proposal optimum

For the one-dimensional wave estimator, smooth data, a nonzero local value
\(b=\phi(z)\), fixed full-support offspring law \(q\), and
\(\lambda=\gamma t\), derive the short-time variance expansion and optimize
its leading term jointly over \(q\) and \(\gamma\). Treat the case \(b=0\)
separately because the scaling changes. This is a supporting result from
`wavelab`, not part of the primary implementation.

## Common mathematical architecture

Use one abstract finite-depth multitype branching model for the first three
results:

- a finite or countable code space;
- finite live mechanism tables;
- code-dependent tuple probabilities;
- code-dependent lifetime laws;
- a shared Markov branch position;
- child subtrees independent conditional on that position;
- exact likelihood weights;
- almost-sure nonexplosion for the full-tree limit.

The proof dependency order is:

1. finite-depth tree and first-event recursion;
2. nonnegative moment operator and minimal fixed point;
3. Dym mechanism instantiation and singular-event lower bound;
4. local tuple and lifetime proposal optimizers;
5. pilot/freeze unbiasedness;
6. finite-depth proposal oracle inequality.

The hard case is addressed first in each proof. Earlier helper lemmas may
temporarily remain admitted during development, but the final Lean deliverable
must contain no `sorry` and the final mathematical note must have no hidden
integrability or support assumptions.

## Lean boundary

Formalize:

- finite labelled mechanism tables and finite-depth evaluators;
- the exact finite-depth \(p\)-moment recursion;
- monotonicity and minimal fixed-point iteration in `ENNReal`;
- treatment of duplicate labelled tuples and embedded coefficients;
- Cauchy--Schwarz optimization on a finite proposal simplex;
- Dym derivative identities on the two half-lines;
- divergence of the \(x^{-1}\) and \(x^{-4/3}\) singular integrals;
- elementary bounded-arity nonexplosion estimates if the available
  infrastructure makes this proportionate.

Leave the following as conventional, fully written mathematical arguments:

- measurable continuous-time Ulam--Harris trees;
- regular conditional laws at random shared branch positions;
- conditional independence of Brownian child subtrees;
- recursive estimator measurability;
- Gaussian-kernel positivity at arbitrary singular points;
- monotone limits over the full random tree.

Attempting to build all of that measure-theoretic infrastructure in Lean is
outside the twelve-week scope.

Lean proofs must be developed one tactic at a time, with diagnostics checked
after each tactic. Syntax errors, then type errors, then unsolved goals, then
lint warnings are fixed in that order. `done` is used whenever further goals
are expected. No result is complete while any `sorry` remains.

## Repository architecture

`parabolab` owns the primary research implementation. Changes are additive:

- a moment-recursion module;
- a proposal-optimization module;
- tests for both modules;
- reproducible Dym, moment, and proposal experiments;
- a self-contained Lean project for the formal core;
- a research note containing theorem statements, proofs, assumptions,
  literature boundaries, and numerical findings.

`wavelab` remains a supporting repository for candidate 10 and existing
ill-posedness evidence. Its solver API is not refactored.

Implementation work will use a dedicated branch or worktree after this design
and its implementation plan are approved. Existing uncommitted changes in
`demo/merton.py` and `demo/merton_vasicek.py` are user-owned and must not be
edited or included in commits.

## Numerical design

### Exact moment recursion

- compute finite-depth moment iterates deterministically for small mechanism
  tables;
- compare them with independent Monte Carlo from the identically truncated
  tree;
- test \(p=1\) and \(p=2\) separately;
- include cases with finite and visibly diverging iterates;
- record depth, code, state, horizon, proposal, and numerical tolerance.

### Dym singularity

- reproduce the live tuple and derivative identities with SymPy;
- regularize terminal singularities at a cutoff \(\varepsilon\);
- show that truncated absolute moments grow at the predicted logarithmic or
  power rate as \(\varepsilon\downarrow0\);
- demonstrate why larger finite samples can look stable before rare singular
  endpoints are observed;
- do not use clipping or deletion of tail observations.

The cutoff experiment corroborates the analytic asymptotic. The proof is the
positive-probability event and divergent integral.

### Proposal optimization

- estimate continuation moments on pilot seeds;
- freeze tuple and lifetime proposals before evaluation;
- preserve positive support with a documented floor;
- compare uniform, hand-tuned, oracle-on-a-small-control, and piloted
  proposals;
- report mean, robust uncertainty where justified, sample variance when
  \(L^2\) is established, maximum magnitude, tree-size quantiles, and
  variance times expected node count;
- use disjoint pilot and evaluation random streams.

### Finance benchmark

Use the exact no-consumption reduced Merton--Vasicek solution already present
in the repository as the primary finance control. The consumption problem is
not a reference until positivity, an independent numerical solution, and its
tree integrability have been established. Policy recovery is not validated by
value-function agreement alone.

## Validation and acceptance

Before implementation, record the current test baselines:

- `parabolab`: 143 passed and 13 deselected in the latest read-only audit;
- `wavelab`: 163 passed and 7 deselected in the latest read-only audit.

Final acceptance requires fresh evidence:

1. all relevant pre-existing Python tests pass;
2. every new deterministic recursion test passes;
3. Monte Carlo checks use fixed, documented seeds and disjoint pilot/evaluation
   streams;
4. the Lean project compiles with no `sorry`;
5. symbolic checks identify the exact Dym tuple and derivative constants;
6. numerical outputs are reproducible from checked-in commands;
7. Gaussian standard errors are reported only where \(L^2\) is established;
8. no outlier filtering silently changes an estimator's target;
9. each claim has an explicit theorem statement, proof status, and novelty
   status, with a complete proof for every result labelled proved;
10. prior-art overlap is cited rather than marketed as novelty.

## Twelve-week schedule

- **Weeks 1--2:** definitions, source audit, finite-depth abstract model, and
  Lean project skeleton.
- **Weeks 3--4:** exact moment theorem, deterministic recursion, and
  finite-depth Monte Carlo comparison.
- **Week 5:** Dym proof, symbolic verification, and singular-cutoff study.
- **Weeks 6--8:** oracle proposals, pilot/freeze unbiasedness, finite-depth
  oracle inequality, and cost-adjusted numerical comparisons.
- **Weeks 9--10:** Merton--Vasicek benchmark and precise treatments of the
  seven secondary candidates.
- **Week 11:** complete and clean the Lean formal core.
- **Week 12:** full reproducibility run, proof audit, novelty-language audit,
  and final research dossier.

## Non-goals

- proving ten publication-grade novel theorems in one FYP;
- claiming global novelty from a bounded web search;
- formalizing the complete Brownian branching construction in Lean;
- treating numerical stability as proof of estimator integrability;
- deleting rare observations to improve plots or standard errors;
- claiming dimension-free complexity without dimension-uniform moment and
  cost bounds;
- claiming bounded-domain/barrier pricing from whole-space code;
- claiming the project generates trading alpha or production P&L;
- modifying the user's uncommitted Merton demo work.

## Decision

Proceed with the estimator-integrity route. Complete the exact moment theorem,
the Dym non-integrability theorem, and the finite-depth safe adaptive-proposal
theorem first. Treat the seven remaining items as ranked secondary
contributions whose status may be theorem, conditional theorem, conjecture,
counterexample, or prior-art overlap.
