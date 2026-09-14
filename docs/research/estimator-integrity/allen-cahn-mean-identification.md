# Identifying the Allen–Cahn tree mean and its variance objective

**Status:** conventional proof for the exact raw uniform one-dimensional
`SemilinearMechanism` and the flat/wave terminal data below, conditional
on one verified six-code second-moment envelope through the requested
horizon. The current certificates at `T=0.05` supply that envelope. This
note does not formalize the stochastic argument in Lean and does not
certify floating-point roundoff in the Monte Carlo implementation.

The result discharges the common-mean assumption behind interpreting
certified second-moment objective gaps as **variance** objective gaps.
In fact, one finite all-code second-moment certificate suffices to
identify the mean at **every positive exponential rate**, including
rates whose second moments may be infinite.

## 1. Precise model and hypothesis

Fix `f(z)=z-z³`, generator `½∂xx`, horizon `T>0`, the raw labelled tuples
of `SemilinearMechanism`, and uniform tuple sampling. The root code is
`Id`. The reachable nonzero code family is

\[
\mathrm{Id},\quad D=\partial_x,\quad F_k^a=(a f^{(k)})^*,
\quad 0\le k\le3,
\]

with absorbing zero derivative codes at `k≥4`. Scalar zero also has zero
functional. Every live particle uses the same exponential rate `λ>0`.
Children share their parent's branch position and have independent future
randomness conditional on the first-event data.

The terminal data are either

\[
\phi(x)=p,\quad 0<p\le1,
\qquad\text{or}\qquad
\phi(x)=-\frac1{1+e^x}.
\tag{1}
\]

The current flat certificate uses `p=1/2`, `T=1/20`; the current wave
certificate uses `T=1/20`.

**Envelope hypothesis.** At some fixed `λ₀>0`, a finite nonnegative
vector `B` bounds the normalized second moments of **all six** codes,
uniformly over `0≤τ≤T` and every `x∈R`:

\[
\mathbb E_{\lambda_0}|H_{c,\tau,x}|^2\le B_c
\quad(c=\mathrm{Id},D,F_0^1,\ldots,F_3^1).
\tag{2}
\]

A root-only second-moment bound would not supply the six-field argument
below. The rational all-code supersolution certificates in
[the codewise note](allen-cahn-codewise-certificate.md) do supply (2),
including all earlier times, not merely their final endpoint.

The raw mechanism has at most three offspring. A common finite
exponential rate therefore gives nonexplosion on every finite horizon,
for every `λ>0`. For example, dominate the number of branching events by
a pure birth process with event rate `λ(1+2n)` after `n` events; stopping
at `n=m` and applying the expectation bound gives a uniform finite bound
on the stopped event count, hence a probability of reaching `m` before
`T` that tends to zero. Thus every realized nonzero tree has finite
depth almost surely at each rate.

## 2. Scalar normalization and rate-independent absolute integrability

The sampler's scalar factors must be retained. Couple clocks, tuple
labels and Brownian motions for `F_k^a` and `F_k^1`. On either raw
alternative, exactly one child transports the parent scalar, and the
diffusion alternative contributes its additional factor `−1/2`.
Uniform tuple probabilities and zero-derivative support are independent
of the nonzero scalar. Finite-depth induction therefore gives

\[
H_{F_k^a}^{[K]}=a H_{F_k^1}^{[K]}
\]

under that coupling, and finite-tree passage to the horizon gives the
same equality for the full functional. Signed first moments normalize
by `a`, absolute first moments by `|a|`, and second moments by `a²`.
These three conventions must not be interchanged.

Let `V_n` denote the zero-seeded vector of killed **absolute first**
moments, with `V_0=0`; `V_{K+1}` corresponds to trees killed at depth
`K`. At moment order one, first-event conditioning cancels the lifetime
survival, density, and tuple probability against their inverse weights.
Consequently

\[
V_{n+1}(\tau,x)=P_\tau|g|(x)
+\int_0^\tau P_s\mathcal A(V_n(\tau-s,\cdot))(x)\,ds,
\tag{3}
\]

where `P` is the Brownian semigroup,

\[
g=(\phi,\phi',f(\phi),f'(\phi),f''(\phi),-6),
\]

and, on nonnegative vectors,

\[
\mathcal A(i,d,a,b,c,e)
=(a,bd,ab+\tfrac12d^2c,ac+\tfrac12d^2e,ae,0).
\tag{4}
\]

In particular, **neither (3) nor its initial value depends on `λ`**.
The raw table still has two `F` alternatives, but first absolute moments
have no inverse-probability factor `2` after averaging. The diffusion
coefficient is `|−1/2|`, not its square.

The exact nonnegative first-moment recursion is valid as an extended
nonnegative integral before finiteness is known. Thus `V_n` is identical
at every positive rate. By nonexplosion, the killed absolute functionals
increase to the full absolute functional, so monotone convergence gives

\[
\mathbb E_\lambda|H_c|
=\sup_n V_{n,c}
=\mathbb E_{\lambda_0}|H_c|
\le\sqrt{B_c}<\infty
\quad\text{for every }\lambda>0.
\tag{5}
\]

The last inequality is Cauchy–Schwarz under (2). It is uniform in the
starting state and remaining time. No second-moment finiteness outside
the certified interval has been asserted or used.

Alternatively, finite-depth signed mean recursions also cancel `λ`.
Because `H^{[K]}=H 1{depth≤K}` and (5) gives integrability, dominated
convergence passes those signed means to the full tree and establishes
rate invariance directly. The following mild-system argument identifies
their actual common value.

## 3. The signed six-field mean equation

Write `h_c(τ,x)=Eλ H_{c,τ,x}` in normalized scalar-one coordinates.
Equation (5) makes every field bounded, uniformly in time and space.
At a branch, conditional independence of the children gives

\[
\mathbb E\!\left[\left|\prod_jH_j\right|
\mid\text{first-event data}\right]
=\prod_j\mathbb E[|H_j|\mid\text{first-event data}],
\]

and the right side is bounded by a product of the constants in (5),
with scalar magnitudes included. There are finitely many labels and a
finite integration horizon. Thus all branch contributions are absolutely
integrable after likelihood cancellation; conditional expectation,
Fubini and multiplication of conditional means are justified. Shared
branch positions put the product inside one Brownian semigroup.

The signed source polynomial is

\[
Q(i,d,a,b,c,e)
=(a,bd,ab-\tfrac12d^2c,ac-\tfrac12d^2e,ae,0).
\tag{6}
\]

First-event conditioning now yields the **rate-free** mild system

\[
h(\tau,x)=P_\tau g(x)
+\int_0^\tau P_s Q(h(\tau-s,\cdot))(x)\,ds.
\tag{7}
\]

Both the negative diffusion coefficient and its `1/2` magnitude are
essential. The `F₂` source has coefficient one even though its live raw
label is sampled with probability `1/2`: the probability cancels its
inverse weight in a first moment. The `F₃` mean is the constant `−6`,
while its second moment is `36 exp(λτ)`. These are consistent statements
about different moments.

The field `D` is not declared an absorbing code merely because its flat
terminal factor vanishes. In this semilinear closure every `D` branch
contains another `D`; the resulting zero functional for flat data also
follows from finite-depth induction. Keeping `D` in (7) preserves the
actual mechanism and the wave case.

## 4. The explicit PDE fields satisfy the same system

Use forward remaining time and put `v(τ,x)=u(T−τ,x)`. Then

\[
v_\tau=\tfrac12v_{xx}+f(v),\qquad v(0,x)=\phi(x).
\tag{8}
\]

For flat data, the explicit solution is

\[
v(\tau,x)=\left(1+(p^{-2}-1)e^{-2\tau}\right)^{-1/2}.
\tag{9}
\]

It is spatially constant, takes values in `[p,1]`, and differentiation
shows `v_τ=v−v³`. At `p=1` it is the constant equilibrium.

For the wave,

\[
v(\tau,x)=-\tfrac12-\tfrac12\tanh(3\tau/4-x/2).
\tag{10}
\]

Writing `z=3τ/4−x/2`, one has

\[
v_\tau=-\tfrac38\operatorname{sech}^2z,
\quad v_x=\tfrac14\operatorname{sech}^2z,
\quad v_{xx}=\tfrac14\operatorname{sech}^2z\tanh z,
\]

and

\[
f(v)=-\tfrac18\operatorname{sech}^2z(3+\tanh z).
\]

These identities verify (8) and the terminal value in (1) directly.

Define the six explicit fields

\[
w=(v,v_x,f(v),f'(v),f''(v),f'''(v)).
\tag{11}
\]

Differentiating (8) once in space gives

\[
(\partial_\tau-\tfrac12\partial_{xx})v_x=f'(v)v_x.
\]

For `a_k=f^{(k)}(v)`, the chain rule gives

\[
(\partial_\tau-\tfrac12\partial_{xx})a_k
=f^{(k+1)}(v)f(v)-\tfrac12 f^{(k+2)}(v)v_x^2.
\tag{12}
\]

Because `f⁽⁴⁾=f⁽⁵⁾=0`, equations (8) and (12) are exactly
`w_τ=½w_xx+Q(w)` with `Q` from (6), including its last two rows.
The initial vector is exactly `g`.

All six fields and the derivatives needed here are bounded and smooth
on `[0,T]×R`. In either family `|v|≤1`, `|f'(v)|≤2`,
`|f''(v)|≤6`, `f'''(v)=−6`, and `|f(v)|≤2/(3√3)`; the spatial
derivative is zero for flat data and at most `1/4` for the wave.
The heat-semigroup variation formula, justified by these bounds,
therefore puts `w` in the same bounded mild system (7).

## 5. Bounded mild uniqueness and identification

On any signed coordinate box `[-R,R]^6`, `R≥1`, the polynomial `Q` is
Lipschitz in the maximum norm. For example, a valid constant is

\[
L_R=2R+\tfrac32R^2.
\]

A product of two bounded coordinates contributes at most `2R` times
the coordinate error; a half-weighted product of three contributes at
most `3R²/2`. This also bounds the linear first row when `R≥1`.

Choose `R` large enough to contain both `h` and `w`, using (5) and the
explicit field bounds. Subtract their mild equations, use the Lipschitz
bound and sup-norm contraction of the heat semigroup, and apply Gronwall.
Equivalently, if their difference is initially bounded by a uniform
constant `C`, repeated positive integral substitution bounds it by
`C(L_R τ)^n/n!` for every `n`; this tends to zero. This version also
proves uniqueness among bounded measurable mild solutions without
assuming a time derivative of the mean field in advance.

Hence `h=w`. In particular,

\[
\boxed{\mathbb E_\lambda H_{\mathrm{Id},\tau,x}=v(\tau,x)
=u(T-\tau,x)\quad\text{for every }\lambda>0.}
\tag{13}
\]

The same argument identifies the derivative and composition-code means,
and scalar homogeneity identifies `F_k^a` with `a f^{(k)}(v)`.
The conclusion holds for the flat/wave horizons for which hypothesis
(2) is available. It is not an automatic identification theorem for
arbitrary smooth nonlinearities, unbounded terminal factors or a
changed tree representation.

## 6. Consequence for global variance certificates

Fix the root and let its common mean be `μ=v(τ,x)`. Equation (5) gives
finite absolute mean for every positive rate. Therefore, in extended
nonnegative values,

\[
\operatorname{Var}_\lambda(H)=M(\lambda)-\mu^2,
\qquad M(\lambda)=\mathbb E_\lambda H^2.
\tag{14}
\]

For finite second moments this is the usual identity. For an infinite
second moment, subtracting the integrable cross term cannot make
`E(H−μ)²` finite, so both sides are infinite. A finite incumbent makes
the infimum of `M` finite. Consequently a certified finite incumbent
satisfies

\[
\boxed{
\operatorname{Var}_{\widehat\lambda}(H)
-\inf_{\lambda>0}\operatorname{Var}_\lambda(H)
=M(\widehat\lambda)-\inf_{\lambda>0}M(\lambda).
}
\tag{15}
\]

The same identity holds with an interval in place of all positive rates.
Thus the saved full-tree second-moment gap is also an additive variance
gap for these estimators. It does not certify the distance between the
selected rate and an optimizer, or a runtime improvement.

No numerical evaluation of `μ` is needed to transfer an **objective
gap** through (15). Reporting an absolute numerical variance by
subtracting an evaluated `μ²` additionally requires a sufficiently
accurate, outward-rounded evaluation of the explicit formula. Finally,
this theorem concerns the mathematical sampler with exact real
arithmetic; floating-point terminal evaluation, multiplication and
exponentials require their own analysis if a machine-arithmetic bias
claim is desired.
