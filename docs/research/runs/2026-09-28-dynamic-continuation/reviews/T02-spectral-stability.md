# T02 — exact odd-sector gap and long-time projected continuation

Date: 28 September 2026. Status: conventional proof and independent review.
No numerical experiment, implementation, Lean build, or timing measurement
was run for this note. The local raw-tree representation and moment bound
are imported from the separately reviewed preceding run. All statements
below distinguish that input from the new deterministic stability argument.

The proposed spectral constant is correct. For the specified Jacobi profile,
the largest Dirichlet eigenvalue of its linearization on the positive half
period is exactly `−1/7`. The order interval `[αg,g]` is invariant under the
PDE and gives pairwise L2 contraction at rate `μ=(2α²−1)/7`; at `α=9/10`,
`μ=31/350`. This removes exponential-in-horizon amplification on this
restricted class. An additional approximation theorem is still needed for
a concrete learned interface. In particular, an orthogonal finite sine
projection cannot both lie below `g` and approximate it nontrivially from
within the order interval. The robust projection-defect theorem in §5 does
not require that false membership assertion.

## 1. Definitions and precise spaces

Use forward elapsed time and the equation

    ∂t u = (1/2) ∂xx u + u − u³

on the torus of length `L`. All functions and Hilbert spaces are real. Write
Jacobi functions in the **parameter** convention `sn(z|m)`, with

    0 < m < 1,       κ² = 2/(1+m),       A² = 2m/(1+m),
    K = integral_0^(π/2) (1−m sin²θ)^(−1/2) dθ,
    L = 4K/κ,       ℓ = L/2,       I = (0,ℓ),
    g(x) = A sn(κx|m).

The case used in this run is `m=1/20`, so `κ²=40/21` and `A²=2/21`.
NIST DLMF instead denotes the modulus by `k`, so its parameter is `k²=m`.
Its derivative identities and sums of squares give

    s′=cd,       c′=−sd,       d′=−msc,
    c²=1−s²,    d²=1−ms²,

where `s=sn(z|m)`, `c=cn(z|m)`, and `d=dn(z|m)`.
The identities are recorded in [DLMF 22.13, Table 1](https://dlmf.nist.gov/22.13#T1)
and [DLMF 22.6.1](https://dlmf.nist.gov/22.6#E1).
Thus `s″=−(1+m)s+2ms³`, and substitution proves

    (1/2)g″ + g − g³ = 0.                                   (1)

On `0<z<2K`, `s>0` and `d>0`; `s` vanishes at both endpoints.
The real periods and zeros are recorded in
[DLMF 22.4](https://dlmf.nist.gov/22.4). In particular `g` is odd,
`L`-periodic, and positive on `I`.

Let `H` be the closed odd subspace of real `L²(R/(LZ))`, with

    ||w||² = (1/L) integral_0^L w²
           = (2/L) integral_I w²       for odd w.

An odd periodic `H¹` function has traces `w(0)=w(ℓ)=0`: oddness gives the
first trace, and periodicity plus oddness gives `w(ℓ)=−w(−ℓ)=−w(ℓ)`.
Restriction to `I` therefore lies in `H₀¹(I)`. Conversely, odd reflection
of an `H₀¹(I)` function across the endpoints gives an odd periodic `H¹`
function. The same reflection identifies `H²(I)∩H₀¹(I)` with the odd
periodic operator domain. There is no extra Neumann condition.

Half-period sign reversal is an optional further symmetry; it is not
needed for this gap. Translation of the reference is not a free symmetry
inside the chosen odd space: `g′` is even and has nonzero endpoint values,
so its neutral translation mode does not contradict the Dirichlet gap.

## 2. Exact spectral inequality by direct factorization

Define the Dirichlet self-adjoint operator

    L_g = (1/2)Dxx + 1 − 3g²,
    D(L_g) = H²(I) ∩ H₀¹(I).

For `ψ(x)=sn(κx|m)dn(κx|m)`, direct differentiation in `z=κx` gives

    (sd)′  = c(1−2ms²),
    (sd)″ = (−1−4m+6ms²) sd.

Consequently

    (1+m)L_g ψ
      = [Dzz + (1+m) − 6ms²](sd)
      = −3m ψ,
    μ₀ = 3m/(1+m),       L_g ψ = −μ₀ ψ.                     (2)

This is an order-two Lamé equation in the convention of
[DLMF 29.2.1](https://dlmf.nist.gov/29.2#E1), but no Lamé eigenvalue table
is used in the proof. Positivity of `ψ` on `I`, its zero endpoint values,
and smoothness imply `ψ∈D(L_g)`.

For `w∈C_c^∞(I)`, write `w=ψη`. An integration by parts with no boundary
term gives

    integral_I [(1/2)|w′|² + (3g²−1−μ₀)w²]
      = (1/2) integral_I ψ² |η′|² ≥ 0.                       (3)

To see the cancellation explicitly, integrate the cross term in
`|w′|²=ψ²|η′|²+2ψψ′ηη′+|ψ′|²η²`; its non-square contribution becomes
`−ψψ″η²`, which cancels by `(2)`.

The left side of `(3)` is continuous in the `H¹` norm because its
potential is bounded. Density of `C_c^∞(I)` in `H₀¹(I)` therefore proves

    −(1/2)||w′||² + integral_I (1−3g²)w²
      ≤ −μ₀ integral_I w²,       w∈H₀¹(I).                  (4)

Here the unnormalized norm in the first term is the norm over `I`.
Multiplying all terms by `2/L` gives the corresponding normalized odd
periodic inequality. The quotient `w/ψ` need not have an assumed trace;
density proves `(4)` without silently imposing one.

Equality is attained by `w=ψ`, by `(2)`. Thus the largest eigenvalue of
`L_g` on the stated Dirichlet domain is exactly `−μ₀`. Equivalently,
`−L_g` has ground-state eigenvalue `μ₀`. At `m=1/20`, `μ₀=1/7`.
This is not a negative spectral bound on the entire periodic function
space; the odd restriction is essential.

## 3. Invariant interval and nonlinear contraction

For `0<α≤1`, define

    B_α = {v odd and L-periodic : αg≤v≤g on I}.

Inequalities hold almost everywhere for mild data and pointwise for the
smooth interfaces used by the local sampler. On `I`, the lower endpoint
is a stationary subsolution because

    (1/2)(αg)″ + αg − (αg)³ = α(1−α²)g³ ≥ 0;              (5)

`g` is a stationary solution and both endpoints vanish at the boundary.
Scalar parabolic comparison with Dirichlet data shows that the solution
map `S_t` preserves this order interval. Oddness is preserved by
uniqueness because the reaction is odd. Boundedness makes the standard
semilinear evolution global in this class. These standard existence,
comparison, regularization, and integration-by-parts results are analytic
inputs, not newly formalized claims in this note.

Let `u(t)=S_t a` and `v(t)=S_t b`, where `a,b∈B_α`. For `w=u−v`,

    (1/2) d/dt ||w||²
      = −(1/2)||w_x||² + ||w||²
        − (2/L) integral_I (u²+uv+v²)w².                    (6)

On `I`, all three terms in the cubic coefficient are bounded below by
`α²g²`. Apply `(4)` and then `g²≤A²` to obtain

    (1/2) d/dt ||w||²
      ≤ −μ₀||w||² + (2/L) integral_I 3(1−α²)g²w²
      ≤ −μ||w||²,
    μ = μ₀ − 3(1−α²)A²
      = [3m/(1+m)](2α²−1).                                (7)

Hence, whenever `α>1/√2`,

    ||S_t a−S_t b|| ≤ exp(−μt)||a−b||.                      (8)

For the present datum,

    μ = (2α²−1)/7,
    α=9/10  gives  μ=(81/50−1)/7=31/350.                   (9)

The constant `μ₀` is exact for the linearized odd operator. The nonlinear
constant `μ` is a sufficient lower bound obtained by replacing `g²` by
`A²`; no optimal nonlinear contraction rate is asserted.

Taking `b=g` also proves convergence `S_t a→g` in normalized L2. However,
`B_α` alone supplies no global derivative bound for an arbitrary member:
a small-amplitude, high-frequency perturbation can stay between the two
profiles while having a large derivative. A realized learned interface
must separately obey the derivative envelope required by the raw-tree
moment theorem. Neither comparison nor `(8)` fills that gap.

## 4. Favorable orthogonal-projection theorem and its obstruction

Let `V⊂H` be a `d`-dimensional space of smooth odd periodic functions,
`P:H→V` its L2 orthogonal projector, and `C⊂V` a nonempty closed convex
set. Assume every `v∈C` belongs to `B_α` and satisfies all local terminal
envelopes. Let `Π_C` be the exact Hilbert metric projector. This says the
**range** lies in the order interval; it does not assert that `P` or
`Π_C` is a monotone map for the pointwise partial order.

Fix an orthonormal basis `e_1,...,e_d` of `V`. Let `u_j=S_(h_j)u_(j−1)`
be the deterministic target, starting in `B_α`. At each slab, condition on
the sigma field `F_(j−1)` containing all preceding draws. The stored
interface `v_(j−1)` is then fixed. Draw `N_j` independent fresh root
locations, uniformly on `[0,L)`, and independent fresh local trees. The
required local sampling input is

    E[H_j(v,x)] = S_(h_j)v(x),
    E[H_j(v,x)²] ≤ M                     uniformly in x,v.   (10)

The preceding run supplies `(10)` for its original rate-two raw
derivative-coded sampler, `h_j≤2/25`, `M=1/4`, and smooth terminals with
`|v|≤2/5`, `|v′|≤1/2`. Its stochastic proof is not repeated here.
Initialize with `v_0=u_0` if that known input is admissible; the first
input need not lie in `C`. Subsequent inputs are stored projections.

Define the vector, identified with its element of `V`,

    Z_j = (1/N_j) sum_i H_(j,i) sum_(k=1)^d e_k(X_i)e_k,
    v_j = Π_C Z_j.

With `f_j=S_(h_j)v_(j−1)`, the conditional moment input and orthonormality
give

    E[Z_j | F_(j−1)] = P f_j,
    E[||Z_j−P f_j||² | F_(j−1)] ≤ ν_j=dM/N_j.              (11)

One tree may serve every basis coefficient. Independence of coordinates
is unnecessary; independence between distinct roots conditional on the
past is required. The variance trace is the sum of coordinate variances.

If the additional target-membership condition `P u_j∈C` holds and
`δ_j=||(I−P)u_j||`, then nonexpansiveness, conditional centering before
projection, Pythagoras, and `(8)` prove

    R_j := E||v_j−u_j||²
      ≤ q_j R_(j−1) + ν_j + δ_j²,
    q_j = exp(−2μh_j).                                     (12)

Indeed the first two steps give
`E[||v_j−Pu_j||² | F_(j−1)] ≤ ||P(f_j−u_j)||²+ν_j`;
adding `δ_j²`, dropping the orthogonal component of `f_j−u_j`, and
using `(8)` proves `(12)`. Clipped/projected samples are not asserted
to be unbiased.

For fixed `h,N` and `δ_j≤δ`, `(12)` yields

    R_J ≤ q^J R_0 + (ν+δ²)(1−q^J)/(1−q).                   (13)

**Membership obstruction.** Suppose `α>0`, `C⊂B_α`, and `Pg∈C`.
On `I`, `r=g−Pg≥0` and `Pg≥αg>0`. Orthogonality implies

    0 = <g−Pg,Pg> = (2/L) integral_I r Pg.

The nonnegative integrand can vanish only when `r=0` almost everywhere.
Thus `g=Pg∈V`. In particular, a finite sine space omitting the nonzero
Jacobi Fourier tail cannot satisfy `Pg∈C`. The earlier stationary box
did contain `Pg`, but its elements were not restricted to `B_α`; it
therefore cannot inherit `(8)` automatically.

For any fixed closed `C⊂B_α` and target trajectory converging to `g`,
the condition `Pu_j∈C` at every time on an unbounded sequence would force
`Pg∈C` by continuity and closedness. Thus merely beginning strictly
below `g` does not repair a claim uniform in the number of slabs. A trial
space containing `g` avoids this particular obstruction, but still needs
a uniform approximation and terminal-envelope argument.

## 5. Robust theorem with the actual distance to the feasible set

Keep the assumptions of §4 through `(11)`, but remove `Pu_j∈C`. Define

    c_j* = Π_C u_j = Π_C(Pu_j),
    β_j  = dist(u_j,C) = ||u_j−c_j*||,
    r_j  = (E||v_j−u_j||²)^(1/2).

The equality of the two projectors follows from Pythagoras because
`C⊂V`. Nonexpansiveness in `V` and conditional centering give

    E[||Π_C Z_j−c_j*||² | F_(j−1)]
      ≤ E[||Z_j−Pu_j||² | F_(j−1)]
      ≤ ||P(f_j−u_j)||² + ν_j
      ≤ q_j ||v_(j−1)−u_(j−1)||² + ν_j.                     (14)

Now apply Minkowski in the Bochner space `L²(Ω;H)` after taking total
expectations:

    r_j ≤ sqrt(q_j r_(j−1)² + ν_j) + β_j.                   (15)

This proves the root researcher's proposed recurrence with coefficient
one on `β_j`. The defect is distance to the **whole feasible set**:

    β_j² = ||(I−P)u_j||² + dist(Pu_j,C)².

A Fourier-tail bound alone is insufficient. Conversely, adding a
separate Fourier tail to `(15)` would count part of the defect twice.
The term `c_j*` is only a proof comparator; the algorithm need not know
the exact intermediate target or compute its projection.

Suppose for now `q_j=q∈(0,1)`, `ν_j≤ν`, and `β_j≤β`. The nonnegative
fixed point of `F(r)=sqrt(qr²+ν)+β` is

    r_* = [β + sqrt(qβ²+(1−q)ν)]/(1−q)
        ≤ β/(1−sqrt(q)) + sqrt(ν/(1−q)).                    (16)

When `β=ν=0`, set `r_*=0`. To verify `(16)`, solve
`(r_*−β)²=qr_*²+ν`; the stated root has `r_*≥β` and hence is not an
extraneous squared-equation solution. The upper bound follows from
`sqrt(a+b)≤sqrt(a)+sqrt(b)`. Since `F` is increasing, its fixed point
is an invariant upper bound, giving

    r_0≤r_*  implies  r_j≤r_* for every j.                 (17)

More generally `F` is `sqrt(q)`-Lipschitz on `[0,∞)`, so

    r_j ≤ r_* + q^(j/2) max(r_0−r_*,0).                    (18)

Retaining the square root in `(15)` matters. Replacing it by
`sqrt(q)r_(j−1)+sqrt(ν)` unnecessarily makes the noise floor scale as
`sqrt(ν)/(1−sqrt(q))`; `(16)` retains the better
`sqrt(ν/(1−q))` scale. No independence between successive projected
interfaces is used, and no variance-projection cross term is silently
discarded.

For a prescribed RMS tolerance `ε>0`, an explicit sufficient budget from
exact initialization is

    sup_j dist(u_j,C) ≤ ε(1−exp(−μh))/2,
    N ≥ 4dM / [ε²(1−exp(−2μh))].                           (19)

The two terms in the upper bound `(16)` are then at most `ε/2`. This
gives `sup_j r_j≤ε` for all slabs, provided the stated set, approximation,
and moment hypotheses hold. Variable final slab lengths can be handled
with `(15)` directly; one must not use a fixed positive contraction
denominator for arbitrarily tiny final steps without changing their
sampling and defect budget.

## 6. What a linear-in-horizon cost claim would require

For equal `h≤2/25`, the number of complete slabs is `J=T/h`. The local
rate-two, at-most-ternary raw tree has expected visited-node bound

    C_h = (3exp(4h)−1)/2,

as in the preceding run. Thus the expected number of tree nodes is at
most `J N C_h`. At fixed `h,μ,M` and a fixed feasible approximation
space, `(19)` has no `T` dependence. The resulting total tree work is
linear in `T`, with `N=O(d ε^(−2))`; constants depend explicitly on the
local time step through `(19)`. A final fractional slab needs the
separate budget noted above, or a fixed-step endpoint can be used.

A polynomial-in-accuracy theorem needs a quantitative approximation
hypothesis. For example, if a constructible family `C_d` satisfies

    C_d ⊂ B_α,       ||v||∞≤2/5, ||v′||∞≤1/2 for all v∈C_d,
    sup_(t≥0) dist(S_t u_0,C_d) ≤ B d^(−s),       s>0,        (20)

with uniform `B`, choose

    d ≥ [2B/(ε(1−exp(−μh)))]^(1/s)

and then use `(19)`. Expected root count is
`O(T ε^(−(2+1/s)))` when `h,μ,M,B,s` are fixed. This is a root-count
bound, not automatically an arithmetic-runtime bound. Basis evaluation,
terminal evaluation at every leaf, orthonormalization, and the feasible
projection must also be computable at polynomial cost, including setup
and tolerances. If terminal/basis evaluation costs `O(d)`, it contributes
another factor `d` to that part of the work. Approximate numerical
projection requires an additional, explicitly budgeted defect; exact
metric projection is an assumption of `(14)`.

Neither `(20)` nor a particular polynomial-time global constraint solver
is proved by the spectral calculation. Global value/order/derivative
constraints must be certified between grid points; sampled inequalities
are not enough. A shrinking feasible set, unknown target-dependent
constraints, or a projector requiring an exact intermediate solution
would not establish the requested implementable continuation theorem.

## 7. Conditional two-dimensional witness and exact budget

The root researcher proposed the following concrete family for separate
regularity analysis by T01. Put `a=A²=2/21` and `z=g²`, and suppose the
true dynamic target has the global representation

    u(t,x)=g(x)R(t,g(x)²),
    9/10≤R(t,z)≤1,   |R_z(t,z)|≤1/35,   |R_zz(t,z)|≤1/50
    for all t≥0 and 0≤z≤a.                                 (21)

These are hypotheses of the present witness. Their endpoint regularity
and all-time validity are not established by assuming a formal quotient
PDE. They are the independent T01 proof obligation.

Define the two-dimensional trial space and its feasible set by

    v_c(x)=g(x)[c_0(1−z/a)+c_1 z/a],
    C={v_c : 9/10≤c_0,c_1≤1, |c_1−c_0|≤a/35}.             (22)

The two displayed basis functions are linearly independent. The
coefficient polygon is compact and convex, so its image `C` is nonempty,
closed and convex. Every interpolated bracket lies between `9/10` and
`1`, and `g∈C` corresponds to `(c_0,c_1)=(1,1)`.

Write `D=c_1−c_0` and `p(z)=c_0+D z/a`. Then

    v_c′=g′[p(z)+2D z/a],
    |v_c′|≤(sqrt(80)/21)(1+2a/35)<1/2.                     (23)

For the strict inequality, `sqrt(80)/21<3/7` and
`1+2a/35=739/735<7/6`. Also `|v_c|≤sqrt(a)<2/5`.
Thus every coefficient vector in `(22)` gives a globally admissible
terminal, and `C⊂B_(9/10)`. These statements concern the entire spatial
domain, independently of how coefficients are learned.

Under `(21)`, the true endpoint values `c_0=R(t,0)`, `c_1=R(t,a)` are
feasible by the mean value theorem. Linear interpolation with the
second-derivative remainder gives a comparator in `C` with

    ||v_c−u(t)||∞≤sqrt(a) a²/400,
    dist(u(t),C)≤sqrt(a) a²/400<1/140000.                   (24)

Indeed the maximal scalar interpolation error is
`a² sup|R_zz|/8=a²/400`. The last strict inequality is exact: it is
equivalent, after squaring positive quantities, to

    a^5=32/4084101 < 1/122500,
    32*122500=3920000 < 4084101.

The endpoint interpolant is a proof comparator, not an oracle used by
the learned algorithm. The actual update is the metric projection in
§5 with dimension `d=2`. In the coefficients of `(22)`, its metric is
the positive-definite L2 Gram matrix, not the ordinary Euclidean metric
unless the basis has first been orthonormalized. In two dimensions the
exact-real projection reduces to minimizing a positive quadratic over a
fixed polygon; checking the unconstrained minimizer and the finitely
many edges is a concrete algorithm. Floating Gram evaluation and
projection error still need their own implementation budget.

Take `h=2/25`, `N=100000`, `M=1/4`, and `μ=31/350`. Then

    ν=dM/N=1/200000,
    x=μh=31/4375,
    1−exp(−x)≥x/(1+x)=31/4406,
    1−exp(−2x)≥2x/(1+2x)=62/4437.                          (25)

The exponential bounds follow from `exp(y)≥1+y`. From `(16)` and `(24)`,
exact initialization therefore gives the uniform endpoint budget

    sup_(J≥0) (E||v_J−u(Jh)||²)^(1/2)
      ≤ 4406/(31*140000) + sqrt(4437/12400000)
      < 1/50.                                             (26)

The last inequality is certified without decimal special-function
evaluation. Its positive residual before taking the square is

    1/50 − 4406/(31*140000) = 41197/2170000 > 0,
    (41197/2170000)² − 4437/12400000
      = 12242059/4708900000000 > 0.                        (27)

This is an all-`J` statement at times `T=J*(2/25)` conditional on `(21)`
and the exact local sampling/projection contract. Arbitrary fractional
final slabs require a separately checked last-step budget. The expected
root count is `100000J=1250000T` at these endpoints; multiply by the
local node bound `C_(2/25)` for the corresponding expected tree-node
bound. This certifies a fixed `0.02` ideal-real-arithmetic tolerance, not
arbitrary accuracy with this fixed two-dimensional space. Finer accuracy
would require a smaller verified approximation defect or a richer set.

## 8. Conditional analytic derivative bound and arbitrary accuracy

This section audits the root researcher's stronger proposed route. It
proves the derivative combinatorics and resulting approximation theorem
**assuming** a global solution `R` that is smooth in `(t,z)` through both
endpoints, solves the following equation there by continuity, and stays
in `[9/10,1]`:

    R_t = a_2(z) R_zz + b(z) R_z + z(R−R³),
    a_2(z)=2z(z²−2z+C_0),
    b(z)=5z²−8z+3C_0,       C_0=80/441.                    (28)

The existence and endpoint-smoothness bridge from the periodic PDE to
`(28)` remains a separate T01 obligation. A formal coordinate calculation
alone does not supply it. The concrete initial datum here is
`u_0=(9/10)g`, equivalently `R(0,z)=9/10`. More generally, the induction
below applies to a fixed exact target started from any
`R_0∈C^∞([0,a])` with

    9/10≤R_0≤1,
    ||R_0^(k)||∞≤(1/70)2^k k! for every integer k≥1.         (28a)

To use the C² feasible approximation in §8.1, additionally require
`||R_0″||∞≤1/50` and the independent propagation statement `(21)`.
The initial class is not assumed to contain every projected polynomial.

Put `r_k=∂z^k R`, `B=1/70`, and

    M_k=B 2^k k!,       k≥1.                               (29)

For `k≥2`, repeated Leibniz differentiation gives the exact equation

    (r_k)_t = a_2 (r_k)_zz + (k a_2′+b)(r_k)_z
              + C_k r_k + E_k r_(k−1) − z N_k − k N_(k−1),
    C_k = k[(6k+4)z−4k−4]+z(1−3R²),
    E_k = k(k−1)(2k+1)+k(1−3R²),
    N_k = 3R sum_(i=1)^(k−1) binom(k,i) r_i r_(k−i)
          + sum_(i,j,l≥1; i+j+l=k) [k!/(i!j!l!)] r_i r_j r_l.
                                                                  (30)

Set `N_1=0`. In `(30)`, the coefficient contribution to `r_(k−1)` from
diffusion and drift is
`12 binom(k,3)+10 binom(k,2)=k(k−1)(2k+1)`. The remaining term comes
from differentiating the factor `z` in `z(R−R³)`. Every derivative in
`N_k` has index strictly smaller than `k`.

Since `0≤z≤a=2/21` and `9/10≤R≤1`,

    C_k≤−D_k,       D_k=k(72k+76)/21,
    0≤E_k≤k(k−1)(2k+1)                    for k≥2.          (31)

The factorization `z²−2z+C_0=(a−z)(2−a−z)` shows that the diffusion
coefficient is nonnegative on `[0,a]` and vanishes at the endpoints.
Its differentiated drift is directed into the interval:

    (k a_2′+b)(0)=(2k+3)C_0>0,
    (k a_2′+b)(a)=−76(2k+1)/441<0.                         (32)

Thus, at an endpoint maximum of `r_k`, the drift contribution is
nonpositive; the diffusion contribution vanishes there. Smoothness up
to the endpoints is what licenses this elementary endpoint maximum
argument without prescribing spurious boundary data for `r_k`.

Suppose `|r_i|≤M_i` has already been established for `1≤i<k`. Each
summand `binom(k,i) M_i M_(k−i)` equals `B²2^k k!`. The ordered positive
triples in `N_k` number `(k−1)(k−2)/2`, and each weighted triple equals
`B³2^k k!`. Consequently the absolute forcing in `(30)`, divided by
`M_k`, is at most

    S_k = (k−1)(2k+1)/2
          + a[3B(k−1)+B²(k−1)(k−2)/2]
          + (3B/2)(k−2)+(B²/4)(k−2)(k−3).                 (33)

The product in the last term is zero at `k=2,3`; no negative-count
combinatorial term is being used. Equation `(33)` agrees with the root
researcher's expression. There is a simple rational margin valid for
every integer `k≥2`: use `a≤1`, `B≤1/10`, and `k≤k²/2` to obtain

    S_k ≤ k² + (9B/2)k + (3B²/4)k²
        ≤ (493/400)k²
        < (24/7)k² ≤ D_k.                                 (34)

For the induction base, differentiation once gives the same inward
drift, damping at least `D_1=148/21`, and the bounded source `R−R³`.
On `[9/10,1]`,

    |R−R³|≤171/1000<1/5<148/735=D_1 M_1.                  (35)

At a first positive contact with the barrier `r_k=M_k`, the parabolic
and drift contributions are nonpositive, while `(31)`–`(35)` make the
remaining time derivative strictly negative. Apply the same argument
to `−r_k`. Induction therefore proves, under the regularity hypotheses
above,

    |∂z^k R(t,z)|≤(1/70)2^k k!    for all k≥1,t≥0,z∈[0,a]. (36)

This is a conventional a priori proof, not evidence that the coordinate
regularity assumption has already been discharged. The sharper curvature
bound `|R_zz|≤1/50` from `(21)` is still needed for the feasible family
below: the `k=2` case of `(36)` alone is weaker.

### 8.1 Explicit feasible polynomial approximation

Assume `(21)` and `(36)`. Let `T_n(t,z)` be the degree-`n` Taylor
polynomial of `R(t,z)` at `z=0`, and put `r=2a=4/21`. Taylor's theorem
applied separately to derivatives of order `j=0,1,2` gives

    e_(n,j) := B 2^j [(n+1)!/(n+1−j)!] r^(n+1−j),
    sup_z |∂z^j R−∂z^j T_n| ≤ e_(n,j).                    (37)

The bounds `e_(n,j)` are explicit; unknown suprema need not be evaluated.
Define

    θ_n = 50 e_(n,2) = (20/7)n(n+1)r^(n−1),
    p_n = (1−θ_n) T_n + θ_n (19/20),       n≥4.             (38)

Then `θ_4=25600/64827<1`, and
`θ_(n+1)/θ_n=r(n+2)/n≤2/7` for `n≥4`; hence `0<θ_n<1`.
The explicit formulas imply

    θ_n≥20e_(n,0),       θ_n≥35e_(n,1),       θ_n=50e_(n,2).

Mixing the true `R` toward `19/20` opens a range margin `θ_n/20`
at both endpoints of `[9/10,1]`. The first bound above absorbs the
Taylor value error in this margin. The other two bounds similarly
absorb derivative errors:

    |p_n′|≤(1−θ_n)(1/35+e_(n,1))≤1/35,
    |p_n″|≤(1−θ_n)(1/50+e_(n,2))≤1/50.

Thus `p_n` belongs to the fixed convex polynomial set

    D_n={p of degree≤n : 9/10≤p≤1, |p′|≤1/35, |p″|≤1/50
                       everywhere on [0,a]},
    C_n={g p(g²) : p∈D_n}.                                 (39)

The set `C_n` is compact and convex in the `(n+1)`-dimensional trial
space spanned by `g,g³,...,g^(2n+1)`. Its entire range lies in the
order interval and obeys the derivative envelope by the same argument
as `(23)`. Projection onto `C_n` is **not** asserted to preserve the
all-derivative bounds `(28a)` or `(36)`. This is unnecessary: the
approximation theorem concerns only the exact target trajectory started
once from the stated `R_0`. Each realized learned polynomial is used
as the next local raw-tree terminal, for which its smoothness and the
global value/first-derivative envelopes suffice. Its exact one-step flow
stays in the order interval by comparison, which is all `(8)` needs.
No fresh analytic-radius or uniform higher-derivative theorem is
invoked on the learned path.

The constructed comparator gives the uniform distance estimate

    sup_(t≥0) dist(u(t),C_n)
      ≤ A(e_(n,0)+θ_n/20)
      ≤ A θ_n/10
      = (2A/7)n(n+1)(4/21)^(n−1)
      ≤ (8/21)^n                  for n≥4.                 (40)

For the last inequality use `n(n+1)≤2^(n+1)` for `n≥4`, proved from
the `n=4` case and a successive ratio at most `3/2<2`, and `A<1/3`.
The Taylor coefficients in this proof are not supplied to the Monte
Carlo algorithm; they certify the distance to the fixed feasible set.

Therefore, with fixed `h` and arbitrary sufficiently small `ε>0`, the
explicit choices

    n ≥ max(4, ceil(log(2/[ε(1−exp(−μh))])/log(21/8))),
    d=n+1,
    N ≥ 4dM/[ε²(1−exp(−2μh))]                             (41)

give a conditional uniform RMS guarantee through `(19)`. Expected root
count at `T=Jh` is `O(T ε^(−2) log(1/ε))` as `ε` tends to zero, with
`h,μ,M` fixed. The claimed order concerns tree roots. It does not yet
include a certified implementation of projection onto the global
polynomial inequalities in `(39)`, its numerical precision, or the
cost of orthonormal coordinates and terminal evaluation. The existence
and uniqueness of metric projection onto `C_n` are proved by convexity
and compactness; they are not a bit-complexity theorem for an optimizer.

## 9. Audit outcome and proof boundary

- **Proved here:** exact odd/Dirichlet gap `(2)`–`(4)`, nonlinear invariant
  interval and contraction conditional only on standard parabolic
  comparison/regularity, the favorable recurrence `(12)`, its membership
  obstruction, the robust recurrence `(15)`, and its uniform budget
  `(16)`–`(19)`. Under the explicit shape hypotheses `(21)`, the
  two-dimensional feasible-set and exact budget deductions `(22)`–`(27)`
  are also proved. Under the additional endpoint smoothness hypotheses
  of `(28)`, the derivative induction `(30)`–`(36)` and the arbitrary-
  accuracy approximation/root-count deductions `(37)`–`(41)` are proved.
- **Imported analytic/stochastic inputs:** Jacobi identities and real
  periods; well-posed semilinear parabolic evolution/comparison; the
  preceding run's uniform local raw-tree mean, moment, and node-cost
  contract. These inputs are named, not inferred from observed runs.
- **Unresolved for a concrete dynamic algorithm:** prove `(21)` (or
  another uniform approximation theorem) and the endpoint-smoothness
  bridge for `(28)`, implement exact or certified approximate projection,
  and account for arithmetic error and basis/projection cost. The
  families `(22)` and `(39)` settle feasibility and derivative/order
  envelopes for these conditional candidates.
- **Formal and numerical status:** this note establishes conventional
  mathematical proofs. It supplies no new Lean declarations or numerical
  experiment evidence. A Python `fractions.Fraction` calculation checked
  the rational margin in `(27)`, the strict inequality in `(24)`, the
  coefficient comparison in `(34)`, and the `θ_4` value in `(38)`; all
  four exact arithmetic checks passed. No general periodic contraction, arbitrary-data theorem,
  universal optimality, or general novelty claim is made.

The defensible long-time conclusion is conditional but useful: local
tree second moments plus a stable feasible interface and a uniform
approximation bound give an RMS error budget independent of the number
of slabs, while total expected work grows linearly with the horizon.
