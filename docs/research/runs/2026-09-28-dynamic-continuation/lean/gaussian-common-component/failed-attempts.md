# Development-failure provenance

This file distinguishes directly captured failures from a retrospective
summary of interactive compiler diagnostics. Final verification commands are
captured independently in the successful final logs.

## Directly retained raw failures

- `explore-01.log` exited 1. Almost all API queries succeeded; two speculative
  names, `iIndepFun.indepFun₀` and `iIndepFun.pairwise_indepFun`, did not exist
  in the pinned Mathlib. The available `iIndepFun.indepFun` API was used.
- `prototype-02.log` exited 125 because the first capture invocation supplied
  the Lake executable as the working-directory argument. The capture command
  itself accurately records that invocation error.
- `prototype-03.log` exited 1 and directly retains the first prototype's Lean
  diagnostics. Unused measure arguments had been omitted from inferred
  definition signatures, so several calls supplied one argument too many; one
  pair-map extensionality goal was also still open.

## Retrospective interactive diagnostics

- Initial continuous-linear-map proofs depended too much on simplifier
  unfolding. They were replaced by explicit function equalities before
  transporting `HasGaussianLaw`, without changing any probability statement.
- The initial residual-variance expansion left a ring-normalization goal. The
  final proof names the actual covariance and closes only the resulting scalar
  ring identity.
- The first edge covariance collapse lacked a local `DecidableEq E` for the
  diagonal split. A local classical instance supplies the finite proof device;
  no decidable-equality premise was added to the public theorem.
- Early edge wrapper calls timed out during implicit argument unification. The
  final proofs first give the derived row-covariance fact its complete type and
  pass that named fact to the common-component theorems.

Every failure was a Lean elaboration or pinned-API issue. No mathematical
assumption, degeneracy, covariance identity, independence conclusion, or
target measure was weakened.
