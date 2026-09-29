# Root draft: general C2 positive-class query complexity

Status: candidate for a separate independent theory audit. Not an accepted
claim, Lean target or numerical protocol. This extends the question in04p
and04q; it does not alter their frozen supporting reports. No novelty is
asserted. The derivations below must be independently checked before use.

## Candidate statement

Fix b>0, a positive C^s norm radius R, integers d,s>=1 and a fixed reaction
f in C^2([0,b]) with f(0)=f(b)=0, f>0 on (0,b), lambda=f'(0)>0. Consider
u_t=Delta u/2+f(u) on the unit torus and the fixed class

    F={v smooth periodic: 0<=v<=b/2, ||v||_(C^s,max)<=R}.

Only opaque exact initial-value point queries are charged; all preprocessing
that depends on the unknown v is charged, and no mass or evolved-value
oracle is supplied. Fixed f and public scalar preprocessing are discussed
explicitly below. For every fixed epsilon in (0,b/2), the proposed minimax
expected-query order, as T tends to infinity, is

    Theta(exp(lambda*d*T/(s+d))).

The lower half is already conventional D23. The candidate upper half is a
biased sample-mean algorithm using the reaction's normalized scalar flow
profile. It is not a new unbiased branching representation. All constants
may depend on f,b,R,d,s,epsilon; no uniformity over reactions with the same
lambda, variable accuracy, bit cost or practical speed is asserted.

## 1. Exact scalar coordinate and its profile

Let M=max(1,||f''||_infinity), Lambda=lambda+M*b/2 and Fmax=Lambda*b.
Taylor's theorem gives |f(y)-lambda*y|<=M*y^2/2 and f(y)<=Lambda*y.
For 0<y<b set

    r(y)=1/f(y)-1/(lambda*y),
    G(y)=y*exp(lambda*integral_0^y r(t)dt).

Near zero, f(y)>=lambda*y/2 for y<=lambda/M and consequently
|r(y)|<=M/lambda^2. Thus G(y)/y tends to1. Direct differentiation gives

    G'(y)/G(y)=lambda/f(y)>0.

As y tends to b, integral dy/f(y) diverges: bounded f' and f(b)=0 imply
f(y)<=||f'||_infinity*(b-y). Hence G maps (0,b) increasingly onto (0,infinity).
Define Phi=G^(-1), with Phi(0)=0. Then Phi maps [0,infinity) to [0,b),
Phi(z) tends to b, Phi'(0)=1, and

    Phi'(z)=f(Phi(z))/(lambda*z), z>0,
    ell_c(t)=Phi(exp(lambda*t)*G(c)), 0<c<b.

The last identity follows by differentiating G along the exact scalar
ODE; it is not a linearized approximation at order-one amplitude.

## 2. A global anchored profile estimate without concavity

Set r0=min(b/2,lambda/M)>0. On 0<y<=r0, G(y)>=exp(-1)*y and
f(y)<=3lambda*y/2. For y>=r0, G(y)>=G(r0)>=exp(-1)*r0 and f(y)<=Fmax.
Thus Phi has a global Lipschitz bound

    Lphi=max(3e/2, e*Fmax/(lambda*r0)).

Its derivative also satisfies z*Phi'(z)<=Fmax/lambda. Define

    Dphi=Fmax/lambda,
    Kphi=max(2Lphi,4b,4Dphi).

Claim, for all x,z>=0:

    |Phi(x)-Phi(z)|<=Kphi*|x-z|/(1+z).              (A)

If z<=1, use the global Lipschitz bound and 1+z<=2. If z>1 and
x<=z/2, use the range bound b and |x-z|>=z/2. If z>1 and x>=z/2,
every point between x and z is at least z/2, so the derivative is at most
2Dphi/z. In both latter cases (1+z)/z<=2. This proves (A) without a
KPP inequality f(y)<=lambda*y, a simple stable root at b, or concavity of
Phi. In particular |Phi(qz)-Phi(z)|<=Kphi*|q-1| for q,z>=0.

## 3. Fixed-class height-versus-mass bound

Let beta=s/(s+d), gamma=1-beta and m=integral v. The polynomial kernel K
and its coefficient bound B from04q give, for 0<h<=1,

    ||v||_infinity<=B*h^(-d)*m + B*R*(d/2)^s*h^s/s!.

For 0<m<=1 take h=m^(1/(s+d)); for m>=1 use ||v||_infinity<=b/2;
for m=0 positivity gives v=0. Thus one valid public constant is

    C=max(1,b/2,B*(1+R*(d/2)^s/s!)),
    ||v||_infinity<=C*m^beta.                      (H)

The signed-kernel proof uses only the derivatives through s and
nonnegativity. No uniform positive mass is promised.

## 4. Uniform nonlinear PDE reduction

For the initially proposed ideal-profile error budget let

    eta=min(1/16,epsilon/(8Kphi)),
    L=max(1,log(8d/eta)/(2*pi^2)),
    csmall=min(b/2,eta*lambda/M),
    Efac=M*C*(exp(Lambda*L)-1)/(2Lambda),
    m0=min(b/2,1,(eta/Efac)^(1/beta),csmall*exp(-lambda*L)/2).

Every constant is finite and strictly positive. The torus Fourier bound
gives ||p_L-1||_infinity<=eta. If A=||v||_infinity, then u(t)<=A exp(Lambda*t).
Since |f(y)/y-lambda|<=M*y/2, comparison with spatially constant potentials
gives the actual PDE bounds

    exp(lambda*t-E(t))*P_t v<=u(t)<=exp(lambda*t+E(t))*P_t v,
    E(t)=M*A*(exp(Lambda*t)-1)/(2Lambda).

For m<=m0, (H) ensures E(L)<=eta. Hence

    c-=exp(lambda*L)*m*(1-eta)*exp(-eta)<=u(L)
       <=exp(lambda*L)*m*(1+eta)*exp(eta)=c+.

For eta<=1/16, (1+eta)exp(eta)<2, so c+<=csmall. On [0,csmall],
|lambda*integral_0^c r|<=M*c/lambda<=eta. Consequently the scalar
comparison at later T>=L places u(T) between Phi(q-*z) and Phi(q+*z),
where z=exp(lambda*T)*m and

    (1-eta)*exp(-2eta)<=q-<=q+<=(1+eta)*exp(2eta).

The lower endpoint is at least1-3eta and the upper endpoint at most1+4eta.
For the latter, the derivative of (1+t)exp(2t) on [0,1/16] is
exp(2t)(3+2t)<4. Thus |q+-1|,|q--1|<=4eta, and (A) yields

    ||S_Tv-Phi(exp(lambda*T)*m)||_infinity<=4Kphi*eta<=epsilon/2

for all small-mass inputs and T>=L. At m=0 both sides vanish.

For m>=m0, nonnegative reaction and heat minorization give
u(1)>=kappa*m0=:c0>0, with kappa=(2*pi)^(-d/2)exp(-d/8). Let
theta=b-epsilon/2. A sufficient class-uniform threshold is

    T*=max(L,
       1+lambda^(-1)*log(G(theta)/G(c0)),
       lambda^(-1)*log(G(theta)/m0)).

Then both u(T) and Phi(exp(lambda*T)*m) lie in [theta,b] for T>=T*,
so their difference is at most epsilon/2. The mass split is used only
in the proof, never by the algorithm. This proposes a genuinely uniform
PDE approximation for all v in F, including arbitrarily small masses.

## 5. Matching point-sampling risk

Query n independent uniform points and form the actual sample mean mhat.
Its variance is at most C*m^(1+beta)/n. By (A), with z=exp(lambda*T)*m,

    E|Phi(exp(lambda*T)*mhat)-Phi(z)|^2
       <= Kphi^2*C*exp(lambda*gamma*T)/n
            * z^(1+beta)/(1+z)^2
       <= Kphi^2*C*exp(lambda*gamma*T)/n.

The ratio is at most1 for 0<beta<1. Choosing
n=ceil(4*Kphi^2*C*epsilon^(-2)*exp(lambda*gamma*T)) bounds sampling RMS
by epsilon/2. Together with the ideal-profile PDE bias, this gives RMS
at most epsilon, with deterministic query count on every input.

This is the core ideal-profile statement. The next section tightens all
three error budgets before claiming an ordinary finite scalar evaluation.

## 6. Scalar preprocessing and implementability must be explicit

Saying that evaluating an arbitrary fixed C2 profile costs no initial-data
queries does not mean an unknown profile is supplied as an extra oracle.
For an ordinary finite-table version, allocate epsilon/3 separately to
PDE bias, sampling RMS and uniform scalar approximation. Reuse Sections
4–5 with eta=min(1/16,epsilon/(12Kphi)), theta=b-epsilon/3, and sample
size n=ceil(9*Kphi^2*C*epsilon^(-2)*exp(lambda*gamma*T)).

Choose a public finite zmax with Phi(zmax)>=b-epsilon/6. On [0,zmax],
use a grid with mesh at most epsilon/(6Lphi), storing rational values
within epsilon/6 of the exact Phi at the left endpoints. Return the
stored left-endpoint value (clipped to [0,b]) for z<zmax and a public
value within epsilon/6 of b for z>=zmax. The pointwise scalar error is
then at most epsilon/3 everywhere. The table is finite and independent
of the unknown v and of T; all v-dependent evaluations remain the n
charged initial queries. The three errors add by the L2 triangle inequality.

For a fixed f, such a finite table exists, which is enough for the usual
nonuniform information-complexity upper bound. Uniformly constructing it
from a supplied representation of arbitrary f requires effective access
to f and certified public bounds; no such computability assumption should
be hidden. If f is given through computable evaluation with the stated
effective C2 bounds, scalar integration/root finding can in principle
construct this input-independent table to the required fixed accuracy.
That last computability assertion requires separate specification if used
as a uniform algorithmic theorem. No profile table has been computed here.

## 7. Audit questions and attribution

The independent review should verify: inverse-coordinate endpoints;
global anchor constants without concavity; early nonlinear potential;
all positivity/range/threshold details; absence of an input mass oracle;
compatibility of the fixed epsilon lower bound in04p; and the distinction
between a nonuniform finite-table upper bound for fixed f and uniform
computability from an f oracle. It must also check that the norm radius R
is strictly positive and that the positive interval contains no extra roots.

Root performed five preliminary targeted searches; none supplied this
specific general matching theorem. Primary inspected conceptual prior is
Hairer–Lê–Rosati, *The Allen–Cahn equation with generic initial datum*,
Eq.(1.5), Theorem2.1 and Proposition4.6, https://arxiv.org/pdf/2201.08426.
That paper explicitly uses nonlinear ODE transition profiles for its
random-field scaling limit. It does not by itself establish the present
deterministic-class, arbitrary-C2 query statement. Scalar separation of
variables, interpolation, and iid integration are classical mechanisms.
No originality follows from this preliminary search or this draft.
