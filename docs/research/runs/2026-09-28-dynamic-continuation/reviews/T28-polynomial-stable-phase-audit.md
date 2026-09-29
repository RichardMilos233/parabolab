# T28 — independent audit of the polynomial stable-phase construction

**Verdict: conventional mathematical pass, with the explicit contracts below.**
I found no counterexample within the stated hypotheses and no error in the
transformation, Bernstein coefficient bound, clock rate, node bound, or
relative-defect estimate. The proof is complete once the bounded multiaffine
vote and the finite-generation completion argument are supplied explicitly.
The result concerns a changed scalar branching representation and ideal node
work. It is neither a likelihood change of the original derivative-coded tree
measure nor a finite-bit complexity theorem.

Audited source: [04k-polynomial-stable-phase.md](../04k-polynomial-stable-phase.md),
128 lines, SHA-256
58604b12796ffbf7adbd46c7495fd076ae84738d51dfb316d9560c89dc893e23.
This audit changes no source file and contains no numerical or Lean experiment.
The two-barrier draft 04l is outside this review. No originality finding is
made here; T27 separately handles the primary-literature comparison for the
voting ingredient.

## 1. Precise statement that passes

Fix a real polynomial $f$ of degree at most an integer $n\geq2$, real numbers
$m<M<b$, and assume

$$
f(b)=0,\qquad f(y)>0\quad(m\leq y<b),\qquad f'(b)<0.
$$

Let $P_t$ be the heat semigroup with generator $L=\Delta/2$ on
$\mathbb R^d$ or a flat torus. For bounded measurable initial data
$m\leq v\leq M$, interpret the PDE as its bounded mild solution, with the
initial datum understood pointwise through a chosen measurable representative
or almost everywhere as appropriate. On each finite horizon, standard
semilinear comparison and local Lipschitz uniqueness give a unique solution
with

$$
\ell_m(t)\leq u(t,x)\leq\ell_M(t)<b.
$$

There is a recursive estimator, defined below, satisfying

$$
0\leq H_{\rm def}(T,x)\leq r_m(T),\qquad
\mathbb E H_{\rm def}(T,x)=b-u(T,x),
$$

which completes almost surely for every finite $T$ and whose expected number
of generated nodes is at most

$$
K_{\rm work}
=\frac{n\exp((n-1)CI)-1}{n-1}.
$$

Here $C,I$ are exactly the source quantities. With
$\Delta=\int_m^M f(y)^{-1}\,dy$, $G=\max_{[m,b]}g$, and
$K_{\rm range}=e^{G\Delta}$, its relative variance is at most
$K_{\rm range}-1$, uniformly in finite $T$, $x$, and $d$.
The constants hold with $f,m,M,n$ fixed. They are not uniform as these phase
parameters approach their excluded boundaries.

These are statements about the mathematical random experiment with exact
scalar barriers, inverse clocks, Brownian draws, polynomial coefficients, and
initial-profile queries. Bounded measurable $v$ need not have an effective
evaluation procedure. The result does not itself supply one.

## 2. Scalar barrier and transformed reaction

Polynomial division gives $f(y)=(b-y)g(y)$ with
$\deg g\leq n-1$ and $g(b)=-f'(b)>0$. The sign hypothesis makes $g$ strictly
positive on the entire compact interval $[m,b]$. Thus

$$
0<c=\min_{[m,b]}g\leq g\leq G=\max_{[m,b]}g<\infty.
$$

The scalar trajectories increase toward $b$. For $r=b-\ell_m$ and
$R=b-m>0$,

$$
r'=-g(\ell_m)r,\qquad
Re^{-Gt}\leq r(t)\leq Re^{-ct}.
$$

In particular division by $r(t)$ is legitimate at every finite time.
Changing variables $y=\ell_m(t)$ gives, as an improper positive integral,

$$
I=\int_0^\infty r(t)\,dt
 =\int_m^b\frac{b-y}{f(y)}\,dy
 =\int_m^b\frac{dy}{g(y)}
 \leq\frac{R}{c}.
$$

For $u=\ell_m+rw$, use $\ell_m'=f(\ell_m)$ and $r'=-f(\ell_m)$:

$$
r(w_t-Lw)=f(\ell_m+rw)-(1-w)f(\ell_m).
$$

Since $b-(\ell_m+rw)=r(1-w)$, this is exactly

$$
F_t(w)=(1-w)\{g(\ell_m+rw)-g(\ell_m)\}.
$$

There is no omitted linear term or factor of $r$. Polynomial Taylor expansion
therefore yields the source formula

$$
F_t(w)=\sum_{j=1}^{n-1}
  \frac{g^{(j)}(\ell_m)}{j!}r^j w^j(1-w).
$$

The calculation applies to the positive-time classical version of a mild
solution, or directly by variation of constants. For merely measurable $v$,
one should not add a claim of pointwise initial convergence everywhere or
continuity at time zero in the uniform norm. Neither is used below.

## 3. Bernstein coefficient calculation and admissibility

Write $B_{n,k}(w)=\binom nk w^k(1-w)^{n-k}$. Degree elevation gives, for
$1\leq j\leq n-1$,

$$
w^j(1-w)=\sum_{k=j}^{n-1}c_{j,k}B_{n,k}(w),\qquad
c_{j,k}
=\frac{\binom{n-j-1}{k-j}}{\binom nk}
=\frac{\binom kj(n-k)}{n\binom{n-1}j}.
$$

This agrees with both coefficient expressions in the source. For
$j\leq k\leq n-1$,

$$
\frac{\binom kj}{\binom{n-1}j}
=\prod_{i=0}^{j-1}\frac{k-i}{n-1-i}
\leq\frac{k}{n-1}.
$$

Every factor after the first lies in $[0,1]$, so

$$
0\leq c_{j,k}\leq\frac{k(n-k)}{n(n-1)}.
$$

Using $0<r(t)\leq R$ in the Taylor expansion proves, with exactly the
source budget

$$
C=\sum_{j=1}^{n-1}
 \frac{\sup_{[m,b]}|g^{(j)}|}{j!}R^{j-1},
\qquad
|d_k(t)|\leq Cr(t)\frac{k(n-k)}{n(n-1)}.
$$

The endpoint coefficients satisfy $d_0=d_n=0$. For $1\leq k\leq n-1$,

$$
\frac{k(n-k)}{n(n-1)}
\leq \min\left(\frac{k}{n},\frac{n-k}{n}\right).
$$

If $C>0$, set $\lambda=Cr$ and $b_k=k/n+d_k/\lambda$. Then
$0\leq b_k\leq1$, including $b_0=0,b_n=1$. Finally
$w=\sum_k(k/n)B_{n,k}(w)$ proves

$$
F_t(w)=\lambda(t)\{B_t(w)-w\},
\qquad
B_t(w)=\sum_{k=0}^n b_k(t)B_{n,k}(w).
$$

If $C=0$, the $j=1$ term forces $g'=0$ on $[m,b]$, hence $g$ is a
constant polynomial and $F=0$. The separate heat-only construction is
necessary to avoid $d_k/\lambda=0/0$. It has one node and is consistent with
$K_{\rm work}=1$. The assumption $n\geq2$ already includes affine reactions
by taking a nonminimal degree bound.

## 4. The branch rule and its conditional expectation

The phrase “bounded multiaffine extension” should be replaced or accompanied
by the following formula. Given independent child returns
$z_1,\ldots,z_n\in[0,1]$ at a branch with remaining time $s$, return

$$
V_s(z_1,\ldots,z_n)=
\sum_{A\subseteq\{1,\ldots,n\}}b_{|A|}(s)
 \prod_{i\in A}z_i\prod_{i\notin A}(1-z_i).
$$

The displayed product weights are nonnegative and sum to one, so
$V_s\in[0,1]$. Its diagonal is $V_s(w,\ldots,w)=B_s(w)$.
More importantly, if the child returns are conditionally independent with
the same conditional mean $q(s,y)$, factorization of each product gives

$$
\mathbb E[V_s(Z_1,\ldots,Z_n)\mid s,y]=B_s(q(s,y)).
$$

Applying $B_s$ to an average of child returns is generally not an equivalent
rule. The explicit extension removes that implementation ambiguity.
Evaluating this finite polynomial has an arity-dependent arithmetic cost;
the node result keeps $n$ fixed and makes no arity-independent cost claim.

Let $\Lambda(t)=\int_0^t\lambda(s)\,ds$. At a node with remaining time $T$,
the first branch occurs with remaining time in $ds$ with density

$$
\lambda(s)e^{-(\Lambda(T)-\Lambda(s))}\,ds,\quad 0<s<T,
$$

and no branch occurs with probability $e^{-\Lambda(T)}$. A concrete ideal
clock uses $E\sim{\rm Exp}(1)$: if $E\geq\Lambda(T)$, create a leaf;
otherwise solve $\Lambda(s)=\Lambda(T)-E$. For $C>0$ the inverse is
unique on every finite interval because $\lambda>0$ there. Brownian motion
over the elapsed time $T-s$ produces the branch location, and the $n$
offspring continue independently from that same location and remaining time.
At a leaf after running the residual Brownian edge, return
$(v(Y)-m)/R$.

## 5. Completion proved before using the completed return

There is a direct finite-generation proof, so no appeal to an already
completed tree or to an unknown PDE solution is needed.
Use operational horizon $a=\Lambda(T)$. Let $N_h$ count generated nodes
through generation $h$, with nodes at depth $h$ counted even if their
descendants are omitted. It is bounded by $1+n+\cdots+n^h$.
Writing $K_h(a)=\mathbb E N_h(a)$ gives

$$
K_0(a)=1,\qquad
K_{h+1}(a)=1+n\int_0^a e^{-(a-s)}K_h(s)\,ds.
$$

The function

$$
K(a)=\frac{n e^{(n-1)a}-1}{n-1}
$$

satisfies this integral equation with $K$ in place of both $K_h$ and
$K_{h+1}$, and $K\geq1$. Positivity of the integral proves inductively
$K_h\leq K$. The variables $N_h$ increase to the number $N$ of all generated
nodes, possibly infinity. Monotone convergence gives

$$
\mathbb E N\leq K(a)<\infty,
$$

so $N<\infty$ almost surely. This proves termination noncircularly.
Only then evaluate the recursive bounded returns on the completed tree.

The exact expected count is also available. A possible node at depth $k$
is born by operational time $a$ when a sum of $k$ independent unit-rate
exponentials is at most $a$. There are $n^k$ possible nodes at that depth.
Tonelli and the gamma densities yield

$$
\begin{aligned}
\mathbb E N(a)
&=1+\sum_{k\geq1}n^k
       \int_0^a e^{-s}\frac{s^{k-1}}{(k-1)!}\,ds\\
&=1+n\int_0^a e^{(n-1)s}\,ds
 =K(a).
\end{aligned}
$$

Every completed full $n$-ary tree has
$L=1+(n-1)I_{\rm int}$ leaves and $N=1+nI_{\rm int}$ total nodes.
Thus $N=(nL-1)/(n-1)$ and $\mathbb E L=e^{(n-1)a}$, confirming both
source constants. Since $a\leq CI$, the claimed uniform bound follows.

The safe wording is “almost-sure completion for each finite $T$, and a
uniform bound on expected node count over all finite $T$.” If desired, one
can couple the operational trees inside a single Yule tree run to $CI$.
There is no need to define a Brownian query at physical time $T=\infty$.

## 6. Bounded expectation and PDE correspondence

For an independent exhaustion argument, truncate the tree at depth $h$ and
assign any fixed value in $[0,1]$, for example zero, to the cuts. The resulting
root returns stay in $[0,1]$ and eventually equal the completed root return
on every finite full tree. Dominated convergence justifies their expected
limit.

Alternatively, after the completion proof, conditioning directly on the
first event and using the conditional product identity in section 4 gives,
with $q_0=(v-m)/R$ and $q(T,x)=\mathbb E Z(T,x)$,

$$
q(T)=e^{-\Lambda(T)}P_Tq_0+
\int_0^T e^{-(\Lambda(T)-\Lambda(s))}
 \lambda(s)P_{T-s}\!\left[B_s(q(s))\right]\,ds.
$$

This is the bounded mild equation for $q_t=Lq+F_t(q)$.
Uniqueness within $[0,1]$ is immediate from Gronwall. For example,

$$
B_t'(w)=n\sum_{k=0}^{n-1}
 (b_{k+1}(t)-b_k(t))B_{n-1,k}(w)
$$

gives $|B_t'|\leq n$ on $[0,1]$ and hence
$|F_t'|\leq(n+1)\lambda(t)$. The latter is integrable on every finite
interval, and even on $[0,\infty)$.
The transformed PDE solution $w=(u-\ell_m)/r$ lies in $[0,1]$ and satisfies
the same mild equation and initial heat term. Therefore $q=w$ and

$$
\mathbb E\{r(T)(1-Z(T,x))\}=b-u(T,x).
$$

The mean is established after completion and boundedness; neither is inferred
from the intended PDE answer. Conversely this bounded stochastic mild
solution can be transformed back to construct $u$. No evolving PDE value is
needed in the sampling rules.

## 7. Uniform relative defect bound and its deterministic baseline

The scalar travel time
$\Delta=\int_m^M 1/f(y)\,dy$ is finite because $M<b$ and $f>0$ on
$[m,M]$. The autonomous scalar flow gives
$\ell_M(t)=\ell_m(t+\Delta)$, so

$$
\frac{r_m(t)}{r_M(t)}
=\exp\left(\int_t^{t+\Delta}g(\ell_m(s))\,ds\right)
\leq e^{G\Delta}=K_{\rm range}.
$$

Set $D=b-u(T,x)$ and $H=H_{\rm def}(T,x)$. Comparison gives
$0<r_M(T)\leq D\leq r_m(T)$, while $0\leq H\leq r_m(T)$ and
$\mathbb EH=D$. Thus

$$
\mathbb EH^2\leq r_m(T)D,\qquad
\frac{{\rm Var}(H)}{D^2}
\leq\frac{r_m(T)}{D}-1
\leq K_{\rm range}-1.
$$

For $\rho>0$, averaging
$\max\{1,\lceil(K_{\rm range}-1)/\rho^2\rceil\}$ independent roots
therefore gives relative root-mean-square error at most $\rho$.
Linearity of expectation gives the stated total node bound. This is an RMS
statement, not an unqualified high-probability confidence bound.

The deterministic harmonic center is also correct. For an unknown
$D\in[a,R_*]$ with $0<a\leq R_*$, the value
$h_*=2aR_* /(a+R_*)$ equalizes the two endpoint relative errors, giving

$$
\sup_{D\in[a,R_*]}\frac{|h_*-D|}{D}
=\frac{R_*-a}{R_*+a}.
$$

Substitute $a=r_M(T)$ and $R_*=r_m(T)$ to obtain the claimed bound.
“Zero-query” here means zero initial-profile queries: the scalar barrier
values still have to be supplied by the stated oracles.

## 8. Adversarial boundary checks and necessary scope corrections

1. **This is a different representation.** The time-dependent affine
   normalization and bounded voting rule change the algebraic tree measure.
   They are not a supported Radon–Nikodym importance proposal for the original
   derivative coding. On a compact torus the earlier obstruction can therefore
   coexist with this bounded scalar estimator. Any identification of these two
   sampling classes would be incorrect.

2. **An upper gap from $b$ is essential to this uniform relative guarantee.**
   Even the affine reaction $f(y)=c(b-y)$ demonstrates the problem if $M=b$
   is admitted. On $\mathbb R^d$, take
   $v(y)=b-R\mathbf1_{\{|y|\leq1\}}$ and $m=b-R$. The heat-only estimator is
   $H=Re^{-cT}\mathbf1_{\{|x+B_T|\leq1\}}$. For fixed $T>0$, write
   $p_T(x)=\mathbb P(|x+B_T|\leq1)$. Its relative variance is
   $(1-p_T(x))/p_T(x)$, which diverges as $|x|\to\infty$.
   For $v\equiv b$, the defect itself is zero and relative error is undefined.
   Completion and bounded absolute output do not require a strict upper gap;
   the stated relative estimate does.

3. **The simple-root condition is essential to this one-barrier finite-rate
   certificate, not a general impossibility theorem.** For
   $f(y)=(b-y)^2$, $g(y)=b-y$, $n=2$, and $R=b-m$,
   $r(t)=R/(1+Rt)$, $C=1$, and
   $\Lambda(T)=\log(1+RT)$. The actual expected node count of this clock is
   $2e^{\Lambda(T)}-1=1+2RT$, so its uniform bound fails.
   More generally a polynomial root of multiplicity at least two makes
   $\int_m^b1/g=\infty$. This says nothing against using two moving barriers,
   changing the rate or representation, or solving a constant profile
   deterministically. The source phrase “essential here” should retain this
   specific scope.

4. **Intermediate equilibria break the flow argument.** For instance
   $f(y)=(b-y)(y-a)^2$ with $m<a<M<b$ traps $\ell_m$ below $a$ while
   $\ell_M$ approaches $b$. The flow travel time across $a$ is infinite.
   This violates the hypotheses and explains why the no-intermediate-root
   assumption is substantive.

5. **Oracle work and arithmetic work remain distinct.** The count includes
   all generated nodes, including all $n$ children at a branch. Each node still
   requires dimension-dependent Brownian sampling and arity-dependent
   arithmetic. Barrier evaluation, inverse-clock evaluation, initial-profile
   evaluation, and relative accuracy for an exponentially small physical
   defect require their own effective numerical contracts. None follows from
   the finite node expectation.

There is no additional sign restriction on $m,M,b$ themselves. There is no
failure at $C=0$ once it is treated separately, and no finite-time zero of
$r$ under the stated hypotheses.

## 9. Suggested finite formal targets and integration changes

The most useful first formal gate is the finite Bernstein admissibility
argument; its assumptions match exactly what drives the sampler.

- Prove the coefficient identity for $w^j(1-w)$ and the bound
  $c_{j,k}\leq k(n-k)/(n(n-1))$ for the stated natural-number indices.
- Prove that $\lambda>0$ and
  $|d_k|\leq\lambda k(n-k)/(n(n-1))$ imply
  $0\leq k/n+d_k/\lambda\leq1$, including separately specified endpoints.
- Prove the finite multiaffine vote lies in $[0,1]$ and has the Bernstein
  diagonal. Independence and expectations are additional probability
  hypotheses, not consequences of that algebraic lemma alone.
- Prove the affine transformation identity and the full finite $n$-ary tree
  count identity. The relative-variance and harmonic-center inequalities are
  further short algebraic targets once their moment and interval hypotheses
  are made explicit.

The scalar ODE comparison, heat mild-solution correspondence, continuous-time
tree law, monotone convergence, and exact-oracle sampling remain conventional
unless separately formalized. A coefficient theorem alone does not certify
those bridges.

For the root document, the necessary integrations are bounded: add the
explicit vote, insert the finite-generation completion proof before invoking
the mean, state the measurable-mild convention, say that the representation
changes, and replace any ambiguous “uniform a.s. completion” wording by the
precise finite-time/uniform-expectation statement. Clarify that $\rho>0$ and
that the deterministic baseline uses zero initial-profile queries.
No coefficient, clock-rate, work, or relative-variance constant needs changing.
