# Candidate two-moving-barrier extension

Status: conventionally proved and independently passed in T30, including
the ratio-clock addendum integrated below. This is a separate extension of04k.
T29 passed the actual integrated-width analytic Lean gate, including derived
half-line integrability and its integral identity; see06f. The ODE-to-flow,
probability and PDE bridges remain conventional. No sampler, effective
arithmetic-cost or publication-priority claim.

## Scope

Let f be a real polynomial of degree at most n>=2. Fix m<M<b such that
f(b)=0 and f(y)>0 for y in [m,b). Unlike04k, no simple-root or negative
f'(b) assumption is made. On R^d or a flat torus, let m<=v(x)<=M be bounded
measurable initial data for u_t=Delta u/2+f(u). Comparison gives

    l(t)=ell_m(t)<=u(t,x)<=a(t)=ell_M(t)<b,
    h(t)=a(t)-l(t)>0,

where ell_c'=f(ell_c), ell_c(0)=c. These scalar flows increase to b.
They exist for all time and do not reach b in finite time, by local Lipschitz
uniqueness at the equilibrium. Statements at t=0 use the assigned measurable
datum and the usual heat-semigroup trace, not sup-norm continuity.

## Integrable bracket width without hyperbolicity

Set Delta=int_m^M 1/f(y)dy, which is finite and positive. Autonomous scalar
flow gives a(t)=l(t+Delta). Hence, for finite T,

    int_0^T h(t)dt
      =int_T^(T+Delta) l(s)ds-int_0^Delta l(s)ds.

Since l(s) tends to b, monotonicity yields the exact finite limit

    I_h=int_0^infinity h(t)dt
       =int_0^Delta (b-l(s))ds
       =int_m^M (b-y)/f(y)dy
       <=Delta(b-m)<infinity.

The upper integration limit is M<b. The argument does not require the
integrability of b-l(t); that may fail at a multiple equilibrium root.

## Rescaled reaction and explicit sufficient branch rate

Put w=(u-l)/h in [0,1]. Then

    w_t=Lw+F_t(w),
    F_t(w)=[f(l+h w)-(1-w)f(l)-w f(a)]/h
          =sum_(j=2)^n f^(j)(l)/j! * h^(j-1)*(w^j-w).

The endpoint coefficients vanish, and linear interpolation cancels the
first derivative term. For degree n Bernstein coefficients and 1<=k<n,

    w^j-w = -sum_(q=1)^(j-1) w^q(1-w),
    |coefficient_k(w^j-w)|
       <=(j-1) k(n-k)/(n(n-1)).

Here coefficient_k(w^q(1-w)) is nonnegative and at most the common factor
k(n-k)/(n(n-1)), by the degree-elevation formula in04k. Let

    C=sum_(j=2)^n (j-1) sup_[m,b]|f^(j)|/j! * (b-m)^(j-2).

Because h<=b-m, the degree n Bernstein coefficients d_k of F obey
|d_k|<=C h k(n-k)/(n(n-1)). If C>0, choose lambda(t)=C h(t), and
voting coefficients b_k(t)=k/n+d_k/lambda. These lie in [0,1], with
b_0=0 and b_n=1, and F=lambda(B_t-w). If C=0, the transformed problem
is linear and no branching is needed. This is a sufficient fixed-arity
construction; mixed arities or smaller rates may improve the constants.

## Uniform ideal expected work

The same bounded multiaffine n-child voting construction as04j uses initial
leaf values (v-m)/(M-m), Brownian edges, and remaining-time rate lambda.
Finite-generation counts and the deterministic integrated-time change must
first establish completion. The expected full-tree node count is

    E N_all(T)=[n exp((n-1)Lambda(T))-1]/(n-1),
    Lambda(T)=int_0^T lambda<=C I_h.

Consequently E N_all(T)<=K_work=[n exp((n-1)C I_h)-1]/(n-1)
uniformly in every finite T and spatial query. Bounded first-event renewal
and uniqueness of the transformed bounded mild solution then give E Z=w.
Return H_u=l(T)+h(T)Z and H_def=b-a(T)+h(T)(1-Z). Thus

    E H_def=b-u(T,x),
    0<r_M(T):=b-a(T)<=H_def<=r_m(T):=b-l(T).

This is an ideal scalar-flow/clock-oracle node bound. It excludes leaf-query,
dimension-dependent Brownian and finite-bit inverse/evaluation costs.

## Relative variance and zero-query comparison

The polynomial g(y)=f(y)/(b-y) extends continuously to b with value
-f'(b)>=0. Let G=max_[m,b]g<infinity. The scalar shift gives

    r_m(T)/r_M(T)
      =exp(int_T^(T+Delta)g(l(s))ds)<=exp(G Delta)=:K.

For any random H supported in [A,B] with 0<A<=B,
E H^2<=(A+B)E H-AB implies

    Var(H)/(E H)^2 <=(B-A)^2/(4AB).

The bound follows by maximizing (A+B)/mu-AB/mu^2-1 over mu in [A,B];
the maximum occurs at the harmonic center mu=2AB/(A+B).
Applying it to H_def yields a relative variance bound

    (K-1)^2/(4K),

uniformly in T,x,d. A deterministic iid root count
max(1,ceil((K-1)^2/(4K rho^2))) gives relative RMS rho, with expected
total nodes bounded by K_work times this count. For the actual time T,
the smaller ratio r_m(T)/r_M(T) can replace K throughout.

The deterministic harmonic-center estimate 2r_m r_M/(r_m+r_M) requires
no spatial-data queries and has relative error <=(r_m-r_M)/(r_m+r_M).
In particular, at a multiple stable root, this ratio tends to zero:
g(b)=0 and the finite time-shift formula imply r_m/r_M tends to one.
Therefore very large T in the degenerate case can become easy without
Monte Carlo; this is an essential comparator, not a claimed speedup.

## Nonhyperbolic one-sided attracting example

For f(y)=(b-y)^q with integer q>=2 and m<M<b,

    b-ell_c(t)=[(b-c)^(1-q)+(q-1)t]^(-1/(q-1)).

For even q the equilibrium repels on its other side; only attraction within
the stated interval from below is claimed. The one-equilibrium-barrier
approach has a nonintegrable rate of order 1/t,
whereas the two-moving-barrier width h is integrable. The exact budget is
I_h=int_m^M (b-y)^(1-q)dy, finite for every strict M<b. This gives a
concrete distinction in work bounds but no novelty or implementation claim.

## Allen–Cahn specialization and a cheaper mixed arity

For f(y)=y-y^3, b=1 and 0<m<M<1, the transformed reaction is exactly

    F_t(w)=h w(1-w)[2l+a+h w].

The degree-three Bernstein rule can use the smaller explicit rate
lambda=h(l+2a), with coefficients (0,(l+a)/(l+2a),1,1). It decomposes
into a mixture of OR_2(w)=2w-w^2 and majority_3(w)=3w^2-2w^3:

    B_t=p_t OR_2+(1-p_t)majority_3,
    p_t=3(l+a)/(2(l+2a)) in [3/4,1].

Thus an event needs two children with probability p_t and three otherwise.
Its mean population-growth rate is

    lambda(2-p_t)=h(l+5a)/2<=3h.

The expected terminal leaf count is exp(int_0^T lambda(2-p_t)); a finite
completed tree with arities two and three satisfies N_all<=2L-1.
Here I_h=log[M(1+m)/(m(1+M))], hence

    E N_all(T)<=2 exp(3 I_h)-1.

At m=1/2, M=3/4, this bound is 2(9/7)^3-1=1115/343, about3.251.
This improves the simple one-barrier ternary bound13 and its mixed-arity
bound about5.364, without asserting optimality or measured runtime.

The exact scalar defect ratio also obeys r_m/r_M<=
(m^(-2)-1)/(M^(-2)-1). For this pair it is at most27/7, giving relative
variance<=100/189 by the preceding positive-range inequality. These are
ideal sufficient bounds for all finite horizons, not empirical estimates.
The harmonic-center zero-query comparator remains mandatory.

## Exact Allen–Cahn ratio clock and sharper work bound

T30 also checked the following root addendum. Define A=m^(-2)-1,
B=M^(-2)-1 and z(t)=l(t)/a(t), z0=m/M. Then

    z(t)=sqrt[(1+B exp(-2t))/(1+A exp(-2t))],
    z'=z(a^2-l^2),  R(z)=z^2/(1+z),
    d/dt log R(z(t))=h(l+2a)=lambda(t).

The survival probability from remaining T down to s is R(z(s))/R(z(T)).
For U in(0,1), no event occurs if U R(z(T))<=R(z0). Otherwise set

    y=U R(z(T)),  zeta=[y+sqrt(y^2+4y)]/2,
    s=-(1/2)log[(1-zeta^2)/(A zeta^2-B)].

Then z0<zeta<z(T), A zeta^2-B>=1-z0^2>0, and the logarithm's argument
lies in(exp(-2T),1), so0<s<T. Brownian edge variance is T-s. This gives
explicit ideal clocks without an unknown PDE or special-function inverse.

The mixed probability p=3(1+z)/(2(2+z)) obeys
d[(5/2)log z-2log(1+z)]/dt=lambda(2-p). Consequently the sharper bound is

    E N_all(T)<=(1+z0)^2/(2 z0^(5/2))-1.

For m=1/2,M=3/4 it is25sqrt(6)/16-1, about2.8273, improving1115/343.
All are sufficient expected-node bounds, not assertions of optimality or
floating-point certification. Near z=1, the inverse needs a separate stable
evaluation and rounding-error contract.

## Integrated T30 proof details and a scoped semigroup corollary

The abstract width lemma needs only continuous monotone l on[0,infinity),
l<=b there, and l(t)->b. For Delta>=0 and J=int_0^Delta(b-l),

    int_0^T [l(t+Delta)-l(t)]dt
      =J-int_T^(T+Delta)(b-l(t))dt,
    0<=int_T^(T+Delta)(b-l(t))dt<=Delta*(b-l(T))->0.

The width is nonnegative; bounded truncated integrals and monotone convergence
prove its integrability and total integral J, without assuming either in
advance. T29's fixed Lean contract05f targets this actual analytic statement.

For tree completion, truncate at depth D in operational time Lambda(T).
The finite expected-count recursion K_0=1,
K_(D+1)(a)=1+n int_0^a exp(-(a-s))K_D(s)ds is dominated inductively by
K(a)=[n exp((n-1)a)-1]/(n-1). Increasing finite counts then give finite
E N and almost-sure completion. Only afterward form the bounded multiaffine
return and identify its first-event renewal with the bounded mild equation.
The same argument with offspring mean2p+3(1-p) gives the mixed leaf formula.

The construction also extends to a jointly measurable conservative Markov
transition semigroup on a standard Borel state space with an independent exact
edge-sampling oracle. Positivity, contraction and P_t1=1 supply comparison,
the affine mild transform and renewal. This statement concerns its semilinear
mild integral equation, not a new regularity theorem. Transition-oracle costs
are uncharged; nonconservative kernels require different barrier equations.

## Reviewed limitations

T30 checks every coefficient formula, the flow-shift identity, finite-generation
completion, measurable mild correspondence, endpoint derivative sign,
relative variance optimization and nonhyperbolic baseline limit.
Existing scalar barriers, affine normalization, Bernstein voting, and
time-inhomogeneous branching are established ingredients; priority for this
combination remains open. Interfaces, coupled systems, unbounded basins and
nonpolynomial finite-branch realizability are outside this result.
