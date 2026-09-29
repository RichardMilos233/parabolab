# Fixed Lean contract: query lower-bound information core and transcript coupling

Theory prerequisite: root04o as integrated after T41; independent reviews
T40 and T41. User order remains theory -> Lean -> numerical checks. This
contract does not authorize changed mathematical assumptions to ease proofs.
No new numerical task starts before the primary formal targets pass.

## T42: actual probability-space finite-information inequality

Own only new formal/EstimatorIntegrity/QueryInformationLowerBound.lean,
06g-query-information-lean.md and lean/query-information/ logs. Use the pinned
project. Do not edit any existing module or entrypoint, toolchain or manifest.

Use an arbitrary probability space (Omega,mu) and a finite index type I.
Write K=card I. Let hit(omega) be a finite subset of I, Q:Omega->Real,
Hplus,Hminus:I->Omega->Real, and deterministic target arrays a,b:I->Real.
Let gamma>0 and epsilonSq>=0. Exact assumptions:

- Q is integrable, and card(hit(omega))<=Q(omega) pointwise.
- For every i, 2*gamma<=a_i-b_i.
- For every omega and i not in hit(omega), Hplus_i(omega)=Hminus_i(omega).
- Both actual squared-loss functions (Hplus_i-a_i)^2 and (Hminus_i-b_i)^2
  are integrable, and each has integral at most epsilonSq.

The primary theorem must DERIVE

    integral Q dmu >= K*(1-epsilonSq/gamma^2).

Do not replace this with a real-variable inequality that assumes its expected
coverage or loss bound. The finite averaging and measure integral are part
of the required target. No finite-support/probability-space specialization.
No bounded-output or unbiasedness hypothesis is required. Integrability of
the squared losses is legitimate and explicit, not an assumed conclusion.
The intended oracle MSE premise supplies it conventionally.

A clean route that avoids unnecessary hit-event measure hypotheses is to
prove the pointwise finite-family inequality first:

    sum_i[(Hplus_i-a_i)^2+(Hminus_i-b_i)^2]
      >=2*gamma^2*(K-card(hit(omega)))
      >=2*gamma^2*(K-Q(omega)),

then integrate the actual finite sum. Each loss is nonnegative on hit
indices; the common-output square identity bounds each no-hit pair. Since
hit itself is not integrated, the abstract theorem may omit measurability
of hit; this must be explicitly reported rather than silently treated as
an event-probability theorem. Q and all integrated losses keep the actual
integrability hypotheses. The usual measurable algorithm supplies more.

Add the exact corollary gamma=1/2, epsilonSq=1/16:

    integral Q dmu >=(3/4)*K.

Optional useful supporting lemmas: real paired-square bound, finite coverage
identity, or the general aggregate-MSE version. Do not substitute these for
the primary integral theorem. No floor/exp/PDE formalization is required
here, and no end-to-end Allen-Cahn certificate may be claimed.

## T43: actual deterministic adaptive oracle-transcript induction

Own only new formal/EstimatorIntegrity/OracleTranscript.lean,
06h-oracle-transcript-lean.md and lean/oracle-transcript/ logs. This task is
independent of T42; do not import or edit its unfinished module.

Define a small genuine adaptive point-query evaluator. Query points have an
arbitrary type X; oracle values and returned outputs may be Real. A policy
maps a finite history of queried (point,value) pairs to either a returned
output or the next query point. Fixing the private random seed selects one
such policy, so it need not explicitly draw randomness.

Use a natural-number query fuel and an Option return. A successful run
returns BOTH a real output and the ordered list of queried points. The
policy is allowed to stop without using any fuel; a requested query consumes
one unit, records the returned exact value in history, and recurses. Specify
whether history is reverse chronological; arbitrary policies may use it.

Primary theorem: if running the baseline oracle f with the policy and a
fixed initial history/fuel returns (y,trace), and another oracle g equals f
at EVERY point in that observed trace, then running g with the same initial
history/policy/fuel returns exactly (y,trace). Prove by induction through the
actual evaluator; do not assume transcript or output equality.

Derive the no-hit corollary: if f and g agree outside a forbidden set and
the baseline trace avoids that set, their output, trace and query count
agree. Two alternative oracles can be handled by two applications. Also
prove that for any finite cell-label map, the number of distinct visited
cell labels is at most trace.length. This supplies the finite coverage
budget used by T42.

This theorem quantifies over every fuel; it is compatible with a different
finite halting length for each random seed. It does not assume a single
uniform global query cap. The bridge from arbitrary measurable a.s.-halting
algorithms to this evaluator, and measurable integration of seed-indexed
runs, remains explicitly conventional unless actually encoded. A fully
operational infinite evaluator is not required. Do not claim to formalize
the PDE, heat minorization, smooth bumps or all abstract algorithms.

## Verification and delivery for both workers

Read Lean proof/elan skills as needed. First solve the primary target, then
supporting corollaries. Preserve failed compile logs and exact fixes. Require
a fresh lake build of the new module, source scan with no sorry/admit/custom
axiom, and #print axioms for every exported declaration. Preserve source,
build and axiom SHA256, actual toolchain/mathlib versions and commands.
Root will compare the encoded assumptions with this contract and the proof.
The source is one fixed scoped contribution; a green build does not complete
the PDE lower-bound proof in Lean or establish novelty.
