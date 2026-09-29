# T15 — noncompact quadratic moment audit and dimension threshold

Date: 28 September 2026. This is an independent conventional audit of
04e-noncompact-quadratic.md, extended at the parent's request to complete
the signed-PDE correspondence and examine dimensions at most four.
Only this review file was written. T13 remains frozen. No numerical
experiment, simulation, code modification, or Lean build was performed.
The research role follows the math-auto-research profile; serving-model
and effort telemetry were not independently available.

## Verdict

**The proposed Gaussian supersolution is valid.** For the original
derivative-coded expansion of $f(u)=-u^2$ on $\mathbb R^d$, with
$d\ge5$ and $v(x)=\varepsilon e^{-|x|^2}$,
$0<\varepsilon\le1/32$, every supported completing importance proposal
has finite first absolute Id moment at every finite horizon. The bound
in 04e is correct, and the ordinary signed expectation equals the global
absorption-PDE solution.

**The low-dimensional obstruction also closes, including $d=4$.**
For this Gaussian terminal family, every $\varepsilon>0$ gives infinite
first absolute Id moment at all points by a finite horizon when
$1\le d\le4$. Sections 5–7 give a proof directly for extended minimal
tree sums. In particular, they do not assume globally finite reaction
mass, differentiability of an infinite moment, or existence of a global
classical solution of the positive comparison system.

Thus, for every fixed $0<\varepsilon\le1/32$ in this Gaussian family,
all-horizon absolute integrability of this raw representation holds
**if and only if $d\ge5$**. This is a sharp dimension classification for
the specified estimator and data family, not a new general critical
exponent theorem for cooperative PDEs, nor a statement about all data or
large amplitudes in higher dimensions.

Required changes to 04e are to promote the upper bound after this audit,
include the signed-code uniqueness bridge in Section 4, replace the
tentative low-dimensional section by the completed proof below, and say
the displayed upper bound *tends to zero as $t\to\infty$* rather than
implying it decreases monotonically at every spatial point.

## 1. The actual raw code closure

Use $L=\Delta/2$ and the original tagged codes, retaining their mechanisms
even when two underlying functions are proportional. Since
$f'=-2u$, $f''=-2$, and $f^{(k)}=0$ for $k\ge3$, every completed tree
rooted at a higher reaction code has zero weight. After separating scalar
code multipliers by exact homogeneity, the normalized reachable closure
has $d+4$ codes: Id, $D_1,\ldots,D_d$, and $F_0,F_1,F_2$.

The nonnegative canonical fields satisfy

\[
\begin{aligned}
 (\partial_t-L)A&=AB+\sum_{i=1}^dD_i^2,
 &A(0)&=v^2,\\
 (\partial_t-L)B&=2A,
 &B(0)&=2v,\\
 (\partial_t-L)D_i&=BD_i,
 &D_i(0)&=|\partial_i v|,\\
 (\partial_t-L)W_I&=A,
 &W_I(0)&=v,
\end{aligned}
\tag{1}
\]

with $W_{F_2}=2$. These are abbreviations for nonnegative mild integral
identities and their minimal finite-tree/Picard construction.

The coefficient of $\sum_iD_i^2$ is exactly one: the gradient tuple has
absolute coefficient $1/2$, multiplied by $W_{F_2}=2$. There are no
cross-coordinate terms. The constant code $F_2$ need not be deterministically
evaluated by the raw sampler: its branching contributions vanish, while
its leaf contribution has canonical expectation two.

For this nonnegative datum there is also the useful exact identity

\[
 B=2W_I.
\tag{2}
\]

It follows directly from the mild equations and initial fields. This is
an identity of canonical expectations; replacing individual $F_1$ samples
by scaled Id samples would change their law and requires separate analysis.

The T13 likelihood contract applies on $\mathbb R^d$ as well: cancel the
full joint conditional sampling likelihood on every finite completed tree,
then sum nonnegative canonical masses by monotone convergence. Terminal
code magnitudes in this finite normalized closure are bounded, so every
bounded-depth integral is finite here. Consequently all valid supported
completing proposals have the same extended fields (1).

## 2. Every Gaussian-envelope constant checks

Put

\[
 G(t,x)=(1+t)^{-d/2}
          \exp\!\left(-\frac{|x|^2}{2(1+t)}\right),
 \qquad w(t)=(1+t)^{-d/2}.
\]

Direct differentiation gives $(\partial_t-L)G=0$; the factor $1/2$ in
the generator is essential. Since $0<G\le w$, one has $G^2\le wG$.
At time zero,

\[
 v\le\varepsilon G(0),\quad
 v^2\le\varepsilon^2G(0),\quad
 |\partial_i v|
  =2\varepsilon|x_i|e^{-|x|^2}
  \le2\varepsilon G(0).
\]

For the last inequality,
$|x_i|e^{-|x|^2/2}\le|x_i|e^{-x_i^2/2}\le1$.

For $d>4$ the two exact integrals are

\[
 I_0=\int_0^\infty w(s)\,ds=\frac2{d-2},\qquad
 I_1=\int_0^\infty s\,w(s)\,ds
     =\frac4{(d-2)(d-4)}.
\]

Define

\[
\begin{aligned}
 C&=2+16dI_0,\\
 b(t)&=2\varepsilon+2C\varepsilon^2t,\\
 J(t)&=\int_0^t b(s)w(s)\,ds,\qquad
 J_\infty=2\varepsilon I_0+2C\varepsilon^2I_1,\\
 \delta(t)&=2\varepsilon e^{J(t)},\\
 a(t)&=\varepsilon^2
       +C\varepsilon^2J(t)
       +4d\varepsilon^2e^{2J_\infty}\int_0^tw(s)\,ds .
\end{aligned}
\tag{3}
\]

For every integer $d\ge5$,
$I_0\le2/3$, $I_1\le4/3$, and $d/(d-2)\le5/3$. Therefore

\[
 0<C=2+\frac{32d}{d-2}\le\frac{166}{3},
\]

and, using $\varepsilon\le1/32$,

\[
 J_\infty\le
 2\frac1{32}\frac23+
 2\frac{166}{3}\frac1{32^2}\frac43
 =\frac1{24}+\frac{83}{576}
 =\frac{107}{576}<\frac14.
\tag{4}
\]

Since $e^{1/2}<2$,

\[
\begin{aligned}
 \frac{a(t)}{\varepsilon^2}
 &\le1+\frac C4+8dI_0\\
 &=\frac{3C}{4}<C.
\end{aligned}
\tag{5}
\]

The equality uses $C/2=1+8dI_0$. All quantities are nonnegative, and
$J(t)\le J_\infty$. Differentiating only these explicitly finite scalar
functions gives

\[
\begin{aligned}
 a'&=w\left(C\varepsilon^2b+
                   4d\varepsilon^2e^{2J_\infty}\right)
       \ge w(ab+d\delta^2),\\
 b'&=2C\varepsilon^2\ge2a,\\
 \delta'&=wb\delta .
\end{aligned}
\tag{6}
\]

No factor of $d$, two, or $\varepsilon$ is missing.

## 3. Supersolution to the full absolute tree system

Set

\[
 \overline A=aG,\qquad
 \overline B=bG,\qquad
 \overline D_i=\delta G,\qquad
 \overline W_I=(\varepsilon+C\varepsilon^2t)G
                    =\overline B/2 .
\tag{7}
\]

For example,

\[
 (\partial_t-L)\overline A=a'G
   \ge w(ab+d\delta^2)G
   \ge \overline A\overline B+
                    \sum_i\overline D_i^2 .
\]

The other components follow from (6); for Id the required inequality is
$C\varepsilon^2G\ge aG$. Their initial values dominate those in (1).
All envelope components and sources are bounded and smooth on every
finite time interval, so their differential inequalities give the
corresponding mild inequalities by the heat Duhamel formula.

The vector reaction map in (1) is coordinatewise increasing on the
nonnegative cone. Starting with the terminal heat contributions, its
positive Picard iterates are bounded componentwise by (7). These iterates
enumerate completed trees of increasing depth; their monotone limit is
the canonical absolute mass. Thus

\[
 \mathbb E_Q|H_I(t,x)|
 \le(\varepsilon+C\varepsilon^2t)
       (1+t)^{-d/2}e^{-|x|^2/[2(1+t)]}<\infty
\tag{8}
\]

for every finite $t,x$ and every proposal $Q$ in the specified contract.
No classical regularity of an unknown infinite moment was used.

The right side tends to zero uniformly in $x$ as $t\to\infty$ for these
dimensions. It is not necessarily monotone in $t$ at a fixed distant
point, because a heat profile can initially increase there.

The proposal class is nonempty: a fixed positive exponential rate and
positive probabilities for the finitely many raw tuple choices give
bounded offspring arity and almost-sure finite completion at every finite
horizon. This is independent of how large the random likelihood weights
can become.

## 4. The signed expectation does represent the absorption PDE

Let

\[
 U=\mathbb E H_I,\qquad S_k=\mathbb E H_{F_k},
 \qquad Q_i=\mathbb E H_{D_i}.
\]

The bounds above apply to every normalized code, uniformly in space on
each finite time interval. Hence all required signed finite-tree sums
and products are absolutely integrable. Fubini and cancellation therefore
give the finite signed mild system associated with

\[
\begin{aligned}
 (\partial_t-L)U&=S_0,\\
 (\partial_t-L)S_0&=S_0S_1+\sum_iQ_i^2,\\
 (\partial_t-L)S_1&=-2S_0,\\
 (\partial_t-L)Q_i&=S_1Q_i,\qquad S_2=-2,
\end{aligned}
\tag{9}
\]

with initial fields $v,-v^2,-2v,\partial_i v$.
In particular, the signed gradient contribution in the $S_0$ equation
is positive, since $-\frac12S_2=1$. The equation for $S_1$ has source
$-2S_0$, not $+2S_0$.

The scalar problem

\[
 u_t=Lu-u^2,\qquad u(0)=v
\]

has a unique global bounded nonnegative classical solution. Standard
local heat-equation fixed-point construction and comparison give
$0\le u\le P_tv\le\varepsilon$; this uniform bound prevents finite-time
breakdown. Smooth Gaussian initial data give the needed classical
derivatives. Each $q_i=\partial_i u$ solves
$q_{i,t}=Lq_i-2u q_i$ and has
$\|q_i(t)\|_\infty\le\|\partial_i v\|_\infty$ by the linear comparison
principle.

The physical family

\[
 (u,-u^2,-2u,\partial_1u,\ldots,\partial_du)
\]

therefore is bounded on every finite interval and satisfies (9).
For instance
$(\partial_t-L)(-u^2)=2u^3+|\nabla u|^2$ verifies its second equation.

The finite polynomial reaction map in (9) is locally Lipschitz on bounded
sets of the product sup-norm space. Two bounded mild solutions on
$[0,T]$ with the same initial fields satisfy

\[
 \|Y(t)-\widetilde Y(t)\|_\infty
 \le L_T\int_0^t
       \|Y(s)-\widetilde Y(s)\|_\infty\,ds .
\]

Gronwall gives uniqueness. One may work in bounded uniformly continuous
functions, or directly with bounded mild fields; Gaussian data and the
bounded mild nonlinearities have the needed continuity. Hence

\[
 \mathbb E_Q H_I(t,x)=u(t,x)
\]

for every finite horizon, point, and supported completing proposal when
$d\ge5$ and $0<\varepsilon\le1/32$.
This closes a finite-system correspondence argument. It does not invoke
uniqueness of an arbitrary infinite derivative hierarchy.

## 5. A rigorous radial heat-average obstruction

Discard the nonnegative $\sum_iD_i^2$ source and denote the minimal
reduced fields by $A_*,B_*$:

\[
 A_*=P_tA_0+\int_0^tP_{t-s}(A_*B_*)(s)\,ds,\qquad
 B_*=P_tB_0+2\int_0^tP_{t-s}A_*(s)\,ds,
\tag{10}
\]

where $A_0=\varepsilon^2e^{-2|x|^2}$ and
$B_0=2\varepsilon e^{-|x|^2}$. These extended fields exist as monotone
Picard/tree sums for all $t$. The full fields satisfy $A\ge A_*$,
$B\ge B_*$, with no finiteness hypothesis.

The initial fields are radial and radially nonincreasing. The heat
semigroup preserves that property, as do products and nonnegative sums.
Thus each Picard iterate, and its extended limit, is radial nonincreasing.
The heat-preservation fact can be proved by layer cake and convolution
of radial decreasing functions; it is not a claim about the anisotropic
individual fields $D_i$ in the full system.

For nonnegative radial nonincreasing $f,g$ and $\ell>0$, Chebyshev
correlation under the radius of a centered Gaussian gives

\[
 P_\ell(fg)(0)\ge P_\ell f(0)P_\ell g(0).
\tag{11}
\]

For bounded functions, twice the covariance is the expectation of
$(f(R)-f(R'))(g(R)-g(R'))\ge0$, with independent radii $R,R'$.
Truncation and monotone convergence give the extended version.

Fix a restart time $t_0\ge0$ and an additional horizon $T>0$. For
$0\le s<T$ define

\[
 a(s)=P_{T-s}A_*(t_0+s)(0),\qquad
 b(s)=P_{T-s}B_*(t_0+s)(0).
\]

Splitting the nonnegative Volterra integrals at $t_0$ and using Tonelli
and the heat semigroup gives

\[
\begin{aligned}
 a(s)&=a(0)+\int_0^s
          P_{T-r}(A_*B_*)(t_0+r)(0)\,dr
       \ge a(0)+\int_0^s a(r)b(r)\,dr,\\
 b(s)&=b(0)+2\int_0^sa(r)\,dr.
\end{aligned}
\tag{12}
\]

These are extended integral inequalities. If
$0<\alpha\le a(0)$, discard $b(0)\ge0$ and compare their finite positive
Picard iterates with

\[
 z'=\alpha+z^2,\qquad z(0)=0.
\]

Until $\theta=\pi/(2\sqrt{\alpha})$,
$a(s)\ge z'(s)$ and $b(s)\ge2z(s)$.
The comparison uses only the finite scalar solution. In particular, if

\[
 \frac{\pi}{2\sqrt{\alpha}}<T,
\tag{13}
\]

then the Id mild integral at total horizon $t_0+T$ is infinite at the
origin, because it dominates
$\int_0^s a(r)\,dr\ge z(s)\to\infty$ as $s\uparrow\theta$.

The divergence holds at **every** spatial point at that same horizon.
For any even nonnegative field $h$,

\[
 P_\ell h(x)\ge
 e^{-|x|^2/(2\ell)}P_\ell h(0).
\tag{14}
\]

To prove it, pair $y$ and $-y$ in the shifted Gaussian integral; the
remaining factor is $\cosh(x\cdot y/\ell)\ge1$. Truncation covers infinite
integrals. While $0\le r<\theta$, the remaining heat time
$T-r\ge T-\theta>0$, so the factor in (14) has a fixed positive lower
bound for each $x$. Integrating the radial reduced field therefore proves
$W_I(t_0+T,x)=\infty$ for all $x$. The nonnegative Id restart identity
then propagates this to every later horizon.

This proves the needed root statement, not merely divergence of a
descendant or of a spatial supremum.

## 6. Completion for dimensions one, two and three

Take $t_0=0$. The exact heat seed is

\[
 a(0)=P_TA_0(0)=
 \varepsilon^2(1+4T)^{-d/2}.
\]

Condition (13) holds whenever

\[
 T>\frac{\pi}{2\varepsilon}(1+4T)^{d/4}.
\tag{15}
\]

For $d<4$ a finite such $T$ exists. An explicit sufficient choice is

\[
 T_d=\max\left\{1,
       \left(\frac{\pi5^{d/4}}{\varepsilon}\right)^{4/(4-d)}
                  \right\}.
\tag{16}
\]

Indeed $1+4T_d\le5T_d$ and the Riccati lifetime is at most $T_d/2$.
Section 5 consequently proves

\[
 W_I(t,x)=\infty\qquad
 (t\ge T_d,\ x\in\mathbb R^d,\ d=1,2,3).
\]

This holds for every $\varepsilon>0$, not only the small amplitudes in
the higher-dimensional construction.

## 7. Completion of the critical dimension four

The following argument resolves the borderline without importing a
mixed-system theorem or assuming an unknown reaction moment is finite.

First, (10) implies the explicit lower bounds

\[
 A_*(t)\ge P_tA_0,\qquad
 B_*(t)\ge2tP_tA_0.
\]

Thus

\[
 A_*(t)\ge L_A(t):=
 P_tA_0+\int_0^tP_{t-s}
                 \left[2s(P_sA_0)^2\right]\,ds.
\tag{17}
\]

The lower field $L_A$ is a positive Gaussian mixture of finite total mass
at every finite time, independently of whether the actual fields are infinite.
In dimension four,

\[
 \|P_sA_0\|_2^2
   =\frac{\varepsilon^4\pi^2}{16(1+4s)^2}.
\]

Consequently its exact total mass is

\[
\begin{aligned}
 M_L(t):=\int_{\mathbb R^4}L_A(t,x)\,dx
 &=\frac{\varepsilon^2\pi^2}{4}\\
 &\quad+\frac{\varepsilon^4\pi^2}{128}
       \left[\log(1+4t)+\frac1{1+4t}-1\right].
\end{aligned}
\tag{18}
\]

The logarithm is the critical-dimensional growth missing from the
single initial heat-seed test.

For a conceptual necessary condition, all-horizon finite Id moments
would force
$T^2P_TA_*(t_0)(0)\le\pi^2/4$ for every $t_0,T$, by Section 5.
Since

\[
 T^2P_TA_*(t_0)(0)
 =\frac1{4\pi^2}\int_{\mathbb R^4}
        e^{-|x|^2/(2T)}A_*(t_0,x)\,dx,
\]

monotone convergence as $T\to\infty$ would imply the extended mass bound
$\int A_*(t_0)\le\pi^4$ at every restart time. Formula (18) violates
that bound for large $t_0$. This already gives a contradiction.

Here is a fully explicit finite-horizon version, avoiding even that
necessary-condition argument. Write

\[
 p_q(x)=(2\pi q)^{-2}e^{-|x|^2/(2q)}
\]

for the four-dimensional heat kernel. The first term of $L_A(t_0)$
has variance $t_0+1/4$. In a source term at time $s$,
$(P_sA_0)^2$ is proportional to $p_{s/2+1/8}$, so convolution to time
$t_0$ gives variance $t_0-s/2+1/8$. Every variance in the mixture is
therefore at most $t_0+1/4$.

Let

\[
 K=1+\frac{512\pi^2}{\varepsilon^4},\qquad
 t_0=\frac{e^K-1}{4},\qquad T=t_0+\frac14=\frac{e^K}{4}.
\tag{19}
\]

Equation (18) gives $M_L(t_0)>4\pi^4$. By the variance bound,

\[
\begin{aligned}
 P_TA_*(t_0)(0)
 &\ge P_TL_A(t_0)(0)\\
 &\ge\frac{M_L(t_0)}{16\pi^2T^2}
  >\frac{\pi^2}{4T^2}.
\end{aligned}
\tag{20}
\]

Choose the finite number
$\alpha=M_L(t_0)/(16\pi^2T^2)$ in Section 5.
Its Riccati lifetime is strictly smaller than $T$, so all-point Id
divergence occurs by the explicit total horizon

\[
 H_4=t_0+T
     =\frac{2\exp(1+512\pi^2/\varepsilon^4)-1}{4}.
\tag{21}
\]

Thus $W_I(t,x)=\infty$ for all $t\ge H_4$ and $x\in\mathbb R^4$.
This deliberately enormous bound is not a sharp critical time.
Every input to its lower construction is finite and explicit, and the
comparison remains valid if some actual moments diverge earlier.

## 8. Semantic counterexamples and limits of the conclusion

The upper and lower arguments concern the same tagged derivative-code
mechanism. They do not silently replace it by the usual polynomial
binary representation, combine signed branches, or use the signed PDE
solution as a terminal oracle.

The absorption PDE has a global bounded solution in every dimension for
this positive datum. Its continued existence therefore does not rescue
the raw moment in dimensions at most four. Conversely, the raw moment
can be finite at every horizon in dimensions at least five despite the
nonlinearity and nonconstant data. This is the requested obstruction to
a blanket extension of the compact-torus theorem to all of Euclidean
space.

The dimension threshold is sharp **within the specified small Gaussian
family**: for $0<\varepsilon\le1/32$ and integer $d\ge1$, all-horizon
absolute integrability holds exactly when $d\ge5$. The result does not
classify large amplitudes for $d\ge5$, arbitrary nonradial or sign-changing
profiles, or other reactions. The case $\varepsilon=0$ is the trivial
root exception; it must be excluded from low-dimensional divergence.

The bounds are for first absolute moments. They imply neither finite
variance nor a finite-variance central limit estimate. No bound on
sample count for a requested accuracy, total computational cost, or
floating-point error has been proved. A fixed-rate full tree can have
exponential expected work while its first absolute moment remains
finite. The conservative constants $1/32$, (16), and (21) have not been
optimized.

## 9. Literature audit and novelty boundary

Gaussian supersolutions, heat-average Riccati comparisons, and the
critical logarithmic-mass argument are established Fujita-type methods.
This review applies them to the canonical moment system of a specified
coding-tree estimator; it does not claim those methods or a general
cooperative-system critical dimension are new.

There is directly relevant older mixed-system literature. With
$u=B_*$ and $z=2A_*$, the reduced equations become

\[
 u_t=Lu+z,\qquad z_t=Lz+uz.
\]

Their exponent tuple is $(p_1,q_1,p_2,q_2)=(0,1,1,1)$, satisfying the
ordering $0<p_1+q_1\le p_2+q_2$ in the publisher's abstract of
[Escobedo–Levine (1995)](https://link.springer.com/article/10.1007/BF00375126).
The full article was not accessible in this bounded audit, so I have not
verified the exact theorem or borderline specialization from that paper.
The system match is verified; the precise literature implication remains
unverified. Sections 5–7 above are self-contained conventional proofs,
not an attribution of their exact statements to that abstract.

[López Mimbela–Wakolbinger](https://www.cimat.mx/BiblioAdmin/RTAdmin/reportes/enlinea/I-99-19.pdf)
treat $u_t=Au+uv$, $v_t=Bv+uv$ and establish global boundedness under
semigroup decay and small-data assumptions. Their second reaction is
bilinear rather than the linear reaction here, so their displayed theorem
is not a direct proof of the present threshold.

The parent also identified
[Snoussi–Tayachi (2002)](https://doi.org/10.1016/S0362-546X(00)00170-X)
and reported that its all-four-exponents-at-least-one hypotheses exclude
the linear second equation. Its full text was blocked by the publisher
in this audit, so that detailed hypothesis comparison was not independently
reverified here. No claim relies on it.

Publication priority of this particular coding-tree application, its
explicit constant, or the resulting data-family classification has not
been established.

## 10. Fixed finite formal target after this audit

The first useful Lean target is the coefficient part of the supersolution,
not a theorem pretending to formalize the entire branching construction.
For real $d\ge5$ and $0<\varepsilon\le1/32$, define

\[
 I_0=\frac2{d-2},\quad
 I_1=\frac4{(d-2)(d-4)},\quad
 C=2+16dI_0,\quad
 J_*=2\varepsilon I_0+2C\varepsilon^2I_1.
\]

Prove

\[
 0<C\le166/3,\qquad 0\le J_*\le107/576<1/4.
\]

Then, for nonnegative $j,h,E,b$ with
$j\le1/4$, $h\le I_0$, $E\le2$, put
$a=\varepsilon^2(1+Cj+4dEh)$ and assume
$\delta^2\le4\varepsilon^2E$. Prove

\[
\begin{aligned}
 a&\le3C\varepsilon^2/4\le C\varepsilon^2,\\
 C\varepsilon^2b+4d\varepsilon^2E
   &\ge ab+d\delta^2,\\
 2C\varepsilon^2&\ge2a.
\end{aligned}
\]

These inequalities match exactly the coefficient uses in (5)–(7).
The substitution $E=e^{2J_\infty}$ additionally needs
$e^{1/2}<2$ and monotonicity of the exponential. A later independent
target could verify the elementary integral

\[
 \int_0^t\frac{s}{(1+4s)^2}\,ds
  =\frac1{16}\left(\log(1+4t)+\frac1{1+4t}-1\right)
 \qquad(t\ge0).
\]

Heat-kernel calculus, supersolution domination of tree sums, covariance,
the extended restart, the Id divergence bridge, and signed PDE uniqueness
remain outside these finite statements. No new formal coverage is asserted
by this review.

## Input fingerprints

Audited 04e draft SHA-256:
7bb06fb77591d59b5ad487218e54d00694f30c33fce26a80eb2c857d04663d37.
Frozen T13 SHA-256:
04289e78366ea84568ceeb9c86af8986f295d9eda16d371a9eedd30f398206cb.
Parent integration may subsequently change 04e; this task did not edit it.
