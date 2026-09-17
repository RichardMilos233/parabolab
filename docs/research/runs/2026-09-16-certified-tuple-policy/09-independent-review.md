# Independent mathematical review and literature check

Reviewed 16 September 2026 by research role T01. Requested and actual role:
`gpt-6-astra`, maximum reasoning. This independently checks C1–C6 in
`04-theory.md` against the sampler, mechanism, moment theorem and existing
Allen–Cahn mean-identification proof. It also reproduces and verifies the
existing uniform moment boxes used by the new wave gate below. It does not
certify new-policy root moment values or empirical results, and no Lean build
was run by this reviewer.

The strongest bounded contribution is a **certified full-tree policy-improvement
framework**: use bounds on the old continuation moments to accept a tuple update,
then inherit finite second moments and variance dominance at unrestricted depth.
Joint convexity of the static rate/probability problem is a useful additional
structural result. Neither the square-root rule nor exact-zero pruning is new.

No substantive mathematical defect was found in the reviewed C1–C6 contracts.
Two interpretation requirements were sent to the author: C6's six-code envelope
must be uniform in space and remaining time for the bounded mild-uniqueness
argument; C4's topology expansion counts completed nonzero physical trees, or
equivalently includes the unpruned zero events with zero integrands. These are
consistent with the proposed certificate construction and current sampler.

## 1. Full-tree improvement: approved mathematical contract

Fix a common positive exponential rate, the Markov motion, terminal evaluators,
and labelled mechanism. Retain the original countable code space and its
deterministic coefficients. Assume measurable policies, full support on all live
labels, shared branch positions, conditionally independent child continuations,
and nonexplosion under both policies. A uniform finite offspring bound with the
common exponential clock is sufficient for the last condition.

For policies matching the current callback information, a tuple is selected
after the lifetime `s` is known but before the Brownian branch position is drawn.
For a nonnegative continuation field `v`, define

\[
A_{c,i}[v](t,x,s)
=P_s\!\left[\prod_{z\in Z_{c,i}}v_z(t+s,\cdot)\right](x).
\]

Mechanism coefficients must be squared outside this expression if they are not
already encoded in child codes. The product is inside one shared-position
expectation. For a policy depending on generation, append generation to the
state and advance it for children. The state-based formula below must not be
claimed for arbitrary sibling-history adaptation without enlarging its state
and rechecking conditional child independence.

Writing `D=T-t`, the second-moment operator is

\[
(\Phi_qv)_c(t,x)
=e^{\lambda D}P_D|g_c|^2(x)
+\int_0^D\frac{e^{\lambda s}}{\lambda}
  \sum_i\frac{A_{c,i}[v](t,x,s)}{q_{c,i}(t,x,s)}\,ds.
\]

Let `M_q` be the old unrestricted moment field, finite at all states and codes
used in the comparison. If the new supported policy satisfies

\[
\sum_i A_{c,i}[M_q]/q'_{c,i}
\leq\sum_i A_{c,i}[M_q]/q_{c,i}
\]

at every reachable decision, up to null sets for the relevant kernels, then

\[
\boxed{M_{q'}\leq M_q.}
\]

**Proof.** The displayed assumption gives
`Phi_q' M_q <= Phi_q M_q = M_q`. Starting the new killed-moment iteration at
zero, monotonicity gives `Phi_q'^n(0) <= M_q` at every depth. Nonexplosion and
monotone convergence identify its supremum with `M_q'`. In particular, finiteness
of the new moment is a conclusion, not an assumed premise. There is no
generation-dependent multiplicative error factor in this argument.

An exact greedy policy uses the square roots of `A[M_q]`. If the greedy policy
has exact-zero coordinates, mixing it with the old supported policy preserves
support and local improvement by convexity of `sum A_i/q_i`. Mixing with an
arbitrary different reference policy has no such general guarantee.

**Important distinction.** If `U` is merely a supersolution for the old operator,
greedifying `A[U]` proves a finite bound `M_q' <= U`; it does not establish
`M_q' <= M_q`. Already in a one-decision problem, true contributions `(1,1)` and
upper estimates `(100,1)` give greedy probabilities `(10/11,1/11)`. The true
objective becomes `121/10`, compared with `4` under uniform sampling. Thus a
verified supersolution is useful for integrability, but its decrease is not a
certificate of actual variance reduction.

## 2. Robust interval gate: approved, with an explicit margin

For an old probability vector `p` and candidate `q`, suppose the exact old
continuation contributions satisfy `L_i <= A_i <= U_i`. Put
`d_i = 1/q_i - 1/p_i`. The computable condition

\[
\sum_{d_i\geq0}d_iU_i+\sum_{d_i<0}d_iL_i\leq0
\]

implies the local comparison needed in Section 1. It is the maximum of the
true objective difference over the specified rectangular uncertainty set.
Finite-depth moments provide lower bounds only when their integration errors
are controlled; ordinary quadrature outputs are not verified lower bounds.

For the binary uniform baseline, write the old contributions as `(A,B)`.
Suppose `A >= a > b >= B >= 0`. Every supported probability

\[
\frac12\leq q\leq\frac{a}{a+b}
\]

for the first alternative is safe. If `b=0`, retain `q<1` unless the second
alternative has been removed by exact pruning. For `1/2<q<1`, the improvement
margin satisfies

\[
2(A+B)-\left(\frac A q+\frac B{1-q}\right)
\geq
\delta(a,b,q)
:=a\left(2-\frac1q\right)
 +b\left(2-\frac1{1-q}\right).
\]

The stated safe interval is exactly the condition `delta >= 0`. For `b>0`, the
choice `q=sqrt(a)/(sqrt(a)+sqrt(b))` maximizes this conservative margin and gives
`delta=(sqrt(a)-sqrt(b))^2`. Rational `q` is preferable when the acceptance check
is intended to use exact rational arithmetic.

The local margin does not itself equal the root variance reduction. A root
with a singleton tuple can benefit only through descendants. Strict root
improvement needs either a positive-measure propagation argument through
reachable nonzero subtrees or disjoint verified root intervals. Nonstrict
dominance follows directly from Section 1.

## 3. Mean invariance extends to supported nonuniform policies

For a completed labelled topology `theta`, put all time and spatial marks into
`xi`, with a common policy-independent reference measure. Let `G_theta(xi)` be
its target integrand, and let `Q_q(theta,xi)` be the product of the actual
conditional tuple probabilities. Then the proposal density contributes `Q_q`
and the estimator contributes `1/Q_q`. Consequently

\[
\mathbb E_q|H_q|
=\sum_\theta\int|G_\theta(\xi)|\,d\nu_\theta(\xi)
\]

is independent of the supported policy as an extended nonnegative integral.
Tonelli justifies this equality even before its finiteness is known. Exact
lifetime likelihoods can be cancelled in the same way if rates are changed.

One integrable baseline therefore makes every other nonexplosive, fully
supported policy integrable at the same root. Absolute convergence then permits
the signed topology sum, and all policies have the same mean. The old
Allen–Cahn PDE mean-identification argument can consequently transfer once its
assumptions cover the specified terminal data and horizon. In particular its
six normalized first-moment fields must be bounded uniformly for every
`x in R` and `0 <= remaining time <= T`; a uniform six-code second-moment
envelope supplies this through Cauchy–Schwarz. Pointwise finiteness alone does
not give that bounded mild-uniqueness argument. A formula for the PDE solution
alone is not an identification proof.

For the proposed six-coordinate certificates, explicitly require that the
proposal for `F_k^a` depends on `k` but not on its scalar `a`. This preserves
`M(F_k^a)=a^2 M(F_k^1)` and permits the normalized closure. An arbitrary callback
depending on `a` need not admit that closure.

## 4. Joint static rate/probability convexity: approved contract

Use finitely many probability rows `q_g=(q_g1,...,q_gm_g)` in the open simplices.
Assign each optimized code to a row using a parameter-independent map; labels
remain distinct, including duplicate tuples. Unoptimized rows remain fixed and
supported. Count the occurrences of row/label pair `(g,i)` on a completed tree
by `n_gi`. Let `N` count all branching expiries, including decisions with fixed
probabilities, and let `L` be the sum of all clipped particle lifetimes.

On the common space of completed physical trees,

\[
M(\lambda,q)
=\sum_\theta\int W_\theta(\xi)
 e^{\lambda L}\lambda^{-N}
 \prod_{g,i}q_{gi}^{-n_{gi}}\,d\nu_\theta(\xi),
\qquad W_\theta\geq0.
\]

Here `W` contains the squared terminal/coefficient factors and inverse fixed
tuple probabilities, and is independent of all optimized parameters. Common
full support and nonexplosion justify the expansion. No differentiation and no
finite moments are required to state it in the extended nonnegative reals.

The logarithm of every positive path factor is

\[
\lambda L-N\log\lambda-\sum_{g,i}n_{gi}\log q_{gi},
\]

which is jointly convex in the **direct rate and direct probabilities**.
Pointwise log-convexity followed by Hölder over the disjoint union of topology
mark spaces proves joint log-convexity of `M`. In particular the finite-moment
domain is convex. Subtracting the common squared mean preserves ordinary
convexity of variance, but does not in general preserve log-convexity.

Do not assert uniqueness or interior attainment for `q` without further
conditions. Unused rows can be flat directions; exactly-zero alternatives can
drive the optimum to the boundary. Compact supported parameter boxes and one
finite incumbent give existence by lower semicontinuity, but not uniqueness.
The older scalar existence theorem does not automatically supply coercivity in
each probability coordinate.

Under a common integrable bound for the differentiated path integrands, the
ambient-coordinate derivatives are

\[
\partial_\lambda M
=\mathbb E_{\lambda,q}[H^2(L-N/\lambda)],
\qquad
\partial_{q_{gi}}M
=-\mathbb E_{\lambda,q}[H^2 n_{gi}/q_{gi}].
\]

The ambient expression extends the topology integral off the simplices;
physical probability derivatives must be taken in tangent directions or with
the simplex constraints. The Hessian integrand is the positive path factor
times

\[
ss^\top+\operatorname{diag}\left(N/\lambda^2,
                                  (n_{gi}/q_{gi}^2)_{g,i}\right),
\quad
s=(L-N/\lambda,(-n_{gi}/q_{gi})_{g,i}).
\]

These formulas require their stated domination. A finite second moment at one
point alone does not license differentiating an infinite-depth sum. A tilted
bound on a parameter neighborhood is one sufficient route because `L` and all
`n_gi` are controlled by `1+N` under bounded arity and finite horizon.

This extension is compatible with the existing scalar topology proof. It does
not establish a validated global joint optimizer or optimality among arbitrary
history-dependent policies.

## 5. Scope of the proposed concrete controls

For constant Allen–Cahn terminal data, the first-derivative subtree is zero
pathwise: every finite nonzero-branch candidate retains a descendant first
derivative, and all its terminal factors vanish. Thus the second alternative in
each `F0`, `F1`, and `F2` row has zero contribution. Increasing the first-label
probability from `1/2` to `19/20` is a valid full-tree improvement at every
starting state for which the baseline has finite moments.

For the wave, the second `F2` alternative contains `F4`, an identically zero
code. Changing only this row to `19/20` is likewise universally safe. These are
useful exact controls for the new certificate machinery, but the improvement is
exact-zero reallocation, not a demonstrated advantage of estimated nonzero
continuation moments over the terminal proxy.

At the actual wave terminal state `x=0`, `phi=-1/2` and `phi'=1/4`. The two `F0`
terminal contributions are both `9/1024`, so its terminal proxy is uniform
there. For `F1`, their ratio is `36`. These values are algebraic interface
checks, not finite-horizon optimal probabilities.

The planned horizons `0.05`, `0.2`, and `0.5` and rates `0.75`, `1` are a useful
bounded matrix. Failed certificates at a longer horizon should be retained as
failures of the tested bound unless an independent divergence proof is given.
Measure root moment/variance bounds at common rates before describing joint
tuning. No measured outcome was supplied to this reviewer at writing time.

### A stronger wave control with two nonzero alternatives

An additional conventional derivation during this review removes the need to
use only the exact-zero `F2` control. It proves a spatially uniform safe bias in
the `F1` row, with both alternatives nonzero.

Fix the old raw uniform policy and denote its normalized second-moment fields
at remaining time `r` by

\[
D=M_D,\quad F=M_{F0},\quad B_1=M_{F1},\quad C=M_{F2},
\quad E=M_{F3}=36e^{\lambda r}.
\]

Assume a verified uniform envelope `B_1(r,x) <= b_*` for `0 <= r <= T`, as
provided by the existing six-code wave certificate. Define

\[
\alpha=\lambda+b_*/\lambda.
\]

The wave terminal data satisfy, on writing `z=-phi(x)` in `(0,1)`,

\[
\phi'=z(1-z),\qquad |f(\phi)|=z(1-z^2),
\qquad (\phi')^2\leq\phi^2,
\qquad |f(\phi)|^2\geq(\phi')^2.
\]

The last inequality and killed-moment induction prove `F >= D` pointwise:
the `F0` branch polynomial is `2 F B_1 + D^2 C/2`, whereas the `D` branch
polynomial is `D B_1`. All coefficients are nonnegative and the first expression
is at least the second whenever `F >= D`.

The linear equation for `D`, or iteration of its nonnegative Volterra kernel,
gives

\[
D(r,x)\leq e^{\alpha r}P_r[(\phi')^2](x)
         \leq e^{\alpha r}P_r[\phi^2](x).
\]

For completeness, divide the `D` equation by `e^{lambda r}` and replace `B_1`
by `b_*`. The `n`-fold semigroup/time integral is
`(b_* r/lambda)^n/n!` times `P_r[(phi')^2]`; summing proves the bound. Uniform
finiteness from the envelope makes the remainder vanish.

The `F2` leaf term alone supplies

\[
C(r,x)\geq36e^{\lambda r}P_r[\phi^2](x).
\]

Combining these statements proves

\[
F(r,x)C(r,x)
\geq e^{-\alpha r}E(r)D(r,x)^2
\geq4e^{-\alpha T}\,\frac{D(r,x)^2E(r)}4.\tag{W1}
\]

The two terms in (W1) are exactly the first and second `F1` conditional branch
contributions before averaging over a shared branch position. Applying `P_s`
preserves the inequality, so it matches the current pre-position callback for
every parent state and delay. Scalar `F1^a` rows multiply both sides by `a^2`.

Since `exp(-u) >= 1-u`, the rational quantity

\[
R=4\left[1-(\lambda+b_*/\lambda)T\right]\tag{W2}
\]

is a conservative lower bound on the contribution ratio. If `R >= 2`, the
binary gate certifies the update `p1=2/3`, uniformly over all states and times.
Indeed `A >= 2B` implies

\[
2(A+B)-[3A/2+3B]=A/2-B\geq0.
\]

The proof uses continuation moment comparison and the full-time `F1` envelope;
it is not a terminal-only optimizer. For the wave, `D>0` at every finite spatial
point because its terminal heat contribution is positive, so both `F1` branch
contributions are positive. With `R>2`, the local comparison is strict.
The `p1=2/3` update may be combined with the safe `p2=19/20` update: both are
compared with the same old uniform moment field in Section 1.

**Strict improvement reaches the Id root.** Keep `p0=1/2`, take `p1=2/3`, and
choose either `p2=1/2` or `p2=19/20`. Write `M` for the old moments and `M'` for
the new moments. Section 1 gives `M' <= M` for every coordinate. At an `F1`
root with positive remaining time, the local residual is bounded below by

\[
\int_0^r\frac{e^{\lambda s}}\lambda
\left(\frac R2-1\right)
P_s\!\left[\frac{D(r-s,\cdot)^2 E(r-s)}4\right](x)\,ds>0.
\]

It is finite because the baseline moment is finite, and it is strictly positive
because `R>2`, `E>0`, and the wave derivative's heat contribution is positive
at every finite point. Since `M'_F1 <= (Phi_q' M)_F1`, this proves
`M_F1 > M'_F1` everywhere at positive remaining time.

The `F0` first-label probability remains `1/2`, and all its source products
decrease. In particular

\[
M_{F0}M_{F1}-M'_{F0}M'_{F1}
\geq M'_{F0}(M_{F1}-M'_{F1})>0
\]

at positive child remaining time: `M'_F0` has the strictly positive leaf
contribution `exp(lambda r) P_r[f(phi)^2]`. Integrating this first-label source
over any nonempty branch-time interval yields `M_F0 > M'_F0` at every positive
remaining time. Finally, the Id source is just `F0`, so its unchanged kernel
integrates this positive difference and gives

\[
\boxed{M_{\mathrm{Id}}(r,x)>M'_{\mathrm{Id}}(r,x)
\quad\text{for every }0<r\leq T,\ x\in\mathbb R.}\tag{W3}
\]

This is the positive `Id -> F0 -> F1` event chain expressed directly through
the exact moment equations. The common-mean argument makes (W3) strict variance
reduction. It supplies no numerical lower bound on the size of that reduction.

This reviewer ran the existing exact-rational wave envelope at `T=1/20`,
100 steps, default 48-bit dyadic outward grid, no tilt. The checker accepted
both returned witnesses, and exact rational comparison gave `R>2`:

| Rate | Verified `b_*` | Rational `R` | Approximate `R` |
|---|---|---|---|
| `3/4` | `367388011711017/70368744177664` | `216186910784669/87960930222080` | `2.4577606244` |
| `1` | `10882937418847/2199023255552` | `30898504436641/10995116277760` | `2.8102026078` |

The source was `parabolab/rate_certificate.py`, SHA-256
`9843be2680ea6bbf6e79003dbd3250c1ccc666cb441c2945d692fd2f83d69322`.
The standard `python` package import first failed because that interpreter had
no NumPy. The successful check loaded this standard-library-only certificate
module directly with `importlib.util.spec_from_file_location`, then called
`enclose_allen_cahn_moment(family='wave', horizon=Fraction(1,20),
rates=(lambda,lambda), steps=100)` and `verify_moment_enclosure`.
These are certificate-algebra checks, not Monte Carlo variance measurements or
a fresh formalization of (W1).

The independently executable standard-library script `wave_gate_check.py`
now saves full baseline witnesses in `wave-gate-checks.json`, together with
exact gate margins and source/script hashes. Both generation and a separate
`--verify` pass completed successfully. The compact canonical-JSON witness
hashes are:

- Rate `3/4`: `14cb6810d8d6e7721ecc411d0a66d5fe5ef0bae1192fb41969cc1cee3adc205a`.
- Rate `1`: `4e918a663fe5373f63fc0e97d879df2dce95f2a6dabddbb7a1dc56605c5f32de`.

An incorrect recorded ratio was rejected by exact recomputation. An altered
last-step `F1` upper endpoint was rejected by the uniform witness verifier even
after its archive hash was recomputed. These probes check the finite acceptance
path; they do not formally verify the Python interpreter or the analytic
correspondence.

## 6. Primary-source literature and novelty boundary

The following bounded search was performed on 16 September 2026. It is not an
exhaustive novelty search.

- Ryu and Boyd prove convex variance optimization in exponential-family natural
  parameters, and analyze an adaptive Monte Carlo procedure under additional
  moment assumptions. This is direct precedent for convex importance-sampling
  optimization. The present tree result uses direct probabilities and a random
  branching exposure, so the parameterization and recursive certification must
  be supplied explicitly. [Author manuscript, Theorem 1 and Section 4](https://stanford.edu/~boyd/papers/pdf/adaMC.pdf).
- Badouraly Kassim, Lelong and Loumrhari change Gaussian means and Poisson
  intensities, prove convexity and derivative formulas for the second-moment
  objective, and optimize sample-average approximations. Their inverse
  intensity powers are particularly close to the tree topology factors. Joint
  convexity is therefore a useful project extension, not evidence of a new
  generic optimization principle. [Primary preprint, Proposition 2.1](https://arxiv.org/pdf/1307.2218).
- Awad, Glynn and Rubinstein characterize zero-variance measures for a class of
  Markov-process expectations and bound approximate proposals using Lyapunov
  inequalities. This is close methodological precedent for certifying proposal
  quality with a supersolution. The present operator has nonlinear child
  products, and the local comparison is with a previous finite-moment policy.
  [Author manuscript](https://web.stanford.edu/~glynn/papers/2013/AwadGRubinstein13.pdf).
- Blanchet, Glynn and Leder connect Lyapunov inequalities and subsolutions for
  efficient importance sampling. This further limits novelty claims about the
  certificate principle itself. [Author publication page](https://web.stanford.edu/~glynn/papers/2012/BlanchetGLeder12.html).
- Henry-Labordère, Oudjane, Tan, Touzi and Warin analyze branching PDE estimators,
  moment conditions, lifetime choices, variance reduction and particle cost.
  These precedents preclude presenting offspring/lifetime tuning in general as
  new. [Primary preprint, Sections 3–6](https://arxiv.org/html/1603.01727).
- Meester proves exponential convergence for adaptive importance sampling in a
  class of Markov-chain expectation problems. A continuation-based adaptive
  sampler is not new merely because it iterates toward an oracle.
  [Primary preprint](https://arxiv.org/abs/1806.03029).

The plausible contribution is the combination of explicit support-safe
continuation interval tests, unrestricted derivative-coded-tree comparison,
transfer of integrability/common mean, and concrete exact certificates beyond
the previously fixed uniform-proposal cases. Publication novelty remains
unestablished; the moderate exact-zero controls do not by themselves settle it.

## 7. Independent review of C8: exact flat moment-divergence boundary

Additional research review T05, 16 September 2026. C8 and the proposed
rate-optimized corollary are mathematically correct under their explicit raw
mechanism, constant supported probabilities, flat `phi=1/2`, and common positive
rate assumptions. This section reviews the conventional argument; it does not
claim Lean coverage of the variable transformations or divergence theorem.

### Variable changes and the root coordinate

The exact flat moment system, with `D=0`, is

\[
\begin{aligned}
i'&=\lambda i+a/\lambda,&
a'&=\lambda a+ab/(\lambda p_0),\\
b'&=\lambda b+ac/(\lambda p_1),&
c'&=\lambda c+ae/(\lambda p_2),&
e'&=\lambda e.
\end{aligned}
\]

Its initial values are `(i,a,b,c,e)=(1/4,9/64,1/16,9,36)`. Factoring out
`exp(lambda*tau)` cancels the linear terms. For the nonlinear coordinates, the
remaining common multiplier is `exp(lambda*tau)/lambda`, which is exactly
`dtheta/dtau` for `theta=(exp(lambda*tau)-1)/lambda^2`. Thus the three equations
in C8 have the stated coefficients; no additional rate factor is missing.

Since `z_a(0)=9/64>0` and its derivative is nonnegative, division by
`ds/dtheta=z_a` is legitimate throughout the finite solution. Successively
integrating `dz_c/ds=36/p2`, `dz_b/ds=z_c/p1`, and `dz_a/ds=z_b/p0` gives exactly
the cubic `P_p(s)` in C8. Conversely these identities reconstruct the original
locally Lipschitz polynomial ODE with its initial values. The scalar separation
argument therefore identifies its maximal finite solution.

The Id step merits a separate calculation because a divergent child can have
an integrable singularity in some other systems. Here

\[
\frac{dz_i}{d\tau}=\frac{z_a}{\lambda},\qquad
\frac{dz_i}{d\theta}=\frac{z_a}{1+\lambda^2\theta},\qquad
\frac{dz_i}{ds}=\frac1{1+\lambda^2\Theta_p(s)}.
\]

Every equality checks directly by the chain rule. Because
`0 <= Theta_p(s) < theta_* < infinity`,

\[
z_i(s)\geq\frac14+
\frac{s}{1+\lambda^2\theta_*}\longrightarrow\infty.
\]

Multiplying by the positive finite clock factor at the threshold preserves
divergence. Thus the root, not merely the nonlinear code subsystem, has the
claimed boundary.

### Why the ODE boundary is the exact full-tree boundary

For every horizon strictly below the scalar blow-up time, the classical
positive ODE solution is finite and bounds the zero-seeded killed-moment
iterations. Their monotone limit is therefore a finite solution of the same
Volterra system. Polynomial local Lipschitz uniqueness identifies it with the
classical ODE solution. This closes the finite direction without assuming the
unrestricted moment is finite in advance.

At the boundary, the full flat moments are nondecreasing in remaining time.
This can be established directly for each killed iterate: after writing its
convolution with `v=tau-s`, it has the form

\[
V_{n+1}(\tau)=e^{\lambda\tau}y_0+
\frac1\lambda\int_0^\tau e^{\lambda(\tau-v)}G_p(V_n(v))\,dv.
\]

Increasing `tau` enlarges a nonnegative integral and its positive exponential
factor. Passing to the supremum in depth preserves the order. Since the Id
moment tends to infinity from below the threshold, monotonicity makes it
infinite at the threshold and at every later time. No continuation of the
classical ODE beyond its blow-up point is used.

For common first-label probability `p`, the substitution `s=pv` leaves the
cubic denominator independent of `p`, and contributes exactly one factor `p`
from the integration measure. Hence

\[
\theta_*=pC,\qquad
\tau_* =\frac{\log(1+\lambda^2pC)}\lambda,
\qquad
M_{\mathrm{Id}}(\tau)<\infty\ \Longleftrightarrow\ \tau<\tau_*.
\]

This is moment divergence of an almost surely finite tree. It is neither
explosion of the number of particles nor blow-up of the bounded Allen–Cahn PDE
solution. Where a supported candidate has finite all-code moments, its envelope
and C6 transfer a finite common absolute/signed mean to the uniform estimator.
There, infinite root second moment is indeed infinite variance.

### Independent exact arithmetic check at T=1/2

This reviewer ran a separate standard-library rational calculation, without
using the new C8 integration implementation. It used decreasing left/right
rectangles for `1/P0` on `[0,8]` with 8192 equal cells, dyadic outward rounding
at denominator `2^60`, and the cubic tail inequalities written in C8. It gave

\[
\frac{387642074935326725255758957}{253922826375521540551737344}
\leq C\leq
\frac{5431912879351002976105}{3541774862152233910272}.
\]

The decimal interval is approximately `[1.5266137372,1.5336697252]`; these
decimals are only a display of the exact rational bounds. For `lambda=3/4`,
`T=1/2`, the comparison variable is
`theta=(exp(3/8)-1)/(9/16)`. A degree-24 positive Taylor lower sum and a
geometric upper bound for its remainder enclosed this exponential. Exact
rational comparisons established

\[
\theta_{\rm lower}>\tfrac12 C_{\rm upper},\qquad
\theta_{\rm upper}<\tfrac{19}{20}C_{\rm lower}.
\]

The separation margins were respectively about `0.04203876` and `0.64140942`.
Thus the flat uniform estimator has infinite second moment at this parameter
pair while the common `p=19/20` estimator has finite second moment. This
conclusion does not rely on the earlier enclosure failure or on an empirical
Monte Carlo variance. The independent arithmetic check was executed in a
terminal cell; the main run's separate C8 artifact is the durable reproduction
entry point.

### Optimizing the rate preserves an exact horizon gain

Let `z=lambda^2 p C`. Then

\[
\tau_*(\lambda,p)=\sqrt{pC}\,
\frac{\log(1+z)}{\sqrt z}.
\]

The factor depending on `z` tends to zero at both endpoints `0` and infinity.
Its derivative has the sign of
`h(z)=2z/(1+z)-log(1+z)`. The identity

\[
h'(z)=\frac{1-z}{(1+z)^2}
\]

shows that `h` increases from zero until `z=1`, then decreases to minus
infinity. Since `h(1)=1-log(2)>0`, it has exactly one positive zero `z_*>1`,
which is the unique maximizer of the horizon factor. Consequently

\[
H_*(p):=\max_{\lambda>0}\tau_*(\lambda,p)
=\sqrt{pC}\,K,\qquad
K=\frac{\log(1+z_*)}{\sqrt{z_*}},
\]

and the usable finite-second-moment horizons are strictly below `H_*(p)`.
The maximum of the threshold is attained, but the finite-moment region excludes
that endpoint. In particular

\[
\boxed{\frac{H_*(19/20)}{H_*(1/2)}=\sqrt{19/10}.}
\]

This comparison optimizes the rate separately for each fixed proposal, so its
horizon gain is not attributable solely to a poor baseline rate. A floating
bisection, used only as a diagnostic, gave `z_* ≈ 3.9215536346`,
`K ≈ 0.8047423425`, and `sqrt(19/10) ≈ 1.3784048752`.

### Existing work and contribution boundary

Repository searches found the six-code ODE/envelope construction, the separate
standard-binary Riccati oracle, and empirical horizon diagnostics, but no
previous exact cubic reduction for the raw flat derivative-coded second moment.
The standard-binary result concerns another estimator and cannot supply this
threshold.

ODE-based branching moment conditions and finite-time limitations are
established. Henry-Labordère and coauthors use scalar ODE bounds to prove moment
finiteness; Bouchard, Tan and Warin use explicit lower bounds on admissible
local horizons in a branching approximation. These are relevant precedents for
the method and motivation. [Henry-Labordère et al., Theorem 3.12](https://arxiv.org/html/1603.01727),
[Bouchard–Tan–Warin](https://arxiv.org/html/1710.10933).

The original coding-tree paper and Huang–Privault's later stability paper
include Allen–Cahn examples. The latter also treats constant terminal data and
proves absolute first-moment integrability bounds for its different mechanism.
The inspected portions did not supply this raw-mechanism second-moment
threshold; the bounded search does not establish worldwide novelty.
[Nguwi–Penent–Privault](https://arxiv.org/html/2201.03882),
[Huang–Privault, Sections 2.3 and 4](https://arxiv.org/html/2502.17853v2).

For flat `phi=1/2`, the already-existing
`TerminalTupleProposal(floor_mass=0.1)` produces exactly `p0=p1=p2=19/20`:
only the first terminal score is nonzero in each of these rows. Therefore the
candidate sampler is not newly invented by C8. The incremental result is the
exact finite-versus-infinite moment law, the root divergence proof, and the
proposal-dependent horizon comparison, alongside the separate nonzero wave
policy theorem.
