# Research checkpoint: selecting the branching rate and tuple proposals

Initial checkpoint: 12 September 2026. Direction and integration updated:
14 September 2026. [Research navigation](README.md).

## Current decision, in plain language

The FYP remains about **improving branching Monte Carlo estimation of nonlinear
PDE solutions**. Selecting the exponential branching rate `lambda` and tuple
probabilities `q_c(Z)` are ways to reduce estimator variance within that
direction. Multidimensional Merton is **inactive as a research application**;
its records and existing PDE examples are retained.

The demo workflow remains one PDE, several solver/algorithm variants, and
solution curves compared with a reference through `solve` and `compare`.
Sampling variants belong inside that workflow; the one-state research checks
supplement it. See [the demo guide](../../demo/README.md) and
[the variance-reduction demo](../../demo/variance_reduction.py).

Small rates make important branching events rare and heavily weighted, while
large rates can also create large weights and expensive trees. A finite variance
sweet spot exists under stated conditions, not for every PDE accepted by the
software.

**We do not have a universal plug-in formula returning the true optimal rate
for an arbitrary PDE.** A rate is attached to a particular estimator,
starting state, horizon, root code, and fixed proposal rule. Numerical
optimization and error control are still required in general.

The intended deliverable is a procedure that chooses useful sampling rules,
explains how trustworthy those choices are, and measures their effect on PDE
estimation accuracy and cost. The current rate selector and proposal proxy
are the first implementations of that procedure.

## What the formulas do and do not say

The local rate objective writes
`J_exp(lambda) = A_0 exp(lambda Delta) + integral A(s) exp(lambda s) ds / lambda`.
For the identity root, `A_0 = P_Delta(phi^2)(x)` depends only on terminal data
and the diffusion law. It can be evaluated without a branching simulation or
a chosen clock rate. By contrast, `A(s)` contains child second moments:
when all nodes use the rate being optimized, it is **`A_lambda(s)`**.
Holding it fixed means changing only the root clock while freezing the
continuation sampling rules. The global-rate optimizer must differentiate
the descendants too. The [rate note](estimator-integrity/exponential-rate-optimization.md#where-the-local-coefficients-come-from)
gives the precise definitions.

Continuation moments can be obtained without simulating random trees by
solving deterministic moment equations. Outside special closed-form models,
this still requires evaluating those equations for candidate rates. The
current 1D implementation approximates them by finite-depth quadrature; strict
convexity supplies uniqueness under its hypotheses, not free coefficients or
a universal closed-form optimal rate.

For the identity-root coding tree, a short-horizon starting approximation is

$$
\lambda_{\rm start}(x)\approx
\frac{|f(J\phi(x))|}{|\phi(x)|}.
$$

Here `J phi` means the terminal value and the derivatives used by the PDE.
The formula requires nonzero numerator and denominator and suitable uniform
short-time moment/derivative expansions. It is not an arbitrary-horizon
formula or a proof of integrability. At an Allen--Cahn terminal value of
`0.5`, it gives `|0.5 - 0.5^3| / 0.5 = 0.75`.

For a fixed tuple decision, if the true conditional continuation second moments
satisfy `0 < A_Z < infinity` for every live alternative, the exact local oracle is

$$
q_c^*(Z)=\frac{\sqrt{A_Z}}{\sum_{Z'}\sqrt{A_{Z'}}}.
$$

Those continuation moments are generally unknown. Pilots or terminal-data
proxies approximate them. A positive uniform mixture preserves support;
the sampler must use the actual inverse selection probability `1/q_c(Z)`.
For the unrestricted estimator, this preserves the mean only when the tree
functional is absolutely integrable. Exact zero contributions require separate
support handling; if all contributions vanish, the displayed ratio is undefined.
This does not establish joint global optimality of lambda and every `q_c`,
nor does it repair infinite absolute moments.

## Evidence inventory

- The existing [moment theorem](estimator-integrity/notation-and-moment-theorem.md)
  identifies exact absolute moments through killed-depth exhaustion. Its
  finite-depth moments are **lower approximations**, not upper certificates.
- The existing [rate note](estimator-integrity/exponential-rate-optimization.md)
  proves local strict convexity, gives a conditional full-tree topology
  argument, a conditional full-recursive short-time law, and an exact
  **standard binary-tree** Riccati oracle. That binary oracle is not the same
  estimator as the derivative-coded representation of the same PDE.
- The [proposal note](estimator-integrity/adaptive-proposals.md) supplies the
  classical square-root optimizer and support/integrability conditions for
  pilot-frozen proposals. Pilot standard errors are not certified tail bounds.
- The [Dym obstruction](estimator-integrity/dym-nonintegrability.md) proves
  non-integrability of the specified real-extension estimator. An apparently
  good finite-sample rate does not create a finite variance optimum there.
- The new [general rate-selection note](estimator-integrity/general-rate-selection.md)
  records the class-wide development: full-tree minimizer existence, exact
  cutoff-minimizer consistency, an explicit all-code tilted-moment bound for a
  semilinear class, and a quantitative rate-selection error inequality.
- These new arguments are **ordinary mathematical proofs under their written
  hypotheses**, independently reviewed by GPT-6 Astra MAX. They are not newly
  Lean-checked stochastic theorems or a completed certified numerical solver.
- The previous [financial milestone](milestone-1-financial-moment-target.md)
  and its symbolic-check artifacts are retained as historical work. Its
  recommendation to proceed with multifactor Merton has been superseded.

## Engineering application in this checkpoint

The implementation is deliberately opt-in and reuses the existing sampler:

1. `TerminalTupleProposal` uses the **parent-birth state**, available before
   the tuple draw, to form the local score `prod_z |g_z(x)|`. It applies the
   square-root rule to terminal-product squared proxies, with a strictly
   positive uniform mixture. All-zero proxy scores fall back to uniform.
   This is a cheap heuristic, not the true conditional-moment oracle.
2. `optimize_exponential_rate_1d` accepts the same fixed proposal and mechanism
   used by the moment evaluator and production sampler. It minimizes a
   **quadrature approximation of a killed-depth second moment on a supplied
   bracket**. Its convergence flag is not a certificate for the unrestricted
   estimator or for rates outside that bracket.
3. The selected rate and proposal can be passed to serial `estimate`,
   `sample_tree`, or `CodingTreeMC(..., rate=..., tuple_proposal=..., label=...)`.
   The high-level solver returns the same solution curves used by `compare`.
   Custom proposals require `n_jobs=1`; multiprocessing and neural training
   do not yet accept this opt-in proposal. Existing sampling defaults remain
   unchanged.

No expensive tuning takes place inside particle spawning. The proposal uses
only deterministic terminal evaluations; rate optimization is a separate
precomputation. Per-branch evaluation overhead may outweigh variance savings,
so runtime and variance must both be measured. The proposal must be held fixed
while taking rate derivatives; a callback that changes with lambda invalidates
those derivatives. Nonfinite parent-state terminal scores fail explicitly;
this proxy can therefore be inapplicable even when random leaf scores are
almost surely finite. A uniform-proposal moment bound does not transfer
unchanged: floor mass `epsilon` gives the conservative replacement `B/epsilon`.

See [the opt-in example](../../examples/sampling_tuning.py) for the one-state
diagnostic and [the demo](../../demo/variance_reduction.py) for the existing
PDE solution-curve workflow with sampling variants.

## Prior-work and novelty boundary

General importance-sampling convexity and adaptation are not new:
[Ryu--Boyd](https://stanford.edu/~boyd/papers/adaMC.html) and
[Badouraly Kassim--Lelong--Loumrhari](https://arxiv.org/abs/1307.2218) are close
precedents. Their exponential/Poisson likelihood calculations are especially
relevant to rate optimization and sample reuse.
[Huang--Privault stability v2](https://arxiv.org/html/2502.17853v2), revised
9 March 2026, provides substantial weighted-progeny integrability results for
a related but different coding mechanism. Scalar ODE majorants are established
branching tools; see [Henry-Labordere et al.](https://arxiv.org/abs/1603.01727).

The candidate research increment is **useful, explicit certificates for actual
recursive coding-tree rate selection**, not the existence of a U-shaped plot,
the square-root rule, generic convex optimization, or a universal best lambda.
Publication novelty remains unestablished.

## Next research checks

First reproduce small optimizer checks, verify the exact mechanism/proposal
being optimized, and sharpen the scalar certificate using
code-dependent bounds. Test cutoff sensitivity and the effect of zero terminal
values; do not interpret finite sample variances as upper bounds.

Then compare default, rate-only, proposal-only, and combined tuning
on one controlled semilinear family using the existing demo workflow. Use
separate evaluation randomness, record precomputation and sampling costs,
and compare both fixed-sample variance and
fixed-budget accuracy across the solution grid. A rate selected at one state
is not automatically optimal at every state. Establish estimator assumptions
before making variance or confidence-interval claims for a chosen PDE.

For the research contribution, require a precise theorem beyond a routine
prior-art restatement, a practically useful certificate or clearly delimited
failure result, and reproducible gains or informative limitations against
strong baselines. Otherwise narrow the estimator class or the certification
claim; do not compensate by adding unrelated financial models.

## Repository integration check: 14 September 2026

The solver/demo integration preserves the existing PDE and comparison
interfaces. `CodingTreeMC` forwards an optional tuple proposal to the serial
sampler, and all four solvers accept custom curve labels. Existing Merton
demos remain available; the multifactor research roadmap is marked inactive.

Validation used the existing `parabolab` environment from the repository root:

```bash
python -m pytest -q
MPLBACKEND=Agg python demo/variance_reduction.py
MPLBACKEND=Agg python demo/dym.py
```

- The default Python suite passed **197 tests**, with **14 slow tests
  deselected**, in 46.98 seconds. The focused solver suite passed 32 tests,
  including same-seed equivalence with direct nonuniform-proposal sampling.
- `lake build` from `formal/` completed successfully with the existing pinned
  toolchain and dependencies. This verifies the written Lean statements;
  formal coverage has not expanded in this integration.
- Both demos completed and saved their figures. The variance demo retained
  the standard solution-curve comparison; its generated figure was inspected.
  Dym output is labelled as a non-integrability diagnostic.
- Local link targets in the current entry-point documents and rate note
  were checked, and `git diff --check` passed.

The variance demo used `T=0.05`, 21 grid points on `[-2, 2]`, 10,000 samples
per point, and seed 0 for each variant. Depth-2, order-4 quadrature selected
rates 0.73055 (uniform tuples) and 0.73049 (terminal proxy) at `x=0`, within
`[0.2, 2.0]`. The mean empirical sample variances over the grid were:

| Configuration | Mean empirical variance |
|---|---:|
| Rate 1, uniform tuples | 0.00745281 |
| Selected rate, uniform tuples | 0.00474964 |
| Rate 1, terminal proxy | 0.00739695 |
| Selected rate, terminal proxy | 0.00458153 |

These are one-seed diagnostics, not certified population variances or
replicated performance claims. Rate selection used deterministic quadrature,
not the evaluation samples. Setup and both rate searches took 0.34 seconds
in this run; sampling times are printed separately by the comparison table.

## Historical verification record: 12 September 2026

The counts and timings below belong to the original one-state checkpoint;
they do not include the later high-level solver/demo integration.

Implementation and execution used GPT-5.6 Sol HIGH; GPT-6 Astra MAX specified
and reviewed the mathematics. All commands ran from the repository root in
the existing `parabolab` conda environment. No dependencies were installed,
no slow experiment was launched, and no Lean build was repeated.

```bash
conda run --no-capture-output -n parabolab python -m pytest tests/test_sampling_tuning.py -q
conda run --no-capture-output -n parabolab python examples/sampling_tuning.py
conda run --no-capture-output -n parabolab python -m pytest -m 'not slow' -q
```

The focused suite passed **28 tests**; the full non-slow suite passed **195
tests, with 14 deselected**, in 44.85 seconds. These tests ran in the existing
working tree, including the user's preserved, unrelated solver edits. The
new tests cover support floors, zero and nonfinite scores, duplicate labels,
large finite products, deterministic callbacks, matching proposal/mechanism
forwarding, and an exact two-alternative moment/optimizer control. The first
focused run exposed an incorrect test expectation that omitted the uniform
floor; correcting that expectation required no change to the formula.

Recorded versions: Python **3.11.15**, NumPy **2.4.6**, SymPy **1.14.0**,
pytest **9.0.3**. The example finished in 2.10 seconds wall time, including
environment/startup overhead. It used the nonconstant one-dimensional
Allen--Cahn wave at `T=0.05`, `(t,x)=(0,0)`, with **2,000 unrestricted trees
per configuration**. Tuning used killed depth 2, time/normal quadrature order
4, rate bracket `[0.2,2]`, and proposal floor mass `0.1`.

Evaluation streams were independently spawned from
`numpy.random.SeedSequence(20260912)`, with spawn keys `(0,)`, `(1,)`, `(2,)`,
and `(3,)` in the table's order. To reconstruct a stream, pass
`SeedSequence(20260912, spawn_key=(i,))` to `default_rng`; the example's
generated uint64 seed-state fingerprint is not an interchangeable integer
seed. No evaluation sample was used to fit either tuning rule.
The [captured numerical record](sampling-tuning-check.json) retains full
reported precision and documents the seed-label correction.

| Configuration | Selected lambda | Empirical variance | Mean nodes | Variance × mean nodes | Sampling seconds | Diagnostic/tuning seconds |
|---|---:|---:|---:|---:|---:|---:|
| Default rate, uniform tuples | 1 | 0.004181661 | 1.0535 | 0.004405380 | 0.003905 | 0.009307 |
| Rate only | 0.730548630 | 0.003291932 | 1.0430 | 0.003433485 | 0.002982 | 0.055575 |
| Proposal only | 1 | 0.004079722 | 1.0525 | 0.004293908 | 0.003595 | 0.007774 |
| Combined | 0.730485368 | 0.003112481 | 1.0390 | 0.003233868 | 0.002791 | 0.070876 |

The exact solution is `-0.5187412159`. Empirical means and standard errors,
in the same order, were `-0.5192225512 +/- 0.0014459704`,
`-0.5175267481 +/- 0.0012829521`, `-0.5177081179 +/- 0.0014282371`, and
`-0.5210005537 +/- 0.0012474938`. The rate-only and combined optimizers
reported convergence for their constrained numerical objectives, with
second moments `0.2723171267` and `0.2723162567`, respectively.

The combined run showed approximately **26% lower empirical variance** than
the default, but this is one small independent-seed comparison, not a
statistically established improvement. It does not isolate the proposal's
incremental benefit. Millisecond sampling timings are particularly noisy.
The fixed-rate configurations' diagnostic time is optional moment evaluation,
not required baseline tuning. At this batch size the rate-optimization cost
exceeds the observed sampling-time saving, so **no end-to-end speedup is
demonstrated**. Larger amortized workloads and replicated fixed-budget tests
remain future work. Empirical standard errors and finite-depth numerical
moments are not upper certificates for the unrestricted estimator.
