# T58: independent positive-sampling protocol audit

Date: 2026-09-28. Scope: theory and protocol review only. The reviewed
02f draft is unchanged. No sampler, diagnostic, experiment, PDE solver,
or Lean build was run by this reviewer; this is the only T58 file.

**Verdict: GO to a revised, frozen implementation/preflight protocol,
with the two reporting clarifications below. This is not clearance for
official execution.** The conventional threshold, fixed input class,
stored-width mass formula, schedules and total query count pass. No
mathematical obstruction to the proposed finite-family experiment was
found. Numerical choices must still be frozen and checked before the
official data, followed by the root source/preflight review required by
02f. The exact iid-real theorem is not a theorem about the proposed
finite-precision PRNG implementation.

The principal estimates and counts below were checked independently
before consulting R02. R02's analogous self-check agrees with them; it
was not substituted for an independent calculation.

## 1. Conventional constants and horizon threshold: PASS

For d=s=1, the reproducing kernel on [-1/2,1/2] is K=1, so B=1.
The Lipschitz remainder used in04q gives, for 0<h<=1 and m=integral v,

    ||v||_infinity <= m/h + h/2.

Since m<=1/2, choosing h=sqrt(m) when m>0 proves
||v||_infinity<=(3/2)*sqrt(m). At m=0, nonnegativity and continuity
give v=0. Thus C=3/2 and beta=1/2 are valid for the entire stated
class, not just the selected bumps. The constant need not be optimal.

For eta=1/64, L=max(1,log512/(2*pi^2))=1. For example, pi>3 and
e>2 imply log512<9<18<2*pi^2. The draft's list of elementary constants
should include this lower bound on pi if presented as exhaustive.

The three entries in04q's small-mass cutoff become

    1/2,
    1/[72*(e^2-1)],
    8/(65*e).

Each is greater than1/504, using e^2<8 and e<3. Also

    kappa^2 = exp(-1/4)/(2*pi) > (3/4)/8 =3/32>1/16,

where exp(-1/4)>1-1/4 and pi<4. Hence kappa>1/4 and

    kappa*m0*sqrt(eta)>1/(4*504*8)=1/16128,
    T*<1+log16128<12.

For the final inequality, e>8/3 and (8/3)^11>16128 suffice. The
lower bound e>8/3 follows from the first five exponential-series terms,
whose sum is65/24. Consequently all three proposed horizons12,16,20
satisfy the conventional uniform PDE-bias theorem. The numerical E3
lower-bound T0 is irrelevant to this calculation.

The formal sample budget specializes to

    n>=64*C*exp((1-beta)*T)=96*exp(T/2).

Thus theorem_96 is the only proposed schedule satisfying that
class-uniform certificate. For the ideal iid-real algorithm its
transformed-surrogate MSE is at most1/64, and its actual PDE RMS is at
most5/32 after the conventional1/32 bias bound. The three smaller
growing constants and fixed_51 are empirical comparisons.

## 2. Fixed profile class, periodic wrap and stored widths: PASS

Write t=1/[r(1-r)]>=4 on0<r<1. Then

    psi(r)=exp(-t),
    |psi'(r)|=t^2*exp(-t)*|1-2r|
             <=t^2*exp(-t)<=16*exp(-4).

The last inequality follows because t^2*exp(-t) decreases for t>=4.
The usual zero extension of this bump is smooth and flat at both
endpoints. For every stored real width0<h<1,

    v(x)=a*h*psi(((x-17/20) mod1)/h), a=1/8,
    ||v||_infinity<=a*h*exp(-4)<1/2,
    ||v'||_infinity<=a*16*exp(-4)<1.

The h from differentiating the amplitude cancels the1/h from the
argument. Higher derivatives need not remain bounded as h shrinks;
that is permitted by the fixed C1 class. The periodic seam at the
shift is smooth because the bump is flat at its support endpoints.
Wrapping through x=0 also preserves smoothness and mass. Zero is a
separate smooth member; its implementation must still receive every
scheduled oracle query.

The draft's width upper bound is valid for the ideal construction:
on[1/3,2/3], psi>=exp(-9/2), so I>exp(-9/2)/3. At T>=12,z<=4 this
gives h^2<96*exp(-15/2)<1. When the manifest is constructed, assert
0<h<1 directly for every stored nonzero binary64 width. Class
membership then holds for that exact stored real number irrespective
of its tiny deviation from the nominal construction.

The largest intended case, T=12,z=4, does wrap past1 from shift17/20.
This can also be checked analytically: writing w=r-1/2 gives
1/[r(1-r)]>=4+16w^2, hence I<=exp(-4)*sqrt(pi)/4. Using
sqrt(pi)<16/9 and e^2<15/2 yields for this ideal width

    h^2>72*exp(-8)>1152/50625>9/400.

Thus h>3/20. For example, pi<22/7 proves sqrt(pi)<16/9, while
summing exp(1) through degree4 and bounding the remaining terms by a
geometric series gives e<65/24+1/100=1631/600 and hence e^2<15/2.
These stronger constants are only an independent wrap check, not new
prerequisites for the horizon theorem. Preflight
must confirm h>3/20 for the stored widest case and exercise values on
both sides of the periodic boundary.

For every exact stored h, translation and change of variables give

    m_h=a*h^2*I,
    z_h=exp(T)*m_h,
    r_h=Psi(z_h).

These identities include wrapped support. The reference must use m_h,
not nominal z*exp(-T). Record nominal z and the computed z_h separately.
The exact rational shift17/20 and its binary64 implementation value
must also remain distinguishable; a translated ideal profile has the
same mass, but floating remainder/evaluation is still an approximation.

The inspected E3 record contains the declared80-digit primary I and
100-digit Gauss–Legendre cross-check, with `rigorous_enclosure=false`.
Use those frozen strings without rerunning quadrature. In implementation
language, the width is computed from the frozen numerical approximation
I_ref, then rounded and stored. Do not imply that an uncertified
quadrature proved correctly rounded binary64 evaluation of a formula
containing the exact integral I. This does not affect the class argument
based on the final stored h.

## 3. Surrogate and empirical PDE RMS interpretation: PASS with wording repair

For any finite list of real outputs y_j, let

    R(r) = sqrt(mean_j (y_j-r)^2),
    u_x = S_T v_h(x).

The conventional theorem gives |u_x-r_h|<=1/32 for every x. The finite
Euclidean triangle inequality therefore proves

    |R(u_x)-R(r_h)|<=1/32.

This is valid for arbitrary outputs, including the real numbers
represented by stored binary64 outputs. It does not require the
outputs to be independent, unbiased, or numerically exact evaluations
of the ideal algorithm. In particular, oracle roundoff does not itself
require an extra term in this deterministic comparison. It does matter
when relating the implemented sampler's expectation to the ideal iid
risk theorem.

**Required clarification R1.** Distinguish the exact r_h from its
computed reference r_hat and a computed statistic R_tilde. If one has
certified bounds |r_hat-r_h|<=delta_ref and
|R_tilde-R(r_hat)|<=delta_stat, the certified interval would use

    max(0,R_tilde-1/32-delta_ref-delta_stat),
    R_tilde+1/32+delta_ref+delta_stat.

No such numerical certification is presently supplied. Thus replace
“exact scalar surrogate statistic” in implementation-facing prose by
“computed scalar-surrogate statistic,” and label the displayed
plus/minus1/32 interval a numerically evaluated interpretation of the
conventional bias theorem. The draft already disclaims a floating-point
certificate; preserve that qualification in tables, plots and summaries.
The experiment does not measure actual PDE error by an independent
solution, nor establish a time-discretization convergence result.

The comparison is uniform in x, so a PDE solve at a selected x is not
needed to report this interpretation. If a report names a particular
actual PDE target, identify its x, or state that the same conventional
comparison applies separately at every fixed point.

## 4. Opaque oracle, random streams and baselines

The proposed estimator interface is appropriate. It may receive only
the callable, public T, public n and its RNG, and it must call the
oracle for each generated point. The driver may construct the known
family and references, but must not pass width, mass, shift, nominal z,
support metadata, or profile-dependent stopping advice to the sampler.
Source review must check actual information use, not merely parameter
names. The fixed schedules make n independent of all such hidden data.

Conditional support sampling, binomial replacement of actual point
draws, zero-observation early exits, and reuse of another schedule's
queries would change the intended experiment. Repeated points and all
zero-input observations are still charged individually. Positive-return
count is exactly the count of observed values>0, not the number of
points in the mathematical support. Underflow can distinguish these
events, and a zero final output need not mean no positive return.

**Required clarification R2.** A fixed PCG64 seed yields a deterministic
pseudorandom sequence on a finite floating grid. Replace a literal claim
of “iid uniform binary64 points” with “binary64 uniform samples from
separate PCG64 streams, used as a numerical approximation to iid uniform
real sampling.” Distinct SeedSequence keys specify separate streams;
they are not a proof of probabilistic independence or exact continuous
uniformity. The T51/T52 theorem uses actual independent real random
variables with the specified integrals. No machine correspondence to
those hypotheses is being certified here.

The three public seed roots and a distinct tuple for every
(horizon index, level index, schedule index, replicate index) provide
a suitable reproducible stream design. Freeze the complete tuple and
index origin before preflight, including the handling of the three
different root entropies. No extra draws for diagnostics should advance
an official estimator stream. Accidental repeated coordinates are
permitted and charged; intended stream/query reuse is excluded.

Constants0,1/2,1 are valid zero-query baselines for the opaque class.
Their errors are deterministic on each input, not stochastic replicate
uncertainty. Include all three even where they perform well. A
formula-aware scalar reference is part of experiment assessment, not an
admissible class-wide zero-query solver. The repeated seed labels do
not create independent evidence for these constant outputs.

## 5. Exact official counts and resource caps: PASS

The schedule integers are:

| T | growing_0p125 | growing_0p5 | growing_2 | theorem_96 | fixed_51 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 12 | 51 | 202 | 807 | 38730 | 51 |
| 16 | 373 | 1491 | 5962 | 286172 | 51 |
| 20 | 2754 | 11014 | 44053 | 2114541 | 51 |

There are3*3*4*5=180 seed/horizon/level/schedule cells. For one
seed/horizon/level combination, the output count is4*128+8=520;
therefore3*3*4*520=18720 stochastic outputs. The constant baselines
are separate zero-query results and are not included in that number.

For one seed and one level, the sums of scheduled queries are

    T12:128*(51+202+807+51)+8*38730       =452048,
    T16:128*(373+1491+5962+51)+8*286172  =3297632,
    T20:128*(2754+11014+44053+51)+8*2114541=24323944.

Multiplying their sum by3 seeds and4 levels gives exactly
336883488 official point queries. This is a deterministic design count,
not an expected count that fluctuates with hits. The maximum n is
2114541<3000000 and the official total is below500000000, with
163116512 calls of headroom. No actual calls were made in this audit.

Preflight must freeze these integers and independently check them
against the schedule formulas. Account separately for diagnostic or
replay oracle calls; do not hide them in zero-query setup. State whether
the500-million cap covers the official run alone or the whole activity.
If intended as a total resource cap, deduct diagnostic/replay calls too.
Full replay would add another336883488 calls and therefore would not
fit the same500-million total cap. A bounded replay subset does fit if
its size is frozen and charged. The draft correctly does not require
an unreported full replay.

## 6. Material settings to freeze at implementation preflight

These are pending settings, not completed checks. They do not prevent
writing the implementation, but must be explicit before its diagnostic
outputs are assessed and before official execution is cleared:

1. Numerical construction: reference arithmetic precision/library,
   conversion of the stored h from its exact binary ratio or hex,
   width-rounding procedure, exact and implemented shift, exp/Psi
   evaluation and the use of each frozen I string. Record all values
   and distinguish high-precision agreement from rigorous enclosure.
2. Summation and statistics: data/accumulator dtype, exact batch size
   and final partial-batch rule, summation order or compensation, and
   reference/statistic diagnostic tolerances. A sample mean must weight
   every point equally; averaging unequal batch means would be wrong.
3. Randomness and replay: complete SeedSequence key scheme, generator
   and environment versions, per-replicate before/after states, and
   a predetermined small replay subset. Freeze the criterion for
   bitwise equality versus tolerance comparison under that environment.
4. Diagnostics: fixed points, inputs and tolerances for zero, constant,
   wrapped and narrow bump cases, support endpoints, representative
   near-boundary underflow, stable Psi, and a nonconstant replay with
   an unequal final batch. Bound and count diagnostic work separately.
   No tolerance may be increased after a failure without preserving
   that failed version and its evidence.
5. Records and failures: result schema, counter placement at actual
   oracle observations, cell persistence/atomic-write policy, exception
   and partial-replicate records, and interruption/resume rules. A
   technical retry must not silently duplicate or discard observations;
   corrected source requires a new version preserving the old failure.
6. Analysis: exact formulas for empirical signed bias, MSE/RMS,
   zero-output frequency and any displayed variability. Pool squared
   errors, then take a square root; do not average seed RMS values.
   Show all per-seed values and replicate counts, especially the
   theorem schedule's only24 pooled outputs per horizon/level. Any
   uncertainty graphic is descriptive unless separately justified.

The frozen manifest must include the protocol, implementation, formal
sources and root correspondence records,04q/T46/T48, E3 scalar input,
HEAD and environment, plus the above choices. Formal logs need not be
rerun to design this experiment, but their exact frozen evidence must
remain traceable. Root's source and preflight review is still required
before official execution. This is the existing internal quality gate,
not a new user permission request.

## 7. Interpretation, preservation and evidence snapshot

The data can illustrate realized rare-event sampling on this finite,
horizon-dependent family and compare the prescribed budgets. They
cannot validate a supremum over the fixed class, infer an asymptotic
minimax rate from three horizons, or test D25/D26. A large realized
error does not refute an expectation bound. Conversely, all empirical
RMS values below1/4 would not prove that bound. Official completion
means the frozen protocol and accounting succeeded; it is not an
error-based success label. Preserve every case, all zero-query
baselines, failures, and the prior unfavorable E2 solver comparison.

The05h contract and root PASS records were read. Current formal source
hashes match the records below. Their scoped conclusions cover the
actual scalar transform and independent-sample risk derivation; the
PDE bias, interpolation, continuous uniform-oracle realization and
floating arithmetic remain outside that formal correspondence. T58
did not rebuild or independently recertify those modules.

| Reviewed artifact | SHA256 |
| --- | --- |
| 02f-positive-query-sampling-protocol-draft.md | 9f375f3716b11da6fe963a05731d29daccac9c9853cbb473e8c3d3a25ef60691 |
| 05h-positive-upper-bound-lean-contract.md | c0d5f17b0e13dcb131405c8bcfad3ad34b1a9f9b91b79e6902606a6f08a376a9 |
| reviews/T51-root-correspondence.json | c561efa0b1daba5e98fb390aeeef281f0c1e58ed79f6dc95441720ace1fb1711 |
| reviews/T52-root-correspondence.json | 0c61f9bbafa85f83e85b7c26204cc6c7f839f8a54e459fd2dd68906d7bd53502 |
| formal/EstimatorIntegrity/PositiveSigmoidRisk.lean | 3ae1d9acff2ff1f8dae63816b53f7c05eb4f5cd3f562b968d1cb7df168bf9a6d |
| formal/EstimatorIntegrity/PositiveSampleMean.lean | 84cb8468f56f55dbfca243209d64a36164acbdc8625076a7d4ae46f302ca6703 |
| artifacts/query-information/checks-v1/scalar_checks.json | bc2fde87b817e3fea39ee20fca65d9caedb630ef5f52da5d8b7dcafa6c7f0bcb |

Run-local paths in this table are relative to the dynamic-continuation
run; formal paths are relative to the repository. T58 did not modify
T55 or any other existing artifact. The audit's final SHA256 is reported
externally after writing this file.
