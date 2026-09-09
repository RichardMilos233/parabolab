# Common notation and the exact coding-tree moment theorem

**Status:** proved theorem.

This note gives a self-contained model for a continuous-time coding tree and
identifies its absolute \(p\)-moment as the minimal nonnegative solution of an
exact multitype recursion. All identities take values in
\([0,\infty]\); no finite-moment assumption is made in deriving them. Fix
\(p>0\), a terminal horizon \(T<\infty\), and a starting triple
\((t,x,c)\) with \(0\leq t\leq T\).

## Model and hypotheses

Let \(E\) be a standard Borel state space. A Markov transition kernel
\(K_s(x,dy)\) has semigroup

\[
P_sh(x):=\int_E h(y)\,K_s(x,dy)
\]

for every nonnegative measurable \(h:E\to[0,\infty]\). The standard Borel
assumption supplies the regular conditional laws used below. The Markov path,
the lifetime clock, and the tuple draw are sampled independently until the
first branch event, subject to the shared-position and child-independence
requirements (H5)--(H6). All kernels, densities, terminal factors, and
code-indexed expressions below are assumed jointly measurable in their
displayed variables.

The code and mechanism assumptions are the following.

- **(H1)** \(\mathcal C\) is a countable code space.
- **(H2)** Every live mechanism table \(\mathcal M(c)\) is finite and
  nonempty, and every labelled live tuple contains at least one child.
- **(H3)** \(q_c(Z)>0\) for every live labelled tuple \(Z\) in
  \(\mathcal M(c)\).
- **(H4)** The lifetime density \(\rho_c\) is positive almost everywhere on
  every branch-time interval used.
- **(H5)** Children share the parent's Markov branch position.
- **(H6)** Conditional on that position and the first-event data, child
  subtrees are independent.
- **(H7)** The continuous-time tree is nonexplosive almost surely, meaning
  that only finitely many particles are born before the finite horizon.

The theorems below quantify over the live codes. An absorbing code whose
functional is identically zero may be adjoined by setting both its moment
and its operator component to zero; it needs no mechanism table and does not
alter any live-code argument.

Here a mechanism table is a labelled finite list, not a set. More precisely,
for each live \(c\) there is a finite label set
\(L_c=\{1,\ldots,m_c\}\), and label \(\ell\in L_c\) carries an ordered,
nonempty tuple

\[
Z_{c,\ell}=(z_{\ell,1},\ldots,z_{\ell,k_\ell}),
\qquad k_\ell\geq1.
\]

Two different labels may carry the same ordered tuple. They are still
different sampling alternatives, have separately specified probabilities,
and occur as separate summands. We write \(q_c(\ell)\), or
\(q_c(Z_{c,\ell})\) when displaying the tuple, with
\(\sum_{\ell\in L_c}q_c(\ell)=1\). Repeated child codes within one tuple also
retain their multiplicity.

The displayed recursion below uses the **coefficient-encoded convention**:
every deterministic mechanism coefficient is included in one of the child
codes, so the branch multiplier outside the child product is one. A
scalar-labelled child \((a,z)\), when present in the model's countable code
space, has evaluator \(H_{(a,z)}=aH_z\); that evaluator is part of the model
data rather than an appeal to any repository representation. If a
coefficient \(a_{c,\ell}\) is instead stored outside the children, the
corresponding moment summand below must be multiplied by
\(\lvert a_{c,\ell}\rvert^p\). Distinct labelled occurrences are never
merged, even when their child lists agree.

For code \(c\), let \(\rho_c(s)\,ds\) be its lifetime law and let

\[
\bar F_c(r):=\int_r^\infty \rho_c(s)\,ds.
\]

Thus \(\rho_c\geq0\) and \(\int_0^\infty\rho_c(s)\,ds=1\). Since an
integrable density is finite almost everywhere, (H4) implies
\(0<\rho_c(s)<\infty\) almost everywhere on each interval used. Every power
of \(\rho_c\) below is evaluated on this full-measure set; assigning zero to
the resulting time integrand on its null complement fixes a measurable
version without changing any integral.

In addition to (H1)--(H7), well-defined likelihood weights require
\(\bar F_c(r)>0\) for every remaining horizon \(r\) that is used. Terminal
factors \(g_c:E\to\mathbb R\) or \(\mathbb C\) are measurable and finite
almost surely under every terminal transition law encountered. These
conditions, (H3), and (H4) make every realized likelihood factor finite
almost surely, although its expectation may be infinite.

A particle born at \((r,y,c)\), with remaining horizon \(T-r\), draws a
lifetime \(\tau\).

1. If \(\tau\geq T-r\), it moves according to \(K_{T-r}(y,\cdot)\) and
   contributes
   \[
   \frac{g_c(X_{T-r})}{\bar F_c(T-r)}.
   \]
2. If \(0<\tau<T-r\), it moves to the single branch position \(X_\tau\),
   draws label \(\ell\) with probability \(q_c(\ell)\), and contributes
   \[
   \frac{1}{q_c(\ell)\rho_c(\tau)}
   \prod_{j=1}^{k_\ell}
   H_{r+\tau,X_\tau,z_{\ell,j}}.
   \]

All children in the second line are born at the same \(X_\tau\). Their
future paths, clocks, and tuple draws are independent conditional on
\((\tau,\ell,X_\tau)\), as required by (H5)--(H6). The full root functional
is denoted \(H_{t,x,c}\). Under (H2) and (H7), it is a finite product of
finite realized factors almost surely. Its value may be assigned arbitrarily
on the null event of explosion.

## Definition 2.1 (finite-depth killed coding tree)

Particles are indexed by finite words and the root has generation zero. For
\(n\in\mathbb N_0\), the killed functional \(H_{t,x,c}^{[n]}\) follows the
ordinary construction through generation \(n\), with one modification:
whenever a particle at generation \(n\) branches strictly before the
horizon, that particle returns zero and no descendants are evaluated. If
the same generation-\(n\) particle survives to the horizon, it contributes
its ordinary terminal factor.

For a nonexplosive realized tree \(\mathcal T\), define
\(\operatorname{depth}(\mathcal T)\) as the largest generation of any
particle born before the horizon. Thus a root that survives has depth zero,
whereas a root that branches and has only surviving children has depth one.
Then, pointwise on every nonexplosive realization,

\[
H_{t,x,c}^{[n]}
=
H_{t,x,c}\,
\mathbf 1_{\{\operatorname{depth}(\mathcal T)\leq n\}},
\]

and hence

\[
\boxed{
\left|H_{t,x,c}^{[n]}\right|^p
=
\left|H_{t,x,c}\right|^p
\mathbf 1_{\{\operatorname{depth}(\mathcal T)\leq n\}}.
}
\tag{2.1}
\]

**Proof.** If \(\operatorname{depth}(\mathcal T)\leq n\), no
generation-\(n\) particle branches. The killed evaluation therefore visits
the same particles and uses the same factors as the full evaluation.

If \(\operatorname{depth}(\mathcal T)>n\), some path reaches generation
\(n+1\). Its generation-\(n\) parent branched before the horizon, so the
killed value at that parent is zero. Every realized branch value is a
product of its child values. The zero therefore propagates along that path
to the root, and \(H_{t,x,c}^{[n]}=0\). These two cases prove (2.1).

By (H7), \(\operatorname{depth}(\mathcal T)<\infty\) almost surely.
Consequently the indicators in (2.1) increase pointwise to one on the
nonexplosion event, and

\[
\left|H_{t,x,c}^{[n]}\right|^p
\uparrow
\left|H_{t,x,c}\right|^p
\qquad\text{almost surely as }n\to\infty.
\tag{2.2}
\]

The increase in (2.2) is for the nonnegative absolute powers; signed or
complex killed functionals need not themselves be monotone. \(\square\)

## Theorem 2.2 (exact finite-depth \(p\)-moment recursion)

Use a zero-seeded index so that the nonlinear iteration begins at the zero
function:

\[
V_{c,0}^{(p)}(t,x):=0,\qquad
V_{c,n+1}^{(p)}(t,x)
:=
\mathbb E\!\left[
\left|H_{t,x,c}^{[n]}\right|^p
\right],
\quad n\geq0.
\tag{2.3}
\]

Let \(\Delta=T-t\). For every \(n\geq0\),

\[
\boxed{
\begin{aligned}
V_{c,n+1}^{(p)}(t,x)
={}&
\bar F_c(\Delta)^{1-p}
P_\Delta|g_c|^p(x)\\
&+
\sum_{\ell\in L_c}
q_c(Z_{c,\ell})^{1-p}
\int_0^\Delta
\rho_c(s)^{1-p}
P_s\!\left[
\prod_{z\in Z_{c,\ell}}
V_{z,n}^{(p)}(t+s,\cdot)
\right](x)\,ds .
\end{aligned}
}
\tag{2.4}
\]

The sum in (2.4) is a sum over labels \(\ell\), even when two labels carry
identical ordered tuples. In the abbreviated notation
\(\sum_{Z\in\mathcal M(c)}\), membership therefore means labelled
occurrence, not set membership.

**Proof.**

*Conditional product at the shared position.* This is the step at which both
(H5) and (H6) enter. Define a continuation random variable by

\[
R_{z,0}:=0,\qquad
R_{z,n}(r,y):=H_{r,y,z}^{[n-1]}\quad(n\geq1).
\]

By (2.3),
\(\mathbb E|R_{z,n}(r,y)|^p=V_{z,n}^{(p)}(r,y)\). Fix a branch time
\(s\), a label \(\ell\), and the one shared branch position \(y\). Put

\[
X_j:=|R_{z_{\ell,j},n}(t+s,y)|^p,\qquad
j=1,\ldots,k_\ell.
\]

For \(n\geq1\), (H6) says that the \(X_j\) are conditionally independent
given \((s,\ell,y)\); for \(n=0\), each \(X_j\) is zero. Under the conditional
product law, Tonelli's theorem applies to the named nonnegative integrand
\((r_1,\ldots,r_{k_\ell})\mapsto\prod_j r_j\). It gives, in the extended
nonnegative reals,

\[
\mathbb E\!\left[
\prod_{j=1}^{k_\ell}X_j
\;\middle|\;s,\ell,y
\right]
=
\prod_{j=1}^{k_\ell}
V_{z_{\ell,j},n}^{(p)}(t+s,y).
\tag{2.5}
\]

If one factor on the right is zero, it is interpreted as absorbing; its
underlying nonnegative random variable is zero almost surely. Thus (2.5)
also covers a zero factor next to an infinite moment without assigning an
ambiguous value to \(0\cdot\infty\). The common \(y\) in every factor is
essential: (2.5) first conditions on the one parent position and only then
multiplies the child moments.

*Branch event.* Conditional on
\((\tau,\ell,X_\tau)=(s,\ell,y)\), the absolute \(p\)-th power of the
branch likelihood factor is

\[
\bigl(q_c(\ell)\rho_c(s)\bigr)^{-p}
\prod_{j=1}^{k_\ell}X_j.
\]

The joint first-event sampling measure contributes separately:

\[
\underbrace{q_c(\ell)}_{\text{tuple label}}\,
\underbrace{\rho_c(s)\,ds}_{\text{lifetime}}\,
\underbrace{K_s(x,dy)}_{\text{shared position}}.
\]

Tonelli's theorem applies to the nonnegative branch integrand

\[
(\ell,s,y)\longmapsto
q_c(\ell)\rho_c(s)
\bigl(q_c(\ell)\rho_c(s)\bigr)^{-p}
\prod_{j=1}^{k_\ell}
V_{z_{\ell,j},n}^{(p)}(t+s,y)
\]

with respect to labelled counting measure, \(ds\), and \(K_s(x,dy)\).
It permits the finite sum and the two integrals to be evaluated in either
order even when the result is infinite. The tuple probability times its
likelihood power gives \(q_c(\ell)^{1-p}\); the lifetime density times its
likelihood power gives \(\rho_c(s)^{1-p}ds\); and integration over \(y\)
gives

\[
P_s\!\left[
\prod_{z\in Z_{c,\ell}}
V_{z,n}^{(p)}(t+s,\cdot)
\right](x).
\]

Summing labels and integrating \(0<s<\Delta\) yields the second line of
(2.4). When \(n=0\), every tuple has at least one child by (H2), so its
product contains \(V_{\cdot,0}^{(p)}=0\); this matches the rule that a root
branch is killed at depth zero.

*Leaf event.* The survival event has probability \(\bar F_c(\Delta)\).
On that event the absolute likelihood power is
\(\bar F_c(\Delta)^{-p}|g_c(X_\Delta)|^p\). Independence of the clock and
the Markov move therefore gives

\[
\bar F_c(\Delta)\bar F_c(\Delta)^{-p}
\int_E |g_c(y)|^pK_\Delta(x,dy)
=
\bar F_c(\Delta)^{1-p}P_\Delta|g_c|^p(x).
\]

The leaf and branch events partition the first-event space up to the
zero-probability equality \(\tau=\Delta\). Adding their nonnegative
contributions proves (2.4) in \([0,\infty]\). \(\square\)

## Theorem 2.3 (minimal fixed point and exact \(L^p\) criterion)

Let \(\mathscr V\) be the measurable functions

\[
v=(v_c)_{c\in\mathcal C},
\qquad
v_c:[0,T]\times E\to[0,\infty],
\]

ordered pointwise. Define \(\Phi_p:\mathscr V\to\mathscr V\) by the
right-hand side of (2.4):

\[
\begin{aligned}
(\Phi_pv)_c(t,x)
:={}&
\bar F_c(T-t)^{1-p}P_{T-t}|g_c|^p(x)\\
&+
\sum_{\ell\in L_c}q_c(\ell)^{1-p}
\int_0^{T-t}\rho_c(s)^{1-p}
P_s\!\left[
\prod_{z\in Z_{c,\ell}}v_z(t+s,\cdot)
\right](x)\,ds .
\end{aligned}
\tag{2.6}
\]

With \(V_0:=0\) and the shifted finite-depth moments from (2.3),

\[
V_1=\Phi_p(0),\qquad
V_{n+1}=\Phi_p(V_n)\quad(n\geq0),\qquad
V_n\uparrow V.
\tag{2.7}
\]

The limit is

\[
V_c(t,x)
=
\mathbb E|H_{t,x,c}|^p
\in[0,\infty],
\tag{2.8}
\]

it satisfies \(V=\Phi_p(V)\), and it is the minimal nonnegative fixed point:
if \(W=\Phi_p(W)\) with \(W\geq0\), then \(V\leq W\) pointwise.
Consequently,

\[
\boxed{
H_{t,x,c}\in L^p
\quad\Longleftrightarrow\quad
V_c(t,x)<\infty.
}
\tag{2.9}
\]

For \(0<p<1\), \(L^p\) in (2.9) denotes the class of random variables with
finite absolute \(p\)-moment; no norm property is asserted.

**Indexing audit.** Because a generation-zero particle that survives still
contributes its ordinary terminal factor, (2.6) gives

\[
\Phi_p(0)_c(t,x)
=
\bar F_c(T-t)^{1-p}P_{T-t}|g_c|^p(x),
\tag{2.10}
\]

which is generally nonzero. Thus the consistent zero-seeded statement is
\(V_0=0\) and \(V_1=\Phi_p(0)\), not
\(V_0=\Phi_p(0)=0\). The latter equality holds only at components whose leaf
\(p\)-moment vanishes. Equations (2.3) and (2.7) use the one-step shift
compatible with Definition 2.1 and the recursion (2.4).

**Proof.**

*Monotonicity of the operator.* Suppose \(0\leq v\leq w\) pointwise. For
each finite tuple, multiplication of nonnegative factors is monotone in
every coordinate, with zero treated as absorbing. Hence

\[
\prod_{z\in Z_{c,\ell}}v_z(t+s,y)
\leq
\prod_{z\in Z_{c,\ell}}w_z(t+s,y).
\]

The Markov kernel integral preserves this inequality because its integrands
are nonnegative. Multiplication by
\(q_c(\ell)^{1-p}\rho_c(s)^{1-p}\geq0\), integration in \(s\), and the
finite labelled sum also preserve it. The leaf term is the same for both
arguments, so \(\Phi_pv\leq\Phi_pw\).

Theorem 2.2 gives \(V_{n+1}=\Phi_p(V_n)\). Since \(V_0=0\) and
\(\Phi_p(0)\geq0\), \(V_0\leq V_1\). Operator monotonicity then gives
\(V_n\leq V_{n+1}\) by induction. This proves existence of the pointwise
limit \(V=\sup_nV_n\).

*Identification with the full-tree moment.* For \(n\geq0\), define the
nonnegative random variable

\[
Y_n:=
|H_{t,x,c}|^p
\mathbf 1_{\{\operatorname{depth}(\mathcal T)\leq n\}}.
\]

Definition 2.1 gives
\(V_{c,n+1}^{(p)}(t,x)=\mathbb EY_n\), and (H7) gives
\(Y_n\uparrow|H_{t,x,c}|^p\) almost surely. The monotone convergence theorem
applies to this named nonnegative sequence \(Y_n\); it requires no
integrable dominating random variable. Therefore

\[
\lim_{n\to\infty}V_{c,n+1}^{(p)}(t,x)
=
\mathbb E|H_{t,x,c}|^p,
\]

which proves (2.8).

*Continuity from below and the fixed-point identity.* Fix a labelled tuple
\(Z_{c,\ell}=(z_{\ell,1},\ldots,z_{\ell,k_\ell})\), a time \(s\), and a
state \(y\). The nonnegative functions

\[
G_{\ell,n}(s,y)
:=
\prod_{j=1}^{k_\ell}
V_{z_{\ell,j},n}^{(p)}(t+s,y)
\]

increase to

\[
G_\ell(s,y)
:=
\prod_{j=1}^{k_\ell}
V_{z_{\ell,j}}^{(p)}(t+s,y).
\]

To verify the synchronized product limit, first note that if one limiting
factor is zero, every term of that factor's increasing sequence is zero. If
all limiting factors are positive, any collection of strict finite lower
bounds for the factors is reached at one common index because the tuple is
finite; taking the supremum over those lower bounds gives the displayed
limit, including infinite limiting factors.

For fixed \(s\), the monotone convergence theorem applied to the nonnegative
integrands \(y\mapsto G_{\ell,n}(s,y)\) under
\(K_s(x,dy)\) gives

\[
P_s[G_{\ell,n}(s,\cdot)](x)
\uparrow
P_s[G_\ell(s,\cdot)](x).
\]

Next define the named nonnegative time integrands

\[
I_{\ell,n}(s)
:=
\rho_c(s)^{1-p}
P_s[G_{\ell,n}(s,\cdot)](x).
\]

They increase pointwise almost everywhere to
\(I_\ell(s):=\rho_c(s)^{1-p}P_s[G_\ell(s,\cdot)](x)\).
The monotone convergence theorem applied to \(I_{\ell,n}\) with respect to
Lebesgue measure on \((0,T-t)\) gives

\[
\int_0^{T-t}I_{\ell,n}(s)\,ds
\uparrow
\int_0^{T-t}I_\ell(s)\,ds.
\]

No domination assumption is needed in either application because every
integrand is nonnegative. Tonelli's theorem, applied to the nonnegative
joint integrand
\[
(s,y)\mapsto
\rho_c(s)^{1-p}G_{\ell,n}(s,y)
\]
under \(ds\,K_s(x,dy)\), ensures that these iterated branch integrals are
well defined even when they are infinite. Since \(L_c\) is finite, the
limit also passes through the labelled sum. The leaf term is independent of
\(n\). Hence

\[
\Phi_p(V)
=
\sup_n\Phi_p(V_n)
=
\sup_nV_{n+1}
=V.
\]

*Minimality.* Let \(W\geq0\) satisfy \(W=\Phi_p(W)\). The base inequality
\(V_0=0\leq W\) holds pointwise. If \(V_n\leq W\), operator monotonicity
gives

\[
V_{n+1}=\Phi_p(V_n)\leq\Phi_p(W)=W.
\]

Induction yields \(V_n\leq W\) for every \(n\), and taking the pointwise
supremum gives \(V\leq W\).

Finally, (2.8) identifies \(V_c(t,x)\) with the exact absolute
\(p\)-moment. By the definition of \(L^p\), that moment is finite exactly
when \(H_{t,x,c}\in L^p\), proving (2.9). \(\square\)

## Scope and assumption audit

1. The recursion and all limiting statements are equalities in
   \([0,\infty]\). Tonelli's theorem is used only for explicitly named
   nonnegative branch or child-product integrands.
2. Conditional child independence is invoked only after conditioning on the
   one shared parent branch position. It is not an assertion that children
   start from independently sampled positions.
3. Every monotone-convergence step identifies its nonnegative increasing
   integrand. No integrable domination is assumed.
4. Full tuple support and positive lifetime density are needed for the exact
   likelihood factors. Positive survival probability is separately required
   for the leaf likelihood.
5. Nonexplosion is used to turn the killed-depth indicators into an
   almost-sure exhaustion of the full tree. It is not used to infer any
   finite moment.
6. The equivalence (2.9) is pointwise in \((t,x,c)\). It does not assert
   uniform boundedness over states, codes, starting times, or terminal
   horizons.
7. If deterministic tuple coefficients are not encoded in child codes,
   their absolute \(p\)-th powers must be restored in (2.4) and (2.6).
