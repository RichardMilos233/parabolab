# Multifactor Merton proof record and research roadmap

> **Archived design; financial application inactive — reviewed 16 September 2026.**
> The proof registry, multifactor mathematical notes, and historical roadmap
> were produced. The proposed multifactor-Merton implementation programme is
> inactive, and its tasks are not outstanding requirements for current work.
> The evidence-recording conventions remain useful; historical implementation
> and Lean descriptions must be checked against the current proof registry.
> Navigation: [archive index](../README.md), [current research](../../research/README.md),
> [documentation map](../../documentation-map.md).

Original approval date: 2026-09-09.

## Goal

Create a durable, auditable record of every mathematical claim and proof in
the project, then document a literature-backed route from the existing
Merton--Vasicek prototype to a genuinely multidimensional Merton benchmark.

The record must distinguish:

- a complete conventional proof;
- a conditional theorem;
- a proof sketch or proof route;
- a Lean-formalized substatement;
- symbolic, deterministic, or Monte Carlo evidence;
- a conjecture;
- an engineering contribution;
- a novelty claim supported only by a scoped literature search.

No numerical experiment or successful Lean build may be described as proving
more than it actually establishes.

## Deliverables

### 1. Atomic proof registry

Create `docs/research/proof-registry.md`. Each claim receives a stable
identifier and an independent record of:

- exact statement and source;
- assumptions, split into structural, analytic, probabilistic, integrability,
  uniqueness, and domain assumptions;
- conventional-proof status and location;
- Lean coverage, exact theorem names, and omitted obligations;
- implementation correspondence;
- symbolic, deterministic, and statistical evidence;
- novelty status and closest prior art;
- dependencies and open obligations;
- last-reviewed commit.

The registry is the source of truth for proof status. Existing thematic notes
remain the source of the full proofs.

### 2. Multifactor Merton research roadmap

Create `docs/research/multifactor-merton-roadmap.md` containing:

1. the recovered prior discussion;
2. the distinction between high-dimensional controls and high-dimensional
   PDE states;
3. a primary-source literature map;
4. the general factor-model HJB and CRRA reduction;
5. the recommended two-factor OU benchmark;
6. exact or semi-exact matrix-Riccati validation;
7. coding-tree proof obligations;
8. estimator-integrity and proposal requirements;
9. a dependency-ordered implementation and theorem roadmap;
10. safe and unsafe novelty language.

### 3. Visual mirror

Update the existing research Canvas with a multifactor-Merton section showing:

- what is already proved;
- what is only partially formalized;
- the current Vasicek prototype;
- the recommended two-factor benchmark;
- ranked candidate contributions;
- blocking proof obligations.

Markdown remains authoritative. The Canvas is a navigational and explanatory
mirror, not a second proof source.

### 4. Reader test

Give the completed documents to a fresh-context reader agent. Test whether it
can correctly answer:

- Which results are fully proved on paper?
- Which parts are actually formalized in Lean?
- Why is the present wealth--rate equation not genuinely multidimensional
  after CRRA reduction?
- What defect prevents the unreduced 2D tree from being globally valid?
- What is the recommended new model?
- Which proposed contributions are potentially novel, and with what caveats?

Repair any ambiguity or overclaim before completion.

## Baseline proof inventory

The registry will begin with the following families.

### Estimator moments

The conventional notes record:

- the killed-depth tree identity;
- the exact finite-depth multitype \(p\)-moment recursion;
- monotone convergence to the minimal nonnegative fixed point;
- the pointwise \(L^p\)-finiteness criterion.

Lean currently verifies selected finite-dimensional algebra and
order-theoretic core lemmas. It does not formalize random trees, conditional
expectations, Markov kernels, Brownian motion, nonexplosion, or identification
of the operator iteration with the tree functional.

### Dym non-integrability

The conventional notes record:

- a positive-probability shallow topology producing a reciprocal
  singularity;
- divergence of the absolute first moment;
- divergence of both signed parts under the stated sign/topology conditions.

Lean currently verifies the relevant algebraic coefficient identity and
one-dimensional reciprocal-integral divergence. It does not formalize the
Gaussian branch position, tree event, expectation, or signed-part theorem.

### Adaptive proposals

The conventional notes record:

- the finite-table square-root optimizer;
- a first-event time-density optimizer;
- pilot/freeze unbiasedness under support and integrability conditions;
- finite-depth local and global oracle inequalities.

Lean currently verifies selected finite-vector inequalities. It does not
formalize pilot sigma-fields, Radon--Nikodym factors, tree-law changes,
conditional unbiasedness, or unrestricted-tree limits.

### Secondary candidates

The registry will separately classify:

- state-dependent arbitrary-jet coding;
- derivative-code Sobolev training;
- robust deep branching;
- multifidelity coupling;
- coefficient sensitivities and policy intervals;
- challenger-model certificates;
- short-time wave proposal asymptotics.

Conditional theorems, classical results, conjectural rates, and prior-art
overlap must remain visibly distinct.

## Meaning of multidimensional Merton

With many constant-coefficient risky assets, the portfolio control is a vector
but total wealth can remain the only PDE state. After optimizing the portfolio,
the assets enter through a squared Sharpe-ratio quantity such as

\[
(\mu-r\mathbf 1)^\top\Sigma^{-1}(\mu-r\mathbf 1).
\]

A genuinely multidimensional Merton PDE requires several evolving opportunity
states: rates, expected-return predictors, volatility factors, beliefs,
income, or holdings.

The existing independent-Vasicek model has the unreduced state
\((x,r)\), but CRRA homogeneity gives

\[
V(t,x,r)=\frac{x^{1-\gamma}}{1-\gamma}F(t,r).
\]

It is therefore a valuable state-dependent and unreduced cross-check, but its
irreducible factor dimension is one.

## Recommended benchmark

Use two economically distinct Gaussian opportunity factors:

- an OU short-rate factor;
- an OU expected-excess-return factor.

Let \(Y_t\in\mathbb R^2\) satisfy

\[
dY_t=K(\bar y-Y_t)\,dt+B\,dW_t^Y,
\]

and let risky-asset excess returns be affine in \(Y_t\). Permit constant
asset--factor correlation. Under CRRA terminal utility, remove wealth and
obtain a genuinely two-dimensional factor PDE.

The first benchmark omits intermediate consumption. Under standard
quadratic-process restrictions, use

\[
F(t,y)=
\exp\!\left(a(t)+b(t)^\top y+y^\top Q(t)y\right),
\]

where \(a,b,Q\) satisfy scalar, vector, and matrix Riccati ODEs. This supplies
values, gradients, and policies as independent ground truth.

After the two-factor case is correct, expose the same construction for
\(m=1,2,5,10,20\) factors to study dimension, covariance conditioning,
correlation rank, tree size, moments, and runtime.

## Required mathematical extensions

### Constant-covariance state-dependent mechanism

For reference covariance \(A\succeq0\), the mechanism must represent

\[
\partial_tu+\frac12 A:D^2u+f(x,Ju)=0.
\]

The state-dependent code

\[
G_{a,\beta,\nu}
=
\left(a\,\partial_x^\beta\partial_z^\nu f\right)^*
\]

requires direct-space, mixed space--jet, and jet-Hessian terms carrying all
entries \(A_{kl}\). The current implementation is only the specialization
\(A=\sigma^2I\).

The representation theorem remains conditional on smoothness, justified
differentiation, terminal measurability, nonexplosion, absolute
integrability, passage to the full-tree limit, and uniqueness of the mild
system.

### Degenerate factor-only diffusion

The unreduced Merton formulation must not add artificial nondegenerate
Brownian noise to wealth. For fractional CRRA terminal utility,
\(x^{1-\gamma}\) is not real on negative wealth, while a Gaussian wealth
coordinate reaches negative values with positive probability at every
positive horizon.

The solver therefore needs either:

- a singular diffusion factor that moves only the opportunity factors; or
- a valid log-wealth formulation with a separately derived mechanism.

The reduced factor equation is the preferred benchmark because it removes
this support problem entirely.

### Correlation and mixed derivatives

Constant factor covariance can be whitened by a linear coordinate transform,
but asset--factor correlation survives the CRRA reduction as a nonlinear
quadratic form in \(\nabla F\). This is the part that turns the exact
multi-factor benchmark into a meaningful nonlinear coding-tree test.

### Moment and proposal certification

Before reporting Gaussian standard errors:

- establish or numerically certify the required \(L^2\) regime;
- distinguish finite-depth stabilization from a proof for the infinite tree;
- retain independent pilot and evaluation randomness;
- impose proposal floors on all live mechanism alternatives;
- compare variance together with expected tree work;
- require higher moments when estimating continuation second moments.

## Candidate contributions

The roadmap will rank, rather than prematurely label, the following.

### Candidate A: explicit-state arbitrary-jet representation

Potential theorem: a coding-tree representation for
\(f(x,Ju)\) with mixed direct-state and jet derivatives under constant
possibly singular covariance.

Novelty caveat: state-dependent branching and arbitrary-jet coding each have
nearby prior art. The potentially new object is their precise combined
mechanism and representation theorem.

### Candidate B: irreducible multifactor Merton benchmark

Potential contribution: the first systematic coding-tree study located for a
CRRA-reduced, genuinely multifactor Merton HJB with matrix-Riccati ground
truth.

Novelty caveat: the Merton model and Riccati solution are classical, and
high-dimensional coding trees already exist. The contribution is their
intersection and its estimator analysis.

### Candidate C: infinite-tree moment certificate

Potential theorem: turn the exact multitype moment recursion into a usable
code/state-conditioned certificate for the unrestricted estimator, then use
it to determine admissible horizon and proposal regimes.

Novelty caveat: minimal fixed points and smoothing transforms have extensive
prior art. The claim must be specific to the coding-tree mechanism and its
computable certificate.

### Candidate D: jointly optimized reference diffusion and proposal

Potential theorem and algorithm: rewrite around a tractable reference
covariance \(A_0\), include \((A-A_0):D^2u/2\) in the mechanism, and optimize
\(A_0\), lifetime law, and tuple proposals using moment surrogates.

Novelty caveat: changing reference processes and importance sampling are
classical. The potentially new element is the joint coding-tree
second-moment/work optimization.

### Candidate E: value-and-policy certification

Potential contribution: estimate value and derivative codes jointly, recover
feedback controls, propagate covariance to policy intervals, and simulate the
candidate policy to obtain a lower bound on achieved utility.

Novelty caveat: verification inequalities and delta-method intervals are
classical. The strength would be an end-to-end reliability package.

## Recommended order

1. Correct the proof-status record.
2. Derive and symbolically verify the general factor HJB and CRRA reduction.
3. Derive and verify the full-covariance state-dependent mechanism.
4. Introduce factor-only or log-wealth transitions.
5. Implement the exact two-factor OU/Riccati benchmark.
6. Cross-check value and derivative roots over a genuine 2D factor grid.
7. Extend moment recursion and adaptive proposals to the new kernel.
8. Scale the benchmark in factor dimension.
9. Add rectangular deep-branching training and held-out surface validation.
10. Recover controls and quantify policy uncertainty.
11. Treat partial information as the next benchmark.
12. Defer CIR/Heston boundaries and transaction-cost variational inequalities
    to separate projects.

## Literature boundary

The roadmap will cite primary sources for:

- Merton's continuous-time consumption/portfolio problem;
- Kim--Omberg predictable returns;
- Liu's quadratic-process and matrix-Riccati framework;
- Vasicek investment/consumption solutions;
- Gaussian partial-information portfolio choice;
- Heston/CIR and labor-income extensions;
- transaction-cost variational inequalities;
- branching-diffusion and arbitrary-jet coding-tree representations.

A negative search result will be written as:

> No source located in the scoped search combines these features.

It will not be written as:

> This is the first such result.

## Non-goals

- Claiming that many risky assets alone create a high-dimensional PDE.
- Claiming financial novelty for the classical CRRA reduction or Riccati
  benchmark.
- Calling a one-sample finite-value smoke test an unbiasedness validation.
- Calling a theorem fully formalized because related Lean lemmas compile.
- Treating finite-depth moment convergence as an unrestricted-tree upper
  bound without uniform-integrability or domination arguments.
- Starting with CIR, Heston, transaction costs, or non-Gaussian filtering.
- Modifying the user's current demo/solver work while writing the research
  record.

## Acceptance criteria

- Every existing theorem family appears in the registry.
- Every Lean theorem is named exactly and linked only to the substatement it
  proves.
- Every unformalized probability or domain obligation is explicit.
- The multidimensional Merton roadmap uses primary-source citations.
- The current Vasicek prototype is described accurately as implemented,
  smoke-tested, or unproved.
- At least three research routes are compared and the selected route is
  justified.
- Candidate contributions carry explicit prior-art caveats.
- The reader test finds no contradiction between the registry, roadmap,
  source proof notes, and Lean files.
