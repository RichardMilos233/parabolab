# D26: general C2 positive-class query complexity

Status: conventionally proved, independently audited in T54 and accepted
by root after reading the complete audit. The original R01 draft remains
unchanged; this version incorporates T54's finite public-advice repair.
No end-to-end Lean theorem, numerical experiment or novelty claim follows.

## Accepted statement

Fix b>0, a positive C^s norm radius R, integers d,s>=1 and a fixed reaction
f in C^2([0,b]) with f(0)=f(b)=0, f>0 on (0,b), lambda=f'(0)>0. Consider
u_t=Delta u/2+f(u) on the unit torus and the fixed class

    F={v smooth periodic: 0<=v<=b/2, ||v||_(C^s,max)<=R}.

Only opaque exact initial-value point queries are charged; all preprocessing
that depends on the unknown v is charged, and no mass or evolved-value
oracle is supplied. Fixed f and public scalar preprocessing are discussed
explicitly below. For every fixed epsilon in (0,b/2), the minimax
expected-query order, as T tends to infinity, is

    Theta(exp(lambda*d*T/(s+d))).

The lower half is conventional D23. The constructive upper half is a
biased sample-mean algorithm using the reaction's normalized scalar flow
profile. It is not a new unbiased branching representation. All constants
may depend on f,b,R,d,s,epsilon; no uniformity over reactions with the same
lambda, variable accuracy, bit cost or practical speed is asserted.

The minimax infimum permits a separate algorithm for each public horizon.
Its public finite advice may depend on f,b,R,d,s,epsilon,T but never on
the unknown v. This is a nonuniform query-complexity theorem, not a single
uniformly computable procedure for an arbitrary unrepresented reaction.
For every sufficiently large T, the lower bound applies to every algorithm
with the class-uniform error guarantee; the upper bound provides one such
algorithm with a deterministic number of charged initial point queries.

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

For the intermediate ideal-profile error budget let

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
in the proof, never by the algorithm. This proves a uniform
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

## 6. Finite public advice and scalar approximation

For the final oracle procedure allocate epsilon/3 separately to PDE bias,
sampling RMS, and all scalar approximation. Recompute Section4's m0,T*
using eta=min(1/16,epsilon/(12Kphi)) and theta=b-epsilon/3. Choose

    N_T=ceil(9*Kphi^2*C*epsilon^(-2)*exp(lambda*gamma*T)).

For each fixed public horizon hard-code this finite integer and a positive
rational a_T satisfying

    |a_T/exp(lambda*T)-1|<=epsilon/(6Kphi).

These exist for each horizon. Their uniform computability from an arbitrary
unrepresented fixed f is not assumed or proved. The query count is still
O(exp(lambda*d*T/(s+d))). Public advice contains no information about v.

Fix a single finite profile table independent of T and v. Choose a rational
zmax with Phi(zmax)>=b-epsilon/12, and a rational grid on [0,zmax] of mesh
at most epsilon/(12Lphi). Store rational values within epsilon/12 of Phi
at each left endpoint. Beyond zmax return a fixed rational value within
epsilon/12 of b. The resulting table function P obeys

    sup_(z>=0) |P(z)-Phi(z)|<=epsilon/6.

The finite-interval error is a sum of grid Lipschitz and stored-value
errors. The tail error is controlled by Phi(zmax)'s proximity to b. No
clipping is needed: rational stored outputs may lie slightly outside [0,b].
Thus no exact runtime comparison with a potentially noncomputable b is
introduced.

Query N_T independent uniform points, compute their sample mean mhat, and
return P(a_T*mhat). For every realized mhat>=0, (A) implies

    |Phi(a_T*mhat)-Phi(exp(lambda*T)*mhat)|<=epsilon/6.

Adding the table error gives scalar error<=epsilon/3. Sampling RMS and
actual PDE bias each contribute at most epsilon/3. The L2 triangle
inequality therefore gives total RMS<=epsilon, uniformly on the fixed
input class. The algorithm never evaluates f, Phi, G, the unknown mass,
a derivative of v, or an evolved PDE value during its run. Only the N_T
initial values depend on the unknown input.

All online scalar constants can be finite rational advice and N_T a
finite integer. Exact real uniform sampling and point-value queries retain
their usual idealized information-model meaning. No bound on random bits,
comparison arithmetic, preprocessing time, table size or bit operations is
claimed. A uniform effective construction would require a specified
computable representation and certified bounds for the public reaction
and parameters; it is outside this theorem. No table has been generated
and no algorithm has been numerically executed for D26.

## 7. Example with a degenerate stable equilibrium

Take b=1 and f(y)=y(1-y)^2. Then lambda=1 but f'(1)=0, so the upper
equilibrium is degenerate. Setting w=y/(1-y), direct integration gives

    G(y)=w*exp(w),
    Phi(z)=W(z)/(1+W(z)),

where W is the inverse of w->w*exp(w) on [0,infinity). Indeed
G(y)/y->1 and d(log G)/dy=1/[y(1-y)^2], which verify the normalized
coordinate without requiring a special-function library. The theorem
therefore gives the same exp(dT/(s+d)) fixed-accuracy query order in this
example. Degeneracy can greatly affect constants and the saturation time;
no uniform bounds over reactions are implied. This is a symbolic example,
not a new numerical or formal result.

## 8. Review, attribution and remaining coverage

Root checked the inverse-coordinate endpoints, global anchor without
concavity, height/mass bound, early nonlinear comparison and mass-split
thresholds against T54. T54 also verifies the lower bound on exactly this
class and at every fixed epsilon in (0,b/2). The strictly positive radius R
and absence of additional zeros in (0,b) remain explicit assumptions.

The normalized unit-torus heat kernel has positive one-time minorization
and uniform mixing. This positive-data proof imposes no comparison of
lambda with the spectral gap. The hypotheses on f are only used on [0,b];
comparison with constant solutions 0,b keeps the classical solution there.
Local extension of f for well-posedness does not affect the theorem.

The original draft SHA256 is
f3fae210587e3349ebd105b1f5b0dbdc4011b9dff504d08549eac1e8bea0876e.
T54 SHA256 is
c01c0138276a1cd89804810db9ab903f702378b0541e77fb8ae0c36de8a5bfb5.
T51's actual sigmoid proof and T52's sample-risk work concern D24's
Allen-Cahn transform; they do not formalize the general C2 scalar
coordinate, profile table or this PDE theorem.

Root performed five preliminary targeted searches. Primary inspected
conceptual prior is [Hairer–Lê–Rosati, The Allen–Cahn equation with generic
initial datum, Eq.(1.5), Theorem2.1 and Proposition4.6](https://arxiv.org/pdf/2201.08426).
It uses nonlinear ODE transition profiles for its random-field scaling
limit. It does not by itself establish this deterministic-class arbitrary-C2
query statement. Separation of variables, interpolation, integration
complexity and sampling ingredients are classical. T55 is a separate,
bounded primary-literature proximity audit; absence of a located predecessor
will not certify originality or importance.
