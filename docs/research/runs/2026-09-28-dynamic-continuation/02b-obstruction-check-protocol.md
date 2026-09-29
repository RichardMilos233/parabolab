# Prespecified deterministic obstruction checks

These checks illustrate the conventional constant-profile theory in
04d-sharp-constant-horizon.md. They may begin only after its independent
review and the separate analytic Riccati Lean gate pass. They are not a
Monte Carlo test for divergence, and they must not be described as proving
the infinite-tree correspondence or the exact critical endpoint.

Use Python, mpmath at 80 decimal digits, NumPy and a standard plotting library.
Save the script, machine-readable values, source hashes, environment, command
and timings. Do not modify the 600 frozen dynamic archives.

1. For f=sin and constant r=pi/2, compare the quadrature integral of sech(z)
   from zero to infinity with pi/2. At fixed fractions .1,.5,.9,.99 of pi/2,
   compare integral_0^t sec(s) ds with log(sec(t)+tan(t)); check the derivative
   of the latter by high-precision differentiation. The true signed solution
   is 2 atan(exp(t)); verify its ODE and initial condition separately.
2. For f(y)=1/(1+y^2), r=0, integrate 1-z^2 on [0,1] and compare with 2/3.
   For 0<=t<=2/3 the canonical Id absolute moment is
   z(t)=2 sin(asin(3t/2)/3), while the signed solution is
   u(t)=2 sinh(asinh(3t/2)/3). Check z-z^3/3=t and u+u^3/3=t at
   t=0, .1, .5, .65, 2/3 using high precision. Do not differentiate z at the
   critical endpoint, where its derivative diverges. The moment equals one
   there and is infinite after it by the theorem, not by numerical detection.
3. For truncations Phi_n=sum_(k=0)^n z^(2k), n=1,2,4,8,16,32, compute
   tau_n=integral_0^infinity 1/Phi_n(z) dz independently by quadrature.
   Compare with [pi/(2n+2)] [cot(pi/(2n+2))-cot(3pi/(2n+2))], verify the
   decreasing sequence and its excess above 2/3. This integral identity
   follows from the standard beta/reflection integral and can also be
   checked directly; it is not part of the current Lean theorem.

Acceptance for finite exact-identity residuals is absolute error below 1e-60
at 80 decimal digits. Report failures with raw values and refine precision
only as a labelled diagnostic, not as a silent replacement of this check.

Produce a compact scientific PNG/SVG with exact signed and absolute curves
for both examples, critical times, and a separate truncation-horizon panel.
For t past the theoretical horizon use a labelled region, not a finite
invented y-value. At the rational critical endpoint explicitly show the
finite point (2/3,1). Figure captions must distinguish these deterministic
identities from the primary continuation Monte Carlo experiment.

No performance superiority or novelty will be inferred from these examples.
