# Rate/proposal accuracy versus total cost: initial replicated result

Date: 2026-09-14. Original branch: `codex/research-certified-rate`.
Integration update, 16 September 2026: the result is included in local
`main`, with user authorization confirmed; see the
[integration record](integration-2026-09-16.md). The [protocol](rate-cost-protocol.md) was
written before calibration and evaluation; its original hash is unchanged.

**The initial replicated study does not demonstrate an end-to-end gain from
deterministic tuning for this small one-profile workload.** At fixed sample
count, the selected-rate/terminal-proposal combination had lower observed
error than default. Charging its tuning cost gave baselines more samples
under the same calibrated predicted budget, and the short-time rate `0.75`
had the lowest observed aggregate RMSE in that comparison. This is an
empirical conclusion for these seeds and this workload, not a significance
claim or a general statement about the methods.

## Conditional cost model

Assume each complete-tree estimator at grid point `x_j` is unbiased with a
finite second moment. For `n` independent trees per point and `m` grid
points, linearity of expectation gives

\[
\mathbb E\!\left[\frac1m\sum_{j=1}^m
 (\widehat u_j-u_j)^2\right]
 =\frac{1}{mn}\sum_{j=1}^m\operatorname{Var}(H_j)
 =\frac{\overline V}{n}.
\]

Under the idealized deterministic cost model `C(n)=h+c*n`, where `h` is
one-time setup and `c` is the cost of one additional sample at every grid
point, a budget `B>h` would imply the continuous approximation

\[
\operatorname{MSE}(B)\approx\frac{c\,\overline V}{B-h}.
\]

For positive denominators, method `a` beats method `b` in this model iff
`c_a*Vbar_a*(B-h_b) < c_b*Vbar_b*(B-h_a)`. This algebra explains why variance
alone is insufficient and why tuning at `x=0` need not optimize the profile
objective. It does not assert that measured median timing is an expectation
or that these estimator hypotheses have been certified for every variant.

## Frozen experiment

The PDE is the existing Allen–Cahn traveling wave, `T=0.05`, `t=0`, evaluated
at `[-2,-1,0,1,2]`. All variants use serial `CodingTreeMC.solve`, with complete
trees, exact zero-code pruning, no depth cutoff, no clipping, and no timed
stopping. The terminal proposal uses floor mass `0.1`. Rate selection is
frozen at `x=0`, depth 2, quadrature orders 4, bracket `[0.2,2]`, tolerance
`1e-5`. Selected rates reproduce `0.7305486297108235` (uniform tuples) and
`0.7304853674984467` (terminal proposal). The short-time baseline is `0.75`;
JCP gives `1.0258658877510114`.

There were 20 independent replicates per variant in each evaluation phase,
with disjoint calibration and evaluation streams. Every scheduled sample
completed: **6,000,000 fixed-size trees plus 10,833,300 budget-phase trees**,
240 profiles and 1,200 point estimates. Calibration used another 900,000
trees in 18 profiles. Seeds, counts, execution order and raw point/profile
results are preserved.

The original protocol used the phrase “expected budget.” The reported
budget is more accurately a **calibrated predicted budget**: coefficients
come from median calibration timing, which is not a mathematical expected
cost. The allocation rule and data are unchanged; only two output labels
were clarified after evaluation. The exact executed driver is preserved
with a matching pre-evaluation hash.

## Fixed sample count

Each profile used 10,000 trees per point. Errors below are in units of
`10^-3`. “Aggregate RMSE” means the square root of the average squared
profile RMSE over all 20 replicates. IQR and ranges describe the observed
replicate distribution; they are not confidence intervals.

| Variant | Aggregate RMSE × 10³ | Median RMSE × 10³ (IQR) | RMSE range × 10³ | Median solve seconds | Median total seconds |
|---|---:|---:|---:|---:|---:|
| Default, uniform | 0.871 | 0.660 (0.572–0.996) | 0.381–1.674 | 0.0777 | 0.0778 |
| JCP, uniform | 1.069 | 0.942 (0.714–1.131) | 0.197–2.105 | 0.0793 | 0.0793 |
| Short time, uniform | 0.696 | 0.702 (0.530–0.765) | 0.325–1.222 | 0.0773 | 0.0773 |
| Selected rate, uniform | 0.752 | 0.553 (0.451–0.830) | 0.266–1.616 | 0.0809 | 0.1513 |
| Default, terminal q | 1.121 | 1.015 (0.801–1.269) | 0.317–1.948 | 0.0801 | 0.0802 |
| Selected rate, terminal q | 0.641 | 0.566 (0.462–0.686) | 0.174–1.382 | 0.0809 | 0.1724 |

Selected-rate/uniform reduced aggregate RMSE by 13.65% relative to default,
while selected-rate/terminal reduced it by 26.40%. Their one-profile total
costs were 1.95 and 2.22 times default. The short-time baseline reduced
aggregate RMSE by 20.14% with negligible setup cost. The terminal proposal
alone had higher observed aggregate error; these samples do not establish
its incremental benefit at fixed rate. With only 20 replicates, rare large
errors materially affect the aggregate statistic, so both the full
replicate distribution and medians are retained.

## Calibrated predicted total budget

Three independent calibration profiles per variant fixed the timing
coefficients. The common predicted total budget was **0.1786677081 s**,
computed before looking at evaluation outcomes. Sample counts were frozen
by `floor((B-setup)/calibrated_cost_per_grid_sample)` and every count was
completed, even when the runtime exceeded its prediction.

| Variant | Samples per point | Aggregate RMSE × 10³ | Median RMSE × 10³ (IQR) | Median actual total seconds | Actual total range, seconds |
|---|---:|---:|---:|---:|---:|
| Default, uniform | 21,242 | 0.583 | 0.563 (0.481–0.648) | 0.1651 | 0.1562–0.2012 |
| JCP, uniform | 21,796 | 0.653 | 0.619 (0.511–0.771) | 0.1716 | 0.1652–0.4074 |
| Short time, uniform | 21,901 | 0.544 | 0.431 (0.300–0.683) | 0.1699 | 0.1628–0.2652 |
| Selected rate, uniform | 12,618 | 0.746 | 0.620 (0.514–0.927) | 0.1702 | 0.1685–0.1967 |
| Default, terminal q | 20,776 | 0.658 | 0.621 (0.394–0.758) | 0.1702 | 0.1622–0.4091 |
| Selected rate, terminal q | 10,000 | 0.711 | 0.592 (0.482–0.843) | 0.1727 | 0.1693–0.2944 |

Selected-rate/uniform had 27.89% higher aggregate RMSE than default and
37.05% higher than the short-time baseline. The combined setting had 21.94%
and 30.68% higher aggregate RMSE, respectively. The short-time baseline had
6.69% lower aggregate RMSE than default in this phase. These are observed
ratios, not population improvement estimates with certified uncertainty.

Actual median total costs ranged from `0.1651` to `0.1727` seconds, about
3.3–7.6% below the calibration target. Individual profiles took up to
`0.4091` seconds. Other research agents were active during this run;
certificate computations, tests and Lean processes may have overlapped.
CPU load and scheduling were not controlled. The run therefore supports
an accuracy/workload comparison with recorded timing, not a precise
hardware speed claim. The fixed-count error comparison is unaffected by
those timing fluctuations because no samples were stopped or discarded.

The uniform and combined deterministic searches cost about `0.0704` and
`0.0915` seconds, respectively. Every reported one-profile total charges
that cost once. Reusing a frozen policy across many profiles could amortize
it, but that is a separate workload from the one-shot budget comparison.
Calibration itself cost `1.5564` seconds and is reported as benchmark
measurement overhead, rather than a required production tuning step. The
whole benchmark took `30.2290` seconds before figure/report generation.

## Interpretation and next experiment

1. Keep the inexpensive short-time rate as a required baseline in future
   certification and cost comparisons. This initial workload supplies no
   reason to replace it with deterministic tuning by default.
2. A future amortization study should prescribe reuse counts or a larger
   workload before running. It should separately test whether the small
   change from `0.75` to approximately `0.73` is worth its selection cost.
3. The negative half of the profile contributes most of the squared error.
   Tuning at one state leaves a spatial mismatch worth studying. A
   grid-averaged objective is a better next test than asserting that the
   reference-state optimum is a profile optimum.
4. The current terminal proxy does not show a stable incremental gain in
   these comparisons. Continuation-aware proposals need their own bounded
   experiment with construction/evaluation overhead included.

These are directions motivated by the observed evidence. No extra
post-hoc sample runs or parameter changes were used to improve the result.
Formal coverage of the cost equation is conditional; this benchmark itself
does not add a Lean proof of stochastic integrability or timing guarantees.

## Artifacts and checks

- [Driver](../../../examples/rate_cost_benchmark.py) and
  [executed snapshot](rate-cost-benchmark/driver_at_execution.py).
- [Configuration and provenance](rate-cost-benchmark/metadata.json),
  [calibration](rate-cost-benchmark/calibration.json),
  [raw profiles](rate-cost-benchmark/profiles.jsonl), and
  [raw points](rate-cost-benchmark/points.csv).
- [Summary CSV](rate-cost-benchmark/summary.csv),
  [summary JSON including pointwise RMSE](rate-cost-benchmark/summary.json),
  [figure](rate-cost-benchmark/rmse_cost.png), and
  [integrity verification](rate-cost-benchmark/validation.json).

The driver passed Python syntax compilation. An independent artifact audit
recomputed exact references from the closed-form wave, every signed error
and RMSE, all aggregate RMSEs, the budget and allocations, complete sample
counts, seed uniqueness across 1,290 calibration/evaluation point streams,
and consistency between profile and point files. All checks passed. The
figure was rendered and visually inspected. The original protocol hash and
executed driver hash were verified.

Executed from the repository root using Python 3.11.15 and NumPy 2.4.6:

```sh
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/parabolab-matplotlib XDG_CACHE_HOME=/tmp/parabolab-cache /opt/miniconda3/envs/parabolab/bin/python examples/rate_cost_benchmark.py --output-dir docs/research/results/rate-cost-benchmark
```

The driver refuses to overwrite an existing run. Use a new output directory
for replication. To rebuild only summaries/plots without drawing samples:

```sh
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/parabolab-matplotlib XDG_CACHE_HOME=/tmp/parabolab-cache /opt/miniconda3/envs/parabolab/bin/python examples/rate_cost_benchmark.py --output-dir docs/research/results/rate-cost-benchmark --report-only
```
