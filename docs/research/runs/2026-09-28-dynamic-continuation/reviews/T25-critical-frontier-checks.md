# T25 — fixed deterministic checks for the critical moment/work frontier

Decision: **PASS for the fixed numerical protocol**. This is a deterministic
illustration of the conventionally reviewed endpoint theorem, not an
independent proof of the asymptotic classification and not a stochastic
sampler experiment.

## Frozen execution contract

The execution used exactly

```text
alpha = 0.5, 1, 2
p = 2, beta = 0.5
delta = 1e-2, 1e-4, 1e-6, 1e-8
mpmath precision = 80 decimal digits
exact-identity acceptance = discrepancy strictly below 1e-60
```

No case, precision, threshold or quadrature split was changed after results
were observed. Before numerical evaluation, the script verified SHA256 hashes
for the accepted theory, frozen audit and protocol, the T23 module and report,
and the actual T23 build and axiom logs:

| Input | SHA256 |
|---|---|
| `reviews/T22-critical-moment-work-audit.md` | `cab149f5b1a7bea91cc9ea3e52d09ce68b1edf9cbf9b2ce3c8329ef2bedbdf4d` |
| `04h-critical-moment-work.md` | `9750b19bab65bd1cc78bf0db6b5385a896e3a8146a8219777f808ea1279e7dd4` |
| `02c-critical-frontier-protocol.md` | `3e6929d0c49d17f69819c3dd7854cbfab8804745103e7d4ef9831126957220cc` |
| `06e-critical-work-lean.md` | `9195a1827c05a78a86ab08b6c6c5b7a3a88feeff01b75806a8d325ae228da068` |
| `formal/EstimatorIntegrity/CriticalMomentWork.lean` | `2aa8eac99d548e1a4ba5e21f7c9d5aef0a6595a527a4ee9d59c49c0dba23893e` |
| `lean/critical-moment-work/build.log` | `cb5476d3a90ba929e47e7cb54ca6dea6315c9a5ad3f7b858a57e32d4e42190e1` |
| `lean/critical-moment-work/axioms.log` | `60d379bd383500c73b4c8aeb738732d748fd32ade4fd708f889244ef04c585e5` |

The executed script hash was
`5e4b61edb9f5d7c5aa1f45d9ccdc26e45bed92b0236e78a407d4fb6f605336fe`.

## Exact identities

All 54 prespecified exact-identity checks passed. They comprise three
quadrature-versus-gamma evaluations of `tau_alpha`, 39 derivative checks
(orders 0 through 12 for each alpha), and 12 direct-tail-quadrature versus
incomplete-beta checks. The largest absolute or scaled discrepancy was

```text
1.0542197943230523e-81,
```

well below the fixed strict `1e-60` threshold.

The independently evaluated critical times were

```text
tau_0.5 = 0.785398163397448309615660845819875721049292349843776455243736...
tau_1   = 0.666666666666666666666666666666666666666666666666666666666667...
tau_2   = 0.533333333333333333333333333333333333333333333333333333333333...
```

The JSON preserves all 80-digit decimal strings, every individual check and
the empty failure list.

## Asymptotic diagnostics

The complementary-beta cusp ratios move toward the proved constants:

| alpha | ratio at `delta=1e-2` | ratio at `delta=1e-8` | proved limit |
|---:|---:|---:|---:|
| 0.5 | 0.9413935628674815 | 0.9428090401678498 | 0.9428090415820634 |
| 1 | 0.9966666666666667 | 0.9999999966666667 | 1 |
| 2 | 1.3233533333333333 | 1.3333333233333334 | 1.3333333333333333 |

These finite ratios carry no acceptance threshold and do not prove the
limits.

For the endpoint integrand, every evaluation used the complementary
incomplete-beta tail and

```text
-log(F_alpha(z)/tau_alpha) = -log1p(-B_alpha(1-z)/tau_alpha),
```

so the calculation does not subtract two nearly equal logarithm arguments.
At `delta=1e-8`, the scaled integrands and analytic limiting constants were:

| alpha | finite scaled integrand | analytic limiting value |
|---:|---:|---:|
| 0.5 | 1.3690658269782046 | 1.3690658273200602 |
| 1 | 1.6329931618554521 | 1.6329931618554521 |
| 2 | 1.8973665984727358 | 1.8973665961010276 |

Again, these are diagnostics without a residual threshold.

All 12 truncated endpoint contributions were positive. For every alpha they
strictly increased as the cutoff decreased in the fixed order:

| alpha | `K(1e-2)` | `K(1e-4)` | `K(1e-6)` | `K(1e-8)` |
|---:|---:|---:|---:|---:|
| 0.5 | 1.172773573 | 1.645164143 | 1.794548651 | 1.841788211 |
| 1 | 2.576010487 | 5.576151607 | 8.576281902 | 11.576412196 |
| 2 | 13.13006394 | 149.3962302 | 1511.889495 | 15136.80528 |

The patterns are consistent with the T22 predictions: a finite limit for
`alpha=0.5`, logarithmic divergence for `alpha=1`, and power divergence for
`alpha=2`. Four cutoff values do not establish any of those conclusions.
In particular, `K_alpha(delta)` integrates only from `z=1/2` to
`z=1-delta`; it is a truncated endpoint contribution and is not the full
sqrt-node absolute mass `S_2`.

## Execution and artifacts

The sole protocol execution was

```text
/opt/miniconda3/envs/parabolab/bin/python \
  docs/research/runs/2026-09-28-dynamic-continuation/numerics/check_critical_frontier.py
```

It exited successfully in `2.875464459` seconds under Python 3.11.15,
mpmath 1.3.0, NumPy 2.4.6 and Matplotlib 3.11.0 on
`macOS-26.3-arm64-arm-64bit`. The full environment strings and paths are in
`numerics/critical_frontier_execution.log`.

The machine-readable record is
`numerics/critical_frontier_checks.json`. The figure hashes are

```text
critical-frontier.png  b966e1b10ff97d1f3157448d48ec6a5b9554b2c6a5a8ef6d74b077f3acd8eba3
critical-frontier.svg  b756d2d892f7d1d81f56c0588f989e6dea293ab885b1d4a0c87d68886a115774
```

Visual inspection of the PNG passed: the left panel distinguishes numerical
cusp ratios from dashed proved limits, and the right panel shows all three
truncated contribution curves on a logarithmic vertical scale with each T22
prediction labeled as theory. Both axes identify the cutoff and dimensionless
quantities, and the caption states that `K_alpha(delta)` is not full `S_2`.

## Scope

This run does not prove convergence, integrability, logarithmic or power
divergence, or the full critical frontier. Those conclusions remain in the
reviewed theory. It does not construct or time a proposal law, sample a tree,
modify the original dynamic experiment, or claim a competitive ODE
algorithm. The signed scalar ODE remains globally solvable; the numerical
diagnostic concerns the original derivative-coded tree representation.
