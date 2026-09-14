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

1. [Certified-rate checkpoint](results/certified-rate-checkpoint.md): verified
   flat and wave global excess bounds, moment/depth bounds, corrected
   binary oracle, replicated cost results, and exact Lean coverage.
2. [Sampling-method checkpoint](lambda-q-optimization-summary.md): the
   practical selector/proposal, solver integration, and earlier evidence.
3. [Moment model](estimator-integrity/notation-and-moment-theorem.md): the exact
   tree functional, code notation, killed-depth recursion, and integrability
   obligations.
4. [Rate optimization](estimator-integrity/exponential-rate-optimization.md):
   frozen-continuation versus full-tree objectives, strict convexity, a
   short-time approximation, and the standard binary-tree control.
5. [Tuple proposals](estimator-integrity/adaptive-proposals.md): the local
   square-root oracle, support requirements, and pilot/freeze reasoning.
6. [General rate selection](estimator-integrity/general-rate-selection.md):
   conditional full-tree existence, exact cutoff consistency, and explicit
   moment bounds for a specified semilinear class.

## Theory, implementation, and remaining work

| Area | Available now | Remaining work |
|---|---|---|
| Rate `lambda` | Conditional general theory and numerical selector; exact-rational global excess certificates for flat Allen–Cahn and the wave root at `T=0.05` | Extend verified scope across states/horizons and obtain useful rates across the evaluation grid |
| Tuple proposal `q_c(Z)` | Local square-root theorem; `TerminalTupleProposal` with a positive uniform mixture and exact inverse-probability weighting | Estimate continuation moments more accurately and establish an incremental benefit over rate tuning alone |
| PDE estimation/demo | Existing solver interface and replicated six-variant wave cost study; no demonstrated tuning gain for its one-profile predicted budget | Prespecified amortization and grid-objective studies against the short-time baseline |
| Integrability | Exact moment recursion, rational six-code Allen–Cahn envelopes and factorial depth tails, plus the Dym counterexample | Discharge remaining estimator-specific assumptions; nonuniform proposals and production roundoff remain separate |
| Formal verification | Sixteen checked public gap/field/convex-enclosure lemmas, plus two private helpers; full Lean build passed | Stochastic correspondence, analytic comparison/existence and numerical-program soundness |

The generic optimizer minimizes a numerical approximation of a **killed-depth
second moment on a supplied rate interval**. Its convergence flag does not
certify unrestricted variance or global accuracy. Exact killed-depth moments
increase to the full moment; quadrature adds a separate error. A
terminal-data proposal is a proxy for conditional continuation moments, not
their exact oracle.

The separate [rational certificate](estimator-integrity/allen-cahn-codewise-certificate.md)
now selects `1907/2560` for flat terminal value `1/2`, `T=1/20`, raw
one-dimensional semilinear trees and uniform tuple probabilities, with an
additive full-tree second-moment excess below `10^-4` over **all positive
rates**. This is an objective-gap bound, not a rate-error bound.

The separate [wave residual certificate](results/wave-rate-certificate.md)
now verifies global variance excess below `6.130773×10^-6` for the rounded
historical rate `0.73055` at `T=0.05,x=0`, raw uniform semilinear mechanism.
The sampled candidate `0.7375` has a smaller certified upper bound and
excess below `5.688312×10^-6`; overlapping moment intervals do not prove
it is actually better than `0.73055`. The result validates the full moment
equation directly, not the generic optimizer's quadrature-error tolerance.
The [conventional mean-identification proof](estimator-integrity/allen-cahn-mean-identification.md)
establishes the common PDE mean for every positive rate in the saved raw
uniform flat/wave settings, so the certified additive second-moment gaps
are also variance gaps. That stochastic correspondence is not Lean-formalized.

The moment evaluator computes deterministic integrals without sampling random
trees. It still needs a candidate rate: descendants' second moments generally
depend on the common `lambda`. The leaf contribution can be obtained directly
from terminal data and the diffusion law. See
[what the local coefficients mean](estimator-integrity/exponential-rate-optimization.md#where-the-local-coefficients-come-from).

Current implementation entry points:

- [moments.py](../../parabolab/moments.py): finite-depth 1D moment quadrature.
- [rate_optimization.py](../../parabolab/rate_optimization.py): recursive rate
  derivatives and constrained optimization.
- [rate_certificate.py](../../parabolab/rate_certificate.py): exact-rational
  six-code moment enclosures, depth tails and flat global rate certificates.
- [wave_certificate.py](../../parabolab/wave_certificate.py): exact polynomial
  residual/linear-error verification and convex wave-rate enclosures.
- [proposals.py](../../parabolab/proposals.py): terminal-data tuple proposal.
- [solve.py](../../parabolab/solve.py): the `CodingTreeMC` solver interface;
  custom tuple proposals currently require serial sampling (`n_jobs=1`).
- [sampling_tuning.py](../../examples/sampling_tuning.py): a bounded numerical
  diagnostic at one state, complementary to the solution-curve demos.
- [certified_allen_cahn_rate.py](../../examples/certified_allen_cahn_rate.py):
  generate or recheck the saved exact rational witnesses.
- [certified_wave_rate.py](../../examples/certified_wave_rate.py): generate or
  recheck the wave full-tree rate witnesses and independent diagnostics.
- [rate_cost_benchmark.py](../../examples/rate_cost_benchmark.py): the frozen,
  replicated cost protocol using the existing solver interface.

## Next checks

Extend the certificates while preserving their exact mechanism and
proposal scope. The [first replicated cost study](results/rate-cost-results.md)
completed all scheduled workloads and found the inexpensive short-time rate
strongest in its calibrated-budget phase. Keep that baseline in future
comparisons. Prespecify policy-reuse or larger workloads before testing
amortization, and investigate a grid-averaged objective rather than assuming
that a rate tuned at `x=0` is optimal across a profile. Any continuation-aware
proposal must establish incremental accuracy gains with its overhead included.
The offline rational certificate procedure was not a benchmark variant;
its roughly 30-second generation/checking/diagnostic run establishes no
practical amortized speedup.

Continue separating deterministic selection from evaluation randomness,
charging tuning cost, and recording actual runtime when allocating samples
from calibrated predicted budgets. These are estimator research checks,
not a new application direction.

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
