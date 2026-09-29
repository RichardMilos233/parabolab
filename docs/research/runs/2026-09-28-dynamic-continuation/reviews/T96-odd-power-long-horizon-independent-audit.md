# T96: independent audit of the normalized odd-power long-horizon theorem

Date: 2026-09-29. Conventional mathematical audit of the frozen T94
candidate. This file is the only artifact owned by this task.

**Verdict: PASS. Required mathematical repairs: none.** For every fixed
integer `p>=1`, integers `d,s>=1`, and `kappa>0`, the candidate proves
the stated exact point/profile query order for the actual normalized
reaction `f(u)=u-u^(2p+1)`. Its paid-work conclusion retains the stated
polynomial factor in the horizon. The physical-coefficient transfer
requires exactly the changed class, tolerance, diffusivity and time
specified in T94 Section 11; its unchanged-class counterexample is valid.

This is an independent proof audit, not a promotion of the candidate
to an accepted ledger. It is not a Lean check, numerical test, claim of
practical speed, exhaustive priority review, or award assessment. The
final audit hash is reported outside this file after the final read.

## 1. Frozen target, dependency locks, and exact audited problem

The full 1,266-line target was read, in order, at
`reviews/T94-odd-power-long-horizon-feasibility.md`, SHA256

    2600c29a2823aefd9a69578de113bc511179d97bdfbea7eb3a6861ac28b7e1d9

All nine dependency hashes in its Section 12 match the actual files:

| Source relative to this run | Verified SHA256 |
| --- | --- |
| `reviews/R20-polynomial-reaction-field-sampler-candidate.md` | `b1e42a195c67942066894d04a11c28d7ba2951a6d6730977070e424ac84542b9` |
| `reviews/R20b-continuous-domain-addendum.md` | `6c5e8b158ca269588c4200ca09c82f4ffa430e8aa0146a52022370ade352e527` |
| `reviews/R21-linear-tree-common-gaussian-candidate.md` | `99f8a23c98332b6797ee1ecc9f0929d94950cd047acb17bcbea0df9052ff7461` |
| `04z-all-positive-diffusivity-sharp-queries.md` | `57ef1d86ddba30ce9d54f316b0eb2dc97f407f7aeb4446a66b3103c28e0aedd4` |
| `reviews/T81-fixed-burnin-all-diffusion-upper-proof.md` | `d9b249ed669897df319ca712fc4ad26625fc97e1a9b32b79eacaf497b290bae5` |
| `reviews/T84-all-diffusion-upper-independent-audit.md` | `39cd98fcf957badbe382123bd1960eac7fb99441114c9433bd9ee0ff2d256d7d` |
| `reviews/T82-all-diffusion-prior-lower-proof.md` | `0b331397bbda06ba02381009ce95bfd7656aabb4bd196bac5e67a616b3a2320a` |
| `reviews/T83-all-diffusion-lower-independent-audit.md` | `902ee581593ace7d682fac5351a1288ccef09544d02893fbacc045782e03a56e` |
| `reviews/T87-all-diffusion-sharp-query-feasibility.md` | `acd788e6ee5564778cd0663be99aab17fb61f22bdfb4b345ccade008f18feff1` |

The accepted D43/D44 statement was also read in full at
`04aa-polynomial-fields-and-linear-gaussian-preparation.md`, with
verified SHA256
`433c699d951c74fa6ba19166e159069130e1340a7a319aa0334b0ba4f8a1b8a1`.
Its original R20/R20b and R21 proofs, rather than only its acceptance
label, were read in full. No pending Gaussian formalization or other
current candidate is used as a premise.

The domain is the normalized unit torus, the equation is

    u_t=(kappa/2) Delta u+u-u^D,       D=2p+1,

and the input class is exactly

    V={v smooth, real, periodic: ||v||inf<=1/2,
       max_(|alpha|<=s)||partial^alpha v||inf<=1,
       min v<0<max v}.

There is no bound on derivatives above total order `s`, analytic
radius, mean margin, basin, or number of unstable spatial modes.
The only unknown information is a scalar `v(x)`; preprocessing and
repeated acquisitions are charged. Rules can be measurable, biased,
adaptive, randomized, and randomly stopped, with input-independent
seeds and almost-sure halting for each promised input.

The profile loss is the strong loss

    sup_v E||U_T-S_Tv||inf^2,

with the spatial supremum inside the expectation. Outputs are finite
explicitly indexed real Fourier polynomials. The exact query theorem
uses RMS tolerance `1/4`; its constructed upper has RMS at most `1/8`.

For `q=s+d/2`, `gamma=d/q`, `J=ceil(1+d/(2s))`, and the stated
`Awork=a0+d^2+2d+2`, the conclusions checked below are

    Q_point(T)=Theta(exp(gamma T)),
    Q_profile(T)=Theta(exp(gamma T)),
    c exp(gamma T)<=W_point(T),W_profile(T)
                         <=C exp(gamma T)(1+T)^Awork

for all sufficiently large real `T`, with the constructive upper and
its deterministic hard query cap available for every `T>=2`.
The fixed bounded-time patch has error at most `3/32` on `[0,2]`.
All constants may depend on the fixed `d,s,p,kappa`.

## 2. Actual flow and the odd-degree bounded parent rule

On the real line `f'(z)=1-D z^(D-1)<=1`. On `[-1,1]`,
`1-D<=f'<=1`, the reaction points inward at the endpoints, and
`|f(z)|=|z|(1-|z|^(D-1))<=|z|`. Local polynomial mild contraction,
comparison with the constant endpoints, and bounded continuation
give the actual global bounded flow. No represented auxiliary flow
is substituted.

For two real bounded solutions, their secant potential is bounded
above by one. Positivity can be proved by shifting its lower bound
and iterating the Volterra equation. Comparison with the free upper
potential then gives

    |S_tv-S_tw|<=e^t P_t|v-w|.

The constant one is a one-sided derivative bound, not an absolute
Lipschitz constant for the reaction. This distinction is respected
both in the upper continuation and the lower scalar comparison.

Direct differentiation verifies the displayed scalar flow

    phi_(t,p)(c)=c e^t/[1+c^(2p)(e^(2pt)-1)]^(1/(2p)).

Its denominator is positive for `t>=0`. Comparison from `|v|<=1/2`
therefore gives exactly the time-one bound `sigma_p<1` in T94 (2.4).
This bound depends on `p`; the cubic identity interval `7/8` cannot
be reused without checking it. T94 correctly replaces that interval.

The new explicit parent rule is

    M(y)=(sum_i y_i-product_i y_i)/(D-1),
    beta_br=D-1.

At the two constant cube corners its values are `+1` and `-1`.
At any other corner the sum lies between `-D+2` and `D-2`; subtracting
the product, which is either sign, keeps the numerator within
`[-D+1,D-1]`. Since `M` is multi-affine, its value anywhere in the
cube is a convex combination of its corner values. Thus `|M|<=1`
on the complete cube. On the diagonal,

    beta_br(M(z,...,z)-z)=z-z^D.

This is a valid specialization of the bounded-parent argument. It
need not have the same rate or tree distribution as R20's particular
Bernstein construction. For example, T94's quintic uses rate four,
whereas R20's illustrative quintic uses rate five. The first-split
identity is rederived for the actual rate and rule used here.

Child independence and multi-affinity move their expectations through
`M`; boundedness justifies the conditional expectations and integrals.
The killed-heat renewal equation converts to the actual mild equation
with reaction `z-z^D`. Its bounded uniqueness identifies the tree
expectation with `S_t`.

If `n_t` is the leaf population, the generator applied to `n^h` is

    beta_br n[(n+D-1)^h-n^h]
       <=beta_br(D^h-1)n^h.

The inequality follows by binomial expansion and `n^(h-l+1)<=n^h`
for `n>=1`, `l>=1`. Stopping at population thresholds gives the
uniform moment bound. The first moment makes the exit probabilities
tend to zero and proves nonexplosion; passage to the limit gives
T94 (3.3) for every fixed integer moment. A full `D`-ary tree with
`n` leaves has `(Dn-1)/(D-1)<=2n-1` segments. Recursive generation
therefore has linear conditional work for fixed `D`.

## 3. The actual D43/D44 field law and its finite cost

All Gaussian independence statements in this section are conditional
on the finite genealogy. This conditional qualification is essential;
independence after mixing over different trees is unnecessary.

At each time the alive segments partition the terminal labels.
For a vector of leaf coefficients, Cauchy--Schwarz on that partition
gives a sum of squared block sums at least the square of the total
sum divided by `n`. Integration through height one yields

    C>=(1/n)11^t.

For the R21 recursion, in both its positive and zero-child branches,

    alpha_c>=0,    sum_c alpha_c=1,
    alpha_c a_c=h,    sum_c alpha_c^2 a_c=h.

These identities prove inductively

    Var(A_v)=a_v,    Cov(X_(v,i),A_v)=a_v.

They also prove that the root aggregate is a convex leaf combination
`A=sum_i w_i X_i`. Consequently `Cw=a1`, `sum w_i=1`, and
`a=w^t Cw>=1/n`. Since every covariance entry is at most one,
`a<=1`. The residuals satisfy

    Cov(X_i-A,A)=0,
    Cov(X_i-A,X_j-A)=C_ij-a.

The full residual vector and `A` are jointly Gaussian, so their zero
cross-covariance proves independence of the whole vectors, including
degenerate cases. Applying the construction independently in each
spatial coordinate and multiplying by `sqrt(kappa)` gives exactly
the physical covariance convention in T94. Zero branches are total
because divisions are taken only with positive variances.

Testing a proposed PSD matrix `C-b11^t` on `w` gives `b<=a`.
This is maximal removable scalar common variance, not an assertion
about global estimator variance or nonlinear Monte Carlo optimality.

The nonlinear identity is obtained by integrating the common Gaussian
through the complete translated leaf function. Conditional on the
tree and residuals, the same displacement acts on every leaf. Hence
the uniform point `U` and density `h_(kappa a)(.-U)` implement its
ordinary torus convolution. All known `g` values, mixed partials,
and selected residual values use the same array `U+Z_i`.
Both the residual covariance and heat variance change from the old
universal extraction. Damping old samples with an unchanged residual
law would not justify the identity; T94 does not do that.

The composed leaf polynomial is multi-affine and bounded by one.
Its selected distinct-label partial is the signed sum of its `2^j`
selected corner values divided by `2^j`, so its absolute value is at
most one. Repeated-label partials vanish. Averaging the uniform ordered
injection cancels
`(n)_j`, giving the full ordered derivative sum. If `n<j`, both that
sum and the returned sample are zero.

For `r=d+1`, Cauchy--Schwarz in Fourier space gives the continuous
embedding into the sup norm. A concrete admissible constant is the
T87 constant `E_d=sqrt(1+4d 3^(d-1))`, obtained by box shells.
For `theta=4pi^2 kappa`, the bounds for `eta>0`

    sum_(l in Z) e^(-eta l^2)<=1+sqrt(pi/eta),
    l^(2r)e^(-eta l^2)<=(2r/eta)^r e^(-eta l^2/2)

with `eta=theta/n` and product factorization bound the squared heat
norm by `C_h n^(r+d/2)<=C_h n^(r+d)`. Since the common variance
`a>=1/n`, replacing the heat variance by `kappa a` preserves this
upper envelope. The explicit
T87 Gaussian-sum constant uses only the permitted public constants
and elementary operations; no integral evaluator is needed.

Combining this envelope with the leaf moment of order `2j+r+d`
gives exactly

    E||W_j||_r^2<=V_j ||e||inf^(2j),
    V_j=C_h exp[beta_br(D^(2j+r+d)-1)].

The domain repair R20b is present: `g,v,e` are continuous, the base
is in the open unit ball, and the Taylor segment condition is stated
separately. Arbitrary continuous derivative directions are permitted.
On finite-tree strata the construction is Borel; heat translations
are continuous in the separable Hilbert space. The square-integrable
envelopes give genuine Bochner integrals. Using one and two extra
leaf labels controls operator continuity and the first derivative
remainder. Taking their expected envelopes proves actual infinite
Frechet differentiability into `H^r`, rather than assuming an exchange
of derivative and expectation. The Taylor remainder is consequently
the Hilbert remainder `B_J||e||inf^J/J!` used by T94.

The real coefficient formulas have positive sine sign because
`h(x-U)` expands as `cos(2pi nu.x)cos(2pi nu.U)` plus the sine product.
The base conversion `c_s=-2 Im uhat(nu)` has the same convention.
Only the finite requested array is computed; the full heat series is
an analytic object used in the proof.

The recursion, path sums, root subtraction, tuple selection, known
leaf evaluation and fixed `2^j` parent passes cost `C[(1+G)n+K]`.
This counts memory accesses and fixed-dimensional Gaussian draws.
The first population moment bounds its expectation; higher moments
are still required for derivative variance. Tree, tuple and partial
preparation precede the at most `j` unknown acquisitions. A null
infinite preparation therefore cannot violate the all-seed query cap.

## 4. Reaction-dependent Gevrey and spatial analytic estimates

I checked the paid solver in T94 Section 4 as a proof for this fixed
degree; an accepted cubic solver alone would not establish it.

For the stated Gevrey norm, the normalized product-rule coefficient
is `1/binom(alpha,beta)<=1`, proving the algebra estimate. Completeness
follows from uniform derivative convergence; strong heat continuity
follows by dominated convergence in the summable derivative norm.
On the radius-`2B` ball,

    ||f(q)||_G<=2B+(2B)^D,
    Lip_G(f)<=1+D(2B)^(D-1).

The two displayed `h0` conditions therefore make the real mild map
invariant and contractive, uniformly in `R`. Integrating by parts in
a largest-frequency coordinate and choosing derivative order of size
`sqrt(|nu|inf/R)` yields the stretched exponential coefficient bound.
Summing shells, and absorbing their polynomial factor into a smaller
exponent, gives `C R^d exp(-c1 sqrt(H/R))`.

For complex spatial smoothing, the periodized Gaussian kernel with
imaginary displacement `y` has absolute integral at most
`exp(|y|^2/(2kappa t))`. Between the tubes at times `r` and `t`, the
contour displacement is

    y-y_r=(1-sqrt(r/t))y,
    |y-y_r|<=sqrt(kappa(t-r)).

Thus its operator norm is bounded by `Kheat=e^(1/2)`. Starting from
a real sup bound one, the complex ball `Bcx=2Kheat` and the two
degree-dependent conditions (4.3) give an invariant contraction.
The polynomial is holomorphic on that ball. Periodicity cancels
contour faces, and the bounds make the time integral legitimate.
Continuity at the real initial datum follows from the approximate
identity and the bounded mild correction. Real uniqueness identifies
the resulting restriction with the actual PDE solution.

Comparison first supplies `||u(t)||inf<=1` at every real time.
Restarting from that real state for duration `h1` supplies a fixed
positive spatial strip at every time at least `h1`. A smaller-strip
contour shift gives `C exp(-bH)` after summing shells. Because
`h1<=h0`, the early and late estimates overlap. Their sum (4.5)
bounds the actual Fourier tail on the whole interval `[0,S]`.
At time one the analytic bound needs only a bounded continuous input.
No analyticity promise is imposed on `v`, and no heat-gap condition
is used. The constants may deteriorate with `D` or small `kappa`.

## 5. Galerkin bootstrap and degree-correct exact FFT computation

The rectangular Dirichlet projector has norm bounded by
`Lambda_H=C_d(1+log(H+1))^d`. Until the real Galerkin solution reaches
sup norm two, `L2=1+D2^(D-1)` is a valid absolute Lipschitz constant
for the reaction on the relevant interval.

Subtract the projected actual mild equation from the Galerkin mild
equation. Real heat is contractive. Adding back the actual Fourier
tail yields an integral inequality for the full error, whose forcing
is bounded by `epsilon0+t_H` and whose linear coefficient is
`L2 Lambda_H`. Gronwall gives (4.6). Requiring it to be at most
`min(1/4,e^(-P)/4)` places the Galerkin trajectory below `5/4`,
strictly inside the stopping boundary. Bounded finite-dimensional
continuation closes this bootstrap. A spectral maximum principle is
neither available nor assumed.

For `H=ceil(C R E^(2d+8))`, the early tail exponent is at least a
constant times `sqrt(C) E^(d+4)`. Meanwhile `log R+P+S Lambda_H`
is bounded by a constant times a lower power of `E`, with only
logarithmic dependence on the cutoff constant `C`. Increasing the
fixed constant therefore enforces the desired spatial error for all
admissible `R,S,P`; this is not a circular choice. The late exponential
tail is smaller after another fixed enlargement.

Choose the least power-of-two initialization grid at least `4H`.
Its size is `O(H)` per coordinate. Retained frequencies have distinct
residues modulo that grid. Each aliased high coefficient contributes
to at most one retained coefficient, so the retained aggregate error
is bounded by one Fourier tail beyond `Q0-H`, with no factor `H^d`.
The initial Gevrey estimate controls this error even at time zero.

If `U` is supported in the box of radius `H`, then `U^D` is supported
in the box of radius `DH`. A power-of-two grid strictly larger than
`2DH` in each coordinate represents the full polynomial without any
frequency collision. Evaluating the fixed integer power on that grid
and transforming back therefore gives the actual projected reaction.
The padding constant depends on `D`; a fixed cubic grid would not be
valid for every odd degree. With `D` fixed, the butterfly arithmetic,
twiddles, padding and memory accesses cost `O_(d,D)(H^d log(H+1))`.
All real-time arrays preserve conjugate symmetry.

## 6. Complex-time sectors, startup ellipses, and numerical bootstrap

For `|arg z|<=pi/4`, direct integration of the absolute complex
Gaussian gives the heat norm

    (|z|/Re z)^(d/2)<=2^(d/4)=Ksec.

It is independent of `H` and positive `kappa`. From a real Galerkin
state of norm at most `5/4`, radial mild Picard iteration on the
complex ball of radius `4Ksec` gives a bounded holomorphic sector
of radius `rho_H=c_(d,D)/Lambda_H`. The constants use the actual
degree-`D` forcing and derivative on that ball. These real restart
states are analytical devices; the algorithm does not query them.

A sector does not cover negative real times near zero. The separate
finite-dimensional estimate

    ||A_H v||inf<=C_d kappa H^(d+2)||v||inf

follows by summing the retained Fourier coefficients and using
`|vhat(nu)|<=||v||inf`. The full finite vector field consequently
has the initial complex disk of radius `a_H` in (4.8). Its logarithmic
reciprocal is `O(1+log(H+1))`. T94 does not assume a uniform initial
time disk for high-frequency Gevrey data.

With `L=ceil(C E^(d+4))` and the Lobatto Lebesgue bound
`beta_L=C(1+log(L+1))`, the constant in
`h=c/(Lambda_H beta_L)` can satisfy all three conditions (4.9).
The parameter-two ellipse of `[0,a_start]` has real extent from
`-a_start/8` to `9a_start/8` and imaginary extent `3a_start/8`.
It fits well inside the separate initial disk.

For a doubling panel `[t,2t]`, the ellipse has real part at least
`7t/8`, imaginary magnitude at most `3t/8`, and modulus below `3t`.
It lies within the angle-`pi/4` forward sector. Doubling stops with
endpoint in `[h,2h)`. On each later balanced panel of length between
`h/2` and `h`, the sector based at `b-h>=0` sees exactly the analogous
bounds with `h`. The radius condition follows from `3h<rho_H`.
There is no unaccounted small final panel. Counting doublings and
the balanced remainder gives (4.10).

The exact projected forcing is bounded by `C_(d,D)Lambda_H` on all
these ellipses. Cauchy bounds give geometrically decaying Banach-valued
Chebyshev coefficients. The Lobatto alias identity then gives the
interpolation defect `C Lambda_H 2^(-L)`; coordinate independence
is not involved. The ordinary cardinal harmonic-sum bound supplies
the displayed logarithmic Lebesgue constant.

On the real radius-four nodal ball with numerical start norm at most
two, heat contraction bounds the map's image by

    2+F4 ell Lambda_H beta_L<4.

Its Lipschitz factor is `q_ell=L4 ell Lambda_H beta_L<=1/4` with
the actual `L4=1+D4^(D-1)`. The linear heat values are a valid
initial iterate. A public `Kiter=ceil(Citer L)` iterations therefore
have error at most `C4^(-Kiter)`.

Inserting the exact Galerkin nodes and their interpolation defect
gives the displayed endpoint recurrence. Its accumulated stability
factor is bounded by

    product_panels (1-q_ell)^(-1)
       <=exp(C sum_panels ell Lambda_H beta_L)
       =exp(C S Lambda_H beta_L).

It is not exponential in the number of startup panels and contains
no stiffness factor `exp(C kappa H^2 S)`. Summing the interpolation
and Picard defects yields (4.12). The chosen `L` dominates the
logarithm of that stability factor, the target precision, and the
panel count. Its error can be made at most both `1/4` and `e^(-P)/4`.
The approximate starts then stay within radius two, closing the
second bootstrap rather than presupposing it.

## 7. Scalar convolution weights and the paid solver exponent

For `z=2pi^2 kappa|nu|^2 ell>0`, integration by parts directly gives

    I_0=(1-exp(-z theta))/z,
    I_j=theta^j/z-(j/z)I_(j-1).

The factor `ell` outside these dimensionless moments in (4.11) is
correct. For the zero mode, the integral is
`theta^(j+1)/(j+1)`; for `theta=0`, it is zero. Positive `kappa`
and positive panel lengths justify every nonzero-mode denominator.
Lobatto nodes generated with the cosine primitive are distinct, so
the cardinal denominators are also nonzero. Finite polynomial
products and the moment recurrences compute the weights exactly in
the stated real-operation model. No quadrature or convolution oracle
is added. Cancellation for small positive `z` would matter in finite
precision, which is outside the claim.

With `D_H=(2H+1)^d`, cardinal and mode-weight construction is at most
`O(D_H L^3)` per panel. Each Picard step costs
`O(D_H L^2+L D_H log(H+1))`, including all correctly padded nonlinear
evaluations. Multiplying by `O(L)` iterations and adding initialization
gives exactly the work expression (4.13).

The largest displayed power of `E` is

    (2d+8)d + (d+2) + 3(d+4)
       =2d^2+12d+14.

It is below `a0=2d^2+20d+50`. Initialization costs
`O(D_H[log(H+1)+Wq])`; enumeration, storage and evaluation of the
finite output are absorbed. Combining the two spatial/time budgets
leaves slack within `e^(-P)`. Section 4 therefore supplies a paid
known-profile solver for the new fixed degree, not merely an existence
statement for a Galerkin solution.

## 8. Interpolation, strong Hilbert risk, and saturation

The original interpolation construction was inspected in T70 Section 2
and T81 Section 3, as well as the relevant T84 explanation. Its bump
denominator is at least `beta(1/2)=exp(-4/3)`, and support guards
precede division. Only a fixed number of translates overlap. Each
fixed tensor stencil reproduces every total-degree polynomial of
degree at most `s-1`. Comparing to the total-degree Taylor polynomial
about the evaluation point, using consistent local torus lifts,
therefore gives `Cint k^(-s)` using only the promised total-order
derivatives through `s`, including when `s=1`.

Fixed-degree coefficients, the scaled Gevrey cutoffs and bounded
overlap give the all-order derivative bound for the constructed `g`.
This is a chosen known representation, not an added input promise.
There are `O_(d,s)(1)` coefficients per node; preparation costs
`O(k^d)`, and floors plus bounded neighboring accesses give uniform
finite lookup cost. Choosing `k>=k0` makes `||g||inf<=3/4`, so the
entire segment to `v` stays in the derivative domain.

The time-one true tail is at most `epsilon/2` with T94's choice of
`N=O(1+T)`. If the paid base solve has sup error `tau`, every complex
coefficient error is at most `tau`, whence

    ||P_N(U_base-S_1g)||_r
       <=sqrt(K)(1+dN^2)^(r/2) tau.

Thus `tau=epsilon/(4E_d D_N)` pays the Hilbert base error correctly.
The additional precision is logarithmic in `D_N`, and this solve uses
the known `g` evaluator, not unknown evolved values.

For independent complete sample copies, the cross-copy Hilbert inner
products vanish by independence, centering and second-moment Fubini.
Projection and centering decrease the second moment. Therefore (5.6)
is an upper inequality, as required by R20b, not a purported exact
equality with the uncentered envelope. Fourier coordinates within
each copy remain correlated throughout this argument.

For `M=k^d`, the order-`j` RMS term is bounded by
`sqrt(V_j) Cint^j k^(-js-d/2)/j!`; the deterministic remainder is
`B_J Cint^J k^(-Js)/J!`. Since `j>=1` and `Js>=s+d/2=q`, all
these powers are at least `q`. The chosen `k` makes their sum at
most `epsilon/(4E_d)`. Together with the base term this gives (5.7),
without a factor depending on `K` in the choice of `k`.

In the real Fourier basis, the Hilbert norm has exactly the weights
stated in T94. The true coefficients lie in `[-1,1]` for the constant
and `[-2,2]` for every sine/cosine coefficient. Coordinate projection
onto these intervals decreases the full weighted squared error on
every path, even though it may introduce bias. Embedding and the
deterministic true tail then prove the strong time-one RMS (5.8).

The new thresholds satisfy
`sigma_p<alpha_chi<beta_chi<1`. On the transition interval the
denominator for `w` is at least `e^(-2)`. With
`phi(t)=e^(-1/t)`, `phi<=e^(-1)` and `phi'<=4e^(-2)` on `(0,1)`,
the quotient derivative gives `0<=w'<=8e<24`. The scaling gap
cancels from

    chi'(z)=1-w(t)+(1-t)w'(t).

The global Lipschitz constant 25 is consequently degree independent,
while its identity interval contains the actual time-one target.
Flatness at both endpoints and the identity near zero make the odd
extension smooth and bounded by `beta_chi`.

Higher derivative constants are degree dependent. Cauchy estimates
for the flat exponential give Gevrey order two, and the positive
denominator's reciprocal follows by normalized derivative induction.
Affine rescaling inserts powers of the reciprocal threshold gap into
`Cchi`; T94 explicitly allows this dependence.

For the clipped polynomial, `||partial^alpha p_N||inf` is at most
`2K(2pi N)^|alpha|`. The ordered finite-jet chain rule gives (5.10).
The elementary inequalities used there follow from the multinomial
identity, `l!<=n!`, `n^n<=e^n n!`, `n<=2^n`, and
`n!<=d^n alpha!`. They give a uniform Gevrey scale `Rhat=NK`
for every clipped array. The actual evaluator costs `O(K)` operations
and no new initial values. No favorable random regularity event or
norm-testing oracle is needed.

## 9. Full upper composition, output, hard cap, and bounded times

Because `chi` fixes the actual target, its Lipschitz property changes
the time-one RMS to at most `e^(-S)/16`, `S=T-1`. Apply actual PDE
comparison pathwise before taking expectation. The final paid solve
adds at most `e^(-T)/16` in sup norm on every completed transcript.
Minkowski therefore gives

    (E||U_T-S_Tv||inf^2)^(1/2)
       <=1/16+e^(-T)/16<=1/8.

This pays for base error, Taylor bias, correlated sample error, true
Fourier tail, clipping, saturation and final nonlinear evolution.
It controls the expected squared spatial supremum, not only a
supremum of pointwise mean squares.

The grid/base cost is `Ck^d(1+T)^a0`; the derivative sampling cost
is `Ck^d(1+K)` in expectation. The continuation input satisfies
`Rhat=O((1+T)^(d+1))`, `Wqhat=O((1+T)^d)`, and
`Eout=O(1+T)`. Its deterministic cost is at most
`C(1+T)^(a0+d^2+2d)`. These are bounded by the advertised paid
upper with `k^d<=C exp(gamma T)` and the stated `Awork`.

The final cutoff is `O((1+T)^(3d+9))`, so the output has at most
`C(1+T)^(3d^2+9d)` real entries. Evaluation at a prescribed point
is a finite trigonometric sum of polynomial cost and no new queries.

The only acquisitions are the `k^d` coarse values and at most `j`
values in each of the `M=k^d` samples of order `j=1,...,J-1`.
Every frequency uses that same tuple. Thus the all-seed cap is
exactly bounded by

    [1+J(J-1)/2] k^d.

An unfinished preparation has no unbounded acquisition loop; earlier
completed samples obey their own caps. Nonexplosion, finite expected
tree work, and fixed finite deterministic solver counts prove almost-
sure halting and the expected work bound. Uniform endpoints and zero
Gaussian variances admit the stated guards. Coefficient clipping
also restores the continuation interface for arbitrary finite
off-promise transcripts. No convergence test controls the iteration
count.

The finite-tree constructions are Borel, and a finite coefficient
array maps continuously to its Fourier polynomial. The strong loss
is therefore measurable. Assigning zero output to a null nonhalting
set defines a random variable without pretending to detect that set
algorithmically.

For `0<=T<=2`, the coarse interpolation error is amplified by at most
`e^2` and is chosen below `1/32`. A fixed Fourier cutoff controls the
Galerkin error throughout `[0,2]`, including zero. With that cutoff,
the finite vector field and its derivative are uniformly bounded on
a fixed neighborhood, giving the stated fixed-step Euler defect and
global `C/n_b` error. A sufficiently large fixed `n_b` closes that
neighborhood bootstrap with error below `1/32`. All nonlinear FFTs
use the degree-correct padding. At `T=0` Euler step lengths vanish
without using a convolution division. The three errors sum to at
most `3/32`, with constant work and query count.

## 10. Independent derivation of the mixed-L1 estimate

Finite-time differentiability of the actual mild flow follows by
local polynomial Picard differentiation and restart, or from the
factorial Volterra inverse. On its bounded trajectory, the actual
linearized propagator obeys

    |E_u(t,r)h|<=e^(t-r)P_(t-r)|h|.

Heat preservation of mass makes this an `L1` as well as an `Linf`
bound. Put `C2=D(D-1)`, `C3=D(D-1)(D-2)`. On the invariant interval
these bound `|f''|` and `|f'''|`.

For one marked `L1` direction, every derivative product contains
exactly one factor carrying that direction. All other factors can
be bounded in `Linf`. The first variation is at most `e^t`; the
second has coefficient bounded by

    C2 integral_0^t e^(t-r)e^(2r) dr
       <=C2 t e^(2t).

The direct third-order source has coefficient at most `C3 e^(3r)`.
Each of the three second-first sources has coefficient at most
`C2^2 r e^(3r)`, whether the marked direction belongs to the second
or first factor. After propagation, their time integrals are bounded
by

    [C3 t+(3/2)C2^2 t^2] e^(3t).

At time one, multiplying the spatial mean by `e^(-1)` gives exactly

    B_D=e^2[C3+(3/2)C2^2].

For `D=3`, this is `60e^2`, as claimed. The argument uses neither
a cubic-specific derivative identity nor a small-time heat-density
supremum that could fail to be integrable.

The actual flow is odd. At zero its derivative is `e^tP_t`, so
`F(v)=e^(-1)Pi S_1v-Pi v` has `DF(0)=0` and `D^2F(0)=0`.
Applying Taylor's integral formula to `DF(rv)[h]` gives (6.4) with
the factor `1/2`. This proves the required marked-norm bound for
the mean correction throughout the open unit ball.

## 11. Complete sign slices and their actual time-one PDE bounds

The bump inputs have disjoint supports, smooth periodic extensions,
and promised derivatives at most `1/8`. Both signs occur on every
chosen slice, so all its members, including the exceptional ones,
belong to the original signed class.

For the even-grid choice, `K` and `ell` are even, and the two slice
counts are integral. From `R_T>=4`, `R_T/2<=k<=R_T`; from
`K>=2048`, `sqrt(K)<=ell<=2sqrt(K)<=K/4`. Direct substitution gives
all five bounds (7.2), including the scale identity

    e^T m_T=(R_T/k)^q ell/sqrt(K).

The prior is the equal mixture of the complete uniform slices. It
is chosen before the algorithm, and it is never conditioned on a
PDE-good event.

For the slice lemma, simultaneous sign reversal makes the balanced
expectation of an odd function zero. Flipping a uniform `ell/2`
subset of its negative entries produces the uniform positive slice;
permutation counting verifies that law without assuming any spatial
symmetry of the tested function. This proves the mean bound.

When coordinates are exposed sequentially on a fixed slice, the two
possible next-sign completions can be coupled by a swap of two signs.
Their conditional expectation difference is at most `2Lflip`.
Each centered Doob increment therefore has conditional variance at
most `Lflip^2` and moment generating function at most
`exp(theta^2 Lflip^2/2)`. Orthogonality and iterated conditional
expectation give the variance and two-sided exponential bounds (7.3).
Forced signs contribute zero. Independent signs are not assumed.

A cell flip changes the datum in `L1` by `2A_bump I/K`. Applying
the independently derived (6.4) along its segment gives the valid
flip bound `B_D A_bump^3 I/K<=L_F=B_D A_bump^3/K`. Consequently

    |EF|/m_T<=B_D A_bump^2/(2I)<=1/128.

On `|F|>m_T/4`, the centered deviation is larger than `m_T/8`.
Chebyshev, `ell^2>=K`, and the chosen amplitude threshold give
exactly the bound at most `1/64` in (7.5). Thus the actual time-one
mean on a favorable positive input is at least `3e m_T/4`.

For the whole profile, Fourier summation with `n^2>=|n|` yields
both heat bounds by the stated finite `rho`. First-variation heat
domination makes a cell flip at most `Ccell A_bump/K` at any point.
Oddness and the complete-slice lemma bound the slice expectation by
`Ccell A_bump/sqrt(K)` and give its pointwise concentration.

The periodized Gaussian gradient has `L1` norm at most
`sqrt(d/kappa)t^(-1/2)`. Differentiating the actual mild equation,
using `|f(u)|<=|u|` and `||u(r)||inf<=e^r A_bump`, gives
`Gkappa=(1+2e)sqrt(d/kappa)` as claimed. The integral of the
time singularity is finite. This bound does not grow with `k`.

The specified `N_K`-grid has at most `Cnet K^(d/2)` points and
nearest-point error at most `A_bump/(2sqrt(K))`. The chosen `z_K`
makes the failure probability at each grid point at most
`1/(64M_K)`. A union bound and the nearest-point estimate prove
the whole-profile event. Since `log K>=log 2`, its constants reduce
exactly to `Hnet`, and (7.2) gives

    ||S_1v||inf<=C0 e^(-T)sqrt(T).

Orthogonal mean subtraction is contractive in normalized `L2`, so
the same right side bounds `W1` without an extra factor two. The
mean and profile bad probabilities sum to at most `1/32` on each
unchanged full slice. Their events need not be independent.

## 12. Long-time mean and space separation for every positive gap

Let `lambda=2pi^2 kappa>0`. Because `z^D` is increasing on the
whole real line, the centered nonlinear energy term
`integral (u-b)(u^D-b^D)` is nonnegative. Poincare on the unit
torus therefore proves (8.1). When `lambda<1` that estimate permits
growth; the proof does not silently replace it by exponential decay.

The exact mean equation has remainder `R=Pi(u^D)-b^D`. The scalar
Taylor expansion about `b` has a linear term whose mean is zero.
Since the complete segment from `b` to `u(x)` stays in `[-1,1]`,
its second derivative is bounded by `D(D-1)`. Hence

    |R|<=C_R||w||2^2,       C_R=D(D-1)/2.

This accounts for all higher powers; it does not require pointwise
smallness of `w`. In particular, at `D=3` it is a valid constant
three, even though the older cubic expansion used the looser five.

The scalar secant potential in comparing `b` with `phi_(t,p)(b1)`
is at most one. Integrating its forcing gives (8.3). At `t=T-1`,

    e^t W1^2<=C0^2 T e^(-T-1),
    J_lambda(T-1)<=T exp(max(0,1-2lambda)T).

Thus the advertised `C_R C0^2 T^2 e^(-mu T)`,
`mu=min(1,2lambda)>0`, is a valid mean-error envelope. The integral
formula includes `lambda=1/2`, where `J_lambda(t)=t`; there is no
missing resonant denominator.

For the last full unit of time, compare the actual PDE to the constant
trajectory starting at `b(t-1)`. The heat `L2` to `Linf` estimate
gives sup error at most `e rho||w(t-1)||2`; subtracting the actual
mean costs at most two. Substituting (8.1) and the time-one bound
gives exactly

    Cw sqrt(T)e^(-lambda T),
    Cw=2e rho C0 e^(2(lambda-1)).

Both errors tend to zero for every fixed `lambda>0`, including the
regime with growing centered linear modes. No synchronization theorem
for arbitrary initial profiles is being asserted.

The specified `Tgrid` ensures `k>=kstar`, including between grid
jumps. It enforces every prior size and amplitude condition. The
elementary bounds

    T^2 e^(-mu T)<=8mu^(-2)e^(-mu T/2),
    sqrt(T)e^(-lambda T)<=lambda^(-1/2)e^(-lambda T/2)

show that the exact factors `512 C_R C0^2/mu^2` and
`64Cw/sqrt(lambda)` in (8.6) make the two envelopes at most `1/64`.
If either logarithm is negative, its prefactor is already small
enough; taking its maximum with zero is valid. `T0>=2` supplies
the last full unit. Every threshold is finite at fixed positive
`kappa`, without claiming uniformity as it tends to zero.

On a favorable positive input, `e^(T-1)b1>=3/4`. The exact scalar
formula implies `phi_(t,p)(c)>=Psi_p(e^t c)` for positive `c`.
Differentiation proves `Psi_p` is increasing. The integer binomial
inequality `(1+y^2)^p>=1+y^(2p)` gives

    Psi_p(3/4)>=Psi_1(3/4)=3/5.

After the two errors, the actual target is therefore at least
`91/160>1/2` at every spatial point. Oddness gives the negative
counterpart. This verifies the new-reaction scalar separation directly.

## 13. Adaptive information, arbitrary bias, and random stopping

For every favorable input, thresholding a point estimator of squared
error at most `1/16` gives sign error at most `1/4`. Adding the bad
mass yields the valid loose Bayes upper `9/32` under the original
full-slice prior.

Revealing the whole sign of a queried half-open cell strengthens the
point oracle: its scalar value is reconstructible from that sign,
the query location and the known bump, even at a boundary or zero
of the bump. No query belongs to more than one cell. Repeated
acquisitions remain charged, though they provide no additional sign.

After truncation at `ncap=floor(K/1024)` original queries, padding
with unused labels produces exactly `ncap` distinct reveals. For a
fixed seed, adaptive index choices depend only on signs already
revealed; unused signs retain the uniform remaining-count law.
The two next-positive probabilities are exactly (9.1)'s displayed
`p_+` and `p_-`. Every prefix of this length is feasible under both
slices because their smaller sign count is at least `3K/8`.

The stated bounds imply `p_-(1-p_-)>=3/16` and
`|p_+-p_-|<=2ell/K`. The elementary Bernoulli KL inequality therefore
gives at most `256/(3K)` per reveal and at most `1/12` for the
whole padded word. Coarse-graining to the event that attains total
variation and differentiating binary relative entropy twice proves
`TV<=sqrt(KL/2)<=sqrt(1/24)<1/4`. Thus capped testing error is at
least `3/8`.

The seed treatment is valid for an arbitrary allowed seed space.
At each fixed horizon the prior is finite, so the union of its
inputwise null nonhalting sets is null. For each remaining fixed
seed, the padded word distribution is the same without-replacement
law, independent of its adaptive choice of labels. Hence the joint
law is the product of the common seed law with the respective finite
word law. The full capped transcript and decision are measurable
functions of this joint data. No regular conditional probability
assumption, independent-coin replacement, or restriction of the seed
law is hidden in the KL step.

If the prior-averaged query count `qbar` is infinite, the lower is
immediate. Otherwise truncating before query `ncap+1` changes the
decision on a set of probability at most `qbar/ncap`. Comparing the
Bayes bounds gives

    qbar>=3ncap/32>=3K/65536.

The last inequality uses `K>=2048`. Combining `k>=R_T/2` gives the
exact positive constant in (9.3),

    3*2^(-d-16)(a_bump I)^(d/q),

and exponent `d/q=2d/(2s+d)`. Worst-input expectation dominates this
finite-prior average. The argument allows biased or unbounded outputs,
adaptive real query locations, rare expensive runs, and observation-
dependent stopping. A finite profile can be evaluated at `x*` without
new acquisition, transferring the lower to the strong-profile problem.
Charging every query transfers it to paid work, while proving no
sharper paid upper than the one already counted.

## 14. Physical coefficients and the unchanged-class counterexample

For fixed `a,b>0`, put `R_amp=(a/b)^(1/(2p))` and
`u(t,x)=R_amp z(a t,x)`. Substitution gives diffusion `kappa/a`
and normalized reaction `z-z^D`. The initial normalized profile is
`v/R_amp`. Thus the theorem transfers exactly to

    V_R=R_amp V,       physical RMS tolerance R_amp/4,
    normalized time theta=aT.

One physical acquisition and division by `R_amp` give one normalized
acquisition, and conversely. Output scaling adds only its finite
array cost. The exponential rate in physical time is therefore
`gamma a`, with threshold `T0/a`; the bounded-time patch concerns
`aT<=2`. The upper's physical RMS is at most `R_amp/8`.
Amplitude scaling alone does not remove `a` from physical time.

The explicit counterexample is exact. Keep the old class `V` and
absolute tolerance `1/4`, but take `b=a8^(2p)`, so `R_amp=1/8`.
Comparison with scalar solutions from `+/-1/2` bounds every profile
by `R_amp phi_(aT,p)(4)`. The normalized scalar factor
`phi_(aT,p)(4)` has inverse `2p`th power

    1-(1-4^(-2p))e^(-2paT).

It is at least `2^(-2p)` precisely once

    aT>=(1/(2p))log(1+2^(-2p)),

because `(1-4^(-2p))/(1-2^(-2p))=1+2^(-2p)`. At those times
the actual sup norm is at most `1/4`. The constant zero Fourier
polynomial meets both original tolerances with zero unknown queries
and constant paid work. Any positive exponential lower on that
unchanged class/tolerance for all `a,b>0` is false. T94 explicitly
excludes this false transfer and states the scaled problem instead.

## 15. Read provenance, assumptions, and limits of this PASS

The following inspections were performed in this task:

- The complete frozen T94, R20, R20b, R21, 04z, 04aa, and T82 texts.
- T81 lines 1--310 and 515--625 for its model, interpolation, actual
  solver, saturation and composition details.
- T84 lines 91--145, 259--394 and 546--639 for the corresponding
  interpolation, time-panel, scalar-weight and Gevrey checks.
- T87 lines 24--152, 276--399, 472--505 and 586--675 for its exact
  model, heat constants, Hilbert derivative/risk construction,
  continuation, query/output and totality interfaces.
- T83 lines 379--539 for the threshold and fully adaptive information
  comparison. The original lower proof T82 was read in full and the
  odd-degree version was independently derived above.
- T70 lines 1--230, including the original interpolation construction;
  its verified SHA256 is
  `46666ef19d4d66eb6196c486df726b6cc623f401fb717d925c82806bd3a905d6`.
- Project README/research-index context, `00-context.md`, the current
  checkpoint's relevant scope, and the inherited working-tree status.
  An early batched context output was truncated; no claim is made that
  unseen portions of that output were read. The complete task-relevant
  mathematical sources and read ranges are listed explicitly above.

The math-auto-research skill, defaults, model-routing, execution
instructions and general reader profile were read directly. They
require distinguishing conventional proof, numerical evidence and
formal coverage. This worker used the inherited research context;
its actual serving backend and reasoning-effort telemetry are not
independently exposed. Reading a configured research-model preference
is not a model switch or backend attestation. Root may separately
record its actual dispatch settings.

No external paper was needed as an additional theorem premise or
opened during T96. The bounded-parent representation, inverse-variance
Gaussian tree recursion, spectral approximation, Hilbert sampling and
finite-prior testing are classical ingredients. The algebra and
correspondence required here were checked from the displayed proofs
and original local sources. T94's attribution discussion is not an
exhaustive novelty certificate, and this audit supplies no such
certificate for the combined theorem.

The assumptions retained in this PASS are the precise fixed parameters,
full signed smooth class, scalar exact-value oracle, measurability and
input-independent seed rules, and stated ideal real-operation model.
Fixed public constants, exact elementary operations and random draws,
and ideal integer/address words are part of that model. They are not
finite-bit implementation claims. Ordinary conventional analytic and
probabilistic tools are used as proved mathematical ingredients; no
unproved PDE separation or free known-profile solver is assumed.

The theorem is for each selected real horizon. It does not assert
simultaneous accuracy at every time, a degree-uniform constant,
uniformity as `kappa` tends to zero, a matching theorem for every inward
polynomial, an exact paid-work Theta order, or practical numerical
performance. The full actual PDE, genealogy and solver composition
has not thereby been checked in Lean. Separate formal pieces or active
formal candidates are not imported by anticipation.

Only read/status/hash commands and the creation/readback of this audit
were performed. No numerical or symbolic experiment, new unknown-input
acquisition, code execution of the solver, or Lean build was run. The
inherited workspace was already dirty. The frozen target, its dependency
files, root claims/state, formal files, code, and numerical artifacts
were not edited. No material defect or counterexample to the stated
normalized theorem was found. Required repairs remain **none**; root
correspondence and acceptance are separate next actions.
