# Fixed contract: actual finite-depth ternary kernel laws

Date: 2026-09-29. Research-owned conventional derivation and proposed Lean
translation contract. Implementation is not yet dispatched. T69 remains
under independent T73 review when this contract is written. This file
does not accept T69, assume the desired moment recurrence, or certify a
full infinite-tree sampler.

The intended formal bridge is T69 Sections 3–4: independent children
conditional on their common state, importance weights, and the tilted
second moment. Formalize the actual finite-depth probability kernels,
not only a scalar sequence assumed to obey the recurrence.

## Objects and algorithm

Let S be a measurable space. Supply two Markov kernels:

    leaf : S -> probability measures on R,
    branch : S -> probability measures on R x S.

The source coefficient l and the branch coefficient omega may have any
real sign. In the branch kernel, omega may be correlated with the next
state r. The three children start at the SAME r, and are independent
conditional on (omega,r). No independence of omega and r is assumed.

Fix p=1/6 and q=5/6. The output space is R x N, with pair (c,n) denoting
the product coefficient and completed-leaf count. Define actual kernels
K_D : S -> probability measures on R x N recursively:

* K_0(s) is the point mass at (0,0).
* With probability q, draw l from leaf(s) and output (l/q,1).
* With probability p, draw (omega,r) from branch(s), then three
  conditionally independent pairs (c_i,n_i) from K_D(r), and output
  ((omega/p)c_1 c_2 c_3, n_1+n_2+n_3).

The last two clauses define K_(D+1). Use actual kernel products,
composition, maps, and the probability mixture. Prove measurability and
the Markov-kernel instance for every D. Do not assume this law exists
or replace its integral by a separately defined recurrence.

The zero base coefficient kills trees reaching the depth cutoff. Its
count need not equal the count of an ungenerated infinite continuation;
all weighted coefficient expressions on those killed outcomes are zero.
No equality of full and truncated joint laws is claimed.

## Weighted second moment and conventional proof

For a>0 and z>0, define the measurable nonnegative weight

    W_(a,z)(c,n)=c^2 a^(2n) z^n.

Let F_D(s) be its actual nonnegative integral against K_D(s). Work with
ENNReal lintegrals first, so no integrability assumption is hidden.
Tonelli, the actual product law of the children, and the identities
for powers give the exact extended-nonnegative recurrence

    F_(D+1)(s)
      = (a^2 z/q) integral l^2 d leaf(s)
        + (1/p) integral omega^2 F_D(r)^3 d branch(s).

The expression is interpreted in ENNReal with nonnegative real constants
embedded by ofReal. In particular, it must be DERIVED from K_D. The
factor in front of each integral is 1/q or 1/p after the corresponding
mixture probability cancels one squared importance denominator.

Suppose M>0, C>=0, R>0, and uniformly in s,

    integral l^2 d leaf(s) <= M^2,
    integral omega^2 d branch(s) <= C^2,
    C R^2 <= 1/8.

The first two are actual lintegral bounds, not names for scalar proxies.
Set a=3R/(4M), z=5/4. If F_D(r)<=R^2 at every r, positivity gives

    F_(D+1)(s) <= M^2 a^2 z/q + C^2 R^6/p
                 <= (27/32)R^2+(3/32)R^2
                 = (15/16)R^2 <= R^2.

The coefficient/state correlation is harmless because F_D(r) is bounded
uniformly BEFORE integrating omega^2. F_0=0. Induction therefore proves
the actual uniform bound for every D,s, and in particular its finiteness.
The same constants yield squared-majorant slope

    3(C^2/p)(R^2)^2 <= 9/32.

This algebraic corollary is useful but does not replace the kernel proof.

## Every fixed polynomial leaf factor

For each j in N, let

    A_j = sum_(n=0)^infinity n^(2j) (4/5)^n.

The series is summable and nonnegative. Hence each term is at most A_j,
which gives n^(2j) <= A_j (5/4)^n. Apply this POINTWISE to the actual
outcomes of K_D, multiply by c^2 a^(2n), and integrate to prove

    integral n^(2j) c^2 a^(2n) d K_D(s) <= A_j R^2

uniformly in D,s. All integrals and conclusions should be actual
ENNReal/real moment statements with finiteness established. A theorem
with a general nonnegative A satisfying the pointwise domination is a
useful intermediate export; the existence of the finite A_j above must
also be proved, not left as a premise.

This A_j is a deliberately larger constant than T69's supremum-based
choice. Record that difference explicitly. Both give the same fixed-order
finiteness statement; this module does not certify T69's sharper explicit
maximum formula unless that separate calculation is also proved.

## Local Mathlib reconnaissance

The pinned repository contains Kernel.prod, lintegral_prod, Markov-kernel
product instances, kernel composition/map/comap, and compProd APIs.
`Mathlib/Analysis/SpecificLimits/Normed.lean` contains
`summable_pow_mul_geometric_of_norm_lt_one`. These sources were inspected
read-only. Their suitability must be checked in Lean; no successful build
of this contract is implied by listing an API.

## Deliverables and acceptance boundary

When dispatched, the worker owns only a new module
`formal/EstimatorIntegrity/FiniteTreeSecondMoment.lean`, a new report
`06m-finite-tree-second-moment-lean.md`, and a new evidence directory
`lean/finite-tree-second-moment/` within this run. Do not edit the project
entrypoint, toolchain, lake files, dependencies, earlier modules, frozen
proofs, or root ledgers. Use Lean 4.33.0 and pinned Mathlib
db584cd6d46c92f209a44c0f1c829460d327499d.

Retain failed attempts and commands. Require a fresh module build, an
inventory and `#print axioms` for every claimed public theorem, no
reachable sorry/admit/custom axiom/native-check trust, source and log
hashes, and exact correspondence of definitions and quantifiers. Ordinary
Lean/Mathlib classical axioms are allowed. Follow the Lean proof skill's
incremental checking workflow. New mathematical obstacles return to the
research role; do not restrict the state space or alter the law silently.

Outside this contract: the infinite genealogical coupling, almost-sure
halting and expected node count; the concrete heat/time kernels and their
primitive costs; graph/PDE identification; derivative label-map sampling;
inner burn-in batches; query caps; final Taylor risk and work theorem;
finite-bit implementation; and numerical performance. A successful module
will be partial coverage of the actual moment mechanism, not a certificate
for the complete T69 sampler or the signed long-time algorithm.
