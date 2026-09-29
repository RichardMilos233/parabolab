# Candidate constructive sampling of the endpoint tilt

Status: conventionally proved and independently passed in T26 in the ideal
exact-oracle model. This is separate from 04h's abstract existence theorem.
No formal, numerical or effective bit-complexity claim.
The algorithm uses ideal exact scalar inverses and derivative-value oracles;
their arithmetic costs are not hidden in a node-count result.

Generating functions satisfying Y'=Phi(Y) and their tree interpretation are
classical; see [Bergeron–Flajolet–Salvy (1992)](https://algo.inria.fr/flajolet/Publications/BeFlSa92.pdf).
Randomizing a Boltzmann sampler's parameter to change its size distribution
is explicitly developed by [Darrasse et al. (2012), Section 2.2](https://dmtcs.episciences.org/2989/pdf).
The gamma mixture below is an application of that established principle to
the inverse-power cost tilt. T26 checks the bounded independent normalization
factor and this coding application; no new general sampling principle or
publication priority is asserted.

Retain 04h's notation: alpha>0, Phi(z)=(1-z^2)^(-alpha),
F(z)=integral_0^z (1-y^2)^alpha dy, tau=F(1), Z=F^(-1), and
mu=|nu_tau|, a measure of total mass one on nonzero completed Id trees.
If a tree has n internal events then N=2n. Fix p>1 and a=1/p.
Here nu and mu are pushed forward to the scalar topology-and-time tree after
integrating the irrelevant Brownian marks of the constant-data problem.
If a proposal on the fully spatially marked original tree is wanted, attach
fresh conditional heat-kernel marks along the rescaled edges at horizon tau.
Rescaling times while retaining old positions would not give that full law.
The scalar pushforward preserves both the signed weight and the node count.

## An accepted gamma tilt

Take S from Gamma(shape=a, rate=2) and accept it with probability

    A(S)=Z(tau exp(-2S))/exp(-2S).

Since Z is convex, Z(0)=0, Z(tau)=1 and Z'(t)>=1,

    t<=Z(t)<=t/tau for 0<=t<=tau,
    tau<=A(S)<=1.

Thus rejection sampling needs at most 1/tau proposals in expectation. The
accepted S has density proportional to s^(a-1) Z(tau exp(-2s)).
Conditional on S, set t=tau exp(-2S)<tau and draw a tree from the normalized
canonical absolute measure at t. Rescale every remaining event time by tau/t.
The same tree's nonnegative mass at t is exp(-S N) times its mass at tau.
The resulting mixture law is therefore

    dQ_* = N^(-a) dmu / Z_p,
    Z_p = integral N^(-a) dmu.

The factor follows from integral_0^infinity s^(a-1)exp(-sN)ds=Gamma(a)N^(-a).
No unknown normalization is needed to sample the accepted S.

## Sampling the positive canonical tree at subcritical t

For constant data and 0<t<tau, the absolute code masses are

    W_I(t)=Z(t),      W_Fk(t)=Phi^(k)(Z(t)).

The Id root has no nonzero terminal contribution. Its first branch remaining
time s is sampled by Z(s)=U Z(t), equivalently s=F(U Z(t)), then starts F0.

For a reaction code Fk, let a_k=Phi^(k)(0). If
U Phi^(k)(Z(t))<=a_k, it terminates at time zero with the sign of f_alpha^(k)(0).
Otherwise invert

    Phi^(k)(Z(s)) = U Phi^(k)(Z(t)),        0<s<t,

then spawn independent children F0 and F(k+1) at s. This is exactly the
positive mild law because

    d/ds Phi^(k)(Z(s))=Phi^(k+1)(Z(s))*Phi(Z(s)).

There are no nonzero spatial branches. The derivative mass is strictly
increasing for positive argument; even k may have derivative zero at zero,
which does not compromise the unique interior inverse. Phi derivatives have
the finite polynomial form

    Phi^(k)(z)=P_k(z)(1-z^2)^(-alpha-k),
    P_0=1,
    P_(k+1)=(1-z^2)P_k'+2(alpha+k)z P_k.

Its coefficients are nonnegative by induction because deg P_k<=k and the
coefficient contribution 2(alpha+k)-j is positive for j<=k. Thus each
requested scalar function is explicit, though evaluating a high-order
polynomial is not a constant-cost operation in a real implementation.

Construct the recursive kernels provisionally allowing an infinite tree.
For each finite completed tree, multiply its leaf probabilities and event
densities. Each numerator child mass cancels the denominator at that child,
leaving exactly the canonical absolute tree density divided by its root
mass. This uses only finite products and does not assume completion. The
canonical masses are the minimal completed-tree sums (the monotone terminal-
jet exhaustion in T13), so summing these finite-tree probabilities gives one.
Tonelli and exhaustion prove almost-sure completion for each 0<t<tau.
Grouping the now-identified Id law by n gives mean nodes
2t Z'(t)/Z(t)<infinity. The derivative equation is used only below tau.
The mixed endpoint sampler completes almost surely for every p>1, even
when its unconditional mean tree size is infinite.

## Removing the unknown output normalization

The optimal likelihood output would be Z_p sign(tree) N^a. Its normalization
is an integral that the sampling procedure need not know. An additional
independent gamma proposal S0 and Bernoulli B with success probability A(S0)
satisfy

    E B = 2^a Z_p.

Hence Zhat_p=2^(-a)B is a bounded unbiased estimate of Z_p. Independent of
the accepted tilted tree, return

    H_new=Zhat_p sign(tree) N^a.

First E|H_new|=1, so the signed expectation factorization is legitimate.
Then E H_new=integral dnu_tau, and

    E|H_new|^p = 2^(a-1) S_p,
    E_Q* N = S_p/Z_p,
    S_p=integral N^((p-1)/p) dmu.

Consequently the proposed ideal construction has finite pth output moment
and finite mean sampled-tree node count exactly in 04h's regime
p<1+1/alpha. Extra gamma proposals and one normalization Bernoulli have finite
expected count. Independence of that Bernoulli from the accepted tree is
essential; reusing the accepting Bernoulli would return a biased result.
Writing r_acc=2^a Z_p in [tau,1], the extra normalization trial inflates
the pth output moment relative to the known-normalizer likelihood by exactly
r_acc^(1-p)<=tau^(1-p), when finite. It does not change the sampled-tree law.
There are at most 1/tau+1 gamma proposals in expectation including this trial.

This randomized-normalization output is not literally the exact likelihood
of a single proposal on the original tree space. Its unbiasedness follows
from the extra independent factor. The phase is inherited from the chosen
tilted tree's S_p integrability, not by silently applying a fixed-law theorem
to a different output architecture.
Its conditional mean given the tree is the exact likelihood
Z_p sign(tree)N^a, so conditional Jensen also transfers the moment obstruction.

## Unresolved practical cost

Counting nodes treats arbitrarily high derivative evaluations and inverses
as oracles. Naively updating the polynomials can introduce superlinear work
in N whose expectation need not be finite. For a cost N^q the corresponding
abstract Hölder criterion is integral N^(q(p-1)/p)dmu<infinity; the critical
cusp permits this only if q(p-1)/p<1/(alpha+1). In particular a genuine
quadratic-in-N cost and p=2 fail this criterion for every alpha>0.
This is the existence criterion across appropriately retuned proposals,
whose tilt would be N^(-q/p). For the particular N^(-1/p) sampler above,
its own qth cost moment is finite iff q-1/p<1/(alpha+1), when q-1/p>0;
nonpositive powers are automatically integrable. These are distinct tests.
The gamma construction can also realize the retuned tilt by taking shape
a=q/p. It then has pth moment
2^(-q(p-1)/p) integral N^(q(p-1)/p)dmu and mean N^q equal to that integral
divided by integral N^(-q/p)dmu. This is still an ideal-oracle statement.

An O(N^2) operation-count upper bound alone does not prove infinite expected
arithmetic cost. Such an obstruction needs an actual comparable or lower
quadratic cost; the upper bound would only fail to certify finiteness.

This is a major limitation, not a rounding detail. Before an implementation
can claim finite expected arithmetic work, it needs an explicit cost model
and a faster derivative/inverse procedure or a different code representation.
The signed ODE also has an elementary scalar inverse description and is a
strong deterministic baseline. This construction presently serves to examine
the representation frontier, not to propose a competitive ODE solver.
