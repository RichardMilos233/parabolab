# General rate selection: existence, cutoff consistency, and certificates

Initial derivation: 12 September 2026. Implementation status reviewed:
16 September 2026.

**Status:** conventional arguments under the explicit hypotheses below.
Five deterministic certificate-transfer and coverage lemmas are now
formalized in [`RateCertificate.lean`](../../../formal/EstimatorIntegrity/RateCertificate.lean).
The stochastic representation, depth-tail and analytic bounds below remain
conventional proofs. Publication novelty is unestablished. This is not an
automatic certified optimizer for every PDE supported by the software.

The [flat/wave certificate checkpoint](../results/certified-rate-checkpoint.md)
and [weighted-profile checkpoint](../results/profile-efficiency-checkpoint.md)
now provide concrete exact-rational bounds for the stated Allen–Cahn
examples. Their all-code envelopes and
[mean-identification proof](allen-cahn-mean-identification.md) close the
needed finiteness and common-mean obligations for those examples. They do
not certify the general quadrature error `delta` in (12).

This extends the [exponential-rate note](exponential-rate-optimization.md),
using the [underlying moment model](notation-and-moment-theorem.md).

## 1. Fixed estimator

Fix root `(t,x,c)` and horizon `tau=T-t>0`. The Markov motion, terminal factors,
mechanism, and positive labelled tuple probabilities are independent of the
common exponential rate `lambda>0`. Predictable proposals may depend on
pre-selection history but not lambda. Children share a branch position and
have independent subsequent randomness. Assume nonexplosion; a uniform arity
bound `1<=k<=m<infinity` is sufficient for the common exponential clock.
Absorbing zero codes may be pruned. All nonzero contributing trees continue
to the terminal horizon.

Let `N` count clock expiries at branch nodes; `L` sums all clipped particle
lifetimes, including terminal survivors. These are not depth and calendar time.
On nonzero contributing trees,

$$
\tau\le L\le\tau[1+(m-1)N].
$$

Set `M(lambda)=E_lambda |H_lambda|^2`, allowing infinity. Absolute convergence
and likelihood cancellation make the mean rate-independent. Minimizing a
finite second moment then minimizes variance, not variance times work.
Identification with a PDE solution is a separate representation obligation.

## 2. Existence of the full-tree optimum

For a labelled completed topology `theta` with spatial/time marks `xi`,
cancelling sampling density against squared likelihood gives

$$
M(\lambda)=\sum_\theta\int W_\theta(\xi)
\lambda^{-N_\theta}e^{\lambda L_\theta(\xi)}d\nu_\theta(\xi),
\qquad W_\theta\ge0, \tag{1}
$$

where `W,nu` do not depend on lambda. Tonelli and nonexplosion justify this
extended nonnegative sum. Repeated labels remain distinct; zero trees contribute
zero. For `h(lambda)=lambda^(-n) exp(lambda l)`,

$$
h''(\lambda)=h(\lambda)
[(l-n/\lambda)^2+n/\lambda^2]>0\quad(l>0). \tag{2}
$$

**Theorem 1.** Suppose `M(lambda_0)<infinity` at some rate and one branched
topology with `n>=1` has positive integrated coefficient mass
`C_b=integral W_theta dnu_theta>0`. Then `M` has a unique global minimizer
`lambda_*>0` with finite value.

**Proof.** Equation (2) gives strict convexity between finite endpoint values;
Fatou gives lower semicontinuity. The finite incumbent implies
`0<C_b<infinity`. Since `L>=tau`,

$$
M(\lambda)\ge C_b\lambda^{-n}e^{\lambda\tau}. \tag{3}
$$

This diverges at zero and infinity. A nonempty finite sublevel set is therefore
compact inside `(0,infinity)`. Lower semicontinuity gives attainment; strict
convexity gives uniqueness.

A positive root-survival term is not necessary, unlike the sufficient
corollary in the older note. A syntactically live label is not sufficient:
its integrated squared terminal-product contribution must be positive. For
Id followed by one surviving source child, the exact contribution has

$$
C_b=\tau P_\tau[|f(J\phi)|^2](x),\qquad n=1,\quad L=\tau. \tag{4}
$$

Without a positive branched contribution an interior optimum need not exist.
An estimator with infinite variance at every rate fails the finite-incumbent
hypothesis. Smooth data and sample-variance plots alone do not establish it.
The second moment is also log-convex, by Holder in (1); variance need not be
log-convex after subtracting the squared mean.

### An implicit equation, not a plug-in formula

Where differentiation is dominated, (1) gives

$$
M'(\lambda)=\mathbb E_\lambda[|H_\lambda|^2(L-N/\lambda)]. \tag{5}
$$

An interior differentiable minimizer satisfies

$$
\lambda_*=
\frac{\mathbb E_{\lambda_*}[N|H_{\lambda_*}|^2]}
{\mathbb E_{\lambda_*}[L|H_{\lambda_*}|^2]}. \tag{6}
$$

These expectations depend on the unknown rate: this is not a universal
constant or an explicit formula from PDE coefficients. The tilted bound below
on a neighborhood controls the `N,L` factors and justifies differentiation.

## 3. Exact depth-optimizer consistency

With root generation zero, let

$$
M_K(\lambda)=\mathbb E_\lambda[
|H_\lambda|^2\mathbf1_{\{\mathrm{depth}\le K\}}].
$$

Then `M_K` increases to `M`. Bounded arity and fixed depth bound `N,L`, so
comparison of kernels with the finite incumbent shows that each `M_K` is finite
at every positive rate. For sufficiently large `K`, the positive topology
from Theorem 1 is retained, providing strict convexity, a unique minimizer
`lambda_K`, and the common coercive bound (3).

**Theorem 2.** Under Theorem 1 and bounded arity,

$$
\lambda_K\to\lambda_*,\qquad \min M_K\uparrow\min M. \tag{7}
$$

**Proof.** The minimizers lie in a common compact set because
`M_K(lambda_K)<=M(lambda_0)` and (3) holds. Their objective minima increase
and are bounded above by `min M`. For a convergent subsequence
`lambda_Kj -> lambda_bar` and each fixed `k`, lower semicontinuity yields

$$
M_k(\bar\lambda)\le\liminf_j M_k(\lambda_{K_j})
\le\lim_j\min M_{K_j}.
$$

Taking the supremum in `k` gives `M(lambda_bar)<=lim min M_K<=min M`.
Equality and uniqueness identify the cluster point with `lambda_*`.
Compactness then gives convergence of the whole sequence.

This concerns exact objectives and exact minimizers, not numerical sweeps.
It does not imply that `M(lambda_K)` is finite or nearly optimal. Numerical
errors and omitted tails require additional bounds.

## 4. A constructed all-code tilted-moment bound

Consider the actual semilinear derivative-coded mechanism for

$$
u_t+\tfrac12\Delta u+f(u)=0,\qquad u(T)=\phi,
\qquad x\in\mathbb R^d.
$$

Assume `|phi|<=R`, `|partial_i phi|<=D`, and constants `C<infinity`, `beta>=1`
with

$$
|f^{(k)}(z)|\le C\beta^k\quad(k\ge0,\ |z|\le R). \tag{8}
$$

Every polynomial satisfies this with `beta=1` and a maximum over its finitely
many nonzero derivatives. Sine and exponential functions also admit geometric
derivative bounds on bounded intervals. Arbitrary smooth nonlinearities or
unbounded terminal factors are not automatically included.

Every live code reached from Id is `Id`, a first derivative `D_i`, or
`F_k^a=(a f^(k))*`. The alternatives are

$$
\mathrm{Id}\to(F_0^1),\quad D_i\to(F_1^1,D_i),
$$
$$
F_k^a\to(F_0^1,F_{k+1}^a)
\quad\hbox{or}\quad(D_i,D_i,F_{k+2}^{-a/2}),\quad i=1,\ldots,d.
$$

No higher spatial derivative is generated in this semilinear closure. Use
spatially constant weights

$$
w_{\mathrm{Id}}=w_{D_i}=1,\qquad w_{F_k^a}=a^2\beta^{2k}.
$$

Zero scalars are absorbing, not positive live weights. Constant-source fallback
branches have zero value. This keeps every live derivative/scalar code and
the coefficients actually used by the sampler.

Set

$$
A=\max(1,R^2,D^2,C^2),\qquad
B=\max\{1,\beta^2,(d+1)(\beta^2+d\beta^4/4)\}. \tag{9}
$$

For uniform labelled tuples, substitution gives `|g_c|^2<=A w_c` and
`sum_Z q_c(Z)^(-1) prod_z w_z<=B w_c` for all live codes. The three row ratios
are `1`, `beta^2`, and the last expression in (9). Uniform exact-zero reduction
only decreases the bound. For a nonuniform proposal satisfying
`q_c(Z)>=epsilon/m_c` on its `m_c` labels, use the conservative replacement
`B/epsilon`. This remains valid for history-dependent probabilities, since
the weights are spatially constant and the probability floor is uniform.
All states in `R^d` are covered; no Brownian state truncation is used.

Give every branch an extra factor `r>1`. First-event conditioning multiplies
the branch moment recursion by `r`. Arity is at most three, and `b>=1` bounds
all child products by `b^3`. Killed-depth induction gives `w_c b` as a bound,
where

$$
b'=\lambda b+(rB/\lambda)b^3,\qquad b(0)=A.
$$

Solving for `b^(-2)` and passing to full depth by monotone convergence yields

$$
\boxed{\mathbb E_\lambda[r^N|H_c|^2]\le w_c b_{\lambda,r}(\tau),\qquad
b_{\lambda,r}(\tau)=
\frac{Ae^{\lambda\tau}}
{\sqrt{1-\dfrac{rBA^2}{\lambda^2}(e^{2\lambda\tau}-1)}}.} \tag{10}
$$

The denominator must be positive. This is a constructed upper bound, not a
conclusion from finite-depth lower moments. A nonempty certified window always
exists: take `r=2`, `lambda_0=A sqrt(2B)`, and
`tau<log(2)/(2 lambda_0)`. This is a feasible incumbent, not the true optimum.
Constants can be conservative, particularly at high dimension or small floors.

For a compact interval `I=[a,b]`, finite endpoint tilted certificates give a
uniform Id-root bound `C_I=max(b_{a,r}(tau),b_{b,r}(tau))`, by log-convexity of
the tilted moment. This applies only when both endpoint denominators are
positive.

### PDE identification is a separate step

Terminal-jet bounds alone do not identify a smooth nonlinearity outside their
range: flat modifications can change the PDE without changing those jets.
A sufficient conventional route is `||phi||_infinity<=R0<R`, suitable classical
regularity, (8) on `[-R,R]`, and additionally `tau<(R-R0)/C` when `C>0`.
Comparison keeps `|u|<R`; the gradient equation gives
`|D_i u|<=D exp(C beta tau)`. The normalized fields `f^(k)(u)/beta^k` and
`u,D_i u` have a locally Lipschitz polynomial vector field on bounded uniform
code/state balls, since shifts `k -> k+1,k+2` are bounded operators.
Mild-system uniqueness by Gronwall identifies these fields with the bounded
tree means. No stochastic-control verification theorem is asserted.

## 5. Quantitative error of the selected rate

Suppose a uniform certificate `sup_{lambda in I} E[r^N H^2]<=C_I` is available.
Depth greater than `K` requires at least `K+1` branch events, hence

$$
0\le M(\lambda)-M_K(\lambda)\le C_I r^{-(K+1)}. \tag{11}
$$

If `Mtilde_K` has a certified uniform error at most `delta` relative to `M_K`,
and `lambda_hat` is `eta`-optimal for `Mtilde_K` on `I`, then

$$
\boxed{M(\widehat\lambda)-\min_{\lambda\in I}M(\lambda)
\le C_I r^{-(K+1)}+2\delta+\eta.} \tag{12}
$$

**Proof.** Bound `M(lambda_hat)` by `M_K(lambda_hat)` plus the tail, then
`Mtilde_K(lambda_hat)+delta` plus the tail. Apply eta-optimality and evaluate
at a minimizer of `M` on `I`. A second numerical error and `M_K<=M` finish.
Only one tail term is needed because killing is one-sided. Rate-invariant
means give the identical additive variance-excess bound.

This is interval optimality, not global optimality without excluding better
rates outside `I`. Alternatively, a genuine upper bound
`U(lambda_hat)>=M(lambda_hat)` and certified lower bound
`L_K<=inf_{lambda>0}M_K(lambda)` give the global certificate
`M(lambda_hat)-min M<=U(lambda_hat)-L_K`. The positive-topology envelope (3)
and a finite incumbent can also bound the global search region. A certificate
near one rate need not cover that entire region.

Current quadrature does not certify `delta`. A tilted second moment also does
not alone provide concentration for squared-weight samples, which can require
fourth moments or another bounded envelope. Finite pilots do not certify the
unrestricted tree or unbounded state weights. The generic finite-depth
selector is a numerical tuning method, not an implementation of (12).
The separate flat verifier uses exact moment enclosures and exterior bounds;
the wave and profile verifiers control the full moment directly through
polynomial residuals and convex bounds. Their accepted witnesses implement
the upper-minus-global-lower route above without claiming a verified error
for the old time/Gaussian quadrature.

## 6. Prior work and the research boundary

Convex importance-sampling optimization and adaptation predate this work:
[Ryu--Boyd](https://stanford.edu/~boyd/papers/adaMC.html) and
[Badouraly Kassim--Lelong--Loumrhari](https://arxiv.org/abs/1307.2218).
The latter's Poisson factors and sample-average optimization are particularly
close. Random exposure `L` and recursive all-code control are the branching
issues, not a new generic importance-sampling principle.

Weighted-progeny/generating-function bounds have close precedent in
[Huang--Privault stability v2](https://arxiv.org/html/2502.17853v2), and scalar
ODE majorants in [Henry-Labordere et al.](https://arxiv.org/abs/1603.01727).
Theorem 2 is a direct monotone-objective/equicoercivity argument, not an
invention of optimizer consistency. Whether sharp practical certificates for
the implemented family provide a publishable increment remains open.

The stated Allen–Cahn certificate specialization is complete. Remaining
algorithmic questions include generalizing useful error control to other
PDEs/horizons and changed proposals, and evaluating continuation-aware tuple
selection. Hold the same proposal fixed when comparing rate objectives and
sampling. Variance reduction and mathematical guarantees are primary;
measured cost is supporting evidence. No multidimensional Merton application
is selected by this result.
