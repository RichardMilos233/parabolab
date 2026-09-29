# T86: actual uniform-slice conditioning in Lean

Date: 2026-09-29

## Result

The fixed 05l contract is implemented in
`formal/EstimatorIntegrity/UniformSliceConditioning.lean`. The module builds
under Lean 4.33.0 and Mathlib commit
`db584cd6d46c92f209a44c0f1c829460d327499d`.

The implementation starts from the actual PMF
`PMF.uniformOfFinset (U.powersetCard h)`, forms the actual normalized
restriction to the revealed-sign event, proves the resulting compatible law,
then pushes that measure through an actual membership bit. No urn probability
formula is assumed.

## Actual prior, event, and conditional law

`sliceFamily U h` is `U.powersetCard h`, and `uniformSlice U h hh` is the
associated PMF measure. The proof `hh : h <= U.card` supplies nonemptiness.
`uniformSlice_singleton` exports the exact atomic law: a member of the slice has
mass `choose(U.card,h)^{-1}`, while a subset outside the slice has mass zero.

For disjoint `P,N` contained in `U`, `compatibleFamily U h P N` is the original
slice filtered by `P subset A` and `Disjoint A N`. The module proves that this
is the same family as the `h`-subsets of `U \ N` containing `P`, and derives

```text
card compatibleFamily
  = choose (U.card - (P.card + N.card)) (h - P.card).
```

`uniformSlice_compatibleEvent` turns this count into the exact prior event
mass `choose(m,r)/choose(K,h)`, and
`uniformSlice_compatibleEvent_pos` proves the denominator for conditioning is
positive from the two feasibility inequalities. `conditionedSlice` is the
actual Mathlib normalized restriction. The theorem
`conditionedSlice_eq_uniformCompatible` proves, by singleton normalization,
that this restriction equals the uniform PMF measure on the compatible family.
The compatible law is not defined to make that conclusion automatic.

## One actual unrevealed coordinate

`nextBit i A` is the Boolean membership indicator of coordinate `i`.
`conditionedSlice_next_true` proves directly from compatible-set counts that

```text
Pr[i is in A | revealed P,N]
  = (h - P.card) / (U.card - (P.card + N.card)).
```

The proof treats `r=0` separately and, for `r>0`, counts compatible sets
containing `i` by inserting `i` into `P`. It uses
`Nat.add_one_mul_choose_eq` to derive the ratio. The named endpoint exports
`conditionedSlice_next_true_zero` and `conditionedSlice_next_true_one` prove
true mass 0 when `h=P.card` and true mass 1 when `r=m`. Thus both deterministic
endpoint cases are checked explicitly.

`conditionedSlice_map_nextBit` then proves equality of the actual pushforward
measure with the existing `bernoulliBool` law at parameter `r/m`. It holds for
every `i` in `U \ (P union N)` and retains both endpoints.

## Two-slice information bound

For `hMinus <= hPlus <= K`, `hPlus+hMinus=K`,
`ell=hPlus-hMinus`, `K>0`, `4*ell<=K`, and
`8*(P.card+N.card)<=K`, `twoSlice_feasible` derives feasibility of the same
revealed `P,N` under both slice counts. No conditioning-event positivity is
assumed.

`twoSlice_ratio_bounds` proves the reference parameter is strictly interior:

```text
1/4 <= pMinus <= 4/7 < 3/4,
pPlus - pMinus = ell / (K-j) <= 2*ell/K.
```

From these bounds it obtains `pMinus*(1-pMinus) >= 3/16`.
`twoSlice_next_kl_ne_top` proves the Mathlib `klDiv` of the two actual
conditional pushforwards is finite. Using the accepted T62 Bernoulli
chi-square bound, `twoSlice_next_kl_toReal_le` proves

```text
(klDiv nextPlus nextMinus).toReal
  <= 64 * ell^2 / (3 * K^2).
```

The optional `256/(3K)` corollary is not included, as permitted by the fixed
contract.

## Verification

The fresh library build

```text
/Users/michael/.elan/bin/lake build EstimatorIntegrity.UniformSliceConditioning
```

completed with exit code 0. The output contains style and unused-variable
linter suggestions only; it contains no compiler error or trust warning.

`Axioms.lean` applies `#print axioms` to every public declaration, including the
three explicit atomic/endpoint corollaries added during correspondence review.
Every declaration depends only on `propext`, `Classical.choice`, and
`Quot.sound`. `Declarations.lean` records every public signature. Both audit
commands exited with code 0. The source trust scan found no occurrence of
`sorry`, `admit`, `axiom`, `native_decide`, or `unsafe`.

Evidence is in
`docs/research/runs/2026-09-28-dynamic-continuation/lean/uniform-slice-conditioning/`:

- `build.log`: directly captured fresh module build and exit code;
- `Axioms.lean`, `axioms.log`: complete public axiom audit;
- `Declarations.lean`, `declarations.log`: exact public signatures;
- `trust-scan.log`: directly captured forbidden-token scan;
- `environment.log`, `environment.md`: pinned versions, revisions, commands,
  and exit codes;
- `failed-attempts.md`: explicitly retrospective summary of material
  development failures;
- `SHA256SUMS`: hashes of the final source, report, and evidence files.

Only the new module, this report, and its evidence directory were written. The
entrypoint, toolchain, Lake configuration, dependencies, earlier modules,
frozen proof sources, root ledgers, and numerical artifacts were not edited.

## Exact boundary

This module proves an actual one-step finite conditioning and information
result. It does not formalize a complete adaptive history, multi-step path-law
composition, seed simulation, padding, random stopping, MSE-to-testing,
slice-martingale concentration, a PDE certificate, a minimax theorem, code
runtime, or numerical evidence. It asserts no independence between successive
coordinates.
