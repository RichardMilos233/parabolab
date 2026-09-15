# 2026-09-15-post-integrity-directions — Context

Mode: `ideate` (plan only; no direction executed). Requested by the user on
2026-09-15: "analyze current progress, look up online (latest papers, repos),
come up with some ideas."

## Main objective and mathematical object

`parabolab` is a from-scratch reproduction and extension of the coding-tree
Monte Carlo method for fully nonlinear parabolic PDEs

\[
\partial_t u + \tfrac{\sigma^2}{2}\Delta u + f(x, D^{\alpha_1}u, \ldots, D^{\alpha_m}u) = 0,
\qquad u(T,\cdot) = \phi,
\]

(JEQ2023, JCP2024). The solution is \(u(t,x) = \mathbb E[H_{t,x,\mathrm{Id}}]\)
for a random coding tree: particles carry operator codes, move as Brownian
motions, die at Exp(rate) times, branch into code tuples drawn uniformly from
the mechanism table \(\mathcal M(c)\), and leaves evaluate their code on
\(\phi\). Known inputs: \(f, \phi, T, \sigma^2\), the lifetime rate, and the
tuple proposal. Unknowns of research interest: for which \((T, \text{rate},
\text{proposal})\) the functional \(H\) has finite \(L^p\) moments, how the
estimator behaves when it does not, and how the representation extends
(state dependence, non-smooth data, longer horizons).

## What already exists (inspected on 2026-09-15)

- Milestones M1–M6 complete (README, CLAUDE.md): semilinear and fully
  nonlinear mechanisms in d = 1 and d = n, deep branching solver, vendored
  deep BSDE / DGM baselines, blow-up study, uniform solver interface. All JEQ
  figures/tables and JCP tables reproduced; 37 documented gotchas.
- Estimator-integrity programme (design spec 2026-09-09, commits
  `c66a5c8`..`40ecb51`): three proved theorems with prose proofs and partial
  Lean 4 coverage —
  1. exact multitype \(L^p\) moment recursion and minimal-fixed-point
     criterion (`notation-and-moment-theorem.md` Thms 2.2–2.3;
     `MomentIteration.lean`: `momentStep_mono`, `picard_le_prefixed`,
     `picard_iSup_least`, `momentStep_iSup_picard`);
  2. Dym coding-tree non-integrability at every \(T>0\)
     (`dym-nonintegrability.md` Thm 4.1 / Cor 4.2; `Dym.lean`);
  3. safe adaptive pilot/frozen tuple proposals
     (`adaptive-proposals.md` Thms 6.1–6.4; `Proposal.lean`).
  Seven secondary candidates ledgered in `secondary-candidates.md`
  (Candidate 4 conditional; 5, 6 prior-art overlap; 7 conjecture; 8
  conditional; 9, 10 proved). Reproducibility ledger records 173 Python
  tests green and a sorry-free `lake build` (3386 jobs) on the research
  worktree (macOS paths; not rerun on this Windows machine today).
- Stochastic-rate Merton extension (design 2026-09-07): state-dependent
  mechanism (`state_dependent.py`), reduced 1D and full 2D Merton–Vasicek
  builders, Vasicek no-consumption exact benchmark, demo scripts. Stage 1
  (reduced problem) numerically validated; stages 2–4 not finished.
- Code modules relevant here: `moments.py` (`finite_depth_moment_1d`,
  tree-recursive quadrature of Theorem 2.2), `proposals.py`,
  `integrability.py`, `blowup.py`.

Historical statements not rerun today: the 173-test and Lean build results.
Evidence produced today: the moment-iterate probe recorded in `01-ideas.md`.

## Gap and failed approaches

Strongest unresolved obstacle: **no verifiable integrability/variance
certificate exists for the Faà-di-Bruno coding-tree estimator at the
horizons the papers use.** JEQ2023 Prop. 4.2 is too conservative to certify
any practical case (CLAUDE.md, "Paper pointers"); Huang–Privault 2026
(arXiv:2502.17853v2) certify only semilinear \(f(u)\) with their own binary
mechanism and narrowed their scope from "nonlinear PDEs" (v1, Feb 2025) to
"semilinear heat equations" (v2, Mar 2026). Practitioners currently judge
usability from plots, which gotchas 5, 15, 19, 20 and 31 show is unreliable
(heavy tails masquerade as bias; the published HJB d = 100 value is 5 of its
own SDs from exact).

Known failed / limited routes: Prop. 4.2-style uniform bounds (unattainable
at T = 0.5); tuple-only proposals (cannot repair a non-integrable target —
Dym; only 2 % work-normalized gain on Merton–Vasicek); the tree-recursive
`finite_depth_moment_1d` (cost exponential in depth: depth 5 at 8×8
quadrature did not finish in 10 min).

## Resources and scope

- Tools: conda env `parabolab` (Python 3.11, numpy/sympy/torch CPU), Lean 4
  v4.33.0 + Mathlib (project skill `lean-proof-verification`), 16-core
  laptop CPU, web search (bounded), authors' repos cloned next to the repo
  on the original machine (not verified present on this machine).
- Source revision: `40ecb51` on `main`; working tree has untracked
  `.agents/`, `.claude/`, `AGENTS.md` and this run directory only.
- Scope requested: ideation only. No implementation started; the one probe
  run is recorded as evidence, not as a result.
- Model actually used for this run: Claude Opus 5 (claude-opus-5) for every
  role; the skill's configured `gpt-6-astra` / `gpt-5.6-sol` routing is not
  selectable in this host and was not applied.
