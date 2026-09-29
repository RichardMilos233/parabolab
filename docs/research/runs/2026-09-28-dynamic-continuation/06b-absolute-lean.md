# Lean gate for the absolute-moment ODE obstruction

Status: **passed** with Lean 4.33.0.  The checked module is
`formal/EstimatorIntegrity/AbsoluteMomentObstruction.lean`.  It contains no
`sorry`, `admit`, or custom axiom declarations.

## Formalized result

`scaledRiccati_time_lt_pi_div_two` states the finite closed-interval barrier.
For real `T,a,b`, a real-valued function `z`, `0 ≤ T`, `0<a`, `0<b`, and

```text
z(0) = 0,
z'(t) = a * (1 + (b*z(t))^2)  for every t in [0,T],
```

in the pointwise `HasDerivAt` sense, Lean proves

```text
a*b*T < pi/2.
```

The proof differentiates `F(t)=arctan(b*z(t))`.  The derivative simplifies
exactly to `a*b` because `1+(b*z(t))^2` is strictly positive.  Mathlib's
right-derivative mean-value theorem then proves
`arctan(b*z(t))=a*b*t` throughout `[0,T]`; the strict range theorem
`arctan(x)<pi/2` gives the endpoint bound.  The argument includes `T=0` and
does not require a sign assumption on `z`.

`riccati_time_lt_pi_div_two` specializes the scaled theorem to `a=b=1`:
if `z(0)=0` and `z'(t)=1+z(t)^2` throughout `[0,T]`, then `T<pi/2`.

## Verification records

The fresh build command

```text
~/.elan/bin/lake build EstimatorIntegrity.AbsoluteMomentObstruction
```

completed successfully with all 2199 jobs built.  Its output is saved in
`lean/absolute-obstruction/build.log`.

`lean/absolute-obstruction/AbsoluteMomentObstructionAxioms.lean` runs
`#print axioms` for both new theorems.  The saved output in
`lean/absolute-obstruction/axioms.log` shows only Mathlib's standard
foundational axioms `propext`, `Classical.choice`, and `Quot.sound`.

## Formalization boundary

This module proves a deterministic finite-time ODE obstruction.  It does not
formalize the heat semigroup, strict heat-kernel positivity on a connected
torus, the positive constants `eta_0` and `eta_p`, or their compactness
argument.

It does not encode branching trees, supported completing proposal laws,
likelihood cancellation, Tonelli or monotone-convergence arguments, canonical
absolute moments, finite positive Picard iterates, or comparison of those
moments with the finite derivative chain.  It also does not prove the
reduction from that chain to the scaled Riccati equation, including the
square-root parameter substitution for the `p=2` case.

Consequently the Lean result does not by itself prove that a sampled tree
functional has infinite absolute moment.  The conventional arguments in
`04c-general-obstruction.md` and `reviews/T10-polynomial-obstruction.md` must
first produce a real function satisfying the stated Riccati derivative
hypotheses.  Nor does the module claim global PDE existence, estimator/PDE
correspondence, a sharp explosion time for the full moment system, or the
analytic all-horizon classification.

Within that boundary, there is no mismatch between the reviewed mathematical
lemma and its Lean statement: the scaled and normalized closed-interval
barriers are encoded directly with the same hypotheses and strict conclusion.
