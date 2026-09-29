# Dynamic invariant interface: conventional theory

Status: the two-dimensional construction has been checked by T01/T02; their detailed notes supply regularity and boundary arguments. The derivative induction and analytic approximation below have also received an independent algebraic audit from T02. These are conventional proofs using named standard PDE inputs, not end-to-end Lean results. Numerical implementation is gated on the finite Lean work.

## 1. Fixed equation and transformed invariant class

Use the previous periodic Allen–Cahn equation u_t=u_xx/2+u−u³, the known stationary Jacobi profileg, and the same normalized spatialL² norm. Put

a=2/21, C=80/441, z=g(x)²∈[0,a], P(z)=z²−2z+C=(z−a)(z−40/21).

Then g'²=P(g²) and g''=−2g+2g³. Consider smooth initial data of the formu₀(x)=g(x)R₀(g(x)²), where

9/10≤R₀≤1, |R₀'|≤1/35, |R₀''|≤1/50 on[0,a].

This is an infinite family of genuinely dynamic data; R₀=9/10 is a concrete example. Symmetries ofg and the initial data persist. Dividingu byg and using the reflection symmetries at zeros and extrema produces a smooth functionR(t,z) at both endpoints. Its equation is

R_t=A(z)R_zz+B(z)R_z+z(R−R³),
A=2zP(z), B=5z²−8z+3C.

The diffusionA is positive in(0,a) and zero at the endpoints. Every derivative equation has inward endpoint drift, so an endpoint maximum contributes a nonpositive drift term. This is a natural degenerate equation; no artificial zero boundary derivative is imposed in thez coordinate.

Forp=R_z,

p_t=A p_zz+(A'+B)p_z+[B'+z(1−3R²)]p+(R−R³).

Its endpoint drifts are5C and6a(a−1). Sincez≤a<1/10 andR≥9/10, its zeroth-order coefficient is≤−7, while0≤R−R³≤1/5. Therefore|p|≤1/35 is invariant by the maximum principle.

Forq=R_zz,

q_t=A q_zz+(2A'+B)q_z+[A''+2B'+z(1−3R²)]q
 +(12−6R²)p−6zR p².

Its endpoint drifts are7C and10a(a−1), its zeroth-order coefficient is≤−20, and the absolute forcing is bounded by12/35+3/(5·35²)<2/5. Hence|q|≤1/50 is invariant. The value interval is invariant as well. Smooth approximation and continuity extend this result toC² data with the same closed bounds; seeT01 for the precise argument.

## 2. Strict stability within the class

OnI=(0,L/2), ψ(x)=sn(κx|m)dn(κx|m)>0 is a Dirichlet ground state forL_g=∂xx/2+1−3g² with eigenvalue−1/7. This classical spectral identity is not a novelty claim; compareWakasa(2006), Theorem3 and Remark4.3, https://www.jstage.jst.go.jp/article/fesi/49/2/49_2_321/_pdf.

Ground-state factorization, followed by density inH₀¹(I), gives

∫[|w'|²/2+(3g²−1)w²]≥(1/7)∫w².

For two odd solutions in the order band(9/10)g≤u,v≤g onI, u²+uv+v²≥3(9/10)²g². The energy identity therefore yields

||S_tu−S_tv||₂≤exp(−μt)||u−v||₂, μ=31/350.

The odd restriction removes the translation mode; this is not a contraction claim on the unrestricted periodic function space.

## 3. A computable two-dimensional admissible interface

LetR_c(z)=c₀(1−z/a)+c₁z/a andv_c=gR_c(g²), with the convex polygon constraints

9/10≤c₀,c₁≤1, |c₁−c₀|≤a/35=2/735.

Every member hasR_c''=0 and belongs to the invariant class. Its value is bounded by√a<2/5 and its derivative by

|v_c'|≤(3/7)(1+2a/35)<1/2.

Thus the previously checked full-tree local certificate applies unchanged: atλ=2 andh≤2/25, E H_Id²≤1/4 and the local mean isS_hv_c.

For any exact evolvingR in the invariant class, interpolate its endpoint values. The interpolant is feasible and

dist(u(t),K)≤β=√a·a²/400<1/140000,

because linear interpolation error is≤a²||R''||∞/8. The exact endpoint values are an existence witness in the proof, not information supplied to the algorithm.

The algorithm uses the known basisb₀=g(1−g²/a), b₁=g³/a. SetG=〈b,bᵀ〉. This Gram matrix is positive definite. Uniform spatial roots and complete local tree outputs giveb̂=N⁻¹ΣH_i b(X_i). The unconstrained coefficient estimate isĉ=G⁻¹b̂. Projectĉ onto the fixed polygon in theG metric. This is a two-dimensional convex quadratic minimization, computable by checking the unconstrained point and the minimum along each of six edges. Using ordinary Euclidean clipping of these nonorthogonal coefficients would implement a different algorithm.

The known stationary functiong is used as a fixed basis throughout; the evolving true solution is never substituted as an intermediate terminal. This use of a known reference and its limitations must remain explicit.

An independent Gram-evaluation identity is available. Write I_k=<g^(2k)>,
I_0=1. In the elliptic parameter convention,
I_1=(40/21)(1-E(m)/K(m)). Integrating the periodic derivative
(g^(2k-1)g')' gives

    (2k+1)I_(k+1)-4kI_k+(2k-1)C I_(k-1)=0,  k>=1.

Consequently I_2=(4I_1-C)/3, I_3=(8I_2-3C I_1)/5, and

    G00=I_1-2I_2/a+I_3/a²,
    G01=I_2/a-I_3/a², G11=I_3/a².

High-precision evaluation of this identity can check a separate quadrature
implementation. Cancellation in these formulas is a reason to use higher
precision; an agreement check is not a rigorous floating-point enclosure.

## 4. Correct projection-defect recurrence

For a finite-dimensional spaceV, closed convexK⊂V, orthogonalP_V and exact targetu_j, setc_j*=Π_Ku_j=Π_KP_Vu_j. The existence of a nearby feasible approximant does not implyP_Vu_j∈K.

The coefficient estimator is conditionally unbiased before projection. Its conditional spatial variance trace is≤dM/N; here d=2 andM=1/4. Projection nonexpansiveness, conditional centering and Minkowski in the joint probability-space norm yield

r_j≤√(q r_(j−1)²+ν)+β,
r_j=(E||v_j−u_j||₂²)^(1/2), q=e^(−2μh), ν=dM/N.

For exact initializationr₀=0, an invariant bound is

r_j≤β/(1−√q)+√[ν/(1−q)]

for every finitej. To verify it, writeb=β/(1−√q), s=√[ν/(1−q)]. Thenq(b+s)²+ν≤(√q b+s)² and√q b+β=b. This handles biased projection without an unjustified cancellation against the true target.

Forh=2/25 andN=100000, x=μh=31/4375, ν=1/200000. Using1−e^(−x)≥x/(1+x),

r_j≤4406/4340000+√(4437/12400000)<1/50.

The last strict inequality is exact: 1/50−4406/4340000=41197/2170000>0 and its square minus4437/12400000 is12242059/4708900000000>0. This is uniform at every grid endpointT=j·.08, with a fixed per-step sample budget. It is sup_j E||error_j||₂² control, not E sup_j||error_j||₂² or a simultaneous pathwise/high-probability bound.

Expected visited tree nodes are bounded byjN(3exp(8/25)−1)/2. This is linear inj for fixed parameters. It does not include basis-evaluation, projection, reference setup, storage or bit-complexity costs. Endpoint-only accuracy on this known-equilibrium benchmark also has the simple returng baseline for sufficiently largeT; this theorem alone is not evidence of superior endpoint complexity.

There is an even stronger baseline limitation, found before any primary
numerical data: the fixed midpoint v_mid=(19/20)g satisfies, for every true
trajectory in the invariant band and every time,

    ||u(t)-v_mid||₂ <= ||g||₂/20 <= sqrt(a)/20 <1/60<1/50.

Therefore the .02 uniform accuracy target is already achieved without any
simulation. The actual normalized-L² midpoint bound is smaller still when
the Gram/elliptic norm is evaluated. The continuation theorem verifies a
mathematical mechanism and general accuracy dependence, but its concrete
.02 witness does not demonstrate useful accuracy beyond prior band knowledge.
Numerical reporting must include this fixed midpoint, not just g and u0.

## 5. A hierarchy for arbitrary accuracy

The degree-n Bernstein family in T01 imposes range bounds on all coefficients,
first differences at most a/(35n), and second differences at most
a²/[50n(n-1)]. These finite linear constraints define a convex polytope of
smooth admissible terminals. The Bernstein approximant using samples of the
true R is a proof witness with distance at most a^(5/2)/(400n). It is not a
true-solution oracle in the algorithm. Combining this approximation with
Section 4 gives a conventional expected-root upper bound O(T ε^(-3)) at
fixed h and fixed local constants. This is not a total arithmetic bound.

For the more regular initial class there is a stronger result. Assume smooth
R0 satisfies the value and C² bounds in Section 1 and, for every k>=1,

    ||R0^(k)||∞ <= M_k,   M_k=(1/70) 2^k k!.

The primary initial datum R0=.9 satisfies these conditions. The exact true
trajectory preserves all of them. Here is the induction, detailed in T02 §8.
Write r_k=∂z^k R and c=1/70. For k>=2 the differentiated equation has drift
kA'+B, damping coefficient at most -D_k, and lower-order forcing, where

    D_k = k(72k+76)/21,
    E_k = k(k-1)(2k+1)+k(1-3R²),
    (r_k)_t = A (r_k)_zz +(kA'+B)(r_k)_z
              +[k((6k+4)z-4k-4)+z(1-3R²)] r_k
              +E_k r_(k-1)-z N_k-k N_(k-1),
    N_k = 3R sum_(i=1)^(k-1) binom(k,i) r_i r_(k-i)
          +sum_(i,j,l>=1; i+j+l=k) k!/(i!j!l!) r_i r_j r_l.

N_1=0. Every factor in N_k has order below k. The endpoint drifts are
(2k+3)C>0 and -76(2k+1)/441<0. Under the induction hypothesis, the absolute
forcing divided by M_k is bounded by

    S_k=(k-1)(2k+1)/2
        +a[3c(k-1)+c²(k-1)(k-2)/2]
        +(3c/2)(k-2)+(c²/4)(k-2)(k-3)
        <=(493/400)k² <(24/7)k² <=D_k.

The apparent triple-count term is zero at k=2,3. The first-derivative base
has damping at least 148/21 and source at most 171/1000<1/5<148/735.
The closed-interval maximum principle from Section 1 therefore proves
|r_k|<=M_k for each finite k, uniformly for all time. Smooth endpoint
factorization and standard parabolic regularity justify the differentiations;
neither follows merely from formally writing the quotient equation.

Let T_n be the degree-n Taylor polynomial of R(t,z) at z=0 and r=4/21.
For j=0,1,2, Taylor's theorem gives the explicit errors

    e_(n,j)=(1/70)2^j (n+1)!/(n+1-j)! r^(n+1-j).

For n>=4 set θ=50e_(n,2) and p_n=(1-θ)T_n+θ(19/20).
Here 0<θ<=25600/64827<1, θ>=20e_(n,0), and θ>=35e_(n,1).
Mixing toward 19/20 opens enough margin to absorb the three Taylor errors.
Thus p_n belongs to the fixed convex set of degree-n polynomials satisfying
.9<=p<=1, |p'|<=1/35, |p''|<=1/50 everywhere on [0,a]. The induced set
K_n={g p(g²)} is compact and convex, and

    sup_(t>=0) dist(u(t),K_n)
       <= (2sqrt(a)/7)n(n+1)(4/21)^(n-1) <= (8/21)^n.

This pointwise polynomial set is different from the Bernstein coefficient
polytope. It must not inherit an implementation or complexity claim from it.
The higher-derivative hypothesis is required only of the fixed true
trajectory. Learned projected terminals need the value/derivative bounds
and order-band contraction; their higher derivatives need not obey M_k.

Consequently choosing d=n+1 with

    n>=max(4, ceil(log(2/[ε(1-exp(-μh))])/log(21/8))),
    N>=4dM/[ε²(1-exp(-2μh))]

gives uniform RMS at most ε and expected tree-root count
O(T ε^(-2) log(1/ε)), at grid endpoints T=Jh and fixed h,μ,M, for exact
metric projection. This is a conventional mathematical sampling bound.
A certified implementation of global polynomial constraints, controlled
projection error, basis conditioning, terminal evaluation and optimizer cost
remain outside this asymptotic claim. The degree-one experiment does not
validate those high-degree costs, and no optimality or novelty is inferred.

## 6. Raw second-moment obstruction on the same dynamic family

The previous run's full-horizon raw rate-two obstruction extends to every
fixed terminal v=gR(g²) in the new class. It is not restricted to stationary
initial data. Since |v|>=.9|g| and |v|<=sqrt(a),

    f(v)² >= (81/100)(19/21)² g² >= (16/25)g².

The last comparison is strict wherever g is nonzero; both sides vanish at
its zeros. This is sufficient for the strict integrated heat seed.

The previous wrapped heat-kernel estimate at time 1 is >1/192, and
integral g²>1/40. Thus the normalized F0 squared-moment field Y0(1,x)
is uniformly >a0=1/12000. The F3 moment is still 36exp(2t).
The same nonnegative restarted Picard comparison, justified by Tonelli even
for extended moments, yields the scalar subsystem

    A_s=A B, B_s=A C, C_s=36A,
    (A,B,C)(0)=(a0,0,0), s=(exp(2t)-exp(2))/2.

Writing Z_s=A gives A=a0+6Z³ and Z_s=a0+6Z³. Its explosion time is

    s*<=12000/30+75=475,
    t*<=log(exp(2)+950)/2<3.5.

For the last inequality, exp(2)<8 and exp(7)>(27/10)^7>958.
The Id mild integral at T=3.5 dominates
(exp(-7)/2) integral_0^(s*) A(s) ds=∞. Positivity propagates this to
all later T. Therefore E H_Id(T,x)²=∞ for all x and T>=3.5 under these
specific unsplit raw sampling parameters, including the dynamic terminal
v=.9g. T01's appendix gives the full comparison audit. This is second-moment
divergence, not an assertion that individual trees explode, nor that every
choice of λ or every branching representation fails.

## 7. The stronger obstruction is independent of importance proposals

There is a more decisive result on this same nonconstant family. It extends
the flat-data absolute-integrability argument in the 2026-09-25 run, using
the heat seed above. The cancellation principle is established methodology,
not a novelty claim; compare Blömker–Romito–Tribe (2007), Theorem 4.1 and
§4.2, and Henry-Labordère–Tan–Touzi, arXiv:1302.4624, Remark 2.14.

Keep the fully expanded original single-tree formula and exact inverse
likelihood weights. Allow any supported clock/tuple importance proposal,
including code-, position-, time- and history-dependent choices, provided
trees complete almost surely and conditional densities, label probabilities
and survival masses are positive almost everywhere on the nonzero canonical
tree mass. Merely topological support is insufficient. This scope excludes
regrouping or cancellation between different signed trees, control variates,
changed branch combiners and the learned continuation approximation.

At finite killed depth, take the absolute value of each complete weighted
tree and cancel its full joint proposal likelihood. This produces the same
nonnegative canonical tree integral for every supported proposal. In the
history-dependent case, perform this cancellation before factorizing the
canonical independent Brownian-child measure; independence under the
proposal itself is not assumed. Almost-sure completion and monotone
convergence pass to the full extended absolute moments W_c.

The resulting minimal positive mild system has no rate or tuple parameter.
In formal PDE notation its reaction is

    W_I,t = heat + W_0,
    W_D,t = heat + W_1 W_D,
    W_0,t = heat + W_0 W_1 + (1/2)W_D² W_2,
    W_1,t = heat + W_0 W_2 + (1/2)W_D² W_3,
    W_2,t = heat + W_0 W_3,
    W_3=6.

Terminal fields are the absolute values of the six terminal codes. These
are nonnegative Volterra identities; the proof never differentiates a field
whose moment has already become infinite.

For v in the stated family, |f(v)|>=(57/70)|g|>=(4/5)|g|, with strict
comparison off the zeros. Since |g|<1/3, integral |g|>3 integral g²>3/40.
At time 1 this gives W_0(1,x)>1/3200. Also f'(v)>=5/7, so W_1(1,x)>=5/7.
Discard the nonnegative derivative contributions and restart a spatially
constant comparison with

    A'=AB, B'=AC, C'=6A,
    (A,B,C)(0)=(1/3200,5/7,0).

Put Z'=A, Z(0)=0. Then

    C=6Z, B=5/7+3Z²,
    A=1/3200+(5/7)Z+Z³,
    Z'=1/3200+(5/7)Z+Z³.

Its lifetime after the restart is bounded by

    integral_0^1 dz/[1/3200+(5/7)z] + integral_1^infinity dz/z³
      =(7/5)log(16007/7)+1/2 <117/10.

The strict bound follows from exp(8)>(8/3)^8>16007/7. Thus explosion occurs
before physical time 127/10<13. The Id mild integral directly dominates
integral A dt=Z, which diverges. Positivity propagates the divergence to
every later horizon. Consequently, for every x and every T>=13,

    E |H_Id(T,x)| = infinity

for every supported, almost-surely-completing importance proposal on this
same original tree expansion. The ordinary first expectation is therefore
not defined as an integrable expectation; calling it unbiased at these
horizons would be unjustified. Second moments are infinite as well.

This obstruction means rate/tuple reweighting alone cannot rescue this
representation on the stated long-time family. It does not mean the PDE
blows up, nor that every tree is infinite, nor that bounded alternative
representations or controlled continuation fail. The explicit threshold is
a conservative upper bound on the onset, not a sharp critical time.

For the uniform raw tuple law, T05 separately proves second-moment failure
by T=14 for every constant rate and by T=17 for positive continuous common
remaining-time rates. Those narrower results are retained as independently
audited intermediate calculations; the absolute-moment theorem gives the
stronger general obstruction here.

## 8. Formalization boundary

Planned finite targets: contraction constant arithmetic; transformed drift/potential polynomial inequalities; interpolation-budget arithmetic; algebraic invariant-radius inequality; the abstract scalar recurrence; final rational RMS budget. The Jacobi identity, maximum principles, Hilbert-space projection, conditional expectations, PDE representation and population interpretation remain conventional unless separately encoded and audited.
