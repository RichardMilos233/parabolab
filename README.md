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
pytest                                  # fast suite (~5 s)
pytest -m 'slow or not slow'            # + paper-budget validation (~30 s)
python examples/jeq_allen_cahn_1d.py    # M1: Allen-Cahn vs closed form
python examples/jeq_fig6_dym.py         # M2: JEQ Figs 6-9 reproductions
python examples/jeq_fig7_tan.py         #     (each prints a table and saves
python examples/jeq_fig8_cosine.py      #      a .png next to the script)
python examples/jeq_fig9_log.py
```

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
| `parabolab/pde.py` | `ParabolicPDE` (semilinear spec) and `FullyNonlinearPDE1D` (sympy f/phi, lazy derivative caches) |
| `parabolab/mechanism.py` | codes (`Id`, `Dx`, `FDeriv`, `FNu`) + semilinear mechanism (2.7) + general `FullyNonlinearMechanism1D` (2.4)–(2.5) |
| `parabolab/fdb.py` | multivariate Faà di Bruno term enumeration (cross-checked against the authors' `deep_branching/fdb.py`) |
| `parabolab/tree.py` | recursive `TREE(t,x,c)` sampler, JCP2024 Alg. 1 / JEQ2023 Def. 4.1 |
| `parabolab/mc.py` | pointwise estimator: mean, stderr, tree-size diagnostics |
| `parabolab/profiles.py` | profile estimation over an x-grid + Fig-style plotting |
| `parabolab/library.py` | Allen–Cahn (5.2)–(5.4); Dym (5.7), tan (5.8), 4th-order cosine (5.10), 3rd-order log (5.11) with exact solutions |

## Milestones

- **M1 (done)** — semilinear coding trees, d = 1, pure Python/numpy;
  validated against the Allen–Cahn closed forms (traveling wave (5.3) and
  space-independent (5.4)) at $10^5$–$10^6$ samples, $T \le 0.5$.
- **M2 (done)** — general fully nonlinear mechanism via the multivariate
  Faà di Bruno formula (JEQ2023 eqs. (2.4)–(2.5)), d = 1, arbitrary
  derivative order n; sympy-based `FullyNonlinearPDE1D`; the four JEQ §5
  examples (Dym, tan, 4th-order cosine, 3rd-order log) reproduce Figs 6–9
  at the paper's sample budgets. Two paper errata found (see Notes).
- **M3** — performance backend (numba and/or vectorized batching) for large
  sample counts and d up to 100 (paper-scale experiments).
- **M4** — deep branching solver (JCP2024 Alg. 2): torch (CPU default,
  GPU optional) neural regression on tree samples.
- **M5** — vendor the authors' baselines and run systematic comparisons
  (their `coding_trees/logs/final` CSVs, deep BSDE, multilevel Picard).

## Notes

- ρ is Exp(rate); the package default is **rate = 1** (the "standard
  exponential" of JEQ2023's Mathematica appendix). JCP2024's choice
  `-log(0.95)/T` (`parabolab.jcp_rate`) yields heavier-tailed weights: at
  T = 0.5 its empirical mean shows a visible systematic deviation — also
  present in the authors' own logs. See `CLAUDE.md` for gotchas.
- The method is short-time by nature: integrability of $\mathcal H$
  (JEQ2023 Prop. 4.2) can fail for large T; Allen–Cahn at T ≲ 0.5 is safely
  inside the window.
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
