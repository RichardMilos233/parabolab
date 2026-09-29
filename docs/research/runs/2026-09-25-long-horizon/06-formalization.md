# Long-horizon Lean formalization

Status: complete for the fixed deterministic scope. The two source modules
build on the pinned Lean/mathlib environment, are imported by
`formal/EstimatorIntegrity.lean`, and contain no `sorry` or `admit`.

## Exact declarations

`formal/EstimatorIntegrity/LongHorizonAlgebra.lean` provides:

- `longHorizonPolynomial`: the polynomial
  `3/8 + s/4 + 3*s^2/2 + s^3`.
- `longHorizonPolynomial_factorization`: the identity
  `P(s) = (s + 3/2) * (s^2 + 1/4)`.
- `longHorizonPolynomial_pos`: strict positivity of `P` for `s >= 0`.
- `rawAbsoluteHorizon`: the exact real number
  `(3*pi - 2*log 3)/5`. This is a definition, not a formal improper-integral
  evaluation.
- `longHorizonPolynomial_reciprocal`: the partial-fraction identity
  `1/P(s) = (2/5)/(s+3/2) + ((-2/5)*s+3/5)/(s^2+1/4)` for `s >= 0`.
- `boundedReaction`: the symmetric rule
  `B_r(a,b,c)=((r+1)/(3r))*(a+b+c)-abc/r`.
- `boundedReaction_diagonal`: for `r > 0`,
  `r*(B_r(u,u,u)-u)=u-u^3`.
- `boundedReaction_corner_le_one_iff`: for `r > 0`, the sharp corner
  condition `B_r(1,1,-1) <= 1` is equivalent to `2 <= r`.
- `boundedReaction_two`: `B_2(a,b,c)=(a+b+c-abc)/2`.
- `boundedReaction_convex_decomposition`: for nonzero `r`,
  `B_r=(2/r)B_2+(1-2/r)(a+b+c)/3`.

`formal/EstimatorIntegrity/LongHorizon.lean` provides:

- `boundedReaction_two_mem_Icc`: `B_2` maps `[-1,1]^3` into `[-1,1]`.
- `ternaryAverage_mem_Icc`: the ternary arithmetic mean preserves the same
  interval.
- `boundedReaction_mem_Icc`: every `B_r` with `r >= 2` maps the cube into the
  interval, using the displayed convex decomposition and weights in `[0,1]`.
- `BoundedTernaryTree`: finite full ternary trees.
- `BoundedTernaryTree.eval`: evaluation with bounded leaves and `B_r` at each
  internal node.
- `BoundedTernaryTree.eval_mem_Icc`: every finite evaluation remains in
  `[-1,1]` for `r >= 2`, proved by structural induction. The rate-two result
  is the specialization `r=2`.

## Verification

The fresh standalone source checks, named-module builds, aggregate import
check and aggregate build all exited zero. The aggregate build completed 3,394
Lake dependency jobs; this is not a count of new declarations. Exact commands
and outputs are in [build.log](lean/build.log). The pinned environment is Lean
4.33.0 and mathlib revision
`db584cd6d46c92f209a44c0f1c829460d327499d`; source hashes are in
[toolchain.log](lean/toolchain.log).

`LongHorizonAxioms.lean` runs `#print axioms` on all eleven theorem
declarations. Every result depends only on the standard axioms `propext`,
`Classical.choice` and `Quot.sound`; none uses `sorryAx` or a new project
axiom. The exact output is in [axioms.log](lean/axioms.log).

## Coverage boundary

Lean does not prove that the raw coding-tree absolute moment obeys the scalar
ODE, identify killed-depth limits, cancel adaptive proposal densities, prove
random-tree nonexplosion, or evaluate the improper integral whose conventional
value is `rawAbsoluteHorizon`. It also does not prove the bounded random-tree
mean/PDE correspondence, conditional independence, continuous-time tree
completion, PDE uniqueness/comparison, variance monotonicity, or expected node
count. Those are the conventional stochastic and analytic arguments in
[04-theory.md](04-theory.md), not consequences silently attributed to this
deterministic Lean build.
