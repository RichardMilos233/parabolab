# Fixed05m: actual Hilbert sample means and profile-risk transfer

Date: 2026-09-29. Root mathematical contract. This is a finite statistical
gate for the all-diffusivity upper route, including the T87 refinement
candidate. It is valid independently of whether T87's PDE/Gaussian bridge
passes review. Theory precedes implementation; no experiment is specified
or run by this contract.

## 1. Exact objects

Let (Omega,mu) be an arbitrary probability space. Let H be a real Hilbert
space with its Borel measurable structure. Requiring a second-countable
topology is permitted: the intended real Sobolev spaces and every finite
Fourier coefficient space satisfy it. Use actual Bochner integrals and
actual square-norm losses, not a scalar variance variable defined to
satisfy the conclusion. All random variables below are in MemLp 2.

For n>=1 and Y_i:Omega->H, i in Fin n, define

    avg(Y)(omega)=(1/(n:Real)) smul sum_i Y_i(omega),
    mean_i=integral Y_i dmu.

Assume pairwise independence of the H-valued random variables. Do not
assume independence between coordinates of one H-valued sample, nor
between derivative-order batches in Section3. Do not require bounded
samples: tree outputs can be unbounded with finite second moment.

## 2. Required actual probability identities

Prove integrability of Y_i, centered Y_i, their square norms, and the
average's square-norm error from MemLp2. Prove the Bochner expectation of
the average is the average of means. Then prove

    integral ||avg(Y)-avg(mean)||^2 dmu
       = (1/n^2) sum_i integral ||Y_i-mean_i||^2 dmu,

and the individual identity

    integral ||Y_i-mean_i||^2 dmu
       = integral ||Y_i||^2 dmu-||mean_i||^2.

The common-mean corollary must use hypotheses integral Y_i=m for each i,
and conclude, if integral ||Y_i||^2<=V for each i,

    integral ||avg(Y)-m||^2 dmu<=V/n.

No identical-distribution assumption is necessary. V>=0 may be explicit;
n>0 must be explicit and division-by-zero behavior must not carry the
mathematical claim. The number of coordinates of H must not occur in
the estimate. A more general finite index set is welcome, not required.

### Conventional proof

On a probability space L2 is contained in L1. Products of norms of two
L2 variables are integrable by Cauchy--Schwarz, hence all inner products
in the finite expansion are integrable. Expand the centered square norm
as a double sum of real inner products. For i!=j, independence is
preserved by subtraction of deterministic means. The expectation of the
continuous bilinear inner product is the inner product of the two zero
means, hence zero. Diagonal terms give the first identity after dividing
by n^2. Expanding ||Y-m||^2 and integrating gives the second identity.
Discard the nonnegative ||m||^2 and sum n upper bounds V to get V/n.

## 3. Multiple derivative batches with their dependence retained

Let m be any natural number, j in Fin m, and for each j let Y_(j,i) be
a family as in Section2 with common mean h_j and second-moment bound V_j.
All batches may be on the same probability space; independence is needed
only between distinct i within each j. Let a_j be arbitrary real weights,
b,c in H, beta>=0, and suppose

    ||b+sum_j a_j smul h_j-c||<=beta.

Define the actual raw coefficient/field estimator

    raw(omega)=b+sum_j a_j smul avg(Y_j)(omega).

Prove its measurability as far as needed for the actual integrals, MemLp2
of raw-c, and

    integral ||raw-c||^2 dmu
      <=(m+1)*(beta^2+sum_j a_j^2*V_j/n).

This deliberately uses a fixed-order factor m+1. It does not multiply
by a Fourier cutoff or ambient coordinate dimension. Treat m=0 as a
valid deterministic-bias case. Allow a_j=0 and V_j=0.

### Conventional proof

Subtract c, writing the result as the deterministic bias plus m centered
batch errors. For any m+1 vectors z_j in H, the triangle inequality and
finite scalar Cauchy--Schwarz yield ||sum z_j||^2<=(m+1)sum||z_j||^2.
Integrate this pointwise inequality and apply Section2 to each batch.
No cancellation or independence between batches is used.

## 4. Actual projection and function-space transfer

First prove an anchored contraction corollary for any continuous K:H->H
such that ||K(z)-c||<=||z-c|| for every z. Derive MemLp2 of K(raw)-c
from this domination and measurability, and transfer the Section3 bound.
Do not assume the final integral bound as a premise.

Next implement an actual nontrivial instance: H=EuclideanSpace Real I
for a finite type I, and deterministic coordinate intervals l_i<=u_i.
Define

    box(z)_i=max(l_i,min(u_i,z_i)).

For c with l_i<=c_i<=u_i, prove coordinate anchoring, continuity, and

    ||box(z)-c||^2<=||z-c||^2,
    ||box(z)-c||<=||z-c||.

This is the real Hilbert coefficient representation after multiplying
each real Fourier coefficient by the square root of its positive Sobolev
weight. The corresponding intervals are scaled by the same factor;
the actual Fourier/Sobolev identification remains a conventional input.
No falsely independent Fourier coordinates are introduced.

Finally, for any real normed space G and bounded linear A:H->G, prove

    integral ||A(K(raw))-A(c)||^2 dmu
       <=||A||^2*(m+1)*(beta^2+sum_j a_j^2*V_j/n).

Derive integrability of this loss; do not rely on an integral returning
zero for a nonintegrable function. This statement applies to the sup norm
on continuous functions on a compact space by choosing G accordingly.
It controls a norm before expectation, rather than unrelated pointwise
risks. The norm bound of an actual reconstruction operator A still has
to be supplied outside this module.

### Conventional proof

Scalar clipping onto an interval containing c_i cannot increase distance
to c_i, as follows by the three cases z_i<l_i, l_i<=z_i<=u_i and z_i>u_i.
Sum squared coordinate inequalities for the Euclidean norm. The general
anchored statement follows by pointwise domination. Bounded linearity
gives ||A(K(raw))-A(c)||<=||A||*||K(raw)-c||; square and integrate.

## 5. Correspondence and exclusions

The intended raw field is a finite Taylor reconstruction with a_j=1/j!,
fixed m=ceil(1+d/(2s))-1, n=k^d, and deterministic bias including the
base-solve error and Taylor remainder. For T87, H is the real Sobolev
space or its finite weighted Fourier image. Candidate bounds V_j are
derived from the actual shared-Gaussian tree sampler, not postulated as
numerical observations. Section2 also applies before Fourier projection.

The contract does NOT formalize the random tree, Brownian covariance,
positive-semidefinite factorization, heat kernel, sampling-law equality,
finite leaf work, Sobolev/Fourier identification, S_1 differentiability,
Taylor remainder, coefficient clipping ranges for the actual PDE,
Gevrey saturation, final PDE continuation, solver accuracy, oracle counts,
the final minimax exponent, finite-bit execution, or novelty. These
omissions must be visible in the report and claimed-declaration inventory.

## 6. Implementation ownership and verification

Target new module: formal/EstimatorIntegrity/HilbertSamplingRisk.lean.
Target report:06o-hilbert-sampling-risk-lean.md.
Target evidence:lean/hilbert-sampling-risk/.
No edits to existing accepted modules, library entrypoint, lakefiles,
toolchain, dependencies, numerical artifacts or root claims/state files.

Pinned Lean4.33.0 and Mathlib db584cd6d46c92f209a44c0f1c829460d327499d.
Use /Users/michael/.elan/bin/lake from formal/. Read lean-proof and elan.
Develop incrementally; preserve failed diagnostics and label incomplete
scratch evidence honestly. No sorry/admit/additional axiom in accepted
exports. Run a fresh library module build with autoImplicit=false, a
direct source check, complete public-declaration #print types and #print
axioms checks. Capture stdout/stderr directly at execution into files
with command, cwd, exit code, timestamp and source hash; do not recreate
logs afterward. Preserve first failures, final success and manifest.
Only propext, Classical.choice and Quot.sound are expected foundations.

Useful inspected pinned APIs include IndepFun.integral_bilin in
Mathlib/Probability/Independence/Integration.lean and finite
sum_mul_sq_le_sq_mul_sq in Algebra/Order/BigOperators/Ring/Finset.lean.
Exact declaration/import names should be checked by the implementer.
Existing PositiveSampleMean.lean is read-only prior reference, but its
nonnegative bounded scalar assumptions are not the contract here.

If a statement is false or needs a material mathematical change, return
the obstacle to root. Do not silently assume covariance cancellation,
bounded samples, coordinate independence or the final risk inequality.
