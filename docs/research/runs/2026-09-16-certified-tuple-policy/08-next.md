# Checkpoint and next decisive experiment

## Completed investigation

The bounded continuation of direction 3 is complete. [C1–C8](03-claims.md)
have conventional proofs or explicit counterexamples, independent review,
and the scoped numerical/formal evidence described in [the report](07-report.md).
No claim of a complete Lean verification or worldwide novelty is made.

- The whole-tree policy-improvement theorem and interval gate handle the
  dependence of all descendants on the changed policy.
- The raw-flat moment system reduces to one reciprocal-cubic integral,
  giving the exact explosion threshold and the sqrt(p) law for its
  rate-optimized horizon. At T=.5, lambda=.75, changing p=.5 to .95 moves
  from infinite to finite variance with the same mean.
- At T=.5, lambda=1, the same flat change reduces variance by at least
  53.42%, using exact rational moment and mean-square bounds.
- A nonzero F1 wave update is strictly beneficial through T=.05 at
  lambda=.75 and 1, globally in finite x. Its diagnostic center gains are
  small; no rigorous percentage was derived.
- All 38 stored nonuniform witnesses, both wave gates and the scalar
  threshold calculation verified. Python: 263 passed, 14 slow tests
  deselected. Lean: five new algebra/order lemmas, full build and standard
  axiom audit passed. [Evidence and commands](05-numerics.md).

The initial and post-result ten-direction scorecards are separate artifacts.
Only D03 is promoted above the strict 1000 threshold, on the basis of the
proved change in the flat finite-variance regime.

## Retained failures and limits

Fourteen failed box searches remain recorded: the separate C8 theorem
explains the two flat uniform failures, while twelve wave failures remain
inconclusive. The wave F3 diagnostic initially failed an absolute tolerance;
the later scale-aware criterion and actual error are disclosed in the
numerical report. No numerical failure was silently discarded.

The scalar explosion theorem, wave semigroup comparison, common-mean
identification, stochastic-to-ODE correspondence and rational-program
soundness are outside the five new Lean declarations. These are explicit
coverage gaps, not tool blockers. Floating sampler probabilities also have
a different roundoff scope from exact rational policies. The flat candidate
already equals the terminal proxy at floor_mass=.1, so it does not establish
an improvement over that proxy. No joint optimizer was implemented.

## Next action

**Target:** obtain a quantitatively certified gain on nonconstant data over
the existing terminal proxy, at a common fixed rate. First determine whether
the small current wave effect is a limitation of the uniform ratio bound
or of the actual continuation oracle.

**Research owner:** derive conditional old-policy tuple contributions using
the actual callback information (birth position and sampled lifetime,
before the shared Brownian displacement). Use `04-theory.md` C1/C2/C7 and
the existing wave residual certificate as inputs. Start with T=.05,
lambda=.75, then freeze any horizon extension before evaluation. Construct
spatial/time-dependent interval contributions and apply the sign-aware
gate; prove coverage between grid points and in the spatial tails.

**Implementation owner, after the mathematical contract is fixed:** implement
an independently checked table and frozen callback. Compare uniform,
terminal proxy, the current static safe policy and the new table at the
same rate. Do not turn unvalidated finite differences into acceptance bounds.

**Acceptance condition:** a nonvacuous exact root variance-decrease bound
relative to the terminal proxy, with common means, positive support, all
reachable-state coverage and all setup costs stated. Record a quantitative
failure if the safe gate is too conservative or the oracle gain is small;
do not substitute an empirical sign or a changed rate. A 10% decrease is
a useful predeclared practical target, not an established result.

**Checks to rerun after affected source changes:** relevant gate/sampler and
certificate tests, exact witness verification, independent mathematical
correspondence review, the full Python regression suite if production code
changes, and Lean module/import build plus axiom audit for changed formal
statements. Preserve this run's evidence; create a new dated continuation
or versioned artifacts. A separate formalization task can mechanize C8's
scalar transform and blow-up comparison before attempting the stochastic
bridge. Nothing is scheduled to run in the background.
