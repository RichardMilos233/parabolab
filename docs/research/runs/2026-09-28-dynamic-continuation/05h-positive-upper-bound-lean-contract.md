# Fixed Lean contract: positive-class sampling upper bound

Theory prerequisite: D24/04q and frozen T46, independently audited in T48.
Do not start a numerical implementation of the new PDE approximation before
these formal gates. Protocol02e is a separate already-authorized check of
the older lower-bound information core, not numerical evidence for D24.

Use the current project pin, Lean4.33.0, without changing existing sources,
entrypoints, lakefile, toolchain or manifests. Each worker owns only its new
module, report and dedicated logs. Do not weaken targets into algebra that
assumes the desired variance or final risk inequality. Preserve failed
attempts; verify a fresh module build and all authored exported axioms.

## T51: actual scalar transform and integral loss bound

Ownership: formal/EstimatorIntegrity/PositiveSigmoidRisk.lean,
06i-positive-sigmoid-lean.md and lean/positive-sigmoid/.

Define Psi(z)=z/Real.sqrt(1+z^2) as a real function. Prove from this definition
that it is continuous, and for nonnegative x,z has range [0,1] and obeys

    |Psi(x)-Psi(z)|<=|x-z|/sqrt(1+z^2).

The proof must establish the anchored inequality for every x,z>=0, including
zero. Do not take monotonicity, concavity, or this inequality as a premise.
One elementary route proves monotonicity by comparing squares of positive
ratios, then uses denominator ordering in each x<=z or z<=x case. A
derivative-based proof is also acceptable if actually formalized.

On an arbitrary probability space, for a measurable nonnegative real random
variable X with integrable squared deviation from a nonnegative constant z,
derive the actual integral inequality

    integral (Psi(X)-Psi(z))^2
       <= integral (X-z)^2 / (1+z^2).

Prove integrability of the transformed loss using continuity/range and the
probability normalization, rather than assuming the final inequality.
Pointwise nonnegativity hypotheses are acceptable; no finite seed space
or bounded X assumption is allowed for this general transform theorem.

Finally derive an exact bias-composition result on the same probability
space: for a real target y with |y-Psi(z)|<=1/32 and actual transformed
MSE<=1/64, prove

    integral (Psi(X)-y)^2 <=25/1024.

Use the actual integral/Cauchy–Schwarz or L2 triangle inequality. Do not
assume an RMS triangle bound as an input. The report must distinguish this
analytic/probabilistic result from any PDE approximation certificate.

## T52: bounded independent samples and the full risk certificate

Ownership: formal/EstimatorIntegrity/PositiveSampleMean.lean,
06j-positive-sample-mean-lean.md and lean/positive-sample-mean/.
Work may begin on the independent sample-mean lemma while T51 is in
progress. Import T51 only after its verified source is frozen; do not edit
that module. Root will explicitly dispatch this second worker.

Let (Omega,mu) be an arbitrary probability space, n a positive natural,
and Y_i:Omega->Real, i:Fin n, measurable pairwise independent random
variables. Assume pointwise 0<=Y_i<=A, A>=0, and actual integrals
integral Y_i=m for every i, with m>=0. Define mhat=(sum_i Y_i)/n.
From these data derive integrability, unbiasedness of mhat, and

    integral (mhat-m)^2 <= A*m/n.

Crucially, the pairwise product-integral identity must follow from actual
IndepFun hypotheses. Do not replace independence by an assumed covariance
sum, supplied sample variance bound, or finite discrete probability model.
The upper theorem needs only pairwise independence; iid point samples
supply it conventionally. The scalar range bounds should supply the needed
L2 and product integrability on a probability space.

After the sample lemma and T51 have passed, prove the combined actual risk
certificate. In addition to those sample hypotheses assume

    0<beta<1, C>=1, T>=0,
    A<=C*m^beta,
    (n:Real)>=64*C*exp((1-beta)*T),
    |y-Psi(exp(T)*m)|<=1/32.

Use Real.rpow for real powers, handling m=0 explicitly. Derive

    integral (Psi(exp(T)*mhat)-Psi(exp(T)*m))^2 <=1/64,
    integral (Psi(exp(T)*mhat)-y)^2 <=25/1024 <1/16.

The power identity and the bound z^(1+beta)/(1+z^2)<=1 must be proved,
not added as hypotheses. A supporting ceiling-budget lemma may be added,
but cannot substitute for the independent-sample and transformed-risk
theorems. No new numerical experiment is authorized by this contract.

## Correspondence boundary and verification

The integral of v, height-versus-mass interpolation, heat kernel,
nonlinear PDE comparison, and their uniform bias <=1/32 remain conventional
inputs from04q/T46/T48. The new formal certificate must identify those inputs
explicitly. It must not claim the whole PDE theorem is proved in Lean.
Likewise, the iid uniform-oracle implementation and bit arithmetic are not
formalized merely by a theorem about independent real random variables.

For each module save actual Lean/Mathlib versions, source SHA256, fresh
build command/log, complete #print axioms output for authored exports, a
clean sorry/admit/custom-axiom scan, and the failed-attempt history. Only
standard Mathlib axioms are acceptable. Root will read the encoded
definitions, quantifiers and hypotheses against this fixed contract before
accepting a gate or advancing this new algorithm to code.
