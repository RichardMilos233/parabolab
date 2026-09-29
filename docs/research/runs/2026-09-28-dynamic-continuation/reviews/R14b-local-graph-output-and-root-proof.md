# R14b: local graph output and finite-time root estimates

Date: 2026-09-29. Root-authored conventional proof candidate; independent
audit pending. This refines R14 Sections 2 and 4. It does not accept the
full spectral-gap extension, the weighted-L1 third derivative, or a new
query/work theorem. No code or formal certificate is supplied here.

## 1. Local assumptions

Let kappa>0 and let S_t be the actual classical flow on the normalized
unit torus of

    u_t=kappa Delta u/2+u-u^3.

Only comparison, uniqueness, preservation of the interval [-1,1], and
the following supplied stable trajectory are used in this note. Suppose
V solves this same PDE, starts at w+c_star with Pi w=0, and obeys

    ||V(t)||infinity <= R exp(-sigma t),
    R>0, sigma>0.

For a stable graph, c_star=Theta(w). We do not prove construction of
that graph here. Assume its backward mean identity

    Pi V(t)=integral_t^infinity exp(t-s) Pi(V(s)^3) ds.

Consequently, with B=R^3/(1+3sigma),

    |Pi V(t)| <= B exp(-3sigma t).                       (1)

This identity also follows by integrating the actual mean equation
backward and using the stated decay, so it need not be a separate
unproved phase hypothesis.

## 2. Comparison with a scalar logistic trajectory

Take an initial datum w+b in [-1,1] pointwise and put h=b-c_star.
Assume |h|<=h_max<1. If h=0, uniqueness gives u=V. If h is positive,
let y=u-V; if h is negative, let y=V-u. Order preservation gives y>=0.
In both cases |u|<=1 and |V|<=R exp(-sigma t), so

    0<=y<=1+R.

For positive h the exact difference equation is

    y_t=kappa Delta y/2+y-y^3-3Vy^2-3V^2y.

For negative h the quadratic term has the opposite sign. In either
case define

    epsilon(t)=3R(1+R) exp(-sigma t)+3R^2 exp(-2sigma t),
    E=integral_0^infinity epsilon(t) dt
      =3R(1+R)/sigma+3R^2/(2sigma).

The reaction of the actual y lies between
(1-epsilon(t))y-y^3 and (1+epsilon(t))y-y^3. Scalar parabolic
comparison therefore bounds y between z_minus and z_plus, where

    z_plus/minus'=(1 +/- epsilon(t))z_plus/minus-z_plus/minus^3,
    z_plus/minus(0)=|h|.

The comparison uses an inequality for the actual bounded y; it does
not assume an a priori bound on the comparison ODE in order to obtain
epsilon. Those scalar solutions are nonnegative and global, as also
seen directly from their formula below.

For any continuous integrable perturbation a(t), put
A(t)=t+integral_0^t a(s) ds. The positive solution of
z'=(1+a(t))z-z^3, z(0)=x, is

    z(t)=x exp(A(t)) /
         sqrt(1+2x^2 integral_0^t exp(2A(s)) ds).        (2)

For x=0 the same formula gives zero. Differentiating (2), or solving
the linear equation for z^(-2) when x>0, verifies it. Let

    phi_t(x)=x exp(t)/sqrt(1+x^2(exp(2t)-1)).

For a=+epsilon the denominator in (2) is at least the unperturbed
denominator, while its numerator is at most exp(E) times the
unperturbed numerator. For a=-epsilon the inequalities reverse in
the required directions. Thus, pointwise for every t>=0,

    exp(-E) phi_t(|h|) <= y(t,x) <= exp(E) phi_t(|h|).   (3)

Since |h|<1, phi_t(|h|)<=1. Taking account of the sign of h gives

    ||u(t)-phi_t(h)||infinity
        <= R exp(-sigma t)+(exp(E)-1).                 (4)

Here phi_t is extended as an odd function. This bound is uniform in
the distance |h| from the stable graph and includes arbitrarily small
nonzero h; the h=0 case follows directly from the supplied V bound.

To replace phi_t(h) by the desired sigmoid, put
Psi(z)=z/sqrt(1+z^2). For h>=0 and z=exp(t)h,

    phi_t(h)=z/sqrt(1+z^2-h^2),
    1 <= phi_t(h)/Psi(z) <= (1-h_max^2)^(-1/2)

when h>0. The zero case is handled without division; negative h uses
oddness. Therefore

    sup_(t>=0,x) |u(t,x)-Psi(exp(t)h)|
      <= R+exp(E)-1+(1-h_max^2)^(-1/2)-1.              (5)

If h_max is chosen proportional to R, the right side tends to zero
as R tends to zero for any fixed sigma>0. This proves the candidate
absolute local output estimate without differentiating G near +/-1.
R14's proposed threshold argument is unnecessary for this proof.

There is no claim that the right side stays bounded as sigma tends
to zero with R fixed, or that a globally smooth asymptotic phase has
been constructed.

## 3. A finite-time mean zero approximates the graph value

Assume additionally 0<r<=1, ||w||infinity<=r/8 and |c_star|<=r/8.
Every datum w+c with c in I=[-r/4,r/4] then lies in [-1,1]. Let

    D=2 exp(E) B,
    D<=min(1,r/16),
    f_tau(c)=Pi S_tau(w+c).

The smallness of D is an explicit condition to be secured by the
graph-radius choice; it is not automatic from decay alone. Define

    h_tau=D exp(-(1+3sigma)tau).

Both c_star +/- h_tau belong to I. By (3), for the positive shift,

    S_tau(w+c_star+h_tau)-V(tau)
      >=exp(-E) phi_tau(h_tau)
      >=exp(-E) D exp(-3sigma tau)/sqrt(1+D^2)
      >=sqrt(2) B exp(-3sigma tau).

Indeed h_tau^2(exp(2tau)-1)<=D^2. Together with (1) this makes
f_tau(c_star+h_tau)>0. The negative shift similarly makes
f_tau(c_star-h_tau)<0. These estimates hold also at tau=0.

For c2>c1 in I the positive difference between their actual flows
solves a linear equation with coefficient

    1-(u2^2+u2*u1+u1^2)>=-2,

because both flows remain in [-1,1]. Comparison with the constant
subsolution exp(-2t)(c2-c1) proves

    f_tau(c2)-f_tau(c1)>=exp(-2tau)(c2-c1).            (6)

The mean is continuous in c by finite-time continuous dependence.
The intermediate-value theorem and (6) therefore give a unique root
c_tau in I, satisfying

    |c_tau-c_star| <= D exp(-(1+3sigma)tau).           (7)

In particular |c_tau|<=3r/16, leaving a fixed spatial bracket buffer
of r/16 at each endpoint. The sharper root convergence in (7) was
obtained from (3) near the graph, not from the crude derivative (6).
Using only exp(-2tau) to estimate the root shift would lose the result
for small sigma, exactly as noted in R14.

## 4. A deterministic buffered evaluation rule

For 0<zeta<r, choose a public tau>=1 with

    D exp(-(1+3sigma)tau)<=zeta/2.

Then tau=O(1+log(1/zeta)) for fixed graph constants. Suppose each
evaluation fhat(c) has a deterministic absolute error at most

    epsilon_f=exp(-2tau) zeta/8.

Bisection starts from I. If fhat>epsilon_f, keep the lower half;
if fhat<-epsilon_f, keep the upper half. These branches retain c_tau.
If neither strict inequality holds, |f_tau(c)|<=2epsilon_f and (6)
imply |c-c_tau|<=zeta/4; return c. Otherwise stop after the public
number of halvings making the interval length at most zeta/2 and
return its midpoint. In either case,

    |returned_value-c_star|<=zeta/4+zeta/2<zeta.

There is no unbounded sign-refinement loop and no division by a
computed phase value. All PDE evaluations have fixed time tau and
fixed absolute tolerance. Their required logarithmic accuracy is
log(8/zeta)+2tau=O(1+log(1/zeta)). Thus at zeta proportional to
exp(-T), both time and logarithmic precision are O(1+T).

A separately proved known-profile solver is still required to turn
this rule into a work theorem. This note does not assign unit cost
to f_tau or import T70's pending audit as an accepted lemma.

## 5. Remaining correspondence and audit gates

An independent reviewer must check the actual PDE comparison, both
signs and h=0, every use of the invariant interval, formula (2), the
uniform scalar comparison (3), root/bracket constants and bisection.
No assumption about global phase smoothness is permitted in this audit.

To finish R14 one must still construct the graph and a uniform burn-in
for every fixed lambda1>1, choose compatible small radii and full
near/far error budgets, prove the weighted-L1 third derivative of the
new proxy, recheck the full signed lower prior and upper sampler, and
redo the shared arithmetic model for the changed diffusivity. The
critical/multiple-unstable-mode regimes remain outside the proposal.
