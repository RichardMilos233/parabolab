# Predeclared profile-rate efficiency and policy-reuse protocol

Declared 2026-09-14 before new setup measurements, calibration or evaluation.
Research branch: `codex/research-profile-efficiency`. Root coordination must
confirm that other heavy research processes have stopped before executing
this protocol. No experiment is started merely by writing this document or
the driver. Preserve this document's pre-evaluation hash with the results;
record any subsequent departure explicitly.

## Question and fixed estimators

Does choosing a rate for a whole requested solution profile improve accuracy
per total cost over a rate chosen at its central point? Does policy reuse
change that comparison once setup is charged correctly?

Use the existing raw uniform one-dimensional `SemilinearMechanism` for the
Allen–Cahn wave at `T=0.05,t=0`, grid `[-2,-1,0,1,2]`, with equal metric
weights `1/5`. Evaluate these five settings in this fixed identity order:

1. `default_uniform`: rate `1`.
2. `point_short_uniform`: rate `abs(f(phi(0)))/abs(phi(0))=0.75`.
3. `point_selected_uniform`: current depth-2 deterministic selector at `x=0`.
4. `grid_short_uniform`: `short_time_profile_rate(pde,grid,weights)`.
5. `grid_selected_uniform`: `optimize_profile_rate_1d(pde,0,grid,weights=weights)`.

Both numerical selectors use depth `2`, time/normal quadrature orders `4`,
bracket `[0.2,2]`, and tolerance `1e-5`. The grid short-time rate is the
profile-level asymptotic rule, not the arithmetic average of pointwise
rates. All settings use the existing
`CodingTreeMC(...,n_jobs=1).solve(pde,grid)` interface, uniform tuples and
the actual complete-tree sampler. No production sampler or solver changes
are part of this driver.

## Workloads and estimands

Use reuse counts `R=1` and `R=10`, with 20 independent workload replicates
per variant for each phase/reuse count. One workload consists of `R`
independent requested curves, with one setup charge for the entire workload.
Every curve solves the same prescribed PDE/grid with fresh randomness;
**do not average predictions across requested curves**.

For each workload record

`workload_MSE = mean_over_R_curves(mean_over_5_points((estimate-exact)^2))`.

Its displayed workload RMSE is `sqrt(workload_MSE)`. Aggregate performance
is `sqrt(mean_over_20_workloads(workload_MSE))`. This averages all `R` curve
errors within the workload and measures the accuracy of individual requested
curves. Increasing `R` does not mechanically reduce an estimator's sample
error by pooling outputs. Also retain each curve's MSE, each point's signed
error and empirical standard error, and all maximum-error diagnostics.

“Cold” means a single requested curve paying for one policy construction;
it does not mean a fresh Python process, cold operating-system caches, or
module-import time. The `R=10` case pays one policy setup for ten curves.

## Setup and independent calibration

Before drawing any calibration/evaluation trees, construct each policy five
times from a fresh PDE instance. Interleave variant order using a separate
deterministic permutation for each setup trial. Record PDE-construction,
rate-selection and total setup times. Freeze `h_i` as the median of the five
total setup measurements. The five deterministic selected rates must agree
within absolute `1e-12`; otherwise stop and investigate before evaluation.
Freeze the first constructed policy's rate for all subsequent curves.
Report all setup traces, median and range; do not cherry-pick the fastest.
Shared Python/import initialization is excluded for every variant.

Then run five independent calibration profiles per variant, each at
`N=10000` trees per point. Record wall time around the complete `.solve()`
call and its sampler-reported time. Let

`c_i = median(calibration_profile_solve_seconds_i)/10000`.

This is a **predicted cost coefficient** for adding one tree at each of the
five grid points. Median timing is not a mathematical expectation. Setup
timing repeats and calibration trees are benchmark-measurement overhead;
report them separately, rather than treating all five repeated setups as
necessary work for a production request. Each evaluation workload's total
cost is its actual complete solve time plus the frozen one-time charge
`h_i`. Also report solve-only cost and per-curve total cost.

No calibration values enter evaluation error statistics or rate selection.
The fixed policy construction itself is entirely deterministic.

## Fixed-N and calibrated predicted-budget phases

First evaluate all variants at `N=10000` trees per point for both reuse
counts. The fixed-N phase schedules exactly
`20*5*(1+10)*5*10000 = 55,000,000` evaluation trees.

For the second phase, choose the smallest calibrated predicted total budget
that fits each variant's prescribed nominal workload:

`B_R = max_i(h_i + R*N*c_i)`.

Set the per-point sample count, identical for all `R` curves in that workload,
to

`n_i,R = floor((B_R-h_i)/(R*c_i))`.

Freeze both `B_R` values and all ten counts before examining any evaluation
outcome. This allocation gives equal predicted total costs up to integer
rounding. Report `B_R`, `B_R/R`, all counts, predictions and realized costs.
The per-curve budget can differ between reuse counts because setup is
amortized. Interpret reuse effects jointly with the fixed-N phase, which
holds per-curve sample count unchanged. Do not claim identical realized
wall time or equality of mathematical expected cost.

The second phase uses 20 fresh workload replicates per variant and each
reuse count, independently of fixed-N evaluation. Complete every prescribed
tree. No cutoff, clipping, rejection, sample/result filtering, timed stopping,
variant removal, or truncation of a slow workload is allowed. If a scheduled
run fails, save an explicit failure record; do not silently change its count
or restart it under a favorable seed.

## Independent seed and ordering plan

Seed entropy is `202609143`, distinct from previous benchmarks. Each profile
uses the uint64 state from
`SeedSequence(entropy,spawn_key=(phase,R,replicate,variant,curve_index))`
as its integer solver seed; the existing solver adds the grid index at each
point. Calibration uses phase `0`, `R=1`, five replicate indices and curve
index `0`. Fixed-N uses phase `1`; predicted-budget evaluation uses phase
`2`. Record the actual integer seeds and audit every scheduled point seed
for collisions across all three phases before drawing samples.

Execution ordering uses disjoint keys: setup permutation
`(3,trial)`; calibration permutation `(4,trial)`; workload permutation
`(5,phase,replicate)` over the ten `(R,variant)` combinations. Complete all
`R` curves of a workload together in their recorded order. Use no evaluation
randomness in ordering. The workload ordering balances time drift across
reuse counts and variants without changing the statistical estimand.

## Predeclared summaries and interpretation

Preserve every profile/point row and aggregate only after all scheduled
samples complete. For each `(phase,R,variant)` report aggregate RMSE,
workload RMSE median, quartiles and full range; median/range of one-shot
total cost, solve-only cost and per-curve cost; pointwise RMSE across all
requested curves; and MSE/RMSE ratios against **both** cheap short-time
baselines, plus default. Keep both expensive selectors visible even when
they perform poorly.

Plots show the full 20-workload RMSE distributions and accuracy versus
recorded total/per-curve cost, separating `R=1` from `R=10`. Also show the
pointwise error profile to reveal which states drive the grid objective.
Empirical variances/standard errors are descriptive only. Do not claim
population-variance confidence intervals, significance from 20 replicates,
global near-optimality of the numerical grid selector, or hardware speed
from noisy timing. The previous root-specific mathematical certificate is
not a certificate for the new grid objective.

## Provenance and pre-execution gate

Save protocol and source hashes, environment, declared branch, exact
configuration, setup/calibration traces, allocation rules/counts, integer
seeds, workload/curve/point records, failures and summaries. Keep an executed
driver snapshot. Existing results remain untouched; the driver must refuse
to overwrite a completed or partial run directory.

Before running setup measurements or calibration, wait for the root's
explicit timing-ready signal and usable profile-rate API. The intended
Python environment is the existing conda `parabolab` environment. No git,
commit or merge action is part of this experiment.
