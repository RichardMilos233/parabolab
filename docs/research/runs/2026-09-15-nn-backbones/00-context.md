# 2026-09-15-nn-backbones — Context

Mode: `ideate` (plan only). Requested 2026-09-15: "collect and integrate
information, produce a new research plan" for (1) what training data /
inputs / labels we provide and (2) which backbones (transformer, CNN,
RNN, diffusion, encoder–decoder) to try, informed by the latest
neural-PDE literature. Constraint from the user: match architecture
complexity to data volume; we generate our own data, so the two
questions are coupled.

## Main objective and mathematical object

The deep branching solver (JCP2024 Alg. 2) is a supervised regression:
the coding-tree sampler gives, for any state \((t, x)\), an unbiased but
noisy estimate \(y = \frac1M\sum_j H_j\) (with a per-state standard
error) of the solution \(u(t,x)\) of a fully nonlinear parabolic PDE
\(\partial_t u + \tfrac{\sigma^2}{2}\Delta u + f(x, D^{\alpha_1}u, \ldots) = 0\),
\(u(T,\cdot)=\phi\). A network is then fitted to those labels. Unlike a
grid solver, the sampler can also give unbiased labels for any
derivative \(\partial^\mu u\) (root code `DxN(mu)`), at any time
\(t \in [0, T]\), at any point of \(\mathbb R^d\), for any \((f, \phi,
\text{parameters})\) it can build, at a cost of seconds per thousand
states. **The data source is a programmable oracle; the current
formulation uses a tiny slice of what it can produce.**

## What already exists (inspected 2026-09-15)

- Ablation branch `research/nn-architecture` (unmerged, 21 commits):
  frozen-data harness (`deep.datasets`, `deep.ablation`,
  `examples/nn_ablation.py`), network/trainer knobs, and the finding that
  on the paper's pointwise interface preprocessing dominates: kept path
  R0→R1→R2→R3a→R4b→R5a (scaled I/O, no BatchNorm, gelu, 6×64) takes
  Merton median L1 from 8.68e-3 to 1.69e-3 with 0/15 outlier runs. Width
  128, depth 8, sin, Fourier features, weighted loss, L-BFGS all
  rejected. Conclusion the user drew and the tables support: on a
  pointwise \((t,x)\to u\) interface, backbone swaps are parts-swapping.
- Sampler capabilities relevant to new interfaces: `generate_training_data`
  already supports `t_range`, `code=DxN(mu)` labels, per-state `stderr`
  and `n_kept`; mechanism tables depend on \(f\) only (gotcha 18/22), so
  instances that vary \(\phi\) or scalar parameters reuse them; d-dim
  Brownian moves exist; the segment-only state sampler is the one
  deliberate restriction (Remark 3.1 vi).
- Estimator-integrity results: exact moment recursion, Dym
  non-integrability, safe proposals; the L^p-horizon direction (run
  2026-09-15-post-integrity-directions, D01) is the tool that would
  certify which \((T, \text{rate})\) instances are safe to include in a
  training corpus.
- Hardware: RTX 4060 Laptop 8 GB, 16 GB RAM, 32 logical cores; the env's
  torch is CPU-only (`pip install torch --index-url .../cu124` switches it;
  gotcha 36 still applies).

## Gap and failed approaches

Gap: the 2024–2026 neural-PDE literature (operator transformers,
foundation models, generative solvers, MLMC-trained operators,
Noise2Noise MC denoisers) all assume a *function-valued* or
*set-valued* interface — a terminal condition, a coefficient field, a
set of observations, a time slice. Our formulation exposes none of
these, so none of those backbones can be applied without first changing
what the network is asked to map. Nothing in that literature learns from
branching-Monte-Carlo labels or treats fully nonlinear PDEs with
higher-order derivative nonlinearities.

Failed/limited route: architecture search on the pointwise interface
(the ablation ladder): gains capped at the MC noise floor (exp1) or the
1-D function's simplicity (ac1).

## Resources and scope

- Compute: CPU sampler (≈ 15 s per \(10^7\) trees on 16 workers); GPU
  for models up to ~50 M parameters once the CUDA wheel is installed.
- Reference solutions for evaluation: closed forms for Allen–Cahn (any
  d), exponential-gradient, Merton HJB, HJB d = 100 (Cole–Hopf), Vasicek
  no-consumption Merton; linear heat equation for any \(\phi\) (kernel
  convolution); 1-D finite differences for semilinear \(\phi\)-families.
- Scope: plan only; no code changed in this run. Model actually used for
  ideation: claude-opus-5 (skill routing not selectable in this host).
