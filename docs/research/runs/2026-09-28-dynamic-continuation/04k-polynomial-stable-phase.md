# Candidate polynomial stable-phase theorem

Status: conventionally proved and independently passed in T28, extending
the mechanism in04j. No Lean, implementation, effective arithmetic or originality claim.
All expectations below concern an ideal real-arithmetic branching model.

## Assumptions and scalar barriers

Let f be a real polynomial of degree at most n, n>=2. Fix m<M<b with
f(b)=0, f(y)>0 on [m,b), and f'(b)<0. On R^d or a flat torus, consider
u_t=Delta u/2+f(u) with bounded measurable initial data m<=v<=M.
The dimension and spatial profile are arbitrary within this scalar phase.
The solution is bounded mild; merely measurable data do not entail sup-norm
continuity at zero or pointwise convergence at every assigned datum point.
Standard comparison gives ell_m(t)<=u(t,x)<=ell_M(t)<b, where
ell_a'=f(ell_a), ell_a(0)=a. All these scalar solutions approach b.

Write f(y)=(b-y)g(y). Then g is a polynomial of degree at most n-1,
positive on [m,b], with g(b)=-f'(b)>0. Put

    c=min_[m,b] g>0,  r(t)=b-ell_m(t),
    I=int_0^infinity r(t)dt=int_m^b 1/g(y)dy <=(b-m)/c.

Thus r'=-g(ell_m)r and r(t)<=(b-m)exp(-ct). The strict stable-root
and no-intermediate-equilibrium assumptions are essential here.

## Transformed polynomial and a Bernstein rate

Set w=(u-ell_m)/r in [0,1]. Exact substitution yields

    w_t=Lw+F_t(w),
    F_t(w)=[f(ell_m+r w)-(1-w)f(ell_m)]/r
          =(1-w)[g(ell_m+r w)-g(ell_m)].

In particular F_t(0)=F_t(1)=0 and

    F_t(w)=sum_(j=1)^(n-1) g^(j)(ell_m)/j! * r^j * w^j(1-w).

For degree n Bernstein basis B_(n,k), the coefficient of w^j(1-w) is

    c_(j,k)=binom(k,j)/binom(n,j)*(n-k)/(n-j)
           =binom(k,j)*(n-k)/(n*binom(n-1,j)),

for j<=k<=n-1, and zero otherwise. For 1<=j<=k<=n-1,

    0<=c_(j,k)<=k(n-k)/(n(n-1)).

Define the finite coefficient budget

    C=sum_(j=1)^(n-1) [sup_[m,b] |g^(j)|/j!] * (b-m)^(j-1).

Writing F_t=sum d_k(t)B_(n,k), we get d_0=d_n=0 and

    |d_k(t)|<=C r(t) k(n-k)/(n(n-1)).

If C>0, take lambda(t)=C r(t) and

    b_k(t)=k/n+d_k(t)/lambda(t).

Since k(n-k)/(n(n-1))<=min(k/n,1-k/n), all b_k lie in [0,1].
Consequently B_t(w)=sum b_k(t)B_(n,k)(w) maps [0,1] to itself and
F_t=lambda(t)(B_t-w). This is an explicit sufficient rate, not the
optimal arity, representation or rate. If C=0, g is constant, F_t=0,
and w solves the linear heat equation without branching.

## Bounded estimator and horizon-uniform ideal node work

Use independent Brownian edges and a remaining-time n-child clock of rate
lambda(s). At a leaf return (v(Y)-m)/(b-m). At a branch use the bounded
multiaffine extension of its Bernstein coefficients. The root value Z lies
in [0,1]. Conditional independence supplies its polynomial expectation.
The transformed PDE has a bounded unique mild solution on each finite time
interval; finite-tree exhaustion and dominated convergence identify E Z=w.
Return H_def=r(T)(1-Z), whose expectation is b-u(T,x).

The clock has total integrated rate

    Lambda(infinity)=C I<infinity.

A deterministic time change gives an n-ary Yule tree with expected terminal
leaves exp((n-1)Lambda(T)). Each full completed tree obeys
N_all=(n L-1)/(n-1). Hence

    E N_all(T)<=[n exp((n-1)C I)-1]/(n-1) =: K_work.

Non-explosion of finite-rate n-ary Yule, or a finite-generation expected-count
bound followed by monotone convergence, must be justified before relying on
completion. The finite horizon in integrated time and the finite expectation
yield a.s. completion uniformly over all physical finite T. No derivative
of the spatial data and no evolving PDE oracle is queried by this estimator.
Scalar barrier and inverse clock evaluation are currently ideal oracles.

## Relative accuracy for the vanishing defect

Let Delta=int_m^M 1/f(y)dy. The scalar semigroup identity gives
ell_M(t)=ell_m(t+Delta). With G=max_[m,b]g,

    r_m(t)/r_M(t)
      =exp(int_t^(t+Delta) g(ell_m(s))ds)<=exp(G Delta)=:K_range.

Comparison ensures D=b-u(T,x)>=r_M(T)>0. Since 0<=H_def<=r_m(T),
H_def^2<=r_m(T)H_def, so

    Var(H_def)/D^2<=r_m(T)/D-1<=K_range-1.

Thus max(1,ceil((K_range-1)/rho^2)) independent roots suffice for relative
RMS rho, with expected total nodes bounded by K_work times this number,
uniformly in finite T,x,d. This is a node count; Brownian sampling costs O(d),
leaf evaluations depend on v, and resolving an exponentially small defect
has a bit-precision contract not addressed here.

The zero-query deterministic harmonic-center estimate
2 r_m(T)r_M(T)/(r_m(T)+r_M(T)) already has relative error at most
(K_range-1)/(K_range+1). Any practical test must compare with this bound and
with stronger known deterministic or stochastic methods.

## Integrated T28 proof details and scope

The vertex return is explicitly
V_s(z)=sum_(A subset {1,...,n}) b_(|A|)(s)
product_(i in A)z_i product_(i notin A)(1-z_i).
Its nonnegative product weights sum to one. Conditional independence gives
E V_s=B_s(E Z_child); evaluating B_s at the average of children would generally
be a different rule. Arity-dependent arithmetic cost is not part of node work.

In operational time a=Lambda(T), depth-capped expected counts obey
K_0(a)=1 and K_(D+1)(a)=1+n integral_0^a exp(-(a-s))K_D(s)ds.
The explicit K(a)=[n exp((n-1)a)-1]/(n-1) solves the same integral equation.
Positivity gives K_D<=K; monotone convergence gives finite E N before the
completed return is used. The completed return's first-event equation is
the killed-semigroup mild form of the transformed PDE. Its Bernstein
polynomial has Lipschitz constant at most n, so Gronwall identifies the
bounded mild solution. This supplies completion and correspondence in the
order required by the earlier sketch.

This is a changed time-dependent scalar representation, not a supported
likelihood proposal on the original derivative-coded signed tree measure;
there is no conflict with D10's compact-domain obstruction. The simple-root
condition is specific to this one-barrier finite-hazard certificate, not an
impossibility theorem for other normalizations. For f(y)=(b-y)^2, this clock
has actual mean nodes1+2(b-m)T. The separate two-barrier candidate04l may
improve that behavior and is not included in T28's verdict.

## Scope and reviewed limitations

This is restricted to a scalar attracting phase separated from intermediate
equilibria, with a simple stable root. It excludes interfaces and data touching
the limiting root if a strict uniform relative-defect guarantee is wanted.
Constants can diverge as the phase bounds approach those boundaries. No
general bistable interface or broad-system complexity theorem follows.

The polynomial voting construction, scalar barriers and deterministic clock
changes are classical ingredients. T27 records primary predecessors and the
limits of its bounded novelty search. T28 checks the degree elevation,
transformation, completion/correspondence, ratio and cost constants. No
publication priority is established. No implementation should precede an
explicitly selected fixed Lean gate.
