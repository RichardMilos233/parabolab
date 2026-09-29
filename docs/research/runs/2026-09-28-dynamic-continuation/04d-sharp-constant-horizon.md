# Exact absolute-moment horizon for constant profiles

Status: conventional proof by root, independently passed in T13 Section 7;
its Id-only wording correction is incorporated below. This is a separate
sharpening of D10, not a claim of publication priority. No end-to-end
formalization is claimed here.

## Fixed object

Keep the fully expanded original single-tree representation and the exact
support/likelihood/completion contract in `04c-general-obstruction.md`. Let
the terminal profile be the constant r and f be smooth near r. Set

    a_k = |f^(k)(r)|,     Phi(z) = sum_(k>=0) a_k z^k/k!.

Let R in [0,infinity] be the nonnegative radius of convergence of this
nonnegative power series. Values at its boundary are extended limits. The
terminal spatial derivative codes are zero; every finite tree rooted at a
spatial derivative code has a zero leaf of that type. Therefore every
gradient tuple contributes zero. This is a statement about finite-tree
weights, and does not require multiplying infinity by zero in moment PDEs.

If a_0=0, every finite F_0 tree has either a zero F_0 leaf or a zero spatial
derivative subtree. Thus the canonical Id absolute moment is |r| at every
finite horizon, irrespective of the growth of the other jets. This case must
be excluded before dividing by Phi.

Suppose a_0>0. Define

    tau = integral_[0,R) dz/Phi(z).

For R=0 the integral is zero. If R=infinity and Phi has degree at most one,
tau=infinity. Otherwise tau is finite: any positive coefficient of degree
p>=2 gives an integrable reciprocal upper bound at infinity; for finite R,
1/Phi<=1/a_0.

The exact extended canonical first absolute moment is

    W_Id(t) = |r| + Z(t),                    0<=t<tau,
    integral_0^Z(t) dz/Phi(z) = t;
    W_Id(tau) = |r| + R,                     tau<infinity;
    W_Id(t) = infinity,                      t>tau.

Here |r|+R is infinity if R=infinity. In particular, a finite radius may
produce a finite Id absolute moment at the critical time itself even though
some reaction-code moments are already infinite. Do not replace t>tau by
t>=tau without this distinction. If R=0, the boundary statement is simply
W_Id(0)=|r|, and every positive time fails.

These statements concern the random functional. For arbitrary smooth f its
formal terminal jet need not determine the actual nonlinear ODE flow.

## Proof using finite systems only

For n>=0, retain the terminal jet a_k only for k<=n, setting higher terminal
code values to zero. This is a nonnegative truncation of canonical tree
weights, not a changed sampling approximation promoted to the original
estimator. The weights increase with n and exhaust every finite tree.

The resulting finite hierarchy has

    V_k'=V_0 V_(k+1), k<n;  V_n'=0;  V_k(0)=a_k.

Let Phi_n(z)=sum_(k=0)^n a_k z^k/k!. Its minimal finite solution is

    Z_n'=Phi_n(Z_n), Z_n(0)=0,
    V_k=Phi_n^(k)(Z_n),  W_Id,n=|r|+Z_n.

The identities follow by differentiation; finite-dimensional local uniqueness
and nonnegative Picard iteration identify them with the finite-tree sum up
to the explosion time. At and after a finite explosion time the Id tree
sum is infinite, by monotonicity in the horizon and divergence on approach.
The highest retained reaction field V_n=a_n need not diverge.

Once n contains a positive coefficient of degree at least two,

    tau_n=integral_0^infinity dz/Phi_n(z) < infinity.

The polynomials increase pointwise. For z<R they converge to Phi(z); for
z>R they increase to infinity. Domination by the reciprocal of one fixed
superlinear Phi_n gives tau_n decreasing to tau. This argument also covers
R=0. If no such coefficient exists, the affine case is explicit and global.

Tonelli over complete finite trees gives W_Id=lim_n W_Id,n. For t<tau,
monotone convergence on any compact subinterval of [0,R) identifies
lim_n Z_n(t) with the inverse of z -> integral_0^z 1/Phi. For t>tau, some
tau_n<t, and that finite subsystem already has infinite Id mass.

For the remaining endpoint, group complete constant-profile trees by the
number of internal vertices. After likelihood cancellation, a fixed tree's
time-simplex integral is a nonnegative constant times t raised to that
integer. Brownian integrals equal one; zero-gradient trees were removed
termwise. Hence W_Id(t)-|r| is a power series in t with nonnegative
coefficients, interpreted in [0,infinity]. Monotone convergence as
t increases to tau proves its value at tau is the left limit, namely R.
This closes the endpoint without assuming uniqueness of an infinite ODE
system or finiteness of all reaction-code moments there.

## Examples that distinguish the cases

1. f(y)=sin(y), r=pi/2: Phi(z)=cosh(z), R=infinity,
   tau=pi/2, Z=log(sec(t)+tan(t)). Thus W_Id diverges at pi/2 while the
   signed solution 2 arctan(exp(t)) exists for all positive time.
2. f(y)=1/(1+y^2), r=0: Phi(z)=1/(1-z^2), R=1,
   tau=integral_0^1 (1-z^2)dz=2/3. Thus W_Id(2/3)=1 is finite,
   but W_Id(t)=infinity for every t>2/3. The signed solution satisfies
   u+u^3/3=t and is global. This prevents an erroneous universal closed
   critical-time divergence statement.
3. f(y)=1+exp(-1/y^2), smoothly extended at zero, r=0:
   Phi=1, tau=infinity, W_Id=t. The actual solution is strictly above t
   at positive times. Tree integrability alone does not prove correspondence.

## Relation to existing work and next verification

The scalar derivative code chain and its relation to Butcher series are
already present in Penent–Privault, [Numerical evaluation of ODE solutions
by Monte Carlo enumeration of Butcher series](https://arxiv.org/pdf/2201.05998),
Sections 2, 4 and 6. That paper provides sufficient integrability conditions
and discusses patching across adjacent intervals. The exact signed-tree
majorant horizon and boundary classification above are derived here; a
bounded search has not established whether they are already stated elsewhere.
No novelty claim follows from failing to find a keyword match.

Independent mathematical review passed in T13. The checked Riccati Lean
module verifies only a finite ODE barrier. A suitable further gate would
verify a finite polynomial chain
reduction or the explicit rational-reaction critical integral; the infinite
tree/series bridge would remain a conventional proof unless separately
formalized. Numerical plots of the examples could illustrate the distinction,
but cannot establish divergence or the general classification.
