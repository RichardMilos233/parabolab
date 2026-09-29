# T47 — independent audit of the query-information check protocol

**PASS for implementation, subject to the protocol's separate source review
and official-run freeze gates.** The finite-model formulas, 105 main
summary rows, scalar identities, and stated scope are consistent. No
mathematical correction is required. The reviewed revision explicitly
reuses endpoint runs for the five budget-mixture rows, pins exhaustive
record counts, and excludes hidden input labels from the evaluator.

This is a design review, not an executed check. No oracle enumeration,
quadrature, scalar numerical evaluation, source implementation, or Lean
build was run for T47. Only this new report is written for this task.

## 1. Audited version and gate evidence

The accepted protocol is `02e-query-information-check-protocol.md`, SHA256
`5e4fe3e20cad7e435142dcf37e343798e730286aa0547cdf7812a8b7a42e33c2`.
Its initial reviewed draft had SHA256
`7bbc4db115ad8dd7509040e5444ff1a103ab716aee7d8fef1569024a87ba18ed`.
After the root added the pre-freeze record-count and evaluator-interface
clarifications, the revised full protocol was reread. Those additions
resolve the initial accounting ambiguity without changing any parameters,
formulas, tolerances, or scientific claims. Acceptance attaches to the
revised `5e4fe3...` version above.

Read gate and source artifacts:

- `05g-query-lower-bound-lean-contract.md`, SHA256
  `7f457eca55cb6f73c84783ba6c10fe6ec448f5b34de0744fd874bac6060acadb`.
- `06g-query-information-lean.md`, SHA256
  `936bd350561c5dae30d29303908049fcb9e000b3c9ecb4402b44345b69a4442e`.
- `06h-oracle-transcript-lean.md`, SHA256
  `50dc5f546febc399407bc8882f37127772436668315a9a1e42b5870cdee78870`.
- `formal/EstimatorIntegrity/QueryInformationLowerBound.lean`, SHA256
  `82422e2894fa5febb586cc6fbb23e73ae3a843d5cd84310c7be3fff38d967483`.
- `formal/EstimatorIntegrity/OracleTranscript.lean`, SHA256
  `997b4af24aeee366a170b6632969431d2bf5fc1e47dc440ecb00ead19d81c53c`.
- `reviews/T42-T43-root-correspondence.json`, SHA256
  `607d603e6ede9cf77f137b228f53d9d7a1d0836c74afdc8b81f4a07a7fb1f95c`.

The Lean source hashes match the source hashes in the root correspondence
record. The reports and record identify Lean `v4.33.0`; the proposed
protocol correctly uses that protected version. This review reads the
statements and existing gate evidence; it does not claim a new build or
axiom audit.

The relevant separation is preserved. T42 proves an actual integral
information inequality on an arbitrary probability space. T43 proves
congruence through a finite adaptive evaluator, together with no-hit and
visited-cell corollaries. The proposed finite enumeration is a restricted
executable example of these ideas. It is not a proof of the arbitrary-space
theorem or a formally checked extraction of the Lean evaluator.

## 2. Exact finite model and exhaustive counts

For fixed `K`, a seed is a permutation `pi` of the cells. The baseline
oracle is the public function `g(i)=i/(K+1)`. On alternative `(j,sigma)`,
the response difference from `g` is zero except at `j`, where it equals
`sigma`. Thus the evaluator can infer the sign from an observed response
after a hit. It need not be given the hidden input label.

The baseline makes exactly `m` queries. An alternative makes
`min(m, position_pi(j))` queries, where positions are numbered `1,...,K`;
the output is `sigma/2` precisely when `position_pi(j)<=m`, otherwise `h`.
At a hit on the last allowed query, the hit output must take precedence
over the miss output. At `m=0`, no oracle call occurs.

For every no-hit alternative, its complete chronological query trace is
the first `m` elements of `pi`, just as on the baseline, and its output
is `h`. The visited-cell count is exactly `m` on the baseline, so the
required inequality against the query count holds. This particular sweep
exercises data-dependent stopping; its next-query order is fixed by the
seed and does not test adaptive changes of location after different
nonterminal responses. That restriction is compatible with the stated
finite-model scope.

The following are hand-derived expected counts, not execution results.
For every `K` there are `5*(K+1)` main summary rows,
`5*K!*(K+1)` seed/cap/miss-output configurations, and
`5*K!*(K+1)*(2K+1)` actual oracle runs if all requested inputs are run.

| K | Main summary rows | Seed/m/h configurations | Baseline + alternative runs | No-hit alternative runs |
| --- | ---: | ---: | ---: | ---: |
| 1 | 10 | 10 | 30 | 10 |
| 2 | 15 | 30 | 150 | 60 |
| 3 | 20 | 120 | 840 | 360 |
| 4 | 25 | 600 | 5,400 | 2,400 |
| 6 | 35 | 25,200 | 327,600 | 151,200 |
| Total | **105** | **25,960** | **334,020** | **154,030** |

The no-hit alternative count for each `K` is

    5*K!*sum_(m=0)^K 2*(K-m)=5*K!*K*(K+1).

There are 25,960 baseline runs and 308,060 alternative runs in the main
sweep. There are also 820 fixed-alternative permutation-average risk
comparisons, since

    sum_K 5*(K+1)*(2K)=820.

These checks may be stored as fields within the 105 primary summary rows;
820 does not replace the prescribed row count. The explicit count of
per-configuration paired-family inequality checks is 25,960.

The budget-mixture block has **five additional summary rows**, one for
each `K`. The accepted revision requires reuse of the already executed
`h=0,m in {0,K}` records and prohibits an additional simulation. The
number of main-sweep endpoint records reused is

    sum_K 2*K!*(2K+1)=19,262,

The total remains **334,020 actual oracle runs**; the mixture adds zero
runs. The manifest should report the 19,262 reused endpoint records.
Combining the 105 sweep rows and five mixture rows produces 110 summaries;
the families should remain distinguishable in machine-readable output.

## 3. Risk formulas and finite-model sharpness

For each fixed seed/cap/output configuration, precisely `m` alternative
cells are detected and incur zero loss for either sign. Each undetected
cell contributes the two losses

    (h-1/2)^2 and (h+1/2)^2.

Their sum is `2*h^2+1/2`. Hence the directly executed alternative-family
mean must agree with

    L=(1-m/K)*(h^2+1/4).

The paired-family lower bound is

    L >= (1/4)*(1-m/K),

with slack `(1-m/K)*h^2`. Equality holds for every row with `h=0`, and
also for `m=K` regardless of `h`. This matches T42 with target separation
one and `gamma=1/2` after division by `2K`.

For fixed `(j,sigma)`, the uniform permutation places `j` beyond the cap
with probability `(K-m)/K`. Its permutation-averaged risk is therefore

    (1-m/K)*(h-sigma/2)^2.

The baseline risk is `h^2`, and its expected cost is `m`. Both should be
computed from actual executions; the equations are independent reference
values for the comparison gate. All quantities are rational. Construct
fractions from integer numerator/denominator pairs, including `g`, `h`,
and weights; avoid an intermediate binary float.

In the mixture block, `h=0`, and the `m=0` branch has probability `1/4`.
It returns zero on every input, giving alternative loss `1/4`. The
`m=K` branch has probability `3/4`, detects every alternative, and has
zero alternative loss. Thus

    E Q(g)=3K/4,
    risk(g)=0,
    risk(f_(j,sigma))=1/16 for every j,sigma.

This attains T42's baseline-cost lower bound on the finite promised class
consisting of `g` and the `2K` alternatives. The protocol's qualified
finite-model sharpness claim is justified. It is not a construction of
a uniformly accurate algorithm on the spatial PDE class.

Most rows of the main `m,h` sweep do not satisfy the `epsilon^2=1/16`
MSE premise. Those rows test the unconditional pointwise loss inequality
and the exact risk formulas; they must not each be reported as an
application of the three-quarters corollary. The mixture block does
satisfy the MSE premise and tests that specialization.

## 4. Scalar block

The derivative certificate is valid. With `r=1/[z*(1-z)]`,

    psi'(z)=(1-2*z)*r^2*exp(-r),
    r>=4,
    |psi'|<=r^2*exp(-r)<=16*exp(-4)<1.

The last monotonicity follows from
`d/dr [r^2*exp(-r)]=r*(2-r)*exp(-r)<=0` for `r>=4`.
Also `psi<=exp(-4)<1`, so `D=1` is the correct certificate for `s=1`.
The usual smooth zero extension is part of the conventional bump
construction; a numerical grid is not being used as its proof.

The protocol specializes 04o correctly:

    a=1/8, q=2, D_s=2*pi,
    kappa=exp(-1/8)/sqrt(2*pi),
    delta=kappa/(128*e*D_s).

For the prescribed `T`, exact algebra gives

    R=k+1/2,
    B=(k+1/2)^2/k^2,
    ell=B/sqrt(1+B^2-c^2),
    background=B/(128*D_s).

The four exact reference values of `B`, in increasing `k`, are
`81/64`, `289/256`, `1089/1024`, and `4225/4096`.
They all lie in `[1,4]`. Since `k+1/2>4`, the selected horizon satisfies
04o's `T0`. Positivity and `c<1` follow from the fixed bump construction.
The scalar bounds consequently give

    ell>=1/sqrt(2),
    background<=1/(32*D_s)<=1/32,
    ell-background>=1/sqrt(2)-1/32>1/2.

The numerical comparisons are correctly framed as checks of formula
implementation. Defining `T` using the same computed `I` makes several
algebraic equalities self-consistency checks; agreement is not independent
evidence for the true spatial PDE. The separate quadrature comparison
checks the numerical integral computation, still without a rigorous
enclosure. The protocol states both limitations.

The quadrature methods, precisions, split point, comparison tolerance,
four `k` values, and identity tolerances are prescribed before results.
No value of `I` was computed in this review, so a successful quadrature
comparison remains an execution gate. Any library defaults or explicit
quadrature options used must be pinned by the implementation source and
version manifest before the official run. Stored 75-digit representations
must not be described as 75 mathematically certified accurate digits.

## 5. Required interpretation at source review and final decision

No mathematical rewrite is needed. The following concrete checks belong
to the protocol's already required implementation review:

1. The evaluator receives an oracle callable, public model parameters,
   cap, seed, and miss output. Hidden `j,sigma` labels are available only
   to the test harness constructing the oracle and target. Detect a hit
   and its sign from the returned exact value, and preserve query order.
2. Distinguish the 105 main rows from the five mixture rows and obey the
   endpoint-reuse rule with zero additional oracle runs. Preserve the
   820 per-alternative checks and the 25,960 pointwise-family checks.
3. Compute outputs, traces, query counts, and losses by the actual
   evaluator. Use closed forms only as reference comparisons afterward.
   Streaming aggregation is permitted, but exhaustive counts and full
   failure context must remain recoverable.
4. Preserve the source-review gate, then hash the accepted protocol,
   this review, listed formal inputs, implementations, and environment
   before the first official run. A revised protocol needs its revised
   hash and any materially changed scope re-reviewed. Preserve failed
   versions rather than overwriting them.

The proposed checks honestly follow the scoped T42/T43 gates. They do
not exercise all measurable algorithms, unbounded random stopping,
general probability spaces, arbitrary adaptive query-location policies,
or the nonlinear PDE. They also do not check T44's repeated-zero
corollary or its C² reaction extension; those are separate statements.
The protocol's existing exclusions prevent finite-model success from
being used as a PDE minimax or novelty claim. **Accept this audited
protocol for implementation; official execution remains behind its
explicit source-review and freeze gates.**
