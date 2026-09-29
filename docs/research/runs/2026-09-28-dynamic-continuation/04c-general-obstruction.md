# General absolute-integrability obstruction

Conventional theory completed and independently reviewed in
`reviews/T10-polynomial-obstruction.md` and
`reviews/T13-general-obstruction-audit.md`. The separate finite analytic
Lean gate passed, with its restricted coverage in `06b-absolute-lean.md`.
No numerical experiment proves the general theorem, and publication priority
remains unconfirmed.

## The representation and the result

Consider the original derivative-coded semilinear mechanism on a connected
flat torus in any fixed finite spatial dimension. The reaction is a scalar
function f(u), not an arbitrary function of spatial jets. Keep the original
fully expanded single-tree functional with exact likelihood weights, genuine
almost-everywhere support of nonzero terms, and almost-sure tree completion.
Clock and tuple proposals may depend on revealed history. Different signed
trees are not regrouped or cancelled inside one sample.

Precisely, if mu is the canonical measure on completed finite labelled trees,
a(theta) is their signed coefficient/terminal product and Q is the proposal,
the required joint likelihood contract is |H| dQ=|a| dmu. All conditional
clock/tuple and leaf-survival factors must appear; marginal reciprocals do
not suffice for adaptive sampling. A finite-depth restriction means
H times the indicator that the completed tree has depth at most N, not
artificial terminal substitution at a cutoff. Restarting positive moment
equations splits a nonnegative Volterra integral using Tonelli and the
semigroup identity; it never subtracts possibly infinite quantities.

Let v be smooth and periodic. If some integer p>=2 has both f(v) and
f^(p)(v) not identically zero, choose any t0>0 and define

    eta0=min_x P_t0 |f(v)|(x)>0,
    etap=min_x P_t0 |f^(p)(v)|(x)>0.

The minima are positive by compactness and heat-kernel positivity. The
nonnegative canonical expansion contains the coefficient-one chain
F_k -> (F_0,F_(k+1)). After restarting at t0, discarding other nonnegative
terms, and retaining the constant lower bound etap at code F_p, the scalar
comparison is

    A_k'=A_0 A_(k+1), 0<=k<p,  A_p=etap,
    A_0(0)=eta0, A_k(0)=0 for 1<=k<p.

Writing Z'=A_0, Z(0)=0 gives

    A_0=eta0+(etap/p!)Z^p.

The separation integral is finite, and splitting it at
(eta0*p!/etap)^(1/p) gives the explicit sufficient threshold

    T >= t0 + [p/(p-1)] eta0^(-(p-1)/p) (p!/etap)^(1/p).

At every such T and every starting point, E|H_Id(T,x)|=infinity for every
supported completing importance proposal on this expansion. The Id root
itself diverges because its positive mild integral dominates integral A_0=Z.
The comparison uses finite positive Picard iterates and Tonelli; it does not
differentiate an infinite moment or assume uniqueness of an infinite system.

In fact the full smooth terminal-jet classification is

    E|H_Id(T,x)| finite for every finite T and every x
      iff f(v) is identically zero, or
          f^(p)(v) is identically zero for every p>=2.

Necessity is the obstruction above. For sufficiency when all higher jets
vanish, every finite F_k tree with k>=2 has a path of successively higher
derivative labels reaching a zero leaf. Thus these code weights vanish
termwise. Connectedness makes f'(v)=b constant, giving the affine formula
below. If f(v)=0, a nonconstant v ranges over an interval on which every
reaction jet vanishes; for a constant root every F_0 tree instead has an
F_0-zero leaf or a spatial-derivative-zero subtree. This proves sufficiency
without an infinite-system uniqueness assumption.

For nonconstant v the smooth condition is equivalent to f being affine on
the image interval v(X). For v=r constant it is equivalent to f(r)=0 or an
affine formal Taylor jet at r. Such a jet does not determine a smooth f
away from r. T13 gives the full finite-tree proof and edge cases.

For real-analytic f on a connected open interval containing the range of v,
this further yields the global reaction classification:

    E|H_Id(T,x)| is finite for every finite T and every x
      iff f is affine on that interval, or v is a constant reaction root.

For nonconstant v and non-affine analytic f, p=2 suffices by the analytic
identity theorem. For constant non-root v, some finite higher derivative
is nonzero. Affine f(y)=a+by has the explicit finite canonical moment

    W_Id(t)=P_t|v|+L_b(t) P_t|a+bv|,
    L_b(t)=(exp(|b|t)-1)/|b|, or t when b=0.

The classification concerns finiteness at all finite horizons. It does not
assert a sharp critical time or even a positive initial interval of
integrability for an arbitrary infinite derivative family. It also does not
assert global PDE existence. Compactness, connectedness, analyticity in the
classification, and the actual specified code mechanism are material.

## Exceptions and comparisons

For merely smooth non-affine f, the analytic conclusion can fail: f(y)=
1+exp(-1/y²), extended by f(0)=1, and v=0 has a flat higher terminal jet and
canonical W_Id(t)=t for all time. Its estimator does not represent the true
nonlinear ODE, which is consistent with the original theorem's separate
infinite-system uniqueness/correspondence assumption.

For f(y)=sin(y), v=pi/2, the canonical absolute system reduces exactly to
A'=AB, B'=A², A(0)=1, B(0)=0. Thus A=sec(t), B=tan(t), and the Id absolute
moment diverges at pi/2. The signed ODE solution 2 arctan(exp(t)) exists
globally. This is an illustrative exact calculation, not a numerical
integrability test or novelty claim.

T10 also checks the raw binary recoding of Huang–Privault (2025): its
zero-spatial-index rule retains this same coefficient-one chain, so binary
recoding alone does not evade the obstruction under the corresponding
canonical proposal contract. A changed representation has to change the
relevant algebra, not merely its tree shape.

## Analytic lemma checked by the separate Lean gate

The following normalized Riccati barrier is proved here before translation.
Let T>=0 and let z be differentiable at every point of [0,T], with

    z(0)=0, z'(t)=1+z(t)^2 on [0,T].

Then T<pi/2. Indeed F(t)=arctan(z(t)) has derivative
(1+z(t)^2)/(1+z(t)^2)=1. It is continuous on the closed interval, so the
mean-value/constant-derivative theorem gives F(T)=T. The strict range bound
arctan(x)<pi/2 for every finite real x proves the claim. This proof includes
T=0 and requires no assumption that z is positive.

A scaled version avoids square-root identities in the formal statement:
if z(0)=0 and z'=a*(1+(b*z)^2) on [0,T], a,b>0, then

    a*b*T < pi/2.

Apply the same proof to arctan(b*z), whose derivative is a*b. The p=2
comparison z'=eta0+(eta2/2)z² takes a=eta0 and
b=sqrt(eta2/(2eta0)). The remaining parameter substitution, heat positivity,
tree likelihood cancellation, moment comparison and derivative-chain
reduction remain outside this finite analytic lemma unless explicitly
formalized later. This gate proves genuine finite-time ODE obstruction,
not just rational constant arithmetic, but is still not an end-to-end
formal verification of the probabilistic theorem.
