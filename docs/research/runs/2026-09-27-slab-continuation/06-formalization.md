# Lean formalization

Date: 2026-09-27. The checked module is
`formal/EstimatorIntegrity/SlabContinuation.lean`, built with Lean and mathlib
4.33.0. The commands and exact outputs are saved under `lean/`.

## Checked statements

The module proves the following deterministic algebraic claims.

- The six-coordinate Allen–Cahn branch polynomial uses the existing exact
  definition
  `G(i,d,a,b,c,e)=(a,bd,2ab+d²c/2,2ac+d²e/2,2ae,0)`.
- For
  `B=(2/5,1/2,2/5,1,12/5,6)` and
  `V=(1/4,1/2,1/2,3,12,50)`, every coordinate satisfies
  `(21/16) B² + G(V)/21 < V`. The weak postfixed inequality is also exposed
  as a separate theorem.
- Projection of a real number onto `[-a,a]` does not increase its absolute
  error relative to any target `z` with `|z|≤a`. This is derived from the
  library theorem that interval projection is 1-Lipschitz.
- If `e 0=0`, `ρ≥1`, `v≥0`, and
  `e (j+1)≤ρ e j+v`, then
  `e n≤n ρ^n v` for every finite `n`.
- The three coefficient caps sum to `4661/20000`, their frequency-weighted
  sum is `957/4000`, and the exact value and derivative envelope inequalities
  hold.
- The periodic stability exponent calculation is exactly
  `1-(20/21)(76/77)²=8989/124509<3/40`.
- The finite-horizon amplification check
  `50(250/247)^50<100` and normalized spatial `L²` MSE budget
  `100((3/4)/200000+(1/100000000)^2)<(1/50)^2` hold over the rationals.

All theorem declarations are free of `sorry` and `admit`. The saved
`#print axioms` audit reports only `propext`, `Classical.choice`, and
`Quot.sound`, with no project-specific axiom.

## Formalization boundary

This module certifies rational supersolution algebra, interval projection,
the finite scalar recurrence, and the displayed finite rational budgets. It
does not identify `G` with stochastic moments, prove an ODE comparison or
nonexplosion theorem, establish a PDE representation, or certify a numerical
implementation.

The finite-product perturbation and geometric leaf-absorption arguments from
the conventional theory are not included in this Lean module. They therefore
must not be cited as machine-checked results of this run.

## Reproduction

From `formal/` run:

```text
~/.elan/bin/lake build EstimatorIntegrity.SlabContinuation
~/.elan/bin/lake env lean ../docs/research/runs/2026-09-27-slab-continuation/lean/PrintSlabContinuationAxioms.lean
```

The module build completed successfully as target 3007/3007. See
`lean/build.log`, `lean/axioms.log`, and `lean/toolchain.txt` for the captured
outputs and hashes.
