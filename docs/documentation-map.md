# Documentation map and status

Reviewed 16 September 2026. The active research concerns **branching Monte
Carlo algorithms and mathematical guarantees**: recursive moments, scalar
rate selection, tuple proposals, integrability and approximation error.
Runtime is supporting evidence. Multifactor Merton is an inactive research
application; its examples and historical mathematical records are retained.

Use the current guides for decisions and interfaces. Read dated reports as
evidence for the specified run, and archived plans as provenance rather
than instructions to resume their old tasks. No literature search or new
mathematical investigation was performed in this documentation cleanup.

## Start here

| Document | Role |
|---|---|
| [Repository README](../README.md) | Installation, solver workflow, current research and historical paper reproductions |
| [Agent/project notes](../CLAUDE.md) | Current scope and conventions, followed by labeled historical implementation notes |
| [Demo guide](../demo/README.md) | Runnable examples and interpretation limits for numerical plots |
| [Research guide](research/README.md) | Main question, achieved guarantees, code mapping and open algorithmic questions |
| [Proof registry](research/proof-registry.md) | Exact mathematical status, hypotheses, code links and Lean coverage |
| [Formal guide](../formal/README.md) | Building the pinned Lean project and understanding its limits |

## Mathematical notes and implementation context

The [theory index](research/estimator-integrity/README.md) distinguishes
current explanatory notes from certificate-bound snapshots.

| Document | Status and interpretation |
|---|---|
| [Moment recursion](research/estimator-integrity/notation-and-moment-theorem.md) | Core tree/moment definitions and analytical assumptions |
| [Exponential-rate theory](research/estimator-integrity/exponential-rate-optimization.md) | Local versus full-tree dependence, convexity and short-time approximation |
| [General rate selection](research/estimator-integrity/general-rate-selection.md) | Conditional general guarantees; finite-depth and full-tree claims kept separate |
| [Adaptive proposals](research/estimator-integrity/adaptive-proposals.md) | Local oracle, support and pilot/freeze theory; not joint global optimality |
| [Dym nonintegrability](research/estimator-integrity/dym-nonintegrability.md) | Negative integrability result for its specified real-extension estimator |
| [Allen–Cahn codewise certificate](research/estimator-integrity/allen-cahn-codewise-certificate.md) | Frozen proof input for saved six-code bounds |
| [Allen–Cahn mean identification](research/estimator-integrity/allen-cahn-mean-identification.md) | Frozen conventional proof connecting the saved moments to PDE variance |
| [Wave residual route](research/estimator-integrity/wave-numerical-certification-route.md) | Frozen proof input; dated pending-merge wording is superseded |
| [Weighted-profile derivation](research/estimator-integrity/profile-rate-efficiency.md) | Frozen derivation; profile objective is optional and costs are supporting |
| [Sampling implementation summary](research/lambda-q-optimization-summary.md) | Practical selectors/proposals plus explicitly historical diagnostic snapshots |
| [Earlier reproducibility ledger](research/estimator-integrity/reproducibility.md) | Historical worktree, environment and test records; not current versions |

## Results, protocols and evidence

Use the [results index](research/results/README.md) for the distinction
between certified numerical bounds, empirical comparisons and frozen data.

| Document | Role |
|---|---|
| [Certified-rate checkpoint](research/results/certified-rate-checkpoint.md) | Main flat/wave mathematical and implementation milestone |
| [Wave certificate report](research/results/wave-rate-certificate.md) | Full-tree pointwise enclosure and global objective-gap result |
| [Binary audit](research/results/binary-benchmark-audit.md) | Corrected correspondence between the standard-binary estimator and its oracle |
| [Profile checkpoint](research/results/profile-efficiency-checkpoint.md) | Optional common-rate grid extension and exact profile bounds |
| [Initial cost study](research/results/rate-cost-results.md) | Supporting six-policy performance evidence |
| [Profile/reuse study](research/results/profile-efficiency-results.md) | Supporting five-policy evidence and conditional fixed-count expected-MSE bounds |
| [Initial cost protocol](research/results/rate-cost-protocol.md) | Frozen predeclared experiment design; not a current research mandate |
| [Profile protocol](research/results/profile-efficiency-protocol.md) | Frozen predeclared experiment design; not an unfinished task list |
| [Integration record](research/results/integration-2026-09-16.md) | Main ancestry, 255-test run, Lean build and three witness rechecks |

The original numerical archives remain under `research/results/`, including
exact fractions, compressed witnesses, raw records, seeds, execution
snapshots, figures and metadata. Earlier example outputs and
`research/sampling-tuning-check.json` remain historical observations.
Their data were not regenerated or relabeled in this cleanup.

## Research options and inactive application records

| Document | Status |
|---|---|
| [Ten directions and original plan](research/future-directions-after-lambda.md) | Updated disposition followed by the original dated literature sweep and schedule |
| [Secondary candidates](research/estimator-integrity/secondary-candidates.md) | Deferred alternatives with individually scoped mathematical status; not a queue of commitments |
| [Multifactor Merton roadmap](research/multifactor-merton-roadmap.md) | Inactive application plan |
| [Multifactor Merton proofs](research/multifactor-merton-proofs.md) | Retained historical mathematical record; no instruction to restart the application |
| [Financial milestone](research/milestone-1-financial-moment-target.md) | Inactive target and historical checks |
| [Financial check output](research/milestone-1-checks.txt) | Preserved output of the historical [check script](research/milestone-1-checks.py), not a new run |

The [historical design/plan index](superpowers/README.md) covers all seven
earlier implementation documents. Their original branch names, unchecked
tasks, model-role instructions and execution gates are historical context.
Their dated status notices identify implemented foundations, superseded
steps and inactive applications. These plans do not override the current
research guide or project instructions.

## Preservation and verification rules

Six Markdown documents are hashed as inputs to saved certificates or
experiments: the four Allen–Cahn/profile proof inputs above and the two
protocols. Their bytes are preserved. Index status and later reports
supersede historical metadata without silently rewriting the evidence.
Source hashes describe a recorded execution; they need not match code
changed after that execution. See the integration record for the
`ff58620` snapshot and later changes.

This review checked document links, referenced interfaces, claim scope,
archive status and frozen-document digests. It did not rerun Monte Carlo
studies, establish new novelty, or extend Lean's formal coverage. The
rate-sensitivity module's explanatory docstrings were corrected; its
executable AST is unchanged after removing docstrings.
