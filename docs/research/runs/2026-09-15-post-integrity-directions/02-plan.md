# 2026-09-15-post-integrity-directions — Research plan (proposed, not started)

Ideation-only run: this plan is the deliverable. Nothing below has been
executed.

## Selected direction and success/failure criteria

**D01 — Supersolution certificates and exact \(L^p\) horizons for fully
nonlinear coding trees** (value 10000; feasible; searched).

Worth testing because Theorem 2.3's minimality already makes any prefixed
point \(W \ge \Phi_p(W)\) a certificate, the Lean lemma
`picard_le_prefixed` already checks that implication, and the 2026 paper
closest to this question (HP26) covers only semilinear \(f(u)\) with a
different mechanism.

Success: (S1) a grid Picard iteration reproducing the probe iterates and
converging for Allen–Cahn d = 1, T = 0.5, rate 1, \(p = 2\); (S2) an explicit
certified bound \(W\) with a written proof of \(\Phi_2(W)\le W\) for that
case and for the JEQ Fig 7–9 examples at their paper horizons; (S3) a proof
that the JCP rate at T = 0.5 has \(V^{(2)} = \infty\) (a subsolution that
blows up, or divergence of a lower bound); (S4) the exact
\(T^*_1, T^*_2(\text{rate})\) curves for Allen–Cahn matched against the
blow-up study (`examples/blowup_allen_cahn.py`).

Refutation: rate-1 iterates diverge at T = 0.5 (then the horizon is shorter
than the paper's own experiments, still a result, but effect drops to 10);
or no supersolution ansatz closes for the derivative-code examples (then
D01 reduces to the polynomial-\(f\) finite-code case).

## Target statements and hardest obstacle

- **C1 (corollary of Thm 2.2).** \(V^{(1)}\) is independent of the lifetime
  law and tuple proposal; hence \(L^1\) integrability of \(H\) cannot be
  changed by any importance proposal. Assumptions: (H1)–(H7). Proof: the
  exponent \(1-p\) vanishes in (2.4). Trivial but worth stating; it is the
  theoretical reason behind the "proposal cannot repair Dym" remark.
- **C2 (certificate principle, concrete form).** For a finite code space and
  polynomial \(f\), if \(W:[0,T]\times\mathbb R\to[0,\infty)^{\mathcal C}\)
  satisfies \(\Phi_p(W)\le W\) pointwise then \(\mathbb E|H|^p \le W\).
  Proof: Theorem 2.3 minimality. Lean: already `picard_le_prefixed` /
  `picard_iSup_least` on the abstract lattice; new work is instantiating
  `FiniteMechanism` with the Allen–Cahn table and discharging the
  inequality for a concrete \(W\) (interval arithmetic or exact rationals).
- **C3 (Allen–Cahn certificate).** Explicit \(W\) of the form
  \(W_c(t,x) = a_c\,e^{b_c (T-t)}\) (spatially uniform, using
  \(|\phi^{(k)}|\le K_k\)) with \(\Phi_2(W)\le W\) at rate 1, T = 0.5.
  Hardest step: the product terms couple codes; the ODE system for the
  \(a_c e^{b_c s}\) ansatz must admit a solution up to \(s = 0.5\) — this is
  a Riccati-type blow-up-time computation (HLOT+19 Thm 3.5 style) but with
  the \(q^{1-p}\rho^{1-p}\) weights, which is what makes the rate enter.
- **C4 (JCP-rate divergence).** A lower bound \(W' \le \Phi_2(W')\) with
  \(W'\uparrow\infty\) in finitely many iterations at rate 0.1026, T = 0.5.
  Proof route: restrict to the depth-1 branch term, which already gives
  \(q^{-1}\rho^{-1}\) factors of size \(\ge 3/0.1026 \approx 29\).
- **C5 (derivative-code certificates, conditional).** For the tan (5.9),
  cosine (5.10) and log (5.11) examples, a weighted generating function
  \(W_{D^k}(t) = \theta^k k!\,w(t)\) over derivative order with
  \(|\phi^{(k)}|\le C\theta^k k!\) (HP26 Prop 2.5 style growth). Hardest
  obstacle: table sizes \(|\mathcal M(D^k)|\) grow with \(k\); the ansatz
  must absorb \(|\mathcal M|\cdot q^{-1}\). Exit: if no closed ansatz works,
  report numerically truncated iterations as "conditional certificate" and
  mark C5 pending.
- **Stretch (D02).** Map \(\lambda \mapsto V^{(2)}(0,0;\lambda)\) on the grid
  and locate the minimizer; theorem only if the structure is clean.
- **Stretch (D04).** Implement HP26's binary mechanism for Allen–Cahn and
  evaluate its \(V^{(2)}\) on the same grid.

## Numerical protocol and Lean scope

Reference checks: (i) grid iteration at depth ≤ 3 must reproduce the
tree-recursive probe values within quadrature tolerance; (ii) Monte Carlo
sample second moments (existing `tests/test_moments.py` cross-check pattern)
at 1e5–1e6 samples must lie within their (heavy-tailed) error of the grid
value where it is finite; (iii) the blow-up study's SD explosion at
T ≈ 1.0/1.1 (rate 1) must coincide with the computed \(T^*_2(1)\) within
grid resolution.

Baseline: JEQ Prop. 4.2 (certifies nothing) and HP26 Prop 2.5 applied to the
Allen–Cahn semilinear case (quantify its admissible T against \(T^*_1\)).
Regime: d = 1 only for the theorems; d = 5/100 Allen–Cahn tables can be
handled numerically via the radial symmetry of \(\phi\) if time permits.
Seeds: fixed per script; no outlier trimming. Cost target: grid iteration
\(\le\) 1 min per (T, rate, p) on the laptop CPU.

Lean scope: instantiate `FiniteMechanism` for the 5-code Allen–Cahn table
with `ENNReal` leaf and branch weights taken from a certified \(W\), and
prove `momentStep M leaf branch W ≤ W` by `norm_num` / `positivity` on
rational bounds; conclude via `picard_iSup_least`. The measure-theoretic
link (Theorem 2.2 itself) stays prose (D10 is separate).

## Task handoffs (proposed)

| Task | Role | Requested model/effort (skill config) | Actual model available | Inputs | Owned files | Deliverable / acceptance | Budget |
|---|---|---|---|---|---|---|---|
| T01 grid Picard iteration | implementation | gpt-5.6-sol / xhigh | claude-opus-5 (no switch possible in this host) | Theorem 2.2 (2.4), `moments.py` API, probe table | `parabolab/moments.py` (new `grid_moment_1d`), `tests/test_moments.py` | reproduces probe to 1e-2; `pytest tests/test_moments.py` green | 1 week |
| T02 certificates C3, C4 | research | gpt-6-astra / max | claude-opus-5 | T01 output, HLOT+19 Thm 3.5, HP26 Prop 2.5 | `docs/research/estimator-integrity/certificates.md` | written proofs; numbers cross-checked by T01 | 2 weeks |
| T03 Lean instantiation | implementation | gpt-5.6-sol / xhigh | claude-opus-5 | C2, C3 constants | `formal/EstimatorIntegrity/AllenCahnCertificate.lean` | `lake build` sorry-free; `rg sorry` empty | 1 week |
| T04 derivative-code ansatz C5 | research | gpt-6-astra / max | claude-opus-5 | T01 on tan/cosine/log tables | `certificates.md` §C5 | proof or documented failure with truncated numerics | 2 weeks |

Escalation: if T01's iterates at rate 1 diverge, or if T02 finds
\(\Phi_2(W)\le W\) impossible for every exponential ansatz, return to the
research role before any further implementation. Prohibited: weakening
(H1)–(H7), trimming samples, or changing the PDE constants to make a
certificate close.
