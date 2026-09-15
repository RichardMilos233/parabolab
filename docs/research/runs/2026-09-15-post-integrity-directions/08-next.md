# 2026-09-15-post-integrity-directions — Checkpoint

## Completed work

- Context (`00-context.md`): project state, existing theorems, code, Lean
  coverage, gap, resources. Inspected on disk; the 173-test / Lean build
  results are quoted from `reproducibility.md`, not rerun here.
- Ideation (`01-ideas.md`, `ideas.json`, `scores.json`): bounded web search
  (9 queries, 1 full PDF read: Huang–Privault arXiv:2502.17853v2), ten
  scored direction cards, computed ranking, recommendation.
- Proposed plan for the single eligible direction D01 (`02-plan.md`),
  including task handoffs. Not executed.
- Probe evidence: finite-depth \(L^1/L^2\) iterates for Allen–Cahn d = 1,
  T = 0.5 at rate 1 and 0.1026 (table in `01-ideas.md`).

Stages theory / numerics / lean / correspondence_review / presentation:
not started (ideation-only scope).

## Failures and blockers

- `finite_depth_moment_1d` is tree-recursive; a depth-5 8×8 run was killed
  after 10 min. Grid Picard iteration (T01) is a prerequisite for D01.
- Model routing from the skill config (`gpt-6-astra`, `gpt-5.6-sol`) is not
  selectable in this host; all roles ran on claude-opus-5.
- Jelenković–Olvera-Cravioto 2012 (D03 evidence) cited from memory; must be
  re-read before D03 is executed.
- `coding_trees_v2` notebooks not opened (GitHub page fetch only).

## Next action

Decision for the user: approve D01 for execution (or pick another card).
If approved: task T01 (grid Picard iteration in `parabolab/moments.py`,
acceptance = reproduces the probe table and `pytest tests/test_moments.py`
green), then T02 (certificates C3/C4). Reruns needed before any claim:
`pytest -m 'slow or not slow'` and `lake build` on this machine (never run
here yet).
