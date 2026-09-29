# R03: direct signed mass-only counterexample without derivative kernels

Status: root derivation submitted for independent review; not a new accepted
claim, Lean target, or numerical authorization. This strengthens the audit
structure of T56 by removing its Section4 derivative-measure theorem from
the mass-only counterexample's dependencies. Frozen T56 is unchanged.

## Precise question

On the unit torus with u_t=Delta u/2+u-u^3, can a method based only on the
exact initial mass uniformly approximate every fixed smooth sign-changing
C^s input with height<=1/2 and C^s,max norm<=1 at large T?

The answer supplied by the proof below is no, even though giving the mass
exactly is stronger information than estimating it from samples. There are
two fixed opposite smooth profiles of zero mean whose solutions converge
uniformly to opposite equilibria. Every mass-only rule has the same output
law on these two inputs, so its worst-case RMS tends to at least1. This is
not a lower bound against algorithms that use the spatial information in
individual point samples. It does not establish signed query optimality.

## 1. Actual nonlinear coordinate from scalar and energy estimates

Fix any a0 in(0,1), for example7/8. For continuous initial data with
||v||infinity<=a0, put b(t)=integral u(t), w(t)=u(t)-b(t), and
nu=2*pi^2-1. Comparison with the constant scalar solutions gives

    |u(t,x)|<=ell_a0(t),
    1-b(t)^2 >= (1-a0^2)exp(-2t).

The actual mean equation is

    b'=b-b^3-R,
    R=3b integral w^2+integral w^3.

Monotonicity of the cube and the unit-torus Poincare inequality give
||w(t)||2<=||v-integral v||2 exp(-nu*t). In particular for this ball,
|R(t)|<=5a0^2 exp(-2nu*t).

Let G(b)=b/sqrt(1-b^2), Psi=G^(-1), and A_t(v)=exp(-t)G(b(t)).
Direct differentiation, not a closed mean approximation, gives

    dA_t/dt=-exp(-t)G'(b(t))R(t).

Since G'(b)=(1-b^2)^(-3/2), the integrand is bounded by a constant times
exp(-(2nu-2)t). Therefore A(v)=lim A_t(v) exists, with a uniform tail
bound |A-A_t|<=C exp(-(2nu-2)t). The centered equation over one time
unit, using its bounded potential and the torus heat L2-to-Linfinity
bound, gives ||w(T)||infinity<=Cw exp(-nu*T) for T>=1. Consequently

    ||S_Tv-Psi(exp(T)A(v))||infinity
      <=Cw exp(-nu*T)+C exp(-(2nu-3)T).

All these estimates use comparison, the centered energy identity and
one-unit heat smoothing. They do not require differentiability of A as a
functional, a kernel on multiple input positions, or an inertial manifold.
In particular A(v)>0 or A(v)<0 implies uniform convergence to+1 or-1.

## 2. Small amplitude with an integrable cubic dominating bound

Take a fixed smooth mean-zero function phi. Set B=||phi||infinity and
D=||phi||2. Let v_epsilon=epsilon*phi, epsilon>0, restricted so that
||v_epsilon||infinity<=a0. Denote its solution by u_epsilon.

The linear upper comparison for absolute values gives

    |u_epsilon(t,x)|<=epsilon*B*exp(t),
    |b_epsilon(t)|<=epsilon*B*exp(t),
    ||w_epsilon(t)||infinity<=2epsilon*B*exp(t).

The centered energy estimate retains the small amplitude:

    ||w_epsilon(t)||2<=epsilon*D*exp(-nu*t).

Hence, for every t>=0, even after the solution has saturated,

    |R_epsilon(t)|
      <=5epsilon^3*B*D^2*exp((1-2nu)t).

This bound may overestimate the amplitude at late times, but it remains a
valid uniform inequality. Combining it with the a0 scalar gap yields

    |exp(-t)G'(b_epsilon(t))*R_epsilon(t)/epsilon^3|
      <=5 B D^2 (1-a0^2)^(-3/2) exp((3-2nu)t).

The right side is integrable because2nu>3. It is independent of epsilon.
Thus dominated convergence is available without exchanging an uncontrolled
Taylor expansion and an infinite time integral.

For each fixed finite t, Duhamel's formula and |u_epsilon|<=epsilon B exp(t)
give

    ||u_epsilon(t)-epsilon exp(t)P_t phi||infinity
      <=epsilon^3 B^3 exp(t)(exp(2t)-1)/2.

Therefore u_epsilon/epsilon converges uniformly to exp(t)P_t phi on each
bounded time interval. Its mean tends to zero after division by epsilon,
and w_epsilon/epsilon tends to the same linear solution. It follows that

    R_epsilon(t)/epsilon^3
      ->exp(3t) integral(P_t phi)^3,
    G'(b_epsilon(t))->1.

Since the initial mean is zero, A(v_epsilon) has no G(initial mean) term.
Dominated convergence now proves the exact cubic limit

    lim_(epsilon->0+) A(epsilon*phi)/epsilon^3
      =-integral_0^infinity exp(2t) integral(P_t phi)^3 dt.

This is a limit theorem, not an assumption about the sign of the initial
mean derivative and not a use of T56's third Frechet derivative.

## 3. Two modes with the same zero mass select opposite phases

Let c>0 be fixed and

    phi(x)=cos(2*pi*x_1)+c*cos(4*pi*x_1).

Then integral phi=0, and elementary Fourier orthogonality gives

    integral(P_t phi)^3=(3c/4)exp(-12*pi^2*t).

Indeed the only nonzero cubic cross average is
integral cos(2*pi*x_1)^2 cos(4*pi*x_1)=1/4. The heat semigroup multiplies
the two modes by exp(-2*pi^2*t) and exp(-8*pi^2*t), respectively.
Thus

    A(epsilon*phi)/epsilon^3
      ->-3c/[4(12*pi^2-2)]<0.

For every sufficiently small fixed positive epsilon, A(epsilon*phi)<0.
Oddness of the PDE and G gives A(-epsilon*phi)=-A(epsilon*phi)>0.
Both profiles are nonzero continuous functions of zero mean, and hence
genuinely change sign. Choosing epsilon still smaller if needed enforces
height<=1/2 and all derivative sup norms through the chosen finite order s
are at most1; explicitly it suffices to bound epsilon times the finite maximum
of (2*pi)^r+c*(4*pi)^r over integers0<=r<=s by1, together with the height
condition. The fixed integer s can be any positive order.

The resulting pair v_plus=epsilon*phi and v_minus=-epsilon*phi is fixed
once and for all, independent of T. Their targets satisfy

    S_T v_plus(x*) ->-1,
    S_T v_minus(x*) ->+1

uniformly in x*. This is stronger than merely showing a nonzero initial
mean derivative.

## 4. Consequence for any mass-only estimator

A mass-only algorithm may use the PDE, public class parameters, T and
independent randomness, but its entire unknown-data input is integral v.
The two profiles above give that input the same exact value zero. Its
output H_T therefore has the same law on both. For any real target pair
a_T,b_T and every output h,

    ((h-a_T)^2+(h-b_T)^2)/2 >= (a_T-b_T)^2/4.

Integrating proves that at least one input has MSE at least
(a_T-b_T)^2/4, also when one risk is infinite. Since a_T-b_T tends to-2,

    liminf_(T->infinity) max(RMS_plus(T),RMS_minus(T)) >=1.

In particular no mass-only rule can attain uniform RMS1/4 on the signed
class at all large horizons. The positive-class mass-profile result D24
cannot be extended by merely allowing the input mass to have either sign.
A genuine nonlinear coordinate or other spatial information is necessary.

## Audit boundary

The independent reviewer should check the retained epsilon-dependent
energy bound, the integrable exp((3-2nu)t) domination, the exact two-mode
Fourier coefficient and the same-output-law information step. This direct
argument does not settle the more difficult derivative-measure and finite
query upper-bound claims in T56. No Lean, code, numerical experiment or
priority assessment is supplied here.
