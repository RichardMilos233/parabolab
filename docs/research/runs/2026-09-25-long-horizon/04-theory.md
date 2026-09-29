# Long horizons: proposal limits and a bounded comparison

Conventional proofs. The raw coding-tree statements concern exactly the project's derivative-coded Allen–Cahn mechanism. The bounded ternary construction is a different representation with established majority-voting precedent; no publication-priority claim is made.

## L1. An exact absolute-integrability ceiling

Let the terminal value be phi=1/2 and f(u)=u-u³. Retain the raw Id, D, F0,F1,F2,F3 mechanism, exact scalar coefficients, and the inverse density/probability weights. A supported proposal has strictly positive conditional label probabilities and lifetime densities/survivals wherever the original completed-tree expansion has nonzero mass. It may depend on code, position, time or previous history. Require that its tree completes almost surely by every finite horizon (nonexplosion); this is automatic for fixed finite positive exponential rates and bounded offspring. The result does not cover mechanisms that regroup or cancel different signed trees.

At any finite killed branch depth, taking the absolute value and conditioning at the first event cancels the lifetime density and tuple probability against their inverse weights. This also holds for history-dependent conditionals by successive conditioning. Diffusion has no effect on flat terminal factors. Every completed derivative-code tree is zero: a D particle always has a D descendant until it terminates at phi'=0. Hence the second tuple alternatives of F0,F1,F2 and all branch alternatives of F3 have zero contribution.

Write J,a,b,c,e for the unrestricted absolute moments of Id,F0,F1,F2,F3. Killed depths increase to these extended nonnegative moments, by nonexplosion and monotone convergence. Their minimal integral system is

    J = 1/2 + integral a,
    a = 3/8 + integral ab,
    b = 1/4 + integral ac,
    c = 3   + integral ae,
    e = 6.

There is **no proposal parameter** in this system. On every interval where the solution is finite, positive ODE uniqueness identifies it with the minimal iteration. Put s=J-1/2, so s'=a and s(0)=0. Since a>0, changing variable from time to s gives

    c=3+6s,
    b=1/4+3s+3s²,
    a=P(s)=3/8+s/4+(3/2)s²+s³
         =(s+3/2)(s²+1/4).

Conversely these expressions solve the entire system when s'=P(s), so this is an exact reduction, not a majorant. Separation gives t=integral_0^s 1/P(v) dv. Since P>0, this strictly increasing map has range [0,T_abs), where

    T_abs = integral_0^infinity 1/[(v+3/2)(v²+1/4)] dv
          = (3*pi - 2*log(3))/5.

For verification, an antiderivative is

    F(s)=(2/5)log(s+3/2) -(1/5)log(s²+1/4)
         +(6/5)atan(2s).

Its derivative is 1/P(s); its logarithmic terms cancel at infinity and F(0)=(2/5)log3. Thus s(t) tends to infinity as t approaches T_abs from below. The minimal moment system is finite exactly before this time. At the boundary the Id root itself diverges because J=1/2+s; later horizons have at least that absolute moment, by the time-homogeneous nonnegative integral iteration. Therefore

    E|H_Id(T)| < infinity  iff  T < T_abs,
    E|H_Id(T)| = infinity  if   T >= T_abs.

This conclusion holds for every supported nonexplosive importance proposal on this same raw expansion, including changing lambda, nonexponential clocks, or tuple probabilities. It is not an assertion about all branching representations of the PDE. A finite sampled tree and a finite sample variance can coexist with either infinite second moment or infinite absolute expectation.

For T<T_abs the corresponding signed finite-moment system has initial (J,a,b,c,e)=(1/2,3/8,1/4,-3,-6) and the same signed products. Absolute integrability permits conditioning and dominated killed-depth limits. Local uniqueness identifies J with the global bounded solution of u'=u-u³, u(0)=1/2, namely u(T)=[1+3exp(-2T)]^(-1/2). At or beyond T_abs, the absolute-integrability hypothesis of the unbiased representation is false. We do not infer a biased but valid estimator, or define a conditionally convergent expectation.

## L2. A universal moment lower bound before the ceiling

For any supported proposal and T<T_abs, Cauchy–Schwarz gives

    E H² >= (E|H|)² = (1/2+s(T))².

This remains valid with infinite left-hand side. When the second moment is finite, the common mean gives Var(H)>=(1/2+s(T))²-u(T)². Thus even unrestricted importance tuning cannot keep variance bounded as T increases to T_abs.

A simple computable near-boundary estimate follows from P(v)<=(v+3/2)³ for v>=0. With delta=T_abs-T,

    delta=integral_s^infinity 1/P(v) dv >= 1/[2(s+3/2)²],
    E|H|=s+1/2 >= max(1/2, 1/sqrt(2*delta)-1).

The inequality is intentionally only a lower bound; the exact implicit s equation is available for calculation. An oracle proposal proportional to absolute tree mass motivates equality in Cauchy–Schwarz, but no such adaptive proposal is implemented or claimed computable here.

## L3. The earlier common-rate L2 ceiling is smaller

For the unchanged common-exponential raw flat estimator and common first-label probability p in (0,1), use the prior exact result

    T₂(lambda,p)=log(1+lambda²*p*C)/lambda,
    C=integral_0^infinity [9/64+v/16+(9/2)v²+6v³]^-1 dv.

The full second moment is finite exactly for T<T₂. This is a previous theorem, freshly evaluated here across longer horizons. Set z=lambda*sqrt(p*C). Then the maximum over lambda is sqrt(p*C)*h(z*), where h(z)=log(1+z²)/z and z*>1 is the unique positive solution

    2z²/(1+z²) = log(1+z²).

Indeed the derivative sign of h is the sign of g(z)=2z²/(1+z²)-log(1+z²); g' has the sign of 1-z², g(0)=0, and g tends to minus infinity. The finite-rate region at a fixed feasible T is an open interval, which shrinks to a point at the horizon maximum. The boundary point itself has infinite variance. The rate maximizing the admissible horizon is not the rate minimizing variance at a fixed smaller T.

The prior exact enclosure of C can be reused only after its witness is verified. Any decimal rate optimizer is labeled a floating calculation. The lambda≈.745 short-time rule is held fixed as a baseline, not assumed to extend to larger T. The paper's lambda=-log(.95)/T keeps the probability of root branching at 5% even when T is enlarged; extending T under that rule does not by itself create frequent root branching.

## B1. A bounded ternary representation for the same PDE

Assume bounded measurable terminal phi with values in [-1,1]. Use standard Brownian motion and ternary branching at rate r>=2; all three children start from the same parent death position and evolve independently thereafter. At a leaf return phi(X_T). At a branch combine child outputs by

    B_r(a,b,c)=((r+1)/(3r))*(a+b+c) - abc/r.

For r=2 this is the multilinear spin-majority polynomial (a+b+c-abc)/2. At cube vertices it is a spin in {-1,1}. Multiaffinity expresses its interior values as convex combinations of its vertex values, so B_2 preserves [-1,1]. More generally

    B_r=(2/r)*B_2+(1-2/r)*(a+b+c)/3,

which preserves the cube for r>=2. Every finite tree output lies in [-1,1] by induction. The ternary continuous-time branching process is nonexplosive at every finite T: a population k increases by two at total rate rk, and its expected population is exp(2rT). The completed estimator is therefore bounded almost surely. This proves all moments finite for every finite horizon and Var(H)<=1-u².

Conditional independence and multiaffinity give E B_r(H1,H2,H3)=B_r(u,u,u). The diagonal identity

    r*(B_r(u,u,u)-u)=u-u³

shows that the bounded mean solves the Allen–Cahn mild equation. Bounded uniqueness follows from the Lipschitz reaction on [-1,1], by the usual semigroup/Gronwall argument. Standard parabolic comparison keeps the PDE solution in [-1,1]. Thus the estimator has the same PDE mean for arbitrary bounded nonconstant terminal data in this interval, with no small-horizon condition. Numerical implementation below is restricted to the repository's one-dimensional tagged Allen–Cahn PDEs.

For r=2, one can instead sample independent terminal spins with mean phi and propagate hard majority votes. Conditional on all tree times and Brownian positions, integrating out the spins gives this soft estimator. Rao–Blackwell gives its variance no greater than the hard-vote variance 1-u². This is an established construction and conditional-expectation principle, used as a baseline here.

## B2. A sharp admissible clock and its cost

Within symmetric multiaffine ternary rules realizing this diagonal cubic, the coefficients of 1,sum a,sum ab,abc are fixed by matching all powers of u. Hence B_r is the unique such rule. At (1,1,-1),

    B_r(1,1,-1)=(r+4)/(3r).

For r>0 this is at most one exactly when r>=2. Consequently r>=2 is necessary and sufficient for this family's cube preservation. This is not a no-go theorem for asymmetric, higher-arity or other representations.

If N(T) is the total number of sampled nodes, a full ternary tree with B branch events has N=1+3B and alive leaves L=1+2B. Since E L=exp(2rT),

    E N=(3*exp(2rT)-1)/2.

The finite-variance horizon is now unlimited, but expected work is exponential. r=2 minimizes this expected node count within the bounded family. It is not generally variance-optimal. At r=2, T=2 the expected node count is approximately 4471 per root, which must be included in practical comparisons.

## B3. Variance decreases as the bounded clock increases

This optional conventional comparison concerns the unrestricted bounded family, not the raw tree. Let m=u(T,x) and v=E H²; always m²<=v<=1. For three iid child outputs define A=(X1+X2+X3)/3 and D=A-X1X2X3. Then B_r=A+D/r and the second-moment reaction is

    F_r(m,v)=r*(E A²-v)+2E(AD)+E D²/r
            =-(2r/3)*(v-m²)+2*((v+2m²)/3-v*m²)
             +((v+2m²)/3-2v*m²+v³)/r.

The coefficient of 1/r is E D²>=0, so for r2>=r1>=2,

    F_r2(m,v)-F_r1(m,v)
      =-(2/3)*(r2-r1)*(v-m²)+(1/r2-1/r1)*E D² <=0.

Both means solve the same bounded PDE. Scalar semilinear parabolic comparison, with common initial phi² and locally Lipschitz reaction on the bounded moment interval, gives v_r2<=v_r1. Thus the variance-versus-rate curve can have qualitatively different behavior after a representation change. Larger r lowers variance but raises expected work. No minimum of variance times cost, universal runtime advantage, or finite variance-optimal rate is asserted. This PDE comparison and its stochastic correspondence remain outside the Lean scope.

## Coverage boundary

The formal target is deterministic: scalar polynomial factorization/positivity, the branch identity and sharp corner bound, cube preservation, and finite-tree induction. Random-tree completion, density cancellation, minimal-moment identification, the improper integral, the PDE correspondence/comparison, and floating implementation are conventional arguments or numerical checks; a successful Lean build does not certify them automatically.
