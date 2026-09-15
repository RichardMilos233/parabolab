# 2026-09-15-nn-backbones — Literature and ten directions

## Search record

Date 2026-09-15. Bounded: 8 web queries + 3 abstract fetches; arXiv
only; no citation crawl. Absence from this search is not evidence of
novelty.

Queries: `transformer neural operator PDE 2025 2026 Transolver GNOT
"physics attention"`; `diffusion model PDE solver 2025 2026 DiffusionPDE
generative neural operator`; `high-dimensional PDE neural network solver
2025 2026 HJB curse of dimensionality transformer neural operator
Kolmogorov Monte Carlo labels`; `"in-context operator" OR "foundation
model" PDE 2025 2026 Poseidon PDE-Transformer DPOT`; `neural network
learning from noisy Monte Carlo estimates PDE regression denoising
Feynman-Kac`; `neural operator transformer option pricing stochastic
control HJB 2025 2026 terminal condition`; `deep Kolmogorov Monte Carlo
single sample loss high-dimensional 2025 parametric families`.

### What the field looks like (Sept 2026), grouped by *interface*

| Interface the net maps | Representative work (date) | Backbone | Labels come from | Relevance to us |
|---|---|---|---|---|
| point \((t,x)\) → value | deep Kolmogorov method; error analysis [arXiv:2508.17167](https://arxiv.org/abs/2508.17167) (Aug 2025, Jentzen et al.): convergence in width, depth, #samples for MC-label regression; parametric families [arXiv:2011.04602](https://arxiv.org/pdf/2011.04602) | MLP | single-sample MC over the whole domain | **This is our formulation.** The theory says: sample the whole domain, more points beat bigger nets; matches the ablation. |
| function \(\phi\) or coefficients → solution field | DeepONet, FNO; attention operators GNOT [arXiv:2302.14376](https://arxiv.org/pdf/2302.14376), Transolver / "Transolver is a linear transformer" [arXiv:2511.06294](https://arxiv.org/pdf/2511.06294) (Nov 2025), Physics Transformer [arXiv:2607.24513](https://arxiv.org/html/2607.24513) (Jul 2026), PGOT [arXiv:2512.23192](https://arxiv.org/html/2512.23192v1), geometry-aware operator transformer [arXiv:2505.18781](https://arxiv.org/html/2505.18781v4), million-point generative transformer operators [arXiv:2512.04974](https://arxiv.org/pdf/2512.04974) | transformer (cross-attention context→query, linear/physics attention), FNO, U-Net | grid solvers, low d | The natural home for "try transformers". Requires a \(\phi\)- or parameter-family and a reference solution per instance. Nobody trains these from branching MC. |
| many PDEs → pretrained operator | Poseidon [arXiv:2405.19101](https://arxiv.org/abs/2405.19101) (scOT, time-conditioned LayerNorm, semigroup data trick), DPOT, MORPH [arXiv:2509.21670](https://arxiv.org/pdf/2509.21670) (Sep 2025), probabilistic operator learning for foundation models [arXiv:2509.05186](https://arxiv.org/pdf/2509.05186), ARC-STAR post-hoc correction [arXiv:2605.22222](https://arxiv.org/pdf/2605.22222) (2026) | operator transformers, 20 M–600 M params | fluid-dynamics grid corpora | Recipe transfers; corpus does not. Fully nonlinear parabolic PDEs with derivative nonlinearities are absent from every corpus because no grid solver produces them in high d — our sampler can. |
| sparse observations → field (generative) | DiffusionPDE [arXiv:2406.17763](https://arxiv.org/html/2406.17763v1), particle-guided diffusion [arXiv:2601.23262](https://arxiv.org/html/2601.23262v2) (Jan 2026), PDE-residual spectral attention in diffusion operators [arXiv:2512.01370](https://arxiv.org/pdf/2512.01370), latent flow-matching solver [arXiv:2503.22600](https://arxiv.org/abs/2503.22600), PerFlow UQ [arXiv:2605.03548](https://arxiv.org/pdf/2605.03548), guided diffusion on function spaces [arXiv:2505.17004](https://arxiv.org/pdf/2505.17004) | diffusion / flow matching over fields | grid solvers | Useful when the *solution* is uncertain or partially observed; our solution is deterministic and our uncertainty is label noise — a denoiser, not a generator, is the right tool. |
| noisy MC estimates → clean estimate | Nonlinear Noise2Noise for MC denoisers [arXiv:2512.24794](https://arxiv.org/abs/2512.24794) (Dec 2025): training on noisy targets is MSE-unbiased; nonlinear target transforms bias it | CNN/attention denoisers (graphics) | MC rendering | **Directly our situation** (targets are MC means; R7 showed how stderr must not be used). Nobody has built a denoiser for PDE-solution estimates. |
| multi-fidelity labels → operator | MLMC training of neural operators [arXiv:2505.12940](https://arxiv.org/html/2505.12940v1) (May 2025) | any | hierarchy of solver resolutions | Our fidelity ladder is \(M\); per-state stderr gives the level variances for free. |
| particles → unsupervised solver | MCNP solver [arXiv:2302.05104](https://arxiv.org/abs/2302.05104) (TPAMI 2025) | grid-based stepping nets | Feynman–Kac particles, no labels | Semilinear/linear only; shows the community's interest in probabilistic representations as training signal. |
| finance operators | derivative-informed operator learning [arXiv:2606.05900](https://arxiv.org/pdf/2606.05900) (Jun 2026): Greeks as supervised targets, −15…−76 % sensitivity errors; risk-neutral neural operator [arXiv:2511.06451](https://arxiv.org/pdf/2511.06451); error propagation in DP for control/pricing [arXiv:2509.20239](https://arxiv.org/pdf/2509.20239) | DeepONet, random-feature operators | analytic / MC pricers | Our `DxN` labels are exactly "derivatives as targets"; the Merton/Vasicek family is the finance instance. |
| high-d reviews | [arXiv:2601.13256](https://arxiv.org/abs/2601.13256) (Jan 2026 tutorial), Anant-Net [arXiv:2505.03595](https://arxiv.org/html/2505.03595v3), inf–sup nets [arXiv:2607.11718](https://arxiv.org/html/2607.11718) (Jul 2026) | MLP-family | PINN / variational losses | Context; none uses MC labels for fully nonlinear equations. |

### The organising conclusion

A backbone is a choice of *what the input is*. On a pointwise interface
every architecture reduces to a smooth-function approximator and the
ablation has already found the ceiling. Transformers, encoder–decoders
and CNN/FNO-type models become meaningful only when the input is a
**function** (terminal condition, coefficients), a **set** (scattered
noisy observations) or a **sequence** (time slices). Our sampler can
produce training data for all three interfaces at a cost of seconds per
instance, which no grid solver can for this PDE class. So the plan is
data-first: define the interfaces, generate the corpora, then let each
interface pick its backbone.

## Direction cards

Full fields in [ideas.json](ideas.json); computed ranking in
[scores.json](scores.json).

| ID | Direction | Interface | N × I × E | Value | Feasibility |
|---|---|---|---|---|---|
| D01 | Full-box, time-conditioned pointwise net (deep-Kolmogorov style) | point | 10·10·10 | 1000 | feasible |
| D02 | Parametric-family conditioned net \((t,x,\theta)\to u,\partial u\) (Merton/Vasicek policies) | point + params | 10·10·10 | 1000 | feasible |
| **D03** | Terminal-condition operator \(\phi \to u(t,\cdot)\): DeepONet vs FNO vs attention operator on coding-tree labels | function | 10·10·100 | **10000** | feasible |
| **D04** | Set-to-field MC denoiser: attention over scattered noisy estimates, Noise2Noise across instances | set | 10·10·100 | **10000** | feasible |
| D05 | Time-autoregressive stepper with certified patch length | sequence | 10·10·10 | 1000 | conditional |
| D06 | Diffusion/flow model of the tree-functional law (UQ) | generative | 10·1·1 | 10 | feasible |
| D07 | Derivative-informed (Sobolev) training with `DxN` labels | any | 1·10·10 | 100 | feasible (prior art) |
| D08 | Backbone bake-off on the pointwise interface (KAN, SIREN, …) | point | 1·10·10 | 100 | feasible (control) |
| D09 | MLMC training over the \(M\)-fidelity ladder | any | 10·10·10 | 1000 | feasible |
| D10 | Foundation-style pretraining across \((f,\phi,\theta)\) with an operator transformer | function, many PDEs | 10·100·10 | **10000** | conditional |

Ranking (script, ties by ID): D03, D04, D10, D01, D02, D05, D09, D07, D08,
D06. Shortlist (searched + feasible + value > 1000): **D03, D04**.
Conditional lead: **D10** (depends on D03 working).

## Recommendation

Run D04 first, then D03, with D01/D02 as the data-interface work that
both need and D09 folded into their training loops:

1. **D04 (set-to-field denoiser)** is the boldest change that still has
   a clean first test: exact labels exist for whole families (Allen–Cahn
   with varying \(T\) and wave offset; Merton across \(\gamma\)), so the
   Noise2Noise question ("does a transformer learn transferable structure
   about MC noise?") can be answered on closed-form problems before any
   PDE without a reference is attempted. It reuses the sampler unchanged
   and it is the direction closest to the user's prior transformer
   denoising work.
2. **D03 (φ → u operator)** is the direction the operator-learning
   literature is built for and where DeepONet / FNO / cross-attention can
   be compared honestly on identical data. Its first test (linear heat,
   exact kernel solution) isolates label-noise and \(\phi\)-family design
   from the nonlinear question.
3. **D02** is the finance deliverable and shares D04's instance generator.
4. **D10** only after D03 shows a single family learns from MC labels.

Rejected for now: D06 (models the wrong uncertainty), D07/D08 (prior art
/ control experiments — cheap add-ons to D02/D03 rather than
directions), D05 (needs sampler surgery; sequence backbones wait for it).

What could overturn this: if D04's first test shows the denoiser cannot
beat a per-instance net at equal budget, the set interface has no
transferable structure at these noise levels and the plan collapses to
D03 + D02 only; if D03's linear-heat test fails to reach 1e-3, MC label
noise at affordable \(M\) is too large for operator learning and D09
(MLMC) moves to the front.
