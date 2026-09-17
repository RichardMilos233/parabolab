# Full-tree tuple-policy improvement

Conventional proofs under explicit hypotheses. The square-root importance rule and monotone fixed-point comparison are established principles; publication novelty of this coding-tree combination is unestablished.

## C1. Exact policy improvement

Fix lambda>0, finite horizon, countable codes, measurable terminal factors and Markov kernels, finite nonempty labelled tables of uniformly bounded arity, shared child birth positions and conditionally independent descendants. Policies q,q' are measurable, positive on every retained label and depend only on available pre-selection state. Include depth in the state if used. Common exponential clocks and bounded arity imply nonexplosion.

Let M=M_q be the finite old-policy second-moment field on **all reachable states/codes**, and Phi_q its exact nonnegative first-event operator. Given birth (t,x,c) and branch delay s, the actual callback's conditional contributions are

\[
A_i(M;t,x,c,s)=P_s[\prod_{z\in Z_{c,i}}M_z(t+s,\cdot)](x).
\]

Coefficients encoded in children remain inside the product. Apply the semigroup **after** multiplying. This is not a product of separately averaged moments, nor a score conditioned on the unavailable branch position.

If at every such state and almost every delay

\[
\sum_i A_i(M)/q'_i\le\sum_i A_i(M)/q_i, \tag{1}
\]

then **M_q' <= M_q pointwise**, even though every descendant changes policy.

Proof: unchanged survival term and integration of (1) against exp(lambda*s)/lambda give Phi_q'(M)<=Phi_q(M)=M. Set v_0=0, v_(n+1)=Phi_q'(v_n). The operator is order preserving, so induction gives v_n<=M. Nonexplosion and monotone convergence identify sup_n v_n with M_q'. This retains new-policy descendant dependence through the iteration, rather than freezing it.

Common signed integrable means transfer the comparison to variance. A local deficit delta>=0 gives M-Phi_q'(M) equal to its weighted time integral; since M_q'<=Phi_q'(M), that integral is also a lower bound on the decrease. A singleton root may have zero immediate deficit even if descendants improve; strictness at an unreachable code does not imply strict root improvement.

## C2. A computable interval gate

For rigorous finite nonnegative bounds L_i<=A_i(M)<=U_i, put d_i=1/q'_i-1/q_i. Termwise multiplication with the appropriate sign gives

\[
\sum_i d_i A_i(M)\le R:=\sum_{d_i\ge0}d_i U_i+\sum_{d_i<0}d_i L_i. \tag{2}
\]

**Accept only if R<=0; otherwise keep q.** This sufficient test must cover all reachable decisions for C1 to apply; passing a sampled mesh is insufficient.

For a binary uniform baseline with true contributions A,B, assume 0<=a<=A, 0<=B<=b and

\[
1/2\le p<1,\qquad p(a+b)\le a. \tag{3}
\]

Then A/p+B/(1-p)<=2(A+B). Indeed (p-1)A+pB<=(p-1)a+pb<=0, and

\[
[ A/p+B/(1-p)-2(A+B)]p(1-p)
=(2p-1)[p(A+B)-A]\le0. \tag{4}
\]

If a>b>=0, any rational p strictly between 1/2 and a/(a+b) gives a strict endpoint deficit. For b>0, p=sqrt(a)/(sqrt(a)+sqrt(b)) makes that worst-case deficit -(sqrt(a)-sqrt(b))². For b=0 keep p<1 for support. An observed zero does not establish b=0.

The gate tolerates intervals instead of simultaneous relative accuracy near zero, but it can be conservative. It cannot turn unvalidated quadrature or noisy pilots into rigorous L,U.

## C3. Two failed shortcuts

If U>=M_q and Phi_q'(U)<=U, iteration gives only M_q'<=U. It does **not** imply M_q'<=M_q. Scalar constant maps Phi_q(v)=1 and Phi_q'(v)=2 share the supersolution U=3, yet their fixed points increase.

A positive support floor likewise gives no improvement theorem. Actual A=B=1 has uniform objective 4, but proxy scores (100,1) give p=10/11 and objective 121/10=12.1. Terminal-proxy greedification can therefore worsen a conditional moment.

## C4. Joint convexity without frozen continuations

Restrict to static probabilities in finitely many compatible code/label groups, all positive, each group summing to one. Grouping, mechanism, motion and terminal values are parameter independent. Normalized F-code policies must also be independent of scalar multipliers.

For a completed marked labelled tree, let N count branch events, L total clipped particle lifetime, n_gi each group/label count. Density cancellation gives

\[
M(\lambda,q)=\sum_\theta\int W_\theta(\xi)
 e^{\lambda L}\lambda^{-N}\prod_{g,i}q_{gi}^{-n_{gi}}\,d\nu_\theta(\xi), \tag{5}
\]

where W>=0 and the measure are parameter independent. Bounded arity gives nonexplosion; Tonelli justifies the extended nonnegative integral. Labels and repeated children remain distinct. Here completed nonzero physical trees are counted, or equivalently the unpruned space is integrated with zero integrands on absorbing-zero events. Truncated zero branches are not counted as nonzero completions.

Each nonzero kernel has convex logarithm

\[
\lambda L-N\log\lambda-\sum_{g,i}n_{gi}\log q_{gi}. \tag{6}
\]

Apply this inequality to linear interpolation of parameters and then Hölder to the sum/integral. M is **jointly log-convex between finite endpoint values**, hence an extended jointly convex objective with convex finite domain. The killed-depth objectives have the same property. Common means imply joint convexity of variance, but subtracting the squared mean need not preserve log-convexity.

This extends the project's scalar theorem and specializes established importance-sampling convexity. It does not supply an oracle or a global joint optimizer. Unused/zero labels can create flat directions: F3's branch labels both give zero. An open simplex need not attain its infimum. On a compact positive rate interval with closed positive floors, a finite incumbent and Fatou lower semicontinuity give attainment.

Under the **additional** domination needed for twice differentiating, the unconstrained Hessian is the integral of k*(s s^T+D), with s=(L-N/lambda,-n_gi/q_gi) and D=diag(N/lambda²,n_gi/q_gi²). For binary coordinates p,1-p, the score is -n0/p+n1/(1-p) and diagonal is n0/p²+n1/(1-p)². This PSD identity is not needed for (5)'s proof. Finite second moment alone is not asserted to justify differentiation.

## C5. Nonuniform Allen–Cahn closure and safe controls

For raw f(u)=u-u³ and normalized states (i,d,a,b,c,e)=(Id,D,F0,F1,F2,F3), static first-label probabilities (p0,p1,p2) give

\[
G_p=(a,bd,ab/p_0+d²c/[4(1-p_0)],
ac/p_1+d²e/[4(1-p_1)],ae/p_2,0). \tag{7}
\]

The 1/4 is the square of -1/2; d² retains both D children. F2's second label and both F3 labels are exactly zero, but retain positive probability. At p0=p1=p2=1/2 this exactly recovers the existing uniform polynomial. Scalar-independent q preserves normalized homogeneity by finite-tree coupling.

For constant terminal data, full-tree moments solve the minimal nonnegative system y'=lambda*y+G_p(y)/lambda with the existing flat terminal vector. For wave terminal data, using the coordinatewise terminal suprema yields only a spatially uniform upper bound.

The field F is monotone and nonnegative on the orthant. If v>=u>=0 and u+h F(v)<=v, the straight line from u to v is a supersolution for that step. A nonnegative lower endpoint l_new<=l+h F(l) stays below the true endpoint because the solution is nondecreasing and F monotone. Rational outward rounding preserves these inequalities; chained witnesses enclose the solution. Failed box search is inconclusive.

Flat derivative trees have D=0: every D branch contains another D, and all derivative terminal leaves vanish. All F-code second alternatives then vanish. Raising p0,p1,p2 from 1/2 to 19/20 satisfies C2 everywhere; C1 gives full-tree improvement wherever the old all-code moment is finite. For wave data, change only p2 to 19/20; the second F2 alternative is structurally zero at every x, so C1 still gives nonincrease. Envelope comparisons alone do not quantify its root variance reduction.

These are exact-zero reallocation controls, not evidence of learned continuation superiority or a new pruning principle.

## C6. Common means under supported policy changes

At absolute-moment order one, q and lifetime densities cancel at each finite depth. The killed absolute first-moment recursion is therefore independent of positive q and lambda. For the Allen–Cahn PDE identification below, require a finite six-code second-moment envelope uniformly over every x in R and every remaining time in [0,T]. It supplies uniformly bounded normalized absolute first moments by Cauchy–Schwarz; pointwise all-code finiteness alone would not justify bounded mild-system uniqueness. Nonexplosion and monotone convergence give those same absolute first moments for other supported policies. Dominated convergence of killed signed functionals gives common signed means.

The existing Allen–Cahn signed mild-system/uniqueness proof identifies the same PDE solution: its cancelled signed recursion is unchanged. This explicitly extends the old uniform-only statement; it does not reinterpret an old witness as a certificate for new q.

For flat phi=1/2, the mean square is 1/(1+3 exp(-2T)). Certified second-moment differences equal variance differences exactly. Relative variance percentages require controlling the mean-square evaluation error; floating reference percentages must be labelled.

## C7. A globally safe nonzero wave update

This advances beyond the zero-branch controls. Use the old **uniform** wave moments at remaining time r, writing `(I,D,A,B,C,E)` for `(Id,D,F0,F1,F2,F3)`. Assume the old six-code uniform spatial/time envelope is finite through T and bounds `B<=Bbar`. Let `s=1/(1+exp(x))`, so terminal phi=-s and phi'=s(1-s).

First, `|f(phi)|²=s²(1-s²)² >= s²(1-s)²=|phi'|²`. The uniform moment sources for A and D are `2AB+D²C/2` and `BD`. Starting both killed recursions at zero, induction preserves A>=D, since `2AB>=DB` whenever A>=D and B>=0. Taking the full-tree limit yields **A>=D everywhere**.

Second, the D moment equation has potential `lambda+B(r,x)/lambda`. Bounded-potential comparison (equivalently iteration of its linear mild equation) and `|phi'|²<=phi²` give

\[
D(r,x)\le e^{(\lambda+\bar B/\lambda)r}P_r[\phi²](x). \tag{8}
\]

The nonnegative F2 branch source gives its survival lower bound

\[
C(r,x)\ge36 e^{\lambda r}P_r[\phi²](x),
\qquad E(r,x)=36e^{\lambda r}. \tag{9}
\]

Combining (8)–(9), without dividing by D, gives

\[
A C\ge D C\ge36e^{-\bar B r/\lambda}D²
=4e^{-(\lambda+\bar B/\lambda)r}\,[D²E/4]. \tag{10}
\]

Thus the two **nonzero F1** tuple products satisfy first >= R times second, uniformly over all child birth positions and all r<=T, where

\[
R=4e^{-(\lambda+\bar B/\lambda)T}
\ge R_{\rm rat}:=4[1-(\lambda+\bar B/\lambda)T]. \tag{11}
\]

The lower bound follows from exp(-z)>=1-z. Apply the same positive Markov semigroup to both sides: the dominance remains true for the actual callback's conditional contributions before the branch position is drawn. If `R_rat>=2`, (3) with `p=2/3` accepts the update. Keep F0 at 1/2 and independently raise F2 to 19/20 using its exact-zero second label. C1 applies to the **simultaneous** policy `(1/2,2/3,19/20)`, because all gate checks refer to the same old uniform moment field. The new descendants need not satisfy the old dominance relation; the old field is already a supersolution for their new operator.

This conclusion is actual full-tree second-moment nonincrease, not merely a smaller majorant. It is restricted to rates/horizons whose checked old envelope makes (11) at least 2. Negative R_rat or a failed envelope is inconclusive. It does not identify an optimal q or imply the terminal proxy is worse. The strictness argument below proves an actual root decrease; a numerical magnitude requires separate root evaluation.

The exact wave-gate script records the baseline witness, Bbar, rational R, verification and source digests. It is a deterministic certificate, not a stochastic confidence interval. See C7 in the claim ledger for executed instances.


### C7 strictness at every finite wave root

For `R_rat>2`, the F1 local decrease is at least `(R_rat/2-1)*(D²E/4)>0` whenever child remaining time is positive: D has a strictly positive wave terminal heat contribution, and E>0. Therefore `M_F1-M'_F1>0` by integration and `M'<=Phi_new(M)`. For F0, whose probabilities remain uniform, all products decrease, and

\[
M_{F0}M_{F1}-M'_{F0}M'_{F1}
\ge M'_{F0}(M_{F1}-M'_{F1})>0.
\]

Here `M'_F0` has a strictly positive terminal heat contribution at every finite x. Its first branch label thus gives `M_F0>M'_F0` at every positive remaining time. The Id equation integrates this strict F0 difference, proving `Var_old(H_Id)>Var_new(H_Id)` for every finite x and every `0<r<=T` in the certified cases. This does not quantify the size; it also applies to F1-only `(1/2,2/3,1/2)` without the F2 change. See independent review W3.

## C8. Exact flat-data variance-explosion time

This additional result was derived after the predeclared flat experiment failed to enclose the uniform moment at T=1/2, lambda=3/4. That failure alone proved nothing. The reduction below supplies a separate analytical test of actual divergence.

Restrict to flat terminal phi=1/2 and constant positive p0,p1,p2<1. D=0 exactly. Write a,b,c,e for F0,F1,F2,F3 second moments, and factor out the linear clock term: `(a,b,c,e)=exp(lambda*tau)*(z_a,z_b,z_c,z_e)`. The initial data are `(a0,b0,c0,e0)=(9/64,1/16,9,36)`. Define a new time

\[
\theta=(e^{\lambda\tau}-1)/\lambda²,
\qquad d\theta/d\tau=e^{\lambda\tau}/\lambda.
\]

The three nonlinear equations become

\[
\frac{dz_a}{d\theta}=z_a z_b/p_0,\quad
\frac{dz_b}{d\theta}=z_a z_c/p_1,\quad
\frac{dz_c}{d\theta}=z_a e_0/p_2,\quad z_e=e_0.
\]

Set `s(0)=0`, `ds/dtheta=z_a>0`. Dividing by this positive derivative and integrating in s gives

\[
z_c=c_0+e_0s/p_2,\qquad
z_b=b_0+c_0s/p_1+e_0s²/(2p_1p_2),
\]

\[
z_a=P_p(s)=a_0+(b_0/p_0)s+
[c_0/(2p_0p_1)]s²+[e_0/(6p_0p_1p_2)]s³. \tag{12}
\]

Conversely these formulas together with `ds/dtheta=P_p(s)` reconstruct the moment ODE and initial values, so uniqueness identifies the solutions up to their maximal finite time. Separation yields

\[
\Theta_p(s)=\int_0^s\frac{dv}{P_p(v)},\qquad
\theta_*(p)=\int_0^\infty\frac{dv}{P_p(v)}<\infty. \tag{13}
\]

All coefficients are positive; the tail is integrable because the cubic coefficient is positive. The inverse s(theta) exists for `0<=theta<theta_*` and tends to infinity as theta increases to theta_*. Thus all displayed nonlinear moment coordinates diverge at theta_*.

**The Id root diverges at the same time.** It is not enough merely to show that a descendant code blows up. If `i=exp(lambda*tau)*z_i`, its singleton source gives `dz_i/dtau=z_a/lambda`. Consequently

\[
z_i=i_0+\int_0^{s(\theta)}
 \frac{dv}{1+\lambda²\Theta_p(v)}. \tag{14}
\]

This diverges as s→infinity because the denominator is at most the finite constant `1+lambda² theta_*`. Before theta_*, the positive polynomial ODE is finite and supplies a moment envelope, so zero-seeded moment iteration agrees with that solution. At and after theta_*, monotonicity in remaining time of the flat nonnegative moment recursion forces the full Id second moment to be infinite.

For a **common first-label probability** p0=p1=p2=p, substitute s=pv into (13). Then

\[
P_p(pv)=9/64+v/16+(9/2)v²+6v³=:P_0(v),
\quad C:=\int_0^\infty\frac{dv}{P_0(v)},
\]

\[
\boxed{\theta_*(p)=pC,\qquad
\tau_*(\lambda,p)=\lambda^{-1}\log(1+\lambda²pC).} \tag{15}
\]

The root has finite second moment **iff** `tau<tau_*`; the boundary is divergent. This is an exact statement for this particular raw flat Allen–Cahn estimator. It does not locate a wave boundary, remove its signed branching mechanism, or claim a universal integrability formula. At a horizon where the candidate policy has an all-code envelope, C6 ensures the uniform estimator still has the same finite mean, so its infinite second moment is indeed infinite variance.

For rigorous computation of C, f(v)=1/P0(v) is decreasing. Rational left/right rectangle sums on [0,R], with dyadic outward rounding of each integrand, give two-sided finite-integral bounds. Since for v>=R,

\[
6v³\le P_0(v)\le
[6+(9/2)/R+(1/16)/R²+(9/64)/R³]v³,
\]

the tail lies between `1/(2R²[6+(9/2)/R+(1/16)/R²+(9/64)/R³])` and `1/(12R²)`. No floating quadrature estimate is used as a certificate.

Compare the resulting rational p*C interval with `(exp(lambda*T)-1)/lambda²`, enclosing the exponential by its positive Taylor sum and a geometric tail bound. Strict separation certifies which side of the explosion time contains T. Floating quadrature and logarithms are useful diagnostics only. The exact scalar reduction itself is not Lean-formalized in this run.

### C8 corollary: improvement survives reoptimizing the clock

Put z=lambda² pC. Equation (15) gives

\[
\sup_{\lambda>0}\tau_*(\lambda,p)
=\sqrt{pC}\,K,\qquad
K=\max_{z>0}\frac{\log(1+z)}{\sqrt z}. \tag{16}
\]

The scalar function tends to zero at both ends and is positive inside. Its derivative has the sign of `g(z)=2z/(1+z)-log(1+z)`. Since `g'(z)=(1-z)/(1+z)²`, g grows from zero to a positive value at 1 and then decreases to negative infinity. There is exactly one positive critical point z*>1 and it is the maximum. The horizon-maximizing rate is `sqrt(z*/(pC))`; this is a different objective from minimizing variance at a fixed horizon.

Consequently changing common p from 1/2 to 19/20 multiplies the **largest achievable finite-variance horizon threshold**, after reoptimizing lambda, by exactly `sqrt(19/10)` (approximately 1.3784). The threshold itself is divergent; usable finite-variance horizons are strictly below it. This is a 37.84% increase in the horizon threshold for the specified flat estimator, not a 37.84% variance reduction or a timing speedup. As p increases toward 1, the corresponding gain over p=1/2 approaches sqrt(2); p=1 is outside this run's supported raw-label class.
