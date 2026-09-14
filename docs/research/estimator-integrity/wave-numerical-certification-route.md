# A practical route to a certified wave-rate objective

**Implemented method:** certify the full six-code moment equation by a
rational polynomial residual on a compact transformed state space.
Generate a short Taylor polynomial as a trial function, verify its
residual with Bernstein coefficients, and propagate that residual through
a positive linear error system. Convex secant extrapolation between
independently certified rate samples bounds the global optimum.

**Production status, 14 September 2026:** the
[implementation](../../../parabolab/wave_certificate.py), exact witness
checker and [saved ten-point result](../results/wave-rate-certificate.md)
now verify this route for the stated wave at `T=0.05`, root `x=0`.
The selected sample `λ=0.7375` has a global full-tree objective gap below
`5.688312×10⁻⁶`; the historical rounded `λ=0.73055` has a gap below
`6.130773×10⁻⁶`. Nine dedicated wave-certificate tests passed. User result
verification and merge approval remain pending.

The theorem and algorithm derivations below are the basis of that
certificate. Section 5 preserves the earlier scratch calculation as
historical feasibility evidence; its prototype values are superseded by
the saved production fractions and witnesses. The conventional
[mean-identification proof](allen-cahn-mean-identification.md) gives the
translation from second-moment gaps to variance gaps for these estimators.
Neither the stochastic representation nor the analytic residual comparison
has been formalized in Lean; the separately stated Lean results concern
algebra and convex enclosures under their explicit hypotheses.

## 1. The remaining problem and why direct recursion is expensive

For the raw uniform `SemilinearMechanism` at `T=0.05`, the
[codewise certificate](allen-cahn-codewise-certificate.md) already supplies
finite full-tree moments on a neighborhood of the selected rate and a
factorial omitted-depth bound. A depth-six tail below approximately
`4.45×10⁻⁶` on `[0.7,0.8]` does not certify the current floating-point
time/Gaussian quadrature error.

The implementation in `moments.py` recursively evaluates each child at
every new time/Gaussian node. With `n_t` time nodes and `n_x` Gaussian
nodes, the always-live `F₀→(F₀,F₁)` alternative alone produces at least
`(n_t n_x)^K` descendant evaluations along the root-to-`F₀` self-descendant
paths at depth `K`, before other alternatives are counted. At `K=6` this
is `16,777,216` evaluations for orders `(4,4)` and `68,719,476,736` for
orders `(8,8)`. A crude raw-table upper recurrence uses five children per
`F` table, giving growth of order `(5 n_t n_x)^K`. Exact-zero pruning and
reusing repeated sibling codes improve constants, but do not remove the
state/time-node proliferation.

Making that calculation rigorous also requires all of the following:

- Bounds on spatial derivatives of the **continuation products**, through
  order `2n_x`, for each depth and code. Terminal derivative bounds alone
  do not give these.
- Bounds on time derivatives of the complete heat-integrated branch
  integrand through order `2n_t`. Apparent singularities from writing a
  Gaussian displacement as `sqrt(s) Z` must be handled at the semigroup
  level near `s=0`.
- A rule for propagating every inner quadrature error through the outer
  products, with the actual code multiplicities and inverse probabilities.
- Validated quadrature nodes, weights, exponentials and evaluations, in
  addition to a truncation-error formula. Refinement agreement alone
  establishes none of these requirements.

For example, if a positive Gaussian quadrature is exact through degree
`2n−1`, Taylor's theorem gives the elementary bound

\[
\left|\mathbb E h(x+\sqrt{s}Z)
-\sum_jw_jh(x+\sqrt{s}z_j)\right|
\le\frac{s^n\|h^{(2n)}\|_\infty}{(2n)!}
\left(\mathbb E|Z|^{2n}+\sum_jw_j|z_j|^{2n}\right).
\]

This follows by applying the Taylor remainder separately to the expectation
and quadrature; their polynomial terms cancel. It illustrates the missing
continuation-derivative obligation without assuming a sharp Gaussian
quadrature remainder theorem. An analogous bound applies to time
quadrature about the interval midpoint. Better analytic-strip estimates
may improve constants, but the continuation system, its complex-domain
bounds and their finiteness would still need to be proved.

**Decision:** retain low-depth quadrature as an independent diagnostic.
For certification, solve and validate the six-code equation directly.
Doing so gives a full-tree objective error, so an additional depth-tail
allowance is unnecessary.

## 2. Compactifying the wave without a spatial-tail approximation

For the current wave terminal value,

\[
\phi(x)=-\frac1{1+e^x},\qquad
s(x):=-\phi(x)=\frac1{1+e^x}\in(0,1).
\]

Then `s′=−s(1−s)` and `s″=s(1−s)(1−2s)`. Under Brownian motion the
transformed generator is

\[
\mathcal L p(s)=
\frac12s^2(1-s)^2p''(s)
+\frac12s(1-s)(1-2s)p'(s). \tag{1}
\]

Equivalently the diffusion obeys

\[
dS=-S(1-S)\,dW+\tfrac12S(1-S)(1-2S)\,dt.
\]

For interior initial states it is exactly `S_t=s(x+W_t)`. At `s=0,1`
the coefficients vanish; adjoining absorbing endpoints extends its
Markov semigroup `Q_t` to the compact interval. This is a coordinate
change of the original process, not truncation of Brownian space or an
approximate reflecting boundary. The root `x=0` becomes **exactly**
`s=1/2`.

In the order `(Id,D,F₀,F₁,F₂,F₃)`, all terminal squared factors are
polynomials:

\[
A(s)=\left(
s^2,\ s^2(1-s)^2,\ s^2(1-s^2)^2,
\ (1-3s^2)^2,\ 36s^2,\ 36
\right). \tag{2}
\]

Use the raw uniform branch polynomial

\[
G(i,d,a,b,c,e)=
(a,bd,2ab+\tfrac12d^2c,2ac+\tfrac12d^2e,2ae,0).
\tag{3}
\]

At a fixed rate the full ordinary second moment `Y` satisfies

\[
\partial_\tau Y=\mathcal L Y+\lambda Y+G(Y)/\lambda,
\qquad Y(0,s)=A(s). \tag{4}
\]

The finite full-moment certificate supplies the bounded solution through
the requested horizon. Its relation to (4) can be expressed entirely in
mild form through `Q_t`; boundary smoothness of an arbitrary PDE solution
need not be assumed. The bounded polynomial reaction is locally Lipschitz,
so the bounded mild solution is unique. The scalar normalization, raw
`F₂` probability and `F₃` survival inflation remain exactly those of the
codewise certificate.

## 3. Residual-to-moment error theorem

Let `B≥0` be an already-verified uniform bound for the true full moments
on `[0,T]×[0,1]`, simultaneously for `λ∈[ℓ,u]`. Let `P(τ,s)` be a vector
of polynomials, or a continuous piecewise polynomial in time, used to
approximate the solution at a stated rate. Define its residual by

\[
R=\partial_\tau P-\mathcal L P-\lambda P-G(P)/\lambda. \tag{5}
\]

Suppose exact polynomial enclosures establish

\[
|P|\le C,\qquad |P(0,s)-A(s)|\le\eta,
\qquad |R(\tau,s)|\le\rho(\tau), \tag{6}
\]

componentwise. The vector `ρ` may be a piecewise constant rational bound
on successive time slabs. Set `\widehat B=max(B,C)` componentwise and
`J=DG(\widehat B)`, using the Jacobian displayed in the codewise note.
This construction is not circular: `B` bounds the true moment independently
of `P`, while `C` comes from a separate polynomial magnitude check.

The approximate coordinates may be signed. For any `v,w` with
`|v|,|w|≤\widehat B`, the segment between them lies in the same signed box,
and the fundamental theorem of calculus gives

\[
|G(v)-G(w)|\le J|v-w|. \tag{7}
\]

Indeed every derivative of `G` is a polynomial with nonnegative
coefficients, so its absolute value on the signed box is bounded by its
value at `\widehat B`. Thus one must not invoke monotonicity on the
nonnegative orthant while silently permitting negative trial values.
Equation (7) is the appropriate signed-box statement.

**Theorem.** Let `e` solve

\[
e'=(\lambda I+J/\lambda)e+\rho,
\qquad e(0)=\eta. \tag{8}
\]

Then

\[
\sup_{s\in[0,1]}|Y(\tau,s)-P(\tau,s)|\le e(\tau). \tag{9}
\]

A componentwise supersolution to (8) is sufficient. The common matrix
`uI+J/ℓ` gives a uniform version when residual bounds are valid over the
entire rate interval.

**Proof.** Polynomial trial functions have bounded derivatives on the
compact state interval. Dynkin's formula, including the absorbing
endpoints, gives their mild equation with forcing `R`. Subtract it from
the true moment's mild equation. Positivity and sup-norm contraction of
`Q_t`, followed by (7), show that the error supremum `E` satisfies

\[
E(\tau)\le\eta+
\int_0^\tau\bigl[(\lambda I+J/\lambda)E(v)+\rho(v)\bigr],dv.
\]

The matrix has nonnegative entries. Positive integral iteration, or the
matrix version of Gronwall's inequality, bounds this by the solution of
(8). Finite-dimensional linear existence is global. For time slabs the
same proof is restarted at each boundary; the trial polynomial must be
continuous there, or a separately bounded jump must be added to the
initial error for the next slab. ∎

At the requested root, (9) immediately gives

\[
P_{\mathrm{Id}}(T,1/2)-e_{\mathrm{Id}}(T)
\le M(\lambda;0)\le
P_{\mathrm{Id}}(T,1/2)+e_{\mathrm{Id}}(T). \tag{10}
\]

The lower bound may be replaced by its maximum with zero.

### Rational verification of the error propagation

For a slab of width `h`, constant rational forcing bound `ρ`, and matrix
`H=uI+J/ℓ`, start from an error upper endpoint `a≥0`. Verify a rational
endpoint `b` satisfying

\[
b\ge a+h(Hb+\rho). \tag{11}
\]

Its affine interpolation is increasing and has slope at least its
largest right-hand side on the slab. Thus it is a valid supersolution
to (8). Iteration with upward rational-grid rounding can propose `b`,
but only the exact inequality accepts a step. This is the same
postfixed-box principle already used for the moment certificate, here
applied to a linear error system. No floating-point matrix exponential
is needed.

## 4. A short formal Taylor polynomial is a convenient trial function

For the first implementation take one slab, `θ=τ/T∈[0,1]`, and

\[
P(\theta,s)=\sum_{n=0}^m a_n(s)\theta^n,\qquad a_0=A.
\]

At rational `λ,T`, generate rational polynomial coefficients by

\[
a_{n+1}=\frac{T}{n+1}
\left(\mathcal L a_n+\lambda a_n+
\lambda^{-1}[\theta^n]G\!\left(\sum_{j=0}^n a_j\theta^j\right)\right).
\tag{12}
\]

Products in the last term use ordinary finite coefficient convolution.
The residual must use `\partial_τ=(1/T)\partial_θ`, not
`\partial_θ`; this scaling is an essential verification check.

**No infinite Taylor-series convergence theorem is required.** Equation
(12) is a trial-generation algorithm. Once the finite polynomial is
constructed, its complete residual, including all terms above degree
`m`, is computed and bounded directly by (5)–(11). Roundoff-free formal
cancellation of the first `m` residual coefficients is a useful check,
not a replacement for bounding the remaining coefficients.

The spatial degrees of `a_n` are bounded by

\[
(2,4,6,4,2,0)+4n,
\]

with the `F₃` degree actually zero throughout. This follows by induction:
`\mathcal L` increases degree by at most two; each branch product has
the stated child's degree budget plus at most four at the next time
order. Thus the trial's maximum spatial degree is `6+4m`, not an
exponential function of `m`. The residual has time degree at most `3m`
and spatial degree at most `10+12m`, due to the cubic branch monomial.
For `m=5`, these are trial degree `26` and residual bidegree at most
`(15,70)`. Each residual component fits in at most `16×71=1,136`
rational coefficient slots, and most components use fewer.

If one slab stops producing useful bounds, use multiple time slabs with
verified continuous trial interpolation, raise the degree, or use a
numerically fitted polynomial that is rounded to rational coefficients
and then checked by the same residual verifier. Failure to meet a target
is inconclusive; it does not imply divergence of the moment.

## 5. Exact Bernstein enclosures on rectangles

For a scalar polynomial `q(θ,s)` of bidegree `(n,d)`, write

\[
q(\theta,s)=\sum_{i=0}^n\sum_{j=0}^d
\beta_{ij}\binom ni\theta^i(1-\theta)^{n-i}
\binom dj s^j(1-s)^{d-j}. \tag{13}
\]

The tensor basis is nonnegative and sums to one on the unit square.
Consequently

\[
\min_{i,j}\beta_{ij}\le q\le\max_{i,j}\beta_{ij},
\qquad |q|\le\max_{i,j}|\beta_{ij}|. \tag{14}
\]

For power coefficients `q=Σ c_{ab} θ^a s^b`, the exact conversion is

\[
\beta_{ij}=\sum_{a\le i,\ b\le j} c_{ab}
\frac{\binom ia}{\binom na}
\frac{\binom jb}{\binom db}. \tag{15}
\]

The identity follows from expanding each monomial in the Bernstein
basis, or directly from the binomial theorem. Rational rectangle endpoints
preserve rational coefficients under affine substitution. De Casteljau
subdivision at rational points, especially `1/2`, tightens bounds while
retaining exact arithmetic. No sampling of residuals is used in (14).

Apply this separately to each trial coordinate for its magnitude bound
`C`, each initial mismatch for `η`, and each residual coordinate for `ρ`.
The polynomial residual requires exact multiplication; truncating its
high time or space coefficients is invalid unless a separate remainder
bound is included. The exponent `s²(1−s)²` in (1), scalar `1/T`, raw
`F₂` coefficient and matrix `J` deserve independent symbolic tests.

Power-to-Bernstein conversion is separable in the two coordinates, with
arithmetic-operation cost `O(n d²+n² d)` per component before subdivision.
Coefficient convolution and subdivisions introduce polynomial, rather
than depth-exponential, work. This count does not bound integer bit
complexity or promise a runtime; saved timings should count both trial
construction and exact checking.

### Historical bounded feasibility calculation

An exploratory exact-`Fraction` implementation used `λ=73/100`,
`T=1/20`, the existing wave box on `[7/10,4/5]`, and 100 rational error
steps on a `2⁻⁶⁰` grid. It reported:

| Trial time degree | Spatial residual cells | Reported root error upper bound |
| --- | ---: | ---: |
| 3 | 2 halves | `7.43×10⁻⁵` |
| 5 | 1 interval | `2.01×10⁻⁵` |
| 5 | 2 halves | `2.11×10⁻⁶` |
| 5 | 4 quarters | `1.60×10⁻⁶` |

For degree five, Bernstein bounds on eight state subintervals put all
trial-coordinate magnitudes below the already-certified moment box.
The four-quarter calculation took approximately two seconds in the local
Python 3.11 environment. These are **historical prototype outputs**, not the production certificate.
The subsequent implementation, independent symbolic tests and exact
witness checks are recorded in the linked production result. Dense
floating-point residual sampling was used only as a diagnostic and is
not the source of either the prototype enclosure calculation or the
production error guarantee.

## 6. Certifying the selected rate using convexity

Independent point certificates avoid an additional parameter dimension.
Let `x₀<⋯<x_N` be rational rates and let

\[
L_i\le M(x_i)\le U_i
\]

be the full-moment intervals from (10). The full objective is convex by
the nonnegative topology-kernel representation in the general-rate note;
the wave moment certificate ensures it is finite on the chosen interval.

For any adjacent pair `a<b`, endpoint intervals imply two extrapolation
bounds:

\[
\begin{aligned}
x\ge b&\implies
M(x)\ge L_b+(x-b)\frac{L_b-U_a}{b-a},\\
x\le a&\implies
M(x)\ge L_a+(x-a)\frac{U_b-L_a}{b-a}.
\end{aligned} \tag{16}
\]

**Proof.** Convexity gives the same inequalities with exact endpoint
values. In the first, the coefficient of `M(b)` is positive and the
coefficient of `M(a)` is negative, so substitute `L_b,U_a`. In the second,
the coefficient of `M(a)` is positive and that of `M(b)` is negative,
so substitute `L_a,U_b`. ∎

These are lower bounds **outside** the secant interval. Interpolating
between two points of a convex function gives an upper bound, so a chord
must never be used as the lower bound inside its own interval.

On a rate cell `[x_i,x_{i+1}]`, use the first line of (16) from
`[x_{i-1},x_i]` when available and the second line from
`[x_{i+1},x_{i+2}]` when available. Their pointwise maximum is a valid
lower envelope. Its minimum on the cell occurs at an endpoint or at
the intersection of the two affine functions when that intersection lies
in the cell. All calculations are rational. The first and last cells
can use the one available affine bound; at least three distinct samples
are needed to cover every cell this way. More distant valid secants may
also tighten the envelope.

Taking the minimum of the cell lower bounds gives `L_I≤inf_I M`. For a
selected sample with upper bound `U_*`,

\[
M(\widehat\lambda)-\inf_{\lambda\in I}M(\lambda)
\le U_*-L_I. \tag{17}
\]

A sensible first grid is `{0.7,0.725,0.75,0.775,0.8}`, with degree-five
point trials. Refine a cell whose lower envelope prevents the target
gap; improve point accuracy if interval uncertainty makes the secant
slopes too weak. No stationarity or optimizer bracket-width tolerance is
substituted for (17).

### A possible global upgrade from the same rate samples

If the first pair satisfies

\[
\frac{U_1-L_0}{x_1-x_0}\le0,
\]

then (16) gives `M(x)≥L₀` for every positive `x≤x₀`. If the last pair
satisfies

\[
\frac{L_N-U_{N-1}}{x_N-x_{N-1}}\ge0,
\]

then `M(x)≥L_N` for every `x≥x_N`. Thus

\[
L_{\rm global}=\min(L_I,L_0,L_N)
\le\inf_{\lambda>0}M(\lambda). \tag{18}
\]

If both endpoint lower bounds exceed the incumbent upper, rates outside
the bracket cannot improve the incumbent, and (17) already gives the
global gap. All slope signs and endpoint comparisons must be checked;
they are not guaranteed by the approximate location of the optimum.

Outside the certified finite-moment interval, `M` may take the value
`+∞`. The topology-kernel convexity argument is interpreted in extended
nonnegative values: when the target exterior value is infinite the
lower bound is immediate, and otherwise ordinary finite-value convexity
on the relevant points proves (16). No global moment-finiteness claim
or attained-optimum assumption is needed for (18). A Lean theorem stated
for real-valued convex functions certifies its explicit real-valued
hypotheses and algebra; the extended-valued moment bridge remains part
of this conventional argument unless separately formalized.

## 7. Implementation and acceptance status

The production implementation now supplies the following parts of the
original acceptance plan:

1. Exact polynomial differentiation, multiplication and coefficient
   extraction generate the one-slab trial. An independent symbolic test
   reconstructs the reaction from the actual sampler tuples and verifies
   the complete residual, including the normalized-time factor.
2. An independent symbolic chain-rule test verifies the transformed
   diffusion generator against differentiation in the original `x`
   coordinate. Terminal-factor checks tie the polynomial data to the
   existing sampler.
3. Exact Bernstein conversion and dyadic spatial subdivision bound the
   trial and residual. Reconstruction and signed interior-extremum
   tests verify the relevant identities. The saved archive contains
   exact polynomial coefficients, bounds and error witnesses.
4. The checker revalidates the independent moment box, trial magnitude,
   residual bounds and every positive linear error step. Tampering tests
   cover altered initial data, residuals, error endpoints, rate identity
   and lost time coverage. The nine dedicated tests passed together.
5. Ten point certificates, exact neighboring-secant lower envelopes and
   verified exterior slope signs produce the saved global objective-gap
   bounds. The minimum is bounded directly; no stationarity condition,
   chord lower bound, or assumed attained optimizer is used.

These checks complete the numerical-certification route for this
particular horizon, root and raw uniform estimator. The
[results note](../results/wave-rate-certificate.md) identifies the exact
witness archive, reproduction commands, independent collocation
diagnostics and formal scope. Its saved fractions supersede rounded
values in this derivation. The current arithmetic checks do not amount
to a Lean proof of the full certificate verifier or its stochastic bridge.

The original `10⁻⁴` objective-gap target has been exceeded: the selected
point's verified gap is below `10⁻⁵`. Further work should test whether
constructing or reusing this certificate pays for itself in prespecified
Monte Carlo workloads, and then extend the verified scope when justified.
Other horizons, state objectives and tuple proposals remain separate
research tasks. If a future parameter choice makes the single-slab
method inconclusive, the first numerical fallbacks are polynomial-degree
or state-subdivision refinement, followed by multiple time slabs.
