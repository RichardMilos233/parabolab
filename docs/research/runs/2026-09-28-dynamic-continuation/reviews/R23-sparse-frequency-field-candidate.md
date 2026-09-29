# R23: one random Fourier mode per derivative-tree sample

Date: 2026-09-29. Root conventional candidate, pending independent audit.
This changes the sampling law and its variance constant. It is not a new
experiment or an amendment to frozen E5. The point is a finite arithmetic
improvement: accumulate M derivative samples in O(M(1+G)+K) expected work,
instead of paying for all K coefficients at each of the M samples.

## 1. Exact inherited object and source locks

Use D43/D44 on the unit d-torus, fixed d>=1, kappa,tau>0, fixed inward
polynomial f, known g in C(X) with sup norm <1 and evaluator cost G, and
unknown continuous v with e=v-g. Only scalar v(x) queries acquire unknown
information, including repeats. Fix derivative order j>=1. The paid model
is the existing exact-real primitive model, including floor, real arithmetic,
uniform draws and ideal finite integer/index words; no bit bound is claimed.

The accepted source is 04aa-polynomial-fields-and-linear-gaussian-preparation.md,
SHA256 433c699d951c74fa6ba19166e159069130e1340a7a319aa0334b0ba4f8a1b8a1.
Its mandatory domain repair is reviews/R20b-continuous-domain-addendum.md,
SHA256 6c5e8b158ca269588c4200ca09c82f4ffa430e8aa0146a52022370ade352e527.
Its actual Gaussian preparation source is
reviews/R21-linear-tree-common-gaussian-candidate.md,
SHA256 99f8a23c98332b6797ee1ecc9f0929d94950cd047acb17bcbea0df9052ff7461.
No pending T94/T95 result is a premise below.

Write r=d+1 and R=r+d=2d+1. The same actual tuple field from D44 is

    W(x)=z h_(kappa a)(x-U),
    z=(n)_j C_I product_b e(U+Z_(I_b)),   tau/n<=a<=tau,
    |z|<=n^j ||e||inf^j,   E W=D^j S_tau(g)[e^j].             (1.1)

When n<j, W=0 without a query. Preparing the tree, residuals, known
coefficient C_I and then z costs C(1+G)n, with at most j queries on
every seed. Fixed-time population moments obey

    E n^k <= exp(lambda tau(B^k-1)),  integer k>=1.           (1.2)

## 2. The stronger Sobolev moment is available

For any fixed integer R>=1 set theta=4*pi^2*kappa*tau,
b0=1+sqrt(pi/theta), b1=1+sqrt(2*pi/theta), and

    H_R=(d+1)^(R-1)[b0^d+d*(2R/theta)^R*b1*b0^(d-1)].

The inequalities

    sum_m exp(-theta m^2/n)<=b0 sqrt(n),
    m^(2R)exp(-theta m^2/n)
      <=(2Rn/theta)^R exp(-theta m^2/(2n)),
    (1+sum_l nu_l^2)^R <=(d+1)^(R-1)(1+sum_l |nu_l|^(2R))

prove by finite products and nonnegative summation that

    ||h_(kappa a)||_(H^R)^2<=H_R n^(R+d),
    E||W||_(H^R)^2<=V_(j,R)||e||inf^(2j),
    V_(j,R)=H_R exp(lambda tau(B^(2j+R+d)-1)).                 (2.1)

The first estimate uses a>=tau/n and n>=1, and deliberately rounds
R+d/2 up to R+d. The pathwise spatial shift does not change the norm.
The same measurable finite-tree construction gives a genuine H^R-valued
square-integrable field. This is the D43 envelope argument at the displayed
larger fixed Sobolev index; no analytic regularity or exponential moment of
the tree population is needed.

## 3. An exactly sampled positive lattice distribution

For one coordinate draw U0 uniform on (0,1), let m=floor(1/U0)-1,
and independently choose a fair sign when m>=1. Return 0 when m=0.
If an implementation of the ideal uniform primitive includes endpoints,
replace an endpoint by 1/2; this changes a null set without retries.
The probability of m is the length of (1/(m+2),1/(m+1)], namely
1/[(m+1)(m+2)]. Thus the signed coordinate law is exactly

    q1(0)=1/2,
    q1(k)=1/[2(|k|+1)(|k|+2)] for k!=0.

It sums to one by telescoping. Draw d independent coordinates, independently
of the complete tree randomness, and write nu for the resulting vector and
q(nu)=product_l q1(nu_l). This law is symmetric, positive at every lattice
point, and sampled with O(d) permitted operations. Its probability can be
evaluated by the displayed rational formula in O(d) operations. In particular

    1/q(nu)<=6^d product_l(1+nu_l^2)
             <=6^d(1+|nu|^2)^d.                             (3.1)

For |k|=m>=1 the first scalar inequality is
2(m+1)(m+2)<=6(1+m^2), equivalent to 2(2m-1)(m-1)>=0;
for k=0 it is 2<=6. The potentially huge but finite index is consistent
with the inherited ideal-word model. It is not a machine-word promise.

## 4. Exact real sparse field and its second moment

For any fixed real field w in H^R with complex Fourier coefficients
w_hat(nu), define a real one-mode function

    A_nu(w)(x)=Re[w_hat(nu) exp(2*pi*i*nu.x)]/q(nu).          (4.1)

For a box cutoff N>=0 let Y_N=A_nu(W) if |nu|inf<=N, and zero otherwise.
The frequency draw is independent of W. Each realized output has either
one constant coefficient or one real cosine/sine pair. For nu!=0 its squared
H^r norm is (1+|nu|^2)^r |W_hat(nu)|^2/[2q(nu)^2]; for nu=0 it is
|W_hat(0)|^2/q(0)^2. Consequently, conditionally on W,

    E_nu ||Y_N||_(H^r)^2
      <=sum_nu (1+|nu|^2)^r |W_hat(nu)|^2/q(nu)
      <=6^d ||W||_(H^R)^2.                                 (4.2)

Nonnegative Tonelli and (2.1) give integrability. For a finite cutoff,
summing (4.1) against q gives P_N W exactly, since w is real and its
conjugate frequencies pair. Thus the actual Bochner identities are

    E Y_N=P_N D^j S_tau(g)[e^j],
    E||Y_N||_(H^r)^2<=Vtilde_j ||e||inf^(2j),
    Vtilde_j=6^d V_(j,R),                                  (4.3)

uniformly in N. The untruncated one-mode field also satisfies these claims
with P_N removed: (4.2) proves Bochner integrability, and the expectation's
Fourier coordinates are those of W, which identify the H^r element.

For (1.1), choose the representative nu_star of {nu,-nu} whose first
nonzero coordinate is positive. A nonzero in-box output has coefficients

    cosine: z exp(-2*pi^2*kappa*a*|nu|^2)
                    cos(2*pi*nu_star.U)/q(nu),
    sine:   z exp(-2*pi^2*kappa*a*|nu|^2)
                    sin(2*pi*nu_star.U)/q(nu).               (4.4)

The constant output is z/q(0). There is NO factor two in a single nonzero
sample: both possible draws nu_star and -nu_star contribute, each with
probability q(nu_star). Their mean supplies the factor two in the ordinary
real Fourier array. The sine sign is positive. All coefficient/location
correlations from the actual W are retained.

## 5. Finite program, hard queries and counted accumulation

For a trial, draw nu first. If it is outside the requested box, return a
sparse zero record without generating a tree or querying v. This is exact
importance sampling with zeros, not conditioning on acceptance. Otherwise
run precisely D44 and compute only (4.4) or the constant. The law equals
Y_N constructed above by imagining an independent unobserved W even on
outside-box trials. n<j still returns zero. Null chronological nontermination
has zero acquisitions because preparation precedes them. The all-seed cap
is j; halting is almost sure for every continuous input.

With fixed d,j,B, expected work per trial is at most
C[1+(1+G)E n], independently of N. Both stochastic components are explicitly
sampled with permitted primitives. No Fourier-coefficient oracle is used:
the one coefficient comes from the actual tree's z,a,U formula.

To average M>=1 independent trials into a finite dense real output with
K=(2N+1)^d entries, initialize K zeros once. Use a fixed box-to-linear index
and an explicitly canonical pair convention. Each nonzero trial changes at
most two entries, each zero trial changes none; scale all entries by 1/M at
the end. Indexing in fixed dimension costs O(d) ideal operations. Therefore

    expected total work<=C[M(1+G)+K],
    total queries<=jM on every seed,
    E||M^-1 sum_b Y_(N,b)-P_N D^jS_tau(g)[e^j]||_(H^r)^2
                       <=Vtilde_j ||e||inf^(2j)/M.           (5.1)

Storage is K plus one live finite tree, rather than a dense output per trial.
The displayed work includes draws, arithmetic, g evaluation, acquisitions,
coefficient creation, array accesses and final dense serialization. It does
not remove the unavoidable O(K) cost when a dense array is requested.

## 6. Meaning, limits, attribution, and next gate

This improves the arithmetic dependence on K in this specified derivative
averaging subroutine from C M(1+G+K) to C[M(1+G)+K]. The moment constant
changes from V_j to Vtilde_j and can be much worse. No finite-parameter speed
or variance dominance is asserted. The sparse law is not the original field
law, although its projected mean is the same. Its independent randomness
must be included in risk calculations.

In the existing long-time construction K is polynomial in T. Substitution
of (4.3) preserves the fixed-time derivative-risk interface with different
public constants. It does not by itself remove the polynomial paid cost of
computing the known base profile and later continuation. Thus this note
does not establish exact Theta total work or improve the accepted exponent.
It proves no fractional solver, variable diffusion theorem, or bit complexity.
T95's analogous higher-Sobolev envelope could support the same abstract
argument if separately accepted, but is not imported here.

Importance weighting and randomly sampled Fourier features are established
techniques. A bounded primary attribution check read Section1.1, equations
(1.1)--(1.3), of Yao--Erichson--Lopes, *Error Estimation for Random Fourier
Features*, AISTATS2023: https://proceedings.mlr.press/v206/yao23a/yao23a.pdf.
That paper approximates kernels; its results are not a theorem about our
nonlinear derivative field or scalar-query model. The direct proof above
supplies that connection. No invention of Fourier sampling or global priority
is asserted.

The exact bounded searches were `random Fourier series unbiased Hilbert
valued estimator importance sampling coordinates randomized approximation`,
`Maurey empirical method Hilbert space random sampling Fourier coefficients
approximation Barron 1993`, and `Barron Universal approximation bounds
superpositions sigmoidal function 1993 pdf stat yale`. Barron's author PDF
returned502; a Wisconsin-hosted primary-paper copy opened but exposed no
text, and screenshot calls supplied no model-visible images. No proof from
that unread text is claimed. Secondary snippets were not theorem evidence.

The root derived Sections2--5 and checked the zero mode, conjugate pair,
probability normalization, and q-tail bound analytically. There has been no
Lean translation, code execution, numerical falsification, unknown-input
acquisition, or independent audit of this candidate. Frozen E4 and E5 are
unchanged. Independent mathematical review and a separate fixed formal
contract would precede any new sampler experiment.
