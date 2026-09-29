# T35 — two-barrier sampler implementation and execution

Date: 2026-09-28  
Status: **PASS** for the fixed implementation, deterministic preflight,
official diagnostics, strict-reference gate, and all 63 primary cells.

This task implements and executes the experiment frozen in
`02d-two-barrier-experiment-protocol.md`, SHA-256
`605eda24574bfb7e44dc997c185836d2a54311c18344e0be4c005674e00beda9`.
It does not alter the protocol, theory, Lean files, reference producer,
existing numerical work, or evidence canvas.

## Owned implementation and artifact

- `numerics/two_barrier_sampler.py`, SHA-256
  `89eafa2cec16c220eb1e049146f21066b3608c8c35e9418e322d40a306afbce0`
- `numerics/run_two_barrier.py`, SHA-256
  `afef0df8ff73608ccb9bbfb644aa2a0846065a762dc4463cc4581014a48b5ed1`
- `numerics/test_two_barrier_sampler.py`, SHA-256
  `0384f39390ea63807a39b1cdd12fe5fba36736ec09b4626ac5e48d8a2dbdce5f`
- `artifacts/two-barrier/sampler-v1/`: 717 files, approximately 14 MiB.

The mathematical sampler imports no deterministic-reference module. The
driver reads the frozen `reference-v1` files only for the primary gate and
post-sampling comparison.

## Correspondence with the reviewed construction

The sampler uses the limiting clock's `8/15` leaf atom and `7/15` event
probability. Event proposals use

```text
y = U/2
zeta = (y + sqrt(y^2 + 4y))/2
d = (1-U)(1+zeta)/(1+zeta-U/2)
q_event = d/(20/9-3d)
s = -log(q_event)/2.
```

Leaves and events with `s<T` are accepted; events with `s>=T` are rejected
without spatial work or children. The binary branch probability
`3(1+zeta)/(2(2+zeta))` is evaluated at the accepted event time. Children
receive remaining time `s` and the same Brownian branch location, followed
by fresh independent descendant draws. The evaluator uses an explicit stack
and has no node or depth cutoff.

Leaves return `(v-m)/(M-m)`. Binary vertices use the multiaffine OR rule and
ternary vertices use the multiaffine majority rule. A completed root returns
the scaled defect directly as `R_M(T) Z + R_m(T) (1-Z)`; it never subtracts a
computed PDE value from one. The exact `T=0` shortcut returns
`Z=(v(x)-m)/(M-m)` and `W=1-v(x)`, one leaf/node, and no clock trials.

Every root checks the three integer tree identities, the positive-time
proposal identity, the normalized range, the local scaled barrier interval,
and the global `[1/4,3/2]` interval. Values are never clipped.

## Pre-freeze development and review corrections

Development tests were kept separate from official diagnostic counts. An
initial nine-test run passed. The final suite added driver/RNG/reference
interface checks and passed all 13 tests. Its endpoint test evaluates 16-root
prefixes from each reserved endpoint stream as a development check only;
those roots are not counted among the 1,792 official endpoint roots.

The source-correspondence review requested and verified four corrections
before the artifact was frozen:

1. Rounded `zeta` may equal `z0` or `1` at a binary64 edge input even though
   the exact-real value is strict. The implementation retains the event,
   applies an explicit `8*ulp(1)` diagnostic tolerance to the rounded
   intermediate, and still requires positive `d`, denominator, `q_event`,
   and event time. It never clips or drops the draw.
2. The inverse preflight uses the frozen combined test
   `abs(error) <= 5e-14 + 5e-14*abs(target)` for each quantity. Relative error
   is recorded but is not a standalone gate for the event time tending to
   zero as `U` approaches the leaf threshold.
3. The reference loader requires exact status `PASS`, all five documented
   reference booleans, matching summary/NPZ arrays, and producer
   `k64_strict`. This handles the actual frozen T36 schema rather than an
   inferred lowercase status.
4. Primary `started_utc` is captured before sampling begins.

After those changes, root read the complete sampler and driver paths and
gave correspondence clearance. No source changed after the freeze.

## Immutable freeze and deterministic preflight

`execution_manifest.json` was written before any official diagnostics. It
records the environment, binary64 contract, commands, 22 source/gate hashes,
the frozen reference snapshot, the exact PCG64 version and initial state for
all 93 official and preflight streams, and every fixed preflight case.

The final 13-test suite was rerun during preparation and preserved in
`development_unit_tests.log`. The immutable preflight then checked four
inverse inputs, including `nextafter(8/15,1)` and `nextafter(1,0)`, against an
independent 100-digit implementation. Its maximum absolute discrepancy was
`4.440892098500626e-16`. Strict remaining-time direction checks passed.
Another 192 smooth roots covered the four preflight horizons and three query
locations; every count/range invariant passed and no coefficient-limit
substitution occurred.

## First-run official diagnostics

All frozen diagnostics ran once and passed. There was no selected rerun.

| Diagnostic | Fixed sample | Observed discrepancy | Fixed threshold |
|---|---:|---:|---:|
| Clock CDF, `T=1/4` | 100,000 accepted clocks | `0.0006498652707990216` | `0.008517234803187071` |
| Clock CDF, `T=1` | 100,000 accepted clocks | `0.002104354508092099` | `0.008517234803187071` |
| Clock CDF, `T=4` | 100,000 accepted clocks | `0.0028964582718358223` | `0.008517234803187071` |
| Constant `v=5/8`, `T=4` | 100,000 roots | `0.0013946296931109936` | `0.010646543503983839` |
| Endpoint constants | 1,792 roots | maximum `4.440892098500626e-16` | `1e-12` |

The clock groups used 384,448 limiting proposals in total: 300,000 accepted
proposals and 84,448 rejections. The raw artifact retains all 300,000
accepted-clock outcomes and proposal counts. It also retains every one of the
101,792 diagnostic PDE roots. There were no exact-zero uniform redraws and
no coefficient-limit substitutions.

The official diagnostic stage took `2.066328375134617` seconds. Passing these
finite checks is a diagnostic of the fixed floating implementation, not a
distributional proof or floating-bias certificate.

## Reference gate and primary execution

Before primary sampling, the driver rechecked the frozen sources and required
the independent reference's uppercase `PASS` status, preflight, all six solver
runs, refinement, shapes, and overall gate. The summary arrays exactly match
`reference.npz`, whose strict array is the `k64_strict` producer. The maximum
21-query refinement discrepancy was `2.282851685464493e-11`, below the fixed
`1e-8` gate.

All 63 primary cells completed their fixed 10,000 roots, for 630,000 roots.
Each cell has ten ordered, append-only 1,000-root NPZ chunks plus metadata;
there are 630 primary chunks. The largest sampling time for a cell was
`0.3037436972372234` seconds, so no 120-second safeguard fired. Total sampling
time across cells was `5.78205124149099` seconds, processing/I/O time was
`1.6537146545015275` seconds, and primary wall time was
`7.993458749726415` seconds.

The fixed sampling times for all 21 queries were:

| Seed | Sampling seconds |
|---:|---:|
| 2026092831 | `2.127089599147439` |
| 2026092832 | `1.890721632167697` |
| 2026092833 | `1.764240010175854` |

The predesignated `k16_loose` deterministic comparator recorded one solve
plus all 21 queries as `0.09698483301326632` seconds. These are timings of the
fixed implementations with different accuracy contracts. They do not imply
an equal-accuracy optimization, speedup claim, or general solver ranking.

Across primary roots, the largest tree had 33 nodes and the largest clock
trial count was 49. The aggregate cell-weighted means were approximately
`2.227519047619047` nodes and `2.7776301587301573` proposals. The reviewed
ideal expectation bounds are approximately `2.8273277230987155` and
`5.301239480810091`; observed sample means below them do not prove those
expectation bounds.

All nine time-zero cells reproduced the exact initial values and left their
PCG64 states unchanged. Across the full primary run there were no exact-zero
redraws, coefficient-limit substitutions, incomplete roots, or failed cells.
The physical factor at `T=256` was positive binary64,
`exp(-512) = 4.377491037053051e-223`.

## Fixed error outcome

The largest absolute signed relative error was
`0.016548194032477773`, for seed `2026092832`, `T=16`, `x=0`.
The largest three-seed RMS was `0.010253539797496892`, also at `T=16`,
`x=0`, with signed errors

```text
2026092831  -0.00031779009592704737
2026092832  -0.016548194032477773
2026092833  -0.006439061954582791
```

This is the only one of the 21 three-seed RMS values above 1%. It is not a
protocol failure. The reviewed `100/189` relative-variance bound gives an
ideal repeated-ensemble RMS bound (`0.00727392967453308` at `N=10000`), not a
hard bound on every realized error, the empirical RMS of only three seed
means, or the floating implementation. The fixed outcome is retained without
changing a seed, sample size, case, threshold, or parameter.

## Post-execution raw audit

A read-only audit reloaded all raw files and passed the following checks:

- 63 complete cells, 630,000 roots, and 630 contiguous chunks of at most
  1,000 roots;
- every integer tree identity and positive-time proposal identity;
- every normalized, local barrier, and global output-range check;
- exact parity of recomputed cell means, standard deviations, and signed
  errors with the summary;
- exact initial PCG64 state reconstruction from each entropy/spawn key;
- all diagnostic and primary raw-file hashes chained through their summaries;
- all frozen source hashes and reference/diagnostic gate hashes; and
- no failure artifact.

The analytic harmonic-center and mean-ODE comparator tabulation and all
scientific figures remain assigned to the root synthesis. The strict
reference values, fixed deterministic timing comparator, complete raw roots,
and metadata needed for that synthesis are preserved here.

## Hash chain

| File | SHA-256 |
|---|---|
| `execution_manifest.json` | `8d08a3d9043c40e61868a3c8def8e75bf94d9d87b5f31b1de61986c13b7132b6` |
| `preflight_results.json` | `f944959771b8cf59b6d22113145ace8784b7523d6bf2d1c4be51ed2b9d039c6b` |
| `development_unit_tests.log` | `064c6de0575f7c63f1d38bb52de00f8b26dedaf5152af592ba60a778f24989c4` |
| `diagnostics_summary.json` | `75ed4c01ad9fa02d54762b168dd79ee490375de7b06f6b751de0ca3f5e6da2a0` |
| `primary_gate.json` | `225dd1a07e041fed8dc4829163f142a20dc8508c81b1a1ed56f2c22c2fbcfe50` |
| `primary_summary.json` | `36a531df750b4fae5762a588c0acaa765c13c2fe2c613a5b44bc6f86cb8f0542` |

This pass certifies execution of the fixed finite experiment and consistency
of its preserved records. It is not a numerical proof for all horizons, a
finite-bit unbiasedness certificate, or an originality, optimality, or
speedup claim.
