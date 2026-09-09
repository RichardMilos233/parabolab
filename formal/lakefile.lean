import Lake
open Lake DSL

package «estimator-integrity» where
  leanOptions := #[⟨`autoImplicit, false⟩]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.33.0"

@[default_target]
lean_lib EstimatorIntegrity
