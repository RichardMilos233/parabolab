# parabolab

From-scratch Python reproduction of the **coding trees** Monte Carlo method for
fully nonlinear parabolic PDEs by Nguwi, Penent & Privault (NTU):

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
$\phi$ (JEQ2023 Thm. 1, JCP2024 Alg. 1).

## Quickstart

```bash
conda env create -f environment.yml     # or: conda env update -f environment.yml
conda activate parabolab
pytest                                  # fast suite (~30 s)
pytest -m 'slow or not slow'            # + paper-budget validation (minutes)
python examples/jeq_allen_cahn_1d.py    # M1: Allen-Cahn vs closed form
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
```

The `jcp_*_deep.py` scripts default to reduced Monte Carlo budgets;
pass `--full` for the paper's budgets and `--device cuda` on a GPU
machine (everything is device-agnostic, CPU by default).

```python
from parabolab import estimate
from parabolab.library import allen_cahn_wave_1d

pde = allen_cahn_wave_1d(T=0.5)
r = estimate(pde, t=0.0, x=0.0, n_samples=100_000, seed=0)
print(r, "exact:", pde.exact_solution(0.0, 0.0))
```

## Layout

| module | contents |
|---|---|
| `parabolab/pde.py` | `ParabolicPDE` (semilinear), `FullyNonlinearPDE1D` (sympy f/phi), `FullyNonlinearPDEnD` (d-dim `deriv_map` jets, diffusion σ², polynomial-support zero detection) |
| `parabolab/mechanism.py` | codes (`Id`, `Dx`, `DxN`, `FDeriv`, `FNu`) + semilinear mechanism (2.7) + `FullyNonlinearMechanism1D` (2.4)–(2.5) + d-dim `FullyNonlinearMechanismND` (JCP2024 §2) with reduced-set table construction |
| `parabolab/fdb.py` | multivariate Faà di Bruno enumeration, 1-d and d-dim, with monotone-predicate pruning (cross-checked against the authors' `deep_branching/fdb.py`) |
| `parabolab/tree.py` | recursive `TREE(t,x,c)` sampler, JCP2024 Alg. 1 / JEQ2023 Def. 4.1; d-dim BM with variance σ² |
| `parabolab/mc.py` | pointwise estimator: mean, stderr, tree-size diagnostics |
| `parabolab/parallel.py` | `estimate_parallel`: sample batches over worker processes (n_jobs-independent results; pure-Python `estimate` stays the reference) |
| `parabolab/profiles.py` | profile estimation over an x-grid (+ d-dim embedding) + Fig-style plotting |
| `parabolab/library.py` | Allen–Cahn (5.1)–(5.4) incl. d-dim; Dym (5.7), tan (5.8), cosine (5.10), log (5.11); exponential gradient (5.5); HJB (5.9) with Cole–Hopf exact value; Merton HJB (JCP 4.6, non-polynomial f) |
| `parabolab/deep/` | M4 deep branching solver (JCP2024 Alg. 2): `generator.py` (batched (τ,X,H̄) training data over worker processes, optional root codes), `net.py` (residual tanh net (3.2)–(3.3)), `solver.py` (Adam training loop, grid errors, Fig-7 consistency plot), `experiments.py` (repeated-run driver) |

## Milestones

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
- **M5** — vendor the authors' baselines and run systematic comparisons
  (their `coding_trees/logs/final` CSVs, deep BSDE, multilevel Picard).

## Notes

- ρ is Exp(rate); the package default is **rate = 1** (the "standard
  exponential" of JEQ2023's Mathematica appendix). JCP2024's choice
  `-log(0.95)/T` (`parabolab.jcp_rate`) yields heavier-tailed weights: at
  T = 0.5 its empirical mean shows a visible systematic deviation — also
  present in the authors' own logs. See `CLAUDE.md` for gotchas.
- **The optimal rate flips at large d**: with a big reduced mechanism
  (HJB d = 100: |ℳ(f*)| = 20 000) every branching multiplies the weight by
  |ℳ|·e^{λτ}/λ, so frequent branching (rate 1) compounds catastrophically
  — the sparse `jcp_rate` is *essential* there, the opposite of the d = 1
  recommendation.
- **Table 5 tail anatomy (HJB d = 100)**: 10⁵-sample runs that miss the
  rare large-weight branches cluster at ≈ 4.580 with deceptively small
  stderr — precisely the paper's published 4.580340 ± 0.001869, which is
  5 of its own SDs below the exact 4.590162. Runs that catch monsters
  report honestly large stderr and centre on the exact value; our 5-run
  mean is 4.590153.
- The method is short-time by nature: integrability of $\mathcal H$
  (JEQ2023 Prop. 4.2) can fail for large T; Allen–Cahn at T ≲ 0.5 is safely
  inside the window.
- **Why our M4 runs are ~30x faster than the paper's GPU runs at the same
  sample budgets**: the authors' torch sampler evaluates the RAW mechanism
  (whose zero members dominate) with autograd-computed φ-derivatives on
  masked full-size tensors; our sampler walks the reduced mechanism with
  lambdified closed-form derivatives. Same estimator distribution, far
  fewer operations. The deep branching runtime is dominated by data
  generation; training (P = 3000 full-batch epochs, N = 1000) is ~10 s.
- **The JCP Fig-7 anomaly reproduces**: at full Merton budget one of our
  10 tanh runs (run 9) trains to L1 6.8e-2 while the other nine give
  5e-3–1.8e-2 — and the Fig-7 consistency plot (MC targets vs net) makes
  the bad fit visible at a glance, exactly the paper's point. Excluding
  the anomalous run our mean is 1.04e-2 (paper: 8.49e-3).
- **Dym instability (JEQ Fig. 6)**: the terminal condition $(6x)^{2/3}$ has
  factorially growing high-order derivatives, so $\mathcal H$ has divergent
  higher moments at *every* Exp rate — increasing the sample count surfaces
  ever-bigger "monster" samples instead of converging (compare
  `examples/jeq_fig6_dym.py` at 1e5 vs 1e6, and `examples/rate_study_dym.py`).
  The paper's clean Fig. 6 at 1e5 samples is a lucky draw; ours at seed 0
  shows the true behaviour.
- **Paper errata found in JEQ2023 §5** (both sympy-verified, see
  `parabolab/library.py`): (i) the quartic terminal-condition coefficients of
  the cosine example (5.10) as printed (b = −36/47, c = 24b, d = 4b²) do not
  solve the PDE — the correct values are b = 3/8, c = 1/16, e = 257/256;
  (ii) the paper text says α = 5 for the log example (5.11) while the
  authors' notebook uses α = 10 (we follow the paper).
