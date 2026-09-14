# Profile-rate selection, certified loss, and amortization

**Scope:** the raw uniform one-dimensional Allen–Cahn wave at `T=0.05`,
evaluated at `t=0` on `[-2,-1,0,1,2]`, with equal positive weights `1/5`.
This is a new profile objective. The previously certified optimum gap at
`x=0` does not establish an optimum gap for this grid.

The formulas below distinguish a fixed-sample variance objective from
accuracy per computational cost. They are conventional mathematical
arguments. Computational certificates, experiment results and any Lean
algebraic coverage must be recorded separately. No practical speedup is
assumed from changing the objective.

## 1. The profile objective and what it controls

More generally, fix a finite set of states `x_j`, weights `w_j≥0` with
`Σw_j=1`, and a common exponential rate `λ>0`. Delete zero-weight entries
when interpreting extended-valued sums. Write

\[
\mu_j=u(0,x_j),\quad M_j(\lambda)=\mathbb E_\lambda H_j^2,
\quad V_j(\lambda)=M_j(\lambda)-\mu_j^2.
\]

The [Allen–Cahn mean-identification argument](allen-cahn-mean-identification.md)
is uniform in the starting state. At this horizon it identifies an
integrable, rate-independent mean for every positive rate; second moments
may still be infinite outside certified regions.

For `n_j≥1` independent complete trees at point `j`, define its sample
mean `\widehat u_j`. Independence is required between the trees used in
one sample mean. Independence across different points is unnecessary for
the expectation of the separable loss

\[
\mathcal L=\sum_jw_j(\widehat u_j-\mu_j)^2,
\qquad
\mathbb E\mathcal L=\sum_j\frac{w_j V_j(\lambda)}{n_j}.
\tag{1}
\]

This is not the variance of a weighted average of the point estimates;
that different objective would include covariances. Likewise, (1) is an
expected squared profile error, not the expected profile RMSE or its
median. `sqrt(E L)` and `E sqrt(L)` are different summaries.

With an equal fixed count `n` at every point, set

\[
J(\lambda)=\sum_jw_jM_j(\lambda),\qquad
\overline V(\lambda)=\sum_jw_jV_j(\lambda)
=J(\lambda)-\sum_jw_j\mu_j^2.
\tag{2}
\]

Then `E L=\overline V/n`, and minimizing `J` is exactly equivalent to
minimizing `\overline V`. In extended nonnegative values, a certified
finite incumbent satisfies

\[
\overline V(\widehat\lambda)-\inf_{\lambda>0}\overline V(\lambda)
=J(\widehat\lambda)-\inf_{\lambda>0}J(\lambda).
\tag{3}
\]

Thus a certified profile-objective gap `Δ` bounds excess expected
squared profile error by `Δ/n` at equal counts. A comparison against a
baseline uses the same implication only when the counts are equal.
The objective does not guarantee pointwise improvement at every grid
location or control maximum spatial error.

If the `n_j` are unequal but fixed independently of the candidate rate,
the relevant weights are `w_j/n_j` in the second-moment objective. If
sample counts themselves change with rate through a cost constraint,
minimizing (2) alone no longer solves the intended problem.

## 2. The grid short-time rate

For a fixed state, the identity-code moment equation is

\[
M_{\mathrm{Id}}(T,x)=e^{\lambda T}P_T\phi^2(x)
+\frac1\lambda\int_0^T e^{\lambda s}
P_s M_{F_0}(T-s,\cdot)(x)\,ds.
\]

The bounded smooth wave data and a local full-moment bound justify the
following expansion, uniformly for rates in a compact subset of
`(0,∞)`:

\[
M_j(\lambda)=\phi_j^2+T\left[
\tfrac12(\phi^2)''(x_j)+\lambda\phi_j^2+
\frac{f(\phi_j)^2}{\lambda}\right]+O(T^2),
\tag{4}
\]

where `\phi_j=\phi(x_j)`. One direct justification is to expand the
terminal heat term using bounded fourth derivatives, and use
`M_{F₀}(r,·)=f(φ)²+O(r)` uniformly in the branch integral. Bounded
second derivatives of its terminal factor and the bounded polynomial
moment source give that latter estimate. These conditions hold for the
current logistic wave. This statement does not give a certified
numerical remainder at `T=0.05`.

Since

\[
u(0,x_j)^2=\phi_j^2+T[
\phi_j\phi_j''+2\phi_j f(\phi_j)]+O(T^2),
\]

subtracting the mean square yields

\[
V_j(\lambda)=T\left[
(\phi_j')^2+\lambda\phi_j^2+
\frac{f(\phi_j)^2}{\lambda}-2\phi_jf(\phi_j)\right]+O(T^2).
\tag{5}
\]

The rate-dependent part of either weighted expansion is

\[
T(A\lambda+B/\lambda),\qquad
A=\sum_jw_j\phi_j^2,\quad B=\sum_jw_jf(\phi_j)^2.
\]

For `A,B>0`, the elementary inequality
`Aλ+B/λ≥2√(AB)` has equality exactly at

\[
\boxed{\lambda_{\rm short,grid}=\sqrt{B/A}.} \tag{6}
\]

This is a cheap leading-order baseline. It is not a certificate of the
finite-horizon optimum, and the compact-rate expansion alone does not
prove convergence of unrestricted minimizers as `T→0`.

For this wave `φ(x)=−1/(1+e^x)` and `f(φ)=φ(1−φ²)`. With the stated
grid and equal weights, ordinary numerical evaluation gives

\[
A\approx0.32935779254200465,
\quad B\approx0.07430182793068835,
\quad\lambda_{\rm short,grid}\approx0.47496956016576364.
\tag{7}
\]

At `x=0` alone, (6) instead gives `0.75`. Equal profile weights still
place more weight on large `|φ|²` in the leading rate penalty `Aλ`;
this explains why a profile baseline differs materially from its
reference-state counterpart. The lower-rate candidate needs its own
moment certificate; it is not covered by a certificate restricted to
`[0.7,0.8]`.

If `A=0` or `B=0`, the positive interior formula requires separate
handling. For general `A>0,B=0`, the leading model decreases toward
`λ=0`; there is no positive minimizer of that leading term. If both
vanish, it does not select a rate. At the present finite wave grid,
`A,B` are strictly positive. Non-normalized positive weights give the
same rate because their common scale cancels in `B/A`.

## 3. Certifying all grid states from one wave trial

A [wave residual certificate](wave-numerical-certification-route.md)
provides a polynomial trial `P(θ,s)` and a uniform root-coordinate error
`e_Id(T)`, where

\[
\theta=\tau/T,\qquad s(x)=1/(1+e^x).
\]

One trial at a given rate serves the entire grid. The method does not
require generating and verifying five separate six-code trial systems.
However, unlike `x=0`, the other grid points do not have exactly rational
logistic coordinates. Their coordinate approximation must be included.

### Rational exponential and logistic intervals

For rational `r≥0`, set `S_N(r)=Σ_{k=0}^N r^k/k!` and assume
`q=r/(N+2)<1`. The exponential series has nonnegative terms, and the
ratio of successive terms in its tail is at most `q`. Hence

\[
S_N(r)\le e^r\le S_N(r)+
\frac{r^{N+1}}{(N+1)!}\frac1{1-r/(N+2)}.
\tag{8}
\]

This is an exact rational enclosure. For negative arguments, reciprocal
bounds for `e^{−r}=1/e^r` reverse the endpoints. If `e^x∈[E_-,E_+]`,
monotonicity gives

\[
s(x)\in\left[\frac1{1+E_+},\frac1{1+E_-}\right].
\tag{9}
\]

At `x=0`, use the exact singleton `s=1/2`. Symmetry `s(−x)=1−s(x)`
can reuse positive-coordinate bounds, with the appropriate reversed
endpoints. A decimal call to `exp` or a decimal-to-rational conversion
of its output is not a proof of (9).

### Trial evaluation with coordinate error included

At the horizon, let `q_λ(s)=P_Id(1,s)`, formed by summing each spatial
coefficient over all time orders. Given a verified interval `[s_-,s_+]`,
exact interval Horner evaluation gives a valid range. For every Horner
multiplication, take the minimum and maximum of all four endpoint
products before adding the next signed coefficient. This handles signed
intermediate intervals without assuming monotonicity of the polynomial.

An alternative is to substitute `s=s_-+(s_+−s_-)z` and bound the resulting
polynomial on `z∈[0,1]` using exact Bernstein coefficients. If either
method encloses its range by `[q_-,q_+]`, then

\[
\boxed{
M_j(\lambda)\in
[\max(0,q_- - e_{\rm Id}),\ q_+ + e_{\rm Id}].
} \tag{10}
\]

All polynomial, coordinate, residual and rounding errors have now been
included. No extra coordinate-error term should be added a second time.
A valid alternative is rational evaluation at the coordinate midpoint
plus a certified derivative bound times the coordinate radius.

The magnitude and residual certificates are uniform over all states,
so reusing them at five points is legitimate. The point intervals may
be highly dependent; deterministic enclosure addition does not require
independence.

For weights that are exact nonnegative rationals, (10) gives

\[
L(\lambda):=\sum_jw_jL_j(\lambda)
\le J(\lambda)\le
\sum_jw_jU_j(\lambda)=:U(\lambda). \tag{11}
\]

If `Σw=1`, the common residual-error contribution remains `e_Id`,
rather than becoming `5e_Id`. The coordinate-range contributions are
weighted separately. Stored normalized weights, exact grid values,
coordinate witnesses and the underlying wave moment certificate are
part of the profile certificate identity.

## 4. Profile convexity, rate comparison and global gaps

Each `M_j(λ)` has the nonnegative topology-kernel representation, hence
is extended-valued convex. A nonnegative weighted sum is also convex:

\[
J(\alpha\lambda+(1-\alpha)\nu)
\le\alpha J(\lambda)+(1-\alpha)J(\nu),
\qquad0\le\alpha\le1.
\tag{12}
\]

Independent certified rate samples provide `(λ_i,L_i,U_i)` from (11).
For a rate between two samples `a≤λ≤b`, put `θ=(λ−a)/(b−a)`.
Convexity gives the complementary **upper** interpolation bound

\[
J(\lambda)\le(1-\theta)U_a+\theta U_b. \tag{12a}
\]

This covers the actual binary-floating-point rate returned by a numerical
policy: regard that finite float as its exact rational value, locate its
two surrounding certified samples, and evaluate (12a) rationally. Subtract
the same global lower bound below to obtain its objective-gap guarantee.
No assumption that a rounded decimal rate equals the implemented policy
is required. This still concerns the ideal real-arithmetic estimator at
that represented rate; it does not certify production arithmetic error.
Upper interpolation applies inside the sampled pair, whereas the lower
secant bounds below apply outside it.

The neighboring-secant extrapolation construction in the wave note
applies directly to this **aggregated** objective. In particular,

\[
\begin{aligned}
x\ge b&\implies J(x)\ge L_b+(x-b)(L_b-U_a)/(b-a),\\
x\le a&\implies J(x)\ge L_a+(x-a)(U_b-L_a)/(b-a).
\end{aligned}
\tag{13}
\]

The secant bounds are used only outside their defining pair. Inside
each rate cell, minimize the maximum of the available neighboring
affine lower bounds at endpoints and their intersections. The minimum
over cells is a valid lower bound for `inf_I J`.

If the first endpoint upper secant slope is nonpositive, the first
point's lower bound also bounds the entire left exterior ray. If the
last endpoint lower secant slope is nonnegative, the last lower bound
covers the right exterior ray. Otherwise nonnegativity gives a safe,
possibly uninformative exterior lower bound. Taking the minimum across
all cells and the two exterior bounds gives `L_global≤inf_{λ>0}J`.
For a selected point with upper bound `U_*`,

\[
J(\widehat\lambda)-\inf_{\lambda>0}J(\lambda)
\le U_*-L_{\rm global}. \tag{14}
\]

No attained optimum or finite moment at every exterior rate is needed.
An infinite exterior objective satisfies every finite lower bound
trivially. Equation (3) transfers (14) to the profile variance objective.
A positive quantity `L(λ_baseline)−U_*` certifies additive improvement
against that baseline at equal sample counts.

All rows in one aggregation must describe the same estimator, horizon,
grid, weights, and rate. A historical `x=0` certificate cannot substitute
for (11), even if its selected rate happens to be in the profile search
interval. Optimizing a finite-depth grid quadrature is a separate
approximation unless its output is subsequently covered by this exact
profile certificate.

### Exact mean-square and relative-gap bounds

Absolute variance values can also be enclosed without evaluating the
mean in floating point. The identified wave mean is

\[
\mu_j=-\frac1{1+\exp(x_j-3T/2)}.
\]

At rational `x_j,T`, apply (8)–(9) to `x_j−3T/2`. If the resulting
positive logistic interval is `[a_j,b_j]⊂[0,1]`, then
`μ_j²∈[a_j²,b_j²]`. Therefore the rate-independent weighted mean square
has the exact rational enclosure

\[
C_-:=\sum_jw_j a_j^2
\le C:=\sum_jw_j\mu_j^2
\le\sum_jw_j b_j^2=:C_+.
\]

For a profile moment interval `[L(λ),U(λ)]`,

\[
\overline V(\lambda)\in
[\max(0,L(\lambda)-C_+),\ U(\lambda)-C_-].
\]

A global moment lower bound gives

\[
V_{\inf}^{\rm lower}:=\max(0,L_{\rm global}-C_+)
\le\inf_{\lambda>0}\overline V(\lambda).
\]

If `V_inf^lower>0` and `Δ` is the certified global objective gap, then

\[
\frac{\overline V(\widehat\lambda)-\inf_{\lambda>0}\overline V(\lambda)}
{\inf_{\lambda>0}\overline V(\lambda)}
\le\frac{\Delta}{V_{\inf}^{\rm lower}}.
\]

This is a relative excess-variance bound with the optimum profile
variance in the denominator. It is not a relative improvement against
an arbitrary baseline. A zero denominator lower bound leaves this
relative certificate inconclusive even when the additive gap is useful.
For equal counts, the same relative excess bound applies to expected
squared profile loss because both numerator and denominator divide by
`n`. No attained optimum is required.

## 5. Equal-count computational efficiency and reuse

For method `i`, let `h_i≥0` be a one-time policy construction cost and
`c_i>0` the cost of one additional complete tree at **every** grid point.
If costs are expected per-tree costs, `c_i=Σ_j c_{ij}`; the averaging
weights in the loss do not divide the actual number of computed points.
A median calibration timing is instead a predicted-cost coefficient,
not a mathematical expected value.

Consider `R≥1` requested profiles under a frozen reusable policy,
with `n` trees at each point of each profile. The model is

\[
C_i=h_i+R c_i n,
\qquad
\mathbb E\!\left[\frac1R\sum_{r=1}^R\mathcal L_r\right]
=\overline V_i/n.
\tag{15}
\]

The requested predictions are not pooled across profiles. Averaging
`R` squared losses therefore does **not** divide the expected loss by
another factor `R`. Reuse may reduce the setup charge per profile; it
does not increase the sample count of a separately requested prediction.

Under a total budget `B>h_i`, the continuous-count model gives

\[
n_i=(B-h_i)/(R c_i),\qquad
\operatorname{Loss}_i(B)=\frac{R P_i}{B-h_i},
\quad P_i=c_i\overline V_i.
\tag{16}
\]

For `B>max(h_a,h_b)`, method `a` has strictly lower modeled loss than
`b` exactly when

\[
P_a(B-h_b)<P_b(B-h_a). \tag{17}
\]

If `ΔP=P_b−P_a>0`, this is equivalent to

\[
B>\frac{P_b h_a-P_a h_b}{\Delta P},
\quad\text{as well as }B>\max(h_a,h_b).
\tag{18}
\]

A tuned method with more setup cost has an eventual break-even budget
only when it has a better variance-cost product. If `ΔP≤0`, do not
apply (18) with a reversed or zero denominator; use (17) and analyze
that case separately. Merely increasing `R` at a **fixed total budget**
does not change the comparison in (17), because its common factor `R`
cancels. A reuse crossover can arise when the total workload/budget
increases with `R`, as in a fixed per-profile budget `B=R b`.

An equivalent fixed-accuracy formulation is often clearer. For target
expected squared profile loss `ε²>0`, the continuous model requires
`n_i=\overline V_i/ε²` and total cost

\[
C_i(\epsilon,R)=h_i+R P_i/\epsilon^2.
\]

Thus method `a` is cheaper at that target exactly when

\[
h_a-h_b<R\Delta P/\epsilon^2. \tag{19}
\]

For `ΔP>0`, the strict break-even condition is
`R>ε²(h_a−h_b)/ΔP`, with `R` a positive integer. This is algebra under
the stated cost/variance inputs, not a statistical estimate of when a
measured implementation will become faster.

Integer counts require the actual allocation
`n_i=floor((B-h_i)/(R c_i))≥1` and loss `\overline V_i/n_i`; the
continuous formulas approximate that staircase. Per-profile overhead
that cannot be shared should be included as `R d_i`, giving available
sampling budget `B-h_i-R d_i`. It should not be silently charged only
once as reusable setup.

Complete every scheduled sample. Random execution cost correlated with
the output does not invalidate (1) or linear expected cost for fixed
counts. Stopping at a realized wall-clock deadline, discarding unfinished
trees, or substituting median timing for expectation changes the model.
Calibration and evaluation should therefore be separated, counts frozen,
and predicted and realized costs reported independently.

The exact profile-certificate construction/checking cost is distinct
from a cheap grid short-time or finite-depth selector's cost. If a
benchmark omits certificate construction as offline validation, its
performance result concerns that deployed selector and workload. It
cannot simultaneously claim that online certification was free.

## 6. Unequal sample allocation changes the optimization target

Let point `j` have per-tree cost `c_j>0`. With a continuous sampling
budget `C=Σ_jc_j n_j`, Cauchy–Schwarz gives

\[
\left(\sum_j\sqrt{w_j V_j c_j}\right)^2
\le\left(\sum_j\frac{w_jV_j}{n_j}\right)
\left(\sum_jc_jn_j\right).
\]

When every `w_jV_j>0`, equality yields

\[
n_j^*=\frac{C\sqrt{w_jV_j/c_j}}
{\sum_k\sqrt{w_kV_kc_k}},\qquad
\min\mathbb E\mathcal L=
\frac{\left(\sum_j\sqrt{w_jV_jc_j}\right)^2}{C}.
\tag{20}
\]

Zero-weight or zero-variance coordinates require separate minimum-count
handling; integer rounding must preserve the budget and the actual
loss should be recomputed. Counts based on pilot variance estimates
also require a frozen independent evaluation phase.

Joint rate selection under this allocation minimizes
`(Σ_j√(w_j V_j(λ)c_j(λ)))²`, not the fixed-weight second-moment sum
`J(λ)`. Even if all costs are equal, the square roots change the
objective. Allocating fixed unequal counts instead gives the effective
weights `w_j/n_j` from Section 1. Assigning equal budget to each point
is another policy and should not be confused with either equal sample
counts or the allocation optimum (20).

The initial profile experiment should retain equal counts to isolate
the effect of tuning the intended grid objective. Unequal allocation
is a subsequent direction, with its own calibration cost and validation.
Finite second-moment certificates do not by themselves provide
concentration for noisy estimates of those second moments; a pilot
allocation or cost advantage needs its own uncertainty assessment.

## 7. Interpretation for the next benchmark

A clean comparison retains default rate `1`, the point short-time rate
`0.75`, the existing point-selected rate, the grid short-time rate (6),
and a rate selected against the same weighted grid. Freeze each policy
and charge its actual construction cost. Use the same five-point loss,
complete profile requests, and independently calibrated fixed counts.

The equal-count phase asks whether profile tuning reduces the intended
profile variance. The budget/reuse phase asks whether that change pays
for its setup and sample costs. The exact certificate answers the
mathematical objective question for its fixed scope; the replicated
benchmark answers a separate empirical workload question. Neither
answer should be substituted for the other, and neither establishes a
claim for nonuniform proposals, other grids, other horizons or different
sample-allocation rules.
