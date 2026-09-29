# Atomic claim ledger

Theory and formalization status after the Lean audit; numerical results are recorded separately as they complete. Existing literature is attributed in the prior survey and T01/T02; these claims are project-specific guarantees and a bounded feasibility demonstration, not a claim to have invented continuation or Galerkin projection.

## C1 — terminal-code finite-product stability

Assumptions: finite common tree, finite common weights, both terminal factors dominated by the same nonnegative B, relative perturbation≤εB. Conclusion: |H−H̃|≤εNW_B≤εW_rB/(r−1), r>1. Conventional proof:04-theory C1/T01. Lean coverage:none in the completed module; finite product and leaf absorption remain conventional-only. Numerical mapping:no separate perturbation experiment claimed; the concrete continuation uses C4–C7. Gap: stochastic lift/PDE identity separate.

## C2 — leaf-marked moment equation

Assumptions: a finite normalized code family, polynomial positive moment recursion, an inflated finite moment in a neighborhood of marking parameter1. Conclusion: equations for M,D,Q with Q=E[N²W²]. Conventional proof:04-theory C2/T01. Lean coverage: none promised for differential/stochastic identity. Numerical mapping: future diagnostic; not mandatory to implement if explicit C4 certificate suffices. This claim is not a measured horizon improvement.

## C3 — finite first-derivative closure for scalar Allen–Cahn

Assumptions: existing one-dimensional SemilinearMechanism, f=u−u³, scalar-independent raw uniform labels/common clock. Conclusion: six normalized observables suffice; G and signed Q in04-theory match actual raw weights, including the selected zero-label probability. Conventional proof:mechanism inspection/chain rule/T01. Lean scope:rational evaluation of the explicitly defined G, not full automatic extraction from Python. Numerical mapping: specialized vectorized sampler must be independently compared with existing sample_tree.

## C4 — uniform local full-tree L² certificate

Assumptions: globally smooth periodic terminal|g|≤2/5,|g′|≤1/2; λ=2,h≤2/25; full trees/raw q=1/2. Conclusion:E[W_(21B/20),c²]≤V_c and especiallyE[H_Id²]≤1/4; E H_Id=S_hg. Conventional proof:positive Volterra box/nonexplosion/monotone limit/bounded six-field uniqueness in04-theory andT01. Lean scope:exact rational postfixed inequality, terminal algebra where encoded. Gaps:probability, parabolic regularity, monotone convergence and mild uniqueness remain conventional. Numerical mapping:unmodified local probability law, no tree caps or discarded outcomes.

## C5 — explicit admissible three-sine interface

Assumptions:period derived fromm=1/20 Jacobi stationary solution; coordinate box(.23,.003,.00005). Conclusion:all interfaces|v|<.4,|v′|<.5; true projected target lies in box and tail L² norm<1e−8. Conventional proof:T02 including DLMF exact identities/series. Lean scope:rational squared-envelope/gamma/budget inequalities; elliptic-function identities and tail series remain conventional. Numerical mapping:finite coefficient vector, analytic polynomial derivatives, first slab exact input only.

## C6 — projected learned-continuation mean-square recurrence

Assumptions:C4,C5; fresh conditional iid roots and uniform spatial states each slab; coordinate projection; odd target and interfaces. Conclusion:R_j≤e^(2γh_j)R_(j−1)+3/(4N_j)+δ². Conventional proof:T02/04-theory. Lean scope:scalar projection contraction and abstract finite recurrence, not measure-theoretic conditional variance or PDE energy identity. Numerical mapping:save raw/projected coefficients, sampling diagnostics and every stage.

## C7 — T=4 ideal-model spatial RMS budget

Assumptions:C4–C6,50 slabs h=.08,N=200000 each,δ²<1e−16,γ≤.075. Conclusion:(E||v₅₀−g||₂²)^1/2<.02. Conventional proof:04-theory/T02. Lean scope:exact finite arithmetic/recurrence portions. Numerical mapping:three predetermined independent repetitions, store actual L² errors and timing; no claim that three repetitions independently certify the population theorem. Floating-point/special-function errors are outside the ideal-model theorem and must be numerically checked separately.

## C8 — measured work and reproduction

Completed with all prespecified seeds. PrimaryT=4 errors(.00195049135,.00163539237,.00068853254), each10millionroots and approximately11.8millionactualnodes. Full bounded-majority comparator completed atT=.8 and2 for allthree8,000-root seeds; itsT=4 cost is theoretical only. The optionalN50k sensitivity completed and remains empirical. Evidence:05-numerics.md, numerics/artifacts/*/results.json, summary.json, tests.log, audit.json. All206archives/32,548,000roots independently audited with no discrepancy; 29tests passed. The earlier flat1.44551 ceiling is not transferred to this different terminal function; C9 supplies a separately proved obstruction. No optimized/general speedup or statistical confidence claim is made.

## C9 — same-datum unsplit raw second-moment obstruction

Assumptions:the C5 Jacobi terminal datum, original unsplit raw common rate λ=2 and uniform F-label probabilities, full tree. Conclusion:E[H_Id(T,x)²]=∞ for every x and T≥3.5. Conventional proof:T02 §9, independently audited in T01 §§9–10; positive extended moment identities, a uniform heat-mixed seed, explicit scalar ODE blow-up, and transfer of divergent time integral to the Id root. Lean coverage:none claimed. This does not prove failure for every rate or proposal, divergence of the first absolute moment, or pathwise finite-time explosion of the branching process. No finite sample variance can certify or refute this infinite-population moment statement.

## Completed formal/code correspondence

All names below are in namespaceEstimatorIntegrity and moduleSlabContinuation. The actual build, declaration list and axiom outputs are in06-formalization.md andlean/. The eleven checked theorems support exactly these deterministic pieces:

- C4:`slabMomentSupersolution_postfixed` and`slabMomentSupersolution_postfixed_strict`; no stochastic Volterra-to-tree or PDE identification in Lean.
- C5:`projectedCoefficientBounds_sum`, `projectedCoefficientBounds_weightedSum`, `projectedCoefficientBounds_value`, `projectedCoefficientBounds_derivative`, `periodicStabilityExponent_upper`; no Jacobi/Fourier/Poincaré analysis in Lean.
- C6:`intervalClamp_abs_sub_le`, `finite_error_recurrence`; no conditional-expectation derivation in Lean.
- C7:`fiftySlabAmplification_upper`, `normalizedSpatialMSE_budget`; no end-to-end stochastic theorem in Lean.

Concrete implementation:C3/C4 inraw_sample ofnumerics/slab_sampler.py; C5/C6 instage_terminal, polynomial_terminal, project_coefficients, run_slab_seed ofnumerics/run_experiment.py. The full numerical/theoretical/formal bridge was independently reviewed in10-correspondence-review.md. C1/C2 remain conventional auxiliary results and have no separate numerical claim in this run.
