# T81: a fixed-burn-in work upper bound for every positive diffusivity

Date: 2026-09-29. Research-only conventional proof candidate.

**Verdict: GO for independent mathematical audit.** The fixed-time
Fourier reconstruction route gives the requested ideal-work upper bound
on the full signed class for every fixed `kappa>0`, including
`2*pi^2*kappa<=1`. The two additional gates close: the audited known-data
solver extends to fixed positive diffusivity, and coefficient clipping
followed by an explicit Gevrey saturation gives a uniformly costed
continuation profile on every completed sample path. No stable graph,
global phase, convergence to a spatial constant, or spectral-gap
assumption enters the proof.

This is a candidate for root correspondence and an independent review,
not an accepted-ledger change. It proves an upper bound with a polynomial
factor in the horizon. It does not prove an exact query order, a lower
bound for the enlarged diffusion scope, bit complexity, practical speed,
novelty, or an end-to-end Lean theorem. No numerical experiment or unknown
initial-data acquisition was performed while writing this proof.

## 1. Statement, class, and operation model

Fix integers `d,s>=1`, one real `kappa>0`, and an output point `x*` on
the normalized unit torus `X=R^d/Z^d`. Write `S_t^kappa` for the actual
Allen--Cahn solution operator

    u_t=(kappa/2) Delta u+u-u^3,       u(0)=v.

The unknown class is exactly the full D29 signed class, with the
diffusion coefficient now as displayed:

    V={v in C^infinity(X): ||v||inf<=1/2,
       max_(|alpha|<=s)||partial^alpha v||inf<=1,
       min v<0<max v}.

Only exact point values of `v` are supplied. Every acquisition costs one
unit, including repeated locations and preprocessing. The common D33
ideal model also charges each real arithmetic operation, comparison,
floor/ceiling, integer/index/modular operation, stored-value read/write,
and evaluation of `exp`, `log`, `sin`, `cos`, or positive square root.
Exact uniform, exponential-clock, and Gaussian draws with known
parameters are charged random primitives. Complex arithmetic is a fixed
number of real operations. Fixed public constants are available.

There is no free known-function, PDE, derivative, transform, or integration
oracle. Exact continuous random locations, arbitrary real magnitudes,
and integer/address word sizes are idealized just as in D33. Every
evaluation of a constructed function below is an actual finite program.

There exist constants `C<infinity` and a finite exponent `A`, depending
on fixed `d,s,kappa`, and Borel almost-surely halting algorithms such that
for every real `T>=2`,

    sup_(v in V) (E|Y_T(v)-S_T^kappa v(x*)|^2)^(1/2) <=1/8,
    sup_(v in V) E Work_T(v)
                  <=C exp(gamma T)(1+T)^A,
    gamma=d/(s+d/2)=2d/(2s+d).                         (1.1)

They have the all-seed unknown-query cap in (9.2). A fixed-cost
deterministic construction in Section 11 covers the bounded interval
`0<=T<=2`, so an upper bound with RMS at most `1/4` can also be stated
for every `T>=0` after increasing `C`.

All constants can be public overestimates. No uniformity as
`kappa` tends to zero, or as `d,s` vary, is asserted. In particular the
positive-diffusion hypothesis is essential to the fixed-time analytic
compression used here.

## 2. Dependencies, scope of reading, and the proof plan

The following source hashes were computed during this task.

| Source in this run | SHA256 |
| --- | --- |
| `reviews/R10b-finite-burnin-derivative-sampling.md` | `23683587539ef2905e0679100325808ae3f6353a3782a4bb362b2d24252034f0` |
| `reviews/T68-finite-burnin-sampler-independent-audit.md` | `442b446ae523b220e34ddadcf8c23b181ce60104100fd27c7e8027524840ed9f` |
| `reviews/T70-known-base-phase-work-feasibility.md` | `46666ef19d4d66eb6196c486df726b6cc623f401fb717d925c82806bd3a905d6` |
| `reviews/T74-known-base-phase-work-independent-audit.md` | `0cc8fea39eeee5f1f43f21fa3d29a52525f26fed767ff0e7b1677c1fc8d2dd1c` |
| `reviews/T69-stable-graph-sampler-feasibility.md` | `ff537ca6679fdefeefe9c08990194a09f6a2cec23460e1656876e7fdf8a37d9b` |
| `04w-signed-ideal-work-exponential-rate.md` | `7eb75d72f0185a75f5823e9fb5175b9033e92a408d89ea268653c4d798f96a79` |

R10b and T68 were read in full. The used interpolation and solver
arguments in T70 Sections 1--7 and T74 Sections 1--9 were read, together
with T74's subsequent stored-coefficient and totality explanations.
T69's statement and interfaces were inspected for context only. Its
stable-graph sampler is not a premise. The D29/D30/D32/D33 ledger entries,
04v, 04w, run context/checkpoint, repository instructions, README, and
math-auto-research defaults/routing/execution/profile were inspected.
No inaccessible earlier session is claimed to have been read.

There are two inherited, independently audited constructive ingredients:

1. T70/T74's paid Gevrey-2 interpolant and finite known-profile solver.
   Sections 3--4 give the precise fixed-`kappa` extension needed here;
   graph-root computations from those files are unnecessary.
2. R10b/T68's rate-two fixed-time derivative tuple sampler. Section 5
   checks the diffusion change, bounded Fourier root weights, query cap,
   and shared-sample vector implementation.

The new interface is Section 7's explicit saturation and its quantitative
composition estimate. Once it is proved, the error composition is the
ordinary real maximum principle, not an asymptotic phase approximation.

## 3. Paid interpolation and a known-profile solver for fixed kappa

Use the exact Gevrey partition/stencil interpolation from T70/T74. With
`k>=k0`, precisely `k^d` uniform-grid acquisitions determine a real smooth
periodic `g` satisfying

    ||g||inf<=3/4,       ||v-g||inf<=Cint k^(-s),
    ||partial^alpha g||inf
                      <=B0(C0 k)^|alpha| (alpha!)^2.  (3.1)

Here and below `alpha!` is the product of coordinate factorials. The
constants and `k0` depend on `d,s`; increase `k0` until
`Cint k0^(-s)<=1/4` and `k0>=2s`.

For clarity, this is a chosen representation, not a Gevrey assumption
on the unknown datum. The cutoff is

    beta(t)=exp(-1/(1-t^2)) if |t|<1, and zero otherwise,

normalized by its integer translates and tensorized. A fixed tensor
degree-`s-1` stencil polynomial is attached to each grid node. It
reproduces every total-degree-`s-1` Taylor polynomial. Comparing to the
Taylor polynomial at an evaluation point shows that only total-order
derivatives through `s` of `v` are needed for the error in (3.1).
The fixed-support Gevrey weights supply its all-order derivative bound.

There are a fixed number of coefficients per grid node. Computing them
costs `O_(d,s)(k^d)`. Given `x`, floors and modular indexing locate a
bounded number of overlapping cells; their stored polynomials and bump
weights are evaluated in `O_(d,s)(1)` charged operations. The bump's
support test precedes its division, and the translate denominator is
bounded below by `exp(-4/3)`. Thus the exact lookup has uniform cost

    Gg<=C_(d,s).                                      (3.2)

The following version of the audited solver separates the scale `R`
from the physical diffusivity `kappa`.

**Known-profile lemma.** Fix `d,kappa>0,B,c>0`. Suppose a known real
periodic `q` has `||q||inf<=1` and

    ||q||_(G_(c/R))<=B,       R>=1,
    ||q||_(G_rho):=sum_alpha rho^|alpha|
                              ||partial^alpha q||inf/(alpha!)^2.

If exact evaluation of `q` costs at most `Wq`, then, for `S,P>=1`,
a deterministic finite elementary-operation program returns an indexed
real Fourier polynomial `U` with

    ||U-S_S^kappa q||inf<=exp(-P),
    Work<=C R^d E^a0(1+Wq),
    E=1+P+S+log(R+1),       a0=2d^2+20d+50.           (3.3)

All cutoffs and loop maxima are public. Constants can depend on fixed
`d,kappa,B,c`. The bound also counts evaluation of the returned polynomial
at one specified point. A previously indexed Fourier input can instead
be copied and padded with its actual array-access cost.

Here is the fixed-diffusivity verification of (3.3), using the audited
proof rather than postulating a new PDE primitive.

### 3a. Uniform spatial tails and spatial algebra

The Gevrey norm is a Banach-algebra norm: normalized product-rule
coefficients are `1/binom(alpha,beta)<=1`. The semigroup
`exp(t kappa Delta/2)` contracts each derivative sup norm for real
`t>=0`. Thus the same local mild fixed point as T70/T74 gives
`||S_t^kappa q||_(G_(c/R))<=2B` up to a fixed positive time `h0`.
Fourier integration by parts and optimization in a coordinate with
largest frequency give

    sum_(|n|inf>H)|uhat(t,n)|
                   <=C R^d exp(-c1 sqrt(H/R)),   0<=t<=h0.

Comparison gives `||S_t^kappa q||inf<=1` at every real time. The
periodized heat kernel shifted by an imaginary vector `y` has `L1`
bound `exp(|y|^2/(2 kappa t))`. On the varying tube
`|Im z|_2<a sqrt(kappa t)`, shift the convolution contour at time `r`
to `y_r=sqrt(r/t)y`. Then

    |y-y_r|<=a sqrt(kappa)(sqrt(t)-sqrt(r))
             <=a sqrt(kappa(t-r)).

The heat map between these tubes has norm at most `exp(a^2/2)`.
The cubic mild map is consequently a contraction in a fixed tube-norm
ball for a fixed short time `h1<=min(h0,1)`. Restricting to the real
torus identifies this holomorphic solution with the actual solution.
Restarting from the actual bounded profile at `t-h1` gives a uniform
strip width `a sqrt(kappa h1)` at every `t>=h1`. Hence

    sum_(|n|inf>H)|uhat(t,n)|<=C_kappa exp(-c_kappa H),
                                                        t>=h1.

Thus on the whole real interval `[0,S]` the spatial tail is bounded by

    t_H=C R^d exp(-c1 sqrt(H/R))
                          +C_kappa exp(-c_kappa H).   (3.4)

The strip width is allowed to shrink with `kappa`. Nothing here uses
the sign of `2*pi^2*kappa-1`.

Rectangular Fourier projection has the unchanged norm bound
`Lambda_H=C_d(1+log(H+1))^d`. The Galerkin equation is

    U'=A_H U+P_H(U-U^3),       A_H=(kappa/2)Delta.

Comparing it to the actual solution until its norm first reaches two
gives, for coefficient-initialization error `epsilon0`,

    ||U(t)-S_t^kappa q||inf
              <=(epsilon0+t_H) exp(11 Lambda_H S).   (3.5)

Real heat contraction is the only heat estimate used in this comparison.
Making the right side at most `min(1/4,exp(-P)/4)` closes the bootstrap;
no spectral maximum principle is asserted.

Set `H=ceil(C_kappa R E^(2d+8))`, increasing the fixed constant as
necessary. Then `log(H+1)<=C_kappa E`, while the tail exponent
`sqrt(H/R)` dominates `log R+P+Lambda_H S`. The second term of (3.4)
is also absorbed. Initialization uses a power-of-two grid at least
`4H` in each coordinate, actual evaluations of `q`, and a tensor FFT.
The alias error in the retained coefficient `l1` norm is bounded by
one Fourier tail beyond grid size minus `H`. For cubing, a
power-of-two grid strictly larger than `6H` computes the projected
cubic exactly. Every transform, twiddle, padding operation, and array
access costs `O_d(H^d log(H+1))` operations. These are finite algorithms.

### 3b. Time analyticity, finite panels, and stability

For a complex time in a fixed forward sector,

    ||exp(z kappa Delta/2)||_(inf->inf)
                      <=(sec(arg z))^(d/2).

The sector norm is unchanged by positive `kappa`. The bounded Galerkin
trajectory therefore has a holomorphic forward sector of radius
`c_d/Lambda_H` from each real starting point. At time zero a genuine
disk crossing the negative real axis has the separately justified radius

    a_H=c_d/(C_d kappa H^(d+2)+Lambda_H),              (3.6)

using the finite-dimensional generator bound. Its logarithmic reciprocal
is still `O_kappa(1+log(H+1))`.

With time degree `p=ceil(C_kappa E^(d+4))` and Lobatto interpolation
bound `beta_p=C(1+log(p+1))`, choose
`h=c/(Lambda_H beta_p)`. Start with a panel of length
`min(a_H/16,h/16)`, double to an endpoint in `[h,2h)`, and balance the
remaining panels with lengths in `[h/2,h]`. The explicit parameter-two
ellipses in T74 C2 lie inside the initial disk or the appropriate
forward sector. Their construction is unaffected by (3.6). The count is

    n_pan<=C_kappa[1+log(H+1)+log(p+1)+S Lambda_H beta_p]
                    <=C_kappa E^(d+2).              (3.7)

On each ellipse the projected forcing is bounded by `C_d Lambda_H`.
Its Lobatto interpolation error is at most `C_d Lambda_H 2^(-p)`.
The finite semigroup-convolution nodal map has contraction factor
`49 ell Lambda_H beta_p<=1/4` on the radius-four real nodal ball.
Starting from linear heat values and performing a public `Citer p`
Picard iterations gives the per-panel fixed-point defect `C 4^(-Citer p)`.
The endpoint recurrence from T74 C3 has accumulated bound

    exp(C S Lambda_H beta_p)
       [C S Lambda_H 2^(-p)
               +C n_pan 4^(-Citer p)+n_pan epsilon_alg].

Choosing the fixed constants makes this smaller than `exp(-P)/4` and
`1/4`. This simultaneously closes the numerical-start bootstrap.
The sensitivity is not `exp(C kappa H^2 S)` and is not exponential
in the number of startup panels. The real heat factors are integrated
exactly. In the exact model here `epsilon_alg=0`.

### 3c. Diffusion-dependent scalar weights and their cost

For a mode `n` and panel length `ell`, put
`z=2*pi^2*kappa*|n|^2*ell`. Expanding a Lobatto cardinal polynomial
reduces the convolution weights to

    I_m(z,theta)=integral_0^theta exp(-z(theta-r)) r^m dr.

For `z>0`, the exact finite recurrences are

    I_0=(1-exp(-z theta))/z,
    I_m=theta^m/z-(m/z)I_(m-1).

For the zero mode use `theta^(m+1)/(m+1)`; at `theta=0` use zero.
Every nonzero mode has `z>0` because `kappa>0`. Public cardinal
denominators are also nonzero. Thus the recurrence uses only listed
primitives. It can be ill conditioned in floating arithmetic; exact
operation counting does not assert finite-precision stability.

Writing `D=(2H+1)^d`, all cardinal and scalar-weight construction on a
panel costs `O(Dp^3)`; one Picard step costs
`O(Dp^2+pD log(H+1))`. With `O(p)` steps and (3.7) panels the work is

    C n_pan D[p^3+p^2 log(H+1)]
                    +C D[log(H+1)+Wq].              (3.8)

The safe `a0` in (3.3) bounds (3.8). One terminal evaluation of the
indexed polynomial costs `O_d(D)` charged trigonometric operations and
arithmetic and is absorbed. This accounts for each modification of the
audited solver caused by `kappa`. The solver lemma is thus available for
every fixed positive diffusivity, with exactly its stated data interface.

## 4. A fixed burn-in has a small Fourier representation

Take `L=1`. For every promised `v`, scalar comparison gives

    ||S_1^kappa v||inf<=a1=(1+3 exp(-2))^(-1/2)<7/8. (4.1)

For example the last inequality follows from `exp(2)<9<49/5`.
This bound is independent of `kappa`. The fixed positive analytic strip
in Section 3a also gives public `A_kappa>=1,b_kappa>0` with

    ||(I-P_N)S_1^kappa v||inf
                <=A_kappa exp(-b_kappa N),           (4.2)

uniformly over the whole promised class. The same smoothing proof
applies to `g`, whose norm is at most `3/4`.

Use one representative of each pair `{n,-n}` in the nonzero box
`|n|inf<=N`, chosen by the sign of the first nonzero coordinate. The
real basis consists of the constant and the corresponding cosines and
sines. It has exactly

    K=(2N+1)^d

members `b_l`, each of sup norm at most one. Its real coefficient
functionals are

    F_0(q)=integral_X S_1^kappa q(x) dx,
    F_(n,c)(q)=2 integral_X S_1^kappa q(x) cos(2*pi*n.x) dx,
    F_(n,s)(q)=2 integral_X S_1^kappa q(x) sin(2*pi*n.x) dx.

Write all of them as `F_l(q)=integral psi_l S_1^kappa q`, where
`||psi_l||inf<=2`. The reconstruction is
`P_N S_1^kappa q=sum_l F_l(q)b_l`.

The constant coefficient of the true target lies in `[-1,1]`; every
other real coefficient lies in `[-2,2]`. For an indexed complex array,
these coefficients are its zero coefficient, `2 Re uhat(n)`, and
`-2 Im uhat(n)`, respectively. No integration primitive is required
to extract the known base coefficients from a solver output.

## 5. Derivative tuple sampling with Fourier weights

Put `e=v-g` and `delta=Cint k^(-s)`. The segment from `g` to `v`
lies in the open unit ball. R10b/T68's construction extends as follows.

Each particle splits into three at rate two, runs to time one, and
has an edge endpoint increment of covariance `kappa times edge_length`
in each coordinate, wrapped onto the torus. The children begin at the
same sampled branch endpoint. Their subsequent randomness is independent.
The vertex polynomial remains

    M(a,b,c)=(a+b+c-abc)/2.

Its first-branch equation has generator `kappa Delta/2` and reaction
`2(M(u,u,u)-u)=u-u^3`. This checks the actual diffusion and reaction
normalization without importing a convention from another paper.

The population law is unchanged: `N_t` jumps from `n` to `n+2` at
rate `2n`. In particular

    E N_1=exp(4),
    E N_1^r<=exp(2(3^r-1)),                 integer r>=1. (5.1)

The stopped-population argument in T68 proves nonexplosion and every
displayed moment. These constants are independent of `kappa`.

For a finite tree, its leaf polynomial is multiaffine and bounded by one
on the whole leaf cube. Every mixed partial in distinct leaf labels has
absolute value at most one by the `2^j`-corner identity. The actual
`j`th derivative is the sum over ordered injections of its `j` direction
labels into distinct leaves. Derivative-expectation interchange in
`C(X)` is dominated by the finite moments `E N_1^(j+1)` and
`E N_1^(j+2)` as in T68; changing only the Gaussian variances does not
affect that argument.

Sample a uniform root `U` and a complete finite tree. If there are at
least `j` leaves, choose a uniform ordered injection `I` into them and
compute its selected partial `C_I` by the corner identity. The scalar
tuple output is

    Z_j=(N_1)_j C_I product_(a=1)^j
                              [v(X_(I_a))-g(X_(I_a))].

Use zero if the population is smaller than `j`. For every retained
coefficient use the same completed sample and return

    Z_(j,l)=psi_l(U) Z_j.

It follows that

    E Z_(j,l)=D^j F_l(g)[e,...,e],
    E|Z_(j,l)|^2<=V_j delta^(2j),
    V_j=4 exp(2(3^(2j)-1)).                           (5.2)

The uniform root, bounded weight, and population moment justify all
spatial integrations. The same measure argument bounds the actual
derivative operator by

    ||D^j F_l(q)||op<=B_j,
    B_j=2 exp(2(3^j-1)),          ||q||inf<1.          (5.3)

Shared samples create correlations between coefficients. No later
argument assumes coefficient independence.

There are at most `j` unknown acquisitions per sample. First generate
the complete tree, select the tuple, and compute the coefficient using
known `g` values. Only then query its selected original-time `v` values.
Each acquisition is charged even if two leaves have the same position.
If preparation fails to terminate on a null seed, no acquisition for
that sample has yet occurred.

The tree has `(3N_1-1)/2` nodes. Its clocks, `d`-coordinate increments,
positions, stack/array accesses, leaf caching, partial Fisher--Yates
selection, and at most `2^j` upward coefficient passes cost
`C_j(d+1+Gg)N_1` operations. Integer selection may use a continuous
uniform draw and floor, with the endpoint assigned a valid index.
Generating all Fourier weights and updating the `K` accumulators costs
an additional `O_d(K)` operations per sample. Hence (3.2) and (5.1) give

    E Work(one shared vector sample of order j)<=C_(j,d,s)(1+K). (5.4)

This counts a concrete calculation, not an oracle for a derivative or
for any evolved value. All orders below are fixed as `T` varies.

## 6. Coefficient estimation and public parameters

For `T>=2` let

    S=T-1,       Lchi=25,
    epsilon=exp(-S)/(16 Lchi),
    N=max(1,ceil((S+log(32 Lchi A_kappa))/b_kappa)),
    K=(2N+1)^d,
    qrate=s+d/2,       J=ceil(1+d/(2s)),       m=J-1.

Then `N=O_kappa(1+T)` and the target tail (4.2) is at most
`epsilon/2`. Fix the public positive constant

    Cstar=1+sum_(j=1)^m sqrt(V_j) Cint^j/j!
                            +B_J Cint^J/J!.

Choose

    eta=epsilon/(4K),
    k=max(k0,ceil((4 Cstar K/epsilon)^(1/qrate))),
    M=k^d.                                           (6.1)

The positive power is evaluated by `exp(log(.)/qrate)` in the declared
model. Every integer loop bound is therefore a public finite quantity.
In particular `log k=O_(d,s,kappa)(1+T)`.

Apply (3.3) to the paid `g`, with scale `R=k`, time one, and
`Pbase=log(2/eta)`. The Gevrey norm is uniformly bounded by (3.1).
Increase the public spatial-cutoff constant, or take its maximum with
`N`, so the returned indexed array contains all requested modes.
This retains the same work estimate. The solver output `U_base` obeys

    ||U_base-S_1^kappa g||inf<=eta/2,
    |c_l^base-F_l(g)|<=eta,
    Work_base<=C k^d(1+T)^a0.                         (6.2)

The second inequality uses the coefficient functional norm at most two.
Reading the `K` coefficients is charged. The complete base solve makes
no additional unknown acquisitions.

For each `j=1,...,m`, generate `M` independent copies of the shared
vector sample (5.2), using fresh input-independent seeds. Define

    c_l^raw=c_l^base+
                  sum_(j=1)^m (1/(j! M)) sum_(r=1)^M Z_(j,r,l).

Taylor's formula along `g+theta e`, (5.3), and `Js>=s+d/2` imply

    |F_l(v)-sum_(j=0)^m D^jF_l(g)[e^j]/j!|
                                      <=B_J delta^J/J!.

Independence within each order's average and Minkowski's inequality,
without any independence across Fourier modes, now give

    ||c_l^raw-F_l(v)||_(L2(Omega))
       <=eta+sum_(j=1)^m sqrt(V_j) Cint^j k^(-js-d/2)/j!
                                      +B_J Cint^J k^(-Js)/J!
       <=eta+Cstar k^(-qrate)
       <=epsilon/(2K).                               (6.3)

This includes the bias of the known-base solve and the Taylor remainder.
The fixed high derivative order is exactly what makes the latter no
larger than the sampling scale. No unknown derivative is acquired.

## 7. Clipping, explicit saturation, and uniform Gevrey control

First project `c_0^raw` onto `[-1,1]`, and each other `c_l^raw` onto
`[-2,2]`; call the results `c_l`. These intervals contain the true
coefficients. Interval projection is nonexpansive relative to any point
of the interval, so (6.3) remains valid for `c_l`. The projection may
introduce bias; unbiasedness is no longer required after (6.3).

Set `p(x)=sum_l c_l b_l(x)`. On every completed sample path,

    ||partial^alpha p||inf<=2K(2*pi*N)^|alpha|.        (7.1)

The zeroth-order norm can grow like `K`; it is not presumed bounded
uniformly in `T`. Hard scalar clipping of `p(x)` would not provide the
smooth initialization needed by (3.3). Use the following fixed smooth
map instead.

### 7a. A primitive-evaluable saturating function

Let `a=7/8`, `b=15/16`, and for `0<t<1` put

    phi(t)=exp(-1/t),
    w(t)=phi(t)/(phi(t)+phi(1-t)).

Extend `w` by zero for `t<=0` and by one for `t>=1`. For `z>=0` define

    chi(z)=z,                              0<=z<=a,
    chi(z)=z+(b-z)w((z-a)/(b-a)),           a<z<b,
    chi(z)=b,                              z>=b,

and extend oddly to negative `z`. The branch tests precede every
division. The interior denominator is at least `exp(-2)`, because one
of `t,1-t` is at least `1/2`. Thus evaluation uses a fixed number of
arithmetic operations, comparisons, and exponentials for every real
argument, with no integration or special-function oracle.

The function is the identity on `[-7/8,7/8]` and has range
`[-15/16,15/16]`. The extension is smooth: `w` is flat at zero and
`1-w` is flat at one, matching the identity and constant pieces to all
orders. There is no absolute-value singularity at zero, where the
function is exactly the identity.

For `0<t<1`,

    0<=phi(t)<=exp(-1),
    0<=phi'(t)<=4 exp(-2),
    0<=w'(t)<=8 exp(1)<24.

The middle derivative of `chi` is `1-w(t)+(1-t)w'(t)`, between zero
and 25. Its other derivatives of first order are zero or one. Therefore

    |chi(z)-chi(z')|<=25 |z-z'|                       (7.2)

globally, establishing the value `Lchi` used in Section 6.

There are fixed public `Achi,Cchi>=1` such that

    sup_(z in R)|chi^(r)(z)|<=Achi Cchi^r(r!)^2,
                                                   integer r>=0. (7.3)

To verify this quantitative statement, Cauchy's estimate for
`exp(-1/z)` on a disk of radius `c t` about positive `t` gives
`r!(c t)^(-r)exp(-c'/t)`. Maximizing over `t` bounds it by
`A C^r(r!)^2`; all derivatives vanish at the zero endpoint. On
`[0,1]`, sum and product preserve such a bound. For the reciprocal of
the denominator, differentiate `D D^(-1)=1`; after normalizing by
`(r!)^2`, the inductive convolution coefficients are
`1/binom(r,l)`. Enlarging the geometric constant makes their geometric
sum at most one, as in T74 Section 3. Affine rescaling, the fixed
linear factor `b-z`, the matching pieces, and odd reflection then give
(7.3) with constants independent of any data, `N`, or `T`.

### 7b. Composition with bounded coefficients has polynomial scale

Define the actual continuation profile

    qhat=chi composed with p.

It always satisfies `||qhat||inf<=15/16`. A direct derivative estimate
shows that it has the precise quantitative Gevrey interface required
by (3.3), uniformly over all clipped coefficient arrays.

For a multi-index `alpha` of total order `n>=1`, the finite-jet
Faà di Bruno identity is

    partial^alpha(chi(p))
      =alpha! sum_(r=1)^n chi^(r)(p)/r!
        sum_(beta_1+...+beta_r=alpha, |beta_i|>=1)
                              product_i partial^beta_i p/beta_i!.

Allowing zero multi-indices in the inner nonnegative bound shows

    sum_(beta_1+...+beta_r=alpha, |beta_i|>=1)
                              1/(beta_1!...beta_r!)
                       <=r^n/alpha!.

Combining (7.1) and (7.3) consequently gives

    ||partial^alpha qhat||inf
       <=Achi(2*pi*N)^n sum_(r=1)^n (2 Cchi K)^r r! r^n.

Use `r!<=n!`, `r^n<=n^n<=exp(n)n!`, `n<=2^n`, and
`n!<=d^n alpha!`. The result is

    ||partial^alpha qhat||inf
             <=Achi(Cchi,d N K)^n (alpha!)^2.        (7.4)

Here `Cchi,d` is a fixed public constant; for instance
`8*pi*exp(1)*Cchi*d^2` suffices. The zeroth derivative is bounded by
`b<=Achi`. Thus, with `Rhat=N K>=1` and a fixed sufficiently small
`chat>0`,

    ||qhat||_(G_(chat/Rhat))<=Achi 2^d.               (7.5)

This is a uniform norm bound, not a random norm estimate. Since
`N=O(1+T)` and `K=O((1+T)^d)`, the inverse Gevrey scale `Rhat`
is polynomial in `T`.

Finally, evaluation of `p` uses its `K` indexed real coefficients,
`d`-term dot products, and sine/cosine primitives. Evaluation of `chi`
has fixed cost. Consequently

    Work(qhat(x))<=C_d K                             (7.6)

uniformly in `x`, the horizon, and the completed random transcript.
There is no free saturated-function evaluator in this assertion.

## 8. Exact risk allocation and deterministic continuation

Minkowski applied to the finite coefficient sum, (4.2), and (6.3) gives

    (E||p-S_1^kappa v||inf^2)^(1/2)
       <=||(I-P_N)S_1^kappa v||inf
                           +sum_l ||c_l-F_l(v)||L2
       <=epsilon/2+K epsilon/(2K)=epsilon.           (8.1)

By (4.1), the exact target is in the identity interval of `chi`.
Hence (7.2) yields

    (E||qhat-S_1^kappa v||inf^2)^(1/2)
                         <=Lchi epsilon=exp(-S)/16. (8.2)

For any two real Allen--Cahn solutions `u,w`, their difference solves

    (u-w)_t=(kappa/2)Delta(u-w)
                    +[1-(u^2+uw+w^2)](u-w).

The bracket is at most one since `u^2+uw+w^2>=0`. The maximum
principle therefore proves the actual flow estimate

    ||S_t^kappa f-S_t^kappa h||inf
                         <=exp(t)||f-h||inf.         (8.3)

This is the rate-one comparison bound, not the absolute Lipschitz
constant of the reaction on a chosen interval. All profiles used here
are bounded by one, so their global real solutions exist and comparison
applies. In particular (8.2)--(8.3), with `t=S=T-1`, give RMS at most
`1/16` between `S_S^kappa qhat(x*)` and `S_T^kappa v(x*)`.

For each completed coefficient array, run (3.3) on the actual known
`qhat`, with scale `Rhat`, uniform bound (7.5), evaluator (7.6), time
`S=T-1`, and precision parameter

    Pout=T+log(16).

It returns a Fourier polynomial `U_out` with deterministic conditional
sup error at most `exp(-T)/16`. This bound and its operation bound are
uniform over every possible clipped coefficient array, regardless of
how large the raw estimates were. Return `Y_T=U_out(x*)`, optionally
projected onto `[-1,1]`. That projection only decreases error relative
to the actual target, which lies in this interval.

Minkowski now gives the complete risk budget

    ||Y_T-S_T^kappa v(x*)||L2
        <= exp(S)Lchi[epsilon/2+K epsilon/(2K)]
                                               +exp(-T)/16
        <=1/16+exp(-T)/16<=1/8<1/4.                 (8.4)

The first term includes the Fourier tail, the base-solver bias, the
finite-order Taylor remainder, and all coefficient sampling errors.
The second term is the fully counted final PDE solve. There is no
phase proxy error, branch-classification error, unspecified norm test,
or probabilistic good event omitted from this budget.

## 9. Work and hard query cap

The coarse interpolation and base solve cost
`C k^d(1+T)^a0`. There are `M=k^d` shared vector samples at each
of the fixed `m` derivative orders. Their total expected work is
`C k^d(1+K)` by (5.4). Clipping, coefficient-array allocation, and
initial frequency enumeration cost `O_d(K)`.

For the final solve, `Rhat<=C(1+T)^(d+1)`,
`Wqhat<=C(1+T)^d`, and `Eout<=C(1+T)`. Its deterministic conditional
work, including the final point evaluation, is at most

    C(1+T)^(a0+d^2+2d).

There is no random derivative-size parameter in this cost. Combining
these observations gives

    sup_v E Work_T(v)
       <=C k^d(1+T)^a0+C k^d(1+T)^d
                                  +C(1+T)^(a0+d^2+2d). (9.1)

The only unknown acquisitions are the coarse grid and the selected
residual tuples. On every seed path, including a null nonterminating
preparation path,

    Q_T <=k^d+sum_(j=1)^m j M
         =[1+J(J-1)/2] k^d.                          (9.2)

Repeated points are included in this count. Sharing the Fourier weights
uses the same tuple values and does not multiply (9.2) by `K`.

From (6.1), with constants absorbing `k0` and the ceiling,

    k^d<=C exp(gamma T) K^(d/qrate)
         <=C exp(gamma T)(1+T)^(d^2/qrate).           (9.3)

Equations (9.1)--(9.3) prove (1.1). One deliberately loose integer
choice of the final polynomial exponent is

    A=a0+d^2+2d+ceil(d^2/qrate)+2.

This is not an optimized exponent. The query cap itself has the
polynomial overhead in (9.3). Nothing in this proof removes it or
establishes an exact `Theta(exp(gamma T))` query theorem for all
diffusivities.

## 10. Borel rules, termination, and off-promise transcripts

Grid sampling, interpolation, FFTs, scalar-weight construction, clipping,
and both solver programs have public finite iteration counts. Their
elementary branches are Borel. Cardinal denominators are public nonzero
numbers; nonzero-mode convolution divisions have positive `z`; cutoff
and saturation divisions are made only in the guarded interiors with
positive denominators. Zero-length Gaussian increments, if encountered
at an endpoint, are assigned the zero vector without a square-root
call. No convergence test or norm oracle controls a solver loop.

One countable product of input-independent random primitives supplies
the finitely many required tree samples. For each one, the population
is nonexplosive, its finite genealogy and all endpoint/query locations
are Borel functions of the seed, and its expected work is finite.
There are finitely many samples at each fixed `T`, so the whole
algorithm halts almost surely and has the expected work in (9.1).
No tree-size truncation or estimator cutoff changes the mean in (5.2).

To interpret the output as a Borel random variable, assign zero on
the null set of nontermination. This does not assert that the program
detects that set. Crucially, the entire preparation for any tuple occurs
before its acquisitions, so a failure to finish preparation does not
invalidate the all-seed cap (9.2), even after earlier samples finished.

All promised input functions are continuous, making their evaluations
at Borel random locations measurable. A completed sample can have an
arbitrarily large but finite raw coefficient. The hard coefficient
projections make the continuation representation obey (7.5)--(7.6)
on every such path. Thus neither expected cost nor validity of the
continuation relies on an unstated high-probability event.

For total finite-transcript rules beyond the promised smoothness class,
coarse responses may first be projected onto `[-1/2,1/2]`, which leaves
every promised transcript unchanged. Interpolation remains a finite
formula and every fixed-count solver step is finite algebra on finite
real arrays. An off-promise base profile can invalidate accuracy and
bootstrap estimates, but not the fixed program or its Borel rules.
If desired, project later acquired responses onto this same interval;
again this does not alter any promised run. Tree preparation is input
independent, so almost-sure halting continues to hold. No additional
promise about the original datum's higher derivatives has been used.

## 11. Optional bounded-horizon completion

The asymptotic theorem needs only `T>=2`, but a uniform finite-cost
patch for `0<=T<=2` is available without a new unknown-input model.
Choose one fixed large grid `k_b`, independent of `T`, with
`exp(2) Cint k_b^(-s)<=1/32`, and construct its same paid `g_b`.
The actual flow difference between `g_b` and `v` is then at most
`1/32` throughout this time interval by (8.3).

The spatial-tail and Galerkin bootstrap in Section 3a are uniform on
`[0,2]`, including zero, for this fixed quantitative Gevrey input.
Choose a fixed cutoff and a fixed padded initialization grid so that
the Galerkin approximation, including its initialization error, stays
within `1/32` of `S_t^kappa g_b` for every `t<=2`. Their sizes are
constants depending on `d,s,kappa`, not on `T` or the unknown datum.

This fixed-dimensional ODE is polynomial. On a fixed neighborhood of
its already bounded real trajectories, its vector field, first
derivative, and the trajectory's second derivative have public finite
bounds, since the diffusion matrix, Fourier projection, and cutoff
are fixed. Explicit Euler with a fixed public number `n_b` of steps
of length `T/n_b` has error at most `C/n_b` uniformly in `0<=T<=2`:
the local Taylor defect is `C(T/n_b)^2`, and the usual finite
Gronwall recurrence bounds their sum. Choose `n_b` large enough for
error at most `1/32`. A bootstrap inside the same fixed neighborhood
justifies these bounds for its numerical iterates.

All its projected cubics use the same exact padded finite transforms;
the number of steps is fixed, even at `T=0`. The resulting scalar
output has deterministic error at most `3/32<1/4`, a fixed hard
query cap, and fixed work. This supplies the bounded-horizon extension
asserted in Section 1, without needing the `S>=1` panel construction
on vanishingly short intervals.

## 12. Audit targets, attribution, and final provenance

The material checks for an independent reviewer are:

- The known-profile solver extension in Section 3: the strip scales
  with `sqrt(kappa)`, the initial disk contains the factor `kappa`,
  and the exact convolution eigenvalues are `2*pi^2*kappa*|n|^2`.
- The bounded real Fourier coefficient normalization, including the
  factor two and the minus sign for the imaginary Fourier coefficient.
- The shared-root tuple estimator, its actual derivative identity and
  `j`-call cap, with unchanged population moments after rescaling the
  Brownian increments.
- The globally defined primitive saturation, the uniform all-order
  composition bound (7.4), and its actual `O(K)` evaluation cost.
- The unconditional coefficient error estimate and rate-one PDE
  comparison, giving the explicit total budget (8.4).
- Every deterministic setup cost, the finite expected random work, and
  the polynomial overhead retained in both (9.1) and (9.3).

I opened An--Henderson--Ryzhik's primary text and inspected its
diffusion convention and Section 3.1 majority construction. The
Allen--Cahn voting representation is established prior work, there
attributed to Etheridge--Freeman--Penington. Its normalization differs
from ours, so Section 5 checks our generator and rate directly.
[Primary AHR text](https://arxiv.org/html/2209.03435).

I also opened Trefethen's one-page Chebyshev-series note, including its
Bernstein-ellipse geometric approximation principle and warning about
monomial conditioning. The parameter-dependent PDE solver bound here
uses the explicit audited T70/T74 construction and Section 3's checks;
the note alone is not a work theorem.
[Primary author note](https://people.maths.ox.ac.uk/~trefethen/outline3_2017.pdf).

These were bounded attribution checks, not a priority search. The
positive-diffusion upper bound may be useful, but no significance,
novelty, prize, or practical-computing conclusion is inferred.

Research routing was explicitly requested as `gpt-6-astra/max`; the
worker's backend is not independently attested by its available tools.
This task performed source/config/context reads, source hashing, the
two primary-source checks, the displayed conventional derivations, and
one new proof-file write. One attempted read used an incorrect 04v
filename and returned no file; the class/interface were checked in 04w
and the actual claim entries, and the correct 04v file was subsequently
located and read in full. No result was inferred from that failed read.

Only this T81 file was written. Existing claims, frozen proofs, canvas,
code, numerics, and Lean were not edited. No solver implementation,
test, numerical PDE solve, or Lean build was run. Final file hashing
is reported in the handoff rather than embedded in the file itself.
Independent review and root shared-model/source correspondence remain
required before the candidate is promoted to an accepted theorem.
