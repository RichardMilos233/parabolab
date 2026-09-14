# Profile-rate efficiency and policy reuse: completed benchmark

The cheap grid short-time rule gave the lowest observed profile RMSE under
both calibrated predicted budgets. The numerical grid selector improved
fixed-sample accuracy over the point selector, but its setup cost was not
recovered by either one-curve or ten-curve workloads. This is a negative
practical result for numerical tuning against the strongest cheap baseline
in this experiment, alongside evidence that the intended grid objective matters.

A separate exact profile certificate also proves that the cheap grid rule
has lower expected squared profile error than all four alternatives at
each frozen predicted-budget allocation, conditional on the policies and
counts in the ideal real-arithmetic model. This strengthens the error
comparison without asserting equality of actual runtime.

The [protocol](profile-efficiency-protocol.md) was frozen before setup or
calibration. This report uses the completed
[archive](profile-efficiency/metadata.json), with no additional Monte Carlo
runs or changed allocations. The related
[theory note](../estimator-integrity/profile-rate-efficiency.md) derives the
profile loss, short-time rate, cost model and reuse comparison.

## Scope, accounting and completion

The estimator is the raw uniform one-dimensional Allen–Cahn wave at
`T=0.05,t=0`, on `[-2,-1,0,1,2]`, with equal loss weights. Both numerical
selectors use depth 2, quadrature orders 4/4, bracket `[0.2,2]` and tolerance
`1e-5`; the production solver draws complete trees without a depth cutoff.
All five variants retain `CodingTreeMC(...).solve(pde,grid)`, one worker
and uniform tuples.

Each group has 20 independently seeded workloads. A workload requests
either `R=1` or `R=10` independent curves, paying one setup charge.
Aggregate RMSE is

`sqrt(mean_workloads(mean_requested_curves(mean_grid_points(error²))))`.

Predictions from different curves are never pooled. The two reuse groups
have the same expected per-curve squared error at fixed N; the R=10 group
averages more independent squared errors and therefore has different
empirical variability. “Cold” means one policy construction for one curve,
with shared imports and interpreter startup excluded.

All prescribed samples completed:

- 25 fresh policy constructions and 25 independent calibration curves;
- 400 evaluation workloads, 2,200 requested curves and 11,000 point rows;
- 55,000,000 fixed-N and 84,621,200 predicted-budget evaluation trees;
- 1,250,000 separate calibration trees;
- 11,125 distinct calibration/evaluation point seeds, entropy `202609143`.

Run duration was 195.43 seconds through sampling and archive completion,
excluding final figure rendering and the later audit. Repeated setup
measurements consumed 1.6345 seconds and calibration solves 1.6876 seconds.
These are experiment overheads. Each workload's accounted cost is its
actual complete solve time plus **one frozen median setup charge**;
repeated measurements are not charged five times to a production request.
Raw solve times, sampler-reported times, elapsed time including artifact
I/O, setup components, counts, errors and tree diagnostics are retained.

## Frozen policies, setup and calibration

Five fresh setup trials produced identical rates within `1e-12` for every
policy. Times below are milliseconds; calibration is the median complete
five-point curve time at 10,000 samples per point.

| Policy | Frozen λ | Setup median | Setup min–max | Calibration curve median |
|---|---:|---:|---:|---:|
| Default | 1 | 0.00971 | 0.00321–0.01996 | 67.678 |
| Point short-time | 0.75 | 0.00550 | 0.00471–0.01092 | 66.213 |
| Point selected | 0.730548629711 | 53.827 | 53.207–59.193 | 68.878 |
| Grid short-time | 0.474969560166 | 0.04379 | 0.02354–0.06154 | 65.647 |
| Grid selected | 0.492264996516 | 270.091 | 266.375–285.088 | 65.523 |

The grid short-time rate is
`sqrt(sum(w*f(phi)²)/sum(w*phi²))`. It targets the leading small-horizon
profile objective, rather than averaging pointwise rates. The numerical
grid policy targets the weighted finite-depth moment objective. Its setup
is approximately four ordinary curve solves in this run.

The offline exact profile certificate was **not** constructed or checked
inside these workload costs. This benchmark measures the practical
finite-depth selector and cheap policies; it does not establish an
end-to-end speedup for online certification. Certificate construction and
its mathematical guarantees are separate artifacts.

## Fixed N = 10,000 per point

Costs are median accounted seconds **per requested curve**, so the R=10
columns already divide one workload's cost by ten.

| Policy | R=1 aggregate RMSE | R=1 cost/curve | R=10 aggregate RMSE | R=10 cost/curve |
|---|---:|---:|---:|---:|
| Default | 0.000832322 | 0.06665 | 0.000907410 | 0.06670 |
| Point short-time | 0.000775379 | 0.06578 | 0.000732050 | 0.06575 |
| Point selected | 0.000759930 | 0.12202 | 0.000749260 | 0.07365 |
| Grid short-time | 0.000737978 | 0.06481 | 0.000661057 | 0.06485 |
| Grid selected | 0.000593429 | 0.33491 | 0.000653985 | 0.09209 |

At R=10, grid selection had 12.7% lower observed aggregate RMSE than point
selection. Relative to the cheap grid rule, its observed RMSE advantage
was only 1.1%, with 42.0% greater median accounted cost per curve. The R=1
sample showed a larger 19.6% accuracy difference between the grid policies;
that difference is not reproduced at the same size in the independent
200-curve R=10 group. Neither difference is treated as a population
variance estimate with a confidence guarantee.

Pointwise records explain why the grid objective matters. In the R=10
fixed-N group, `x=-2` contributed about 57% of the default policy's squared
profile error, versus 36% for the grid short-time rule. Lower grid rates
improved errors at negative states while some central or positive states
favored the point policy. Aggregate improvement does not imply improvement
at every point or in the maximum-error metric.

The [fixed-N figure](profile-efficiency/fixed_n.png) shows all 20 workload
RMSE values per group, plus recorded cost/error scatter. The
[pointwise figure](profile-efficiency/pointwise_rmse.png) retains all five
states for both phases and reuse counts.

## Frozen predicted budgets and completed allocations

Using each policy's median setup `h_i` and calibration coefficient `c_i`,
the predeclared rule was

`B_R=max_i(h_i+R*10000*c_i)`,
`n_i,R=floor((B_R-h_i)/(R*c_i))`.

This gives `B_1=0.3356139581 s` and `B_10=0.9253198346 s`, or
`0.09253198346 s` per curve in the ten-curve workload. Those per-curve
budgets differ; compare reuse effects together with fixed-N results.
They are calibrated predictions, not equal mathematical expected costs.

| Policy | R=1 samples/point | R=10 samples/point |
|---|---:|---:|
| Default | 49,588 | 13,672 |
| Point short-time | 50,686 | 13,974 |
| Point selected | 40,911 | 12,652 |
| Grid short-time | 51,117 | 14,094 |
| Grid selected | 10,000 | 9,999 |

The last allocation is the direct floating-point floor in the frozen
rule: one sample below nominal at the policy setting the budget. It was
retained as scheduled. Each predicted cost is below its budget by less
than the cost of one additional sample at every point of every curve.
No wall-clock deadline stopped a curve.

| Policy | R=1 aggregate RMSE | R=1 median total s | R=10 aggregate RMSE | R=10 median total s |
|---|---:|---:|---:|---:|
| Default | 0.000370217 | 0.34929 | 0.000817942 | 0.96529 |
| Point short-time | 0.000364374 | 0.35063 | 0.000605256 | 0.97574 |
| Point selected | 0.000359683 | 0.34555 | 0.000609167 | 0.96304 |
| Grid short-time | 0.000269823 | 0.34870 | 0.000562130 | 0.97036 |
| Grid selected | 0.000620275 | 0.33918 | 0.000644322 | 0.95465 |

The grid short-time rule had 25.9% and 7.1% lower observed aggregate RMSE
than the point short-time rule at R=1 and R=10, respectively. Relative to
default, reductions were 27.1% and 31.3%. Both cheap baselines required by
the protocol remain visible.

Numerical grid selection had 2.299 times the cheap grid rule's RMSE at R=1
and 1.146 times its RMSE at R=10. Its setup reduced available sample
counts substantially. The point selector was close to the point short-time
baseline, with a 1.3% lower observed RMSE at R=1 and a 0.6% higher value at
R=10. These data do not demonstrate a practical advantage for either
numerical selector over the best cheap policy in this workload range.

The [predicted-budget figure](profile-efficiency/predicted_budget.png)
shows complete distributions, including all high-error or slow
observations. Full MSE and RMSE ratios against default, point short and
grid short policies are stored in the summaries.

## Conditional expected-error certificate

The independent [profile certificate summary](profile-certificate/summary.json)
now contains `benchmark_policy_bounds` and `allocation_bounds` tied to
the benchmark metadata's SHA-256. Each implemented rate is interpreted
as its exact binary-floating-point rational value using
`Fraction.from_float`; it is not replaced by a nearby rounded decimal.
Convex upper interpolation between certified nodes covers these rates.
For rates without an exact node, the lower bound conservatively uses
the certified global profile lower bound.

For a frozen policy with weighted single-tree variance `Vbar` and `n`
samples per point, the expected mean squared error per requested curve
is `Vbar/n`. Averaging the losses of R separately requested curves leaves
that expectation unchanged. Dividing the exact rational variance bounds
by the recorded integer allocations gives the following expected-MSE
ratios to the cheap grid short-time policy. Displayed intervals are
rounded outward; they concern **expected MSE**, rather than empirical
RMSE or expected RMSE.

| Competing policy | R=1 expected-MSE ratio | R=10 expected-MSE ratio |
|---|---:|---:|
| Default | [2.120240, 2.154154] | [2.120306, 2.154221] |
| Point short-time | [1.359965, 1.381733] | [1.360078, 1.381848] |
| Point selected | [1.229799, 1.654674] | [1.096438, 1.475239] |
| Grid selected | [5.031234, 5.163123] | [1.387352, 1.423721] |

All eight lower bounds exceed one. In particular, numerical grid
selection has more than 5.03123 times the cheap grid policy's expected
MSE at R=1, and more than 1.38735 times at R=10, under the frozen counts.
Those pairs use 10,000 versus 51,117 samples per point and 9,999 versus
14,094 samples per point, respectively. The empirical RMSE ratios above
are a different statistic from these expectation ratios.

These conclusions are conditional on the independently calibrated,
frozen policies and sample counts, for the ideal raw uniform estimator
at exact horizon `T=1/20` with real arithmetic. They do not certify
production floating-point or pseudorandom arithmetic, constrain actual
wall-clock costs, or give a confidence interval from the 20 replicate
workloads. Offline certificate construction is excluded from the
benchmark's setup charges. The stochastic and analytic identifications
are conventional proofs; this is not a Lean verification of the sampler.

At equal N, the certificate does not order the two grid policies:
their expected-MSE ratio interval contains one. The implemented cheap
grid rule has a global relative excess profile-variance upper bound
below 1.60%, and the implemented numerical grid rule below 1.006%,
each relative to the global optimum variance. These separate bounds
do not prove that the numerical grid rule improves on the cheap rule.

## Timing limits and interpretation

Before setup, the coordinator reported that the full Python suite,
certificate generation and Lean build had completed, with no known other
root or agent CPU jobs running. The coordinator restricted itself to
reading and writing until sampling finished. No outside CPU disturbance
was reported; outside processes were not controlled or continuously
monitored, so perfect machine isolation is not claimed.

At R=1, policy median totals ranged from 0.33918 to 0.35063 seconds, about
1.1%–4.5% above their predictions. Individual totals ranged from 0.33225 to
0.46529 seconds. At R=10, median totals ranged from 0.95465 to 0.97574
seconds, about 3.2%–5.5% above predictions; individual totals ranged from
0.92616 to 1.08813 seconds. All were retained. Timing variation limits
hardware-speed claims; prescribed complete counts preserve the fixed-N
error comparison.

These are empirical results from 20 workloads per group. Quartiles,
full ranges and pointwise errors are descriptive. There is no significance
claim, population-variance confidence interval, or universal claim across
horizons, grids, proposals, hardware or reuse counts beyond 1 and 10. A
numerical selector's convergence flag alone is not a full-tree certificate.

The practical next step is to keep the cheap grid rule as the incumbent
baseline and use its small certified remaining profile-variance gap to
assess whether further tuning can repay setup. Larger reuse experiments are justified only if
the attainable variance-cost improvement can plausibly repay setup.
Unequal point allocation is a separate target, since the leftmost state
still accounts for substantial error; it changes the objective and needs
its own frozen protocol. None of these follow-up experiments was run here.

## Reproducibility and verification

Recorded base revision:
`05012ffe711e19f2839d6a868ccf843d713fe44d`, declared branch
`codex/research-profile-efficiency`. This subtask performed no git
operation. The environment was Python 3.11.15, NumPy 2.4.6, macOS 26.3
arm64 in the existing conda `parabolab` environment.

The exact argument vector, coordination context and source hashes are in
[metadata.json](profile-efficiency/metadata.json). The run used
`MPLBACKEND=Agg`, `MPLCONFIGDIR=/tmp/parabolab-matplotlib` and
`XDG_CACHE_HOME=/tmp/parabolab-cache`, with:

```sh
/opt/miniconda3/envs/parabolab/bin/python examples/profile_efficiency_benchmark.py \
  --run --output-dir docs/research/results/profile-efficiency \
  --base-commit 05012ffe711e19f2839d6a868ccf843d713fe44d \
  --timing-context 'Coordinator reported full Python suite and Lean build finished, with no known other root or agent CPU jobs running. Coordinator restricted itself to reading and writing during calibration and evaluation. Outside processes were not controlled or continuously monitored; perfect machine isolation is not claimed.'
```

The driver refuses to overwrite a nonempty directory. Reproducing sampling
requires a new directory. Existing plots and summaries can be rebuilt
without samples using `--report-only`.

Predeclared hashes match the executed driver and current sources:

- Protocol: `0df97adfa09e50921af026f7496b33426ca28aa614252e9c0a0b4301d6555da4`.
- Driver: `7a9091fe5446f3fc8abb1251dff954d41805ea1f61962e18ba57af9446c33aef`.

The independent [archive audit](profile-efficiency/validate_archive.py)
passes all 22 recorded checks in
[validation.json](profile-efficiency/validation.json). It recomputes the
full schedule and ordering, unique seeds, median calibration, integer
allocations, exact analytic solution, curve/point errors, unpooled workload
losses, one-time setup charges, comparisons and completed tree counts.
This checks arithmetic and provenance, not stochastic correctness.

```sh
/opt/miniconda3/envs/parabolab/bin/python -m py_compile examples/profile_efficiency_benchmark.py
/opt/miniconda3/envs/parabolab/bin/python examples/profile_efficiency_benchmark.py --check-plan
/opt/miniconda3/envs/parabolab/bin/python docs/research/results/profile-efficiency/validate_archive.py
```

Raw data: [setup traces](profile-efficiency/setup_traces.json),
[calibration](profile-efficiency/calibration.json),
[workloads](profile-efficiency/workloads.jsonl),
[curves](profile-efficiency/profiles.jsonl), [points](profile-efficiency/points.csv),
[JSON summary](profile-efficiency/summary.json),
[CSV summary](profile-efficiency/summary.csv), and
[executed driver snapshot](profile-efficiency/driver_at_execution.py).
