# T45 — independent audit of the fixed-zero corollary

Status: **ACCEPT the Allen–Cahn corollary and its information argument.**
The optional C² reaction extension is also accepted with the positive
norm-radius interpretation made explicit below. There is no blocking
conventional proof defect. Two minor parameter-dependence clarifications
are recorded; neither changes the stated `epsilon=1/4` conclusion.

This audit fixes `v=0` as the datum on which query cost is measured while
retaining a uniform accuracy promise on an unknown spatial input class.
It does not assert a lower bound when the datum is supplied as a known
zero formula, or transfer this datum into the old sign-changing class.

## 1. Frozen scope and decisions

Audited sources, read without modification:

- `reviews/T44-zero-baseline-corollary.md`, SHA256
  `124d2c2152fb8ce1f8edd8585ce38ee3739a69892c6769a856be42d85b0f6d29`.
  This matches the dispatched frozen SHA exactly.
- `04o-unstable-phase-query-lower-bound.md`, SHA256
  `67d6463087775a857a2ffc035fa6ef7fa31db47b4c99b496ecdcc9e8f87fd765`.

These hashes were rechecked immediately before writing this report.
T40 was consulted for the existing attribution and context. The argument
below independently checks the frozen T44 formulas and quantifiers; it
does not treat another review's verdict as proof. The repository already
contained unrelated modified and untracked files at the initial status
check. This task writes only this new T45 report.

| Claim under review | Decision | Exact scope |
| --- | --- | --- |
| Fixed-zero Allen–Cahn query lower bound | **ACCEPT** | Uniform MSE on the fixed class `F+`, with only exact point-value information. |
| Smooth bump membership and nonlinear target gap | **ACCEPT** | Finite fixed `C^s` control; target gap at least `1/sqrt(2)`. |
| Repetition of zero in the finite-family average | **ACCEPT** | One coupled zero output, reused algebraically with total weight `1/2`. |
| Adaptive queries, private randomness, random stopping | **ACCEPT** | Input-independent seed, measurable transcript rules, a.s. finite halting. |
| Displayed Allen–Cahn constants and threshold | **ACCEPT** | The general-error prefactor depends on `epsilon`; `T0` does not. |
| Optional C² reaction extension with `f'(0)=lambda>0` | **ACCEPT** | Fixed `f,b`, positive fixed norm radius, and `epsilon<theta/2<b/2`. |
| Relabeling the old sign-changing theorem as this fixed-datum result | **REJECT** | Zero is not in the old class; the separate class and proof are essential. |
| A lower bound for a promised known zero/constant input | **REJECT** | That changes the class or gives extra input information. |

The role is independent mathematical research review under the
math-auto-research workflow. Its configured research preference is
`gpt-6-astra` with `max` effort; the serving model/effort is not
independently inspectable in this worker. No code, numerical experiment,
Lean build, implementation change, or novelty determination is part of
T45. Existing formal gates are outside this audit's acceptance claim.

## 2. The fixed datum and the class quantifiers

Fix `d>=1`, integer `s>=1`, `x*`, and one bump `psi`. The accepted class is

    F+ = {v in C^infinity(T^d): 0<=v<=1/2,
          max_{|alpha|<=s} ||partial^alpha v||_infinity <=1}.

For each fixed `epsilon in (0,1/(2 sqrt(2)))`, the statement is

    for every T>=T0 and every admissible algorithm A_T,
      [sup_{v in F+} E|H_T(v)-S_Tv(x*)|^2 <=epsilon^2]
        implies E Q_T(0) >= C_epsilon exp(d*T/(s+d)).

The class, datum zero, and threshold are fixed before `T` and `A_T`.
The alternatives `b_{j,T}` and their finite number depend on `T`, but
not on the algorithm. This is legitimate: the accuracy premise applies
to every one of these alternatives at the horizon in question. No
interchange of a limit, supremum, and expectation is used. The theorem
permits a different algorithm at every horizon, so a family of uniformly
accurate algorithms also satisfies the bound at each horizon.

Knowing the hard-family formulas only supplies public possibilities.
It does not supply the identity of the unknown input. The oracle
restrictions in T44 exclude source inspection, labels, preprocessing,
and evaluation side information that could reveal that identity. They
also count every input evaluation. With these restrictions, having
zero as the actual datum is different from being told that the datum
is zero. No further datum quantifier is hidden in the proof.

Finite smoothness control is important. The class contains smooth
functions whose higher derivatives grow as the cells shrink. T44
does not claim a common analytic radius, all-order derivative bounds,
or a finite-dimensional class. Likewise, the fixed positive-mass
conditions discussed in T44 exclude zero and eventually exclude these
shrinking bumps; this corollary does not negate such conditional work
bounds.

## 3. Bump, heat, nonlinear flow, and constant checks

Write `q=s+d`, with T44's fixed constants

    I=integral psi>0,
    D=max(1,max_{|alpha|<=s} ||partial^alpha psi||_infinity),
    a=1/(8D),
    kappa=(2*pi)^(-d/2) exp(-d/8).

For a cell indexed by `j`, differentiation of its extended bump gives

    partial^alpha b_j(x)
      =a*k^(|alpha|-s)*(partial^alpha psi)(kx-j)

inside the cell. Compact support strictly inside the cell makes all
derivatives match the zero extension, including at the torus boundary.
For `|alpha|<=s` and `k>=1`, its norm is at most `aD=1/8`.
The change of variables gives mass `mu=aI*k^(-q)`. Thus every alternative
and zero belong to `F+`, and no `T`-dependent enlargement of the class
is being used.

The stated threshold

    T0=max(1,1+q*log(4)-log(kappa*a*I))

ensures `R=(kappa*a*I*exp(T-1))^(1/q)>=4`. Consequently,

    k=floor(R)>=4,  R/2<=k<=R,
    1<=kappa*mu*exp(T-1)=(R/k)^q<=2^q,
    K=k^d>=2^(-d)*(kappa*a*I/e)^(d/q)*exp(d*T/q).

The heat-kernel normalization matches the generator `Delta/2`.
The Gaussian term for a nearest integer translate has squared distance
at most `d/4`, giving the lower bound `kappa` at time one. The invariant
interval `[0,1]` and nonnegative reaction there yield

    S_1 b_j >=P_1 b_j >=kappa*mu =c.

Here `0<c<1`, since `kappa<1`, `I<=1`, and `mu<=1/8`.
Scalar comparison for the remaining nonnegative time `T-1` then gives

    S_T b_j(x*) >= ell_c(T-1),
    ell_c(t)=c*exp(t)/sqrt(1+c^2*(exp(2t)-1)).

This expression solves `ell'=ell-ell^3` with `ell(0)=c`.
Putting `z=c*exp(T-1)>=1` shows

    ell_c(T-1)=z/sqrt(1+z^2-c^2)
      >=z/sqrt(1+z^2)>=1/sqrt(2).

Thus `a_j=S_Tb_j(x*)>=1/sqrt(2)` and `S_T0=0` exactly.
The estimate is uniform in the cell and target point. No spatial-mean
closure or approximation by the linearized reaction is present.

All displayed Allen–Cahn constants pass. The prefactor is precisely

    C_epsilon=(1-8*epsilon^2)*2^(-d)*(kappa*a*I/e)^(d/q).

At `epsilon=1/4` this becomes

    C_(1/4)=2^(-d-1)*(kappa*a*I/e)^(d/q)>0.

**Minor wording clarification:** T44's sentence that the constants
depend only on `d,s` and the bump applies to `a,I,kappa,T0` and to the
specialized `epsilon=1/4` prefactor. In the general-error statement the
displayed `C_epsilon` also depends on `epsilon`. A claim that this
particular prefactor were uniform in all admitted `epsilon` would be
incorrect; its explicit formula already shows the correct dependence.

## 4. Coupling and repeated-zero risk

Fix a seed on which the baseline halts, with finite query count `n`.
Let `J` be the set of half-open cells visited on that zero run. Then
`|J|<=n`; repeated queries and visits at zeros of a bump only overcount
potentially informative visits.

For `j not in J`, prove transcript equality by induction. Before any
query both runs have the same seed and empty transcript. If their
transcripts agree, the measurable algorithm rules choose the same
next query or the same halt decision. Every next baseline query before
its stopping time is outside cell `j`, where `b_j=0`, so its response
also agrees. At step `n` the alternative therefore halts at the same
step and returns the same real output. This argument includes `n=0`.
It requires no common deterministic query horizon and no independence
between the stopping time, visited cells, and returned output.

The baseline no-hit event `E_j={j not in J}` is a measurable event on
the common seed space, formed from the finite random transcript. At a
fixed `T` there are only `K+1` distinct inputs. Thus the per-input null
sets allowed by the a.s. halting condition can be removed by a finite
union. Infinite expected baseline cost already proves the conclusion;
otherwise all following cost manipulations are finite. No information
is assumed about the coupled runs after a distinguishing query.

On `E_j`, write their common output as `y`. The exact identity is

    ((y-a_j)^2+y^2)/2=(y-a_j/2)^2+a_j^2/4>=1/8.

Let `R_j=E|H_T(b_j)-a_j|^2` and `R_0=E|H_T(0)|^2`.
Integrating the pointwise inequality and discarding nonnegative losses
off `E_j` gives

    (R_j+R_0)/2 >= P(E_j)/8.

Average these `K` inequalities:

    (1/(2K))*sum_j R_j + R_0/2
      >= (1/(8K))*sum_j P(E_j)
       = (1/8)*(1-E|J|/K)
      >= (1/8)*(1-E Q_T(0)/K).

The left side is at most `epsilon^2`. It is exactly the risk of a
finite prior that places probability `1/2` on zero and `1/(2K)` on
each alternative. Its repeated-zero presentation neither creates new
independent observations nor duplicates an information budget. Only
finite linearity of expectation is used. Hence

    E Q_T(0)>=(1-8*epsilon^2)*K.

Rare expensive runs, arbitrary bias, and unbounded real outputs do not
invalidate a pointwise loss inequality. The uniform MSE premise makes
these losses integrable. The proof needs neither optional stopping nor
a Bernoulli-oracle substitution. The repeated-zero and adaptive-stop
claims are therefore accepted as written.

## 5. Optional C² extension and complete parameter dependence

Accept the extension for fixed

    f in C^2([0,b]), b>0, f(0)=f(b)=0,
    f(y)>0 on (0,b), f'(0)=lambda>0.

Make its class fully explicit by fixing `L>0` and requiring

    F_(b,L)+={v in C^infinity(T^d): 0<=v<=b/2,
             ||v||_(C^s,max)<=L}.

Choose any fixed `0<a<=min(b/2,L/D)` for the same bump construction.
This ensures class membership for every `k>=1`. The invariant interval
`[0,b]` keeps the reaction in its stated domain; if a PDE construction
uses an extension of `f` outside that interval, comparison ensures
that the solutions used here never evaluate that extension.

**Minor scope clarification:** a finite norm bound must be strictly
positive for this construction. If `L=0`, the class is `{0}` and the
asserted positive query lower bound would be false. The original
Allen–Cahn radius is `1`, so this issue concerns only making the
optional extension's abbreviated class description explicit.

Fix `theta in (0,b)`. To verify the nonlinear step directly, let
`M=max_[0,b]|f''|`. Taylor's theorem gives, for small positive `y`,

    |f(y)-lambda*y|<=M*y^2/2,
    f(y)>=lambda*y/2.

Thus

    |1/f(y)-1/(lambda*y)|
      =|lambda*y-f(y)|/(lambda*y*f(y))<=M/lambda^2.

Away from zero and up to the fixed `theta<b`, the same integrand is
continuous because `f` is strictly positive. Therefore T44's
`J_theta=integral_0^theta |1/f(y)-1/(lambda*y)|dy` is finite and
`B_theta=theta*exp(lambda*J_theta)>0` is finite. For `0<c<theta`,
separation of variables for the positive scalar flow gives

    tau(c,theta)=integral_c^theta dy/f(y)
      <=(1/lambda)*log(theta/c)+J_theta
       =(1/lambda)*log(B_theta/c).

It follows that `c*exp(lambda*S)>=B_theta` is sufficient to reach
`theta` by time `S`; when `c>=theta`, scalar monotonicity already gives
the result. No behavior at `b` beyond the stated hypotheses is needed,
because the target `theta` stays strictly below it. In particular,
the rate `lambda` does not rely on a global inequality
`f(y)>=lambda*y`, which need not hold.

An explicit threshold and prefactor omitted from T44's abbreviated
extension can be taken as

    T0_theta=max(1,
      1+(q*log(4)+log(B_theta)-log(kappa*a*I))/lambda),
    R_theta=(kappa*a*I*exp(lambda*(T-1))/B_theta)^(1/q),
    k=floor(R_theta),
    C_(theta,epsilon)=(1-4*epsilon^2/theta^2)*2^(-d)
      *(kappa*a*I*exp(-lambda)/B_theta)^(d/q).

For `T>=T0_theta`, `R_theta>=4`, so all floor estimates used above
hold. Nonnegative reaction gives `S_1b_j>=c=kappa*aI*k^(-q)` and

    c*exp(lambda*(T-1))
      =B_theta*(R_theta/k)^q>=B_theta.

Thus `S_Tb_j>=theta`. Replacing the gap `1/sqrt(2)` by `theta` in
the paired loss argument proves

    E Q_T(0)>=(1-4*epsilon^2/theta^2)*k^d
      >=C_(theta,epsilon)*exp(lambda*d*T/q),

with a positive prefactor whenever `epsilon<theta/2`.
The constants depend on fixed `f,b,L,d,s,psi,theta,epsilon` as shown;
they are not uniform over reactions merely sharing the same `lambda`.
For every fixed `0<epsilon<b/2`, a fixed `theta in (2epsilon,b)` is
available. At `epsilon>=b/2`, the zero-query output `b/2` has error at
most `epsilon` on `[0,b]`, so such an accuracy restriction is required.

This verifies the optional extension conventionally. It makes no claim
for merely C¹ reactions, sign-changing general-reaction inputs, or a
uniform constant independent of the reaction.

## 6. Source check and acceptance boundary

The bounded primary-source check supports the existing methodological
attribution only. Kunsch–Rudolf, Section 2.1, formulates randomized
adaptive value information and finite input priors; Section 2.2 uses
scaled bumps in disjoint cubes. Their fixed-cardinality presentation
does not by itself replace the direct random-stopping proof given
above. [Kunsch–Rudolf, *Optimal confidence for Monte Carlo integration
of smooth functions*](https://arxiv.org/pdf/1809.09890).

Kwas, Section 3.2, measures randomized pointwise PDE approximation by
worst-case RMS error and expected function-value count. This verifies
the relevance of those information and cost conventions, without
attributing T44's nonlinear fixed-zero theorem to that paper.
[Kwas, *Complexity of multivariate Feynman–Kac path integration in
randomized and quantum settings*](https://arxiv.org/pdf/quant-ph/0410134).

The fixed-zero result can be integrated as a **separate nonnegative-class
corollary**, retaining its oracle contract and uniform-error premise.
There is no numerical evidence or complete formalization asserted by
this audit. No optimal exponent, publication priority, or novelty claim
is accepted or made.
