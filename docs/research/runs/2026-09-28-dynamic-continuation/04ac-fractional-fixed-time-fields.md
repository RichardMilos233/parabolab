# D47: fixed-time derivative fields for fractional diffusion

Date: 2026-09-29. Accepted conventional fixed-time result after T97 and
root correspondence. A full fractional long-time complexity theorem is
not established by this result.

## Frozen evidence and statement

The proof is `reviews/T95-fractional-diffusion-field-feasibility.md`,
773 lines, SHA256
`9bc1d42d582f75b96a4e562dacbc925cbd01151b2a3b4702c5dc2b0a1ab99d74`.
Independent T97, `reviews/T97-fractional-field-independent-audit.md`,
736 lines, SHA256
`9e38a6d166806997d9c42ab8653615edad0a47b0fc1fa81dc9e31e980f5dec90`,
checks twelve lemmas and requires no source repair. Root read both complete
final texts, verified their locks, and independently checked the normalized
stable-law input against Demni's primary paper, pages1–2.

On X=(R/Z)^d fix d>=1, 0<beta<=1, c,tau>0 and a known polynomial f
with f(-1)>=0 and f(1)<=0. Let S_t be the actual flow of

    u_t=-c(-Delta)^beta u+f(u),
    (-Delta)^beta exp(2*pi*i*nu.x)
          =(4*pi^2*|nu|^2)^beta exp(2*pi*i*nu.x).

For known g in C(X), ||g||inf<1, with paid evaluator cost G, and unknown
v in C(X), put e=v-g. For every fixed integer j>=1 there is an actual
strongly measurable H^(d+1)-valued sample W_j with

    E W_j=D^j S_tau(g)[e,...,e],
    E||W_j||_(H^(d+1))^2<=V_j ||e||inf^(2j).

The flow is genuinely C-infinity Frechet differentiable from the open
unit ball of C(X) into this Hilbert space. Derivative directions may be
arbitrary continuous functions. Taylor evaluation at v separately requires
the entire segment g+t(v-g) to remain in the open unit ball.

Only scalar point values of v are acquired, with at most j on every seed,
including repeated locations. A finite real Fourier projection with
K=(2N+1)^d entries costs C[(1+G)n+K] on a finite tree with n leaves,
and C(1+G+K) in expectation. The program halts almost surely. The inherited
paid exact-real primitive model is unchanged; no stable-density, Fourier,
conditional-law or PDE-value oracle is added.

## The clock, Gaussian decomposition, and moment bound

For 0<beta<1, a positive stable variable with Laplace transform exp(-z^beta)
is sampled by the classical Kanter uniform-angle/exponential formula.
Each edge of chronological length ell uses L=(c ell)^(1/beta) S_beta;
ell=0 and beta=1 have separate deterministic branches. Evaluating the
positive-edge formula uses three sines, five logarithms, one exponential,
two scalar draws and fixed arithmetic. Null draw endpoints are guarded.

Conditional on L, that edge has d-dimensional Gaussian covariance 2L I_d.
The SAME scalar clock is shared across its spatial coordinates. Independent
clocks per coordinate would produce a different, anisotropic generator.
Different edges use independent clocks and conditional Gaussian arrays.

Condition on the whole chronological tree and every clock. Its Gaussian
covariance is C=sum_e L_e b_e b_e^t, where b_e indicates descendant leaves.
Let H_i be the clock height to leaf i and m=min_i H_i. Height intervals
along root paths give a partition below m, even for unequal H_i, so

    C>=(m/n)11^t.

The guarded inverse-variance tree recursion of D44 still produces a convex
leaf combination A=w^t X with Cw=a1, Var(A)=a and

    m/n<=a<=m,
    a>=1/(sum_i H_i^(-1)).

The entire residual vector X-A1 is independent of A under this conditional
Gaussian law. Physical residuals are sqrt(2)(X-A1), and the common Gaussian
has covariance 2a I_d. Adding them reconstructs the original leaf law.
Gaussianity, independence and finite covariance are not asserted after
mixing clocks. The recursion and path passes take linear work in n.

Given the chronology, every H_i has the marginal Laplace transform
exp(-c tau z^beta). Leaf heights can be dependent. For q>0,

    M_q=E H_i^(-q)
       =Gamma(q/beta)/[beta Gamma(q)] (c tau)^(-q/beta).

The partition bound gives E[a^(-q)|tree]<=n^(q+1)M_q for all q>0.
The harmonic bound improves this, for q>=1, to

    E[a^(-q)|tree]<=n^q M_q.

The q>=1 restriction matters: T97 gives a two-leaf stable-clock counterexample
to extending this sharper inequality to 0<q<1, including positive root
lengths by a limiting argument. No small-edge time integral is used.

With r=d+1 and P=r+d, Gaussian Fourier sums give
||h_(2a)||_(H^r)^2<=H(1+a^(-P)). The rate-lambda B-ary population has
E n^k<=exp(lambda tau(B^k-1)); nonexplosion is proved from stopped first
moments first. Thus one explicit envelope is

    V_j=H(1+Mbar_P) exp(lambda tau(B^(2j+P)-1)),

where H is elementary and Mbar_P is the factorial upper bound in T95,
so Gamma need not be a computational primitive. The constants depend on
the fixed parameters and need not be small or uniform.

## Actual derivative output and interpretation

Integrate the common Gaussian through the COMPLETE nonlinear leaf
polynomial. With an independent uniform U and an ordered distinct j-tuple I,

    W_j=h_(2a)(.-U) z,
    z=(n)_j C_I product_b e(U+Z_(I_b)).

The selected mixed partial C_I is computed from known g and satisfies
|C_I|<=1. When n<j the output is zero without a query. The actual nonzero
real Fourier coefficients are

    2z exp(-4*pi^2*a*|nu|^2) cos(2*pi*nu.U),
    2z exp(-4*pi^2*a*|nu|^2) sin(2*pi*nu.U).

The moment envelopes justify Bochner integration and Frechet differentiation
via finite-tree Taylor remainders. For M independent complete samples,
the projected average has H^r risk at most V_j||e||inf^(2j)/M around
the PROJECTED derivative. Comparing to the full derivative also requires
the omitted Fourier tail. Fourier coordinates inside a sample can correlate.

For beta<1/2, spatial analyticity fails even for f=0: choose
2beta<eta<1 and a small smooth signed cosine series with coefficients
delta exp(-k^eta). At positive time its coefficients are
(delta/2)exp[-k^eta-c tau(2*pi*k)^(2beta)], which have no exponential-in-k
bound. This invalidates simply copying the old analytic cutoff argument.
It does not exclude a weaker Gevrey estimate or polynomial cutoff cost.

Kanter sampling, subordination, negative stable moments and fractional
branching have published predecessors, including Penent–Privault. Their
no-gradient branching result already removes the relevant short-edge
integrability restriction; the initial-data derivative here is a different
object from a spatial derivative weight. No novelty is assigned to those
ingredients. A paid fractional known-profile solver, same-class long-time
composition/lower theorem, implementation and full formalization remain
separate. This checkpoint adds no numerical acquisition.
