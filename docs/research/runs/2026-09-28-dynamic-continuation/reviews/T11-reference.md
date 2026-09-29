# T11 deterministic reference audit

Status: **accepted**.  The independent odd-sine Galerkin computation passed
the prespecified empirical convergence gate.  It is a floating-point
reference, not a rigorous PDE discretization or rounding-error enclosure.

## Frozen problem and implementation

The reference solves

```text
u_t = u_xx/2 + u - u^3,
u(0,x) = 0.9 sqrt(2/21) sn(sqrt(40/21) x | m=0.05)
```

on the period `4 K(0.05)/sqrt(40/21)`.  It uses the orthonormal basis
`sqrt(2) sin(k omega x)` for positive odd frequencies.  The coefficient ODE
is integrated by SciPy DOP853 at all 201 times `0, 0.08, ..., 16`.

The mode/grid pairs are `(15,128)`, `(31,256)`, and `(63,512)`.  In each
case the periodic uniform quadrature size is greater than four times the
largest retained frequency.  It therefore integrates every cubic Galerkin
product exactly in ideal arithmetic.  All three spatial resolutions were run
at both `(rtol,atol)=(1e-12,1e-14)` and the stricter
`(2e-13,2e-15)`.  The strict mode-63 result is the saved reference.

`numerics/reference.py` imports only the Python standard library, NumPy, and
SciPy.  It does not import the Monte Carlo driver, dynamic interface, sampler,
terminal callback, or any project solver module.  Source hashes for the
reference, its tests, the plan, theory, and Lean gate records are stored in
`reference.json`.

## Verification results

All six DOP853 solves succeeded and returned finite arrays at all requested
times.  Maximum normalized spatial L2 differences were:

| Comparison | Maximum over 201 times |
|---|---:|
| strict mode 63 vs strict mode 31 | `1.0560761786271712e-11` |
| strict mode 31 vs strict mode 15 | `1.5396522965122617e-11` |
| strict mode 63 vs default mode 63 | `1.1429960503148533e-12` |
| accepted empirical floor | `1.0560761786271712e-11` |

The empirical floor is the pointwise maximum of the first and third
comparisons.  Its maximum is below the frozen `1e-9` threshold.  Recomputing
the two acceptance comparisons on an independent 16,384-point physical grid
agreed with the orthonormal coefficient norm within `8.08e-28`.

The projected-initial-data normalized L2 residuals on that grid were
`2.74e-16`, `2.75e-16`, and `2.78e-16` at maximum modes 15, 31, and 63.  These
numbers have reached double-precision quadrature noise and are diagnostics,
not certified Fourier-tail bounds.

The analytic Jacobi stationary residual had normalized L2 value `4.30e-17`
and maximum absolute value `1.39e-16`.  Galerkin RHS norms for projected `g`
were `1.01e-14`, `1.73e-14`, and `1.11e-13` at the three resolutions.  At the
actual initial datum, the Galerkin RHS differed from the independent projection
of `(0.9-0.9^3) g^3` by `1.05e-13` in normalized L2.

The test suite also compares periodic cubic quadrature against a separate
finite complex-Fourier convolution and evolves projected stationary `g` to
check solver drift.  All four tests passed:

```text
4 passed in 0.67s
```

## Artifacts and cost labels

`artifacts/reference/reference.npz` has the producer-facing frozen schema:

| Key | Shape |
|---|---:|
| `times` | `(201,)` |
| `period` | scalar |
| `omega` | scalar |
| `odd_modes` | `(32,)` |
| `coefficients` | `(201,32)` |

Its SHA-256 is
`abf0d174b4c5492f32560ba4243474fa00a9cc1abee13fb03562d8632bc970b3`.
`validation_runs.npz` stores every zero-padded run in an array of shape
`(2,3,201,32)` and has SHA-256
`f0075edfc475dbf15c5c551a604f0ef3840c3add95b79bed0539f388f8d05b9a`.
`reference.json` stores all per-time convergence values, solver statuses,
evaluation counts, timings, diagnostics, environment details, and hashes.
Its loader-facing top-level fields are `passed=true`, `acceptance=true`,
`convergence_max=1.0560761786271712e-11`, and a 201-entry
`convergence_per_time` array.

With BLAS thread counts fixed to one, the strict mode-63 reference solve took
`1.5384556251` seconds and 111,317 RHS evaluations.  This is the label for one
finest reference algorithm run after shared setup.  Setup, all six validation
solves, diagnostics, and NPZ serialization took `3.7347516250` seconds.  This
larger number is the honest total deterministic-reference validation cost for
comparison with the Monte Carlo experiment.

The convergence evidence supports using the saved curve as the numerical
truth proxy for this experiment.  It does not establish a rigorous solution
error bound; accuracy statements must retain the empirical reference floor
and the formalization boundary described in `06-lean.md`.
