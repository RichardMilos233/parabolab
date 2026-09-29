# T05 — raw second-moment failure for every common constant rate

Date: 28 September 2026. Status: independent conventional audit accepted.
This note contains proofs, not numerical experiments or Lean declarations.
The constant-rate result concerns the existing raw estimator law. Section 8
defines and analyzes a further deterministic remaining-time-rate law; it
does not claim that this extension is implemented. The finalized T01 note
and all earlier-run files remain unchanged.

## 1. Accepted statements and scope

Fix one terminal function from the new dynamic family,

    v(x)=g(x)R0(g(x)^2),               9/10<=R0<=1,

with sufficient regularity to evaluate the original derivative-coded
terminal observables (in particular the C2-R class in T01 suffices). Let g
be the same periodic Jacobi profile as in T01. Retain the original raw
uniform probability 1/2 for both F-code labels.

**Theorem A: every common constant rate.** For every finite constant
`lambda>0`, every starting position x and every `T>=14`,

    E[H_(Id,T,x)^2] = infinity.

The rate may depend on the requested horizon T: the quantifiers are
`for every T>=14, for every lambda>0`. Choosing a different common constant
rate for each large horizon cannot restore L2 for this terminal family and
this raw label law.

**Theorem B: common deterministic remaining-time rates.** Fix `T>=17` and
any positive continuous function `lambda:[0,T]->(0,infinity)`. Define the
common branch hazard and its likelihood weights as in Section 8. The same
Id-root second moment is infinite for every starting position.

Theorem B permits a different deterministic profile for each horizon, but
does not cover state-dependent, code-dependent, history-adaptive or random
rates. Neither theorem changes or optimizes the tuple probabilities. They
are not impossibility claims for all branching representations, all data,
all importance-sampling laws or short-slab continuation.

The assertions concern the extended nonnegative second moment. They do
not assume that an ordinary variance or an absolutely integrable first
moment exists at these horizons. The tree is still almost surely finite
for each fixed horizon under either rate contract.

## 2. Fixed profile, terminal observables and source checks

Use the notation

    a=2/21,       A0=sqrt(a),       kappa=sqrt(40/21),
    m=1/20,       L=4K(sqrt(m))/kappa,
    g(x)=A0 sn(kappa*x | m).

The K argument uses the modulus convention and sn uses the parameter
convention. The existing analytic profile bounds are

    4<L<5,         ||g||_infinity=A0>3/10,
    ||g'||_infinity=sqrt(80)/21<1/2,
    g^2<=2/21,
    integral_0^L g(y)^2 dy > 1/40.                        (2.1)

The last integral is with respect to ordinary Lebesgue measure, not `dy/L`.

The exact normalized terminal codes are

    (v, v', f(v), f'(v), f''(v), f'''(v)),      f(r)=r-r^3.

This audit checked the raw moment polynomial in
[the prior theory, C3–C4](../../2026-09-27-slab-continuation/04-theory.md),
the raw divergence proof in its C9, and the general terminal-family
extension in [T01, Section 15](T01-order-interface.md). The earlier
independent positive-moment review is
[old T01, Section 10](../../2026-09-27-slab-continuation/reviews/T01-interface-theory.md).

In the coordinate order `(I,D,F0,F1,F2,F3)`, write squared moments as
`M=(i,d,a0,b,c,e)` when displaying the moment polynomial. Then

    G(M) = (a0, bd, 2a0b+d^2c/2, 2a0c+d^2e/2, 2a0e, 0).
                                                               (2.2)

The temporary symbol a0 in (2.2) is a coordinate, not the seed eta below.
The coefficient `2a0e` in the F2 row retains the probability 1/2 of the
active label. Its other label is identically zero but is still drawn by
the raw law. The factor 2 must not be deleted by silently renormalizing
the proposal after excluding that label. Both F3 branch products vanish,
while its terminal observable is the constant -6.

Exact pruning of a selected zero subtree leaves this law unchanged and
is allowed. Changing the proposal by deleting the zero label and
renormalizing the remaining label is outside the stated result.

## 3. The constant-rate nonnegative mild equations

Fix `lambda>0` and let `P_t` be the periodic Brownian heat semigroup with
diffusion coefficient 1/2. Let B_c denote the terminal observable for code
c. First-branch conditioning and independence of the children give

    M_c(t)
      = exp(lambda*t) P_t[B_c^2]
        + (1/lambda) integral_0^t exp(lambda*(t-r))
            P_(t-r)[G_c(M(r))] dr.                       (3.1)

These are nonnegative extended integral identities. They follow by Tonelli
or from monotone finite-tree expansions. No differentiation of an infinite
moment field is performed. If finite classical fields happened to exist,
their equation would have reaction `lambda M+G(M)/lambda`; the proof uses
only (3.1).

Normalize

    Y_c(t,x)=exp(-lambda*t)M_c(t,x).

The F3 row of (2.2) gives exactly `Y_3=36`. Dropping only the nonnegative
derivative-code terms in the F0 and F1 rows leaves

    Y_0(t) >= P_t[f(v)^2]
                + integral_0^t b_lambda(r)P_(t-r)[Y_0(r)Y_1(r)] dr,
    Y_1(t) >= P_t[f'(v)^2]
                + integral_0^t b_lambda(r)P_(t-r)[Y_0(r)Y_2(r)] dr,
    Y_2(t)  = P_t[f''(v)^2]
                + 36 integral_0^t b_lambda(r)P_(t-r)[Y_0(r)] dr,

    b_lambda(r)=(2/lambda)exp(lambda*r).                  (3.2)

The normalized Id identity is

    Y_I(T)=P_T[v^2]
             + (1/lambda) integral_0^T P_(T-r)[Y_0(r)] dr.
                                                               (3.3)

In particular the common reduced coefficient is `(2/lambda)exp(lambda*r)`,
and the root coefficient is `1/lambda`. Both agree with the earlier
rate-two formulas on substituting lambda=2.

## 4. The heat seed has no rate dependence

The magnitude order of the terminal function implies

    |v| >= (9/10)|g|,           v^2 <= g^2 <= 2/21,
    f(v)^2 >= (81/100)(19/21)^2 g^2 >= (16/25)g^2.         (4.1)

The coefficient comparison is strict:
`29241/44100 > 28224/44100`. The function inequality in (4.1) is strict
where g is nonzero, while both sides vanish at its zeros.

At time one, the periodic heat kernel relative to dy contains a Gaussian
image with displacement at most `L/2<5/2`. Consequently

    p_1(x,y)>exp(-4)/3>1/192.                             (4.2)

The final inequality uses `exp(2)<8`. One can also recover the last bound
in (2.1) directly: intervals of radius 1/10 around the positive and
negative peaks have `|g|>1/4`, since the peaks exceed 3/10 and
`|g'|<1/2`. Their total length is 2/5 and they are disjoint.

Keeping the terminal heat contribution in (3.2) yields, uniformly in x,

    Y_0(1,x) >= P_1[f(v)^2](x)
              > (16/25)(1/192)(1/40)
               = eta := 1/12000.                         (4.3)

The normalization cancels the rate-dependent no-branch factor exactly:
the unnormalized no-branch squared moment is
`exp(lambda*t)P_t[B_c^2]`. Therefore (4.3) does not conceal a lambda-dependent
survival probability. This cancellation is essential to the all-rate result.

## 5. A common positive scalar comparison

Restart the exact nonnegative mild equations at t=1 and then discard
their nonnegative derivative contributions. The restart follows from
splitting their integrals and the heat-semigroup law, so it remains valid
for extended moments. The initial F0 field is bounded below by eta and
the other two fields are nonnegative.

Because the heat semigroup preserves constants, compare with the spatially
constant Volterra system whose initial vector is `(eta,0,0)` and whose
common coefficient is b_lambda. This comparison can be carried out one
nonnegative Picard iterate at a time. Every lower iterate is finite on a
compact time interval; monotone passage gives the lower solution before
its scalar blow-up time. Actual moment finiteness is never assumed.

Introduce

    s_lambda(t)=integral_1^t b_lambda(r)dr
               =2[exp(lambda*t)-exp(lambda)]/lambda^2.
                                                               (5.1)

In this time parameter the lower system is the same for every rate:

    A_s=AB,       B_s=AD,       D_s=36A,
    (A,B,D)(0)=(eta,0,0).                                 (5.2)

Here D is merely the name of a scalar comparison component. It is not
the derivative-code moment M_D. Set `Z_s=A`, `Z(0)=0`. Direct integration
of (5.2) gives

    D=36Z,       B=18Z^2,       A=eta+6Z^3,
    Z_s=eta+6Z^3.

Thus its explosion time is

    s_* = integral_0^infinity dZ/(1/12000+6Z^3)
        <= integral_0^(1/30)12000 dZ
             + integral_(1/30)^infinity dZ/(6Z^3)
         = 400+75 = 475.                                 (5.3)

If `t_*` solves `s_lambda(t_*)=s_*`, then
`Y_0(t,x)>=A(s_lambda(t))` for every x and `1<=t<t_*`.
In particular an explicit rate-dependent upper bound is

    t_* <= tau_lambda
         := log[exp(lambda)+(475/2)lambda^2]/lambda.      (5.4)

This is an upper bound on the second-moment obstruction time, not a claim
that the true moment system stays finite before it.

## 6. A uniform constant-rate horizon of fourteen

For lambda>0, subtracting the exponential power series termwise gives

    exp(14lambda)-exp(lambda)
      >= 13lambda+(195/2)lambda^2+(2743/6)lambda^3.         (6.1)

All omitted coefficients are positive. Dividing by lambda^2 and applying
the elementary two-term AM–GM inequality gives

    13/lambda+(2743/6)lambda
      >= 2sqrt(13*2743/6)>140,

because

    13*2743/6=35659/6>4900=70^2.

Together with `195/2+140=475/2`, (6.1) proves

    exp(14lambda)-exp(lambda)>(475/2)lambda^2,
    s_lambda(14)>475>=s_*,
    t_*<=tau_lambda<14.                                  (6.2)

No compactness restriction on lambda is used; the estimate applies to
arbitrarily small positive rates and arbitrarily large finite rates.
The integer fourteen is a conservative analytic threshold, not an
optimized value or a numerical maximization of (5.4).

## 7. The Id root diverges, for every position

Fix `T>=14` and retain only `1<=r<t_*` in (3.3). Positivity, preservation
of constants and the scalar comparison give

    Y_I(T,x) >= (1/lambda) integral_1^(t_*) A(s_lambda(r))dr.

Since `ds_lambda/dr=(2/lambda)exp(lambda*r)`,

    (1/lambda)dr=(1/2)exp(-lambda*r)ds_lambda
                  >= (1/2)exp(-14lambda)ds_lambda

before t_*. The multiplying constant is strictly positive for every fixed
finite lambda, even though it has no positive uniform lower bound over all
rates. Therefore

    Y_I(T,x)
      >= [exp(-14lambda)/2] integral_0^(s_*) A(s)ds
       = [exp(-14lambda)/2] lim_(s->s_*)Z(s)
       = infinity.                                      (7.1)

Multiplication by the finite positive factor `exp(lambda*T)` proves
Theorem A. This transfer through the Id mild integral is indispensable:
an infinite descendant second moment alone would not settle the root.

## 8. Extension to deterministic remaining-time rates

### 8.1 The clock law and its orientation

Fix T and a positive continuous function `lambda:[0,T]->(0,infinity)`.
Let

    Lambda(t)=integral_0^t lambda(r)dr.

For this estimator family, t is the remaining-horizon parameter of the
moment field. A parent with remaining horizon t survives until its child
would have remaining horizon r with probability

    S(t,r)=exp[-(Lambda(t)-Lambda(r))],       0<=r<=t.

Its first-death density at r, relative to dr, is

    rho_t(r)=lambda(r)exp[-(Lambda(t)-Lambda(r))].         (8.1)

In particular its probability of reaching the terminal time is
`exp(-Lambda(t))`. Children use the same deterministic remaining-time
profile, restricted to their smaller remaining horizon. The corresponding
branch and terminal likelihood weights divide by these densities and
survival probabilities, just as in the raw constant-rate representation.
The raw F-label probabilities remain 1/2.

The orientation in (8.1) matters: the rate at death is lambda(r), not
lambda(t), where t was the parent's initial horizon. Simply replacing a
constant by a time-varying number inside the old homogeneous density would
not automatically implement this law.

Continuity and positivity on the compact interval bound the rate above
and away from zero. The resulting finite-horizon branching process is
dominated in node count by a finite-rate ternary birth process, so the
tree is almost surely finite. This observation does not assert a finite
second moment.

### 8.2 Derivation of the nonautonomous moment identity

The squared no-branch contribution is
`exp(Lambda(t))P_t[B_c^2]`. Squared first-branch likelihood weighting
contributes the reciprocal of (8.1). Consequently Tonelli gives directly

    M_c(t)
      = exp(Lambda(t))P_t[B_c^2]
        + integral_0^t exp[Lambda(t)-Lambda(r)]/lambda(r)
              P_(t-r)[G_c(M(r))]dr.                      (8.2)

Thus, when finite classical fields exist, (8.2) has reaction
`lambda(t)M+G(M)/lambda(t)`. Equation (8.2), not that conditional
differential shorthand, is the proof for possibly infinite moments.

Normalize `Y_c(t)=exp(-Lambda(t))M_c(t)`. Again `Y_3=36`, and the reduced
quadratic coefficient and root identity become

    b_lambda(r)=2exp(Lambda(r))/lambda(r),
    Y_I(T)=P_T[v^2]
             + integral_0^T P_(T-r)[Y_0(r)]/lambda(r)dr.   (8.3)

The terminal heat term in the normalized fields is still `P_t[B_c^2]`.
The seed eta=1/12000 from Section 4 therefore remains independent of
the entire rate profile, not merely of its value at time one.

### 8.3 The time change must reach the scalar explosion

Restart at t=1 and apply precisely the positive Picard comparison in
Section 5, now with

    s_lambda(t)=2 integral_1^t exp(Lambda(r))/lambda(r)dr.
                                                               (8.4)

The scalar system and its explosion bound `s_*<=475` are unchanged.
Define `W(t)=exp(-Lambda(t))`. Then

    -W'(t)=lambda(t)exp(-Lambda(t))>0,
    exp(Lambda(t))/lambda(t)=1/[-W'(t)].

Cauchy–Schwarz on `[1,t]` gives

    (t-1)^2
      <= [integral_1^t 1/(-W')][integral_1^t(-W')],
    s_lambda(t)
      >= 2(t-1)^2/[W(1)-W(t)]
       > 2(t-1)^2,                      t>1.             (8.5)

The strict last inequality follows from `0<W(t)<W(1)<=1`, so
`0<W(1)-W(t)<1`. Therefore, for every such profile on `[0,T]` with T>=17,

    s_lambda(17)>2*16^2=512>475>=s_*.

The increasing continuous time change reaches s_* at some `t_*<17`.

### 8.4 Root transfer under the variable profile

From (8.3), the spatially uniform comparison and (8.4),

    Y_I(T,x)
      >= integral_1^(t_*) A(s_lambda(r))/lambda(r)dr
       = (1/2) integral_0^(s_*) exp(-Lambda(r(s)))A(s)ds
      >= [exp(-Lambda(17))/2] integral_0^(s_*) A(s)ds
       = infinity.                                      (8.6)

The factor `exp(-Lambda(17))` is strictly positive for each fixed profile.
Multiplication by `exp(Lambda(T))` proves Theorem B. Again no rate-uniform
positive lower bound on this factor is required to multiply a divergent
nonnegative integral.

## 9. What is established, and what remains outside it

The independent audit accepts both Theorem A and Theorem B. Their main
ingredients are the exactly weighted raw moment law, a rate-independent
normalized heat seed, positive Picard comparison with one scalar blow-up
equation, and transfer of its divergent integral to the Id coordinate.

This strengthens the previous rate-two obstruction in a specific direction:
common constant-rate tuning alone cannot repair the full-horizon raw L2
failure beyond T=14 on this family. Even the explicitly defined common
deterministic remaining-time rate contract fails beyond T=17. Both results
allow the rate choice to depend on the requested horizon.

Still outside the result are code/state/adaptive rate laws, altered tuple
probabilities, other representations, global optimal thresholds and
arbitrary terminal data. Short-slab continuation changes the full-horizon
estimator and is therefore not contradicted by these obstructions.

No numerical experiments, clock implementation changes or formal proofs
were run for this note. Possible later Lean targets are the scalar
Taylor/AM–GM bound in Section 6 and the conditional time-change inequalities;
those algebraic targets alone would not formalize the nonnegative-tree
measure, first-branch identities, heat-kernel bound or Picard/root transfer.
