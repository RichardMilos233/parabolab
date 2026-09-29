# R08: what remains between optimal queries and a useful signed algorithm

Root research note, 2026-09-29 local date. This is a prospective work
contract and a cost audit of one explicit construction, not a new accepted
theorem. D27 is accepted only for `d<=4s`; D28 gives the all-dimension lower.
R07/T65's all-dimension upper is still under construction/review.

## 1. An explicit implementation can lose the desired time exponent

T56 Section 6 constructs a positive fine partition `theta_i`, a residual
interpolant `Pr=sum_i r(z_i)theta_i`, and complete tables of first and
second derivative coefficients. Its residual has a public Lipschitz bound
independent of the paid coarse-grid size. To make the linear discretization
error at most a constant times `eta`, a safe uniform partition choice has
support diameter `h<=c*eta`, with fixed `c>0` depending on that Lipschitz
bound and the derivative TV bounds.

Choose explicitly `m=ceil(C/eta)` nodes in each coordinate, with a fixed
sufficiently large `C`. This valid realization has

    N=m^d=Theta(eta^(-d))

partition elements. T56 enumerates all `N^2` quadratic entries using
known-profile phase finite differences. Even before accounting for the
cost of a single phase solve, materializing this full table costs at least
`N^2` writes/arithmetic operations. With its `eta=exp(-T)/64`, this chosen
realization costs at least order `exp(2dT)` for the full table, whereas the
proved unknown-input query cap is order `exp(2dT/(2s+d))`.

This is deliberately a statement about that specific safe partition and
full-table implementation. It is **not** an arithmetic lower bound for all
implementations, an assertion that this mesh is necessary, or a defect in
the information-model theorem. Other approximations or implicit tables may
be much cheaper. In an order-`J-1` extension, a complete analogous tensor
can have `N^(J-1)` entries. Actual coefficient sparsity or fast sampling has
to be proved; bounded total variation alone supplies neither.

The phase evaluations are an additional cost. Finite differences require
more accurate phase values as their steps decrease. The proof that some
finite monotone PDE mesh works does not bound this cost by the query cap.

## 2. A concrete stronger target

Retain the same unknown fixed signed C^s class, exact initial point oracle,
fixed unit torus and absolute RMS target `1/4`. Do not add a supplied phase,
derivative, evolved-value, or known-formula oracle.

The next useful theorem would exhibit a uniform implementation with

    expected initial queries <= C exp(gamma*T),
    expected arithmetic work <= C (1+T)^p exp(gamma*T),
    gamma=2d/(2s+d),

for fixed `d,s`, or else give a precise larger work exponent with an
explained cause. This target is not established. Initially use a stated
real-arithmetic and random-sampling cost model; bit complexity requires a
separate precision analysis. Input acquisition is always charged, while
evaluations of the interpolant built from paid values must still be counted
in arithmetic work. Preprocessing cannot be hidden just because it has no
new unknown-input queries.

The full target has two separate obligations:

1. Evaluate the known coarse-profile phase or graph functional to absolute
   accuracy `O(exp(-T))` at near-query-order arithmetic cost.
2. Sample its derivative residual corrections without enumerating the
   enormous fine coefficient tensors, with bounds on both second moment
   and work, including every inner approximation or randomization.

Solving only the second does not solve the first. A bounded-variance
unbiased base-phase estimator averaged to error `exp(-T)` generally needs
order `exp(2T)` samples. Since `gamma<2` for fixed `s>0`, that naive step
would already lose the target exponent even with free coefficient access.
This is a warning about the standard sample-average bound, not a universal
lower bound on all ways of computing the known phase.

## 3. Ranked candidate routes and failure tests

**First: exploit the explicit interpolant and parabolic smoothing for the
base value.** The paid interpolant is not an arbitrary unknown function;
it is a fixed local formula with `k^d` coefficients. Investigate whether
high-order integration within cells, fast heat convolution and a stable
graph evaluation yield exponential accuracy in a polynomial number of
precision levels with work `k^d poly(T)`. Required proof: uniform error
and cost over all admissible coefficient vectors, including initial
high-frequency layers and sign cancellation. Spatial smoothing after a
fixed time alone does not prove cheap evolution up to that time. A generic
low-order mesh refinement may reintroduce an exponential cost in accuracy.

**Second: sample explicit derivative heat-tree kernels directly.** T65's
proposed measure construction gives a structural starting point. To use it
algorithmically, supply a simulable positive proposal, actual signed
weights, fixed-order derivative labels, and simultaneous bounds on
`E(weight^2)` and the full tree/inner-solve work. The Lyapunov--Perron map's
small operator norm need not imply a small second moment for a particular
simulation. Also, a small centered field can be the difference of two
large noisy quantities; centering its mean is not a variance proof.

**Third: matrix-free derivative actions or compression.** Incremental
state/adjoint solves can avoid explicit coefficient tensors. But a
directional derivative action is not automatically a point-tuple sample
with the needed law and bounded importance weight. Uniform low-rank or
sparse structure on the whole input class must be established before
claiming cost savings. Numerical rank on selected examples is insufficient.

Each route must preserve the near-stable-boundary class where the phase
is `O(exp(-T))`. Restricting to inputs whose phase is separated from zero
would evade the present difficulty and answer a different problem.

## 4. Bounded primary-literature check

Four search queries examined randomized smooth functionals, validated
parabolic stable manifolds, higher-order control variates, and the title
of the following Taylor paper. This is a targeted implementation search,
not a priority audit. Two primary PDFs were opened; only the indicated
parts were inspected, not their complete proofs.

- Van den Berg, Jaquette and Mireles James, *Validated Numerical
  Approximation of Stable Manifolds for Parabolic PDEs*, July 2021 version.
  Its abstract and Sections 2/5 describe validated manifold approximations
  using finite subspaces, an infinite tail, and Lyapunov--Perron contraction;
  Theorem 5.11 packages contraction conditions. This supports investigating
  certified graph computation. It does not by itself supply our exact-value
  query model, derivative sampling law, or work exponent.
  [Primary PDF](https://arxiv.org/pdf/2004.14830).
- Chen, Villa and Ghattas, *Taylor approximation and variance reduction for
  PDE-constrained optimal control under uncertainty*. Sections 3.2--3.4,
  Algorithm 1 and formula (3.23) use state/adjoint actions and Taylor control
  variates with a Monte Carlo correction. Their uncertainty model and
  objective differ from the present worst-input initial-value problem.
  Matrix-free actions are a relevant computational precedent, not a proof
  of uniform coefficient compression or our desired large-T complexity.
  [Primary PDF](https://arxiv.org/pdf/1804.04301).

No worldwide originality, efficient implementation, new Lean result or
experimental success is inferred from this search. The next formal/code
task must follow a proved theory contract; this note authorizes no new
numerical experiment or unbounded coefficient computation.
