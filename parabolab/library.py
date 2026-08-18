"""Example PDEs from JEQ2023 Section 5.1 (Allen-Cahn / Ginzburg-Landau).

Both examples solve (JEQ2023 eq. (5.2), here in d = 1)

    du/dt + (1/2) d^2u/dx^2 + u - u^3 = 0,   u(T, .) = phi,

with f(u) = u - u^3 (so f' = 1 - 3u^2, f'' = -6u, f''' = -6, f^(k>=4) = 0).
"""

from __future__ import annotations

import math

from .pde import ParabolicPDE


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
