# Neural-network fitting research line

**Status, 16 September 2026.** A second research line, parallel to the
branching-estimator work in [the research guide](../README.md): what
network should sit on top of the coding-tree sampler, and what should it be
asked to map. It lives entirely in `parabolab/deep/` (plus the
backwards-compatible `allen_cahn_nd(shift=)` parameter in `library.py`);
it does not change the sampler, mechanisms, rates or proposals. Branches:
`research/nn-architecture` (merged), next `research/nn-backbone-benchmark`.

## What is established

| Finding | Where |
|---|---|
| The paper's tanh anomaly is an input-scaling artefact; scaled I/O + no BatchNorm + gelu + width 64 give 5× the paper's Merton accuracy with 0/15 anomalous runs (gotcha 38) | [ablation spec §Results](../../superpowers/specs/2026-09-15-nn-architecture-ablation-design.md), `examples/nn_ablation_results.csv` |
| A set-to-field transformer over noisy MC points only ties a per-instance MLP on the Allen–Cahn family (gotcha 45) — stopped | [corpus/denoiser spec §Results](../../superpowers/specs/2026-09-15-general-corpus-set-denoiser-design.md), `examples/set_denoiser_gonogo.csv` |
| One FiLM-conditioned net over Merton parameters θ beats per-instance nets 50/50 (u-L1 4.1e-3 vs 2.0e-2); with inverse-variance-weighted derivative labels its autograd policy is within 0.19 % of the closed form (gotcha 46) | [parametric Merton spec §Results](../../superpowers/specs/2026-09-15-parametric-merton-net-design.md), `examples/parametric_merton.csv` |
| Operator learning φ ↦ u(0,·) from coding-tree labels works; the best backbone depends on the PDE — FNO on linear heat, cross-attention on Allen–Cahn, DeepONet worst on both (gotcha 47) | [φ-operator spec §Results](../../superpowers/specs/2026-09-16-phi-operator-design.md), `examples/phi_operator.csv` |

Every experiment ran against a pre-registered rule written into its spec
before the run; failures (the denoiser, the D02 policy target at first, the
unit-weight derivative labels) are recorded as such.

## Scope and limits

- Tested on 1-D problems at t = 0: Allen–Cahn (semilinear), linear heat,
  Merton HJB (fully nonlinear in u_x, u_xx). Not yet: derivative-code
  families (tan / cosine / log), d > 1, time-dependent queries.
- Labels come from the sampler, so the usable PDE class is the class with a
  finite-variance estimator at the chosen (T, rate) — see the
  estimator-integrity notes; Dym is unusable at any T.
- The per-state stderr of Id-rooted Merton labels at M = 1000 is
  miscalibrated (RMS z ≈ 4.6, gotcha 46); derivative-code labels are
  calibrated but heteroscedastic over three orders of magnitude.

## Code map (`parabolab/deep/`)

| Module | Role |
|---|---|
| `datasets.py` | frozen single-PDE `.npz` datasets (ablation) |
| `corpus.py` | multi-instance corpora: `Family`, `InstanceSpec`, `Instance` (two MC draws, optional derivative labels, `phi_grid`), cache, `collate` |
| `families.py` | NN-only PDE builders: Merton derivatives, Fourier terminal conditions, heat/Allen–Cahn Fourier families, 1-D FD reference |
| `ablation.py` | single-knob ladder over `DeepBranchNet`/`train_deep_branching` knobs |
| `setnet.py`, `settrain.py` | set-to-field denoiser (also the attention operator's core) |
| `condnet.py`, `condtrain.py` | θ-conditioned nets (concat / FiLM), autograd derivatives, Merton policy referee |
| `opnet.py`, `optrain.py` | φ → u operators: DeepONet, FNO-1D, cross-attention |

Drivers: `examples/nn_ablation.py`, `set_denoiser_gonogo.py`,
`parametric_merton.py`, `phi_operator.py` (all with `--tiny` smoke modes
exercised by `tests/test_deep_*.py`). Corpora are regenerated from their
specs into the git-ignored `examples/nn_corpus/`.

## Next

Find a backbone that is good across a broad set of nonlinear PDEs rather
than per PDE: the same three-way comparison (plus the conditioned MLP)
over the sampler's whole supported class, then tune the winner. Design in
progress on `research/nn-backbone-benchmark`.
