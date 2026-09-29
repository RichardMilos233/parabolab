# Theory, formal statements and numerical correspondence

Status: passed within the dynamic-continuation and deterministic-obstruction
scope, after T14/T16 completed. This is a research-role synthesis of source
inspection and independent numerical audit, not an end-to-end formal proof.
The later noncompact sampler has not yet passed its own implementation gate.

## Mathematical object and normalization

The target is elapsed-time periodic Allen–Cahn, u_t=Delta u/2+u-u^3, with
u(0)=.9g. The known Jacobi profile g is time independent; the evolving solution
is not supplied to any producer terminal callback. Spatial norms use the
probability measure dx/L. Thus coefficient observations are H*b(X) for
uniform X in [0,L), with no missing factor of L.

`dynamic_interface.py` uses z=g^2, a=2/21 and the two functions
b0=g(1-z/a), b1=g*z/a. Its callback evaluates

    v=g[c0+(c1-c0)z/a],
    v'=g'[c0+3(c1-c0)z/a].

The factor three in the derivative is present. The closure copies and freezes
the input coefficient pair. Its feasible region is exactly the prescribed
six-vertex polygon .9<=ci<=1, |c1-c0|<=2/735, with a small explicit floating
point feasibility tolerance. The producer neither clips each coefficient
separately nor assumes the constraint projection is unbiased.

The Gram matrix uses the same normalized measure. Independent elliptic
identities and high-precision quadrature establish its numerical value;
positive eigenvalues and condition number about 6.93 are recorded. This is
numerical verification, not an interval-arithmetic enclosure.

## One stage reconstructed from the implementation

`run_dynamic.py` first saves the PCG64 state, draws all root positions, freezes
the previous stored coefficients into a callback, then calls the frozen raw
sampler at h=.08. The imported sampler's source hash is checked. It retains
the original signed code weights, exponential rate two and the prescribed
label probabilities; no observed-value clipping or tree-size cap is added.

The producer forms bhat as the arithmetic mean of H*b(X), solves G*c=bhat,
and minimizes the Gram quadratic distance over the feasible interior and all
six edges. It saves the raw and projected coefficients, all root values and
positions, work counts, RNG states and diagnostics. Only afterward does it
read the reference coefficients to compute error metrics. The next terminal
depends only on the projected pair, not any reference-derived quantity.

The independent T14 audit reconstructs G and the projection without importing
the producer/interface modules. It streamed every one of the 600 archives and
verified all 60 million stored position draws by replaying their pre-stage
RNG states. This does not replay the complete tree draws, so it is not claimed
as an independent regeneration of every random tree. It verifies coefficient
and RNG chain continuity, archive manifests, feasibility, moments, work and
errors. Every coefficient and moment difference was zero; the largest
recomputed error-field difference was 3.47e-18. All 342 protected initial
files remained unchanged.

The two-hour per-seed wall-clock safeguard was never reached. Partial stages
would be retained and labeled incomplete rather than used for a coefficient
update. All three prescribed paths completed 200 stages with 100,000 roots
per stage; no selected retry or outcome-dependent parameter change was made.

## Why the statistical conclusion is limited

Conditional on the previous interface, the coefficient observation is centered
around the semigroup coefficient vector. Its imported local population second
moment bound and the orthonormal trace identity give nu=d*M/N. This centering
is applied before the nonlinear metric projection. Nonexpansiveness, the
deterministic approximation defect and Minkowski give the reviewed recurrence

    r_next <= sqrt(exp(-2*mu*h)*r_previous^2+nu)+beta.

The conventional derivation is in `04-theory.md` and T01/T02. The finite Lean
module proves this recurrence's invariant bound from its hypotheses and the
exact rational budget. It does not derive unbiasedness or prove the PDE
invariant class. Nor does the sample maximum of H^2 verify the population
second-moment bound: rare events are not ruled out by this diagnostic.

The reported three-seed empirical RMS is descriptive, not a confidence bound.
The theorem bounds each grid endpoint in ensemble RMS, not the expectation of
the maximum over all endpoints. Floating point and deterministic-reference
errors are outside its exact-arithmetic guarantee.

## Independent reference and comparator fairness

T11 solves a separate odd-sine Galerkin ODE with direct cubic projection,
without the stochastic sampler or learned projection. Its four tests include
an independent complex-Fourier convolution. Six mode/grid/tolerance runs
give an empirical reference discrepancy of 1.0561e-11, below the prespecified
1e-9 acceptance threshold. This is convergence evidence, not a rigorous PDE
discretization enclosure.

T14 compares the complete [0,16] interval including t=0. The fixed midpoint
.95g has maximum measured error .0109458, already below the .02 target.
At T=16, g itself outperforms the three-seed empirical RMS. Each MC path
took 26.6–27.7 times the strict deterministic solve. Timing scope distinguishes
sampling, stage time, whole path, preflight and six-solve reference validation.
The negative comparison is not hidden by summing three stochastic paths and
comparing only that aggregate against one deterministic solve.

## Obstruction theorem, Lean and deterministic illustrations

T13 checks the joint-likelihood cancellation, genuine support, exhaustion by
completed finite-depth trees, and nonnegative Tonelli restart used in D10.
It also checks D11's finite-radius critical endpoint: the Id absolute moment
can remain finite exactly at tau, while being infinite strictly afterward.

`AbsoluteMomentObstruction.lean` proves the stated real-function Riccati
barrier via arctangent and the mean-value theorem. The two declarations use
only standard foundational axioms. It does not formalize the finite code
comparison, canonical probability measure, infinite power series or restart.

T16's 80-decimal calculations verify fixed analytic identities for the sine
and rational examples and their truncation horizons. The maximum residual is
1.0543e-81. The figures' infinite regions come from the reviewed theorem, not
extrapolation of finite numerical samples. No infinite-moment claim is inferred
from a numerical blow-up, and no finite moment is inferred from successful
sampling. The checks do not change the frozen dynamic experiment.

## Subsequent scoped theory and formal checks

T15 closes the conventional all-horizon dimension split for the noncompact
small Gaussian quadratic family and separately proves signed PDE
correspondence. T18 completed the seven finite coefficient inequalities in
HeatEnvelopeBudget.lean; its report06c explicitly excludes heat kernels,
probability, PDE comparison and the remaining exponential substitution.

T17 passed the ideal heat-transform sampling law and finite-depth work
argument. T21 completed seven theorems in HeatTransformWork.lean for the
bounded products, finite multitype recurrence and scalar binary budgets.
The formal112-node corollary takes the recurrence as a hypothesis; it does
not derive the random tree law. All checked declarations use only standard
foundational axioms. No floating sampler or arithmetic-cost certificate is
implied. T20's relative-cost separation remains a conventional theorem and
its matched scalar baseline is retained in04g and the report.

T22 passed the critical moment/work phase in04h. T26 separately passed the
ideal gamma-tilt construction in04i; finite-tree density telescoping and
completed-tree exhaustion close recursive completion. Its independent
normalization has conditional mean equal to the true tree likelihood.
Node work and derivative/inverse arithmetic costs remain distinct. T23 passed
the actual real-measure Cauchy–Schwarz/integrability theorem and three finite
critical-exponent statements in CriticalMomentWork.lean. The fresh build
passed3396/3396; all four axiom audits list only standard foundations.
The canonical tree/cusp and general-p optimal proposal bridge remain
conventional. The fixed02c deterministic illustrations passed inT25 after
the formal gate. The script checks source/build/axiom hashes before evaluation
and preserves all54 exact-identity checks at80digits. Their maximum discrepancy
is1.0543e-81. All12 finite-cutoff endpoint contributions are positive and
increase as the cutoff decreases. Root inspected the PNG and matching
code/protocol: the figure distinguishes theory from diagnostics and excludes
a full-S2 interpretation. No asymptotic theorem is inferred from four cutoffs.

T27/T28 conventionally passed04j/04k and T30 passed04l's two-barrier extension.
The finite-generation proof establishes completion before using the bounded
return; the expectation is identified by first-event renewal and bounded
mild uniqueness. T30 separately checks the actual width-integrability lemma,
the explicit Allen–Cahn clock addendum and the relative-variance constants.
T29 passed the actual formal analytic translation: continuity, monotonicity
and convergence derive width integrability and its total integral, without
assuming either the width or the individual deficit is integrable. All eight
declarations built in a fresh3385-job run with standard axioms only. The
ODE shift/change-of-variables and stochastic/PDE bridges remain outside06f.
No corresponding sampler experiment or floating-point certificate exists. The Markov corollary assumes
a jointly measurable conservative transition kernel and exact independent
edge draws; it does not hide transition-oracle work inside a node count.

On this continuation, all342 protected initial hashes were rechecked with
zero mismatches. That check does not rerun the600-archive audit, which remains
the separate frozenT14 evidence.

No result in this correspondence review establishes publication priority,
high-dimensional practical superiority, or achievement of the user's long-term
award-level research aspiration.


T31 passed the limiting-clock conditional law, stable scaled-defect algebra,
and scoped coefficient-limit bound. It explicitly excludes a complete
floating-bias proof and proves the arbitrary-measurable-data oracle obstacle.
T32 passed minorized burn-in plus two imported linear Bernoulli factories,
including fresh conditional-cost composition; no evolved solution oracle is
assumed. Neither that factory extension nor its cost is formally certified.
T33 preserves all frozen critical arrays and legacy201-point series in the
canvas; SDK TypeScript and bundle checks passed, without a GUI-render claim.
T34's bounded protocol clarifications were incorporated before implementation:
accepted clocks, explicit zero-time output, prespecified RMS, failure gates,
and full21-query deterministic timing scope. No numerical outcomes were used
to choose these parameters.


## Two-barrier implementation checkpoint before the raw audit

Root inspected the full T35 stochastic mechanism and the driver's preflight,
official diagnostics, failure retention and primary paths before clearing
execution. Accepted event time s is the children's remaining horizon;
Brownian edge variance is T-s; all children share the branch location and
have fresh descendants. Mixture probability uses the accepted event's zeta,
not the original root time. Leaf data are the original fixed cosine, and the
bounded multiaffine return is converted directly to the scaled defect.
No PDE reference is imported into the mathematical sampler.

Before artifact freeze, source review corrected the reference loader's
uppercase PASS/structured gate interface, replaced an unjustified standalone
relative-error test at a vanishing event time by a frozen combined absolute
and relative tolerance, and corrected start-time recording. Rounded
intermediate zeta endpoints are retained with an explicit diagnostic
tolerance; event values are not clipped or discarded. These are implementation
checks, not a proof of the floating probability law.

T36's independently implemented scaled PDE passed all six fixed Radau
refinements, with maximum21-query discrepancy2.282851685464493e-11.
Independent convolution verifies its projection and analytic Jacobian;
three scalar constant profiles provide a separate dynamics check. Five tests
passed. The prescribed deterministic comparator is16-mode loose, one solve
plus all21queries, excluding basis/system setup.

After the root's source clearance, T35's official diagnostics and all63
primary cells completed. The producer retains630000 raw root records in630
ordered checkpoint chunks and separate official diagnostic records. The
maximum three-seed empirical RMS is1.02535398%, so an all-points-below1%
statement would be false. This finite three-seed statistic is not the ideal
ensemble RMS guarantee. T38 independently passed992 checks over all630 primary chunks,18 official
diagnostic archives, reference coefficients, source/gate hashes and all342
protected initial paths. It reproduced the reported errors and independently
evaluated the two analytic baselines. All81 official stream initial states
were reconstructed and final states checked present; full tree RNG draws
were not independently replayed. The auditor initially overrestricted the
zero-redraw count to0/1; all observed counts are0, so this did not change the
result. A separate dtype/nonnegative-count check is being preserved outside
the frozen992-check total. Version1's log error axis cannot show exact zeros;
a separate version2 figure uses a scale that retains them. No simulation is
rerun for this presentation correction.


T38's separate dtype supplement passed648archives,4524 nonnegativeint64
count arrays and648Boolean arrays. It places no upper bound on redraw
counts. Root visually inspected two-barrier-results-v2.png: all panels,
zero-error points, finite horizon labels and expectation-versus-empirical
work labels are visible. The old figures and immutable audit remain intact.

D22 is a new conventional theorem after T40/T41. Root integrated the exact
per-horizon quantifier order, opaque point-value oracle, measurable common
seed/halting interface and explicitT0. It covers biased/adaptive methods,
not just one tree representation, but its hard inputs change withT and its
error is absolute solutionMSE. T42/T43 formalize actual information-integral
and finite transcript arguments, not merely the final exponential algebra.
Both builds passed, and root read the actual source, integral hypotheses
and evaluator induction against05g, then verified source/build/axiom hashes.
The protected toolchain is actually Lean4.33.0; no toolchain file was changed.
No formal PDE/heat/bump or publication-priority certificate follows.
The root correspondence record also rechecked all342 protected paths with
zero mismatches. See06g/06h and reviews/T42-T43-root-correspondence.json.


D23 is now separately accepted after T44/T45. Root read both proofs and
integrated the epsilon dependence and strictly positive C^s norm radius
into04p. Its zero baseline is fixed, but the uniform-error class is
nonnegative and includes zero; D22's sign-changing class is not silently
changed. General C^2 reaction constants depend on the reaction, not only
its unstable derivative. There is no numerical or end-to-end Lean claim
for this corollary. T46/T48 now independently pass the matching Allen-Cahn upper complexity;
root read both proofs and their explicit constants, and integrated D24/04q.
The matched class and absolute-error criterion agree with D23; no
optimality on the sign-changing class or the C2 extension is inferred.
The upper algorithm is biased, has deterministic query count, and uses
no free mass or evolved-value oracle. New05h fixes actual scalar/integral
and independent sample-variance Lean targets before numerical D24 work.


T49's source was fully read against frozen02e/T47 before execution. Its
policy receives only an oracle callable and public baseline/permutation/cap;
hidden labels belong only to the driver. It computes actual traces/outputs
and Fraction losses before comparing formulas; mixtures reuse executed
endpoint aggregates. Pre-freeze source review required immediate persistence
of each completed block and fresh scalar failure context. The final source
c856a9ba2548a6486d756af0b628396e8ab3d9186413e13e906fc57cd795930d
passed the single official run in11.33197475s. All334020runs and four
prescribed scalar rows passed. Root's separate output audit verifies exact
risk summaries and stored scalar formulas, all12input/4output hashes and
342initial hashes, without claiming a full evaluator/quadrature replay.
See reviews/T49-root-source-clearance.json and T49-root-output-audit.json.
No D24 upper-algorithm experiment has been run.


D25/04r is now conventionally accepted after the frozen T50/T53 chain.
Root read both complete proofs. The exact signed class and unit-torus scale
are retained; the stronger exponent is a prior-average/worst-input result,
not the older common-baseline quantifier. Mean drift is bounded by the cubic
remainder, and the adaptive sign information is a without-replacement urn,
with random stopping handled by explicit truncation. d=4s has its separate
amplitude choice; d>4s remains unproved. No existing no-hit Lean result or
finite-model E3 check is described as certifying this distinct KL argument.


Root read the complete T51 source against05h and verified all ten authored
exports in the axiom harness, fresh3396-job build/source hashes and the
342protected paths. Its scalar anchor, range-derived integrability, actual
integral inequality and actual Cauchy bias composition satisfy the contract.
Root did not repeat the already passed build. Record:T51-root-correspondence.json.
T52 still owes the joined independent-sample certificate.

Root also read complete R01/T54. D26/04s incorporates rational per-horizon
scale advice and a tighter rational table; the draft remains immutable.
The repaired scalar error budget is epsilon/6 for scaling plus epsilon/6
for the table, alongside epsilon/3 each for PDE bias and sampling RMS.
Exact real sampling/value queries remain idealized. No T51/T52 result is
presented as a general-C2 or full PDE Lean proof; no novelty follows.


T52 root correspondence PASS: root read the full383-line final source and
all15 authored exports, actual Pairwise IndepFun hypotheses and variance_sum
proof, the zero-mean branch and real-power cancellation. Exact final source,
report, build and axiom hashes agree; all342protected inputs still match.
No root rebuild was needed after the recorded fresh3457-job build. The final
risk theorem includes the deterministic PDE bias explicitly as a hypothesis.
Both05h gates are complete, not an end-to-end PDE formalization. See
reviews/T52-root-correspondence.json. Numerical protocol design may proceed.


T55's frozen primary-literature audit was fully read by root. Root also
opened the primary1805.08637v2 and1907.06729 PDFs; fixed-T MLP quantifiers
and costs cannot be substituted for a sharp large-T initial-query theorem.
The accepted claims retain their scope, with direct credit for classical
information arguments. A bounded negative search is not originality proof.

T57 completed by root after the worker-credit interruption: all28 old
canvas constants are verbatim,29local links exist, all unfavorable prior
baselines remain, and new E3 counts match frozen outputs. TypeScript6.0.3
reports zero diagnostics; esbuild-wasm0.25.9 produced the64473-byte bundle.
The preserved failed compiler-path attempt and first root JSX-escaping
attempt are not hidden. No scientific data were generated or modified,
and a queued file-open is not visual-render evidence. See T57 report.


T59 root correspondence checkpoint: read independent T58/T59/T60 audits
fully, verified their published hashes and protected342 originals, then
accepted04t/D27 with exactly the signed d<=4s query-model scope. Record:
reviews/T59-root-correspondence.json. R03's direct equal-mass counterexample
also passes. R04 is explicitly conditional and assigned as T61; no general
dimension theorem is promoted. T58 clarifications were incorporated into
new frozen02g, preserving02f: exact/computed references, PRNG scope, fixed
precision/summation/streams/diagnostics, whole-activity cap and subset replay.
T63 receives implementation/preflight clearance only. T60's actual Mathlib
API gaps led to05i/T62; a Bernoulli gate alone will not count as full D25.


Current checkpoint, 2026-09-29 local date: root read final T64 and accepted
D28/04u, extending the signed expected-query LOWER to every fixed integers
d,s>=1. The upper of D27 still requires d<=4s. R07 is frozen as a candidate;
T65 develops its actual all-order stable-graph derivative measures and
finite-query construction before a separate independent audit.

T63v2 full changed-source/evidence review passed. Root preserved the v1
HOLD and both655633-call preflights, verified science/RNG parity and all342
initial hashes, wrote a hash-bound clearance, and executed exactly one
official02g run. It completed180cells/18720outputs/336883488queries. T66
now owns independent raw/statistical audit and only the fixed rep0-of-all-
180cells replay (30075636calls). Source and official data are frozen;
no selective rerun, full replay or free formula access is authorized.
The total after that subset will be368270390calls including bothpreflights.
T62 remains active on05i; no signed Lean theorem is yet certified.


R08 records a bounded four-query primary-literature check and a concrete
arithmetic gap: one valid full fine-coefficient-table realization can cost
exp(2dT) despite its much smaller unknown-input query count. This is not a
universal work lower bound. Near-query-order computation of the known
base phase and direct derivative sampling are separate unresolved gates.
R09 completes the D28-only managed canvas update: all47prior constants
verbatim,33validlinks,TypeScript6.0.3zeroerrors,esbuildexit0. NewSHA
b1280e8dab63ae9cd908b8b6dc20eb07fa706c439b5400ff06fa9dc0abc584ed.
Open returnedqueued; no GUI render claim. T62 reports actual Bernoulli KL
formula and chi-square lift compile; remaining endpoint-aware Pinsker and
testing exports still prevent a PASS. T65/T66 remain active.


Current checkpoint: T65frozenSHA58e862c9cfbaf0946605d30d9c8e8a37e2570c0c0719d626683f22db60fc9f81,
rootread1003lines; independentT67active. NoD29yet. T66independentE4audit
completed with180subsetreplays bitwise,30075636replaycalls,total368270390.
Rootread928auditorlines, verified559inputs/11outputs/342protectedfiles,
recomputed180/60/36statisticrows and inspectedfinalPNG. Data/statistics
accepted; exact final layout recipe still needs a standalone archive.
R10now derives a fixed-burnin actual derivative tuple sampler with≤jpaid
residualqueries, controlled secondmoment and fixed-Lexpectedprimitivework.
It does not solve stablegraphsampling or e^-Tbasevalue computation; T68
independent auditactive. T62fixed05i remains active, nofullPASSyet.


Root acceptance of T62/T67/T68 (2026-09-29 local date):
Full final audit/source reviews completed. See reviews/T62-root-correspondence.json,
reviews/T67-root-correspondence.json and reviews/T68-root-correspondence.json.
D29 is the conventional all-fixed-dimension matching signed query theorem;
D30 is only the ideal fixed-time derivative sampler. T62 proves actual
Bernoulli information ingredients, not an assumed-KL abstraction and not the
remaining adaptive urn chain. All17formal manifest entries and14public
standard-axiom records checked; all342protected files unchanged. Root authored
R10 and contributedR07, so T68/T67 respectively supply independent reviews.

T66figure recipe and T71canvas root correspondence now PASS. ExactfinalPNG
reproduced byte-for-byte, allfrozeninputs unchanged and zerooraclecalls.
Canvas embeds exactacceptedE4projections, retainsallbaselines and olddata,
and separates D29query complexity from unproved work. SeeT66-figure-root
andT71-root correspondence records for hashes/checks and one corrected
rootworking-directory check failure. NoGUIrender is asserted.


D31 root correspondence: complete frozen T69 and independent T73 read; exact coefficient law, both time directions, tilted moment, small-RMS independent batches, all-label-map composition, every-path query cap and actual g-cost work match. No repair required. See reviews/T73-root-correspondence.json. Gate A/combined work are still pending T74. Fixed05k/T75 target actual finite-depth kernel moments only, not an infinite-tree/PDE certificate. All342 protected hashes match; zero added oracle calls.


T72/05j root PASS: complete276-line final source, contract and report read. Source endpoints and zero history masses retained; actual density/conditional averaging/chain and arbitrary measurable Bool postprocessing agree. All16 manifest entries and10public axiom records verified, fresh3511-jobbuild inspected, all342protected paths unchanged. Root did not redundantly rebuild. Failure evidence consists of retrospective diagnostic summaries; successful output logs are transcriptions of actual commands, not tee captures. No full signed lower certificate is inferred.


D32/D33 root PASS: full T70/T74 source/audit reviewed and bound to T69/T73, R12 and D28 in reviews/T74-root-correspondence.json. C1-C4 are retained explicitly. Both gates use the same exact saved Gevrey interpolant; elementary evaluations and continuous random draws are separately counted. Taylor risk, hard acquisition cap and Work>=Q yield04w. No bit/practical/fullLean/numerical/novelty or weaker-diffusion conclusion is inferred.


D34/T76 root correspondence: complete 205-line R14b and524-line independent audit read; source hashes and342 initial protected files checked. Both signed comparisons, actual PDE regularity, h=0, root rate/buffer and public bisection match. The result assumes an actual decaying trajectory and certified finite mean evaluation; no graph construction or new full complexity class is accepted from this local lemma. R14c separately proposes those graph/burn-in interfaces and awaits audit. See reviews/T76-root-correspondence.json.


D35/D36 root correspondence: full255-line R14c,210-line R14d,565-line T78,
744-line independent T79 and482-line independent T80 read. The common actual
heat/graph definitions, stronger R14c radii, fixed burn-in, mixed L1 chain
rule and rescaling Atilde=exp(-L)H match. T78/T80 discharge R14d's named
conditional premise; the unconditioned full-prior lower follows on the
same signed input class for every fixed lambda1>1. Source hashes and all342
protected files were checked. Record: reviews/T79-T80-root-correspondence.json;
synthesis:04x-natural-gap-graph-and-signed-lower.md. No changed-kappa matching
upper, lambda1<=1 theorem, full Lean or numerical extension follows here.

T82 all-positive-diffusivity candidate has now been fully read by root and
dispatched to independent T83. Its time-one mean correction and full-profile
concentration avoid the stable graph assumptions. This is a candidate review
step, not an accepted extension. T75 final actual-kernel evidence and T81
upper remain pending. E4 total stays368270390calls.


T75 fixed05k root PASS: full645-line source,144-line contract,162-line report,
all123declaration-output lines, both harnesses and27standard-axiom records
read. All14manifesthashes and342protectedpaths match. Root additionally
ran a fresh exact-source elaboration with autoImplicit=false (exit0,39.607s)
and reran both imported audit harnesses; direct captured axiom/declaration
logs match stored worker logs byte-for-byte. Failed-attempt summary and
worker capture limitations remain explicit in T75-root-correspondence.json.
Only finite-depth actual moment laws are accepted; no infinite-tree or
fullsigned PDE/runtime proof is inferred. Zero added numerical calls.


D37--D39 root acceptance (2026-09-29): complete T81(857), T82(698),
T83(591), T84(884) read, frozen SHA256 values rechecked, and all342
initial protected files unchanged. Same actual flow, signed class, initial
point-value oracle, fixed positive diffusivity and fixed d,s align.
T84 Section10a explicitly proves the spatial supremum inside expectation
and polynomial-size Fourier output; evaluation transfers D37 to the profile
problem. Work includes queries, so both complexity lower bounds apply.
04y SHA256 2a62aaec24cb762ebe8ef213ce7bbbb2dbd56e3b7ced197a851736db913d9ba8;
root record SHA256 32324f4040d90da451def37559513a8c5642018691c8f0ba50b46e9cd6e92db5.
Only exponential-rate matching is promoted, not exact Theta queries/work
for all kappa, vanishing-diffusion uniformity, finite-bit complexity,
simultaneous all-time pathwise control, full Lean, numerical performance
or novelty. This checkpoint adds zero unknown-input acquisitions.


R19 v5 evidence presentation review complete: source hashes and full semantic diff checked; D37-D39 and T75 now visible, D33/older limits/data retained. See reviews/R19-canvas-v5-root-correspondence.json and artifacts/evidence-canvas-signed-v5/ for exact candidate, direct check outputs, and deployment record. R18 literature distinction remains a priority assessment, not proof of originality. T87 entire frozen candidate root-read and dispatched to independent T90; no accepted ledger promotion yet. Fixed05m statistical Lean contract does not include Gaussian/tree/PDE/solver bridges; T89 active after successful worker reuse.


T75 late worker provenance clarification (2026-09-29): the worker reports that build.log, axioms.log and declarations.log were direct stdout+stderr shell redirections; failed-build-autoImplicit.log was copied byte-for-byte from the first failed full library build. failed-attempts.md is a retrospective summary and not every incremental failed direct-Lean stream was retained. This supplements, and does not rewrite, frozen T75-root-correspondence.json, whose wording correctly records that capture was not clarified at that acceptance time. Root fresh source/import checks remain independently directly captured and byte-agree on public audit output. No formal claim or source hash changed.


2026-09-29 sharp-query acceptance: D40-D42 now recorded in04z after frozenT87 (acd788e6ee5564778cd0663be99aab17fb61f22bdfb4b345ccade008f18feff1), full814-line T90 (f8959804af651f78b1a48ee6f9d96139aa397388fba88167f6e30daa5804a907), root same-class/risk/cost review and342 protected hashes. All fixed positive diffusivities now have exactTheta point/profile query order; paidwork still exp(gamma T)polyT. No new numerical acquisition or complete formal claim. R21 proposes O(n) actual Gaussian preparation via classical inverse-variance tree recursion, frozen at99f8a23c98332b6797ee1ecc9f0929d94950cd047acb17bcbea0df9052ff7461; this andR20 remain unaudited, not premises ofD40-D42. T91 fresh/reuse dispatch failed at thread limit. T86 adding contract endpoint/singleton exports before freeze; T89 actualHilbert formal proof active. Canvasv5 displays acceptedD37-D39/T75, and has not yet been refreshed forD40-D42.


T86 fixed05l root accepted: source d50bd7145685480ab802270d4a5eae623205b373b70c1158b30cdbef50fd80fe,658lines,28public declarations,14manifest entries. Worker fresh3403-jobbuild and root autoImplicit=false directsourcecheck (62.97s) pass; root axioms/types direct captures match worker bodies. Failed-attempt list remains retrospective. Full adaptive/nstep/stopping/PDE excluded. T91 reuse succeeded after this worker completed and audits R20+explicit R20b repairs (6c5e8b158ca269588c4200ca09c82f4ffa430e8aa0146a52022370ade352e527) andR21; no acceptance yet. T92 now packages D40-D42/T86 canvasv6; T89 HilbertRisk still active. Zero new numerical calls.


### T91 fixed-time polynomial and linear-Gaussian acceptance

Root read all736 lines of final independent T91 and checked the ten displayed derivations. Six frozen source hashes and all342 protected initial hashes match. R20 alone has two recorded defects; R20 plus final R20b passes, and R21 passes without repair. D43/D44 synthesis and root machine record are04aa and reviews/T91-root-correspondence.json. The new result concerns fixed-time sampling and conditional tree preparation only; the classical voting and Gaussian-tree recursions are attributed, generalized long-time complexity and practical speed remain excluded. T93 implements fixed05n after conventional argument and this acceptance, while T94 studies a separate long-time odd-power extension. No numerical execution.


T92 canvas v6 deployed at SHA ecb20ba4106227f902ce40c1eb098fd72a6c29fb9740e3be5a473ddd8644675a after complete semantic review and two separately archived root wording repairs (explicit continuous g/e; replace stale candidate status by frozen dependency statement). Frozen worker candidate remains a35be1ea0d6c6357cae2b1176df538e31fd61b5012c0f9e77ad0a947226f5b73. Root verified22 manifest entries, all82 old constants,68 old link occurrences,63 old paths,5 charts and all E4 data; exact new candidate TypeScript0 diagnostics, bundle/parity pass. Managed hash-guarded copy approved, open queued, no GUI claim. T89 source complete pending root acceptance; T95 explicitly spawned gpt-6-astra/max for fixed-time fractional-diffusion sampler feasibility, separate from T94 odd-power long-time extension. No new numerical acquisition.


T89 fixed05m root accepted at reviews/T89-root-correspondence.json (SHA3617d62fe22eea254dcd74c46df77b008d90a7b3a9839b1f215c4624c8b87503). Frozen662-line source SHA0cef39d33c11dd113b1ee2d60059485b214fd7ffd9e4fbe68e21709de2b2487c,41theorems and5definitions. All46 public declarations have only standard axioms; root fresh source autoImplicit=false check took77.04s; direct types match worker and all21manifest entries pass. Actual finite Hilbert statistical bridge only; PDE/Fourier/tree law remains separate. E5 fixed02h protocol frozen SHA1866585a86fcfceb0f9b05f632dae093d3c6e03f4ab005b4eae02fbfa5b27612, no implementation/run. It specifies12cells with analytic PDE derivative references, actual D44 Gaussian sampler,4096samples/seed/cell, shared cutoff prefixes and averaging sizes, frozen300000-call all-activity cap, explicit abort rather than biased truncation. Needs T93 and independent protocol check before code execution. Full long-T signed PDE experiment still separate. A message to the completed T89 worker hit the agent-thread limit after acceptance; it does not block active research or change proof status.


T93 fixed05n root accepted:447-line GaussianCommonComponent.lean SHA68d4cb7a1c04720703f819d52ae2ea0667c3e7f0afd4e918506d1b3497defc19,47public declarations,22manifest entries and all342 protected hashes verified. Fresh worker3648-jobbuild plus root direct source autoImplicit=false (85.52s), public signatures and all axioms pass; root import output byte-matches worker. Actual independent-edge Gaussian covariance, whole-vector residual/common independence, degenerate scalar/product/reconstruction laws and integrable bounded-continuous expectations are covered. Tree recursion, heat/PDE/derivative and total algorithm remain outside. Record reviews/T93-root-correspondence.json SHAab7aa78b0f4bb898ed01fcebf50aa8e418592d8b6847cca66a62cf74e04d40d8. T98 independently audits fixed E5 protocol; still no E5 implementation/execution or new acquisition.


D45/D46 root accepted in04ab (SHAa8bd72ec33c69aae4d50126c72f6fd75ac4e1625cb08cfcef6a1b310918d18c0) after frozenT94 and T96 (944lines, SHAb8f5f32be92c820bd8b955c5969406a49fa21e12a1b38c86d17bb7467ba1eda4), full mathematical content review,13source locks and342protected checks. No mathematical repair,11audit prose joins corrected before freeze. Same-class odd-power exactThetaqueries/strongRMS and paidwork exponent pass; physical transfer explicitly rescales class/tolerance and retains time factor a, with zero-query counterexample to the unscaled claim. Record reviews/T96-root-correspondence.json SHAe5ce79241a307089106d20135eedbbb77a13b121b10c727b152e3e0dc185cf0c. T100 now independently audits frozenR23 sparse-frequency subroutine; T97/T98 remain active. No new input acquisition or full Lean/numerical claim.


D47 accepted in04ac SHA3330cccbe4fd4f666569b1f94401a7d8308d3a2ec5302f02616fd188c253ae3d after complete773-line T95 and736-line T97, nine locked hashes and342 protected checks. Actual fractional fixed-time derivative field, explicit stable primitive sampler and linear Gaussian passes pass; sharper inverse moment retains q>=1, Gaussian independence remains conditional on complete clocked tree, finite-output risk centered at projected mean. Root record reviews/T97-root-correspondence.json SHA4699d716473c6f384307a5a153343f79c6a17a6c16062b720bfb0df33a2453e5. T101 research worker now develops a separate paid fractional known-profile solver/long-time upper; root investigates lower transfer. Neither gate accepted yet. T98 E5 protocol andT100 sparse-mode audit remain active; no new numerical acquisition.


D48/T98 root correspondence: all five sparse-source locks and nine E5/proof-prerequisite locks verified;342 protected originals unchanged. Root accepts the complete R23/T100 actual-law, Bochner-risk and finite-work argument including strict variance counterexample; no numerical/fullLean claim. Root accepts frozen02h after all761linesT98, exact references/scaling/factorials/signs, fixed streams/counters and abort policy. Scheduled replay bound480 is tighter than valid864cap. Nested batch monotonicity is Jensen, not statistical confirmation; six reference means miss cross-leaf covariance errors. T99 must freeze source/environment and pass independent deterministic covariance/corner/sign fixtures before root clears official execution.


D49 conventional composition accepted — Root fully read all four final upper/lower/audit texts and checked the shared actual PDE, original signed class, RMS convention, hard-cap upper versus expected-query lower, paid solver, and nonuniform parameter boundaries. Twelve union locks and342protected hashes pass. Record reviews/T103-T104-root-correspondence.json. Complete fractional PDE/algorithm Lean coverage remains pending; no sampled result or solver code has been inferred from this theorem.
