# Candidate all-horizon positive-phase Allen–Cahn sampler

Status: conventionally proved and independently passed in T27. No Lean,
numerical, novelty or total-arithmetic claim. This changes the scalar representation; it is not
a proposal-only repair of the original derivative-coded tree.

## Scope and the nontrivial accuracy target

On R^d or a flat torus, consider u_t=Delta u/2+u-u^3 with a bounded measurable
terminal/initial oracle v satisfying 0<m<=v(x)<=M<1 everywhere. The dimension
is arbitrary. The solution lies in the stable positive phase, with no known
spatial profile supplied. The pointwise quantity of interest can be the small
defect 1-u(T,x); returning the equilibrium 1 has 100% relative defect error.
Sign-changing profiles, phase interfaces and data touching zero or one are
outside the strict two-sided defect guarantee.
The solution is bounded mild. For measurable data the initial condition uses
the assigned oracle and heat-semigroup trace; no sup-norm continuity at zero
or convergence to v(x) at every point is asserted. All horizons are finite.

The existing scalar voting representation has bounded output but constant
branch rate and exponential expected full-tree size. The candidate below
uses the explicit scalar lower solution to produce an integrable branch
rate, and hence expected full-tree work uniform in T.

## Exact lower-solution change of variable

Let ell(t) solve ell'=ell-ell^3, ell(0)=m, and r(t)=1-ell(t). Explicitly,

    ell(t)=[1+(m^(-2)-1)exp(-2t)]^(-1/2).

Comparison gives ell(t)<=u(t,x)<=ell_M(t)<1. Define

    w(t,x)=(u(t,x)-ell(t))/r(t),       0<=w<=1.

For every finite t, r(t)>0. Direct substitution gives

    w_t=Lw + r(1+2ell)w -3ell*r*w^2-r^2*w^3
         = Lw + lambda(t)[B_t(w)-w],
    lambda(t)=r(t)(2+ell(t)).

Here B_t is the cubic Bernstein polynomial with coefficients

    (b0,b1,b2,b3)=(0,(1+ell)/(2+ell),1,1).

Indeed the linear coefficient in lambda(B_t-w) is r(1+2ell), the
quadratic coefficient is -3ell*r and the cubic coefficient is -r^2.
All four Bernstein coefficients lie in [0,1].

## Exact bounded branching representation

Use Brownian motion (modulo the period for a torus) and a time-inhomogeneous
ternary clock whose rate at remaining time s is lambda(s). At a leaf at time
zero, return (v(Y)-m)/(1-m) in [0,1]. At an event at remaining time s, simulate
three independent child values z1,z2,z3 and return the multiaffine extension

    F_s(z1,z2,z3)
      = sum_(S subset {1,2,3}) b_(|S|)(s)
           product_(i in S) z_i * product_(i notin S)(1-z_i).

Its coefficients form a convex combination, so 0<=F_s<=1. Conditional
independence gives E F_s(children)=B_s(w). The signed root estimator is

    H_u=ell(T)+r(T) Z_w,          H_defect=r(T)(1-Z_w).

Thus every completed output obeys ell(T)<=H_u<=1 and
0<=H_defect<=r(T). With completion and the bounded mild uniqueness argument,
their expectations are u and 1-u respectively. No derivative oracle or
evolving PDE solution oracle is used. A Bernoulli implementation of the same
vertex voting rule is possible but is not needed for this bounded multiaffine
return construction.

## Total integrated rate and expected full-tree size

Since ell'=ell(1-ell)(1+ell),

    Lambda(T)=integral_0^T lambda(s)ds
      = [2log ell-log(1+ell)]_(m)^(ell(T)),
    Lambda(infinity)=log[(1+m)/(2m^2)]<infinity.

A ternary pure-birth tree with this deterministic rate has expected leaves
exp(2Lambda(T)). Its total visited nodes are (3L-1)/2, hence

    E N_all(T)=[3exp(2Lambda(T))-1]/2
      <= K_m := [3((1+m)/(2m^2))^2-1]/2.

More explicitly, for depth-capped trees n_0(T)=1 and
n_(D+1)(T)=1+3 integral_0^T exp(-(Lambda(T)-Lambda(s)))lambda(s)n_D(s)ds.
The explicit n(T)=[3exp(2Lambda(T))-1]/2 solves that same integral equation.
Positivity gives n_D<=n. Increasing node counts and monotone convergence
then prove finite expectation and a.s. completion, before defining the full
return. The completed expectation obeys the first-event renewal equation;
bounded mild uniqueness follows from the uniform Lipschitz voting polynomial
and Gronwall. This closes unbiasedness without presupposing tree completion.
At m=1/2, K_m=13.
The bound deteriorates like m^(-4) as the lower positive bound approaches zero.

## An explicit clock inverse

Put R(a)=a^2/(1+a). Clock survival from remaining T to s is
R(ell(s))/R(ell(T)). For a uniform U:

    if U R(ell(T))<=R(m): no event before time zero;
    otherwise y=U R(ell(T)),
      a=[y+sqrt(y^2+4y)]/2,
      s=(1/2)log[(1-m^2)a^2/(m^2(1-a^2))].

This gives 0<s<T. Brownian edges use variance T-s. At very large T the
formulas need stable residual/exponential handling; exact ideal inverses do
not certify a floating implementation.

## Relative defect accuracy uniform in the horizon

Let a_m=m^(-2)-1, a_M=M^(-2)-1, and K_range=a_m/a_M>=1. Since

    1-ell_b(t) = a_b exp(-2t) /
      [sqrt(1+a_b exp(-2t))*(1+sqrt(1+a_b exp(-2t)))],

we have r_m(t)/r_M(t)<=K_range. Comparison gives
1-u(T,x)>=r_M(T)>0. As 0<=H_defect<=r_m(T), the pointwise inequality
H_defect^2<=r_m(T)H_defect gives the sharpened bound

    Var(H_defect)/(1-u(T,x))^2 <= K_range-1.

Consequently a deterministic number max(1,ceil((K_range-1)/rho^2)) of independent
roots gives relative RMS at most rho for the defect, with expected full-tree
nodes at most K_m times that number, uniformly in every finite T, x and d.
The constants depend on the initial lower and upper phase bounds m,M.
This is a genuine relative target for a vanishing quantity, although a
problem-specific deterministic approximation could still be better.

## Stronger elementary comparisons

At the same lambda clock, the identical voting polynomial decomposes as
B=p OR_2+(1-p)majority_3, where p=3(1+ell)/(2(2+ell)) in [3/4,1].
OR_2(w)=2w-w^2 and majority_3(w)=3w^2-2w^3 have bounded multiaffine
extensions. Choosing two or three children with these probabilities gives
the same expectation and range, but need not give the same variance law.
The population-growth rate is lambda(2-p)=r(5+ell)/2. Its integral is
[(5/2)log ell-2log(1+ell)]_m^ell(T). Since every such completed tree
has N_all<=2L-1, the uniform node bound improves to

    E N_all<=(1+m)^2/(2m^(5/2))-1,

which at m=1/2 equals9sqrt(2)/2-1, about5.364. T27 provides the same
finite-depth completion argument. Pure ternary rate minimality is not
overall work optimality.

The zero-query harmonic-center estimate 2r_m r_M/(r_m+r_M) already has
relative defect error at most (r_m-r_M)/(r_m+r_M)<=
(K_range-1)/(K_range+1). Meaningful future accuracy tests must beat this
bound and retain the comparison.

## Boundaries and review obligations

The main positive claim concerns ideal expected node work; a Brownian edge
costs O(d) and each leaf calls v. A meaningful total-cost theorem must charge
those oracles and bit precision, including the tiny defect r(T). It does not
cover phase interfaces or rescue the original derivative-code representation.

Bernstein voting is established in [An–Henderson–Ryzhik2022, Theorem3.2](https://arxiv.org/html/2209.03435),
and mixed offspring in [O'Dowd2019, Section4.5](https://www.stats.ox.ac.uk/~etheridg/odowd.pdf).
Normalization producing decaying branching also has a primary predecessor in
[Engländer–Winter2005/2006, Section2.1 and AppendixB](https://arxiv.org/pdf/math/0504377).
T27's bounded primary search did not establish exact publication priority;
the generic ingredients are not new. T27 independently checks the signs,
clock, finite-tree work, completion, mild correspondence and relative bound.
No implementation may precede an explicitly selected fixed Lean gate.
