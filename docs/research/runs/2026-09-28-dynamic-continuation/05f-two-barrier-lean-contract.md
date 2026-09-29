# Fixed analytic Lean target for the two-barrier extension

Status: mathematical contract, not a completed formalization. Dispatch only
after T30 freezes its conventional audit of04l and the abstract lemma below.
Keep the user's theory -> Lean -> code order. This gate must not be replaced
by a theorem that assumes the desired width integral is already finite.

## Primary target: integrability of a monotone flow difference

For a real function l continuous on [0,infinity), monotone there, with
l(t)<=b on that domain and limit b at infinity, let Delta>=0 and
h(t)=l(t+Delta)-l(t). Prove with Lebesgue measure that

    IntegrableOn h (Ici 0),
    integral_(Ici 0) h = integral_0^Delta (b-l(t))dt.

Also establish the finite-T identity and remainder bounds used in the proof:

    integral_0^T h
      =J-integral_T^(T+Delta)(b-l(t))dt,
    J=integral_0^Delta(b-l(t))dt,
    0<=integral_T^(T+Delta)(b-l(t))dt<=Delta*(b-l(T)),

for every T>=0. A global continuous, globally monotone l is an acceptable
statement specialization if explicitly documented: the scalar flow on
[0,infinity) has a continuous monotone extension constant at l(0) to the
negative axis. Bounds only for t>=0 suffice; do not assume integrability of
b-l on the half line, which fails for the motivating multiple-root example.

Proof plan: finite interval translation and splitting give the identity;
monotonicity gives h>=0 and the remainder squeeze. Nonnegative truncated
integrals bounded by J imply half-line integrability, and monotone convergence
identifies its integral as J. Treat Delta=0 without a division shortcut.
The abstract proof does not need a derivative of l or an ODE theorem.

The conventional correspondence is l=ell_m, Delta=int_m^M 1/f and
a(t)=ell_M(t)=l(t+Delta). Those scalar ODE facts, Bernstein voting, the random
tree law and the PDE mean identity remain outside this analytic module unless
they are separately and explicitly formalized.

## Secondary target if the primary is complete

For real positive endpoints A<=B, a positive mean mu in [A,B], and second
moment s2 satisfying s2<=(A+B)*mu-A*B, prove

    s2-mu^2 <= ((B-A)^2/(4*A*B))*mu^2.

This is a finite algebraic positive-range relative-variance bridge. It does
not alone show that mu and s2 are integrals or derive sample-average RMS.
At A=B the conclusion has zero RHS. State all denominator assumptions.
Optional exact rational check for A=1,B=27/7 gives100/189.

## Artifact and verification contract

Own a new formal/EstimatorIntegrity/MovingBarrierWidth.lean, a scoped06f
report, and lean/moving-barrier-width/ logs in this run. Do not edit existing
modules, the entrypoint, package configuration, or protected source files.
Read the Lean proof/elan skills as needed; use the pinned toolchain already
available through lake in formal/. Build the new target freshly and capture
the actual exit status. Print axioms for every exported declaration. No sorry,
admit, custom axiom, or undocumented assumption change. Keep failed proof
attempts in the log and report precisely if the full analytic target remains
unfinished; a passing algebraic fragment does not pass this gate.
