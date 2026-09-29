# Research: reliable branching-estimator algorithms

**Current scope, 26 September 2026:** this worktree owns branching Monte Carlo
and its mathematical theory. Improve branching Monte Carlo PDE
estimation through exponential-rate selection, tuple proposals, moment
control and verifiable approximation error. Algorithmic and mathematical
contributions are primary. Runtime measurements support practical claims;
they do not determine whether a theoretical question is worth studying.

Neural-network fitting, backbone comparison, operator learning and
latent/Fourier work now live in the sibling `parabolab-latent-fourier`
checkout on `research/nn-latent-fourier`. Keep MC data and interfaces usable
for that consumer, but do not develop the NN research line in this worktree.

The earlier certificate/profile work is on local `main`. The
[integration record](results/integration-2026-09-16.md) records the last
code/test/witness checks. For every documentation area and its status, use
[the repository documentation map](../documentation-map.md).

The [tuple-policy research run](runs/2026-09-16-certified-tuple-policy/07-report.md)
adds an exact flat-data second-moment explosion threshold, a 37.84% increase
in the rate-optimized horizon threshold, certified flat variance reductions,
and a strict wave improvement theorem. Its code and evidence are local
working-tree additions on the integrated baseline. The
[claim ledger](runs/2026-09-16-certified-tuple-policy/03-claims.md) separates
the conventional proofs, exact numerical checks and five Lean sublemmas.

The [long-horizon investigation](runs/2026-09-25-long-horizon/07-report.md)
extends this question beyond short times. Its exact raw-flat absolute-moment
ceiling is `(3*pi-2*log(3))/5`, independent of supported nonexplosive importance
proposals on the same expansion. A separately attributed bounded ternary
Allen–Cahn representation is the long-time comparator; its exponential tree
cost remains material. The [claim ledger](runs/2026-09-25-long-horizon/03-claims.md)
separates conventional probability/PDE arguments, eleven deterministic Lean
declarations, exact scalar checks and floating experiments. This does not
extend the raw-wave certificate or solve arbitrary fully nonlinear PDEs.

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
8. [Tuple-policy continuation](runs/2026-09-16-certified-tuple-policy/07-report.md):
   supported whole-tree improvement and the exact flat variance boundary.
9. [Long-horizon investigation](runs/2026-09-25-long-horizon/07-report.md):
   longer-time rate selection, the raw absolute-integrability ceiling, and
   bounded ternary sampling with nonconstant data through T=2.

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
| Tuple proposal | Full-tree policy-improvement theorem, exact nonuniform six-code certificates and safe nonzero wave update; at flat T=.5, lambda=1, p=.95 lowers variance by at least 53.42% versus uniform | Wave magnitude remains diagnostic; no certified joint optimizer or improvement over the terminal proxy; support alone does not prove integrability |
| Flat variance boundary | Exact threshold log(1+lambda² p C)/lambda; p=.95 versus .5 increases the rate-optimized threshold by sqrt(1.9) | Raw 1D Allen–Cahn, flat phi=.5, common first-label p; conventional proof and exact rational checks, not Lean formalization |
| Lean | 26 prior certificate/profile/cost public lemmas plus five new tuple-policy algebra/order lemmas, and two prior private helpers | Not a formal verification of the stochastic solver, Python verifier, explosion theorem or concrete witness values |

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
| Nonuniform tuple certificates and interval acceptance | [tuple_certificate.py](../../parabolab/tuple_certificate.py), [runnable example](../../examples/certified_tuple_policy.py) |
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
- Extend the proved safe wave tuple update to a materially larger certified
  gain on nonconstant data, at a common lambda and against the terminal proxy;
  retain support and recheck integrability. The latest run's wave sign is
  proved, while its estimated short-horizon effect is about 0.30% at lambda=.75.
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
