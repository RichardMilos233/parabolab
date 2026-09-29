# Signed-information formalization: first actual probability gate

Status: fixed root contract after T60 API reconnaissance. This is a new
formalization target, not a certificate. It preserves D25's conventional
proof and constants. The first bounded implementation task is T62 below;
later urn/adaptive/chain-rule gates are not authorized by implication.

## T62: actual Bernoulli KL and binary testing

Own new `formal/EstimatorIntegrity/BernoulliInformation.lean`, new
`06k-bernoulli-information-lean.md`, and new attempt/build/axiom evidence
under `lean/bernoulli-information/`. Import the pinned Mathlib directly.
Do not modify entrypoints, toolchain, lakefiles, accepted formal modules,
protected original files, or frozen research reviews.

Use actual `ProbabilityTheory.bernoulliMeasure` on Bool and actual
`InformationTheory.klDiv`, or a definition proved equal to these objects.
A real scalar called KL with no measure bridge is insufficient. State
all probability and finite-divergence assumptions explicitly; take care
with ENNReal infinity and `toReal`. Probability p of true means the
measure of {true} is p. Verify the argument order of the library's Ber
notation; do not assume it.

Required exports, with equivalent precise statements/names permitted:

1. Bernoulli KL formula: for 0<=p<=1 and 0<q<1, the actual divergence
   is finite and its real value is
   p*log(p/q)+(1-p)*log((1-p)/(1-q)). The 0*log0 endpoint convention is
   the library's actual real arithmetic, with the relevant limits proved.
2. Upper bound: that actual real divergence is at most
   (p-q)^2/(q*(1-q)), obtained from the real logarithm inequality. Include
   p=0 and p=1; q remains strictly interior.
3. Binary Pinsker: for 0<=p,q<=1 and finite actual divergence,
   2*(p-q)^2 <= (klDiv Ber_p Ber_q).toReal. The q=0 or q=1 cases must
   follow from actual absolute continuity/finiteness, not be omitted.
4. Actual binary testing corollary: when the true-label probabilities
   under the positive and negative hypotheses are p and q, and actual
   KL <= ENNReal.ofReal(1/12), prove equal-prior error
   ((1-p)+q)/2 >= 3/8. Preserve the direction of each hypothesis. This
   last arithmetic is useful only together with the preceding measure
   theorems; assuming Pinsker or a testing inequality does not pass.

A conventional proof route is as follows. For fixed interior q, the
Bernoulli divergence D_q(p) has derivative
log(p/q)-log((1-p)/(1-q)) and second derivative
1/p+1/(1-p)=1/[p(1-p)]>=4 on (0,1). Since D_q(q)=D_q'(q)=0,
D_q(p)>=2(p-q)^2; continuity handles p endpoints. For q endpoints,
finiteness forces equality of the Bernoulli laws. The upper bound uses
log x<=x-1 in the interior followed by continuity. Equivalent sound
convexity/relative-entropy proofs are allowed. None of these steps is a
new research hypothesis or an axiom to be introduced.

Build the new module with Lean4.33.0/Mathlib at the existing pinned SHA.
Keep every failed attempt log, one final successful module build, and
`#print axioms` for every exported theorem. Only standard Lean axioms are
allowed; no sorry/admit/custom axioms or opaque proof obligations.
Describe each theorem's exact coverage and give source/evidence hashes.
Root must read the source and compare it with this contract before PASS.

## Remaining gates, explicitly outside T62

The real D25 information argument still requires actual fixed-weight
uniform priors, adaptive fresh-cell exchangeability, padded observation
laws, common seed/transcript postprocessing, a finite conditional-KL
average or bound and its accumulation, MSE-to-label conversion, random
stopping/truncated execution agreement with Markov, and finite-prior
averaging. T60 maps these obligations as G1--G11. Passing T62 alone
formalizes only the Bernoulli and binary-testing ingredients. It does not
formalize D25/D27, the PDE phase coordinate, or an arbitrary randomized
point-query algorithm, and it does not authorize signed numerical work.
