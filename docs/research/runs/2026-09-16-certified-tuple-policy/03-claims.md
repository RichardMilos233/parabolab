# Atomic claim ledger

All conventional proofs and assumptions are in [04-theory.md](04-theory.md). A numerical checker verifies rational inequalities, not its own implementation or the stochastic correspondence. Independent mathematical review is [09-independent-review.md](09-independent-review.md); the later C7 addition is reviewed there separately.

## C1 — Full-tree supported policy improvement

**Statement/assumptions:** Fixed mechanism/motion/clock, measurable supported state policies, shared birth positions, independent child futures, nonexplosion, finite old moments at every reachable state. If the exact local old-continuation objective never increases, new unrestricted second moments are no larger.

**Status:** Conventional theorem by monotone iteration; new-policy finiteness follows. Common means required for variance interpretation (C6).

**Implementation/evidence:** Numerical controls in `numerics/`; generic gate in `parabolab/tuple_certificate.py`. Those controls do not implement every possible state policy.

**Lean:** `prefixed_policy_bounds_iterates`, `policy_improvement_iSup` in `TuplePolicy.lean` cover complete-lattice order transfer only; build/axiom evidence in `06-formalization.md`. Random-tree identification, measurability and semigroups omitted.

## C2 — Sign-aware interval acceptance

**Statement/assumptions:** Finite nonnegative contribution intervals, supported normalized old/new probabilities. The sign-selected endpoint sum bounds the true local objective difference. A nonpositive sum certifies local improvement; universal state coverage is needed for C1.

**Status:** Conventional exact finite algebra. Binary criterion: `1/2<=p<1`, `0<=a<=A`, `0<=B<=b`, `p(a+b)<=a`.

**Implementation/evidence:** `tuple_policy_interval_gate`, focused tests, `check_theory.py` and `theory-checks.json`: 1,962 exact rational binary cases, including equality and zero contributions.

**Lean:** `binary_policy_improvement`, `robust_binary_policy_improvement`; binary case only, not the arbitrary-length interval-box function or its Python correctness. See build/axiom log.

## C3 — Refuted shortcuts

**Statement:** A common upper supersolution alone does not order the two true fixed points. Proxy square-root scoring with support alone does not ensure lower variance.

**Status:** Exact counterexamples, respectively constant maps 1 and 2 with bound 3, and true `(1,1)` versus proxy `(100,1)`, objective 4 versus 12.1.

**Evidence:** `04-theory.md`, `theory-checks.json`. No Lean coverage claimed.

## C4 — Joint static rate/probability log-convexity

**Statement/assumptions:** Fixed parameter-independent target/mechanism, bounded arity/nonexplosion, finitely many compatible static positive probability rows and one common positive exponential rate. Full-tree second moment is jointly log-convex via the completed-topology integral. Common mean implies ordinary convexity of variance. No general uniqueness or open-simplex attainment.

**Status:** Conventional theorem. Gradient/Hessian formulas additionally require domination and are conditional. The principle has close generic importance-sampling prior art.

**Evidence:** 1,000 floating finite-kernel log-convexity/Hessian checks in `theory-checks.json` corroborate algebra, not the stochastic theorem. No optimizer implemented and no Lean coverage of joint convexity claimed.

## C5 — Nonuniform six-code certificate

**Statement/assumptions:** Raw 1D Allen–Cahn, scalar-independent static `(p0,p1,p2)`, strictly positive raw labels, constant data for two-sided ODE enclosure; wave coordinatewise suprema for upper-only envelope. Exact branch polynomial and rational step inequalities in theory C5.

**Status:** Conventional closure/comparison argument plus exact rational witnesses for successful instances; all failures retained as inconclusive. Flat improvement control uses exact-zero diffusion tuples; initial wave control uses F2's exact-zero second label.

**Code/experiments:** `parabolab/tuple_certificate.py`, `tests/test_tuple_certificate.py`, `examples/certified_tuple_policy.py`, frozen numerical protocol, `numerics/results.json`, `numerics/witnesses.json.gz`, `numerics/verifier.json`. Executed counts and comparisons in `05-numerics.md`.

**Lean:** C1/C2's algebra/order core only. Six-code stochastic closure, ODE comparison, concrete rational witness values and Python checker are not formalized.

## C6 — Common mean for supported policy changes

**Statement/assumptions:** Same target, supported nonexplosive policies; uniform all-space/all-time six-code second-moment envelope at one policy for the bounded Allen–Cahn mild-system identification. Cancellation of absolute first-moment factors and convergence imply common integrable means; signed bounded mild uniqueness identifies the PDE value.

**Status:** Conventional proof explicitly extending the prior uniform-only note. Thus exact moment differences equal variance differences. Floating mean-square evaluation alone does not certify relative percentages.

**Evidence:** `04-theory.md` C6, independent review §3, successful full all-code witnesses. No new Lean stochastic coverage.

## C7 — Safe nonzero wave F1 update

**Statement/assumptions:** Uniform baseline wave moments, finite uniform all-time/space six-code bound with `M_F1<=Bbar`. C7 derives `M_F0*M_F2 >= R*(M_D²*M_F3/4)` with `R>=4[1-(lambda+Bbar/lambda)T]`. If the rational lower bound is at least 2, replacing the F1 first-label probability by 2/3 is safe at every reachable decision. F0 stays uniform; F2 may independently increase to 19/20.

**Status:** Conventional theorem plus exact checks for the rates/horizons saved by `wave_gate_check.py`. The two F1 alternatives are genuinely nonzero. The global envelope ratio is conservative, and the result is neither an optimal-q theorem nor a comparison against the terminal proxy.

**Evidence:** `wave-gate-checks.json`, exact baseline witness and independent review. For R_rat>2, positivity propagates along F1 to F0 to Id and proves a strict variance decrease at every finite x and positive remaining time through T. A smaller new wave envelope alone does not quantify its magnitude.

**Lean:** `binary_policy_improvement` and `two_thirds_policy_improvement` passed the build and axiom audit recorded in `06-formalization.md`; they supply the algebra after the ratio inequality. The spatial semigroup and nonlinear moment comparison producing that ratio remain conventional.

## C8 — Exact flat variance-explosion threshold and optimized-horizon scaling

**Statement/assumptions:** Raw 1D Allen–Cahn, flat phi=1/2, positive constant common first-label probability p for F0,F1,F2 (F3 unchanged), common lambda>0, exact likelihoods. The unrestricted Id second moment is finite exactly for `T<log(1+lambda² p C)/lambda`, where `C=integral_0^infinity 1/(9/64+v/16+9v²/2+6v³) dv`. The endpoint and all later horizons have infinite second moment. Under C6's common finite mean this is an exact variance boundary.

**Status:** Conventional theorem with an independent mathematical audit, including an explicit proof that the Id root itself diverges. This is not inferred from the failed ODE solver or box search. Maximizing the threshold over lambda separately for each p makes it proportional to sqrt(p), so p=19/20 improves over p=1/2 by exactly sqrt(19/10). That is a horizon-threshold ratio, not a variance or runtime ratio.

**Code/evidence:** `numerics/flat_explosion_check.py`, frozen `numerics/flat-explosion-protocol.json`, and `numerics/flat-explosion-checks.json` give exact rational integral/Taylor bounds. At T=1/2, lambda=3/4, uniform p=1/2 is proved divergent, while p=19/20 is proved finite; the earlier candidate all-code ODE certificate independently supplies finiteness. At lambda=1 both are finite. The main integral enclosure is approximately [1.5296515573,1.5306314106], with exact rational endpoints in the artifact. Independent reviewer used a different coarser exact mesh and obtained the same separation. Floating quadrature is diagnostic only.

**Novelty/limits:** The scalar reduction and concrete threshold are new to this project in the inspected record; ODE-based moment horizons have primary-literature precedent. The flat candidate coincides with the existing terminal proxy at floor_mass=.1, so a new sampler is not claimed. Nonconstant data do not admit this derived scalar reduction.

**Lean:** None for the scalar transform, explosion theorem, integral/exponential numerical bounds or optimized-horizon corollary. The five checked lemmas cover C1/C2/C7's finite algebra and order steps only.
