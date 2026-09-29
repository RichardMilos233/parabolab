# A noncompact all-horizon counterpoint

Status: conventionally proved and independently reviewed in
`reviews/T15-noncompact-quadratic-audit.md`, including signed correspondence
and the sharp dimension split below. The finite coefficient Lean gate is
being translated separately; no numerical validation or novelty claim.
The compactness assumption
in D10 is essential; this note constructs a specific way it can fail on R^d.

## Target and original moment equations

Let d>=5, 0<epsilon<=1/32, and v(x)=epsilon exp(-|x|^2) on R^d. Consider
the original derivative-coded expansion for f(u)=-u^2 (the absolute system
is the same for f(u)=u^2). Keep exact likelihood weights, genuine support
and almost-sure completion. Let L=Delta/2 and use

    A=W_F0, B=W_F1, D_i=W_(partial_i), W_F2=2.

All higher reaction codes have zero finite-tree weight. The nonnegative
canonical system, understood first as finite-tree Picard iteration, is

    (partial_t-L)A = A B + sum_i D_i^2,
    (partial_t-L)B = 2 A,
    (partial_t-L)D_i = B D_i,
    (partial_t-L)W_Id = A.

Initial values are v^2, 2v, |partial_i v| and v respectively. It is enough
to exhibit a finite nonnegative supersolution of these finite-code mild
equations at every horizon. Monotone iteration is then bounded without
differentiating a possibly infinite moment.

## Explicit heat-envelope construction

Put

    G(t,x)=(1+t)^(-d/2) exp(-|x|^2/[2(1+t)]),
    w(t)=(1+t)^(-d/2),
    I0=integral_0^infinity w(t)dt=2/(d-2),
    I1=integral_0^infinity t w(t)dt=4/[(d-2)(d-4)],
    C=2+16 d I0.

Then (partial_t-L)G=0 and G^2<=wG. Initial values obey

    v<=epsilon G(0), v^2<=epsilon^2 G(0),
    |partial_i v|<=2epsilon G(0).

The last bound follows from |x_i|exp(-|x|^2/2)<=1. Define

    b(t)=2epsilon+2C epsilon^2 t,
    J(t)=integral_0^t b(s)w(s)ds,
    Jinf=2epsilon I0+2C epsilon^2 I1,
    delta(t)=2epsilon exp(J(t)),
    a(t)=epsilon^2+C epsilon^2 J(t)
                     +4d epsilon^2 exp(2Jinf) integral_0^t w(s)ds.

For d>=5, I0<=2/3, I1<=4/3 and C<=166/3. Therefore

    Jinf <= 1/24+83/576 = 107/576 < 1/4.

Using exp(1/2)<2 gives

    a(t)/epsilon^2 <= 1+C/4+8d I0 = 3C/4 < C.

Direct differentiation now yields

    a' >= w(a b+d delta^2),
    b'=2C epsilon^2 >= 2a,
    delta'=w b delta.

Consequently

    Abar=aG, Bbar=bG, Dbar_i=delta G,
    Wbar_Id=(epsilon+C epsilon^2 t)G

are componentwise supersolutions, because each nonlinear product contributes
G^2<=wG. All dominate the initial terminal-code magnitudes. Thus at every
finite time and every x,

    E|H_Id(t,x)| <= (epsilon+C epsilon^2 t)G(t,x) < infinity.

The bound tends to zero as t grows for each fixed x. It is independent of the
supported importance proposal because it bounds the canonical absolute mass.
An ordinary fixed-rate proposal with finitely many offspring per event
completes almost surely at every finite horizon, so the contract is nonempty.

The signed absorption PDE u_t=Lu-u^2 with this nonnegative datum is globally
well posed and bounded by P_t v. T15 Section 4 verifies that its fields
(u,-u^2,-2u,-2,partial_i u) solve the signed normalized finite-code system.
On any finite time interval both these fields and the absolutely integrable
tree expectations are bounded; the polynomial reaction is Lipschitz on the
resulting bounded range. Sup-norm Gronwall uniqueness identifies the two
finite mild systems and proves E H_Id=u. The detailed regularity and uniqueness
bridge is part of that reviewed proof, not inferred from integrability alone.

## What this does and does not settle

This refutes extending D10's compact-domain obstruction to all of R^d:
the reaction is nonlinear, the datum nonconstant and nonzero, but the same
original tree is absolutely integrable for all finite horizons. Heat
dispersion replaces the positive uniform seed available on a compact torus.

It is a first-absolute-moment result only. No uniform second moment, efficient
implementable importance proposal, root-count improvement or floating-point
guarantee follows. A fixed-rate full tree can still have exponential work.
For the specified small Gaussian family, d>=5 is the sharp dimension threshold.
The smallness constant 1/32 is deliberately conservative and not optimized.

## Low-dimensional obstruction, including the borderline

Discard the D_i terms and use the cooperative radial system

    A_t=LA+AB, B_t=LB+2A,
    A(0)=epsilon^2 exp(-2|x|^2), B(0)=2epsilon exp(-|x|^2).

T15 Sections 5–7 give the full conventional proof using finite positive
Picard approximations and extended nonnegative tree sums. Radial
monotonicity is preserved. For a fixed final T, average with P_(T-t) at x=0.
Positive correlation of two radial decreasing functions under the same
radial Gaussian law gives a'>=ab and b'=2a, with
a(0)=epsilon^2(1+4T)^(-d/2). Setting z=(b-b(0))/2 then gives

    z'>=a(0)+b(0)z+z^2.

A Riccati bound makes existence to T impossible whenever

    T > [pi/(2epsilon)](1+4T)^(d/4).

This inequality holds for sufficiently large T if d<4. The review proves
divergence of the Id integral at every x using heat-kernel comparison, with
strictly positive remaining time. It avoids differentiating infinite moments.

For d=4, use the explicit finite Gaussian mixture

    L_A(t)=P_t A(0)+integral_0^t P_(t-s)[2s(P_s A(0))^2]ds.

It lies below A and has mass

    epsilon^2*pi^2/4 + epsilon^4*pi^2/128
      * [log(1+4t)+(1+4t)^(-1)-1].

Every Gaussian in this mixture has variance at most t+1/4. At
t0=(exp(1+512*pi^2/epsilon^4)-1)/4 its mass exceeds 4*pi^4.
A backward heat average over an extra T=t0+1/4 therefore has a Riccati
seed greater than pi^2/(4T^2), forcing divergence strictly before the
additional horizon. In particular the original Id absolute moment is infinite
at every x for every t >= (2*exp(1+512*pi^2/epsilon^4)-1)/4.
This deliberately enormous bound is not the exact critical time.

Consequently, for each 0<epsilon<=1/32 and integer d>=1 in this Gaussian
family, all-finite-horizon absolute integrability holds iff d>=5. The signed
absorption PDE remains global in every dimension. Large high-dimensional data
and other terminal profiles are not classified.

These are established Fujita-type methods applied to the coding-tree moment
system. The reduced system, after swapping and rescaling components, is the
mixed-exponent case (0,1,1,1) in the scope of the abstract of
[Escobedo–Levine (1995)](https://link.springer.com/article/10.1007/BF00375126).
The exact theorem in the inaccessible full article has not been checked.
No priority claim follows from this bounded literature search.
