# D23: a fixed zero input can have increasing query cost

Conventional status: accepted after the independent T44/T45 proofs and
constant/oracle audits. This is a separate nonnegative input class from
D22. The information argument is classical in form; neither priority nor
optimality is inferred here. T46 investigates a matching upper bound.

## Allen–Cahn theorem

Fix positive integers d,s and a point x* on the unit torus. Let S_T denote
the solution of u_t=Delta u/2+u-u^3. The fixed promised input class is

    F+={v smooth and periodic: 0<=v<=1/2,
        max_{|alpha|<=s} ||partial^alpha v||_infinity<=1}.

Only these finitely many derivative orders are bounded uniformly. The
algorithm receives only exact values of the unknown initial function at
chosen points. It has an input-independent private seed, measurable finite
transcript rules, and almost-sure finite halting on F+. Every input-dependent
evaluation, including preprocessing, counts. Labels, formulas, source code,
integrals and other input-dependent side information are unavailable.
Adaptive queries/stopping, horizon-dependent algorithms, bias and unbounded
real outputs are allowed. Infinite expected baseline cost already satisfies
the conclusion. Scalar arithmetic and private randomness are free.

For each fixed epsilon in (0,1/(2sqrt(2))), there are constants
C_epsilon>0 and T0 such that, for every T>=T0 and every such algorithm,

    sup_(v in F+) E|H_T(v)-S_Tv(x*)|^2 <= epsilon^2
      implies E Q_T(0) >= C_epsilon exp(d*T/(s+d)).

The baseline here is the same zero function at every horizon. The hidden
alternative inputs depend on T. The accuracy premise is uniform on F+;
being told that the input is zero would define a different problem with a
zero-query solution. Zero is outside D22's sign-changing class.

Use 04o's fixed bump psi, I=integral psi, derivative bound D, a=1/(8D),
q=s+d, and kappa=(2*pi)^(-d/2)exp(-d/8). Explicitly,

    T0=max(1,1+q*log(4)-log(kappa*a*I)),
    k=floor((kappa*a*I*exp(T-1))^(1/q)), K=k^d,
    C_epsilon=(1-8epsilon^2)*2^(-d)*(kappa*a*I/e)^(d/q).

At epsilon=1/4 the finite lower bound is E Q_T(0)>=K/2. Constants are
independent of T and the algorithm; the general prefactor depends on
epsilon as its formula shows.

## Proof and why repeated zero is legitimate

Place b_j=a*k^(-s)*psi(kx-j) inside each of the K half-open cells and extend
by zero. Every b_j lies in F+, has mass mu=aI*k^(-q), and has derivatives
through order s bounded by 1/8. Time-one heat minorization and nonnegative
reaction give S_1 b_j>=kappa*mu. The exact scalar Allen–Cahn flow then gives

    S_T b_j(x*)>=ell_(kappa*mu)(T-1)>=1/sqrt(2),
    S_T0=0.

For a fixed common seed, let J be the cells queried along the zero run.
Then |J|<=Q_T(0). If j is absent from J, finite induction on the actual
adaptive transcript shows that the run on b_j has the same queries,
responses, stopping decision and output as the zero run. On that event,
with common output y and target a_j>=1/sqrt(2),

    ((y-a_j)^2+y^2)/2 >= a_j^2/4 >=1/8.

Average over j and the seed, retaining nonnegative losses elsewhere:

    (1/(2K))*sum_j Risk(b_j) + Risk(0)/2
       >=(1/8)*(1-E Q_T(0)/K).

Uniform accuracy bounds the left side by epsilon^2. It is the risk of a
finite prior with mass 1/2 at zero and 1/(2K) at each bump. Reusing the same
zero output is an algebraic average, with no independence assumption.
The floor estimate k>=R/2 gives the displayed exponential bound. The full
measurability and null-set handling is in T44/T45; no optional stopping or
coin-oracle substitution is used.

## Controlled reaction extension

Fix b>0, L>0 and f in C^2([0,b]) with f(0)=f(b)=0, f>0 on (0,b), and
f'(0)=lambda>0. Replace F+ by the fixed class with range [0,b/2] and
C^s,max norm at most L. A strictly positive L is necessary. Choose the
bump coefficient 0<a<=min(b/2,L/D). For a fixed theta in (0,b), set

    J_theta=integral_0^theta |1/f(y)-1/(lambda*y)| dy,
    B_theta=theta*exp(lambda*J_theta).

The C^2 Taylor estimate makes J_theta finite. The exact scalar hitting
time satisfies tau(c,theta)<=lambda^(-1)log(B_theta/c). Thus, with

    T0_theta=max(1,1+(q*log(4)+log(B_theta)-log(kappa*a*I))/lambda),
    k=floor((kappa*a*I*exp(lambda*(T-1))/B_theta)^(1/q)),

the bump targets are at least theta for T>=T0_theta. The same risk argument
yields

    E Q_T(0)>=(1-4epsilon^2/theta^2)*k^d
       >=C_(theta,epsilon)*exp(lambda*d*T/q),
    C_(theta,epsilon)=(1-4epsilon^2/theta^2)*2^(-d)
        *(kappa*a*I*exp(-lambda)/B_theta)^(d/q).

This is positive for epsilon<theta/2. Every fixed epsilon<b/2 admits a
choice theta in (2epsilon,b); at epsilon>=b/2 the constant output b/2
already suffices. These constants depend on the fixed reaction and other
displayed parameters, not only on lambda. No C^1-only or sign-changing
general-reaction extension is asserted.

## Boundaries and evidence

D21's uniform-work theorem requires a known positive lower mass for the
initial function. Zero violates it, and the bumps' suprema tend to zero,
so no probability measure supplies a common positive mass certificate for
these alternatives. The two statements are compatible.

T42's general paired-loss integral inequality and T43's evaluator no-hit
theorem apply to the information core. A specialized irrational-gap
corollary, general algorithm encoding, heat/PDE comparison and bump
membership have not been joined into an end-to-end Lean theorem. The C^2
extension is conventional only. Numerical examples cannot verify the
universal oracle quantifiers.

Frozen detailed evidence: reviews/T44-zero-baseline-corollary.md, SHA256
124d2c2152fb8ce1f8edd8585ce38ee3739a69892c6769a856be42d85b0f6d29;
reviews/T45-zero-baseline-independent-audit.md, SHA256
adee6286ee36102e55a45ca968a03b99cfe5fb4420e87e24658529c1a2224b19.
