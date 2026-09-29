# T09 — dynamic producer implementation and primary execution

Date: 28 September 2026. Status: implementation, prespecified execution, and
post-run archive audit complete. This note reports a floating-point Monte Carlo
experiment. Three paths do not estimate rare tails or establish a simultaneous
all-times confidence event, and the deterministic reference has no rigorous
rounding or discretization enclosure.

## Implemented contract

`numerics/dynamic_interface.py` implements the fixed Jacobi profile, the basis

    b = (g(1-g^2/a), g^3/a),       a = 2/21,

the value/derivative terminal

    v = g[c0 + (c1-c0)g^2/a],
    v' = g'[c0 + 3(c1-c0)g^2/a],

and the G-metric projection onto the prescribed hexagon. The projection checks
the unconstrained point when it is feasible and the quadratic minimizer on
each of the six closed edges. It does not use coordinate clipping.

`numerics/run_dynamic.py` loads the prior sampler through its explicit path and
requires SHA-256
`994e892784f36930fa63649aa749985448df75887f9096f6c40c142b46ff108a`.
It starts from `c=(.9,.9)`, draws 100,000 fresh uniform roots on `[0,L)` per
stage, runs every started raw tree to completion, computes
`bhat=mean(H*b(X))`, solves `G raw_c=bhat`, and projects `raw_c` in the G
metric. The next terminal closes only over the preceding stored coefficient
pair. The exact evolving solution is absent from the terminal callback and is
loaded from the accepted reference artifact only after tree sampling to
calculate errors.

Each stage archive preserves `X`, unmodified `H`, node counts, root-branch
flags, terminal-code counts, prior/raw/projected coefficients, `bhat`, G, RNG
states before and after the stage, source/reference hashes, timings, and all
four normalized-spatial RMS errors. Each seed directory was created only when
absent, contains source copies and a pre-sampling source record, and has an
SHA-256 manifest for every file other than the self-referential manifest.

## Preflight evidence

The Gram matrix obtained from the 80-decimal elliptic identity is

    [[0.0059329342220773405, 0.0059710936464823295],
     [0.0059710936464823295, 0.030049232873579173 ]].

Independent 80-decimal quadrature agrees after conversion to binary64, and a
262,144-point periodic grid differs by at most `4.17e-17`. Its eigenvalues are
`0.00453549272106896` and `0.031446674374587556`, giving condition number
`6.9334637510290085`. These are diagnostics, not rigorous enclosures.

Fixed inside/outside projection cases agree with an independent SciPy SLSQP
implementation. The implementation also passes direct variational-inequality
and idempotence checks. Independent centered differences check the analytic
terminal derivative, while dense-grid inner products check basis and
coefficient normalization. Source inspection and closure inspection show that
the terminal has only the frozen coefficient pair in its closure.

The new suite passed `15/15` tests. The unchanged old sampler and driver suite
passed `29/29` tests. The accepted independent reference has a maximum
empirical convergence floor `1.0560761786271712e-11`, below its `1e-9` gate.

## Primary execution

No run was retried or selected by its result. All three prescribed runs
finished far below the two-hour per-run cap.

| Seed | Roots | Nodes | Recorded seconds | Projections / 200 | Max MC error | Final MC error |
|---:|---:|---:|---:|---:|---:|---:|
| 2026092801 | 20,000,000 | 23,601,272 | 41.38 | 179 | 0.006296 | 0.002340 |
| 2026092802 | 20,000,000 | 23,596,128 | 42.54 | 169 | 0.004398 | 0.002419 |
| 2026092803 | 20,000,000 | 23,603,771 | 40.89 | 166 | 0.006552 | 0.005124 |

The total is exactly 60,000,000 roots, 70,801,171 visited nodes, and 600
completed stages. Projection was active at 514 of 600 stages. The largest
observed per-stage sample second moment of `H` was `0.058493`; this is an
empirical diagnostic and is not a proof of the imported `1/4` moment bound.

All 200 per-stage MC and comparator errors, coefficient paths, covariances,
second moments, work, and timings are in each seed's `progress.json`; the raw
observations are in the corresponding 200 NPZ files. Selected endpoints are:

| T | MC errors by seed | 3-seed empirical RMS | g | .95g | .9g |
|---:|---|---:|---:|---:|---:|
| 0.08 | 0.000160, 0.000305, 0.000212 | 0.000233 | 0.021678 | 0.010733 | 0.000220 |
| 0.40 | 0.000249, 0.000265, 0.000660 | 0.000435 | 0.020843 | 0.009897 | 0.001055 |
| 1.04 | 0.002005, 0.000272, 0.000192 | 0.001173 | 0.019254 | 0.008308 | 0.002640 |
| 2.00 | 0.000932, 0.001231, 0.001732 | 0.001339 | 0.017066 | 0.006121 | 0.004827 |
| 4.00 | 0.001279, 0.000299, 0.001996 | 0.001379 | 0.013198 | 0.002253 | 0.008694 |
| 8.00 | 0.002812, 0.001911, 0.000403 | 0.001977 | 0.007752 | 0.003194 | 0.014140 |
| 16.00 | 0.002340, 0.002419, 0.005124 | 0.003540 | 0.002564 | 0.008382 | 0.019328 |

The maximum three-seed empirical RMS over all 200 endpoints was `0.00468048`
at stage 159. The maximum individual MC error was `0.00655173`. Every observed
MC error is below `0.02`, but the experiment does not turn the theoretical
ensemble RMS statement into a pathwise or simultaneous confidence claim.

The fixed midpoint `.95g` has maximum measured error `0.0107326` and already
satisfies the pre-data analytic `<0.02` bound without simulation. Thus the
experiment validates the intended continuation mechanism and correspondence,
but its concrete accuracy target is not competitive with the prior order-band
baseline. The finest deterministic M63 reference solve took `1.54s`; even its
full setup and six validation solves took `3.73s`, compared with about `125s`
for the three MC paths. The MC method is not faster on this smooth
one-dimensional benchmark with a known equilibrium.

## Archive audit

A separate full readback audit hashed all 600 NPZ files and their companion
records, recomputed `bhat`, raw coefficients, and projected coefficients from
all 60 million stored observations, checked every position in `[0,L)`, checked
every `H` finite and every node count positive, verified the exact prior chain,
and recomputed all four errors on the 16,384-point grid. The largest difference
in recomputed `bhat`, raw coefficients, or projected coefficients was zero; the
largest error-field difference was `3.47e-18`. The largest floating
variational-inequality violation was `2.46e-19`. All 342 initially protected
files were present and unchanged.

Implementation source hashes are:

- `dynamic_interface.py`: `c15e7a4ebdd8e3838ec3302ed6bd67305fda41dfc7be8a34f3ebb55060493268`
- `run_dynamic.py`: `59a006e29b6b370d9d55b3a7fb6553b5ee94e1888be2babb78422ee0ef10b8db`
- `test_dynamic.py`: `3d4fc3b382f611fd51c90c666d3b88705045e846ebacd719531de0125122e673`

The command, Python/NumPy/SciPy versions, git revision, source copies, and
reference hashes are independently recorded in every seed's
`source-record.json`. `numerics/audit.log` contains the aggregate audit and
selected-endpoint values; the preflight, test, and primary command outputs are
preserved in the other T09 log files.
