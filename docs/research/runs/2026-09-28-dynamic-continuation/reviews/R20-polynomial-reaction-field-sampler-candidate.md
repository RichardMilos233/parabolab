# R20: a field sampler for invariant-interval polynomial reactions

Date: 2026-09-29. Root conventional candidate, not independently audited,
not promoted to the claim ledger, and not a new full complexity theorem.
This extends the specific fixed-time sampling gate of T87. The general
voting representation itself is established prior work.

## 1. The precise scope

Let f be a fixed real polynomial with f(-1)>=0 and f(1)<=0. On the unit
d-dimensional torus, d>=1, fix kappa>0 and a positive finite burn-in time
tau. Let S_t denote the actual mild solution of

    u_t=(kappa/2) Delta u+f(u).

The invariant interval is [-1,1]. Constants below may depend on the
entire known polynomial, d, kappa and tau. No uniform bound as these
parameters vary is asserted. In particular this does not treat a
non-polynomial reaction, a gradient reaction, a variable diffusion,
a system, or a polynomial without an invariant bounded interval.

For a known evaluable g with ||g||inf<1 and an unknown residual e=v-g,
we construct, for every fixed j>=1, an actual H^(d+1)-valued random
element W_j with

    E W_j = D^j S_tau(g)[e,...,e],
    E ||W_j||_(d+1)^2 <= V_j ||e||inf^(2j).            (1.1)

Only at most j point values of v are acquired for each sample, on
every seed path. For any requested box frequency cutoff N, the actual
finite real coefficients of P_N W_j can be computed with expected
paid work C(1+G+(2N+1)^d), where G bounds one evaluation of known g.
There is no unknown-function integral, derivative, or PDE oracle.

The actual fixed-time map from the open unit ball of C(X) to H^(d+1)
is infinitely Frechet differentiable, with a corresponding explicit
Taylor remainder. This is the sampling gate only. It does not supply
the polynomial-reaction version of the paid known-profile solver,
the final long-horizon algorithm, or a matching lower bound.

## 2. A bounded multilinear parent rule

Choose an integer B>=max(2,deg(f)). Write the ordinary known polynomial
in the degree-B Bernstein basis:

    f(2t-1)=sum_(i=0)^B F_i binom(B,i) t^i(1-t)^(B-i).

This is a finite linear change of coordinates in a polynomial space.
For example, if f(2t-1)=sum_l a_l t^l, then

    F_i=sum_(l=0)^i a_l binom(i,l)/binom(B,l).

To check the formula, expand the identity
sum_i binom(i,l)binom(B,i)t^i(1-t)^(B-i)=binom(B,l)t^l
by choosing l distinguished elements and summing the remaining
binomial expansion. All constants are obtainable by finitely many
public arithmetic operations. Put

    Fmax=max_i |F_i|, lambda=1+B Fmax/2,
    c_i=2i/B-1+F_i/lambda.                            (2.1)

The endpoints obey F_0=f(-1)>=0 and F_B=f(1)<=0. Their increments
have magnitude less than 2/B<=1, so c_0,c_B are in [-1,1]. Each
interior number 2i/B-1 has distance at least 2/B from both endpoints;
|F_i/lambda|<2/B implies c_i in [-1,1] there as well.

For y=(y_1,...,y_B) define the symmetric multiaffine polynomial

    M(y)=sum_(A subset {1,...,B}) c_(|A|)
               product_(i in A) (1+y_i)/2
               product_(i notin A) (1-y_i)/2.         (2.2)

On the cube the product weights are nonnegative and sum to one.
Hence |M|<=1. On the diagonal the binomial identity and the mean
of a binomial count give

    M(z,...,z)=z+f(z)/lambda.                         (2.3)

Thus rate-lambda, B-ary branching with parent rule M has exactly
the required reaction f. Equation (2.2) costs a fixed C_B operations
per parent; no optimal dependence on polynomial degree is claimed.
For Fmax=0 the same definitions give lambda=1 and the arithmetic
average rule, consistently representing the heat equation.

This construction is a signed-coordinate adaptation of the classical
Bernstein/voting construction; it is not claimed as a new representation.

## 3. Actual finite-time branching law and PDE identification

Each particle lives for an independent rate-lambda exponential time
and is replaced by B children. During its life it moves as Brownian
motion with coordinate variance kappa per unit time. Stop the genealogy
at tau. If n(t) is the active population, it jumps from n to n+B-1
at rate lambda n. For every integer p>=1 and n>=1,

    n[(n+B-1)^p-n^p] <= (B^p-1)n^p.                 (3.1)

Indeed expand the left side in powers of B-1; every term n^(p-l+1)
with l>=1 is at most n^p, and the binomial coefficients sum to B^p-1.
Stop at the first population at least L. Dynkin's formula and Gronwall
give a bound exp(lambda(B^p-1)tau) for the p-th stopped moment,
uniformly in L. The p=1 bound makes the probability of reaching L
by tau at most exp(lambda(B-1)tau)/L. Explosion by tau therefore
has probability zero. Fatou then gives

    E n(tau)^p <= exp(lambda tau (B^p-1)).            (3.2)

The finite tree has n leaves and (B n-1)/(B-1)<=2n total lifetime
segments. Propagating leaf values through M produces a multiaffine
leaf polynomial P_tree bounded by one on [-1,1]^n. Both properties
follow by induction: child subtrees have disjoint leaf labels, and
each parent is separately affine in each child value.

For continuous q in [-1,1], its bounded tree expectation F_t(q)(x)
obeys the first-branch renewal equation

    F_t=e^(-lambda t) P_(kappa t) q
        +integral_0^t lambda e^(-lambda a) P_(kappa a)
                   [M(F_(t-a),...,F_(t-a))] da.       (3.3)

Here P_b denotes heat convolution with covariance b. Conditional
independence of the B descendant trees and multiaffinity justify
expectation through M; no nonlinear expectation interchange is assumed.
The integrands are bounded, so conditioning and Fubini are legitimate.
The killed-heat variation-of-constants identity converts (3.3), using
(2.3), to the mild equation for f. Conversely that mild equation yields
(3.3). Polynomial local Lipschitz continuity and the invariant interval
give uniqueness of the bounded solution, so F_t=S_t q. Existence
also follows by the usual local contraction and interval comparison;
boundedness prevents finite-time continuation failure.

## 4. Common Gaussian smoothing for every arity

Fix a finite genealogy with n leaves. For each lifetime segment a,
including the initial ancestor and the final truncated segments, let
ell_a be its length and b_a its descendant-leaf indicator. Conditional
on the genealogy, one coordinate of leaf displacements has covariance
kappa C, with

    C=sum_a ell_a b_a b_a^t.

At almost every time the alive particles partition all n terminal
labels. For every z in R^n, finite Cauchy--Schwarz on that partition
implies

    z^t C z >= (tau/n)(sum_i z_i)^2.                 (4.1)

Only the number of blocks being at most n is used; ternary branching
is unnecessary. Therefore R=C-(tau/n)11^t is positive semidefinite.
Sample independent physical coordinates of a residual Gaussian array
Z with covariance kappa R, and an independent common Gaussian of
covariance (kappa tau/n)I_d. Their sum has exactly the original joint
leaf law, by addition of Gaussian covariances. This includes n=1,
zero-time segments and singular residual covariances.

Let h_b be the torus heat density with covariance b. For an independent
uniform torus point U, the actual random field

    h_(kappa tau/n)(.-U) P_tree(q(U+Z_1),...,q(U+Z_n)) (4.2)

has expectation S_tau q. The common Gaussian has been integrated
through the complete nonlinear polynomial. This follows by heat
convolution of the function u -> P_tree(q(u+Z_i)); the density is even.
The residual covariance must change as above. Damping old Fourier
weights while retaining old leaf positions would give another law.

Set r=d+1. The Fourier norm from T87 and its elementary Gaussian-sum
bound, with kappa replaced by kappa tau, give a public finite C_h such
that

    ||h_(kappa tau/n)(.-U)||_r^2 <= C_h n^(r+d),
    ||w||inf <= E_d ||w||_r,
    E_d^2=1+4d 3^(d-1).                             (4.3)

The norm is translation invariant; no independence of U and the
scalar polynomial value is required for the bound. This uses a fixed
separable real Hilbert space, independent of the requested cutoff.

## 5. Derivatives, tuple queries and finite computation

For any j distinct leaf labels, the mixed partial of P_tree is its
signed average over the 2^j selected corner values, divided by 2^j.
It consequently has absolute value at most one. Repeated-label
partials vanish. The j-th derivative of (4.2) at q in directions
e_1,...,e_j is the ordered-injection sum of these partials times
product_a e_a(U+Z_(I_a)), multiplied by the same heat profile.

With n=n(tau), define

    V_j=C_h exp(lambda tau (B^(2j+r+d)-1)), j>=0.

Equations (3.2) and (4.3) bound the expected squared operator envelope
n^(2j)||h_(kappa tau/n)||_r^2 by V_j. All relevant field-valued
integrals are actual Bochner integrals. On each finite-tree event,
the finite arithmetic construction is Borel and U -> h_b(.-U) is
continuous in H^r. The countable union over finite shapes is strongly
measurable. Expectations of multilinear expressions are taken per
fixed tuple of directions, avoiding an operator-valued measurability
claim in a possibly nonseparable space.

Finite-polynomial Taylor's theorem on a segment inside the open unit
ball bounds the derivative-order-j first-order remainder by

    (1/2)n^(j+2)||h_(kappa tau/n)||_r ||q-q0||inf^2.

Its expectation is finite by V_(j+2). Induction proves that S_tau
maps the open unit ball of C(X) infinitely differentiably into H^r.
In particular, if the segment g+t e stays there, then

    ||S_tau(g+e)-sum_(j=0)^(J-1) D^jS_tau(g)[e^j]/j!||_r
                      <=sqrt(V_J)||e||inf^J/J!.       (5.1)

For a j-th order sample, first prepare the entire genealogy, residual
Gaussian array, U, a uniform ordered injection I of j labels, and the
selected partial C_I using only known g at all leaf locations. If
n<j return zero without any acquisition. Otherwise query v at only
the selected j locations and set

    z=(n)_j C_I product_(a=1)^j (v-g)(U+Z_(I_a)),
    W_j=h_(kappa tau/n)(.-U) z.                       (5.2)

The uniform injection cancels (n)_j in expectation and recovers the
ordered derivative sum. The bound |C_I|<=1 proves (1.1), with all
correlations between coefficients and between locations retained.
Even repeated spatial locations count as separate queries.

For one representative nu from each pair {nu,-nu}, P_N W_j has
constant coefficient z and real coefficients

    2z exp(-2pi^2 kappa tau |nu|^2/n) cos(2pi nu.U),
    2z exp(-2pi^2 kappa tau |nu|^2/n) sin(2pi nu.U).

The sine sign is positive. This is a finite formula in the same
charged exp/sin/cos ideal primitives as T87; no full heat series is
evaluated. The covariance matrix can be built and factored by the
exact positive-semidefinite Cholesky procedure of T87 in O(n^3).
Zero pivots yield zero columns because PSD forces their remaining
off-diagonal entries to vanish. No division by a zero pivot is made.

At most 2^j complete parent passes compute the corner partial. With
B,j,d fixed, the actual cost is bounded by

    C_(B,j,d)[n^3+(1+G)n+(2N+1)^d].                 (5.3)

Equation (3.2) gives the claimed finite expected work. All preparations
precede unknown acquisition; a null nonterminating preparation adds
zero queries. Thus the hard j-query cap is valid even on exceptional
seeds, without truncating the tree distribution. An a.s. finite seed
space and finite ideal program suffice for the output law. Infinite
heat-valued W_j is the analytical random variable; the actual returned
sample is always its finite coefficient array.

Independent copies now give actual mean-square error V_j delta^(2j)/M
in H^r. Fourier projection is contractive in that norm, real weighted
coordinate clipping about the true coefficient box cannot increase
error, and the embedding in (4.3) controls the spatial supremum.
These are the statistical gates already isolated in fixed05m. They
do not require independence of Fourier coordinates.

## 6. Concrete new reaction and the remaining long-time gates

Take f(u)=u-u^5, B=5. Its degree-five Bernstein coefficients in the
signed-coordinate convention are

    (F_0,...,F_5)=(0,-8/5,4/5,-4/5,8/5,0).

Equation (2.1) gives lambda=5 and parent corner values

    (c_0,...,c_5)=(-1,-23/25,-1/25,1/25,23/25,1).

Direct substitution into the diagonal Bernstein expression yields
5(M(u,...,u)-u)=u-u^5. It is a bounded five-child rule and therefore
has the sampling gate proved above. This example was derived by exact
algebra here; no implementation or numerical experiment was run.

For this quintic, f'(u)=1-5u^4<=1, f'(0)=1, f is odd, and its positive
scalar flow is

    phi_t(a)=a exp(t)/[1+a^4(exp(4t)-1)]^(1/4).

These identities make the same exponent 2d/(2s+d) a plausible target.
They do NOT prove the minimax extension. Required additional work is:

1. A complete paid known-profile solver and positive-time Fourier tail
   for this polynomial, with explicit constants, output and work.
   The cubic solver cannot merely be cited as if its proof were unchanged.
2. Actual signed lower-prior PDE separation, including time-one
   fluctuations, the mean/nonconstant coupling, scalar signal and all
   adaptive information quantifiers. Oddness alone is not that proof.
3. Review of the full upper/lower same-class composition and then
   corresponding formal and numerical work under separate contracts.

For general invariant-interval f, comparison gives at most exp(L t)
with L=sup_[-1,1] f'. That L need not equal an unstable derivative
f'(a) at a selected equilibrium. Accordingly a general upper exponent
based on max(L,0) is not automatically a matching lower exponent.
Neither the exact all-polynomial exponent nor full universality is
claimed by this candidate.

## 7. Prior work and activity record

The primary [An--Henderson--Ryzhik text](https://arxiv.org/html/2209.03435)
was read at Sections3.2--3.4, including Theorems3.2--3.4 and their
Bernstein/rate construction. It already treats polynomial voting and
credits an earlier O'Dowd thesis; that thesis was not retrieved here.
The bounded cube rule in Section2 is an explicitly rederived signed
adaptation with inward endpoints. No priority is asserted for it.

The primary [Kriechbaum--Ryzhik--Zeitouni abstract](https://arxiv.org/abs/2312.03944)
describes polynomial voting for discrete nonlocal recursions and
tightness/traveling-profile results. Only its abstract and publisher
metadata were inspected; no full theorem or query-complexity import
is made from it.

Bounded search queries used: "branching Brownian motion polynomial
nonlinearity voting Bernstein coefficients reaction diffusion
representation"; "probabilistic representation semilinear PDE arbitrary
polynomial nonlinearity branching bounded voting rule Bernstein";
and the exact title "Voting models and tightness for a family of
recursion equations" plus "arxiv". Search results also included the
original weighted-branching work, posters and unrelated particle
systems; their technical results were not used. This is not an
exhaustive novelty review of the common-Gaussian derivative sampler.

Local dependency: frozen T87 at SHA256
acd788e6ee5564778cd0663be99aab17fb61f22bdfb4b345ccade008f18feff1,
fully read by root. Its independent T90 audit is pending as this
candidate is written. The covariance, moment and derivative argument
above is rederived for general fixed arity; inherited primitive and
Fourier conventions are explicit. Root research backend identity is
not separately exposed. No claimed model switch, Lean run, numerical
test, new input acquisition, protected-source edit, or claim promotion.
