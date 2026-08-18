"""The semilinear mechanism must match JEQ2023 eq. (2.7) exactly."""

import pytest

from parabolab import Dx, FDeriv, Id, ParabolicPDE, SemilinearMechanism

MECH = SemilinearMechanism


def make_pde():
    # f(u) = u - u^3 with derivative list ending after f''' (polynomial).
    return ParabolicPDE(
        T=1.0,
        f=lambda z: z - z ** 3,
        f_derivatives=(
            lambda z: 1.0 - 3.0 * z * z,
            lambda z: -6.0 * z,
            lambda z: -6.0,
        ),
        phi=lambda x: 2.0 * x,
        phi_derivatives=(lambda x: 2.0,),
        name="test",
    )


def test_mechanism_of_id():
    # M(Id) = {(f*,)}
    assert MECH.tuples(Id()) == ((FDeriv(1.0, 0),),)


def test_mechanism_of_dx():
    # M(d/dx) = {((f')*, d/dx)}
    assert MECH.tuples(Dx(1)) == ((FDeriv(1.0, 1), Dx(1)),)


def test_mechanism_of_g_star():
    # M(g*) = {(f*, (g')*), (d/dx, d/dx, -1/2 (g'')*)} for g = a f^(k):
    # the derivative bumps k, the -1/2 goes into the coefficient a.
    a, k = -3.0, 2
    tuples = MECH.tuples(FDeriv(a, k))
    assert tuples == (
        (FDeriv(1.0, 0), FDeriv(a, k + 1)),
        (Dx(1), Dx(1), FDeriv(-a / 2.0, k + 2)),
    )


def test_uniform_tuple_probabilities():
    # q_c = 1/|M(c)|: 1 for Id and d/dx, 1/2 for g*.
    assert len(MECH.tuples(Id())) == 1
    assert len(MECH.tuples(Dx(1))) == 1
    assert len(MECH.tuples(FDeriv(1.0, 0))) == 2


def test_higher_dx_not_in_semilinear_mechanism():
    with pytest.raises(NotImplementedError):
        MECH.tuples(Dx(2))


def test_terminal_values():
    pde = make_pde()
    x = 0.25
    u_T = pde.phi(x)  # = 0.5
    assert MECH.terminal(Id(), pde, x) == u_T
    assert MECH.terminal(Dx(1), pde, x) == 2.0
    # (a f^(k))*(u)(T, x) = a * f^(k)(phi(x))
    assert MECH.terminal(FDeriv(1.0, 0), pde, x) == u_T - u_T ** 3
    assert MECH.terminal(FDeriv(2.0, 1), pde, x) == 2.0 * (1.0 - 3.0 * u_T ** 2)
    assert MECH.terminal(FDeriv(-0.5, 3), pde, x) == -0.5 * (-6.0)
    # beyond the derivative list: identically zero
    assert MECH.terminal(FDeriv(1.0, 4), pde, x) == 0.0


def test_zero_code_detection():
    pde = make_pde()
    assert not MECH.is_identically_zero(FDeriv(1.0, 3), pde)
    assert MECH.is_identically_zero(FDeriv(1.0, 4), pde)
    assert MECH.is_identically_zero(FDeriv(-2.0, 7), pde)
    assert not MECH.is_identically_zero(Id(), pde)
    assert not MECH.is_identically_zero(Dx(1), pde)
