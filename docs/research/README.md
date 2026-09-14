# Research: reducing branching-estimator variance

Current direction, 14 September 2026: improve the estimation of nonlinear PDE
solutions using branching Monte Carlo. Choosing the exponential clock rate
`lambda` and the tuple probabilities `q_c(Z)` are algorithmic choices within
that solver. The PDE-solving purpose and the existing demo workflow remain
the same.

The demos continue to solve one PDE with several methods, collect solution
curves, and compare them with the available reference solution. Default,
rate-only, proposal-only, and combined sampling can be compared as variants
of `CodingTreeMC` in that workflow. See the [demo guide](../../demo/README.md)
and [variance-reduction demo](../../demo/variance_reduction.py).

## Start here

1. [Current checkpoint](lambda-q-optimization-summary.md): decisions, practical
   algorithm, evidence, limitations, and next experiments.
2. [Moment model](estimator-integrity/notation-and-moment-theorem.md): the exact
   tree functional, code notation, killed-depth recursion, and integrability
   obligations.
3. [Rate optimization](estimator-integrity/exponential-rate-optimization.md):
   frozen-continuation versus full-tree objectives, strict convexity, a
   short-time approximation, and the standard binary-tree control.
4. [Tuple proposals](estimator-integrity/adaptive-proposals.md): the local
   square-root oracle, support requirements, and pilot/freeze reasoning.
5. [General rate selection](estimator-integrity/general-rate-selection.md):
   conditional full-tree existence, exact cutoff consistency, and explicit
   moment bounds for a specified semilinear class.

## Theory, implementation, and remaining work

| Area | Available now | Remaining work |
|---|---|---|
| Rate `lambda` | Strict-convexity and existence results under stated assumptions; 1D deterministic moment derivatives and safeguarded Newton/bisection | Useful bounds on omitted tree depths and quadrature error; rates that remain effective across the evaluation grid |
| Tuple proposal `q_c(Z)` | Local square-root theorem; `TerminalTupleProposal` with a positive uniform mixture and exact inverse-probability weighting | Estimate continuation moments more accurately and establish an incremental benefit over rate tuning alone |
| PDE estimation/demo | Existing solver/curve/comparison interface; opt-in serial `CodingTreeMC` variants | Replicated comparisons of solution error, empirical variance, and total computational cost |
| Integrability | Exact moment recursion and class-specific sufficient bounds; the Dym counterexample | Discharge assumptions for each estimator/application being evaluated |

The current optimizer minimizes a numerical approximation of a **killed-depth
second moment on a supplied rate interval**. Its convergence flag does not
certify unrestricted variance or global accuracy. Exact killed-depth moments
increase to the full moment; quadrature adds a separate error. A
terminal-data proposal is a proxy for conditional continuation moments, not
their exact oracle.

The moment evaluator computes deterministic integrals without sampling random
trees. It still needs a candidate rate: descendants' second moments generally
depend on the common `lambda`. The leaf contribution can be obtained directly
from terminal data and the diffusion law. See
[what the local coefficients mean](estimator-integrity/exponential-rate-optimization.md#where-the-local-coefficients-come-from).

Current implementation entry points:

- [moments.py](../../parabolab/moments.py): finite-depth 1D moment quadrature.
- [rate_optimization.py](../../parabolab/rate_optimization.py): recursive rate
  derivatives and constrained optimization.
- [proposals.py](../../parabolab/proposals.py): terminal-data tuple proposal.
- [solve.py](../../parabolab/solve.py): the `CodingTreeMC` solver interface;
  custom tuple proposals currently require serial sampling (`n_jobs=1`).
- [sampling_tuning.py](../../examples/sampling_tuning.py): a bounded numerical
  diagnostic at one state, complementary to the solution-curve demos.

## Next checks

Keep the PDE, mechanism, horizon, evaluation grid, and reference solution fixed
when comparing default, rate-only, proposal-only, and combined sampling. Fit
sampling choices before evaluation and use separate evaluation randomness.
Report tuning cost as well as sampling cost; compare both variance at a fixed
sample count and accuracy at a fixed total budget. Check sensitivity to the
rate interval, moment depth, and time/space quadrature before interpreting an
optimized rate. These checks are part of estimator evaluation, not a new
application direction.

## Proof records and historical work

The [proof registry](proof-registry.md) tracks exact claim boundaries and Lean
coverage. The [estimator-integrity ledger](estimator-integrity/reproducibility.md)
and the checkpoint's [captured tuning record](sampling-tuning-check.json)
describe particular historical runs; they are not current-environment or
end-to-end speedup certificates. [Secondary candidates](estimator-integrity/secondary-candidates.md)
are retained as research ideas, outside the current implementation plan.

Multidimensional/multifactor Merton is **inactive as a research application**.
Its [roadmap](multifactor-merton-roadmap.md),
[proofs](multifactor-merton-proofs.md), and
[financial milestone](milestone-1-financial-moment-target.md) remain in place
for provenance, together with the milestone check script and captured
outputs. Their application-specific implementation plans are superseded.
Existing Merton demos and library examples remain available as PDE examples.
