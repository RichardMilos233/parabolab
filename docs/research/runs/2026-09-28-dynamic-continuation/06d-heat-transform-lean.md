# Lean gate for normalized products and finite heat-transform work

Status: **passed** with Lean 4.33.0. The checked standalone module is
`formal/EstimatorIntegrity/HeatTransformWork.lean`. It contains no `sorry`,
`admit`, or custom axiom declarations, and no existing module or entrypoint
was edited.

## LT17.1: bounded normalized products

`abs_scalar_mul_list_prod_le_one` proves that for a finite list of real
numbers whose entries have absolute value at most one, and a real prefactor
whose absolute value is at most one,

```text
|σ * z.prod| ≤ 1.
```

The list induction includes the empty product. The separate terminal lemma
`abs_div_le_one_of_abs_le` proves
`0 < h ∧ |g| ≤ h → |g/h| ≤ 1`.

## LT17.2: simultaneous finite-depth work invariant

`heatTransformWork_fixedPoint` checks all four exact substitutions for

```text
K = (220/3, 56, 20, 56).
```

`finiteHeatTransformWorkInvariant` takes four real sequences `A,B,D,I`.
It retains the fixed assumptions that every entry is nonnegative, each
initial entry is nonnegative and at most one, and every natural index obeys

```text
A(n+1) ≤ 1 + (A(n)+B(n))/4 + 2*D(n)
B(n+1) ≤ 1 + 3*A(n)/4
D(n+1) ≤ 1 + (B(n)+D(n))/4
I(n+1) ≤ 1 + 3*A(n)/4.
```

A simultaneous natural-number induction proves, at every finite depth,

```text
A(n) ≤ 220/3,  B(n) ≤ 56,  D(n) ≤ 20,  I(n) ≤ 56.
```

No finiteness or expectation hypothesis about an untruncated tree appears in
the theorem. `finiteHeatTransformTotalRootWork_le` then proves the requested
finite arithmetic corollary: `R(n) ≤ 2*I(n)` together with `I(n) ≤ 56`
implies `R(n) ≤ 112`.

## Optional scalar recurrences

The optional LT17.3 is also checked. For nonnegative real entries, a
nonnegative `η ≤ 1/48`, `M(0) ≤ 1`, and

```text
M(n+1) ≤ 1 + 2*η*M(n),
```

`finiteScalarBaselineWorkInvariant` proves `M(n) ≤ 24/23` at every finite
depth. The separately requested matched-Gaussian specialization uses the
same recurrence with `η ≤ 1/96` and proves the sharper `M(n) ≤ 48/47`.

## Verification records

The fresh command

```text
~/.elan/bin/lake build EstimatorIntegrity.HeatTransformWork
```

completed successfully with all 3006 jobs built. Its output is saved in
`lean/heat-transform-work/build.log`.

`lean/heat-transform-work/HeatTransformWorkAxioms.lean` runs
`#print axioms` for every declaration in the module. The saved output in
`lean/heat-transform-work/axioms.log` reports only Mathlib's standard
foundational axioms `propext`, `Classical.choice`, and `Quot.sound` for all
seven declarations. Resolved direct-check failures and warnings are recorded
in `lean/heat-transform-work/development.log`.

## Formalization boundary

This module does not formalize the heat-transform kernel, its probability
law, clock or branch identities, conditional independence, expectations,
monotone convergence, almost-sure tree completion, the PDE bridge, uniqueness,
or floating-clock implementation error. The product and recurrence theorems
are finite deterministic gates and do not by themselves certify the ideal
sampler or an executable implementation.
