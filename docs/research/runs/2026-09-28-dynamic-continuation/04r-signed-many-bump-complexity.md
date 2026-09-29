# D25: a larger query exponent on the sign-changing class

Conventional status: accepted after T50 and independent T53. The result
concerns worst-case expected query cost on exactly D22's fixed class and
oracle. It does not strengthen D22's common-baseline quantifier. No signed
matching upper bound, priority claim, Lean certificate or numerical evidence
is asserted here.

## Theorem and quantifiers

Fix integer s>=1, dimension 1<=d<=4s and a point x* on the unit-volume
torus. Let F_signed consist of smooth periodic v with ||v||_infinity<=1/2,
all partial derivatives through total order s bounded by1, and both signs.
The PDE is u_t=Delta u/2+u-u^3.

An admissible algorithm knows the PDE, class and horizon but receives only
opaque exact initial-value point queries. It may use input-independent
randomness, adaptive locations and stopping, and biased or unbounded real
outputs. All input-dependent evaluations count; no formula, mean,
derivative or evolved-value oracle is given. Its rules are measurable and
it halts almost surely on the promised class.

There are C>0,T0, depending on the fixed parameters, such that for every
T>=T0 and every admissible algorithm with

    sup_(v in F_signed) E|H_T(v)-S_Tv(x*)|^2 <=1/16,

one has

    sup_(v in F_signed) E Q_T(v) >=C exp(2dT/(2s+d)).

More precisely, a public finite prior, independent of the algorithm,
has expected query cost at least that amount. An expensive member thus
exists but may depend on both T and the algorithm. The theorem does not
specify one baseline that is expensive for all algorithms, and does not
make a fixed-profile claim. The critical d=4s case uses a separately chosen
smaller bump amplitude. No assertion at this exponent is made for d>4s.

## Actual nonlinear PDE estimate

For any smooth datum with A=||v||_infinity<=1 and m=integral v, let ell_m
be the scalar Allen–Cahn flow. Set

    nu=2*pi^2-1,
    h=exp(-4*pi^2), H_d=((1+h)/(1-h))^(d/2),
    C_d=e*(H_d+3/(nu+1)).

For T>=1 the proved estimate is

    ||S_Tv-ell_m(T)||_infinity
      <=(5/(2nu))*exp(T)*A^3+C_d*A*exp(-nu*(T-1)).

Indeed, for b(t)=integral u and w=u-b, the unit-torus Poincare inequality
and monotonicity of the cube give ||w(t)||_2<=A exp(-nu*t). The mean has
the exact correction

    b'=b-b^3-R, R=3b integral w^2+integral w^3,
    |R|<=5A^3 exp((1-2nu)t).

Variation of constants gives the first error term. One-unit heat smoothing
of w, retaining its scalar forcing integral(u^2+ub+b^2)w, gives the second.
Thus the proof controls nonlinear mean drift instead of assuming that the
initial mean determines the PDE. The spectral gap exceeds the unstable
growth rate because this is the unit torus; changing the domain scale
requires another analysis.

## Hard family and the dimensional restriction

Fix the smooth interior bump psi with mass I>0 and derivative bound D from
D22. Put q=s+d/2, a=1/(8D) for d<4s, and

    R_T=(aI exp(T))^(1/q), k=2 floor(R_T/2), K=k^d,
    b_j=a*k^(-s)*psi(kx-j),
    r=2 ceil(sqrt(K)/2).

For large T, k and K are even, K>=2048, and sqrt(K)<=r<=2sqrt(K)<=K/4.
Choose uniformly among sign vectors with sum+r or sum-r, giving the two
layers equal prior weight. Every function sum_j sigma_j b_j is smooth,
belongs to the same fixed F_signed, and genuinely takes both signs.
Their means are +/-aI*k^(-s-d)*r, so exp(T)*|m|>=1 and the corresponding
scalar values have magnitude at least1/sqrt(2).

The cubic PDE error scales as

    exp(T)*A^3=O(exp(-(4s-d)*T/(2s+d))).

For d<4s it tends to zero; the spatial remainder does too. T50 gives a
fully explicit T0 making their sum at most1/8 for every T>=T0 and every
arrangement in either layer. The actual targets then lie above1/2 on the
positive layer and below-1/2 on the negative layer.

At d=4s choose instead

    a=min(1/(8D),sqrt(nu*I/(40*2^(3s)))).

The cubic error is then at most1/16 uniformly in T and the other error
eventually at most1/16, preserving the same separation. For d>4s the
current bound grows at this scale; this is an unresolved proof limitation,
not a counterexample to the stronger rate.

## Information and expected cost

An exact query reveals at most one cell sign. Granting the sign even when
the point lies at a zero of its bump gives a stronger oracle. For a test
using at most n=floor(K/1024) queries, pad the observed distinct signs to n.
Exchangeability of each layer gives a without-replacement urn law for
every adaptively selected unused cell.

For all histories before n, the negative-layer next-positive probability
lies in[1/4,3/4], and the two conditional probabilities differ by at most
2r/K. Their Bernoulli KL is at most256/(3K), so the seed-and-transcript KL
is at most1/12. Pinsker and data processing give total variation<1/4 and
equal-prior test error at least3/8. These are fixed spatial functions under
a finite prior, not independent noisy coin responses.

An estimator with the stated MSE gives a sign test with error at most1/4.
If its prior-average expected cost is qbar, truncating before query n+1
increases error by at most qbar/n. Hence

    qbar>=n/8>=K/16384
      >=2^(-d-14)*(aI)^(d/q)*exp(2dT/(2s+d)).

This derives the expected-cost statement even with rare expensive runs.
The full proof handles finite-prior null sets and measurable common seeds.

## Evidence and limits

Detailed proof/constants: reviews/T50-signed-many-bump-lower-bound.md,
SHA256 45e56dc4c5bb656cc3f3407f4e7627e772e13b013a8ca9837ffebe8f79806151.
Independent audit: reviews/T53-signed-many-bump-independent-audit.md,
SHA256 0c09832487dd497422e8078fadd8814957da85f1bd452d333b475a4757f11cb4.

The Hamming-layer problem and randomized smooth-integration exponent have
explicit classical predecessors identified in those reports. The accepted
contribution here is the stated local proof, not a novelty determination.
D24's matching rate applies to the different nonnegative class. T42/T43's
no-hit formalization does not certify this new urn/KL argument. A separate
formal target is still needed before any D25 numerical work is selected.
