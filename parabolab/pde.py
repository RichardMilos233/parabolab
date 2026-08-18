"""Problem specification for parabolic terminal-value PDEs.

We consider (JEQ2023 eq. (1.1), semilinear case n = 0 for milestone M1)

    du/dt + (1/2) d^2u/dx^2 + f(u) = 0,   u(T, x) = phi(x),
    (t, x) in [0, T] x R,

whose solution is represented as u(t, x) = E[H(T_{t,x,Id})] over random
coding trees (JEQ2023 Theorem 1 / JCP2024 Algorithm 1).

Note the 1/2 in front of the Laplacian: the driving process is a *standard*
Brownian motion (generator (1/2) d^2/dx^2).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

# Either an explicit list [f', f'', f''', ...] -- derivatives beyond the end
# of the list are declared identically zero (suitable for polynomial f) --
# or a callable k -> (z -> f^{(k)}(z)) for k >= 1 (e.g. f = exp).
FDerivatives = Union[Sequence[Callable[[float], float]],
                     Callable[[int], Callable[[float], float]]]


@dataclass(frozen=True)
class ParabolicPDE:
    """A semilinear parabolic terminal-value problem (d = 1 for now).

    Parameters
    ----------
    T : terminal time.
    f : the nonlinearity f(u).
    f_derivatives : derivatives of f. Either a sequence [f', f'', ...] with
        the convention that derivatives past the end are identically zero
        (exact for polynomial f), or a callable k -> f^{(k)} valid for all
        k >= 1 (for non-polynomial f such as exp).
    phi : terminal condition phi(x).
    phi_derivatives : sequence [phi', phi'', ...]. The semilinear mechanism
        only ever needs phi', higher entries are optional.
    d : spatial dimension (only d = 1 supported in M1).
    exact_solution : optional closed form u(t, x) for validation.
    name : human-readable identifier.
    """

    T: float
    f: Callable[[float], float]
    f_derivatives: FDerivatives
    phi: Callable[[float], float]
    phi_derivatives: Sequence[Callable[[float], float]] = ()
    d: int = 1
    exact_solution: Optional[Callable[[float, float], float]] = None
    name: str = field(default="")

    def __post_init__(self) -> None:
        if self.d != 1:
            raise NotImplementedError("M1 supports d = 1 only")
        if self.T <= 0:
            raise ValueError("T must be positive")

    def f_derivative(self, k: int) -> Optional[Callable[[float], float]]:
        """Return f^{(k)}, or None if it is identically zero.

        k = 0 returns f itself. With a sequence-valued ``f_derivatives``,
        indices beyond the sequence return None (identically-zero
        convention); with a callable, it is invoked as ``f_derivatives(k)``
        and may itself return None.
        """
        if k == 0:
            return self.f
        if callable(self.f_derivatives):
            return self.f_derivatives(k)
        if k - 1 < len(self.f_derivatives):
            return self.f_derivatives[k - 1]
        return None

    def phi_derivative(self, k: int) -> Callable[[float], float]:
        """Return phi^{(k)} (k = 0 returns phi itself)."""
        if k == 0:
            return self.phi
        if k - 1 < len(self.phi_derivatives):
            return self.phi_derivatives[k - 1]
        raise ValueError(
            f"phi derivative of order {k} not provided for PDE {self.name!r}"
        )


# --------------------------------------------------------------------------
# Fully nonlinear problems (M2): symbolic specification via sympy
# --------------------------------------------------------------------------

def z_symbols(n: int):
    """The sympy symbols (z0, ..., zn) used as the arguments of f."""
    import sympy as sp

    return sp.symbols(f"z0:{n + 1}")


def x_symbol():
    """The sympy symbol x used in phi expressions."""
    import sympy as sp

    return sp.Symbol("x")


@dataclass(eq=False)
class FullyNonlinearPDE1D:
    """A fully nonlinear terminal-value problem (JEQ2023 eq. (1.1), d = 1)

        du/dt + (1/2) d^2u/dx^2 + f(u, du/dx, ..., d^n u/dx^n) = 0,
        u(T, .) = phi.

    f and phi are given as sympy expressions (in ``z_symbols(n)`` and
    ``x_symbol()`` respectively) so that the mechanism can take derivatives
    of any order and detect identically-zero derivatives exactly.  All
    derivative callables are lambdified lazily and cached.

    PDEs with no 1/2-Laplacian of their own (e.g. the Dym equation) are
    written in this framework by including -z2/2 in f.
    """

    T: float
    n: int
    f_expr: "object"      # sympy Expr in z0..zn
    phi_expr: "object"    # sympy Expr in x
    exact_solution: Optional[Callable[[float, float], float]] = None
    name: str = ""

    def __post_init__(self) -> None:
        if self.T <= 0:
            raise ValueError("T must be positive")
        if self.n < 0:
            raise ValueError("n must be >= 0")
        self._f_nu_cache: Dict[Tuple[int, ...], Optional[Callable]] = {}
        self._phi_k_cache: Dict[int, Callable] = {}
        self._phi_jet_fn: Optional[Callable] = None
        self._mechanism = None

    # -- derivatives of f ---------------------------------------------------
    def f_nu(self, nu: Tuple[int, ...]) -> Optional[Callable]:
        """Numeric d^nu f (a function of z0..zn), or None if identically 0."""
        nu = tuple(nu)
        if nu not in self._f_nu_cache:
            import sympy as sp

            zs = z_symbols(self.n)
            expr = self.f_expr
            for z, order in zip(zs, nu):
                if order:
                    expr = sp.diff(expr, z, order)
            is_zero = expr.is_zero
            if is_zero is None:
                is_zero = sp.simplify(expr) == 0
            self._f_nu_cache[nu] = (
                None if is_zero else sp.lambdify(zs, expr, "math")
            )
        return self._f_nu_cache[nu]

    # -- derivatives of phi -------------------------------------------------
    def phi_k(self, k: int) -> Callable[[float], float]:
        """Numeric phi^{(k)}."""
        if k not in self._phi_k_cache:
            import sympy as sp

            x = x_symbol()
            self._phi_k_cache[k] = sp.lambdify(
                x, sp.diff(self.phi_expr, x, k), "math"
            )
        return self._phi_k_cache[k]

    def phi_jet(self, xval: float) -> Tuple[float, ...]:
        """(phi(x), phi'(x), ..., phi^{(n)}(x)) in one lambdified call."""
        if self._phi_jet_fn is None:
            import sympy as sp

            x = x_symbol()
            self._phi_jet_fn = sp.lambdify(
                x,
                [sp.diff(self.phi_expr, x, k) for k in range(self.n + 1)],
                "math",
            )
        return self._phi_jet_fn(xval)

    # -- mechanism ----------------------------------------------------------
    @property
    def mechanism(self):
        """The Faa-di-Bruno mechanism bound to this PDE (memoized)."""
        if self._mechanism is None:
            from .mechanism import FullyNonlinearMechanism1D

            self._mechanism = FullyNonlinearMechanism1D(self)
        return self._mechanism


# --------------------------------------------------------------------------
# Fully nonlinear problems in d dimensions (M3): JCP2024 section 2
# --------------------------------------------------------------------------

def x_symbols(d: int):
    """The sympy symbols (x0, ..., x_{d-1}) used in d-dim phi expressions."""
    import sympy as sp

    return sp.symbols(f"x0:{d}")


@dataclass(eq=False)
class FullyNonlinearPDEnD:
    """A fully nonlinear terminal-value problem in d dimensions
    (JCP2024 section 2)

        du/dt + (sigma2/2) Lap u + f(d^{alpha_1} u, ..., d^{alpha_m} u) = 0,
        u(T, .) = phi,   (t, x) in [0, T] x R^d,

    where deriv_map = (alpha_1, ..., alpha_m) lists the spatial-derivative
    multi-indices (each of length d) that appear as arguments of f.  The
    driving Brownian motion has variance sigma2 per unit time (the authors'
    ``nu``); sigma2 = 2 turns the 1/2-Laplacian into a full Laplacian.

    f_expr is a sympy expression in z_symbols(m - 1) (i.e. z0..z_{m-1}, one
    per deriv_map row) and phi_expr a sympy expression in x_symbols(d).

    The d = 1 full-jet case deriv_map = ((0,), (1,), ..., (n,)) reproduces
    FullyNonlinearPDE1D / FullyNonlinearMechanism1D exactly (tested).
    """

    T: float
    d: int
    deriv_map: Tuple[Tuple[int, ...], ...]
    f_expr: "object"      # sympy Expr in z0..z_{m-1}
    phi_expr: "object"    # sympy Expr in x0..x_{d-1}
    sigma2: float = 1.0
    exact_solution: Optional[Callable] = None
    name: str = ""

    # cap on cached lambdified d^mu phi / on mechanism Dx tables; at d = 100
    # the set of distinct multi-indices encountered is open-ended (e.g. HJB
    # spawns order-3 codes d^{e_a+e_b+e_c}), so unbounded caches would leak.
    _PHI_CACHE_MAX = 4096

    def __post_init__(self) -> None:
        if self.T <= 0:
            raise ValueError("T must be positive")
        if self.d < 1:
            raise ValueError("d must be >= 1")
        self.deriv_map = tuple(tuple(int(a) for a in row)
                               for row in self.deriv_map)
        for row in self.deriv_map:
            if len(row) != self.d:
                raise ValueError("deriv_map rows must have length d")
        self._f_nu_cache: Dict[Tuple[int, ...], Optional[Callable]] = {}
        self._phi_mu_cache: Dict[Tuple[int, ...], Callable] = {}
        self._phi_jet_fn: Optional[Callable] = None
        self._mechanism = None
        self._support = _UNSET  # lazily computed polynomial support info

    @property
    def m(self) -> int:
        """Number of arguments of f (= number of deriv_map rows)."""
        return len(self.deriv_map)

    # -- fast monotone nonzero-support predicate ------------------------------
    def _support_info(self):
        """Polynomial structure of f, computed once.

        Returns either ('poly', E) with E an (n_monomials, m) integer array
        of exponent vectors, or ('degrees', degs) with degs[q] the largest
        power of z_q occurring (None = unbounded, e.g. exp/trig directions).
        The induced predicate is exact for polynomials and a safe
        overapproximation otherwise.
        """
        if self._support is _UNSET:
            import numpy as np
            import sympy as sp

            zs = z_symbols(self.m - 1)
            try:
                poly = sp.Poly(self.f_expr, *zs)
                E = np.array(poly.monoms(), dtype=int).reshape(-1, self.m)
                self._support = ("poly", E)
            except sp.PolynomialError:
                degs = []
                for q, z in enumerate(zs):
                    expr, deg = self.f_expr, None
                    for k in range(1, 9):
                        expr = sp.diff(expr, z)
                        if expr.is_zero or sp.simplify(expr) == 0:
                            deg = k - 1
                            break
                    degs.append(deg)
                self._support = ("degrees", tuple(degs))
        return self._support

    def possibly_nonzero(self, nu: Tuple[int, ...]) -> bool:
        """Fast monotone test: False guarantees d^nu f is identically zero."""
        kind, data = self._support_info()
        if kind == "poly":
            import numpy as np

            return bool((data >= np.asarray(nu)).all(axis=1).any())
        return all(deg is None or v <= deg for v, deg in zip(nu, data))

    # -- derivatives of f ------------------------------------------------------
    def f_nu(self, nu: Tuple[int, ...]) -> Optional[Callable]:
        """Numeric d^nu f (function of z0..z_{m-1}), None if identically 0."""
        nu = tuple(nu)
        if nu not in self._f_nu_cache:
            if not self.possibly_nonzero(nu):
                self._f_nu_cache[nu] = None
            else:
                import sympy as sp

                zs = z_symbols(self.m - 1)
                expr = self.f_expr
                for z, order in zip(zs, nu):
                    if order:
                        expr = sp.diff(expr, z, order)
                is_zero = expr.is_zero
                if is_zero is None:
                    is_zero = sp.simplify(expr) == 0
                self._f_nu_cache[nu] = (
                    None if is_zero else sp.lambdify(zs, expr, "math")
                )
        return self._f_nu_cache[nu]

    # -- derivatives of phi ------------------------------------------------------
    def phi_mu(self, mu: Tuple[int, ...]) -> Callable:
        """Numeric d^mu phi as a function of (x0, ..., x_{d-1})."""
        mu = tuple(mu)
        fn = self._phi_mu_cache.get(mu)
        if fn is None:
            import sympy as sp

            xs = x_symbols(self.d)
            expr = self.phi_expr
            for x, order in zip(xs, mu):
                if order:
                    expr = sp.diff(expr, x, order)
            fn = sp.lambdify(xs, expr, "math", cse=True)
            if len(self._phi_mu_cache) >= self._PHI_CACHE_MAX:
                self._phi_mu_cache.pop(next(iter(self._phi_mu_cache)))
            self._phi_mu_cache[mu] = fn
        return fn

    def phi_jet(self, xval) -> Tuple[float, ...]:
        """(d^{alpha_1} phi(x), ..., d^{alpha_m} phi(x)) in one call."""
        if self._phi_jet_fn is None:
            import sympy as sp

            xs = x_symbols(self.d)
            exprs = []
            for row in self.deriv_map:
                expr = self.phi_expr
                for x, order in zip(xs, row):
                    if order:
                        expr = sp.diff(expr, x, order)
                exprs.append(expr)
            self._phi_jet_fn = sp.lambdify(xs, exprs, "math", cse=True)
        return self._phi_jet_fn(*xval)

    # -- mechanism ------------------------------------------------------------
    @property
    def mechanism(self):
        """The d-dimensional Faa-di-Bruno mechanism (memoized)."""
        if self._mechanism is None:
            from .mechanism import FullyNonlinearMechanismND

            self._mechanism = FullyNonlinearMechanismND(self)
        return self._mechanism


class _Unset:
    pass


_UNSET = _Unset()
