# T01 — Terminal-code perturbation and the scope of a slab interface

Date: 27 September 2026. Role: independent theory review. Requested research
model/effort: `gpt-6-astra` / max; serving-model identity is not independently
verified. This note owns no Lean or numerical implementation. Existing dirty
files were read, not changed. The requested sequence is theory → Lean → code.

**Verdict.** The proposed finite-tree perturbation inequality and its
inflated-envelope stochastic lift are correct. They give a conditional
interface theorem for code families. They do not themselves establish that a
generic fully nonlinear PDE has an admissible terminal-code envelope after
each slab. For the present one-dimensional scalar Allen–Cahn
`SemilinearMechanism`, the normalized code family is genuinely finite: it
contains only `Id`, `Dx(1)`, and four nonlinear observables. A bounded C¹
interface contract therefore controls every terminal code in this specific
mechanism. The useful composition constants come from leaf-marked moments;
the inflation argument supplies a robust finiteness certificate.

## 1. Exact finite-tree statement

Let a realized finite tree have a list of terminal factors indexed by
`j=1,…,n`. Repeated codes and repeated spatial states are separate factors.
Write the terminal code/state pairs as `(c_j,x_j)`. All tree topology,
positions, nonterminal coefficients and likelihood factors are common to the
two evaluations. Their product is a finite real number `A`. In the coding
tree, reciprocal sampling densities and probabilities are positive; the
argument also permits signed coefficients in `A`.

For finite, nonnegative bounds `B_c(x)` and a number `ε≥0`, assume at every
factor

\[
|b_c(x)|\le B_c(x),\qquad
|\widetilde b_c(x)|\le B_c(x),\qquad
|b_c(x)-\widetilde b_c(x)|\le\varepsilon B_c(x).
\tag{1}
\]

Define

\[
H_b=A\prod_{j=1}^n b_{c_j}(x_j),\quad
H_{\widetilde b}=A\prod_{j=1}^n\widetilde b_{c_j}(x_j),\quad
W_B=|A|\prod_{j=1}^n B_{c_j}(x_j).
\]

Then

\[
|H_b-H_{\widetilde b}|\le\varepsilon nW_B,
\qquad |H_b|\vee|H_{\widetilde b}|\le W_B.
\tag{2}
\]

**Proof.** Telescope the product difference, replacing one factor at a time.
The `j`th summand has absolute value at most
`ε B_{c_j}(x_j) ∏_{i≠j} B_{c_i}(x_i) = ε ∏_i B_{c_i}(x_i)`.
Sum its `n` terms and multiply by `|A|`. No bound is divided by. Equivalently,
induct on the list using
`aP−bQ=(a−b)P+b(P−Q)` and the triangle inequality. ∎

The algebra needs neither independence nor a probabilistic tree law. It also
gives the saturation bound `|H_b−H_b̃|≤min(εn,2) W_B`.

For `r>1`, Bernoulli's inequality gives

\[
1+n(r-1)\le r^n,
\qquad n\le\frac{r^n-1}{r-1}\le\frac{r^n}{r-1}.
\]

Since `W_{rB}=r^n W_B`,

\[
|H_b-H_{\widetilde b}|
\le\frac\varepsilon{r-1}W_{rB}.
\tag{3}
\]

Here `rB` multiplies **every terminal factor bound** by `r`; it is not a tilt
by the number of branch events.

### Zero bounds and zero terminal factors

- If a factor has `B_c(x)=0`, (1) forces both terminal evaluations to vanish.
  Both products and `W_B` are zero. Formula (2) remains exact.
- If `n=0`, the empty product is one, so both functionals equal `A` and the
  difference is zero. Do not assign zero to an empty product.
- A killed/pruned tree that returns zero should be encoded with a common
  killing indicator or `A=0`. Absence of terminal factors alone does not
  encode killing.
- Bounds `B=0` are compatible with the theorem, but normalized error ratios
  require a convention: a zero denominator allows only zero numerator.

An asymmetric version is available if only `|b|≤B` is known: a relative error
bound gives `|b̃|≤(1+ε)B`, and the product estimate changes accordingly. One
must not silently use (2) with the original `B` in that case.

## 2. Stochastic lift and generation limits

Fix a root code, starting time and state. Assume the tree is finite almost
surely; its terminal count is `N`. Assume the two functionals and envelopes
are measurable, their likelihood factors are finite on sampled events, and
(1) holds almost surely for every encountered terminal factor. Uniform
pointwise bounds over all reachable code/state pairs are an easy sufficient
way to obtain this last property.

If

\[
\mathbb E W_{rB}^2\le M<\infty,
\tag{4}
\]

then `H_b,H_b̃∈L²` and

\[
\|H_b-H_{\widetilde b}\|_2
\le\frac\varepsilon{r-1}\sqrt M,
\qquad
|\mathbb EH_b-\mathbb EH_{\widetilde b}|
\le\frac\varepsilon{r-1}\sqrt M.
\tag{5}
\]

**Proof.** Square (3), integrate, and take square roots. The individual
functionals are dominated by `W_B≤W_{rB}`. The mean bound follows from
`|EX|≤E|X|≤||X||₂` on a probability space. ∎

There are sharper quantities:

\[
P_B:=\mathbb E[NW_B],\qquad Q_B:=\mathbb E[N^2W_B^2].
\]

Whenever these are finite,

\[
|\mathbb EH_b-\mathbb EH_{\widetilde b}|\le\varepsilon P_B,
\qquad
\|H_b-H_{\widetilde b}\|_2\le\varepsilon\sqrt{Q_B}.
\tag{6}
\]

Assumption (4) implies `Q_B≤M/(r−1)²` and finiteness of `P_B`.
For a zero-width slab with one terminal factor, `P_B=B_root` and
`Q_B=B_root²`. Thus normalized constants from (6) tend to one as the width
tends to zero. The coarse constant in (5) need not have this property.

### What an all-generation certificate actually proves

Use the project’s killed-depth convention. On a full finite tree let
`E_K={depth≤K}` and `H_b^[K]=H_b 1_{E_K}`; similarly define
`W_{rB}^[K]=W_{rB}1_{E_K}`. The events increase to the whole sample space under
nonexplosion. If a proof supplies

\[
\sup_K\mathbb E[(W_{rB}^{[K]})^2]\le M,
\]

monotone convergence gives (4). Dominated convergence then gives
`H_b^[K]→H_b` and `H_b̃^[K]→H_b̃` in L². Signed expectations may now be
passed to the limit. A uniform finite-depth bound becomes a full-tree bound
only with this coupling and an established nonexplosion/limit argument.

If infinitely many events can occur before the horizon, a product over the
finite terminal factors has not defined the desired estimator on that event.
One needs a separately specified limit, convergence and integrability
theorem. A uniform L² bound on arbitrary truncations alone does not imply L²
convergence. In the present Allen–Cahn mechanism, at most three children and a
common finite exponential rate give nonexplosion on any finite time interval.
For general state/code-dependent rates, pointwise finiteness of each rate
does not suffice; uniformly bounded rates with bounded arity are sufficient.

## 3. The actual slab-interface contract

Let `C` contain every code that can appear at the terminal boundary of the
slab for the requested root codes. Let `R` contain every root code required
by the preceding slab. For a code family `e`, define the weighted domination
gauge

\[
\|e\|_B:=\inf\{\varepsilon\ge0:
 |e_c(x)|\le\varepsilon B_c(x)\text{ for all relevant }(c,x)\}.
\tag{7}
\]

For positive bounds this is the usual supremum of normalized errors. With
zeros it is an extended-valued gauge with the zero-denominator convention
above. The state set must cover the Brownian terminal support; checking only
a finite spatial plotting grid does not supply (7).

Define the code-family propagation operator, without yet asserting a PDE
identity, by

\[
\mathcal T_h b(c,x):=\mathbb E H_{b;c,h,x}.
\]

For chosen output weights `D_c(x)`, suppose the relevant full-tree quantities
satisfy

\[
P_{B;c,h,x}\le L_hD_c(x)
\quad\text{for every }c\in R,x.
\tag{8}
\]

Then (6) proves the genuine interface estimate

\[
\|\mathcal T_h b-\mathcal T_h\widetilde b\|_D
\le L_h\|b-\widetilde b\|_B,
\tag{9}
\]

on the admissible class `|b|,|b̃|≤B`. The L² version uses
`sqrt(Q_{B;c,h,x})≤L_h^{(2)}D_c(x)` for coupled root functionals.
One can instead use the weaker sufficient condition
`sqrt(M_{rB;c,h,x})≤(r−1)L_h^{(2)}D_c(x)`.

For composition, also prove or assume that each exact and approximate
interface remains in the next slab's admissible class. A sufficient
code-family self-map condition is
`E W_{B;c,h,x}≤D_c(x)` together with an approximation procedure whose output
also obeys `|b̃_out|≤D`. More informative PDE invariants can replace this
conservative positive-envelope condition. Merely proving (9) supplies
neither condition.

If local approximation errors `η_j` and interface errors `e_j` are measured
in these compatible code-family gauges, the elementary backward recurrence is

\[
e_j\le\eta_j+L_j e_{j+1},\qquad
e_0\le\sum_{j=0}^{m-1}\eta_j\prod_{i=0}^{j-1}L_i
+e_m\prod_{i=0}^{m-1}L_i.
\tag{10}
\]

Empty products in this formula are one. The `η_j` must bound the output
family needed by the preceding slab. A pointwise Monte Carlo standard error
at a finite set of `Id` queries is not a certified uniform code-family
approximation error.

For one fixed root and a deterministic approximate interface, an average of
`m` independent trees obeys

\[
\operatorname{RMSE}(\overline H_{\widetilde b},\mathbb EH_b)^2
\le\frac{\mathbb E W_B^2}{m}
+\varepsilon^2P_B^2.
\tag{11}
\]

This follows by the exact variance-plus-squared-bias decomposition. It is a
pointwise sampling statement, separate from constructing a spatially uniform
interface. A random fitted interface can be treated conditionally if the
bounds hold conditionally and fresh tree samples are used. If only a
high-probability fitting certificate holds, the complement event needs its
own error bound; it cannot be discarded.

To identify (9) with a PDE slab, an external representation theorem must give
`T_h(c(u)(s,·))(d,x)=d(u)(s−h,x)` for every required root `d`. Root `Id` alone
does not supply derivative or nonlinear root observables. Arbitrary code
families need not have the form `c(g)` for one scalar function `g`; they may
still be propagated as a code system, but that does not make each approximate
family a coherent jet of a scalar PDE solution.

## 4. Pruning, proposals, and nesting

**Structural zero pruning.** A common exact rule based on an identically zero
operator is compatible with (2), provided both interfaces enforce that zero
code. Pruning a selected zero subtree may use a shared killing indicator.
Removing zero tuple labels before sampling and renormalizing their
probabilities changes the tree law and likelihood factors. Compare both
interfaces under that same new law, or supply a separate change-of-law
argument. Terminal-dependent approximate pruning, thresholds, or declaring a
derivative code zero merely because it vanishes at one boundary are not
covered. In particular, `B_D=0` is legitimate for the structurally persistent
`D` factor in the flat scalar semilinear example, not for arbitrary derivative
mechanisms.

**State-dependent proposals.** A shared supported proposal
`q(c,time,position,tuple)` is compatible with the pathwise theorem: the same
tree and reciprocal weights are used in both evaluations. The proposal may
depend on common history if a valid conditional law and its moment bound are
given. Conditional child independence needed by the usual moment recursion
is a separate requirement. A proposal that changes with the terminal
interface generally changes topology or `A`; identical random seeds do not
restore (2). Means can sometimes be compared under a fixed common reference
proposal, but its support, representation and moment bounds must be proved.
Zero proposal probabilities on nonzero mechanism terms invalidate the usual
PDE representation.

**Independent terminal-code nesting.** Unbounded unbiased inner estimators
usually do not satisfy the pathwise envelope (1), so the current perturbation
theorem is not a theorem for raw nested Monte Carlo. Such a construction needs
its own conditional second-moment envelopes and absolute integrability.
Products of conditionally independent unbiased estimates of each terminal
code can preserve the correct mean, including separate replicas for repeated
factors. Evaluating a nonlinear code on one noisy value or jet generally does
not. Reusing one noisy factor in a square introduces a variance term.

## 5. Closed one-dimensional Allen–Cahn specialization

Take `f(z)=z−z³`, generator `½∂xx`, the raw tuple tables, common exponential
rate `λ>0`, and uniform raw tuple probabilities. Inspection of
`parabolab/mechanism.py` confirms

\[
I\to(F_0),\qquad D\to(F_1,D),\qquad
F_k^a\to(F_0,F_{k+1}^a)\text{ or }(D,D,F_{k+2}^{-a/2}).
\tag{12}
\]

No `Dx(2)` is produced. Since `f^(k)=0` for `k≥4`, the six normalized
observable classes are `(I,D,F₀,F₁,F₂,F₃)` plus absorbing zeros. Scalar `a`
is transported through exactly one child. Under scalar-independent tuple
probabilities and common clocks, its functional is `a` times the normalized
functional. Thus there are six classes for moment and error bounds, even
though the literal scalar-bearing code set is not finite. A scalar-dependent
proposal needs a new normalization argument.

For two smooth terminal functions `g,g̃` with

\[
|g|\vee|\widetilde g|\le1,
\quad |g'|\vee|\widetilde g'|\le D_*,
\quad\|g-\widetilde g\|_\infty\le\delta_0,
\quad\|g'-\widetilde g'\|_\infty\le\delta_1,
\]

valid componentwise envelopes and errors are

\[
B=(1,D_*,2/(3\sqrt3),2,6,6),\qquad
\Delta=(\delta_0,\delta_1,2\delta_0,6\delta_0,6\delta_0,0).
\tag{13}
\]

The nonlinear differences follow from the mean value theorem and the bounds
on `f'`, `f''`, `f'''`. If `D_*>0`, one valid common relative error is

\[
\varepsilon=\max(3\sqrt3\,\delta_0,\delta_1/D_*).
\tag{14}
\]

If `D_*=0`, require `δ₁=0` and omit that ratio. Scalar-bearing codes scale
both their envelope and error by `|a|`. No higher derivative of the terminal
function occurs in this terminal contract. Smoothness/regularity needed to
identify tree means with PDE code fields remains a separate analytical
obligation; (13) does not prove it.

### Correct raw second-moment system

In the coordinate order `(i,d,a,b,c,e)=(I,D,F₀,F₁,F₂,F₃)`, define

\[
G(i,d,a,b,c,e)=
(a,bd,2ab+\tfrac12d^2c,2ac+\tfrac12d^2e,2ae,0).
\tag{15}
\]

The factor `2` is `1/q` for a raw `F` label. The diffusion coefficient is
`(1/q)(−1/2)²=1/2`; two derivative children produce `d²`. The live `F₂`
label still has probability `1/2`, hence `2ae`. Both `F₃` branch labels kill
the sample, but survival contributes the terminal value, so its squared
envelope moment is `B_F₃² exp(λh)`, not a constant.

A nonnegative supersolution for

\[
m'=F_2(m):=\lambda m+\lambda^{-1}G(m),
\qquad m(0)=r^2 B^2
\tag{16}
\]

certifies `E W_{rB,c}²` for all six roots. Squares are componentwise.
With spatially constant envelopes, the normalized positive envelope moments
equal the finite solution of this ODE once the full-tree limit is justified.
For spatially varying terminal bounds, a spatially uniform ODE envelope is
an upper bound, not automatically the exact spatial moment.

Equation (16) is an **ordinary** branch-moment equation with inflated boundary
data. The existing codewise note also uses a branch-event tilt, whose ODE is
`m'=λm+(s/λ)G(m)` with initial `B²`; that `s` is a different parameter.
If `J` counts branch events, bounded arity gives `N≤1+2J`, hence the optional
comparison

\[
\mathbb E W_{rB}^2
\le r^2\mathbb E[(r^4)^J W_B^2].
\tag{17}
\]

### Leaf-marked constants suitable for composition

Let

\[
M(z,h)=\mathbb E[z^N W_B^2],\qquad M(z,0)=zB^2.
\]

For constant envelopes and the present raw mechanism, its ODE is
`∂_h M=F₂(M)`. Suppose a finite inflated-envelope solution exists through
the requested horizon for some `z_*>1`. Nonnegative power series, or
dominated differentiation using an interior margin below `z_*`, justify
differentiation at `z=1`. Ordinary smooth dependence for the polynomial ODE
gives the same derivatives. Put

\[
m=M(1,\cdot),\quad d=\partial_zM(1,\cdot),\quad
q=d+\partial_z^2M(1,\cdot).
\]

These are respectively `E W_B²`, `E[NW_B²]`, and `E[N²W_B²]`; they obey

\[
\begin{aligned}
m'&=F_2(m),\\
d'&=DF_2(m)d,\\
q'&=DF_2(m)q+D^2F_2(m)[d,d],\\
m(0)&=d(0)=q(0)=B^2.
\end{aligned}
\tag{18}
\]

Thus the parent's proposed `Q=D+H` equation is correct; the second derivative
term has no additional factor of two. To make that coefficient checkable,
for `x=(i,d,a,b,c,e)` and direction `v`,

\[
D^2G(x)[v,v]=
\begin{pmatrix}
0\\
2v_bv_d\\
4v_av_b+c v_d^2+2d v_dv_c\\
4v_av_c+e v_d^2+2d v_dv_e\\
4v_av_e\\
0
\end{pmatrix}.
\tag{19}
\]

All right-hand sides in the augmented system are nonnegative polynomials on
the nonnegative orthant. Finite supersolutions can therefore bound the marked
moments directly, with the same finite-depth/nonexplosion bridge. An
unvalidated floating ODE trajectory is not such a certificate.

For expectation bias, use the smaller first-absolute-moment system

\[
\mathcal A(i,d,a,b,c,e)
=(a,bd,ab+\tfrac12d^2c,ac+\tfrac12d^2e,ae,0).
\]

Lifetime and tuple likelihoods cancel at moment order one. If
`V(z,h)=E[z^N W_B]`, then `V'=𝒜(V)`, `V(z,0)=zB`. Its marked derivative
`p=∂_z V(1,·)` satisfies

\[
v'=\mathcal A(v),\qquad
p'=D\mathcal A(v)p,\qquad v(0)=p(0)=B.
\tag{20}
\]

It gives `P_B=p`; this bound is independent of the common sampling rate.
With unchanged positive output weights `B`, the constants
`max_c p_c(h)/B_c` and `max_c sqrt(q_c(h))/B_c` start at one. Retain codewise
or directional errors when possible: `F₃` never changes under perturbing `g`,
so a common scalar `ε` loses information.

### The literal high-frequency test needs a larger envelope

For the traveling wave approaching `−1` at one spatial infinity,
`g̃=g+δ cos(kx)` is not globally confined to `[-1,1]` for any `δ>0`.
Using (13) unchanged would be incorrect. For `M_*:=1+δ≥1` and
`D_*:=1/4+δ|k|`, valid bounds are

\[
B=(M_*,D_*,\max\{2/(3\sqrt3),M_*^3-M_*\},3M_*^2-1,6M_*,6),
\]

with code errors bounded by
`(δ,δ|k|,(3M_*²−1)δ,6M_*δ,6δ,0)`. This explicitly exposes the derivative
cost at fixed value error. Alternatively choose an interval-preserving
perturbation and prove its own C¹ bounds. The experiment must use its actual
envelope, including all Brownian states, in the moment certificate.

### Audited rational local certificate proposed by the parent

For the narrower admissible class `|g|≤2/5`, `|g'|≤1/2`, use the safe
terminal envelope

\[
B=(2/5,1/2,2/5,1,12/5,6),\quad
\lambda=2,\quad 0\le h\le2/25,\quad r=21/20.
\tag{21}
\]

Here `|f(g)|≤|g|≤2/5`, `|f'(g)|≤1`, and `|f''(g)|≤12/5`.
For every remaining time `τ≤h`, the exponential power series gives

\[
e^{2\tau}\le\frac1{1-2\tau}\le\frac{25}{21},\qquad
\frac12\int_0^\tau e^{2s}\,ds
=\frac{e^{2\tau}-1}{4}\le\frac1{21}.
\]

Set `V=(1/4,1/2,1/2,3,12,50)`. Then

\[
G(V)=(1/2,3/2,9/2,73/4,50,0),\qquad
(25/21)r^2=21/16,
\]

and the exact rational slack is

\[
V-\left(\frac{21}{16}B^2+\frac1{21}G(V)\right)
=\left(\frac{17}{1050},\frac{45}{448},\frac{53}{700},
\frac{275}{336},\frac{1081}{525},\frac{11}{4}\right)>0.
\tag{22}
\]

**Volterra-box proof.** Start the nonnegative killed-moment iteration at
zero. If its previous iterate is bounded by `V` for every time `τ≤h` and
state, monotonicity of `G`, constant preservation by the Brownian semigroup,
and the preceding kernel bounds place its next iterate below
`(21/16)B²+G(V)/21≤V`. Induction and nonexplosion/monotone convergence give

\[
\mathbb E W_{rB;c,\tau,x}^2\le V_c
\quad(0\le\tau\le2/25,\ x\in\mathbb R)
\tag{23}
\]

for all six normalized roots. Scalar-root moments scale by `a²`. In
particular the inflated `Id` moment is at most `1/4`. This argument does not
mistake a constant box for an ODE differential supersolution: it is a
supersolution of the full finite-horizon Volterra operator.

The arithmetic and proof above are an independent conventional check of the
parent's proposed witness. T01 did not run a numerical verifier or Lean build.
This local witness is restricted to (21); it does not cover an unscaled
traveling wave or an interface that has left these bounds.

### Audited all-root PDE-mean identification without stopped exact trees

The six-code L² envelope is enough to avoid a separate stopped-exact-solution
boundary domination argument. Write `h_c(τ,x)=E H_{b;c,τ,x}`. From (23),
all these fields are bounded in absolute value by `sqrt(V_c)`. Child futures
are independent conditional on the branch time, position and selected tuple.
Consequently each child product is absolutely integrable, with its absolute
conditional expectation bounded by the product of the corresponding uniform
first-moment bounds, including scalar coefficients. There are finitely many
labels and a bounded time interval. First-event conditioning, Fubini and the
likelihood cancellations are therefore legitimate.

The result is the bounded signed mild system

\[
h(\tau)=P_\tau b+\int_0^\tau P_s Q(h(\tau-s))\,ds,
\quad
Q(i,d,a,b,c,e)=(a,bd,ab-\tfrac12d^2c,ac-\tfrac12d^2e,ae,0).
\tag{24}
\]

For a smooth scalar solution `v_τ=½v_xx+f(v)` with terminal input `g`, put
`w=(v,v_x,f(v),f'(v),f''(v),f'''(v))`. The relevant chain rules are

\[
(\partial_\tau-\tfrac12\partial_{xx})v_x=f'(v)v_x,
\quad
(\partial_\tau-\tfrac12\partial_{xx})f^{(k)}(v)
=f^{(k+1)}(v)f(v)-\tfrac12 f^{(k+2)}(v)v_x^2.
\]

They give exactly `Q`, including the negative diffusion terms and the final
zero row. Assuming the regularity needed for these fields to satisfy the
heat-semigroup variation formula, `w` solves (24) with the same input.
For smooth bounded data in (21), familiar scalar comparison and the
linearized derivative equation give
`|v(τ)|≤(2/5)e^τ` and `|v_x(τ)|≤(1/2)e^τ` on this slab; these ensure that all
six actual fields are bounded. The representation proof only needs this
boundedness, not that the interior fields fit the original terminal envelope
or the leaf-inflation factor `21/20`.

**Bounded mild uniqueness.** On a finite coordinate box containing both
`h` and `w`, the polynomial `Q` has a finite Lipschitz constant `L`. Begin
with a uniform bound `|h−w|_∞≤C`. Subtract (24), apply the heat semigroup's
sup-norm contraction, and iterate the positive integral inequality. At every
state and time the difference is at most `C(Lτ)^n/n!` for every natural `n`,
hence zero. This argument works for bounded measurable mild solutions and
does not require differentiability of the mean field or measurability of an
uncountable pointwise supremum. Therefore `h=w` for **all six** normalized
roots, and scalar homogeneity gives the remaining scalar-bearing codes.

Thus the parent's simpler signed-system identification route is sound under
the stated smooth-solution/mild-identity hypothesis. Enlarging the terminal
inflation to dominate every unfinished exact-solution boundary is unnecessary
for this route. Global PDE existence and the extension from smooth data to
only C¹ data are distinct analytical claims unless separately supplied.

## 6. Hardest gap and strongest honest result

The hardest generic gap is a **reproducible admissible all-code boundary
class**: it must control every reachable terminal observable, identify every
root code needed by the previous slab, remain stable under approximation and
PDE propagation, and retain finite full-tree moments with usable constants.
For fully nonlinear mechanisms, the displayed PDE order does not bound the
reachable derivative order. A weighted analytic/Gevrey hierarchy or a proved
finite closure must be specified; a value fit or an arbitrary fixed finite
jet is insufficient.

For the present scalar Allen–Cahn mechanism, finite closure removes that
particular infinite-derivative obstruction. What still needs concrete
evidence is a C¹ approximation at the interface, moment certificates for its
actual envelopes, compatible all-code error budgets, and full computation
cost. An oracle interface proves none of the approximation-cost claims.
The finite product lemma cannot, by itself, prove larger usable `T`, global
PDE existence, an unbiased nested algorithm, or an arbitrary-horizon
continuation theorem. No novelty claim follows from it.

The strongest present statement is therefore: **under an explicit common
tree law, complete terminal-code domination, nonexplosion, full marked moment
bounds and a separate all-root representation identity, slab terminal
perturbations have the certified codewise mean and L² bounds (6)–(10). The
one-dimensional Allen–Cahn raw mechanism reduces these assumptions to six
normalized code classes with the concrete systems (15)–(20).** This is a
sound theory contract for formal algebra and subsequent certificates.

## 7. Precise elementary Lean targets

These are proposed declarations, not declarations already checked here.

1. **Finite product domination.** For a finite real list of factor triples
   `(a_i,b_i,B_i)` satisfying `B_i≥0`, `|a_i|≤B_i`, `|b_i|≤B_i`, and
   `|a_i−b_i|≤εB_i`, prove
   `|prod a−prod b|≤ε·length·prod B`. Use list induction without division.
2. **Tree prefactor.** Multiply the preceding result by `|A|`; include the
   empty list and a zero bound in the theorem, not as excluded cases.
3. **Geometric absorption.** For `n:ℕ`, `r:ℝ`, `1<r`, prove
   `(n:ℝ)·(r−1)≤r^n−1`, then the weaker bound needed for (3). Also prove
   `prod (r·B_i)=r^n·prod B_i`.
4. **Squared domination.** Given the nonnegative quantities in (3), prove
   `|H−H̃|²≤ε²/(r−1)²·W_{rB}²`. Probability and integration can remain an
   explicitly external bridge for this first formalization.
5. **Finite slab recurrence.** Unroll `e_j≤η_j+L_j e_(j+1)` with all
   quantities nonnegative into (10). A constant-`L` specialization is a
   useful smaller formal target if the varying product indexing is costly.
6. **Allen–Cahn algebra.** Check `f'=1−3z²`, `f''=−6z`, `f'''=−6`, vanishing
   higher polynomial derivatives, the tuple coefficient identities in (15),
   and the augmented polynomial identity (19). These certify algebra only,
   not code reachability or the stochastic ODE identification unless those
   objects are explicitly encoded too.
7. **Certificate acceptance.** Given the polynomial definitions and a
   nonnegative box, verify monotonicity and the algebraic rational-step
   implication used to build supersolutions. Analytic existence, integration
   and random-tree identification remain separate unless actually formalized.

Do not introduce a new axiom asserting derivative closure, a PDE solution, or
stochastic representation in order to call the whole method machine proved.

## 8. Closest sources and inspection record

- Bouchard–Tan–Warin–Zou,
  [*Numerical approximation of BSDEs using local polynomial drivers and branching processes*](https://arxiv.org/pdf/1612.06790):
  Theorem 2.4 supplies projected local-polynomial/Picard continuation;
  Proposition 2.8 controls approximation-operator errors under its
  assumptions. This is prior art for finite-slab stability, not a proof of
  the present arbitrary-code contract. Theorem 2.4, its slab projection,
  Proposition 2.8 and Remark 2.10 were reopened for this review.
- Bouchard–Tan–Warin,
  [*Numerical approximation of general Lipschitz BSDEs with branching processes*](https://arxiv.org/html/1710.10933):
  §2.2 modifies a function coherently to control value and gradient;
  Theorem 2.1 proves convergence; Proposition 3.1 gives local second moments
  under explicit lifetime/proposal choices. Its semilinear value/gradient
  assumptions do not establish arbitrary higher-derivative closure. These
  sections were reopened and checked here.
- Nguwi–Penent–Privault,
  [*A deep branching solver for fully nonlinear partial differential equations*](https://arxiv.org/html/2203.03234):
  Definition 2.1 and §2 explicitly require terminal code observables and
  include unrestricted multi-index derivative codes. Those definitions and
  their terminal evaluation rule were reopened. The generic code family is
  wider than this note's scalar semilinear closure.

Local theorem/code checks: `CLAUDE.md`, the survey `02-plan.md` and
`sources/R01-continuation.md`, `parabolab/mechanism.py`,
`estimator-integrity/allen-cahn-codewise-certificate.md`, and
`estimator-integrity/allen-cahn-mean-identification.md`. The last two existing
notes already establish the six-code normalization, raw `G` coefficients and
conditional PDE-mean correspondence for their stated benchmarks. This review
adds no claim that their saved `T=0.05` certificates apply at a new horizon.
Search was bounded to these close primary references; no comprehensive
forward-citation or worldwide novelty claim was attempted. No numerical
solver, experiment or Lean build was run by T01.

## 9. Independent audit of the constructive three-mode proposal

This follow-up first checked the parent's explicit interim specification,
then read the completed `T02-constructive-theory.md`. The mathematical verdict
is positive with the metric, initialization and exact-arithmetic
qualifications below. T02 explicitly uses the exact input on the first slab,
resolving the initialization distinction. Its independent complementary
elliptic-series proof of the nome bound and its stated 60-million-root
sup-norm conversion are also consistent with the bounds below. No algorithm
implementation was performed.

### Stationary benchmark and elementary elliptic bounds

Let the elliptic **parameter** be `m=1/20`, set
`a=sqrt(2/21)`, `κ=sqrt(40/21)`, and

\[
g(x)=a\,\operatorname{sn}(\kappa x\mid m),\quad
L=4K(m)/\kappa,\quad \omega=2\pi/L.
\]

Here the notation `K(m)` uses the parameter convention; DLMF writes its
modulus argument as `k=sqrt(m)`. The Jacobi differential equation gives
`sn''=−(1+m)sn+2m sn³`. The choices of `a,κ` therefore give
`½g''+g−g³=0`. The function is smooth, odd and `L`-periodic. Its initial
amplitude and derivative obey `|g|≤a<2/5` and
`|g'|≤aκ=sqrt(80)/21<1/2`.
[DLMF §22.13](https://dlmf.nist.gov/22.13)

There is a short exact bound for the elliptic integral. Convexity on `[0,1]`
puts `t↦(1−mt)^(-1/2)` below its endpoint secant. Integrate at
`t=sin²θ` and use `∫₀^(π/2)sin²θ dθ=π/4`:

\[
1\le\frac{K(m)}{\pi/2}
\le\frac{1+\sqrt{20/19}}2
\le\frac{77}{76},
\]

where `sqrt(20/19)≤39/38` follows by squaring positive rationals. Consequently

\[
\omega^2\ge\frac{40}{21}\left(\frac{76}{77}\right)^2
=\frac{231040}{124509}>\frac{37}{20},\quad
0<\gamma:=1-\omega^2/2<3/40.
\tag{25}
\]

This bound also proves the advertised nome bound without numerical special
function evaluation. For the real nome `0<q<1`, the identities
`K/(π/2)=θ₃(0,q)²` and `θ₃(0,q)=1+2∑_{n≥1}q^(n²)≥1+2q` give
`(1+2q)²≤77/76`. But `(151/150)²>77/76`, hence `q<1/300`.
[DLMF 20.9.2](https://dlmf.nist.gov/20.9#E2),
[DLMF 20.2.3](https://dlmf.nist.gov/20.2#E3)

Use the **normalized** spatial measure `dx/L`. The functions
`ψ_n(x)=sqrt(2) sin(nωx)` are orthonormal. The Jacobi Fourier formula yields

\[
g=\sum_{n\ge1,\ n\text{ odd}}\theta_n\psi_n,
\qquad
\theta_n=\frac{2\sqrt2\,\omega\,q^{n/2}}{1-q^n}.
\tag{26}
\]

The factor `sqrt(2)` in this conversion must not be dropped.
[DLMF 22.11.1](https://dlmf.nist.gov/22.11#E1)

Since `ω²≤κ²=40/21` and `q<1/300`, (26) bounds the three retained
coefficients by `(23/100,3/1000,1/20000)` with room to spare. For example,
`θ₁²<96000/1877421<(23/100)²`. The squared tail after modes `1,3,5` obeys

\[
\tau^2:=\|(I-\Pi)g\|_2^2
\le\frac{320}{21}\,
\frac{300^{-7}}{(1-300^{-7})^2(1-300^{-2})}<10^{-16}.
\tag{27}
\]

One elementary check of the last strict inequality uses
`(1−300⁻⁷)²(1−300⁻²)≥(299/300)³>9/10` and `320/21<16`, leaving the
rational comparison `160/(9·300⁷)<10⁻¹⁶`.

### Admissibility and coherence of every random interface

Let `C` be the three-dimensional coefficient box with these symmetric
coordinate limits. For `v=∑_{n=1,3,5}c_n ψ_n`, `c∈C`,

\[
\|v\|_\infty\le\sqrt2(0.23+0.003+0.00005)<2/5,
\]

\[
\|v'\|_\infty\le\sqrt2\,\omega(0.23+3\cdot0.003+5\cdot0.00005)
<2(0.23925)<1/2.
\tag{28}
\]

The bound `sqrt(2)ω<2` follows from `ω≤κ<sqrt(2)`. Therefore componentwise
clipping into `C` guarantees the complete terminal contract (21) on every
sample outcome and every spatial state. Derivatives are analytic derivatives
of this same trigonometric function; nonlinear codes are evaluated on its
value. The six codes are coherent, and no hidden high-order jet fit is used.

### Conditional variance and projection/clipping bias

Condition on the previous random interface `v`. Independently draw `N`
uniform root states `X_i` on one full period and fresh raw local trees `H_i`
targeting `S_h v(X_i)`. Define the *unclipped* coefficient estimator by

\[
\widehat c_n=N^{-1}\sum_i H_i\psi_n(X_i).
\]

The all-root mean correspondence and (23) give
`E[ĉ_n|v]=<S_hv,ψ_n>` and `E[H_i²|X_i,v]≤1/4`. Hence

\[
\operatorname{tr}\operatorname{Cov}(\widehat c\mid v)
\le\frac1N\sum_{n=1,3,5}\mathbb E[H^2\psi_n(X)^2\mid v]
\le\frac{3}{4N}.
\tag{29}
\]

The same `(X_i,H_i)` may supply all three coordinates: cross-coordinate
covariances do not enter this trace. Independence between different samples,
conditional on `v`, is required. Uniform root states and normalized `dx/L`
are essential to this normalization.

Let `c*=coeff(Πg)`, which belongs to `C`. Coordinate projection `P_C` is
nonexpansive relative to `c*`, so
`||P_C(ĉ)−c*||²≤||ĉ−c*||²` pathwise. The unclipped estimator is unbiased;
the clipped estimator need not be. The variance-plus-squared-bias identity
applied before clipping and orthogonality of the omitted modes give

\[
\mathbb E[\|v_{new}-g\|_2^2\mid v]
\le\|\Pi S_hv-\Pi g\|_2^2+\frac3{4N}+\tau^2.
\tag{30}
\]

Thus there is no missing extra clipping-bias term in the claimed MSE bound.
Its control depends on the proved inclusion `Πg∈C`.

### Odd periodic stability and total error

The Allen–Cahn reaction is odd. Uniqueness therefore preserves oddness of
the exact flow started at an odd interface. For two odd periodic solutions,
their difference `w` has mean zero. Since
`(f(u)−f(v))(u−v)≤(u−v)²`, the energy identity and Poincaré inequality give

\[
\frac d{dt}\|w\|_2^2
\le-\|w_x\|_2^2+2\|w\|_2^2
\le2\gamma\|w\|_2^2.
\]

Since `S_hg=g`, (30) implies for `E_j=E||v_j−g||₂²`

\[
E_j\le e^{2\gamma h}E_{j-1}+\frac3{4N}+\tau^2.
\tag{31}
\]

For `h=2/25`, `J=50`, `T=4`, `N=200000`, and `E₀=0`,

\[
E_{50}<100\left(\frac{3}{800000}+10^{-16}\right)<0.0004.
\tag{32}
\]

Indeed `2γT<3/5` and
`exp(3/5)=(exp(1/5))³≤(5/4)³<2`; each of the 50 recurrence multipliers is
less than two. The condition `E₀=0` holds if the first slab starts from the
given terminal function `g` itself, which satisfies (21), before fitting its
first finite-dimensional interface. If instead the initial interface is
`Πg`, add `exp(2γT)τ²<2·10⁻¹⁶`; the target `0.0004` still holds, but this
initial term must appear in the displayed recurrence bound.

**Scope.** Equation (32) is an expected squared **spatially averaged** error,
`E||v₅₀−g||²_{L²(dx/L)}`. Its square root is below `0.02`; it is not a
pointwise or sup-norm RMSE certificate. A pointwise conversion incurs a
finite-dimensional evaluation factor (at most `sqrt(6)` for the retained
three-mode coefficient error), plus a separately bounded Fourier tail.
The oracle-free update must use the preceding random fitted interface at
every later slab. Replacing that interface by the exact stationary `g`
would prove a different oracle procedure. The known stationary profile can
be used as the input terminal data and to prove/analyze benchmark error.

These formulas prove a conditional mathematical MSE result for the specified
exact-real-arithmetic scheme. They do not report a completed run, observed
cost, roundoff certification, or a generic time-dependent-profile theorem.
The stationary tail and odd subspace are material assumptions.

## 10. Independent audit of a same-profile raw L² obstruction

The parent subsequently supplied the following proposed comparison for the
same Jacobi profile, the **raw uniform mechanism at the particular common
rate `λ=2`**, and horizon `t=7/2`. The derivation is correct with the
nonnegative-moment and heat-kernel conventions made explicit here. It proves
neither an all-rate obstruction nor loss of the PDE solution.
The subsequently appended T02b proof in `T02-constructive-theory.md` was
read in full and agrees with this audit; no blocking mathematical defect was
found in its normalization, comparison or transfer of divergence to `Id`.

Let `M_I,M_0,M_1,M_2,M_3` be the raw squared moments and set
`Y_c(t,x)=exp(−2t)M_c(t,x)`. The exact second-moment identities may take
values in `[0,∞]`; Tonelli applies because all moment terms are nonnegative.
The constant last field is `Y_3=36`. Dropping the nonnegative derivative-code
terms gives, in the mild sense,

\[
\begin{aligned}
\partial_tY_0&\ge\tfrac12\partial_{xx}Y_0+e^{2t}Y_0Y_1,\\
\partial_tY_1&\ge\tfrac12\partial_{xx}Y_1+e^{2t}Y_0Y_2,\\
\partial_tY_2&\ge\tfrac12\partial_{xx}Y_2+36e^{2t}Y_0.
\end{aligned}
\tag{33}
\]

These are statements about positive Volterra systems, not an assertion that
possibly infinite moment fields have classical derivatives.

### A positive spatial lower seed at time one

The period satisfies `L<5`, using `K≤77π/152`, `π<22/7` and `κ>4/3`.
The periodic Brownian kernel at time one, expressed against ordinary
Lebesgue measure `dy`, contains a Gaussian term whose displacement has
absolute value at most `L/2<5/2`. Since `sqrt(2π)<3`, its density is greater
than `e^(−4)/3>1/192`; the latter follows from `e²<8`.
Here the intended expression is **`exp(−4)/3`**, not `exp(−4/3)`.

The positive and negative peaks of `g` exceed `3/10` in magnitude. Its
derivative is bounded by `1/2`, so intervals of length `1/5`, centered at
each of these two peaks, satisfy `|g|≥1/4`. They are disjoint in a period.
Therefore

\[
\int_0^L g(y)^2\,dy\ge\frac1{40}.
\]

Also `g²≤2/21`, so `(1−g²)²≥(19/21)²>4/5` and
`f(g)²≥(4/5)g²`. Keeping only the no-branch contribution yields

\[
Y_0(1,x)\ge P_1[f(g)^2](x)\ge a:=\frac1{9600}
\quad\text{for every }x.
\tag{34}
\]

There is no missing factor of `L`: the kernel and integral in this step are
with respect to `dy`, whereas normalized `dy/L` was used for the Fourier
error metric.

### Spatially constant positive comparison and blowup

Starting at time one, compare (33) with spatially constant functions, with
initial data `(a,0,0)`. Introduce

\[
s=s(t)=\int_1^t e^{2r}\,dr=(e^{2t}-e^2)/2.
\]

The comparison ODE is

\[
A_s=AB,\qquad B_s=AC,\qquad C_s=36A,
\qquad(A,B,C)(0)=(a,0,0).
\]

Let `z_s=A`, `z(0)=0`. Direct integration gives
`C=36z`, `B=18z²`, `A=a+6z³`, hence

\[
z_s=a+6z^3,\qquad
s_*:=\int_0^\infty\frac{dz}{a+6z^3}
\le\underbrace{(1/30)/a}_{320}
+\underbrace{\int_{1/30}^\infty\frac{dz}{6z^3}}_{75}
=395.
\tag{35}
\]

Positive Picard comparison makes `Y_0(t,x)≥A(s(t))` for every state and
`1≤t<t_*`, where `s(t_*)=s_*`. It is enough to compare each lower Picard
iterate with the extended nonnegative moment mild equation; no assumption
that all actual moments are finite is needed. The spatial heat semigroup
preserves constants.

The exponential estimates can be checked using rational series: summing
terms through order eight gives `e⁷>798`, and bounding the tail of the
`e²` series from order three by a geometric series gives `e²<23/3<8`.
Thus `s(7/2)>395≥s_*` and `t_*<7/2`.

### The root moment also diverges

A divergence confined to a descendant code would not by itself suffice.
Here the normalized `Id` equation is exactly

\[
Y_I(t,x)=P_t[g^2](x)+\tfrac12\int_0^t
P_{t-r}[Y_0(r,\cdot)](x)\,dr.
\]

At `t=7/2`, its nonnegative integral, restricted to `1≤r<t_*`, is bounded
below by

\[
\frac12\int_1^{t_*} A(s(r))\,dr
\ge\frac12 e^{-7}\int_0^{s_*}A(s)\,ds
=\frac12e^{-7}\lim_{s\uparrow s_*}z(s)=\infty.
\tag{36}
\]

The change of variable uses `dr=e^(−2r)ds≥e^(−7)ds` before `7/2`.
Consequently `E[H_{Id,7/2,x}²]=∞` at every starting state for this raw
`λ=2` estimator. The same integral argument gives divergence at every later
horizon as well. This is a same-PDE, same-terminal-profile contrast with the
finite-MSE continuation theorem at `T=4`, with a changed global estimator
formed from learned short slabs. It is not a claim that rate/proposal tuning
is impossible or that another existing representation cannot do better.
