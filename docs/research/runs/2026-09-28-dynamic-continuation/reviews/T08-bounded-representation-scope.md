# T08 — the scope and cost of bounded polynomial branching rules

Date: 28 September 2026. Status: bounded conventional-theory assessment and
primary-literature check. No numerical experiment, implementation or Lean
formalization was performed. This is the only file written for T08.

## 1. Decision

There is a nonperturbative extension beyond the Jacobi interface: **every
real polynomial f with `f(-1)>=0` and `f(1)<=0` has a finite-arity bounded
multiaffine branching representation on `[-1,1]`**. The endpoint conditions
are necessary and sufficient, and no degree elevation is needed merely
to obtain existence. A finite Bernstein-coefficient formula gives the
exact smallest rate at each fixed arity, even if asymmetric kernels are
allowed.

This general construction is not a defensible novelty claim. Bernstein
voting representations for endpoint-vanishing polynomial reactions are
explicit in An–Henderson–Ryzhik, and minimal effective branching structures
are already studied by Cordero–Hummel–Schertzer. Allowing inward endpoint
drift amounts to allowing a parent to change a unanimous child vote.
The algebra below makes that elementary extension and its exact constants
explicit for this project.

The representation removes the long-horizon moment explosion of the raw
signed tree, but it retains an exponential workload. For Allen–Cahn,
ternary majority at rate two minimizes the expected leaf count and total
node count over **all fixed-arity bounded multiaffine kernels**, including
asymmetric ones. More generally, sensitivity at an interior unstable
equilibrium forces exponential expected leaf count for the input-independent
bounded multiaffine tree architecture. Neither assertion is a lower bound
for every possible PDE algorithm.

## 2. Exact existence theorem and rate formula

Let f be a real polynomial and fix an integer

    n >= max(2,deg f).

For the zero polynomial, any n>=2 is allowed. Set

    p=(u+1)/2,                    F(p)=f(2p-1)/2,
    b_(k,n)(p)=binomial(n,k)p^k(1-p)^(n-k),
    F(p)=sum_(k=0)^n F_k^(n)b_(k,n)(p).

The Bernstein coefficients are explicitly computable. If
`F(p)=sum_(j=0)^d a_j p^j`, then

    F_k^(n)=sum_(j=0)^min(k,d) a_j binomial(k,j)/binomial(n,j).
                                                               (2.1)

Use `x_+=max(x,0)`. Under the inward endpoint conditions, define

    r_n^* = max {
        F_0^(n), -F_n^(n),
        n(F_k^(n))_+/(n-k), n(-F_k^(n))_+/k : 1<=k<n
    }.                                                        (2.2)

It is finite and nonnegative. For nonzero f it is positive. A simple
sufficient, possibly nonoptimal, choice is

    r=max(1,n max_(0<=k<=n)|F_k^(n)|).

For a given `r>0`, a bounded multiaffine map `B:[-1,1]^n->[-1,1]` with

    r[B(u,...,u)-u]=f(u)                                (2.3)

exists **if and only if** the endpoint conditions hold and `r>=r_n^*`.
If n is smaller than deg f and deg f>=2, no such map exists because its
diagonal has degree at most n.

### 2.1 Construction

For `r>=r_n^*`, put

    q_k=k/n+F_k^(n)/r,       c_k=2q_k-1.                 (2.4)

The endpoint signs are precisely
`F_0^(n)=f(-1)/2>=0`, `F_n^(n)=f(1)/2<=0`. Formula (2.2) ensures
`0<=q_k<=1` at both endpoints and every interior index. Define B by its
values on cube vertices: at a vertex with k plus signs, set B=c_k.
Equivalently, for `p_i=(x_i+1)/2`,

    B(x_1,...,x_n)
      = sum_(S subset {1,...,n}) c_|S|
          product_(i in S)p_i product_(i notin S)(1-p_i). (2.5)

The nonnegative weights sum to one, so B is bounded by one and is affine
in each coordinate. On the diagonal,

    (B(u,...,u)+1)/2
       = sum_k q_k b_(k,n)(p)
       = p+F(p)/r,

which is (2.3). This is a direct construction at degree n, not an
approximation of f by Bernstein polynomials.

The apparent `2^n` formula need not be evaluated by enumerating corners.
The probabilities of k successes with independent success parameters p_i
are the coefficients of `product_i[(1-p_i)+p_i z]`. Successive multiplication
by these linear factors takes O(n^2) arithmetic operations and O(n) memory;
then take their weighted sum with c_k. This describes a finite evaluation
algorithm, not an implementation or an arithmetic-error certificate.

### 2.2 Necessity, including asymmetric kernels

At the two constant vertices, boundedness and (2.3) give

    f(-1)=r[B(-1,...,-1)+1]>=0,
    f(1)=r[B(1,...,1)-1]<=0.

Thus even endpoint tangency is allowed, while an outward endpoint sign
is impossible. For example `f(u)=1` cannot have such a bounded rule.

For any possibly asymmetric bounded multiaffine B, average its vertex
values over all vertices with k plus signs and call that average c_k.
These averages lie in `[-1,1]`. Multiaffine interpolation then writes
the diagonal in the same Bernstein form as (2.5). Uniqueness of
Bernstein coefficients forces `(c_k+1)/2=q_k` from (2.4).
The inequalities `0<=q_k<=1` are exactly (2.2). Symmetrization therefore
loses no feasibility for a prescribed diagonal and fixed arity.

Strict inward drift does not require unanimous votes to be preserved:
`f(-1)>0` means `q_0>0`, and `f(1)<0` means `q_n<1`. This is the only
endpoint change needed relative to the usual unanimous voting contract.

## 3. The bounded PDE estimator and its full-tree cost

Consider

    u_t=(1/2)Delta u+f(u),        u(0,x)=phi(x) in [-1,1],

on Euclidean space or the periodic domain, with the corresponding Brownian
heat semigroup. At rate r, each particle splits into n children at its death
position; the children evolve independently after birth. A terminal leaf
returns phi at its final position, and a branch combines its n child outputs
using (2.5).

For finite n and r, this branching process is nonexplosive at every finite
horizon. Every finite-tree output lies in `[-1,1]` by induction, hence

    |H_T|<=1 almost surely,       E[H_T^2]<=1,
    Var(H_T)<=1-u(T,x)^2.                                (3.1)

At the first branch, conditional independence and multiaffinity yield

    E B(H_1,...,H_n)=B(EH_1,...,EH_n).

Consequently the bounded mean satisfies the renewal identity

    m(t)=exp(-rt)P_t phi
          + integral_0^t r exp(-rs)P_s[h(m(t-s))]ds,
    h(u)=B(u,...,u)=u+f(u)/r.

This is the mild equation for the desired reaction f. Lipschitz continuity
of a polynomial on `[-1,1]` gives uniqueness among bounded mild solutions.
Inward endpoint signs preserve this interval by the usual comparison
principle. The result applies to arbitrary bounded nonconstant terminal
profiles in the interval; it is not a small perturbation or one-profile
statement. Diffusion dimension does not affect the boundedness argument.

Let L_T be the number of leaves and N_T the total number of sampled nodes
in the complete n-ary tree. Then

    E L_T=exp(r(n-1)T),
    E N_T=[n exp(r(n-1)T)-1]/(n-1).                      (3.2)

For example, the first formula follows from the population generator:
each of the L live particles adds n-1 live particles at rate r. The
identity `N=1+n(L-1)/(n-1)` gives the second formula. Stopping/localization
justifies the expectation equation, and its finite bound also establishes
nonexplosion. The O(n^2) branch-combination cost is additional to node
generation and terminal evaluation.

There is also a hard-vote version: leaves are independent spins with means
phi, and a parent with k plus child spins returns +1 with probability q_k.
Integrating out all leaf and parent vote randomness conditional on the
Brownian tree gives the soft recursion (2.5). Thus the soft estimator is
a conditional expectation of the hard estimator and has no larger variance.
Both still require the complete tree under the contract used in (3.2).

## 4. Allen–Cahn: optimality among all fixed arities

Let `f(u)=u-u^3`. Any fixed-arity multiaffine realization must have n>=3.
Independently of multiaffinity, its bounded diagonal must satisfy

    h(u)=u+(u-u^3)/r,       h(1)=1,       h(-1)=-1.

Since `h(u)<=1` for u<1, its left derivative at 1 is nonnegative. Therefore

    h'(1)=1-2/r>=0,         r>=2.                        (4.1)

The same condition follows from the right derivative at -1. Increasing
arity or removing symmetry cannot evade this diagonal constraint.

It follows that every such fixed-arity complete tree has

    r(n-1)>=4,               E L_T>=exp(4T).              (4.2)

Ternary majority at rate two attains equality:

    B_2(x,y,z)=(x+y+z-xyz)/2,
    E N_T=(3exp(4T)-1)/2.

It also minimizes expected total node count for every T>=0 in this class.
Indeed the derivative in T of the expression in (3.2) is
`nr exp(r(n-1)T)`, at least `6exp(4T)` when n>=3 and r>=2; all candidates
start from one node at T=0.

This conclusion extends the earlier fixed-ternary comparison in
[the old B1–B2 proof](../../2026-09-25-long-horizon/04-theory.md).
It does not claim optimality among random-offspring mixtures, leaf-dependent
early stopping, shared-subtree schemes, biased continuation, or other
representations. The prior independent review already observed the
arity-independent bound r>=2; the added cost conclusion follows directly
from the degree and population formulas.

## 5. A general sensitivity barrier, with precise architecture assumptions

Fix an interior equilibrium `u_* in (-1,1)` with `f(u_*)=0`. Assume one
representation is exact for all spatially constant initial values u in
an open neighborhood of u_*. Impose the following structural contract:

* The random finite tree and any auxiliary branch-rule randomness have
  laws independent of the constant input value u.
* Distinct descendant leaves are distinct inputs; a leaf is not reused
  in two supposedly independent child subtrees.
* Conditional on the tree and its auxiliary randomness, the root is a
  bounded multiaffine function `Phi_T:[-1,1]^(L_T)->[-1,1]` of those leaves.

Bounded multiaffine local rules with independent subtrees satisfy this
contract by finite-tree induction. It also describes the conditional
mean of a bounded voting procedure given its independent terminal spins.

### 5.1 Direct leaf-Lipschitz bound

Holding all other inputs fixed, a bounded affine function on `[-1,1]`
has slope of absolute value at most one. Telescoping the leaf coordinates
therefore gives, for the same coupled tree,

    |Phi_T(u,...,u)-Phi_T(v,...,v)|<=L_T|u-v|.

If `E L_T=infinity`, the following lower bounds are already true. Otherwise
expectation and the difference quotient give

    |m_T'(u)|<=E L_T,

where m_T is the scalar ODE flow at time T. Linearization of `y'=f(y)`
at the equilibrium gives `m_T'(u_*)=exp(f'(u_*)T)`, hence

    E L_T>=exp(f'(u_*)T).                                (5.1)

Finite E L_T also supplies the domination needed to differentiate the
averaged conditional polynomial. No unproved exchange of a derivative
with an uncontrolled tree expansion is needed.

### 5.2 A stronger score bound under the same contract

Attach conditionally independent spins `xi_i in {-1,1}` with mean u to
the leaves, and evaluate the same bounded map on those spins:

    Z_T=Phi_T(xi_1,...,xi_(L_T)).

Multiaffinity gives `E Z_T=m_T(u)`. The tree law does not depend on u.
The score for its terminal spins is

    S_u=sum_(i=1)^(L_T)(xi_i-u)/(1-u^2),
    E S_u=0,                E S_u^2=E L_T/(1-u^2).

For each finite tree, differentiating the finite spin probability sum gives
the score identity. The leaf-Lipschitz domination above and finite E L_T
allow its average, yielding

    m_T'(u)=E[(Z_T-m_T(u))S_u].

Since `|Z_T|<=1`, Cauchy–Schwarz gives

    (m_T'(u))^2 <= [1-m_T(u)^2] E L_T/(1-u^2).             (5.2)

At the equilibrium the two variance factors cancel, so

    E L_T>=exp(2 f'(u_*)T).                              (5.3)

Thus an unstable equilibrium forces exponential expected leaf count even
when the estimator's output is uniformly bounded. For Allen–Cahn, (5.3)
gives `exp(2T)`; the fixed-arity endpoint/degree argument in Section 4
is stronger and gives `exp(4T)` for that smaller architectural class.

Equation (5.2) is the familiar information/score lower bound behind
Bernoulli-factory sample complexity. A primary treatment is
[Mendo, Theorem 3 and its proof](https://arxiv.org/pdf/1612.08923).
That theorem treats a more general sequential setting with its stated
regularity assumptions. The direct proof above uses the narrower,
input-independent random-tree contract and finite E L_T.

### 5.3 Why the assumptions matter

Boundedness and subtree independence alone do not imply a leaf-Lipschitz
bound: the bounded scalar map `sin(Kx)` can have slope K. Multiaffinity
supplies the unit coordinate slope here. A method allowed to insert the
known scalar ODE flow itself at one leaf would also evade this information
contract. Input-dependent tree laws introduce additional score terms.
Shared samples, nonlinear terminal transforms, data-dependent pruning,
and cancellation or approximation across separate trees require their
own analysis. Neither (5.1) nor (5.3) is asserted for those methods.

## 6. Finite arity search for the expected leaf-growth exponent

There is a simple finite search for the best exponent within the homogeneous
fixed-arity class. For a nonzero inward-pointing polynomial, define

    r_cont = sup_(-1<u<1)
                max{ f(u)/(1-u), -f(u)/(1+u), 0 }.        (6.1)

This number is finite and strictly positive. Endpoint inward signs prevent
a positive infinite limit; if an endpoint value is zero, the corresponding
finite quotient limit is given by an endpoint derivative. A nonzero
polynomial is nonzero at some interior point, which proves positivity.

Every bounded diagonal `u+f(u)/r` requires `r>=r_cont`, regardless of
arity. In particular `r_n^*>=r_cont`. Define

    gamma_n=(n-1)r_n^*.

Choose any available admissible arity m and let `Gamma=gamma_m`. Any
candidate arity which improves or ties Gamma must satisfy

    n <= 1+Gamma/r_cont.                                (6.2)

Consequently one need only evaluate the finitely many exact coefficient
thresholds (2.2) below this bound; the minimum is attained. One may replace
r_cont in (6.2) by any known positive lower bound on it. For rational or
algebraic polynomial coefficients, a certified nonzero value at a rational
interior point already supplies such a bound; exact root isolation can
instead compute (6.1) from polynomial critical-point equations.

This optimizes expected **leaf growth**, not automatically expected total
runtime, variance times cost, or total-node count at a prescribed finite T.
The zero reaction is separate: no branching is needed for the heat equation.
If unary rules are allowed, affine reactions also have a separate simpler
case; the search here uses n>=2 as in Section 2.

The optimization question itself has substantial precedent in minimal
ancestral structures. The finite cutoff is a useful elementary certificate
for this restricted implementation class, not evidence of a new general
branching-optimization theory.

## 7. Primary-source comparison and research decision

The earlier run's B1–B2 proof and independent review were read first. The
following primary sources were then opened and their indicated statements
checked; this is a bounded search, not worldwide priority certification.

1. [An, Henderson and Ryzhik, *Voting models and semilinear parabolic
   equations*](https://arxiv.org/pdf/2209.03435), Section 3.2, equations
   (3.24)–(3.31), and Theorem 3.2: the endpoint-vanishing polynomial case
   uses the same Bernstein coefficient construction. Section 3.3 gives
   monotone random-threshold variants; Section 3.4 considers broader
   recursive polynomial propagation. The inward-endpoint version here
   relaxes their unanimous-vote restriction. Its elementary extension
   should not be presented as a methodological breakthrough.
2. [Cordero, Hummel and Schertzer, *General selection models: Bernstein
   duality and minimal ancestral structures*](https://arxiv.org/pdf/1903.06731),
   Theorem 2.6, Proposition 2.32 and Section 7: polynomial selection
   decompositions, effective branching-rate minimization, convex-polytope
   characterizations and algorithms already have a developed theory.
   Their branching/coalescing population-genetic setting is broader in
   some directions and different from this spatial full-tree estimator.
3. [Mendo, *An asymptotically optimal Bernoulli factory for certain functions
   that can be expressed as power series*](https://arxiv.org/pdf/1612.08923),
   Theorem 3 and Section 7.5: the derivative-squared sample lower bound is
   established through sequential Cramer–Rao analysis. The proof in
   Section 5 is a specialization to independent random trees.

The theorem provides a genuinely broader **input and reaction scope** than
the known Jacobi interface: arbitrary interval-valued spatial data and any
inward-pointing scalar polynomial reaction. Its construction is established
mathematics, and its complete-tree cost is exponential. For Allen–Cahn,
changing the fixed arity cannot improve the minimal full-tree work below
ternary majority at rate two. These facts favor investigating architectures
that reduce complete-tree work—while proving their bias, dependence and
approximation effects—rather than presenting the generic bounded voting
construction or more sample plots as a new resolution of long-time cost.

No implementation is requested by this note. Its completed outputs are
the exact existence/rate characterization, the stated architecture-specific
cost lower bounds, and the literature-grounded assessment of what they do
and do not add to the current project.
