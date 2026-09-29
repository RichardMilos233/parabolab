# R10b: direct derivative sampling for a fixed Allen--Cahn burn-in

Root conventional proof candidate, 2026-09-29. This version explicitly
states residual continuity, as identified during T68 review; the submitted
R10 text is preserved. No other mathematical content changed. Independent review is
pending. This is a candidate subroutine for R08's derivative-work gate,
not a stable-graph or base-phase solver, practical long-horizon algorithm,
new Lean target, or authorized numerical experiment.

## 1. Statement and explicit work model

Fix L<infinity, integer j>=1, a known continuous g on the unit torus with
||g||infinity<=a<1, and an unknown continuous residual e=v-g with ||e||infinity<=delta.
In the intended application v is the original smooth C^s input and g is
the paid smooth interpolant; all Frechet directions here lie in C(X).
Let S_t solve u_t=Delta u/2+u-u^3. The construction returns Z_j(x) with

    E Z_j(x)=D^j S_L(g)[e,...,e](x),
    E|Z_j(x)|^2 <=delta^(2j) E N_L^(2j)
                 <=delta^(2j) exp(2(3^(2j)-1)L).             (1)

Every path acquires at most j exact unknown v values, including repeats.
All other function evaluations use the known g formula. They count as
work, not as new unknown-input queries. The tree is finite almost surely.

In an explicitly ideal model counting exact exponential/Gaussian/uniform
draws, scalar operations and one g evaluation as primitives, expected
work is at most C_j(d+1)exp(4L). Actual formula-evaluation cost multiplies
the appropriate term. A paid local interpolant's cell lookup and local
polynomial/partition evaluation must be counted. Constants may be huge
in fixed L,j,d. Continuous random seeds define measurable query points;
exact Gaussian draws are not claimed to be finite-bit operations. A
machine implementation requires separate rounding and random-bit analysis.

The mean derivative uses a uniform root. A centered derivative can use
one fair coin, has at most four times the second moment in (1), and keeps
the j-query cap. No infinite-time graph derivative is claimed here.

## 2. Bounded multiaffine tree polynomials

At every ternary vertex propagate

    M(a,b,c)=(a+b+c-abc)/2.

Its eight corner values on {-1,1}^3 are majority signs. Multilinear
interpolation therefore bounds M by one on the cube. A fixed finite
ternary tree with N distinct leaf labels defines a multiaffine polynomial
P_T(z_1,...,z_N), bounded by one on [-1,1]^N: the child subtrees have
disjoint labels, preserving multiaffinity under each parent product.

For distinct leaf labels i_1,...,i_j,

    |partial_(i_1)...partial_(i_j) P_T(z)|<=1.              (2)

Freeze other coordinates. This derivative does not depend on the selected
coordinates and equals exactly

    2^(-j) sum_(epsilon in {-1,1}^j)
         product_l(epsilon_l) P_T(z with z_(i_l)=epsilon_l).

All 2^j summands have magnitude at most one. A repeated differentiation
in the same leaf coordinate is zero. These are exact polynomial identities,
not approximate finite differences in the initial profile.

## 3. Actual tree, nonexplosion and moments

Start one particle at x, diffuse with generator Delta/2, split each particle
into three at rate 2, and stop descendants at elapsed time L. Wrap Brownian
increments onto the torus. The leaf count N_t starts at 1, jumps by 2, and
has jump rate 2N_t. For integer m>=1 its generator satisfies

    2n[(n+2)^m-n^m]
      =2 sum_(r=1)^m binom(m,r)2^r n^(m-r+1)
      <=2(3^m-1)n^m,                    n>=1.             (3)

Stop at the first count at least K. Dynkin's identity and Gronwall give
E N_(t stopped)^m<=exp(2(3^m-1)t). For m=1, the probability of reaching
K by t is <=exp(4t)/K, hence finite-time explosion has probability zero.
Fatou proves the moment bound after removing stopping. Integrability then
removes stopping from the first-moment integral equation and gives exactly

    E N_t=exp(4t).                                        (4)

If B is the number of branch events, N=2B+1 and the complete tree has
3B+1=(3N-1)/2 nodes. Each node requires a clock and one Brownian endpoint
increment, not a sampled continuous path. Generation/storage costs O(dN)
primitives. Its law and all moments are independent of g and e.

## 4. PDE identity and genuine derivatives

Let X_1,...,X_N be terminal positions. Attach g(X_i) and propagate P_T.
Conditional child-tree independence and multiaffinity give branch mean
M(u,u,u)=(3u-u^3)/2. The first-branch renewal equation therefore has PDE

    u_t=Delta u/2+2(M(u,u,u)-u)=Delta u/2+u-u^3.

Bounded mild uniqueness implies

    S_Lg(x)=E P_T(g(X_1),...,g(X_N)).                      (5)

For a fixed tree the jth derivative in h_1,...,h_j is

    sum_(i_1,...,i_j distinct)
      partial_(i_1)...partial_(i_j)P_T(g(X))
          product_(ell=1)^j h_ell(X_(i_ell)).              (6)

The sum is over ordered injections of derivative labels, so there is no
missing j! factor. It is represented by a finite atomic signed measure on
the full j-fold leaf product, with TV <=(N)_j, the falling factorial (zero
if N<j). Taking its setwise expectation gives a countably additive Borel
measure with TV<=E(N)_j, by the integrable variation bound. No generic
multilinear-operator-to-measure theorem is used.

On any sup-norm segment inside the open unit ball, the next derivative
and the Taylor remainder are dominated by powers of N times the appropriate
products of direction norms, using (2). All such moments are finite by
(3). The operator difference of order-j expressions at g and g' is at
most E N^(j+1) ||g-g'||, using one extra leaf label. Uniformity in x and
the integral remainder identify every finite Frechet derivative of the
expectation with (6), with operator continuity. By (5) these are the actual
flow derivatives. This proves a finite-time measure representation as
well as the probabilistic identity; it says nothing about infinite-time
stable-graph derivatives.

## 5. Sample a tuple instead of enumerating a tensor

If N<j, return zero without residual calls. Otherwise choose an ordered
injection (I_1,...,I_j) uniformly from the (N)_j possibilities. Evaluate
known g at all leaves and compute the selected mixed partial C_I of P_T.
Acquire v(X_(I_l)), l=1,...,j, then output

    Z_j=(N)_j C_I product_(l=1)^j
                            [v(X_(I_l))-g(X_(I_l))].       (7)

Averaging over the selected tuple gives (6) with every direction equal to
e. Averaging over the tree gives (1)'s mean. Pathwise,
|Z_j|<=(N)_j delta^j, which proves (1)'s second moment. Distinct leaves
can have identical spatial positions; every acquisition is still charged.

The corner identity in Section 2 computes C_I in at most 2^j passes through
the existing tree, caching unselected g values. This takes at most C_j N
arithmetic/g-evaluation primitives. Ordered tuple selection needs at most
linear work via a partial or full shuffle. A partial integer-selection
method with fair-bit rejection has expected bit count O(j(1+log(N+1))),
which is integrable. This does not convert Gaussian draws to finite bits.
Thus (4) proves the stated expected ideal work bound.

No unknown residual value controls branching, tuple selection or weights.
Every rule is measurable in the input-independent seed and previously
paid transcript. The full tree halts almost surely, and the j-query cap
even holds on paths on which tree generation does not terminate, since
queries are postponed until the finite tree and tuple are ready.

For the mean derivative choose a uniform root before generation. For
D^j(Q S_L)(g)[e^j](x), flip a fair coin: root x and output 2Z_j on heads;
a uniform root and output -2Z_j on tails. This has the desired difference
as mean, at most j queries, and second moment <=4delta^(2j)E N^(2j).

## 6. Remaining work gates and scope

For fixed L,j, all moments and work constants are independent of the target
horizon T. This avoids a full tensor for the finite-time derivative alone.
It may be useful in composing a future stable-graph derivative sampler, but
its signed weights and total second-moment/work bounds must also be proved.

- Direct use at L=T costs exp(4T) expected leaves and is not made cheap here.
- A generic bounded-variance average for H(g) at error exp(-T) can still
  need order exp(2T) samples. The base-value gate in R08 remains open.
- Small deterministic Q S_Lg does not imply small variance of the difference
  of two noisy flow values. Operator contraction alone does not establish
  a useful second moment for a stable-graph recursion.

For growing L,j the dependence in (1) and (4) must be retained. No
uniform-in-dimension, bit-cost, floating-error or practical-speed theorem
is inferred. This candidate is not a new general voting representation.

## 7. Primary attribution and independent review gate

The Allen--Cahn ternary-majority representation is established prior work.
The normalization for Delta/2 and u-u^3 was checked directly in Section 4.
Root opened An--Henderson--Ryzhik, checked Section 3.1 and the indicated
recursive-propagation context of Section 3.4, and opened the EFP abstract.
Their presentation credits Etheridge, Freeman and Penington for the
majority construction. [AHR primary text](https://arxiv.org/html/2209.03435),
[EFP primary abstract](https://arxiv.org/abs/1607.07563).
This was not a priority search for derivative samplers.

Independent review should check the cube partial bound, ordered-label
factorials, derivative-expectation exchange, rate-two normalization, and
the precise known-profile/unknown-query/random-primitive work distinction.
No accepted ledger, Lean source, experiment or frozen proof was changed.
