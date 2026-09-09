# Dym coding-tree non-integrability

**Mathematical status:** proved theorem.
**Priority status:** not established; the bounded literature audit in the
design specification did not locate this Dym-specific result.

This note proves that the coding-tree random variable used for the Dym
example is not integrable at any positive horizon. The obstruction already
occurs on one five-particle tree: two prescribed branches followed by three
terminal leaves. It is therefore not a large-depth or tree-explosion
phenomenon.

## Exact implementation instance

For \(T>0\) and \(\alpha\in\mathbb R\), `parabolab.library.dym_1d` constructs
the one-dimensional full-jet problem with \(n=3\),

\[
f(z_0,z_1,z_2,z_3)
=-\frac12z_2+z_0^3z_3,
\qquad
\phi_\alpha(x)
=\bigl((3\alpha x)^2\bigr)^{1/3}.
\tag{4.1}
\]

The real cube root in (4.1) is applied to a nonnegative square. Consequently

\[
\phi_\alpha(x)
=|3\alpha x|^{2/3}
=C_\alpha |x|^{2/3},
\qquad
C_\alpha:=|3\alpha|^{2/3}.
\tag{4.2}
\]

The implementation represents the relevant codes as follows:

\[
\begin{aligned}
\mathrm{Id}
&=\texttt{Id()},\\
f^*
&=\texttt{FNu(1.0, (0, 0, 0, 0))},\\
(f_{z_2})^*
&=\texttt{FNu(1.0, (0, 0, 1, 0))},\\
(f_{z_0})^*
&=\texttt{FNu(1.0, (1, 0, 0, 0))},\\
D^2
&=\texttt{Dx(2)}.
\end{aligned}
\tag{4.3}
\]

The identity table is the singleton

\[
\mathcal M(\mathrm{Id})=\{(f^*,)\}.
\tag{4.4}
\]

The live \(f^*\)-table contains

\[
\boxed{
Z_*=\bigl((f_{z_2})^*,(f_{z_0})^*,D^2\bigr).
}
\tag{4.5}
\]

Here is the repository-level derivation of (4.5). In
`FullyNonlinearMechanism1D._raw_tuples`, the \(k=2\) union prefixes a
Faà-di-Bruno tuple by
\(\texttt{FNu(1.0, (0, 0, 1, 0))}\). The order-two Faà-di-Bruno term with
one block \((l,q,\mathrm{mult})=(2,0,1)\) has coefficient one and derivative
multi-index \((1,0,0,0)\). `_fdb_tuple` therefore appends
\(\texttt{FNu(1.0, (1, 0, 0, 0))}\) and
\(\texttt{Dx(0 + 2)}\), in that order. None of the three codes is
identically zero for (4.1), so the exact zero-tuple reduction in
`FullyNonlinearMechanism1D.tuples` retains this tuple.

The sampler draws uniformly from the resulting reduced table. If

\[
m_*:=|\mathcal M(f^*)|,
\tag{4.6}
\]

then \(m_*<\infty\) and the proposal probability of (4.5) is
\(q_*=1/m_*>0\). Real mechanism coefficients are stored inside the
`FNu.a` field rather than in an external branch multiplier; every
coefficient in (4.5) equals one.

Finally, `parabolab.tree._tree` uses independent
\(\operatorname{Exp}(\lambda)\) clocks, one shared Brownian branch position
for all children of a particle, and independent recursive calls for the
children after that shared birth position. Its branch likelihood is
\(1/(q\rho(\tau))\), and a surviving leaf born with remaining time \(r\)
has likelihood \(1/\bar F(r)\), where

\[
\rho(s)=\lambda e^{-\lambda s},
\qquad
\bar F(s)=e^{-\lambda s},
\qquad \lambda>0.
\tag{4.7}
\]

## Terminal identities on both half-lines

Assume from now on that \(\alpha\ne0\), so \(C_\alpha>0\) and

\[
C_\alpha^3=|3\alpha|^2=9\alpha^2.
\tag{4.8}
\]

The derivatives of \(f\) needed by (4.5) are

\[
f_{z_2}=-\frac12,
\qquad
f_{z_0}=3z_0^2z_3.
\tag{4.9}
\]

At the terminal time, \(z_0=\phi_\alpha\) and
\(z_3=\phi_\alpha'''\). The signs introduced by the even extension in
(4.2) must be retained.

### The half-line \(x>0\)

For \(x>0\),

\[
\begin{aligned}
\phi_\alpha(x)&=C_\alpha x^{2/3},\\
\phi_\alpha'(x)&=\frac{2C_\alpha}{3}x^{-1/3},\\
\phi_\alpha''(x)&=-\frac{2C_\alpha}{9}x^{-4/3},\\
\phi_\alpha'''(x)&=\frac{8C_\alpha}{27}x^{-7/3}.
\end{aligned}
\tag{4.10}
\]

It follows from (4.8)--(4.10) that

\[
\begin{aligned}
f_{z_0}\bigl(\phi_\alpha(x),J\phi_\alpha(x)\bigr)
&=3\phi_\alpha(x)^2\phi_\alpha'''(x)\\
&=3\bigl(C_\alpha^2x^{4/3}\bigr)
  \left(\frac{8C_\alpha}{27}x^{-7/3}\right)\\
&=\frac{8C_\alpha^3}{9x}
=\frac{8\alpha^2}{x}>0.
\end{aligned}
\tag{4.11}
\]

### The half-line \(x<0\)

Write \(r=-x>0\). Since \(dr/dx=-1\),

\[
\begin{aligned}
\phi_\alpha(x)&=C_\alpha r^{2/3},\\
\phi_\alpha'(x)&=-\frac{2C_\alpha}{3}r^{-1/3},\\
\phi_\alpha''(x)&=-\frac{2C_\alpha}{9}r^{-4/3},\\
\phi_\alpha'''(x)&=-\frac{8C_\alpha}{27}r^{-7/3}.
\end{aligned}
\tag{4.12}
\]

Thus

\[
\begin{aligned}
f_{z_0}\bigl(\phi_\alpha(x),J\phi_\alpha(x)\bigr)
&=3\bigl(C_\alpha^2r^{4/3}\bigr)
  \left(-\frac{8C_\alpha}{27}r^{-7/3}\right)\\
&=-\frac{8C_\alpha^3}{9r}
=-\frac{8\alpha^2}{r}
=\frac{8\alpha^2}{x}<0.
\end{aligned}
\tag{4.13}
\]

Combining (4.10) and (4.12), for every \(x\ne0\),

\[
\boxed{
f_{z_2}=-\frac12,\qquad
f_{z_0}\bigl(\phi_\alpha(x),J\phi_\alpha(x)\bigr)
=\frac{8\alpha^2}{x},\qquad
\phi_\alpha''(x)
=-\frac{2|3\alpha|^{2/3}}9|x|^{-4/3}.
}
\tag{4.14}
\]

In particular, \(f_{z_0}(\phi_\alpha,J\phi_\alpha)\) is odd and changes
sign at zero, whereas \(\phi_\alpha''\) is even and strictly negative on
both punctured half-lines. At the repository default \(\alpha=2\), these
formulas specialize to
\(\phi_2(x)=|6x|^{2/3}\) and
\(f_{z_0}(\phi_2,J\phi_2)=32/x\).

## A positive-probability five-particle event

Fix a starting state \(x\in\mathbb R\), a starting time \(t<T\), and the
positive horizon

\[
h:=T-t>0.
\tag{4.15}
\]

Let

\[
I_h:=\left(\frac h8,\frac h4\right).
\tag{4.16}
\]

Define the following finite-depth event \(E_*\).

1. The root \(\mathrm{Id}\)-particle has lifetime
   \(\tau_1\in I_h\), hence branches before \(T\), and selects the singleton
   tuple \((f^*,)\).
2. The resulting \(f^*\)-particle has lifetime
   \(\tau_2\in I_h\), hence also branches before \(T\), and selects \(Z_*\).
3. Each of the three children in \(Z_*\) has a lifetime longer than its
   remaining horizon and therefore survives to \(T\) without branching.

For \((\tau_1,\tau_2)\in I_h^2\), put

\[
s:=\tau_1+\tau_2,
\qquad
\delta:=h-s.
\tag{4.17}
\]

The interval restrictions give

\[
\frac h4<s<\frac h2,
\qquad
\boxed{\frac h2<\delta<\frac{3h}4}.
\tag{4.18}
\]

In particular, both prescribed branches occur before the horizon. Conditional
on the two branch times, independence of the clocks gives

\[
\begin{aligned}
\mathbb P(E_*)
&=
q_*
\int_{I_h}\int_{I_h}
\rho(r_1)\rho(r_2)\bar F(h-r_1-r_2)^3
\,dr_2\,dr_1\\
&=
\frac1{m_*}
\int_{I_h}\int_{I_h}
\lambda^2e^{-\lambda(r_1+r_2)}
e^{-3\lambda(h-r_1-r_2)}
\,dr_2\,dr_1
>0.
\end{aligned}
\tag{4.19}
\]

Every integrand in (4.19) is finite and strictly positive on a rectangle of
positive Lebesgue measure. This proves the required positive probability
without imposing any condition on a Brownian endpoint.

## Conditioning at the shared second branch position

Let \(Y\) be the position at which the \(f^*\)-particle branches. Conditional
on \((\tau_1,\tau_2)=(r_1,r_2)\), the two Brownian displacements before the
second branch add, so

\[
Y\sim N(x,s),
\qquad s=r_1+r_2.
\tag{4.20}
\]

Now condition in the order

\[
(\tau_1,\tau_2)\quad\longrightarrow\quad Y=y
\quad\longrightarrow\quad\text{three child continuations}.
\tag{4.21}
\]

The children share the birth position \(y\). They do not share their
post-birth Brownian increments. Conditional on (4.21) and on their survival
clocks, write their endpoints as

\[
\begin{aligned}
X^{(2)}&=y+\sqrt{\delta}\,Z_2,\\
X^{(0)}&=y+\sqrt{\delta}\,Z_0,\\
X^{(D)}&=y+\sqrt{\delta}\,Z_D,
\end{aligned}
\qquad
Z_2,Z_0,Z_D\stackrel{\mathrm{iid}}{\sim}N(0,1).
\tag{4.22}
\]

The superscripts label the
\((f_{z_2})^*\), \((f_{z_0})^*\), and \(D^2\) children, respectively.
Equation (4.22) is conditional independence after conditioning on the one
shared birth position; it does not replace that birth position by three
independent branch positions.

For fixed \(y\) and \(\delta>0\), every endpoint in (4.22) has density

\[
g_{y,\delta}(r)
=\frac1{\sqrt{2\pi\delta}}
\exp\left(-\frac{(r-y)^2}{2\delta}\right),
\qquad r\in\mathbb R.
\tag{4.23}
\]

Choose the compact interval

\[
K:=[1,2].
\tag{4.24}
\]

It is bounded away from zero, and (4.14) gives, for \(r\in K\),

\[
0<
\frac{2C_\alpha}{9}\,2^{-4/3}
\leq |\phi_\alpha''(r)|
\leq\frac{2C_\alpha}{9}
<\infty,
\qquad
\phi_\alpha''(r)<0.
\tag{4.25}
\]

Moreover,

\[
\mathbb P\!\left(X^{(D)}\in K
\mid \tau_1,\tau_2,Y=y,E_*\right)
=\int_K g_{y,\delta}(r)\,dr>0
\tag{4.26}
\]

for every finite \(y\) and every \(\delta\) in (4.18). The future Brownian
increments are independent of the survival clocks, so conditioning on
\(E_*\) does not alter (4.22)--(4.23). Equations (4.19) and (4.26) show that
the event \(E_*\cap\{X^{(D)}\in K\}\) also has strictly positive
probability.

## Theorem 4.1 (infinite absolute first moment)

Let \(T>0\), \(\alpha\ne0\), \(\lambda>0\), \(0\leq t<T\), and
\(x\in\mathbb R\). Let \(H_{t,x,\mathrm{Id}}\) be the coding-tree
functional produced by the implementation instance (4.1), the standard
Brownian motion, the exponential clock (4.7), and the repository's uniform
full-support proposal on each reduced mechanism table. Then

\[
\boxed{
\mathbb E\!\left[|H_{t,x,\mathrm{Id}}|\right]=\infty.
}
\tag{4.27}
\]

Thus the root estimator is not in \(L^1\) for any starting state and any
positive horizon.

### Proof

On \(E_*\), the realized likelihood multiplier outside the three terminal
factors is

\[
\begin{aligned}
L(r_1,r_2)
&=
\frac1{\rho(r_1)}
\frac1{q_*\rho(r_2)}
\frac1{\bar F(\delta)^3}\\
&=
\frac{m_*}{\lambda^2}
\exp\!\left(\lambda(r_1+r_2+3\delta)\right)
\in(0,\infty).
\end{aligned}
\tag{4.28}
\]

The three terminal factors are given by (4.14). Outside null endpoint
events at zero,

\[
H_{t,x,\mathrm{Id}}
=L(r_1,r_2)
\left(-\frac12\right)
\left(\frac{8\alpha^2}{X^{(0)}}\right)
\phi_\alpha''(X^{(D)})
\qquad\text{on }E_*.
\tag{4.29}
\]

The endpoint \(X^{(2)}\) does not appear on the right because its
\((f_{z_2})^*\)-terminal factor is the constant \(-1/2\).

Fix \(r_1,r_2\in I_h\) and \(Y=y\). The singular endpoint density satisfies

\[
g_{y,\delta}(0)
=\frac1{\sqrt{2\pi\delta}}
\exp\left(-\frac{y^2}{2\delta}\right)>0.
\tag{4.30}
\]

By continuity at zero, for every fixed \(\varepsilon>0\) there are
\(\varepsilon_0\in(0,\varepsilon]\) and \(c_{y,\delta}>0\) such that
\(g_{y,\delta}(r)\geq c_{y,\delta}\) whenever
\(|r|\leq\varepsilon_0\). Therefore

\[
\begin{aligned}
\int_{-\varepsilon}^{\varepsilon}
\frac{8\alpha^2}{|r|}g_{y,\delta}(r)\,dr
&\geq
8\alpha^2c_{y,\delta}
\int_{-\varepsilon_0}^{\varepsilon_0}\frac{dr}{|r|}\\
&=\infty.
\end{aligned}
\tag{4.31}
\]

This is a conditional terminal singularity, not an asymptotic statement
about deep generations.

For completeness, the sampling densities and the likelihood factors can be
kept visible in one Tonelli calculation. Let \(p_s(x,y)\) denote the
\(N(x,s)\) density in (4.20), and restrict
\(0<|X^{(0)}|<\varepsilon\) and \(X^{(D)}\in K\). The factors
\(\rho(r_1)\), \(\rho(r_2)\), \(q_*\), and \(\bar F(\delta)^3\) from the
sampling law cancel their inverses in (4.28). Since every remaining
integrand is nonnegative, Tonelli's theorem gives

\[
\begin{aligned}
&\mathbb E\!\left[
|H_{t,x,\mathrm{Id}}|;
E_*,\ 0<|X^{(0)}|<\varepsilon,\ X^{(D)}\in K
\right]\\
&\quad=
\int_{I_h}\int_{I_h}\int_{\mathbb R}
p_s(x,y)
\left(\frac12\int_{\mathbb R}g_{y,\delta}(\xi_2)\,d\xi_2\right)\\
&\qquad\qquad\qquad\times
\left(
\int_{0<|r_0|<\varepsilon}
\frac{8\alpha^2}{|r_0|}
g_{y,\delta}(r_0)\,dr_0
\right)
\left(
\int_K|\phi_\alpha''(r_D)|
g_{y,\delta}(r_D)\,dr_D
\right)
\,dy\,dr_2\,dr_1.
\end{aligned}
\tag{4.32}
\]

The first bracket in (4.32) equals \(1/2\); the last bracket is finite and
strictly positive by (4.23)--(4.25); and the middle bracket is infinite by
(4.31). The outer density \(p_s(x,y)\) is positive for every \(y\), and
\(I_h^2\) has positive measure. Hence the right-hand side of (4.32) is
infinite. It is a lower bound for the full absolute first moment, proving
(4.27). \(\square\)

The proof only used a tree with the root, one \(f^*\)-particle, and three
terminal children. Any measurable version of the full functional that
agrees with the sampler on finite trees inherits the same lower bound;
behavior on deeper or exceptional trees cannot restore \(L^1\).

## Corollary 4.2 (both signed parts diverge)

Under the hypotheses of Theorem 4.1, define

\[
H^+:=\max(H_{t,x,\mathrm{Id}},0),
\qquad
H^-:=\max(-H_{t,x,\mathrm{Id}},0).
\tag{4.33}
\]

Then

\[
\boxed{
\mathbb E[H^+]=\infty,
\qquad
\mathbb E[H^-]=\infty.
}
\tag{4.34}
\]

Consequently \(H_{t,x,\mathrm{Id}}\) has no Lebesgue expectation, even as an
extended-real expectation.

### Proof

On the restriction \(X^{(D)}\in K\), every sign outside the
\((f_{z_0})^*\)-factor is fixed:

\[
L>0,\qquad
f_{z_2}=-\frac12<0,\qquad
\phi_\alpha''(X^{(D)})<0.
\tag{4.35}
\]

The product of these three factors is positive. It follows from (4.29) that

\[
\operatorname{sgn}(H_{t,x,\mathrm{Id}})
=\operatorname{sgn}(X^{(0)})
\quad\text{on }E_*\cap\{X^{(D)}\in K\},
\tag{4.36}
\]

apart from the null event \(X^{(0)}=0\).

For each conditioned \(y,\delta\), continuity and positivity of
\(g_{y,\delta}\) at zero give the two separate divergences

\[
\int_0^\varepsilon
\frac{8\alpha^2}{r}g_{y,\delta}(r)\,dr=\infty,
\qquad
\int_{-\varepsilon}^0
\frac{8\alpha^2}{|r|}g_{y,\delta}(r)\,dr=\infty.
\tag{4.37}
\]

Apply Tonelli's theorem first to \(H^+\) with
\(0<X^{(0)}<\varepsilon\), and then to \(H^-\) with
\(-\varepsilon<X^{(0)}<0\), while retaining
\(E_*\cap\{X^{(D)}\in K\}\). The same nonzero factors as in (4.32) remain,
and the relevant half of (4.37) is infinite in each calculation. This proves
(4.34). \(\square\)

Since both nonnegative signed parts have infinite expectation, the formal
difference

\[
\mathbb E[H^+]-\mathbb E[H^-]=\infty-\infty
\tag{4.38}
\]

is undefined. A symmetric Cauchy principal value may impose a cancellation
near \(X^{(0)}=0\), but such a limit is not the Lebesgue integral of the
random variable and does not define its probabilistic expectation.

## Exact scope and sharpness

The hypotheses \(h>0\), \(\alpha\ne0\), a clock able to branch before the
horizon, and positive proposal probability for the displayed topology are
essential to the statement proved above.

1. **Zero horizon.** If \(h=0\), the root is already at the terminal time and
   \[
   H_{T,x,\mathrm{Id}}=\phi_\alpha(x)
   \]
   deterministically. This is finite for every \(x\). There is no interval
   \(I_h\) and no branch event of the form used in the proof.

2. **Degenerate parameter.** If \(\alpha=0\), then
   \(\phi_0\equiv0\), all of its spatial derivatives vanish, and the
   singular coefficient \(8\alpha^2/x\) in (4.14) is zero. The zero function
   is the trivial terminal solution. On every finite tree rooted at
   \(\mathrm{Id}\), either the continuing \(f^*\)-line reaches a zero
   \(f(0)\) leaf or a spatial-derivative line reaches a zero derivative leaf,
   so the root product is zero. The conclusion (4.27) is therefore false in
   this case.

3. **A clock that cannot branch.** Suppose instead that the lifetime law is
   supported strictly after \(h\). The root cannot branch before \(T\), its
   survival probability is one, and
   \[
   H_{t,x,\mathrm{Id}}
   =\phi_\alpha(x+\sqrt h\,Z),
   \qquad Z\sim N(0,1).
   \]
   Since \(\phi_\alpha(r)=C_\alpha|r|^{2/3}\), this random variable has a
   finite absolute first moment. Thus (4.27) cannot be asserted for an
   arbitrary lifetime law merely because the Dym mechanism contains
   \(Z_*\).

4. **Loss of proposal support.** If a non-full-support rule assigns
   \(q(Z_*)=0\), then the event \(E_*\) has probability zero and this
   singular-event proof no longer applies. This alone does not prove that
   the altered random variable is integrable, because other live Dym tuples
   can contain terminal singularities. If every singular live tuple is
   deleted, the corresponding mechanism terms are omitted and the sampled
   recursion is no longer the original coding-tree representation.

   At the root the issue is even more rigid:
   \(\mathcal M(\mathrm{Id})=\{(f^*,)\}\). A normalized proposal on the
   original root table cannot assign probability zero to \(f^*\). A rule
   that does so either has no valid root draw or replaces a root branch by a
   cemetery value. Such a rule can produce an integrable random variable
   (for example, return zero on a root branch and retain the integrable root
   leaf), but it is a biased, different functional rather than an
   importance proposal for the Dym estimator.

The support qualification is therefore exact: Theorems 4.1 and 4.2 concern
the repository's uniform full-support mechanism, and more generally any
proposal that gives the two displayed live choices positive probability
with the corresponding exact likelihood ratios. They do not claim
integrability or non-integrability for a target-changing mechanism obtained
by deleting live alternatives.
