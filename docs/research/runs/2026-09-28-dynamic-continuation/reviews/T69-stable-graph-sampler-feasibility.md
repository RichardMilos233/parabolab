# T69: a finite-variance derivative sampler for the local stable graph

Date: 2026-09-29. Complete conventional proof candidate, frozen for
independent audit. The sole T69 edit is this file. Frozen sources,
ledgers, Lean, code, experiments, and other artifacts were not changed
by this work.

**Verdict: GO candidate for the derivative-sampling gate, in the explicit
ideal real-arithmetic/random-primitive model below.** For every fixed
finite derivative order `j>=1`, there is an actual point-tuple sampler
for `D^j H_L(g)`, where

    H_L(q)=Pi S_Lq-Theta(Q S_Lq),

with a residual factor `delta^j`, a uniformly finite coefficient second
moment, at most `j` new unknown initial-value calls on every path, and
finite expected primitive work independent of the final horizon `T`
when the paid `g` representation has uniformly bounded lookup cost.
More generally the expected-work bound is affine in a uniform lookup
bound `Gg(T)`, so polynomial lookup cost gives polynomial sample work.
The input remains the fixed signed class: `g` is its paid coarse
interpolant, and `e=v-g` is queried only at selected original-data points.
Neither `Q S_Lg` nor `Theta` is supplied as an oracle.

This statement does not complete R08's arithmetic-work objective. It
does not evaluate the base value `H_L(g)` to error `O(exp(-T))` at
near-query-order work. A constant-variance base estimator is constructed
as an ingredient, but ordinary averaging of it retains an
`O(exp(2T))` sufficient sample count for that accuracy. No lower bound
against better base algorithms is claimed.

The decisive mechanism is a squared-weight majorant with a positive
leaf-count exponential moment. A small deterministic centered field
alone is not used as a variance bound. A fixed, possibly immense,
number of independent burn-in samples makes the *RMS* of each unmarked
leaf small enough. The full cost of those samples is retained.

## 1. Objects, fixed constants, and exact scope

Use the normalized unit torus `X`, Haar measure `lambda`, heat semigroup
`P_t` for `Delta/2`, `Pi` for averaging, `Q=I-Pi`, and the actual flow

    u_t=Delta u/2+u-u^3,       S_tq=u(t).

The local graph `Theta` and constants are those constructed in frozen
T65. For clarity we use their explicit choice

    lambdaH=2*pi^2,   nu=lambdaH-1,   sigma=1,
    qH=exp(-lambdaH),
    rho=((1+qH)/(1-qH))^d,
    M=2*rho*exp(lambdaH),
    C=M/(nu-sigma)+1/(1+sigma).

Choose the same sufficiently small `R>0` and `r=R/(4M)` as in T65,
in particular

    C R^2<=1/8.                                      (1.1)

Retain the other T65 conditions if the graph is used in its phase
proxy. Define the positive public amplitude envelope

    a=3r=3R/(4M).                                    (1.2)

This `a` is a bound chosen in advance, not an observed leaf value.
No algorithm below divides by `w(y)` or by any noisy estimate of it.

Fix the T65 burn-in `L` with

    sup_(||q||<=7/8) ||Q S_Lq||infinity<=r/16.          (1.3)

It is independent of `T`. We need `||g||<=3/4`, as ensured by the
paid interpolation threshold. All neighborhoods used to differentiate
at `g` stay in the `7/8` ball. The residual is continuous and satisfies
`||e||<=delta`; no sign separation from the stable manifold is imposed.

R10b/T68 supply actual finite-time derivative tuple samplers. At a
specified root `y`, their centered version estimates

    D^b(Q S_L)(g)[e,...,e](y)

with at most `b` paid initial-value calls and a representation
`A_b product_(ell=1)^b e(Z_ell)` whose coefficient has

    E A_b^2<=V_b,
    V_b=4 exp(2(3^(2b)-1)L),       b>=1.               (1.4)

The bound follows directly from their selected-leaf coefficient bound,
so it does not require dividing by residuals or assuming nonzero
residual values. Their primitive expected work is finite, uniformly
in the root and `g`, with their `2^b` tree passes fully charged.

The stochastic part of the work model permits exact exponential,
Gaussian and uniform draws, basic real arithmetic, comparisons,
modular reduction, floor/integer indexing, random-access stored-value
reads, and fixed public computable constants. It is the continuous-seed
ideal model of R10b/T68. A known-profile `g` evaluation is charged its
actual cost `Gg`, rather than declared free. Counting it as one primitive
recovers the simpler R10b/T68 convention; Section 10 states the fully
costed formula and R12 correspondence.
No heat-density, total-variation-normalizer, stable-graph, evolved-value,
or global-phase evaluation primitive is added. Even a variable cosine
or exponential evaluation is unnecessary in the stochastic kernel rules:
the construction below implements the needed values by bounded random
estimators and clocks.
Finite-bit and rounding complexity remain outside this theorem.

## 2. A normalized centered-heat sampler with a uniform second moment

Write

    B_tau=exp(tau)(P_tau-Pi).

For every `tau>=0` and root `x`, we construct a point `Y` and a real
coefficient `beta` satisfying, for every bounded Borel `f`,

    E[beta f(Y)] = exp(nu*tau) B_tau f(x)/M,
    E beta^2<=1.                                      (2.1)

The expectation is over an explicitly simulable seed. Its expected
primitive work is uniformly bounded in `tau,x` by a finite constant
depending only on fixed `d`. This preserves the stable heat decay in
the *sample second moment*. A plain heat-versus-uniform coin used at
every lag would instead need a normalized weight growing like
`exp(2*pi^2*tau)` and would not prove (2.1).

### 2a. Two elementary random primitives

For any known `z>=0`, a fresh rate-one exponential `E` gives

    J_z=1_(E>=z),       E J_z=exp(-z),       J_z^2=J_z. (2.2)

Thus a decaying coefficient can be implemented by one clock comparison.
Its argument may be arbitrarily large; its ideal operation count does
not depend on that argument's bit length.

For an angle `theta` reduced modulo `2*pi` to `[-pi,pi]`, let
`K` be Poisson with mean `pi`, generated as the number of successive
rate-one exponential arrivals before time `pi`. Set

    Ctheta=exp(pi)*(theta/pi)^K*c_K,
    c_K=1,0,-1,0 according as K mod 4=0,1,2,3.          (2.3)

The Poisson probabilities follow from the exponential waiting-time
simplex formula. Summing them gives

    E Ctheta=sum_(k>=0) c_k theta^k/k! = cos(theta),
    |Ctheta|<=exp(pi).

Let `Kcos=ceil(exp(2*pi))` and average `Kcos` independent copies to
obtain `Cbar_theta`. Then

    E Cbar_theta=cos(theta),
    E Cbar_theta^2
      =cos(theta)^2+Var(Ctheta)/Kcos<=2.                (2.4)

Each copy uses expected `pi+1` exponential draws and at most a fixed
multiple of `K+1` scalar operations, by forming the integer power by
repeated multiplication. Thus this is a finite expected-work cosine
estimator with a uniform second-moment bound. It does not call a
trigonometric oracle. All replicas are independent conditional on
the known angle.

### 2b. Short lags

For `0<=tau<1`, flip a fair coin. On heads take
`Y=x+N(0,tau I) modulo X` and sign `+1`; on tails take an independent
uniform `Y` and sign `-1`. Independently draw `J_(lambdaH(1-tau))`
and set

    beta=sign * [2 exp(lambdaH)/M]
                    * J_(lambdaH(1-tau)).             (2.5)

Since `nu+1=lambdaH`, its mean is
`exp(lambdaH*tau)(P_tau-Pi)f(x)/M`, exactly (2.1).
Moreover `2exp(lambdaH)/M=1/rho<=1`, so `E beta^2<=1`.
At `tau=0` the Gaussian endpoint is simply `x`. Every operation is
defined there as well.

### 2c. Long lags without a heat-density oracle

For `tau>=1`, sample `n in Z^d\{0}` with probability

    p_n=qH^(|n|_1)/(rho-1).                            (2.6)

An explicit sampler takes independent coordinates with probabilities
proportional to `qH^|n_i|` and rejects the all-zero vector. Each
coordinate can use a zero-versus-nonzero coin, a fair sign, and a
geometric magnitude. Explicitly, its zero probability is
`(1-qH)/(1+qH)`; conditional on nonzero, the positive magnitude has
probability `(1-qH)qH^(k-1)` at `k>=1`, and the sign is fair.
The magnitude can be generated by repeated uniform comparisons,
with mean `1/(1-qH)`. The normalization is
`sum_(m in Z) qH^|m|=(1+qH)/(1-qH)`. Thus the all-zero rejection
succeeds with probability `(rho-1)/rho>0`; the expected number of
proposals is `rho/(rho-1)`, finite for every fixed `d>=1`.

Take `Y` uniform on `X`, independently. Put

    z=lambdaH*((|n|^2-1)*tau-|n|_1+1)>=0,
    Aconst=(rho-1) exp(lambdaH)/M=(rho-1)/(2rho),
    theta=2*pi*n dot (x-Y), reduced to [-pi,pi],
    beta=Aconst * J_z * Cbar_theta.                    (2.7)

The nonnegativity of `z` follows from `tau>=1`, `|n|^2>=1`, and
`|n|^2>=|n|_1`. Conditional on `n,Y`, the clock and cosine-estimator
randomness are independent. Equations (2.2)--(2.4) give

    E beta^2<=2 Aconst^2<=1/2.                         (2.8)

For the mean, the product of the mode probability and its expected
coefficient is exactly

    p_n Aconst exp(-z)
       =exp(lambdaH*tau)*exp(-lambdaH |n|^2 tau)/M.

The absolutely convergent real Fourier series on the unit torus is

    p_tau(x-y)-1
      =sum_(n!=0) exp(-lambdaH |n|^2 tau)
                                    cos(2*pi*n dot(x-y)).

Integrating against `f` proves (2.1). Both signs of every Fourier
index are included in (2.6); there is no omitted factor two.

The coordinate geometric draws have finite expected length. Reducing
the angle and computing its dot product costs `O(d)` unit scalar
operations. A useful coarse bound for the expected heat-sampler work is

    Kheat(d)<=C0[(d+1)rho/(rho-1)+Kcos(pi+1)],           (2.9)

with a fixed numerical `C0`. It is uniform in lag and root. The
possibly large Fourier indices and clocks require no bounded-bit
claim. This proposal uses an explicitly known geometric normalizer,
not the unknown total variation of a signed heat kernel.

## 3. Time-weighted Lyapunov--Perron primitives

Let `u(w)` be T65's decaying trajectory and put

    V(w;t,x)=exp(sigma*t)u(w;t,x).

Its fixed-point equation is

    V=A_w+K(V^3),
    A_w(t)=exp(sigma*t)B_t w,

    (K F)(t,x)
      =-integral_0^t exp(sigma*t-3sigma*r)
                                     B_(t-r)F(r)(x) dr
       +integral_t^infinity exp(sigma*t+t-r-3sigma*r)
                                     Pi F(r) dr.       (3.1)

This is just T65's equation after multiplying by the time weight;
the plus sign in the infinite backward mean integral is preserved.

For the source, invoke Section 2 at lag `t`, obtaining `Y,beta`, and
independently draw `J_((nu-sigma)t)`. Define

    ell=M beta J_((nu-sigma)t).

Then

    E[ell f(Y)]=exp(sigma*t)B_t f(x),
    E ell^2<=M^2.                                    (3.2)

For the nonlinear integral define

    Cf=M/(nu-sigma),       Cb=1/(1+sigma),       C=Cf+Cb.

With probability `Cf/C`, use the forward rule:

* Draw `A` exponential with rate `nu-sigma`.
* If `A>t`, set `Omega=0` and assign a harmless dummy child state,
  for example `(0,x)`. This is the killed part of the time proposal.
* Otherwise set `r=t-A`, obtain `(Y,beta)` from Section 2 at lag
  `A` and root `x`, and set `Omega=-C beta J_(2sigma*r)`.

With probability `Cb/C`, use the backward rule:

* Draw `A` exponential with rate `1+sigma`, set `r=t+A`, take
  `Y` uniform, and set `Omega=C J_(2sigma*r)`.

All displayed clock thinnings use fresh independent clocks. Direct
substitution of the proposal densities shows

    E[Omega F(r,Y)]=(K F)(t,x),
    E Omega^2<=C^2,                                  (3.3)

uniformly in the current state. For example the forward density is
`M exp(-(nu-sigma)A)/C`; using (2.1) leaves exactly
`-exp(sigma*A-2sigma*r) B_A F(r)`, as in (3.1).
The backward density leaves
`exp(-(1+sigma)A-2sigma*r) Pi F(r)`, also exactly (3.1).

These are second-moment bounds for the actual random coefficients.
The clock-thinned coefficients need not be bounded pathwise by their
decaying means. Both time directions, every integration tail, and
the heat cancellation have been included in the sampling law.
The expected work of either rule is at most `Kheat(d)` plus a fixed
number of clock, root, and scalar operations.

## 4. A subcritical tree with a squared-weight exponential moment

At each outer node independently choose three children with probability

    p=1/6,

or choose a leaf with probability `1-p=5/6`. At a leaf in state
`(t,x)`, use (3.2), record its point `Y`, and give it coefficient
`ell/(1-p)`. At a branching node, use (3.3), give the node coefficient
`Omega/p`, and start all three independent child subtrees at the
same sampled state `(r,Y)`. Common child state is necessary for the
cube in (3.1).

For clean accounting one may generate the whole Galton--Watson tree,
even if a coefficient is zero. Dummy states for killed proposals are
then arbitrary public states; all descendants of such a vertex have
total coefficient zero. Skipping that zero subtree is an optional
cost reduction, not required by the theorem.

The mean offspring count is `3p=1/2`. If `N` is the number of leaves,
the tree is finite almost surely and

    E total_nodes=1/(1-3p)=2,
    E N=(1-p)/(1-3p)=5/3.                             (4.1)

For instance the expected size of generation `k` is `(3p)^k`;
summing gives finite expected total population and therefore almost
sure finiteness. This proof does not assume that small analytic
operator norm makes a supercritical simulation terminate.

Let `K_T` be the product of all source and branch coefficients, so
the terminal functional for a known `w` is the monomial

    K_T product_(i=1)^N w(Y_i).                        (4.2)

The shape and every coefficient law are independent of `w` and of
the unknown residual. Leaves are distinct labels even when their
spatial points agree.

Here is the main quantitative gate. For `z0=5/4`,

    sup_(t,x) E[K_T^2 a^(2N) z0^N] <=R^2.             (4.3)

To prove it, first restrict to trees of height less than `D`, setting
the coefficient to zero otherwise. Let `F_D(z)` be the supremum over
the starting state of the corresponding weighted second moment.
Equations (3.2)--(3.3), conditional independence of the three children,
and their uniform statewise bounds give

    F_(D+1)(z)<=alpha*z+beta2*F_D(z)^3,
    alpha=M^2 a^2/(1-p),       beta2=C^2/p,
    F_0(z)=0.                                        (4.4)

This induction only uses *conditional* squared envelopes at each
current state. Coefficients may be correlated with their sampled child
states or leaf positions. Bounding the descendant moment uniformly
before averaging the current coefficient is what makes (4.4) valid.

With (1.1)--(1.2) and `p=1/6`,

    alpha*z0=(27/32)R^2,
    beta2*R^6<= (3/32)R^2,
    alpha*z0+beta2*R^6 <= (15/16)R^2<R^2.              (4.5)

Thus `F_D(z0)<=R^2` by induction. The full tree is finite almost
surely; monotone convergence of the height indicators proves (4.3).
The squared-majorant feedback derivative on `[0,R^2]` also obeys

    3 beta2 (R^2)^2<=9/32<1.                          (4.6)

This is a variance contraction calculation, not an inference from
the deterministic contraction `3CR^2<=3/8`.

For every fixed `j>=1`, define the finite public number

    Aj=sup_(n>=1) n^(2j) z0^(-n)
       <=(2j/(e*log(z0)))^(2j).

Then (4.3) gives the weighted leaf-count estimate

    E[N^(2j) K_T^2 a^(2N)]<=Aj R^2.                   (4.7)

The positive factor `z0>1` is essential: a plain unweighted
second-moment bound alone would not justify removing several small
leaf factors or multiplying by high-order label counts.

## 5. The tree mean is the actual local graph

Suppose first that `w` is a known continuous mean-zero profile with
`||w||<=2r`. Let `Vhat(w;t,x)` be (4.2). Equation (4.3) gives a
uniform second-moment bound at most `R^2`. Conditional on the first
node, its expectation therefore satisfies

    Vbar=A_w+K(Vbar^3).                                (5.1)

Integrability of the branch product follows from the uniform second
moments and independence of its children conditional on their common
state. The leaf/branch probabilities cancel their importance factors
`1/(1-p)` and `1/p` exactly. All countable series and expectations
are consequently absolutely integrable.

The fixed-point map in (5.1) has deterministic Lipschitz constant at
most `3CR^2<1` on the bounded radius-`R` ball. This uniqueness holds
even in bounded Borel trajectories, so no unproved continuity of a
measure-valued random variable is needed. T65's continuous solution
is in that ball, as is `Vbar` by Cauchy--Schwarz. They therefore agree:

    E Vhat(w;t,x)=exp(sigma*t)u(w;t,x).                 (5.2)

Taking a uniform starting root at time zero yields an unbiased
estimate of `Theta(w)=Pi u(w;0)`. This identification uses the actual
Lyapunov--Perron solution, not a new definition of the graph.

For differentiation, a fixed outer tree is a polynomial in point
values of `w`. Its order-`j` derivative is bounded on a smaller
neighborhood of the base profile by

    |K_T| N^j a^(N-j) product_l ||h_l||.               (5.3)

An integrable envelope follows from (4.3) and Cauchy--Schwarz:

    E[|K_T| a^N N^j]
      <=(E[K_T^2 a^(2N)z0^N])^(1/2)
           (E[N^(2j)z0^(-N)])^(1/2)
      <=R sqrt(Aj).                                  (5.4)

The same bound at the next orders controls Taylor remainders and
operator continuity. The base profile has room inside `a=3r`;
small perturbations also stay in T65's local domain. Differentiation
of the expectation is therefore justified at every fixed finite order.
Directions need not be small after taking a derivative; their norms
enter by homogeneity.

For non-mean-zero directions, the functional represented by (5.2)
at time zero with a uniform root is `F(z)=Theta(Qz)`, because each
source uses `B_t` and annihilates constants in expectation. Thus the
sampler below estimates `D^jF(w)` in arbitrary continuous directions,
or `D^jTheta(w)` when the directions are mean zero. Neighborhoods
can be chosen to satisfy both `||z||<3r` and `||Qz||<3r`; for a
mean-zero base with norm at most `2r`, a perturbation of norm below
`r/4` suffices.

## 6. Direct graph derivatives when the small base profile is known

When `N>=j`, choose a uniform ordered injection `I` of the `j`
direction labels into the outer leaves. For a diagonal direction `h`
with `||h||<=delta`, return

    ZTheta_j=(N)_j K_T
        *product_(i not in I) w(Y_i)
        *product_(ell=1)^j h(Y_(I_ell)).               (6.1)

When `N<j`, return zero. There is no division by a leaf value.
Conditional tuple averaging gives the ordinary ordered-injection
derivative of (4.2), including its `j!` multiplicity. Sections 4--5
justify averaging over the tree. With a uniform starting root at
time zero, the mean is the corresponding derivative of the graph.

The coefficient independent of `h` has second moment at most

    a^(-2j) E[N^(2j)K_T^2 a^(2N)]
       <=a^(-2j) Aj R^2.                              (6.2)

Consequently `E ZTheta_j^2<=delta^(2j) a^(-2j)AjR^2`.
This is the explicit joint derivative envelope requested in the
handoff: removing `j` small factors costs the fixed public `a^(-2j)`,
and weighted leaf-count moments pay for all ordered labels.

If `h=v-g`, there are at most `j` new initial-value acquisitions.
Known base values `w(Y_i)` have finite expected count `E N=5/3`;
the actual cost of evaluating their known formula must be charged.
This simpler subroutine is not yet the `H_L` implementation, because
`w=Q S_Lg` in that implementation is not available as an exact known
formula. The next sections remove that obstacle.

## 7. Small RMS base leaves from actual burn-in samples

For a point `y`, use the bounded primal voting tree from R10b to
construct a centered flow sample `C_y(g)`:

* On heads, root at `y` and return twice the primal tree value.
* On tails, root at an independent uniform point and return minus
  twice the primal tree value.

Then, with `w_g=Q S_Lg`,

    E C_y(g)=w_g(y),        |C_y(g)|<=2.                (7.1)

Its expected work includes a complete rate-two burn-in tree, of
expected leaf count `exp(4L)`, and all its known `g` evaluations.
It acquires no new unknown `v` values. It is a simulation of the
actual finite-time flow, not an evolved-value oracle.

Choose the fixed positive integer

    Kbase=ceil(8/a^2),

and average `Kbase` independent copies at that point:

    Wbar_y(g)=Kbase^(-1) sum C_y^(m)(g).

By (1.3),

    E Wbar_y(g)=w_g(y),
    E Wbar_y(g)^2
       <=(r/16)^2+4/Kbase
       <=a^2/2304+a^2/2<a^2.                         (7.2)

This calculation is uniform in `y` and in the whole `7/8` input
ball. It explicitly proves small RMS using an independent batch.
The deterministic inequality `||w_g||<=r/16` alone would not prove
(7.2) for one centered coin sample.

Every outer unmarked leaf uses its own independent batch, conditional
on all outer tree states and points. Reusing one batch in two factors
would generally invalidate the product means and squared majorants.
`Kbase` can be extremely large, but is fixed by `d,L,R,r` and does
not depend on the final horizon, interpolation size, residual size,
or requested final accuracy. Its full factor is included in work.

Replacing each leaf value in (4.2) by an independent `Wbar` therefore
gives an unbiased estimator of `V(w_g;t,x)` with second moment at
most `R^2`, by the same induction (4.4). This already constructs a
base graph-value estimator without knowing `w_g` exactly. It does
not make exponentially accurate base evaluation cheap.

## 8. Composed graph derivatives: label maps instead of injections

Let

    G(q)=Theta(Q S_Lq).

For the fixed outer tree, conditional mean of the independent base
leaves is the smooth scalar function

    F_T(q)=K_T product_(i=1)^N w_q(Y_i),
    w_q=Q S_Lq.                                      (8.1)

Its order-`j` derivative is the sum over all maps
`f:[j]->[N]`, not just injections. For leaf `i`, put
`B_i=f^(-1)(i)` and `b_i=|B_i|`. The term corresponding to `f` is

    K_T product_(i:b_i=0) w_q(Y_i)
        *product_(i:b_i>0)
            D^(b_i)w_q[h_l:l in B_i](Y_i).             (8.2)

Each direction label chooses which factor it differentiates. This
gives exactly `N^j` terms, with no additional multinomial or `j!`
factor. Multiple labels at one outer leaf are allowed because
`w_q` is nonlinear in `q`.

The interchange with outer expectation is justified independently of
the randomized implementation. On a neighborhood of `g` inside the
`7/8` ball, `||w_q||<=r/16<a`, and R10b/T68 give uniform finite
operator bounds on each `D^b w_q`. Let `Db` be any such public bound.
For example `Db=sqrt(V_b)` follows from the same mixed-direction
coefficient bound and Cauchy--Schwarz.
For each fixed `j`, define

    Rj=max_(b_1+...+b_k=j; b_i>=1)
                       a^(-k) product_i D_(b_i).

Then the operator norm of (8.2), summed over its label maps, is at
most `|K_T| a^N N^j Rj`. Equation (5.4) is a uniform integrable
majorant. The same reasoning through order `j+1`, together with the
finite-time derivative continuity, controls integral Taylor remainders.
Therefore the expectation of (8.2) is the actual `D^jG(g)`. This
does not differentiate a noisy mean by an unsupported interchange.

Here is the actual estimator of that derivative in direction
`e=v-g`.

1. Generate the outer tree at time zero with a uniform starting root,
   retaining its `N` leaf points and coefficient `K_T`.
2. Choose `f` uniformly from its `N^j` maps by drawing `j` independent
   uniform integers from `1,...,N`. Form the counts `b_i` and retain
   the individual direction labels in their fixed order.
3. At an unmarked leaf (`b_i=0`), sample the independent batch
   `Wbar_(Y_i)(g)` of Section 7.
4. At a marked leaf (`b_i>0`), use a fresh R10b/T68 centered
   order-`b_i` derivative sampler rooted at `Y_i`, in those direction
   labels. Prepare its coefficient `A_(b_i)` and `b_i` original-time
   tuple coordinates, with coefficient bound (1.4). Residual values
   can be acquired after all outer and inner preparation terminates.
5. Multiply all these leaf returns and `N^j K_T`.

Call the result `ZG_j`. Conditional means at distinct outer leaves
factor because the inner random streams are independent, given the
outer tree and the label map. Averaging over the label map gives
(8.2), and then the tree expectation gives

    E ZG_j=D^jG(g)[e,...,e].                           (8.3)

This is a point-tuple sample at the *original initial time*. Marked
outer leaves call R10b's original-data derivative sampler; they do
not request `evolved e(Y_i)` or `D^bS_L(g)` from an oracle.

Define

    Vstar_j=max(1,max_(1<=b<=j) V_b/a^2).

The whole return has the form

    ZG_j=WGraph_j product_(ell=1)^j e(Z_ell),

where the coefficient and selected initial points depend only on
the known `g`, public parameters, and private randomness. Conditional
on the outer tree and label map, let `k` be its number of marked
leaves. Equations (7.2), (1.4), and independence give

    E[WGraph_j^2 | outer tree, f]
      <=N^(2j) K_T^2 a^(2(N-k)) product_(i:b_i>0) V_(b_i)
      <=N^(2j) K_T^2 a^(2N) Vstar_j^j.                (8.4)

Here `k<=j`; the positive public `a`, not an actual leaf value, is
used in the bound. Integrating and using (4.7) proves

    E WGraph_j^2<=Vstar_j^j Aj R^2,
    E ZG_j^2<=delta^(2j) Vstar_j^j Aj R^2.             (8.5)

If an inner derivative tree has too few leaves, its contribution is
zero and no missing residual values need be queried. Zero coefficients
can use arbitrary dummy tuple coordinates in the mathematical signed
measure representation.

This also gives actual signed product measures by the setwise
expectation `E[WGraph_j delta_(Z_1,...,Z_j)]`. Its variation is finite
by Cauchy--Schwarz and (8.5); countable additivity follows from
dominated convergence. Thus the construction samples actual kernels,
not merely abstract bounded multilinear operators. For mixed directions,
retain each label's own `h_l` in its inner ordered tuple; all arguments
are unchanged and the measure integrates every product
`product_l h_l(Z_l)` to the actual mixed derivative. Continuous product
functions determine a finite measure on the compact product torus,
so this is also the derivative measure identified by T65. Its action
on bounded Borel directions is a measure extension; no assertion of
Frechet differentiation on a different function space is needed.

## 9. The final H derivative and exact query cap

The mean-flow derivative `D^j(Pi S_L)(g)[e^j]` is sampled by the
R10b order-`j` primitive with a uniform root. Its coefficient second
moment is at most

    Vmean_j=exp(2(3^(2j)-1)L).

Choose a fair coin. On heads run that mean derivative sampler and
return twice its value. On tails run Section 8 and return minus
twice its value. Then the resulting `ZH_j` satisfies

    E ZH_j=D^jH_L(g)[e,...,e],
    ZH_j=WH_j product_(ell=1)^j e(Z_ell),
    E WH_j^2<=V_H,j,
    V_H,j=2[Vmean_j+Vstar_j^j Aj R^2],
    E ZH_j^2<=V_H,j delta^(2j).                        (9.1)

For the graph branch, the sum of marked inner derivative orders is

    sum_(i:b_i>0) b_i=j.

Each such sampler uses at most its order in new initial-value calls.
Unmarked batches use known `g` only. Consequently every path makes
at most `j` new unknown `v` acquisitions, including repeats. The
mean branch has the same cap. Choosing one branch by a coin preserves
`j`; computing both branches independently would instead allow `2j`.

One can prepare every tree, tuple, coefficient, and known `g` value
before acquiring any residual values. On a null nonterminating
generation/rejection path, no subsequent data acquisitions take place.
Thus the cap is deterministic on all seeds, not merely an expected
call bound. Arithmetic work and the number of known-profile
evaluations are random and are bounded only in expectation below.

All earlier coarse acquisitions used to construct `g` remain charged
to the enclosing algorithm. This is a per-correction-sample statement
conditional on that already paid transcript, with fresh independent
randomness. There is no uncharged preprocessing access to `v`.

## 10. Work, measurability, and almost-sure halting

The outer tree has expected two nodes and `5/3` leaves. Each node's
expected clock/heat-mark work is bounded uniformly in its potentially
unbounded time state by Section 2. Equation (2.9) counts the geometric
mode rejection and every Poisson cosine replica. Label maps need
`O(N+j)` ideal operations with a leaf array; ordered injections in
Section 6 can use a partial shuffle.

At an unmarked outer leaf, charge `Kbase` complete primal burn-in
samplers. At a marked leaf of order `b`, charge the full R10b
order-`b` derivative sampler, including its at most `2^b` tree
passes and all cached known `g` values. Each burn-in tree has expected
leaf count `exp(4L)` and finite expected primitive work. The inner
streams and their costs may depend on the known outer point, but
their uniform rootwise bounds allow conditional expectation and
then summation over the outer leaves.

If one known `g` evaluation costs at most `Gg` ideal operations,
a finite bound of the form

    E Work(ZH_j)
      <=C_j [Kheat(d)+(Kbase+1)(d+1+Gg) exp(4L)+1]     (10.1)

holds, with a public fixed-order `C_j`. This deliberately charges
the entire nested average and derivative work, as well as at most
`j` unknown acquisitions and their residual subtractions. Its size can be
enormous. It is independent of `T` and `delta` when `d,j,L`, the
graph constants, and `Gg` are fixed. Treating a known `g` evaluation
as a unit primitive gives precisely the R10b/T68 ideal model.

For a paid local interpolant with a bounded stencil, a unit-cost
random-access realization can locate its grid cell by scaled
coordinates and floor/indexing, then inspect only a number of nearby
coefficients and partition functions depending on fixed `d,s`. Its
local polynomial degree is fixed by `s`. If the chosen public partition
functions themselves have bounded evaluation cost in the shared
elementary-operation model, this gives a constant `Gg` independent
of the coarse grid size. For example, a fixed formula using arithmetic,
comparisons and a fixed number of exponential evaluations has that
property when those exponential evaluations are charged as primitives.
This condition is about the explicit saved formula, not an entitlement
to free arbitrary known-function evaluation.

The cost of storing or constructing that coarse data structure is
additional and remains charged once by the enclosing algorithm.
If a different formula, lookup model, or finite-precision implementation
gives a growing `Gg(T)`, that dependence remains in (10.1). In particular,
for any shared representation satisfying

    Gg(T)<=C_g(1+T)^b,

(10.1) proves the sample-work bound `C_j'(1+T)^b` required by
R12's Gate B, with the same fixed-second-moment constants and hard
`j`-call cap. This implication does not assume R12's separate Gate A
has been proved: construction of such a representation, its mean
test, and exponentially accurate base computation remain its own
obligations. The present sampling procedure works for every continuous
`g` in the stated ball and charges whatever lookup bound its supplied
paid representation actually has.

The times along an outer branch may move into the future and have
unbounded range. They are finite on each finite tree because every
clock is finite almost surely. No PDE is evolved up to those random
large times: only the explicit heat/time primitives use them. Every
known-profile simulation still has the fixed finite duration `L`.
This distinction is necessary for the horizon-independent cost bound.

All index distributions, endpoint locations, coefficients, root
translations, thinnings, and finite tree operations are Borel in
their parameters and the countable product seed. Concretely, label
potential vertices by finite words over `{1,2,3}` and assign each a
countable independent array of marks for its clocks, heat proposal,
cosine replicas and any nested burn-in trees. Finite completion events
and all returns on them are Borel; extend returns by zero on the null
noncompletion event when defining expectations. The mode proposal
has positive acceptance probability, the Poisson arrival construction
terminates almost surely, the outer tree is subcritical, and each
of the finite number of inner burn-in trees terminates almost surely
by R10b. Conditional on the finite outer tree, all finitely many
inner averages therefore terminate almost surely. The final sampler
is measurable and halts almost surely for every promised input.

Variation in `g` is also measurable. In the sup-norm topology,
`(g,y)->g(y)` is continuous on `C(X) x X`. Every finite-tree return
and coefficient is a finite polynomial in such values; partial
evaluation at corners in R10b is still a polynomial. This gives the
needed Borel dependence on a paid coarse transcript. No choice of
a norm-minimizing representation or nonmeasurable measure sampler
is hidden in the construction.

The unit-cost assumptions do not bound bit lengths of the random
Fourier indices, random time states, importance products, or stored
coarse coefficients. Exact Gaussian/uniform locations and ideal
known-function evaluations are not a finite-bit program. Rounding,
random-bit simulation of continuous locations, and conditioning of
large cancellations need their own analysis.

## 11. Relation to Neumann kernels and the failed shortcuts

The construction expands the full cubic Lyapunov--Perron fixed point
rather than sampling coefficients `u(t,x)^2` from an unavailable
stable trajectory. When marked labels all pass into one child at
a cubic vertex, the two other unmarked subtrees have mean `u`;
summing the three possible child choices gives the differentiated
feedback `3u^2 D^j u`. Thus grouping marked paths reorganizes the
same signed Neumann kernels as in T65.

The direct variance control is stronger than the deterministic
operator calculation: (4.4)--(4.6) provide a squared-weight
contraction with slope at most `9/32`, while (4.3) at `z0>1` pays
for every fixed number of derivative labels. This proves convergence
and second moments for the actual recursive sampler, including
both time directions and every centered heat mark.

Three tempting shortcuts would leave the gate open:

* Sampling `P_tau-Pi` by an unscaled coin for all times and then
  attaching the unstable `exp(tau)` factor loses the needed
  uniform second-moment envelope. Section 2's long-lag Fourier
  proposal restores the spectral decay in the sampling law.
* Using one noisy centered burn-in value because its expectation
  is small would not imply a small leaf second moment. Section 7
  explicitly pays `Kbase` independent samples to obtain (7.2).
* Differentiating a tree by dividing its product by selected
  actual `w` values would be undefined at zeros and would not
  preserve a uniform bound. Sections 6 and 8 multiply only the
  required unmarked factors and use the positive public `a` in
  the analysis, never in such a division.

There is also no independence assumption across repeated spatial
points of the unknown input. The input is fixed. Independence is
required between inner random simulations conditional on the outer
tree, and fresh leafwise batches explicitly provide it.

## 12. What remains for the global work objective

The derivative portion of a fixed-order residual Taylor estimator
can now be averaged directly without a fine partition coefficient
tensor: (9.1) gives standard deviation at most
`sqrt(V_H,j)delta^j/sqrt(n)` from `n` independent samples, at most
`jn` new unknown values, and expected ideal work proportional to
`n` with the fixed constant in (10.1). Taylor coefficients still
divide the raw derivative estimates by `j!`.

This is a candidate resolution of R08's derivative-sampling obligation
for the actual local proxy `H_L`, including its burn-in composition.
It is not just a sampler for a separated signed subclass or for a
supplied phase functional. The constants are uniform over the paid
interpolants in the fixed input class and do not depend on distance
to the stable manifold.

The base value remains separate. Taking no derivative labels yields
an unbiased finite-variance graph-value estimator from Section 7,
and a primal mean-flow sample gives an unbiased `H_L(g)` estimate.
That fact alone gives no near-query-order way to attain error
`eta=O(exp(-T))`: an ordinary sample-average guarantee uses
`O(eta^(-2))=O(exp(2T))` samples with a fixed variance bound.
The tiny but fixed graph constants do not change that asymptotic
precision exponent. This is a limitation of that averaging route,
not a universal lower bound against known-profile computation.

Neither practical efficiency, all-dimension finite-bit complexity,
nor a matching arithmetic-work theorem is established. The Fourier
rejection, cosine averaging, `Kbase`, fixed burn-in, and high-order
moment constants may be prohibitive in practice. No numerical run
or executable implementation is authorized by this theory note.

## 13. Provenance and next audit boundary

Read as dependencies and scope controls: frozen T65, R10b, T68, R08,
and the later conditional interface R12. The new sampling law and its
squared majorant are derived above; they are not inferred from existence
of T65's finite-TV measures.
R10b/T68's majority representation and its attribution remain their
explicit predecessors. No new literature theorem is used to fill
a sampling or variance obligation, and no publication-priority or
novelty claim is made.

Source hashes checked for T69:

    T65-local-stable-graph-upper-proof.md
    58e862c9cfbaf0946605d30d9c8e8a37e2570c0c0719d626683f22db60fc9f81

    R10b-finite-burnin-derivative-sampling.md
    23683587539ef2905e0679100325808ae3f6353a3782a4bb362b2d24252034f0

    T68-finite-burnin-sampler-independent-audit.md
    442b446ae523b220e34ddadcf8c23b181ce60104100fd27c7e8027524840ed9f

    R08-signed-arithmetic-work-gates.md
    f4ff50a6f56750ac010e7a6778499e6786fd2eda0fa7b24acf2c1bc00834a756

    R12-signed-work-composition-contract.md
    390ede56727253adb0c23fb5356671f6b691b5c958ff4258d0e69ceeafd280ee

The highest-risk independent review points are (2.6)--(2.8)'s
normalized Fourier sampling, the two time proposals in Section 3,
the conditional-state induction (4.4) and its `z0>1` margin,
the all-label-map composition and squared envelope (8.4), and the
full nested cost/query accounting. All are part of the claimed
conventional derivation; none is deferred as an assumed lemma.
Independent acceptance of this new candidate remains pending.

Research-role metadata: T69 was assigned the skill's
`gpt-6-astra`/`max` routing. This worker made no model-setting change;
its actual backend and effort are not independently exposed in the
tool context. Work performed: source reading, hash inspection,
conventional derivation and review, and this single file write.
No agent delegation, Lean, code, numerical execution, ledger change,
or new primary-literature search was performed. The final file hash
is reported in the handoff rather than self-embedded.
