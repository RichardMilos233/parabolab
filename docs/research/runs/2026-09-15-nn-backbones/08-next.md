# 2026-09-15-nn-backbones — Checkpoint (updated 2026-09-16)

## Completed work
- Ideation (`01-ideas.md`, `scores.json`) and the staged plan (`02-plan.md`).
- Stage 0 (corpus) — built: `parabolab/deep/corpus.py`, `families.py`.
- Stage 1 / D04 (set-to-field denoiser) — run, FAIL by its rule (tie with
  per-instance nets); stopped. Spec `2026-09-15-general-corpus-set-denoiser-design.md`.
- Stage 3 / D02 (θ-conditioned Merton net) — run, C0–C5; FiLM net kept for
  value, inverse-variance derivative weighting for policy (0.19 %). Spec
  `2026-09-15-parametric-merton-net-design.md`.
- Stage 2 / D03 (φ → u operators) — run on heat and Allen–Cahn; both gates
  pass; best backbone flips with the PDE. Spec `2026-09-16-phi-operator-design.md`.
- Summary of the line: `docs/research/nn-fitting/README.md`.

## Failures and blockers
- D04 tie (recorded). D02 policy target missed at first, met after C4.
- Derivative-code labels are calibrated but heteroscedastic; Id labels at
  M = 1000 are miscalibrated (Merton) — see gotcha 46.

## Next action
Broad backbone benchmark across the sampler's supported nonlinear PDE
class (D10-lite): same comparison on every family, pick the best overall
backbone, then tune it. New branch `research/nn-backbone-benchmark`.
