# Historical designs and implementation plans

**Status reviewed: 16 September 2026.** This directory preserves the design
decisions that preceded the current implementation. It is an archive, not an
execution queue. Start with the [documentation map](../documentation-map.md)
and [current research index](../research/README.md) for active work.

| Record | Present use |
|---|---|
| [Stochastic-rate Merton design](specs/2026-09-07-stochastic-rate-merton-design.md) and [plan](plans/2026-09-07-stochastic-rate-merton-plan.md) | Historical design for implemented state-dependent PDE and Vasicek example support. Existing examples remain usable; further financial application development is inactive. |
| [Estimator-integrity design](specs/2026-09-09-branching-estimator-integrity-design.md) and [plan](plans/2026-09-09-branching-estimator-integrity-plan.md) | Historical design for the moment, Dym, proposal, and finite Lean foundations now recorded in the research notes and code. The old finance narrative, schedule, and model assignments are superseded. |
| [Multifactor Merton proof-record design](specs/2026-09-09-multifactor-merton-proof-record-design.md) | The proof registry and mathematical notes were produced. The proposed multifactor application and its implementation roadmap are inactive. |
| [Exponential-rate design](specs/2026-09-10-exponential-rate-optimization-design.md) and [plan](plans/2026-09-10-exponential-rate-optimization-plan.md) | Historical design for scalar rate theory and finite-depth selection. Later work corrected the binary benchmark and added full-tree certificates; the present proof scope is narrower than some original formalization targets. |

Unchecked boxes record the original proposed steps; they do not indicate a
current missing task, nor does an archived design prove that every proposed
deliverable was completed. Old branch names, worktree paths, dirty-file
snapshots, test counts, model ownership, and execution gates describe their
original sessions. They are not current operating instructions.

Use the [proof registry](../research/proof-registry.md) for claim-by-claim
evidence, the [integration record](../research/results/integration-2026-09-16.md)
for the recorded main-branch validation, and the actual modules for current
interfaces. The active research concerns branching-PDE algorithms, scalar
lambda and tuple probabilities q, and mathematical guarantees. Runtime
comparisons support that work; they do not determine its mathematical value.

The mathematical content and earlier literature assessments remain available
for provenance. A historical candidate or novelty assessment is not a
current priority or an established claim of publication novelty.
