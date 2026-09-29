# R25: coefficient-weighted leaf subsets before acquiring the direction

Date: 2026-09-29. Root conventional candidate, not an accepted claim.
This is a separate sampler proposal. Frozen E5 continues to use uniform
ordered tuples and complete signed-corner passes. No code, Lean, numerical
sampling or unknown-input acquisition was executed for R25.

## 1. Exact inherited object and goal

Retain accepted D43/D44 with fixed arity B>=2 and derivative order j>=1,
fixed tau,kappa>0, continuous known g with ||g||inf<1 and evaluator cost G,
and continuous unknown v with e=v-g. Work is in the inherited ideal-real
model. The Gaussian genealogy, common variance a, residual positions Z,
uniform translation U, and every known leaf value b_i=g(U+Z_i) are prepared
before any v acquisition. Repetitions at the scalar v boundary are charged.

The exact finite leaf polynomial P_T is multiaffine and bounded on its
cube. For a j-element leaf set S, write c_S=partial_S P_T(b). The finite
directional derivative to be estimated conditionally on this preparation is

    F_j(e)=j! sum_(|S|=j) c_S product_(i in S) e_i,
    e_i=e(U+Z_i).

The ordinary uniform-subset version is equivalent to D44's ordered tuples:
with L=binomial(n,j), its output is j! L c_S product e_i. We seek a law
depending only on the known coefficients, with linear preparation for
fixed B,j, that retains the exact mean and hard j-query cap.

Source locks:

- `04aa-polynomial-fields-and-linear-gaussian-preparation.md`:
  `433c699d951c74fa6ba19166e159069130e1340a7a319aa0334b0ba4f8a1b8a1`.
- `reviews/R20b-continuous-domain-addendum.md`:
  `6c5e8b158ca269588c4200ca09c82f4ffa430e8aa0146a52022370ade352e527`.
- `reviews/R21-linear-tree-common-gaussian-candidate.md`:
  `99f8a23c98332b6797ee1ecc9f0929d94950cd047acb17bcbea0df9052ff7461`.

No fractional or sparse-frequency extension is needed for the statement.
For a Taylor application the original open-unit-segment condition remains.

## 2. Exact absolute derivative masses without enumerating leaf subsets

At every subtree v compute its actual base value b_v=P_v(b_leaves).
Internal values are evaluated by the parent polynomial; they are not
silently replaced by a common initial constant. In addition store

    H_(v,0)=1,
    H_(v,k)=sum_(S subset leaves(v), |S|=k) |partial_S P_v(b)|,
                1<=k<=j.

The zero entry is a bookkeeping identity, NOT |P_v(b)|. At a leaf,
H_0=H_1=1 and H_k=0 for k>=2. At an internal node with children c=1..B,
let A={c:k_c>0} for a vector of nonnegative counts with sum k_c=k>0.
Define d_A=partial_A M(b_1,...,b_B). Then

    H_(v,k)=sum_(k_1+...+k_B=k)
                 |d_A| product_(c in A) H_(c,k_c).             (2.1)

Proof: each chosen leaf set S partitions uniquely into S_c in the
disjoint child subtrees. Since M is separately affine in each child
argument, the exact chain rule has just the factor

    partial_S P_v = d_A product_(c in A) partial_(S_c) P_c.     (2.2)

For a fixed S there is no sum of competing chain-rule terms: differentiating
the same child argument twice at the outer level gives zero, while all its
leaf derivatives occur within that child. Taking absolute values in (2.2)
and summing over the unique child-set choices proves (2.1). This specific
disjoint-subtree fact is essential; an arbitrary arithmetic circuit with
shared variables need not admit the same absolute-mass recursion.

For fixed B,j the number of count vectors and local partials is constant.
Each d_A is computable from the fixed finite parent polynomial, or its
fixed-dimensional corner formula, at the known child base values.
Consequently all H arrays and base values cost C_(B,j)(1+G)n operations
and O_(B,j)(n) storage. This never computes an exponential list of leaf
coefficients. The full B-ary segment count is linear in n.

## 3. Exact subset generation and signed weight

If n<j or H=H_(root,j)=0, return the zero field without a v call. In the
latter case every c_S vanishes, so the conditional derivative is indeed
zero for every direction.

Otherwise at a node tasked with selecting k>0 leaves, choose a count
vector in (2.1) with probability equal to its nonnegative summand divided
by H_(v,k). Recurse into precisely the children with k_c>0, independently
using their corresponding conditional selection rules. At a leaf the
only positive task is k=1, which selects that leaf. Zero-mass alternatives
are never selected. A fixed finite list and one uniform draw implement
each categorical choice; endpoint conventions choose a positive-mass
interval and do not create retries or unknown acquisitions.

Induction and (2.2) show that the resulting j-element set has exactly

    p_*(S)=|c_S|/H.

The selected coefficient's sign is the product of the local d_A signs
along the selected recursion, with unit leaf sign. It can alternatively
be checked by the actual complete derivative formula. Its probability
is positive exactly when c_S is nonzero. Query the selected j leaf labels,
even when their spatial locations coincide, and return the scalar

    Z_* = j! H sign(c_S) product_(i in S) e_i.                 (3.1)

There is no ordered-tuple factorial missing: the j! in F_j already
accounts for all orderings. No random permutation is needed because
the repeated direction makes the product symmetric. Formula (3.1) is
unbiased for F_j, conditionally on the complete known preparation.
The subset generation visits at most all tree nodes and has linear cost.

The actual field is Z_* h_(kappa a)(.-U). The conditioning includes U,
Z,a and all base values; p_* is generally dependent on those quantities.
Conditional unbiasedness followed by the existing D44 identity gives
the same actual PDE derivative mean. One must not assert independence
between the new subset and the spatial preparation.

## 4. Precise minimax second-moment statement

Consider the restricted family of one-subset estimators

    Z_p=j! c_S product e_i / p(S),

where p is chosen from the known coefficients before seeing any e values
and p(S)>0 whenever c_S!=0. For any delta>=0,

    sup_(|e_i|<=delta) E_p Z_p^2
          =(j!)^2 delta^(2j) sum_(c_S!=0) c_S^2/p(S).         (4.1)

The bound is attained by the constant direction e_i=delta. Cauchy–Schwarz
and sum p<=1 imply sum c_S^2/p(S)>=H^2, with equality for p_*. Thus p_*
minimizes this conditional worst-case second moment in this specified
estimator family. It is not claimed to minimize variance, all estimators,
total runtime, or the unconditional PDE loss.

Relative to uniform subsets,

    H^2 <= L sum c_S^2,
    sup_e E Z_*^2 <= sup_e E Z_uniform^2.                    (4.2)

The inequality is strict for unequal absolute coefficients unless delta=0
or all coefficients vanish. This comparison is conditional and concerns
the full cube of direction values. A constant continuous direction attains
its envelope, so continuity does not obstruct that upper envelope.

Since |c_S|<=1, H<=L. Therefore the pathwise bound

    |Z_*| <= j! L ||e||inf^j = (n)_j ||e||inf^j

is the same as D44's bound. Its accepted cutoff-independent Hilbert
second-moment envelope remains valid, without a larger population power.
Hard queries remain at most j on every seed, preparation precedes them,
and almost-sure termination follows from the unchanged finite tree.
Expected full K-coefficient work remains C(1+G+K), with changed constants.

## 5. Why directionwise improvement is false

Take a single cubic parent M=(y1+y2+y3-y1y2y3)/2, j=1, and known leaf
values (9/10,9/10,0). Its first coefficients are (1/2,1/2,19/200),
so H=219/200. Choose direction values (0,0,delta). Uniform selection has
conditional second moment

    3(19/200)^2 delta^2 = 1083 delta^2/40000,

whereas p_* gives

    (219/200)(19/200) delta^2 = 4161 delta^2/40000.

Both means equal (19/200)delta, so the actual conditional variance is
also strictly larger for p_* in this example. Distinct leaf positions
permit continuous g and e with these values, ||g||inf<1 and arbitrarily
small delta. This disproves a universal directionwise claim; the correct
minimax-envelope statement in section 4 remains true.

## 6. A fixed mixture protects each conditional second moment

For a fixed 0<=eta<1, use p_eta=(1-eta)/L+eta p_*, when H>0.
Sample the component by a Bernoulli draw, then use either the uniform
subset rule or section 3. Compute the selected c_S before any v query,
using (2.2) or the existing corner formula, and use the actual mixture
probability in Z_p. A uniform draw with c_S=0 can return zero without a
v call. H=0 and n<j retain their zero guards.

For every fixed direction,

    E Z_(p_eta)^2 <= (1-eta)^(-1) E Z_uniform^2.              (6.1)

Convexity of reciprocal probabilities, followed by (4.2), also gives

    sup_e E Z_(p_eta)^2 <= sup_e E Z_uniform^2.               (6.2)

Indeed the worst-case coefficient sum is at most (1-eta)L sum c_S^2
+ eta H^2. Multiplication by the fixed conditional heat norm squared
preserves both bounds. This offers an explicit tradeoff without using
unknown-direction values to choose p. It is still a second-moment
statement; subtracting the common nonzero mean does not turn (6.1)
into the same multiplicative variance bound.

For fixed eta<1, |Z_(p_eta)|<=(1-eta)^(-1)(n)_j ||e||inf^j.
That is a safe pathwise envelope; the conditional worst-case comparison
in (6.2) separately implies the original D44 integrated second-moment
envelope. No post hoc choice of eta or numerical performance is asserted.

## 7. Attribution, verification level and next gate

Importance weighting and dynamic evaluation/differentiation of arithmetic
circuits are classical. A bounded search used exactly:

- `branching diffusion Monte Carlo variance reduction importance sampling automatic differentiation semilinear PDE Henry Labordere`
- `sampling subsets elementary symmetric polynomials dynamic programming weighted sampling without replacement exact`
- `Darwiche differential approach inference Bayesian networks derivatives polynomial 2003 pdf`

[Darwiche's primary paper](https://people.cs.pitt.edu/~milos/courses/cs3710/readings/differential-darwiche.pdf)
was inspected at the abstract/introduction and the opening descriptions
of network polynomials and their derivative semantics. It explicitly
connects polynomial circuit differentiation with efficient probabilistic
inference. Its full 20-page proof was not read; it is not cited as proving
this absolute-subset recursion for our PDE tree.

[Henry-Labordere et al.](https://arxiv.org/abs/1603.01727) was inspected
at the abstract/metadata only in this bounded check. Its automatic
differentiation concerns gradient-dependent branching representations
via Malliavin methods. That is not the initial-value leaf-subset derivative
used here. No proof from the unread full paper is imported in R25.
Secondary snippets and generic subset-sampling search hits were not
used as theorem evidence. No global novelty conclusion follows.

Root has derived the exact finite recursion, subset law, mean, cost,
minimax second-moment envelope, failure of directionwise dominance and
fixed-mixture inequalities above. An independent review must check these
before any claim is promoted. A separate formal contract and numerical
protocol would precede implementation. Frozen E4/E5, their samplers,
caps and raw evidence are unchanged.
