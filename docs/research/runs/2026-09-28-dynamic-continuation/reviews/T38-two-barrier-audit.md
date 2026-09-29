# T38 independent two-barrier raw-evidence audit

**Status: PASS.** The frozen independent auditor passed **992/992 checks**. It read the raw producer and deterministic-reference artifacts directly and did not import `two_barrier_sampler.py`, `run_two_barrier.py`, or `two_barrier_reference.py`.

## Frozen execution

The auditor source was finalized before the audit, and `prepare` then froze SHA-256 hashes for all 734 audit inputs. `run` verified that complete snapshot before reading the evidence. The audit directory and both figure paths use exclusive creation and refuse overwrite; there is no failure artifact because the first frozen run completed successfully.

Commands:

```text
/opt/miniconda3/envs/parabolab/bin/python numerics/audit_two_barrier.py prepare
/opt/miniconda3/envs/parabolab/bin/python numerics/audit_two_barrier.py run
```

The commands above are relative to `docs/research/runs/2026-09-28-dynamic-continuation/`.

| Item | SHA-256 |
|---|---|
| `numerics/audit_two_barrier.py` | `0ffaa92c20cc56945d1bc0508085ce4ab31774672f54252c6a7bec8c1ed8e324` |
| `audit-v1/execution_manifest.json` | `655aaa245e99fb3e1b799f11ab1ec18cf91e3ffc7556466a03ce79f3c128e147` |
| `audit-v1/derived_tables.json` | `d24a0934ab95f303069e9970fc8efa0dcce81e054e1a5e3a305ffbf8106b5636` |
| `audit-v1/audit_summary.json` | `8a72f0cdf4320d90e95dbe2d63ac15a89341bbaf677259c9a3aadace0e3828e0` |
| `two-barrier-results.png` | `b0fad3b4acb5dae0a69ee9b86b389021f4be82f2d50e5b19853e3e9cdbe2b695` |
| `two-barrier-results.svg` | `361fdd75d577e381df87b2804b515a027bafb3eb30645308d39f3f5a5110f9f7` |

The original figure render used a logarithmic error axis, which did not display the exact zero RMS values at `T=0` or the exact zero mean-ODE error at `(T,x)=(0,pi/2)`. Those figures and hashes remain untouched. A presentation-only v2 was frozen from the same `derived_tables.json` and uses a symmetric-log error axis:

| Versioned presentation item | SHA-256 |
|---|---|
| `numerics/plot_two_barrier_v2.py` | `fd88c24111eb1487d0eeace4d7a1b3745dce93128dab57f7ccfa770b9c05eafa` |
| `figure-v2/execution_manifest.json` | `d327f7c4f8faac551df219ec43afc998f04d377d550ecad6b8a663e3d6cec2f7` |
| `figure-v2/render_qa.json` | `f3c31ec72f8697b929e8ee9500d137c88b088eee783fd486440464138b4b787b` |
| `two-barrier-results-v2.png` | `812bbba5bf93d6c5528d66e04acef455d2d63eb5b2e01a236e8ade471d6ca0ad` |
| `two-barrier-results-v2.svg` | `a32d270d30461757310f452ea6ca1b611f3ffd9e3ff6286711cf5a7287075406` |

The v2 render did not resample, rerun a PDE solve, or change any value. Its QA records three exact zero entries in the `(7,3)` RMS table and one exact zero in the mean-ODE comparison table. The v2 files are the recommended scientific figures.

The frozen protocol hash is `605eda24574bfb7e44dc997c185836d2a54311c18344e0be4c005674e00beda9`. All 342 paths in `initial-source-hashes.json` were present and unchanged. All 22 hashes in the producer source-and-gate snapshot matched, as did the three primary-gate hashes. The audit manifest additionally protects every raw producer file and every reference file read by this run.

## Raw-evidence results

The auditor checked all 63 fixed primary cells, all 630 ordered chunks, and all 630,000 primary roots. Every chunk hash matched its cell summary; chunk intervals were continuous, positive, no larger than 1,000 roots, and ended at 10,000 roots per cell. The independently recomputed total work was 1,403,337 tree nodes and 1,749,907 clock proposals. There were no coefficient-limit substitutions or zero redraws. The largest primary tree had 33 nodes, and the largest primary proposal count was 49.

Every archive had the exact expected raw fields and one-dimensional lengths. The audit independently checked

```text
N = L + I2 + I3,
N = 1 + 2 I2 + 3 I3,
L = 1 + I2 + 2 I3,
proposals = N + rejections  (T > 0),
W = R_3/4(T) Z + R_1/2(T) (1-Z),
R_c(T) = (c^-2 - 1) /
         [sqrt(1 + (c^-2 - 1)e^-2T) (1 + sqrt(1 + (c^-2 - 1)e^-2T))].
```

All identities, count nonnegativity, Boolean flag ranges, `Z` and `W` ranges, and stable-coefficient reconstructions passed. At `T=0`, all nine seed-query cells had their exact `Z=(1,1/2,0)`, `W=(1/4,3/8,1/2)`, one-node states, zero proposals, and unchanged RNG state.

### Post-freeze dtype correction

Source review after the immutable audit-v1 run found two schema-check details that needed an explicit supplement. The audit-v1 code treated `zero_redraws` as a `{0,1}` indicator even though it is an unbounded nonnegative count, and its nonnegativity check did not separately require integer dtypes. The overrestrictive upper bound did not affect the result because every observed zero-redraw count was exactly zero. Audit-v1 has not been edited or rerun.

The separate frozen supplement scanned the same 648 raw NPZ inputs: 630 primary chunks, 15 root diagnostic archives, and three clock archives. It checked 4,524 count arrays for integer dtype and nonnegative values, with no upper bound on `zero_redraws`, and checked 648 Boolean arrays separately. All count fields were `int64`, all `coefficient_limit_substitution` and clock `is_leaf` fields were `bool`, and the scan passed with zero failures. This supplemental PASS is not included in the original 992-check count.

| Dtype supplement item | SHA-256 |
|---|---|
| `numerics/check_two_barrier_dtypes.py` | `9a74bb4b94bc101ed1b82f730d0458fd940ed00dd28e901e335a6183f7eaf89a` |
| `figure-v2/dtype_scan_manifest.json` | `3e3f80d1fbaffd7fe3ffb62ab45cb15e28022381fc324a085d4d9a00ffd06947` |
| `figure-v2/dtype_scan.json` | `d22fde2bfd266ae06d2b29d540a288d753c20d2c6841ccd24c86f186580409f9` |

The 18 official diagnostic archives also passed: 300,000 accepted-clock observations, 100,000 nonendpoint constant-profile roots, and 1,792 endpoint roots. The independently recomputed maximum five-point clock-CDF discrepancies were:

| Horizon | Maximum discrepancy | Fixed threshold |
|---:|---:|---:|
| 0.25 | 0.000649865270799 | 0.008517234803187 |
| 1 | 0.002104354508092 | 0.008517234803187 |
| 4 | 0.002896458271835 | 0.008517234803187 |

The clock `zeta` values reconstructed from accepted times to at most `2.220446049250313e-16`. The nonendpoint constant-profile mean was `0.778299360561040`, versus the independently evaluated scalar target `0.779693990254151`; its absolute discrepancy `0.001394629693111` passed the fixed `0.010646543503984` threshold. All 14 endpoint archives equaled their independent scalar targets pathwise within the fixed tolerance; their observed maximum discrepancy was zero.

The audit reconstructed the fixed-key PCG64 initial states for all 81 official raw streams, 63 primary plus 18 diagnostic, with zero mismatches, and verified all 81 final-state records were present. It **did not independently replay the descendant draws inside the sampled trees**, so the RNG result is a fixed-stream state and raw-evidence audit rather than a second stochastic implementation.

## Reference and Monte Carlo results

The strict reference array had the exact `(7,3)` schema and was bitwise identical to the `K=64` strict query array. Direct cosine reconstruction from every retained coefficient array reproduced every stored query value exactly. Recomputed maximum 21-query discrepancies against the strict run ranged up to `2.282851685464493e-11`, passing the frozen `1e-8` refinement gate without rerunning any PDE solve.

The independently recomputed three-seed relative RMS diagnostics are:

| `T` | `x=0` | `x=pi/2` | `x=pi` |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 0.25 | 0.000397168 | 0.002165159 | 0.000588790 |
| 1 | 0.002203031 | 0.004378671 | 0.001759640 |
| 4 | 0.004179565 | 0.003369637 | 0.002398937 |
| 16 | 0.010253540 | 0.005127392 | 0.007902367 |
| 64 | 0.005207345 | 0.001906952 | 0.002340107 |
| 256 | 0.003884080 | 0.001522772 | 0.004990922 |

The maximum is `0.010253539797497` at `(T,x)=(16,0)`. Therefore the finite run does not support a statement that every point lies below 1%. This is not a protocol acceptance failure: the frozen gates concern artifact completeness, raw invariants, diagnostics, and deterministic-reference refinement. The largest individual signed relative error was `0.016548194032478`.

`derived_tables.json` retains all 63 seed-cell means, within-root standard deviations, signed relative errors, work means, maxima, and timings. It also retains all 21 RMS values and all 21 comparisons for each prespecified analytic baseline. The baselines were evaluated independently as

```text
harmonic center = 2 R_1/2(T) R_3/4(T) / (R_1/2(T) + R_3/4(T)),
mean ODE       = R_5/8(T).
```

Their largest absolute relative errors over the 21 fixed points were `0.4202997785189998` and `0.5088696460613167`, respectively. They are comparisons, not candidate replacements for the spatial reference.

## Work and timing

The work panel reports empirical means separately from theoretical expectation bounds. The time-aggregated empirical mean nodes were

```text
[1.000000, 1.281178, 2.148644, 2.784278, 2.787011, 2.798344, 2.793178]
```

at `T=(0,0.25,1,4,16,64,256)`. The corresponding proposal means were

```text
[0.000000, 2.140956, 2.972722, 3.574444, 3.575667, 3.594656, 3.584967].
```

The theoretical values `E[nodes] <= 2.827327723098716` and `E[proposals] <= 5.301239480810091` are expectation bounds, not per-root or per-cell finite-sample caps. In particular, the largest individual cell mean was `2.8354` nodes at seed `2026092832`, `T=16`, `x=pi/2`; that finite fluctuation is not a bound violation.

The prescribed sampler-only times for all 21 queries were compared with the fixed `K=16` loose reference time `0.09698483301326632` seconds:

| Seed | Sampler-only seconds | Fixed-reference seconds | Ratio |
|---:|---:|---:|---:|
| 2026092831 | 2.127089599 | 0.096984833 | 21.9322 |
| 2026092832 | 1.890721632 | 0.096984833 | 19.4950 |
| 2026092833 | 1.764240010 | 0.096984833 | 18.1909 |

The producer primary wall time was `7.993458750` seconds. Per-seed processing-and-I/O sums were `0.617442007`, `0.577452550`, and `0.458820097` seconds; official diagnostics took `2.066328375` seconds and preflight took `0.002234042` seconds. Reference six-run validation cost is recorded separately in `derived_tables.json`. The fixed reference comparator contains one solve plus all 21 query evaluations and excludes basis/system construction. These are measurements of the frozen implementations and do not establish equal accuracy, optimality, a speedup, or general performance superiority.

## Figures and interpretation

The recommended `two-barrier-results-v2.png` and `two-barrier-results-v2.svg` contain the three fixed panels:

1. strict scaled-defect reference curves and all three Monte Carlo seed means at all 21 time-query points;
2. the explicitly labeled per-time maximum of the three query-wise RMS diagnostics, together with all harmonic-center and mean-ODE comparisons;
3. empirical mean node and proposal counts versus their distinct theoretical expectation bounds.

All horizon axes use a symmetric-log scale and include `T=0`. The v2 error axis also uses a symmetric-log scale, labels its linear threshold, and visibly places the exact `T=0` errors at zero. No curve or time point was selected after inspecting the outcomes. This is an audit of finite floating-point evidence and empirical convergence. It is not a rigorous PDE enclosure, an all-horizon result, or an independent set of six numerical certificates.
