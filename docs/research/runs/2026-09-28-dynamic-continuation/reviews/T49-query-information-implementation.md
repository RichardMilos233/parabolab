# T49 query-information implementation checks

**Status: PASS.** One official execution of the frozen `02e-query-information-check-protocol.md` completed successfully. The run exhaustively evaluated the fixed finite oracle model using exact `Fraction` arithmetic, reused its endpoint records for the budget mixture, and passed both prescribed high-precision quadratures and all four scalar rows.

This is an implementation check for the older D22 information core. It is not a D24 upper-algorithm experiment, a PDE simulation, an empirical proof of the universal lower bound, or evidence of novelty.

## Freeze and execution

The accepted protocol has SHA-256 `5e4fe3e20cad7e435142dcf37e343798e730286aa0547cdf7812a8b7a42e33c2`; the T47 review has SHA-256 `c2bd4343117f20a0b6b2e93e03d9773643a281a89fa4635cd433513f41ac1ffc`. Root read the complete implementation and cleared the exact source hash before execution in `reviews/T49-root-source-clearance.json`, SHA-256 `b17a42d366d5a7212a629d3b2fb0acaf80451e5421f84fb126110112a526bd13`.

The implementation source is `numerics/query_information_checks.py`, SHA-256 `c856a9ba2548a6486d756af0b628396e8ab3d9186413e13e906fc57cd795930d`. Syntax checking used the prescribed Python executable and passed before the freeze. No finite enumeration or quadrature was run during development.

After source clearance, `prepare` created `artifacts/query-information/checks-v1/execution_manifest.json` before the official run. The manifest froze 12 implementation, protocol, review, theory, Lean, and toolchain inputs. A post-run comparison found zero input-hash mismatches. It recorded:

```text
Python 3.11.15
mpmath 1.3.0
Lean 4.33.0, commit d8b18978322de05a8f3dba51ef03cf5461676c17
Lake 5.0.0-src+d8b1897
Mathlib db584cd6d46c92f209a44c0f1c829460d327499d
macOS-26.3 arm64
```

The authorized commands were executed exactly once:

```text
/opt/miniconda3/envs/parabolab/bin/python numerics/query_information_checks.py prepare
/opt/miniconda3/envs/parabolab/bin/python numerics/query_information_checks.py run
```

The run took `11.331974749919027` seconds. There is no failure artifact and no rerun.

## Exact finite oracle model

The evaluator receives only an oracle callable, the public baseline, a permutation, a query cap, and a miss output. It receives no hidden cell, sign, or assigned target. The driver constructs the alternative oracle and scores the completed run afterward.

Every response, output, target, cost, squared loss, probability, average, formula difference, and slack is a Python `Fraction`. The evaluator records the actual chronological trace and stops as soon as an observed oracle response differs from the public baseline. A canonical streaming digest commits to all executed records:

```text
98f5ff6c884388bfa4f9113c367d2e2afcde6a852c1871f990835d7977670d15
```

The exhaustive observed counts exactly match the frozen values:

| Quantity | Observed |
|---|---:|
| Seed/cap/miss-output configurations | 25,960 |
| Baseline oracle runs | 25,960 |
| Alternative oracle runs | 308,060 |
| Total oracle runs | 334,020 |
| No-hit alternative runs | 154,030 |
| Direct configuration paired-loss checks | 25,960 |
| Main summary rows | 105 |
| Fixed-alternative permutation-risk checks | 820 |

The per-`K` run counts were `30`, `150`, `840`, `5,400`, and `327,600` for `K=1,2,3,4,6`. The corresponding no-hit counts were `10`, `60`, `360`, `2,400`, and `151,200`.

For every executed no-hit alternative, the output and complete ordered trace equaled the baseline run. Every baseline distinct-visited-cell count was at most its query count. Every configuration passed the directly evaluated paired-loss inequality. All 105 rows exactly matched

```text
(1-m/K) * (h^2 + 1/4),
```

and each of the 820 fixed alternatives exactly matched

```text
(1-m/K) * (h-sigma/2)^2.
```

The maximum two equality discrepancies were both the exact rational zero. All lower-bound slacks were nonnegative; the stored minimum family slack and minimum direct paired-loss slack were zero because the sweep includes equality cases. The complete 105 rows retain baseline risk, positive-input mean risk, negative-input mean risk, combined alternative-family risk, exact numerators and denominators, lower bounds, slacks, configuration statistics, and every fixed-alternative comparison.

## Reused randomized budget mixture

The five mixture rows were derived from the already executed `m=0` and `m=K`, `h=0` records. They reused exactly `19,262` main-sweep records and made zero additional oracle calls.

| `K` | Baseline expected cost | Baseline risk | Every alternative risk |
|---:|---:|---:|---:|
| 1 | `3/4` | `0` | `1/16` |
| 2 | `3/2` | `0` | `1/16` |
| 3 | `9/4` | `0` | `1/16` |
| 4 | `3` | `0` | `1/16` |
| 6 | `9/2` | `0` | `1/16` |

Thus the prescribed finite abstract promised class attains the T42 coefficient. This does not construct a uniformly accurate PDE algorithm or prove a matching upper bound for the PDE function class.

## Scalar amplification checks

The bump integral was evaluated after splitting at `1/2`:

```text
80-digit tanh-sinh:
0.0070298584066096562392412705303539560761553994753572487961297388286445458695463593

100-digit Gauss-Legendre:
0.007029858406609656239241270530353956076155399475357248796129738828644545869546359346285080438977033932
```

Both methods used explicit `maxdegree=12`. Their absolute difference was approximately `4.628508043898e-83`, below the fixed `1e-70` tolerance. This is a numerical convergence comparison, not a rigorous quadrature enclosure. The primary rows use the 80-digit integral as input and perform all row arithmetic at 100 decimal digits; the stored primary values contain 80 significant digits.

The implementation also recorded the analytic derivative certificate

```text
r = 1/[z(1-z)] >= 4,
|psi'| <= r^2 exp(-r) <= 16 exp(-4) < 1,
psi <= exp(-4) < 1,
D = 1.
```

No derivative grid was used. The shared constants included

```text
kappa = 0.35206532676429947777468044159651765311031518037571194965546901798822319783671661
delta = 0.00016104191849690709292413426487491402352279171232567027144989057240288895026466828
T0    = 11.853557511793995799148564610787033534060895621594482895183037728925591209310028
```

All 12 rearranged identity checks and all 36 row inequality/floor checks passed. Selected values are shown below; the machine-readable table retains at least 75 significant digits for every prescribed value.

| `k` | `T` | `B` | `ell` | background | `ell-background` | `floor(R)` |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 12.0891235831068 | 1.265625 | 0.784634745870586 | 0.001573675584771 | 0.783061070285815 | 4 |
| 8 | 13.3611011165468 | 1.12890625 | 0.748551447808738 | 0.001403679765428 | 0.747147768043310 | 8 |
| 16 | 14.6876895513673 | 1.0634765625 | 0.728514150444153 | 0.001322324623314 | 0.727191825820839 | 16 |
| 32 | 16.0434489682256 | 1.031494140625 | 0.717982743006696 | 0.001282557744147 | 0.716700185262549 | 32 |

For every row, `T≥T0`, `1≤B≤4`, `0<c<1`, `ell≥1/sqrt(2)`, `background≤1/32`, `ell-background>1/2`, and `floor(R)=k`. The independent forms of `B`, `ell`, and `R` met the combined tolerance `1e-70*(1+|target|)`.

## Artifacts and hashes

| Artifact | SHA-256 |
|---|---|
| `execution_manifest.json` | `cf0dff8a5dd4a51387d192ce489479554072deb4e9fa3d32d1165e62287a2199` |
| `finite_summary.json` | `faae74bf139b9e2401b34d7863e17df58dc6c7f4b59fe289c6abe02f89113ea9` |
| `budget_mixture_summary.json` | `95406301ecfc7e87359af8f43911aa798824206ee58e33e3d3569728aa81e26a` |
| `scalar_checks.json` | `bc2fde87b817e3fea39ee20fca65d9caedb630ef5f52da5d8b7dcafa6c7f0bcb` |
| `run.log` | `b9f8c675b6a9254471332b7bb4137d77160889338d8c4f831556332b40b53bfa` |
| `check_result.json` | `75608875daf99067390f5f31179f7898c22582e895f4dbb0512308e342b1f0d5` |

Completed blocks were written immediately before the next block began, so a later failure would have preserved earlier completed evidence. Scalar failure context was reset for each quadrature stage, the comparison, and every prescribed `k,T` row. The first and only official run passed, so no failure file exists.

Root's post-run audit is `reviews/T49-root-output-audit.json`, SHA-256 `0058452ba084f29eed3556ca78a8e93f38f46c3a620c0eda417bd5c6467e427a`. It independently recomputed all 105 main summary rows, all 820 fixed-alternative risks, all five mixture rows, and the four scalar rows from stored values. It also verified all 12 manifest inputs, the four output hashes recorded in `check_result.json`, and all 342 initially protected project paths, with zero mismatches. Root did not replay the complete evaluator or independently reexecute either quadrature; the audit states those limits explicitly.

## Interpretation boundary

The finite alternatives use assigned targets `sigma/2`; they are not numerically evaluated Allen–Cahn solution values. The enumeration checks a restricted deterministic policy family and cannot validate the universal quantifiers over measurable randomized algorithms proved conventionally in 04o/T40/T41. It does not exercise arbitrary adaptive changes of query location, unbounded random stopping, or general probability spaces.

The scalar block checks the implemented bump integral and algebraic amplification/scaling formulas. It does not validate heat minorization, nonlinear PDE comparison, smooth periodic extension, hard-input class membership, or minimax optimality. No PDE discretization or stochastic benchmark was performed.
