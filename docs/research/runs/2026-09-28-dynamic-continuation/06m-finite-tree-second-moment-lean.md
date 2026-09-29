# T75: finite-tree second moments in Lean

Date: 2026-09-29

## Result

The fixed T75 statement is implemented in
`formal/EstimatorIntegrity/FiniteTreeSecondMoment.lean`. The module builds with
Lean 4.33.0 and Mathlib commit
`db584cd6d46c92f209a44c0f1c829460d327499d`.

The implementation constructs the actual finite-depth Markov laws and derives
their ENNReal moment recurrence. It does not introduce a scalar recurrence as
an assumption. The state type is an arbitrary measurable space `S`.

## Actual law

`Output` is `ℝ × ℕ`. The public kernels are:

- `childTriple K`: three product-kernel copies of `K`, each read at the same
  state in `(omega,r)`. Product kernels give conditional independence.
- `branchKernel branch K`: first samples the correlated pair `(omega,r)` from
  `branch(s)`, samples the child triple conditionally at that single `r`, and
  maps the result to
  `(6 * omega * c₁ * c₂ * c₃, n₁+n₂+n₃)`.
- `sourceKernel leaf`: maps `l` to `((6/5)*l,1)`.
- `stepKernel leaf branch K`: uses the actual Bernoulli law
  `Ber(true,false,1/6)`, choosing the branch law on `true` and source law on
  `false`.
- `treeKernel leaf branch 0`: the deterministic killed output `(0,0)`;
  `treeKernel leaf branch (D+1)` is the preceding step applied to depth `D`.

The module proves `IsMarkovKernel` for every component and every depth. No
independence of `omega` and `r` is assumed: they remain one sample from the
supplied branch kernel. Only the three children are conditionally independent
after that pair is sampled.

## Derived recurrence and radius bound

The weight is represented as

```text
coeffSq(c) * ofReal(a^2*z)^n,
```

which is the ENNReal form of `c² a^(2n) z^n`. The product-law, map, composition,
and Bernoulli lintegrals are evaluated in separate lemmas. Their combination is
the public theorem `weightedMoment_succ`:

```text
F_(D+1)(s)
  = (6/5) ofReal(a^2*z) integral l^2 d leaf(s)
    + 6 integral omega^2 F_D(r)^3 d branch(s).
```

Thus the factors are exactly `1/q=6/5` and `1/p=6`. The proof of the branch
identity retains the joint `(omega,r)` integral.

For `M>0`, `R>0`, `C>=0`, `C*R²<=1/8`, and the two actual uniform lintegral
bounds, `weightedMoment_uniform_bound` proves

```text
F_D(s) <= ofReal(R²)
```

for every natural depth `D` and every state `s`, with
`a=3R/(4M)` and `z=5/4`. In the induction, the uniform child bound is applied
before integrating `omega²`; hence coefficient/state correlation causes no
factorization assumption. The source contribution is `27R²/32`, the branch
contribution is at most `3R²/32`, and their sum is at most `R²`.

`weightedMoment_ne_top` records actual finiteness. The real algebraic corollary
`squaredMajorant_slope_bound` proves

```text
3 * (C²/(1/6)) * (R²)² <= 9/32.
```

## Polynomial leaf moments

For every `j : ℕ`, the module defines exactly

```text
A_j = sum n, n^(2j) (4/5)^n
```

as the real `leafPolynomialConstant j`. It proves summability using
`summable_pow_mul_geometric_of_norm_lt_one`, nonnegativity, finiteness after
embedding in ENNReal, and the pointwise inequality

```text
n^(2j) <= A_j (5/4)^n.
```

`polynomialMoment` is the actual lintegral of
`n^(2j) c² a^(2n)` against `treeKernel`. The general public theorem
`polynomialMoment_le_weightedMoment` converts any nonnegative pointwise
geometric envelope into an integral bound. Instantiating it with the proved
`A_j` inequality and the finite-depth radius theorem gives

```text
polynomialMoment leaf branch j D (3R/(4M)) s
  <= ofReal(A_j) * ofReal(R²)
```

uniformly in `D,s`; `polynomialMoment_ne_top` states its finiteness explicitly.
This `A_j` is deliberately larger than T69's supremum-based constant. The
sharper maximum formula is not claimed here.

## Verification

The fresh library-module command

```text
~/.elan/bin/lake build EstimatorIntegrity.FiniteTreeSecondMoment
```

completed successfully. The build emitted only Mathlib style-linter suggestions
about using `let` rather than `letI` for proof-valued instances. There are no
compiler errors or trust warnings in the successful log.

`Axioms.lean` runs `#print axioms` on every public theorem. Every result contains
only the ordinary Mathlib axioms `propext`, `Classical.choice`, and `Quot.sound`.
There is no `sorryAx`, custom axiom, `admit`, or native-check trust dependency.
`Declarations.lean` and `declarations.log` retain the exact public signatures and
quantifiers. A text scan of the source for `sorry`, `admit`, `axiom`,
`native_decide`, and `unsafe` is empty.

Evidence is in
`docs/research/runs/2026-09-28-dynamic-continuation/lean/finite-tree-second-moment/`:

- `build.log`: successful fresh module build;
- `Axioms.lean` and `axioms.log`: complete public-theorem axiom audit;
- `Declarations.lean` and `declarations.log`: exact declaration inventory;
- `trust-scan.log`: empty forbidden-token scan result;
- `environment.md`: pinned toolchain, Mathlib revision, and commands;
- `failed-attempts.md` and `failed-build-autoImplicit.log`: retained material
  failed attempts;
- `SHA256SUMS`: final source, report, and evidence-log hashes.

Only the new module, this report, and its evidence directory were written. The
project entrypoint, toolchain, lake configuration, dependencies, earlier
modules, frozen sources/proofs, and root ledgers were not edited.

## Exact coverage boundary

Covered here:

- arbitrary measurable state space;
- actual source, correlated coefficient/state branch, conditionally independent
  child-triple, Bernoulli-mixture, and finite-depth Markov kernels;
- derived ENNReal recurrence;
- uniform finite-depth weighted second moments and finiteness;
- the `9/32` squared-majorant slope;
- every fixed polynomial leaf-count moment using the summable `A_j`.

Outside this module: infinite genealogical coupling; almost-sure halting and
expected node count; concrete heat/time kernels and primitive costs; graph/PDE
identification; derivative label-map sampling; inner burn-in batches; query and
runtime caps; the final Taylor risk and work theorem; finite-bit implementation;
and numerical performance. No full T69 sampler or signed long-time algorithm is
certified by this partial finite-depth result.
