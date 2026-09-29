# T32: minorized burn-in and affine Bernoulli-factory audit

Date: 2026-09-28. Independent mathematical review of
`04n-minorized-burnin-factory.md`, reviewed SHA-256
`753c1a411c8cd7e9a080ee375a1293b8ebe01ace0cca99f02c92979fc9f4e384`.
Frozen T27 and T30 were preserved. This task read the requested primary
factory papers, performed no broad novelty survey, and wrote no Lean or code.
Role: research reviewer; actual service model/effort is not independently
exposed here. The previously read math-auto-research instructions apply.

## Verdict

**Pass in the stated ideal oracle model, with Huber's factory theorem as an
explicit imported result.** The burn-in inequalities, exact `p`-coin law,
complements, amplification domains, strict slacks and the constant `1444`
are correct. The nested cost product and outer-tree bound are valid under
fresh, conditionally independent subcalls. A proof of that conditioning step
is given below; independence of the final stopping count and call costs is
neither true in general nor needed.

The construction does not use an oracle evaluating `u(t0,x)`. It uses the
initial-data and transition oracles to generate coins whose mean is that
unknown value. The result removes pointwise separation from zero and one
under the specified uniform minorization and positive mass certificates.
It does not provide a finite-bit exact sampler or a practical efficiency
bound. No unresolved mathematical gap was found within this contract.

The contract must retain all of the following: a conservative jointly
measurable Markov transition semigroup, exact independent transition draws,
an exact bounded initial-data/leaf-coin oracle, certified constants
`t0>0`, `0<eta<=1`, `delta0>0`, `delta1>0`, `delta0+delta1<=1`, and the
uniform minorization `P_t0(x,dy)>=eta*pi(dy)` for every query state. Known
factory-parameter auxiliary distributions are interpreted in the same ideal
oracle model. Obtaining these certificates or implementing these oracles
is not included in the counted work.

## 1. Deterministic interior bounds

For the unique bounded mild Allen–Cahn solution, comparison gives `0<=u<=1`.
On this interval `f(u)=u-u^3>=0`, so positivity of the semigroup in the mild
equation gives

```
u(t)>=P_t v.
```

For `D=1-u`, conservativity is essential to obtain

```
D_t=L D-k D,   k=u+u^2 in [0,2].
```

No unprovided Feynman–Kac path oracle is needed for the lower bound. Rewriting
the mild equation with killing rate `2` gives

```
D(t)=exp(-2t)P_t(1-v)
   + integral_0^t exp(-2(t-s))P_(t-s)[(2-k(s))D(s)]ds
 >= exp(-2t)P_t(1-v).
```

Minorization and the certified mass bounds therefore imply, for every `x`,

```
L=eta*delta0 <= p(x)=u(t0,x)
             <= U=1-eta*exp(-2t0)*delta1.
```

The strict ordering claimed in the source is justified even if the mass
bounds sum to one and `eta=1`:

```
U-L = 1-eta*(delta0+delta1)
      +eta*(1-exp(-2t0))*delta1 > 0.
```

Both terms before the strict inequality are nonnegative, and the second is
strictly positive. Thus `0<L<U<1`. Set

```
a=L/2,   b=(1+U)/2.
```

Then `0<a<L<=p<=U<b<1`, as required. The measure `pi` is used only to justify
the global bounds. The algorithm need not integrate the unknown evolved
solution against `pi` or sample a residual minorization kernel.

## 2. The burn-in coin law and its work

For rate `2` and ternary Bernstein coefficients `(0,1/2,1,1)`,

```
B(z)=(3/2)z(1-z)^2+3z^2(1-z)+z^3
    =(3/2)z-(1/2)z^3,
2(B(z)-z)=z-z^3.
```

At each time-zero leaf, generate a Bernoulli variable of mean `v(Y)`. At an
internal vertex with `k` successful child votes, return a Bernoulli variable
with mean the corresponding coefficient, using an independent auxiliary
coin when `k=1`. This is a binary output at every vertex; it is not an
unbounded affine transformation of an estimator.

Finite-generation count domination proves completion of the full rate-2
ternary tree at the fixed horizon `t0`, independently of its returns. Its
expected visited nodes are

```
B0=(3 exp(4t0)-1)/2.
```

Conditional child independence gives the displayed polynomial mean. The
bounded first-event equation and uniqueness of the bounded mild solution
then give an exact `Bernoulli(p(x))` root. Repeated fresh runs at a fixed
location `x` produce iid `p(x)`-coins. The node-cost law may correlate with
the returned bit; that fact must remain visible in the later cost argument.

At random leaf locations the same statement holds conditionally on the
location, uniformly over all locations. The input data may take the values
zero and one: the ideal Bernoulli leaf at such values is well-defined. This
does not by itself resolve the earlier finite-information obstruction for
arbitrary boundary-touching measurable data.

## 3. The primary theorem actually imported

[Huber, *Nearly optimal Bernoulli factories for linear functions*, Theorem 1](https://arxiv.org/pdf/1308.1562v2)
states the uniform bound `9.5 C/epsilon` for the Section 2 algorithm on the
domain `C>1`, `p in [0,(1-epsilon)/C]`. Definition 1 identifies its running
time as the number of input Bernoulli observations and permits independent
auxiliary randomness. The pseudocode also uses known-parameter geometric
draws and auxiliary Bernoulli draws. The theorem is therefore an input-call
bound, not a count of all random bits or scalar arithmetic. Both slacks below
are less than `1/2`, so they do not encounter the pseudocode's `0.644`
slack cap. The theorem and relevant definition/pseudocode were read directly.

[Nacu–Peres, *Fast simulation of new coins from old*, Theorem 2](https://arxiv.org/pdf/math/0309222)
provides an analytic-function existence result on a closed interval contained
in `(0,1)` when the target stays in `(0,1)`. The remark after Definition 1,
made precise by Proposition 21, makes the exponential tail constants uniform
on a closed domain. This applies to the affine target on `[L,U]` and supports
the source's contextual statement. Its existential constants are not used
in the displayed work budget.

Neither paper's result is newly proved here, and neither is presently a Lean
dependency that has been checked in this project. The conventional theorem
below explicitly depends on Huber's published correctness and expectation
bound.

## 4. Both factory stages and every slack

Using the source's definitions,

```
C1=1/(1-a),
epsilon1=(L-a)/(2(1-a)),
C2=(1-a)/(b-a),
epsilon2=(b-U)/(2(b-a)),
```

all denominators are positive. Since `a>0` and `b<1`, both `C1,C2>1`.
Moreover

```
epsilon1=L/[4(1-L/2)] in (0,1/2),
epsilon2=(1-U)/[2(1+U-L)] in (0,1/2).
```

Factory 1 consumes complemented raw `p`-coins and returns a bit of mean
`C1(1-p)=(1-p)/(1-a)`. Its admissibility follows from

```
C1(1-p) <= (1-L)/(1-a) = 1-2epsilon1 < 1-epsilon1.
```

Complementing that output gives a coin of mean

```
q=1-(1-p)/(1-a)=(p-a)/(1-a).
```

Factory 2 consumes fresh iid versions of these `q`-coins, and

```
C2 q=(p-a)/(b-a),
C2 q <= (U-a)/(b-a)=1-2epsilon2 < 1-epsilon2.
```

Both input means are nonnegative, and all target means are strictly between
zero and one. The calls are safely inside the imported theorem's domain,
including when `p=L` or `p=U`. The extra factor of two in each slack is
conservative; it is not a domain mistake.

Let `B1` bound raw `p`-coin calls in one Factory 1 run, and `B2` bound
Factory 2's requested `q`-coins. Huber's bounds simplify to

```
B1=9.5 C1/epsilon1 = 38/L,
B2=9.5 C2/epsilon2 = 38(1-a)/(1-U),
B1 B2 = 1444(1-L/2)/(L(1-U)) = B_factory.
```

The target affine identity, admissibility and constant all pass independently
of any implementation. No step evaluates the unknown number `p(x)`.

## 5. Random stopping, nested work and completion

Here is the precise lemma needed for the product of budgets. Suppose an
algorithm requests calls sequentially, `N` is its eventual number of
requests, and `C_j>=0` is the cost of call `j`. The event `{N>=j}` must be
decided from the history before call `j`. If fresh subcall randomness gives

```
E[C_j | history before call j] <= B
```

on that event, then Tonelli and conditional expectation give

```
E[sum_(j=1)^N C_j]
 = sum_j E[1_{N>=j} C_j]
 <= B sum_j P(N>=j) = B E[N].
```

There is no hypothesis that `C_j` is independent of the bit it returns, or
that costs are independent of `N`. Conditioning on an eventual output or
on `N` and then multiplying unconditional means would not be justified.

For Factory 2, the next fresh Factory 1 run, including its cost and returned
bit, is independent of the previous history conditional on the fixed spatial
location. Its mean raw-call cost is at most `B1`, uniformly over admissible
`p`. The lemma gives expected raw `p` calls at most `B1 B2`.

Apply the same lemma inside Factory 1: the next burn-in tree is fresh before
its coin is read and has conditional expected node count `B0`. Thus the
expected burn-in tree nodes consumed by one completed affine factory are
at most `B_factory B0`. One may equivalently flatten all raw-coin requests;
the decision to request each next tree is predictable in the same way.

Completion is also valid. First construct countably many independent
potential burn-in calls, each almost surely finite. Conditional on a fixed
location, they supply the iid input stream for Factory 1, whose requested
call count is almost surely finite by the imported theorem. Fresh copies
give iid `q`-coins to Factory 2, which also stops almost surely. Countable
intersections and the uniform conditional statements handle the arrays of
possible calls. The finite expected budgets above additionally rule out
infinite counted work. The proof does not assume a completed infinite
recursive computation in order to justify its expectation.

## 6. Outer leaves, nonlinear restart and combined bound

For `T>=t0`, put `S=T-t0`. Autonomy of the reaction, the semigroup law and
uniqueness of bounded mild solutions imply the nonlinear restart identity:
evolving the datum `p=u(t0)` for time `S` yields `u(T)`.

The outer two-barrier mixed tree uses scalar initial bounds `a,b`. It can be
generated independently of its leaf returns: its rates and offspring
probabilities depend on the deterministic scalar flows and times. Condition
on this finite outer skeleton, including all leaf locations `Y_j`. At leaf
`j`, the affine factory returns a Bernoulli variable with conditional mean

```
(p(Y_j)-a)/(b-a),
```

using randomness disjoint from every other leaf. These returns are
conditionally independent. Their shared, unknown deterministic function
`p` does not create probabilistic dependence. They need not be independent
after forgetting the correlated outer locations; that is not the property
required by the branching proof.

The ordinary bounded voting renewal proof therefore identifies the outer
mean with the restarted solution. Every normalized leaf is in `{0,1}`, so
the outer return remains in `[0,1]`. In the selected OR/majority binary-vote
implementation the root is itself a bit. Consequently the signed solution
and defect outputs obey exactly the two-barrier range guarantee at horizon
`S`, with initial phase bounds `a,b`, and are unbiased for `u(T,x)` and
`1-u(T,x)`.

Let `N_out` and `L_out` be outer nodes and leaves. The existing mixed-tree
bound gives `E N_out<=K_work` and pathwise `L_out<=N_out`. Conditional on the
skeleton, each leaf factory costs at most `B_factory B0` expected burn-in
nodes. Therefore

```
E combined_tree_nodes
 <= E N_out + B_factory B0 E L_out
 <= K_work*(1+B_factory B0).
```

This is uniform over finite `T>=t0` and all query states. With the sharper
mixed bound one may take

```
z0=a/b,
K_work=(1+z0)^2/(2*z0^(5/2))-1.
```

No independence between outer leaf count, leaf locations, final output or
total cost was assumed. At `T=t0` the outer tree has one leaf, so the same
construction and bound apply without a limiting argument.

The uniform relative variance follows from the positive output interval and
the established scalar defect ratio for `a,b`. A deterministic number of
fully independent final roots gives the relative RMS guarantee. The
factory's internal sample count may adapt; the prescribed number of final
roots in this guarantee does not adapt to their observed outcomes.

## 7. Falsification attempts and limits

- Exact initial zeros or ones cause no theoretical leaf-coin failure under
  the stipulated exact oracle. Constant data identically zero or one cannot
  satisfy both positive mass bounds and are excluded rather than repaired.
- Letting either mass certificate or `eta` vanish destroys the positive
  margins and makes the displayed factory bound diverge. Removing uniform
  minorization does not preserve the claimed state-uniform theorem.
- Correlation of a burn-in bit with its node count does not refute the cost
  product because requests are predictable. Reusing a realized burn-in tree
  or a Factory 1 output as several purported iid inputs would invalidate
  the proof; fresh subcalls are substantive assumptions.
- Directly returning `(Bernoulli(p)-a)/(b-a)` would sometimes be negative
  or exceed one. The two factory stages, including the intermediate
  complement, supply the proposed bounded leaf contract; substituting the
  direct affine random value changes the argument. This does not assert
  that every valid construction must use two factories.
- The mean-only bound `L<=p<=U` is not silently upgraded to a pathwise bound
  on burn-in votes. Those votes remain zero or one. The factory theorem is
  exactly the bridge from iid votes to the required transformed mean.
- The work statement counts outer and burn-in tree nodes. It excludes
  factory arithmetic, auxiliary geometric/Bernoulli draws, bit generation,
  exact comparisons, leaf-value evaluation costs, transition costs and the
  derivation of minorization/mass certificates. Huber's theorem supplies no
  permission to identify input-call work with all these costs.

For the deterministic comparator, use the **tighter genuine mean bounds**
`L,U`, rather than the deliberately widened factory bounds `a,b`. At outer
time `S`, scalar comparison already gives a defect interval
`[1-ell_U(S), 1-ell_L(S)]`. Its harmonic-center estimate and relative-error
guarantee require no spatial queries. A meaningful future accuracy regime
should beat that comparator. The current large sufficient constants establish
an ideal existence/work result, not a practical advantage.

The preceding finite-information obstruction for arbitrary measurable
boundary data remains outside this ideal theorem. Exact oracle coin generation
does not constitute a finite-precision construction. No originality claim is
supported by this audit; linear factories, general analytic factories and
their composition are imported established methods.

## 8. Fixed possible formal algebra targets

The conventional mathematics above passes. The following are now precise
finite algebra targets for a separately selected gate, not declarations
claimed to have been built.

1. **Margins from minorization constants.** Given `0<eta<=1`, positive
   `delta0,delta1` with sum at most one, and `0<e<1`, define
   `L=eta*delta0`, `U=1-eta*e*delta1`; prove `0<L<U<1` using the decomposition
   in Section 1. Link `e=exp(-2t0)` separately to `t0>0`.
2. **Factory domain algebra.** From `0<L<=p<=U<1`, `L<U`, and the displayed
   `a,b,C1,C2,epsilon1,epsilon2`, prove positive denominators, `C_i>1`,
   `0<epsilon_i<1/2`, both strict-slack inequalities, and
   `C2*(1-C1*(1-p))=(p-a)/(b-a)` with target in `(0,1)`.
3. **Imported-budget arithmetic.** Using `9.5=19/2`, prove
   `B1=38/L`, `B2=38(1-L/2)/(1-U)` and
   `B1*B2=1444(1-L/2)/(L*(1-U))`. A formal theorem conditional on these
   budgets is not a formal proof of Huber's factory algorithm.
4. **Burn-in polynomial identity.** Prove the ternary Bernstein expansion
   and `2(B(z)-z)=z-z^3`, together with the coefficient/range bounds.
   The PDE and probabilistic mean identification are separate obligations.
5. **Cost transfer algebra.** Given nonnegative expected-count quantities
   satisfying `E L_out<=E N_out<=K_work` and conditional-cost consequences
   as stated, prove the final sum bound. Keep the predictable-request/Tonelli
   lemma, conditional independence, almost-sure completion and restart
   proof separately labelled if they are not formalized.

In particular, no algebra-only gate certifies the burn-in PDE inequalities,
the external Bernoulli-factory theorem, stochastic stopping-cost composition,
kernel measurability, nonlinear semigroup restart, or finite-bit implementation.
Those dependencies are explicit rather than hidden in an unknown PDE-value
oracle.
