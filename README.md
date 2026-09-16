# parabolab

Coding-tree Monte Carlo and deep branching solvers for fully nonlinear
parabolic PDEs. The paper reproductions and common solver interface are
implemented; current research improves the branching estimator by selecting
the clock rate $\lambda$ and tuple probabilities $q_c(Z)$ to reduce variance.
The PDE-solving workflow stays the same: define a PDE, choose solver or
sampling settings, and compare estimates on a common grid.

The implementation reproduces the methods of Nguwi, Penent & Privault (NTU):

- **[JEQ2023]** *A fully nonlinear Feynman–Kac formula with derivatives of
  arbitrary orders*, J. Evol. Equ. 23:22 (2023).
  [doi:10.1007/s00028-023-00873-3](https://doi.org/10.1007/s00028-023-00873-3) —
  official repo: [nguwijy/coding_trees](https://github.com/nguwijy/coding_trees)
- **[JCP2024]** *A deep branching solver for fully nonlinear partial
  differential equations*, J. Comput. Phys. 499 (2024) 112712.
  [doi:10.1016/j.jcp.2023.112712](https://doi.org/10.1016/j.jcp.2023.112712) —
  official repos: [nguwijy/deep_branching](https://github.com/nguwijy/deep_branching),
  [nguwijy/deep_branching_with_domain](https://github.com/nguwijy/deep_branching_with_domain)

The solution of

$$\partial_t u + \tfrac12 \partial_x^2 u + f(u, \partial_x u, \dots) = 0,
\qquad u(T,\cdot) = \phi,$$

is represented as $u(t,x) = \mathbb E[\mathcal H(\mathcal T_{t,x,\mathrm{Id}})]$
over random *coding trees*: particles carry operator **codes**, move as
Brownian motions, die at Exp-distributed times and branch into code tuples
drawn from the **mechanism** $\mathcal M(c)$; leaves evaluate their code on
$\phi$ (JEQ2023 Thm. 1, JCP2024 Alg. 1), under the representation's
integrability assumptions.

Start with [demos](demo/README.md) for the existing solver workflow and the
[research guide](docs/research/README.md) for current results and open work.
The [documentation map](docs/documentation-map.md) separates current guidance
from dated experiments and inactive directions.
Multifactor Merton research is retained as historical material; the original
Merton benchmarks and general multidimensional PDE support remain available.

## Quickstart

```bash
conda env create -f environment.yml     # or: conda env update -f environment.yml
conda activate parabolab
pytest                                  # default suite (slow tests excluded)
pytest -m 'slow or not slow'            # + paper-budget validation (minutes)
python demo/allen_cahn.py               # start here: one PDE, several
python demo/merton.py                   #   methods (see demo/README.md)
python demo/variance_reduction.py       # same workflow: baseline / lambda / q / both
python demo/rate_variance.py            # rate diagnostics and binary Riccati control
python demo/dym.py                      # non-integrability diagnostic
python examples/jeq_allen_cahn_1d.py    # paper reproductions (see examples/)
python examples/jeq_fig6_dym.py         # M2: JEQ Figs 6-9 reproductions
python examples/jeq_fig7_tan.py         #     (each prints a table and saves
python examples/jeq_fig8_cosine.py      #      a .png next to the script)
python examples/jeq_fig9_log.py
python examples/jeq_fig1_allen_cahn_nd.py   # M3: Fig 1, d = 5 and d = 100
python examples/jeq_fig4_exponential_nd.py  # M3: Figs 4/5, d = 5 and 10
python examples/jeq_table2_allen_cahn_d100.py  # M3: Table 2 (d = 100)
python examples/jeq_table5_hjb_d100.py         # M3: Table 5 (HJB, d = 100)
python examples/jcp_table1_allen_cahn_deep.py  # M4: JCP Table 1/Fig 1 (deep)
python examples/jcp_table3_exponential_deep.py # M4: JCP Table 3 (deep)
python examples/jcp_table5_merton_deep.py      # M4: JCP Table 5 + Fig 7
python examples/jcp_comparison_baselines.py    # M5: Tables 1/3/5 three-way
                                               #     (ours vs BSDE vs DGM)
python examples/blowup_allen_cahn.py           # M5: blow-up study (Fig 2)
```

The `jcp_*_deep.py` scripts default to reduced Monte Carlo budgets;
pass `--full` for the paper's budgets and `--device cuda` on a GPU
machine (everything is device-agnostic, CPU by default).

Reproducing on a new machine needs only the clone and the conda env
above. Optionally, clone the authors' repos **next to** `parabolab/`
to enable the golden cross-check tests and the reference-CSV overlays
in the example plots (everything skips gracefully without them):

```bash
git clone https://github.com/nguwijy/coding_trees
git clone https://github.com/nguwijy/deep_branching
git clone https://github.com/nguwijy/deep_branching_with_domain
```

The papers themselves are not distributed with this repo — see the
DOI/arXiv links at the top.

One value:

```python
from parabolab import estimate
from parabolab.library import allen_cahn_wave_1d

pde = allen_cahn_wave_1d(T=0.5)
r = estimate(pde, t=0.0, x=0.0, n_samples=100_000, seed=0)
print(r, "exact:", pde.exact_solution(0.0, 0.0))
```

A whole profile, and the same PDE through a different method — every
solver is `Solver(**budget).solve(pde, grid) -> Curve`, so swapping one
for another is a one-line edit:

```python
from functools import partial
import numpy as np
from parabolab import CodingTreeMC, compare
from parabolab.library import allen_cahn_nd

pde  = partial(allen_cahn_nd, d=1, T=0.5)     # a factory: PDEs are not picklable
grid = np.linspace(-8.0, 8.0, 27)

mc = CodingTreeMC(n_samples=10_000, seed=0).solve(pde, grid)
# deep = DeepBranching(n_states=1000, m_samples=10_000, epochs=3000).solve(pde, grid)
# bsde = DeepBSDE(epochs=3000, n_states=1000).solve(pde, grid)
# dgm  = DeepGalerkin(epochs=3000, n_states=1000).solve(pde, grid)
compare(pde, mc).table().plot("allen_cahn.png")
```

`CodingTreeMC` estimates pointwise expectations; the three network solvers
train approximations to the solution. Runnable versions are in `demo/`.
Profile examples use the same interface. Multi-run tables, the three-way
comparison, blow-up diagnostics and rate sweeps keep separate drivers
because their output is a statistic rather than a solution curve. Runtime
depends on the PDE, mechanism, sampling policy, hardware and budget.

## Current research: branching variance reduction

Selecting `lambda` and `q_c(Z)` changes how the same branching estimator is
sampled. Exact inverse-probability weights preserve its represented mean when
the estimator is integrable. The research priority is recursive optimization,
variance control and mathematical guarantees. Runtime comparisons support
these questions; a single accurate curve does not establish finite variance
or optimal sampling.

Three complementary components are implemented:

- **Pointwise rate selection:** finite-depth moment quadrature differentiates
  the recursive child contributions and chooses a candidate rate on a supplied
  interval. The short-time rule is an approximation, not a finite-time optimum.
- **Full-tree certification:** separate exact-rational programs bound the
  candidate second moment from above and the global optimum from below for
  specified raw-uniform Allen–Cahn settings. Their difference bounds the
  objective gap; the corresponding mean-identification argument makes this
  also a variance gap. See the [certified-rate report](docs/research/results/certified-rate-checkpoint.md).
- **Shared-profile selection:** an optional weighted extension chooses one
  common scalar rate for several starting states. For the five-point wave
  benchmark at `T=0.05`, the cheap rule is certified within 1.60% of optimal
  weighted variance. This is neither an error bound on the rate itself nor
  a rate that adapts inside each tree. See the [profile report](docs/research/results/profile-efficiency-checkpoint.md).

The mathematical arguments, Python selectors/verifiers and Lean lemmas have
separate scopes. Lean does not formally verify the full stochastic solver or
the numerical certificate programs; consult the [proof registry](docs/research/proof-registry.md).

`TerminalTupleProposal(pde, floor_mass=0.1)` provides a cheap, support-preserving
terminal-data proxy for `q_c` at each branching decision. Pass the same proposal
to `optimize_exponential_rate_1d(..., tuple_proposal=proposal)` and
`CodingTreeMC(rate=result.rate, tuple_proposal=proposal).solve(pde, grid)`.
Custom labels distinguish sampling variants in the existing comparison table
and figure. Proposal tuning currently uses the serial path (`n_jobs=1`).

[`demo/variance_reduction.py`](demo/variance_reduction.py) compares the baseline,
rate-only, proposal-only, and combined settings using the original
`Solver.solve(...) -> Curve` interface. Its rate is selected at one reference
state and reused across the profile, so it is not a pointwise optimum at every
grid location. The existing Allen–Cahn, Merton, and network-solver demos keep
their original roles.

For pointwise variance and timing diagnostics, run:

```bash
conda run --no-capture-output -n parabolab python examples/sampling_tuning.py
```

The generic rate/proposal tuning above is **opt-in heuristic tuning**, not a universal formula or a certified
full-tree optimum: the rate objective uses finite-depth numerical quadrature,
and the proposal uses terminal values at the parent-birth state, not exact
continuation moments. The full-tree continuation second moments themselves
depend on `lambda`; the frozen-continuation local theorem does not supply them
for free. A positive proposal floor does not prove integrability. Defaults and
tree draw order are unchanged. Measure tuning overhead and sampling runtime
when making a speedup claim, separately from the algorithmic variance result. See the
[research checkpoint](docs/research/lambda-q-optimization-summary.md) for the
precise claims and remaining work.

`demo/rate_variance.py` adds rate-sensitivity plots for Allen–Cahn, Fisher–KPP
and binary Riccati. Its first three curves use finite-depth approximations;
only the specified binary control uses a closed-form full-tree moment.
Empirical error bars and U-shaped plots are diagnostics, not proofs of
strict convexity or optimality. See the [demo interpretation notes](demo/README.md#rate-sensitivity-diagnostics).

## Historical reproduction results

The following records describe the completed M1–M5 reproduction runs, not
fresh results on every later source revision. Numbers came from this repo's
scripts on a laptop CPU; "paper" denotes published values (GPU where
applicable). Cross-hardware runtimes are descriptive, not controlled speedup
measurements. Current source verification is recorded separately in the
[integration record](docs/research/results/integration-2026-09-16.md).

| reproduction | ours | reference |
|---|---|---|
| JEQ Figs 1, 4–9 (profile plots, d = 1..100) | within ~3·stderr of the exact solutions at paper budgets | — |
| JEQ Table 2: Allen–Cahn d = 100, u(0,0), T = 0.3 | 0.052665 (SD 0.000306, 5 × 10⁶ samples, rate 1) | coding trees 0.052754 ± 0.000364; deep BSDE ref 0.052802 |
| JEQ Table 5: HJB d = 100, u(0,0), T = 1 | **4.590153** (SD 0.0096, 5 × 10⁵ samples) vs exact 4.590162 | paper 4.580340 ± 0.001869 — 5 SDs below exact, see Notes |
| JCP Table 1: deep branching Allen–Cahn L1, full budget | d = 1: 1.25e-3 (2–3 CPU-min/run); d = 5: 3.47e-3 | d = 1: 1.32e-3 (28 GPU-min); d = 5: 3.63e-3 (110 GPU-min) |
| JCP Table 3: deep branching exponential d = 1 L1 | 1.25e-2 | 1.17e-2 (42 GPU-min) |
| JCP Table 5: deep branching Merton HJB L1 | median 1.0e-2 + the paper's tanh anomaly reproduced (Fig 7) | 8.49e-3 (54 GPU-min) |
| JCP Tables 1/3/5 three-way (vs vendored deep BSDE / DGM) | table below | Tables 1/3/5 columns |
| JCP Fig 2 blow-up study | empirical precision-loss thresholds: T ≈ 0.8–0.9 (jcp rate), T ≈ 1.0–1.1 (rate 1); authors' CSVs inside the recorded seed spread | `coding_trees` blow_up_analysis CSVs |

### Three-way comparison (M5, reduced budget: 3 runs, CPU)

`python examples/jcp_comparison_baselines.py` (append `--full` for the
paper's 10-run/full-M budgets).  L1 error, mean (SD); "paper" columns are
the published full-budget GPU values:

| problem | deep branching (ours) | deep BSDE (vendored) | deep Galerkin (vendored) |
|---|---|---|---|
| Allen–Cahn d = 1 (Table 1) | 2.08e-3 (6.8e-4), 19 s/run — paper 1.32e-3 | 4.26e-3 (1.3e-3), 46 s — paper 4.60e-3 | 7.66e-4 (4.3e-4), 45 s — paper 1.40e-3 |
| Allen–Cahn d = 5 (Table 1) | 3.64e-3 (3.4e-4), 18 s — paper 3.63e-3 | 4.70e-3 (3.8e-4), 51 s — paper 4.71e-3 | 4.10e-3 (1.7e-3), 181 s — paper 6.83e-3 |
| exponential d = 1 (Table 3) | 2.11e-2 (4.8e-3), 22 s — paper 1.17e-2 | 1.39e-2 (3.2e-3), 55 s — paper 1.39e-2 | 2.56e-2 (1.3e-2), 58 s — paper 2.53e-2 |
| Merton HJB d = 1 (Table 5) | 2.14e-2 (7.3e-4), 9 s — paper 8.49e-3 | **1.61e+0** (1.0e-1) — paper **1.61e+0** (fails) | inapplicable (loss divides by the net's 2nd derivative) — as in the paper |

These reduced-budget runs recover the main reported qualitative behavior,
including the poor deep-BSDE Merton result. They use different budgets from
the paper and do not establish a universal ranking of the methods. The full
M4 reproduction values are recorded above.

## Layout

| module | contents |
|---|---|
| `parabolab/pde.py` | `ParabolicPDE` (semilinear), `FullyNonlinearPDE1D` (sympy f/phi), `FullyNonlinearPDEnD` (d-dim `deriv_map` jets, diffusion σ², polynomial-support zero detection) |
| `parabolab/mechanism.py` | codes (`Id`, `Dx`, `DxN`, `FDeriv`, `FNu`) + semilinear mechanism (2.7) + `FullyNonlinearMechanism1D` (2.4)–(2.5) + d-dim `FullyNonlinearMechanismND` (JCP2024 §2) with reduced-set table construction |
| `parabolab/fdb.py` | multivariate Faà di Bruno enumeration, 1-d and d-dim, with monotone-predicate pruning (cross-checked against the authors' `deep_branching/fdb.py`) |
| `parabolab/tree.py` | recursive `TREE(t,x,c)` sampler, JCP2024 Alg. 1 / JEQ2023 Def. 4.1; d-dim BM with variance σ² |
| `parabolab/mc.py` | pointwise estimator: mean, stderr, tree-size diagnostics |
| `parabolab/proposals.py` | nonuniform tuple probabilities, pilot-frozen proposals, and the terminal-data proxy |
| `parabolab/moments.py` | deterministic finite-depth absolute-moment quadrature |
| `parabolab/rate_optimization.py` | finite-depth rate derivatives, bracket-constrained rate selection, and the binary Riccati oracle |
| `parabolab/profile_rates.py` | short-time weighted-profile rule and finite-depth selection of one common rate |
| `parabolab/rate_certificate.py`, `wave_certificate.py`, `profile_certificate.py` | exact-rational full-tree bounds for the specified Allen–Cahn flat, wave and profile settings |
| `parabolab/rate_variance.py` | finite-depth/MC rate diagnostics and a separate binary Riccati control; not a certificate verifier |
| `parabolab/solve.py` | uniform solver interface: `CodingTreeMC`, `DeepBranching`, `DeepBSDE`, `DeepGalerkin`, all `Solver(**budget).solve(pde, grid) -> Curve`, plus `compare(...)` for the table and figure; pins the grid convention and keeps torch out of the top-level import |
| `parabolab/parallel.py` | `estimate_parallel`: sample batches over worker processes (n_jobs-independent results; pure-Python `estimate` stays the reference) |
| `parabolab/profiles.py` | profile estimation over an x-grid and d-dimensional embedding; plotting is in `solve.py` |
| `parabolab/library.py` | Allen–Cahn (5.1)–(5.4) incl. d-dim; Dym (5.7), tan (5.8), cosine (5.10), log (5.11); exponential gradient (5.5); HJB (5.9) with Cole–Hopf exact value; Merton HJB (JCP 4.6, non-polynomial f) |
| `parabolab/deep/` | M4 deep branching solver (JCP2024 Alg. 2): `generator.py` (batched (τ,X,H̄) training data over worker processes, optional root codes), `net.py` (residual tanh net (3.2)–(3.3)), `solver.py` (Adam training loop, grid errors, Fig-7 consistency plot), `experiments.py` (repeated-run driver) |
| `parabolab/vendor/` | M5 vendored baselines: the authors' deep BSDE (`bsde.py`) and deep Galerkin (`galerkin.py`) solvers, verbatim from [deep_branching](https://github.com/nguwijy/deep_branching) @ `c06bef2` (MIT), plus our thin `adapters.py` (index mapping + sympy→torch lambdify — no solver logic of ours) |
| `parabolab/blowup.py` | M5 blow-up machinery: `sweep_T` (pointwise estimate/stderr/seed-spread/max\|H\| vs horizon T), `integrability_edge` (persistent drift or >5 % relative stderr) |
| `docs/research/` | current variance-reduction guide, theory notes, claim registry, and historical Merton records |
| `formal/` | Lean checks for selected algebraic and moment-iteration lemmas; coverage is listed in the proof registry |

## Completed reproduction milestones

- **M1 (done)** — semilinear coding trees, d = 1, pure Python/numpy;
  validated against the Allen–Cahn closed forms (traveling wave (5.3) and
  space-independent (5.4)) at $10^5$–$10^6$ samples, $T \le 0.5$.
- **M2 (done)** — general fully nonlinear mechanism via the multivariate
  Faà di Bruno formula (JEQ2023 eqs. (2.4)–(2.5)), d = 1, arbitrary
  derivative order n; sympy-based `FullyNonlinearPDE1D`; the four JEQ §5
  examples (Dym, tan, 4th-order cosine, 3rd-order log) reproduce Figs 6–9
  at the paper's sample budgets. Two paper errata found (see Notes).
- **M3 (done)** — multidimensional extension (JCP2024 §2): `deriv_map`
  jets, multi-index codes ∂^μ, diffusion σ², d-dim Brownian sampler,
  reduced-set mechanism construction (tractable at d = 100), and
  multiprocessing over sample batches. Reproduced JEQ §5.1: Fig 1
  (Allen–Cahn d = 5/100), Figs 4/5 (exponential gradient d = 5/10),
  Table 2 (Allen–Cahn d = 100, T = 0.3) and Table 5 (HJB d = 100, T = 1,
  exact 4.590162 via Cole–Hopf quadrature).
- **M4 (done)** — deep branching solver (JCP2024 §3 Algorithm 2 +
  Remark 3.1) in `parabolab/deep/`: batched (τ, X, H̄) training-data
  generator on top of the M3 sampler, the paper's residual tanh net,
  full-batch Adam with the paper's schedule, Fig-7 consistency
  diagnostic. Reproduced at **full paper budgets on CPU** (10 runs each):
  Table 1 Allen–Cahn d=1 L1 1.25e-3 (paper 1.32e-3) and d=5 3.47e-3
  (paper 3.63e-3); Table 3 exponential d=1 1.25e-2 (paper 1.17e-2);
  Table 5 Merton HJB median 1.0e-2 (paper 8.49e-3) including the paper's
  own tanh training anomaly, exposed by the Fig-7 plot. Runtimes: 2–5
  CPU-min/run vs the paper's 28–110 GPU-min/run (see Notes).
- **M5 (done)** — vendored baselines + blow-up study.  The authors' deep
  BSDE and deep Galerkin solvers run against our PDE library through a
  ~150-line adapter (`parabolab/vendor/`); the three-way comparison
  (`examples/jcp_comparison_baselines.py`) rebuilds JCP Tables 1/3/5
  including the paper's negative findings (deep BSDE fails on Merton at
  L1 ≈ 1.6, DGM inapplicable to Merton).  The blow-up study
  (`examples/blowup_allen_cahn.py`, machinery in `parabolab/blowup.py`)
  records empirical loss of precision for Allen–Cahn d = 1/10 — see
  the diagnostic interpretation below.

## Interpreting the historical blow-up diagnostics

`examples/blowup_allen_cahn_d{1,10}.png`: pointwise estimate of
u(0,0) for Allen–Cahn as the horizon T grows from 0.1 to 2.0
(3 seeds × 10⁵ samples, both ρ rates), overlaid on the authors'
`coding_trees` blow-up CSVs. The representation requires integrability, but
these finite-sample sweeps do not locate a mathematical integrability or
second-moment boundary. They measure how empirical precision deteriorates
under two sampling rates:

- **JCP rate −log(0.95)/T** (authors' choice, tiny trees, heavy leaf
  weights): no dramatic explosion — instead the *sample SD grows
  smoothly* until the estimator stops resolving the solution.  Our
  5 %-relative-stderr edge: **T ≈ 0.8 (d = 1), T ≈ 0.9 (d = 10)**.  The
  authors' single-seed curve falls within the recorded three-seed spread.
  This is consistent with substantial sampling variability; it does not
  establish bias or the existence of moments.
- **rate = 1** (the package default): recorded stderr stays ≲1 % out to
  T ≈ 0.9/1.0, followed by much larger observed weights (max |H| reaches 7.6e9 at
  T = 2, d = 1; estimates land at ±10³–10⁴).  Edge: **T ≈ 1.0 (d = 1),
  T ≈ 1.1 (d = 10)** under the recorded diagnostic rule.

Standard-error growth, maximum weights and seed spread are useful warning
signs. Their absence is not an integrability proof. The separate Dym
non-integrability theorem and the exact Allen–Cahn certificates supply
mathematical conclusions for their own explicitly stated settings.

## Notes

- ρ is Exp(rate); the package default is **rate = 1** (the "standard
  exponential" of JEQ2023's Mathematica appendix). JCP2024's choice
  `-log(0.95)/T` (`parabolab.jcp_rate`) showed larger sampling variability
  in the recorded one-dimensional Allen–Cahn runs. This observation is not
  a bias theorem or a universal comparison. See `CLAUDE.md` for gotchas.
- **Rate choice depends on the mechanism**: with a big reduced mechanism
  (HJB d = 100: |ℳ(f*)| = 20 000) every branching multiplies the weight by
  |ℳ|·e^{λτ}/λ. The sparse `jcp_rate` performed better than rate 1 in the
  recorded high-dimensional HJB runs. Neither rate is thereby proved optimal.
- **Table 5 tail anatomy (HJB d = 100)**: 10⁵-sample runs that miss the
  rare large-weight branches cluster at ≈ 4.580 with deceptively small
  stderr — precisely the paper's published 4.580340 ± 0.001869, which is
  5 of its own SDs below the exact 4.590162. Runs that catch monsters
  report honestly large stderr and centre on the exact value; our 5-run
  mean is 4.590153.
- Integrability and second-moment assumptions must be checked for the
  specified PDE, horizon, mechanism and sampling proposal. The saved
  Allen–Cahn certificates at `T=0.05` do not certify every benchmark horizon.
- **M4 implementation difference**: the authors' torch sampler evaluates the RAW mechanism
  (whose zero members dominate) with autograd-computed φ-derivatives on
  masked full-size tensors; our sampler walks the reduced mechanism with
  lambdified closed-form derivatives. Removing zero tuples and adjusting
  probabilities preserves the represented mean under the required
  integrability assumptions; it can change the sample distribution and
  variance. Historical CPU/GPU timing differences do not isolate this effect.
- **The JCP Fig-7 anomaly reproduces**: at full Merton budget one of our
  10 tanh runs (run 9) trains to L1 6.8e-2 while the other nine give
  5e-3–1.8e-2 — and the Fig-7 consistency plot (MC targets vs net) makes
  the bad fit visible at a glance, exactly the paper's point. Excluding
  the anomalous run our mean is 1.04e-2 (paper: 8.49e-3).
- **Dym non-integrability (JEQ Fig. 6)**: for the specified real-extension
  estimator, a fixed finite tree topology already gives an infinite absolute
  first moment at every positive exponential rate. There is no finite
  variance-minimizing rate for this estimator. Its demos and rate sweeps are
  diagnostics; a visually accurate finite-sample curve is not convergence
  evidence. See the [proof](docs/research/estimator-integrity/dym-nonintegrability.md).
- **Paper errata found in JEQ2023 §5** (both sympy-verified, see
  `parabolab/library.py`): (i) the quartic terminal-condition coefficients of
  the cosine example (5.10) as printed (b = −36/47, c = 24b, d = 4b²) do not
  solve the PDE — the correct values are b = 3/8, c = 1/16, e = 257/256;
  (ii) the paper text says α = 5 for the log example (5.11) while the
  authors' notebook uses α = 10 (we follow the paper).
