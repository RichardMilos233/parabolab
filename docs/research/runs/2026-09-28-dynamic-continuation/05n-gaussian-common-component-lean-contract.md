# Fixed05n: actual Gaussian common-component law

Date: 2026-09-29. Root mathematical contract and conventional proof.
This is a fixed finite-dimensional probability gate motivated by R21.
Its statements are valid independently of the tree-recursion audit.
No implementation, build, or numerical experiment is claimed here.

## 1. Exact finite probability objects

Let (Omega,mu) be an arbitrary probability space, I a finite nonempty
index type, and X:Omega -> (I -> Real) an actually jointly Gaussian
random vector, expressed by Mathlib HasGaussianLaw X mu. Each
coordinate has actual Bochner mean zero. Do not replace joint
Gaussianity by only marginal Gaussianity or pairwise independence.

Define the actual covariance matrix from the random vector:

    C(i,j)=covariance (fun omega => X omega i)
                       (fun omega => X omega j) mu.

Let w:I->Real and a:Real obey

    sum_i w_i=1,
    for every i, sum_j w_j C(i,j)=a.                 (1.1)

The w_i need not be nonnegative for this probability theorem. Define
actual random variables

    A(omega)=sum_i w_i X(omega,i),
    Z(omega,i)=X(omega,i)-A(omega).

All means, variances and covariances below must refer to these actual
functions and mu. Derive their measurability/integrability/MemLp2 from
joint Gaussianity; do not add final covariance or independence results
as premises. Degenerate Gaussian laws and a=0 must be retained.

## 2. Required common-component statements

Prove:

1. A and Z, and their paired vector (Z,A), are jointly Gaussian;
   A and every Z_i have mean zero.
2. covariance(X_i,A)=a for all i, variance(A)=a, and a>=0.
3. covariance(Z_i,A)=0 and covariance(Z_i,Z_j)=C(i,j)-a.
4. IndepFun Z A mu for the ENTIRE vector Z. Coordinatewise
   independence alone is insufficient.
5. The actual scalar law mu.map A equals gaussianReal 0 a.toNNReal.
   GaussianReal's variance parameter is NNReal, not ENNReal.
6. The joint pushforward is the product measure

       mu.map (fun omega => (Z omega,A omega))
                    = (mu.map Z).prod (gaussianReal 0 a.toNNReal).

7. With addCommon(z,t)(i)=z(i)+t, prove the exact law identity

       mu.map X
        = ((mu.map Z).prod (gaussianReal 0 a.toNNReal)).map addCommon.

8. For any bounded continuous real function F on I->Real, derive
   the corresponding actual expectation identity over that product
   measure. Prove integrability rather than exploiting totalized
   integrals of nonintegrable functions. An iterated integral is a
   welcome corollary, but the product-law identity is mandatory.

### Conventional proof

Finite continuous linear maps preserve Gaussian laws. All Gaussian
coordinates and finite linear combinations are in L2. Covariance
bilinearity gives Cov(X_i,A)=sum_j w_j C(i,j)=a. Then
Var(A)=sum_i w_i Cov(X_i,A)=a. Nonnegativity of variance proves a>=0.
Expanding covariance after subtraction gives statements3. Joint
Gaussianity plus zero cross-covariances yields independence of the
whole finite vector Z and A, including singular laws. The scalar
Gaussian mean/variance characterization and independence give the
product pushforward. The pointwise identity addCommon(Z,A)=X and
pushforward composition give statement7. Bounded-continuous
integrability on probability measures and integral_map give8.

## 3. Required explicit independent-edge construction

To connect the gate to a finite Gaussian program, let E be another
finite type and Y_e:Omega->Real an independent family of centered
Gaussian variables with actual variances ell_e>=0. Zero ell_e are
allowed. Let L:I->E->Real be a supplied real coefficient array.
Define, rather than postulate, the leaf vector

    X(omega,i)=sum_e L(i,e) Y_e(omega).

Prove joint Gaussianity, its zero coordinate means, and the exact
actual covariance formula

    C(i,j)=sum_e ell_e L(i,e)L(j,e).                 (3.1)

Independence must be of the family of complete scalar edge variables;
derive vanishing off-diagonal covariance from it. Then instantiate
Section2 under the explicit coefficient condition

    sum_i w_i=1,
    for every i,
      sum_e ell_e L(i,e) (sum_j w_j L(j,e))=a.       (3.2)

This gives an actual independent-edge-to-residual product-law theorem,
not merely a covariance matrix assumed to come from a Gaussian law.
The edge family can be on any probability space with the displayed
laws/independence; constructing a particular product sample space is
optional because this theorem already quantifies over real variables.

### Conventional proof

An independent finite family of Gaussian variables is jointly
Gaussian. The finite linear map L supplies X. Expand its covariance
as a double edge sum, use independence for distinct edges, and
variance ell_e on the diagonal. Interchange finite sums to see that
(3.2) is exactly (1.1), and apply the actual product-law theorem.

## 4. Deterministic certificate and precise omissions

The intended leaf coefficient L(i,e) is the indicator that edge e
lies on the path to leaf i, and ell_e is kappa times that edge's
length. R21's known inverse-variance tree recursion constructs w
and a satisfying (3.2) with a>=kappa*tau/n. Those tree-recursion,
partition and lower-variance assertions are NOT assumptions silently
discharged by this module. They remain conventional separate bridges.

This module does NOT formalize the tree datatype/recursion, clocks,
nonexplosion, cost of generating the edge family, torus wrapping,
heat convolution, polynomial voting, derivatives, Sobolev norm,
Hilbert sample averaging, PDE identity, final solver, queries, whole
long-time complexity, bit precision or numerical performance. These
exclusions must appear in the report and public declaration inventory.

The purpose is to certify actual joint Gaussian independence and
the precise reconstruction law, including degeneracies. Do not
substitute a purely matrix inequality or assume IndepFun Z A.

## 5. Implementation and evidence contract

Own only a new formal/EstimatorIntegrity/GaussianCommonComponent.lean,
run/06p-gaussian-common-component-lean.md, and
run/lean/gaussian-common-component/. No edits to existing modules,
entrypoint, Lake configuration, toolchain, dependencies, root ledgers,
frozen proofs or numerical artifacts. Read lean-proof and elan.

Pin Lean4.33.0 and Mathlib db584cd6d46c92f209a44c0f1c829460d327499d.
Use /Users/michael/.elan/bin/lake from formal/. Preserve incremental
failure diagnostics honestly; capture all new build and audit process
stdout/stderr directly with command, cwd, timestamp, exit, and source
hash. Require a fresh actual library build, direct source check with
autoImplicit=false, all public signatures and #print axioms inventory,
no sorry/admit/custom axiom/native-check trust, and hash manifest.
Only ordinary propext/Classical.choice/Quot.sound foundations expected.
The proof strategy is fixed above; return mathematical defects rather
than weakening the statement.

Pinned APIs inspected read-only include HasGaussianLaw.map,
HasGaussianLaw.map_eq_gaussianReal,
HasGaussianLaw.indepFun_of_covariance_eval (a finite singleton index
for A may help), iIndepFun.hasGaussianLaw, and covariance finite-sum
and scalar-multiplication lemmas in Probability/Moments/Covariance.
Their availability is source reconnaissance, not successful formal
implementation evidence. No coding worker has been dispatched by
this document itself.
