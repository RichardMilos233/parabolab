# T91: polynomial field sampling and linear-time common Gaussian audit

Date: 2026-09-29. Independent conventional mathematical review.

**Separate verdicts:**

- **Frozen R20 alone: REPAIR.** Its standalone statement omits the
  continuous-function domain of its Frechet derivative. Its closing
  mean-square-error sentence also needs an explicit upper inequality.
  Section 2 records exact counterexamples and the necessary repairs.
- **Frozen R20 together with frozen R20b: PASS.** I read the final
  addendum completely and checked its hash. It closes both issues
  without changing the intended smooth-input application, sampling law,
  constants, or fixed-time mathematical result.
- **Frozen R21: PASS.** The guarded tree recursion, full Gaussian
  independence, maximal common variance including singular covariance,
  nonlinear field identity, and linear preparation work all pass.

These are fixed-time sampling results for the specified scalar
polynomial reaction and constant positive diffusion. They do not
supply a generalized long-horizon solver, matching complexity lower
bound, practical speedup, finite-bit implementation, or complete Lean
proof. Root acceptance and source correspondence remain separate.
The accepted T87/T90 results are unchanged by this audit.

## 1. Read sources and precise scope

Paths in this table are relative to
`docs/research/runs/2026-09-28-dynamic-continuation/`.

| Frozen source | Lines | SHA256 |
| --- | ---: | --- |
| `reviews/R20-polynomial-reaction-field-sampler-candidate.md` | 332 | `b1e42a195c67942066894d04a11c28d7ba2951a6d6730977070e424ac84542b9` |
| `reviews/R20b-continuous-domain-addendum.md` | 46 | `6c5e8b158ca269588c4200ca09c82f4ffa430e8aa0146a52022370ade352e527` |
| `reviews/R21-linear-tree-common-gaussian-candidate.md` | 231 | `99f8a23c98332b6797ee1ecc9f0929d94950cd047acb17bcbea0df9052ff7461` |
| `reviews/T87-all-diffusion-sharp-query-feasibility.md` | 788 | `acd788e6ee5564778cd0663be99aab17fb61f22bdfb4b345ccade008f18feff1` |
| `reviews/T90-sharp-query-independent-audit.md` | 814 | `f8959804af651f78b1a48ee6f9d96139aa397388fba88167f6e30daa5804a907` |

R20, R20b and R21 were read completely for this task. T87 was read
completely and independently audited in the immediately preceding
T90 task; T90 is this reviewer's own prior audit. Their unchanged
hashes were rechecked. This provenance does not make T90 independent
of this reviewer; the new R20/R21 arguments are independently derived
below rather than inferred from a previous verdict.

Fix a known real polynomial `f`, integers `d>=1`, real `kappa>0`
and `0<tau<infinity`, with `f(-1)>=0` and `f(1)<=0`. The actual
equation on the normalized unit torus is

    u_t=(kappa/2) Delta u+f(u).

In the corrected R20 statement, `g,v in C(X)` are real,
`||g||inf<1`, `e=v-g in C(X)`, and `g` has an explicit known
evaluator costing at most `G` paid operations per lookup. The only
new unknown information consists of charged exact point values of
`v`. The derivative at `g` accepts any continuous direction `e`;
its definition does not require the full point `g+e` to remain in
the unit ball. A Taylor assertion about `S_tau(g+e)` separately
requires the whole segment to stay in that ball.

All work bounds use the inherited paid exact-real model: scalar
arithmetic, comparisons, floors/ceilings, indexing/modular operations,
stored reads/writes, the stated elementary functions, and known-
parameter exact Gaussian, uniform, and exponential draws are charged.
Ideal word sizes and arbitrary finite exact magnitudes are allowed.
No arbitrary function, integral, derivative, covariance sampler,
matrix inverse, transform, or PDE oracle is added. The finite output
of a sample is a real box-frequency coefficient array; the infinite
Hilbert-valued field is the analytical object establishing its law.

## 2. The two R20 repairs and the final addendum

**Domain defect.** R20 Section 1 originally only requires a known
evaluable `g` with sup norm below one and a residual `e=v-g`.
That permits, on the one-dimensional torus,

    g(x)=(1/2) 1_[0,1/2)(x modulo 1),       v(x)=0.

This `g` has a fixed finite evaluator using modular reduction and
one comparison, and `||g||inf=1/2`. It meets that literal wording,
but it is not in `C(X)`. The expression `D^jS_tau(g)` for the
explicitly claimed map on the open unit ball of `C(X)` is undefined.
Likewise, taking `g=0` and a discontinuous `v` permits a direction
outside that Banach space. These are domain counterexamples, not
failures of the continuous-input construction. A possible separate
bounded-Borel extension is not the stated Frechet theorem.

The necessary repair is to require real `g,v in C(X)`, a uniform
finite known evaluator cost for `g`, and `e=v-g in C(X)`, while
retaining `||g||inf<1`. No extra bound `||v||inf<1` is needed for
the derivative sampler itself. The existing Taylor clause continues
to require `g+t e` in the open ball for every `0<=t<=1`. This
distinction matters for a polynomial whose flow outside its invariant
interval might have a different existence interval.

**Risk wording defect.** The closing paragraph of R20 Section 5
says that averaging gives mean-square error `V_j delta^(2j)/M`.
The proof supplies an upper bound, not that generally exact value.
For a literal-equality counterexample, take `f=0`, `g=0`, a nonzero
constant continuous `e`, and `j=2`. The parent rule is the arithmetic
average, every complete leaf polynomial is linear, and every
second-order sample is identically zero. Its mean-square error is
zero, whereas `V_2||e||inf^4/M>0`. The required wording is

    E||M^-1 sum_a W_(j,a)-E W_j||_r^2
      <=V_j delta^(2j)/M,       delta>=||e||inf.

The exact identity instead has the centered Hilbert second moment
in its numerator. Original formula R20 (1.1) already uses the correct
inequality; only the later sentence needed precision.

The final R20b at the hash in Section 1 explicitly makes both repairs,
states the actual open domain and separate segment condition, and
preserves the original file. I find the combined corrected statement
well defined. No further repair is needed for the fixed-time claims
proved below. The root supplied this addendum during the review;
this reviewer did not modify R20 or R20b.

## 3. Lemma 1: explicit bounded parent rule for every inward polynomial

Choose a fixed integer `B>=max(2,deg f)`; for the zero polynomial
one may simply choose `B=2`. If
`f(2t-1)=sum_(l=0)^B a_l t^l`, its degree-`B` Bernstein coefficients
are

    F_i=sum_(l=0)^i a_l binom(i,l)/binom(B,l).

To verify the change of basis, use

    binom(B,i)binom(i,l)=binom(B,l)binom(B-l,i-l).

Summing against `t^i(1-t)^(B-i)` gives
`binom(B,l)t^l(t+1-t)^(B-l)`. This proves the formula exactly,
including degree elevation. It is a finite public arithmetic
construction; all binomial denominators used are positive integers.

Set `Fmax=max_i |F_i|`, `lambda=1+B Fmax/2`, and

    c_i=2i/B-1+F_i/lambda.

One has `lambda>0` and `|F_i|/lambda<2/B`. For interior `i`,
the base value `2i/B-1` is at distance at least `2/B` from each
endpoint of `[-1,1]`. At `i=0`, the sign `F_0=f(-1)>=0` moves
the base value inward by less than `2/B<=1`. At `i=B`,
`F_B=f(1)<=0` does the same from the upper endpoint. Hence every
`c_i` lies in `[-1,1]`, with no missing endpoint assumption.

For child values `y_1,...,y_B`, put

    M(y)=sum_(A subset {1,...,B}) c_(|A|)
                product_(i in A)(1+y_i)/2
                product_(i notin A)(1-y_i)/2.

This is symmetric and multiaffine. Its weights are nonnegative on
the cube and sum to one, so `|M|<=1`. On the diagonal, the
binomial mean gives the contribution `2t-1=z` from `2i/B-1`,
and the Bernstein identity gives `f(z)/lambda` from the remaining
coefficients. Thus

    lambda[M(z,...,z)-z]=f(z).

If `Fmax=0`, then `f=0`, `lambda=1`, and the same sum reduces
to `B^-1 sum_i y_i`. The construction has no division by `Fmax`
and covers this case without a limiting argument. Evaluation costs
a finite constant depending on fixed `B`; a degree-uniform or
optimal-degree algorithm is not claimed.

## 4. Lemma 2: actual branching law, moments, and the PDE

For rate-`lambda` branching into exactly `B` children, the population
has jumps `n -> n+B-1` at total rate `lambda n`. Expanding its
generator on the `p`th power, for each integer `p>=1`, gives

    lambda n[(n+B-1)^p-n^p]
      =lambda sum_(l=1)^p binom(p,l)(B-1)^l n^(p-l+1)
      <=lambda(B^p-1)n^p.

The process stopped on reaching population at least `L` is bounded
by `L+B-2` when `L>=2`. Dynkin and Gronwall therefore apply before
assuming nonexplosion. Its first-moment bound implies hitting
probability at most `exp(lambda(B-1)tau)/L`. Letting `L` increase
proves nonexplosion. Fatou gives

    E n(tau)^p<=exp(lambda tau(B^p-1)).

Every realized finite full `B`-ary tree with `n` terminal leaves
has `(Bn-1)/(B-1)<=2n` particle segments. Its recursive leaf
polynomial is multiaffine because child label sets are disjoint;
the cube bound follows inductively from Lemma 1.

For continuous initial `q` with values in `[-1,1]`, the tree
expectation is bounded by one. Conditional on the first split and
its spatial endpoint, the child trees are independent. Since `M`
is affine in each separate child variable, its conditional mean is
`M` applied to their common conditional mean. This is a valid use
of independence, not an exchange of expectation with a general
nonlinear function of a single variable.

The renewal equation has killed-heat generator
`kappa Delta/2-lambda` and source `lambda M(u,...,u)`.
Lemma 1 turns their sum into `kappa Delta/2+f(u)`. All renewal
terms are bounded, so conditioning and Fubini are legitimate. Local
mild existence follows from polynomial local Lipschitz continuity;
the constant functions `-1` and `1` are a subsolution and a
supersolution by the inward endpoint signs. Comparison keeps the
solution in that interval and prevents finite-time failure. Bounded
mild uniqueness identifies the tree expectation with the actual
`S_t q`. The Brownian coordinate variance `kappa t` gives the
displayed diffusion coefficient exactly.

## 5. Lemma 3: common smoothing, Hilbert moments, and Frechet derivatives

For every finite clock genealogy of height `tau`, including
zero-length segments, its lifted one-coordinate leaf covariance is

    C=sum_e ell_e b_e b_e^t,

where `b_e` indicates the descendant terminal labels. At almost
every time, the active particles partition the `n` labels into at
most `n` blocks. For every signed vector `z`, Cauchy--Schwarz on
those blocks and integration over `[0,tau]` give

    z^t C z>=tau(1^t z)^2/n.

Consequently `C-(tau/n)11^t` is positive semidefinite for any
fixed arity. Degenerate edges alter the partition at finitely many
times only. For `n=1`, the covariance is `tau` and the residual is
zero. Exact guarded semidefinite Cholesky, as audited in T90, samples
the residual from scalar Gaussians in `O(n^3)` operations, including
zero-pivot cases.

Conditional on the tree, take that residual array `Z` with physical
covariance scaled by `kappa`, and an independent common Gaussian
of covariance `kappa tau I_d/n`. Their sum has the exact original
joint leaf law. Integrating the common Gaussian in the entire
translated polynomial and then using independent uniform `U in X`
gives the field

    F_tree(q)=h_(kappa tau/n)(.-U)
                P_tree(q(U+Z_1),...,q(U+Z_n)).

Positions are reduced modulo the torus in every known or unknown
function evaluation. The expectation of this field is `S_tau q`
for `||q||inf<1`. The heat convolution acts on the whole polynomial,
not separately on its factors or only on its selected derivative.

Use the real separable Hilbert space `H^r`, `r=d+1`, with

    ||w||_r^2=sum_nu (1+|nu|^2)^r |what(nu)|^2.

The shell calculation in T87/T90 gives the continuous embedding
`||w||inf<=E_d||w||_r`, `E_d^2=1+4d3^(d-1)`. With
`theta=4*pi^2*kappa*tau`, the Gaussian-sum calculation gives a
fixed public `C_h` such that

    ||h_(kappa tau/n)(.-U)||_r^2
      =sum_nu (1+|nu|^2)^r exp(-theta|nu|^2/n)
      <=C_h n^(r+d/2)<=C_h n^(r+d).

This is the same explicit Gaussian-sum bound with `kappa` replaced
by `kappa tau`, both positive. Translation does not change the
norm. The frequency cutoff has not entered any constant.

A mixed partial in `j` distinct leaf labels equals `2^-j` times
the signed sum of the selected `2^j` corner values. Therefore its
absolute value is at most one. Repeated labels give zero. The
order-`j` directional derivative of the complete field is the
ordered-injection sum with norm at most

    n^j ||h_(kappa tau/n)||_r product_a ||e_a||inf.

Its squared envelope has expectation at most

    V_j=C_h exp(lambda tau(B^(2j+r+d)-1)),       j>=0.

On each finite-tree event, the Gaussian arithmetic, leaf positions,
and evaluations of continuous profiles are Borel. For fixed `n`,
translation of the heat kernel is continuous in `H^r`. Countably
many finite shapes and counts cover the almost-sure termination
event. The directional fields are thus strongly measurable and,
by their integrable norm envelopes, genuinely Bochner integrable.
Only fixed tuples of directions are integrated; no strong
measurability in an operator or Dirac-measure space is needed.

Finite-polynomial Taylor bounds on a segment in the open unit ball
give operator continuity with envelope
`n^(j+1)||h||_r ||q-q0||inf` and first-order derivative remainder

    (1/2)n^(j+2)||h||_r ||q-q0||inf^2.

Both envelopes have finite expectation. Taking directional
expectations and then the operator supremum proves genuine Frechet
differentiability at each order, without an unsupported exchange.
By induction, the actual map from the open ball of `C(X)` into
`H^r` is `C^infinity`, with operator norm bound `sqrt(V_j)` at
order `j`. The continuous embedding commutes with point evaluation,
so the map is the actual PDE flow identified in Lemma 2.

For any segment `g+t e` entirely in that open ball, the integral
Taylor remainder is consequently

    ||S_tau(g+e)-sum_(j=0)^(J-1)D^jS_tau(g)[e^j]/j!||_r
      <=sqrt(V_J)||e||inf^J/J!.

The corrected domain in R20b is exactly what these steps require.
No higher spatial derivative of the unknown input has been used.

## 6. Lemma 4: actual tuple queries, finite output, and risk

After complete tree and residual preparation, choose uniform `U`
and a uniform ordered injection `I` of `j` labels when `n>=j`.
Cache the known `g(U+Z_i)` and evaluate the selected mixed partial
`C_I` by at most `2^j` tree passes. Only then acquire the selected
original values and form

    z=(n)_j C_I product_(a=1)^j e(U+Z_(I_a)),
    W_j=h_(kappa tau/n)(.-U) z.

For `n<j`, return zero with no acquisitions. Conditional averaging
over the injection cancels `(n)_j` and gives the ordered derivative
sum exactly. Equal directions retain the usual `j!` multiplicity;
Taylor division by `j!` occurs only in the Taylor formula. Thus

    E W_j=D^jS_tau(g)[e,...,e],
    E||W_j||_r^2<=V_j||e||inf^(2j).

The coefficient and the heat shift share the same `U`; independence
between them is not assumed. The norm bound is pathwise before
integrating and therefore keeps every relevant correlation.

There are at most `j` scalar acquisitions on every seed, including
repeated spatial locations. A null nonterminating preparation makes
no acquisition for that sample. The finite algorithm never queries
a derivative, a PDE value, or an integral. Its known evaluations are
charged at their actual cost `G`.

For a requested finite cutoff, the complex coefficient is

    z exp(-2*pi^2*kappa*tau*|nu|^2/n) exp(-2*pi*i*nu.U).

The real constant is `z`, and the real cosine/sine coefficients for
one representative of each `{nu,-nu}` are the stated twice-amplitude
cosine and positive-sine expressions. The sign follows because the
real sine coefficient is minus twice the complex imaginary part.
These are finite formulas in allowed primitives, not infinite heat
series evaluations.

With `K=(2N+1)^d`, matrix construction/factorization, tree passes,
lookup, tuple selection, coefficient generation, and storage cost

    C_(B,j,d)[n^3+(1+G)n+K].

Lemma 2's first and third moments yield expected cost at most
`C_(f,d,kappa,tau,j)(1+G+K)`. All statement parameters are fixed
before drawing a tree. Preparation is almost surely finite, and
the finite Fourier output is Borel; it may be extended by zero on
null nontermination seeds for its probability law.

For independent copies, the genuine Hilbert identity is

    E||M^-1 sum_a(W_(j,a)-mu_j)||_r^2
      =M^-1(E||W_j||_r^2-||mu_j||_r^2)
      <=V_j delta^(2j)/M,
    mu_j=E W_j,       delta>=||e||inf.

Cross terms vanish by centering and independence between copies,
with Fubini justified by second moments. No coordinate independence
is required. Fourier projection contracts this norm. In the actual
real basis its squared norm is

    c0^2+(1/2)sum_(nu representatives)
                    (1+|nu|^2)^r(c_(nu,c)^2+c_(nu,s)^2).

Coordinate clipping decreases error only relative to a target whose
coordinates lie in the chosen intervals. This statistical observation
does not say that clipping an individual derivative sample preserves
its mean or that flow coefficient intervals automatically contain
all derivative coefficients. No such additional claim is needed for
the fixed-time sampler. The embedding controls the supremum before
expectation for any error field to which this Hilbert bound applies.

## 7. Lemma 5: exact quintic check and its limited consequence

For `f(u)=u-u^5`, direct expansion gives

    f(2t-1)=-8t+40t^2-80t^3+80t^4-32t^5.

Substitution in Lemma 1's exact coefficient formula for `B=5` gives

    (F_0,...,F_5)=(0,-8/5,4/5,-4/5,8/5,0).

For example `F_2=-16/5+40/10=4/5`, and
`F_3=-24/5+3*40/10-80/10=-4/5`. The endpoint sum at `i=5`
is zero, as required. Hence `Fmax=8/5`, `lambda=5`, and

    (c_0,...,c_5)=(-1,-23/25,-1/25,1/25,23/25,1).

All corners lie in the cube. The verified Bernstein identity gives
`5[M(u,...,u)-u]=u-u^5` without an approximation. This establishes
the quintic fixed-time sampler through Lemmas 1--4.

Also `f'(u)=1-5u^4<=1`, `f'(0)=1`, and `f` is odd. Solving
`z'=-4z+4` for `z=u^-4` at a positive scalar initial value `a`
gives

    phi_t(a)=a exp(t)/[1+a^4(exp(4t)-1)]^(1/4).

These scalar identities are correct. They do not supply the missing
spatial known-profile solver, lower-prior PDE separation, or full
same-class complexity argument. No universal exponent or new
long-time theorem is inferred from the quintic example.

## 8. Lemma 6: R21's guarded recursion, including zero children

Now fix the deterministic finite genealogy of R21. Every root-to-leaf
length is `tau>0`, and each internal segment has at least two
children for the cost statement. In one physical coordinate let
the independent edge Gaussians have variances `ell_v>=0`, with
the variable set identically to zero when that length is zero.

At a leaf define `a_v=ell_v`, `A_v=Y_v`. At an internal segment,
if every child `a_c>0`, put

    h=(sum_c 1/a_c)^-1,       alpha_c=h/a_c.

The denominator is strictly positive. Direct algebra gives

    alpha_c>=0,       sum_c alpha_c=1,
    alpha_c a_c=h for each c,
    sum_c alpha_c^2 a_c=h.

If at least one child has `a_c=0`, put weight one on the first
such child in the stored ordering and zero on the others, with
`h=0`. Every displayed identity remains exact, even with several
zero children or a mixture of zero and positive values. No reciprocal
of zero is formed. Then set

    a_v=ell_v+h,       A_v=Y_v+sum_c alpha_c A_c.

The recursion is a total Borel finite rule on all nonnegative edge
lengths. If `a_v=0`, then `ell_v=0`, and either the vertex is a
zero leaf or its selected zero child also has zero aggregate by
induction. Thus `A_v` is identically zero in the actual algebraic
construction on such a subtree. One does not merely appeal to a
zero-variance event while continuing to divide by zero.

The identities and zero guards even make sense on non-ultrametric
trees; the common-height assumption is needed later for the lower
bound `tau/n`. On a common-height subtree with positive remaining
height, its aggregate cannot have zero variance, as Lemma 8 will
also show. Keeping the general zero guard handles endpoint
degeneracies without relying on that later conclusion.

## 9. Lemma 7: covariance induction and the full residual independence

Write `X_(v,i)` for the path sum from the beginning of segment `v`
to its terminal descendant `i`. The base case gives

    Var(A_v)=a_v,       Cov(X_(v,i),A_v)=a_v.

For an internal node, different child subtrees and `Y_v` are
independent. Lemma 6 therefore gives

    Var(A_v)=ell_v+sum_c alpha_c^2 a_c=ell_v+h=a_v,
    Cov(X_(v,i),A_v)=ell_v+alpha_c a_c=ell_v+h=a_v

when the leaf belongs to child `c`. These equalities include every
zero-child case. All variables are centered Gaussian linear
combinations with deterministic coefficients conditional on the tree.

There is also a convex leaf-weight identity. If each child's
aggregate is a convex combination of its descendant path sums,
multiply those weights by `alpha_c` and unite the disjoint label
sets. Their sum is one, which counts the common `Y_v` exactly once.
At the root this proves, for deterministic weights conditional on
the genealogy,

    w_i>=0,       sum_i w_i=1,
    A=sum_i w_i X_i,       Var(A)=a,       Cw=a1.

The weights are a proof device. They need not be expanded or stored
by the algorithm, which computes `A` by the recursion.

Set `Z_i=X_i-A`. The covariance identities give

    Cov(Z_i,A)=0,       Cov(Z_i,Z_j)=C_ij-a.

The vector `(A,Z_1,...,Z_n)` is jointly Gaussian, possibly singular.
Its characteristic function factors when the cross block is zero.
Hence `A` is independent of the entire residual vector `Z`, not
merely uncorrelated with each coordinate or pairwise independent.
Sampling ordinary independent edge Gaussians, evaluating `A`, and
subtracting it from each leaf samples precisely this residual law.

Different physical coordinates use independent edge arrays. After
multiplication by `sqrt(kappa)`, the common vector `G` has covariance
`kappa a I_d` and is independent of the entire physical residual
array, conditional on the genealogy. A random-tree mixture need not
give unconditional independence of `G` and `Z`; R21 does not need
that stronger and generally false assertion.

## 10. Lemma 8: positivity and maximal removable common variance

Apply the deterministic common-height partition inequality to `w`:

    a=w^t Cw>=tau(1^t w)^2/n=tau/n>0.

This does not assume an inverse or positive definiteness of `C`.
For each leaf, `Var(X_i)=tau` and `Cov(X_i,A)=a`, so covariance
Cauchy--Schwarz gives `a^2<=tau a`. Positivity now implies
`a<=tau`. Thus

    tau/n<=a<=tau.

The covariance matrix of `Z` is `C-a11^t`, so it is positive
semidefinite. If some real `b` also has `C-b11^t` positive
semidefinite, then

    0<=w^t(C-b11^t)w=a-b.

Consequently `a` is the largest removable scalar common variance,
including when `C` is singular. Equivalently, it is the minimum of
`z^t C z` over real `z` with `1^t z=1`: the PSD residual proves
the lower bound and `w` attains it. Signed competitors are therefore
covered; the optimization is not restricted to convex weights.

If `C` is invertible, `Cw=a1` and `1^t w=1` give
`a=(1^t C^-1 1)^-1`. This is a corollary, not the program used
for singular or nonsingular trees. The optimality concerns a common
Gaussian covariance for this fixed genealogy; it does not optimize
the nonlinear estimator's variance or its complete computational cost.

## 11. Lemma 9: changed residual and heat law give the same nonlinear mean

Interpret all leaf function arguments on the inherited unit torus.
For `F in C(X^n)`, bounded by compactness, fix the tree and the
residual array of Lemma 7. Their common Gaussian is independent of
that whole array. Gaussian convolution of the complete translated
function gives

    E_G F(x+G+Z_1,...,x+G+Z_n)
      =integral_X h_(kappa a)(x-u) F(u+Z_1,...,u+Z_n) du.

The orientation follows from evenness of the heat density. All
arguments here are reduced modulo the torus. This is not asserted
for an arbitrary nonperiodic function of unwrapped Euclidean leaf
positions. Applied to the tree polynomial and to its full ordered
directional-derivative expression, it proves R21's actual mean
identity with the same PDE derivative as R20/R20b or T87.

With independent uniform `U`, the new field is

    W_j=h_(kappa a)(.-U)(n)_j C_I
                  product_(b=1)^j e(U+Z_(I_b)).

All unselected known values, the coefficient `C_I`, and all residual
directions use this same array `U+Z`. The preparation has changed
the residual covariance to `kappa(C-a11^t)` and the heat variance to
`kappa a` jointly. Keeping the old leaf law while changing only a
Fourier damping factor would not establish this identity.

The lower bound for `a` yields termwise Fourier monotonicity:

    ||h_(kappa a)||_r^2
      =sum_nu(1+|nu|^2)^r exp(-4*pi^2*kappa*a*|nu|^2)
      <=||h_(kappa tau/n)||_r^2<=C_h n^(r+d).

Hence every derivative envelope and second-moment bound in Lemma 3
survives with the same constants. The heat-kernel map `(a,U)` into
`H^r` is continuous for `a>0`, by Fourier dominated convergence
locally in `a`. On each finite-tree event one even has
`a>=tau/n>0`. Combined with the guarded Borel tree recursion, this
proves strong measurability for the new fields. Their Bochner,
Frechet, Taylor and projected Hilbert-risk arguments proceed with
the same integrable envelopes.

For finite output use `exp(-2*pi^2*kappa*a*|nu|^2)` in the real
coefficient formulas of Lemma 4. The positive sine sign, ordered
tuple factor, and hard `j`-query cap remain correct. There is no
claim that the complete estimator variance is smaller: its residual
law and scalar coefficient have changed as well. The preserved
upper bound follows from the pathwise envelope, not a comparison
of the two complete sample distributions.

## 12. Lemma 10: actual linear preparation work and endpoint examples

Let the tree have `m` particle segments and `n` leaves. Since every
internal segment has at least two children, `m<=2n-1`, and the
number of child-list entries is exactly `m-1`. A fixed number of
traversals therefore has the following actual paid costs:

1. A postorder pass inspects child variances, applies the zero guard
   or harmonic formula, and stores each `a_v` and child weight.
   Each child list is scanned a fixed number of times, costing `O(m)`.
2. Generate `d` scalar Gaussians for each nonzero segment, with the
   prescribed variance or a guarded positive square root and scaling;
   zero segments are assigned zero. A preorder pass propagates path
   sums from the root and stores all leaf sums, costing `O_d(m)`.
3. A postorder pass computes the aggregates `A_v` with the stored
   weights. Subtract the root aggregate from every terminal path sum.
   This also costs `O_d(m)`.

No leaf's whole root path is resummed separately, so no hidden
depth-times-leaf-count factor occurs. No dense covariance matrix,
expanded leaf-weight vector, inverse, or rejection conditioning is
constructed. Storage, comparisons, reciprocals, and Gaussian draws
are included. Tiny positive variances pose no extra operation-count
cost in the explicitly ideal model; finite-precision conditioning is
outside this statement.

Genealogy generation is linear in the number of segments. With
fixed arity `B` and order `j`, the at-most-`2^j` parent passes,
known-value cache, coordinate reduction, and tuple selection also
cost `C_(B,j,d)(1+G)n`. The `K=(2N+1)^d` finite output costs
`O_d(K)`. Thus the complete conditional sample cost is

    C_(B,j,d)[(1+G)n+K].

The corresponding expected-work claim uses only the first
population moment `E n<=exp(lambda tau(B-1))` for preparation.
Higher moments are still required for the derivative second moment.
Almost-sure halting, Borel rules, and the all-seed query cap follow
with the same preparation-before-acquisition order as in Lemma 4.

The exact examples also pass. With one leaf, `a=tau`, `A=X_1`,
and the residual is zero. For a star with ancestral length `b`
and `n` terminal lengths `tau-b`, when `b<tau` the child weights
are `1/n`, giving

    a=b+(tau-b)/n,       A=n^-1 sum_i X_i.

When `b=tau`, all child variances are zero; the specified first-zero
branch gives `a=tau`, `A=Y_root`, and all residuals zero. All leaf
values coincide, so this is also their average. When `b=0`,
`a=tau/n`, attaining the universal lower bound. These are exact
algebraic edge-case checks, not simulation results.

The no-unary assumption matters for expressing the bound as `O(n)`:
a tree with arbitrarily many unary segments and one leaf would
instead cost its number of segments. R21 explicitly excludes that
case from its `O(n)` statement, and the T87/R20 genealogies obey
the required arity condition.

## 13. Acceptance boundary and attribution

R20 plus R20b proves an actual fixed-time `H^(d+1)` derivative
sampler for each fixed polynomial with the stated inward signs,
each fixed positive constant diffusivity and positive finite burn-in,
and continuous base/direction data. It includes the precise quintic
example. R21 supplies a compatible linear-time Gaussian preparation
with the largest removable common variance for each finite tree.
Together they preserve the fixed-time field mean, second moment,
finite output, and scalar query cap.

No claim is made for general nonpolynomial or gradient reactions,
systems, spatially varying diffusion, missing invariant intervals,
zero burn-in, zero diffusivity, or constants uniform in the reaction,
dimension, derivative order, diffusivity, or time. In particular,
R20's extra moments can be very large as fixed parameters increase.

Neither note supplies a generalized paid known-profile solver or
a matching lower bound. The upper comparison rate
`sup_[-1,1] f'` need not equal the instability rate of a chosen
equilibrium. The Allen--Cahn exact-query theorem is not automatically
transferred to every inward polynomial. R21 improves conditional
tree preparation work; this audit does not claim a changed
long-horizon work exponent or global estimator optimality.

I opened the primary An--Henderson--Ryzhik text at Sections 3.2--3.4,
including the Bernstein coefficient/rate construction and Theorems
3.2--3.4. Its bounded voting construction with vanishing endpoint
reaction is established prior work; R20 directly proves its stated
signed inward-endpoint adaptation. No theorem from that source is
used in place of the cube, moment, or derivative proofs above.
[Primary voting text](https://arxiv.org/html/2209.03435).

I also inspected the text of Felsenstein's original paper at printed
pages 8--10, particularly page 10's inverse-variance weighted tip
aggregation, branch-variance update, and treatment of multifurcations
via zero branches. This confirms the classical recursion attribution.
The complete singular covariance and nonlinear field statements
were independently proved above. A requested screenshot of the
printed page failed because the web tool's screenshot support was
unavailable; no visual inspection is claimed.
[Felsenstein primary paper](https://ichthyology.usm.edu/courses/multivariate/Felsenstein_1985.pdf).

These limited source inspections are attribution checks. They do
not establish worldwide novelty or priority of any combined theorem,
and no prize-level or practical-significance conclusion is drawn.

## 14. Activity, model routing, and frozen T90 clarification

Only this new T91 audit file is owned or changed by this task. I
checked that it did not already exist and inspected the dirty tree.
R20, R20b, R21, T87, T90, accepted ledgers, run configuration,
Lean, code, numerical data, and canvases were not edited by this
reviewer. The addendum was supplied by the root in response to
the two specific findings, and its final supplied version alone
was read for the corrected verdict.

The math-auto-research skill, defaults, model-routing and execution
instructions, configured General profile, and applicable project
scope instructions were already read in this worker's preceding
T90 task. They were retained rather than repeatedly reread. This
task used the continued requested research configuration
`gpt-6-astra/max`; the actual serving backend and effort remain
unexposed. Reusing a worker and reading model preferences are not
evidence of an independently attested model switch. No model-setting
change, cost estimate, or token total is fabricated.

Actual work was source inspection and hashing, independent exact
derivation, communication of the repairs, bounded primary-source
inspection, and writing/rereading this audit. No original input was
queried. No numerical PDE solve, stochastic experiment, symbolic
algebra program, implementation test, or Lean invocation was run.
The quintic coefficients and tree examples above were checked by
displayed exact algebra. Their role is a check, not experimental
proof of a universal result. Final source hashes are verified again
after writing; this audit's hash is reported in the handoff.

For the root's explicit provenance question, the final T90
813-to-814-line self-review patch made four wording/layout changes:

1. It wrapped the sentence identifying `S_1 q` under `||q||inf<1`.
2. It replaced the one-line sentence about every step being a
   spatial-supremum bound with two lines stating that the embedding,
   saturation and continuation inequalities hold pathwise for that
   supremum. This change accounted for the one added line.
3. It replaced the ambiguous phrase about an unsigned class with
   the same bounded smoothness class without the sign-change condition.
4. It changed the description of an actual new sampling law to an
   actual modified sampling law, avoiding an unintended novelty reading.

No T90 formula, assumption, verdict, or frozen dependency changed
in that final patch. Its final hash is the one in Section 1. T90
has not been altered during this new task.
