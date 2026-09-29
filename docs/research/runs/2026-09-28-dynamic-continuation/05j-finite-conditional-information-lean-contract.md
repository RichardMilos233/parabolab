# T72: finite conditional information and actual binary postprocessing

Status: fixed root mathematical contract after accepted T62. This is the
next bounded formal gate, not a certificate for the full signed lower bound.
The conventional derivation below precedes implementation. It fills the
finite-history conditional-KL averaging step identified as G6 by T60 and
connects actual observation measures to T62's binary testing theorem.

## Owned files and unchanged dependencies

Own only new `formal/EstimatorIntegrity/FiniteConditionalInformation.lean`,
new `06l-finite-conditional-information-lean.md`, and new evidence under
`lean/finite-conditional-information/`. Import the frozen accepted T62
module and pinned Mathlib. Preserve entrypoints, lakefiles, toolchain,
all accepted formal sources and research evidence. No code experiment,
oracle acquisition or change to the PDE claim is part of this task.

## Actual objects

Let `H` be a finite type with measurable singleton sets, and let `mu,nu`
be actual probability measures on `H`. For functions `p,q:H->[0,1]`,
let `Kp,Kq` be the actual Markov kernels whose values at `h` are
`EstimatorIntegrity.bernoulliBool (p h)` and its `q` counterpart.
Either use a direct definition or prove the chosen kernels equal to
these measures. In this gate assume `0<q h<1` for every `h`; `p h` may
be an endpoint. Zero-mass history atoms under `mu` or `nu` are allowed.

The product `mu tensor_m Kp` is the actual joint law of the retained
history and one new Bool answer. It is not a scalar named entropy or
an assumed expression for a path law.

## Required exports

1. Conditional averaging identity and finiteness:

       klDiv(mu tensor_m Kp)(mu tensor_m Kq) != infinity,
       (klDiv(mu tensor_m Kp)(mu tensor_m Kq)).toReal
          = sum_h mu.real {h}
                * (klDiv(Ber(p h))(Ber(q h))).toReal.

   The sum is over every history. Prove the measure identity and actual
   Radon--Nikodym/KL bridge; do not take conditional averaging as a
   hypothesis. Source endpoints and zero-weight histories must be covered.

2. Uniform one-step bound: if `B>=0` and every actual conditional
   divergence satisfies `klDiv(Ber(p h))(Ber(q h))<=ofReal B`, then

       klDiv(mu tensor_m Kp)(mu tensor_m Kq)<=ofReal B.

3. Accumulation step: if additionally `A>=0` and
   `klDiv mu nu<=ofReal A`, then

       klDiv(mu tensor_m Kp)(nu tensor_m Kq)<=ofReal(A+B).

   This must use actual joint laws and the proved averaging bound,
   together with Mathlib's composition-product chain rule. A base-law
   divergence premise is legitimate in this generic one-step lemma;
   it must not be described as a derived urn/transcript bound.

4. Actual binary postprocessing/testing: on an arbitrary measurable
   observation space `Omega`, for probability measures `P,Q` and a
   measurable decision `D:Omega->Bool`, prove that

       klDiv P Q<=ofReal(1/12)
       implies
       (P.real {omega | D omega=false}
           + Q.real {omega | D omega=true})/2 >= 3/8.

   Identify the two actual pushforward laws with Bernoulli laws using
   their true masses. Use actual KL data processing and accepted T62;
   do not assume Pinsker, testing error, a pushforward identity, or an
   abstract contraction coefficient. No total-variation definition is
   required. State measurability and probability assumptions explicitly.

Equivalent precise export names and choices of finite-history encoding
are permitted. Do not silently weaken these statements, exclude source
endpoints, or require all history atoms to have positive mass.

## Conventional proof supplied for implementation

For the shared-history joint pair, put

    r(h,true)=p(h)/q(h),
    r(h,false)=(1-p(h))/(1-q(h)).

The denominators are positive. On each joint singleton `(h,b)`, multiplying
the `mu tensor_m Kq` mass by `r(h,b)` gives the `mu tensor_m Kp` mass.
Equality on singletons determines a finite measure, including when
`mu{h}=0`. Thus the former measure with density `r` is the latter.
This proves absolute continuity; all real functions on the finite
space are integrable. The actual KL formula is therefore the finite
sum of target mass times log density. Group its two terms for each
history and apply the accepted Bernoulli formula. The endpoint factors
are zero under the library's real convention; no logarithm of a zero
denominator appears. Alternatively, use the `r log r` integral against
the reference measure and the same finite singleton calculation.

Probability weights `mu.real{h}` are nonnegative and sum to one. Each
conditional divergence is finite by T62. Averaging gives a real bound
by `B`; the joint finiteness theorem makes its conversion back to the
actual ENNReal divergence valid. Mathlib's exact identity

    KL(mu tensor_m Kp || nu tensor_m Kq)
      = KL(mu||nu) + KL(mu tensor_m Kp || mu tensor_m Kq)

then gives the accumulation bound using `ofReal(A+B)=ofReal A+ofReal B`
for nonnegative `A,B`. This route does not need a new infinite-history
conditional expectation theorem.

For the decision theorem, define `p=P.real(D^-1{true})` and the analogous
`q`. These are in the closed unit interval. The mass of `false` is the
complement of the mass of `true`, because `P,Q` are probability measures
and Bool has only two points. Hence `P.map D=Ber(p)` and `Q.map D=Ber(q)`.
KL data processing supplies T62's exact `<=1/12` hypothesis. Its conclusion
`((1-p)+q)/2>=3/8` is exactly the displayed decision error. The reference
decision mass `q` may equal zero or one; T62 already handles both endpoints.

## Verification and correspondence boundary

Use the existing Lean4.33.0/Mathlib pin. Preserve failed attempts, then
obtain a successful fresh module build and print the axioms of every
authored public declaration. Only standard Lean axioms are allowed;
no `sorry`, `admit`, custom axiom or opaque proof obligation. Hash source,
contract, logs and the exact dependency. Root reviews the full source
against this contract before accepting the gate. Report a missing API
or mathematical obstacle explicitly instead of changing the statement.

The uniform-layer law, adaptive fresh-cell exchangeability, sequence
padding, common private-seed simulator, n-step urn construction, actual
conditional parameter arithmetic, random-stop coupling and MSE-to-label
argument remain separate obligations. Even a complete PASS of this gate
does not by itself prove transcript KL<=1/12, the full D28 lower theorem,
the PDE phase construction or the D29 upper theorem. No originality claim
is attached to these standard information-theoretic facts.
