# Lean finite gate

Status: **passed** with Lean 4.33.0.  The checked module is
`formal/EstimatorIntegrity/DynamicContinuation.lean`.  It contains no
`sorry`, `admit`, or custom axiom declarations.

## Formalized statements

The module proves the finite scalar gate used after the analytic and
probabilistic reductions.

* `dynamicRadicand_le_square` proves, for nonnegative `r,b,s` and
  `0 ≤ t ≤ 1`, that `r ≤ b+s` implies
  `t²r²+(1-t²)s² ≤ (tb+s)²`.  The surplus is the nonnegative term
  `2t(1-t)bs`.
* `dynamicRmsStep_invariant` uses monotonicity of the real square root to
  prove
  `sqrt(t²r²+(1-t²)s²)+(1-t)b ≤ b+s`.
* `finiteDynamicRmsRecurrence` proves by induction that every finite member
  of a nonnegative sequence satisfying that one-step bound is at most
  `b+s`, provided the initial member is.
* `finiteDynamicRmsRecurrence_of_parameters` exposes the continuation
  notation explicitly: `q=t²`, `nu=(1-t²)s²`, and `beta=(1-t)b`.  It proves
  the all-finite-index consequence from
  `r(j+1) ≤ sqrt(q*r(j)²+nu)+beta`.

The exact rational certificates also check:

* `mu*h=(31/350)*(2/25)=31/4375`;
* `(3/7)*(1+2*(2/21)/35)<1/2`, the affine-interface derivative envelope;
* `(2/21)^5/160000<(1/140000)^2`, the squared interpolation defect bound;
* the rational values `x/(1+x)=31/4406` and
  `2x/(1+2x)=62/4437` at `x=31/4375`;
* `4406/4340000 + sqrt(4437/12400000) < 1/50`.

The last theorem is strict: Lean checks positivity of
`41197/2170000` and the exact squared comparison
`4437/12400000 < (41197/2170000)^2` before applying square-root
monotonicity.

## Verification records

The saved build record is in `lean/build.log`.  The command

```text
~/.elan/bin/lake build EstimatorIntegrity.DynamicContinuation
```

completed successfully with all 3006 jobs built.  The audit source
`lean/DynamicContinuationAxioms.lean` runs `#print axioms` for every theorem
in the new module; its output is saved in `lean/axioms.log`.  Every theorem
depends only on Mathlib's standard foundational axioms `propext`,
`Classical.choice`, and `Quot.sound`.

## Formalization boundary

This gate does **not** formalize the Jacobi elliptic identities, period and
zero structure, the odd-sector spectral factorization, or the derivation of
the contraction rate `mu=31/350`.  It takes the resulting finite constant as
input.

It does not formalize existence, uniqueness, smoothing, symmetry
preservation, comparison, endpoint regularity, or the degenerate maximum
principles for the transformed Allen--Cahn PDE.  In particular, invariance of
the bounds on `R`, `R_z`, and `R_zz` remains the conventional argument in
`04-theory.md` and review `T01-order-interface.md`.

It also does not formalize the Bernstein interpolation theorem, the
Hilbert-space orthogonal projection, existence and nonexpansiveness of the
metric projection onto the coefficient polygon, the Gram-coordinate
quadratic program, or numerical projection error.

No probability spaces, conditional expectations, unbiased coefficient
estimator, variance trace, Minkowski step, local branching-tree
representation, second-moment bound, or population interpretation are
encoded.  Those arguments are what produce the scalar recurrence supplied
to the gate; the Lean theorem proves only its deterministic finite-index
consequence.

The analytic inequality `1-exp(-x) ≥ x/(1+x)` is likewise outside this
module.  Lean checks the exact rational substitutions that follow from it,
not the real-exponential inequality itself.  The result is an ensemble RMS
bound at fixed grid endpoints, not a pathwise, simultaneous-time, or
high-probability statement.

Finally, the formal budget is a correctness certificate for the proposed
continuation recurrence.  It is not a competitiveness theorem: on this
restricted benchmark the simple midpoint baseline described in the theory
note is already below `0.02` in normalized spatial RMS.
