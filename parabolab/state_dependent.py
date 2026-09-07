"""State-dependent coding-tree mechanism and PDE classes.

Extends the fully nonlinear Feynman-Kac framework (JCP2024 section 2 /
JEQ2023 Definition 2.2) to nonlinearities with explicit spatial coordinates:

    du/dt + (sigma2/2) Lap u + f(x, d^{alpha_1} u, ..., d^{alpha_m} u) = 0,
    u(T, .) = phi,   (t, x) in [0, T] x R^d.

Here f depends on both the spatial vector x = (x0, ..., x_{d-1}) and the
solution jet z = (z0, ..., z_{m-1}).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from .mechanism import Code, CodeTuple, DxN, Id


@dataclass(frozen=True)
class StateFNu(Code):
    """The code (a * d_x^beta d_z^nu f)*.

    Evaluates a * (d_x^beta d_z^nu f)(x, jet(u)(x)) at position x.
    beta is a multi-index of length d (spatial derivatives on f).
    nu is a multi-index of length m (jet derivatives on f).
    """

    a: float
    beta: Tuple[int, ...]  # spatial derivative multi-index (length d)
    nu: Tuple[int, ...]    # jet derivative multi-index (length m)


def _bump(idx: Tuple[int, ...], k: int, step: int = 1) -> Tuple[int, ...]:
    """Increment index tuple at position k by step."""
    return idx[:k] + (idx[k] + step,) + idx[k + 1:]


@dataclass(eq=False)
class StateDependentPDEnD:
    """A fully nonlinear parabolic PDE with explicit spatial dependence f(x, z)."""

    T: float
    d: int
    deriv_map: Tuple[Tuple[int, ...], ...]
    f_expr: object       # sympy Expr in x0..x_{d-1} and z0..z_{m-1}
    phi_expr: object     # sympy Expr in x0..x_{d-1}
    sigma2: float = 1.0
    exact_solution: Optional[Callable] = None
    name: str = ""

    def __post_init__(self) -> None:
        if self.T <= 0:
            raise ValueError("T must be positive")
        if self.d < 1:
            raise ValueError("d must be >= 1")
        self.deriv_map = tuple(tuple(int(a) for a in row) for row in self.deriv_map)
        for row in self.deriv_map:
            if len(row) != self.d:
                raise ValueError("deriv_map rows must have length d")

        self._f_cache: Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], Optional[Callable]] = {}
        self._phi_mu_cache: Dict[Tuple[int, ...], Callable] = {}
        self._phi_jet_fn: Optional[Callable] = None
        self._mechanism = None

    @property
    def m(self) -> int:
        return len(self.deriv_map)

    def f_beta_nu(
        self, beta: Tuple[int, ...], nu: Tuple[int, ...]
    ) -> Optional[Callable[[Sequence[float], Sequence[float]], float]]:
        """Return lambdified d_x^beta d_z^nu f, or None if identically zero.

        Callable signature: (x_vector, z_vector) -> float.
        """
        key = (tuple(beta), tuple(nu))
        if key not in self._f_cache:
            import sympy as sp

            xs = sp.symbols(f"x0:{self.d}")
            zs = sp.symbols(f"z0:{self.m}")

            expr = self.f_expr
            # Differentiate w.r.t x
            for x, order in zip(xs, beta):
                if order:
                    expr = sp.diff(expr, x, order)
                    if expr.is_zero or expr == 0:
                        break
            # Differentiate w.r.t z
            if not (expr.is_zero or expr == 0):
                for z, order in zip(zs, nu):
                    if order:
                        expr = sp.diff(expr, z, order)
                        if expr.is_zero or expr == 0:
                            break

            is_zero = expr.is_zero
            if is_zero is None:
                is_zero = sp.simplify(expr) == 0

            if is_zero:
                self._f_cache[key] = None
            else:
                fn = sp.lambdify((xs, zs), expr, "math")
                # Wrap to ensure float output
                def wrapper(xval, zval, fn=fn):
                    return float(fn(xval, zval))
                self._f_cache[key] = wrapper

        return self._f_cache[key]

    def phi_mu(self, mu: Tuple[int, ...]) -> Callable[[Sequence[float]], float]:
        """Numeric d^mu phi as a function of x_vector."""
        mu = tuple(mu)
        if mu not in self._phi_mu_cache:
            import sympy as sp

            xs = sp.symbols(f"x0:{self.d}")
            expr = self.phi_expr
            for x, order in zip(xs, mu):
                if order:
                    expr = sp.diff(expr, x, order)
            fn = sp.lambdify((xs,), expr, "math")

            def wrapper(xval, fn=fn):
                return float(fn(xval))

            self._phi_mu_cache[mu] = wrapper
        return self._phi_mu_cache[mu]

    def phi_jet(self, xval: Sequence[float]) -> Tuple[float, ...]:
        """Evaluate (D^{alpha_0} phi, ..., D^{alpha_{m-1}} phi) at xval."""
        if self._phi_jet_fn is None:
            callables = [self.phi_mu(alpha) for alpha in self.deriv_map]
            self._phi_jet_fn = lambda xv: tuple(c(xv) for c in callables)
        return self._phi_jet_fn(xval)

    @property
    def mechanism(self) -> StateDependentMechanismND:
        if self._mechanism is None:
            self._mechanism = StateDependentMechanismND(self)
        return self._mechanism


@dataclass(frozen=True)
class _ExpansionTerm:
    coeff: float
    beta: Tuple[int, ...]
    nu: Tuple[int, ...]
    u_factors: Tuple[Tuple[int, ...], ...]  # list of mu multi-indices on u


class StateDependentMechanismND:
    """Branching mechanism for state-dependent PDEs f(x, z)."""

    def __init__(self, pde: StateDependentPDEnD, reduce_zero_tuples: bool = True):
        self.pde = pde
        self.reduce_zero_tuples = reduce_zero_tuples
        self._tuples_cache: dict = {}
        self._dx_expansion_cache: dict = {}

    def _zero_tuple(self) -> Tuple[CodeTuple, ...]:
        zero_b = (0,) * self.pde.d
        zero_nu = (0,) * self.pde.m
        return ((StateFNu(0.0, zero_b, zero_nu),),)

    def _expand_dx(self, mu: Tuple[int, ...]) -> List[_ExpansionTerm]:
        """Expand D_x^mu [f(x, Ju)] into sum of _ExpansionTerm objects by induction."""
        mu = tuple(mu)
        if mu in self._dx_expansion_cache:
            return self._dx_expansion_cache[mu]

        zero_b = (0,) * self.pde.d
        zero_nu = (0,) * self.pde.m
        if not any(mu):
            # Base case: f(x, Ju)
            term = _ExpansionTerm(1.0, zero_b, zero_nu, ())
            self._dx_expansion_cache[mu] = [term]
            return [term]

        # Find first non-zero coordinate to step down
        k = next(i for i, val in enumerate(mu) if val > 0)
        mu_prev = _bump(mu, k, -1)
        prev_terms = self._expand_dx(mu_prev)

        new_terms: List[_ExpansionTerm] = []
        for t in prev_terms:
            # 1. d/dx_k acts on explicit x: beta -> beta + e_k
            new_terms.append(
                _ExpansionTerm(t.coeff, _bump(t.beta, k), t.nu, t.u_factors)
            )
            # 2. d/dx_k acts on z_p: for each p, nu -> nu + e_p with added factor D^{alpha_p + e_k} u
            for p, alpha in enumerate(self.pde.deriv_map):
                new_terms.append(
                    _ExpansionTerm(
                        t.coeff,
                        t.beta,
                        _bump(t.nu, p),
                        t.u_factors + (_bump(alpha, k),),
                    )
                )
            # 3. d/dx_k acts on each u-factor D^{lam} u -> D^{lam + e_k} u
            for idx, lam in enumerate(t.u_factors):
                updated_factors = (
                    t.u_factors[:idx] + (_bump(lam, k),) + t.u_factors[idx + 1 :]
                )
                new_terms.append(
                    _ExpansionTerm(t.coeff, t.beta, t.nu, updated_factors)
                )

        # Simplify by sorting u_factors
        canonical_terms: List[_ExpansionTerm] = []
        for t in new_terms:
            sorted_u = tuple(sorted(t.u_factors))
            canonical_terms.append(
                _ExpansionTerm(t.coeff, t.beta, t.nu, sorted_u)
            )

        self._dx_expansion_cache[mu] = canonical_terms
        return canonical_terms

    def _dx_tuples(self, mu: Tuple[int, ...]) -> Tuple[CodeTuple, ...]:
        terms = self._expand_dx(mu)
        tuples = []
        for t in terms:
            if self.reduce_zero_tuples and self.pde.f_beta_nu(t.beta, t.nu) is None:
                continue
            head = StateFNu(t.coeff, t.beta, t.nu)
            children = (head,) + tuple(DxN(lam) for lam in t.u_factors)
            tuples.append(children)
        return tuple(tuples) if tuples else self._zero_tuple()

    def _fnu_tuples(self, code: StateFNu) -> Tuple[CodeTuple, ...]:
        a, beta, nu = code.a, code.beta, code.nu
        d, m, sigma2 = self.pde.d, self.pde.m, self.pde.sigma2
        tuples = []

        # Term 1: First/Second union via chain rule on D^{alpha_p} f
        for p, alpha in enumerate(self.pde.deriv_map):
            nu_p = _bump(nu, p)
            if self.reduce_zero_tuples and self.pde.f_beta_nu(beta, nu_p) is None:
                continue
            g_child = StateFNu(a, beta, nu_p)
            for t in self._expand_dx(alpha):
                if self.reduce_zero_tuples and self.pde.f_beta_nu(t.beta, t.nu) is None:
                    continue
                f_child = StateFNu(t.coeff, t.beta, t.nu)
                u_children = tuple(DxN(lam) for lam in t.u_factors)
                tuples.append((g_child, f_child) + u_children)

        # Term 2: Direct spatial Laplacian on g: - (sigma2 / 2) * Lap_x g
        half_sig = -a * sigma2 / 2.0
        for k in range(d):
            beta_2k = _bump(beta, k, 2)
            if self.reduce_zero_tuples and self.pde.f_beta_nu(beta_2k, nu) is None:
                continue
            tuples.append((StateFNu(half_sig, beta_2k, nu),))

        # Term 3: Mixed spatial-jet derivatives: - sigma2 * sum_{p, k} d_{x_k z_p} g * D^{alpha_p + e_k} u
        neg_sig = -a * sigma2
        for p, alpha in enumerate(self.pde.deriv_map):
            nu_p = _bump(nu, p)
            for k in range(d):
                beta_k = _bump(beta, k)
                if self.reduce_zero_tuples and self.pde.f_beta_nu(beta_k, nu_p) is None:
                    continue
                g_mix = StateFNu(neg_sig, beta_k, nu_p)
                tuples.append((g_mix, DxN(_bump(alpha, k))))

        # Term 4: Jet Hessian (classical third union): - (sigma2 / 2) * sum_{p, q, k} d_{z_p z_q} g * D^{alpha_p+e_k}u * D^{alpha_q+e_k}u
        for p, alpha_p in enumerate(self.pde.deriv_map):
            nu_p = _bump(nu, p)
            for q, alpha_q in enumerate(self.pde.deriv_map):
                nu_pq = _bump(nu_p, q)
                if self.reduce_zero_tuples and self.pde.f_beta_nu(beta, nu_pq) is None:
                    continue
                for k in range(d):
                    g_hess = StateFNu(half_sig, beta, nu_pq)
                    tuples.append((g_hess, DxN(_bump(alpha_p, k)), DxN(_bump(alpha_q, k))))

        return tuple(tuples) if tuples else self._zero_tuple()

    def tuples(self, code: Code) -> Tuple[CodeTuple, ...]:
        if code not in self._tuples_cache:
            zero_b = (0,) * self.pde.d
            zero_nu = (0,) * self.pde.m
            if isinstance(code, Id):
                raw = ((StateFNu(1.0, zero_b, zero_nu),),)
            elif isinstance(code, DxN):
                raw = self._dx_tuples(code.mu)
            elif isinstance(code, StateFNu):
                raw = self._fnu_tuples(code)
            else:
                raise TypeError(f"Unknown code: {code!r}")

            self._tuples_cache[code] = raw

        return self._tuples_cache[code]

    def terminal(self, code: Code, pde: StateDependentPDEnD, x: Sequence[float]) -> float:
        """Evaluate c(u)(T, x) on terminal condition phi."""
        x_vec = tuple(float(v) for v in x) if hasattr(x, "__len__") else (float(x),)
        if isinstance(code, Id):
            return pde.phi_mu((0,) * pde.d)(x_vec)
        if isinstance(code, DxN):
            return pde.phi_mu(code.mu)(x_vec)
        if isinstance(code, StateFNu):
            fn = pde.f_beta_nu(code.beta, code.nu)
            if fn is None:
                return 0.0
            jet = pde.phi_jet(x_vec)
            return code.a * fn(x_vec, jet)
        raise TypeError(f"Unknown code: {code!r}")

    def is_identically_zero(self, code: Code, pde: StateDependentPDEnD) -> bool:
        if isinstance(code, StateFNu):
            return pde.f_beta_nu(code.beta, code.nu) is None
        return False
