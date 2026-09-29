# Retained failed attempts

The final proof was developed by incremental Lean checks. The material failures were:

1. The first radius-induction attempt used the unavailable identifiers `mul_le_mul_left'` and `mul_le_mul_right'`, and supplied a measurable-composition argument to `lintegral_mul_const` without enough parentheses. It was replaced by the pinned API's `mul_le_mul_left`/`mul_le_mul_right` orientations and an explicitly typed `lintegral_mul_const` invocation.
2. A following `gcongr` attempt did not descend through the ENNReal multiplication in the needed orientation. Explicit monotonicity lemmas closed those goals.
3. The first `lake build` exposed that the library sets `autoImplicit := false`, unlike the direct incremental invocation. The type `S` had been left implicit in the private helpers `branchResult`, `measurable_branchResult`, `weight_branchResult`, `chooseBranch`, and `measurableSet_chooseBranch`. Explicit `{S : Type*}` binders fixed the issue. The complete failed build is retained in `failed-build-autoImplicit.log`.

After these fixes, the fresh library-module build and both audit files exited successfully. No failed attempt introduced a mathematical assumption or changed the fixed law.
