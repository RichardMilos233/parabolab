# 2026-09-15-post-integrity-directions — Ten directions

## Search record

Date: 2026-09-15. Tools: WebSearch (US index), WebFetch of arXiv abstract
pages and one full PDF, GitHub page fetch. This is a **bounded** search: eight
queries, no Google Scholar / MathSciNet, no citation-graph crawl. Absence
from this search does not establish global novelty.

Queries (verbatim): `"coding trees" fully nonlinear PDE Monte Carlo branching
2025 2026 arXiv`; `Nguwi Penent Privault 2025 2026 branching diffusion fully
nonlinear Feynman-Kac new paper`; `Huang Privault 2026 "Monte Carlo" ODE
solutions branching "Hamilton-Jacobi" weighted progeny arXiv`; `multilevel
Picard fully nonlinear PDE gradient nonlinearity 2025 2026 arXiv Hutzenthaler
Nguyen`; `branching diffusion Monte Carlo importance sampling variance
reduction nonlinear PDE "branching" 2025 arXiv`; `Nguwi Privault 2025 OR 2026
"branching" PDE bounded domain OR "deep branching" OR "coding trees" new
arXiv`; `Lean 4 Mathlib formalization Monte Carlo estimator unbiased OR
"branching process" OR "Galton-Watson" OR "Feynman-Kac" 2025 2026`; `walk on
spheres nonlinear PDE recursive Monte Carlo estimator variance "branching"
OR "fixed point" graphics 2025 2026 arXiv`; `"deep branching" OR "branching
diffusion" Navier-Stokes OR HJB OR "bounded domain" neural network solver
2025 2026 arXiv Nguwi`.

Primary sources examined:

| Source | What was read | Relevance |
|---|---|---|
| [arXiv:2502.17853v2](https://arxiv.org/abs/2502.17853) Huang & Privault, *Stability analysis of a branching diffusion solver for semilinear heat equations* (v1 25 Feb 2025 titled "...for nonlinear PDEs"; v2 9 Mar 2026) | Full PDF pp. 1–26: Defs 2.1–2.2 (normalized codes \(\alpha!^{-1}\partial^\alpha\), at-most-binary mechanism), Assumption \(H_\rho\), Props 2.5–2.6 (factorial / exponential growth sufficient \(L^1\) criteria via a contact Hamilton–Jacobi equation for the generating function of the multiplicative weighted progeny), Thms 2.8, 2.10 (classical / mild / viscosity representation), Sec. 4 numerics (Allen–Cahn and a functional example, d up to 1000, comparison with NPP23 and deep BSDE), Sec. 5 (coded PDE system (2.14), Props 5.2, 5.7 uniqueness under uniform integrability). Code: `github.com/nprivaul/coding_trees_v2` (notebooks, no README). | Closest prior art for D01/D04/D05/D08. Semilinear \(f(u)\) only; sufficient, not exact; \(L^1\) only. Authors report their binary mechanism "generally less stable numerically" than NPP23 and that NPP23 at d = 1000, T = 0.5 gives −0.67516 vs exact −0.67918 (heavy-tail bias consistent with gotcha 5). |
| [arXiv:2501.10951](https://arxiv.org/abs/2501.10951) Huang & Privault, *Binary Galton–Watson trees with mutations* (2025) | Abstract | Multitype GW machinery of the same group; no PDE / Monte Carlo content. |
| [arXiv:2606.18919](https://arxiv.org/abs/2606.18919) Chan & Privault, wave equations with complex polynomial nonlinearities (Jun 2026) | Abstract | Integrability criteria for branching estimators of nonlinear **wave** equations — sibling `wavelab` domain, not this project. |
| [arXiv:2310.12545](https://arxiv.org/abs/2310.12545) Hutzenthaler & Nguyen, MLP for semilinear PDEs with gradient-dependent nonlinearities (JNMA 2025); [arXiv:2410.00203](https://arxiv.org/abs/2410.00203) Nguyen, MLP in \(L^p\) | Abstracts / search summaries | Closest prior art for D05; no fully nonlinear / higher-derivative results. |
| [arXiv:2409.08526](https://arxiv.org/abs/2409.08526) Deep Picard iteration; [arXiv:2508.14215](https://arxiv.org/abs/2508.14215) Deep BSDE on bounded domains | Titles / abstracts | Context for D05/D06. |
| [arXiv:2410.18944](https://arxiv.org/abs/2410.18944) Path guiding for Monte Carlo PDE solvers; [arXiv:2604.21717](https://arxiv.org/abs/2604.21717) Monte Carlo PDE solvers for nonlinear radiative BCs (2026); Walk-on-probes / walk-on-heat-stars (2026) | Abstracts | Graphics-community recursive Monte Carlo PDE solvers with learned proposals and MIS — source of D09. |
| [arXiv:2606.01356](https://arxiv.org/abs/2606.01356) Coelho, *A Formally Verified Library of Mathematical Finance in Lean 4* (2026) | Abstract | Mathlib + BrownianMotion package now reach Itô and a Feynman–Kac link; no branching / Monte Carlo — context for D10. |
| Nicolas Privault arXiv author page | 2025–2026 listing | No other branching/PDE preprint found beyond the above. |
| [arXiv:1603.01727](https://arxiv.org/abs/1603.01727) HLOT+19 (known) | Not re-read; Thm 3.5 majorant ODE cited from memory and from HP26's citation | Prior art for the majorant technique in D01. |

Not searched (limits): journal-only venues, Chinese-language preprints,
the `coding_trees_v2` notebook internals, Jelenković–Olvera-Cravioto 2012
(cited from memory for D03 — must be re-read before D03 is executed).

## Direction cards D01–D10

Full fields (gap, hypothesis, scores with rationale, evidence, feasibility,
first test) are in [ideas.json](ideas.json); computed values in
[scores.json](scores.json). Summary:

| ID | Direction | N × I × E | Value | Feasibility | Evidence |
|---|---|---|---|---|---|
| D01 | Supersolution certificates and exact \(L^p\) horizons for fully nonlinear coding trees | 10 × 10 × 100 | **10000** | feasible | searched |
| D02 | Optimal exponential rate theorem: \(T^*_2(\lambda)\) and the second-moment-minimizing rate | 10 × 10 × 10 | 1000 | feasible | searched |
| D03 | Tail index = \(L^p\) threshold; heavy-tail-corrected confidence intervals | 10 × 10 × 10 | 1000 | conditional | searched |
| D04 | Exact second-moment comparison: HP26 binary mechanism vs Faà-di-Bruno mechanism | 10 × 10 × 10 | 1000 | feasible | searched |
| D05 | Multilevel Picard over the coded PDE system for fully nonlinear PDEs | 10 × 100 × 10 | **10000** | conditional | searched |
| D06 | Moment-certified time patching with a network terminal condition | 10 × 10 × 10 | 1000 | conditional | searched |
| D07 | Non-smooth payoffs: mollification error vs moment blow-up | 10 × 10 × 10 | 1000 | feasible | searched |
| D08 | Proved state-dependent representation theorem + Merton–Vasicek 2D completion | 10 × 10 × 10 | 1000 | feasible | searched |
| D09 | Learned state-dependent first-event proposals with MIS safety (path guiding) | 10 × 10 × 10 | 1000 | conditional | searched |
| D10 | Measure-theoretic Lean formalization of Theorem 2.2 | 1 × 10 × 10 | 100 | feasible | searched |

Hardest obstacle and fallback per card (not in the JSON schema):

- **D01** — obstacle: for infinite code spaces (derivative codes of unbounded
  order) a supersolution needs a generating-function ansatz over derivative
  order with factorial weights; the Faà-di-Bruno table sizes grow with
  order, so the ansatz must absorb \(|\mathcal M(c)|\). Fallback: exact
  horizons for the finite (polynomial-\(f\)) systems only, plus numerical
  truncated iterations for the others labelled "conditional certificate".
  Effort: 3–5 weeks (grid iteration 1 week; certificates 2–3 weeks; Lean
  instantiation of `picard_le_prefixed` on the concrete table 1 week).
- **D02** — obstacle: proving uniqueness of the minimizer; fallback: numerical
  rate map with a theorem only for the depth-1 truncation. Effort: 1–2 weeks
  on top of D01.
- **D03** — obstacle: Cramér / non-lattice condition for the tree recursion;
  fallback: empirical Hill estimates and median-of-means intervals without
  the identification theorem. Effort: 2–3 weeks.
- **D04** — obstacle: the binary mechanism uses normalized codes and its own
  proposal (HP26 (2.4a)–(2.4b)); a like-for-like comparison must match the
  proposal or compare at each mechanism's optimal proposal. Fallback:
  empirical variance comparison only. Effort: 2 weeks.
- **D05** — obstacle: MLP convergence proofs need Lipschitz nonlinearity;
  product nonlinearities are only locally Lipschitz, and the code system is
  infinite. Fallback: empirical MLP on the finite Allen–Cahn code system.
  Effort: 6+ weeks; theorem uncertain.
- **D06** — obstacle: network (and derivatives) as terminal condition inside
  the sampler (scoped out in M4). Fallback: patching for the semilinear
  case (Id leaves only). Effort: 3–4 weeks after D01.
- **D07** — obstacle: PDE-stability constant for the mollified Dym problem;
  fallback: numerical trade-off curve only. Effort: 2 weeks.
- **D08** — obstacle: existence of a classical solution for the 2D
  Merton–Vasicek HJB with the required derivative bounds. Fallback:
  conditional theorem with the existence assumption stated. Effort: 3 weeks.
- **D09** — obstacle: topology/cost change from event-time proposals;
  fallback: drop after the oracle test. Effort: 3 weeks.
- **D10** — obstacle: expressing lifetime × position × tuple product measure
  in Mathlib's `Kernel` API. Fallback: leaf term only. Effort: 3–4 weeks.

## Probe evidence recorded during ideation

Command (2026-09-15, conda env `parabolab`, `parabolab.moments`):
`finite_depth_moment_1d(allen_cahn_wave_1d(T=0.5), 0.0, 0.0, p, max_depth=n, rate, quadrature=MomentQuadrature(5,5))`
(6×6 for the \(p=1\) rows). Values are finite-depth iterates
\(V^{(p)}_{\mathrm{Id},n+1}(0,0)\); quadrature orders are low, so digits
beyond the second are not trusted.

| p | rate | n=0 | n=1 | n=2 | n=3 |
|---|---|---|---|---|---|
| 1 | 1.0 | 0.500 | 0.668 | 0.696 | — |
| 1 | 0.1026 | 0.500 | 0.668 | 0.696 | — |
| 2 | 1.0 | 0.454 | 0.550 | 0.567 | 0.607 |
| 2 | 0.1026 | 0.290 | 0.888 | 1.741 | 33.56 |

Reading: the \(p=1\) iterates are proposal-independent (the exponent
\(1-p\) vanishes — a corollary of Theorem 2.2 worth stating explicitly:
**no lifetime law or tuple proposal can change \(L^1\) integrability**);
the \(p=2\) iterates at the JCP rate grow super-geometrically while at rate
1 they grow slowly. This is consistent with gotchas 5 and 31 but is not yet a
result: convergence at rate 1 is unproved and the depth-3 jump (0.567 →
0.607) may be quadrature error. Depth ≥ 4 is out of reach for the
tree-recursive implementation (an 8×8 run to depth 5 was killed after 10
min) — the grid iteration is D01's first deliverable.

## Ranking and recommendation

Computed ranking ([scores.json](scores.json), ties by ID): D01, D05, D02,
D03, D04, D06, D07, D08, D09, D10. Script shortlist (searched + feasible +
value > 1000): **D01 only**. High-value conditional lead: **D05**. The
remaining seven score exactly 1000 or below and do not qualify.

Recommendation (not changing any arithmetic):

1. **Execute D01** — supersolution certificates and exact \(L^p\) horizons.
   It is the direct continuation of the completed programme (uses Theorems
   2.2–2.3 and the existing Lean prefixed-point lemma), it addresses the
   exact gap the closest 2026 paper stepped back from, and its first test
   is cheap. D02 and D04 are near-free corollaries once the grid iteration
   exists (rate sweep; second mechanism table) and should be folded into
   the D01 plan as stretch claims rather than run separately.
2. **Keep D05 as a lead**, not a project: run its first test (textbook MLP on
   the finite Allen–Cahn code system at T = 1, 2) only after D01, because
   D01's horizon tells exactly where MLP would have to beat the tree.
3. **D08 is the finance continuation** and can proceed in parallel at the
   implementation level (2D solver validation) without competing for the
   theory budget; its integrability certificate is a D01 output.

Rejected for now: D06 (needs sampler surgery scoped out in M4), D09 (oracle
gain unproven; tuple-proposal experiment gave 2 %), D10 (worthwhile only once
D01 gives a concrete certificate to formalize), D03 and D07 (good follow-ons
that both consume D01's horizon computations).

What could overturn the D01 assessment: (i) a majorant/supersolution
treatment of Faà-di-Bruno coding trees in the `coding_trees_v2` notebooks or
in a journal version of HP26 not indexed by arXiv; (ii) the grid iteration
showing that rate-1 iterates also diverge at T = 0.5 (then the certificate
covers a shorter horizon and the effect score drops to 10).
