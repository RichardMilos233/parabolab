# Candidate extension to boundary-touching data after fixed burn-in

Status: conventionally proved and independently passed in T32 under the
explicit ideal-oracle contract and imported Huber theorem. It is separate
from D19. No Lean, implementation, practical cost or priority claim. Known
Bernoulli-factory constructions turn a mean-only interior PDE bound into
the bounded stochastic leaf oracle required by the two-barrier method.

## Scope and deterministic interior bounds

Consider Allen–Cahn u_t=L u+u-u^3 under the conservative measurable Markov
semigroup contract in04l. Assume for a fixed t0>0 that

    P_t0(x,dy)>=eta*pi(dy),  0<eta<=1,

where pi is a probability measure. Let the initial oracle satisfy0<=v<=1,
with known positive mass bounds pi(v)>=delta0 and pi(1-v)>=delta1,
where delta0+delta1<=1. Values zero and one are now permitted pointwise.
This is a minorized/mixing setting, not a claim for general unbounded space.
Connected compact heat kernels provide examples; obtaining a useful explicit
minorization constant is a separate input, not hidden computational work.

Comparison on[0,1] and the nonnegative reaction imply u(t)>=P_t v.
For D=1-u, the equation is D_t=L D-(u+u^2)D, with0<=u+u^2<=2.
Thus D(t)>=exp(-2t)P_t(1-v). At the fixed burn-in time,

    L0:=eta*delta0 <= p(x):=u(t0,x)
       <=U0:=1-eta*exp(-2t0)*delta1,
    0<L0<U0<1.

Set a=L0/2 and b=(1+U0)/2, so0<a<L0<=p<=U0<b<1. The later two-barrier
sampler can use scalar flows starting at a and b, provided it can sample a
bounded leaf with mean w0(x)=(p(x)-a)/(b-a). Its unknown p must not be
silently supplied by a PDE-value oracle.

## A finite-cost p-coin without knowing p

The original scalar voting representation on[0,1] can use constant rate2,
ternary Bernstein coefficients(0,1/2,1,1), and Bernoulli(v(Y)) leaves.
Its conditional vertex output is a Bernoulli with success probability
the coefficient indexed by the number of successful children. This gives
a Bernoulli(p(x)) root at horizon t0 by the standard bounded voting proof.
The full-tree expected nodes are

    B0=[3exp(4t0)-1]/2,

uniformly in x. Repeated calls at a fixed x with fresh independent tree,
transition and vote randomness give iid p(x)-coins. This phase runs only
for the fixed t0, regardless of the final horizon T.

## Explicit affine factory from two known linear factories

The required affine map has a negative intercept, so merely subtracting a
from a Bernoulli(p) outcome would lose the[0,1] range. Instead use the
linear amplification factory from [Huber, Theorem1, arXiv:1308.1562v2](https://arxiv.org/pdf/1308.1562v2).
For C>1 and known epsilon>0 with Cq<=1-epsilon, that established algorithm
simulates Bernoulli(Cq) using at most9.5 C/epsilon input-coin calls in mean.
Only that input-call bound is imported here, not a new factory algorithm.

Define

    C1=1/(1-a),   epsilon1=(L0-a)/(2(1-a)),
    C2=(1-a)/(b-a), epsilon2=(b-U0)/(2(b-a)).

Both C_i>1 and epsilon_i in(0,1). Complement a p-coin to get1-p.
Factory1 amplifies it to(1-p)/(1-a), then complement its output to obtain
a coin with parameter q=(p-a)/(1-a). Factory2 amplifies q to

    C2 q=(p-a)/(b-a)=w0.

The allowed-domain conditions have strict slack:

    C1(1-p)<=1-2epsilon1,
    C2 q<=1-2epsilon2.

Factory2's requested q-coins use independent fresh Factory1 runs. The number
of raw p-coins needed therefore has uniform expected bound

    B_factory <=(9.5)^2*C1*C2/(epsilon1*epsilon2)
               =1444*(1-L0/2)/(L0*(1-U0)).

The half-slack choice avoids ambiguity at a cited theorem's domain boundary.
The bound is intentionally conservative and can be very large. Standard
conditioning on the history before each requested coin, followed by Tonelli,
justifies multiplication of the two mean budgets; independence from the
eventual stopping time is not required or assumed.
Explicitly, the individual bounds are B1=38/L0 and
B2=38(1-L0/2)/(1-U0). Before the next raw coin is requested, its activation
event is determined by the preceding history. Its fresh joint(output,cost)
batch has the uniform mean-cost bound conditional on that history. Summing
over requested batches proves the product bound even though the cost can be
correlated with the returned coin and with subsequent stopping decisions.

[Nacu–Peres, Theorem2 and the remark after Definition1](https://arxiv.org/pdf/math/0309222)
also give a general analytic-function existence route on a closed interior
probability interval, with uniform tails. The two-linear-factory composition
above makes a concrete imported input-call budget available instead of
claiming effective arithmetic complexity from that general existence result.

## Later-horizon construction and total oracle budget

For T>=t0, run the two-barrier mixed voting tree for horizon S=T-t0 with
scalar initial bounds a,b. At a leaf located at x, use the factory output
just constructed, a Bernoulli with mean(p(x)-a)/(b-a). All leaf factories and
their internal burn-in simulations use fresh independent randomness.
The bounded first-event proof then gives the original u(T,x) and defect
1-u(T,x); the terminal mean is u(t0), obtained by exact composition rather
than by supplying unknown evolved values to a callback.

Let K_work be04l's mixed mean-node bound with z0=a/b. Expected raw burn-in
tree nodes per final root are at most K_work*B_factory*B0, since the number
of final leaves is at most its total nodes. Including the outer tree gives

    E combined_tree_nodes <=K_work*(1+B_factory*B0),

uniformly in all T>=t0 and x. The range and relative-defect variance bounds
from04l still hold with phase bounds a,b, because each factory leaf is in
{0,1}. A fixed iid root count then gives horizon-uniform relative RMS in
the ideal oracle model. Factory internal scalar arithmetic, transition
oracle work and finite-bit accuracy are separate from this count.

This removes the pointwise strict initial bounds under the stated mixing
and mass assumptions. It does not cover T=0 relative error at points v=1,
interfaces between negative and positive phases, vanishing global mass,
absence of minorization, or practical efficiency with the displayed large
constants. The harmonic-center scalar-bound baseline remains mandatory and
should use the genuine narrower L0,U0 bounds at t0, not the artificially
widened a,b needed by the factory. Otherwise the comparison would weaken a
known deterministic competitor.

## Reviewed scope and novelty obligations

T32 checks the heat/comparison inequalities, minorization margins, first-stage
Bernoulli law, factory domains/complements, nested mean cost and semigroup
restart. It reads the actual primary factory theorem and its input-call cost
definition. General factories and their composition are published methods;
exact priority for this PDE application is unestablished. Transition/data
oracles and constants are ideal; T31's measurable-data finite-bit obstruction
still applies. A separately selected formal gate is required before any
implementation. The first smooth two-barrier experiment remains primary.
