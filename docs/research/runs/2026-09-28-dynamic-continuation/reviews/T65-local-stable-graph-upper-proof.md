# T65: local stable graph and the signed query upper bound in every fixed dimension

Date: 2026-09-29. This is a new conventional proof candidate, supplied for
independent audit. The sole T65 edit is this file. R07 and the frozen
T56/T59 sources are preserved. No accepted ledger, Lean target, code,
numerical evidence, or canvas is changed.

**Verdict: GO for an all-dimension upper theorem, subject to independent
review of this proof.** For every fixed pair of integers `d,s>=1`, the
same fixed signed class and exact initial-point-value oracle as D27 admit
a randomized algorithm with uniform RMS below `1/4` and deterministic
query cap `C exp(2dT/(2s+d))` for sufficiently large `T`.

The central new obligation is discharged by an explicit Banach space of
measurable signed kernels and a contraction in total variation. It gives
actual finite signed measures on every finite leaf product for every
fixed finite derivative of a local stable graph. No multilinear
operator-to-product-measure identification is assumed. Finite-time
composition, paid branch selection, arbitrary finite Taylor order,
finite coefficient calculation, measurability, and halting are included.

This is an upper theorem only. During this work the root reported that
T61's all-dimension lower proof passed the separate T64 audit; that
lower theorem is not a dependency here. This file does not expand D27's
accepted matching range `d<=4s`: the new upper still requires its own
independent review before any matching synthesis. There is no runtime,
unbiasedness, dimension-uniform, arbitrary-domain, formalization,
numerical-performance, novelty, or award-level claim.

## 1. Exact statement and dependencies

Let `X=(R/Z)^d` with normalized Haar measure `lambda`, and let `P_t` be
the heat semigroup for `Delta/2`. Write `Pi f=integral_X f d lambda`
also for the corresponding constant function, and `Q=I-Pi`. Consider

    u_t=Delta u/2+u-u^3,   u(0)=v,   S_t v=u(t).

For fixed integers `d,s>=1` and a fixed target point `x*`, the input
class is exactly

    F={v in C^infinity(X): ||v||infinity<=1/2,
       max_(|alpha|<=s)||partial^alpha v||infinity<=1,
       min v<0<max v}.

Only an exact returned value `v(y)` can reveal unknown-input information,
and every acquisition is charged, including preprocessing and repeats.
The allowed algorithm may use a public horizon, private fair random
bits, finite calculations on its transcript, and bias. Its transcript
maps must be Borel and it must halt almost surely for every input.
There is no input formula, mass, derivative, phase, or PDE-value oracle.

The assertion is: there are finite public `C,T0`, depending on fixed
`d,s`, and admissible algorithms `Y_T`, for `T>=T0`, such that

    sup_(v in F) (E |Y_T-S_Tv(x*)|^2)^(1/2) < 1/4,
    Q_T(v,omega) <= C exp(2dT/(2s+d)).                  (1.1)

The data-call cap is deterministic, including paths on which a random
bit rejection loop never terminates. The latter paths have probability
zero and acquire no additional values during that loop.

The proof uses these accepted T56/T59 facts, on `||q||infinity<=a0=7/8`:

1. With `nu=2*pi^2-1`, the actual phase

       A(q)=lim_(t->infinity) exp(-t) G(Pi S_tq),
       G(b)=b/sqrt(1-b^2),  Psi(z)=z/sqrt(1+z^2),

   exists, is `C^3` on a neighborhood of this ball, and has a public
   uniform third operator-derivative bound `K3`. The accepted stronger
   product-measure result through order three is not extended by fiat.

2. There are public `Cw,C0` with, for `t>=1`,

       ||Q S_tq||infinity <= Cw exp(-nu*t),
       ||S_tq-Psi(exp(t)A(q))||infinity <= E(t),
       E(t)=Cw exp(-nu*t)+C0 exp(-(2nu-3)t).             (1.2)

   The coordinate tail is
   `|A(q)-exp(-t)G(Pi S_tq)|<=C0 exp(-(2nu-2)t)`.

3. From exactly `k^d` paid uniform-grid values there is a fixed smooth
   periodic interpolant `g` with

       ||v-g||infinity <= Cint k^(-s)=delta,
       ||g||_(C^s,max) <= Cint.                         (1.3)

   It has a known finite formula and public bounds on any fixed higher
   derivative. Once `k` is above a public threshold, `||g||<=3/4` and
   `delta<=1/4`. The residual has a public Lipschitz bound, also for
   `s=1`. Total-order derivatives through `s` suffice.

4. `A(q)` on an explicitly known smooth `q` in the `7/8` ball can be
   approximated to any positive prescribed precision by a finite
   deterministic calculation. This means the known-profile procedure
   in T56 Section 6c and T59 Sections 5--6, not a new oracle. Section 8
   below specifies exactly how it is used and why all its inputs are
   known finite formulas.

All of these accepted facts hold in every fixed finite dimension. The
restriction `d<=4s` in D27 came later, from its cubic Taylor remainder.
No weighted third-derivative estimate from T61 is needed here.

Comparison also gives, for real profiles in the unit sup-norm ball,

    ||S_tq-S_tq'||infinity <= exp(t)||q-q'||infinity.    (1.4)

Indeed the difference potential is
`1-(u^2+u u'+u'^2)<=1`. The strict open unit ball is sufficient in
all subsequent differentiations.

## 2. Stable heat kernel and an explicit local graph

Put `sigma=1`, so `0<sigma<nu`. Define the signed heat kernel

    B_t(x,dy)=exp(t)(P_t(x,dy)-lambda(dy)).

At time zero this means `delta_x-lambda`. There is a public finite `M`
such that

    sup_x ||B_t(x,.)||TV <= M exp(-nu*t),  t>=0.        (2.1)

This is a total-variation statement about the explicit kernel. For
`t>0` the norm equals `exp(t) integral |p_t-1|`. To verify a usable bound,
put

    rho=((1+exp(-2*pi^2))/(1-exp(-2*pi^2)))^d,
    M=2 rho exp(2*pi^2).

For `0<=t<=1`, `||B_t||TV<=2 exp(t)` proves (2.1). For `t>=1`, the
Fourier series and `|n|^2>=1` for nonzero `n` give

    integral |p_t-1|
      <= sum_(n!=0) exp(-2*pi^2 |n|^2 t)
      <= exp(-2*pi^2(t-1)) (rho-1),

which also proves (2.1). Bounds may be rounded upward to public
computable constants. No uniformity in `d` is asserted.

Let `E_sigma` be the real Banach space of continuous trajectories
`u:[0,infinity)->C(X)` with

    ||u||sigma=sup_(t>=0) exp(sigma*t)||u(t)||infinity.

Define the linear forward/backward integral operator

    (L F)(t,x)
      =-integral_0^t integral_X F(r,y) B_(t-r)(x,dy) dr
       +integral_t^infinity exp(t-r) Pi F(r) dr.        (2.2)

It maps `E_sigma` to itself and has norm at most

    Cstar=M/(nu-sigma)+1/(1+sigma).                    (2.3)

The forward estimate integrates `M exp(-(nu-sigma)(t-r))`; the backward
estimate integrates `exp(-(1+sigma)(r-t))`. Strong continuity of the
heat semigroup on `C(X)` and these integrable bounds give continuity of
the resulting trajectory. Pointwise multiplication is a bounded
trilinear map `E_sigma^3 -> E_sigma` of norm at most one.

Choose a positive public `R`, and then `r=R/(4M)`, small enough that

    Cstar R^2<=1/8,
    R^3/(1+3sigma)<=r/8,
    r<1/8,
    K3 r^2/2<=epsilon0:=1/64.                          (2.4)

Such a choice exists because every condition is an upper bound on a
positive power of `R` with fixed coefficients. Rational smaller choices
are permitted. In particular `R<1` can also be imposed.

For every `z in C(X)` with `||Qz||<3r`, solve

    U(z)(t)=B_t z + L(U(z)^3)(t).                      (2.5)

On the closed radius-`R` ball in `E_sigma`, its right side has norm
at most `3Mr+Cstar R^3<=7R/8`. Its Lipschitz constant in `u` is at
most

    kappa=3 Cstar R^2<=3/8<1.                         (2.6)

The contraction therefore has a unique solution in that ball; its norm
is at most `7R/8`. It depends only on `Qz`. Define, for mean-zero `w`,

    Theta(w)=Pi U(w)(0),       F(z)=Theta(Qz).

Equation (2.5) gives

    U(w)(0)=w+Theta(w),
    Theta(w)=integral_0^infinity exp(-t) Pi U(w)(t)^3 dt,
    |Theta(w)|<=R^3/(1+3sigma)<=r/8.                  (2.7)

The plus sign is essential. Differentiating the mean formula gives
`b'=b-Pi U^3`; the centered part obeys the forward mild equation. Thus
`U(w)` is the actual mild PDE solution from `w+Theta(w)`, and uniqueness
identifies it with `S_t(w+Theta(w))`. This datum has norm below `1`
for `||w||<3r`, by (2.4) and (2.7). It decays to zero in `E_sigma`, so

    A(w+Theta(w))=0.                                  (2.8)

The solution map is `C^infinity` on `||Qz||<3r` as an ordinary
`E_sigma`-valued map. One direct justification applies the Banach
implicit theorem to `u-Bz-L(u^3)`: its `u` derivative is
`I-L(3u^2 .)`, whose Neumann inverse has norm at most `(1-kappa)^(-1)`.
Equivalently, contraction difference quotients give the first derivative,
and differentiating that resolvent equation inductively gives all finite
orders. The polynomial maps are bounded on `E_sigma` and the solution
lies strictly inside the radius-`R` ball. This argument establishes
ordinary smoothness only. Actual derivative measures are proved next.

## 3. The kernel Banach space, including the measurability issue

For `j>=1`, let `K_j` consist of signed Borel kernels

    K:(t,x) in [0,infinity) x X -> M(X^j)

such that `K(t,x;A)` is Borel for every Borel `A subset X^j`, every
`K(t,x;.)` is a finite signed measure, and

    ||K||sigma,TV
       =sup_(t>=0) exp(sigma*t) sup_x ||K(t,x;.)||TV
       <infinity.                                    (3.1)

These are actual kernels, with a supremum over all roots and times, not
equivalence classes whose exceptional sets could depend on a leaf tuple.
All finite Borel measures on the compact metric spaces used here are
Radon. The order in (3.1) is important: take total variation in the full
leaf product for each root, and only then take the root supremum.

This space is complete. A Cauchy sequence in (3.1) has a total-variation
limit at each `(t,x)`, by completeness of finite signed measures in that
norm. The uniform weighted bound gives convergence in (3.1), and each
set evaluation is a pointwise limit of Borel functions. It is therefore
again a signed Borel kernel.

Here are the closure operations used below, with their justification.

* Total variation is itself a Borel kernel. Fix a countable algebra
  generating the Borel sets of the compact metric leaf space. For any
  fixed Borel set `A`, variation on `A` is the supremum of
  `sum_l |K(t,x;A intersect A_l)|` over the countably many finite
  algebra partitions `(A_l)` of the space. This equals the full
  variation by approximation in the finite measure `|K(t,x)|`.
  Thus the supremum is Borel. Jordan positive and negative parts are
  consequently Borel kernels as well.

* Kernels with disjoint leaf labels can be tensor multiplied at the
  same `(t,x)`, and their coordinates can be permuted into label order.
  For rectangles, measurability is just the product of the set
  evaluations; extension to all Borel sets follows from the monotone
  class argument for positive kernels and then the finite Jordan
  decomposition. The variation satisfies

       ||K tensor K'||TV <= ||K||TV ||K'||TV.           (3.2)

  Consequently a product of `p` kernels, each of weight `sigma`, is a
  kernel of weight `sigma`, with norm at most the product of the norms:
  its extra time factor is `exp(-(p-1)sigma*t)<=1`. Multiplication by a
  scalar continuous trajectory is the zero-leaf version of this rule.

* For a signed kernel `K(r,y;dY)` and a signed spatial kernel
  `D(t,r,x;dy)`, composition means the setwise integral

       A -> integral K(r,y;A) D(t,r,x;dy).

  It is countably additive whenever the integral of the variations is
  finite, by dominated convergence on disjoint unions. Its variation
  is bounded by `integral ||K(r,y)||TV |D|(t,r,x;dy)`.
  Measurability follows first for simple functions and then by bounded
  or monotone convergence. The same statement applies after time
  integration when the variation envelope is integrable.

This deliberately uses setwise kernel integration. It does **not**
claim that `x -> delta_x` is strongly measurable or continuous as an
`M(X)`-valued map with its total-variation norm; such a claim would be
false. Nor is an unproved Bochner integral in that nonseparable range
being used. The kernel facts above construct countably additive measures
and control their variation directly.

Apply (2.2) to such kernels by these setwise compositions and integrals.
The same estimates as in (2.3), now with variation before any supremum,
give

    ||L K||sigma,TV <= Cstar ||K||sigma,TV.             (3.3)

Both the signed heat kernel at lag zero and the infinite backward time
integral are covered. Endpoint values in time integrals are harmless,
and the backward tail converges in total variation at each root, with
the weighted uniform bound in (3.3). No `sup_x` has been moved through
an arbitrary leaf integral.

## 4. Every finite graph derivative has an actual product measure

Fix `z` in `||Qz||<3r` and put `u=U(z)`. For a finite label set `I`,
write `U_I=D^(|I|)U(z)[h_i:i in I]`, with `U_empty=u`. Differentiating
the cubic gives the exact ordered-partition formula

    D^j(u^3)[h_1,...,h_j]
      =sum_(A disjoint B disjoint C=[j]) U_A U_B U_C.  (4.1)

There are three terms in which one block is all of `[j]` and the other
two are empty. Their sum is `3u^2 U_[j]`. All other blocks have size
strictly less than `j`. Define their sum to be `V_[j]`; it is zero
when `j=1`. The derivative equation is

    U_[j]=1_(j=1) B_.h_1 + L(3u^2 U_[j]+V_[j]).      (4.2)

We now solve (4.2) with actual measures. For order one, use the
one-leaf signed kernel `B_t(x,dy)`, whose norm is at most `M`. For
every higher order, replace each proper block in (4.1) by the
lower-order kernel already constructed and tensor the disjoint labels.
Empty blocks mean multiplication by `u`. Section 3 makes the resulting
source an element of `K_j`.

On `K_j`, the same feedback map

    T_u K=L(3u^2 K)

has norm at most `kappa`, independently of `j`. Hence

    K^[j]=sum_(n=0)^infinity T_u^n
                 (1_(j=1) B + L V^[j])               (4.3)

converges in the Banach norm (3.1). In particular, this is a limit of
actual measures in total variation, not a weak limit of possibly
unbounded partition coefficients. Every time integral, tensor product,
and Neumann sum has been controlled before taking the spatial supremum.

Here is a public finite bound at every order. Set

    v0=R,       v1=M/(1-kappa),
    vj=Cstar/(1-kappa)
          * sum_(a+b+c=j; 0<=a,b,c<j)
                 [j!/(a! b! c!)] va vb vc,  j>=2.      (4.4)

The sum is finite and depends only on previously defined numbers. The
count `j!/(a!b!c!)` is exactly the number of ordered label partitions
with those block sizes. Induction in (4.3) proves

    ||K^[j]||sigma,TV <= vj.                          (4.5)

Pair (4.3) against `product_i h_i(y_i)` for arbitrary continuous
directions. Tensor products pair to the appropriate products of the
lower variations, and the integrable variation envelopes justify every
interchange. The resulting trajectory satisfies (4.2). It is continuous:
inductively its forcing is continuous in `E_sigma`, (2.2) preserves that
space, and its Neumann sum converges there. The resolvent in (4.2) is
unique. Thus it equals the actual ordinary Frechet derivative already
identified in Section 2. This proves the representation, rather than
assuming it from that ordinary differentiability.

Finally, define an actual scalar signed measure on `X^j` by

    tau_j(z;dY)=integral_X K^[j](0,x;dY) lambda(dx).

Since `F(z)=Pi U(z)(0)=Theta(Qz)`, we have, for every fixed `j>=1`,

    D^jF(z)[h_1,...,h_j]
       =integral_(X^j) product_i h_i(y_i) tau_j(z;dY),
    ||tau_j(z)||TV<=vj,   uniformly for ||Qz||<3r.     (4.6)

Only the existence and uniform variation bounds are needed. We do not
need strong measurability of `z -> tau_j(z)` or norm analyticity into a
space of measures. Coefficients will be obtained by finite scalar
calculations, not by accessing these measures as an oracle.

There is no condition of the form `j sigma<nu` or `3j+2<2nu` in
(4.4). All differentiated stable trajectories live in the same
`E_sigma`. Products improve time decay, and the contraction constant
is the same at every finite order. The price for high order is large
finite constants, which are allowed when `d,s` are fixed.

## 5. Finite-time composition is also a measure construction

We first record the all-order finite-time kernel fact needed for
composition. Fix any finite `L>0` and a real `q` with `||q||<1`.
For the flow `u(t)=S_tq`, the first variation has potential

    c(t,x)=1-3u(t,x)^2,       |c|<=2.

On `[0,L]`, its mild equation can be solved by the Volterra Neumann
series using the positive heat kernel. The `n`th feedback iterate has
variation at most `(2L)^n/n!`; this comes from the ordered time simplex.
Thus the series of actual signed kernels converges uniformly in
pointwise-root total variation. Its norm is at most `exp(2L)`.

For order `j>=2`, separate `3u^2 U_[j]` in the cubic as before. The
source is minus the sum of all proper ordered three-block products;
all its derivative orders are smaller than `j`. Apply the same
Volterra resolvent to the heat integral of this source. Tensor products,
spatial integrations, time integrations, and convergence are justified
by Section 3, now on a finite time interval without a time weight.
Pairing with continuous directions identifies these kernels with
`D^jS_t(q)` by the variational equations. Ordinary finite-time `C^infinity`
regularity follows from local Picard differentiation and continuation
of the bounded solution over `[0,L]`.

For an entirely finite uniform recipe, put

    a_0^flow=1,    a_1^flow=exp(2L),
    a_j^flow=L exp(2L)
        * sum_(a+b+c=j; 0<=a,b,c<j)
               [j!/(a!b!c!)] a_a^flow a_b^flow a_c^flow. (5.1)

Then the order-`j` flow kernel `Gamma_j(q;t,x;dY)` satisfies

    sup_(0<=t<=L) sup_x ||Gamma_j(q;t,x;.)||TV
       <=a_j^flow.                                   (5.2)

Indeed, `exp(2(t-r))` bounds the absolute resolvent propagator and
`L exp(2L)` bounds its source integral. The constants in (5.1) are
loose but finite and independent of `q` in the open unit ball.

Now choose once and for all a public `L>=1` such that

    Cw exp(-nu*L)<=r/16.                              (5.3)

This is a fixed burn-in, independent of the target horizon. Define

    H(q)=H_L(q)=Pi S_Lq-F(S_Lq)
                  =Pi S_Lq-Theta(Q S_Lq).             (5.4)

It is `C^infinity` on the open set

    D={q: ||q||<1, ||Q S_Lq||<3r},

which contains the entire closed `7/8` ball by (5.3). Thus the Taylor
and coefficient computations below have one uniform domain. Small mean
is needed only for the phase comparison in Section 6, not for defining
or differentiating `H`.

For a set partition `pi` of the `j` input labels into `p` nonempty
blocks, order the blocks by their least label. The corresponding
chain-rule term in `D^j(F composed with S_L)` is represented by

    integral_(X^p) [tensor_(B in pi)
          Gamma_(|B|)(q;L,z_B;dY_B)]
             tau_p(S_Lq;d(z_B:B in pi)),               (5.5)

with a permutation putting the leaf coordinates into label order.
This is an actual measure: the tensor integrand is a Borel signed
kernel in the intermediate roots, and its variation is bounded by
`product_(B in pi) a_(|B|)^flow`. Integrating against the finite
variation of `tau_p` proves existence and countable additivity, with
bound `vp product_B a_(|B|)^flow`. This addresses the product-measure
composition step explicitly; an operator chain rule alone would not.

The mean term is the root integral of `Gamma_j`. Summing over the
finitely many set partitions yields an actual measure `mu_j(q)` with

    D^jH(q)[h_1,...,h_j]=integral product_i h_i(y_i) mu_j(q;dY),
    ||mu_j(q)||TV<=Bj,
    Bj=a_j^flow+sum_(pi partition of [j])
                   v_(|pi|) product_(B in pi) a_(|B|)^flow.     (5.6)

These bounds hold uniformly on `D`, hence on the `7/8` ball. The finite
recursions (4.4), (5.1), and finite partition sum (5.6) give public
bounds for any prescribed finite `J`. No derivative of the global
phase `A` beyond order three has entered.

## 6. Multiplicative phase proxy in the local region

Oddness of the actual PDE and `G` implies oddness of `A`. At zero,
linearization gives `DA(0)=Pi`, and oddness gives `D^2A(0)=0`.
For example, in T56's phase formula the correction is at least cubic
at zero, and the derivative of `G(Pi q)` is `Pi`. The accepted `C^3`
bound and two applications of the fundamental theorem therefore give

    |DA(p)[1]-1|<=K3 ||p||^2/2<=epsilon0,
                                 ||p||<=r.            (6.1)

Let `w` have mean zero, and suppose the segment joining
`b+w` to `Theta(w)+w` lies in the radius-`r` sup ball. Set
`h=b-Theta(w)`. By (2.8) and (6.1),

    A(b+w)=c h,        1-epsilon0<=c<=1+epsilon0.       (6.2)

This statement includes `h=0`. Otherwise `A` and `h` have the same
sign. For any real `z` and `c` in that interval,

    |Psi(c z)-Psi(z)|
       <= |c-1|/[2(1-epsilon0)] <=epsilon0.            (6.3)

To verify it, differentiate in `c`: the absolute derivative is
`|z|/(1+c^2 z^2)^(3/2)`. With `y=|cz|`, the inequality
`y/(1+y^2)^(3/2)<=1/2` follows from `1+y^2>=2y`.
Integrating over `c` proves (6.3), since `epsilon0<=1/2`.
It is uniform in `z`, even when `z=exp(t)h` and `h` is arbitrarily
close to zero. An additive error in `A` would not give this property.

The phase limit also gives the exact semigroup identity

    A(S_Lq)=exp(L) A(q),                               (6.4)

whenever both sides are defined. Indeed, shift the time variable in
the defining limit. Profiles in the strict unit ball remain in it
at every finite time by scalar comparison. In the application below
`S_Lv` is in the radius-`r` ball, so the accepted local phase bounds
apply directly. Combining (6.2)--(6.4) then gives

    |Psi(exp(T) A(v))-Psi(exp(T-L) H(v))|<=1/64.        (6.5)

## 7. Branch selection from paid coarse information

Choose the public grid threshold `k0` large enough for (1.3),
`delta<=1/4`, `||g||<=3/4`, and

    exp(L) delta<=r/32.                               (7.1)

The whole segment `q_theta=g+theta(v-g)` lies in the `3/4` ball.
Using only the known formula for `g`, compute

    |btilde-Pi S_Lg|<=r/32                            (7.2)

by the finite known-profile solver described in Section 8. This makes
no new query to `v`.

If `|btilde|>r/2`, let `sign=btilde/|btilde|` and return that sign.
Equations (1.4), (7.1), and (7.2) imply

    sign * Pi S_Lv>7r/16.

By (5.3), `||Q S_Lv||<=r/16`, so `sign*S_Lv>=3r/8` pointwise.
Scalar comparison then gives, with `a=3r/8`,

    |sign-S_Tv(x*)|<=1-ell_a(T-L),
    ell_a(t)=[1+(a^(-2)-1)exp(-2t)]^(-1/2).            (7.3)

For a public sufficiently large `T-L`, this is at most `1/16`.
For instance `T-L>=max(0,log(8a^(-2))/2)` suffices, using
`1-(1+z)^(-1/2)<=z/2` for `z>=0`.

If `|btilde|<=r/2`, every `q_theta` instead satisfies

    |Pi S_Lq_theta|<=r/2+r/32+r/32=9r/16,
    ||Q S_Lq_theta||<=r/16,
    ||S_Lq_theta||<=5r/8.                             (7.4)

For `v` in particular, put `w=Q S_Lv`. Then the stable datum has
norm at most `r/16+r/8=3r/16`. Both it and `S_Lv` are in the
radius-`r` ball, as is their constant-direction joining segment.
Thus (6.5) applies. This near branch includes the stable manifold
itself and every arbitrarily close input. No exact phase sign or
exact unknown PDE mean is used to choose a branch.

## 8. Finite evaluation of H on known profiles

We give a finite algorithm to approximate `H(q)` to any prescribed
`epsilon>0`, for an explicitly known smooth `q` with `||q||<=7/8`.
This will be applied only to formulas built from the coarse transcript
and public perturbations.

### 8a. A smooth known approximation to S_Lq

For any prescribed `xi>0`, a finite uniform-grid computation produces
a known smooth function `p` with

    ||p-S_Lq||infinity<=xi.                            (8.1)

One concrete procedure uses the monotone explicit Euler/central
difference scheme from T56 Section 6c, with time step satisfying
`h_t<=(d/h_x^2+2)^(-1)` and an integer number of steps ending at `L`.
The update fixes `+/-1`, is order preserving there, and has sup-norm
Lipschitz constant at most `1+h_t`. Public solution-derivative bounds
through spatial order four and time order two give the finite global
error `C(q,L) exp(L)L(h_x^2+h_t)`. Such bounds come recursively from
the polynomial differentiated PDE and the maximum principle; the
initial bounds are computable from the known finite formula for `q`.
In particular they do not require additional values of `v`.

Blend the final grid values with a fixed smooth nonnegative periodic
partition of unity supported near its nodes. Its translation symmetry
gives every partition weight integral `1/Ngrid`, so `Pi p` is exactly
the arithmetic mean of the computed grid values. The interpolation
error is bounded by the public Lipschitz bound for `S_Lq` times the
support diameter. Choose the numerical error and that error to sum
to at most `xi`. Include value-evaluation and rounding errors with
the same stability bound; clipping updates to `[-1,1]` is nonexpansive.
This proves (8.1) by a fixed finite mesh rule. The resulting `p` has
a finite smooth formula and public derivative bounds, even if those
bounds and the number of mesh cells are enormous.

The same construction, followed by its exact mean, proves (7.2) by
taking `xi<=r/32`.

### 8b. Reduce graph evaluation to a scalar root on known data

Set

    wtilde=p-Pi p,      w=Q S_Lq.

Then `Pi wtilde=0` exactly and

    ||wtilde-w||<=2xi.

Taking `xi<=r/64` and using (5.3) ensures
`||wtilde||<=3r/32<r/8`. The function

    f(c)=A(c+wtilde),        -r/4<=c<=r/4,

has its zero at `c*=Theta(wtilde)` by (2.8), with `|c*|<=r/8`.
All profiles on this interval have norm below `r`, so

    f'(c)>=m0:=63/64.                                 (8.2)

In particular, the root is unique there and the endpoint signs have
a fixed nonzero buffer. They need not be guessed numerically.

For a desired root accuracy `zeta>0`, approximate each queried `f(c)`
to `epsA=m0*zeta/4`. Start with `[-r/4,r/4]`. At a midpoint `c`, if
`fhat>epsA`, keep the lower half; if `fhat<-epsA`, keep the upper
half. Otherwise `|f(c)|<=2epsA`, so `|c-c*|<=zeta/2` by (8.2), and
return `c`. After a public number of halvings making the interval
length at most `2zeta`, return its midpoint. Thus every branch halts
after a fixed finite maximum number of phase evaluations and achieves
error at most `zeta`. Equalities in the comparisons use the middle
case and pose no undecidability or unbounded refinement issue in the
accepted exact-real arithmetic model.

Each phase evaluation is the accepted finite known-profile calculation:
choose `tau` from `C0 exp(-(2nu-2)tau)` to control the phase tail,
solve the known datum `c+wtilde` up to `tau` by the finite monotone
mesh scheme, and approximate `exp(-tau)G` of its mean. Clip that mean
to the known scalar comparison interval. On this interval the
derivative of `exp(-tau)G` is at most a public constant times
`exp(2tau)`, so a public sufficiently accurate finite mesh achieves
`epsA`. The new initial profile has a finite formula: `p`, its
known mean, and a scalar. Its derivative bounds are public from the
partition and bounded mesh coefficients. No value of the unknown
input is requested in any of these solves or root steps.

### 8c. Allocate the H evaluation error

By (4.6), `Theta` is Lipschitz with constant at most `v1` on the
mean-zero local ball. Hence, for the returned root approximation
`chat`,

    |(Pi p-chat)-H(q)| <= (1+2v1)xi+zeta.              (8.3)

Choose

    xi<=min(r/64, epsilon/[4(1+2v1)]),
    zeta<=min(r/16,epsilon/2).

Then the error is less than `epsilon`. The numbers of spatial cells,
time steps, root iterations, and inner phase solves are all finite
public functions of the requested accuracy and formula-derivative
bounds. The same is true if safe rational upper bounds replace the
displayed constants.

This completes a finite evaluation procedure for `H(q)`. It never
assumes access to exact `S_Lq`, exact `Theta`, or exact `A`. The
extreme possible auxiliary cost is not charged as input information,
because every such initial profile is already an explicit function
of the paid coarse values. No arithmetic-work bound is claimed.

## 9. Arbitrary finite Taylor order and computable coefficients

Fix

    qrate=s+d/2,
    J=ceil(1+d/(2s))>=2,       m=J-1.

Then `Js>=qrate`. Let `e=v-g`, so `||e||<=delta`. Since the whole
segment is in the `7/8` ball, (5.6) gives

    H(v)=H(g)+sum_(j=1)^m D^jH(g)[e,...,e]/j!+Rem,
    |Rem|<=BJ delta^J/J!.                             (9.1)

For every positive `eta<=1`, the following finite coefficient
procedure uses only the coarse transcript. It produces `c0`, nodes
`z_i`, and rational ordered-tuple coefficients `c_I^(j)`, `1<=j<=m`,
such that

    |c0-H(g)|<=eta,
    sum_I |c_I^(j)|<=Bj+1,
    |sum_I c_I^(j) product_(ell=1)^j e(z_(i_ell))
                  -D^jH(g)[e,...,e]|<=eta.            (9.2)

The last inequalities hold uniformly over all residuals consistent
with the public sup-norm and Lipschitz bounds. No residual-grid values
are acquired while computing the coefficients.

### 9a. Positive partitions and the l1 bound

Take a fixed sufficiently fine smooth nonnegative partition
`theta_i`, `i=1,...,N`, with `sum_i theta_i=1` and nodes `z_i` close
to its supports. Define the formal interpolated residual

    Pe=sum_i e(z_i)theta_i.

Positivity gives `||Pe||<=delta`. The public Lipschitz bound gives
`||Pe-e||<=epsilonP` once the support diameter is small enough.
Choose

    epsilonP<=eta/[2Dstar],
    Dstar=1+max_(1<=j<=m) j Bj.

The exact ordered coefficients

    a_I^(j)=D^jH(g)[theta_(i_1),...,theta_(i_j)]

obey

    sum_I |a_I^(j)|<=Bj.                              (9.3)

Indeed sum the nonnegative products of partition weights against
`|mu_j(g)|`; their sum on `X^j` is identically one. Moreover,
multilinear telescoping gives

    |D^jH(g)[Pe,...,Pe]-D^jH(g)[e,...,e]|
       <=j Bj delta^(j-1) epsilonP<=eta/2.             (9.4)

This is precisely the step that would fail if (5.6) were replaced
by an ordinary multilinear operator bound alone.

### 9b. Mixed finite differences, including repeated indices

For a fixed ordered tuple `I=(i_1,...,i_j)`, use

    Deltah_I H(g)
      =h^(-j) sum_(S subset [j]) (-1)^(j-|S|)
                 H(g+h sum_(ell in S) theta_(i_ell)).  (9.5)

Repeated indices are allowed and correspond to repeated directions;
the subset labels still distinguish all `j` occurrences. The iterated
fundamental theorem gives exactly

    Deltah_I H(g)
      =integral_[0,1]^j D^jH(g+h sum_l t_l theta_(i_l))
                    [theta_(i_1),...,theta_(i_j)] dt.

Consequently, if the perturbed profiles stay in the `7/8` ball,

    |Deltah_I H(g)-a_I^(j)|<= (j/2) B_(j+1) h.        (9.6)

The factor `j/2` is the integral of `sum_l t_l`. Thus all orders up
to `m` need only the bounds through `J`; no hidden `J+1` bound or
analytic convergence of a Taylor series is required.

For each `j`, choose a positive rational `h_j` such that

    h_j<=1/(16m),
    h_j<=eta/[4j N^j (B_(j+1)+1)].                    (9.7)

Compute each scalar `H` in (9.5) by Section 8 with error at most

    epsH_j=eta h_j^j/(8*2^j*N^j),

and round each final coefficient rationally with error at most
`eta/(8N^j)`. Summing over the `N^j` tuples, the finite-difference
error is at most `eta/8`, scalar evaluation error at most `eta/8`,
and rounding error at most `eta/8`. Therefore

    sum_I |c_I^(j)-a_I^(j)|<=3eta/8<eta/2.             (9.8)

Its action on products of residual values has error at most
`(eta/2)delta^j<=eta/2`. Equations (9.3), (9.4), and (9.8) prove
(9.2); `c0` is a separate Section 8 evaluation to accuracy `eta`.
All factorials in (9.1) remain in the estimator below.

Every profile in (9.5) is known from the coarse data and public
functions. On promised transcripts its norm is at most
`3/4+m h_j<=13/16<7/8`. For a total off-promise definition, first
clip coarse entries to `[-1/2,1/2]` and apply a fixed smooth saturation
to the raw coarse interpolant, equal to the identity on `[-3/4,3/4]`
and with range `[-13/16,13/16]`. This changes no promised run.
Then (9.7) makes every perturbed profile stay within `7/8` even on
these extended transcripts. Public high-derivative bounds are still
available from the finite formula. No exact norm test is needed.

## 10. Sampling, risk, and the all-dimension query cap

On the near branch, set `Mquery=k^d`. Conditional on the fixed coarse
transcript, all coefficients in (9.2) are known. For each
`j=1,...,m`, put

    Wj=sum_I |c_I^(j)|.

If `Wj=0`, that correction is zero. Otherwise draw `Mquery`
independent ordered tuples with probability `|c_I^(j)|/Wj`. At each
draw acquire the `j` required exact values of `v`, charging every
one, and return

    Zj=Wj sign(c_I^(j)) product_(ell=1)^j
                                  (v(z_(i_ell))-g(z_(i_ell))).

Set

    Hhat=c0+sum_(j=1)^m average(Zj)/j!,
    Yraw=Psi(exp(T-L) Hhat).                           (10.1)

For every fixed input the new samples have the stated finite-sum
means and obey `|Zj|<=(Bj+1)delta^j`. Independent samples within
each average give standard deviation at most
`(Bj+1)delta^j/sqrt(Mquery)`. Minkowski's inequality and (9.1)--(9.2)
therefore yield

    RMS(Hhat-H(v))
      <=sum_(j=1)^m (Bj+1)delta^j/(j! sqrt(Mquery))
           +BJ delta^J/J! +3eta.                      (10.2)

Here `1+sum_(j=1)^m 1/j!<3` accounts for all deterministic coefficient
errors. No unbiasedness of `Hhat` for `H(v)` or of `Yraw` for the
PDE target is asserted.

Every stochastic exponent `js+d/2` is at least `qrate=s+d/2`, and
`Js>=qrate`. Define the public finite constant

    Bstar=1+sum_(j=1)^m (Bj+1) Cint^j/j!
                  +BJ Cint^J/J!.

For `k>=k0`, the first two parts in (10.2) are at most
`Bstar k^(-qrate)`. For `T>=L`, choose exactly

    k=max(k0,ceil((32 Bstar exp(T-L))^(1/qrate))),
    eta=exp(-(T-L))/192.                              (10.3)

Then

    exp(T-L) RMS(Hhat-H(v))<=1/32+1/64=3/64.            (10.4)

Choose `T0>=L` large enough that `E(T)<=1/32` and the far-branch
condition following (7.3) holds for all `T>=T0`. The accepted PDE
profile error (1.2), the multiplicative local comparison (6.5), and
the global 1-Lipschitz property of `Psi` now give, on the near branch,

    RMS(Yraw-S_Tv(x*))<=1/32+1/64+3/64=6/64.

An optional final finite scalar approximation of `Yraw` to accuracy
`1/64`, clipped to `[-1,1]`, gives RMS at most `7/64<1/4`. On the
far branch the error is at most `1/16` and the returned sign is exact.
The branch is deterministic given the coarse transcript, and the
bounds hold for each promised input, so they imply the uniform risk
in (1.1).

The number of charged values is at most

    k^d + sum_(j=1)^m j Mquery
      =[1+J(J-1)/2] k^d.                              (10.5)

This includes coarse information and every residual value, even
repeats within or across tuples. Coefficient evaluation, burn-in
selection, the graph-root computations, and every auxiliary PDE
solve reveal no further unknown-input values. The far branch costs
only the coarse `k^d` values.

The fixed thresholds, exact ceiling choice in (10.3), and fixed finite
`J` show that (10.5) is at most

    C exp(dT/qrate)=C exp(2dT/(2s+d)).                  (10.6)

This works for every fixed `d,s>=1`, including equality in
`Js=qrate` when it occurs. In that case the Taylor remainder has the
same order as the leading random error and is absorbed by `Bstar`.
There is no dimension ceiling such as `d<=20s`.

If a bound for the bounded interval `0<=T<T0` is desired, use a fixed
coarse interpolant fine enough that `exp(T0)||v-g||<=1/16`, then the
known-profile finite PDE calculation to another `1/16`. It has a fixed
finite query count; it changes no large-horizon exponent.

## 11. Measurability, finite precision, and halting

All structural sizes can be fixed by public bounds in this order:

1. `M,Cstar,R,r`, the fixed burn-in `L`, derivative constants through
   order `J`, interpolation constants, and `k0,T0`;
2. the horizon-dependent `k,eta`, the fine positive partition, and its
   finite size `N`;
3. the increments `h_j`, scalar evaluation tolerances, rational
   rounding precisions, and public derivative bounds of all possible
   known profiles used in these finite differences;
4. the finite PDE meshes and time steps, maximum root-bisection counts,
   and inner phase-tail times needed to implement Section 8 at those
   tolerances.

The bounds in the fourth item may use the previously fixed finite
partition and the bounded mesh coefficients, rather than an unknown
norm of a solution or an uncertified stopping test. All deterministic
loops have finite public maximum lengths. Conditional choices during
bisection only shorten those loops or choose which finite arithmetic
operations follow; both sign comparisons and the uncertain-sign
return are Borel operations on already computed real numbers.

Smooth formula evaluation, finite arithmetic, clipping, saturation,
fixed-precision rational rounding, and comparisons are Borel functions
of the finitely many exact returned coarse values. The initial and
residual query locations are chosen by these maps and private random
bits. The exact-real point-query model accepts this scalar processing;
the argument is not a finite-bit encoding theorem for arbitrary real
oracle responses.

Rational coefficients make each sampling distribution a finite set of
nonnegative integer weights after multiplication by a common
denominator. Draw a uniform integer using rejection from the smallest
covering power of two. Each attempt succeeds with probability at least
`1/2`; it makes no initial-data query. A fixed finite number of these
draws halts almost surely. Zero-weight orders are skipped. Once a tuple
is selected, it acquires exactly its charged `j` values. Therefore no
random-bit path can breach (10.5), and termination is almost sure for
each input.

The finite scalar evaluation of `Psi` to the stated fixed output
tolerance is also permitted. It may use elementary interval
approximation on a bounded argument interval, with the tails returned
as the corresponding sign once their explicit error is below the
tolerance. This does not query the datum. All output values remain
bounded by one after clipping.

## 12. Repairs to the candidate, failure modes, and audit boundaries

R07 correctly isolated the main obligation, but its ordinary analytic
fixed-point observation did not prove product measures. Sections 3--4
close that gap with actual Borel kernels, a complete weighted
total-variation norm, setwise integrations, and convergent measure
Neumann series. A proposed replacement using Bochner continuity of
Dirac kernels would fail; this proof deliberately does not use it.

R07's finite-time composition is expanded in (5.5), with explicit
signed-kernel integration and a finite partition sum. The fixed
burn-in makes `Q S_Lq` small for the entire `7/8` input ball, which
means `H_L` itself is available there even when the evolved mean is
large. Only the multiplicative phase comparison needs branch selection.
This removes an unnecessary local-domain concern from the Taylor
coefficient calculations without changing the input class.

Generic high smoothness of an inertial manifold would not establish
either (4.6) or (5.6), and no such theorem is imported. Nor is the
global phase asserted to be smooth to arbitrary order. Directly
extending T56's global phase differentiation retains its finite
spectral-bunching bound and does not prove an all-dimension result.
Here the local stable trajectories and all their derivatives decay
in one fixed weighted space; this is the specific reason the
order-dependent obstruction disappears.

The paid mean test has a strict error buffer and a fully specified
near branch. Replacing it with exact unknown phase access or excluding
interface inputs would change the problem. Likewise, querying all
fine partition nodes during coefficient construction would destroy
the count (10.5). Section 8 computes only already-known profiles, and
Section 10 lists every actual data acquisition.

The high-order finite-difference bound (9.6) includes repeated indices
and uses only `B_(j+1)`. The rational l1 coefficient errors, Taylor
factorials, critical equality `Js=qrate`, finite root evaluation, and
almost-sure discrete sampling are explicit. No numerical verification
or source-code implementation is offered as a substitute for these
claims.

Independent audit should concentrate on the setwise kernel construction
and its completeness, equality with the derivatives, the signed
composition measure (5.5), the local phase multiplier, and the nested
known-profile evaluation without additional data access. Within this
derivation no unproved product-measure or extra-oracle obligation is
left as an assumption. External acceptance is still pending.

## 13. Evidence and primary-literature scope

Read completely: R07, the 717-line frozen T56, the 544-line frozen T59,
and the accepted D27 synthesis. T61 was inspected for its theorem,
normalization, and the separate lower-bound boundary; its weighted
derivative proof is not used. Project instructions, the current
research guide, and the research skill routing/execution instructions
were read. Existing working-tree modifications were observed and left
alone.

Source hashes checked before writing this proof:

    R07-local-stable-graph-upper-candidate.md
    adbe2c455bc36b22b5414b6090930e2f0e92711a85029643ca517d6676d52071

    T56-signed-upper-feasibility.md
    0f0cd6a6fbe97d5746c42f2da94161284f4b4fb3da70b724b5992450388d5933

    T59-signed-upper-independent-audit.md
    47d3ce98ac19210e9bbcd318ac1de2fb9dddd5bc372bff201dc97d47572301ab

    04t-matching-signed-query-complexity.md
    260ae16cb5104bfdc56eadc8a7829410c1a4b73c81703b038665427313d8eca9

    T61-all-dimension-lower-proof.md
    404a237be72991ac60efb97c48b5ba2347384b0a30ffe3a98219a74d1604d691

The primary abstracts in R07 were opened for bounded methodological
context. [Van den Berg, Jaquette, and Mireles James](https://arxiv.org/abs/2004.14830)
describe validated stable-manifold computation using a Lyapunov--Perron
method in adapted coordinates. [Kostianko and Zelik](https://arxiv.org/abs/2102.03473)
discuss limits on general inertial-manifold smoothness and smooth
extensions under additional constructions. Neither abstract supplies
the product-measure or query theorem here; their full proofs were not
used to fill a gap. This is not a comprehensive literature or priority
search. The classical smooth-integration rate and residual sampling
precedents already recorded by T56/T59 remain explicit predecessors.

Research-role metadata: task T65 was requested with the skill's
`gpt-6-astra`/`max` research routing. This worker made no model-setting
change; its actual backend and effort are not independently exposed by
the tools in this task. Work performed: read-only source inspection,
hash verification, primary-abstract retrieval, conventional derivation,
and this single proof-file write. No Lean, code, numerical experiment,
ledger update, or additional agent was used. The final file hash is
reported in the handoff rather than self-embedded.
