# Sharp point and profile query complexity for every positive diffusivity

Date: 2026-09-29. Accepted conventional synthesis of frozen T87 and
independent T90, with the separately accepted D37 lower. This strengthens
the query conclusion of04y without rewriting that earlier result.
It does not strengthen its paid-work exponential rate to exact order.

## 1. Same problem, stronger query upper

On X=(R/Z)^d with normalized volume consider

    u_t=(kappa/2) Delta u+u-u^3,     u(0)=v.

Fix kappa>0 and integers d,s>=1. The fixed full signed class is

    V={v smooth periodic real: ||v||inf<=1/2,
       max_(|alpha|<=s)||partial^alpha v||inf<=1,
       min v<0<max v}.

There is no common bound on derivatives above s, no common analytic
radius, no positive mean margin, and no restriction to one basin.
The only unknown information is an exact point value v(x). Every
acquisition is charged, including preprocessing and repeated locations.
The allowed rules are measurable, randomized, adaptive and biased if
desired, with an input-independent seed and a.s. halting on each input.

Put q=s+d/2 and gamma=d/q=2d/(2s+d). At the common RMS tolerance1/4,
let Q_point(T) be the infimum of worst-input expected acquisition
counts among point estimators at a fixed prescribed x*. Define
Q_profile(T) analogously for algorithms returning finite explicitly
indexed real Fourier polynomials with loss E||U-S_Tv||inf^2<=1/16.
Auxiliary arithmetic is free for these query quantities. In the paid
work quantities, use exactly the ideal real primitives stated in04y
and T87; every query, arithmetic operation, read/write, comparison,
index operation, listed elementary function, and scalar random draw
is charged. No new function-space oracle is introduced.

**D40: actual fixed-time field sampling.** For a known evaluable g in
the open unit ball of C(X), an unknown residual e=v-g, and fixed j>=1,
there is an actual random field W_j in H^(d+1)(X) such that

    E W_j=D^j S_1^kappa(g)[e,...,e],
    E||W_j||_(d+1)^2<=V_j ||e||inf^(2j).

It uses at most j unknown initial-value queries on every seed path.
For a box cutoff N its actual returned finite real coefficient array
P_NW_j costs at most C_(kappa,d,j)(1+Gg+(2N+1)^d) in expectation,
where Gg is a bound for a known-g lookup. All constants are independent
of N and the residual. The map S_1:C(X)_{||.||inf<1}->H^(d+1) is
genuinely infinitely Frechet differentiable, with derivative and Taylor
remainder bounds obtained from this same field law. This statement
is conventional; fixed05m formalizes a statistical part only.

**D41: strong profile upper with a sharp hard query cap.** For every
prescribed real T>=2, an explicit a.s. halting paid algorithm returns
an indexed real Fourier polynomial U_T with

    sup_(v in V)(E||U_T-S_T^kappa v||inf^2)^(1/2)<=1/8,
    Q_T<=[1+J(J-1)/2]k^d on every seed,
    J=ceil(1+d/(2s)),       k^d<=C exp(gamma T),
    sup_v E Work_T<=C exp(gamma T)(1+T)^A.

The array has at most C(1+T)^(3d^2+9d) entries. Its evaluation at any
specified point has polynomial paid cost and needs no new initial
values. The existing bounded-time patch has deterministic sup error
3/32<1/8 and constant query/work bounds for0<=T<=2.

**D42: exact minimax query order.** For all sufficiently large real T,

    c exp(gamma T)<=Q_point(T)<=C exp(gamma T),
    c exp(gamma T)<=Q_profile(T)<=C exp(gamma T).

The upper has the stronger RMS tolerance1/8, and so qualifies at1/4.
The accepted D37 lower applies at RMS1/4 to all permitted point rules.
Evaluating a returned finite profile at x* gives a point rule at the
same acquisition count, transferring the lower to the profile problem.
This proves both Theta statements with the same fixed class and oracle.

For the paid work quantities, only the already matching exponential
rate is established:

    c exp(gamma T)<=W_point(T),W_profile(T)
                       <=C exp(gamma T)(1+T)^A.

Constants may depend on kappa,d,s and may be very large. These are
neither finite-bit costs nor measured wall-clock performance.

## 2. What removes the polynomial query loss

For a fixed rate-two ternary genealogy stopped at time one, with n
leaves, write its Brownian leaf covariance as kappa C. Each lifetime
segment contributes its length times the outer product of its
descendant indicator. At any time the alive segments partition the
n terminal labels. Cauchy--Schwarz on that partition proves

    C >= 11^t/n.

Thus the original leaf displacements can be expressed in law as a
common N(0,kappa/n) displacement plus residual Gaussian vectors of
covariance kappa(C-11^t/n). T87 constructs those residuals using a
finite guarded semidefinite Cholesky program, including zero pivots.
This costs O(n^3), whose expectation is finite at the fixed burn-in.

Integrate the common Gaussian through the complete nonlinear tree
polynomial, and sample a uniform root location U. The selected tuple
sample becomes the smooth field

    W_j=h_(kappa/n)(.-U) (n)_j C_I
                            product_a (v-g)(U+Z_(I_a)).

All known leaf values and selected residuals use the same translated
array. This modifies the residual law as well as the Fourier weights;
merely damping the old tuple coefficients would not be unbiased.
Distinct-label mixed partials C_I are bounded by one. The actual
Hilbert heat norm is bounded by C n^(r+d), r=d+1, and the finite-time
population has all integer moments. Consequently E||W_j||_r^2 has
a bound independent of the Fourier cutoff. Ordered tuple averaging
gives the genuine PDE derivative; finite-polynomial remainders and
integrable envelopes establish the Hilbert Frechet derivative claim.

Independent complete field samples satisfy the Hilbert mean-square
identity. Fourier modes within one sample are allowed to be correlated.
The fixed embedding ||f||inf<=E_d||f||_r controls the spatial supremum
without a factor equal to the number of retained modes. Projection
onto the Fourier box is a contraction in H^r; clipping the real
coefficients around their true ranges contracts the weighted square
error as well. No type-two property of C(X) is assumed.

## 3. Paid reconstruction and continuation

The known Gevrey interpolant g uses exactly k^d initial grid values,
has ||v-g||inf<=Cint k^-s and fixed paid lookup cost. For each
j=1,...,J-1 take M=k^d independent derivative samples. The j-th
averaged Hilbert error is at most C k^(-js-d/2), and the J-th Taylor
remainder is at most C k^(-Js). Since Js>=q and j>=1, the sum is
at most C k^-q. All powers concern the actual residual; no derivative
of v above the promised order is acquired or assumed bounded.

For S=T-1 and epsilon=exp(-S)/(16*25), choose N=O(1+T), so the actual
time-one solution's omitted Fourier tail is at most epsilon/2.
The paid base solve approximates S_1 g more accurately than epsilon
by the explicit factor sqrt(K)(1+dN^2)^(r/2), K=(2N+1)^d. This costs
only polynomial additional work, because precision enters that
solver logarithmically. It does not cost additional unknown queries.

Choosing k^q>=4E_d Cstar/epsilon now requires no K factor. Hence
k^d<=C exp(gamma T). Field averaging, deterministic Taylor/base
errors and real-coordinate clipping give strong time-one RMS<=epsilon.
The fixed saturation has Lipschitz constant25, agrees with the true
time-one state and yields a uniformly bounded known Gevrey profile.
Actual parabolic comparison amplifies error by at most exp(S).
The final paid known-profile solve contributes at most exp(-T)/16.
The total strong RMS is at most1/16+exp(-T)/16<=1/8.

Every acquired original value is either a coarse-grid value or a
selected j-tuple value. All retained frequencies share the tuple.
The preparatory tree/covariance/partial computation precedes those
queries, so a null nonterminating preparation cannot break the hard
cap. Finite tree moments and finite public solver loops give a.s.
halting and the expected work bound. Measurability and the finite
output contract are checked explicitly in T90.

## 4. Evidence and limits

Root read the full788-line frozen T87 candidate and814-line independent
T90 audit, which supplies14 checked lemmas and requires no material
repair. Six source hashes and all342 protected initial-file hashes
were verified. See reviews/T90-root-correspondence.json for the locks
and same-class/risk/oracle checks. D37's lower remains the separately
accepted T82/T83 result; it was not silently redefined here.

The theorem fixes kappa>0 before letting T increase. It is not uniform
as kappa tends to zero. The point problem at kappa=0 has a one-query
scalar solution; this does not mean an entire unknown profile can
be reconstructed from one query. The guarantees concern each chosen
horizon, not simultaneous pathwise accuracy for all times.

R18 records classical residual integration and Hilbert/Banach-valued
Monte Carlo precedents. The bounded voting representation is also
classical. The precise combined theorem's originality and significance
remain unresolved. A successful internal proof/audit is not an award
judgment or a substitute for external mathematical review.

T86's actual finite-slice conditioning and T89's actual Hilbert risk
formalizations are being completed separately. Even completed versions
of those gates would leave Gaussian genealogy, actual PDE, Fourier
identification, interpolation, solver, and full adaptive/stopping
correspondence outside end-to-end Lean coverage. No new numerical
experiment or unknown-input acquisition accompanies D40--D42. R20
and R21 remain separate unaudited extension/implementation candidates;
neither is needed for this accepted theorem.
