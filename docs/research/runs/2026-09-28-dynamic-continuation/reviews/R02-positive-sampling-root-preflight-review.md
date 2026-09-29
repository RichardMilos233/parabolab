# R02: root self-check of the draft positive-query protocol

Status: root self-review of its own02f draft. This does not replace T58's
independent review and does not authorize implementation or execution.
T58's worker stopped with a workspace-credit error before producing a
report. No random samples or new PDE/numerical evidence were generated here.

The conventional one-dimensional height/mass constant C=3/2 follows from
using the constant reproducing kernel and the Lipschitz remainder. For
eta=1/64 the mixing cutoff L=1 is valid: log512<2*pi^2 (for example pi>3
and e>2 suffice). The draft's later displayed list of coarse inequalities
should include this lower bound on pi if it is meant to be exhaustive.
The three entries of m0 are each greater than or equal to1/504, and
kappa>1/4. The resulting threshold1+log16128 is less than12, since
e>8/3 and (8/3)^11>16128. The E3 lower-bound T0 is not used.

The sample-budget formulas give these exact integer schedules, checked by
ordinary deterministic arithmetic at the draft's fixed horizons:

    T12: 51, 202, 807, 38730; fixed schedule51.
    T16: 373, 1491, 5962, 286172; fixed schedule51.
    T20: 2754, 11014, 44053, 2114541; fixed schedule51.

The count is180cells,18720outputs and336883488 charged point queries,
below500000000. This is a design/accounting calculation, not an experiment.
The estimator count is independent of the unknown nominal transition level;
zero-input calls are still charged. The three small growing constants and
fixed51 do not satisfy the universal D24 budget.

The proposed empirical RMS interval follows from an exact deterministic
PDE bias bound and the finite-vector triangle inequality. Its numerical
display uses a quadrature-derived scalar reference. The old two quadratures
are not rigorous enclosures, so a displayed floating interval must never
be described as a machine-certified enclosure of actual PDE error. An
appropriate label is a numerically evaluated interpretation of the
conventional bias theorem. This qualification already appears in02f and
must survive code, figure captions and summaries.

The profile's stored binary width must define its reference mass, including
when it differs from the nominal exp(-T) scaling. Periodic shifts do not
change mass, but binary64 oracle evaluation is still an approximation to
an ideal smooth real datum. Underflow observations and pseudorandom streams
are not formal implementations of the real-probability theorem.

Before any official run, a future accepted protocol/manifest must include
all diagnostic points and tolerances, exact seed-key ordering, accumulation
method, stored-width/reference construction, and failure persistence. The
source reviewer must confirm that the sampler accesses only returned point
values and never the support width or driver reference. No early zero-data
exit or conditional rare-event generation is justified. These are pending
implementation details, not passed checks.
