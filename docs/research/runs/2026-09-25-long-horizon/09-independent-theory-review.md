# Independent theory audit: a sharp raw-tree ceiling and a bounded long-horizon alternative

Status: complete conventional derivations for the statements below; no implementation or Lean work performed by this audit. The formulas were checked directly against `parabolab/mechanism.py`, `parabolab/tree.py`, and C5–C8 of `docs/research/runs/2026-09-16-certified-tuple-policy/04-theory.md`. This note owns no project files.

## 1. Main theorem: an exact universal absolute-integrability ceiling

Let remaining time be `r=T-t`. Use the **existing raw semilinear coding mechanism** for `f(u)=u-u^3`, and spatially constant terminal data `phi=1/2`. Let the code tables, terminal factors, and reciprocal-importance functional be unchanged. Allow code-, state-, time-, depth-, and history-dependent lifetime and tuple proposals, subject to:

1. The conditional lifetime density is strictly positive almost everywhere on each possible pre-horizon delay; the conditional survival probability through the remaining horizon is positive.
2. Every raw label with potentially nonzero contribution has positive conditional probability. Requiring every raw label positive is sufficient. Exact-zero pruning is permitted.
3. The weight uses the actual reciprocal conditional density, reciprocal conditional label probability, and reciprocal leaf-survival probability.
4. The resulting sampled tree is almost surely finite, and conditional draws are measurable and depend only on available information. Branching arity is bounded here. This nonexplosion assumption is automatic for the existing common exponential clock, but should be stated for arbitrary adaptive clocks.

Then, as an extended nonnegative expectation,

\[
\mathbb E|H_{\mathrm{Id}}(r)|=\frac12+s(r),
\quad s'=P(s),\quad s(0)=0,
\]

up to the maximal finite time, where

\[
P(s)=\frac38+\frac14s+\frac32s^2+s^3
=(s+\tfrac32)(s^2+\tfrac14).
\]

The sharp ceiling is

\[
\boxed{T_{L^1}=\frac{3\pi}{5}-\frac25\log3\approx1.445510676686.}
\]

The root has a finite absolute first moment **if and only if** `0<=r<T_L1`. At and beyond the endpoint its absolute first moment is infinite. Consequently every such raw importance estimator has infinite second moment there. This is independent of lambda and of all supported tuple changes; it strictly exceeds the scope of C8, which treated second moments for common exponential clocks and static policies.

This statement concerns the raw estimator, not the PDE. The flat Allen–Cahn solution remains bounded and global:

\[
u(r)=\frac1{\sqrt{1+3e^{-2r}}}.
\]

### 1.1 Why every proposal cancels at absolute-moment order one

First restrict to completed trees with generation depth at most `n`, killing the value if any nonzero continuation would branch beyond that depth. On a fixed completed labelled topology, the absolute weight is a product of absolute terminal factors times positive reciprocal proposal factors. Multiplying by its sampling density cancels each lifetime density, label probability, and leaf survival probability exactly. Motion remains unchanged; because terminal data are constant, its probability kernels integrate to one.

The same reasoning works for history-dependent conditional proposals: the joint density factors into its actual sequential conditional densities, and each factor cancels. It is not necessary to assume that the proposal itself is invariant under code-scalar normalization. After cancellation the base topology integrals have the normalization by absolute code multiplier.

Thus every finite-depth absolute expectation is independent of the admissible proposal. Couple all depths to the same unrestricted random tree. For a finite realized tree, the killed value is zero until the entire nonzero tree is included and is then the full value. Therefore its absolute values increase to `|H|`. Monotone convergence identifies the extended unrestricted moment with the common nonnegative topology sum. Early stopping of an exact-zero branch does not alter any of these integrals. This proves proposal invariance without first assuming integrability.

### 1.2 Derivative trees vanish exactly

Every descendant path of a `Dx(1)` root retains a `Dx(1)` child under the raw mechanism. Every derivative leaf has terminal value `phi'=0`. Nonexplosion therefore implies that its full functional is zero almost surely. Every second F-code label contains two such derivative children and contributes zero. For `F3`, both raw alternatives contain a structurally zero higher F derivative, so its branching contribution is zero as well.

Write the normalized absolute moments of `(F0,F1,F2,F3)` as `(A,B,C,E)`. The **absolute** initial factors are

\[
(A_0,B_0,C_0,E_0)=(3/8,1/4,3,6),
\]

because `f(1/2)=3/8`, `f'(1/2)=1/4`, `f''(1/2)=-3`, and `f'''=-6`. The signs of the last two factors must not be retained in the absolute system.

After proposal cancellation the minimal nonnegative Volterra equations are

\[
A=A_0+\int_0^r AB\,dv,\quad
B=B_0+\int_0^r AC\,dv,\quad
C=C_0+\int_0^r AE\,dv,\quad E=6,
\]

and

\[
I=\frac12+\int_0^r A(v)\,dv.
\]

The killed-depth iterations start at zero and successively apply this order-preserving Volterra operator. Their increasing limit is the minimal nonnegative extended solution. A locally finite solution is continuous and obeys the polynomial ODE; the polynomial vector field is locally Lipschitz, so it is unique until explosion.

### 1.3 Scalar reduction and reconstruction

Set `s(r)=integral_0^r A(v)dv`; then `s'=A>0`. Dividing by `s'` and integrating gives

\[
E=6,\quad C=3+6s,\quad B=\frac14+3s+3s^2,
\]

\[
A=\frac38+\frac14s+\frac32s^2+s^3=P(s),\quad I=\frac12+s.
\]

Conversely these expressions, with `s'=P(s)`, solve every ODE and initial condition, so uniqueness proves the correspondence while finite. The positive coefficients ensure that this finite solution dominates all killed-depth iterates. Conversely the iterates converge to that same solution by local uniqueness and continuation on each compact subinterval below its explosion time. This discharges the bridge from a positive ODE to the actual moments before the threshold.

### 1.4 Exact separation integral

For `s>=0`, define

\[
\Theta(s)=\frac25\log(s+\tfrac32)
-\frac15\log(s^2+\tfrac14)
+\frac65\arctan(2s)-\frac25\log3.
\]

Direct differentiation gives `Theta'(s)=1/P(s)>0` and `Theta(0)=0`. The separated equation is `Theta(s(r))=r`. At infinity the logarithmic terms cancel, while `arctan(2s)->pi/2`, so

\[
\lim_{s\to\infty}\Theta(s)=3\pi/5-(2/5)\log3=T_{L^1}.
\]

Hence `s(r)` increases to infinity as `r` approaches `T_L1` from below. In particular the **root** absolute moment `I=1/2+s` diverges; no inference from descendant divergence alone is being used.

For every completed flat topology, after proposal cancellation its absolute contribution is a nonnegative constant times `r^N`, where `N` is the number of branching events. This follows either by scaling the ordered event-time simplex, or directly by induction on the topology. Therefore the full nonnegative topology sum is nondecreasing in `r`. Its divergence as `r` increases to `T_L1` implies divergence at the boundary and at every later horizon. An equivalent argument uses monotonicity of all flat killed-depth Volterra iterates.

### 1.5 Signed mean and optional signed-parts corollary

For every strict subcritical horizon all reached absolute moments are finite and uniformly bounded on the time interval. Dominated convergence for the killed signed trees gives the cancelled signed mild system. Its locally bounded solution is unique and is the usual `(u,f(u),f'(u),f''(u),f'''(u))` solution, with derivative component zero. Thus `EH_Id=u(r)` for `r<T_L1`.

The main theorem needs only `E|H|=infinity` outside this interval, and that is sufficient to rule out an ordinary finite unbiased expectation. A stronger statement is available with an additional explicit topology observation: the sign of each completed flat topology is fixed by its terminal factors. Its contribution to either `EH^+` or `EH^-` is again a nonnegative constant times `r^N`. Both signed-part expectations are therefore nondecreasing in `r`. For `r<T_L1`,

\[
EH^+=(I+u)/2,\qquad EH^-=(I-u)/2.
\]

Since `I->infinity` while `1/2<=u<=1`, both tend to infinity. Monotonicity then yields `EH^+=EH^-=infinity` at and beyond the boundary. This is a separate, proved conventional corollary; omit it from the main headline if the project prefers the minimal obstruction claim.

## 2. Universal second-moment lower bound near the ceiling

For any proposal in the preceding class, Cauchy–Schwarz gives the extended inequality

\[
\boxed{M_2(r)=EH^2\ \ge\ (E|H|)^2=(1/2+s(r))^2.}
\]

This is stronger than the ordinary Jensen bound `M_2>=u^2`: it captures the cancellation cost in the raw representation independently of sampling design. If `M_2` is finite, its variance is at least `(1/2+s)^2-u^2`; if it is infinite the bound still holds in the extended sense.

There is a clean explicit lower bound sufficiently near the endpoint. If `s>=1/2`, then for every `v>=s`,

\[
P(v)=(v+1/2)^3+1/4-v/2\le(v+1/2)^3.
\]

Consequently, with `delta=T_L1-r`,

\[
\delta=\int_s^\infty\frac{dv}{P(v)}
\ge\frac1{2(s+1/2)^2},
\quad\boxed{M_2(r)\ge\frac1{2(T_{L^1}-r)}}.
\]

This bound applies whenever

\[
r\ge r_0:=\Theta(1/2)
=\frac35\log2+\frac{3\pi}{10}-\frac25\log3.
\]

In that regime `Var(H)>=1/[2(T_L1-r)]-1`. The exact asymptotic is `I(r)^2~1/[2(T_L1-r)]`, since `P(s)/s^3->1`. No claim is made that a practical clock attains this lower bound. An oracle complete-tree importance law proportional to absolute contribution would attain its second moment in a relaxed support class, but constructing or approximating that law is outside this run.

## 3. Bounded long-horizon alternative on genuinely nonconstant data

For bounded measurable terminal data `phi:R^d->[-1,1]`, use ternary branching Brownian motion at clock rate `lambda>0`, with the same diffusion convention as the project (`sigma^2/2` times the Laplacian). Every leaf returns `phi(X)` and a branching vertex returns

\[
\mathcal B_\lambda(a,b,c)
=\frac{\lambda+1}{3\lambda}(a+b+c)-\frac{abc}{\lambda}.
\]

There are no reciprocal-density tree weights. This is a change of representation, not a clock change inside the raw coding mechanism.

### 3.1 Diagonal identity and sharp boundedness condition

The exact diagonal identity is

\[
\lambda[\mathcal B_\lambda(u,u,u)-u]=u-u^3.
\]

The kernel is affine in each argument separately, so its extrema on `[-1,1]^3` occur at corners. Its values at all-positive/all-negative corners are `+1/-1`. At corners with two positive signs and one negative sign it equals `(lambda+4)/(3lambda)`, and the opposite corners give its negative. Therefore

\[
\boxed{\mathcal B_\lambda([-1,1]^3)\subseteq[-1,1]
\quad\Longleftrightarrow\quad\lambda\ge2.}
\]

At `lambda=2`, this is the soft-majority kernel `(a+b+c-abc)/2`. For `lambda>=2`, it is the convex combination `(2/lambda) B_2 +(1-2/lambda)(a+b+c)/3`.

The lower bound `lambda>=2` is not merely an artifact of symmetry or of ternary arity. Any bounded branch-output rule with diagonal mean `g(u)=u+(u-u^3)/lambda` must satisfy `g(u)<=1` for `u<=1`. As `g(1)=1`, this implies the left derivative `g'(1)>=0`. But `g'(1)=1-2/lambda`, so `lambda>=2`. Equivalently for `lambda<2`, `g(u)>1` for some `u<1` sufficiently close to one; even deterministic equal child values violate boundedness. This statement concerns a fixed event rate and the same instantaneous reaction identity; it does not rule out more general state-dependent rates or nonlocal changes of representation.

### 3.2 Unbiasedness, finite variance, and nonexplosion

Ternary BBM with finite rate is nonexplosive on every finite horizon. By induction up each realized finite tree, the returned value lies in `[-1,1]` whenever `lambda>=2`. Conditional on a shared branch position, the three descendant trees are independent and identically distributed; multilinearity therefore gives

\[
E\mathcal B_\lambda(H_1,H_2,H_3)
=\mathcal B_\lambda(m,m,m).
\]

First-event conditioning gives

\[
m(r)=e^{-\lambda r}P_r\phi
+\int_0^r\lambda e^{-\lambda s}P_s
[\mathcal B_\lambda(m(r-s),m(r-s),m(r-s))]ds.
\]

Thus `m_r=Lm+m-m^3`, with terminal/initial field `phi`. Uniqueness in the bounded mild class identifies the Allen–Cahn solution. The result holds for arbitrary nonconstant bounded terminal data and every finite horizon, not just the flat benchmark. It yields

\[
|H_\lambda|\le1,\qquad EH_\lambda=u,\qquad
\operatorname{Var}(H_\lambda)\le1-u^2\le1.
\]

The number of live particles has expectation `exp(2lambda*r)`, since each branch increases population by two. The expected count of all sampled vertices is

\[
\boxed{E N_{\rm nodes}=(3e^{2\lambda r}-1)/2.}
\]

Global moment control therefore comes with exponential expected work. Large-horizon finite variance is not a claim of uniformly efficient computation.

### 3.3 Conditional Rao–Blackwell interpretation

At `lambda=2`, give each leaf an independent sign with mean `phi(X)` and take majority signs at internal vertices. Conditional on the whole Brownian tree, integrating out the leaf votes gives exactly the soft kernel recursion. At `lambda>2`, define random sign output at each vertex so that its conditional mean, given the three child signs, equals `B_lambda` at that corner; all corner values lie in `[-1,1]`. Equivalently mix majority with selecting a uniformly random child, with mixing weight `2/lambda`. Integrating out all leaf and vertex votes, conditional on the Brownian tree, gives the deterministic soft recursion by independence and multilinearity. Hence the soft estimator is a Rao–Blackwellization and has second moment no larger than the binary-sign estimator's second moment, which is one.

## 4. Exact tunable-clock second-moment monotonicity for the soft family

This is a separate conventional analysis theorem for the bounded classical/mild solutions just described. It is not Lean-formalized in this audit.

Let `u=EH_lambda` (independent of lambda), `z=u^2`, and `v=EH_lambda^2`. Conditional iid children give, with `alpha=(lambda+1)/(3lambda)` and `beta=1/lambda`,

\[
Q_\lambda(z,v):=E[\mathcal B_\lambda(H_1,H_2,H_3)^2]
=\alpha^2(3v+6z)-6\alpha\beta vz+\beta^2v^3.
\]

Thus `v_r=L v+F_lambda(z,v)` and `v(0)=phi^2`, where

\[
F_\lambda(z,v)=\lambda(Q_\lambda(z,v)-v)
=-\frac{2\lambda}{3}(v-z)
+2[(v+2z)/3-vz]+\frac{D(z,v)}{\lambda},
\]

\[
D(z,v)=(v+2z)/3-2vz+v^3.
\]

Because the tree is bounded, Jensen yields `0<=z<=v<=1`. On this entire domain, `D>=0`:

* If `v<=1/3`, use `D=v/3+v^3+(2/3-2v)z>=0`.
* If `v>=1/3`, use `z<=v` and the nonpositive coefficient `2/3-2v` to obtain `D>=v(1-v)^2>=0`.

For `2<=lambda_1<=lambda_2`,

\[
F_{\lambda_2}(z,v)-F_{\lambda_1}(z,v)
=-\tfrac23(\lambda_2-\lambda_1)(v-z)
+(1/\lambda_2-1/\lambda_1)D(z,v)\le0.
\]

The old solution `v_lambda1` is therefore a supersolution to the `lambda_2` scalar moment equation. The reactions are locally Lipschitz on the common compact domain, so scalar parabolic comparison (or mild comparison after adding a sufficiently large linear shift) yields

\[
\boxed{EH_{\lambda_2}^2\le EH_{\lambda_1}^2,
\qquad\operatorname{Var}(H_{\lambda_2})\le\operatorname{Var}(H_{\lambda_1}).}
\]

This compares actual full-tree moments, not a frozen-child or envelope proxy. It includes every nonconstant bounded phi in the mild comparison class. Its utility is a rigorous variance/work tradeoff: increasing lambda decreases variance while increasing expected tree size. It does not prove that increasing lambda improves variance times cost, nor that lambda=2 is the cost-normalized optimum.

## 5. Formalization contract and scope risks

Useful small exact Lean targets, without claiming they formalize stochastic or analytic bridges:

1. `P(s)=(s+3/2)*(s^2+1/4)` and positivity on `s>=0`.
2. Polynomial reconstruction identities `C_s=6`, `B_s=C`, `A_s=B`, and `I_s=1` for the displayed scalar parametrization.
3. The derivative of the rational integral primitive (only if the toolchain makes the logarithm/arctangent derivative proof straightforward).
4. The finite near-barrier polynomial inequality `P(s)<=(s+1/2)^3` for `s>=1/2`.
5. The soft branch diagonal identity.
6. The convex-combination identity for `B_lambda` and its boundedness on `[-1,1]^3` for `lambda>=2`.
7. Necessity from the corner `(1,1,-1)` or the diagonal endpoint derivative; the corner proof is algebraically simpler.
8. The second-moment expansion, the two-case proof of `D>=0`, and the reaction-order inequality.

Remaining outside such lemmas: proposal cancellation over random trees, nonexplosion, monotone convergence identification, Volterra minimality, ODE separation and improper-integral limit unless actually formalized, PDE existence/uniqueness/comparison, conditional independence, and the exact expected node count.

Risks to avoid in the report:

* Do not present the raw L1 ceiling as a PDE blow-up time.
* Do not claim tuning lambda/q can remove the raw ceiling; changing to soft voting changes the functional itself.
* Do not describe soft voting as a new invention. The underlying representation is established literature.
* Do not extend the flat raw obstruction numerically to the wave without an additional comparison proof.
* Do not claim global feasibility from bounded variance without reporting exponential work.
* The raw arbitrary-proposal theorem needs actual likelihood cancellation and almost-sure finite trees; unsupported labels or silent depth/node cutoffs are outside it.

## 6. Primary literature checked for novelty boundaries

The global majority-vote Allen–Cahn representation is established by Alison Etheridge, Nic Freeman, and Sarah Penington, *Branching Brownian Motion, mean curvature flow and the motion of hybrid zones*, Electronic Journal of Probability 22 (2017), article 103, DOI 10.1214/17-EJP127. Primary preprint: <https://arxiv.org/abs/1607.07563>.

Broader probabilistic voting representations for polynomial semilinear reactions are developed by Jing An, Christopher Henderson, and Lenya Ryzhik, *Voting models and semilinear parabolic equations*, Nonlinearity 36 (2023), 6104–6123. Primary preprint: <https://arxiv.org/abs/2209.03435>; author manuscript: <https://par.nsf.gov/servlets/purl/10503704>.

The present audit's candidate project contribution is the exact raw-coded absolute-integrability ceiling, the explicit universal second-moment cost near it, and (subject to literature review) the tuned soft-family actual moment comparison. The bounded representation and importance-sampling cancellation principles are prior art. This bounded search does not establish publication priority for any remaining result.
