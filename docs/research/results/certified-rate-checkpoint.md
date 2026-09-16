# Certified-rate research checkpoint

14 September 2026. Research branch: `codex/research-certified-rate`, based on
`0afcb3c4ba446d20ff9337e4a4e1f2124bda5730`.

**Integration update, 16 September 2026:** commits `2f26313` and `05012ff`
are included in local `main`, with user authorization confirmed. See the
[integration record](integration-2026-09-16.md) for current checks.

The prescribed profile/reuse follow-up is now complete in the
[profile-efficiency checkpoint](profile-efficiency-checkpoint.md).
This document retains the original certificate milestone and its dated
next-step discussion for provenance.

**The flat control and the actual wave root now have verified global
rate-selection certificates.** For the wave at `T=0.05,x=0`, the rounded
historical rate `0.73055` has additive full-tree variance excess below
`6.130773×10^-6`. The binary benchmark is corrected, while a separate
replicated cost study finds no demonstrated end-to-end gain from the
existing deterministic selector for its small one-profile workload.

## 1. Exact-rational flat Allen–Cahn certificate

The benchmark is `allen_cahn_flat(phi0=1/2, T=1/20)`, using the raw
one-dimensional `SemilinearMechanism`, uniform labelled tuple probabilities,
and the ideal real-arithmetic full-tree functional. The six code classes
are `(Id,D,F₀,F₁,F₂,F₃)`. Exact zero-subtree pruning retains the original
tuple probabilities; deleting dead labels and renormalizing would describe
a different estimator.

The [derivation](../estimator-integrity/allen-cahn-codewise-certificate.md)
reduces the spatially constant moment system to a positive polynomial ODE.
The verifier checks rational upper-box inequalities and lower integration
steps. A rate cover supplies a lower bound for the infimum; topology
contributions exclude improvements outside the search interval. The saved
run uses 200 time steps, a 48-bit rational rounding grid and 45 final rate
cells covering `[1/5,2]`.

| Quantity | Verified exact value | Decimal display |
|---|---|---:|
| Selected rate | `1907/2560` | 0.744921875 |
| Selected full-tree second-moment upper bound | `75820673137583/281474976710656` | ≈ 0.269369142592 |
| Global infimum lower bound | `18948168212961/70368744177664` | ≈ 0.269269665594 |
| Additive excess bound | `28000285739/281474976710656` | < 0.0001 |

The bounds outside the search interval are `73/256` for rates at most
`1/5` and `11/40` for rates at least `2`. Both exceed the incumbent upper
bound in exact arithmetic, so the excess guarantee applies to **all
positive rates**, not only the searched interval. No claim of optimizer
attainment is needed. The guarantee concerns objective excess; it is not
an error bound of `10^-4` on the selected rate itself.

The rate-one lower enclosure exceeds the selected-rate upper enclosure by
at least `30840997895/35184372088832`, approximately `0.000876553881`.
This is a certified second-moment and variance reduction. The separate
[mean-identification proof](../estimator-integrity/allen-cahn-mean-identification.md)
now discharges the rate-invariant mean condition for these saved flat and
wave estimators. It uses one all-code moment envelope, rate cancellation
in the absolute first-moment recursion, and bounded uniqueness of the
explicit signed mild system. The result covers every positive rate,
including rates with infinite second moment, and is conventional
mathematics rather than Lean stochastic formalization.

An independent floating ODE solve gives a minimizer near `0.74367026` and
agrees with the rational enclosure. It is a diagnostic, not the certificate.
The certified additive gap is conservative relative to the diagnostic
optimal variance of about `0.00015113`; no tight relative variance
optimality claim follows.

Evidence: [summary](rate-certificate/summary.json),
[exact witness archive](rate-certificate/witnesses.json.gz),
[verifier](../../../parabolab/rate_certificate.py), and
[reproduction script](../../../examples/certified_allen_cahn_rate.py).

## 2. Wave moment, depth-tail and full-tree rate certificates

The saved wave envelope uses the same raw mechanism and uniform tuple law,
`T=1/20`, and the entire rate interval `[7/10,4/5]`. Terminal-code bounds
hold at every spatial state, so no Brownian spatial cutoff is used.

The ordinary root moment is bounded by the exact rational number
`297372020821519/281474976710656` (approximately `1.0564776461`). The
`2^N`-tilted root moment is bounded by
`307426758639711/281474976710656` (approximately `1.0921992506`), where
`N` counts branch clock expiries. The attempted tilt-4 box was inconclusive
at step 171; this does not prove moment divergence.

The positive-system Jacobian gives a factorial bound on the difference
between the full moment and the exact generation-killed moment. Values
below are decimal displays of rational bounds recomputed from the saved
ordinary-moment witness:

| Killed branch depth K | Uniform upper bound on omitted second moment |
|---:|---:|
| 2 | < 0.0033770080 |
| 4 | < 0.0001772628 |
| 6 | < 0.0000044445 |
| 8 | < 0.0000000650 |
| 10 | < 0.000000000622 |

These envelope/tail bounds alone do not certify the old Gaussian/time
quadrature objective. A separate completed
[wave residual certificate](wave-rate-certificate.md) now encloses the
full moment directly, using an exact logistic coordinate change, rational
degree-five trial polynomials, Bernstein residual bounds on four spatial
subintervals and 100 rational linear-error steps on a `2^-60` grid. It
therefore avoids relying on a new quadrature-error estimate or adding a
separate killed-depth tail.

Ten exact rational rates were certified:
`{0.7,0.7125,0.725,0.73055,0.7375,0.75,0.7625,0.775,0.7875,0.8}`.
Neighboring secant extrapolation gives lower envelopes between sampled
rates. Verified exterior slope signs exclude improvements below `0.7`
and above `0.8`, so the following bounds compare with **all positive
rates** at the stated root:

| Candidate | Certified additive full-tree second-moment and variance-excess bound |
|---|---:|
| `59/80 = 0.7375`, smallest certified upper-bound candidate | < `5.688312×10^-6` |
| `14611/20000 = 0.73055`, rounded historical rate | < `6.130773×10^-6` |

The point intervals overlap, so this does not prove that `0.7375` has a
smaller true moment than `0.73055`. The historical certificate applies to
the exact rounded rate, not literally the earlier floating-point output
`0.7305486297108235`. Against rate one, the selected candidate has a
certified additive second-moment and variance reduction exceeding
`0.000955093206`, with the common-mean condition discharged by the linked
conventional proof.

Evidence: [exact summary](wave-certificate/summary.json) and
[witness archive](wave-certificate/witnesses.json.gz). Independent
collocation lies inside the rational bounds, as a separate diagnostic.
The certificates cover one horizon/root and the raw uniform mechanism;
nonuniform terminal proposals and production roundoff remain outside
their scope. The approximately 30-second certificate generation/checking/
diagnostic run is an offline verification procedure, distinct from the
approximately 0.1-second practical selector studied below.

## 3. Binary benchmark correction

The historical binary plot optimized derivative-coded trees but compared
them with a standard-binary Riccati oracle. The corrected driver explicitly
uses `Id → (Id,Id)`, terminal value one and tuple probability one, and
separates finite-depth from full-tree optima. Historical files remain in
place and are labelled as mismatched evidence in the
[binary audit](binary-benchmark-audit.md).

For `T=0.15`, depth 2 selects approximately `1.06018744`; the full-tree
oracle selects approximately `1.08236282`. The former leaves **19.48%
excess full-tree variance**, although its second moment is only about
0.0076% above the minimum. This illustrates why a visually close moment
curve can still miss a material variance improvement. Oracle identities,
cutoff convergence and untruncated Monte Carlo checks are recorded in the
audit; these binary quantities do not transfer to Allen–Cahn.

## 4. Replicated accuracy versus total cost

The [cost protocol](rate-cost-protocol.md) was frozen before calibration
and evaluation. Six existing solver variants were evaluated on the wave
at `T=0.05`, grid `[-2,-1,0,1,2]`, with 20 independent replicates per variant
in each of two phases. All 6,000,000 fixed-size trees and 10,833,300
calibrated-budget trees completed, producing 240 profiles.

At fixed `N=10000` per point, selected-rate/terminal-proposal sampling had
26.4% lower observed aggregate RMSE than default, but its median total
cost was 2.22 times default once one-time tuning was charged. With separate
calibration used to allocate a common **predicted** total budget, aggregate
RMSEs were:

| Setting | Observed aggregate RMSE |
|---|---:|
| Short-time λ = 0.75, uniform q | 0.00054436 |
| Default λ = 1, uniform q | 0.00058338 |
| Selected λ, uniform q | 0.00074607 |
| Selected λ, terminal q | 0.00071137 |

All six settings, complete replicate distributions, pointwise errors and
actual timings are in the [results](rate-cost-results.md) and
[raw/summary artifacts](rate-cost-benchmark/summary.json). The simple
short-time rate was the strongest observed baseline in the budget phase.
The terminal proxy's incremental benefit was not established.

The budget is predicted from median calibration timing, not a proved
expected cost or identical realized runtime. Other research processes were
active; actual median total costs were `0.1651–0.1727 s` against a predicted
`0.1787 s`, with individual runs up to `0.4091 s`. The comparison does not
support precise hardware speed or population-significance claims. Policy
reuse could amortize setup, but that needs a separately specified workload.

## 5. Lean coverage and verification boundary

Three new modules contain **16 checked public algebra/order theorems**, plus
two private helpers in the convex-enclosure module:

- [RateCertificate.lean](../../../formal/EstimatorIntegrity/RateCertificate.lean):
  five conditional transfer lemmas for numerical/depth/optimization errors,
  infimum bounds, common-mean variance differences and interval/exterior
  coverage.
- [AllenCahnBounds.lean](../../../formal/EstimatorIntegrity/AllenCahnBounds.lean):
  six lemmas for polynomial/field positivity and monotonicity, rate-interval
  domination and the postfixed-box slope inequality.

- [ConvexEnclosure.lean](../../../formal/EstimatorIntegrity/ConvexEnclosure.lean):
  five public secant/exterior/pointwise-envelope lemmas and two private
  algebraic helpers. Convexity and correct finite endpoint enclosures are
  assumptions; the cell-envelope minimization algorithm is not formalized.

They do not formalize the stochastic moment correspondence, Brownian
motion, ODE comparison/existence, rational-program soundness, concrete
witness numbers, quadrature error, or empirical confidence statements.
The [proof registry](../proof-registry.md) lists the exact declarations and
omissions. Classical axioms reported by the Lean audit were only
`propext`, `Classical.choice` and `Quot.sound`; no project-specific axioms
or proof holes were introduced in these modules.

The latest root verification ran `python -m pytest -q`: **226 passed,
14 deselected**, in 53.47 seconds, including nine new wave-certificate
tests. The full `lake build`, including the new convex-enclosure module,
completed **3,390 jobs without warnings**. Its five public declarations
also passed the standard-axiom audit. The corrected binary suite separately
passed 14 tests. The cost artifact integrity audit passed and its figures
were visually inspected.

During this documentation checkpoint, the saved rational witness archive
was rechecked directly, and the global gap, exterior exclusion and all
reported wave tail values were recomputed from exact archived fractions:

```sh
/opt/miniconda3/envs/parabolab/bin/python examples/certified_allen_cahn_rate.py --verify docs/research/results/rate-certificate/witnesses.json.gz
```

Output: `all_witnesses_valid: true`. The saved wave archive also rechecked
successfully; its digest, ten point intervals, global/historical gaps and
exterior exclusion were recomputed from exact fractions. The final formal
build has passed, and the separate conventional mean-identification proof
now discharges the variance interpretation for these benchmarks. Practical next work is
a prespecified amortization or profile-objective comparison against the
inexpensive short-time baseline, with continuation-aware proposals and
the other research directions still open. This checkpoint does not
complete the entire research plan on its own. Its prescribed follow-up
was subsequently completed in the profile-efficiency checkpoint; the
dated integration update above supersedes the original merge hold.
