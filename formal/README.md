# Lean verification

This directory formalizes selected deterministic mathematical statements
used by the branching-estimator research. The
[proof registry](../docs/research/proof-registry.md) is the authoritative
mapping between claims, exact declarations and omitted obligations.

## Build

Use the pinned [Lean toolchain](lean-toolchain) and
[Mathlib dependency](lake-manifest.json):

```sh
cd formal
lake build
```

The aggregate [EstimatorIntegrity.lean](EstimatorIntegrity.lean) imports
the proof modules. The latest recorded integrated build completed 3,391
jobs; see the [integration record](../docs/research/results/integration-2026-09-16.md).
Build counts are dated environment records, not mathematical claims.

## Coverage

| Modules | Encoded scope |
|---|---|
| `FiniteTree`, `MomentIteration` | Abstract finite-mechanism algebra and moment iteration |
| `Dym` | Coefficient and integral-divergence building blocks |
| `Proposal` | Finite proposal optimization and comparison inequalities |
| `ExponentialRate` | Rate-kernel positivity and model-objective algebra |
| `RateCertificate` | Conditional objective-gap transfer and coverage |
| `AllenCahnBounds` | Positive polynomial field and enclosure inequalities |
| `ConvexEnclosure` | Convex endpoint bounds, cells and exterior rays |
| `ProfileEfficiency` | Weighted objectives, interpolation, variance shifts and continuous cost algebra |

The recent certificate/profile checkpoints added 26 public lemmas and
two private helpers across the last four modules. That count is not the
number of declarations in the entire project. Their recorded axiom
audits use standard Lean axioms only; the registry records the details.

Passing the build checks the encoded statements under their assumptions.
It does not formalize the whole continuous-time random tree, its PDE
correspondence, analytical residual comparison, the Python verifier,
production roundoff, experimental confidence claims or historical novelty.
Do not call the complete solver formally verified on the basis of this build.

For the mathematical notes, runnable tools and current research priorities,
return to the [research guide](../docs/research/README.md).
