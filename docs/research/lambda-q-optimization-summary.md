# Research checkpoint: selecting the branching rate and tuple proposals

Date: 12 September 2026.

## Current decision, in plain language

The FYP remains about **reliably selecting the exponential branching rate
lambda**, with tuple probabilities `q_c` as a related variance-reduction tool.
Multidimensional Merton is **not** the chosen financial application. Dropping
that application does not mean abandoning branching Monte Carlo or starting an
American-option, execution, XVA, market-making, or neural-surrogate project.

Small rates make important branching events rare and heavily weighted, while
large rates can also create large weights and expensive trees. A finite variance
sweet spot exists under stated conditions, not for every PDE accepted by the
software.

**We do not have a universal plug-in formula returning the true optimal rate
for an arbitrary PDE.** A rate is attached to a particular estimator,
starting state, horizon, root code, and fixed proposal rule. Numerical
optimization and error control are still required in general.

The intended deliverable is a procedure that returns a useful rate and explains
how trustworthy that choice is. Aim for one defensible theorem and one
convincing application, rather than many unrelated extensions.

## What the formulas do and do not say

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
3. The selected rate and proposal can be passed to serial `estimate` or
   `sample_tree`. Existing defaults and the tree's random-draw order remain
   unchanged. Multiprocessing/high-level solver integration is not included
   in this checkpoint.

No expensive tuning takes place inside particle spawning. The proposal uses
only deterministic terminal evaluations; rate optimization is a separate
precomputation. Per-branch evaluation overhead may outweigh variance savings,
so runtime and variance must both be measured. The proposal must be held fixed
while taking rate derivatives; a callback that changes with lambda invalidates
those derivatives. Nonfinite parent-state terminal scores fail explicitly;
this proxy can therefore be inapplicable even when random leaf scores are
almost surely finite. A uniform-proposal moment bound does not transfer
unchanged: floor mass `epsilon` gives the conservative replacement `B/epsilon`.

See [the opt-in example](../../examples/sampling_tuning.py) for the executable
workflow and its explicitly labelled numerical limitations.

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

## Next two weeks and week-eight decision gate

During week one, reproduce only small optimizer checks, verify the exact
mechanism/proposal being optimized, and sharpen the scalar certificate using
code-dependent bounds. Test cutoff sensitivity and the effect of zero terminal
values; do not interpret finite sample variances as upper bounds.

During week two, compare default, rate-only, proposal-only, and combined tuning
on one controlled semilinear family. Use separate evaluation randomness, record
precomputation and sampling costs, and compare both fixed-sample variance and
fixed-budget accuracy. Choose one application only after its economic purpose
and estimator assumptions are established.

At week eight, proceed only if there is a precise theorem beyond a routine
prior-art restatement, a practically useful certificate or clearly delimited
failure result, and reproducible gains or informative limitations against
strong baselines. Otherwise narrow the estimator class or the certification
claim; do not compensate by adding unrelated financial models.

## Verification record

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
