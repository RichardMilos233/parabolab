# T36 — independent deterministic two-barrier reference

Date: 2026-09-28. Verdict: **PASS**.

The frozen scaled-PDE reference completed all deterministic preflight checks
and all six prescribed cosine-Galerkin/Radau refinement runs. Every solver
reported success. The largest absolute difference over the 21 fixed
time/query values, comparing any run with the 64-mode strict run, was

```text
2.282851685464493e-11 < 1e-8.
```

This is empirical convergence evidence for six refinements of one numerical
method. It is not a rigorous enclosure and does not provide six independent
numerical certificates.

## Frozen inputs and implementation boundary

The implementation followed
`02d-two-barrier-experiment-protocol.md`, SHA-256
`605eda24574bfb7e44dc997c185836d2a54311c18344e0be4c005674e00beda9`,
after the T34/T34b review and freeze pass. It owns only:

- `numerics/two_barrier_reference.py`, SHA-256
  `d2561072434d4eaa3966c3353b299e3fa5813455d7ccf8454ee8889be64856ce`;
- `numerics/test_two_barrier_reference.py`, SHA-256
  `835249633d23a08207243c96f3b19991db14f899f1b2da92232fdcb613a113ef`;
- `artifacts/two-barrier/reference-v1/`;
- this review.

It imports NumPy and SciPy, and does not import a sampler, clock, barrier, PDE
production helper, or any existing numerical implementation. The frozen
source solves directly

```text
w_t = 0.5*w_xx + 3*exp(-2t)*w^2 - exp(-4t)*w^3,
w(0,x) = 3/8 - (1/8)*cos(x)
```

on the `2*pi` torus. It represents
`w=a_0+sum_(k=1)^K a_k cos(k*x)`, with modes zero through `K`. On the
uniform grid `2*pi*j/J`, it uses the grid mean for mode zero and twice the
cosine-weighted mean for positive modes. The analytic projected Jacobian is

```text
-0.5*k^2*delta_(k,l)
+ P_k[(6*exp(-2t)*w - 3*exp(-4t)*w^2)*cos(l*x)].
```

The immutable `reference-v1/execution_manifest.json` was created before the
test suite or deterministic preflight ran. Its SHA-256 is
`3ef7ed5110497633b64a248e050404ae557de8f6bd181010c736b777140eaa7c`.
It fixes source and gate hashes, Python and library versions, all cases,
tolerances, solver order, thresholds, and schemas. The execution rechecked
all frozen source hashes before doing numerical work. The artifact refuses
both directory overwrite during `prepare` and result overwrite during
`run`; no failure or source correction occurred, so `reference-v1` is the
only attempted version.

The recorded environment was Python `3.11.15` at
`/opt/miniconda3/envs/parabolab/bin/python`, NumPy `2.4.6`, SciPy `1.17.1`,
and macOS arm64. Binary64 epsilon was `2.220446049250313e-16`.

## Deterministic preflight

The five source tests passed in `0.64s`. The frozen all-mode vector

```text
c_0=3/8,
c_k=(-1)^k/(8*(k+1)^2),  k=1,...,K
```

was checked at `t in {0,1/4,4}` for every `K in {16,32,64}`. The independent
comparison converts the cosine vector to finite complex-Fourier
coefficients, performs explicit convolution, and converts the retained
coefficients back. It does not reuse the quadrature projection. The maximum
absolute discrepancies were:

| quantity | observed maximum | gate |
|---|---:|---:|
| nonlinear projection | `1.2695058762904332e-15` | `1e-10` |
| analytic Jacobian entry | `7.105427357601002e-15` | `1e-10` |

The three fixed constant profiles were evolved with the 16-mode strict
system and compared at all seven times with the independently evaluated
stable scalar formula. For `alpha=c^(-2)-1`, that target was

```text
R_c(t) = alpha /
  (sqrt(1 + alpha*exp(-2t)) * (1 + sqrt(1 + alpha*exp(-2t)))).
```

All three solves succeeded. Their maximum scaled coefficient discrepancies
were `9.672262990534364e-13` for `c=1/2`,
`4.120037644383956e-13` for `c=5/8`, and
`1.439959262938828e-13` for `c=3/4`, below the fixed `1e-8` gate.
`preflight_arrays.npz` retains every quadrature/convolution projection and
Jacobian pair plus all constant-profile coefficient traces and targets.

## Six refinement runs

Every run was one SciPy Radau solve from `0` to `256`, evaluated at
`{0,1/4,1,4,16,64,256}`. The resolutions were `(K,J)=(16,128),(32,256),
(64,512)`, and each used both fixed tolerance pairs
`(rtol,atol)=(1e-10,1e-12)` and `(1e-12,1e-14)`.

| run | coefficient shape | solver success | max 21-value difference | solve seconds |
|---|---:|---:|---:|---:|
| `k16_loose` | `(7,17)` | yes | `6.95177249099288e-12` | `0.0969756250269711` |
| `k16_strict` | `(7,17)` | yes | `9.625633623500107e-14` | `0.3034875416196883` |
| `k32_loose` | `(7,33)` | yes | `2.036104618241552e-11` | `0.131675458047539` |
| `k32_strict` | `(7,33)` | yes | `1.3666845433135677e-13` | `0.4082174161449075` |
| `k64_loose` | `(7,65)` | yes | `2.282851685464493e-11` | `0.44244037522003055` |
| `k64_strict` | `(7,65)` | yes | `0` | `0.7382458751089871` |

The order of these discrepancies is not monotone because the looser time
tolerance dominates differences at this scale. The fixed gate concerns the
maximum, and all six runs pass it without changing any case or tolerance.

The six solve times sum to `2.1210422911681235s`; their 126 query evaluations
sum to `6.358372047543526e-05s`. Preflight took
`0.4952787081710994s`, and validation wall time before the final summary was
`2.632992916274816s`. Artifact I/O before the summary took
`0.014336624182760715s`.

The predesignated comparator `k16_loose` is eligible. Its one solve plus all
21 query evaluations took `0.09698483301326632s`, and its maximum strict-run
difference was `6.95177249099288e-12`. This comparator timer begins after
the fixed cosine basis/system is constructed, so it excludes basis/system
construction. It includes the solve and the single all-query matrix
evaluation. The result is a fixed-implementation timing, not an optimized
or equal-accuracy comparison and not evidence of general solver superiority.

## Frozen strict values

The strict `K=64` scaled values, with columns `x=0,pi/2,pi`, are:

| `T` | `x=0` | `x=pi/2` | `x=pi` |
|---:|---:|---:|---:|
| `0` | `0.25` | `0.375` | `0.5` |
| `0.25` | `0.30943141259447354` | `0.4680004423046071` | `0.6422735533911363` |
| `1` | `0.47411013939082064` | `0.6927585043583621` | `0.9486894989396278` |
| `4` | `0.750239407458248` | `0.8215511170309717` | `0.8931583157631559` |
| `16` | `0.821788384704521` | `0.8219656614988032` | `0.8221429382930953` |
| `64` | `0.8219656614988099` | `0.821965661498816` | `0.8219656614988221` |
| `256` | `0.821965661498816` | `0.821965661498816` | `0.821965661498816` |

At time zero these are the exact frozen initial values. The later equality
shown in decimal at `T=256` is binary64 output, not an assertion of exact
finite-time spatial constancy.

## Artifact interface and audit

`reference.npz`, SHA-256
`dd49e4f5c630466942b9c276be7b807763c46171a79311ac71c7840d71603072`,
has exactly:

```text
times         float64 (7,)
queries       float64 (3,)
scaled_values float64 (7,3)
```

Its three arrays are byte-for-byte equal to the corresponding arrays in
`refinement_k64_strict.npz`. Each of the six
`refinement_k{K}_{tolerance}.npz` files contains `times`, `queries`, full
`coefficients`, and `scaled_values`; the coefficient shapes are those in the
table above, and every array is finite. Reconstructing all query values from
the retained coefficients and cosine basis gave exact binary64 array
equality.

`reference_summary.json`, SHA-256
`cb384301956b0a650dea10f458522f55981d6e10ab738aacb105624d75dbfc81`,
is self-contained: it records gate status, strict values, per-run solver
diagnostics and discrepancies, timing scopes, source hashes, limitations,
and artifact schemas. The separate artifact audit passed and is preserved in
`artifact_audit.log`, SHA-256
`09aea7d17fb4b40017374d4449715c755d70e88335ba452ef20f5140293bfc48`.
The complete `reference-v1` subtree is approximately `268K`.

## Use by downstream tasks

The stochastic producer may read the frozen `reference.npz` for its execution
gate and post-sampling comparisons, but its mathematical sampler must not
import this module or use the evolving reference as leaf data. Independent
diagnostic math should likewise implement the scalar target above and the
forward clock CDF target

```text
F_T(s)=exp(Lambda(s)-Lambda(T))=R(z(s))/R(z(T))
```

without importing either this reference or sampler helpers. A leaf is
represented at `s=0` in that CDF. The deterministic result does not certify
floating unbiasedness, stochastic-law correctness, arbitrary measurable
data, higher-dimensional performance, or a universal runtime advantage.
