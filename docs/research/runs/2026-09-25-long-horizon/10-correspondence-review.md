# Bounded sampler correspondence review

Status: **pass after one guard fix**. I found no unresolved blocking defect or
mathematical correspondence mismatch in the final bounded-majority sampler,
its Solver integration, or the canonical 60-row evidence.

This was an implementation audit against `04-theory.md` B1--B3 and the Lean
finite-tree result in `formal/EstimatorIntegrity/LongHorizon.lean`. It is not a
second proof of the stochastic representation.

## Reviewed implementation

The main path is `parabolab/majority.py`:

1. A live particle draws one exponential lifetime and one standard normal.
   Its death position is `x + sqrt(duration) * normal`, matching the
   repository's standard-Brownian convention and the `1/2` Laplacian.
2. If the particle branches, its single death position and death time are
   repeated three times. On the next loop iteration the three children receive
   separate exponential and normal draws. Thus siblings share their birth
   position and are conditionally independent thereafter.
3. If the particle survives to the horizon, the observed terminal value is
   checked to be finite and in `[-1,1]` and is returned without a survival
   likelihood factor. If it branches, the three completed child values are
   combined by `majority_branch`.
4. Children are created as consecutive triples in parent order. The stored
   generation arrays are then traversed in reverse; reshaping the next
   generation to `(-1,3)` therefore aligns exactly one triple with each true
   entry of the preceding generation's branch mask. This is a correct
   bottom-up reduction of the sampled ternary forest.

The implemented kernel is

```
(2/r) * ((a+b+c-abc)/2) + (1-2/r) * ((a+b+c)/3),
```

which is algebraically the `B_r` in B1. The code admits only finite `r >= 2`.
The Lean declarations `boundedReaction_convex_decomposition`,
`boundedReaction_mem_Icc`, and `BoundedTernaryTree.eval_mem_Icc` establish the
corresponding exact-real finite-tree enclosure. The conventional diagonal
identity `r(B_r(u,u,u)-u)=u-u^3` supplies the Allen--Cahn reaction after
first-event conditioning.

There are no depth or node limits, outlier filters, value clips, likelihood
weights, or per-root rejection paths. `_sample_batch` continues until an
entire root batch has no live branch, records every node through its root id,
and returns one value, node count, and root-branch flag per scheduled root.
Batching limits working memory only. The identity `N=1+3B` is visible in every
archived root count.

## PDE and input contract

`ParabolicPDE.reaction_kind` is an explicit compatibility marker. Only
`allen_cahn_flat` and `allen_cahn_wave_1d`, the two scalar Allen--Cahn library
constructors in scope, set it to `"allen_cahn"`; an untagged callback and the
Fisher--KPP entry are rejected. The solver also requires `d=1`. This is a
trusted marker: it intentionally does not infer or symbolically prove that an
arbitrary user-modified callback equals `u-u^3`.

The final checks reject nonfinite or sub-threshold rates, nonpositive or
nonintegral sample/batch counts, nonfinite positions, times outside `[0,T]`,
simultaneous `seed` and `rng`, nonfinite/nonpositive PDE horizons, and observed
terminal values outside the bounded contract. `AllenCahnMajorityMC.solve`
also requires a finite nonempty one-dimensional grid and returns the existing
`Curve` fields, including per-point standard errors and actual evaluated
points.

One material guard gap was identified during review: a tagged PDE with
`T=+infinity` passed the original checks and could branch forever. The final
`_validate_pde` now requires a finite positive terminal time, and the focused
tests cover both `T=inf` and `T=nan`. No scheduled valid draw changed, so the
canonical rerun has the same raw archive hash as the first execution.

## Tests and independent algebra checks

I reran:

```
/opt/miniconda3/envs/parabolab/bin/python -m pytest -q \
  tests/test_majority.py tests/test_solve.py tests/test_allen_cahn.py
```

Result: `47 passed, 3 deselected in 22.40s`. The majority-specific subset has
11 passing tests. In particular it tests the shared parent position followed
by three separate child draws, exact constant fixed points, the reaction tag,
the finite-horizon guard, observed terminal bounds, broad flat/wave mean
agreement, tree-count congruence, Curve/factory behavior, and torch-free
top-level import.

`numerics/check_bounded_theory.py` separately checked 120 finite-support laws
and 9,720 exact rational kernel evaluations. It verified the diagonal mean
law, the conditional second-moment formula, cube values for rates 2, 2.5 and
3, corner failure below rate two, and generator ordering across those three
rates. Its floating flat-moment ODE reference used two solvers/tolerances; the
largest refinement gap was `7.03e-10`. These checks support B2/B3 algebra but
do not replace the PDE comparison proof.

## Canonical 60-row evidence

The final driver exactly reconstructs the frozen protocol:

- rate two at six horizons, rates 2.5 and 3 at three horizons each;
- one flat point, three fixed wave points, and one moving-front wave point per
  rate/horizon pair;
- 60 rows, 2,048 roots per row, seeds `20260925 + row_index`;
- 12 moving-front rows with `x=1.5*T` and exact value `-0.5`.

The archive contains arrays of shape `(60,2048)` for values, node counts and
root-branch flags: 122,880 completed roots. Row indices, seeds, raw means,
sample variances, mean node counts and root-branch fractions reproduce the
JSON exactly. Every node count is positive and congruent to one modulo three.
The largest sampled tree has 76,237 nodes. The largest absolute empirical
node-mean discrepancy from `(3 exp(2rT)-1)/2` is about 8.80%, at the
rate-two, `T=2` moving-front row; this is sampling variation in a heavy-tailed
cost, not evidence of clipping.

All 60 pointwise and union-bound simultaneous Hoeffding intervals contain the
known exact solution. The largest absolute mean error is
`0.0074756232413158985`, at the rate-two, `T=2` moving front. All 12 moving
front estimates remain close to `-0.5`, so the long-horizon wave evidence is
not limited to fixed points that approach the stable state.

The canonical raw SHA-256 is
`a05f404895daf22a02abb4056c15975b41d414ef3b5ec0cd4267199c30e4b74a`.
`bounded-results.json` records the current sampler hash
`00a8fa89bbf318b17bc5f587892b8237741f712a845951abffc7e7f8df42e3a3`.
The driver reports no cutoff, clipping, outlier removal or discarded root.
The initial execution log/JSON was overwritten by the source-bound rerun
before a later retention request; `bounded-initial-execution-manifest.json`
records that provenance limitation without reconstructing missing bytes. Both
executions printed the same raw archive hash.

## Remaining coverage limits

The Lean theorem covers exact-real evaluation of an already finite tree. It
does not prove continuous-time nonexplosion, conditional independence, the
first-event mild equation, or PDE uniqueness. Those bridges remain the
conventional B1 argument. The implementation audit checks that the code has
the structure required by that argument; the 60-row agreement is numerical
evidence rather than a proof of unbiasedness.

The terminal bound is checked at every sampled leaf, but code cannot establish
that an arbitrary callback is globally bounded before sampling. The explicit
reaction marker is also a caller-maintained contract. A manually forged marker
or a callback changed after construction lies outside the reviewed library
path.

Exact real arithmetic preserves `[-1,1]`. In the raw NumPy archive, three of
122,880 outputs are `-1.0000000000000002`, one binary64 ulp outside the exact
interval. The sampler correctly does not clip them. The JSON explicitly says
floating evaluation error is not enclosed, so its Hoeffding radii should be
read as exact-arithmetic bounds with this recorded floating limitation, not as
machine-verified intervals.

B3's variance monotonicity is a theorem about full moments and PDE comparison.
The exact finite-law checks and flat ODE references agree with it, while the
finite Monte Carlo rows alone do not prove monotonicity or any variance-cost
optimum. Likewise, empirical node means do not prove the conventional expected
node-count formula. Exponential work remains the practical long-horizon limit
even though the exact estimator value is bounded.

## Reviewed hashes

```
00a8fa89bbf318b17bc5f587892b8237741f712a845951abffc7e7f8df42e3a3  parabolab/majority.py
3aa55239626e5bd09a0520aa09225361a2bd296be3054ebfa28be1e468a7ea52  parabolab/pde.py
b37aebf5940be5832ed30986165cc53dc9d7bdade13faa37919a262c92612638  parabolab/library.py
16f522f56b0c2d898a383c43d24f561cac85b2347ff39b06b40546c7ea1bf953  parabolab/__init__.py
9e1397bfc1da476e5f86716d0ab3d7de67f009700740f12530c01336b4d4e308  tests/test_majority.py
a95d3b369c94f50451db55b1e4b1851fa435f326b8f5c20f1e309fac5bb59db7  numerics/bounded_experiment.py
a6788084236680b2fdae919c8d3582259895be69ed247be336cda866c2b28fea  numerics/bounded-results.json
a05f404895daf22a02abb4056c15975b41d414ef3b5ec0cd4267199c30e4b74a  numerics/bounded-raw.npz
6f9a8dde10f0c12467fd23b0585e3f526907bfc02834d9958b5bb5f9f08e864e  numerics/bounded-theory-checks.json
```
