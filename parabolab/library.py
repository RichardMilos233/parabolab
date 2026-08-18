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

from .pde import FullyNonlinearPDE1D, ParabolicPDE, x_symbol, z_symbols


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
