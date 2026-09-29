# R21: linear-work extraction of a common Gaussian on a finite tree

Date: 2026-09-29. Root conventional candidate, pending independent
review. This is a replacement implementation of the Gaussian preparation
in T87/R20, not an alteration of their frozen proofs. No Lean or code
has been written for this candidate and no experiment has been run.

The purpose is to replace a dense n-by-n covariance factorization,
costing O(n^3), by a fixed number of tree traversals costing O_d(n).
It also integrates the largest admissible common Gaussian variance
for each finite genealogy, rather than the universal lower bound
tau/n. The inverse-variance tree recursion is classical; its use in
this particular nonlinear derivative sampler still needs review.

## 1. Finite deterministic tree and Gaussian variables

Consider a finite rooted tree of lifetime segments. Each segment v
has a nonnegative length ell_v. A leaf segment ends at the terminal
time; an internal segment has a nonempty finite list of child segments.
For the stated O(n) cost suppose every internal segment has at least
two children, as in T87/R20. All root-to-leaf lengths equal tau>0.
There are n terminal leaves and at most 2n-1 segments.

For one physical coordinate, draw independent centered Gaussians
Y_v with variance ell_v, taking Y_v=0 when ell_v=0. The leaf variables
X_i are the sums of Y_v on their root paths. Write their covariance
matrix as C; hence C_ii=tau. Scaling all Y_v by sqrt(kappa) later
gives the actual diffusion convention. All arguments below are
conditional on the fixed genealogy; no input values enter them.

## 2. Recursion with all zero cases defined

For each segment compute a scalar a_v and a Gaussian aggregate A_v
from its subtree, starting at leaves. At a leaf,

    a_v=ell_v,                 A_v=Y_v.

At an internal segment, its children have already supplied a_c>=0
and A_c. Define h_v and weights alpha_c as follows.

- If every a_c>0, let h_v=(sum_c 1/a_c)^(-1) and alpha_c=h_v/a_c.
- If at least one a_c=0, choose the first such child in the fixed
  stored ordering, put h_v=0, its weight equal to one, and every
  other weight equal to zero.

Then set

    a_v=ell_v+h_v,         A_v=Y_v+sum_c alpha_c A_c. (2.1)

All divisions occur only with strictly positive denominators. In
both cases the finite algebraic identities are

    alpha_c>=0, sum_c alpha_c=1,
    alpha_c a_c=h_v for every c,
    sum_c alpha_c^2 a_c=h_v.                         (2.2)

They include multiple zero children. Thus the rule is a total Borel
finite procedure on nonnegative lengths, without an inverse matrix
or numerical regularization. Every deterministic arithmetic operation,
comparison and array access is charged in the same ideal model.

## 3. Covariance induction

Let X_(v,i) be the sum of Gaussian edge variables along the path
from the beginning of segment v to one of its terminal descendants.
We claim

    Var(A_v)=a_v,
    Cov(X_(v,i),A_v)=a_v for every descendant i.       (3.1)

For a leaf this is immediate. At an internal segment, disjoint child
subtrees and Y_v are independent. The variance is
ell_v+sum_c alpha_c^2 a_c=ell_v+h_v. For a leaf below child c,
its covariance with A_v is ell_v+alpha_c a_c=ell_v+h_v.
These equalities use (2.2) and remain valid when some child has
zero variance. A centered Gaussian with zero variance is the zero
variable almost surely; the algebraic construction is also zero
there because all contributing positive-variance weights vanish.

In addition A_v is a convex linear combination of the X_(v,i).
This is true at a leaf. For the induction, distribute alpha_c times
the child's convex combination; the weights sum to one, so the
shared Y_v is counted exactly once. The root therefore provides
known deterministic weights w_i>=0 with sum_i w_i=1 and

    A=sum_i w_i X_i,   Var(A)=a,   C w=a 1.          (3.2)

These weights need not be expanded or stored by the algorithm:
the aggregate A is evaluated by the recursion itself.

Let Z_i=X_i-A. Joint Gaussianity and (3.1) give

    Cov(Z_i,A)=0,
    Cov(Z_i,Z_j)=C_ij-a,
    X_i=A+Z_i.                                      (3.3)

Consequently the entire residual vector Z is independent of A,
not merely each coordinate separately. This remains true for
degenerate Gaussian vectors by their characteristic functions.
The construction directly samples the desired residual vector:
generate ordinary independent edge Gaussians, compute A, and
subtract it from each terminal path sum. No conditioning rejection,
conditional-density oracle, matrix square root, or extra random
common shift is required.

## 4. The extracted variance is positive and optimal

The deterministic partition inequality from T87, valid at any
finite genealogy of common height tau, gives

    C >= (tau/n)11^t.

Apply this quadratic inequality to w in (3.2). Since sum_i w_i=1,

    a=w^t Cw >= tau/n>0.                            (4.1)

Also every C_ij lies in [0,tau] and the w_i are nonnegative, giving
a<=tau. Alternatively Cauchy--Schwarz and Cov(X_i,A)=a yield this
upper bound once a>0.

The covariance in (3.3) proves C-a11^t is positive semidefinite.
If any b has C-b11^t positive semidefinite, testing against w gives
0<=a-b. Thus a is the largest removable common Gaussian variance.
No invertibility of C is needed. If C happens to be invertible,
(3.2) also yields a=(1^t C^(-1)1)^(-1), but the algorithm does not
compute that inverse. This optimality concerns scalar common
Gaussian extraction for a fixed tree, not global estimator variance
or optimal running time.

## 5. The actual nonlinear field sampler

Perform the construction independently in each of d physical
coordinates and scale by sqrt(kappa). The common d-vector G has
covariance kappa a I_d and is independent of the full residual array
Z. The original Brownian leaf positions have exactly the law

    x+G+Z_i,        i=1,...,n.

For any bounded continuous function F of these n leaf arguments,
conditionally on the tree and residual array,

    E_G F(x+G+Z_1,...,x+G+Z_n)
      =integral_X h_(kappa a)(x-u) F(u+Z_1,...,u+Z_n) du. (5.1)

This is ordinary Gaussian convolution of the complete translated
function. It applies in particular to the tree polynomial and its
selected ordered leaf partials. With independent uniform U, the
corresponding derivative sample is

    W_j=h_(kappa a)(.-U) (n)_j C_I
                         product_(b=1)^j e(U+Z_(I_b)). (5.2)

All nonlinear known-leaf values, selected coefficients, and residual
values are evaluated at the same translated array U+Z. The rule
differs from T87 in both the Gaussian preparation and the heat
variance; both must be changed together. Averaging the whole law
still gives the identical actual PDE derivative.

Because a>=tau/n, every Fourier heat multiplier has magnitude at
most the multiplier used in T87/R20. In particular

    ||h_(kappa a)||_r^2
       <=||h_(kappa tau/n)||_r^2<=C_h n^(r+d).

The previous cutoff-independent derivative and second-moment bounds
therefore survive unchanged. This monotonicity bounds the heat norm;
it does not assert that the complete estimator variance is smaller,
since the residual sampling law and scalar coefficient also change.

For a requested finite cutoff, replace the old Fourier factor by
exp(-2pi^2 kappa a |nu|^2). The same real cosine/sine formulas,
Hilbert averaging, clipping and j-query cap remain valid. No full
heat kernel is evaluated. Conditional expectation uses the actual
independence from (3.3), not a falsely independent coordinate model.

## 6. Paid work and simple exact examples

One postorder pass computes a_v and alpha_c; a Gaussian draw per
nonzero segment and a preorder pass give the leaf path sums; another
postorder pass computes A. Subtracting the root aggregate costs
O_d(n). The total number of child entries is the number of segments
minus one, so all passes together have O_d(n) work and storage.
The genealogy generation, tuple selection and known-leaf polynomial
passes are already linear for fixed arity and fixed j.

Thus the previous conditional sample-cost bound improves to

    Work(sample)<=C_(B,j,d)[(1+G)n+(2N+1)^d].        (6.1)

Only the first population moment is needed for preparation work.
Higher moments are still needed for the field's derivative variance;
this does not remove their large constants or prove practical speed.
No finite-bit stability claim follows from ideal positive divisions.

For one leaf, a=tau, A=X_1, and Z_1=0. For a star with ancestral
segment length b and n equal terminal segments tau-b, the formula
is a=b+(tau-b)/n and A is the leaf average. For b=tau all terminal
segments are zero; the zero-child branch gives a=tau and all Z_i=0.
For b=0 it gives a=tau/n and recovers the universal bound sharply.
These are exact algebraic checks, not numerical executions.

## 7. Attribution, evidence and next gate

The inverse-variance recursion has substantial prior art. The original
[Felsenstein paper](https://ichthyology.usm.edu/courses/multivariate/Felsenstein_1985.pdf)
was read at printed pages8--10, especially page10's inverse-variance
tip aggregation and branch-length update. Its 1985 construction also
allows multifurcations through zero branches. The use of Brownian
tree covariance and this recursion cannot be claimed as new here.
A screenshot was requested for page10; no additional visual QA is
claimed beyond the returned text inspection. The publisher abstract
was also retrieved at DOI10.1086/284325.

An Oxford primary search result for "Maximum Likelihood Estimation
for Linear Gaussian Covariance Models" gave the descendant-indicator
covariance formula. Full opening failed with an inaccessible redirected
page; no further theorem from that paper is used. Search queries were
"Brownian motion phylogenetic tree ancestral mean independent contrasts
variance harmonic sum Felsenstein 1985" and "Gaussian tree root
estimation effective resistance variance Brownian covariance leaf
weighted average". Other effective-resistance results were not used.

The proof above is a direct deterministic/probabilistic derivation
for the exact sampler contract. It is not an exhaustive priority
search. Independent review must check the zero branches, full-vector
Gaussian independence, covariance optimality, changed nonlinear law,
and O(n) counted traversal construction before any promotion.
T87 and R20 remain frozen; this note does not change their accepted
or candidate status. No unknown-input call, Lean run, numerical
experiment, implementation, or complete long-time work improvement
is reported here.
