# T16 — deterministic constant-profile obstruction checks

Date: 28 September 2026. Status: complete. The checks were run only after T13
Section 7 accepted the theorem in `04d-sharp-constant-horizon.md` and the
separate Riccati Lean gate recorded in `06b-absolute-lean.md` passed.

These are 80-decimal deterministic identity checks and illustrations. They are
not Monte Carlo experiments, and no divergence conclusion is inferred from
finite numerical values. The critical-time classifications written below come
from the reviewed conventional theorem.

## Prespecified checks

For `f(y)=sin(y)` and `r=pi/2`, direct quadrature of
`integral_0^infinity sech(z) dz` agreed with `pi/2`. At
`t=(.1,.5,.9,.99) pi/2`, independent quadrature of `sec` agreed with
`log(sec(t)+tan(t))`; high-precision differentiation of the logarithmic
formula agreed with `sec(t)`. The signed solution

    u(t) = 2 atan(exp(t))

satisfied its initial condition and `u'=sin(u)` at every prescribed point.
The reviewed theorem, rather than the finite calculation, states that the
canonical Id absolute moment is infinite at `t=pi/2`, while the signed
solution remains global.

For `f(y)=1/(1+y^2)` and `r=0`, quadrature of `1-z^2` on `[0,1]` agreed with
`2/3`. At `t=0,.1,.5,.65,2/3`, the explicit formulas

    z(t) = 2 sin(asin(3t/2)/3),
    u(t) = 2 sinh(asinh(3t/2)/3)

satisfied `z-z^3/3=t` and `u+u^3/3=t`. The derivative of `z` was deliberately
not evaluated at the critical endpoint. The check gives the exact finite
point `z(2/3)=1`; the reviewed theorem says the Id absolute moment is infinite
only for `t>2/3`.

For `Phi_n=sum_{k=0}^n z^(2k)`, independent reciprocal-polynomial quadrature
agreed with the cotangent formula for every prescribed truncation:

| n | tau_n | tau_n - 2/3 | identity residual |
|---:|---:|---:|---:|
| 1 | 1.5707963267948966 | 0.9041296601282300 | 0 |
| 2 | 0.9068996821171089 | 0.2402330154504423 | 1.05e-81 |
| 4 | 0.7386327321961827 | 0.0719660655295160 | 0 |
| 8 | 0.6875255115692054 | 0.0208588449025388 | 1.05e-81 |
| 16 | 0.6724009170276096 | 0.0057342503609430 | 1.05e-81 |
| 32 | 0.6681801383301914 | 0.0015134716635248 | 1.05e-81 |

The sequence is strictly decreasing at these six indices and every value is
strictly above `2/3`. The largest residual among all prespecified exact
identity checks was

    1.0542197943230523e-81,

well below the fixed `1e-60` acceptance threshold. No precision refinement
was used.

## Outputs and visual inspection

`numerics/check_obstruction.py` refuses to overwrite the final JSON or figure
outputs, verifies selected frozen T09 hashes before running, records source
hashes and environment versions, and fails if any exact residual reaches the
threshold. `numerics/obstruction_checks.json` contains every raw
high-precision value and residual, the decreasing/excess checks, timings, and
provenance. `numerics/obstruction-checks.log` preserves the execution result.

The PNG and SVG show the exact signed and absolute curves, shade only the
regions classified as infinite by the theorem, mark the rational finite point
`(2/3,1)`, and show the truncation horizons descending toward `2/3`. The final
PNG was inspected at its native `2698 x 855` resolution. Its labels and
annotations are legible and do not overlap; the caption explicitly says the
plot is not Monte Carlo evidence of divergence.

Final SHA-256 values are:

- `check_obstruction.py`: `d85ae0b6f154db4f72063d95b9ef0ab23dfe4cdd2f559da5c0e88c2fdf41be8c`
- `obstruction_checks.json`: `f97c9af8463fec4a7ca993cabca053068414dcc97605db836de64f9301ef9aca`
- `obstruction-checks.log`: `dcbf8bc4501128ffd524f42936463e4d76d14d68ef08272796c9bcb1fc9f6ff8`
- `obstruction-examples.png`: `b90e1cd6101d6e8d16fb729cb1ea6d5e2084079c1f047fbb0d8d005d75c44002`
- `obstruction-examples.svg`: `752415ba99422df7d96108bdc2f57b1470980a49b5bd592bcacbf6e77c4e997f`

The script froze the reviewed `04d` source at SHA-256
`9f345008b3f44ab53848887c65d4aa0744c7cd38d35aa514249bdfd11c69cb16`.
It also rechecked the selected T09 implementation, audit, and review hashes;
all matched their frozen values.

## Formal and numerical boundary

The current Lean module proves the finite closed-interval analytic Riccati
barrier. It does not formalize the reciprocal-polynomial/cotangent identity,
the infinite nonnegative series, the finite-tree exhaustion, likelihood
cancellation, Tonelli or monotone convergence, or the bridge from sampled
trees to these absolute moments. Those steps remain part of the reviewed
conventional argument. The finite computations here illustrate exact formulas
already justified there; they do not prove the tree correspondence, endpoint
classification, or infinite values.

No T09/T11 source or data file was modified, and these checks do not change
the frozen primary continuation experiment.
