# Fixed contract: actual uniform-slice conditioning and one revealed bit

Date: 2026-09-29. Research-owned conventional proof and Lean translation
contract. No implementation or build is claimed by this document.

This closes a concrete gap between the actual finite priors of D28/T82
and the accepted T62/T72 Bernoulli information modules. The target is an
actual uniform fixed-cardinality subset law, its normalized restriction
after some signs are observed, and the actual law of one further sign.
It is not enough to assume an urn probability formula or supply arbitrary
Bernoulli parameters. The statement does not yet formalize a complete
adaptive query program or its entire transcript.

## 1. Finite population and actual prior

Use a finite type alpha with decidable equality and its discrete sigma
algebra, or equivalently alpha=Fin K. Let U be a finite subset of alpha,
K=card U, and h a natural number with h<=K. Define

    Slice(U,h)={A subset U: card A=h},
    mu_(U,h)=uniform probability on Slice(U,h).

Use an actual PMF such as PMF.uniformOfFinset on U.powersetCard h and
its associated probability measure on Finset alpha. Prove the required
nonemptiness from h<=K; do not add nonemptiness as an unexplained extra
input. The probability of an individual member is 1/choose(K,h), and
is zero outside Slice(U,h).

Supply disjoint finite sets P,N contained in U. They represent revealed
positive and negative coordinates. Put

    j=card P+card N, z=card P, m=K-j, r=h-z,
    E={A: P subset A and A disjoint N}.

Assume the explicit feasibility conditions

    z<=h,  h<=K-card N.

They imply j<=K and 0<=r<=m. Define the compatible family

    C={A in Slice(U,h): P subset A and A disjoint N}.

The actual conditional probability measure is the normalized restriction

    mu_E = (mu_(U,h)(E))^(-1) * (mu_(U,h) restricted to E),

with scalar multiplication in the appropriate nonnegative scalar space.
The positive finite denominator must be proved. No arbitrary regular
conditional-distribution existence theorem is needed for this event.

## 2. Counting and conditional-law proof

Let R=U\(P union N). The map B -> P union B is a bijection from
Slice(R,r) to C. Its inverse is A -> A\P. Disjointness gives
card R=K-j=m and cardinality preservation gives card C=choose(m,r).
Consequently

    mu_(U,h)(E)=choose(m,r)/choose(K,h)>0,
    mu_E=uniform probability on C.

The second equality follows by evaluating each singleton: its restricted
mass is 1/choose(K,h) for compatible A and zero otherwise; normalization
turns the nonzero mass into 1/choose(m,r). Finite atomic extensionality
proves equality of the actual measures. This is an essential export.

The bijection can be implemented directly. Alternatively first identify
C with the h-element subsets of U\N that contain P, and use the pinned
Finset.filter_powersetCard_subset/card_filter_powersetCard_subset APIs.
Either route must prove equality with the event-filtered original slice,
not redefine the conditional law so the conclusion is automatic.

## 3. The actual next coordinate law, including endpoints

Take i in R; hence m>=1. Under the preceding conditional law, map
A to the Bool value of i in A. Prove that this actual measure pushforward
equals the existing bernoulliBool measure with parameter

    p=r/m in [0,1].

To derive it, compatible sets containing i correspond to the
(r-1)-element subsets of R\{i} when r>0. For r=0 there are none.
For 1<=r<=m the binomial identity

    m * choose(m-1,r-1) = r * choose(m,r)

gives probability r/m. The false mass is 1-r/m because this is a
probability law on Bool. Check r=0 and r=m explicitly; the resulting
laws are the deterministic false and true measures. This theorem must
retain these endpoints even though the later information comparison
uses interior parameters.

The formula is valid for every unrevealed coordinate i. Thus one may
instantiate it at any coordinate chosen from a fixed revealed P,N.
This fact alone is not a formal adaptive-history simulation theorem;
that additional correspondence remains outside the present contract.

## 4. Quantitative two-slice information corollary

For one common population U, supply integer counts h_minus<=h_plus<=K
with

    h_plus+h_minus=K,
    ell=h_plus-h_minus,
    K>0, 4ell<=K, 8j<=K.

The same P,N must be feasible under both counts. In fact the displayed
size assumptions imply this feasibility since h_minus>=3K/8 and
h_plus<=5K/8, while j<=K/8. Prove this implication and the positivity
of both conditioning events, rather than assuming their probabilities.

For any common unrevealed i, the preceding actual conditional
pushforwards are Bernoulli with parameters

    p_plus=(h_plus-z)/(K-j),
    p_minus=(h_minus-z)/(K-j).

The denominators are positive. All ratios here are real divisions of
cast natural counts; record every natural-subtraction side condition.
Direct inequalities give

    1/4<=p_minus<=4/7<3/4,
    p_plus-p_minus=ell/(K-j)<=2ell/K.

Both parameters lie in [0,1], and the reference parameter is strictly
interior. The existing actual Bernoulli chi-square bound from T62 now
gives an actual KL conclusion for these two conditional pushforwards:

    KL(next_plus || next_minus) <=64ell^2/(3K^2).

Use the existing Mathlib/project klDiv, state its finiteness, and make
the real/toReal conversion explicit as needed. An ENNReal bound is also
acceptable with the same constant and proved finiteness. Do not replace
this by a separately named scalar divergence unrelated to the measures.
Optionally derive <=256/(3K) under ell^2<=4K; that extra condition is
exactly the scale used in the lower proof, not a universal slice property.

The arithmetic proof is short: h_minus=(K-ell)/2>=3K/8;
h_minus-z>=K/4 and K-j<=K give the lower reference bound. The upper
uses h_minus<=K/2 and K-j>=7K/8. The same denominator gives the gap
bound, and p_minus(1-p_minus)>=3/16. No independence of successive
coordinates is asserted.

## 5. Deliverables and formal boundary

The implementation task owns only:

- formal/EstimatorIntegrity/UniformSliceConditioning.lean;
- 06n-uniform-slice-conditioning-lean.md in this run;
- lean/uniform-slice-conditioning/ in this run.

Do not edit existing modules, project entrypoint, toolchain, lakefiles,
Mathlib, frozen proofs, numerical artifacts, or root ledgers. Use the
pinned Lean4.33.0 and Mathlib db584cd6d46c92f209a44c0f1c829460d327499d.
Import accepted BernoulliInformation/FiniteConditionalInformation only
where useful. Read the Lean proof skill and check one proof step at a
time. New mathematical issues must return to the research role.

Require a fresh actual module build with the library options, complete
public signatures and #print axioms inventory, no reachable sorry/admit/
custom axiom/native-check trust, and source/log hashes. Capture new
successful and failed command stdout/stderr directly where possible;
label any retrospective summary or transcription accurately. Preserve
material failures and do not claim every scratch state was saved unless
it actually was. Give commands, cwd, exit codes and version provenance.

Outside this contract: full n-step path-law/chain composition, arbitrary
adaptive cell-selection and seed simulation, padding, random stopping,
MSE-to-testing, slice martingale concentration, PDE separation, the
minimax theorem, code runtime and numerical evidence. These exclusions
must remain visible even if this actual finite probability gate builds.

The pinned source reconnaissance found PMF.uniformOfFinset and its
singleton/set-mass formulas in Probability/Distributions/Uniform.lean,
the slice-cardinality/filter APIs in Data/Finset/Powerset.lean, and
Nat.add_one_mul_choose_eq in Data/Nat/Choose/Basic.lean. Their presence
is read-only API evidence, not proof that this proposed module compiles.
