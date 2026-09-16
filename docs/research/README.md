# Research: reliable branching-estimator algorithms

**Current scope, 16 September 2026:** improve branching Monte Carlo PDE
estimation through exponential-rate selection, tuple proposals, moment
control and verifiable approximation error. Algorithmic and mathematical
contributions are primary. Runtime measurements support practical claims;
they do not determine whether a theoretical question is worth studying.

The completed work is on local `main`. The
[integration record](results/integration-2026-09-16.md) records the last
code/test/witness checks. For every documentation area and its status, use
[the repository documentation map](../documentation-map.md).

## The central problem

For a fixed PDE, mechanism, tuple law, root code and starting state, choose
one positive exponential rate lambda for the whole tree to reduce its
variance. Full child moments depend on that same lambda; freezing them
solves a different local problem. The leading short-time formula is a
useful approximation, not a universal finite-horizon closed form.

A candidate is numerically useful only within the objective actually
computed. A finite-depth optimizer's convergence flag does not certify
the full tree. The current certification work instead constructs a valid
candidate upper bound and a lower bound on the global best objective,
then bounds their difference. Rate-invariant means transfer that
second-moment gap to a variance gap in the stated certified settings.

Choosing one rate shared by several starting points is an optional
weighted-objective extension. Those points are distinct PDE queries, not
child nodes inside one tree. It neither replaces the single-state problem
nor produces a rate that is individually optimal at every location.

## Reading order

1. [Moment model](estimator-integrity/notation-and-moment-theorem.md) and
   [rate optimization](estimator-integrity/exponential-rate-optimization.md):
   exact recursion, full-child rate dependence and short-time approximation.
2. [General selection guarantees](estimator-integrity/general-rate-selection.md):
   hypotheses for full-tree minimization, cutoff consistency and objective-gap bounds.
3. [Certified-rate checkpoint](results/certified-rate-checkpoint.md):
   implemented flat/wave guarantees and the corrected standard-binary control.
4. [Proof registry](proof-registry.md): claim-by-claim conventional proof,
   numerical evidence, Lean coverage and outstanding obligations.
5. [Sampling implementation guide](lambda-q-optimization-summary.md) and
   [proposal theory](estimator-integrity/adaptive-proposals.md): actual
   selector/proposal interfaces and what they approximate.
6. [Profile extension](results/profile-efficiency-checkpoint.md): one
   common rate for a prescribed weighted grid; its cost experiment is separate evidence.
7. [Directions and their disposition](future-directions-after-lambda.md):
   ten earlier research options, completed work and deferred alternatives.

The [theory index](estimator-integrity/README.md) and
[results index](results/README.md) give the complete collections and mark
which documents are frozen parts of numerical certificates.

## What is established and implemented

| Component | Available result | Boundary |
|---|---|---|
| Single-state numerical selection | Finite-depth quadrature and recursive rate derivatives, including child dependence | Bracket-constrained approximate objective; no generic full-tree convergence certificate |
| Flat Allen–Cahn certificate | At phi=1/2 and T=1/20, selected 1907/2560 has global additive variance excess below 1e-4 | Specified raw 1D mechanism and uniform tuples; not a tight relative-variance result |
| Wave-root certificate | At x=0,T=1/20, rounded historical rate 0.73055 has global additive excess below 6.130773e-6 | Separate rational residual verifier; does not certify the old quadrature algorithm |
| Weighted-profile certificate | At five equally weighted points, lambda=1/2 has relative variance excess below 0.93%; implemented short-time rule about 0.475 is within 1.60% | Bounds concern weighted variance, not error in lambda or every PDE value; actual grid candidates are not strictly ordered by the saved intervals |
| Tuple proposal | Support-preserving terminal proxy, inverse-probability weighting, and historical finite-depth Merton pilot tooling | Continuation-aware q has not been evaluated or certified for the current Allen–Cahn λ study; a support floor alone does not prove integrability |
| Lean | 26 public certificate/profile/cost lemmas across the two recent checkpoints, plus two private helpers | Not a formal verification of the stochastic solver, Python verifier or concrete witness values |

The wave candidate 0.7375 has a tighter saved excess bound than 0.73055;
overlapping point intervals do not prove it has smaller true variance.
The [mean-identification proof](estimator-integrity/allen-cahn-mean-identification.md)
closes the common-mean obligation for the saved raw uniform Allen–Cahn
certificates through conventional mathematics.

## Theory-to-code entry points

| Purpose | Code or runnable guide |
|---|---|
| Finite-depth moment evaluation | [moments.py](../../parabolab/moments.py) |
| Recursive derivatives and pointwise selection | [rate_optimization.py](../../parabolab/rate_optimization.py) |
| Shared-profile short-time rule and numerical selection | [profile_rates.py](../../parabolab/profile_rates.py) |
| Flat moment/gap and depth bounds | [rate_certificate.py](../../parabolab/rate_certificate.py) |
| Wave residual verification | [wave_certificate.py](../../parabolab/wave_certificate.py) |
| Exact profile coordinates, aggregation and policy interpolation | [profile_certificate.py](../../parabolab/profile_certificate.py) |
| Tuple proposals | [proposals.py](../../parabolab/proposals.py) |
| Solver workflow and diagnostic limits | [demo guide](../../demo/README.md), [solve.py](../../parabolab/solve.py) |
| Lean build and claim boundaries | [formal guide](../../formal/README.md) |

The solver workflow remains `Solver(**settings).solve(pde, grid) -> Curve`.
Rate selection is precomputation; production trees use the selected
settings. Custom tuple proposals currently require serial sampling.
Existing paper reproductions, network solvers and Merton examples retain
their roles as supported examples, not new certificate claims.

## Open algorithmic questions

- Make recursive optimization and its approximation error more systematic
  across horizons, states, mechanisms and nonlinearities.
- Extend useful full-tree moment and objective-gap guarantees beyond the
  saved cases; handle nonuniform proposals and numerical soundness explicitly.
- Test continuation-aware q for the current Allen–Cahn study at a common lambda before attributing an effect
  to joint tuning; retain support and recheck integrability.
- Evaluate representation changes, other lifetime laws or conditional
  expectation only as separately specified extensions.

The multi-point extension and the two cost studies are completed auxiliary
investigations. A low setup cost or a faster run is not, by itself, a new
algorithmic theorem; a slower implementation does not invalidate a theorem.
No additional research direction is being executed merely by listing it here.

## Historical and frozen material

Multifactor Merton is inactive as a research application. Its roadmap,
proofs and recorded checks are retained through the
[documentation map](../documentation-map.md), alongside archived design
plans and earlier diagnostic runs. Dym is a negative integrability
example, not a variance-reduction success benchmark.

Exact witness archives, raw runs and six hash-bound documents retain
their original bytes. Their dated pending-merge or historical environment
statements are superseded by the integration record and index status.
Later source changes mean historical hashes are not all current-source
hashes. Do not change the evidence to make a newer checkout match an old run.
