# T14 independent artifact audit and numerical summary

Status: **passed**.  The independent auditor streamed all 600 primary stage
archives, recomputed the mathematical outputs from the raw arrays, verified
the archive provenance, and found no contract failure.  The resulting summary
and figure describe three prescribed paths; they do not estimate rare tails,
produce a confidence interval, or convert the theorem into a simultaneous
all-times pathwise statement.

## Independent audit

`numerics/audit_dynamic.py` imports neither the producer nor its interface,
sampler, projection helper, or reference Python module.  It reconstructs the
Gram matrix from the 80-decimal elliptic-moment recurrence and independently
projects each raw coefficient vector by minimizing the quadratic objective on
all six closed polygon segments (plus the feasible interior).

All 56 aggregate audit checks passed:

- all three manifests have exact file sets and valid SHA-256 entries;
- all 342 initially protected files are present with their original hashes;
- all 600 stages are complete, with 100,000 roots per stage and exactly
  60,000,000 roots in total;
- every raw position lies in `[0,L)`, every tree value is finite, and every
  node count is positive;
- the first PCG64 state matches `default_rng(seed)`, every saved after-state
  equals the next stage's before-state, and replaying the uniform position draw
  from every before-state reproduces all 60 million stored positions exactly;
- every prior coefficient pair equals the preceding stored projected pair,
  starting exactly from `(0.9,0.9)`;
- every projected pair is feasible, and the smallest independent
  variational-inequality value is `-2.4575e-19`;
- all raw moments, covariances, node and branch summaries, terminal counts,
  `bhat`, raw coefficients, and projected coefficients agree with the archived
  records;
- all four normalized-spatial errors were recomputed on the independent
  16,384-point grid against the frozen reference.

The maximum absolute differences were zero for the Gram matrix, `bhat`, raw
and projected coefficients, projection diagnostics, all stored moments and
covariances, and all work summaries.  The only nonzero maximum was
`3.469446951953614e-18` for a recomputed error field.  The complete streaming
audit took `20.56 s` with single-threaded BLAS.

## Primary numerical result

| Seed | Roots | Nodes | Projections | Whole primary-path time | Maximum observed MC error |
|---:|---:|---:|---:|---:|---:|
| 2026092801 | 20,000,000 | 23,601,272 | 179 / 200 | 41.38 s | 0.006296 |
| 2026092802 | 20,000,000 | 23,596,128 | 169 / 200 | 42.54 s | 0.004398 |
| 2026092803 | 20,000,000 | 23,603,771 | 166 / 200 | 40.89 s | 0.006552 |

The aggregate path contains 70,801,171 visited nodes.  Projection was active
at 514 of 600 stages (`85.67%`).  The maximum three-seed empirical RMS was
`0.00468048` at stage 159, `T=12.72`; the maximum individual error was
`0.00655173` for seed 2026092803 at the same endpoint.  Every observed error
is below `0.02`, but the observed maximum is not an ensemble bound and does
not verify a simultaneous-time event.

The largest observed per-stage sample mean of `H^2` was `0.0584929`.  This is
a raw sample diagnostic.  It is not a proof or estimate of the imported
population second-moment bound under rare tails.

The compact summary contains all 201 times, with the exact initialization at
time zero, each seed's errors and coefficient trajectory, empirical RMS,
mean, minimum, maximum, range and sample standard deviation, projection
indicators, second moments, root/node counts, and timing series.  The selected
positive endpoints are:

| T | MC errors by seed | empirical RMS | mean | range | g | .95g | .9g |
|---:|---|---:|---:|---:|---:|---:|---:|
| 0.08 | 0.000160, 0.000305, 0.000212 | 0.000233 | 0.000226 | 0.000144 | 0.021678 | 0.010733 | 0.000220 |
| 0.40 | 0.000249, 0.000265, 0.000660 | 0.000435 | 0.000391 | 0.000411 | 0.020843 | 0.009897 | 0.001055 |
| 1.04 | 0.002005, 0.000272, 0.000192 | 0.001173 | 0.000823 | 0.001813 | 0.019254 | 0.008308 | 0.002640 |
| 2.00 | 0.000932, 0.001231, 0.001732 | 0.001339 | 0.001298 | 0.000801 | 0.017066 | 0.006121 | 0.004827 |
| 4.00 | 0.001279, 0.000299, 0.001996 | 0.001379 | 0.001191 | 0.001697 | 0.013198 | 0.002253 | 0.008694 |
| 8.00 | 0.002812, 0.001911, 0.000403 | 0.001977 | 0.001709 | 0.002410 | 0.007752 | 0.003194 | 0.014140 |
| 16.00 | 0.002340, 0.002419, 0.005124 | 0.003540 | 0.003294 | 0.002785 | 0.002564 | 0.008382 | 0.019328 |

At time zero, the mathematical MC error is recorded as exactly zero because
the stored interface equals the initial datum.  Its discrepancy from the
finite floating-point reference proxy is retained separately in the JSON.

## Honest comparator and cost result

Over the full interval `[0,16]`, including time zero, the fixed midpoint
`.95g` has maximum measured error `0.0109458`.  Over the 200 positive stages
its maximum is `0.0107325` at `T=0.08`.  Thus the midpoint already meets the
`0.02` target, in agreement with the pre-data order-band bound.  The fixed
initial datum `.9g` also has maximum measured error `0.0193278` on this finite
window.  The continuation paths are more accurate numerically, but the stated
accuracy target does not establish a competitive advantage over these simple
baselines.

Raw sampling took `29.34 s`, the sum of recorded stage times was `61.66 s`,
and the sum of the three primary-path elapsed times was `124.81 s`.  The last
quantity excludes preflight checks, deterministic-reference validation, this
audit, and summary/plot generation.  One strict mode-63 deterministic solve
took `1.538 s`; each individual MC path therefore took `26.6–27.7` times as
long.  Even the full six-solve deterministic validation cost `3.735 s`, so
each MC path took `10.9–11.4` times as long.  The spectral method is plainly
faster on this smooth one-dimensional problem with a known equilibrium.

## Reproducible outputs

- `numerics/audit_dynamic.json`: complete pass/fail record, independent Gram,
  maximum differences, hashes, and all recomputed per-seed series;
- `numerics/summary_dynamic.json`: compact 201-time summary, selected
  endpoints, explicit scope statements, cost comparisons, hashes, and
  regeneration commands;
- `numerics/audit_dynamic.log` and `numerics/summary_dynamic.log`: concise
  captured command summaries;
- `dynamic-results.png` and `dynamic-results.svg`: inspected 2-by-2 scientific
  figure showing errors and baselines, coefficient paths, sample second
  moments, and cumulative nodes/stage time.

SHA-256 records:

- `audit_dynamic.py`:
  `8599add4d8513336e4555f49db6f1b4f019b93643ee2f4463e08b94fdc3aa8a5`
- `summarize_dynamic.py`:
  `4de7bc3ec8189f00ee57658aaf78e8db22674b47a3a228bbeb9ff9a183cb1c3d`
- `audit_dynamic.json`:
  `7ae549873b064269f5b3da47923bbdb9546ddd41a6ca1f12e2fc1ae73e9177b0`
- `summary_dynamic.json`:
  `cea9d280cf8d37681c00aca3a5ecc7697ecb51ec7103702dc5d7615c231712c5`
- PNG:
  `97938d53de4185523b358d7da4be70d8afb052e8f280c1b86256d3ca454a379c`
- SVG:
  `bb6d57259c2550bd2c376091518f43e585ef2bf80370581f3cd43b44a6c7bb2f`
- seed-manifest hashes for 2026092801, 2026092802, and 2026092803:
  `a334a03c6d5bb98e8e814c185d70d81276ef91a985dadab7897bc00ed8a7fe62`,
  `8bed8edc9f6eb35419a70e527416fe2ae25663ea77beb9c66c14409967447e31`,
  and `7000a8470c8153a08783eaedf889e5f9ecaec054d83a9f176dc8f1c88ab8af0c`.

Regenerate with:

```text
/opt/miniconda3/envs/parabolab/bin/python docs/research/runs/2026-09-28-dynamic-continuation/numerics/audit_dynamic.py
MPLCONFIGDIR=/tmp/parabolab-mpl /opt/miniconda3/envs/parabolab/bin/python docs/research/runs/2026-09-28-dynamic-continuation/numerics/summarize_dynamic.py
```

The figure's `.02` line is labeled as the theorem envelope, and its footnote
states the correct per-endpoint ensemble interpretation.  The figure and JSON
also label the second moments as sample diagnostics rather than population
bounds.
