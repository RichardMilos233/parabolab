# R12: exact composition target for the remaining work gates

Status: conditional proof/interface only. T69 and T70 are still candidates;
none of the required algorithmic hypotheses below is accepted by this note.
D29 remains a query theorem. This note states exactly what would suffice
to improve it to an expected arithmetic-work theorem and prevents the two
workers from discharging different problems under the same terminology.

## Model and fixed analytic inputs

Keep D29's class, unit torus, fixed d,s, fixed burn-in L, near/far branch
test and actual smooth proxy H. Put q=s+d/2, J=ceil(1+d/(2s)), m=J-1.
The deterministic coarse transcript has k^d paid values and defines a
known g with ||v-g||inf<=Cint k^(-s). The analytic Taylor remainder is
at most B_J ||v-g||inf^J/J! and Js>=q.

Work is counted in one explicitly shared ideal real-arithmetic model.
Every unknown-input acquisition costs at least one unit. State which
random draws, elementary function evaluations, integer/index operations
and stored-value accesses are primitives. Arbitrary known-profile function
evaluation is not free unless its actual cost is bounded by the chosen
representation. No finite-bit interpretation is inferred. In particular,
exact continuously distributed query locations are an idealization.

## Gate A: known-base computation

Given only the paid transcript, construct g and a data structure for it,
compute the coarse mean test to its fixed required tolerance, and compute
a deterministic approximation h0 of H(g) satisfying

    |h0-H(g)|<=eta,        eta=exp(-(T-L))/192,

with work at most C k^d (1+T)^a, uniformly over promised transcripts.
The same work bound must include preprocessing, all finite solves, all
root iterations, spectral transforms, quadrature and tolerance choices.
Every later evaluation of the known g in Gate B must cost at most
C(1+T)^b, or its actual aggregate cost must be included explicitly.

Only the near branch needs high-accuracy H(g). A correct fixed-tolerance
mean test and scalar-comparison far branch suffice elsewhere. No free
unknown value or unknown norm is allowed in either branch.

## Gate B: each actual derivative action

For j=1,...,m and e=v-g, with independent fresh randomness conditional
on the fixed coarse transcript, produce Z_j such that

    E Z_j = D^j H(g)[e,...,e],
    E|Z_j|^2 <= V_j ||e||inf^(2j).

The constants V_j are uniform over promised inputs and k,T; they may
depend on fixed d,s,L,j and on a public fixed burn-in batch size.
Require at most j new unknown-input calls on every path, almost-sure
halting, Borel rules, and expected total work at most C_j(1+T)^b.
Count every inner genealogy, averaging batch and known-g evaluation.
All unmarked leaf evaluations must use the saved coarse formula, not v.
If only an expected query bound is obtained, it does not discharge this
hard-cap interface and must be reported as a different result.

## Conditional combination

Take M=k^d independent copies of Z_j for each order, and define

    Hhat=h0+sum_(j=1)^m (1/j!)(1/M)sum_(ell=1)^M Z_(j,ell).

Only independence within each average is needed. Conditional on the
coarse transcript, the mean error of order j has RMS at most
sqrt(V_j)||e||inf^j/sqrt(M). Minkowski and the analytic Taylor remainder
give

    RMS(Hhat-H(v))
      <= eta + sum_(j=1)^m sqrt(V_j) Cint^j k^(-js-d/2)/j!
                + B_J Cint^J k^(-Js)/J!
      <= eta+Cstar k^(-q),

where Cstar is finite and public. Select

    k=max(k0,ceil((32 Cstar exp(T-L))^(1/q))).

Then the scaled proxy error is at most 1/32+1/192, which is below the
3/64 budget already allowed in D29. Its existing multiplier, PDE and
scalar-output budgets therefore still imply RMS<=7/64<1/4. This does
not require bounded derivative samples, only the actual second moments.
An exact or uniformly controlled elementary evaluation of Psi must be
included in the common work model; unbounded samples cannot silently
be assigned a fixed finite-bit encoding cost.

There are at most [1+J(J-1)/2]k^d unknown acquisitions. Linearity of
expected work, a fixed number of orders, and Gate A/B give

    sup_v E Work_T(v) <= C exp(2dT/(2s+d)) (1+T)^c.

As each acquisition costs at least one unit, D28 gives the corresponding
exponential-order work lower bound. This would match the exponential
rate up to a polynomial factor in T; it would not prove an exact Theta
work bound without that factor, a dimension-uniform result, a bit bound,
or a practical speed advantage.

## Acceptance requirements

The two gates must each have a complete frozen proof and an independent
audit, followed by root correspondence in the same primitive model.
T69's possible signed-kernel sampling and T70's possible Gevrey/spectral
computation are not assumptions that can be promoted merely because the
combination above is elementary. A mismatch in input class, query cap,
norm, precision, mean test or primitive cost reopens this interface.
Lean and numerical stages follow a fixed accepted theorem/algorithm;
neither begins from this conditional note alone.
