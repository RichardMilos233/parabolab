# T98: independent audit of the frozen E5 smooth-field protocol

Date: 2026-09-29. Verdict: **PASS as a preimplementation component
protocol. No mathematical or accounting repair to the frozen protocol is
necessary.** This is not a pass of an implementation or an experimental
result: neither was executed in this audit.

The protocol's references, derivative normalization, common-Gaussian law,
real Fourier output, Hilbert weights, fixed streams, acquisition caps and
abort rules are mutually consistent with accepted D43/D44. Several choices
must be recorded when the implementation is frozen; section 11 distinguishes
these from changes to the estimator. In particular, the common variance is
in chronological units before multiplication by kappa, and the analytic
cells alone cannot diagnose every incorrect cross-leaf covariance.

## 1. Scope, frozen sources and verification level

The inspected repository HEAD was
`65dca46e42db1c80cdf9ddd8eed6a415148c37f3`. The working tree contains other
ongoing work; this audit does not claim that HEAD alone identifies all
inspected source bytes. The run directory is
`docs/research/runs/2026-09-28-dynamic-continuation`.

The following source SHA256 values were rechecked for this audit:

| Source relative to the run directory | SHA256 |
| --- | --- |
| `02h-smooth-field-component-experiment-protocol.md` | `1866585a86fcfceb0f9b05f632dae093d3c6e03f4ab005b4eae02fbfa5b27612` |
| `04aa-polynomial-fields-and-linear-gaussian-preparation.md` | `433c699d951c74fa6ba19166e159069130e1340a7a319aa0334b0ba4f8a1b8a1` |
| `reviews/R20-polynomial-reaction-field-sampler-candidate.md` | `b1e42a195c67942066894d04a11c28d7ba2951a6d6730977070e424ac84542b9` |
| `reviews/R20b-continuous-domain-addendum.md` | `6c5e8b158ca269588c4200ca09c82f4ffa430e8aa0146a52022370ade352e527` |
| `reviews/R21-linear-tree-common-gaussian-candidate.md` | `99f8a23c98332b6797ee1ecc9f0929d94950cd047acb17bcbea0df9052ff7461` |
| `reviews/T91-polynomial-field-linear-gaussian-independent-audit.md` | `2f06d787fcbb631662b3be4997eb6c610e145120147a0e831d245345abde1af7` |

The protocol and accepted 04aa statement were read completely for this
assignment. The underlying R20, mandatory R20b, R21 and T91 had been read
in this worker's preceding bounded assignment; their frozen identities
were rechecked and the relevant constructions reread here. R20 alone is
not the accepted continuous-domain statement, and its uncorrected final
risk wording is not used.

This audit independently derives the identities below by conventional
mathematics. It uses no numerical output, symbolic-computation result,
Lean result produced by this worker, or observed sample. The only external
sources newly needed are official NumPy documentation for the specified
random-stream interface. They are cited in section 7.

The math-auto-research workflow is applied within the root's bounded
ownership instruction: this file is the only output owned by this audit.
No protocol, ledger, old evidence, Lean source, implementation or experiment
was edited. Unknown-input acquisitions in this audit: **zero**.

The requested dispatch was gpt-6-astra with maximum reasoning effort;
the serving backend is not observable here. This records a requested role,
not an independently verified model identity.

## 2. Both branching parent laws are correct

Write b for the constant initial base, to distinguish it from the root
common-variance parameter a_T used below. Let eta be the displayed shape
1 or cos(2*pi*x). The actual derivative direction is
d=v-g=delta eta, delta=1/10. All six bases and directions are continuous;
the listed base and perturbed profiles lie strictly inside the unit ball.

For the cubic parent,

    M3(y1,y2,y3) = (y1+y2+y3-y1 y2 y3)/2,
    2(M3(z,z,z)-z) = 2((3z-z^3)/2-z) = z-z^3.

At corners with i positive signs, i=0,1,2,3, its values are
(-1,-1,1,1). Multiaffine interpolation is a convex combination of corner
values on the cube, so M3 maps [-1,1]^3 into [-1,1]. The stated rate is
lambda=2, not an unmentioned unit-rate convention.

For the quintic parent,

    M5(y1,...,y5) = (6/25) sum_i yi - (1/5) product_i yi,
    5(M5(z,...,z)-z) = 5((6/5)z-(1/5)z^5-z) = z-z^5.

At a corner with i positive signs, sum yi=2i-5 and
product yi=(-1)^(5-i). Substitution gives exactly

    (-1, -23/25, -1/25, 1/25, 23/25, 1).

Thus the quintic rule is also bounded on the cube. This derivation uses
the accepted particular parent in 04aa, not any pending generalized rule.

For a rate-lambda B-ary tree, each split changes the leaf population by
B-1. Consequently E n=exp(lambda(B-1)tau). For the cubic cells this exponent
is 2*2*(1/2)=2; for the quintic cells it is 5*4*(1/10)=2.
The probability of at least one split is 1-exp(-lambda tau), giving
1-exp(-1) and 1-exp(-1/2), as stated. Equal expected populations do not
make their full population or estimator distributions identical.

A full finite B-ary tree with I internal segments has

    n=1+(B-1)I,       number of segments=1+B I=(B n-1)/(B-1).

These identities provide inexpensive node/leaf-count reconciliation.
They also show that n<j in every listed j=2 or j=3 cell occurs exactly
when there has been no split. The one-leaf event must remain in the data.

## 3. Actual mixed partials and the ordered-tuple normalization

Let P_T(y1,...,yn) be the complete recursively composed leaf polynomial.
Every leaf label belongs to exactly one child subtree at each ancestor.
Separate affinity of M3/M5 and disjoint child leaf sets imply that P_T is
multiaffine in the original n leaf variables, with values in [-1,1]
on their cube.

For a set S of j distinct selected leaves and fixed unselected values,

    partial_S P_T
      = 2^(-j) sum_(epsilon in {-1,1}^S)
                    (product_(i in S) epsilon_i) P_T(y^(epsilon)).

Here y^(epsilon) substitutes the signs only at selected leaf variables.
It does not substitute signs at their parents or at every leaf.
The selected derivative is independent of the selected base values, and
the formula proves |partial_S P_T|<=1. Repeated differentiation with
respect to the same leaf label gives zero.

This is the derivative that must be computed by the protocol's complete
signed-corner passes. Known leaf values are g(U+Z_i)=b here. Internal
subtree values generally are not b: for example M3(b,b,b) need not equal b.
Replacing every internal base value by b is an incorrect shortcut.

An independent recursive fixture calculation can use the following
identity. At a node with child polynomials P_c, put S_c=S intersect the
child's descendant labels, and A={c:S_c is nonempty}. For S nonempty,

    partial_S P_node
      = (partial_A M)(P_1,...,P_B)
          product_(c in A) partial_(S_c) P_c.

For S empty, evaluate P_node normally. This formula follows by separate
affinity; no second derivative of M in a repeated child variable remains.
At a leaf its own first partial is one and all incompatible partials are
zero. This is an independent chain-rule computation, not a second call
to the corner implementation under a different name.

The local parent partials needed by that recursion are explicit:

    partial_i M3 = 1/2 - (1/2) product_(k != i) yk;
    partial_S M3 = -(1/2) product_(k notin S) yk,  2<=|S|<=3;

    partial_i M5 = 6/25 - (1/5) product_(k != i) yk;
    partial_S M5 = -(1/5) product_(k notin S) yk,  2<=|S|<=5.

An empty product is one. Repeated selected node coordinates give zero.

Differentiating P_T evaluated at g+t d gives

    D^j[P_T(g)][d,...,d]
      = sum_(ordered distinct I1,...,Ij)
          partial_I P_T(g) product_(h=1)^j d_(Ih)
      = j! sum_(unordered S, |S|=j)
          partial_S P_T(g) product_(i in S) d_i.

A uniform ordered tuple has probability 1/(n)_j. Its weight (n)_j in
the protocol therefore gives the actual Frechet derivative. There is no
division by j! in E5. Such a division belongs to a Taylor coefficient,
which E5 is not estimating. Nor should an extra delta^j be inserted:
each observed v-g already includes delta.

As a sign/factorial check, a cubic first-split tree has
partial_123 M3=-1/2, so its j=3 tuple weight is 6*(-1/2)=-3.
A split has probability 2 tau+o(tau), producing -6 tau delta^3+o(tau),
which agrees with f'''(0) tau delta^3. Similarly, the cubic j=2 weight
at leaf base b is -3b and the quintic j=2 weight is -4b^3.
After multiplying by first-split rates 2 and 5, these are
f''(b)=-6b and f''(b)=-20b^3. These checks are algebraic, not simulations.

At most 2^j full parent passes are needed. Here j<=3, B is fixed and
the segment count is linear in n, so this is O(n) arithmetic after
known-leaf evaluation. No unknown-value acquisition is needed to compute
the selected coefficient.

## 4. Chronological covariance and the actual residual law

Fix a clock genealogy T. Let ell_e be its nonnegative chronological
segment lengths, and let every root-to-leaf sum equal tau. In this section,

    C_ij = sum_(e shared by paths i,j) ell_e

has chronological units. It is not yet the covariance of the physical
draws. Draw independent Y_e with law N(0,kappa ell_e); these are the
protocol's physical edge Gaussians. Their leaf sums X_i have covariance
kappa C, and C_ii=tau.

The scalar recursion uses the unscaled lengths:

    leaf: a_v=ell_v;
    positive child case:
        h=(sum_c 1/a_c)^(-1),    alpha_c=h/a_c;
    zero child case:
        h=0, alpha=1 on the first zero child, 0 on other children;
    internal: a_v=ell_v+h.

Using the same deterministic alpha values, the physical aggregate is

    leaf: A_v=Y_v;
    internal: A_v=Y_v+sum_c alpha_c A_c.

Thus a_T=a_root is chronological, whereas A=A_root is physical.
The protocol uses the letter a both for an initial base in its cell list
and for this common variance in its algorithm. D44 and the explicit
fixture bound tau/n<=a<=tau resolve the meanings. They must occupy
distinct implementation variables.

In either guard branch,

    alpha_c>=0,     sum_c alpha_c=1,
    alpha_c a_c=h,  sum_c alpha_c^2 a_c=h.

Induction through independent child subtrees yields

    Var(A_v)=kappa a_v,
    Cov(X_(v,i),A_v)=kappa a_v.

The aggregate is a convex leaf combination A=sum_i w_i X_i, with
sum w_i=1 and Cw=a_T 1. Defining the actual residuals by Z_i=X_i-A gives

    Var(A)=kappa a_T,
    Cov(Z_i,A)=0,
    Cov(Z_i,Z_j)=kappa(C_ij-a_T),
    X_i=A+Z_i.

All these variables are jointly Gaussian conditional on T. The zero
cross-covariance block therefore makes A independent of the entire
residual vector, including singular cases. This is a conditional
Gaussian assertion. Marginalizing over random T need not leave A and Z
independent.

For completeness, at almost every time s in (0,tau), the living edges
partition the terminal labels into k(s)<=n descendant blocks. Hence,
for every real vector q,

    q^t C q
      = integral_0^tau sum_(blocks D at s) (sum_(i in D) q_i)^2 ds
      >= (tau/n) (sum_i q_i)^2.

Applying this to w proves a_T>=tau/n>0. Since 0<=C_ij<=tau and w is a
probability vector, a_T=w^t Cw<=tau. The residual covariance is positive
semidefinite directly from its construction. Testing C-b*11^t on w
also shows b<=a_T whenever that matrix is positive semidefinite.

The allowed stable harmonic expression is algebraically identical:

    m=min_c a_c>0,
    h=m/(sum_c m/a_c)=(sum_c 1/a_c)^(-1).

Its denominator lies in [1,B], so m/B<=h<=m. The exact zero guard must
precede every division. Replacing a small positive a_c by zero, clipping
a negative covariance entry, or adding a ridge changes the stipulated
exact law. Ordinary binary64 rounding is already disclosed by the
protocol; these extra alterations are not licensed by that disclosure.

One may instead derive the same recursion from physical variances
kappa ell_e, but then its root output is kappa a_T and must not be
multiplied by kappa again. The frozen protocol chooses the chronological
a_T convention. Using physical a values and the displayed kappa*a
damping would be an implementation error, not an alternative estimator.

### Nonlinear common translation

For fixed T and residuals Z, let F_q(u)=P_T(q(u+Z_1),...,q(u+Z_n)).
Conditional independence and symmetry of the wrapped Gaussian give

    E_A F_q(x+A)
      = integral_[0,1) h_(kappa a_T)(x-u) F_q(u) du.

The same identity holds for the complete ordered directional derivative
of F_q. Independently choosing uniform U and a uniform ordered leaf tuple
therefore gives the accepted sample

    W_j(x)=h_(kappa a_T)(x-U) z,
    z=(n)_j C_I product_h [v(U+Z_(Ih))-g(U+Z_(Ih))].

The selected C_I is evaluated in the same translated array as every
residual value. The original Brownian tree law is recovered by adding
the common A to these Z_i. Subtracting an independently redrawn shift,
or damping the unmodified X_i instead, does not implement this identity.

All additions at the evaluator boundary are reduced modulo one. The
covariance calculations concern lifted real Gaussians, so reducing the
query positions modulo one does not change the periodic-field law.

### Deterministic fixture content

The protocol's required fixture classes have explicit independent checks:

- One leaf: C=[tau], w=[1], a_T=tau, A=X_1 and Z_1=0.
- A B-star with ancestral length b0 and positive terminal length
  t=tau-b0: C=b0*11^t+t*I, w_i=1/B,
  a_T=b0+t/B and Cov(Z)=kappa*t*(I-11^t/B).
- An unbalanced full B-ary tree: root length b0, one child of length c
  that splits into B terminal edges of length t-c, and B-1 other
  terminal root children of length t. Here 0<=c<t=tau-b0. The split
  child's effective variance is u=c+(t-c)/B. For positive t,u,
  a_T=b0+(1/u+(B-1)/t)^(-1). Its B grandchildren each receive weight
  alpha_split/B; the other root children receive their root alpha.
  This supplies unequal child effective variances without unequal
  root-to-leaf heights.
- Taking b0=tau in the star makes all terminal edges zero. The prescribed
  first-zero guard gives a_T=tau and Z=0. C=tau*11^t is singular;
  an inverse-C fixture must not exclude it.
- Taking one leaf in j=2 or j=3 gives n<j, the zero array and no call to v.

For each small fixture, form C independently from shared paths and
form w from products of child weights. Check Cw=a_T 1 and the physical
residual covariance kappa(C-a_T*11^t), using stated tolerances. A small
Gaussian simulation may reveal a coding error, but cannot prove whole
vector independence. No such simulation was performed here.

## 5. Fourier signs, normalization and the H^2 norm

Use normalized Lebesgue measure on the unit torus and the complex
Fourier convention exp(2*pi*i*nu*x). For sigma=kappa a_T,

    h_sigma(x-U)
      = sum_(nu in Z) exp(-2*pi^2*sigma*nu^2)
                       exp(2*pi*i*nu*x) exp(-2*pi*i*nu*U).

Pairing the positive and negative frequencies gives

    h_sigma(x-U)
      = 1 + 2 sum_(nu>=1) exp(-2*pi^2*sigma*nu^2)
          [cos(2*pi*nu*x) cos(2*pi*nu*U)
           + sin(2*pi*nu*x) sin(2*pi*nu*U)].

Multiplication by the real z proves the exact real coefficients in
02h: constant z; cosine 2z times damping times cos(U); sine 2z times
damping times sin(U), with a positive sine sign. For example U=1/4,
z=1 and nu=1 have a positive sine coefficient. A sine-sign error need
not be detected by a zero-sine analytic target, so the explicit
deterministic fixture is substantive.

For a real array with coefficients c0, c_cos,nu, c_sin,nu,

    hat c_nu=(c_cos,nu - i*c_sin,nu)/2,    nu>0.

The inherited Fourier definition of H^2 has weight (1+nu^2)^2.
Pairing the two complex frequencies yields

    ||c||_(H^2)^2
       = c0^2 + (1/2) sum_(nu=1)^N
                       (1+nu^2)^2(c_cos,nu^2+c_sin,nu^2).

Thus the half factor and the protocol's weights are correct.
Substituting (1+4*pi^2*nu^2)^2 would define a different, equivalent
norm rather than the stipulated one. Treating the real cosine basis
as orthonormal would also change the numerical statistic.

For N=4,16,64 the real dimensions are 9,33,129. One unambiguous storage
layout is [c0,c_cos,1,c_sin,1,...], whose literal prefixes have those
lengths; a labeled frequency axis is equally valid. The storage schema
must make the prescribed nested projections exact. Recomputing fresh
samples for each cutoff is not allowed.

No independence of different Fourier coordinates is used. For every
fixed positive kappa,tau, accepted D43/D44 give

    |z|<=(n)_j delta^j,
    ||h_(kappa a_T)||_(H^2)^2 <= C_h n^3,
    E||W_j||_(H^2)^2 <= C_h delta^(2j) E n^(2j+3) < infinity.

Projection cannot increase that norm. These conventional moment facts
justify the Hilbert averaging identity, but a finite E5 run cannot
prove their universal bounds or their usefulness as numerical constants.

## 6. All six analytic references, including both diffusivities

Let m=D-1 and R=1+(exp(m t)-1)b^m. Solving the constant-profile ODE
u'=u-u^(m+1), for instance by differentiating u^(-m) away from zero
and extending at zero, gives

    phi_t(b)=b exp(t) R^(-1/m).

Direct differentiation gives

    phi'_t(b)=exp(t) R^(-1-1/m),
    phi''_t(b)=-(m+1)exp(t)(exp(m t)-1)b^(m-1) R^(-2-1/m).

At a constant base the first variational equation is

    w_t=(kappa/2) w_xx + f'(phi_t(b)) w.

The scalar multiplier exp(integral_0^t f'(phi_s(b)) ds) is phi'_t(b).
The eigenvalue of the diffusion operator on cos(2*pi*x) is
-2*pi^2*kappa. Therefore its order-one reference is exactly

    delta phi'_tau(b) exp(-2*pi^2*kappa*tau) cos(2*pi*x).

For constant directions, S_tau(b+s delta) is the scalar function
phi_tau(b+s delta), so the second derivative is delta^2 phi''_tau(b).
For the cubic at b=0,

    phi_tau(b)
      = exp(tau)[b-(1/2)(exp(2*tau)-1)b^3+O(b^5)],

and its third derivative is
-3 delta^3 exp(tau)(exp(2*tau)-1). None of these is a finite difference
or a spatially discretized PDE reference.

Define the exact constants

    E3=exp(1/2),       R3=(15+exp(1))/16,
    E5=exp(1/10),      R5=(255+exp(2/5))/256,
    d3(kappa)=exp(-pi^2*kappa),
    d5(kappa)=exp(-pi^2*kappa/5).

The following table gives every nonzero real target coefficient. The
first cell index uses kappa=1/100; the second uses kappa=1/10. All other
real coefficients, including every sine coefficient, are zero.

| Configuration | Cell indices | Nonzero coefficient | Exact value |
| --- | --- | --- | --- |
| D=3, tau=1/2, b=0, j=1, cosine direction | 0,6 | cosine mode 1 | (1/10) E3 d3(kappa) |
| D=3, tau=1/2, b=1/4, j=1, cosine direction | 1,7 | cosine mode 1 | (1/10) E3 R3^(-3/2) d3(kappa) |
| D=3, tau=1/2, b=1/4, j=2, constant direction | 2,8 | constant | -(3/400) E3 (exp(1)-1) R3^(-5/2) |
| D=3, tau=1/2, b=0, j=3, constant direction | 3,9 | constant | -(3/1000) E3 (exp(1)-1) |
| D=5, tau=1/10, b=1/4, j=1, cosine direction | 4,10 | cosine mode 1 | (1/10) E5 R5^(-5/4) d5(kappa) |
| D=5, tau=1/10, b=1/4, j=2, constant direction | 5,11 | constant | -(1/1280) E5 (exp(2/5)-1) R5^(-9/4) |

The diffusivity substitution is fully determined:

| kappa | d3(kappa) | d5(kappa) |
| --- | --- | --- |
| 1/100 | exp(-pi^2/100) | exp(-pi^2/500) |
| 1/10 | exp(-pi^2/10) | exp(-pi^2/50) |

A target A*cos(2*pi*x) has real cosine coefficient A, not 2A; its
complex coefficients at +/-1 are A/2. Its H^2 norm squared is 2A^2.
A target constant B has norm squared B^2. The constant references
are kappa-independent even though their estimator variances need not be.

These exact expressions independently check all protocol factors and
signs. High-precision decimal evaluations and their binary64 conversions
remain work for the later implementation; this audit did not execute them.
The reference library, precision and rounding conversion should be
recorded with those values. The protocol correctly disclaims interval
certification.

### Exact limitation of these reference cells

Because g is constant, the entire coefficient C_I depends on T and I
but not on U or Z. All nonconstant directions in E5 have j=1. Conditional
on T,I=i, their analytic mean depends on Z_i only through

    E exp(2*pi*i*Z_i)=exp(-2*pi^2*kappa*(tau-a_T)).

Multiplying by the heat damping gives exp(-2*pi^2*kappa*tau).
For all j>=2 cells the directions are constant, so z does not depend
on residual positions at all.

Consequently an incorrect implementation that replaces the residual
vector by independent centered Gaussians with the correct individual
variances kappa*(tau-a_T) can pass all six analytic mean references.
For these particular cells even the sampled field's distribution can
fail to expose the missing cross-leaf correlations, since each
nonconstant sample uses only one selected residual value.

This is a genuine coverage limit, not an algebraic flaw or a reason to
change the frozen cell list. It explains why the required dense joint
covariance fixtures and independent code-to-D44 correspondence cannot
be replaced by good-looking PDE-reference plots. Similarly, the sine
sign is fixed by the Fourier fixtures, not established by targets whose
sine coefficients vanish. Passing E5 remains the bounded component
diagnostic stated in the protocol.

## 7. Stream and replay reproducibility

The exact mapping is

    Generator(PCG64DXSM(SeedSequence(
        [seed, cell_index, sample_index, tag]))).

Here seed is one of 2026092901, 2026092902, 2026092903;
cell_index is 0,...,11 in the protocol's displayed order;
sample_index is 0,...,4095 for official sampling;
tag=0 is official and tag=1 is preflight. The prespecified replays use
the original tag=0 and sample indices 0,...,7. They do not acquire new
statistical replicates by using a new tag or seed.

Official NumPy documentation confirms that PCG64DXSM accepts a
SeedSequence and guarantees a stable seeded integer stream. It is
distinct from PCG64; an unspecified default generator would not implement
the frozen choice. [NumPy PCG64DXSM documentation](https://numpy.org/doc/stable/reference/random/bit_generators/pcg64dxsm.html)

NumPy supports combining deterministic unique identifiers and a root
seed in an integer sequence. The prescribed four-entry lists provide
such explicit identifiers. The documentation describes statistical
stream separation, not a proof of mathematical independence of finite
pseudorandom samples. The root-first ordering should remain frozen;
there is no need to introduce a separate spawn hierarchy. [NumPy parallel random number generation](https://numpy.org/doc/stable/reference/random/parallel.html)

For distribution-valued draws, replay also depends on identical method
calls and arguments, including requested array sizes, and on the NumPy
build and environment. Merely repeating a seed with a different traversal
or vectorization is insufficient. NumPy's stated compatibility conditions
therefore support recording the actual implementation and environment,
rather than promising universal cross-version bitwise replay. [NumPy compatibility policy](https://numpy.org/doc/stable/reference/random/compatibility.html)

The implementation manifest should freeze the code hash, NumPy version
and build/environment, arithmetic dtype, chronology traversal and child
ordering, zero-length draw policy, exact exponential/Gaussian APIs and
draw shapes, ordered-tuple method, and U-draw position in the call sequence.
These are implementation choices consistent with the protocol; they
must not be selected after seeing official results. The same frozen
program can reconstruct each sample from its four-entry identifier.

Within the ideal model, clock, Gaussian, U and tuple randomness are
independent as specified by D43/D44. The future binary64 program will be
a disclosed pseudorandom realization of that design. The present audit
does not certify ideal randomness from deterministic seed labels.

A separate sample generator for every identifier makes official sample
content independent of scheduling order, provided no shared mutable RNG
or cross-sample adaptive state is added. Outputs should be stored in
the prescribed index order. Replay compares deterministic mathematical
metadata and coefficients, not elapsed-time values.

## 8. Nested cutoffs, batches and prescribed statistics

There are 12*3*4096=147456 planned official field samples. Each stores
one N=64 array of length 129; the N=4 and N=16 arrays are projections of
those same data. All cutoffs therefore use the same tree, tuple, U,
unknown observations, scalar z and common variance.

For each cell/seed, let L=4096 and let X_i^N be the projected real array.
For M in {1,4,16,64,256}, use consecutive disjoint batches and define

    B_M=L/M,
    bar X_b^(M,N)=(1/M) sum_(i in batch b) X_i^N,
    Ehat_(M,N)=(1/B_M) sum_b ||bar X_b^(M,N)-r_N||_(H^2)^2.

The batch counts are respectively 4096,1024,256,64,16.
No new original-value calls are involved. For a fixed M, ideal batches
use disjoint samples. Different M and N reuse data and are correlated.

The coefficient mean error is

    (1/L) sum_i X_i^N - r_N.

Equivalently it is the mean of the batch-mean errors for every listed M.
It is thus the same statistic across M up to floating summation order,
not five independent estimates. The raw sample Hilbert second moment is

    (1/L) sum_i ||X_i^N||_(H^2)^2.

It is distinct from centered sample variance. For independent ideal
copies, the exact population identity is

    E||bar X^(M,N)-r_N||_(H^2)^2
      = [E||X^N||_(H^2)^2-||r_N||_(H^2)^2]/M.

This uses zero expected inner products between different centered
samples, not independence among the Fourier coordinates of one sample.
The accepted V_j envelope supplies an inequality, not equality to
V_j*delta^(2j)/M.

The reported M*Ehat values are diagnostics of this scaling; a finite
realization need not give exactly flat scaled values. The unscaled Ehat
does have a pathwise monotonicity here: every larger batch averages four
adjacent smaller batches, and Jensen's inequality shows
Ehat_(4M,N)<=Ehat_(M,N). This decrease is built into nested grouping, so
it is not itself evidence of 1/M scaling. A violation beyond rounding
tolerance indicates changed data or an aggregation error. Since the
reference is contained in every cutoff, increasing N adds nonnegative
squared-error terms to each fixed batch error, apart from roundoff;
there is no target truncation bias in these cells.

One transparent convention for the unspecified standardized discrepancy
is a coordinatewise value

    (sample_mean - target)/(sample_standard_deviation/sqrt(L))

when that standard deviation is positive, with its precise sample
variance divisor recorded. Other declared descriptive conventions must
identify their denominator. Zero empirical variance is reported directly,
not repaired by an arbitrary denominator. These values are not calibrated
joint confidence statements or proofs of unbiasedness.

The three seed runs must be displayed without selection. Their spread
is descriptive; neither the protocol nor this audit infers a guaranteed
coverage probability or a central-limit accuracy bound from three seeds.

## 9. Oracle caps, actual calls and replay arithmetic

The unknown scalar evaluator is the sole acquisition boundary.
Every invocation is charged, including repeated locations, constant
profiles, failures after entry and full replays. Known g calls, reference
formula evaluation, raw-array analysis and arithmetic are separately
accounted work; none licenses uncounted direct access to v.

With n>=j, the written algorithm queries the selected j distinct leaf
labels. Their spatial locations need not be distinct. With n<j it returns
the zero output without querying. Therefore the per-output cap is j on
every completed sample, including those with coincident coordinates.

For one diffusivity, the six derivative orders sum to

    1+1+2+3+1+2=10.

For all twelve cells the sum is 20. The official hard cap is exactly

    20*3*4096=245760.

A second reconciliation by order gives:

| Derivative order | Number of cells | Official samples | Maximum v calls |
| --- | --- | --- | --- |
| 1 | 6 | 73728 | 73728 |
| 2 | 4 | 49152 | 98304 |
| 3 | 2 | 24576 | 73728 |
| Total | 12 | 147456 | 245760 |

For the literal rule making j calls whenever n>=j, the expected total
official calls are

    24576 * [3+5(1-exp(-1))+2(1-exp(-1/2))]
      =24576 * [10-5exp(-1)-2exp(-1/2)].

This is an ideal expectation for a complete suite, not a realized budget
or a criterion for rejecting an observed run.

The fixed replay visits 12*3*8=288 original sample identifiers. Its
tighter worst-case acquisition count is

    20*3*8=480.

The protocol's 864 is the valid looser bound 288*max(j)=288*3.
It is not an arithmetic error and requires no repair. The unused
difference is not permission to choose additional replay indices.

Using the protocol's conservative caps,

    preflight + official + replay
      <=8192+245760+864
      =254816 < 300000.

The global remainder under these reservations is 45184. Using the
tighter scheduled-replay bound would give 254432 and remainder 45568.
Neither calculation enlarges the fixed official suite. Debugging,
failed versions, repeated preflight calls and any attempted rerun must
all fit the same global 300000-call ledger.

Counters must persist across failures and versions. In an implementation,
an atomic capacity-check-and-charge immediately before invoking v
prevents exceptions or parallel workers from creating
unlogged calls or overrunning the cap. The local preflight and official
caps still apply; the global cap is not a substitute for them.

Reading stored raw observations or recomputing their statistics costs no
new original-value query. Re-executing the sampler against the opaque v
does. An arithmetic check using cached old values must not be mislabeled
as a new, uncharged original-value acquisition.

The reference calculation is intentionally outside the sampler. A code
correspondence audit must verify that the sampler receives the known g
evaluator and opaque v callback, not the test-profile formula or analytic
answer. The fact that the experimental harness knows its own synthetic
input does not exempt a sampler invocation from charging.

E4's frozen budget, counter and evidence remain separate and immutable.

## 10. Work measurement, abort semantics and retained evidence

Tree generation precedes acquisitions. A fixed number of tree passes,
the selected-corner passes and known evaluations require O((1+G)n)
conditional work for fixed B,j. The real output through N=64 requires
O(K), K=129 here. E5 should report actual measured generation/output
time, node count, Gaussian draws and g calls; it does not infer a finite-bit
operation theorem or practical speed from the ideal O(n+K) expression.

The implementation must state timer boundaries. Computing N=64 once
and taking shorter prefixes shares costs. The reported cutoff times
must identify this reuse instead of counting three independent trees.
Random generation, known evaluations, preparation, output and record
handling are real elapsed work even when they consume no v queries.

The frozen limits are 100000 segments per tree, 10000000 total generated
segments, 30 minutes for the official suite, and finite output values.
The natural conservative reading of total generated segments includes
preflight, failed attempts and replays as well as official generation;
record that scope in the run manifest. It does not permit resetting
a total counter when a version changes.

Encountering a limit, a nonfinite output, or a failed required fixture
does not create a legitimate zero sample. Retain the attempted identifier,
prefix, failure reason and all resource/acquisition counts, then stop the
official suite as specified. Never redraw a large tree, discard an
unfavorable sample or fill a missing sample with zero. Replacing a sample
conditioned on its size or outcome changes its law.

A capped incomplete attempt may be inspected and reported as incomplete.
It is not a completed unbiased full suite, and its missing outputs cannot
be supplied by relabeling additional runs as replay. A later separately
identified attempt, if undertaken by the root, must preserve the earlier
failure and cumulative budgets; this audit does not execute or prescribe
such an attempt.

Before a later numerical validation can be credited, the evidence needs:

- The frozen protocol and implementation identities, parameter/cell map,
  RNG/environment manifest, reference expressions and evaluated targets,
  fixture tolerances and result records.
- Every planned raw N=64 array with cell, seed and sample index, including
  n<j zero outputs; node/leaf counts, chronological a_T, ordered tuple
  or explicit no-tuple reason, replay metadata and per-output v counts.
- Logs reconciling preflight, official, replay, debugging and failed
  acquisitions against persistent counters, plus work/timing data.
- Independent preflight corner-versus-recursion checks, shared-path dense
  covariance checks, zero-guard fixtures and explicit Fourier-sign checks.
- An independent auditor's recomputation of the real H^2 norms, projections,
  batches, second moments and displayed discrepancies from raw data.
- Replays of precisely indices 0,...,7 in every completed seed/cell using
  the original streams, with new evaluator invocations charged and every
  mismatch or unavailable output reported.
- Scientific figures labeled with D, tau, base, direction, j, kappa, cutoff,
  batch size, seed, units and completion status. Prior E1-E4 artifacts
  remain unchanged.

This list explicates evidence already required by the protocol. A graph
matching a reference without these artifacts would not establish the
claimed implementation correspondence or its acquisition accounting.

## 11. Ambiguity classification and final scope

| Point | Classification | Consequence |
| --- | --- | --- |
| Initial base a versus root common a | Source-resolved notation reuse | Use distinct variables b and a_T; damping uses the latter. |
| Physical edge draws versus chronological a_v and C | Source-resolved convention | D44 and tau/n<=a_T<=tau fix the unscaled recursion; covariance and damping both receive one kappa factor. |
| Ordered tuples and factorials | No ambiguity in the accepted derivative contract | Weight (n)_j estimates D^j, with no extra 1/j! or delta^j. |
| Replay 864 versus 480 | Valid conservative budget | Keep the frozen 864 cap and fixed indices; no amendment is needed. |
| Array layout and prefix extraction | Implementation discretion | Freeze a schema that gives exactly the same modes without new calls. |
| Tree traversal, RNG call shape and leaf selection routine | Implementation discretion affecting replay | Freeze them with code/environment before official execution; the same abstract law can have different seeded arrays. |
| Tolerances, high-precision reference settings and timer boundaries | Implementation discretion affecting evidence | State them before official output inspection and retain failed preflight versions. |
| Standardized-discrepancy convention | Descriptive analysis discretion | Record the chosen denominator and avoid unprovided confidence claims. |
| No numerical pass/fail significance threshold | Consistent with a diagnostic protocol | Do not invent a post hoc theorem or acceptance certificate from small discrepancies. |
| Joint residual law not identified by the six analytic means | Real coverage limitation | Mandatory covariance fixtures and code correspondence remain necessary; no new cells are introduced here. |
| Pseudorandom binary64 versus exact-real primitives | Explicit disclosed scope | No exact-real or finite-bit accuracy theorem is inferred from replay. |

No row requires changing the frozen protocol bytes. A future wish to
change cells, seeds, cutoffs, caps, estimators, clipping, or abort treatment
would require a separately versioned design rather than reinterpretation
of this PASS.

The root reported that T89 and T93's named formal prerequisites have
been accepted. This auditor did not rerun or independently re-audit those
Lean modules. They concern finite Hilbert/Gaussian correspondence and do
not formalize the whole branching/PDE bridge.

The present result is an independent conventional **protocol PASS**.
Implementation review, preflight, official sampling, independent raw-data
audit and replay remain separate work. E5 remains a fixed-time component
diagnostic. It supplies no long-horizon performance certification,
universal numerical unbiasedness certificate, full signed/minimax test,
new theorem for other reaction/diffusion candidates, finite-bit guarantee,
priority claim or award-level conclusion.
