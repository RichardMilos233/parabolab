# R07: local stable graph as a possible all-dimension query upper route

Status: new root research candidate. The main all-order product-measure
lemma in Section3 is NOT proved here. This file is neither an accepted
theorem nor a Lean/numerical contract. It preserves D27 and frozen T56.
Its purpose is to attack the actual upper-bound dimension obstruction,
rather than merely repeat the C3 calculation in a few more dimensions.

## 1. Motivation and the precise missing bridge

D27 approximates the global asymptotic phase A by a quadratic Taylor
polynomial. The residual cubic remainder is O(k^(-3s)), while the desired
sampling rate is k^(-s-d/2). This gives d<=4s. Differentiating the present
global phase proof to order J would require3J+2<2nu. Even if all its
measure details extend, nu=2*pi^2-1 gives only a finite J range.

A different coordinate may avoid this limitation at fixed absolute
accuracy. Near the local stable manifold of zero, estimate the signed
distance in the constant direction to that manifold. If the manifold
graph has derivatives of every required finite order, with ACTUAL
bounded-TV product measures, then high-order residual sampling could
reach the classical integration rate for every fixed d,s. We need not
assert that the global asymptotic phase itself is analytic or C-infinity.

Generic invariant-manifold language does not discharge this obligation.
The primary [stable-manifold computation paper](https://arxiv.org/abs/2004.14830)
uses Lyapunov--Perron constructions for parabolic stable manifolds; the
abstract was inspected here as methodological background. The primary
[inertial-manifold smoothness paper](https://arxiv.org/abs/2102.03473)
explicitly discusses limited generic smoothness and separate extensions.
Neither abstract supplies the product-measure/query theorem needed here.
Their full proofs have not been used to assert this candidate.

## 2. A concrete local Lyapunov--Perron construction

Work on the same normalized unit torus. Pi is spatial averaging, Q=I-Pi,
and nu=2*pi^2-1. There is a finite public M>=1 such that

    ||exp(t)P_t Q||_(C->C) <=M exp(-nu*t), t>=0.

For example the Fourier heat bound and ||Q||<=2 give a sufficiently loose
M=2*rho*exp(2*pi^2), rho=((1+exp(-2*pi^2))/(1-exp(-2*pi^2)))^d.
The same estimate must hold for the signed convolution kernel's total
variation; for this explicit heat kernel it follows from its absolute
integral, rather than from an arbitrary operator representation.

Choose sigma in(0,nu), for example sigma=1. On trajectories with norm
||u||_sigma=sup_(t>=0) exp(sigma*t)||u(t)||infinity, prescribe mean-zero
w0 and solve the integral fixed-point equation

    u(t)=exp(t)P_t w0
         -integral_0^t exp(t-r)P_(t-r)Q(u(r)^3)dr
         +integral_t^infinity exp(t-r)Pi(u(r)^3)dr.      (2.1)

The sign in the last integral is positive: a decaying mean solves
b'=b-Pi(u^3) with the unstable homogeneous component removed. Set
Theta(w0)=Pi u(0). Then u is a stable trajectory from Theta(w0)+w0,
and A(Theta(w0)+w0)=0.

Put C=M/(nu-sigma)+1/(1+sigma). On the radius-R trajectory ball the
nonlinear term has norm at most C R^3 and Lipschitz constant3C R^2.
Choose R so C R^2<=1/8 and ||w0||<=R/(2M). The map preserves the
ball and is a strict contraction. Polynomial analyticity over the complex
Banach algebra of trajectories suggests analytic dependence on w0 on a
smaller ball, uniformly to every fixed finite derivative order.

This ordinary Banach-space analytic dependence is not yet the needed
measure lemma. It is, however, a direct local stable-manifold construction
with no high-order spectral bunching involving J. All differentiated
trajectories decay in the SAME weighted trajectory space. Products only
improve their time decay; no exp(Jt) unstable variations arise here.

Let r=R/(4M), shrink R further as necessary so
R^3/(1+3sigma)<=r/8, r<1/8 and K3*r^2/2<=1/64, where K3 is the
accepted uniform ordinary third-derivative bound for A on the7/8 ball.
Then Theta is available on mean-zero ||w0||<2r, and its stable value
has |Theta(w0)|<=r/8 there. All constants can depend on fixed d.

## 3. Outstanding all-order kernel lemma

Required statement: for every fixed finite J and ||w0||<=r, the first
J derivatives of Theta(Qz), viewed as a scalar functional of z in C(X),
are represented by signed measures on X^j with uniformly finite TV
bounds L_j. The domain needs a small margin for finite differences.

A proposed proof is to carry the Picard/differentiated fixed-point
construction out with actual measure-valued kernels. The linear initial
term exp(t)P_t Q has an explicit signed kernel and the exponential TV
bound from Section2. The forward and backward integral operators in
(2.1) also have explicit signed kernels. Polynomial products use
disjoint derivative labels and hence tensor-product measures. A
derivative of the fixed point solves the same linear feedback equation
with norm bounded by3C R^2<1; its Neumann inverse is a convergent sum
of such kernels. Induction in j adds only products of already constructed
lower-order kernels, with bounded time integrals in the weighted norm.

To make this a proof, check the appropriate kernel Banach space, total
variation before each spatial supremum, completeness, tensor products,
time measurability, the convergence of all measure series, and equality
with the actual Frechet derivatives. This is the central research gate.
An analytic scalar functional with bounded operator derivatives is NOT
automatically represented by a finite measure on a product space.

An alternative route may establish a sufficient finite-partition l1
coefficient bound directly, but it must be uniform over partitions and
must actually be proved. Do not replace the obligation by an oracle.

## 4. Why the local graph can substitute for the phase

Let z be a scalar, w mean-zero, and assume both z+w and Theta(w)+w
and their joining segment have sup norm<=r. Write H=z-Theta(w).
Accepted C3 regularity, DA(0)=Pi and D2A(0)=0 imply

    |DA(v)[1]-1|<=K3 ||v||infinity^2/2<=1/64.

The fundamental theorem along the constant-direction segment gives

    |A(z+w)-H|<=|H|/64.                             (4.1)

Thus H and A have the same sign (or both vanish), and for every a>=0

    |Psi(a A(z+w))-Psi(a H)|<=1/64.                 (4.2)

Use the accepted anchored Psi inequality on two nonnegative arguments,
or use oddness when both are nonpositive. This fixed output error is
uniform in a, including arbitrarily close to H=0. No derivative of A
beyond order3 is needed in this proxy comparison.

For a fixed burn-in L define the local proxy on suitable initial inputs q:

    H_L(q)=Pi S_Lq-Theta(Q S_Lq).

The phase has the exact semigroup identity A(S_Lq)=exp(L)A(q).
Consequently Psi(exp(T-L)H_L(v)) approximates the phase profile within
1/64 whenever S_Lv lies in the stated local domain.

The first J derivatives of the finite-time map S_L have actual heat-tree
kernels of finite TV for each fixed J,L. Conditional on Section3, finite
composition should give the same product-measure property for H_L, with
uniform constants on the local domain. This composition also needs to
be written down, not merely inferred from C-infinity regularity.

## 5. Paid coarse-data branch selection

Choose a FIXED L so the accepted spatial estimate on the7/8 ball gives
||Q S_Lq||infinity<=r/16 for all such q. It may be a very large constant,
but must not depend on T. Form the usual paid k^d-point interpolant g
with ||v-g||<=delta=Cint k^-s, ||g||<=3/4. Require

    exp(L)*delta<=r/32.

Compute the mean of S_Lg, a KNOWN-profile problem, with deterministic
absolute error<=r/32 by a public finite mesh. Denote it b_tilde.

- If |b_tilde|>r/2, then the actual mean of S_Lv has that sign and
  magnitude>7r/16. Its spatial deviation is<=r/16, so all S_Lv have
  that sign and magnitude>3r/8. Return sign(b_tilde). For sufficiently
  large T, ordinary scalar comparison bounds its target error by1/16.
- If |b_tilde|<=r/2, then every profile on the segment from g to v has
  |Pi S_Lq|<=9r/16 and spatial deviation<=r/16. Its sup norm is at
  most5r/8, safely inside the local ball. The local proxy and Taylor
  expansion apply throughout that segment.

Thus there is a buffer for the deterministic branch-selection error;
we never decide from an exact unknown PDE mean. The coarse transcript
determines the branch. Sufficiently small public finite-difference
perturbations of g preserve the same local margin by finite-time
Lipschitz stability. This selection works for all promised initial data,
including inputs exactly on or arbitrarily close to the stable manifold.

## 6. Conditional all-dimension sample/query balance

Fix d,s. Choose a finite integer J>=2 with Js>=s+d/2, for example
J=ceil(1+d/(2s)). Conditional on the kernel lemma, expand H_L(v)
about g through order J-1. Each order-j residual term is approximated
by a finite point-tuple weighted sum using a positive partition. Sample
M=k^d tuples from its normalized absolute coefficients. Each tuple
uses j paid values of v, counting repeats. Taylor factorials are retained.

With delta=Cint k^-s and bounded derivative measures, the stochastic
RMS terms have order delta^j/sqrt(M); the deterministic remainder has
order delta^J. Hence total proxy RMS is bounded by a fixed multiple of

    k^(-s-d/2)+k^(-Js),

plus allocated finite coefficient errors. Choose k a fixed multiple of
exp(T/(s+d/2)); the constants can absorb the fixed exp(L). The scaled
sampling RMS can be at most1/16. The deterministic query cap is

    [1+sum_(j=1)^(J-1) j] k^d
      =[1+J(J-1)/2] k^d=O(exp(2dT/(2s+d))).

The local proxy error1/64, actual PDE phase-remainder bound (say1/32)
and sampling1/16 total7/64<1/4. The far-phase branch has its separate
1/16 deterministic error. These are proposed budget allocations, not
an executed or formalized algorithm.

Finite differences of orders<=J-1 need the Jth derivative bound. Their
multinomial errors and rational coefficient l1 approximations must be
quantified. Partitions can be chosen from the public residual Lipschitz
bound. As in T56, auxiliary coefficient computation can be enormous;
the theorem would count only unknown initial values, not runtime.

## 7. Finite evaluation of the graph must not be an extra oracle

For an explicitly known local mean-zero w, Theta(w) can potentially be
computed by finding the zero of c -> A(c+w). The stable construction
provides a root, and Section4 gives derivative in[63/64,65/64] in the
local interval, so bisection with certified scalar evaluation errors
and interval widths can approximate the root to any fixed precision.
T56 already supplies finite evaluation of A on known smooth profiles.

The actual input to Theta in H_L(q) is w=Q S_Lq. Approximate this known
PDE profile in sup norm, remove its computed mean consistently, and use
a public local Lipschitz bound for Theta to control that error. A finite
known interpolant may then be used in the phase evaluations. All mesh,
root and rounding errors must be allocated explicitly. Only q built
from previously paid coarse values and public perturbations is used.
No evaluation of the unknown v is permitted in this auxiliary stage.

This is a possible constructive route, not a finished implementation
bridge. Direct computable Picard iteration is another option. Measurable
selection, margin handling, finite coefficients and almost-sure discrete
sampling must all match the existing exact-query model.

## Decision gate

First prove or refute the all-order ACTUAL kernel lemma and its finite-time
composition. If it fails, report the exact obstruction. If it passes,
complete the local/far branch and finite-query accounting before requesting
independent review. Do not silently weaken the target to a phase oracle,
known formula, bounded-away-from-interface subclass or a few dimensions.
No new accepted claim, Lean target or numerical experiment follows from
this draft. Its potential contribution remains subject to both proof and
primary-literature scrutiny.
