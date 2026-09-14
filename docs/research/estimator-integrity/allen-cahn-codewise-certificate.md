# Codewise full-tree moment certificates for Allen–Cahn

**Status:** conventional derivation for the exact raw one-dimensional
`SemilinearMechanism`, with a rational-arithmetic verification procedure.
A floating-point ODE trajectory is not a certificate. Any concrete numerical
claim requires the saved verifier output for the specified parameters. This
note does not claim publication novelty or a Lean formalization of the
probability model.

The estimator, depth convention and coefficient encoding are those of
[the moment theorem](notation-and-moment-theorem.md). This sharpens the
all-code scalar bound in [general rate selection](general-rate-selection.md)
by retaining six distinct code classes. The target benchmarks are
`allen_cahn_flat(phi0=0.5, T=0.05)` and `allen_cahn_wave_1d(T=0.05)`.

## 1. Estimator identity and normalized code family

Fix `f(z)=z-z³`, diffusion generator `½ ∂xx`, a common exponential lifetime
rate `λ>0`, and uniform sampling over the **raw** labelled tuples returned
by `SemilinearMechanism.tuples`. Write `D=Dx(1)` and `F_k^a=FDeriv(a,k)`.
The reachable family from `Id` is

\[
\mathrm{Id},\quad D,\quad F_0^a,F_1^a,F_2^a,F_3^a,
\]

plus absorbing zero derivative codes `F_k^a` for `k≥4`. No second spatial
derivative code is generated. Zero scalar codes have zero functional and
are never divided by their scalar.

For every nonzero `a`, normalized absolute-square moments of `F_k^a` are
those of `F_k^1`, multiplied by `a²`. This follows by coupling the same
clocks, tuple labels and motions: every nonzero branch transports the
parent scalar into exactly one child; the diffusion label introduces an
additional factor `−½`. Induction proves scalar homogeneity at finite
depth, then passage to full depth proves it for the full functional. The
uniform tuple probabilities are independent of `a`, which is essential
for this equality. A proposal depending on the scalar needs its own
argument or a uniform upper bound across scalars.

The raw table is

\[
\begin{aligned}
\mathrm{Id}&\longrightarrow(F_0^1),\\
D&\longrightarrow(F_1^1,D),\\
F_k^a&\longrightarrow(F_0^1,F_{k+1}^a)
\quad\text{or}\quad(D,D,F_{k+2}^{-a/2}).
\end{aligned}
\]

The two `F` alternatives each have probability `½`, including when one
or both alternatives contain a zero code. Consequently `F₂` retains an
inverse-probability factor `2` on its first, live label. Pruning a selected
zero subtree leaves that factor unchanged. Removing a zero label before
sampling and renormalizing the table defines a different estimator; it
would change the `F₂` coefficient below from `2` to `1`.

At `F₃` every branch contributes zero, but a surviving leaf contributes
`−6a exp(λτ)`. Thus its normalized second moment is exactly
`36 exp(λτ)`, not the constant `36`. Constant-source branches cannot simply
be suppressed without changing the functional.

## 2. The six-dimensional positive system

Let `N` count branch clock expiries and let `r≥1`. For remaining time `τ`,
use the normalized tilted moments

\[
Y(\tau,x)=
\left(
\mathbb E[r^N|H_{\mathrm{Id}}|^2],
\mathbb E[r^N|H_D|^2],
\mathbb E[r^N|H_{F_0^1}|^2],\ldots,
\mathbb E[r^N|H_{F_3^1}|^2]
\right).
\]

The state order throughout is `(Id,D,F₀,F₁,F₂,F₃)`. Define the polynomial
map on the nonnegative orthant by

\[
G(i,d,a,b,c,e)=
\begin{pmatrix}
a\\
bd\\
2ab+\tfrac12 d^2c\\
2ac+\tfrac12 d^2e\\
2ae\\
0
\end{pmatrix}. \tag{1}
\]

The `½` coefficients are `(1/q)×(−½)² = 2×¼`; the two `D` children give
`d²`, retaining their multiplicity. The exact finite-depth recursion,
with zero seed `Y₀=0`, is

\[
Y_{n+1}(\tau,x)=e^{\lambda\tau}P_\tau A_{\rm term}(x)
+\frac r\lambda\int_0^\tau e^{\lambda s}
 P_s[G(Y_n(\tau-s,\cdot))](x)\,ds. \tag{2}
\]

Here `A_term(x)` contains the six squared terminal factors. The product is
inside the same Markov expectation: siblings share their birth position.
`Y_{K+1}` is the tilted moment of the functional killed when a particle at
generation `K` branches. In particular it corresponds to full-tree depth
at most `K`, under the notation of the moment theorem.

Take any spatially uniform terminal bound `A≥A_term(x)`. For the wave,
valid exact bounds are

\[
A_{\rm wave}=(1,1/16,4/27,4,36,36). \tag{3}
\]

Indeed `−1≤φ≤0` and `|φ′|≤¼`; with `z=φ`, the maximum of
`z²(1−z²)²` on `[-1,0]` is `4/27`, attained when `z²=1/3`.
The maxima of `(1−3z²)²`, `36z²`, and `36` give the remaining entries.
These bounds apply to every Brownian state, without a spatial cutoff.
They are separate coordinate maxima; they need not occur at one state.

For constant terminal value `p`, the terminal vector is exactly

\[
A_{\rm flat}(p)=
\bigl(p^2,0,(p-p^3)^2,(1-3p^2)^2,36p^2,36\bigr).
\tag{4}
\]

At `p=½` this is `(¼,0,9/64,1/16,9,36)`. In this particular semilinear
closure, every `D` branch contains a descendant `D`, so zero derivative
terminal data imply that all `D` subtrees have zero functional. This is
a structural statement about this closure, not a general rule that a
vanishing terminal derivative makes its code identically zero.

The candidate ODE is

\[
y'=F_{\lambda,r}(y):=\lambda y+\frac r\lambda G(y),
\qquad y(0)=A. \tag{5}
\]

Every coefficient of `G` is nonnegative. Therefore `G` and `F` are
coordinatewise monotone on the nonnegative orthant and `F≥0` there.
They are locally Lipschitz, being polynomials. A finite solution to (5)
is a spatially uniform majorant; existence through the requested horizon
must be established, not inferred from the finiteness of a numerical run.

## 3. Full-tree upper-bound theorem

**Theorem.** Suppose there is an absolutely continuous, nonnegative vector
`U:[0,T]→R⁶` satisfying

\[
U(0)\ge A,\qquad U'(\tau)\ge F_{\lambda,r}(U(\tau))
\quad\text{for almost every }\tau. \tag{6}
\]

Then every finite-depth tilted moment satisfies `Y_n(τ,x)≤U(τ)` and

\[
\mathbb E_\lambda[r^N|H_{\mathrm{Id}}|^2]\le U_{\mathrm{Id}}(\tau),
\qquad
\mathbb E_\lambda[r^N|H_{F_k^a}|^2]\le a^2U_{F_k}(\tau),
\tag{7}
\]

with the corresponding derivative bound, for every starting state and
`0≤τ≤T`.

**Proof.** Multiplication of (6) by `exp(−λτ)` and integration give

\[
U(\tau)\ge e^{\lambda\tau}A+
\frac r\lambda\int_0^\tau e^{\lambda s}G(U(\tau-s))\,ds.
\]

Equation (2), monotonicity of `G`, and the fact that the Markov semigroup
preserves constants prove `Y_n≤U` by induction from `Y₀=0`. Bounded
arity (at most three) and a common finite exponential rate ensure
nonexplosion on finite horizons. The tilted killed moments increase to
the tilted full moment by the full-tree depth indicators and monotone
convergence. This proves (7). Zero-valued trees contribute zero whatever
branch count convention is used inside a pruned zero subtree. ∎

For the wave, (5) generally bounds the exact spatial moments rather than
equalling them. For flat data, the spatial Markov semigroup acts on
constants and (2) becomes the finite-dimensional Volterra iteration for
(5). Once (6) supplies finiteness, its increasing limit satisfies the
finite Volterra equation, is continuous and differentiable, and solves
(5). Local Lipschitz uniqueness identifies it with the ODE solution on
`[0,T]`. Thus validated **lower and upper** ODE enclosures bound the exact
full-tree flat moments. The finiteness argument precedes this
identification; finite-depth convergence alone does not give a finite
answer.

The result concerns moments of the specified estimator. Identifying its
mean with the PDE solution remains a separate obligation, as in the
[general-rate note](general-rate-selection.md#pde-identification-is-a-separate-step).

## 4. An exact rational verifier

The polynomial system permits certificates using rational arithmetic
only; evaluating an exponential is unnecessary for the main upper bound.
Let a positive rate interval be `λ∈[ℓ,u]`, with rational endpoints, and
fix rational `r≥1`. On nonnegative vectors set

\[
F^-(z)=\ell z+\frac r uG(z),\qquad
F^+(z)=u z+\frac r\ell G(z). \tag{8}
\]

Then `F⁻(z)≤F_{λ,r}(z)≤F⁺(z)` for every rate in the interval. The
upper and lower systems are enclosures; neither is the true rate-dependent
ODE unless the interval is a point.

### Upper steps

Starting with a rational upper endpoint `a`, choose rational `h>0` and
`b≥0` and verify the six inequalities

\[
b\ge a+hF^+(b). \tag{9}
\]

The affine segment `U(t_j+s)=a+s(b−a)/h`, `0≤s≤h`, is increasing,
nonnegative and bounded by `b`. Its slope satisfies

\[
U'=(b-a)/h\ge F^+(b)\ge F^+(U)\ge F_{\lambda,r}(U).
\]

Concatenating accepted segments gives exactly the supersolution required
by (6), simultaneously for the entire rate interval. The final `b` also
bounds all previous times because the path is increasing. A final
partial step is needed if the horizon is not an integer multiple of the
chosen step.

One way to propose `b` is iteration of
`b ← ceil_grid(a+h F⁺(b))` on a fixed rational grid, beginning at `a`.
This is only a candidate-generation method. Acceptance is the exact test
(9); a maximum iteration count, numerical closeness, or convergence of
floating-point iterates cannot replace it. If candidate generation fails,
reduce `h` or report inconclusive. Failure of this particular certificate
is not evidence that the actual moment diverges.

### Lower steps for flat moments

Starting from a rational lower endpoint `a⁻`, set

\[
a^-_{\rm next}=\operatorname{floor}_{\rm grid}
\left(a^-+hF^-(a^-)\right). \tag{10}
\]

This is a valid lower bound for the flat full moment at the next time.
To see this, the exact moment solution `y` is nonnegative and increasing
because `F_{λ,r}(y)≥0`. If `a⁻≤y(t_j)`, then

\[
y(t_j+h)=y(t_j)+\int_0^h F_{\lambda,r}(y(t_j+s))\,ds
\ge a^-+hF^-(a^-).
\]

Rounding downward preserves the inequality. Start from the exact terminal
vector (4), rounded down if necessary. The upper enclosure establishes
finiteness first. A lower solution started from the wave's coordinatewise
**upper** terminal vector (3) is not a lower bound for wave moments.

### What the verifier must record

A reproducible certificate records the exact estimator identity, `A`,
rate interval, tilt, horizon, rational grid, accepted step endpoints,
and the result of all inequalities (9). Integers or numerator/denominator
strings preserve exactness when serializing. Float conversion is allowed
for display only, with outward rounding if the display itself claims a
bound. The verifier should reject unsupported mechanisms, invalid rate
intervals, a mismatched terminal vector, and any unverified final step.

For a fixed-rate tilted certificate at both endpoints `ℓ,u`, one may
instead use log-convexity of `Eλ[r^N H²]` to obtain a uniform bound equal
to the larger endpoint certificate. This requires the same tuple law and
estimator throughout the interval. Direct use of (8) is simpler to verify
but may be more conservative.

## 5. Two rigorous omitted-depth bounds

The existing tilted-progeny argument gives, for any uniform certificate
`C_r≥sup_{λ∈I,x} Eλ[r^N H²]` with `r>1`,

\[
0\le M(\lambda,x)-M_K(\lambda,x)
\le C_r r^{-(K+1)}. \tag{11}
\]

Here `M_K` is the **exact** killed-depth moment. A branch count is not a
depth; the argument uses only that depth greater than `K` requires at
least `K+1` branches.

A finite codewise certificate also gives a useful factorial alternative.
This second bound needs only `r=1`. Suppose a constant vector `B` bounds
all full ordinary moments for `τ≤T`, all states, and all rates under
consideration; a final rational upper endpoint from Section 4 does so.
Let `J=DG(B)`. Explicitly, with `B=(i,d,a,b,c,e)`,

\[
J=\begin{pmatrix}
0&0&1&0&0&0\\
0&b&0&d&0&0\\
0&dc&2b&2a&d^2/2&0\\
0&de&2c&0&2a&d^2/2\\
0&0&2e&0&0&2a\\
0&0&0&0&0&0
\end{pmatrix}. \tag{12}
\]

For `0≤w≤v≤B`, the fundamental theorem of calculus along the line segment
between `w` and `v` gives

\[
0\le G(v)-G(w)\le J(v-w). \tag{13}
\]

All partial derivatives are nonnegative polynomials, so their values on
the segment are bounded by their values at `B`. Repeated child codes
are already accounted for by the derivatives in (12).

Let `E_n(τ)` be the vector of spatial suprema of `Y(τ,x)−Y_n(τ,x)` at
`r=1`. The full recursion and (13) imply

\[
E_1(\tau)\le\frac1\lambda\int_0^\tau e^{\lambda s}G(B)\,ds,
\qquad
E_{n+1}(\tau)\le\frac1\lambda\int_0^\tau
 e^{\lambda s}J E_n(\tau-s)\,ds. \tag{14}
\]

Iterating, the `K+1` positive time increments lie in a simplex of volume
`τ^{K+1}/(K+1)!`; their sum is at most `τ`, so the product of exponential
kernels is at most `exp(λτ)`. Since `M_K=Y_{K+1,Id}`, this proves

\[
\boxed{
\sup_x\bigl(M(\lambda,x)-M_K(\lambda,x)\bigr)
\le
\frac{e^{\lambda T}(T/\lambda)^{K+1}}{(K+1)!}
\left[J^K G(B)\right]_{\mathrm{Id}}.
} \tag{15}
\]

For `λ∈[ℓ,u]`, replace the scalar prefactor by
`exp(uT)(T/ℓ)^{K+1}/(K+1)!` and use the common `B`. If `uT<1`, the
rational inequality `exp(uT)≤1/(1−uT)` gives a wholly rational bound.
More generally, for rational `x≥0` and any positive integer `m>x`,

\[
e^x=\bigl(e^{x/m}\bigr)^m\le (1-x/m)^{-m}. \tag{16}
\]

Indeed the exponential power series is bounded term by term by the
geometric series when `0≤x/m<1`, because `1/n!≤1`. Raising this
nonnegative inequality to the integer power `m` proves (16). Substituting
`x=uT` gives a rational exponential upper bound at any horizon, with no
unverified floating-point transcendental call. The chosen integer `m`
should be recorded with a numerical depth-tail certificate.

This factorial decay is a consequence of an already-established finite
full-moment box and the fixed finite polynomial closure. It is not a
standalone proof of finiteness and does not extend automatically to an
unbounded code family. It can be compared with (11), retaining the smaller
verified bound. A time-dependent Jacobian enclosure can sharpen (15),
but requires an additional validated integral calculation.

## 6. Consequences and remaining obligations

A successful upper certificate at `r=1` establishes finite unrestricted
second moments at the stated rate or interval. A successful certificate
at `r>1` additionally supplies the progeny control used in rate
regularity and omitted-depth estimates. Neither statement by itself
certifies that an approximate rate is near-optimal.

For the flat benchmark, validated lower and upper endpoint integration
can be used directly in interval subdivision over rates. An incumbent
upper bound and the minimum of valid lower bounds over a rate cover
certify an objective gap on that cover.

For this flat benchmark, an entirely rational exterior exclusion can
upgrade the interval result to a global one. The no-branch topology and
the topology with exactly one `Id→F₀` branch followed by a surviving
`F₀` child are disjoint. Their exact contributions give

\[
M(\lambda)\ge e^{\lambda T}
\left[p^2+\frac{T(p-p^3)^2}{\lambda}\right]. \tag{17}
\]

For the second topology, a branch at time `s` and a surviving child have
probability density `λ exp(−λT) ds`, while the functional is
`f(p) exp(λT)/λ`; multiplying its square by this density and integrating
`s∈[0,T]` gives the second term in (17).

Thus, for a proposed search interval `[a,b]⊂(0,∞)`,

\[
\begin{aligned}
\lambda\le a&\implies
M(\lambda)\ge p^2+T(p-p^3)^2/a=:L_{\rm left},\\
\lambda\ge b&\implies
M(\lambda)\ge p^2(1+bT)=:L_{\rm right}.
\end{aligned} \tag{18}
\]

The first line uses `exp(λT)≥1`, and the second uses only the survival
term and `exp(λT)≥1+λT`. More generally, if `L_I` is a certified lower
bound on `inf_{λ∈[a,b]} M(λ)` and `U` bounds the selected rate's moment,
then

\[
L_{\rm global}:=\min(L_I,L_{\rm left},L_{\rm right})
\le\inf_{\lambda>0}M(\lambda),
\qquad
M(\widehat\lambda)-\inf_{\lambda>0}M(\lambda)
\le U-L_{\rm global}.
\]

This argument uses infima only: attainment of an optimum is not needed.
If the incumbent `U` is strictly below both exterior lower bounds, no
rate outside `[a,b]` can improve that incumbent, so the certified interval
excess bound is also a global excess bound. For `p=½`, `T=1/20`, and
`[a,b]=[1/5,2]`,

\[
L_{\rm left}=73/256=0.28515625,
\qquad L_{\rm right}=11/40=0.275. \tag{19}
\]

Hence **any verified incumbent upper bound below `11/40`** suffices for
this global upgrade. The actual comparison with the incumbent must be
performed and recorded in exact arithmetic; the theorem does not turn
an unchecked decimal output into a certificate. For other parameters,
(18) may be too weak and the global conclusion must remain unclaimed.

For the wave, (3) loses spatial dependence. It certifies a full-tree
moment envelope and the depth tail, but does not by itself certify the
Gaussian/time quadrature error `δ` in the finite-depth objective. To use

\[
M(\widehat\lambda)-\inf_{\lambda\in I}M(\lambda)
\le\text{verified depth tail}+2\delta+\eta,
\]

one still needs a uniform numerical integration error and an objective
optimization error `η`. A finite scalar ODE bound, a plot of a smooth
curve, or a change smaller than the quadrature tolerance does not supply
these quantities. Also keep mean/PDE identification, floating-point
sampler effects, confidence statements for empirical squared weights,
and total-runtime comparisons separate from the analytic moment theorem.

The appropriate next computational checks are: verify raw transition
coefficients against `mechanism.py`; produce exact rational flat and
wave certificates at the current horizon; compare independent numerical
ODE approximations only as diagnostics; quantify the depth tail; and use
the exact flat moment enclosure as the first rate-optimization oracle.
The Lean track can formalize the finite polynomial inequalities and
rational certificate acceptance theorem while explicitly leaving the
stochastic representation and analytic existence bridge outside that
formalization until those are separately completed.
