# Multifactor Merton theorem package

**Status:** conventional mathematical proofs recorded on 2026-09-09.

This note contains the mathematical core needed for a genuinely
multidimensional Merton coding-tree benchmark. It deliberately separates
algebraic PDE identities from stochastic-control verification and from the
integrability of a coding-tree estimator.

The results use the following status labels.

- **Proved algebraic theorem:** the conclusion follows from the displayed
  smoothness, sign, and matrix assumptions by the proof given here.
- **Conditional representation theorem:** the coding mechanism is proved
  algebraically, but equality with the unrestricted random-tree expectation
  additionally requires nonexplosion, integrability, a full-tree limit, and
  uniqueness.
- **Not proved here:** existence of the stochastic-control value function,
  admissibility of the feedback controls, global classical regularity,
  coding-tree moments, and literature priority.

## 1. Market model and notation

Let \(Y_s\in\mathbb R^m\) be an observable opportunity-factor process,

\[
dY_s=b(Y_s)\,ds+\beta\,dW_s^Y,
\qquad
A:=\beta\beta^\top\succeq0.
\tag{1.1}
\]

There are \(n\) risky assets. Their excess-return vector is
\(\lambda(y)\in\mathbb R^n\), and their instantaneous return covariance is
\(\Sigma\in\mathbb R^{n\times n}\), with \(\Sigma\succ0\). Let

\[
C\,ds
:=
d\left\langle
\text{risky-asset return shocks},Y
\right\rangle_s
\in\mathbb R^{n\times m}.
\tag{1.2}
\]

The joint covariance block

\[
\begin{pmatrix}
\Sigma&C\\
C^\top&A
\end{pmatrix}
\tag{1.3}
\]

is assumed positive semidefinite.

The investor chooses risky-asset wealth fractions
\(\pi_s\in\mathbb R^n\) and an absolute consumption rate \(c_s\geq0\).
Wealth follows

\[
dX_s=
\left[
r(Y_s)X_s+X_s\pi_s^\top\lambda(Y_s)-c_s
\right]ds
+X_s\pi_s^\top\sigma\,dW_s^S,
\qquad
\sigma\sigma^\top=\Sigma.
\tag{1.4}
\]

For \(0<\gamma<1\), put

\[
a:=1-\gamma\in(0,1),
\qquad
U(c):=\frac{c^a}{a}.
\tag{1.5}
\]

The utility discount rate is denoted by \(\delta\), to avoid confusing it
with an interest rate or a branching lifetime density.

## 2. The factor Merton HJB

### Theorem MM-1 (optimized factor HJB)

**Status:** proved algebraic theorem, conditional on the dynamic-programming
HJB and the stated differentiability and concavity.

Suppose \(x>0\) and the value function \(V(t,x,y)\) is \(C^{1,2}\) in the
variables needed below, with

\[
V_x>0,
\qquad
V_{xx}<0.
\tag{2.1}
\]

Its pre-optimization HJB is

\[
\begin{aligned}
0={}&V_t+b(y)\cdot\nabla_yV+\frac12A:D_y^2V
+r(y)xV_x-\delta V\\
&+\sup_{c\geq0}\left\{\frac{c^a}{a}-cV_x\right\}\\
&+\sup_{\pi\in\mathbb R^n}
\left\{
x\pi^\top\lambda(y)V_x
+\frac12x^2\pi^\top\Sigma\pi\,V_{xx}
+x\pi^\top C\nabla_yV_x
\right\}.
\end{aligned}
\tag{2.2}
\]

The pointwise optimizers are

\[
\boxed{
c^*=V_x^{-1/\gamma}
}
\tag{2.3}
\]

and

\[
\boxed{
\pi^*
=
-\frac1{xV_{xx}}
\Sigma^{-1}
\left(
\lambda(y)V_x+C\nabla_yV_x
\right).
}
\tag{2.4}
\]

After substitution, the HJB becomes

\[
\boxed{
\begin{aligned}
0={}&V_t+b\cdot\nabla_yV+\frac12A:D_y^2V
+rxV_x-\delta V\\
&-\frac{
\left(\lambda V_x+C\nabla_yV_x\right)^\top
\Sigma^{-1}
\left(\lambda V_x+C\nabla_yV_x\right)
}{2V_{xx}}
+\frac{\gamma}{a}V_x^{-a/\gamma}.
\end{aligned}
}
\tag{2.5}
\]

#### Proof

The consumption Hamiltonian is

\[
h(c)=\frac{c^a}{a}-cV_x.
\]

Since \(a-1=-\gamma\),

\[
h'(c)=c^{-\gamma}-V_x,
\qquad
h''(c)=-\gamma c^{-\gamma-1}<0.
\]

Hence its unique maximizer is (2.3). At this point,

\[
h(c^*)
=
\left(\frac1a-1\right)(c^*)^a
=
\frac{\gamma}{a}V_x^{-a/\gamma}.
\tag{2.6}
\]

For the portfolio part, define

\[
q:=\lambda(y)V_x+C\nabla_yV_x.
\tag{2.7}
\]

The portfolio Hamiltonian is

\[
g(\pi)=x\pi^\top q+\frac12x^2V_{xx}\pi^\top\Sigma\pi.
\]

Because \(V_{xx}<0\) and \(\Sigma\succ0\), \(g\) is strictly concave. Its
first-order condition is

\[
xq+x^2V_{xx}\Sigma\pi=0,
\]

which gives (2.4). Completing the square, or substituting (2.4), gives

\[
\sup_\pi g(\pi)
=-\frac{q^\top\Sigma^{-1}q}{2V_{xx}}.
\tag{2.8}
\]

Equations (2.6) and (2.8) inserted into (2.2) yield (2.5).
\(\square\)

### Proof boundary

Theorem MM-1 does not prove that \(V\) exists, that it equals the control
value, or that the feedback controls are admissible. Those conclusions
require a stochastic-control verification theorem and the corresponding
integrability and boundary conditions.

## 3. CRRA reduction

### Theorem MM-2 (wealth homogeneity removes one state)

**Status:** proved algebraic theorem.

Suppose

\[
V(t,x,y)=\frac{x^a}{a}F(t,y),
\qquad x>0,
\qquad F(t,y)>0.
\tag{3.1}
\]

Then (2.5) is equivalent to

\[
\boxed{
\begin{aligned}
0={}&F_t+b(y)\cdot\nabla F+\frac12A:D^2F
+\bigl(a\,r(y)-\delta\bigr)F\\
&+\frac{a}{2\gamma F}
\left(\lambda(y)F+C\nabla F\right)^\top
\Sigma^{-1}
\left(\lambda(y)F+C\nabla F\right)
+\gamma F^{-a/\gamma}.
\end{aligned}
}
\tag{3.2}
\]

For terminal utility \(V(T,x,y)=x^a/a\),

\[
F(T,y)=1.
\tag{3.3}
\]

The feedback controls simplify to

\[
\boxed{
\pi^*(t,y)
=
\frac1\gamma
\Sigma^{-1}
\left(
\lambda(y)+C\nabla\log F(t,y)
\right),
}
\tag{3.4}
\]

\[
\boxed{
\frac{c^*(t,x,y)}x=F(t,y)^{-1/\gamma}.
}
\tag{3.5}
\]

#### Proof

From (3.1),

\[
\begin{aligned}
V_t&=\frac{x^a}{a}F_t,&
\nabla_yV&=\frac{x^a}{a}\nabla F,&
D_y^2V&=\frac{x^a}{a}D^2F,\\
V_x&=x^{-\gamma}F,&
V_{xx}&=-\gamma x^{-\gamma-1}F,&
\nabla_yV_x&=x^{-\gamma}\nabla F.
\end{aligned}
\tag{3.6}
\]

Therefore

\[
-\frac{
\left(\lambda V_x+C\nabla_yV_x\right)^\top
\Sigma^{-1}
\left(\lambda V_x+C\nabla_yV_x\right)}
{2V_{xx}}
=
\frac{x^a}{2\gamma F}
\left(\lambda F+C\nabla F\right)^\top
\Sigma^{-1}
\left(\lambda F+C\nabla F\right).
\tag{3.7}
\]

Also,

\[
V_x^{-a/\gamma}
=
\left(x^{-\gamma}F\right)^{-a/\gamma}
=x^aF^{-a/\gamma}.
\tag{3.8}
\]

Every term in (2.5) now contains \(x^a/a\). Dividing by this positive
quantity gives (3.2). Substitution of (3.6) into (2.3)--(2.4) gives
(3.4)--(3.5). \(\square\)

### Corollary MM-2.1 (many assets need not mean a high-dimensional PDE)

**Status:** proved.

If there are no stochastic factors and \(r,\lambda,\Sigma\) are constant,
then the CRRA value has only a time coefficient. The number \(n\) of risky
assets affects the equation through

\[
\lambda^\top\Sigma^{-1}\lambda
\tag{3.9}
\]

and affects the optimal portfolio through

\[
\pi^*=\frac1\gamma\Sigma^{-1}\lambda,
\tag{3.10}
\]

but it does not create \(n\) spatial PDE variables.

#### Proof

Set \(m=0\) in Theorem MM-2. Then \(F=F(t)\), all factor derivatives
disappear, and (3.2) is an ordinary differential equation. Equations
(3.9)--(3.10) are the remaining portfolio terms. \(\square\)

## 4. A test for a genuinely two-factor benchmark

The phrase “genuinely multidimensional” needs a checkable meaning. Here it
means that the factor PDE cannot collapse to a function of one fixed linear
projection \(v^\top y\).

### Theorem MM-3 (short-time obstruction to one-index reduction)

**Status:** proved.

Consider the no-consumption form of (3.2), with terminal condition
\(F(T,y)=1\). Put \(\tau=T-t\), and suppose

\[
r(y)=r_0+r_1^\top y,
\qquad
\lambda(y)=\ell+Ly.
\tag{4.1}
\]

Assume the PDE holds up to the terminal face, with for example

\[
F(T-\cdot,\cdot)\in
C^1([0,\varepsilon];C^2(\mathbb R^m)).
\]

If, on a nontrivial short-time interval,

\[
F(T-\tau,y)=\widetilde F(\tau,v^\top y)
\tag{4.2}
\]

for a fixed nonzero \(v\), then the function

\[
G(y)
:=
a\,r(y)-\delta
+\frac{a}{2\gamma}
(\ell+Ly)^\top\Sigma^{-1}(\ell+Ly)
\tag{4.3}
\]

must also be a function of \(v^\top y\).

Consequently, either of the following is sufficient to rule out (4.2):

1. \(\operatorname{rank}(L^\top\Sigma^{-1}L)\geq2\);
2. in the scalar-asset case
   \(\lambda(y)=\ell_0+\ell_1^\top y\),
   \(\ell_1\neq0\), and
   \(r_1\notin\operatorname{span}\{\ell_1\}\).

#### Proof

At \(\tau=0\),

\[
F=1,\qquad \nabla F=0,\qquad D^2F=0.
\]

The forward-in-\(\tau\) version of the no-consumption PDE therefore gives

\[
\partial_\tau F(0,y)=G(y).
\tag{4.4}
\]

If (4.2) holds, differentiating it at \(\tau=0\) shows that \(G(y)\) is a
function of \(v^\top y\). Any twice differentiable function of one linear
projection has Hessian of rank at most one:

\[
D^2G(y)=h''(v^\top y)vv^\top.
\tag{4.5}
\]

But direct differentiation of (4.3) gives

\[
D^2G(y)=\frac{a}{\gamma}L^\top\Sigma^{-1}L.
\tag{4.6}
\]

This proves the first sufficient condition.

For one risky asset with variance \(\sigma^2\),

\[
D^2G(y)
=
\frac{a}{\gamma\sigma^2}\ell_1\ell_1^\top.
\tag{4.7}
\]

If (4.2) holds and \(\ell_1\neq0\), equations (4.5)--(4.7) force
\(v\) to be collinear with \(\ell_1\). On the other hand,

\[
\nabla G(y)
=
a r_1+
\frac{a}{\gamma\sigma^2}
(\ell_0+\ell_1^\top y)\ell_1.
\tag{4.8}
\]

The gradient of a function of \(v^\top y\) must be collinear with \(v\).
If \(r_1\) is not collinear with \(\ell_1\), (4.8) contradicts this
requirement. \(\square\)

### Interpretation

A two-factor model with a short-rate loading and a nonparallel
expected-return loading is not merely the existing one-factor Vasicek
equation written with an extra coordinate. Theorem MM-3 is only a
no-fixed-linear-projection result; it does not exclude every conceivable
nonlinear change of variables.

## 5. Exact matrix-Riccati benchmark

### Theorem MM-4 (exponential-quadratic solution)

**Status:** proved PDE theorem on the maximal interval on which the displayed
ODE solution remains finite.

Assume the no-consumption equation, and let

\[
b(y)=k-Ky,
\qquad
r(y)=r_0+r_1^\top y,
\qquad
\lambda(y)=\ell+Ly,
\tag{5.1}
\]

where all matrices and vectors are constant. Let

\[
R:=\Sigma^{-1}.
\tag{5.2}
\]

For \(\tau=T-t\), define

\[
F(T-\tau,y)
=
\exp\!\left(
\alpha(\tau)+\beta(\tau)^\top y+\frac12y^\top P(\tau)y
\right),
\tag{5.3}
\]

where \(P(\tau)\) is symmetric. Put

\[
h:=\ell+C\beta,
\qquad
H:=L+CP.
\tag{5.4}
\]

If \((\alpha,\beta,P)\) solves

\[
\boxed{
P'
=
-(K^\top P+PK)
+PAP
+\frac{a}{\gamma}H^\top RH,
}
\tag{5.5}
\]

\[
\boxed{
\beta'
=
Pk-K^\top\beta+PA\beta
+a r_1
+\frac{a}{\gamma}H^\top Rh,
}
\tag{5.6}
\]

\[
\boxed{
\begin{aligned}
\alpha'
={}&
k^\top\beta
+\frac12\operatorname{tr}(AP)
+\frac12\beta^\top A\beta\\
&+a r_0-\delta
+\frac{a}{2\gamma}h^\top Rh,
\end{aligned}
}
\tag{5.7}
\]

with

\[
\alpha(0)=0,\qquad \beta(0)=0,\qquad P(0)=0,
\tag{5.8}
\]

then (5.3) is a positive classical solution of the reduced terminal-value
PDE on every interval on which the ODE solution is finite.

#### Proof

Write

\[
g(\tau,y)
=
\alpha+\beta^\top y+\frac12y^\top Py,
\qquad
p:=\nabla_y g=\beta+Py.
\tag{5.9}
\]

Then

\[
\frac{\nabla F}{F}=p,
\qquad
\frac{D^2F}{F}=P+pp^\top.
\tag{5.10}
\]

The no-consumption equation (3.2), written forward in \(\tau\) and divided
by \(F>0\), is

\[
\begin{aligned}
\partial_\tau g
={}&
(k-Ky)^\top p
+\frac12\operatorname{tr}(AP)
+\frac12p^\top Ap\\
&+a(r_0+r_1^\top y)-\delta\\
&+\frac{a}{2\gamma}
\bigl(\ell+Ly+Cp\bigr)^\top
R
\bigl(\ell+Ly+Cp\bigr).
\end{aligned}
\tag{5.11}
\]

By (5.4),

\[
\ell+Ly+Cp=h+Hy.
\tag{5.12}
\]

The constant coefficient on the right of (5.11) is

\[
k^\top\beta
+\frac12\operatorname{tr}(AP)
+\frac12\beta^\top A\beta
+a r_0-\delta
+\frac{a}{2\gamma}h^\top Rh.
\tag{5.13}
\]

The linear coefficient is

\[
Pk-K^\top\beta+PA\beta
+a r_1
+\frac{a}{\gamma}H^\top Rh.
\tag{5.14}
\]

The symmetric quadratic coefficient, in the convention
\(\frac12y^\top(\cdot)y\), is

\[
-(K^\top P+PK)
+PAP
+\frac{a}{\gamma}H^\top RH.
\tag{5.15}
\]

On the left,

\[
\partial_\tau g
=
\alpha'+(\beta')^\top y+\frac12y^\top P'y.
\]

Matching constant, linear, and quadratic coefficients gives
(5.5)--(5.7). The initial conditions (5.8) give \(F(T,y)=1\).
\(\square\)

### Proof boundary

Theorem MM-4 supplies an exact PDE benchmark. To identify it with the
stochastic-control value, one still needs admissibility and a verification
argument. A finite-time blow-up of the Riccati system is a genuine warning
about the candidate value problem, but it is not automatically identical to
a coding-tree moment explosion.

Intermediate consumption adds \(\gamma F^{-a/\gamma}\) to (3.2). After
division by \(F\), this becomes \(\gamma e^{-g/\gamma}\), so the
exponential-quadratic ansatz is not closed in general. This is why the first
multifactor benchmark should omit intermediate consumption.

## 6. Artificial wealth diffusion is not harmless

### Theorem MM-5 (CRRA support obstruction)

**Status:** proved.

Let the financial terminal utility be

\[
\phi(x,y)=\frac{x^a}{a},
\qquad x>0,
\qquad 0<a<1.
\tag{6.1}
\]

Suppose a coding-tree representation uses, at the root, a driftless
constant-covariance reference Brownian motion whose wealth coordinate has
variance coefficient \(A_{xx}>0\). Let the remaining horizon be \(h>0\).
Suppose the root clock survives to the terminal time with probability
\(\bar F_{\rm life}(h)>0\), independently of the reference Brownian
increment.
Then the root terminal factor is outside the financial domain with strictly
positive probability.

In particular, this construction does not define an almost-surely
real-valued CRRA tree functional on the original wealth domain.

#### Proof

Conditional on root survival, the terminal reference wealth is

\[
X_T^{\rm ref}=x+\sqrt{hA_{xx}}\,Z,
\qquad Z\sim N(0,1).
\tag{6.2}
\]

For every \(x>0\), \(h>0\), and \(A_{xx}>0\),

\[
\mathbb P(X_T^{\rm ref}\leq0)
=
\Phi\!\left(
-\frac{x}{\sqrt{hA_{xx}}}
\right)>0.
\tag{6.3}
\]

The lifetime clock and Brownian increment are independent in the coding-tree
construction. Hence

\[
\mathbb P(
\text{root survives and }X_T^{\rm ref}\leq0
)
=
\bar F_{\rm life}(h)
\Phi\!\left(
-\frac{x}{\sqrt{hA_{xx}}}
\right)>0.
\tag{6.4}
\]

On this event, (6.1) is not defined as the original real financial utility.
For the repository default \(a=1/2\), it is not real-valued at all.
Therefore the terminal factor required by the coding-tree theorem is not a
finite real random variable almost surely. \(\square\)

### Consequences

The probability in (6.4) can be astronomically small at wealth \(x=100\)
and a short horizon. That explains why smoke tests may never observe the
failure; it does not repair the theorem.

Valid routes include:

1. CRRA reduction to the factor-only equation;
2. a singular reference covariance with \(A_{xx}=0\);
3. a separately derived log-wealth coordinate;
4. a domain-aware stopped representation with the correct boundary problem.

Replacing \(x^a\) by \(|x|^a\) changes the terminal condition and therefore
changes the PDE problem.

## 7. Full-covariance state-dependent coding identity

Consider

\[
\partial_tu+\mathcal L_Au+f(x,Ju)=0,
\qquad
\mathcal L_A
:=
\frac12\sum_{k,l=1}^dA_{kl}\partial_{x_kx_l},
\tag{7.1}
\]

where \(A=A^\top\succeq0\) is constant and

\[
Ju=(D^{\alpha_1}u,\ldots,D^{\alpha_m}u).
\tag{7.2}
\]

For \(a_0\in\mathbb R\), spatial multi-index \(\beta\), and jet
multi-index \(\nu\), define

\[
G_{a_0,\beta,\nu}
:=
\left(
a_0\partial_x^\beta\partial_z^\nu f
\right)^*.
\tag{7.3}
\]

Let \(\mathscr E_\mu\) be the labelled expansion of
\(D^\mu[f(x,Ju)]\) obtained by repeatedly applying the ordinary product and
chain rules. A record

\[
(c,\beta',\nu';\lambda_1,\ldots,\lambda_s)
\in\mathscr E_\mu
\tag{7.4}
\]

denotes

\[
c
(\partial_x^{\beta'}\partial_z^{\nu'}f)(x,Ju)
\prod_{j=1}^sD^{\lambda_j}u.
\tag{7.5}
\]

Repeated labelled records retain their multiplicity.

### Theorem MM-6 (full-covariance mechanism identity)

**Status:** proved algebraic theorem.

Assume all displayed mixed space-time derivatives exist and commute, so that
the following chain-rule calculation is licensed.

The source for the code \(G_{a_0,\beta,\nu}\) is represented by the labelled
union of the following tuples.

First, for every \(p\) and every record (7.4) in
\(\mathscr E_{\alpha_p}\),

\[
\left(
G_{a_0,\beta,\nu+e_p},
G_{c,\beta',\nu'},
D^{\lambda_1},\ldots,D^{\lambda_s}
\right).
\tag{7.6}
\]

Second, for every \(k,l\),

\[
\left(
G_{-a_0A_{kl}/2,\,\beta+e_k+e_l,\,\nu}
\right).
\tag{7.7}
\]

Third, for every \(p,k,l\),

\[
\left(
G_{-a_0A_{kl},\,\beta+e_k,\,\nu+e_p},
D^{\alpha_p+e_l}
\right).
\tag{7.8}
\]

Fourth, for every \(p,q,k,l\),

\[
\left(
G_{-a_0A_{kl}/2,\,\beta,\,\nu+e_p+e_q},
D^{\alpha_p+e_k},
D^{\alpha_q+e_l}
\right).
\tag{7.9}
\]

All ranges in (7.7)--(7.9) are ordered labelled ranges. In particular,
\((k,l)\) and \((l,k)\) remain separate when \(k\neq l\), and reversed
\((p,q,k,l)\) labels remain separate even if their child products agree.

When \(A=\sigma^2I\), the zero off-diagonal terms disappear and
(7.6)--(7.9) reduce to the isotropic state-dependent mechanism already
recorded in `estimator-integrity/secondary-candidates.md`.

#### Proof

Put

\[
h(x,z)
=
a_0\partial_x^\beta\partial_z^\nu f(x,z),
\qquad
w(t,x)=h(x,Ju(t,x)).
\tag{7.10}
\]

Because \(A\) is constant and the required mixed derivatives commute,
\(D^{\alpha_p}\) commutes with
\(\partial_t+\mathcal L_A\). Equation (7.1) gives

\[
(\partial_t+\mathcal L_A)D^{\alpha_p}u
=
-D^{\alpha_p}[f(x,Ju)].
\tag{7.11}
\]

The first spatial derivative of \(w\) is

\[
\partial_{x_k}w
=
h_{x_k}
+\sum_p h_{z_p}D^{\alpha_p+e_k}u.
\tag{7.12}
\]

Differentiating once more,

\[
\begin{aligned}
\partial_{x_kx_l}w
={}&h_{x_kx_l}
+\sum_p h_{x_kz_p}D^{\alpha_p+e_l}u
+\sum_p h_{x_lz_p}D^{\alpha_p+e_k}u\\
&+\sum_p h_{z_p}D^{\alpha_p+e_k+e_l}u\\
&+\sum_{p,q}
h_{z_pz_q}
D^{\alpha_p+e_k}u
D^{\alpha_q+e_l}u.
\end{aligned}
\tag{7.13}
\]

Combining the time derivative with the terms in (7.13) containing
\(h_{z_p}\), and then using (7.11), yields

\[
\begin{aligned}
(\partial_t+\mathcal L_A)w
={}&
-\sum_p h_{z_p}D^{\alpha_p}[f(x,Ju)]\\
&+\frac12\sum_{k,l}A_{kl}h_{x_kx_l}\\
&+\sum_{p,k,l}
A_{kl}h_{x_kz_p}D^{\alpha_p+e_l}u\\
&+\frac12\sum_{p,q,k,l}
A_{kl}h_{z_pz_q}
D^{\alpha_p+e_k}u
D^{\alpha_q+e_l}u.
\end{aligned}
\tag{7.14}
\]

The two mixed terms in (7.13) combine into the third line of (7.14)
because \(A\) is symmetric.

The source in the backward Duhamel equation for \(w\) is the negative of
(7.14). Expanding \(D^{\alpha_p}[f(x,Ju)]\) with
\(\mathscr E_{\alpha_p}\) gives (7.6). The negatives of the final three
lines give (7.7), (7.8), and (7.9), respectively. \(\square\)

### Theorem MM-7 (conditional coding-tree representation)

**Status:** conditional representation theorem.

Choose any matrix \(B\) with \(BB^\top=A\), and define the possibly
degenerate Gaussian semigroup by

\[
P_sg(x)=\mathbb E[g(x+BW_s)].
\]

No transition density, inverse of \(A\), or determinant of \(A\) is used.

Use:

- \(\mathcal M(\mathrm{Id})=\{(G_{1,0,0})\}\);
- the labelled chain-rule expansion \(\mathscr E_\mu\) for
  \(\mathcal M(D^\mu)\);
- (7.6)--(7.9) for \(\mathcal M(G_{a_0,\beta,\nu})\);
- the constant-covariance Markov kernel generated by \(\mathcal L_A\);
- terminal factors
  \[
  g_{\mathrm{Id}}=\phi,\qquad
  g_{D^\mu}=D^\mu\phi,\qquad
  g_{G_{a_0,\beta,\nu}}
  =
  a_0(\partial_x^\beta\partial_z^\nu f)(x,J\phi(x)).
  \tag{7.15}
  \]

Assume:

1. every derivative reached from the requested root codes exists and the
   differentiated Duhamel equations are valid;
2. each reached code has a lifetime density positive almost everywhere on
   every used branch-time interval and a positive survival tail at every
   used horizon;
3. every live labelled mechanism alternative has positive proposal
   probability; the clock, Markov motion, and tuple draw are independent;
   terminal and branch weights are respectively
   \(1/\bar F_c\) and \(1/(\rho_cq_c)\);
4. all children use the same branch position and are conditionally
   independent after birth;
5. the continuous-time tree is nonexplosive;
6. every reached unrestricted tree functional is absolutely integrable;
7. the resulting infinite code-indexed mild system is unique in a class
   containing both the classical code fields and the tree expectations.

Then

\[
\mathbb EH_{t,x,\mathrm{Id}}=u(t,x),
\tag{7.16}
\]

\[
\mathbb EH_{t,x,D^\mu}=D^\mu u(t,x),
\tag{7.17}
\]

and

\[
\mathbb EH_{t,x,G_{a_0,\beta,\nu}}
=
a_0(\partial_x^\beta\partial_z^\nu f)(x,Ju(t,x)).
\tag{7.18}
\]

#### Proof

Theorem MM-6 and the labelled expansion \(\mathscr E_\mu\) show that the
classical fields on the right of (7.16)--(7.18) solve the code-indexed
backward Duhamel system with terminal data (7.15).

Condition on the first lifetime, the first Markov branch position, and the
selected labelled tuple. The survival factor cancels the probability of
surviving to the horizon. On a branch event, the lifetime-density and
tuple-probability denominators cancel their respective proposal laws.
Conditional child independence at the one shared branch position turns the
expected product of child functionals into the product of their
expectations. Absolute integrability licenses these conditional
expectations and the required Fubini steps. The unrestricted tree
expectations therefore solve the infinite mild system directly.

Equivalently, for the canonical killed construction,
\[
H^{[n]}=H\mathbf1_{\{\operatorname{depth}\leq n\}}.
\]
Nonexplosion and absolute integrability then give
\(H^{[n]}\to H\) in \(L^1\) by dominated convergence, while first-event
conditioning identifies the killed expectations with the finite Picard
iterates. Assumption 7 identifies the limiting mild-system solution with the
classical code fields.
\(\square\)

### Proof boundary

Theorem MM-7 does not establish any of its seven assumptions for the Merton
model. In particular:

- a valid mechanism identity does not imply \(L^1\) or \(L^2\);
- finite batches do not prove integrability;
- singular covariance removes artificial wealth motion but also removes
  elliptic smoothing in that direction;
- for singular \(A\), all regularity and uniqueness in
  \(\ker A\) remain assumptions;
- the Hessian denominator in the HJB requires a sign and separation
  condition;
- a standard error is justified only after a finite second moment is
  established;
- no result in this note is presently formalized end-to-end in Lean.

## 8. What the search supports

The following prior-art boundaries are important.

1. Merton's continuous-time portfolio/consumption model and CRRA reduction
   are classical:
   [Merton (1971), DOI 10.1016/0022-0531(71)90038-X](https://doi.org/10.1016/0022-0531(71)90038-X).
2. Predictable OU returns and finite-horizon nonmyopic behavior are
   classical:
   [Kim and Omberg (1996), DOI 10.1093/rfs/9.1.141](https://doi.org/10.1093/rfs/9.1.141).
3. Multifactor quadratic opportunity models and matrix-Riccati solutions
   are classical:
   [Liu (2007), DOI 10.1093/rfs/hhl001](https://doi.org/10.1093/rfs/hhl001).
4. Correlated Vasicek investment/consumption problems already have
   analytical and dual treatments:
   [Chang and Chang (2014), DOI 10.1007/s11424-014-1165-6](https://doi.org/10.1007/s11424-014-1165-6).
5. Multidimensional Gaussian partial-information portfolio choice is
   established:
   [Lakner (1998), DOI 10.1016/S0304-4149(98)00032-5](https://doi.org/10.1016/S0304-4149(98)00032-5).
6. Arbitrary-derivative coding trees without explicit state dependence are
   established:
   [Nguwi, Penent, and Privault (2023), DOI 10.1007/s00028-023-00873-3](https://doi.org/10.1007/s00028-023-00873-3).
7. Their multidimensional deep implementation is:
   [Nguwi, Penent, and Privault (2024), DOI 10.1016/j.jcp.2023.112712](https://doi.org/10.1016/j.jcp.2023.112712).
8. State-dependent coefficients in semilinear branching with gradient
   marks have close prior art:
   [Henry-Labordère et al. (2019), DOI 10.1214/17-AIHP880](https://doi.org/10.1214/17-AIHP880).

The bounded search did not locate a source combining:

- explicit-state arbitrary-jet coding;
- constant possibly singular full covariance;
- a CRRA-reduced irreducible multifactor Merton benchmark;
- exact matrix-Riccati validation;
- code-conditioned moment certification;
- pilot-frozen adaptive tuple proposals.

This is evidence for a candidate contribution, not proof of publication
priority.

## 9. Ranked theorem opportunities

1. **Full-covariance explicit-state arbitrary-jet representation.**
   Theorem MM-6 gives the algebra; the research task is to discharge useful
   conditions in Theorem MM-7.
2. **Merton-specific unrestricted-tree moment certificate.**
   Connect the existing exact multitype moment recursion to a computable
   \(L^1/L^2\) region for the two-factor benchmark.
3. **Joint reference-covariance and proposal optimization.**
   Optimize the Brownian reference covariance, lifetime law, and tuple
   probabilities against second moment times expected work.
4. **Representation-comparison theorem.**
   Compare drift-as-source Brownian coding with an exact OU-semigroup coding
   mechanism, including the derivative commutator terms.
5. **Policy certification.**
   Combine joint derivative-code moments, denominator separation, feedback
   uncertainty, and a simulated achieved-utility lower bound.

These are potential contributions. None should be called a breakthrough
until its theorem is completed and a broader systematic novelty review is
performed.
