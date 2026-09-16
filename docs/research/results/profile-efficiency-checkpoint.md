# Reliable rate selection: certification, profile loss and total cost

14 September 2026. Consolidated research result on
`codex/research-profile-efficiency`, based on
`05012ffe711e19f2839d6a868ccf843d713fe44d` from
`codex/research-certified-rate`.

**Integration update, 16 September 2026:** this checkpoint was committed
as `ff58620` and is included in local `main`; the user has authorized
integration. See the [integration record](integration-2026-09-16.md) for
current verification and the distinction from historical run provenance.

The approximate sweet spot depends on the loss being optimized. For the
five-point Allen–Cahn wave profile, a cheap short-time formula gives
λ≈0.475 and is certified within **1.60% of the best weighted variance over
all positive common scalar rates**. Numerical grid selection gives
λ≈0.4923, but its setup does not pay off at the tested workloads. Exact
certificates show that it has at least 5.0312 times the cheap rule's
expected squared error at the frozen one-request allocation and 1.3873
times at the ten-request allocation. Separately, a rational candidate
λ=0.5 is certified within 0.93% of optimal weighted variance.

These results complete the main certification-and-cost milestone in the
[research plan](../future-directions-after-lambda.md). They support a
useful certificate and a practical cheap baseline. They do not establish
a speedup from the numerical selector or from online certification.

## 1. Research question and estimator specification

The initial question was whether a promising approximate rate can be
connected to the full-tree estimator and to useful PDE estimation at
total computational cost. Three different quantities must be separated:
the variance at one state, the error over an intended solution profile,
and the error affordable after paying for policy construction.

The primary benchmark is the one-dimensional Allen–Cahn equation
`u_t + (1/2)u_xx + u − u³ = 0`, with terminal data
`phi(x)=−1/(1+exp(x))` and exact wave
`u(t,x)=−1/(1+exp(x−3(T−t)/2))`. Here `T=1/20`, `t=0`, the profile is
`[-2,-1,0,1,2]`, and each point has weight `1/5`.

The estimator uses the raw labelled semilinear mechanism, uniform tuple
probabilities, exponential lifetimes and one scalar positive λ throughout
each tree. Its six normalized code classes are `(Id,D,F₀,F₁,F₂,F₃)`.
Exact zero-subtree pruning retains raw tuple probabilities. Renormalizing
after deleting dead labels would define a different estimator.

Production comparisons use complete trees through
`CodingTreeMC(...).solve(pde, grid)`, one worker, no clipping and no timed
stopping. Certificates concern the corresponding ideal real-arithmetic
functional. The numerical selector uses depth-two moment quadrature;
that finite-depth objective is explicitly distinct from the certified
full-tree objective.

## 2. Theoretical derivation

Let `M_j(λ)=E[H_{λ,x_j}²]`, with rate-invariant means `u_j`. Define

`Mbar(λ)=sum_j w_j M_j(λ)`,
`Vbar(λ)=Mbar(λ)−sum_j w_j u_j²`.

For independent unbiased sample averages with the same n trees at each
point, expected weighted squared profile error is `Vbar(λ)/n`. A workload
containing R separately requested curves averages R such losses, so its
expected loss is still `Vbar(λ)/n`. The predictions are not pooled.

The [profile derivation](../estimator-integrity/profile-rate-efficiency.md)
proves that fixed nonnegative weights preserve convexity and that
moment-excess bounds transfer unchanged to variance excess. The leading
short-time λ-dependent objective is

`λ sum_j w_j phi_j² + (1/λ) sum_j w_j f(phi_j)²`.

Under its nondegeneracy and small-time assumptions, its minimizer is

`λ_short = sqrt(sum_j w_j f(phi_j)² / sum_j w_j phi_j²)`.

This produces `0.47496956016576375` on the profile, compared with `0.75`
at the central state alone. Averaging pointwise optimal rates would not
derive this formula. The numerical profile selector instead minimizes a
weighted sum of finite-depth moment quadratures and returns
`0.49226499651590583`. Its convergence flag does not certify full-tree
optimality.

The [mean-identification argument](../estimator-integrity/allen-cahn-mean-identification.md)
closes the probabilistic mean obligation for these saved flat/wave
settings: an all-code second-moment envelope at one rate supplies absolute
first-moment control; rate cancellation in the killed first-moment
recursion extends it to every positive rate; bounded mild-system
uniqueness identifies the explicit PDE fields. This is a conventional
proof, not a Lean formalization of the stochastic process.

## 3. Exact full-profile numerical certificate

Fourteen rational candidate rates between 0.4 and 1 have degree-seven
polynomial residual witnesses, with two spatial subdivisions and exact
linear error bounds. The existing wave construction works in the compact
coordinate `s=1/(1+exp(x))`; no Gaussian spatial truncation is introduced.
New exact Taylor/remainder bounds for exp enclose each coordinate, signed
interval Horner evaluation bounds the trial polynomials, and nonnegative
weights combine them into profile bounds.

Convex secants supply global lower bounds, including exterior intervals;
the exterior bounds exclude an improvement over the incumbent. Exact
mean-square intervals convert second moments to variances. All rational
witnesses passed verification.

| Certified quantity | Bound, rounded conservatively |
|---|---:|
| Candidate λ | 1/2 |
| Global infimum of weighted variance | > 0.0041421075 |
| Weighted variance at λ=1/2 | [0.0041793670, 0.0041805932] |
| Global additive variance excess at λ=1/2 | < 0.00003848558 |
| Relative excess at λ=1/2 | < 0.93% |
| Relative excess of actual cheap grid policy | < 1.60% |
| Relative excess of actual numerical grid policy | < 1.006% |

The actual policies are the exact rational representations of their
saved binary-float rates. For a rate between two certified nodes, the
convex chord between endpoint upper bounds supplies a valid upper bound
without rounding the policy to a nearby node. Off-node lower bounds are
conservatively taken from the global lower bound. Consequently, the two
actual grid policies' variance intervals overlap: the smaller individual
excess bound does not prove that numerical selection improves on the
cheap rule at equal n.

At the rounded central rate `0.73055`, the profile variance lies in
`[0.0054853323,0.0054854120]`. Its lower bound exceeds the upper bound at
λ=0.5 by more than `0.0013047392`. Thus a good central rate can have a
certified disadvantage for this profile. This does not invalidate its
earlier center-specific certificate.

Independent floating collocation calculations, assembled from the
sampler's actual tuple mechanism at orders 24 and 36, fall inside all
six checked profile intervals. The largest inter-resolution difference
was about `2.77e-12`. These calculations corroborate the result; the
rational residual and comparison inequalities provide the certificate.

Evidence: [exact summary](profile-certificate/summary.json),
[witness archive](profile-certificate/witnesses.json.gz),
[verifier](../../../parabolab/profile_certificate.py),
[driver](../../../examples/certified_profile_rate.py).

## 4. Practical accuracy and total cost

The [protocol](profile-efficiency-protocol.md) was frozen before setup,
calibration or evaluation. It compares default, point short-time, point
selected, grid short-time and grid selected policies. Each phase/reuse/
policy group contains 20 independently seeded workloads. Setup is paid
once per workload; R=1 and R=10 represent separately requested curves
sharing the frozen policy. Repeated setup measurements and calibration
are recorded as experimental overhead.

All 400 workloads completed: 2,200 curves, 139,621,200 evaluation trees
and 1,250,000 separate calibration trees. The five-point numerical
selector's median setup was 0.270091 seconds, versus 0.00004379 seconds
for the cheap grid formula. A 10,000-sample-per-point curve took roughly
0.0655 seconds in calibration for either policy.

Using frozen setup medians `h_i` and calibration coefficients `c_i`, the
predicted total budget was `B_R=max_i(h_i+R*10000*c_i)`, with complete
counts `n_i,R=floor((B_R−h_i)/(R*c_i))`. These are calibrated predicted
budgets, not exact expected-cost or deadline guarantees.

| Comparison of grid selected with grid short-time | R=1 | R=10 |
|---|---:|---:|
| Predicted total budget, seconds | 0.335614 | 0.925320 |
| Selected samples per point | 10,000 | 9,999 |
| Cheap-rule samples per point | 51,117 | 14,094 |
| Observed aggregate RMSE ratio | 2.299 | 1.146 |
| Certified expected-MSE ratio | [5.031234, 5.163123] | [1.387352, 1.423721] |

The one-sample reduction to 9,999 is the original floating-point floor
in the frozen allocation rule and was retained. Dividing exact variance
intervals by these integer counts proves all eight competing
predicted-budget expected-MSE comparisons favor the cheap grid rule.
The certificate is conditional on independently frozen policies/counts
and the ideal estimator. It is not a confidence interval inferred from
the observed errors, an expected-RMSE bound or a runtime guarantee.

At fixed n=10,000, the R=10 numerical grid group had only 1.1% lower
observed aggregate RMSE than the cheap grid group, while median accounted
cost per curve was 42.0% higher. The R=1 group had a larger apparent
accuracy difference, which was not reproduced at the same size in the
independent R=10 group. No significance claim is made. All errors,
outliers, cost variation and incomplete/failed-run counts are retained.

The full [empirical report](profile-efficiency-results.md) includes five
policy comparisons, pointwise errors, timing deviations, all 22 archive
checks and source/seed provenance. Figures show
[fixed-n results](profile-efficiency/fixed_n.png),
[predicted-budget results](profile-efficiency/predicted_budget.png) and
[pointwise error](profile-efficiency/pointwise_rmse.png).

## 5. Is further amortization worth testing?

For the continuous model `n=(B−h)/(R*c)`, expected loss becomes
`R*c*Vbar/(B−h)`. Writing `W=c*Vbar`, a selector A with `W_A<W_B` improves
on baseline B exactly when the remaining budgets are positive and

`B > (W_B*h_A−W_A*h_B)/(W_B−W_A)`.

The saved variance bounds and frozen calibration medians give a useful
optimistic limit. Take the numerical selector's smallest compatible
`W_A` and the cheap rule's largest compatible `W_B`. The maximum compatible
product advantage is only about 1.760%, and even this favorable continuous
model cannot cross over below **15.3468 seconds of total budget**. The
tested totals were 0.3356 and 0.9253 seconds.

This is a conditional model calculation using median timing coefficients.
It does not predict that crossover occurs above that threshold, identify
an integer-allocation cutoff or certify timing on another machine. If
the selector's actual work-variance product is no smaller, its larger
setup prevents any eventual crossover in this model. A larger reuse
experiment is therefore a separate optional question, rather than a
necessary continuation of the current rate search.

## 6. Formal verification and reproducibility

The full Lean build passed with 3,391 jobs and no warnings. The new
[ProfileEfficiency module](../../../formal/EstimatorIntegrity/ProfileEfficiency.lean)
contains ten public lemmas: four continuous-budget comparison/substitution
lemmas and six weighted-convexity, enclosure, variance-transfer and exact
interpolation lemmas. Each passed an axiom audit using only `propext`,
`Classical.choice` and `Quot.sound`.

Together with the earlier certificate checkpoint, this gives 26 public
certificate/profile/cost lemmas and two private convex helpers. This
count concerns the two research checkpoints, not the entire repository.
The [proof registry](../proof-registry.md) names every declaration and
its omitted obligations. Lean does not verify the random-tree/PDE
correspondence, the rational Python verifier, concrete witness values,
floating sampler or measured cost model.

The final Python suite passed **248 tests, with 14 slow tests deselected,
in 46.32 seconds**. All certificate and benchmark source hashes match;
the independent experiment archive audit passed all 22 checks. Focused
profile tests cover weighted derivative
evaluation, optimizer behavior, exact exp/logistic intervals, signed
polynomial evaluation, common-horizon enforcement and policy interpolation.
Independent audits reconstructed all 14 profile intervals, five actual
policy bounds and 20 allocation rows from exact archived data, and
checked source/archive/metadata digests.

Recheck the certificate without sampling:

```sh
/opt/miniconda3/envs/parabolab/bin/python examples/certified_profile_rate.py \
  --verify docs/research/results/profile-certificate/witnesses.json.gz
/opt/miniconda3/envs/parabolab/bin/python \
  docs/research/results/profile-efficiency/validate_archive.py
```

To reconstruct the summary and exact allocation comparisons from the
same witnesses, use `--from-witnesses` instead of `--verify`, add
`--policy-metadata docs/research/results/profile-efficiency/metadata.json`
and select a new `--output` directory to preserve the historical summary.
This performs deterministic verification and collocation diagnostics;
it does not draw Monte Carlo samples. Reproducing the timed experiment
requires a new output directory; the complete command is in the empirical
report. Its executed driver and protocol are frozen.

The profile witness SHA-256 is
`199f40d34ceb2b9fd58dd053184ce812fbdb902dce201eb3c67e01b6997bf503`.
The certificate summary links the benchmark metadata hash
`d362a05bedd4375cf0b3d552e5b451bc5776dfb56b45873b4ee015dd6f40aba3`.
No offline certification cost is hidden inside a claimed sampler speedup.

## 7. Contribution, limits and continuation decision

The core contribution is a traceable chain from the explicitly fixed
coding-tree mechanism to useful full-tree excess bounds, then to a
profile loss and a total-cost decision. The previous
[certificate checkpoint](certified-rate-checkpoint.md) supplies the
corrected binary oracle, flat certificate, wave-root certificate,
moment/depth bounds and first six-variant cost study. This checkpoint
completes its prescribed profile/reuse follow-up.

The closest literature and claim boundaries remain those documented in
the [fourteen-source research sweep](../future-directions-after-lambda.md#literature-coverage-and-sources)
and [registry](../proof-registry.md): coding-tree representations, positive
moment comparison, convex importance-sampling objectives and
variance-cost tradeoffs are established tools. The evidence here is a
mechanism-specific certification and evaluation result. It does not
establish general publication priority, a universal optimal rate or
dominance over other PDE representations.

The result applies to this horizon, profile, weights, common scalar rate
and uniform tuple law. It makes no claim about maximum pointwise error,
unequal sample allocation, state-dependent lifetimes, other horizons,
high dimensions, deep-network training or nonuniform-proposal
certification. Production roundoff is also outside the exact guarantee.

**Practical decision from the recorded experiment:** retain the cheap grid short-time rule as the practical
incumbent for this benchmark. The remaining scalar-rate variance
headroom is bounded, and the tested numerical selectors spend more
setup than the saved samples justify. The certificate remains useful
for validating the cheap policy and quantifying that headroom.

**Research priority update, 16 September 2026:** the user prioritizes
algorithmic and mathematical contributions. The practical timing result
does not close the questions of full recursive optimization, approximation
error, broader guarantees or improved proposals. The grid objective is an
optional extension for multiple starting states sharing one rate, not a
prerequisite for the single-state problem.

Continuation-aware q is **deferred as optional and untested**. The prior
terminal-proxy experiment does not test a continuation-moment proposal.
If pursued, the next finite project should freeze a small code/time
table with positive support, compare uniform/terminal/continuation q at
a common λ, then reoptimize λ with each q held fixed. It must charge
training, storage and evaluation costs and recheck integrability under
the changed probabilities. Assess algorithmic value through variance
reduction, analytical scope and error control; assess practical speedup
separately using full cost accounting.

The main plan's certification and cost directions, evaluation discipline,
one profile/reuse extension and consolidation are complete. Other
directions remain alternatives. The completed result is integrated into
local `main`; no continuation-proposal experiment has been run.
