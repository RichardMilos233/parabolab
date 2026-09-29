# Atomic claim ledger

All conventional mathematical claims are stated and proved in [04-theory.md](04-theory.md), with an independent [theory audit](09-independent-theory-review.md). Formal and numerical columns are updated only after their actual checks.

| ID | Exact scope and assumptions | Mathematical status | Code/evidence | Lean and omitted scope |
|---|---|---|---|---|
| L1 | Raw flat phi=.5 Allen–Cahn, same labelled expansion, actual reciprocal conditional weights, positive support, almost-sure completion. E\|H\| finite iff T<(3pi−2log3)/5. | Conventional proof; independent reconstruction agrees | [Rational boundary certificate](numerics/boundary-certificates.json), 100-digit and quadrature diagnostics in [raw results](numerics/raw-results.json); binary64 containment misses retained | Factorization, positivity and reciprocal identity proved; density cancellation, improper integral, random tree and blow-up outside formal coverage |
| L2 | Same object and strict subcritical T. EH²>=(.5+s(T))², extended inequality; variance version requires common finite mean. | Cauchy–Schwarz proof; independent review | Implicit scalar absolute moments and near-boundary lower bounds in `raw-results.json:absolute_rows` | Not separately formalized |
| L3 | Raw flat common scalar exponential rate and common p in (0,1). Full L2 finite iff T<log(1+lambda²pC)/lambda; optimized horizon sqrt(pC) max h. | Existing threshold theorem plus elementary maximization proof | Prior C witness [reverified](numerics/prior-flat-verify.log); exact caps <.705/.972/1; 24 longer-horizon rows and 41 scalar checks | Prior stochastic/ODE bridge remains conventional; no new global optimizer formalization |
| B1 | Standard ternary Brownian tree, common rate r>=2, measurable phi in [-1,1], shared child birth position. Output bounded, mean equals bounded Allen–Cahn mild solution for every finite T. | Conventional proof, known majority representation | `parabolab/majority.py`; 60 [prescheduled rows](numerics/bounded-results.json); [implementation review](10-correspondence-review.md) | Reaction identity, cube and all-finite-tree bound proved; completion and mean/PDE bridge outside formal coverage |
| B2 | Symmetric multiaffine ternary kernel B_r. Cube preservation iff r>=2; E nodes=(3exp(2rT)−1)/2. | Algebra, uniqueness of diagonal coefficients, branching mean identity | Exact corner checks and complete node records; 122,880 roots [audited](numerics/bounded-audit-reproducible.json) | Corner necessity and cube sufficiency proved; expected tree population outside formal coverage |
| B3 | Bounded B_r family, common bounded PDE mean. Full second moment nonincreasing r>=2; expected nodes increasing. | Conventional second-moment reaction and PDE comparison proof | 9,720 exact rational kernel evaluations; independent flat moment solvers agree to 7.03e-10 in [theory checks](numerics/bounded-theory-checks.json) | Not formalized; never used as a universal variance-cost optimum |
| N1 | Predeclared finite sample and deterministic mesh regimes only. | Completed empirical/numerical evidence | 60 bounded rows to T=2; six raw batches to T=2; 72 raw-wave rows with 12 stops and 28 unreached horizons retained; [numerical record](05-numerics.md) | Not a theorem or end-to-end certificate; floating error and unvalidated spatial boundaries remain explicit |

No current claim asserts a worldwide first result, full solver formal verification, or that a deterministic numerical failure proves explosion. The implemented comparator is Allen–Cahn-specific; no claim transfers to arbitrary fully nonlinear PDEs. The known majority representation is a comparison, not an improvement in lambda for the raw tree.

Final verification: eleven Lean theorem declarations with standard axioms only;
274 Python tests passed (14 deselected); 16 raw verifier checks passed;
the independent bounded archive audit passed. Details and retained failed
diagnostics are in [05-numerics.md](05-numerics.md) and
[06-formalization.md](06-formalization.md).
