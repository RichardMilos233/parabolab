# T41 — exact point-query lower bound near the unstable phase

**Verdict: conventional mathematical PASS.** The stated constants and
exponent are correct. The bump family lies in the fixed smooth,
sign-changing class, the nonlinear PDE values have the required opposite
separation, and the adaptive randomized transcript argument gives
$\mathbb E Q(g_T)\geq3K/4$. I found no oracle-model counterexample under
the exact point-value information restriction.

Before presenting an accepted theorem, add the explicit quantifiers and
measurable halting interface in section 1. These complete the proof contract;
they do not change the constant, exponent, oracle strength, or error criterion.
This is a worst-case-in-input, horizon-by-horizon information lower bound,
not a fixed-profile or fixed-tree claim.

Reviewed source:
[04o-unstable-phase-query-lower-bound.md](../04o-unstable-phase-query-lower-bound.md),
SHA-256
473cdd043991659cac12180731500f3bff63be4377f56f902dadd7afdee40844.
Only this review was written. No implementation, experiment, Lean run, or
additional literature search was performed. T40 independently reports that
its mathematical comparison with 04o passes; its primary-source audit handles
precedent and supplies no novelty claim.

## 1. Exact theorem and oracle interface

Let $\mathcal V_{d,s}$ be the source's fixed class of real smooth functions
on $\mathbb T^d=\mathbb R^d/\mathbb Z^d$:

$$
\max_{|\alpha|\leq s}\|\partial^\alpha v\|_\infty\leq1,\qquad
\|v\|_\infty\leq\frac12,
$$

with both a strictly positive and a strictly negative value somewhere.
Here $d,s$ are positive integers. The derivative norm includes the zeroth
derivative, and only the fixed finite order $s$ is bounded uniformly.

The precise lower-bound quantifiers are:

> There are $C>0$ and $T_0<\infty$, depending only on $d,s$ and the fixed
> bump, and an explicitly chosen $g_T\in\mathcal V_{d,s}$ for each
> $T\geq T_0$, such that every admissible point-value algorithm $A_T$ with
> $\sup_{v\in\mathcal V_{d,s}}\mathbb E|H_T(v)-S_Tv(x_*)|^2\leq1/16$
> satisfies $\mathbb E Q_T(g_T)\geq C e^{dT/(s+d)}$.

The algorithm may depend on $T,d,s,x_*$ and the entire public problem
description. There is no requirement that the same computational policy be
used at different horizons.

An adequate admissible-algorithm interface is as follows.

- The unknown input is accessed only through an opaque oracle returning the
  exact real number $v(x)$ for a requested $x\in\mathbb T^d$. Oracle metadata,
  evaluation side information, source/formula access, integrals, derivatives,
  Fourier coefficients and evolved values are not supplied.
- All private randomness is represented by a seed $\omega$ on a probability
  space whose law is independent of the unknown input. At each finite
  transcript, measurable rules decide whether to halt or select the next
  query point. A measurable halting rule returns a real output from that
  transcript and the seed.
- Count every point evaluation, including preprocessing that depends on the
  unknown input. Input-independent computation, scalar arithmetic and
  knowledge of the public hard-family construction may be free.
- Outputs in the MSE premise must be well defined. The usual convention is
  almost-sure finite halting on the promised input class. For the proof below
  it suffices that the baseline run has finite expected query count, hence
  finite halting almost surely, and that the hard-input outputs appearing in
  the MSE premise are measurable real random variables. Infinite expected
  baseline cost already proves the asserted lower bound.

A standard Borel seed space and Borel transcript/query maps are a convenient
concrete version. Fixed smooth input functions make oracle evaluation
measurable. Only the finite family of $2K+1$ input runs at the chosen horizon
is coupled, so exceptional null sets can be removed simultaneously.
Unmeasurable rules for which the displayed expectations have no meaning are
outside the theorem.

The algorithm can precompute the formula for $g_T$. It is not promised that
the unknown oracle equals $g_T$ rather than one of the hard alternatives.
That distinction is why a lower bound on the baseline run is legitimate.

## 2. Bump scaling, norm bounds and torus geometry

Fix the source's nonnegative nonzero
$\psi\in C_c^\infty((0,1)^d)$, with $0\leq\psi\leq1$. Put

$$
I=\int\psi>0,\quad
D=\max\left(1,\max_{|\alpha|\leq s}\|\partial^\alpha\psi\|_\infty\right),
\quad a=\frac1{8D},\quad q=s+d.
$$

In particular $I\leq1$ and $a\leq1/8$. Index the cells by
$j\in\{0,\ldots,k-1\}^d$ and use the half-open partition of $[0,1)^d$.
Within cell $j$ set

$$
b_j(x)=a k^{-s}\psi(kx-j),
$$

and extend by zero. Compact support strictly inside the reference cube
provides a collar on which every derivative vanishes. The extension is
therefore smooth across all cell faces and across the torus boundary.
For $|\alpha|\leq s$ and $k\geq1$,

$$
\|\partial^\alpha b_j\|_\infty
\leq a k^{|\alpha|-s}D\leq\frac18.
$$

Also $0\leq b_j\leq1/8$ and

$$
\int_{\mathbb T^d}b_j
=a I k^{-(s+d)}=\mu.
$$

The bumps have disjoint cell supports. A boundary query receives the
baseline value for all relevant bumps; assigning that point to its unique
half-open cell only overcounts which alternative might have been exposed.
It cannot invalidate the lower bound.

## 3. Heat-kernel, floor, and tiny-sine constants

For the generator $\Delta/2$ on the unit torus, the time-one heat kernel is
the periodized density

$$
p_1(x,y)=(2\pi)^{-d/2}
\sum_{n\in\mathbb Z^d}
\exp\!\left(-\frac{|x-y+n|^2}{2}\right).
$$

For each $x,y$ choose a translate whose coordinate differences lie in
$[-1/2,1/2]$. Its squared length is at most $d/4$. Thus

$$
p_1(x,y)\geq
\kappa:=(2\pi)^{-d/2}e^{-d/8}>0.
$$

The factor is correct for unit covariance at time one; no diffusivity or
torus-volume factor is missing. Also $\kappa<1$.

Set

$$
R_T=(\kappa a I e^{T-1})^{1/q},\qquad k=\lfloor R_T\rfloor,\qquad K=k^d.
$$

An explicit acceptable threshold is

$$
T_0=\max\{1,\ 1+q\log4-\log(\kappa a I)\}.
$$

Then $T\geq T_0$ implies $R_T\geq4$ and $k\geq4$. The loose floor
bounds used in the source are valid:

$$
R_T/2\leq k\leq R_T,\qquad
1\leq\kappa\mu e^{T-1}
=\left(\frac{R_T}{k}\right)^q\leq2^q.
$$

For $D_s=\max(1,(2\pi)^s)$ and
$\delta=\kappa/(32e\,2^qD_s)$, define
$g_T(x)=\delta\mu\sin(2\pi x_1)$. The preceding upper floor bound gives

$$
e^T\delta\mu\leq\frac1{32D_s},\qquad
\|g_T\|_{C^s,\max}\leq\delta\mu D_s\leq\frac{e^{-T}}{32}.
$$

These are exactly the two estimates stated in 04o.
For $T\geq1$, every $g_T\pm b_j$ has derivative norm at most
$1/8+e^{-T}/32<1/4$ and supremum norm below $1/4$. Thus it lies strictly
inside both advertised bounds $1$ and $1/2$; the construction has ample
margin.

The strict sign-changing property is also valid. A cell's projection onto
the first coordinate is an interval of length at most $1/4$. It cannot
cover either open half-circle on which $\sin(2\pi x_1)$ has a fixed strict
sign. Choose a positive-sine point and a negative-sine point whose first
coordinates are outside that cell interval. Both points are outside the
cell, so both $g_T+b_j$ and $g_T-b_j$ agree there with the same nonzero
sine values. The baseline itself is nonzero and changes sign.

No common bound on higher derivatives or analytic radius is required or
obtained. The higher derivatives may grow with $k$, as the source correctly
states.

## 4. Nonlinear PDE separation

For every hard input, standard scalar comparison keeps the solution in
$[-1,1]$. The smooth bounded initial data on the compact torus give a
global classical solution, for example by first using a globally Lipschitz
extension of $f$ outside that invariant interval. The extension does not
change these solutions.

For a nonnegative bump $b_j$, comparison gives $0\leq S_t b_j\leq1$.
Since $u-u^3\geq0$ on this interval, the positive heat-semigroup mild formula
implies

$$
S_1b_j(x)\geq P_1b_j(x)\geq\kappa\mu.
$$

Write $c=\kappa\mu$. It is positive and at most one, since
$\kappa<1$, $I\leq1$, $a\leq1/8$, and $k\geq1$. Comparison during the
remaining $T-1$ time units gives

$$
S_Tb_j(x)\geq\ell_c(T-1),\qquad
\ell_c(t)=\frac{ce^t}{\sqrt{1+c^2(e^{2t}-1)}}.
$$

With $B=ce^{T-1}\geq1$,

$$
\ell_c(T-1)
=\frac{B}{\sqrt{1+B^2-c^2}}
\geq\frac{B}{\sqrt{1+B^2}}
\geq\frac1{\sqrt2}.
$$

Every inequality has the correct direction. Oddness of the reaction and
uniqueness give $S_T(-b_j)=-S_Tb_j$.

To restore the common sign-changing background, let $U,V$ be two solutions
in $[-1,1]$ and put $w=U-V$. Then

$$
w_t=\frac12\Delta w+c(t,x)w,\qquad
c(t,x)=1-(U^2+UV+V^2)\leq1.
$$

The quadratic is nonnegative, and $c$ is bounded. Comparing both $w$ and
$-w$ with the supersolution $e^t\|w(0)\|_\infty$ proves

$$
\|S_t(v+h)-S_t(v)\|_\infty\leq e^t\|h\|_\infty.
$$

This correctly uses an upper potential bound. It does not use the false
assertion $|f'|\leq1$ on $[-1,1]$.
Apply it with $h=g_T$ and $v=\pm b_j$:

$$
y_{j,+}:=S_T(g_T+b_j)(x_*)\geq\frac1{\sqrt2}-\frac1{32}>\frac12,
$$

$$
y_{j,-}:=S_T(g_T-b_j)(x_*)\leq-\frac1{\sqrt2}+\frac1{32}<-\frac12.
$$

The separation is uniform in the query point and in $j$.
The perturbation does reduce the individual $1/\sqrt2$ bump bound; the
correct final targets are the displayed perturbed bounds, as 04o states.
No spatial-mean closure or discarded nonlinear correction is involved.

## 5. Adaptive transcript induction and the expected-query bound

Fix $T$ and an admissible algorithm, and use the same seed for all hard
inputs and the baseline. Assume the baseline expected query count is finite;
otherwise the claimed conclusion is already true.

For a baseline run define $J(\omega)$ to be the set of cells containing
its queried points before halting. It is measurable under the stated
interface and satisfies

$$
|J(\omega)|\leq Q_T(g_T,\omega).
$$

For a fixed $j\notin J(\omega)$, all baseline query points are outside cell
$j$. The adaptive coupling is a finite induction:

1. Before the first query, the public problem description and seed are
   identical, so the same action is selected.
2. If the previous transcripts agree, the next stopping decision or query
   point agrees. That baseline point is outside cell $j$, where
   $g_T+b_j=g_T-b_j=g_T$, so the returned exact values agree.
3. At the finite baseline stopping time, both alternative runs have the
   same transcript and seed and therefore halt with the same real output.

This proves equality of both alternative outputs on the baseline no-hit
event, including their stopping decisions. The event need not be independent
of the output, query count, query locations, or seed. Independence is not
used.

For real $h$ and targets $a,b$,

$$
\frac{(h-a)^2+(h-b)^2}{2}
=\left(h-\frac{a+b}{2}\right)^2+\frac{(a-b)^2}{4}.
$$

Since $y_{j,+}-y_{j,-}>1$, on the no-hit event the average of the two
squared losses is at least $1/4$. On its complement the losses are
nonnegative. Taking expectations and then averaging the finite set of
indices gives

$$
\begin{aligned}
\frac1{2K}\sum_{j,\sigma}
\mathbb E|H_T(g_T+\sigma b_j)-y_{j,\sigma}|^2
&\geq\frac1{4K}\sum_j\mathbb P(j\notin J)\\
&=\frac14\left(1-\frac{\mathbb E|J|}{K}\right).
\end{aligned}
$$

Finite sums of nonnegative measurable losses justify this step directly;
Tonelli also applies. The uniform MSE premise bounds the left side by
$1/16$, so

$$
\mathbb E|J|\geq\frac{3K}{4},\qquad
\mathbb E Q_T(g_T)\geq\frac{3K}{4}.
$$

It is slightly cleaner to derive the first inequality before substituting
$|J|\leq Q$, but the source's combined inequality is equivalent.
Finally,

$$
\mathbb E Q_T(g_T)
\geq
\underbrace{\frac34\,2^{-d}
 \left(\frac{\kappa a I}{e}\right)^{d/q}}_{C>0}
e^{dT/q}.
$$

This is exactly the source constant with $q=s+d$. There is no assumption
of unbiasedness, no fixed deterministic stopping horizon, no variance/work
optimization premise, and no fixed-tree representation restriction.

## 6. General error/separation lemma

The finite information argument has a useful precise abstract form.
Suppose $K$ alternatives come in pairs whose deterministic targets have
separation at least $2h_*$, where $h_*>0$. Suppose their outputs agree on
the no-hit events of a baseline run, with the visited-index count bounded
by $Q$. If the average MSE over all $2K$ alternatives is at most
$\varepsilon^2$, then

$$
\mathbb E Q
\geq K\left(1-\frac{\varepsilon^2}{h_*^2}\right).
$$

The positive part of the right side may be taken because $Q\geq0$.
No uniform MSE premise is needed for this abstract lemma beyond its
implication for the finite-family average.
In 04o, choose $h_*=1/2$ and $\varepsilon=1/4$ to get $3K/4$.
The actual PDE separation is larger, but optimizing that constant is
unnecessary and should not obscure the proof.

## 7. Failed attacks and limits of the conclusion

- **Exact real values do not defeat the argument.** They can carry unlimited
  information when a bump is encountered, but outside its cell the values
  are exactly equal, not merely close or statistically hard to distinguish.
  No noisy-coin oracle is substituted for the stated stronger oracle.
- **Adaptive querying and stopping do not defeat the argument.** The
  no-hit event is defined using the baseline run; the finite induction
  transfers that entire run to either alternative before the first possible
  distinguishing query.
- **The sine is not a change of the input promise.** Its amplitude is
  positive at every finite horizon, every family member takes both signs,
  and all belong to one fixed norm-bounded class. The hard functions change
  with the horizon; a single fixed profile becoming harder is not shown.
- **The baseline being explicitly written is not free identification.**
  Public knowledge of $g_T$ and all bump formulas is harmless. A promise
  that the unknown oracle is exactly a particular formula, or access to its
  source/identity, would change the information model and is excluded.
- **This does not contradict positive-basin work theorems.** The hard
  functions approach the unstable zero state and take both signs. They do
  not lie in a fixed strictly positive basin or satisfy a fixed positive
  mass certificate.
- **The error criterion is absolute solution error at a fixed point.**
  It is not relative defect error, and no estimator-tail or unbiasedness
  condition is imposed beyond the finite MSE premise.
- **The exponent is not established as optimal.** A single hidden bump
  suffices for this exponential lower bound. No matching upper bound,
  stronger minimax exponent, or publication priority is established by the
  argument.

## 8. Formalizable core after this conventional pass

A useful first fixed target is the finite paired-loss/no-hit lemma in
section 6, instantiated to $h_*=1/2$ and $\varepsilon^2=1/16$.
Its real algebra, finite index averaging, indicator identity
$\sum_j\mathbf1_{\{j\notin J\}}=K-|J|$, and cardinality bound yield
$\mathbb EQ\geq3K/4$. A version on a general probability space can retain
explicit measurability and integrability hypotheses; a purely finite
probability version would be narrower and must be labelled accordingly.

A second useful target is the deterministic finite-transcript induction
under an explicit point-value algorithm interface. It would justify the
output-equality hypothesis of the first lemma rather than assuming that
oracle step away. Scalar amplification algebra, derivative scaling,
floor estimates and the final constant calculation are additional separate
targets.

The torus heat-kernel minorization, nonlinear PDE global comparison,
one-sided-Lipschitz semigroup estimate, and construction of smooth periodic
bumps remain conventional unless actually formalized. A Lean theorem that
assumes the separated targets and no-hit coupling would certify the
information-theoretic core, not the entire Allen–Cahn lower bound.

The required source integrations are therefore precise and limited: state
the horizon-by-horizon quantifiers, give an explicit $T_0$ or its equivalent
conditions, and specify measurable common-seed query/halting/output maps.
No mathematical constant, hard-family amplitude, oracle strength, or
exponential rate needs correction.
