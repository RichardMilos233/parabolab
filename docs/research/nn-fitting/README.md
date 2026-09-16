# Neural-network fitting research line

**Status, 17 September 2026.** A second research line, parallel to the
branching-estimator work in [the research guide](../README.md): what
network should sit on top of the coding-tree sampler, and what should it be
asked to map. It lives entirely in `parabolab/deep/` (plus the
backwards-compatible `allen_cahn_nd(shift=)` parameter in `library.py`);
it does not change the sampler, mechanisms, rates or proposals. Branches:
`research/nn-architecture` (merged), `research/nn-backbone-benchmark` (the
six-family backbone benchmark, the last row below).

## What is established

| Finding | Where |
|---|---|
| The paper's tanh anomaly is an input-scaling artefact; scaled I/O + no BatchNorm + gelu + width 64 give 5× the paper's Merton accuracy with 0/15 anomalous runs (gotcha 38) | [ablation spec §Results](../../superpowers/specs/2026-09-15-nn-architecture-ablation-design.md), `examples/nn_ablation_results.csv` |
| A set-to-field transformer over noisy MC points only ties a per-instance MLP on the Allen–Cahn family (gotcha 45) — stopped | [corpus/denoiser spec §Results](../../superpowers/specs/2026-09-15-general-corpus-set-denoiser-design.md), `examples/set_denoiser_gonogo.csv` |
| One FiLM-conditioned net over Merton parameters θ beats per-instance nets 50/50 (u-L1 4.1e-3 vs 2.0e-2); with inverse-variance-weighted derivative labels its autograd policy is within 0.19 % of the closed form (gotcha 46) | [parametric Merton spec §Results](../../superpowers/specs/2026-09-15-parametric-merton-net-design.md), `examples/parametric_merton.csv` |
| Operator learning φ ↦ u(0,·) from coding-tree labels works; the best backbone depends on the PDE — FNO on linear heat, cross-attention on Allen–Cahn, DeepONet worst on both (gotcha 47) | [φ-operator spec §Results](../../superpowers/specs/2026-09-16-phi-operator-design.md), `examples/phi_operator.csv` |
| One backbone across six nonlinear families: **FNO-1D** wins the pre-registered benchmark (S = 0.74, no failure family, worst 1.13×); the coefficient FiLM MLP is second (0.77, fails heat); attention collapses when handed the coefficient vector (memorisation) but is the best and most robust backbone on every family once conditioned on θ only — a post-hoc arm, so the tuning spec starts with a confirmatory gate (gotcha 48). `expgrad_phi` and `log_phi` fail the label-calibration pre-check at M = 1000 | [backbone benchmark](backbone-benchmark.md), `examples/backbone_benchmark.csv`, `examples/backbone_benchmark_precheck.json` |

Every experiment ran against a pre-registered rule written into its spec
before the run; failures (the denoiser, the D02 policy target at first, the
unit-weight derivative labels) are recorded as such.

## Scope and limits

- Tested on 1-D problems at t = 0: linear heat, Allen–Cahn and Fisher–KPP
  (semilinear), the JEQ tan (2nd-order) and cosine (4th-order) fully
  nonlinear examples with random Fourier φ, and Merton HJB. Not yet: the
  exp-gradient and log families (their labels fail calibration at
  M = 1000), d > 1, time-dependent queries.
- The cosine family is scored at its reference-noise floor (M = 10⁵ grid
  references, mean stderr 1.5e-2 vs L1 2–3e-2): it separates backbones
  only coarsely until the reference is sharpened.
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
| `families.py` | NN-only PDE builders: Merton derivatives, Fourier terminal conditions, heat/Allen–Cahn/KPP/exp-gradient/tan/cosine/log Fourier families, 1-D FD reference (with first-order terms) and MC grid reference with stderr |
| `ablation.py` | single-knob ladder over `DeepBranchNet`/`train_deep_branching` knobs |
| `setnet.py`, `settrain.py` | set-to-field denoiser (also the attention operator's core) |
| `condnet.py`, `condtrain.py` | θ-conditioned nets (concat / FiLM), autograd derivatives, Merton policy referee |
| `opnet.py`, `optrain.py` | φ → u operators: DeepONet, FNO-1D, cross-attention, coefficient FiLM MLP (all `net(phi_grid, cond, q_tx)`); calibration pre-check |
| `benchmark.py` | pre-registered scoring: per-family ratios, geometric-mean score, failure families, robustness winner |

Drivers: `examples/nn_ablation.py`, `set_denoiser_gonogo.py`,
`parametric_merton.py`, `phi_operator.py`, `backbone_benchmark.py` (all with `--tiny` smoke modes
exercised by `tests/test_deep_*.py`). Corpora are regenerated from their
specs into the git-ignored `examples/nn_corpus/`.

## Next

Tuning spec (pending confirmation): the cross-attention operator with
θ-only conditioning, with the FNO-1D — the pre-registered winner — as the
control at every rung and a confirmatory first gate on fresh held-out
seeds; sharpen the cosine reference (M ≈ 10⁶); find a
(T, rate) at which the exp-gradient and log families calibrate. Then d > 1
and time-dependent queries.
