# Branch ownership and review checkpoints

User policy confirmed 2026-10-05; applies to all agents in this repository.

- `research/branching-mc-theory` holds ongoing MC mathematics, code, proofs,
  experiments and reviewed research results. Commit completed, checked work
  there in small scoped commits; organize by substantive results, not time.
- `main` is the user-reviewed baseline. Research validity alone does not
  authorize promotion: explain the result, its assumptions and evidence,
  then integrate only the scope the user has understood and approved.
- Never advance `main` after an ordinary research commit (`branch -f`,
  `update-ref`, reset or automatic merge). Never merge the whole research
  branch merely to promote a small approved result.
- When scope spans a mixed commit, use a dedicated integration branch/worktree
  from `origin/main` and select the approved changes and necessary dependencies.
  Record source commits and preserve frozen evidence bytes and hashes.
- Push `main` after a user-authorized integration and relevant checks. Do not
  force-push. Research pushes require their own authorization.
- Preserve other agents' uncommitted drafts; stage explicit paths only.
  Check the current branch and shared worktree state before each mutation.
- Keep new NN work in `../parabolab-latent-fourier` on
  `research/nn-latent-fourier`; MC integration does not authorize NN changes.
- Prioritize mathematical innovation; use theory -> Lean -> numerical checks.
  Delegate code and numerical verification to `gpt-5.6-sol`.
