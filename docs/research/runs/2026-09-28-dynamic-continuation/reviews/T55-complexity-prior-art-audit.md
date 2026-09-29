# T55: primary-literature proximity audit of D23–D26

Completed 2026-09-28. Independent research review; bounded literature scope.
This report is the only file owned by T55. No code, numerical experiment,
Lean proof, external communication, or publication was performed.

**Verdict: GO for the precisely scoped theorem statements and their
attributed combination; NO-GO for a worldwide originality or priority
claim.** Eighteen targeted searches and the primary theorem inspections
below did not locate a theorem with the same fixed smooth input class,
exact initial-value oracle, fixed absolute RMS target, and asymptotic
parameter T tending to infinity. Several ingredients are already explicit
in prior work, including hidden smooth bumps at zero, adaptive query
symmetry with expected stopping cost, smooth-integration exponents,
gap-majority hardness, interpolation, and the Allen–Cahn scalar profile.
Their combination with the required uniform nonlinear PDE estimates is
the defensible subject of the project result. This is an absence statement
about this search, not a claim that the combination is absent everywhere.

## 1. Exact statements used for comparison

The domain is the unit-volume torus, with generator Delta/2, and the
target is S_T v(x*) at a public point. The unknown v is a deterministic
smooth function. Only its exact point values are available; its formula,
integral, derivatives and evolved solution are unavailable. Queries may
be adaptive, algorithms may stop randomly and have biased outputs, and
every input-dependent evaluation counts. Private input-independent
randomness and scalar operations are free. The accuracy guarantee takes
a supremum over the promised class; expectation is over the algorithm.
The bounded derivatives are those through the fixed finite order s,
not all derivatives of the smooth input.

| Claim | Statement compared with the literature | Essential qualification |
| --- | --- | --- |
| D23 | On 0<=v<=b/2, C^s,max norm<=R with R>0, the general-reaction extension gives E Q_T(0)>=c exp(lambda*d*T/(s+d)) for every uniformly RMS-epsilon accurate algorithm, epsilon<b/2. | The expensive zero input is the same at all horizons. Hidden alternatives depend on T. The reaction is fixed, C², positive on (0,b), vanishes at 0,b, and lambda=f'(0)>0. |
| D24 | For f(u)=u-u³, b=R=1 and RMS tolerance 1/4, the minimax expected query order on the nonnegative class is Theta(exp(d*T/(s+d))). | The matching upper bound samples point values and applies a biased scalar transform. Its query count is deterministic. |
| D26 | The positive-class matching order is Theta(exp(lambda*d*T/(s+d))) for the D23 reactions and every fixed epsilon in (0,b/2). | Constants depend on the fixed reaction and class. The repaired upper bound is nonuniform per horizon, with finite public rational/integer advice independent of v. |
| D25 | On the genuinely sign-changing Allen–Cahn class with height<=1/2 and C^s,max norm<=1, RMS 1/4 requires worst-case E Q_T>=c exp(2dT/(2s+d)), for 1<=d<=4s. | A finite prior proves average expected cost and hence worst-case cost. The expensive input may depend on the algorithm and T. The critical d=4s case has a separate amplitude choice. No matching signed upper bound or d>4s conclusion is asserted. |

D26 is the accepted R01 statement after the T54 repair, now recorded in
04s. Its advice consists of a hard-coded finite sample count, a positive
rational approximation to exp(lambda*T), and a finite rational profile
table. There is no online reaction, profile, mass, or PDE oracle. The
minimax infimum allows a different algorithm for each public horizon.
This is not a uniform effective construction from an arbitrary
unrepresented C² reaction, and no bit or preprocessing complexity is
claimed.

## 2. Closest primary PDE-complexity sources

**P1. Marek Kwas, _Complexity of multivariate Feynman–Kac path integration
in randomized and quantum settings_ (2004), arXiv:quant-ph/0410134v1.**
Inspected §§3.2, 8.1–8.2 and 9. The paper already counts expected exact
function evaluations and uses worst-input RMS error for a linear
Feynman–Kac problem with unknown initial function and potential. Section
8.1 reduces the problem to weighted integration by setting the potential
to zero; §9 treats smooth function classes. The target time is fixed in
the problem definition. This is close prior art for the information model
and integration reductions, but it neither includes saturating semilinear
reaction dynamics nor states the audited fixed-error large-T rates.
Replacing an accuracy parameter by exp(-T) would require a new uniform
comparison and control of the time-dependent constants.
[Primary version](https://arxiv.org/pdf/quant-ph/0410134v1).

**P2. Knut Petras and Klaus Ritter, _On the Complexity of Parabolic
Initial Value Problems with Variable Drift_ (2005 Dagstuhl version).**
Inspected §2, Theorem 4 in §4.3, Corollary 2, and §5.4. Theorem 4
transfers integration hardness to the coefficient-to-solution map;
Corollary 2 gives randomized error at least order
n^(-(r+alpha)/(d+1)-1/2) for the specified coefficient Hölder class.
The queried inputs are space-time drift/potential coefficients, the
initial function and target time are fixed, and the PDE is linear in u.
The solution depends nonlinearly on the queried coefficients. Thus even
a nonlinear-map integration reduction for a parabolic problem is prior
art, but the unknown object, dimension in the exponent, and asymptotic
parameter differ here. Theorem numbers refer to this inspected preprint,
not an unchecked journal revision.
[Primary PDF](https://drops.dagstuhl.de/storage/16dagstuhl-seminar-proceedings/dsp-vol04401/DagSemProc.04401.10/DagSemProc.04401.10.pdf),
[record and DOI](https://doi.org/10.4230/DagSemProc.04401.10).

**P3. Christian Beck, Fabian Hornung, Martin Hutzenthaler, Arnulf Jentzen
and Thomas Kruse, _Overcoming the curse of dimensionality … via
truncated full-history recursive multilevel Picard approximations_
(Allen–Cahn paper; title abbreviated)
(2019), arXiv:1907.06729v1.** Inspected Theorem 1.1, with its quantifier
order and cost definition; Theorem 4.5 is the general result and
Corollary 5.3 treats Allen–Cahn. Theorem 1.1 fixes T before obtaining a
constant c and a cost bound c*d*epsilon^(-(2+delta)) together with RMS
accuracy. Its cost there counts scalar Gaussian realizations, rather
than exactly our charged initial-value queries. This is genuine
semilinear Allen–Cahn approximation prior art. It supplies neither a
large-T minimax lower bound nor a constant controlled uniformly as T
grows, so it does not settle or contradict D23–D26.
[Primary version](https://arxiv.org/pdf/1907.06729v1).

**P4. Martin Hutzenthaler, Arnulf Jentzen, Thomas Kruse, Tuan Anh Nguyen
and Philippe von Wurstemberger, _Overcoming the curse of dimensionality
in the numerical approximation of semilinear parabolic partial
differential equations_ (ETH report 2019-46, 3 September 2019).**
Inspected Theorem 1.1, a specialization of Theorem 3.8. It gives RMS
approximation and polynomial dimension/accuracy cost for globally
Lipschitz, gradient-independent nonlinearities and polynomially growing
terminal data. Again T is fixed before the complexity constant is
chosen. This establishes that broad semilinear PDE complexity guarantees
predate the project; it does not establish the horizon asymptotics on the
audited positive or signed classes.
[Inspected primary report](https://www.sam.math.ethz.ch/sam_reports/reports_final/reports2019/2019-46.pdf).

## 3. Information and statistical ingredients that are already known

**P5. Robert J. Kunsch, Erich Novak and Daniel Rudolf, _Solvable
Integration Problems and Optimal Sample Size Selection_ (2018),
arXiv:1805.08637v2.** Inspected §3.4, Proposition 3.13 and its proof,
and Theorem 3.15. Proposition 3.13 compares general adaptive algorithms
with iid algorithms over unions of permuted finite-valued cell classes,
under expected-cost constraints. The proof uses conditional symmetry,
private randomness, stopping rules, and Markov truncation to bounded
cardinality. Theorem 3.15 distinguishes zero from one randomly hidden
positive smooth bump to prove unsolvability on unbounded C-infinity([0,1]).
These information arguments are close precedents for D23/D25. Theorem
3.15 has no fixed derivative/range ball; Proposition 3.13's limiting
union differs from D25's finite-K experiment. Fixed norm scaling,
finite constants, and nonlinear PDE transfer remain local obligations.
[Primary version](https://arxiv.org/pdf/1805.08637v2).

**P6. Robert J. Kunsch and Daniel Rudolf, _Optimal confidence for Monte
Carlo integration of smooth functions_ (2018), arXiv:1809.09890v1.**
Inspected Lemmas 2.1–2.2, Theorem 2.3, the norm-scaled bumps in its proof,
and Theorem 3.6. For fixed confidence and isotropic W^s_infinity classes,
these give the smooth-integration error order n^(-s/d-1/2). The source
distinguishes probabilistic error from mean and RMS error; those notions
must not be silently equated. In particular, the fixed-confidence lower
bound also constrains RMS algorithms via Markov's inequality. The
disjoint signed bumps and the numerical exponent underlying D25 are
classical. This source estimates a linear integral, not a nonlinear PDE
value after a growing evolution time.
[Primary version](https://arxiv.org/pdf/1809.09890v1).

**P7. Shalev Ben-David and Eric Blais, _A Tight Composition Theorem for
the Randomized Query Complexity of Partial Functions_ (2020),
arXiv:2002.10809v2.** Inspected §3, Definition 25 and Lemma 26.
Lemma 26 gives Theta(K) randomized query complexity for majority
restricted to two Hamming layers separated on the square-root-K scale.
Its proof uses permutation symmetry to remove the adaptive choice of
query locations. This directly overlaps D25's discrete information
problem. The paper's lemma does not provide D25's exact numerical KL and
truncation constants or its PDE separation estimate. Those constants
remain the responsibility of the local proof, not imported guarantees.
[Primary version](https://arxiv.org/pdf/2002.10809v2).

**P8. Louis Nirenberg, _On elliptic partial differential equations_,
Annali della Scuola Normale Superiore di Pisa, series 3, 13(2)
(1959), 115–162.** Inspected Lecture II, the interpolation theorem at
printed page 125, equations (2.1)–(2.2), and the bounded-domain
qualification in remark 5 at page 126. The height-versus-mass exponent
s/(s+d) is the Gagliardo–Nirenberg interpolation exponent obtained from
the L1 norm and bounded derivatives of order s. On a compact domain a
lower-order term must be retained. The project's explicit periodic
kernel proof supplies convenient constants and its particular norm
convention; it should not be presented as a new interpolation exponent.
[Primary scan](https://www.numdam.org/item/ASNSP_1959_3_13_2_115_0.pdf).

**P9. Mark Huber, _An optimal (epsilon,delta)-approximation scheme for
the mean of random variables with bounded relative variance_ (2017),
arXiv:1706.01478v1.** Inspected Theorems 1–2. The problem is iid mean
estimation with a known upper bound on relative variance, and relative
accuracy with prescribed confidence; matching leading sample constants
are established. This is relevant statistical context, not the D24/D26
guarantee. Our positive class includes zero and arbitrarily small mass,
and does not have a class-uniform bounded relative variance. The
algorithm only needs absolute accuracy after a bounded nonlinear
transform.
[Primary version](https://arxiv.org/pdf/1706.01478v1).

A related search lead was L. Gajek, W. Niemiro and P. Pokarowski,
_Optimal Monte Carlo integration with fixed relative precision_,
Journal of Complexity 29 (2013), 4–26,
[DOI 10.1016/j.jco.2012.09.001](https://doi.org/10.1016/j.jco.2012.09.001).
Publisher metadata/abstract and the bibliography in P5 were accessible;
the full publisher text did not open. No theorem in that paper is claimed
to have been inspected or excluded as an exact overlap.

## 4. The closest nonlinear long-time PDE mechanism

**P10. Martin Hairer, Khoa Lê and Tommaso Rosati, _The Allen–Cahn
equation with generic initial datum_ (2022), arXiv:2201.08426v1.**
Inspected equations (1.1)–(1.5), Theorem 1.1, Theorem 2.1 and
Proposition 4.6. The source explicitly uses the normalized scalar
profile Phi(t,a)=a/sqrt(exp(-2t)+a²), and proves a random-field scaling
limit through linear amplification followed by nonlinear scalar flow.
The initial data are rescaled mollified white noise on Euclidean space;
their pointwise scale grows as the small spatial parameter vanishes.
The convergence is in law, with the stated local spatial topology and
coupling refinements. It is not uniform over a fixed bounded C^s class,
and it states no exact-point-query information complexity. Thus the
scalar-profile mechanism is established prior art, but this theorem
cannot replace D24/D26's deterministic class-uniform approximation or
D25's target separation for every arrangement in either finite layer.
[Inspected primary version](https://arxiv.org/pdf/2201.08426v1).

The general-C² coordinate in D26 also follows by direct one-dimensional
separation of variables: G'/G=lambda/f and Phi=G^(-1). The report does
not count that algebra as a novel conjugacy theorem. The distinctive
obligations of the local argument are its endpoint conditions, global
profile error bound, and use in a uniform PDE/query estimate without
assuming concavity or a simple root at b. No exact prior matching query
theorem for this general reaction class was located in the inspected
sources.

## 5. What the comparisons do and do not establish

The two exponents have transparent information-theoretic origins. A
positive bump of width 1/k and height k^(-s) has mass of order
k^(-(s+d)). Setting this mass at the unstable scale exp(-lambda*T)
gives K=k^d of order exp(lambda*d*T/(s+d)). With K signed bumps and
a square-root-K imbalance, the mass is instead of order
k^(-(s+d/2)). Setting that at exp(-T) gives
K of order exp(2d*T/(2s+d)). The latter is the inversion of the
classical smooth-integration error scale, rather than a new discrete
query exponent. The source-specific precedents are P5–P7 above.

This scaling alone proves neither PDE theorem. For D23 a hidden bump
must reach a fixed target gap by the actual nonlinear evolution. For
D24/D26 the scalar profile of the true mass must approximate the entire
positive class uniformly, including arbitrarily small mass, before
sampling that mass can be justified. For D25 the nonlinear correction
to the mean must be controlled for every sign arrangement, not merely
with high probability over a spatial random field.

In D25 the audited cubic error is of size exp(T)*A³. On the chosen bump
scale it decays for d<4s; at d=4s the separate amplitude choice makes
it small. The threshold is a limitation of this proof's nonlinear
remainder estimate. It is not an established universal critical
dimension for query complexity. No matching signed upper theorem or
sharpness in all dimensions follows from classical integration rates.

The positive result is also not a claim that ordinary integration of
nonnegative smooth functions at small absolute tolerance has exponent
d/(s+d). Its target is a saturated profile of an exponentially enlarged
mass, at fixed final accuracy. Large masses need little discrimination
after saturation, whereas the transition region moves toward zero.
The anchored profile estimate controls these regimes together, and
the zero datum is part of the uniform promise.

Three model distinctions prevent invalid literature deductions:

1. A theorem with time fixed before its cost constant cannot simply be
   reinterpreted as a sharp time-asymptotic theorem. It may have constants
   growing rapidly with T. Conversely, our time lower bounds do not
   contradict fixed-time polynomial dimension/accuracy bounds.
2. A stochastic initial-data scaling theorem controls its specified
   probability law. A finite hard prior can prove a worst-input
   information bound only after every function in its support satisfies
   the required class and PDE separation estimates.
3. Expected-cost hardness requires a justified stopping argument.
   Finite-query hardness alone does not cover algorithms with rare
   expensive runs. D25 supplies its own finite-prior truncation; P5 is
   close prior art for that methodology. D23 uses its common zero
   transcript directly.

## 6. Defensible contribution wording

A defensible description is:

> We establish matching large-time, fixed-accuracy randomized point-query
> bounds on a fixed nonnegative smooth initial-data class for a stated
> family of scalar reaction–diffusion equations. The upper bound uses a
> uniform nonlinear reduction to a scalar profile of the spatial mass;
> the lower bound transfers classical hidden-bump information hardness
> through the actual PDE. For a genuinely signed Allen–Cahn class, we
> additionally establish a stronger lower bound in the stated dimension
> range by controlling the nonlinear mean error and applying classical
> gap-majority information arguments.

For D26 append the finite public-advice/nonuniform qualification from
Section 1. The result is an information-complexity theorem, not a
practical cost comparison with branching, MLP, or grid algorithms.

The search does **not** justify “first parabolic query lower bound,”
“first hard zero input,” “new smooth-integration exponent,” “new
gap-majority lower bound,” “new Allen–Cahn scalar profile,” or a
uniformly computable efficient solver for arbitrary C² reactions.
It also does not justify calling D25 a signed matching-complexity
theorem. No inspected source has been identified as already proving
the complete D23/D24/D26 or D25 statement, but the search is too bounded
to certify priority. Attribution should attach to the exact ingredients
at P1–P10, rather than treating a literature search with no exact hit as
evidence of worldwide originality.

## 7. Frozen search inventory and access limits

All searches were conducted on 2026-09-28. Exactly 18 search strings were
used, within the assigned 12–18-query scope. Subsequent direct opens,
PDF reads, in-document finds, and bibliography following introduced no
additional search queries. Only primary papers/reports support the
comparisons above; search snippets alone did not establish a theorem.

| ID | Exact search string |
| --- | --- |
| Q01 | `randomized information complexity semilinear parabolic equation long time initial function point evaluations` |
| Q02 | `Petras Ritter parabolic initial value problems complexity theorem lower bound` |
| Q03 | `"reaction diffusion" "query complexity"` |
| Q04 | `"Allen-Cahn" "information-based complexity"` |
| Q05 | `"semilinear parabolic" "randomized" "complexity" "lower"` |
| Q06 | `"parabolic" "initial condition" "randomized complexity"` |
| Q07 | `"nonnegative" "integration" "relative error" "smooth" randomized complexity` |
| Q08 | `"long time" "information-based complexity" differential equations` |
| Q09 | `"Feynman-Kac" "randomized" "complexity" Kwas point evaluations` |
| Q10 | `"Allen-Cahn" "overcoming the curse" complexity theorem time` |
| Q11 | `"nonnegative functions" "randomized integration" lower bounds` |
| Q12 | `"gap majority" "randomized query complexity" Ben David Blais` |
| Q13 | `semilinear reaction diffusion torus small initial data nonlinear scalar profile long time spatial average` |
| Q14 | `"nonnegative" "smooth" "integration" "complexity" Monte Carlo lower` |
| Q15 | `"parabolic" "complexity" "time horizon" lower bound` |
| Q16 | `"unstable equilibrium" "query" complexity differential equations` |
| Q17 | `"Optimal Monte Carlo integration with fixed relative precision" pdf` |
| Q18 | `"Allen-Cahn equation with generic initial datum"` |

The links P1–P10 freeze the inspected versions where versioned primary
URLs exist. P2 is the Dagstuhl preprint, P4 the dated ETH report, and P8
the original journal scan. The general-integration source P5 was reached
through primary-paper references. The inaccessible relative-precision
article remains an explicit access limit. This was not an exhaustive
search of books, theses, all languages, unpublished work, or all later
citing papers; no negative conclusion is drawn about those collections.

## 8. Local evidence snapshot and remaining scope

The comparisons use the following local SHA256 snapshot. These files
were read without modification by T55. A later change to a claim's
oracle, quantifiers, reaction assumptions, or time dependence requires
a fresh comparison.

| Local source, relative to the run directory | SHA256 |
| --- | --- |
| 04p-fixed-zero-query-lower-bound.md | ee54d260705193b8d946b1f0d493215374230985fd6f3f3fb173d2252b8ffa99 |
| 04q-matching-positive-query-complexity.md | a655e649b70e6f99097eeccff7c459f6faadb14acd82019e7727da051d4ab6d0 |
| 04r-signed-many-bump-complexity.md | 4bdcb75b7ee62c40879a80cb84b0949f1a9e796d387775e5760cab04a33fa419 |
| 04s-general-reaction-query-complexity.md | 56286d5d92a8ba894c115d6cc29665c6f4137481cf91f73f567f5e580a17409e |
| reviews/R01-c2-profile-generalization-draft.md | f3fae210587e3349ebd105b1f5b0dbdc4011b9dff504d08549eac1e8bea0876e |
| reviews/T54-c2-profile-independent-audit.md | c01c0138276a1cd89804810db9ab903f702378b0541e77fb8ae0c36de8a5bfb5 |

The mathematical proof audits remain T44/T45, T46/T48, T50/T53, and
T54 for their respective claims. T55 adds literature proximity and
attribution, not a new end-to-end proof or formal verification. It
identifies no literature-based blocker to retaining the accepted scoped
claims. Remaining qualifications are priority uncertainty, the explicit
unread source, D26's nonuniform scalar advice, and D25's limited
dimension range and absence of a matching upper bound. The report hash
is supplied in the completion message after writing this file, avoiding
a self-referential hash inside the artifact.
