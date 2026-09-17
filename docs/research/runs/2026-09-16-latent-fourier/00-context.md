# Context and scope

Date: 2026-09-16. User requested Chinese literature research, feasibility assessment and a written formulation of one specified idea: latent eigendecomposition versus Fourier structure in PDE encoder–decoder models. This is a focused feasibility study, not a request for ten unrelated ideas, full model training, or Lean formalization.

The user clarified that the relevant NN code was on the newest remote main and authorized preserving existing uncommitted work on a new branch before obtaining main.

- Original checkout: `/Users/michael/Desktop/NTU/fyp/parabolab`, initially main at `ff2fa5f4858c695dd125c3b1ca7cfe63372398e7`.
- Original dirty files remain there, uncommitted, on `codex/preserve-tuple-policy-2026-09-16`. SHA-256 checks of all 49 original modified/untracked files matched after the Git operations. No stash, reset or WIP commit was used.
- Fetched origin/main and fast-forwarded local main to `9b02157` (58 commits ahead of the original checkout).
- Independent permanent worktree: `/Users/michael/Desktop/NTU/fyp/parabolab-latent-fourier`, branch `codex/latent-fourier-research`, based on latest main.

Relevant sources: `parabolab/deep/opnet.py`, `setnet.py`, `optrain.py`, `families.py`, `corpus.py`; `examples/phi_operator.py`; `docs/research/nn-fitting/README.md`; D03 operator design/results document.

Objects: terminal condition phi -> fixed-time solution u(0,x); attention token memory, DeepONet branch coefficients, FNO hidden fields. No shared compact latent definition applies to all models. The current training family is a peak-normalized four-mode Fourier series. Existing results are historical project records, not rerun measurements.

Key unknowns: trained checkpoints not obtained; source driver saves CSV but not checkpoints; no learned latent/Fourier correspondence measured. Existing model is fixed-time, not a learned temporal latent propagator. Full nonlinear rollout evidence remains proposed.

Skills consulted: math-auto-research 0.2.0 (focused feasibility scope), its default profile and model-routing/presentation guidance; Canvas selection guidance was read, but a written research document is the specific deliverable, so no separate Canvas app was produced. No production solver or training code changed.
