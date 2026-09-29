# Candidate exact point-query lower bound near an unstable phase

Status: conventionally proved and independently passed in T41, with T40
independently deriving a compatible theorem and auditing primary predecessors.
The explicit oracle/quantifier/threshold clarifications are integrated below.
No complete Lean, numerical, optimal-exponent or publication-priority claim.
This is a stronger oracle-model question than the fixed-tree obstruction, but
it does not cover algorithms given an initial function's formula/source code.

## Proposed statement and actual information model

Fix d>=1 and an integer s>=1. On the unit flat torus consider

    u_t = (1/2) Delta u + u - u^3,   u(0)=v.

Use the fixed input class of smooth periodic real functions satisfying

    max_{|alpha|<=s} ||partial^alpha v||_infinity <=1,
    ||v||_infinity <=1/2,
    v takes both strictly positive and strictly negative values.

Only derivatives through the fixed finite order s have uniform bounds; there
is no common analytic radius or bound on all derivatives. Higher derivatives
of hard inputs can grow with T. Let S_T v(x*) be the solution at one fixed
query point. The algorithm knows the PDE, d,s,T,class and x*. It may adaptively
choose arbitrary points and receive exact deterministic values v(x), use
internal randomness, stop adaptively and return a biased or unbiased real
estimate H. It cannot inspect the unknown input's formula, source, integral,
Fourier coefficients or evolved solution except through those point queries.
Scalar arithmetic is free for this lower bound. Count initial-data queries Q.

There are constants C>0,T0 depending only on d,s and a fixed bump,
such that any such algorithm with

    sup_v E |H(v)-S_T v(x*)|^2 <=1/16

has, for every T>=T0, a smooth sign-changing input g_T in the same fixed class
with

    E Q(g_T) >= C exp(d T/(s+d)).

The quantifier order is: fix d,s,x*; choose C,T0 and the family g_T; then for
EVERY T>=T0 and EVERY admissible algorithm A_T with the uniform MSE premise,
the displayed baseline cost bound holds. The algorithm may depend on T and
on the entire public problem description, including the hard-family formulas.
It is not promised which member the unknown oracle represents.

Private randomness is a common seed on an input-independent probability
space. Measurable rules on the finite transcript and seed choose the next
query or halt with a measurable real output. A standard Borel seed space
and Borel rules give one concrete interface. Oracle metadata, evaluation
side information and uncharged input-dependent preprocessing are excluded;
every initial-data evaluation is counted. Almost-sure finite halting is
required on the promised class. At each fixed T only2K+1 input runs are
coupled, so their exceptional null sets may be removed simultaneously.

This is a worst-case-in-input bound for each T; the hard inputs depend on T.
It does not say one fixed profile becomes increasingly difficult. Infinite
expected query cost already satisfies the conclusion. For the nontrivial
case assume a.s. termination and finite expected Q on g_T. Exact values are
essentially stronger than noisy coins; no coin-oracle substitution is used.

## Fixed smooth bump and time-dependent hard family

Fix psi in C_c^infinity((0,1)^d), 0<=psi<=1, with

    I = integral psi >0,
    D = max(1,max_{|alpha|<=s} ||partial^alpha psi||_infinity),
    a =1/(8D),  q=s+d.

At time1 the periodized unit-covariance Gaussian heat kernel has lower bound

    kappa = (2*pi)^(-d/2) exp(-d/8)>0.

For each pair of torus points choose its nearest integer translate, with
coordinate differences in[-1/2,1/2]; its single Gaussian term supplies this
lower bound. Other periodized terms are nonnegative.

Take the explicit threshold

    T0=max(1,1+q*log(4)-log(kappa*a*I)).

For T>=T0, R_T=(kappa*a*I*exp(T-1))^(1/q)>=4. Set

    k=floor(R_T),  K=k^d,  mu=a*I*k^(-q).

Partition the torus into K half-open cubes of side1/k. Each cube j contains a
smooth bump

    b_j(x)=a*k^(-s)*psi(k*x-j)

extended by zero outside the cube. Compact support inside the cube makes
this extension smooth and periodic. Every bump has mass mu and C^s norm
at most1/8. Its maximum value is at most1/8. The floor bounds give

    R_T/2 <=k<=R_T,
    1 <= kappa*mu*exp(T-1) <=2^q.

Set D_s=max(1,(2*pi)^s) and

    delta = kappa/(32*e*2^q*D_s),
    g_T(x)=delta*mu*sin(2*pi*x_1),
    v_{j,+}=g_T+b_j,  v_{j,-}=g_T-b_j.

Then

    exp(T)||g_T||_infinity <=1/(32D_s)<=1/32,
    ||g_T||_{C^s,max} <= exp(-T)/32.

For T>=1 all g_T and v_{j,+/-} lie strictly inside the displayed norm/range
bounds. Because k>=4, the complement of any one cube contains points where
sin(2*pi*x_1) is strictly positive and strictly negative. Hence all these
functions, including the baseline g_T, are genuinely sign-changing.
Outside cube j both v_{j,+} and v_{j,-} equal exactly the same known baseline
function g_T. This exact transcript equality is the information bottleneck.

## Heat spreading followed by unstable amplification

For nonnegative b_j<=1/8, comparison gives 0<=S_t b_j<=1. On this interval
f(u)=u-u^3>=0, so the mild equation yields

    S_1 b_j(x) >= P_1 b_j(x) >= kappa*mu.

Scalar comparison for the remaining T-1 time units yields

    S_T b_j(x) >= ell_{kappa*mu}(T-1),
    ell_c(t) = c*exp(t)/sqrt(1+c^2*(exp(2t)-1)).

Let B=kappa*mu*exp(T-1)>=1. Since c<=1,

    ell_c(T-1) >= B/sqrt(1+B^2) >=1/sqrt(2).

Oddness gives S_T(-b_j)=-S_T(b_j). For any two solutions in[-1,1], their
difference solves a linear equation whose potential is

    1-(u^2+u*v+v^2) <=1.

The maximum principle therefore gives the one-sided-Lipschitz stability bound

    ||S_T(v+w)-S_T(v)||_infinity <=exp(T)||w||_infinity.

The proof uses the upper bound on the potential for both signs of the
difference; it does not incorrectly replace it by an absolute derivative
bound of1. Consequently, for every j and x*,

    S_T v_{j,+}(x*) >=1/sqrt(2)-1/32 >1/2,
    S_T v_{j,-}(x*) <=-1/sqrt(2)+1/32 <-1/2.

This argument avoids a closed evolution equation for the spatial mean and
does not discard nonlinear mean corrections.

## Adaptive randomized transcript lower bound

Couple the algorithm across all inputs by the same internal random seed.
Run it on baseline g_T and let J(seed) be the set of cubes visited by its
queries before stopping. A query belongs to at most one half-open cube, so

    |J(seed)| <= Q(g_T,seed).

For j outside J, induction over adaptive queries shows the full transcript,
stopping decision and returned H are identical on g_T,v_{j,+},v_{j,-}.
The two exact solution values have separation at least1. Thus, on this no-hit
event, the average of the two squared losses is at least1/4, for every real
returned H. Nonnegativity allows us to ignore all hit events. Average over
uniform j, the two signs and the random seed, using Tonelli:

    average_{j,+/-} E|H(v_{j,+/-})-S_T v_{j,+/-}(x*)|^2
      >= (1/4)*(1-E|J|/K)
      >= (1/4)*(1-E Q(g_T)/K).

The uniform1/16 MSE premise implies E Q(g_T)>=3K/4. Therefore

    E Q(g_T) >= (3/4)*2^(-d)*(kappa*a*I/e)^(d/q)*exp(d*T/q).

No likelihood differentiation, unbiasedness, fixed stopping horizon, finite
variance beyond the MSE premise, or independence of stopping from returned
values is assumed. Adaptive random seeds are coupled only before an input
can be distinguished. A complete proof must state measurability and halting
interfaces; this candidate is not an implemented oracle-complexity library.

## Boundaries, overlap and next gate

The hard family has shrinking mass and approaches the unstable phase. It is
outside D19's fixed strictly positive basin and D21's fixed positive mass
certificates. It creates no contradiction with their uniform work bounds.
The bound is not for the fixed known cosine profile or for algorithms given
symbolic descriptions. It is not a lower bound for arbitrary preprocessing
that already encodes the unknown input, alternative query oracles, or a
single fixed profile. It concerns absolute solution RMS and should not be
silently relabelled as relative defect error.

T40 verifies direct primary precedents: [Kunsch–Rudolf, Section2.1,
Lemmas2.1–2.2 and Theorem2.3](https://arxiv.org/pdf/1809.09890) for adaptive
information and norm-scaled disjoint bumps; [Kwas, Sections3.2 and8.1](https://arxiv.org/pdf/quant-ph/0410134)
for expected exact-value query cost and PDE reductions; and
[Petras–Ritter, Section4.3, Theorem4/Corollary2](https://drops.dagstuhl.de/storage/16dagstuhl-seminar-proceedings/dsp-vol04401/DagSemProc.04401.10/DagSemProc.04401.10.pdf)
for parabolic lower bounds with higher-order control.

The hidden-bump/disjoint-support argument is classical information-based
complexity material. The PDE-specific transfer through positivity and
unstable amplification may also be known; T40 must compare primary sources.
No novelty or optimal exponent is claimed. The exponent d/(s+d) is only this
construction's sufficient lower bound, not a matching minimax classification.
T41 passed the conventional proof; the next fixed formal contract05g targets
the genuine integral information inequality and finite adaptive transcript
induction. The heat/PDE/bump bridges remain conventional unless separately
formalized. No numerical lower-bound proof can replace these arguments.
