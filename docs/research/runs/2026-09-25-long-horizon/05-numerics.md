# Numerical evidence and reproducibility

Completed 25–26 September 2026, after the conventional theory review and the
scoped Lean build/axiom gate. The initial protocol and moving-front amendment
were fixed before implementation. Mathematical claims are in
[04-theory.md](04-theory.md); this record distinguishes rational certificates,
floating deterministic calculations, and Monte Carlo observations.

## Raw estimator: boundaries and longer-time rate selection

[raw_experiment.py](numerics/raw_experiment.py) produces
[raw-results.json](numerics/raw-results.json),
[boundary-certificates.json](numerics/boundary-certificates.json),
[wave-results.json](numerics/wave-results.json), and
[raw-samples.npz](numerics/raw-samples.npz).

The prior rational enclosure of the reciprocal-polynomial integral C was
independently regenerated with the previous witness verifier, which passed
all checks; see [prior-flat-verify.log](numerics/prior-flat-verify.log).
New rational Machin/atan and atanh series bounds enclose the absolute boundary
`(3*pi-2*log(3))/5` in an interval of width `7.58349e-21`.
The approximate value is `1.4455106766866320665`.
Rational exponential bounds enclose the dimensionless horizon maximizer in
`[1.980,1.981]` and prove the following upper caps:

| Common first-label probability | Certified upper bound on any finite-L2 horizon | Floating maximum of the exact formula | Floating rate at maximum |
|---|---:|---:|---:|
| p=.5 | 203/288 < .705 | .7038899675 | 2.2640247053 |
| p=.95 | 1943/2000 < .972 | .9702453629 | 1.6424961489 |
| p→1 | 17951/18000 < 1 | not needed | not needed |

The boundary itself is excluded. The limiting p=1 bound also bounds every
supported p<1; no unsupported p=1 proposal is used in the sampler. The
decimal maxima use floating quadrature `C=1.5301212285131`, not a sharper
validated enclosure.

There are 24 flat policy/horizon rows, three rate baselines per row
(`1`, `.745`, and `-log(.95)/T`), plus full five-field moment minimization over
the feasible common-rate interval. Optimizations use log(rate) and two ODE
tolerances, `1e-8` and `1e-10`; they are floating scalar optimizations, not
certified global minimizers. Uniform-policy optima change from `.743670` at
T=.05 to `1.159118` at T=.5 and `2.207099` at T=.7. At the last of these,
the largest same-rate ODE tolerance difference is about `1.22e-7`.
The 41 available independent scalar reconstructions agree with the five-field
ODE within a maximum scale-normalized difference `2.61687e-9`.

The absolute-moment curve is computed independently of the rate optimizer.
Its implicit positive scalar equation supplies L2's proposal-independent
lower bound; values at and after the absolute ceiling are explicitly marked
nonintegrable, never replaced by finite ODE stop values.

Six raw Monte Carlo batches use the existing exact-zero-code pruning,
lambda=1, uniform policy, T=`.05,.5,.7,1,1.5,2`, N=4096 each, and seeds
`40260925 + row_index`. All 24,576 scheduled values happened to be finite.
Nevertheless, the last four batches have mathematically infinite variance,
and the last two lack absolute integrability. Their empirical means and
variances remain diagnostic only. At T=2 the empirical mean is `1.694407`
against PDE value `.973609`; its finite sample variance `3293.17` is not an
estimate with ordinary finite-variance guarantees. No ordinary confidence
coverage is claimed for these batches.

## Nonconstant raw-wave moment diagnostic

The full six-field positive moment PDE is discretized on `[-12,12]` with
dx=`.1,.05`, rates `.75,1,2`, common policies `.5,.95`, and RK4 with
`dt <= .2 dx²`. Scheduled horizons are `.05,.1,.25,.5,.75,1`.
All 12 configurations and all 72 scheduled rows are retained. Each
configuration triggers the predeclared safety condition (a field above
`1e12` or nonfinite) at a time between approximately `.383` and `.686`.
There are 44 reached rows and 28 `not_reached` rows. All 12 configurations
reach .25, eight reach .5, and none reaches .75.

Among the 22 available pairs of meshes, the maximum absolute difference in
the reported root second moment is `3.69521e-5`. The field named
`relative_to_fine` actually divides by `max(1,abs(fine))`; it is a
scale-normalized discrepancy. The largest available true relative discrepancy
is about `4.31236e-5`. Initial-field reconstruction error is zero; the
maximum reached F3 relative error against its independent expression is
`3.5674e-9`. These are internal diagnostics on a truncated domain. Neither
two-mesh agreement nor a safety stop certifies a spatial explosion boundary.

## Complete bounded-tree experiment

[bounded_experiment.py](numerics/bounded_experiment.py) follows
[protocol.json](numerics/protocol.json) and the
[pre-code moving-front amendment](numerics/protocol-amendment-before-code.md).
It runs rate 2 at T=`.05,.25,.5,1,1.5,2`, and rates 2.5 and 3 at
T=`.25,.5,1`. Each pair has a flat point, three fixed wave points
`-2,0,2`, and a moving wave-front point `x=1.5T`, where the exact value stays
at `-.5`. There are 60 rows, 2048 complete roots per row, root batches of
32, and seeds `20260925 + row_index`. No root, outlier, or unfinished tree
is discarded; no node/depth cutoff or value clipping is used.

[bounded-raw.npz](numerics/bounded-raw.npz) retains all values, node counts
and root-branch flags in arrays of shape `(60,2048)`. The canonical run
completed 122,880 roots and 60,696,849 nodes. The generation elapsed time
through the raw-archive write is 7.856 seconds on macOS arm64, Python
3.11.15/NumPy 2.4.6; the 60 sampler timings sum to 7.759 seconds. The former
includes the sampling loop, row logging and NPZ serialization, but excludes
subsequent source hashing and result-JSON writing. Neither is an end-to-end
research cost or a hardware-independent benchmark; imports, theory, formal
compilation, deterministic reference construction and report generation are
also excluded.
The largest tree has 76,237
nodes. The archive SHA-256 is
`a05f404895daf22a02abb4056c15975b41d414ef3b5ec0cd4267199c30e4b74a`.

| Rate-2 moving front | Estimate (exact -.5) | Sample variance | Root branched | Observed / expected nodes per root |
|---|---:|---:|---:|---:|
| T=.05 | -.498158 | .006035 | 8.69% | 1.30 / 1.33 |
| T=.5 | -.502716 | .041599 | 63.38% | 9.90 / 10.58 |
| T=1 | -.497475 | .057848 | 87.50% | 81.51 / 81.40 |
| T=1.5 | -.497277 | .066256 | 95.21% | 596.03 / 604.64 |
| T=2 | -.492524 | .066517 | 97.80% | 4077.62 / 4470.94 |

The pointwise 95% Hoeffding radius is
`sqrt(2 log(40)/2048)=.0600202`; the simultaneous 95% union-bound radius
across the 60 prescheduled rows is `.0871826`. Every interval contains its
exact PDE value. The largest realized absolute mean error is `.00747562`.
Normal standard errors are diagnostics only. Hoeffding theory here applies
to the exact bounded estimator: floating evaluation error is not enclosed.
Three archived outputs equal `-1.0000000000000002`, one binary64 ulp below
the exact interval. They were retained without clipping. This is not an
end-to-end machine-certified confidence interval.

[bounded-audit.json](numerics/bounded-audit.json) independently recomputes
sample summaries, full-ternary count congruence, root flags, coverage and
floating overshoots from the raw arrays. The separate reproducible audit
driver is [audit_bounded.py](numerics/audit_bounded.py).
[check_bounded_theory.py](numerics/check_bounded_theory.py) checks 120
finite-support child laws and 9,720 exact rational kernel evaluations,
including second-moment identities and rate ordering. Independent flat
second-moment ODE solvers agree within `7.033e-10`.
At flat T=1, increasing the bounded rate from 2 to 3 changes the calculated
variance from `.0257682` to `.0127122`, while expected nodes increase from
`81.3972` to `604.6432`; variance times expected nodes increases from about
`2.0975` to `7.6863`. This comparison does not establish a global
variance-cost optimum or a runtime win over the differently pruned raw tree.

## Corrections, unsuccessful checks and provenance limits

1. The first independent scalar check incorrectly reconstructed the raw Id
   moment as an affine function of its integrating-factor scalar variable.
   It failed with relative discrepancy `1.53813`. The primary five-field
   equations, optimizer and raw sampler were unaffected. The independent
   equation was corrected to `Id_tilde'=P(v)/lambda`, with
   `v'=exp(lambda*t)P(v)/(lambda*p)`, and all artifacts regenerated. Initial
   source/result hashes and the failed discrepancy remain in
   `raw-results.json:implementation_corrections`; original file bytes were
   not separately archived. The final verifier passes all 16 checks.
2. Both binary64 absolute-boundary calculations fall outside the rational
   interval of width `7.58e-21`, smaller than a binary64 ulp. These two
   observations remain **false** in the JSON. A 100-digit floating value
   falls inside, and the quadrature error bar intersects the interval. The
   rational series bounds provide the certificate; precision diagnostics do
   not replace it.
3. Review found a missing finite-horizon input guard in the new sampler.
   It was added and tested. The canonical rerun produced a byte-identical
   raw archive, but overwrote the initial timing JSON/log. The initial
   manifest retains the known first total time, timestamps and archive hash
   without reconstructing unavailable per-row timings. See
   [bounded-initial-execution-manifest.json](numerics/bounded-initial-execution-manifest.json).
4. All 12 raw-wave safety stops and all 28 unreached scheduled rows remain in
   the evidence. They are expected retained protocol outcomes, not hidden
   verifier failures.

## Commands and checks

Run from the repository root using the existing environment:

```bash
/opt/miniconda3/envs/parabolab/bin/python docs/research/runs/2026-09-25-long-horizon/numerics/raw_experiment.py --verify
/opt/miniconda3/envs/parabolab/bin/python docs/research/runs/2026-09-25-long-horizon/numerics/audit_bounded.py
/opt/miniconda3/envs/parabolab/bin/python -m pytest -q
```

Generation is reproducible with `raw_experiment.py` without `--verify`,
`bounded_experiment.py`, and `check_bounded_theory.py`; running generation
again replaces canonical output files and timing metadata. Prefer the
verification commands when inspecting this run; they preserve the primary
experiment data, while the bounded audit refreshes its separate audit files.
Source hashes and package versions accompany both primary result JSONs.
The exact commands for Lean are retained in [lean/build.log](lean/build.log).

The full default Python suite passed **274 tests, 14 deselected**, in 51.83
seconds after the final production fix. The selected-out tests were not run
in that invocation. Both Lean modules and the aggregate build passed; all
11 theorem axiom checks use only standard axioms. See
[python-tests.log](python-tests.log), [06-formalization.md](06-formalization.md),
and [10-correspondence-review.md](10-correspondence-review.md).
