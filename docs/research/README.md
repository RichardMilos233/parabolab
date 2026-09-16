# Research: reducing branching-estimator variance

Current direction, 16 September 2026: improve the estimation of nonlinear PDE
solutions using branching Monte Carlo. Choosing the exponential clock rate
`lambda` and the tuple probabilities `q_c(Z)` are algorithmic choices within
that solver. The PDE-solving purpose and the existing demo workflow remain
the same.

The completed certificate and profile-selection work is integrated into
local `main`, with user authorization confirmed on 16 September 2026.
See the [integration record](results/integration-2026-09-16.md). Current
research prioritizes algorithms, recursive moment control and mathematical
guarantees; measured setup/runtime comparisons are supporting evidence.

The demos continue to solve one PDE with several methods, collect solution
curves, and compare them with the available reference solution. Default,
rate-only, proposal-only, and combined sampling can be compared as variants
of `CodingTreeMC` in that workflow. See the [demo guide](../../demo/README.md)
and [variance-reduction demo](../../demo/variance_reduction.py).

## Start here

1. [Profile-efficiency checkpoint](results/profile-efficiency-checkpoint.md):
   certified grid objective, cheap-rate headroom, completed setup/reuse study,
   conditional expected-MSE comparisons and ten additional Lean lemmas.
2. [Certified-rate checkpoint](results/certified-rate-checkpoint.md): verified
   flat and wave global excess bounds, moment/depth bounds, corrected
   binary oracle, replicated cost results, and exact Lean coverage.
3. [Sampling-method checkpoint](lambda-q-optimization-summary.md): the
   practical selector/proposal, solver integration, and earlier evidence.
4. [Moment model](estimator-integrity/notation-and-moment-theorem.md): the exact
   tree functional, code notation, killed-depth recursion, and integrability
   obligations.
5. [Rate optimization](estimator-integrity/exponential-rate-optimization.md):
   frozen-continuation versus full-tree objectives, strict convexity, a
   short-time approximation, and the standard binary-tree control.
6. [Tuple proposals](estimator-integrity/adaptive-proposals.md): the local
   square-root oracle, support requirements, and pilot/freeze reasoning.
7. [General rate selection](estimator-integrity/general-rate-selection.md):
   conditional full-tree existence, exact cutoff consistency, and explicit
   moment bounds for a specified semilinear class.

## Theory, implementation, and remaining work

| Area | Available now | Remaining work |
|---|---|---|
| Rate `lambda` | Exact-rational global excess certificates for flat Allen–Cahn, the wave root and the five-point wave profile at `T=0.05`; cheap profile rate within 1.60% of optimal weighted variance | Transfer to other horizons or mechanisms requires new bounds |
| Tuple proposal `q_c(Z)` | Local square-root theorem; `TerminalTupleProposal` with a positive uniform mixture and exact inverse-probability weighting | Estimate continuation moments more accurately and establish an incremental benefit over rate tuning alone |
| PDE estimation/demo | Existing solver interface; two replicated cost studies, including one/ten-request reuse; cheap grid rate wins the latest frozen expected-MSE allocation comparison | Assess continuation proposals through variance reduction, integrability and approximation guarantees; report runtime separately |
| Integrability | Exact moment recursion, rational six-code Allen–Cahn envelopes and factorial depth tails, plus the Dym counterexample | Discharge remaining estimator-specific assumptions; nonuniform proposals and production roundoff remain separate |
| Formal verification | Twenty-six checked public certificate/profile/cost lemmas across the two research checkpoints, plus two private helpers; full Lean build passed | Stochastic correspondence, analytic comparison/existence and numerical-program soundness |

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

The [profile certificate](results/profile-efficiency-checkpoint.md) extends
this argument to equal weights on `[-2,-1,0,1,2]`. The rational candidate
`lambda=1/2` has global weighted-variance excess below `3.848558e-5`, or
0.93% relative to the optimum. The actual cheap grid policy
`0.47496956016576375` is within 1.60%; exact convex interpolation covers its
binary-float rate. The numerical grid selector's small possible variance
gain did not repay setup in the completed one/ten-request comparisons.

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
- [profile_rates.py](../../parabolab/profile_rates.py): cheap weighted
  short-time rate and a weighted finite-depth numerical selector.
- [profile_certificate.py](../../parabolab/profile_certificate.py): exact
  spatial intervals, weighted global bounds and policy-rate interpolation.
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
- [certified_profile_rate.py](../../examples/certified_profile_rate.py):
  recheck profile witnesses and frozen-allocation expected-MSE bounds.
- [profile_efficiency_benchmark.py](../../examples/profile_efficiency_benchmark.py):
  completed grid-objective and setup-reuse protocol.

## Next checks

The completed work is integrated into `main`. The main mathematical result
is a computable full-tree objective-gap guarantee; the grid selector is a
weighted extension of the single-point objective. Selecting one common
rate for a profile is optional when the research question concerns a
single starting state.

Further algorithmic work can address recursive rate optimization,
systematic approximation-error control, broader certificate scope and
continuation-aware tuple proposals. The cheap grid rule has at most 1.60%
relative variance excess in this specific profile and provides a useful
baseline. The [cost study](results/profile-efficiency-results.md) is an
auxiliary practical result; its measured tuning overhead is not a reason
to close these mathematical questions. Any later speedup claim still
requires complete cost accounting. Offline rational certification was
not a timed benchmark variant.

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
Hash-bound derivations and experiment records retain their original dated
status text; the integration record supersedes their old merge status
without changing the evidence or claiming that later code has old hashes.

Multidimensional/multifactor Merton is **inactive as a research application**.
Its [roadmap](multifactor-merton-roadmap.md),
[proofs](multifactor-merton-proofs.md), and
[financial milestone](milestone-1-financial-moment-target.md) remain in place
for provenance, together with the milestone check script and captured
outputs. Their application-specific implementation plans are superseded.
Existing Merton demos and library examples remain available as PDE examples.
