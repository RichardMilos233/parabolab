# T04 — Vectorized complete-tree sampler implementation

Date: 27 September 2026. Scope: numerical implementation and tests after the
theory→Lean core gate. This task added only the slab sampler, its tests, and
this implementation note. It did not alter the existing tree mechanisms or
theory.

## Result

`numerics/slab_sampler.py` implements the agreed producer API:

- `raw_sample(positions, h, terminal, rng, root_code=0)`;
- `majority_sample(positions, h, phi, rng)`;
- both return `SlabSamples(values, node_counts, root_branched,
  terminal_counts)`;
- the first three arrays are aligned one-dimensional per-root records;
- `terminal_counts` is aggregate `int64` shape `(6,)` in the fixed order
  `(Id, Dx, F0, F1, F2, F3)`.

The raw implementation uses breadth-first vectorized generations and folds
child products in reverse. Its normalized branch rules are exactly:

- `Id -> F0`, coefficient `exp(2 tau)/2`;
- `Dx -> (F1, Dx)`, coefficient `exp(2 tau)/2`;
- label zero for `Fk -> (F0, F{k+1})`, coefficient `exp(2 tau)`;
- label one for `Fk -> (Dx, Dx, F{k+2})`, coefficient
  `-exp(2 tau)/2`.

Every `Fk` branch draws its uniform binary label before structural-zero
handling. A selected tuple containing `F4` or above returns zero immediately
without changing the label probability and without creating child nodes.
All live children receive the same parent death position. Every started root
is retained and completed. There is no depth or node cutoff, tree-value
clipping, failed-root deletion, or output-dependent sample count.

The raw API enforces the certified local range `0 <= h <= 2/25`. The terminal
callback is vectorized and supplies `(g,g')`. The C4 certificate additionally
requires the global contracts `|g| <= 2/5` and `|g'| <= 1/2`; finite sampled
leaf checks cannot prove those global bounds, so the implementation documents
them rather than claiming to certify them. Finite positions, horizons, random
draws, terminal values, and returned tree values are checked. Values are not
clipped to the C4 envelope.

The majority implementation is the complete rate-two ternary law
`(a+b+c-abc)/2`. Its internal root batches bound ordinary working memory but
never split or truncate an individual tree. Majority leaves are counted in
the `Id` terminal coordinate.

## Deterministic and correspondence tests

`numerics/test_slab_sampler.py` has 20 tests. Scripted draws independently
check the six signed terminal polynomials and their squares, leaf survival,
the unary `Id` coefficient, the `Dx` product, both `Fk` labels and signs,
post-label structural zero handling, common child birth position, exact node
and leaf counts, the majority rule, finite-input rejection, local-horizon
validation, and absence of terminal-value clipping.

Independent fixed-seed distribution diagnostics compare the vectorized raw
sampler with `parabolab.tree.sample_tree` at rate two, `h=0.05`, and
`N=12000` per case. The terminal polynomial was
`g(x)=0.2 sin(x)+0.01 sin(3x)`. The entries below are
`vectorized - original`; no seeds were selected after observing outcomes.

| normalized root | x | vector seed | original seed | mean deviation | second-moment deviation |
|---|---:|---:|---:|---:|---:|
| Id | -0.7 | 3000 | 9000 | -9.896050e-4 | 2.584947e-4 |
| Dx | 0.4 | 3001 | 9001 | 1.203903e-3 | 4.328480e-4 |
| F0 | 1.1 | 3002 | 9002 | -6.294813e-4 | -1.282527e-4 |
| F2 | -0.2 | 3004 | 9004 | 2.347960e-3 | 4.321587e-3 |

The corresponding majority comparison used `h=0.2`, `x=0.45`, `N=12000`,
vector seed 771, and existing-sampler seed 991. Its mean deviation was
`1.016712e-3` and second-moment deviation was `1.907458e-4`. Test thresholds
use eight empirical standard errors plus a small absolute floor. The
second-moment uncertainty is only an empirical diagnostic; it is not stated
as a proved fourth-moment confidence interval.

The sampler tests passed as `20 passed in 0.52s`. The combined sampler and
T05 driver suite passed as `29 passed in 3.12s` in the `parabolab` conda
environment.

## Smoke throughput and source freeze

After one warm-up, one Apple-host CPU smoke run completed 200,000 `Id` roots
at `h=0.08` in 0.01645 seconds, about 12.16 million roots/second. It processed
236,594 nodes, or 1.18297 nodes/root. This is a local implementation timing,
not a production-runtime guarantee or a mathematical selection criterion.

Source hashes at the completed T04 test gate:

- `slab_sampler.py`:
  `994e892784f36930fa63649aa749985448df75887f9096f6c40c142b46ff108a`;
- `test_slab_sampler.py`:
  `ffa532620067c3e6570694b3b1b8d21243fdddb957d0a72cb2ec23ef7e768791`.

No mismatch with C3/C4 or the existing sampler law was found.
