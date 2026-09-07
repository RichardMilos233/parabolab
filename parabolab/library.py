"""Example PDEs from JEQ2023 Section 5 in their d = 1 form.

Semilinear (5.2) Allen-Cahn with closed forms (5.3)/(5.4), and the four
quasilinear / fully nonlinear examples (5.7), (5.8), (5.10), (5.11), each
written in the framework du/dt + (1/2) d^2u/dx^2 + f(jet of u) = 0 --
equations without their own (1/2)-Laplacian carry a -z2/2 term inside f.
All exact solutions are verified symbolically in tests/test_library.py and
tests/test_fully_nonlinear_examples.py.
"""

from __future__ import annotations

import math

from .pde import (
    FullyNonlinearPDE1D,
    FullyNonlinearPDEnD,
    ParabolicPDE,
    x_symbol,
    x_symbols,
    z_symbols,
)


def _allen_cahn_f_derivatives():
    return (
        lambda z: 1.0 - 3.0 * z * z,  # f'
        lambda z: -6.0 * z,           # f''
        lambda z: -6.0,               # f'''
        # derivatives of order >= 4 are identically zero (list convention)
    )


def allen_cahn_wave_1d(T: float = 0.5) -> ParabolicPDE:
    """Allen-Cahn with the tanh traveling-wave solution, JEQ2023 eq. (5.3).

    In d = 1 the closed form is

        u(t, x) = -1/2 - (1/2) tanh( (3/4)(T - t) - x/2 ),

    so the terminal condition is phi(x) = -1/2 - (1/2) tanh(-x/2).
    """

    def exact(t: float, x: float) -> float:
        return -0.5 - 0.5 * math.tanh(0.75 * (T - t) - 0.5 * x)

    def phi(x: float) -> float:
        return -0.5 - 0.5 * math.tanh(-0.5 * x)

    def phi_prime(x: float) -> float:
        th = math.tanh(-0.5 * x)
        return 0.25 * (1.0 - th * th)

    return ParabolicPDE(
        T=T,
        f=lambda z: z - z ** 3,
        f_derivatives=_allen_cahn_f_derivatives(),
        phi=phi,
        phi_derivatives=(phi_prime,),
        exact_solution=exact,
        name=f"allen_cahn_wave_1d(T={T})",
    )


def allen_cahn_flat(phi0: float = 0.5, T: float = 0.5) -> ParabolicPDE:
    """Allen-Cahn with constant terminal data phi == phi0, JEQ2023 eq. (5.4).

    The solution is space independent and solves the ODE u' = -u + u^3
    backwards from u(T) = phi0:

        u(t) = ( 1 - (1 - phi0^{-2}) exp(-2(T - t)) )^{-1/2}.
    """
    if phi0 <= 0.0:
        raise ValueError("phi0 must be positive for the closed form (5.4)")

    def exact(t: float, x: float) -> float:
        return 1.0 / math.sqrt(
            1.0 - (1.0 - phi0 ** -2) * math.exp(-2.0 * (T - t))
        )

    return ParabolicPDE(
        T=T,
        f=lambda z: z - z ** 3,
        f_derivatives=_allen_cahn_f_derivatives(),
        phi=lambda x: phi0,
        phi_derivatives=(lambda x: 0.0,),
        exact_solution=exact,
        name=f"allen_cahn_flat(phi0={phi0}, T={T})",
    )


# --------------------------------------------------------------------------
# Fully nonlinear examples, JEQ2023 Section 5 (d = 1) -- M2
# --------------------------------------------------------------------------

def dym_1d(T: float = 0.01, alpha: float = 2.0) -> FullyNonlinearPDE1D:
    """Dym equation, JEQ2023 eq. (5.7) in d = 1 (Fig. 6):

        du/dt + u^3 d^3u/dx^3 = 0,

    i.e. f(z0,...,z3) = -z2/2 + z0^3 z3 (the -z2/2 cancels the framework's
    Laplacian).  Traveling wave: u(t, x) = (3 alpha (4 alpha^2 (T-t) + x))^{2/3}.
    Paper: T = 0.01, alpha = 2, 1e5 samples, x in [1, 2] (the authors' repo
    uses alpha = -2 with the sign inside, same solution u = (6x + 96(T-t))^{2/3}).

    phi(x) = (3 alpha x)^{2/3} is written as ((3 alpha x)^2)^{1/3}, the even
    real extension, so that stray Brownian excursions to x < 0 (probability
    ~ Phi(-10) at these parameters) do not produce NaNs.
    """
    import sympy as sp

    z = z_symbols(3)
    x = x_symbol()
    f_expr = -z[2] / 2 + z[0] ** 3 * z[3]
    phi_expr = ((3 * alpha * x) ** 2) ** sp.Rational(1, 3)

    def exact(t: float, xv: float) -> float:
        w = 3.0 * alpha * (4.0 * alpha ** 2 * (T - t) + xv)
        return (w * w) ** (1.0 / 3.0)

    return FullyNonlinearPDE1D(
        T=T, n=3, f_expr=f_expr, phi_expr=phi_expr, exact_solution=exact,
        name=f"dym_1d(T={T}, alpha={alpha})",
    )


def quasilinear_tan_1d(T: float = 0.01, alpha: float = 10.0) -> FullyNonlinearPDE1D:
    """Quasilinear non-polynomial example, JEQ2023 eq. (5.8) in d = 1 (Fig. 7):

        du/dt + alpha du/dx + (d^2u/dx^2)/(1 + u^2) - 2u = 0,

    i.e. f = -z2/2 + alpha z1 + z2/(1 + z0^2) - 2 z0.  Solution
    u(t, x) = tan(alpha (T-t) + x).  Paper: T = 0.01, alpha = 10, 1e6
    samples, x in [-pi/4, pi/4].
    """
    import sympy as sp

    z = z_symbols(2)
    x = x_symbol()
    f_expr = -z[2] / 2 + alpha * z[1] + z[2] / (1 + z[0] ** 2) - 2 * z[0]
    phi_expr = sp.tan(x)

    def exact(t: float, xv: float) -> float:
        return math.tan(alpha * (T - t) + xv)

    return FullyNonlinearPDE1D(
        T=T, n=2, f_expr=f_expr, phi_expr=phi_expr, exact_solution=exact,
        name=f"quasilinear_tan_1d(T={T}, alpha={alpha})",
    )


#: Corrected coefficients for the quartic terminal condition of (5.10).
#: JEQ2023 states b = -36/47, c = 24 b, d = 4 b^2 (and the authors'
#: coding_trees notebook uses the same), but those do NOT satisfy the
#: traveling-wave consistency phi - (phi''/12)^2 + cos(pi phi''''/24) = 0:
#: sympy gives residual -143 xi^2/188 - 858 xi/47 + 2939/2209.  Solving the
#: consistency exactly (unique for monic quartic with unit cubic term) gives
COSINE_B, COSINE_C, COSINE_E = 3.0 / 8.0, 1.0 / 16.0, 257.0 / 256.0


def cosine_fourth_order_1d(T: float = 0.04, alpha: float = 10.0) -> FullyNonlinearPDE1D:
    """Fully nonlinear 4th-order example, JEQ2023 eq. (5.10) in d = 1 (Fig. 8):

        du/dt + alpha du/dx + u - (u''/12)^2 + cos(pi u''''/24) = 0,

    i.e. f = -z2/2 + alpha z1 + z0 - (z2/12)^2 + cos(pi z4/24).  Solution
    u(t, x) = phi(alpha (T-t) + x) with phi(x) = x^4 + x^3 + b x^2 + c x + e.

    NOTE: we use the corrected coefficients b = 3/8, c = 1/16, e = 257/256
    (sympy-verified); the coefficients printed in the paper and used in the
    authors' notebook (b = -36/47, c = 24b, e = 4b^2) do not solve (5.10)
    -- see COSINE_B above and CLAUDE.md.  Paper: T = 0.04, alpha = 10,
    1e5 samples, x in [-5, 5].
    """
    import sympy as sp

    z = z_symbols(4)
    x = x_symbol()
    b, c, e = sp.Rational(3, 8), sp.Rational(1, 16), sp.Rational(257, 256)
    f_expr = (
        -z[2] / 2 + alpha * z[1] + z[0]
        - (z[2] / 12) ** 2 + sp.cos(sp.pi * z[4] / 24)
    )
    phi_expr = x ** 4 + x ** 3 + b * x ** 2 + c * x + e

    def exact(t: float, xv: float) -> float:
        xi = alpha * (T - t) + xv
        return xi ** 4 + xi ** 3 + COSINE_B * xi ** 2 + COSINE_C * xi + COSINE_E

    return FullyNonlinearPDE1D(
        T=T, n=4, f_expr=f_expr, phi_expr=phi_expr, exact_solution=exact,
        name=f"cosine_fourth_order_1d(T={T}, alpha={alpha})",
    )


def log_third_order_1d(T: float = 0.02, alpha: float = 5.0) -> FullyNonlinearPDE1D:
    """Fully nonlinear 3rd-order example, JEQ2023 eq. (5.11) in d = 1 (Fig. 9):

        du/dt + alpha du/dx + log((u'')^2 + (u''')^2) = 0,

    i.e. f = -z2/2 + alpha z1 + log(z2^2 + z3^2).  Solution
    u(t, x) = cos(alpha (T-t) + x) (the log term vanishes on it since
    cos^2 + sin^2 = 1).  Paper: T = 0.02, alpha = 5, 1e5 samples,
    x in [-pi, pi].
    """
    import sympy as sp

    z = z_symbols(3)
    x = x_symbol()
    f_expr = -z[2] / 2 + alpha * z[1] + sp.log(z[2] ** 2 + z[3] ** 2)
    phi_expr = sp.cos(x)

    def exact(t: float, xv: float) -> float:
        return math.cos(alpha * (T - t) + xv)

    return FullyNonlinearPDE1D(
        T=T, n=3, f_expr=f_expr, phi_expr=phi_expr, exact_solution=exact,
        name=f"log_third_order_1d(T={T}, alpha={alpha})",
    )


# --------------------------------------------------------------------------
# Multidimensional examples (M3): JEQ2023 Section 5.1
# --------------------------------------------------------------------------

def _grad_rows(d: int):
    """deriv_map rows (e_1, ..., e_d) for first-derivative arguments."""
    return tuple(tuple(1 if j == i else 0 for j in range(d))
                 for i in range(d))


def allen_cahn_nd(d: int, T: float = 0.5) -> FullyNonlinearPDEnD:
    """Allen-Cahn traveling wave in d dimensions, JEQ2023 eqs. (5.2)-(5.3):

        du/dt + (1/2) Lap u + u - u^3 = 0,
        u(t, x) = -1/2 - (1/2) tanh( (3/4)(T-t) - sum_i x_i / (2 sqrt d) ).

    The paper's Fig. 1 uses d = 5 with T = 0.5 and d = 100 with T = 0.3
    (settings from the authors' coding_trees notebook, cells
    allen_cahn_jeeq_dim_{5,100}), profile along x = (0, ..., 0, s),
    s in [-8, 8], 1e5 samples.

    phi is written in the logistic form -1 + 1/(1 + e^{-2 y}),
    y = sum x_i/(2 sqrt d), identical to -1/2 - tanh(-y)/2: sympy's FIRST
    derivative of tanh(100-term Add) takes ~3 minutes (pathological cache
    warm-up), the exp form differentiates in milliseconds.
    """
    import sympy as sp

    z = z_symbols(0)
    xs = x_symbols(d)
    inv = 0.5 / math.sqrt(d)

    def exact(t: float, xv) -> float:
        return -0.5 - 0.5 * math.tanh(
            0.75 * (T - t) - inv * float(sum(xv))
        )

    return FullyNonlinearPDEnD(
        T=T, d=d, deriv_map=((0,) * d,),
        f_expr=z[0] - z[0] ** 3,
        phi_expr=-1 + 1 / (1 + sp.exp(-2 * inv * sum(xs))),
        exact_solution=exact,
        name=f"allen_cahn_nd(d={d}, T={T})",
    )


def allen_cahn_bsde(d: int = 100, T: float = 0.3) -> FullyNonlinearPDEnD:
    """Allen-Cahn benchmark of JEQ2023 Table 2 / deep-BSDE Table 1 [19]:

        du/dt + Lap u + u - u^3 = 0   (FULL Laplacian: sigma2 = 2),
        phi(x) = 1 / (2 + 2 |x|^2 / 5),   d = 100,  T = 0.3,  u(0, 0) = ?

    No closed form; the deep-BSDE reference value at u(0, 0) is 0.052802
    (E-Han-Jentzen 2017), coding trees report 0.052754 +/- 0.000364.
    """
    import sympy as sp

    z = z_symbols(0)
    xs = x_symbols(d)

    return FullyNonlinearPDEnD(
        T=T, d=d, deriv_map=((0,) * d,),
        f_expr=z[0] - z[0] ** 3,
        phi_expr=1 / (2 + sp.Rational(2, 5) * sum(x ** 2 for x in xs)),
        sigma2=2.0,
        name=f"allen_cahn_bsde(d={d}, T={T})",
    )


def exponential_gradient_nd(
    d: int, T: float = 0.05, alpha: float = 10.0
) -> FullyNonlinearPDEnD:
    """Gradient-dependent exponential nonlinearity, JEQ2023 eq. (5.5):

        du/dt + (alpha/d) sum_i du/dx_i + (1/2) Lap u
              + d e^{-u} (1 - 2 e^{-u}) = 0,

    i.e. f = (alpha/d) sum z_i + d e^{-z0} - 2d e^{-2 z0} over the jet
    (u, grad u).  Traveling-wave solution (5.6):

        u(t, x) = log(1 + (alpha (T-t) + sum_i x_i)^2).

    Paper Figs. 4/5: d = 5 and 10, T = 0.05, alpha = 10, 1e5 samples,
    profile along x = (0, ..., 0, s), s in [-4, 4].
    """
    import sympy as sp

    z = z_symbols(d)
    xs = x_symbols(d)
    f_expr = (
        sp.Rational(1, 1) * alpha / d * sum(z[1:])
        + d * sp.exp(-z[0]) - 2 * d * sp.exp(-2 * z[0])
    )

    def exact(t: float, xv) -> float:
        return math.log(1 + (alpha * (T - t) + float(sum(xv))) ** 2)

    return FullyNonlinearPDEnD(
        T=T, d=d, deriv_map=((0,) * d,) + _grad_rows(d),
        f_expr=f_expr,
        phi_expr=sp.log(1 + sum(xs) ** 2),
        exact_solution=exact,
        name=f"exponential_gradient_nd(d={d}, T={T}, alpha={alpha})",
    )


def hjb_nd(d: int = 100, T: float = 1.0) -> FullyNonlinearPDEnD:
    """Hamilton-Jacobi-Bellman equation of JEQ2023 Table 5 / eq. (5.9):

        du/dt + Lap u = |grad u|^2   (FULL Laplacian: sigma2 = 2),
        phi(x) = log((1 + |x|^2) / 2),   d = 100,  T = 1.

    In our framework: f = -sum_q z_q^2 over the gradient jet, sigma2 = 2.
    Exact value at (0, x) via Cole-Hopf (w = e^{-u} solves the heat
    equation): u(t, x) = -log E[exp(-phi(x + sqrt(2(T-t)) Z))]; use
    hjb_exact_u0 for x = 0.  Coding trees report 4.580340 +/- 0.001869,
    deep BSDE 4.5977 +/- 0.0019.
    """
    import sympy as sp

    z = z_symbols(d - 1)  # d args z0..z_{d-1}, one per first derivative
    xs = x_symbols(d)

    return FullyNonlinearPDEnD(
        T=T, d=d, deriv_map=_grad_rows(d),
        f_expr=-sum(zi ** 2 for zi in z),
        phi_expr=sp.log((1 + sum(x ** 2 for x in xs)) / 2),
        sigma2=2.0,
        name=f"hjb_nd(d={d}, T={T})",
    )


def hjb_exact_u0(T: float = 1.0, d: int = 100) -> float:
    """Exact u(0, 0) for hjb_nd via Cole-Hopf + chi-squared quadrature.

    u(0,0) = -log E[ 2 / (1 + 2 T S) ],  S ~ chi^2_d
    (since |sqrt(2T) Z|^2 = 2T S), computed by high-resolution trapezoidal
    integration of the chi^2_d density (log-pdf via lgamma for stability).
    """
    import numpy as np

    hi = d + 12.0 * math.sqrt(2.0 * d)
    s = np.linspace(1e-12, hi, 200_001)
    log_pdf = (
        (d / 2.0 - 1.0) * np.log(s)
        - s / 2.0
        - (d / 2.0) * math.log(2.0)
        - math.lgamma(d / 2.0)
    )
    integrand = np.exp(log_pdf) * 2.0 / (1.0 + 2.0 * T * s)
    return -math.log(float(np.trapezoid(integrand, s)))


def merton_hjb(
    T: float = 0.1,
    mu: float = 0.03,
    sigma: float = 0.1,
    gamma: float = 0.5,
    rho: float = 0.01,
) -> FullyNonlinearPDEnD:
    """Merton-problem HJB equation, JCP2024 eq. (4.6), d = 1:

        du/dt - (mu^2/(2 sigma^2)) (du/dx)^2 / d2u/dx2
              + (gamma/(1-gamma)) (du/dx)^{1-1/gamma} = rho u,

    written in our framework (du/dt + (1/2) d2u/dx2 + f = 0) as

        f(z0, z1, z2) = -z2/2 - (mu^2/(2 sigma^2)) z1^2/z2
                        + (gamma/(1-gamma)) z1^{1-1/gamma} - rho z0

    over the jet (u, du/dx, d2u/dx2).  Note f is NON-polynomial (division
    by z2, fractional power of z1) -- the sympy pipeline handles it, with
    possibly_nonzero falling back to its safe degree analysis.

    Terminal condition phi(x) = x^{1-gamma}/(1-gamma) and exact solution

        u(t, x) = x^{1-gamma} (1 + (a-1) e^{-a(T-t)})^gamma
                  / (a^gamma (1-gamma)),
        a := (2 sigma^2 gamma rho - (1-gamma) mu^2) / (2 sigma^2 gamma^2).

    JCP2024 Table 5 / Figs 6-7: mu=0.03, sigma=0.1, gamma=0.5, rho=0.01,
    T=0.1, x in [100, 200], M = 10,000 tree samples per training point.
    With these values a = -0.07 < 0 (fine).  x must stay positive
    (fractional powers of x in phi); on [100, 200] with T = 0.1 the
    Brownian excursions are ~0.3, so this is never an issue.
    """
    import sympy as sp

    z = z_symbols(2)
    (xsym,) = x_symbols(1)

    a = (2 * sigma**2 * gamma * rho - (1 - gamma) * mu**2) / (
        2 * sigma**2 * gamma**2
    )

    f_expr = (
        -z[2] / 2
        - mu**2 / (2 * sigma**2) * z[1] ** 2 / z[2]
        + gamma / (1 - gamma) * z[1] ** (1 - 1 / gamma)
        - rho * z[0]
    )

    def exact(t: float, xv) -> float:
        # combine numerator and a^gamma BEFORE the gamma-power: with the
        # paper's parameters a < 0 and 1 + (a-1)e^{-a(T-t)} < 0, but their
        # ratio is positive.
        x = float(xv[0]) if hasattr(xv, "__len__") else float(xv)
        base = (1 + (a - 1) * math.exp(-a * (T - t))) / a
        return x ** (1 - gamma) * base**gamma / (1 - gamma)

    return FullyNonlinearPDEnD(
        T=T, d=1, deriv_map=((0,), (1,), (2,)),
        f_expr=f_expr,
        phi_expr=xsym ** (1 - gamma) / (1 - gamma),
        exact_solution=exact,
        name=(f"merton_hjb(T={T}, mu={mu}, sigma={sigma}, "
              f"gamma={gamma}, rho={rho})"),
    )


# ---------------------------------------------------------------------------
# Stochastic-rate Merton extensions (Vasicek)
# ---------------------------------------------------------------------------

def vasicek_no_consumption_exact(
    t: float,
    y: float,
    *,
    T: float = 0.1,
    kappa: float = 1.0,
    theta: float = 0.03,
    eta: float = 0.02,
    lambda_: float = 0.03,
    sigma: float = 0.1,
    gamma: float = 0.5,
    rho: float = 0.01,
) -> float:
    """Exact solution F(t, y) for the reduced Merton problem without consumption.

    When intermediate consumption is omitted, the reduced PDE for F(t, y) is:
        F_t - kappa*y*F_y + (1/2)*F_yy + (a0 + a1*y)*F = 0,   F(T, y) = 1,
    with a0 = (1-gamma)*theta + (1-gamma)*lambda_^2/(2*gamma*sigma^2) - rho
    and a1 = (1-gamma)*eta.

    By the Feynman-Kac formula on the OU process dY_s = -kappa*Y_s ds + dW_s,
    int_t^T Y_s ds is conditionally Gaussian with known mean and variance,
    yielding this exact closed form to machine precision.
    """
    tau = T - t
    if tau <= 0.0:
        return 1.0
    a0 = (1.0 - gamma) * theta + (1.0 - gamma) * (lambda_**2) / (2.0 * gamma * sigma**2) - rho
    a1 = (1.0 - gamma) * eta
    if kappa > 1e-12:
        m_I = float(y) * (1.0 - math.exp(-kappa * tau)) / kappa
        s_I2 = (1.0 / (kappa**2)) * (
            tau - 2.0 * (1.0 - math.exp(-kappa * tau)) / kappa
            + (1.0 - math.exp(-2.0 * kappa * tau)) / (2.0 * kappa)
        )
    else:
        m_I = float(y) * tau
        s_I2 = (tau**3) / 3.0
    exponent = a0 * tau + a1 * m_I + 0.5 * (a1**2) * s_I2
    return math.exp(exponent)


def merton_vasicek_reduced(
    T: float = 0.1,
    kappa: float = 1.0,
    theta: float = 0.03,
    eta: float = 0.02,
    lambda_: float = 0.03,
    sigma: float = 0.1,
    gamma: float = 0.5,
    rho: float = 0.01,
    consumption: bool = True,
):
    """Reduced Merton problem with Vasicek stochastic rate, F(t, y), d = 1.

    Normalized interest rate coordinate y = (r - theta) / eta, dY = -kappa*y*dt + dW.
    CRRA value function scales as V(t, x, y) = x^(1-gamma)/(1-gamma) * F(t, y).
    Terminal condition F(T, y) = 1.
    """
    import sympy as sp
    from .state_dependent import StateDependentPDEnD

    (y,) = sp.symbols("x0:1")
    z = sp.symbols("z0:2")  # z0 = F, z1 = F_y

    a0 = (1.0 - gamma) * theta + (1.0 - gamma) * (lambda_**2) / (2.0 * gamma * sigma**2) - rho
    a1 = (1.0 - gamma) * eta

    f_expr = -kappa * y * z[1] + (a0 + a1 * y) * z[0]
    if consumption:
        f_expr += gamma * (z[0] ** (-(1.0 - gamma) / gamma))

    def exact(t: float, yv) -> float:
        y_val = float(yv[0]) if hasattr(yv, "__len__") else float(yv)
        if consumption:
            return float("nan")
        return vasicek_no_consumption_exact(
            t=t, y=y_val, T=T, kappa=kappa, theta=theta, eta=eta,
            lambda_=lambda_, sigma=sigma, gamma=gamma, rho=rho,
        )

    return StateDependentPDEnD(
        T=T,
        d=1,
        deriv_map=((0,), (1,)),
        f_expr=f_expr,
        phi_expr=sp.Integer(1),
        exact_solution=exact if not consumption else None,
        name=f"merton_vasicek_reduced(T={T}, consumption={consumption})",
    )


def merton_vasicek_2d(
    T: float = 0.1,
    kappa: float = 1.0,
    theta: float = 0.03,
    eta: float = 0.02,
    lambda_: float = 0.03,
    sigma: float = 0.1,
    gamma: float = 0.5,
    rho: float = 0.01,
    consumption: bool = True,
):
    """Full 2D Merton HJB with Vasicek stochastic rate, V(t, x, y), d = 2.

    Coordinates: x0 = wealth x, x1 = normalized rate y = (r - theta) / eta.
    deriv_map rows: u, u_x, u_xx, u_y, u_yy.
    Terminal condition V(T, x, y) = x^(1-gamma)/(1-gamma).
    """
    import sympy as sp
    from .state_dependent import StateDependentPDEnD

    x, y = sp.symbols("x0:2")
    z = sp.symbols("z0:5")  # z0=u, z1=u_x, z2=u_xx, z3=u_y, z4=u_yy

    f_expr = (
        -z[2] / 2
        - kappa * y * z[3]
        + (theta + eta * y) * x * z[1]
        - (lambda_**2 / (2.0 * sigma**2)) * (z[1] ** 2 / z[2])
        - rho * z[0]
    )
    if consumption:
        f_expr += (gamma / (1.0 - gamma)) * (z[1] ** (1.0 - 1.0 / gamma))

    def exact(t: float, xv) -> float:
        if consumption:
            return float("nan")
        x_val = float(xv[0])
        y_val = float(xv[1])
        F_val = vasicek_no_consumption_exact(
            t=t, y=y_val, T=T, kappa=kappa, theta=theta, eta=eta,
            lambda_=lambda_, sigma=sigma, gamma=gamma, rho=rho,
        )
        return (x_val ** (1.0 - gamma)) / (1.0 - gamma) * F_val

    return StateDependentPDEnD(
        T=T,
        d=2,
        deriv_map=((0, 0), (1, 0), (2, 0), (0, 1), (0, 2)),
        f_expr=f_expr,
        phi_expr=(x ** (1.0 - gamma)) / (1.0 - gamma),
        exact_solution=exact if not consumption else None,
        name=f"merton_vasicek_2d(T={T}, consumption={consumption})",
    )


