# Formal scope and executed checks

Five declarations in `formal/EstimatorIntegrity/TuplePolicy.lean` were built and imported through `formal/EstimatorIntegrity.lean`:

- `EstimatorIntegrity.binary_policy_improvement`: real A,B>=0, 1/2<=q<1 and q(A+B)<=A imply A/q+B/(1-q)<=2(A+B).
- `EstimatorIntegrity.robust_binary_policy_improvement`: lower/upper bounds a<=A, B<=b transfer the analogous endpoint certificate to the true binary objective.
- `EstimatorIntegrity.two_thirds_policy_improvement`: A>=2B with nonnegative A,B implies safety of q=2/3.
- `EstimatorIntegrity.prefixed_policy_bounds_iterates`: every iterate from bottom of a monotone map stays below a prefixed point in a complete lattice.
- `EstimatorIntegrity.policy_improvement_iSup`: if F(v)=v and G(v)<=F(v) for monotone G, the supremum of zero/bottom-seeded G iterates lies below v.

The first three verify C2/C7's finite acceptance algebra; the last two verify C1's abstract order step. They do not assume that an arbitrary moment function is a fixed point: that identification is an explicit conventional stochastic obligation in C1.

Toolchain: `leanprover/lean4:v4.33.0`; mathlib tag v4.33.0, manifest revision `db584cd6d46c92f209a44c0f1c829460d327499d`. Implementation task T03 ran:

```sh
cd formal
/Users/michael/.elan/bin/lake env lean EstimatorIntegrity/TuplePolicy.lean
/Users/michael/.elan/bin/lake build EstimatorIntegrity.TuplePolicy
/Users/michael/.elan/bin/lake env lean EstimatorIntegrity.lean
/Users/michael/.elan/bin/lake build EstimatorIntegrity
/Users/michael/.elan/bin/lake env lean /Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-16-certified-tuple-policy/lean/TuplePolicyAxioms.lean
```

All exited 0. The full build completed 3,392 jobs; these are Lake's dependency-job count, not 3,392 new theorems. See [build.log](lean/build.log).

The axiom audit uses `#print axioms` for every new declaration. Algebra declarations depend only on `propext`, `Classical.choice`, `Quot.sound`; order declarations only `propext`, `Quot.sound`. No `sorryAx`, `sorry`, `admit` or new project axiom supports a claimed result. See [axioms.log](lean/axioms.log) and the actual audit source.

## Correspondence limits

The complete lattice is abstract; Lean does not identify its iterates with continuous-time killed trees or prove nonexplosion, conditional independence, semigroup bounds, PDE uniqueness, or common means. It does not formalize C4's joint topology-integral convexity, C5's nonuniform six-code reduction, the C7 wave dominance argument, C8's scalar reduction/explosion time, or the optimized-horizon corollary. It also does not verify Python rational arithmetic programs, generated concrete values, floating production probabilities, ODE diagnostics or publication novelty. These omissions are coverage boundaries, not failed declarations hidden by a clean build.

Semantic review: real q is the first probability of a binary normalized row `(q,1-q)`. The domain excludes 0 and 1. The robust theorem bounds actual contributions before changing descendants; the separate order theorem handles descendant changes. The wave 2/3 statement needs the conventional all-state ratio inequality before it applies. No stochastic assumption was weakened to complete Lean.
