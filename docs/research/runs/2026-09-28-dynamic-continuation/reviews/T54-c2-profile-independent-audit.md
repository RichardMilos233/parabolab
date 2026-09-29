# T54 — independent audit of the general C2 positive-class profile bound

## Verdict and exact statement

**GO for the nonuniform, fixed-reaction, large-time query theorem.** The
scalar coordinate, global profile bound, interpolation estimate, actual PDE
comparison, and sampling-risk calculation are correct. One model
clarification and finite-arithmetic repair should accompany promotion:
the profile table alone does not make `exp(f'(0)*T)` uniformly computable
for an arbitrary fixed `C^2` reaction. Section 6 below removes that issue
for the intended nonuniform theorem using finite public advice at each
horizon, with the same exponent and three error budgets.

There is **no approval of a uniformly computable algorithm for an arbitrary
unrepresented reaction**. The draft itself disclaims that stronger claim;
the qualification must also cover its growth-rate scalar, not just the
profile table. No extra oracle for the unknown datum is needed by the
repaired upper bound.

The audited source is
`reviews/R01-c2-profile-generalization-draft.md`, SHA-256
`f3fae210587e3349ebd105b1f5b0dbdc4011b9dff504d08549eac1e8bea0876e`.
I also checked its dependencies in
`04p-fixed-zero-query-lower-bound.md` and
`04q-matching-positive-query-complexity.md`.

Precisely, fix `b,R>0`, positive integers `d,s`, and

    f in C^2([0,b]), f(0)=f(b)=0, f>0 on (0,b),
    lambda=f'(0)>0,  epsilon in (0,b/2).

On the normalized unit torus use the fixed class of smooth periodic `v`
with `0<=v<=b/2` and `C^s,max` norm at most `R`. Under the exact
initial-value point-query model in 04p, there are constants `c,C,T0>0`
depending on these fixed public parameters such that, for `T>=T0`,

    c exp(lambda*d*T/(s+d))
       <= inf_{uniform RMS<=epsilon algorithms} sup_v E Q_T(v)
       <= C exp(lambda*d*T/(s+d)).

The upper algorithm has a deterministic number of queries and generally
biased output. Horizon-specific algorithms and public advice are permitted
in this infimum. Neither advice nor preprocessing may depend on the unknown
`v`. The lower bound still includes arbitrary adaptive locations, random
stopping, and bias. No signed-class extension, variable-accuracy order,
bit-complexity bound, practical speed claim, or novelty claim is approved.
This is a conventional proof audit; no Lean, code, or numerics were added.

## 1. Scalar conjugacy and endpoints

Write `M=max(1,||f''||_infinity)` as in the draft. Taylor's theorem gives

    |f(y)-lambda*y| <= M*y^2/2.

For `0<y<=lambda/M` within the domain, `f(y)>=lambda*y/2` and

    |1/f(y)-1/(lambda*y)| <= M/lambda^2.

The integral defining `G` is consequently finite at zero. In fact the
integrand has a continuous removable extension there, although boundedness
alone is sufficient for the proof. Thus `G(y)/y ->1`, and direct
differentiation gives `G'/G=lambda/f>0`.

At the other endpoint, let `Lf=||f'||_infinity>0`. The endpoint condition
and positivity imply `0<f(y)<=Lf*(b-y)`, so `integral dy/f(y)` diverges
as `y` approaches `b` from below. Hence `G(y)` increases from zero to
infinity. No simple root at `b` is required. Its inverse `Phi` is defined
on the whole nonnegative half-line, approaches `b` at infinity, and has
right derivative one at zero. For positive arguments,

    Phi'(z)=f(Phi(z))/(lambda*z).

The scalar ODE never reaches either endpoint in finite time from an
interior initial value. Differentiating `G(ell_c(t))` proves exactly

    ell_c(t)=Phi(exp(lambda*t)*G(c)).

No linearized formula is substituted for the nonlinear flow.

## 2. The global anchored bound and height versus mass

Set `r0=min(b/2,lambda/M)`. For `y<=r0`, the integral bound gives
`G(y)>=e^(-1)y`, while `f(y)<=3lambda*y/2`. For `y>=r0`, monotonicity
gives `G(y)>=e^(-1)r0`, and `f(y)<=Fmax=(lambda+Mb/2)b`. These bounds
prove the displayed global `Lphi`. Also
`z Phi'(z)<=Dphi=Fmax/lambda`.

The three cases proving (A) are exhaustive, including `x=0` or `z=0`.
When `z>1` and `x<=z/2`, the range bound `b` is controlled by
`4b|x-z|/(1+z)`. When `z>1` and `x>=z/2`, all intermediate arguments
are at least `z/2`, so the derivative bound is `2Dphi/z`, which is at
most `4Dphi/(1+z)`. The small-`z` case uses `2Lphi`.
Thus, with the stated `Kphi`,

    |Phi(x)-Phi(z)| <= Kphi |x-z|/(1+z)

holds globally. In particular, multiplicative argument error `q` costs
at most `Kphi|q-1|`, uniformly in the argument. This step uses neither
concavity nor the KPP upper inequality `f(y)<=lambda*y`.

The 04q polynomial reproducing kernel works with an arbitrary positive
norm radius `R`. Its Taylor remainder becomes
`BR(d/2)^s h^s/s!`. Nonnegativity and the scaled cube's injectivity on
the torus give the other term `B h^(-d)m`. With
`beta=s/(s+d)`, the choice `h=m^(1/(s+d))` gives the stated bound for
`0<m<=1`. If `m>=1`, the extra `b/2` in the public constant `C` handles
the height; if `m=0`, continuity and nonnegativity force `v=0`.
Therefore

    ||v||_infinity <= C m^beta

holds for the entire fixed class, including every finite `s` and arbitrary
`b,R>0`. The signed reproducing kernel is legitimate; a positive
high-order kernel is not assumed. `R>0` is material: with radius zero the
class would consist only of zero and the positive lower rate would fail.

## 3. Actual nonlinear PDE reduction and thresholds

Extending `f` locally off its compact interval, if needed to state local
well-posedness, does not affect the solution: comparison with the constant
solutions zero and `b` preserves `[0,b]`. Local Lipschitz regularity and
this bound give a global classical solution for the smooth initial data.
All estimates use `f` only on `[0,b]`.

Let `A=||v||_infinity` and `Lambda=lambda+Mb/2`. Since
`f(y)<=Lambda*y`, actual parabolic comparison gives
`u(t)<=e^(Lambda*t)P_t v<=Ae^(Lambda*t)`. The Taylor estimate then bounds
the solution's time-dependent potential by

    |f(u)/u-lambda| <= (MA/2)e^(Lambda*t),

using the continuous value at zero. Comparison with spatially constant
linear potentials proves both sides of the draft's bound

    e^(lambda*t-E(t))P_t v <=u(t)<=e^(lambda*t+E(t))P_t v,
    E(t)=MA(e^(Lambda*t)-1)/(2Lambda).

This controls the actual early nonlinear evolution, not a closed mean
equation. All constants are finite and positive because `lambda,M,C,L`
are positive; in particular `Efac>0`.

The heat-mixing choice is valid in every fixed dimension. Writing
`r=e^(-2pi^2 L)<=eta/(8d)`, the Fourier bound is

    ||p_L-1||_infinity
       <=((1+r)/(1-r))^d-1 <=e^(4dr)-1 <=eta.

For `m<=m0`, the height bound and the third entry of the minimum defining
`m0` ensure `E(L)<=eta`. The last entry ensures
`e^(lambda L)m<=csmall/2`. Since `(1+eta)e^eta<2` for
`eta<=1/16`, both comparison endpoints `c-,c+` lie in `[0,csmall]`.
In this interval

    |lambda integral_0^c r(y)dy| <= Mc/lambda <=eta.

For `m>0`, the precise later-time multipliers are

    q+/- = e^(-lambda L)G(c+/-)/m.

They are ordered because `G` is increasing and satisfy the claimed
bounds `(1-eta)e^(-2eta)<=q-<=q+<=(1+eta)e^(2eta)`.
The lower bound is at least `1-3eta`. For the upper bound,
`e^(1/8)<=8/7` implies
`e^(2t)(3+2t)<=25/7<4` on `[0,1/16]`, proving `q+<=1+4eta`.
Both multipliers are therefore within `4eta` of one. Scalar comparison
and (A) give the uniform small-mass PDE bias `4Kphi eta` for all `T>=L`.
At `m=0`, zero is an exact solution and there is no division by `m`.

For `m>=m0`, `f>=0` implies
`u(1)>=P_1v>=kappa*m0=c0`. Here `0<c0<b/2`, because `kappa<1` and
`m0<=b/2`. Thus `G(c0)` is defined. The selected `theta` lies strictly
between `c0` and `b`; both logarithms in `T*` have valid positive
arguments. The first scalar threshold makes
`ell_c0(T-1)>=theta`; the second makes
`Phi(e^(lambda T)m)>=theta`. Since both quantities are at most `b`,
their difference is at most `b-theta`. Taking the maximum with `L>=1`
also ensures that all later scalar time intervals are nonnegative.

For the final three-budget construction, recompute `m0,T*` using
`eta=min(1/16,epsilon/(12Kphi))` and `theta=b-epsilon/3`. The result is

    sup_v ||S_Tv-Phi(e^(lambda T) integral v)||_infinity
       <=epsilon/3, T>=T*.

The split by the unknown mass is only in the proof. The proposed algorithm
never determines which case holds, queries the mass, or evaluates a PDE
solution at an intermediate time. No condition comparing `lambda` with a
spectral gap is required by this positive-data argument.

## 4. Actual sampling risk and the matching lower bound

For iid uniform queries, the actual sample mean is unbiased for the
unknown mass and has

    E(mhat-m)^2 <= integral v^2/n <= C m^(1+beta)/n.

This is a direct variance statement about the proposed observations.
Applying (A) with `x=e^(lambda T)mhat` and `z=e^(lambda T)m` gives

    E|Phi(e^(lambda T)mhat)-Phi(z)|^2
       <= [Kphi^2 C e^(lambda(1-beta)T)/n]
           * z^(1+beta)/(1+z)^2.

The ratio is at most one: use its numerator bound when `z<=1` and
`z^(beta-1)<=1` when `z>=1`. The choice
`n=ceil(9Kphi^2 C epsilon^(-2)e^(lambda(1-beta)T))` gives sampling RMS
at most `epsilon/3`. This includes missed bumps and a zero sample mean;
no relative mass-estimation guarantee is assumed.

The lower reaction extension in 04p applies to the same class after its
norm radius `L` is renamed `R`. Choose any
`theta_lower in (max(b/2,2epsilon),b)` and a fixed bump amplitude
`0<a<=min(b/2,R/D)`. The Taylor estimate above makes
`J_theta=integral_0^theta |1/f(y)-1/(lambda*y)|dy` finite. Separation of
variables gives

    tau(c,theta) <=lambda^(-1)log(B_theta/c),
    B_theta=theta exp(lambda J_theta),

when `0<c<=theta`; if already above `theta`, no hitting-time estimate
is needed. Heat minorization and the grid in 04p therefore give targets
at least `theta_lower` after the stated threshold. Its paired-loss/no-hit
argument yields

    E Q_T(0) >= (1-4epsilon^2/theta_lower^2) k^d.

The prefactor is strictly positive. The floor bound gives the rate
`exp(lambda*d*T/(s+d))`, matching `1-beta=d/(s+d)` in the upper bound.
Take the maximum of the fixed upper and lower time thresholds. Exact
initial-value queries, fixed accuracy, and the promised class agree on
both sides; the upper bound is not matched to a weaker oracle or class.

## 5. What the draft's finite table does and does not establish

The displayed original table has uniform error at most `epsilon/3`:
Lipschitz error on a grid interval and its stored-value error each cost
at most `epsilon/6`; the tail is controlled by proximity to `b`. This
argument is correct. A finite rational endpoint and rational grid can
always be chosen, and the table depends only on the fixed public
parameters, not on `v` or `T`.

However, for arbitrary fixed `f`, its derivative `lambda` need not be a
computable real. A finite table for `Phi` does not by itself supply a
uniform procedure for computing `e^(lambda T)`, or the exact displayed
ceiling defining the sample count, as `T` varies. The sentence describing
an ordinary finite-table version should therefore not be read as a
single uniformly computable algorithm for arbitrary unrepresented `f`.
The issue is public parameter access, not an extra unknown-input query.

For the abstract measurable-transformation information model, the ideal
profile proof already gives an upper bound. If a finite arithmetic/table
procedure is desired, the following explicit repair makes the nonuniform
interpretation precise without invoking any exact profile or reaction
oracle during the run.

## 6. Finite-advice repair preserving the three error budgets

Keep the draft's final `eta`, `theta`, and sample-count formula. At each
fixed horizon `T`, choose and hard-code the finite integer

    N_T=ceil(9Kphi^2 C epsilon^(-2)e^(lambda(1-beta)T))

and a positive rational `a_T` satisfying

    |a_T/e^(lambda T)-1| <=epsilon/(6Kphi).

These exist for each public horizon; no uniformly computable rule for
choosing them from an arbitrary unrepresented `f` is asserted. The count
remains `O(e^(lambda*d*T/(s+d)))`. Hard-coding an integer avoids requiring
an online exact-real ceiling operation.

Tighten the fixed table to uniform error `epsilon/6`:

- Choose a rational `zmax` with `Phi(zmax)>=b-epsilon/12`.
- Use a rational grid with mesh at most `epsilon/(12Lphi)`.
- Choose rational stored values within `epsilon/12` of `Phi` at the
  left endpoints, and a rational tail value within `epsilon/12` of `b`.

No clipping is needed. Rational stored outputs may lie outside `[0,b]`;
the approximation bounds already suffice. Thus the run needs no exact
comparison with a potentially noncomputable endpoint. The table is finite,
independent of `T`, and may be fixed before receiving any unknown input.

After the `N_T` charged queries, return this table applied to `a_T*mhat`.
The global anchored estimate gives, for every possible sample mean,

    |Phi(a_T*mhat)-Phi(e^(lambda T)*mhat)| <=epsilon/6.

Together with the table error this consumes at most `epsilon/3` uniformly.
Sampling RMS and PDE bias each consume at most `epsilon/3` as already
proved. The `L^2` triangle inequality yields total RMS at most `epsilon`.
All online scalar constants can now be finite rational advice and the
sample count a finite integer. Sampling uniform real points and exact
value queries still have their usual idealized information-model meaning;
this is not a finite-random-bit or bit-complexity theorem.

Thus the precise accepted quantifier is: for each sufficiently large
public horizon there exists such a finite oracle procedure, with public
advice depending on `f,b,R,d,s,epsilon,T` but never on `v`. A uniformly
effective construction would require a specified computable representation
of the public parameters and reaction, certified derivative bounds, and
certified scalar approximation. It is a separate assertion and is not
needed for this nonuniform minimax query order.

## 7. Attribution and promotion scope

[Hairer–Lê–Rosati, equation (1.5), Theorem 2.1, and Proposition 4.6](https://arxiv.org/pdf/2201.08426)
are primary prior for nonlinear scalar transition profiles in Allen–Cahn
growth from small random initial data. The inspected results use a
different random-field and spatial scaling setting; they do not supply
the present arbitrary-`C^2`, deterministic-class query theorem. The scalar
coordinate here is directly justified by separation of variables, and
the kernel and sampling arguments are explicit in the audited documents.
No additional broad literature search was performed and no priority
assessment follows.

Promotion is justified with the nonuniform qualification and finite-advice
repair above. The analytical estimates need no correction. A claim of
uniform computability for arbitrary `f`, or a claim that a fixed finite
table alone supplies all horizon-dependent public constants, should not
be promoted. Only this new audit report was changed; the source draft and
all earlier frozen reports remain untouched by this audit.
