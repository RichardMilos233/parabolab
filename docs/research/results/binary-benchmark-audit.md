# Standard-binary benchmark correction and numerical audit

Date: 2026-09-14. Branch: `codex/research-certified-rate`. Base commit:
`0afcb3c4ba446d20ff9337e4a4e1f2124bda5730`. These are research results awaiting
user verification; nothing was merged to main.

## What was corrected

The historical binary panel and `binary_control_optimum` CSV rows used
`FullyNonlinearPDE1D`'s derivative-coded mechanism in the optimizer, while the
comparison column used the standard-binary Riccati formula. The two trees
represent the same PDE but have different second moments. Those historical
rows therefore do **not** establish the standard-binary optimum or a pure
rate improvement. The historical CSV and PNG in `examples/` are preserved.

The corrected script explicitly passes `BinaryControlMechanism`: every
particle has code `Id`, its only offspring tuple is `(Id, Id)` with probability
one, and terminal values equal one. Both the finite-depth calculation and
the full-tree oracle now concern this same estimator. CSV fields and plotted
markers distinguish the full-tree optimum from the depth-2 numerical optimum.

The new [CSV](binary-benchmark/standard_binary_rate_audit.csv),
[figure](binary-benchmark/standard_binary_rate_audit.png),
[cutoff table](binary-benchmark/cutoff_convergence.csv),
[Monte Carlo table](binary-benchmark/full_tree_mc.csv), and
[metadata](binary-benchmark/metadata.json) are separate durable artifacts.

## Theoretical identity and what the cutoff means

For remaining horizon \(r\), first-event conditioning gives

\[
V(r;\lambda)=e^{\lambda r}
 +\lambda^{-1}\int_0^r e^{\lambda s}V(r-s;\lambda)^2\,ds.
\]

Setting \(Y(r)=e^{-\lambda r}V(r)\) yields
\(Y'(r)=\lambda^{-1}e^{\lambda r}Y(r)^2\), \(Y(0)=1\). Thus

\[
V(T;\lambda)=\frac{\lambda^2e^{\lambda T}}
 {\lambda^2+1-e^{\lambda T}},
\qquad \lambda^2+1-e^{\lambda T}>0.
\]

This formula is exact for the full binary tree. Its rate is located
numerically by solving
\(T\lambda(\lambda^2+1)-2(e^{\lambda T}-1)=0\) within the finite-moment
domain, using the existing strict-convexity result. The stored rate is a
floating-point root, not an interval-certified real number.

At depth zero only surviving leaves contribute: \(V_0=e^{\lambda T}\).
Replacing child moments by \(V_{D-1}\) defines \(V_D\). This corresponds to
killing a branch when it reaches the depth cap; it does not force the
particle to become an unweighted terminal leaf. On a common full binary
tree, the cutoff estimator equals the full estimator if every branch
finishes before the cap and is zero otherwise. Positivity and non-explosion
therefore give \(V_D\uparrow V\) by monotone convergence. The quadrature
values below approximate these exact cutoff moments; their ordering is
numerically checked, not an integration-error certificate.

The unrestricted first moment is \(u(0)=1/(1-T)\). Its variance is
\(V-u(0)^2\), independent of the candidate rate through the first moment.
The killed estimator has a different mean. In particular, one must not
subtract the unrestricted \(u(0)^2\) from a cutoff second moment and call
the result a variance.

## Deterministic result

Depth-2 quadrature uses 8 time nodes, 1 spatial node (exact for the constant
spatial integrand), rate bracket `[0.2, 4.0]`, and derivative tolerance
`1e-9`. The full-tree stationary bracket is bisected to width `1e-12`.

| T | Depth-2 selected λ | Full-tree optimal λ | Full-tree V at depth-2 λ | Full-tree minimum V | Full-tree V at JCP λ |
|---|---:|---:|---:|---:|---:|
| 0.05 | 1.023286680643 | 1.025756300053 | 1.108046366581 | 1.108046027731 | 1.108046028397 |
| 0.10 | 1.043308363103 | 1.053143290077 | 1.234706909424 | 1.234694830616 | 1.315861605730 |
| 0.15 | 1.060187443242 | 1.082362816780 | 1.384725901697 | 1.384621079699 | 1.914219013258 |

At `T=0.15`, the full-tree variance is `0.000538034716733` at the oracle rate,
`0.000642856713919` at the depth-2 selected rate, and `0.002079814390282` at
rate one. The depth-2 selection therefore leaves about **19.48% excess
variance**, even though its full second moment is only about 0.0076% above
the minimum. Near a small-variance estimator, a small relative second-moment
error can be material relative to the variance. This is a direct motivation
for the rate-certification work; these binary values do not establish the
Allen–Cahn optimum.

At the full-tree optimal rate for `T=0.15`, increasing the cutoff gives:

| Depth | Numerical second moment | Gap to exact full-tree moment |
|---:|---:|---:|
| 0 | 1.176277066529 | 0.208344013170 |
| 1 | 1.353271544104 | 0.031349535595 |
| 2 | 1.381239704654 | 0.003381375045 |
| 3 | 1.384345074096 | 0.000276005603 |
| 4 | 1.384603053270 | 0.000018026430 |

This convergence check uses 4 time nodes and 1 spatial node. It is a small
control calculation, not a certified error bound for other mechanisms.

## Independent untruncated Monte Carlo check

Each row uses 120,000 complete trees, a separate fixed seed, no depth cap,
and no clipping. The exact mean is `1.1764705882352942` in both rows.

| Rate | Empirical mean ± empirical SE | Empirical second moment ± empirical SE | Oracle second moment |
|---:|---:|---:|---:|
| 1.0 | 1.176659793 ± 0.000132578 | 1.386637491 ± 0.000336915 | 1.386162859 |
| 1.082362816780392 | 1.176444093 ± 0.000066293 | 1.384548074 ± 0.000156850 | 1.384621080 |

Both mean and second-moment discrepancies are below 1.5 empirical SE.
These are numerical agreement checks, not confidence guarantees. The fourth
moment needed for a sample-second-moment SE is finite at both tested rates:
the general positive binary moment has denominator
\(1-(e^{(p-1)\lambda T}-1)/((p-1)\lambda^p)\), positive here for `p=4`.
The JCP rate at `T=0.15` has an infinite fourth moment, so this audit does
not apply the same second-moment SE argument to that rate. Its full second
moment is finite and is compared analytically instead.

## Verification and reproduction

Environment: conda `parabolab`, Python 3.11.15, NumPy 2.4.6. Focused tests:

```sh
/opt/miniconda3/envs/parabolab/bin/python -m pytest tests/test_rate_optimization.py -q
```

Result: **14 passed in 1.15s** on final verification (first run: 16.15s). These tests include an independent
first-event integral identity for the oracle, the analytically integrated
depth-one formula, increasing-cutoff convergence, rate derivative finite
differences, explicit separation of the two optima, and sampler agreement.
The corrected report was run with:

```sh
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/parabolab-matplotlib XDG_CACHE_HOME=/tmp/parabolab-cache /opt/miniconda3/envs/parabolab/bin/python examples/exponential_rate_sweet_spot.py --binary-only --output-dir docs/research/results/binary-benchmark
```

The additional cutoff and Monte Carlo rows reproduce with the following
Python code, executed from the repository root in the same environment:

```python
import math
import numpy as np
from examples.exponential_rate_sweet_spot import (
    BinaryControlMechanism, _binary_control_pde, _binary_oracle_optimum,
)
from parabolab.moments import MomentQuadrature
from parabolab.rate_optimization import (
    finite_depth_moment_derivatives_1d, riccati_binary_second_moment,
)
from parabolab.tree import sample_tree

T = 0.15
pde = _binary_control_pde(T)
opt = _binary_oracle_optimum(T)
oracle = riccati_binary_second_moment(T, opt)
for depth in range(5):
    value = finite_depth_moment_derivatives_1d(
        pde, 0., 0., max_depth=depth, rate=opt,
        mechanism=BinaryControlMechanism,
        quadrature=MomentQuadrature(time_order=4, normal_order=1),
    ).value
    print(depth, value, oracle - value)
for rate, seed in [(1., 2026091401), (opt, 2026091402)]:
    rng = np.random.default_rng(seed)
    n = 120000
    samples = np.array([
        sample_tree(pde, 0., 0., rng=rng, rate=rate,
                    mechanism=BinaryControlMechanism).value
        for _ in range(n)
    ])
    print(rate, seed, samples.mean(), samples.std(ddof=1) / math.sqrt(n),
          np.mean(samples**2), np.std(samples**2, ddof=1) / math.sqrt(n),
          riccati_binary_second_moment(T, rate))
```

The figure was rendered and visually inspected. No Allen–Cahn or Dym
experiment was rerun. This audit does not add a Lean proof; the mathematical
derivation above identifies the exact statements to connect to the
parallel formal-certification work. User verification is still pending.
