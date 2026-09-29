# T50 — signed many-bump query lower bound

## Verdict

**GO for the requested restricted theorem.** For every fixed integer
`s>=1` and dimension `1<=d<4s`, the exact point-query lower bound on
the same genuinely sign-changing class as 04o improves to

    sup_v E Q_T(v) >= C exp(2*d*T/(2*s+d))

for all sufficiently large `T`, whenever the algorithm has uniform
absolute RMS at most `1/4`. Adaptive query locations, random stopping,
biased or unbounded real outputs, and exact real data values are allowed.
The proof controls the actual nonlinear PDE, rather than assuming that
the initial mean determines its solution.

The critical case **`d=4s` also passes**, with a smaller fixed bump
amplitude; Section 6 states that refinement separately. No result at
this exponent is proved here for `d>4s`. In particular, no concentration
statement about a nonlinear unstable-phase functional is assumed.

The cost lower bound first holds averaged over an explicit finite prior
on two sign layers, hence on at least one input in that prior. Those
inputs depend on `T`; the expensive member can depend on the algorithm.
There is no fixed-zero conclusion on this class, and no matching upper
bound or minimax-optimality claim for sign-changing inputs.

Only this report is changed. 04o is read-only; earlier reports remain
frozen. No Lean, implementation, numerical data, or experiment is added.
This is a conventionally closed proof for independent review, with a
10-query primary-literature check and no publication-priority claim.

## 1. Exact class and information contract

On the unit torus with normalized Lebesgue measure, consider

    u_t=(1/2)Delta u+u-u^3,  u(0)=v.

Fix a target point `x*`, `d>=1`, and integer `s>=1`. The promised class
is exactly the 04o class:

    F_signed={v in C^infinity(T^d):
      max_{|alpha|<=s} ||partial^alpha v||_infinity<=1,
      ||v||_infinity<=1/2,
      min v<0<max v}.

The only unknown-input information is the exact deterministic value
`v(x)` at each requested point. The algorithm may know the PDE,
`d,s,T,x*`, and the whole hard-family construction. It is not told
which family member is the input and cannot inspect its formula,
source, sign vector, Fourier coefficients, integral, or evolved values.
All initial-data evaluations count toward `Q_T`; input-independent
arithmetic and randomness are free.

Use an input-independent private seed and measurable next-query,
stopping, and output rules on finite transcripts. Require almost-sure
halting on the promised class. At each fixed horizon the hard prior
has finite support, so exceptional null sets can be removed for all its
runs simultaneously. Infinite expected cost already satisfies a lower
bound. No uniform deterministic cap is assumed for the original algorithm.

For every sufficiently large `T`, assume

    sup_{v in F_signed} E |H_T(v)-S_T v(x*)|^2 <=1/16.         (E)

The theorem below constructs a prior independent of that algorithm and
proves a lower bound on its prior-average expected query count. This
implies the advertised worst-case-in-input bound.

## 2. A uniform signed PDE estimate with its cubic correction

The following lemma is the analytic core. It applies to any smooth
initial datum with `A=||v||_infinity<=1`, not just the eventual bumps.
Let `m=integral v`, and let

    ell_m(t)=m*exp(t)/sqrt(1+m^2*(exp(2t)-1))

be the signed scalar Allen–Cahn solution. Put

    nu=2*pi^2-1>0,
    h=exp(-4*pi^2),
    H_d=((1+h)/(1-h))^(d/2),
    C_d=e*(H_d+3/(nu+1)).

Then, for every `T>=1`,

    ||S_T v-ell_m(T)||_infinity
      <=[5/(2nu)]*exp(T)*A^3
          +C_d*A*exp[-nu*(T-1)].                            (P)

Here and below scalar functions in a spatial norm mean constant spatial
functions. We prove both terms, including the effect on the mean.

### 2a. Spatial variance decays at the spectral rate

Write `u=S_t v`, `b(t)=integral u(t)`, and `w=u-b`. Comparison yields
`|u|<=1` and `||u(t)||_infinity<=A*exp(t)`. The latter follows by
comparison for both signs, or from Kato's inequality for `|u|`.

Since `integral w=0`, integration by parts gives

    (1/2) d/dt ||w||_2^2
      =-(1/2)||gradient w||_2^2+||w||_2^2-integral w*u^3.

The last integral is nonnegative:

    integral w*u^3=integral (u-b)*(u^3-b^3)>=0,

because the real cube function is increasing. The mean-zero Poincare
inequality on this particular unit torus is
`||gradient w||_2^2>=4*pi^2||w||_2^2`. Consequently

    ||w(t)||_2<=exp(-nu*t)||w(0)||_2<=A*exp(-nu*t).           (V)

The last step uses normalized volume and
`||v-m||_2^2=integral v^2-m^2<=A^2`.

### 2b. The nonlinear mean error is controlled

The mean does not solve the scalar equation exactly. Its exact equation is

    b'=b-b^3-R(t),
    R(t)=3*b(t)*integral w^2+integral w^3.

Using `|b|<=A exp(t)`, `||w||_infinity<=2A exp(t)`, and (V),

    |R(t)|<=5*A^3*exp[(1-2nu)*t].                           (R)

The difference `b-ell_m` has zero initial value and satisfies a scalar
linear equation with coefficient

    1-(b^2+b*ell_m+ell_m^2)<=1

and forcing `-R`. Variation of constants therefore implies

    |b(T)-ell_m(T)|
      <=integral_0^T exp(T-t)|R(t)|dt
      <=[5/(2nu)]*exp(T)*A^3.                               (B)

No closed mean equation, cancellation of the cubic term, or replacement
of the PDE by its linearization is assumed.

### 2c. One-unit smoothing upgrades the spatial remainder

Define

    G(t,x)=u(t,x)^2+u(t,x)*b(t)+b(t)^2.

Then `0<=G<=3` and

    w_t=(1/2)Delta w+(1-G)w+q(t),
    q(t)=integral G(t,x)w(t,x)dx.

In particular `|q(t)|<=3||w(t)||_2<=3A exp(-nu*t)`.
Positive linear comparison, or Kato's inequality followed by the heat
semigroup, gives for `T>=1`

    |w(T)|<=e*P_1|w(T-1)|
               +integral_{T-1}^T exp(T-t)|q(t)|dt.

The heat kernel satisfies

    ||p_1||_2^2=sum_{k in Z^d} exp(-4*pi^2*|k|^2)<=H_d^2,

using `sum_{n>=1} h^(n^2)<=h/(1-h)`. Hence

    ||w(T)||_infinity
      <=e*[H_d+3/(nu+1)]*A*exp[-nu*(T-1)].                  (W)

Combining (B) and (W) proves (P). The argument uses the unit torus and
its mean-zero spectral gap exceeding the linear growth rate one; it
does not automatically extend unchanged to arbitrary domain sizes.

## 3. Two Hamming layers inside the fixed smooth class

Fix a known nonzero bump

    psi in C_c^infinity((0,1)^d),  0<=psi<=1,
    I=integral psi>0,
    D=max(1,max_{|alpha|<=s} ||partial^alpha psi||_infinity).

For the subcritical case `d<4s`, take `a=1/(8D)` and put

    q=s+d/2,
    R_T=(a*I*exp(T))^(1/q),
    k=2*floor(R_T/2),  K=k^d.

Take `T` large enough that `R_T>=4` and `K>=2048`. The even `k`
makes `K` even, and `R_T/2<=k<=R_T`. Partition the torus into
half-open cubes indexed by `j in {0,...,k-1}^d`, and define

    b_j(x)=a*k^(-s)*psi(k*x-j)

in cube `j`, extended by zero elsewhere. For a sign vector
`sigma in {-1,1}^K`, let

    v_sigma=sum_j sigma_j*b_j,
    r=2*ceil(sqrt(K)/2),
    L_+={sigma: sum_j sigma_j=r},
    L_-={sigma: sum_j sigma_j=-r}.

The integer `r` is even and satisfies

    sqrt(K)<=r<=2sqrt(K)<=K/4.

Each layer is nonempty. Every vector in either layer has both signs,
so every corresponding `v_sigma` is genuinely sign-changing. Compact
support in each cell makes all functions smooth and periodic, including
across cell boundaries. Disjoint supports give

    ||v_sigma||_infinity<=A:=a*k^(-s),
    max_{|alpha|<=s} ||partial^alpha v_sigma||_infinity<=aD<=1/8.

Thus these are members of the original fixed class with substantial
slack, not a new `T`-dependent smoothness class.

Every bump has mass `mu=aI*k^(-s-d)`. The two layers have signed means

    m_sigma=+mu*r on L_+,   m_sigma=-mu*r on L_-,
    1<=exp(T)*|m_sigma|<=2^(q+1).                            (M)

In particular `|ell_{m_sigma}(T)|>=1/sqrt(2)`, with the correct sign:
for `z=exp(T)|m_sigma|>=1`,

    |ell_{m_sigma}(T)|=z/sqrt(1+z^2-m_sigma^2)
                       >=z/sqrt(1+z^2)>=1/sqrt(2).

## 4. Subcritical uniform separation, with an explicit threshold

For `d<4s`, set

    delta=3s/q-1=(4s-d)/(2s+d)>0,
    rho=nu+s/q>0,
    C1=[5/(2nu)]*2^(3s)*a^3*(aI)^(-3s/q),
    C2=C_d*2^s*a*(aI)^(-s/q)*exp(nu),
    Rmin=max(4,2*2048^(1/d)).

The floor bounds and (P) imply, for all sign vectors in either layer,

    ||S_T v_sigma-ell_{m_sigma}(T)||_infinity
        <=C1*exp(-delta*T)+C2*exp(-rho*T).

One sufficient common threshold is

    T0=max(1,
           q*log(Rmin)-log(aI),
           max(0,log(16*C1))/delta,
           max(0,log(16*C2))/rho).

For all `T>=T0`, `K>=2048` and the PDE error is at most `1/8`.
Combining this with (M) gives, uniformly over all arrangements in a layer
and all target points,

    S_T v_sigma(x*)>=1/sqrt(2)-1/8>1/2  on L_+,
    S_T v_sigma(x*)<=-1/sqrt(2)+1/8<-1/2 on L_-.              (G)

This proves the strong separation required for the intended `1/4`
absolute RMS threshold. It does not merely separate the average target
over a random layer.

## 5. Adaptive testing lower bound and random stopping

Give the two layers equal prior probability and sample a sign vector
uniformly within the selected layer. These layers have equal cardinality
by the map `sigma -> -sigma`. The prior is public and independent of
the algorithm's private seed.

### 5a. An exact function query reveals at most one unknown sign

The value at a point in cube `j` is `sigma_j` times the known bump
value there. A stronger oracle may reveal the entire sign of that cube,
even if the requested point is in a region where the bump vanishes.
Repeated visits require no new sign revelation. Therefore an algorithm
using at most `n` original point queries can be simulated with at most
`n` sign queries; allowing this extra information only strengthens the
algorithm against which the lower bound is proved.

By exchangeability of each layer, conditional on any already observed
signs, the sign at any unqueried cell has the same remaining-urn law.
Adaptive selection of the cell does not change that fact. A procedure
which uses fewer than `n` distinct signs can be padded with unused cells.
Its output and original transcript are measurable functions of its seed
and the `n` revealed signs. Thus it suffices to bound the total variation
distance between the two length-`n` urn experiments, even when the seed
and adaptive query indices are included in the transcript.

### 5b. A self-contained fixed-query bound

Take `n=floor(K/1024)`. After `i<n` signs have been exposed, with
`S_i` positive signs, the conditional probabilities for the next sign
to be positive are

    p_+=( (K+r)/2-S_i )/(K-i),
    p_-=( (K-r)/2-S_i )/(K-i).

Every history of this length is feasible under both layers. Since
`i<=K/8` and `r<=K/4`,

    1/4<=p_-<=3/4,
    p_+-p_-=r/(K-i)<=2r/K.

For Bernoulli laws, `log x<=x-1` gives

    KL(Ber(p_+) || Ber(p_-))
       <=(p_+-p_-)^2/[p_-(1-p_-)]
       <=(64/3)*r^2/K^2<=256/(3K).

The KL chain rule, conditioning on the private seed if needed, yields

    KL(P_+^n || P_-^n)<=256*n/(3K)<=1/12.

Here logarithms are natural. Pinsker's inequality and data processing
give transcript total variation at most `1/sqrt(24)<1/4`. Consequently
every such capped test has equal-prior classification error at least

    (1-TV)/2>=3/8.                                         (TV)

This proof does not model the original oracle as independent biased
coins. The data are a fixed spatial function whose signs have a finite
hard-input prior; conditional draws are without replacement. Adaptivity
is handled by conditional exchangeability, not by assuming iid answers.

### 5c. From RMS to testing, then to expected queries

For an original algorithm satisfying (E), classify as positive when
`H_T>=0` and negative otherwise. By (G), any classification mistake has
squared solution error at least `1/4`. Hence the mistake probability
is at most `1/4` for every input, and also under the prior.

Let `qbar` be its prior-average expected original query count. If it is
infinite there is nothing to prove. Otherwise truncate the test when it
would request query `n+1`, assigning an arbitrary label on truncation.
Its prior error increases by at most

    P_prior(Q_T>n)<=qbar/n.

The truncated test uses at most `n` original queries, so (TV) applies.
Therefore

    3/8<=1/4+qbar/n,
    qbar>=n/8>=K/16384.                                    (Q)

The last inequality uses `K>=2048`. No independence between stopping,
the input, or the output is used. The bound allows arbitrarily expensive
rare branches and does not require unbiased outputs.

Finally,

    K>=2^(-d)*(aI)^(d/q)*exp(d*T/q),

so (Q) gives the explicit lower bound

    qbar>=2^(-d-14)*(aI)^(d/q)*exp(2*d*T/(2*s+d)).            (LB)

At least one member of this finite prior has expected cost at least
`qbar`. Thus (LB) proves the claimed worst-case lower bound at every
sufficiently large horizon, not just along a selected time sequence.

## 6. Critical dimension d=4s

At `d=4s`, `q=3s` and the generic error term no longer decays with `T`,
but its fixed coefficient can be made small. Choose instead

    a=min(1/(8D), sqrt(nu*I/(40*2^(3s)))).

All class, layer, information, and floor arguments are unchanged. Now

    [5/(2nu)]*exp(T)*A^3
       <=[5/(2nu)]*2^(3s)*a^2/I<=1/16.

The spatial remainder still tends to zero. Use the same `Rmin,C2,rho`
with this `a` and `q=3s`, and take

    T0=max(1,
           q*log(Rmin)-log(aI),
           max(0,log(16*C2))/rho).

The total PDE error is again at most `1/8`, so (G)–(LB) hold. This is
a separate verified critical-dimension refinement; it does not rely
on taking a negative or zero value of the subcritical decay parameter.

## 7. What remains unproved above the critical dimension

For `d>4s`, the present scale gives

    exp(T)*A^3 = O(k^(d/2-2s)),

with a positive power of `k`. Making the fixed bump coefficient smaller
does not stop that expression from growing as `T` tends to infinity.
Therefore (P) cannot establish uniform separation of every sign
arrangement in these two layers at the proposed scale. This is a
limitation of this proof, not a disproof of the stronger lower bound.

Nor may the cubic correction be discarded simply because the signed
mean is tiny. Even the smooth mean-zero datum

    v(x)=epsilon*(cos(2*pi*x_1)+c*cos(4*pi*x_1)),  c!=0,

has initial mean derivative `-(3/4)c*epsilon^3` and belongs to the fixed
class for sufficiently small positive `epsilon`. Thus a zero signed
mean is not preserved in general. Small signed mass provides none of the
nonnegative height-versus-mass control used in T46.

The suggested alternative based on a nonlinear unstable-phase
functional would need a defined functional, its approximation error,
per-cell influence bounds uniform up to the relevant exit scale, and
concentration on these fixed Hamming layers. None of those statements
is supplied or assumed here. A proof holding with sufficiently high
probability under each layer could potentially replace uniform
separation, but its probability loss would have to enter the testing
error budget explicitly. The all-dimension claim remains open in this
bounded audit.

## 8. Scope, falsification checks, and decision

- The hard functions are genuinely sign-changing because both signs
  occur in every layer vector; no zero baseline or nonnegative-class
  substitution is used.
- The smoothness class is fixed. Only its selected members and their
  derivatives above order `s` change with `T`.
- Point queries can be arbitrary and adaptive. A cell partition is a
  description of the input family, not a grid imposed on the algorithm.
- Exact values reveal at most one unknown cell sign. Neither independent
  coin noise nor inaccessible input metadata is inserted into the model.
- The scalar mean comparison includes a proved cubic remainder. Spatial
  mixing is estimated over the actual full horizon, rather than presumed
  adequate after a fixed time relative to a shrinking signed mean.
- Expected cost is controlled by explicit truncation under one finite
  prior. No fixed-count lower bound is silently substituted for a
  random-stopping statement.
- There is no conclusion that a fixed known sign-changing formula gets
  harder, or that every layer member is expensive. The prior-average
  and resulting worst-case quantifiers are the proved statements.
- T46's smaller matching exponent concerns a different nonnegative
  class; it creates no contradiction. No signed-class matching upper
  bound is established by this report.

The conventional proof is closed for `d<4s`, with the separate `d=4s`
refinement. The appropriate next step is an independent audit of this
fixed theorem and constants. No numerical experiment, implementation,
or formal target is proposed before that gate.

## 9. Primary-literature overlap

[Ben-David–Blais, *A Tight Composition Theorem for the Randomized Query
Complexity of Partial Functions*, Section 3, Definition 25 and Lemma
26](https://arxiv.org/pdf/2002.10809), is direct prior for the core
information problem: its gap-majority promise consists of two Hamming
levels separated by order `sqrt(K)`, and its randomized query complexity
is linear in `K`. The proof uses permutation symmetry to remove any
advantage of adaptive index selection. Their Section 2 transcript
definition includes internal randomness. Section 5 above supplies its
own conditional-KL constants and the expected-cost truncation step; no
new gap-majority principle is claimed.

[Kunsch–Rudolf, *Optimal confidence for Monte Carlo integration of smooth
functions*, Section 2.1, Lemma 2.1, and Section 2.2, proof of Theorem
2.3](https://arxiv.org/pdf/1809.09890), is direct prior for disjoint
norm-scaled bumps carrying unknown signs. The latter proof yields the
familiar `n^(-s/d-1/2)` integration scale. The paragraph before the
lower-bound lemmas explicitly permits adaptive locations and notes the
extension to random input-dependent cardinality with modified constants.
The exponent targeted here is therefore a classical integration scale;
the required extra work is its controlled transfer through nonlinear
long-time PDE evolution on the stated signed class.

[Hairer–Lê–Rosati, *The Allen–Cahn equation with generic initial datum*,
equation (1.5), Theorem 1.1 and Proposition
4.6](https://arxiv.org/pdf/2201.08426), is relevant prior for small signed
initial data growing near the unstable state and passing through a
nonlinear scalar transition profile. Its setting uses random fields
on unbounded space and a different scaling regime. It does not supply
the unit-torus query theorem or the uniform estimate (P) in the inspected
statements. Neither the unstable-growth mechanism nor the scalar profile
is asserted to be new.

The 10-query search did not locate the exact PDE/query lower-bound
combination proved here. This is not evidence sufficient to establish
priority; the information argument is explicitly classical, and the
PDE transfer may also be known under different terminology.

## 10. Bounded search log

1. `randomized integration lower bound Hamming weight layer hypergeometric adaptive queries Bakhvalov`
2. `query complexity approximate counting gap majority square root n randomized expected queries`
3. `Allen Cahn torus mean zero exponential decay nonlinear mean small initial data unstable equilibrium`
4. `"Gap Majority" "randomized query complexity" arxiv`
5. `"Hamming layers" "randomized" "query"`
6. `"gap majority" "expected" "queries" Ben David Blais`
7. `"randomized integration" "signs" "Bakhvalov" lower bound`
8. `"Allen-Cahn" "spatial average" "Poincare" convergence`
9. `"reaction diffusion" "asymptotic phase" "unstable" equilibrium mean`
10. `"Allen-Cahn" "mean-zero" "small" periodic solution`

Primary-paper opens and in-document searches followed. Teaching pages
and secondary search results were used only to locate primary papers,
not to support the theorem or an originality assessment.
