# parabolab — agent notes

## Project state
- **M1 complete**: semilinear coding-tree Monte Carlo (JEQ2023 §2 mechanism,
  JCP2024 Alg. 1 sampler), d = 1, pure Python/numpy. 25 tests green
  (`pytest -m 'slow or not slow'`, ~10 s). Allen–Cahn validated against the
  closed forms (5.3)/(5.4) at 1e5–1e6 samples, T ≤ 0.5, and cross-checked
  against `../coding_trees/logs/final/allen_cahn_jeeq_dim_1_blow_up_analysis.csv`.
- M2 (general Faà-di-Bruno mechanism), M3 (numba/vectorized backend),
  M4 (torch deep branching, JCP Alg. 2), M5 (vendored baselines): not started.
- Env: `conda activate parabolab` (python 3.11). Editable install of this repo.
  Torch intentionally NOT installed until M4.

## Conventions
- Terminal-value problem u_t + (1/2)u_xx + f(u) = 0, u(T,·) = φ. The 1/2
  Laplacian factor means the driving process is a STANDARD Brownian motion.
- Codes are frozen dataclasses in `mechanism.py`: `Id()`, `Dx(order)`,
  `FDeriv(a, k)` = (a·f^{(k)})*. Real constants (e.g. the −1/2 in M(g*))
  are absorbed into `FDeriv.a`, never into sampling weights.
- The mechanism object exposes `tuples(code)`, `terminal(code, pde, x)`,
  `is_identically_zero(code, pde)`. tree.py depends only on this protocol —
  the M2 fully nonlinear mechanism should implement the same three methods.
- `ParabolicPDE.f_derivatives` is either a list [f′, f″, …] (entries past the
  end are declared ≡ 0 — the polynomial convention used for pruning) or a
  callable k ↦ f^{(k)} for non-polynomial f (e.g. exp; pruning then off).
- rng: pass `seed=` or a `np.random.Generator`. Tests rely on the exact draw
  order inside `_tree`: exponential → (leaf) normal | (branch) integers-if-
  |M|>1 → normal → children in tuple order. Changing the order breaks
  `tests/test_tree.py::test_hand_computed_tree_weight` (update it together).

## Gotchas discovered (M1)
1. **JCP2024 Algorithm 1 typesetting is misleading**: it reads as if a fresh
   Brownian increment W is drawn per child inside the for-loop. WRONG for the
   math: all children must start from the SAME branch position (parent's
   death position). JEQ2023 §3 says so explicitly, the fixed point (4.1) has
   ∏_z u_z(s,y) under ONE space integral, and the authors' code
   (`deep_branching_with_domain/branch/branch.py`, `gen_sample_batch`) draws
   `next_x` once before recursing into all children.
2. **numpy Exp parametrization**: ρ = Exp(rate) ⇒
   `rng.exponential(scale=1/rate)`. Passing the rate as scale silently gives
   Exp(1/rate) and biases everything.
3. **Leaf survival factor uses the leaf's BIRTH time**: weight
   c(u)(T, X_T)/F̄(T − t_birth), where t_birth is the parent's death time
   (JEQ2023 Def. 4.1: F̄(T − T_{k̄−})). The Brownian stretch at a leaf runs
   only to the horizon: W ~ N(0, T − t_birth), NOT N(0, τ).
4. **Interior weight** is 1/(q_c(I_c)·ρ(τ)) with q uniform ⇒ |M(c)|/ρ(τ),
   using the particle's own lifetime τ.
5. **Rate choice matters more than the papers suggest.** JCP2024's
   ρ rate = −log(0.95)/T gives mean tree size ~1.05 but rare branch events
   carry weight ~2e^{λτ}/λ ≈ 20+ ⇒ heavy tails: at T = 0.5 (Allen–Cahn) the
   empirical mean is systematically off (≈ −0.687 vs exact −0.679 at 1e5;
   the authors' own 1e6-sample log shows −0.6851) and stderr underestimates
   the error. rate = 1 (JEQ Mathematica default) is unbiased-in-practice with
   ~4x smaller stderr at the same N. Package default: rate = 1.
6. **Exact zero-code pruning**: for polynomial f, a code (a·f^{(k)})* with
   f^{(k)} ≡ 0 spawns a subtree whose H ≡ 0 a.s. (every tuple in M(g*)
   contains a descendant of g). `prune_zero=True` returns 0 immediately and
   consumes no rng draws. Verified mean-preserving in tests.
7. `coding_trees/main.ipynb` does NOT contain the sampler — it pip-installs
   `branch` from `deep_branching_with_domain` and calls `Net.gen_sample`.
   Their code representation: numpy int arrays (negative = ∂^{|code|−1} on u,
   positive = derivative multi-index on f, shifted by ±1), uniform tuple
   choice via `len(L)` multiplier. Ours uses explicit dataclasses instead.
8. Their d=1 blow-up CSV (branch column) deviates from exact increasingly
   with T even below T = 1 — consistent with the heavy-tail effect of their
   λ ≈ 0.1 (gotcha 5), NOT necessarily with PDE/representation breakdown.
9. **Workspace shadowing**: `import parabolab` from the fyp/ workspace root
   picks up the repo FOLDER (namespace package) instead of the installed
   package. Run python/pytest from inside `parabolab/` (the repo root).

## Paper pointers (for M2)
- General mechanism: JEQ2023 Def. 2.2, eqs. (2.4)–(2.5); multivariate Faà di
  Bruno constants k_q^j, l_j (Prop. 1.1). JCP2024 p. 4 has the d-dim version
  with multi-indices; their `deep_branching/fdb.py` implements it.
- Integrability / short-time: JEQ2023 Prop. 4.2 (sufficient, very
  conservative: needs K < 1 bounds and ρ(T) ≥ 1/min q_c — unattainable for
  the semilinear mechanism at T = 0.5 with any Exp rate, yet MC is fine).
- First-order example mechanism (n = 1): JEQ2023 §2 second example — good
  first target for M2 tests (7 tuples for M(g*), 2 for M(∂x)).
