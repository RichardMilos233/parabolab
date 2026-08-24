# parabolab — agent notes

## Workspace
- Sessions for THIS project open this repo directly as the workspace
  root. The repo lives inside the umbrella `fyp/` folder (one level up),
  which keeps the papers and hosts the sibling projects.
- Source papers (NOT in the repo, kept in `../`): `../JEQ2023.pdf`
  (coding trees / fully nonlinear Feynman–Kac) and `../JCP2024.pdf`
  (deep branching solver). DOI links are in README.md.
- Sibling project: `../wavelab` = the EARLIER wave-equation project
  (branching MC for `u_tt − c²Δu = f(u)`, FD ill-posedness study) with
  its own repo and CLAUDE.md; its paper is `../m.pdf`. Not needed here.
- Cross-check material: sibling clones `../coding_trees`,
  `../deep_branching`, `../deep_branching_with_domain` (the authors'
  repos). Tests and example scripts locate them RELATIVE to the repo
  parent and skip/degrade gracefully if absent — on a new machine,
  clone them next to `parabolab/` to enable the golden tests and
  CSV overlays.

## Project state
- **M1 complete**: semilinear coding-tree Monte Carlo (JEQ2023 §2 mechanism,
  JCP2024 Alg. 1 sampler), d = 1, pure Python/numpy. Allen–Cahn validated
  against the closed forms (5.3)/(5.4) at 1e5–1e6 samples, T ≤ 0.5, and
  cross-checked against
  `../coding_trees/logs/final/allen_cahn_jeeq_dim_1_blow_up_analysis.csv`.
- **M2 complete**: general fully nonlinear mechanism (JEQ eqs. (2.4)–(2.5))
  in d = 1, arbitrary order n. `fdb.py` (our Faà-di-Bruno enumeration,
  golden-tested against `../deep_branching/fdb.py`),
  `FullyNonlinearMechanism1D` (per-PDE memoized, exact zero-tuple
  reduction), `FullyNonlinearPDE1D` (sympy f/phi, lazy lambdified
  derivative caches). Four JEQ §5 examples in library.py reproduce
  Figs 6–9 at paper budgets (examples/jeq_fig6..9_*.py). 64 tests green
  (`pytest -m 'slow or not slow'`, ~35 s).
- **M3 complete**: multidimensional extension (JCP2024 §2).
  `FullyNonlinearPDEnD` (deriv_map jets, diffusion σ² = authors' `nu`,
  polynomial-support zero detection), `DxN(mu)` codes,
  `FullyNonlinearMechanismND` with reduced-set table construction (the
  Faà-di-Bruno recursion itself is pruned by a monotone possibly-nonzero
  predicate — this, not raw enumeration, is what makes d = 100 tractable),
  d-dim BM in tree.py (scalar d = 1 path byte-identical),
  `parallel.estimate_parallel` (multiprocessing over sample batches,
  n_jobs-independent results). Reproduced: Fig 1 (Allen–Cahn d = 5/100),
  Figs 4/5 (exp gradient d = 5/10), Table 2 (AC d = 100, T = 0.3),
  Table 5 (HJB d = 100, T = 1, exact 4.590162 by Cole–Hopf quadrature).
- **M4 complete**: deep branching solver (JCP2024 §3 Algorithm 2 +
  Remark 3.1) in `parabolab/deep/` (torch; NOT imported by the top-level
  package — `import parabolab.deep` explicitly). `generator.py` draws N
  training states (τ≡0, X uniform on the 10%-overtrained segment
  [x_lo,x_hi]×{x_mid}^{d−1}, Remark 3.1 vi) and M tree samples per state
  through the M3 sampler over worker processes, with the authors'
  outlier filter; supports non-Id root codes (∂^α families). `net.py` =
  the paper's residual net (first plain + 5 residual hidden layers of
  20, tanh, batchnorm after activation). `solver.py` = full-batch Adam,
  lr 0.01 ÷10 every ⌊P/3⌋, P = 3000; grid_errors implements the paper's
  101-point L1/L2 protocol; consistency_plot = JCP Fig 7. Reproduced (on
  CPU, minutes instead of the paper's GPU-hours): Table 1/Fig 1 (AC
  d = 1, 5), Table 3 (exp d = 1), Table 5 + Fig 7 (Merton HJB (4.6),
  new library entry `merton_hjb`, non-polynomial f) — including the
  paper's own tanh training anomaly (our run 9 ≙ their third run).
- **M5 complete**: vendored baselines + blow-up study.
  `parabolab/vendor/` = authors' `bsde.py` (deep BSDE / 2BSDE) and
  `galerkin.py` (DGM) verbatim from deep_branching @ c06bef2 (MIT,
  provenance headers) + our `adapters.py` (~150 lines: deriv_map row →
  BSDE input-slot mapping, DGM Laplacian-row extension, sympy→torch
  lambdify; raises `BaselineInapplicable` for rows outside
  {0, e_k, 2e_k} or σ² ≠ 1). `examples/jcp_comparison_baselines.py`
  rebuilds JCP Tables 1/3/5 three-way (reduced budgets default,
  --full for paper budgets), reproducing the paper's negative results
  (BSDE fails on Merton, DGM inapplicable). `parabolab/blowup.py` =
  `sweep_T` + `integrability_edge`; `examples/blowup_allen_cahn.py`
  sweeps T = 0.1..2.0 for AC d = 1/10 at both ρ rates with the authors'
  blow_up_analysis CSVs overlaid (figures in examples/).
- **M6 complete**: uniform solver interface `parabolab/solve.py` --
  `CodingTreeMC`, `DeepBranching`, `DeepBSDE`, `DeepGalerkin`, each
  `Solver(**budget).solve(pde, grid, t=0.0) -> Curve`, plus
  `compare(pde, *curves)` -> `.table()` / `.plot()` / `.errors()`. Thin
  facade over profiles.py / deep/ / vendor/ -- no new numerics. Exported
  from the top level; `demo/` (two ~25-line scripts, Allen-Cahn and
  Merton) is its showcase. 29 tests in `tests/test_solve.py`.
  The seven PROFILE examples were migrated onto it (jeq_fig1/4/6/7/8/9 +
  jeq_allen_cahn_1d), verified numerically identical row-for-row except
  jeq_allen_cahn_1d, whose hand-rolled seed scheme
  (`seed + 1000*i + int(100t)`) was replaced by the library's `seed + i`
  per curve -- a different draw of the same distribution, flagged in the
  script. The other SEVEN examples were deliberately NOT migrated: their
  deliverable is not a curve. `jeq_table2/table5_d100` report mean/SD of
  a single point over runs AND share one ProcessPoolExecutor across them
  (migrating would rebuild the d=100 mechanism table per call, gotcha 22);
  `jcp_table1/3/5_deep` report multi-run L1/L2 plus consistency plots
  (`DeepBranching` is n_runs=1 by design); `jcp_comparison_baselines` is a
  three-way report with paper columns and `--full`; `blowup_allen_cahn`
  sweeps T; `rate_study_dym` sweeps the rho rate. Do not "finish the job"
  by forcing these onto `.solve(pde, grid)`.
  `profiles.plot_profile` lost its last caller in the migration and is now
  dead code (untested, unexported) -- left in place pending a decision.
- Env: `conda activate parabolab` (python 3.11). Editable install of this
  repo. Torch CPU build installed (M4); all deep code is device-agnostic —
  pass device="cuda" on a GPU machine.

## Conventions
- Terminal-value problem u_t + (1/2)u_xx + f(u) = 0, u(T,·) = φ. The 1/2
  Laplacian factor means the driving process is a STANDARD Brownian motion.
- Codes are frozen dataclasses in `mechanism.py`: `Id()`, `Dx(order)`,
  `FDeriv(a, k)` = (a·f^{(k)})*. Real constants (e.g. the −1/2 in M(g*))
  are absorbed into `FDeriv.a`, never into sampling weights.
- The mechanism object exposes `tuples(code)`, `terminal(code, pde, x)`,
  `is_identically_zero(code, pde)`. tree.py depends only on this protocol.
  `SemilinearMechanism` is a static class; `FullyNonlinearMechanism1D` is an
  instance bound to one `FullyNonlinearPDE1D` (reachable as `pde.mechanism`,
  memoized). `estimate`/`sample_tree` with `mechanism=None` resolve to
  `pde.mechanism` if present, else the semilinear mechanism.
- General codes: `FNu(a, nu)` = (a·∂^ν f)*, ν a multi-index over (z0..zn).
  `FDeriv(a, k)` ≅ `FNu(a, (k,))` (n = 0); the semilinear path is kept
  untouched for M1 compatibility.
- `ParabolicPDE.f_derivatives` is either a list [f′, f″, …] (entries past the
  end are declared ≡ 0 — the polynomial convention used for pruning) or a
  callable k ↦ f^{(k)} for non-polynomial f (e.g. exp; pruning then off).
- `solve.py` contracts: (a) `.solve()` takes a PDE **or** a zero-argument
  factory; solvers that use worker processes (`CodingTreeMC(n_jobs>1)`,
  `DeepBranching`) require the factory and raise `TypeError` naming the fix
  when given an instance -- PDE objects hold lambdified sympy callables and
  local closures and are genuinely unpicklable (verified). (b) The grid
  convention is `s -> (s, x_mid, ..., x_mid)` via the single `_point_map`,
  matching `deep/solver.py::_grid_inputs`, NOT
  `profiles.last_coordinate_embedding`'s `(0, ..., 0, s)` -- see gotcha 33.
  (c) torch is imported inside the three network `.solve()` bodies only, so
  `import parabolab` stays torch-free (subprocess-tested).
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

## Gotchas discovered (M2)
10. **JEQ2023 (5.10) terminal condition is wrong in the paper AND in the
    authors' notebook**: b = −36/47, c = 24b, d = 4b² do not satisfy the
    traveling-wave consistency φ − (φ″/12)² + cos(πφ⁗/24) = 0 (sympy
    residual −143ξ²/188 − 858ξ/47 + 2939/2209). Unique correct values for a
    monic quartic with unit cubic term: b = 3/8, c = 1/16, e = 257/256
    (`library.cosine_fourth_order_1d`). Their Fig 8 still "looks right"
    because the y-scale is O(1000) and the error is O(1) relative O(10²)…
    at T = 0.04 the wrong-exact curve differs by ≲1% of the plotted range.
11. **JEQ2023 (5.11) α mismatch**: paper text says α = 5, the notebook uses
    α = 10. We follow the paper (Fig 9 reproduces fine with α = 5).
12. **The paper's displayed mechanism tables list duplicate tuples instead
    of coefficients**: e.g. M(∂ₓ²) at n = 1 shows ((∂z0∂z1 f)*, ∂ₓ, ∂ₓ²)
    twice; we carry one tuple with the Faà-di-Bruno integer constant (2)
    inside FNu.a — same expectation, |M(c)| differs (only affects variance).
13. **Zero-tuple reduction is a big deal for sparse f**: cosine example
    (n = 4) has |M(f*)| = 306 raw → 23 after dropping tuples containing an
    identically-zero (∂^ν f)* code (exact, mean-preserving — same induction
    as gotcha 6). Without it, weights |M(c)|/ρ(τ) would be ~13x larger.
    If reduction empties a table we keep one zero tuple (sampler returns 0).
14. **Dym (Fig 6) has divergent higher moments at every rate**: φ = (6x)^{2/3}
    ⇒ |φ^{(k)}| ~ Γ(k − 2/3)·x^{2/3−k} grows factorially, beating the
    (λT)^depth branching probability for ANY λ; deep ∂ₓ-chains produce
    monster samples (−54 ± 56 at 1e6 samples where exact = 4.05). More
    samples make the profile WORSE, not better; higher rate is catastrophic
    (rate 5: estimates in the thousands), lower rate just hides the
    nonlinear correction. Strictly, φ violates the growth assumptions of
    JEQ Prop 4.2 — the representation is numerically usable only in the
    pre-asymptotic "lucky seed" regime. Central to the FYP short-time story.
15. **Heavy tails masquerade as bias at small N** (cosine/log examples):
    below ~1e5 samples the rare large-weight branches are missed, so both
    the mean AND the stderr are too small — z-scores of 3.5–6.5 that shrink
    with N (cosine at 4e5: all |z| < 2). Never judge these examples at 2e4.
16. **sympy Subs pitfall in tests**: comparing our (∂^ν f)*-at-jet Subs
    expressions against sympy's own chain-rule output fails for n ≥ 1
    (different Subs normal forms; diff of a Subs-built jet can even raise).
    The identity tests instead use f = exp(Σ a_q z_q) with symbolic a_q —
    ∂^ν f = (Π a_q^{ν_q}) f separates every ν as a distinct monomial.

## Gotchas discovered (M3)
17. **Full-Laplacian problems ((5.1), (5.9)) via σ²**: the authors' `nu`.
    ∂ₜu + (σ²/2)Δu + f = 0 with BM variance σ²·dt and the third mechanism
    union carrying −σ²/2 (only place σ² enters the tables). Validated by a
    σ² = 2 heat control and by HJB against the Cole–Hopf exact value.
18. **d = 100 is tractable only through reduced-set construction**: the
    raw M(g*) has m²d + Σ|fdb(α_p)| elements (HJB: ~1.01e6); we prune the
    FdB recursion itself with the monotone `possibly_nonzero` predicate
    (polynomial support test) and build the reduced table directly
    (HJB |M(f*)| = 20 000 in ~1 s). The authors sample the RAW set — for
    HJB ~98% of their branch draws are identically-zero samples with the
    full 1.01e6 weight multiplier.
19. **The optimal ρ rate flips at large d** (vs gotcha 5): each branching
    multiplies H by |M(c)| e^{λτ}/λ; with |M| = 2e4 (HJB) frequent
    branching at rate 1 compounds to exploding variance AND 184 min/1e5
    samples. The authors' jcp_rate(T) = −log(0.95)/T keeps branchings rare
    (mean nodes 1.05, 11 s/1e5, sane variance). Rate 1 stays better for
    small-|M| problems (d = 1, Fig-1/4 profiles).
20. **Table 5 heavy-tail anatomy**: at 1e5 samples, HJB runs bifurcate —
    tail-missing runs cluster at ≈4.580 with stderr ≈0.0037 (the paper's
    published 4.580340 ± 0.001869 is exactly this cluster, 5 of its own
    SDs below the exact 4.590162), tail-catching runs have stderr 0.01–0.02
    and centre on the exact value. Our 5-run mean 4.590153. Same mechanism
    as gotcha 15, now with a quantitative fingerprint.
21. **sympy pathology: first diff of tanh(wide Add) takes minutes**
    (~173 s for tanh of a 100-term sum; subsequent diffs are cached).
    The logistic/exp form −1 + 1/(1 + e^{−2y}) differentiates in ms —
    `library.allen_cahn_nd` writes φ that way (identical function).
22. **Worker processes must reuse PDE instances**: a FullyNonlinearPDEnD
    is cheap to build but its lazy caches (mechanism tables, lambdified
    ∂^μφ) are not; rebuilding per chunk made d = 100 profiles ~30x slower.
    parallel.py keeps a per-process `_PDE_CACHE` and profiles.py shares
    one ProcessPoolExecutor across grid points.
23. **Constant-derivative codes cannot be pruned** (exp example (5.5):
    ∂z_i f = α/d for the gradient arguments): their reduced tables are the
    guaranteed-zero fallback tuple, so such particles return 0 whenever
    they branch and the constant only at leaves — unbiased (the source
    term of a constant really is 0) but variance-adding. Together with
    exact u ≈ 0 near the dip of (5.6), this is why Fig-4 error bars blow
    up around x ≈ −0.44 (the paper plots no error bars there; the
    authors' own d = 10 value at that point is 0.157 vs exact 0.003).

## Gotchas discovered (M4)
24. **The paper's eq. (3.6) vs branch.py**: the paper writes the loss over
    individual tree samples H_{i,j}; the authors' code regresses on the
    per-state (outlier-filtered) MEAN over the M samples. Same argmin
    (the losses differ by a v-independent variance term); we follow the
    code (cheaper: N targets instead of N·M). The outlier filter is
    percentile-based: keep [lo − 1000(hi−lo), hi + 1000(hi−lo)] with
    (lo, hi) the (1, 99) percentiles of the M values, plus drop NaNs.
25. **Deliberate deviations from branch.py** (all validated harmless):
    (a) no antithetic Brownian variates (we forego a ~2x variance saving);
    (b) our tree samples come from the M3 reduced-mechanism sympy sampler,
    not their torch autograd sampler over the RAW mechanism — same
    distribution (tested), orders of magnitude faster: Merton full budget
    N=1000, M=10,000 costs us ~13 s datagen on 6 CPU cores vs their 54
    GPU-minutes; (c) time patching (`branch_patches`) NOT implemented —
    it is in their code (default 1, unused in all JCP §4 experiments,
    central only in the successor deep_branching_with_domain repo);
    doing it properly needs net-as-terminal-condition inside the sampler
    (autograd ∂^μ of the net at leaves) — scoped out to M5+.
    (d) the authors train u only (root code Id); we also train u only,
    but generate_training_data(code=DxN(mu)) gives ∂^μu families for
    free (tested against the exact Allen–Cahn du/dx).
26. **Merton HJB (4.6) fits the sympy pipeline despite non-polynomial f**
    (z1²/z2 and z1^{1−1/γ} terms; possibly_nonzero falls back to safe
    degree analysis). Its exact solution needs the numerator and α^γ
    combined BEFORE the γ-power — with the paper's parameters
    α = −0.07 < 0 and both factors are negative separately (complex
    powers if evaluated naively).
27. **The paper's tanh anomaly is real and reproducible**: at full budget
    (M=10,000, 10 runs) our run 9 trains to L1 6.8e-2 (9 other runs:
    5e-3–1.8e-2, median ≈ 1e-2 ≙ paper's 8.49e-3) with the net visibly
    detaching from the MC scatter for x ≳ 180 — exactly the paper's Fig 7
    (their anomaly was on the third run). The Fig-7 consistency check
    (MC targets ARE unbiased pointwise estimates of u) catches it; that
    diagnostic is unavailable to deep BSDE/Galerkin. Batchnorm running
    stats + full-batch training make the anomaly a pure optimization
    pathology, not a data problem.

## Gotchas discovered (M5)
28. **The deep BSDE f-input layout is FIXED**, independent of the
    deriv_map you pass it: index 0 = u, 1..d = ∇u, d+1..2d = diag Hess
    (second_order=True only); its `deriv_map` argument is used for
    SHAPES only. And the driving BM is standard, so σ² = 2 problems
    ((5.1), (5.9)) don't fit. The DGM residual is ∂ₜu + f with f
    entirely caller-supplied — it must INCLUDE the (σ²/2)Δu term
    (the authors' demo passes `.5*y[second_rows].sum()` explicitly).
29. **The Merton baselines only run on regularized expressions**: the
    authors' notebook (cell 21, comment "TODO: how to deal with negative
    x and y[1] properly???") puts |·| around the fractional power's base
    and inside φ; without it the BSDE z-net's negative outputs give NaN
    at once. Also 2BSDE needs the y_lo=0, y_hi=100 clipping. We pass
    these as expression OVERRIDES to the adapter — library.merton_hjb
    itself stays the honest PDE.
30. **Paper-vs-notebook config mismatch (BSDE)**: JCP §4 says the time
    grid is (0, T/5, ..., T) = 5 intervals; comparison.ipynb runs the
    tables with `bsde_nb_time_intervals=4`. We follow the notebook.
31. **The blow-up has two distinct faces depending on the ρ rate**
    (examples/blowup_allen_cahn.py, AC d=1/10, 3 seeds × 1e5): at
    jcp_rate the sample SD grows SMOOTHLY (stderr > 5%·|u| past
    T ≈ 0.8/0.9) and the authors' single-seed "systematic drift" curve
    lies inside our 3-seed spread — it is one draw from a huge sampling
    distribution, not a bias law; at rate = 1 the estimator is sharper
    until T ≈ 1.0/1.1 and then explodes outright (max|H| ~ 7.6e9,
    estimates ±10³–10⁴ at T = 2). `integrability_edge` therefore checks
    BOTH persistent drift AND relative precision loss — the drift test
    alone never fires (the error bars balloon along with the error).
32. **conda run captures output**: `conda run ... > log` writes the log
    only at process exit (use --no-capture-output to stream). Long
    comparison runs look "empty" until they finish.

## Gotchas discovered (M6)
33. **Two incompatible profile-grid conventions coexist in the package**:
    `profiles.last_coordinate_embedding(d)` maps a scalar grid point to
    `(0, ..., 0, s)` (the authors' notebook plots), while
    `deep/solver.py::_grid_inputs` maps it to `(s, x_mid, ..., x_mid)`
    (the paper's evaluation grid, `x_mid` = grid midpoint). Identical at
    d = 1, silently different for d >= 2 -- an MC profile and a network
    curve plotted together would be sampling different states. `solve.py`
    pins the `_grid_inputs` convention for everything and
    `tests/test_solve.py` asserts the two agree elementwise.
34. **`estimate_profile` needs an explicit `embed` for every
    `FullyNonlinearPDEnD`, including d = 1**: its phi is lambdified over a
    d-vector, so passing a float raises a bare
    `TypeError: _lambdifygenerated() argument after * must be an iterable`
    from inside sympy with no hint about the cause. `solve.py` picks the
    embedding by `isinstance(pde, FullyNonlinearPDEnD)`.
35. **JCP2024 Sec. 4 (d)'s "DGM is inapplicable to Merton" is an editorial
    judgement, not something the code detects.** `vendor/adapters.py`
    raises `BaselineInapplicable` only for deriv_map rows outside
    {0, e_k, 2e_k} or sigma^2 != 1; `dgm_functions(merton_hjb())` builds
    fine and `DeepGalerkin.solve` runs there. The skip lives in the
    `dgm_inapplicable` entry of `examples/jcp_comparison_baselines.py`'s
    CASES dict. Do not describe it as automatic detection.

## Paper pointers (M2 done, for M3)
- General mechanism: JEQ2023 Def. 2.2, eqs. (2.4)–(2.5); multivariate Faà di
  Bruno constants k_q^j, l_j (Prop. 1.1) — implemented in `fdb.py` as
  multisets of blocks (l, q, mult), coeff = k!/Π(mult!·(l!)^mult).
- |M(g*)| = 1 + Σ_{k=1..n} |fdb(n+1, k)| + (n+1)² (confirmed against the
  Mathematica appendix variable `l1`).
- Integrability / short-time: JEQ2023 Prop. 4.2 (sufficient, very
  conservative: needs K < 1 bounds and ρ(T) ≥ 1/min q_c — unattainable for
  the semilinear mechanism at T = 0.5 with any Exp rate, yet MC is fine).
- M3 (multidimensional) needs: d-dim codes ∂^μ with μ ∈ N^d (fdb.py's block
  sizes l become multi-indices — the authors' fdb_nd already supports this
  via `ks`), d-dim Brownian moves, and the JCP2024 p.4 d-dim mechanism.
  Runtime is NOT the bottleneck for the JEQ figures (tiny trees at T ≤ 0.04:
  1e5 samples/point ≈ 0.15 s) — numba matters for T ~ 0.5 (Allen-Cahn-type,
  mean nodes > 1.5) and for d ≥ 2 sample counts.
