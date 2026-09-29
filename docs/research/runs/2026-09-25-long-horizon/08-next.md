# Completed run and next research actions

This bounded investigation is complete. Ten directions were searched and
evaluated conservatively; none exceeded the strict score threshold. D01 was
executed because the user explicitly requested a longer-horizon study, not
because its score was upgraded. The requested theory → Lean → code sequence
was followed. Conventional proofs, eleven scoped Lean declarations, the
bounded sampler, raw and bounded experiments, independent audits, scientific
figures and the [Chinese report](07-report.md) are delivered.

The result is an exact obstruction for the raw flat tree, a measured shift
in longer-horizon common-rate selection, and an attributed bounded comparator
that works at T=2 on nonconstant data. No universal long-time raw solver or
cheap arbitrary-horizon algorithm has been established. No background run,
publication, commit or pull request is part of this task.

## Recommended next bounded investigation

**First priority for the existing raw algorithm: certify a nonconstant
moment boundary (D10), then evaluate code/time policies inside it (D04/D05).**
The current wave computations are diagnostics: all 12 configurations stopped,
but a large field or exploding descendant does not prove root divergence.

1. Derive a positive subsolution cone on a specified spatial interval whose
   growth propagates to the Id coordinate at the queried point. Pair it with
   a supersolution where feasible. Keep terminal data and boundary handling
   explicit.
2. Prove the comparison and root propagation before implementation; formalize
   the deterministic polynomial inequalities in Lean. If the invariant cone
   fails, retain that failed inequality and report the missing obligation.
3. Only then compute rational lower/upper horizon bounds. First reproduce
   a short-time finite case, then bracket an intermediate horizon using two
   validated spatial/time resolutions. A safety stop is not success.
4. Test a supported code/time policy only where the baseline and candidate
   moments are both validated. Include construction cost and compare whole
   descendant-dependent moments. Frozen child moments cannot certify a
   full-tree policy improvement.

**First priority for practical longer times: certified slab continuation
(D03), using the bounded sampler as a comparison baseline.** Begin with two
slabs and analytic continuation to isolate composition; then replace it by
a deliberately perturbed deterministic continuation with known value and
derivative bounds. Derive propagation of approximation bias, derivative
error and sampling error. Only after those bounds succeed should a numerical
continuation approximation be implemented. Noisy continuation products need
independence or an explicitly justified debiasing construction; plain restart
does not automatically preserve unbiasedness.

Useful acceptance criteria are a nontrivial nonconstant example beyond the
raw common-rate ceiling, a certified total error bound, and lower total work
than complete rate-two trees at matched accuracy. Failure to improve work is
a retained result. Broader novelty claims need a tighter comparison with the
local polynomial/Picard and nesting literature already recorded in D03/D06.

The exact raw absolute-moment obstruction also motivates D07 analytic
regrouping and D08 residual centering. Their convergence justification and
closest prior art remain incomplete, so they should not bypass the research
screening stage. D02's variance-cost optimization likewise remains open:
rate two minimizes expected nodes within the bounded family, not necessarily
variance times cost.

## Resume without recomputing samples

Inspect [05-numerics.md](05-numerics.md), [03-claims.md](03-claims.md), and
[run.json](run.json). The raw verifier and bounded audit can be rerun directly:

```bash
/opt/miniconda3/envs/parabolab/bin/python docs/research/runs/2026-09-25-long-horizon/numerics/raw_experiment.py --verify
/opt/miniconda3/envs/parabolab/bin/python docs/research/runs/2026-09-25-long-horizon/numerics/audit_bounded.py
```

Generation commands overwrite canonical timing metadata; use a new run
folder when changing assumptions, protocols or sources. Preserve the three
pre-existing dirty rate-variance files and their saved initial patch.
