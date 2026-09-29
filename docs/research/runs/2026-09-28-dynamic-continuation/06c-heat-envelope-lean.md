# Lean gate for the Gaussian heat-envelope coefficient budget

Status: **passed** with Lean 4.33.0. The checked standalone module is
`formal/EstimatorIntegrity/HeatEnvelopeBudget.lean`. It contains no `sorry`,
`admit`, or custom axiom declarations, and no existing Lean module or
entrypoint was edited.

## Formalized statements

The module defines the audited real constants

```text
I0(d)       = 2 / (d - 2)
I1(d)       = 4 / ((d - 2) * (d - 4))
C(d)        = 2 + 16*d*I0(d)
Jstar(d,ε)  = 2*ε*I0(d) + 2*C(d)*ε^2*I1(d).
```

For a real dimension parameter `d ≥ 5`, Lean proves
`0 < I0 ≤ 2/3`, `0 < I1 ≤ 4/3`, `d/(d-2) ≤ 5/3`, and
`0 < C ≤ 166/3`. For `0 < ε ≤ 1/32`, it then proves

```text
0 ≤ Jstar ≤ 107/576 < 1/4.
```

The theorem `heatEnvelopeA_bounds` retains the Section 10 hypotheses
`0 ≤ j ≤ 1/4`, `0 ≤ h ≤ I0`, and `0 ≤ E ≤ 2`, together with the audited
definition

```text
a = ε^2 * (1 + C*j + 4*d*E*h).
```

It proves `0 ≤ a` and the exact two-step bound

```text
a ≤ 3*C*ε^2/4 ≤ C*ε^2.
```

Finally, `heatEnvelopeCoefficientBudget` also assumes `0 ≤ b` and
`δ^2 ≤ 4*ε^2*E` and proves, in the same theorem,

```text
C*ε^2*b + 4*d*ε^2*E ≥ a*b + d*δ^2,
2*C*ε^2 ≥ 2*a.
```

The proof of the first chain checks the exact identity
`1 + C/4 + 8*d*I0 = 3*C/4`. The remaining comparisons use multiplication
by the supplied nonnegative `b` and `d`; no mathematical hypothesis from
the reviewed target was weakened.

## Verification records

The fresh module build command

```text
~/.elan/bin/lake build EstimatorIntegrity.HeatEnvelopeBudget
```

completed successfully with all 3006 jobs built. Its output is saved in
`lean/heat-envelope/build.log`.

`lean/heat-envelope/HeatEnvelopeBudgetAxioms.lean` runs `#print axioms` for
all four definitions and every theorem in the module. The saved output in
`lean/heat-envelope/axioms.log` reports only Mathlib's standard foundational
axioms `propext`, `Classical.choice`, and `Quot.sound` for every declaration.
The one resolved development failure and its actual command are recorded in
`lean/heat-envelope/development.log`.

## Formalization boundary

This finite gate does not formalize the Gaussian heat kernel, the heat
Duhamel formula, supersolution domination of Picard or tree sums, likelihood
cancellation, absolute integrability, covariance, restart arguments, or
signed-PDE existence and uniqueness. Those conventional steps remain in the
reviewed theory.

The optional analytic substitution `E = exp (2*Jstar)` is outside this
module. In particular, this gate does not prove `exp (1/2) < 2` or exponential
monotonicity; Section 10 marked that extension optional, while the requested
finite coefficient inequalities are all checked here.
