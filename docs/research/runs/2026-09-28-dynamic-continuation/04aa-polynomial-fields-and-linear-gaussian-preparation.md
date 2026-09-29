# D43–D44: polynomial derivative fields and linear Gaussian preparation

Date: 2026-09-29. Status: accepted **conventional fixed-time results** after
independent T91 and root correspondence. These extend the sampling component,
not the full long-horizon complexity theorem.

## Locked evidence and two explicit repairs

The proof sources are `reviews/R20-polynomial-reaction-field-sampler-candidate.md`
(`b1e42a195c67942066894d04a11c28d7ba2951a6d6730977070e424ac84542b9`),
the mandatory `reviews/R20b-continuous-domain-addendum.md`
(`6c5e8b158ca269588c4200ca09c82f4ffa430e8aa0146a52022370ade352e527`), and
`reviews/R21-linear-tree-common-gaussian-candidate.md`
(`99f8a23c98332b6797ee1ecc9f0929d94950cd047acb17bcbea0df9052ff7461`).
The independent 736-line T91 audit is
`reviews/T91-polynomial-field-linear-gaussian-independent-audit.md`
(`2f06d787fcbb631662b3be4997eb6c610e145120147a0e831d245345abde1af7`).
Root read the complete final audit and checked its ten lemmas against these
sources and the stated oracle model.

R20 alone is not the accepted statement: its domain did not explicitly say
continuous, and its closing sampling-risk sentence could be read as equality.
R20b requires continuous base and direction, and states the upper inequality.
The original is preserved so these repairs remain inspectable.

## D43: every fixed inward polynomial has an actual smooth derivative sampler

Let X be the normalized d-dimensional unit torus, d>=1, kappa>0, tau>0,
and f a fixed known real polynomial satisfying f(-1)>=0 and f(1)<=0.
Let S_t be the actual flow of

    u_t=(kappa/2) Delta u+f(u).

Fix known g in C(X), ||g||inf<1, with a paid evaluator costing G per value,
and unknown v in C(X), e=v-g. The derivative statement needs no bound on
||v||inf; a Taylor statement separately requires g+t e in the open unit
ball for every t in [0,1]. Only exact scalar point values of v supply new
unknown information. Repeated evaluations are charged.

For each fixed integer j>=1 there is an actual strongly measurable,
Bochner-integrable H^r-valued random field W_j, r=d+1, such that

    E W_j=D^j S_tau(g)[e,...,e],
    E||W_j||_(H^r)^2 <= V_j ||e||inf^(2j),

with at most j unknown-value acquisitions on every seed. The map S_tau
from the open unit ball of C(X) to H^r is genuinely C-infinity Frechet
differentiable. Its order-j derivative norm is at most sqrt(V_j).

An explicit construction uses B>=max(2,deg f), Bernstein coefficients
F_i of f(2t-1), lambda=1+B max_i|F_i|/2, and corner values
c_i=2i/B-1+F_i/lambda in [-1,1]. Their multiaffine cube interpolant M
satisfies lambda(M(z,...,z)-z)=f(z). Rate-lambda B-ary branching to tau
is nonexplosive and has, for each fixed integer q>=1,

    E n^q <= exp(lambda tau(B^q-1)).

This bounded voting representation is a classical ingredient. The field
construction integrates a common Gaussian from the complete nonlinear leaf
polynomial. With residual covariance kappa(C-(tau/n)11^t), uniform U in X,
and a uniform ordered j-tuple I of distinct leaf labels, it uses

    W_j=h_(kappa tau/n)(.-U) (n)_j C_I
                           product_(b=1)^j e(U+Z_(I_b)).

Here C_I is the actual selected mixed leaf derivative of that polynomial,
evaluated using known g. It has absolute value at most one. If n<j,
return zero without querying. Tree, tuple, known evaluations and coefficient
preparation precede acquisitions. The original Brownian leaf law is recovered
by adding the independent common Gaussian to the residual array.

For theta=4*pi^2*kappa*tau, the explicit Gaussian-sum bound in R20/T91
supplies finite C_h with ||h_(kappa tau/n)||_(H^r)^2<=C_h n^(r+d).
One valid cutoff-independent choice is

    V_j=C_h exp(lambda tau(B^(2j+r+d)-1)).

The exact finite real-Fourier projection through box cutoff N is output
by elementary damping/cosine/sine formulas. With K=(2N+1)^d its original
guarded-Cholesky construction costs C[n^3+(1+G)n+K] conditionally, and
C_(f,d,kappa,tau,j)(1+G+K) in expectation in the inherited paid exact-real
primitive model. Constants are not asserted small or parameter-uniform.

For M independent copies, the actual Hilbert risk satisfies

    E||M^-1 sum_a W_(j,a)-E W_j||_(H^r)^2
      <= V_j ||e||inf^(2j)/M.

It is the centered second moment, not this envelope, that gives the exact
variance identity. Correlations among Fourier coordinates are retained.

For f(u)=u-u^5 one exact instance is B=5, lambda=5 and
c=(-1,-23/25,-1/25,1/25,23/25,1). This is an exact representation check;
it supplies no empirical long-horizon performance result.

## D44: the same field law admits linear tree preparation

Fix a finite genealogy with nonnegative segment lengths, common root-to-leaf
height tau>0, n leaves and at least two children at every internal segment.
The one-coordinate covariance C includes every shared ancestral edge. Draw
the usual independent edge Gaussians and their leaf path sums X_i.

At a leaf set a_v=ell_v and A_v=Y_v. At an internal segment, when all child
a_c>0, put h=(sum_c 1/a_c)^-1 and alpha_c=h/a_c. When some a_c=0, give
weight one to the first such child and set h=0. In either case set

    a_v=ell_v+h,     A_v=Y_v+sum_c alpha_c A_c.

At the root the actual A is a convex leaf combination, Var(A)=a,
Cov(X_i,A)=a and Cw=a1 for weights summing to one. Thus Z_i=X_i-A gives

    Cov(Z_i,Z_j)=C_ij-a,     Z independent of the whole scalar A,
    tau/n <= a <= tau.

These statements include singular covariance and zero-length segments.
Joint Gaussianity, not mere zero pairwise correlations, establishes the
whole-vector independence. The assertions are conditional on the genealogy;
unconditional independence in a random-tree mixture is not claimed.

Moreover a is maximal among b for which C-b11^t is positive semidefinite:
testing that matrix on w gives b<=a. This optimizes removable common
Gaussian variance for the fixed tree, not the nonlinear estimator variance.

Use physical residual sqrt(kappa) Z and common heat variance kappa a.
Integrating the common Gaussian in the complete leaf function preserves
the derivative mean. Since a>=tau/n, the heat Hilbert norm is bounded by
the previous envelope, so D43's V_j and query cap still apply. Both residual
law and heat variance change together; damping old samples alone is invalid.

A fixed number of preorder/postorder passes computes path sums, aggregates
and residuals in O_d(n) operations and storage. No dense matrix or expanded
leaf-weight vector is needed. The sample's conditional paid work becomes

    C_(B,j,d)[(1+G)n+K].

Expected preparation work now uses only the first population moment.
Derivative variance still requires higher moments. This is the classical
inverse-variance Gaussian-tree recursion, with the above field-law and
degenerate-case correspondence checked explicitly.

## Boundaries and next gates

The results exclude variable diffusion, systems, gradient nonlinearities,
nonpolynomial reactions, missing invariant intervals, tau=0 and kappa=0.
They do not supply a generalized paid continuation solver or matching
long-time lower bound. For a general inward polynomial, sup f' can differ
from an equilibrium's instability rate, so the Allen–Cahn sharp exponent
cannot simply be copied. D40–D42 remain the accepted full cubic result.

Fixed 05n asks Lean to verify the actual finite Gaussian linear-combination,
independence and pushforward laws. It excludes the tree recursion and PDE
bridge. T89 separately formalizes actual Hilbert sampling risk. Neither is
accepted here by anticipation. No experiment or unknown-input acquisition
was run for D43/D44; frozen E4 remains unchanged. Finite-bit cost, practical
speed, worldwide originality and award significance remain unestablished.
