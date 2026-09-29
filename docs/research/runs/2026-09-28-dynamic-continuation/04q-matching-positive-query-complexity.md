# D24: matching large-time query complexity on the nonnegative class

Conventional theorem: T46 derives the constructive upper bound; T48
independently checks it. Together with D23/T44/T45 the large-time exponent
is matched on exactly the same fixed class, information model and fixed
absolute accuracy. This is not a priority, practical speed, relative-error,
unbiased branching, or bit-complexity claim.

## Statement and algorithm

Use the unit torus and Allen–Cahn equation from04p. Fix positive integers
d,s and the class F+ of smooth periodic functions with 0<=v<=1/2 and
C^s,max norm<=1. The only input-dependent information consists of exact
initial-value point queries. Put beta=s/(s+d), gamma=d/(s+d) and

    Psi(z)=z/sqrt(1+z^2), z>=0.

There are known finite constants C>=1 and T*, depending only on d,s,
such that for every T>=T* the following algorithm works uniformly on F+:

    n=ceil(64*C*exp(gamma*T));
    query v at n independent uniform torus points;
    mhat=the arithmetic mean of these n observed values;
    return Psi(exp(T)*mhat).

It uses exactly n queries on every input, including zero, and its absolute
RMS is at most 5/32 at every target point. The output is biased in general.
The algorithm does not query the actual spatial mean or any evolved value.

For every sufficiently large T, therefore,

    inf_(uniform RMS<=1/4 algorithms) sup_(v in F+) E Q_T(v)
       =Theta(exp(d*T/(s+d))).

The same order holds for the infimum of E Q_T(0) over that uniformly
accurate algorithm class, by the fixed-zero lower bound. The upper and
lower bounds use the maximum of their fixed time thresholds. Algorithms
with adaptive queries, random stopping and arbitrary bias are included in
the lower bound; the matching upper bound has a deterministic query count.
Only fixed precision and fixed d,s are asserted sharp.

## 1. A public height-versus-mass constant

Let m=integral v. On Q=[-1/2,1/2]^d, let K be the polynomial of degree at
most s-1 satisfying integral_Q K(y)p(y)dy=p(0) for every polynomial p of
that degree. The positive definite monomial Gram matrix constructs it from
rational entries. Write K=sum_alpha c_alpha y^alpha and set

    B=sum_alpha |c_alpha|*2^(-|alpha|),
    C=B*(1+(d/2)^s/s!).

Then B>=1 and C>=1. A Taylor remainder, the vanishing moments, and
nonnegativity of v give for every 0<h<=1

    ||v||_infinity <= B*h^(-d)*m + B*(d/2)^s*h^s/s!.

The scaled cube wraps injectively up to null boundaries, so no omitted
torus overlap factor occurs. Take h=m^(1/(s+d)) when m>0. When m=0,
v=0. Thus ||v||_infinity<=C*m^beta for the entire fixed class. The signed
kernel is allowed; no positive high-order kernel or all-order smoothness
bound is assumed. T48 also gives an independent compact-kernel derivation.

## 2. Uniform PDE approximation, not exact mass closure

Set eta=1/64 and choose the public constants

    L=max(1,log(8*d/eta)/(2*pi^2)),
    m0=min(1/2,
      (2*eta/(C^2*(exp(2L)-1)))^(1/(2*beta)),
      sqrt(eta)*exp(-L)/(1+eta)),
    kappa=(2*pi)^(-d/2)*exp(-d/8),
    T*=max(L,1+log(1/(kappa*m0*sqrt(eta)))).

The heat Fourier series proves ||p_L-1||_infinity<=eta. If m<=m0 and
A=||v||_infinity, actual parabolic comparison gives

    exp(t-A^2*(exp(2t)-1)/2)*P_t v <=u(t)<=exp(t)*P_t v.

At t=L this puts u(L) between e^L*m*(1-2eta) and e^L*m*(1+eta), both at
most sqrt(eta). Evolving these two constants by the exact scalar flow

    ell_c(t)=c*exp(t)/sqrt(1+c^2*(exp(2t)-1))

and retaining its finite-time denominator correction gives

    ||u(T)-Psi(exp(T)*m)||_infinity <=2eta, T>=L.

For m>=m0, heat minorization gives u(1)>=kappa*m0. At T>=T* both u(T)
and Psi(exp(T)*m) lie between Psi(eta^(-1/2)) and 1, so their separation
is at most eta/2. Together these estimates establish

    sup_(v in F+) ||S_Tv-Psi(exp(T)*integral v)||_infinity <=1/32

for every T>=T*. Finite-time nonlinear evolution is not determined by m;
the estimate is a uniform large-time approximation with its early cubic
loss controlled. No evolved-value oracle is hidden in this proof device.

## 3. Sampling risk

The actual iid sample mean satisfies

    E(mhat-m)^2 <= (integral v^2)/n <= C*m^(1+beta)/n.

For all x,z>=0 the scalar transform satisfies the anchored bound

    |Psi(x)-Psi(z)|<=|x-z|/sqrt(1+z^2).

It follows directly by monotonicity and comparing the two positive
denominators; it includes x=0 and thus also missed rare bumps. With
z=exp(T)*m,

    E|Psi(exp(T)*mhat)-Psi(z)|^2
      <=(C*exp(gamma*T)/n)*z^(1+beta)/(1+z^2)
      <=1/64.

Here 0<beta<1 ensures the displayed ratio is at most one. Minkowski then
gives total RMS<=1/8+1/32=5/32, completing the large-time upper bound.
No relative mean-estimation guarantee at arbitrarily small m is needed.

## Evidence and next gate

Detailed proof and source search: reviews/T46-positive-class-upper-bound.md,
SHA256 6ad43f33f45739a510ea6ea968041e4332762fa3c358773ce431c57ac9e93997.
Independent audit: reviews/T48-matching-upper-bound-audit.md. The accepted
claim here requires only large horizons; T46's optional capped-tree
completion of bounded horizons is separate from this asymptotic statement.

Interpolation, iid integration, and the same nonlinear transition profile
have primary predecessors listed in T46. The bounded search did not locate
this precise matching theorem, which does not establish novelty. Existing
T42/T43 formalize lower-bound information ingredients only. The new upper
bound's scalar transform, actual sample variance, transformed integral
risk and error composition are the next Lean targets. Its PDE and
interpolation inputs remain conventional until explicitly formalized.
No numerical implementation or experiment for this new algorithm has run.
