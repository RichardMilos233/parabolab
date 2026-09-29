# R14e: a direct elementary centered-heat primitive for fixed diffusivity

Date: 2026-09-29. Root-authored conventional candidate, pending independent
review. The common D33 ideal model already counts exp, log, cos, floor,
real arithmetic/comparisons and continuous random draws as elementary
operations. This note uses exactly those paid primitives to simplify
the centered-heat subroutine. It is not a finite-bit or practical-speed
claim, and it does not by itself extend the full D31/D33 theorem.

## 1. Exact interface

Fix d>=1, kappa>0 and lambda=2pi^2 kappa>1. Set

    nu=lambda-1, q=exp(-lambda),
    rho=((1+q)/(1-q))^d, M=2 rho exp(lambda),
    B_tau=exp(tau)(P_tau-Pi),

where P is actual heat evolution for kappa Delta/2 on the unit torus.
For a supplied finite lag tau>=0 and spatial root x, the proposed
program returns a real beta and point Y with

    E[beta f(Y)]=exp(nu tau)(B_tau f)(x)/M,
    E beta^2<=1                                       (1.1)

for every bounded Borel f. Its elementary operation count is at most
C(d+1), including every discrete-frequency and spatial random draw,
uniformly in the lag. The fixed d,kappa-dependent probability table is
public and may instead be charged once as O(d) preprocessing.
The program acquires no unknown input values; evaluating f is outside
this primitive. All arithmetic magnitudes and integer bit lengths are
idealized as in D33, not suppressed in a finite-bit analysis.

## 2. The short-lag branch

For 0<=tau<1, toss a fair coin. In its first outcome draw a wrapped
Gaussian Y=x+sqrt(kappa tau)Z mod 1 with Z standard d-dimensional
normal and assign beta=2exp(lambda tau)/M. For tau=0 use Y=x.
In the second outcome draw Y uniformly on the torus and assign the
negative of the same beta. Therefore

    E[beta f(Y)]=exp(lambda tau)(P_tau f(x)-Pi f)/M,

which is (1.1). Also |beta|<=2exp(lambda)/M=1/rho<=1. Gaussian
coordinate draws, scaling, modular reduction and the exponential
evaluation use at most C(d+1) counted ideal operations. No heat-density
or total-variation-normalizer evaluation is used.

## 3. Exact nonzero frequency law without an all-zero rejection loop

The required frequency law on Z^d\{0} is

    P(N=n)=q^(|n|_1)/(rho-1).                       (3.1)

Here is a finite program for it. Put p0=(1-q)/(1+q). A one-dimensional
integer with mass p0 q^|n| has probability p0 of zero. Conditional on
being nonzero, its sign is fair and its magnitude has law

    P(G=m)=(1-q)q^(m-1), m>=1.

Generate this magnitude from a uniform U by
G=1+floor(log(U)/log(q)) for 0<U<1. At either endpoint set U=1/2
before applying the formula; these exceptional assignments are Borel
and change no distribution. All returned integers are finite.

First choose I in {1,...,d} with the public probabilities

    P(I=i)=p0^(i-1)(1-p0)/(1-p0^d).

A sequential cumulative comparison with one uniform draw requires at
most d comparisons. Precompute the powers by d multiplications. Set
N_j=0 for j<I, generate N_I from the nonzero signed geometric law,
and generate each coordinate j>I independently from the full
one-dimensional law (zero with probability p0, otherwise signed G).

The product probability of a nonzero vector n whose first nonzero
coordinate is i is its original independent-coordinate probability
p0^d q^|n|_1 divided by 1-p0^d. Since rho=p0^(-d), this equals (3.1).
Thus the algorithm samples the product law conditioned on being
nonzero without a potentially long all-zero rejection stage. It uses
at most C(d+1) ideal operations on every seed, regardless of the size
of the returned integer coordinates. This last qualification is
precisely where finite-bit cost would be different.

## 4. The long-lag branch

For tau>=1, draw N by Section 3 and independently draw Y uniformly.
Set

    z=lambda[(|N|^2-1)tau-|N|_1+1],
    A=(rho-1)/(2rho),
    beta=A exp(-z) cos(2pi N.(x-Y)).                 (4.1)

The exponent is nonnegative. Indeed the bracket is
(|N|^2-1)(tau-1)+|N|^2-|N|_1, with both terms nonnegative for a
nonzero integer vector. In particular |beta|<=A<1/2, so its second
moment is at most 1/4. Dot products, integer-square summation, exp
and cos have at most C(d+1) operations in the stated ideal model.
Modulo reduction of the angle can be included at constant cost.

For a fixed n, multiplying its probability (3.1) by A exp(-z) gives

    [q^|n|_1/(rho-1)] A exp(-z)
      =exp(-lambda(|n|^2-1)tau)/M.                 (4.2)

The real Fourier series of p_tau-1, summed over all nonzero integers,
is sum_(n!=0)exp(-lambda|n|^2 tau)cos(2pi n.(x-y)). It has absolute
convergence. Summing (4.2) and integrating against f(y) therefore
gives

    E[beta f(Y)]
      =exp(lambda tau)(P_tau f(x)-Pi f)/M,

as required. Finite total absolute coefficients justify interchange
with integration for bounded Borel f. No stochastic cosine series,
exponential waiting-time kill, heat density, PDE value or unknown
normalizing function is evaluated. The used exp and cos are already
explicitly charged elementary functions in D33's common cost model.

## 5. Two weighted Lyapunov--Perron coefficients

This section records the exact additional interface to a future outer
tree proof, without claiming that full proof here. Fix 0<sigma<nu and
put C_f=M/(nu-sigma), C_b=1/(1+sigma), C=C_f+C_b. For a state (t,x),
use Section 1 at lag t and set

    ell=M exp(-(nu-sigma)t) beta.

Then for any bounded f,

    E[ell f(Y)]=exp(sigma t)(B_t f)(x), E ell^2<=M^2. (5.1)

For the cubic integral, choose forward with probability C_f/C and
backward otherwise. In the forward case draw a waiting time A_f with
rate nu-sigma. If A_f>t, return coefficient zero and any fixed state.
Otherwise put r=t-A_f, draw (beta,Y) at lag A_f from root x, and
return child state (r,Y) and coefficient

    Omega=-C exp(-2sigma r) beta.

In the backward case draw A_b with rate 1+sigma, put r=t+A_b,
draw Y uniformly, and return child state (r,Y) and

    Omega=C exp(-2sigma r).

For every bounded Borel F on time-space, direct integration of these
two waiting-time densities and (1.1) gives

    E[Omega F(r,Y)]
      =-integral_0^t exp(sigma(t-r)) B_(t-r)F(r)(x)
                                     exp(-2sigma r) dr
        +integral_t^infinity exp(-(1+sigma)(r-t))
                                     Pi F(r) exp(-2sigma r) dr. (5.2)

Also E Omega^2<=C^2. Forward coefficients may correlate with the
returned child state; the future child samples must be independent
conditional on that common state in any outer-tree use. No unconditional
independence is asserted or needed. All sampled times are finite
almost surely; null exceptional random inputs can be assigned the
zero coefficient before acquiring any unknown data. Each coefficient
uses at most C0(d+1) elementary operations, uniformly in t.

## 6. Boundaries of this candidate

Equations (1.1), (5.1) and (5.2) are exact actual-kernel statements.
They provide the source and cubic-kernel moment bounds with the same
symbols used by the ternary tilted-moment construction, now for the
changed kappa and the explicitly allowed elementary primitives.

A full upper algorithm must still prove the infinite-tree law and
domination, actual graph identification, all derivative label maps,
independent burn-in batches, hard unknown-query cap, expected total
work and the paid-g/base-solve composition. Those statements cannot
be inferred merely by citing this one heat primitive. Neither a new
full-scope query/work theorem nor measured speed is accepted here.
Independent review is pending. No code, Lean or numerical execution
was used to produce this derivation.
