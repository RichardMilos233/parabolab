# R27: a nonconstant equilibrium can amplify faster than the homogeneous saddle

Date: 2026-09-29. Root conventional counterexample candidate, pending
independent review. No Lean, numerical eigensolve, symbolic computation,
unknown-input acquisition or sampler execution has occurred.

## 1. Question and exact proposed obstruction

The odd-power proof uses f'(u)<=f'(0) on the invariant interval. An
extension to an arbitrary inward polynomial cannot replace that fact
by a claim that the homogeneous unstable equilibrium always gives the
largest long-time amplification. The following explicit local branch
proposes a counterexample to that claim.

Fix b=1/10, a=1-b=9/10, and the polynomial

    f(u)=u(1-u)(u+b)=b u+a u^2-u^3.                      (1.1)

It is inward on [-1,1]: f(-1)=2(1-b)>0 and f(1)=0. Its equilibria
are -b,0,1, with f'(0)=b>0 and f'(-b),f'(1)<0. On the unit torus,
consider u_t=(kappa/2)u_xx+f(u). There exist fixed kappa>0 and smooth
nonconstant sign-changing equilibria u_* of arbitrarily small norm,
whose largest linearized eigenvalue lambda_* satisfies

    lambda_*>b=f'(0).                                   (1.2)

For every fixed finite s>=1, such an equilibrium can be chosen strictly
inside all the amplitude and derivative bounds of the same signed class
V from D45. Choose one small branch parameter once, thereby fixing both
u_* and kappa before varying the prediction horizon T.

Consequently there is no fixed C such that the actual nonlinear flow
obeys, for all v,w in this V and every T>=0,

    ||S_Tv-S_Tw||inf<=C exp(f'(0)T)||v-w||inf.             (1.3)

This is a flow-sensitivity counterexample. It is NOT a new query lower
bound, nor a proof that the optimal query exponent equals lambda_*.

## 2. A genuine branch from an explicit invertible implicit equation

Use theta=2pi x and omega=2pi^2 kappa. The stationary equation is

    omega u''+b u+a u^2-u^3=0,                          (2.1)

where prime denotes theta differentiation on the 2pi-periodic circle.
Normalize the cosine coefficient so that the coefficient of cos(theta)
in u is exactly epsilon. Work with even functions to fix the phase.

Choose any integer m>=max(1,s+1). Let X be the closed subspace of
even H^(m+2) functions with zero cos(theta) coefficient, and Y the
even H^m space. Set u=epsilon(cos(theta)+w), w in X. After dividing
the polynomial equation by epsilon, define also at epsilon=0 the map

    F(epsilon,w,omega)
       =omega[-cos(theta)+w'']+b[cos(theta)+w]
          +a epsilon[cos(theta)+w]^2
          -epsilon^2[cos(theta)+w]^3.                   (2.2)

This is real analytic from a neighborhood in R x X x R into Y,
because one-dimensional H^m with m>=1 is a Banach algebra and the
derivative term is bounded from H^(m+2) to H^m. At(0,0,b), F=0.
The derivative in(w,omega) maps(h,t) to

    b(h''+h)-t cos(theta).                              (2.3)

It is an isomorphism X x R -> Y. Given y, take t to be minus its
cos(theta) coefficient, and divide every other cosine coefficient
by b(1-n^2). These denominators are nonzero for n!=1 and have quadratic
growth, giving the bounded inverse from H^m to H^(m+2).

The ordinary analytic implicit function theorem therefore supplies
actual analytic w(epsilon),omega(epsilon) near zero with w(0)=0 and
omega(0)=b. This establishes existence, rather than treating a formal
power series as an exact stationary solution. Elliptic bootstrapping
in(2.1) makes each profile smooth. Taking m as above also gives the
needed convergence in every prescribed finite C^s norm.

## 3. Stationary branch coefficients

Write

    u_epsilon=epsilon cos(theta)+epsilon^2 v(theta)+O(epsilon^3),
    omega_epsilon=b+omega_1 epsilon+omega_2 epsilon^2+O(epsilon^3).

The remainder statements hold in the chosen Sobolev spaces, hence in
the required finite continuous-derivative norms. The cos(theta)
coefficient of v and every higher profile correction is zero.

The order-epsilon^2 equation is

    b(v''+v)-omega_1 cos(theta)+a cos(theta)^2=0.

Projection onto cos(theta) gives omega_1=0. Since
cos(theta)^2=(1+cos(2theta))/2,

    v(theta)=-a/(2b)+a/(6b) cos(2theta).                 (3.1)

At order epsilon^3 the first cosine coefficient of the stationary
equation gives

    -omega_2+2a[-a/(2b)+a/(12b)]-3/4=0,
    omega_2=-5a^2/(6b)-3/4.                             (3.2)

For b=1/10,a=9/10 these formulas are

    u_epsilon=epsilon cos(theta)
                  +epsilon^2[-9/2+(3/2)cos(2theta)]+O(epsilon^3),
    omega_epsilon=1/10-(15/2)epsilon^2+O(epsilon^3).      (3.3)

Thus omega_epsilon and kappa_epsilon=omega_epsilon/(2pi^2) remain
positive for every sufficiently small epsilon. Also u_epsilon takes
both signs and tends to zero in C^s. For a chosen small positive
epsilon it therefore satisfies ||u_*||inf<1/2 and all derivatives
through order s have sup norm strictly less than one. The min/max
sign inequalities are strict, so u_* has a C^s neighborhood inside V.

## 4. Actual positive principal eigenfunction

The linearized operator in theta coordinates is

    L_epsilon=omega_epsilon partial_theta^2
                      +b+2a u_epsilon-3u_epsilon^2.     (4.1)

Normalize an eigenfunction as phi_epsilon=1+eta_epsilon with
mean eta_epsilon=0. Its eigenvalue equation, with lambda=b+l, is

    G(epsilon,eta,l)
       =L_epsilon(1+eta)-(b+l)(1+eta)=0.                 (4.2)

Use even H^(m+2) functions of mean zero for eta and even H^m for the
output. At(0,0,0), the derivative in(eta,l) is b eta''-l. It is an
isomorphism: take l=-mean(y), and divide each nonzero cosine coefficient
of y by -b n^2. The analytic implicit function theorem again gives
an actual analytic eigenpair. Uniform convergence phi_epsilon->1
makes phi_epsilon strictly positive for sufficiently small epsilon.

This eigenvalue is the largest on the full periodic real space, not
merely on the even subspace. For any smooth periodic h, write h=phi g.
The eigenfunction equation and integration by parts give

    integral h L_epsilon h
        =lambda_epsilon integral h^2
                     -omega_epsilon integral phi^2 (g')^2.   (4.3)

The inequality extends by density to the form domain H^1. Since
omega_epsilon>0 and equality is attained at h=phi, the Rayleigh
supremum is exactly lambda_epsilon. The periodic elliptic self-adjoint
operator has compact resolvent. Thus the constructed eigenvalue is
indeed its principal eigenvalue, including non-even perturbations.

## 5. The principal growth rate is strictly larger than b

Write phi=1+epsilon phi_1+epsilon^2 phi_2+O(epsilon^3) and
lambda=b+lambda_1 epsilon+lambda_2 epsilon^2+O(epsilon^3), with all
phi_i of mean zero. Use normalized circle averages, so mean cos^2=1/2.
At first order the eigenvalue equation gives

    b phi_1''+2a cos(theta)=lambda_1,
    lambda_1=0, phi_1=(2a/b)cos(theta).                  (5.1)

At second order its spatial mean gives

    lambda_2=mean[2a v-3cos^2(theta)+2a cos(theta)phi_1]
             =-a^2/b-3/2+2a^2/b
             =a^2/b-3/2.                              (5.2)

The diffusion correction omega_2 differentiates the leading constant
eigenfunction, so it contributes zero at this order; omega_1=0 as
already proved. No missing diffusion term changes(5.2).

Whenever a^2>(3/2)b, the quadratic coefficient is positive, and the
analytic remainder proves lambda_epsilon>b for all sufficiently small
nonzero epsilon. For the fixed example,

    lambda_epsilon=1/10+(33/5)epsilon^2+O(epsilon^3).     (5.3)

Equations(2.2) and(4.2), not a numerical eigenvalue fit, establish the
existence and controlled remainder behind this strict inequality.
No explicit admissible numerical epsilon is claimed without a
quantitative remainder bound or later validated computation.

## 6. Consequence for the actual solution map

Fix one admissible epsilon and hence fixed u_*,kappa,phi,lambda_*.
The bounded scalar reaction-diffusion flow is Frechet differentiable
near u_* over every finite time interval, by differentiating its
polynomial mild equation. Since u_* is stationary, its first variation
is generated by the time-independent operator L_*, so

    D S_T(u_*)[phi]=exp(lambda_* T)phi.                   (6.1)

For all sufficiently small real h, u_*+h phi remains in V: every
amplitude and finite-derivative constraint has slack, and both signs
persist. If(1.3) held, apply it to v=u_*+h phi and w=u_*, divide by
|h|, and let h tend to zero for each fixed T. Equation(6.1) would give

    exp(lambda_* T)||phi||inf
           <=C exp(bT)||phi||inf.

As phi is nonzero and lambda_*>b, this fails for sufficiently large T.
The same argument rules out any uniform exponential sensitivity bound
with rate strictly less than lambda_*. It is not an assertion that
finite perturbations grow exponentially forever: differentiation is
taken at each fixed horizon before increasing that horizon.

## 7. Implication for the next generalization, and limits

For u-u^(2p+1), the pointwise inequality f'<=1 makes the rate-one
comparison available everywhere. The asymmetric example has
f'(u)=b+2a u-3u^2, whose maximum is b+a^2/3>b. Its nonconstant
equilibrium supplies an actual persistent rate above b, rather than
merely a transient pointwise derivative maximum.

A general signed-class long-time theory must therefore examine
nonconstant stationary states and their linearized growth, or use
another valid global sensitivity argument. Importing only f'(0)
from the homogeneous saddle is insufficient. The fixed-time inward-
polynomial sampler D43 remains valid; nothing here contradicts it
or the accepted normalized odd-power complexity theorems.

It remains open in this note whether lambda_* yields a sharper
query lower bound, how to build a full-slice prior near u_*, whether
the resulting trajectories have fixed target separation, and what
upper rate is sharp across the full class. Spectral sensitivity alone
does not answer any of those information questions. There is no
claim that this classical bifurcation phenomenon is new.

## 8. Bounded primary-source attribution and pending checks

The searches were exactly:

1. `Crandall Rabinowitz bifurcation from simple eigenvalues 1971 pdf`
2. `asymmetric bistable reaction diffusion periodic stationary solutions principal eigenvalue unstable equilibrium bifurcation`

The publisher's [Crandall–Rabinowitz1971 record](https://www.sciencedirect.com/science/article/pii/0022123671900152)
was inspected at abstract/metadata through the search result. It
identifies the classical simple-eigenvalue bifurcation framework.
No complete proof from that paper, the later1973 spectral paper,
or a secondary search result was read or imported. Here the two
explicit isomorphisms permit direct use of the standard analytic
implicit function theorem; every example-specific coefficient and
the principal-eigenvalue identification are derived above.

Independent review should especially check the Sobolev isomorphisms,
cosine normalization, stationary and eigenvalue expansions, fixed-
diffusivity quantifier, positivity/ground-state identity, class slack,
and the order of differentiation and long-time limits. A later formal
contract and fixed numerical protocol would be separate. Frozen E4/E5
and all accepted artifacts are unchanged.
