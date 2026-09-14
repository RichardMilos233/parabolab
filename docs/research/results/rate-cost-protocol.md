# Predeclared rate/proposal cost benchmark protocol

Declared 2026-09-14 before running calibration or evaluation. Branch:
`codex/research-certified-rate`. This protocol is frozen for the initial run;
any departure must be recorded explicitly before interpreting results.

## Question and scope

For the Allen–Cahn traveling wave at `T=0.05`, does deterministic rate tuning
or the existing terminal tuple proposal improve observed solution accuracy
per total computation cost? Evaluate `(t,x)=(0,x)` on the fixed grid
`[-2,-1,0,1,2]`. Reuse rates selected at `x=0` over the whole grid.

The six fixed variants are:

1. Default rate `1`, uniform tuples.
2. JCP rate `-log(0.95)/T`, uniform tuples.
3. Short-time rate `abs(f(phi(0)))/abs(phi(0))`, uniform tuples.
4. Deterministically selected rate, uniform tuples.
5. Default rate `1`, terminal tuple proposal with uniform floor mass `0.1`.
6. Deterministically selected rate, the same terminal tuple proposal.

Both selectors use depth `2`, time and normal quadrature orders `4`, bracket
`[0.2,2.0]`, and optimizer tolerance `1e-5`. Selection uses only deterministic
calculations. The proposal is the current `TerminalTupleProposal`, including
its actual runtime evaluation and probability-validation costs. No solver
or proposal implementation changes are part of this benchmark.

## Samples, independent streams and complete workloads

Use `CodingTreeMC(..., n_jobs=1).solve(pde, grid)` for every profile. No depth
cap, clipping, rejection, result filtering, time-based stopping, or early
termination is allowed. Complete every scheduled tree even if a realized
runtime exceeds its expected budget. Report failures if sampling fails.

The seed entropy is `202609142`. Each profile gets the uint64 state generated
by `SeedSequence(entropy, spawn_key=(phase,replicate,variant))` as the integer
solver seed. The existing solver uses that integer plus the grid index for
each point. Store these actual seeds and check all point seeds for collisions.
Phases are `0` for calibration, `1` for fixed sample size and `2` for the
budget comparison. Ordering uses separate spawn keys `(3,phase,replicate)`
and a deterministic random permutation of all six variants each replicate.
Calibration and both evaluation phases therefore use separate randomness.

## Cost accounting and independent calibration

Record fresh PDE construction, proposal construction, and any required rate
selection separately for each variant. Baselines do not pay for optional
moment diagnostics. The selected policies and measured setup costs are
frozen before calibration. Every reported one-profile total cost charges
that variant's complete one-time setup plus its profile solve time, even
though the frozen policy is reused to run the replicated evaluation. Also
report sampling-only costs to show the effect of amortizing setup.

Use three independent calibration profiles per variant, each with `10000`
trees per point. Record each calibration solve time. Let `c_i` be the median
calibration profile time divided by `10000` (seconds per one tree at each of
the five grid points). Calibration samples never contribute to evaluation
accuracy statistics. Calibration costs are reported as a separate benchmark
overhead and are not charged as policy tuning needed by a production user.

For the expected-total-budget comparison, define the common target entirely
from calibration and setup costs:

`B = max_i(setup_seconds_i + 10000*c_i)`.

This is the smallest calibrated budget that fits the prescribed fixed-size
workload for every variant. Set
`N_i = floor((B - setup_seconds_i)/c_i)` trees **at each point**, frozen before
examining any evaluation result. This gives equal predicted total budgets
up to rounding. Record both predicted and actual costs; unequal realized
times are expected because calibration and execution are noisy. This is an
expected-cost comparison, not an assertion of identical wall-clock budgets.

## Evaluation and predeclared summaries

First run `20` independent replicates per variant with `10000` trees per
point: exactly `6,000,000` evaluation trees in the fixed-size phase. Then run
`20` fresh independent replicates with the calibrated `N_i` per point.

For each curve record each point estimate, reference value, signed error,
empirical sample standard error, actual seed, and sample count. Record
profile RMSE `sqrt(mean_x((estimate-exact)^2))`, maximum absolute point
error, solve seconds, setup charge, and total seconds. Summarize RMSE by
median, quartiles, minimum, maximum, and `sqrt(mean_replicates(RMSE^2))`;
summarize total cost by median and range. Present all six variants, pointwise
RMSE across replicates, and ratios against default and short-time baselines.

Plots show the full replicate RMSE distribution and accuracy versus
realized total cost. Sample-variance or standard-error outputs are descriptive
diagnostics, not certified population quantities. Do not claim confidence
intervals for population variance, statistical significance from overlapping
or non-overlapping empirical bars, global optimality, or a theorem about
speedup. Report unfavorable and inconclusive results as such.

## Provenance and stop rules

Store protocol hash, source hashes, environment versions, branch/base commit,
configuration, setup records, calibration records, allocated counts, seeds,
and every evaluation row. Only the protocol, script and result artifacts may
change. Historical artifacts remain intact, and nothing is merged to main.
If an allocation is invalid or the prescribed sample workload fails, stop
that phase with an explicit failure record; do not silently reduce budgets,
discard a variant, or rerun evaluation with a better-looking seed.
