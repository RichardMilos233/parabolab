# T94: odd-power long-horizon query and paid-work feasibility

Date: 2026-09-29. Conventional proof candidate, pending independent root
review. Requested research routing: `gpt-6-astra/max`; this worker cannot
independently attest its actual backend or reasoning effort.

**Verdict: feasible for every fixed normalized odd power.** The proof
below gives the same full signed input class, scalar point-value oracle,
strong whole-profile RMS loss, and exact query order as 04z, for
`f(u)=u-u^(2p+1)` with every fixed integer `p>=1` and every fixed
`kappa>0`. Paid work retains a polynomial factor in the horizon.

For `f(u)=a u-b u^(2p+1)`, the corresponding result holds after the
explicit amplitude, time, class, and tolerance scaling in Section 11.
An unchanged physical class and unchanged absolute tolerance do not
admit such a theorem for all `a,b>0`; Section 11 gives a zero-query
counterexample. These two statements must not be conflated.

This is a new proof candidate, not an amendment to the frozen cubic
theorem, a new accepted claim, a Lean result, or an implementation.

## 1. Exact normalized theorem and model

Fix integers `d,s,p>=1`, put `D=2p+1`, and fix `kappa>0`. On
`X=(R/Z)^d`, with normalized volume, write `S_t` for the actual flow

    u_t=(kappa/2) Delta u+f(u),       f(u)=u-u^D.

Use exactly 04z's class

    V={v smooth periodic real: ||v||inf<=1/2,
       max_(|alpha|<=s)||partial^alpha v||inf<=1,
       min v<0<max v}.

Smoothness above order `s` has no common bound. In particular, no
analytic-radius assumption, basin promise, positive mean margin, or
restriction on the number of unstable spatial modes is imposed.

The only acquired unknown information is an exact scalar value `v(x)`.
Acquisitions include preprocessing and repeated points. Admissible
measurable rules may be biased, adaptive, and randomized, with an
input-independent seed and almost-sure halting for each input. For a fixed prescribed
point `x*`, let `Q_point(T)` be the infimum of worst-input expected
queries at RMS tolerance `1/4`. Let `Q_profile(T)` be its analogue for
finite explicitly indexed real Fourier outputs, with loss

    sup_(v in V) E ||U_T-S_T v||inf^2 <=1/16.

The spatial supremum is inside the expectation. Auxiliary arithmetic
is free for these two query quantities. Let `W_point,W_profile` be the
corresponding infima of worst-input expected paid work at the same
respective tolerance. Paid-work quantities charge
each query, arithmetic operation, comparison, floor/ceiling, integer
and index operation, stored-value access, `exp,log,sin,cos`, positive
square root, and scalar uniform/exponential/Gaussian draw with known
parameters. Complex arithmetic is a fixed number of real operations.
Fixed public real constants and ideal integer/address words are as in
04z/T87. Fourier transforms, integration, evolved values, and arbitrary
known-function evaluations are not additional primitives.

Put

    q=s+d/2,       gamma=d/q=2d/(2s+d),
    J=ceil(1+d/(2s)),       m=J-1,
    a0=2d^2+20d+50,       Awork=a0+d^2+2d+2.

There are fixed positive constants, depending only on `d,s,p,kappa`,
such that for each prescribed real `T>=2` an actual algorithm returns
a real indexed Fourier polynomial satisfying

    sup_v (E||U_T-S_T v||inf^2)^(1/2) <=1/8,
    Q_T <=[1+J(J-1)/2] k^d on every seed path,
    k^d <=C exp(gamma T),
    sup_v E Work_T <=C exp(gamma T)(1+T)^Awork.         (1.1)

Its output has at most `C(1+T)^(3d^2+9d)` entries. Evaluation at any
specified point costs polynomial work and uses no further initial
values. A deterministic constant-work patch has sup error `3/32` for
`0<=T<=2`.

For all sufficiently large real `T`,

    c exp(gamma T) <=Q_point(T),Q_profile(T)
                                      <=C exp(gamma T). (1.2)

For paid work the conclusion is only

    c exp(gamma T) <=W_point(T),W_profile(T)
                         <=C exp(gamma T)(1+T)^Awork.  (1.3)

The constants need not be uniform as `p` grows or `kappa` decreases to
zero. The guarantee concerns each selected horizon, not simultaneous
accuracy over all times. It is an exact-real operation statement.

## 2. Actual flow, comparison, and scalar dynamics

On `[-1,1]`, the reaction is inward, with equilibria `-1,0,1`, and

    f'(z)=1-D z^(D-1) <=1 for every real z,
    1-D <=f'(z)<=1 for |z|<=1,
    |f(z)|<=|z| for |z|<=1.                           (2.1)

The heat mild fixed point on a bounded ball of `C(X)` gives local
existence and uniqueness. Comparison with `+/-1` keeps every solution
started in that interval there, so bounded continuation gives global
existence. These assertions concern the actual PDE.

For two such real solutions their difference solves a linear equation
with potential equal to the secant slope of `f`. This potential is at
most one by (2.1). Positivity, or the heat Duhamel iteration after a
constant lower shift of the potential, proves

    |S_t v-S_t w| <=e^t P_t |v-w|,
    ||S_t v-S_t w||inf <=e^t ||v-w||inf,               (2.2)

where `P_t=exp(t kappa Delta/2)`. In particular
`||S_t v||inf<=e^t||v||inf`.

For the scalar equation `z'=z-z^(2p+1)`, direct differentiation gives

    phi_(t,p)(c)
       =c e^t/[1+c^(2p)(e^(2pt)-1)]^(1/(2p)),        (2.3)

with value zero at `c=0`. The denominator is positive for `t>=0`.
It is an odd, order-preserving flow. Starting at `|c|<=1`, it stays
in `[-1,1]`. This formula replaces the cubic formula throughout.

In particular the time-one target has the strict bound

    ||S_1 v||inf<=sigma_p
       =[1+(2^(2p)-1)e^(-2p)]^(-1/(2p))<1.           (2.4)

The cubic-specific number `7/8` is not imported as a bound for this
scalar expression. The saturation used below depends on `p`.

## 3. A concrete odd-power tree and its actual derivative field

The general classical bounded polynomial representation in R20,
with its final R20b domain/risk repairs, is sufficient. Here the
odd-power reaction has the particularly simple explicit rule

    beta_br=D-1,
    M(y_1,...,y_D)=(sum_i y_i-product_i y_i)/(D-1).     (3.1)

At an all-positive or all-negative cube corner its numerator is
respectively `D-1` or `-(D-1)`. At any other corner the sum belongs
to `[-D+2,D-2]` and the product is `+/-1`; hence the numerator belongs
to `[-D+1,D-1]`. Multi-affine interpolation from the corners proves
`|M|<=1` on the complete cube. Moreover

    M(z,...,z)=z+(z-z^D)/(D-1).                       (3.2)

Run Brownian particles of covariance `kappa t I_d`, each splitting
at rate `beta_br` into exactly `D` children. Stop at time one and
apply (3.1) recursively to the leaf data. The resulting finite-tree
polynomial `P_tree` is multi-affine in its distinct leaf variables
and bounded by one on their cube. Conditional independence of the
child subtrees gives the first-split renewal identity

    u(t)=e^(-beta_br t)P_t g
       +integral_0^t beta_br e^(-beta_br r) P_r
                     M(u(t-r),...,u(t-r)) dr.

Its equivalent mild equation has reaction
`beta_br(M(z,...,z)-z)=z-z^D`. Bounded mild uniqueness identifies
the expectation with the actual `S_t g`, not an auxiliary flow.

If `n_t` is the terminal population, its jump is `D-1` at rate
`beta_br n_t`. Stopping and applying its generator to an integer
power `h>=1` gives

    E n_t^h <=exp[beta_br t(D^h-1)].                  (3.3)

Indeed `n[(n+D-1)^h-n^h]<=(D^h-1)n^h` for `n>=1` by binomial
expansion. The first moment bounds stopped exit probabilities and
proves nonexplosion; monotone limiting gives (3.3). The number of
segments is at most `2n-1`. Recursive generation uses `O_D(n)` paid
operations and scalar clocks; no chronological sorting is necessary.

For distinct leaf labels `i_1,...,i_j`, the corner difference formula
for a bounded multi-affine polynomial gives

    |partial_(i_1)...partial_(i_j) P_tree|<=1.         (3.4)

The derivative is `2^(-j)` times a signed sum of `2^j` corner values
in the selected coordinates. This is also a finite way to compute
it, using `2^j` upward passes. Repeated leaf derivatives vanish.

For completeness, the precise Gaussian input to the field law can
be prepared by R21's guarded linear recursion. Given the finite
tree, let `C` be its unscaled leaf covariance and let every root-to-leaf
length equal one. Partitioning the terminal labels by the segments
alive at a time and applying Cauchy--Schwarz, then integrating, gives

    C >= (1/n) 11^t.                                 (3.5)

For each segment of length `ell`, compute an aggregate variance from
the children: use the harmonic sum `h=(sum_c 1/a_c)^(-1)` and weights
`h/a_c` if all child variances are positive; otherwise use the first
zero child with weight one and set `h=0`. Set `a_v=ell+h`. Apply the
same weights to the child Gaussian aggregates, adding the segment's
own independent Gaussian. At a leaf use its length and edge Gaussian.
Zero-length edges have Gaussian value zero, and divisions are guarded.

Induction in one unscaled coordinate gives `Var(A)=Cov(X_i,A)=a` at
the root and `A=sum_i w_i X_i` with nonnegative weights summing to one.
Perform it independently in all `d` coordinates. The physical residuals
`Z_i=sqrt(kappa)(X_i-A)` are independent of the complete physical common
Gaussian vector `sqrt(kappa)A`, including singular cases, and have
covariance `kappa(C-a11^t)` in each coordinate. Also

    1/n<=a<=1.

The recursion and the path-sum/subtraction passes cost `O_d(n)`.
Testing a proposed `C-b11^t>=0` against `w` also gives `b<=a`; no matrix
inverse or covariance factorization is needed. R21's maximality is a
statement about this scalar common variance, not global Monte Carlo
variance optimality.

Take `g,v in C(X)`, with `g` known by an actual evaluator of uniform
finite cost `G`, `||g||inf<1`, and `e=v-g`. Let `U` be an independent
uniform point of `X`. At all leaves use the same locations `U+Z_i`.
Select a uniformly distributed ordered injection `I` of `j` distinct
leaves. If `n<j`, return zero with no acquisition. Otherwise set

    C_I=partial_I P_tree((g(U+Z_i))_i),
    Zscalar=(n)_j C_I product_(b=1)^j e(U+Z_(I_b)),
    W_j=h_(kappa a)(.-U) Zscalar.                    (3.6)

Here `h_v` is the periodic centered Gaussian density of variance `v`;
its Fourier multiplier is `exp(-2pi^2 v|nu|^2)`. The only unknown
values in (3.6) are the selected at most `j` values of `v`.

Conditionally on the tree and residuals, integrating the common
Gaussian is convolution of the *complete* translated tree polynomial
or its complete ordered derivative expression. Uniform `U` performs
that integral. Ordered injection averaging cancels `(n)_j`, producing
exactly the ordered-leaf expansion of the `j`th derivative. In
particular the residual law and the heat variance have both changed;
this is not a damping of the old leaf samples with their old law.

Use the real Hilbert space with norm

    ||h||_r^2=sum_nu (1+|nu|^2)^r |hhat(nu)|^2,
    r=d+1,        ||h||inf<=E_d||h||_r.               (3.7)

The embedding follows directly by Cauchy--Schwarz and convergence of
`sum_nu(1+|nu|^2)^(-r)`. Gaussian Fourier shells and `a>=1/n` give
`||h_(kappa a)||_r^2<=C_h n^(r+d)`. Consequently

    E W_j=D^j S_1(g)[e,...,e],
    E||W_j||_r^2<=V_j ||e||inf^(2j),
    V_j=C_h exp[beta_br(D^(2j+r+d)-1)],
    B_j=sqrt(V_j).                                   (3.8)

The identities are Bochner identities. On each finite tree stratum,
all evaluations and finite Gaussian operations are measurable; heat
translations are continuous in `H^r`. A countable union of such strata,
separability of `H^r`, and the displayed square-integrable envelope give
strong measurability and Bochner integrability. The same envelope for
each higher ordered derivative, and finite-polynomial Taylor remainders
with one or two more leaf labels, prove actual infinite Frechet
differentiability of

    S_1:{q in C(X): ||q||inf<1} ->H^r(X).

More explicitly, the derivative candidate at order `j` is bounded by
`B_j product_i||h_i||inf`; its first remainder is bounded by a constant
times `||eta||inf^2 product_i||h_i||inf` using the `(j+2)`-label envelope
on a small ball about the base profile. Dominated expectation of this
finite-tree identity proves the Frechet derivative and its continuity
inductively. For a whole segment in the open unit ball it gives

    ||S_1(g+e)-sum_(j=0)^(J-1) D^jS_1(g)[e^j]/j!||_r
                                    <=B_J||e||inf^J/J!. (3.9)

The derivative permits arbitrary continuous directions; the segment
condition is separately required for (3.9), exactly as in R20b.

For a box cutoff `N`, the actual sample is only its finite real array.
Choose one representative from each `{nu,-nu}` pair. Its coefficients
are

    z_0=Zscalar,
    z_(nu,c)=2 Zscalar e^(-2pi^2 kappa a|nu|^2)
                                            cos(2pi nu.U),
    z_(nu,s)=2 Zscalar e^(-2pi^2 kappa a|nu|^2)
                                            sin(2pi nu.U). (3.10)

The positive sine sign follows from `h(x-U)`. Enumerating the
`K=(2N+1)^d` real coefficients costs `O_d(K)`. Partial Fisher--Yates
selection, leaf lookup, the finitely many upward passes, residual
generation, and all memory accesses give

    Work(sample)<=C_(d,D,j)[(1+G)n+K],
    E Work(sample)<=C_(d,D,j,kappa)(1+G+K).            (3.11)

Tree, Gaussian, tuple, and selected-partial `C_I` preparation precedes
unknown queries. Null nonterminating tree preparation thus never
exceeds the `j`-query cap. Uniform endpoints and zero edges use fixed
total guards.

## 4. Paid known-profile solver for this fixed odd degree

The following proof adapts the actual T81/T84 construction with its
polynomial-dependent constants exposed. It does not assume a cubic
solver remains valid after merely renaming its reaction.

Fix `d,kappa,D,B,c`, with `B>=1`. Suppose an explicitly known real
periodic `q0` satisfies

    ||q0||inf<=1,
    ||q0||_(G_(c/R))<=B,       R>=1,
    ||q||_(G_rho)=sum_alpha rho^|alpha|
                                  ||partial^alpha q||inf/(alpha!)^2,

and one evaluation costs at most `Wq`. For `S,P>=1` there is a finite
deterministic elementary-operation solver with output `U` such that

    ||U-S_S q0||inf<=e^(-P),
    Work<=C R^d E^a0(1+Wq),
    E=1+P+S+log(R+1),       a0=2d^2+20d+50.           (4.1)

All constants can depend on the listed fixed parameters. The output
is an indexed real Fourier array and its evaluation cost is included.

### 4a. Gevrey and analytic estimates for the actual PDE

The `G_rho` norm is a Banach-algebra norm: the normalized product rule
has coefficient `1/binom(alpha,beta)<=1`. Completeness and strong heat
continuity follow from uniform derivative convergence and dominated
summation. Real heat contracts every derivative sup norm. On its ball
of radius `2B`, the polynomial has bounds

    ||f(q)||_G<=2B+(2B)^D,
    Lip_G(f)<=1+D(2B)^(D-1).

For example, any positive `h0<=1` satisfying

    h0[2B+(2B)^D]<=B/2,
    h0[1+D(2B)^(D-1)]<=1/2

gives a uniform local mild solution bounded by `2B`, independently of
`R`. Integration by parts in a coordinate of largest frequency,
optimizing the derivative order, and summing Fourier shells gives

    sum_(|nu|inf>H)|uhat(t,nu)|
       <=C R^d exp(-c1 sqrt(H/R)),       0<=t<=h0.     (4.2)

For late times, first use actual comparison to obtain `||u(t)||inf<=1`.
The periodized heat kernel shifted by an imaginary vector `y` has
`L1` norm at most `exp(|y|^2/(2kappa t))`. In the varying tube
`|Im z|_2<sqrt(kappa t)`, move the time-`r` contour to
`y_r=sqrt(r/t)y`. Then

    |y-y_r|<=sqrt(kappa)(sqrt(t)-sqrt(r))
                                           <=sqrt(kappa(t-r)).

Thus the heat map between these tubes has norm at most `Kheat=e^(1/2)`.
Set `Bcx=2Kheat` and choose `0<h1<=min(h0,1)` so that

    h1 Kheat(Bcx+Bcx^D)<=Kheat/2,
    h1 Kheat(1+D Bcx^(D-1))<=1/2.                    (4.3)

These bounds make the complex-spatial mild map invariant and
contractive on the tube ball. Polynomial composition preserves
holomorphy; periodic contour faces cancel and the uniform bounds
justify the integrals at zero. Real uniqueness identifies its real
restriction with the actual solution. Restarting from the bounded
real state at `t-h1` gives the same strip of positive width
`sqrt(kappa h1)` at every `t>=h1`. Contour shifting in a smaller strip
therefore gives

    sum_(|nu|inf>H)|uhat(t,nu)|<=C exp(-b H), t>=h1.  (4.4)

Combining (4.2) and (4.4), since `h1<=h0`, bounds the tail throughout
`[0,S]` by

    t_H=C R^d exp(-c1 sqrt(H/R))+C exp(-b H).          (4.5)

For arbitrary bounded continuous initial data of norm at most one,
(4.4) still holds at time one. The constants depend on `D,kappa,d`;
the strip need not stay positive uniformly as `kappa` goes to zero.

### 4b. Galerkin bootstrap and honest FFT padding

The rectangular projector has norm
`Lambda_H=C_d(1+log(H+1))^d>=1`. Consider the finite ODE

    U'=A_H U+P_H f(U),       A_H=(kappa/2)Delta.

Until `||U||inf` reaches two, a safe real Lipschitz constant for `f`
is `L2=1+D 2^(D-1)`. Comparing its mild equation to `P_H u`, adding
the actual tail, and using real heat contraction gives

    ||U(t)-u(t)||inf
       <=(epsilon0+t_H) exp(L2 Lambda_H S), 0<=t<=S,  (4.6)

where `epsilon0` is the initialization error relative to `P_H q0`.
Making this at most `min(1/4,e^(-P)/4)` keeps `||U||inf<=5/4` and
closes the bootstrap. The bounded finite-dimensional trajectory
continues to `S`. No Galerkin maximum principle is used.

Choose

    H=ceil(C R E^(2d+8)).                            (4.7)

After increasing the fixed `C`, the quantity `sqrt(H/R)` dominates
`log R+P+L2 Lambda_H S`, and (4.5)--(4.6) have the claimed size.
Here `log(H+1)<=C E` and `Lambda_H<=C E^d`; growth of `log C` in
the projector is dominated by the square-root growth of `C` in the
tail exponent, so this choice is not circular.

Evaluate `q0` on a power-of-two grid `Q0>=4H` and use a tensor FFT.
Retained frequencies have distinct residues modulo `Q0`, so the
aggregate retained coefficient alias error is bounded by the one
Fourier tail beyond `Q0-H`. It incurs no additional mode-count factor.
Equation (4.2) controls that tail and hence `epsilon0`.

For the polynomial nonlinearity, `U^D` has Fourier support inside
the box of radius `D H`. A power-of-two grid strictly larger than
`2D H` in each coordinate represents that full polynomial without
aliasing. Transforming, evaluating the fixed power, and restricting
therefore computes the *actual* `P_H(U-U^D)`. Cubic padding `6H`
is replaced by `2D H`, not reused for larger degree. Butterfly
operations, pointwise powers, trigonometric twiddles, padding, and
array accesses cost `O_(d,D)(H^d log(H+1))`. No FFT oracle is used.
Conjugate symmetry is preserved, so real-time outputs are real.

### 4c. Complex time, panels, and finite Picard count

For `|arg z|<=pi/4`, the full heat semigroup on `C(X)` has norm
at most `Ksec=2^(d/4)`, independent of `H,kappa`. The mild equation
from a real Galerkin start of norm at most `5/4` is contractive on
a fixed complex ball, for example radius `4Ksec`, in a forward
sector of radius

    rho_H=c_(d,D)/Lambda_H.

Choose `c_(d,D)` using the bounds `z+z^D` and
`1+D z^(D-1)` at that ball radius. This is a spatial sup-norm
bound on the exact finite ODE; no exact restart values are acquired
by the algorithm.

A disk crossing the negative real axis at time zero is separately
needed. The finite Fourier generator satisfies

    ||A_H v||inf<=C_d kappa H^(d+2)||v||inf.

A finite-dimensional complex Picard argument on a fixed ball gives

    a_H=c_(d,D)/(C_d kappa H^(d+2)+Lambda_H).          (4.8)

Its logarithmic reciprocal is `O(1+log(H+1))`. A frequency-independent
initial disk is not asserted.

Choose the time polynomial degree and Lobatto norm bound as

    L=ceil(C E^(d+4)),       beta_L=C(1+log(L+1))>=1.

Put `L4=1+D 4^(D-1)`, `F4=4+4^D`, and
`h=c/(Lambda_H beta_L)`, choosing its fixed positive constant so

    h<=min(1/100,rho_H/100),
    L4 h Lambda_H beta_L<=1/4,
    F4 h Lambda_H beta_L<=1/2.                       (4.9)

Start with a panel of length `a_start=min(a_H/16,h/16)`. Double
with panels `[t,2t]` until the endpoint `b0` first belongs to `[h,2h)`.
Use `ceil((S-b0)/h)` equal remaining panels; their lengths lie in
`[h/2,h]`, since `S>=1` and `h<=1/100`.

The parameter-two Bernstein ellipse of `[0,a_start]` fits inside
the initial disk. The ellipse of `[1,2]` has real part at least
`7/8`, imaginary part at most `3/8`, and modulus less than three;
the scaled startup ellipses fit in the forward sector. For a later
panel beginning at `b`, use the sector based at `b-h>=0`. Its
relative ellipse has real part at least `7h/8`, imaginary part at
most `3h/8`, and modulus less than `3h`. Thus all panels have the
same fixed ellipse parameter and

    n_pan<=C[1+log(H+1)+log(L+1)+S Lambda_H beta_L]
                                                  <=C E^(d+2). (4.10)

On these ellipses the projected forcing is bounded by `C_(d,D)Lambda_H`.
Cauchy bounds on Banach-valued Chebyshev coefficients and the Lobatto
alias identity give interpolation error `C Lambda_H 2^(-L)`.

On a panel of length `ell`, the actual finite nodal map is

    V_i=e^(theta_i ell A_H) U_b
       +ell integral_0^(theta_i) e^((theta_i-r)ell A_H)
                         sum_j l_j(r) P_H f(V_j) dr. (4.11)

On the real nodal ball of radius four, with start `||U_b||inf<=2`,
its image norm is at most `2+F4 ell Lambda_H beta_L<4`; its
Lipschitz factor is
`q_ell=L4 ell Lambda_H beta_L<=1/4`. Starting at the linear heat
values and taking the public count `Kiter=ceil(Citer L)` Picard
iterations gives error at most `C 4^(-Kiter)`.

Insert the exact Galerkin nodal values into (4.11). If the initial
panel error is `e`, the endpoint error obeys

    e_next<=e/(1-q_ell)
          +C ell Lambda_H 2^(-L)/(1-q_ell)+C 4^(-Kiter).

Since the sum of panel lengths is `S`, the global bound is

    exp(C S Lambda_H beta_L)
       [C S Lambda_H 2^(-L)+C n_pan 4^(-Kiter)].      (4.12)

Increasing the fixed constants makes it at most `min(1/4,e^(-P)/4)`.
Induction keeps numerical starts within radius two, closing this
second bootstrap. The stability exponent does not contain `kappa H^2 S`
and is not proportional to the number of startup panels.

### 4d. Exact scalar weights and the paid bound

For mode `nu`, write `z=2pi^2 kappa |nu|^2 ell`. Expanding a Lobatto
cardinal polynomial reduces (4.11) to finitely many moments

    I_j(z,theta)=integral_0^theta e^(-z(theta-r))r^j dr.

For `z>0`, integration by parts gives

    I_0=(1-e^(-z theta))/z,
    I_j=theta^j/z-(j/z)I_(j-1).

For the zero mode use `theta^(j+1)/(j+1)`, and for `theta=0` use
zero. Positive `kappa` and positive panel lengths justify every
nonzero-mode denominator. Distinct Lobatto nodes justify all cardinal
denominators. These are exact primitive formulas, not quadrature calls.

Let `D_H=(2H+1)^d`. Weight construction costs `O(D_H L^3)` per
panel, and a Picard step costs
`O_(d,D)(D_H L^2+L D_H log(H+1))`, including the correctly padded
degree-`D` nonlinearity at each node. Thus total work is bounded by

    C n_pan D_H[L^3+L^2 log(H+1)]
                      +C D_H[log(H+1)+Wq].          (4.13)

Substitution of (4.7) and (4.10) gives an `E` exponent no larger
than `2d^2+12d+14`, which is below the chosen `a0`. Enumeration,
storage and one terminal evaluation are absorbed. Equations
(4.6),(4.12) leave slack within the claimed `e^(-P)` error.

Small-`z` cancellation in these moment recurrences is a finite-precision
issue; no floating-point or bit-complexity guarantee is inferred.
This proves the paid known-profile lemma for the fixed odd degree.

## 5. Sharp-query strong-profile upper construction

### 5a. Coarse input and the fixed-time estimation budget

Use the explicit normalized Gevrey bump partition and fixed tensor
stencils of T81/T84. Exactly `k^d` initial grid values give an actual
known smooth profile `g` with

    ||g||inf<=3/4,       ||v-g||inf<=Cint k^(-s),
    ||partial^alpha g||inf<=B0(C0 k)^|alpha|(alpha!)^2. (5.1)

Choose `k0>=2s` with `Cint k0^(-s)<=1/4`. A total-degree Taylor
comparison proves (5.1) using only the promised derivatives through
order `s`; the tensor stencils do not require higher total-order
mixed derivatives. The compact Gevrey weights are normalized integer
translates of `exp(-1/(1-t^2))` on `|t|<1`, with denominator at
least `exp(-4/3)`. Support guards precede division. Setup costs
`O_(d,s)(k^d)` and each known lookup costs `Gg<=C_(d,s)`, using
floors and a bounded number of neighboring records. This interface
is independent of the reaction.

By (4.4) at time one there are public `A_tail>=1,b_tail>0` such that

    ||(I-P_N)S_1 v||inf<=A_tail exp(-b_tail N).        (5.2)

Set `Lchi=25`. For `T>=2` define

    S=T-1,       epsilon=e^(-S)/(16 Lchi),
    N=max(1,ceil((S+log(32 Lchi A_tail))/b_tail)),
    K=(2N+1)^d,
    Cstar=1+sum_(j=1)^m sqrt(V_j) Cint^j/j!
                                          +B_J Cint^J/J!,
    k=max(k0,ceil((4 E_d Cstar/epsilon)^(1/q))),
    M=k^d.                                          (5.3)

These are public finite integers/constants. The tail in (5.2) is at
most `epsilon/2`; `N=O(1+T)`; and directly from the ceiling bound,

    k^d<=C exp(gamma T).                              (5.4)

There is no factor involving `K` in this grid choice.

The known base solve is paid as follows. Put

    D_N=sqrt(K)(1+d N^2)^(r/2),
    tau=epsilon/(4 E_d D_N),       Pbase=log(1/tau).

Apply (4.1) at time one, scale `R=k`, and precision `Pbase`, with
cutoff at least `N`. Increasing a fixed cutoff constant suffices;
`N=O(1+T)` and all of (4.7)'s bounds remain valid. Its output has
`||U_base-S_1g||inf<=tau`. Every complex Fourier error coefficient
is at most `tau`, so

    ||P_N(U_base-S_1g)||_r<=D_N tau=epsilon/(4E_d).    (5.5)

This costs `C k^d(1+T)^a0`: the extra base precision is only
`log D_N=O(log(2+T))`, and there is no unknown evolved-value query.

For each `j=1,...,m`, take `M` independent complete field samples
from (3.10), using fresh seeds. Conditioned on the deterministic
coarse transcript for a fixed input, their Hilbert means obey

    E||M^(-1)sum_a(P_N W_(j,a)-E P_N W_j)||_r^2
                        <=V_j ||v-g||inf^(2j)/M.     (5.6)

Independence and centering make cross-copy inner products vanish;
second moments justify Fubini. No independence of Fourier coordinates
within a sample is assumed. This is an inequality, as repaired in R20b.

Form the finite real polynomial

    p_raw=P_N U_base
                 +sum_(j=1)^m [1/(j! M)]sum_a P_N W_(j,a).

The complete segment `(1-t)g+tv` has norm at most `3/4`. Equations
(3.9),(5.1),(5.5),(5.6), Hilbert Minkowski, and `Js>=q` give

    (E||p_raw-P_N S_1v||_r^2)^(1/2)
      <=epsilon/(4E_d)
         +sum_(j=1)^m sqrt(V_j) Cint^j k^(-js-d/2)/j!
         +B_J Cint^J k^(-Js)/J!
      <=epsilon/(4E_d)+Cstar k^(-q)
      <=epsilon/(2E_d).                              (5.7)

The higher derivatives here belong to the fixed-time flow on `C(X)`;
they are not extra smoothness assumptions on the unknown input.

In the real basis `1,cos,sin`, clip the constant coefficient to
`[-1,1]` and every other coefficient to `[-2,2]`. The actual target
coefficients lie in these intervals because `||S_1v||inf<=1`.
For real coefficients the Hilbert square norm is

    c_0^2+(1/2)sum_(nu representatives)(1+|nu|^2)^r
                                          (c_(nu,c)^2+c_(nu,s)^2).

Each coordinate projection decreases its weighted squared error to
the target. Thus the clipped polynomial `p_N` still has (5.7), despite
any clipping bias. The embedding (3.7) and deterministic tail (5.2)
give the strong bound

    (E||p_N-S_1v||inf^2)^(1/2)<=epsilon.              (5.8)

The complex-to-real conversion of a stored Fourier array is
`c_(nu,c)=2 Re uhat(nu)`, `c_(nu,s)=-2 Im uhat(nu)`.
It agrees with the sample convention (3.10).

### 5b. The degree-dependent saturation and its paid evaluator

Use the fixed, explicitly evaluable thresholds

    alpha_chi=(1+sigma_p)/2,
    beta_chi=(1+alpha_chi)/2,       sigma_p<alpha_chi<beta_chi<1.

For `0<t<1` let
`w(t)=exp(-1/t)/(exp(-1/t)+exp(-1/(1-t)))`, extended by zero or
one outside that interval. For `z>=0` set

    chi(z)=z,                                      z<=alpha_chi,
    chi(z)=z+(beta_chi-z)
                  w((z-alpha_chi)/(beta_chi-alpha_chi)),
                                      alpha_chi<z<beta_chi,
    chi(z)=beta_chi,                               z>=beta_chi,

and extend oddly. Guards precede all divisions; the interior
denominator is at least `e^(-2)`. The function is smooth because
the transition is flat at both endpoints. Its middle derivative is
`1-w(t)+(1-t)w'(t)`; `0<=w'(t)<=8e<24` proves global Lipschitz
constant 25, independently of the gap between these fixed thresholds.
Its range is inside `[-beta_chi,beta_chi]`, and (2.4) lies in its
identity interval.

The same Cauchy estimate for the flat exponential, product and
reciprocal induction gives

    sup_z |chi^(l)(z)|<=Achi Cchi^l(l!)^2, l>=0,     (5.9)

with public constants now allowed to depend on `p`. The rescaling
by `beta_chi-alpha_chi` is included in `Cchi`; it is not suppressed
as a uniform-in-degree constant.

A clipped box polynomial has
`||partial^alpha p_N||inf<=2K(2pi N)^|alpha|`. The finite-jet
Faà di Bruno identity, followed by
`sum_(beta_1+...+beta_l=alpha)1/(beta_1!...beta_l!)=l^|alpha|/alpha!`,
gives for `n=|alpha|>=1`

    ||partial^alpha chi(p_N)||inf
      <=Achi(2pi N)^n sum_(l=1)^n (2Cchi K)^l l! l^n
      <=Achi(C_(d,p) N K)^n (alpha!)^2.              (5.10)

The last step uses `l!<=n!`, `l^n<=n^n<=e^n n!`, `n<=2^n`, and
`n!<=d^n alpha!`. Hence `qhat=chi(p_N)` has a public uniform
Gevrey norm at scale `Rhat=N K`, independently of its random array.
Evaluating its finite Fourier sum and the guarded transition costs
`O_d(K)` actual operations. No new initial values are used.

### 5c. Continuation, output size, queries, and work

Equations (2.4),(5.8) and the Lipschitz bound imply

    (E||qhat-S_1v||inf^2)^(1/2)<=e^(-S)/16.

Run (4.1) at time `S`, precision `Pout=T+log(16)`, and this actual
known `qhat`. Its conditional sup error is at most `e^(-T)/16`
on every completed transcript. Applying the pathwise comparison
(2.2) before expectation, and then Minkowski, proves

    (E||U_T-S_Tv||inf^2)^(1/2)
                                  <=1/16+e^(-T)/16<=1/8. (5.11)

This includes base error, finite-order Taylor bias, all correlated
Fourier-mode sampling errors, omitted true tail, saturation, and the
final paid nonlinear evolution.

The base and grid cost `C k^d(1+T)^a0`. Equation (3.11) bounds all
the fixed number of derivative orders by `C k^d(1+K)` expected
work. For continuation,

    Rhat<=C(1+T)^(d+1),
    Wqhat<=C(1+T)^d,       Eout<=C(1+T).

It therefore costs at most `C(1+T)^(a0+d^2+2d)`. Together with
(5.4) these give (1.1) with `Awork` as stated. The final cutoff
is at most `C(1+T)^(3d+9)`, so the real array has at most
`C(1+T)^(3d^2+9d)` entries.

All new acquisitions are either coarse values or selected tuple
values. Every frequency shares the same tuple. Consequently

    Q_T<=k^d+M sum_(j=1)^m j
        =[1+J(J-1)/2] k^d                            (5.12)

on every seed, including a null path stuck in a preparation: preceding
completed samples obey their own caps and an unfinished preparation
adds no unbounded sequence of queries. Nonexplosion, finite moments,
and deterministic finite solver counts prove almost-sure halting and
the expected work bound.

All operations on each finite tree are Borel finite formulas. The
finite indexed array embeds continuously in `C(X)`, so its spatial
supremum loss is measurable. For probability statements assign the
zero array to the null nontermination set; no algorithmic detection
of that set is asserted. Off-promise finite responses may first be
clipped to `[-1/2,1/2]`. Fixed-count polynomial solver operations
remain finite even if their accuracy hypotheses fail; final coefficient
clipping always restores the uniform continuation interface. No
unverified convergence test or regularity test controls the count.

## 6. A reaction-specific mixed-L1 short-time derivative estimate

The lower proof needs an actual PDE estimate, not only the field
sampler. On any finite interval inside the open unit ball of initial
data, differentiating the mild equation is legitimate in `C(X)`.
One justification is local polynomial Picard differentiation followed
by finitely many restarts; equivalently the linearized Volterra inverse
has a convergent simplex series with factorial denominators. The
bounded actual trajectory makes every coefficient bounded.

Let `E_u(t,r)` be the positive propagator with potential `f'(u)`.
By (2.1),

    |E_u(t,r)h|<=e^(t-r) P_(t-r)|h|,                 (6.1)

both in `Linf` and `L1`. Write `Y_i`, `Y_ij`, `Y_123` for the
actual first, second and third variations. Their equations are

    Y_i=E_u(t,0)h_i,
    Y_ij=integral_0^t E_u(t,r)[f''(u)Y_iY_j] dr,
    Y_123=integral_0^t E_u(t,r)[f'''(u)Y_1Y_2Y_3
                         +f''(u)(Y_12Y_3+Y_13Y_2+Y_23Y_1)] dr.

Set

    C2=D(D-1),       C3=D(D-1)(D-2),
    B_D=e^2[C3+(3/2)C2^2].                           (6.2)

On `[-1,1]`, `|f''|<=C2`, `|f'''|<=C3`. Assign one direction an
`L1` norm and all other directions `Linf` norms. Heat domination
and Holder's elementary `L1*Linf` product bound give, for `0<=t<=1`,

    ||Y_i(t)|| <=e^t ||h_i||,
    ||Y_ij(t)|| <=C2 t e^(2t) ||h_i|| ||h_j||,
    ||Y_123(t)||
       <=[C3 t+(3/2)C2^2 t^2] e^(3t)
                          ||h_1||inf||h_2||inf||h_3||1. (6.3)

In the last line the three second-first terms each contribute at
most `C2^2 r e^(3r)` before propagation; integration bounded by
`e^(3t)` gives `3 C2^2 t^2/2`. The second line has the marked
`L1` version whenever one of its directions is marked. This proves
the mixed estimate directly for the odd-power reaction. At `D=3`,
`B_D=60e^2`, agreeing with the cubic value as a check.

Let `Pi` denote the spatial mean and set

    A1(v)=e^(-1)Pi S_1v,       F(v)=A1(v)-Pi v.

The actual flow is odd, and its derivative at zero is `e^tP_t`.
Thus `F` is odd, `DF(0)=0`, and `D^2F(0)=0`. Equation (6.3)
gives

    |D^3A1(v)[h_1,h_2,h_3]|
                   <=B_D||h_1||inf||h_2||inf||h_3||1.

Taylor's formula along the segment from zero to `v` then yields

    DF(v)[h]=integral_0^1(1-r)D^3A1(rv)[v,v,h] dr,
    |DF(v)[h]|<=(B_D/2)||v||inf^2||h||1.             (6.4)

No cubic identity has been used to obtain (6.2)--(6.4).

## 7. A fixed full-slice prior and its two time-one estimates

The information construction uses full uniform slices, never a prior
conditioned on a favorable PDE event. Choose once and for all
`psi in C_c^infinity((0,1)^d)`, with `0<=psi<=1` and

    I=int psi>0,
    Dpsi=max(1,max_(|alpha|<=s)||partial^alpha psi||inf),
    a_bump=1/(8Dpsi).

For even `k`, write `K=k^d`, `A_bump=a_bump k^(-s)`, and define

    v_xi(x)=sum_cells xi_j A_bump psi(kx-j), xi_j in {-1,1}.

Disjoint supports and flat cell boundaries give smooth periodic
profiles with each promised derivative bounded by `1/8`. On each
slice below both signs occur, so every profile belongs to `V`.

At a prescribed sufficiently large real `T`, set

    R_T=(a_bump I e^T)^(1/q),
    k=2 floor(R_T/2),
    ell=2 ceil(sqrt(K)/2),
    m_T=A_bump I ell/K.                              (7.1)

Take the equal mixture of the *complete uniform* slices
`sum_j xi_j=+ell` and `sum_j xi_j=-ell`. For `R_T>=4` and
`K>=2048`, these slices are nonempty, and

    R_T/2<=k<=R_T,
    sqrt(K)<=ell<=2sqrt(K)<=K/4,
    1<=e^T m_T<=2^(q+1),
    A_bump/sqrt(K)<=2^q I^(-1)e^(-T),
    log K<=dT/q.                                    (7.2)

All choices depend only on public parameters and `T`, and precede
the algorithm. Each slice has mean profile value `+/-m_T`.

We use the following elementary complete-slice lemma. If an odd
function of the entire sign cube changes by at most `Lflip` on one
coordinate flip, then on either of the slices in (7.1),

    |E H|<=ell Lflip/2,
    Var(H)<=K Lflip^2,
    P(|H-EH|>z)<=2 exp[-z^2/(2K Lflip^2)].           (7.3)

To prove the mean bound, start with a uniform balanced sign vector
and flip a uniformly chosen set of `ell/2` negative entries. The
output is uniform on the positive slice by permutation symmetry.
The balanced mean is zero by oddness. The negative slice is analogous.
For concentration, reveal coordinates successively. Conditional on a
prefix, couple the two possible next-sign completions by a uniform
subset and one added uniform element. The coupled full vectors differ
by a swap of two signs, so the conditional expectation difference is
at most `2Lflip`. Each Doob increment has conditional range length
at most `2Lflip`, conditional variance at most `Lflip^2`, and
conditional exponential moment at most
`exp(theta^2 Lflip^2/2)`. Summing variances and iterating that bound
proves (7.3). Deterministic next signs have zero increments.

For the mean correction `F(v_xi)`, a one-cell change has `L1` norm
`2A_bump I/K`; its interpolation segment has norm at most `A_bump`.
Equation (6.4) therefore gives the valid flip bound

    L_F=B_D A_bump^3/K,
    |E F|<=B_D A_bump^3 ell/(2K),
    Var(F)<=B_D^2 A_bump^6/K.                        (7.4)

Choose the threshold so that `A_bump^2<=I/(64 B_D)`. Then
`|EF|<=m_T/128`, and Chebyshev with (7.2) gives

    P(|F|>m_T/4)<=64 B_D^2 A_bump^4/I^2<=1/64.       (7.5)

Outside that bad event, the actual mean `b1=Pi S_1v` on the positive
slice is at least `3e m_T/4`; the negative slice has the opposite
bound.

We also need a whole-profile time-one estimate. Put

    lambda=2pi^2 kappa,
    rho=((1+e^(-lambda))/(1-e^(-lambda)))^d,
    Ccell=2e rho,
    Gkappa=(1+2e)sqrt(d/kappa),
    Cnet=(1+sqrt(d)Gkappa)^d.

Fourier summation bounds both the `Linf` and `L2` norm of the
time-one heat kernel by `rho`. From (6.1) a one-cell flip changes
`S_1v(x)` by at most `Ccell A_bump/K`, uniformly in `x`.
Equation (7.3) therefore bounds its slice mean by
`Ccell A_bump/sqrt(K)` and supplies its Gaussian concentration.

The elementary heat gradient bound
`int|grad p_t|<=sqrt(d/kappa)t^(-1/2)`, the actual mild equation,
`|f(u)|<=|u|`, and `||u(r)||inf<=e^r A_bump` give

    ||grad S_1v||inf<=Gkappa A_bump.                 (7.6)

Take a uniform torus grid with `N_K=ceil(sqrt(d)Gkappa sqrt(K))`
points per coordinate. Its size `M_K=N_K^d` is at most
`Cnet K^(d/2)`, and its nearest-point error in (7.6) is at most
`A_bump/(2sqrt(K))`. In (7.3) choose

    z_K=Ccell A_bump K^(-1/2) sqrt(2log(128M_K)).

A union bound gives failure probability at most `1/64`. To make all
constants explicit, set

    beta_net=log(128Cnet)/log(2)+d/2,
    Hnet=(Ccell+1/2)/sqrt(log(2))+Ccell sqrt(2beta_net),
    C0=(2^q Hnet/I)sqrt(d/q).

Equations (7.2),(7.6) then give, outside that event,

    ||S_1v||inf<=C0 e^(-T)sqrt(T),
    W1:=||(I-Pi)S_1v||2<=C0 e^(-T)sqrt(T).          (7.7)

The two favorable conditions (7.5),(7.7) have joint probability at
least `31/32` on each unchanged full slice. There is no inputwise
claim that every slice member is favorable.

## 8. Actual long-time PDE separation for the odd power

From now on write `u(t)=S_(1+t)v`, `b(t)=Pi u(t)`, and
`w(t)=u(t)-b(t)`, so `b(0)=b1` and `||w(0)||2=W1`.
Since the map `z ->z^D` is increasing on the real line,

    (1/2)d||w||2^2/dt
      =-(kappa/2)||grad u||2^2+||w||2^2
                          -int w(u^D-b^D)
      <=(1-lambda)||w||2^2.

Poincare on the normalized torus therefore gives

    ||w(t)||2<=e^((1-lambda)t) W1.                   (8.1)

This permits growth when `lambda<1`; no false decay assumption or
natural spectral-gap hypothesis is made.

The mean satisfies

    b'=b-b^D-R(t),       R=Pi(u^D)-b^D.

The linear Taylor term in `w` integrates to zero. Both `u` and its
mean belong to `[-1,1]`, so the real scalar Taylor remainder gives

    |R(t)|<=C_R ||w(t)||2^2,
    C_R=D(D-1)/2.                                   (8.2)

This replaces the cubic expansion of the mean remainder. It includes
all higher powers of `w` without assuming that `w` is pointwise small.

Compare `b(t)` to `phi_(t,p)(b1)`. Their secant potential is at most
one, by (2.1). Equations (8.1),(8.2) imply

    |b(t)-phi_(t,p)(b1)|
       <=C_R e^t W1^2 J_lambda(t),
    J_lambda(t)=int_0^t e^((1-2lambda)r) dr.          (8.3)

At `t=T-1`, with `mu=min(1,2lambda)>0`, (7.7) yields

    Emean(T):=C_R C0^2 T^2 e^(-mu T)                (8.4)

as a uniform upper bound. The integral definition of `J_lambda`
handles `lambda=1/2` without division by zero.

For `t>=1`, compare the last unit of actual PDE evolution to the
constant trajectory starting at `b(t-1)`. Equation (2.2), followed
by the heat `L2 ->Linf` bound, gives

    ||w(t)||inf<=2e rho ||w(t-1)||2.

Thus at `t=T-1`,

    ||w(T-1)||inf<=Espace(T):=Cw sqrt(T)e^(-lambda T),
    Cw=2e rho C0 e^(2(lambda-1)).                     (8.5)

Both errors decay for every fixed positive `kappa`.

Here is one fully specified horizon threshold. Choose an integer
`kstar>=4` with

    kstar^d>=2048,
    a_bump^2 kstar^(-2s)<=I/(64B_D).

Define

    Tgrid=q log(2kstar)-log(a_bump I),
    Tmean=(2/mu)max(0,log(512 C_R C0^2/mu^2)),
    Tspace=(2/lambda)max(0,log(64Cw/sqrt(lambda))),
    T0=max(2,Tgrid,Tmean,Tspace).                    (8.6)

These are finite public constants. For `T>=T0`, the prior conditions
hold and each of (8.4),(8.5) is at most `1/64`: use
`T^2 e^(-mu T)<=8mu^(-2)e^(-mu T/2)` and
`sqrt(T)e^(-lambda T)<=lambda^(-1/2)e^(-lambda T/2)`.

On a favorable positive-slice profile,
`e^(T-1)b1>=3/4` by (7.2),(7.5). For `0<c<=1`, formula (2.3)
implies

    phi_(t,p)(c)>=Psi_p(e^t c),
    Psi_p(y)=y/(1+y^(2p))^(1/(2p)).

The function `Psi_p` increases on the positive line, and
`(1+y^2)^p>=1+y^(2p)` proves

    Psi_p(3/4)>=Psi_1(3/4)=3/5.

Consequently (8.4),(8.5) give, simultaneously at every spatial point,

    S_T v(x)>=3/5-1/32=91/160>1/2.                  (8.7)

Oddness gives the negative bound on favorable negative-slice profiles.
This scalar separation is derived for the new reaction, not imported
from the cubic formula.

## 9. The finite-prior information lower and exact query order

Consider any permitted point estimator with squared error at most
`1/16` on every `v in V`. Threshold its real output at zero to test
the slice sign. On each favorable profile, (8.7) and Markov's
inequality make its error probability at most `1/4`. Equations
(7.5),(7.7) then bound its Bayes error under the original full-slice
mixture by `1/4+1/32=9/32`.

Strengthen a point query by revealing the entire sign of the
half-open cell containing the queried location. Its actual scalar
value can be reconstructed from that sign and the known bump.
Boundary and zero-bump queries can also receive this stronger reply;
no point meets more than one cell. Repeats remain charged and cannot
increase the number of distinct signs learned.

Cap at `ncap=floor(K/1024)` queries and, if fewer distinct cells were
revealed, pad with unused cell reveals until there are `ncap`. For
any adaptive sequence of unused labels and any fixed seed, after
`j` reveals with `z` positive signs, the next-sign probabilities are

    p_+=[(K+ell)/2-z]/(K-j),
    p_-=[(K-ell)/2-z]/(K-j).

Every prefix is feasible under both slices: each sign count is at
least `3K/8>ncap`. Along these prefixes,

    1/4<=p_-<=4/7,
    p_+-p_-<=2ell/K,
    KL(Ber(p_+)||Ber(p_-))
       <=(p_+-p_-)^2/[p_-(1-p_-)]
       <=64ell^2/(3K^2)<=256/(3K).                  (9.1)

The word chain rule yields KL at most `1/12` and total variation
at most `sqrt(1/24)<1/4`. The latter finite-word inequality follows
by coarse-graining to the event attaining total variation: binary
relative entropy is at least twice the squared probability difference,
since its second derivative in the first probability is at least four.
To include an arbitrary input-independent seed without a hidden
conditional-probability assumption, fix a
seed outside the finite union of the inputwise null nonhalting sets.
The padded word law is the same without-replacement law for every
such seed; adaptive label choices change no transition above. The
joint laws are therefore the product of the seed law and their
respective finite word laws. The same KL/TV bound holds for all
measurable tests using that joint data. The equal-prior capped error
is at least `3/8`.

Let `qbar` be the original estimator's expected query count averaged
over this fixed finite prior. If it is infinite there is nothing to
prove. Truncating just before query `ncap+1` changes the test only
on an event of probability at most `qbar/ncap`. Hence

    3/8<=9/32+qbar/ncap,
    qbar>=3ncap/32>=3K/65536.                         (9.2)

Finally (7.2) proves

    qbar>=c_lower exp(gamma T),
    c_lower=3*2^(-d-16)(a_bump I)^(d/q)>0,
                                                   T>=T0. (9.3)

The prior is independent of the algorithm; bias, adaptive locations,
unbounded estimator values, and variable stopping are all allowed.
The worst-input expected count is at least this finite-prior mean.
Thus (9.3) proves the point lower in the exact model of Section 1.
Evaluating a finite profile output at `x*` adds no acquisition and
transfers it to the strong-profile problem. Combining with (5.4),
(5.11),(5.12) proves both exact query orders (1.2). Since every
query is a charged operation, the paid-work lower in (1.3) follows;
the upper keeps its polynomial factor.

## 10. Bounded-horizon patch for the new polynomial

Choose a fixed coarse grid `k_b>=k0` so large that
`e^2 Cint k_b^(-s)<=1/32`. Its known interpolant `g_b` then differs
from the actual input flow by at most `1/32` on `0<=T<=2`, using
the new reaction's comparison (2.2).

Equations (4.2)--(4.6), with scale `k_b`, permit a fixed cutoff and
a fixed initialization grid for which the actual Galerkin flow stays
within `1/32` of `S_t g_b` throughout `[0,2]`, including zero. The
cutoff depends only on `d,s,p,kappa`. On a fixed neighborhood of
these bounded finite-dimensional trajectories, the polynomial vector
field, its derivative and the trajectory's second derivative have
uniform finite bounds. Explicit Euler with a fixed public `n_b`
steps of length `T/n_b` has local defect `C(T/n_b)^2`; the finite
Gronwall recurrence gives global error `C/n_b`, uniformly in `T`.
Choosing it at most `1/32` closes an Euler neighborhood bootstrap.

Each polynomial evaluation uses the degree-`D` padding `Q>2D H`.
All counts are fixed even at `T=0`; no zero-length convolution
division is used. The real indexed Fourier output has deterministic
sup error at most `3/32<1/8`, a constant hard query cap, and constant
paid work. This proves the bounded-time claim for this reaction.

## 11. General coefficients: the exact transfer and a counterexample

Fix `a,b>0` and let `R_amp=(a/b)^(1/(2p))`. For the physical PDE

    u_t=(kappa/2)Delta u+a u-b u^(2p+1),

set `u(t,x)=R_amp z(a t,x)`. Direct substitution gives

    z_theta=(kappa/(2a))Delta z+z-z^(2p+1),
    z(0,x)=v(x)/R_amp.                               (11.1)

The physical invariant amplitude is `[-R_amp,R_amp]`. Applying the
normalized theorem means the physical input class is explicitly

    V_R={R_amp w:w in V}
       ={v smooth periodic real: ||v||inf<=R_amp/2,
          max_(|alpha|<=s)||partial^alpha v||inf<=R_amp,
          min v<0<max v},

and the physical tolerance is `R_amp/4`. One physical scalar query
divided by the known constant `R_amp` is one normalized scalar query,
and conversely. Output scaling costs its finite array size; no new
unknown information is obtained. With normalized time `theta=aT`
and diffusivity `kappa/a`, the exact conclusion is

    Q_point(T),Q_profile(T)=Theta(exp(gamma aT)),
    c exp(gamma aT)<=W_point(T),W_profile(T)
                       <=C exp(gamma aT)(1+T)^Awork. (11.2)

The constructed physical RMS is at most `R_amp/8`. The long-time
threshold is the normalized `T0/a`, and the bounded-time patch
covers `aT<=2`. Constants may depend on fixed `a,b,p,kappa,d,s`.
Amplitude normalization alone gives reaction `a(z-z^(2p+1))`;
obtaining the exponent `gamma T` also requires measuring the horizon
in normalized time. It cannot erase the factor `a` in physical time.

Keeping the old physical class `V` and absolute RMS tolerance `1/4`
instead is not a harmless convention. Fix any `a>0` and choose
`b=a 8^(2p)`, so `R_amp=1/8`. Comparison with the scalar trajectories
starting at `+/-1/2` bounds every input in `V` by their positive
magnitude. In normalized variables that magnitude starts at four;
its inverse `2p`th power at time `theta=aT` is

    1+(4^(-2p)-1)e^(-2p theta).

It is at least `2^(-2p)` whenever

    theta >=(1/(2p))log(1+2^(-2p)).                  (11.3)

At such times every actual profile has sup norm at most
`R_amp*2=1/4`. The identically zero Fourier polynomial, using zero
unknown queries, meets the prescribed `1/4` RMS tolerance uniformly
on the original class. Thus the unscaled positive exponential lower
bound is false, both for point queries and for profile queries.
The scaled-class theorem (11.2) and this counterexample describe
different, explicitly stated problems.

## 12. Dependencies, provenance, and limits

All paths in this table are relative to this research run. These
hashes were checked against the actual files for this task.

| Source | SHA256 |
| --- | --- |
| `reviews/R20-polynomial-reaction-field-sampler-candidate.md` | `b1e42a195c67942066894d04a11c28d7ba2951a6d6730977070e424ac84542b9` |
| `reviews/R20b-continuous-domain-addendum.md` | `6c5e8b158ca269588c4200ca09c82f4ffa430e8aa0146a52022370ade352e527` |
| `reviews/R21-linear-tree-common-gaussian-candidate.md` | `99f8a23c98332b6797ee1ecc9f0929d94950cd047acb17bcbea0df9052ff7461` |
| `04z-all-positive-diffusivity-sharp-queries.md` | `57ef1d86ddba30ce9d54f316b0eb2dc97f407f7aeb4446a66b3103c28e0aedd4` |
| `reviews/T81-fixed-burnin-all-diffusion-upper-proof.md` | `d9b249ed669897df319ca712fc4ad26625fc97e1a9b32b79eacaf497b290bae5` |
| `reviews/T84-all-diffusion-upper-independent-audit.md` | `39cd98fcf957badbe382123bd1960eac7fb99441114c9433bd9ee0ff2d256d7d` |
| `reviews/T82-all-diffusion-prior-lower-proof.md` | `0b331397bbda06ba02381009ce95bfd7656aabb4bd196bac5e67a616b3a2320a` |
| `reviews/T83-all-diffusion-lower-independent-audit.md` | `902ee581593ace7d682fac5351a1288ccef09544d02893fbacc045782e03a56e` |
| `reviews/T87-all-diffusion-sharp-query-feasibility.md` | `acd788e6ee5564778cd0663be99aab17fb61f22bdfb4b345ccade008f18feff1` |

T81/T84 and T87 were read completely in the preceding T90 work;
their relevant solver, interpolation, saturation, risk, work and patch
passages were reread for T94. R20/R20b and R21 were read completely
in the immediately preceding T91 audit, including both R20b repairs;
the domain addendum and Gaussian recursion were checked again here.
04z and the complete T82/T83 lower sources were read for this task.
No conclusion is inferred merely from an audit's PASS label.

The math-auto-research skill, configuration/defaults, general profile,
model-routing and execution instructions, and project instructions
were read in this worker's preceding tasks and remain applicable.
This is the configured research route, not a backend attestation.
The inherited workspace was already dirty. Only this new T94 file
is owned and written by this task.

The bounded branching/voting representation is established prior
work. An--Henderson--Ryzhik explain polynomial voting and recursive
tree constructions, including the classical Allen--Cahn representation
attributed there to Etheridge--Freeman--Penington. The simple odd-power
rule (3.1) is verified algebraically here; no novelty of the method or
of that formula is asserted. I reopened the primary paper and its
polynomial construction for attribution:
[An--Henderson--Ryzhik](https://arxiv.org/html/2209.03435).

R21's inverse-variance tree recursion is classical Gaussian/Brownian
tree algebra, with the Felsenstein attribution documented and checked
in T91. Its role here is the correctly coupled nonlinear residual and
heat law and its paid tree traversal, not a claim to have invented
that recursion.

I also reopened the author's one-page Chebyshev-series note and its
Bernstein-ellipse approximation statement. The paid solver bound above
comes from the explicit polynomial-dependent estimates and finite
algorithm, not from interpreting that approximation statement as a
complexity theorem:
[Trefethen author note](https://people.maths.ox.ac.uk/~trefethen/outline3_2017.pdf).

These are bounded primary attribution checks, not an exhaustive
priority search. The combined theorem's novelty and significance
remain unresolved. No award or practical speed claim is made.

No Lean file, code, numerical artifact, accepted claim, run state,
configuration, or frozen source was edited. No numerical experiment,
symbolic script, solver run, new input acquisition, or Lean build was
performed. File reads, hashing, primary-source reads, and the displayed
conventional derivations are the evidence. One early attempted lower
source read used a nonexistent guessed T82 filename; the actual file
was located and read completely before using it.

The proved candidate scope is precisely (1.1)--(1.3) for each fixed
normalized odd power and its explicitly scaled transfer (11.2).
It does not establish a full long-horizon theorem for every inward
polynomial, degree-uniform constants, uniformity as diffusivity tends
to zero, exact paid-work Theta order, finite-bit complexity, or an
end-to-end formalization. The unchanged-class claim refuted in
Section 11 is not silently replaced by the scaled theorem. Root
independent review and source/model correspondence are required before
acceptance. The final file SHA is reported separately after self-review.
