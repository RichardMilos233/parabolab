# T46 — matching randomized query upper bound on the nonnegative class

## Verdict

**GO: the exponent is matched conventionally for every fixed integer
`s>=1`, not only `s=1`.** On precisely T44's nonnegative input class,
there is a constructive algorithm using a deterministic number
`O(exp(d*T/(s+d)))` of exact initial-data point queries and achieving
uniform absolute RMS below `1/4`, for every sufficiently large `T`.
Its output is a sigmoid of a sample average. The proof controls both
sampling error and the error of replacing the nonlinear PDE by that
scalar function. The estimator is generally biased.

Combined with T44, this establishes the asymptotic query order

    inf_{uniformly RMS<=1/4 algorithms} sup_{v in F+} E Q_T(v)
        = Theta(exp(d*T/(s+d))).

The constants and starting horizon depend on `d,s`. The lower bound
permits adaptive randomized stopping; the upper bound needs neither
adaptivity nor random query cardinality. The same exponent therefore
also matches when the upper cost is measured by a deterministic cap.
This is a statement about ideal exact-value information, not bit cost,
unbiased estimation, relative defect error, or practical efficiency.

The proof is ready for independent theory audit. No code, experiment,
or formalization is performed. Only this report is changed; 04o and the
frozen T44 report were read without modification. The bounded primary
search used 17 queries. No publication-priority claim is made.

## 1. Fixed class and explicit algorithm

Fix `d>=1`, integer `s>=1`, and a point `x*` on the unit flat torus. Write

    u_t = (1/2) Delta u + u-u^3,  u(0)=v,  u(T)=S_T v,
    F+ = {v in C^infinity(T^d): 0<=v<=1/2,
          max_{|alpha|<=s} ||partial^alpha v||_infinity<=1},
    beta=s/(s+d),  gamma=d/(s+d)=1-beta,
    m=integral_{T^d} v(x) dx,
    Psi(z)=z/sqrt(1+z^2),  z>=0.

The torus measure has total mass one. The only unknown-input operation
is evaluating the exact deterministic value `v(x)` at a chosen point.
No input formula, mass oracle, or evolved-PDE oracle is supplied. As in
T44, arbitrary private randomness and scalar arithmetic are free for
the query count. Independent uniform torus samples are permitted.

Section 2 constructs a known constant `C=C(d,s)>=1`. Section 3 supplies
an explicit finite `T*`, independent of `v`, such that for `T>=T*`

    sup_{v in F+} ||S_T v-Psi(exp(T)*m)||_infinity <=1/32.       (P)

For such a horizon, the algorithm is:

1. Set `n=ceil(64*C*exp(gamma*T))`.
2. Draw iid uniform points `X_1,...,X_n` on the torus, query `v(X_i)`,
   and form `mhat=(1/n) sum_i v(X_i)`.
3. Return `H=Psi(exp(T)*mhat)`.

Its number of data queries is exactly `n` on every input and every
random seed, including the fixed zero input. It returns a value in
`[0,1]` and halts after a fixed finite number of queries. Section 4 proves

    sup_{v in F+} (E |H-S_T v(x*)|^2)^(1/2) <=5/32<1/4.      (U)

All constants are defined from the public class, never estimated using
unaccounted input evaluations. The algorithm is allowed to know `T`.

## 2. The small-mass amplitude bound holds for all finite s

The required inequality is

    A:=||v||_infinity <= C m^beta.                            (A)

It follows from the usual interpolation mechanism, but the following
finite-dimensional kernel proof makes the periodic and high-order
cases explicit. Let `Q=[-1/2,1/2]^d` and let `P_{s-1}` be the real
polynomials of total degree at most `s-1`. There is a polynomial `K` in
this space satisfying

    integral_Q K(y) p(y) dy = p(0)  for every p in P_{s-1}.

Indeed, the Gram matrix of the monomials in `L^2(Q)` is positive
definite: a polynomial with zero squared integral on this cube is the
zero polynomial. Solve this finite nonsingular system for the Riesz
representer of evaluation at zero. In particular, `integral K=1` and
all its moments of positive total degree below `s` vanish. This kernel
can be signed; positivity of the kernel is not required.

For an explicit bound, write `K(y)=sum_alpha c_alpha y^alpha` and set

    B=sum_alpha |c_alpha|*2^(-|alpha|),
    C=B*(1+(d/2)^s/s!).

Then `||K||_infinity<=B`, `||K||_1<=B`, and `B>=1`. The monomial
integrals on `Q` are rational, so these constants can be obtained from
a finite rational matrix computation depending only on `d,s`.

For `0<h<=1`, Taylor expansion on the periodic lift gives

    |v(x)-integral_Q K(y)v(x-hy)dy|
      <= B*(d/2)^s*h^s/s!.

The remainder uses only the given derivatives of total order `s`;
the vanishing moments cancel all lower-order terms. Nonnegativity of
`v` and injectivity, up to null boundaries, of the scaled cube in the
torus give

    |integral_Q K(y)v(x-hy)dy| <= B*h^(-d)*m.

Take `h=m^(1/(s+d))<=1` when `m>0`. The two bounds imply (A), with
the displayed `C`. When `m=0`, continuity and nonnegativity give
`v=0`, so (A) holds as well.

This resolves the proposed concern for `s>2`: the argument does not
assert that the function lies above its Taylor polynomial or that a
positive high-order averaging kernel exists. It uses a signed
polynomial-reproducing kernel and an absolute remainder estimate.

## 3. Uniform PDE reduction with actual error constants

Mass alone does not determine the finite-time nonlinear evolution.
For example, the spatial mean initially has derivative
`m-integral v^3`, which depends on more than `m`. The following
argument proves the approximation needed here instead of assuming
an exact reduction.

Fix `eta=1/64`. Choose `L>=1` with

    ||p_L-1||_infinity<=eta,                                 (M)

where `p_L` is the heat kernel for `(1/2)Delta` on the unit torus.
This is effective. One possible choice is

    L=max(1, log(8*d/eta)/(2*pi^2)).

To verify it, put `r=exp(-2*pi^2*L)<=eta/(8d)`. The Fourier series gives

    ||p_L-1||_infinity
      <= sum_{k in Z^d, k!=0} exp(-2*pi^2*|k|^2*L)
      <= ((1+r)/(1-r))^d-1
      <= exp(4*d*r)-1 <=eta.

The middle estimate uses `sum_{n>=1} r^(n^2)<=r/(1-r)`;
`log((1+r)/(1-r))<=4r` and `exp(eta/2)-1<=eta` apply for these
parameters. Consequently every nonnegative `v` satisfies

    (1-eta)m <= P_L v(x) <=(1+eta)m.                          (M1)

Choose the fixed positive threshold

    m0=min(1/2,
           [2*eta/(C^2*(exp(2L)-1))]^(1/(2*beta)),
           sqrt(eta)*exp(-L)/(1+eta)).                       (m0)

Also set the explicit time-one heat lower bound

    kappa=(2*pi)^(-d/2)*exp(-d/8),
    T*=max(L, 1+log(1/(kappa*m0*sqrt(eta)))).                 (T*)

The same nearest-Gaussian-translate argument as T44 proves
`p_1>=kappa>0`. These constants are fixed before receiving the input.

### 3a. Early cubic loss at mass at most m0

Comparison and the invariant interval give `0<=u(t)<=1`. Since
`u-u^3<=u`, linear comparison also gives

    u(t)<=exp(t)*P_t v<=A*exp(t).

Thus

    u_t-(1/2)Delta u >=[1-A^2*exp(2t)]u.

Compare with the solution of this linear equation with a spatially
constant potential. For every `0<=t<=L`,

    exp[t-A^2*(exp(2t)-1)/2]*P_t v <=u(t)<=exp(t)*P_t v.       (E)

This estimate includes the whole early nonlinear loss. If `m<=m0`,
(A) and (m0) make the loss exponent at `L` at most `eta`. Combining
(E), (M1), and `exp(-eta)(1-eta)>=(1-eta)^2>=1-2eta` gives

    w_-:=exp(L)*m*(1-2eta) <=u(L,x)
          <=exp(L)*m*(1+eta)=:w_+.

Both constants belong to `[0,sqrt(eta)]`. Scalar comparison for the
remaining time `S=T-L>=0` therefore yields

    ell_{w_-}(S)<=u(T,x)<=ell_{w_+}(S),
    ell_w(S)=w*exp(S)/sqrt(1+w^2*(exp(2S)-1)).                (B)

Put `z=exp(T)*m` and `c_-=1-2eta`, `c_+=1+eta`. Then

    ell_{w_+}(S)
      =Psi(c_+ z)*[1-w_+^2/(1+c_+^2*z^2)]^(-1/2)
      <=Psi(c_+ z)+eta,
    ell_{w_-}(S)>=Psi(c_- z).

For the first bound use `w_+^2<=eta`, `0<=Psi<=1`, and
`(1-t)^(-1/2)-1<=t` for `0<=t<=eta<=1/4`. For every `z>=0` and
`c>=0`, concavity and `Psi(0)=0` give the anchored estimate

    |Psi(cz)-Psi(z)|<=|c-1|*z/sqrt(1+z^2)<=|c-1|.            (C)

Hence, uniformly in `x` and in all `T>=L`,

    |u(T,x)-Psi(exp(T)*m)|<=2eta  when m<=m0.                (S)

The argument also covers `m=0` directly, since both sides then vanish.

### 3b. Saturation above m0

For `m>=m0`, the nonnegative reaction implies

    u(1)>=P_1v>=kappa*m0=:c0.

For `T>=T*`, scalar comparison and the scalar formula give

    u(T,x)>=ell_{c0}(T-1)
             >=Psi(c0*exp(T-1))>=Psi(1/sqrt(eta)).

Also `exp(T)*m>=c0*exp(T-1)`, so the same lower bound holds for
`Psi(exp(T)*m)`. Both quantities are at most one. Therefore

    |u(T,x)-Psi(exp(T)*m)|
      <=1-Psi(1/sqrt(eta))
       =1-(1+eta)^(-1/2)<=eta/2.

Together with (S), this proves (P), since `2eta=1/32`. In particular,
repeating this construction with smaller `eta` proves the genuinely
uniform asymptotic statement

    sup_{v in F+} ||S_T v-Psi(exp(T)*integral v)||_infinity ->0.

The fixed `L` is a proof parameter, not an uncharged burn-in oracle.
The actual large-horizon algorithm never evaluates `u(L,.)`.

## 4. Sampling the mass at the matching query scale

For iid uniform point values,

    E mhat=m,
    Var(mhat)=Var(v(X_1))/n
                <=integral v^2/n<=A*m/n<=C*m^(1+beta)/n.     (V)

Let `Z=exp(T)*mhat` and `z=exp(T)*m`. For `z>0`, concavity and
monotonicity of `Psi` imply, for every `x>=0`,

    |Psi(x)-Psi(z)|<=|x-z|*Psi(z)/z
                     =|x-z|/sqrt(1+z^2).                   (L)

For `x<=z`, use `Psi(x)>=(x/z)Psi(z)`; for `x>=z`, use
`Psi(x)<=(x/z)Psi(z)`. This is a global estimate anchored at the
true `z`, including the event that every sample value is zero.
No event splitting, unknown-mass-dependent sample count, or relative
accuracy guarantee for arbitrarily tiny `m` is needed.

Applying (V) and (L) gives

    E |Psi(Z)-Psi(z)|^2
      <= C*exp(gamma*T)/n * z^(1+beta)/(1+z^2)
      <= C*exp(gamma*T)/n <=1/64.

Indeed, `z^(1+beta)/(1+z^2)<=1`: use `z<=1` and `z>=1`
separately, with `0<beta<1`. If `z=0`, then `v=0` and every sample
value is zero, so the same conclusion holds exactly.

Minkowski's inequality and (P) now prove

    (E |H-S_Tv(x*)|^2)^(1/2) <=1/8+1/32=5/32.

This is the promised uniform bound (U). The substitution of `mhat`
into a nonlinear sigmoid introduces bias; no unbiasedness assertion
is made or needed by T44's error criterion.

## 5. Bounded horizons and the meaning of matching

The asymptotic result already matches T44 for `T>=max(T*,T44's T0)`.
If an algorithm for every `T>=0` is required, the bounded interval
`[0,T*]` can be filled without a PDE oracle using the already validated
constant-rate-two ternary voting construction from 04n/T32: degree-three
Bernstein coefficients `(0,1/2,1,1)` and Bernoulli initial-data leaves
give a bounded root with mean `u(T,x*)`. Its mean total node count is
at most

    B*=(3*exp(4T*)-1)/2.

For a deterministic query cap, abort a root and return zero if it would
require more than `M=ceil(16 B*)` nodes. Couple it to the original root.
Markov's inequality bounds its bias by `B*/M<=1/16`. Average 16
independent capped roots. Their range `[0,1]` bounds the RMS fluctuation
by `1/8`, so the final RMS is at most `3/16`. Data queries are at most
`16M`, a fixed constant depending on `d,s`. This is only a completeness
device for bounded times; the large-time algorithm above uses sample
averages alone. No efficiency claim is based on this very large constant.

Thus the upper query cap is `O(exp(gamma*T))` for all horizons after
enlarging its constant, while T44 gives the matching asymptotic lower
bound even on the fixed zero oracle for any uniformly accurate algorithm.
This determines the exponent in this fixed-precision, fixed-class
query model. It does not determine the best constants, joint dependence
on dimension or accuracy, or complexity under additional input promises.

## 6. Falsification checks and remaining scope

- **High smoothness and positivity.** The kernel can be signed; no
  invalid positive high-order kernel or Taylor lower bound is used.
  Positivity enters through `||v||_1=m` and `integral v^2<=A*m`.
- **Finite-time mass sufficiency.** It is false in general. The proof
  gives an explicit uniform approximation after `T*`, including early
  nonlinear loss and a separate large-mass saturation argument.
- **Unseen rare bumps.** They are included in (V) and (L), even when
  `mhat=0`. The sample count has exactly the order forced by T44.
- **Uncharged evolved values or derivatives.** None are queried. The
  class derivative bound is public; the algorithm samples only `v`.
- **Expected versus worst-case count.** The large-time count is exactly
  `n`; the optional bounded-time completion is explicitly capped. The
  lower bound covers the larger class with finite expected count and
  adaptive stopping, so the comparison is in compatible models.
- **All-zero or constant-input promise.** Such a smaller promise makes
  the task easier. This algorithm is uniformly accurate over unknown
  spatial inputs and pays its full public sample budget on zero.
- **Sign-changing data.** Not covered. A small signed mass need not
  imply a small amplitude, and both positivity arguments can fail.
- **Practical or unbiased branching gains.** Not established. The
  method is a biased large-time approximation, and `T*` and the constants
  are conservative. It is a query-complexity upper bound, not evidence
  of a faster implemented PDE solver or a new unbiased representation.

No mathematical proof gap remains in the conventional derivation above;
independent review is the next gate. No numerical check could substitute
for the uniform PDE estimate or the information-model comparison.

## 7. Primary-literature overlap and bounded search

[Nirenberg, *On elliptic partial differential equations* (1959),
Lecture II, pp. 124–126, interpolation theorem and bounded-domain
remark 5](https://www.numdam.org/item/ASNSP_1959_3_13_2_115_0.pdf), is
direct prior for the interpolation mechanism. The exponent in (A) is
classical. Section 2 gives an independent periodic kernel proof with
explicit finite constants rather than relying on an unstated endpoint
or bounded-domain version of that theorem.

[Kunsch–Rudolf, *Optimal confidence for Monte Carlo integration of smooth
functions*, Section 3.1, Remark 3.3, and Section 3.2, Theorem
3.5](https://arxiv.org/pdf/1809.09890), discusses iid integration bounds
and exploiting smoothness by approximation and variance reduction.
The point-query model and these generic tools are established. Its
inspected results do not supply the present positive-mass-dependent
PDE bound; ordinary smooth-integration rates alone do not prove the
sigmoid sampling estimate used here.

[Gajek–Niemiro–Pokarowski, *Optimal Monte Carlo integration with fixed
relative precision*, publisher Abstract and Section 0
excerpt](https://www.sciencedirect.com/science/article/pii/S0885064X12000805),
studies positive means that can approach zero and adaptive sampling for
uniform relative precision. Only publisher abstract/introduction text
was retrieved, so no full-paper theorem or cost constant is imported.
Our criterion
is absolute error after a saturating transformation, including zero,
which permits a fixed sample size depending on `T` and the class.

[Hairer–Lê–Rosati, *The Allen–Cahn equation with generic initial datum*,
equation (1.5), Theorem 1.1, and Proposition
4.6](https://arxiv.org/pdf/2201.08426), is close conceptual prior for
linear growth near zero followed by the nonlinear ODE profile
`z/sqrt(1+z^2)`. Its theorem concerns rapidly mixing Gaussian initial
fields on unbounded space, scaling limits, and front formation. It is
not the uniform deterministic nonnegative torus statement (P) or a
point-query complexity theorem. The nonlinear transition profile itself
is explicitly present in that prior work and is not new here.

The search did not locate the exact fixed-class matching query theorem.
This does not establish novelty: interpolation, Monte Carlo integration,
and the Allen–Cahn transition profile are known ingredients, and the
simple torus application may appear under other terminology. The proof
and its matching claim within the specified model do not depend on a
priority assessment.

The 17 purposeful queries were:

1. `nonnegative integration smooth functions randomized complexity positive integrands Gagliardo Nirenberg small integral`
2. `Allen Cahn equation small initial data torus long time unstable equilibrium mean asymptotic`
3. `"nonnegative" "integration" "randomized" "relative error" smooth functions`
4. `"positive functions" "randomized" "integration" complexity`
5. `Nirenberg 1959 On elliptic partial differential equations interpolation inequality pdf`
6. `"Allen-Cahn" "small initial" "ODE"`
7. `"Monte Carlo" "nonnegative functions" "smoothness" integration`
8. `"integration" "relative error" "smooth" "nonnegative"`
9. `"randomized integration" "positive" "small"`
10. `"Allen-Cahn equation with generic initial datum" arxiv`
11. `"Optimal Monte Carlo integration with fixed relative precision" pdf`
12. `"Allen-Cahn" "torus" "small" "mean" initial data ODE approximation`
13. `"reaction diffusion" "small initial data" "bounded domain" "unstable" asymptotic`
14. `Gajek Niemiro Pokarowski "Optimal Monte Carlo" filetype:pdf`
15. `"nonnegative" "smooth functions" "Monte Carlo" "integral"`
16. `"Allen-Cahn" "nonnegative initial" "asymptotic"`
17. `"reaction-diffusion" "initial mass" "logarithmic" "bounded domain"`

Primary-paper opens and in-document searches followed these queries.
Search snippets from secondary pages were only used to locate primary
sources, not to support the mathematical verdict.
