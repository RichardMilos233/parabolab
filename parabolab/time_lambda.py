"""Full-tree second-moment boundaries for flat polynomial semilinear data.

For a raw uniform ``SemilinearMechanism`` with constant terminal value ``a``,
the analytic reduction gives

    P(v) = sum_k f^(k)(a)^2 v^k / k!,
    K = (1/2) integral_0^infinity dv / P(v),
    T_2(lambda) = log(1 + K lambda^2) / lambda.

The integral is floating-point quadrature, not a formal certificate.  The
caller explicitly asserts the globally flat terminal condition through
``flat_terminal``; sampling ``phi`` can only reject obvious mismatches.

Under those assumptions the squared derivative-code moments satisfy

    F_k' = lambda F_k + 2 F_0 F_{k+1} / lambda,
    F_k(0) = f^(k)(a)^2.

Removing the common exponential factor and using the exponential generating
function gives ``v' = 2 exp(lambda t) P(v) / lambda``.  Consequently

    integral_0^v(T) ds/P(s) = 2 expm1(lambda T) / lambda^2.

The explosion endpoint is reached when ``v`` tends to infinity, which yields
the stated ``K`` and ``T_2``.  The root second moment diverges at the same
endpoint because its remaining ``v``-integrand tends to a positive constant.
This is a boundary calculation, not an optimization of ``lambda``.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
from typing import Optional, Sequence, Union

import matplotlib.pyplot as plt
import numpy as np

from .library import BinaryControlMechanism
from .mechanism import SemilinearMechanism
from .pde import FullyNonlinearPDE1D, ParabolicPDE, z_symbols


def _bisect(fn, lo: float, hi: float) -> float:
    flo, fhi = fn(lo), fn(hi)
    if not (flo <= 0.0 <= fhi or fhi <= 0.0 <= flo):
        raise ValueError("root is not bracketed")
    for _ in range(100):
        mid = (lo + hi) / 2.0
        fmid = fn(mid)
        if (flo <= 0.0 <= fmid) or (fmid <= 0.0 <= flo):
            hi, fhi = mid, fmid
        else:
            lo, flo = mid, fmid
    return (lo + hi) / 2.0


_PEAK_X = _bisect(
    lambda x: 2.0 * x * x / (1.0 + x * x) - math.log1p(x * x),
    1.0,
    5.0,
)


def _boundary(lam, K: float):
    rates = np.asarray(lam, dtype=float)
    log_scale = math.log(K) + 2.0 * np.log(rates)
    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        values = np.where(
            log_scale < -36.0,
            K * rates,
            np.logaddexp(0.0, log_scale) / rates,
        )
    return float(values) if values.ndim == 0 else values


def _integral_K(coefficients: Sequence[float], order: int) -> float:
    nodes, weights = np.polynomial.legendre.leggauss(order)
    theta = (nodes + 1.0) * math.pi / 4.0
    v = np.tan(theta)
    jacobian = (math.pi / 4.0) / np.cos(theta) ** 2
    polynomial = np.polynomial.polynomial.polyval(v, coefficients)
    if np.any(~np.isfinite(polynomial)) or np.any(polynomial <= 0.0):
        raise ValueError("P(v) must remain finite and positive at quadrature nodes")
    return 0.5 * float(np.dot(weights, jacobian / polynomial))


@dataclass(frozen=True)
class TimeLambdaSweep:
    """One full-tree second-moment boundary and its reference-time slice."""

    pde: object
    title: str
    flat_terminal: float
    K: float
    quadrature_error: float
    lambdas: np.ndarray
    boundary: np.ndarray
    peak_lambda: float
    peak_T: float
    reference_T: float
    safe_interval: tuple[float, float] | tuple[()]

    @property
    def finite_boundary(self) -> bool:
        return math.isfinite(self.K)

    def table(self) -> "TimeLambdaSweep":
        print(f"\n{self.title}")
        if not self.finite_boundary:
            print("  K = infinity; finite second moment for all T and lambda > 0")
        else:
            interval = (
                "empty" if not self.safe_interval
                else f"({self.safe_interval[0]:.6g}, {self.safe_interval[1]:.6g})"
            )
            print(f"  K={self.K:.12g}  peak lambda={self.peak_lambda:.6g}  "
                  f"peak T={self.peak_T:.6g}  approx. safe at T={self.reference_T:g}: {interval}")
        return self

    def plot(
        self,
        ax: Optional[plt.Axes] = None,
        path: Optional[Union[str, Path]] = None,
        figsize: tuple[float, float] = (7.0, 5.0),
    ) -> "TimeLambdaSweep":
        standalone = ax is None
        if standalone:
            fig, ax = plt.subplots(figsize=figsize)
        if self.finite_boundary:
            y_max = 1.15 * max(self.peak_T, self.reference_T)
            ax.fill_between(self.lambdas, 0.0, self.boundary, color="#D8ECFA",
                            alpha=0.8, label="finite second moment")
            ax.fill_between(self.lambdas, self.boundary, y_max, color="#FCE8E6",
                            alpha=0.65, label="divergent")
            ax.plot(self.lambdas, self.boundary, color="#155EEF", linewidth=2.3,
                    label="boundary (equality diverges)")
            ax.scatter([self.peak_lambda], [self.peak_T], color="#155EEF", s=34, zorder=4)
            ax.annotate(
                rf"peak $({self.peak_lambda:.3g}, {self.peak_T:.3g})$",
                (self.peak_lambda, self.peak_T), xytext=(5, 7),
                textcoords="offset points", fontsize=8,
            )
            ax.axhline(self.reference_T, color="#7A8696", linestyle="--", linewidth=1.2,
                       label=rf"reference $T={self.reference_T:g}$")
            if self.safe_interval:
                lo, hi = self.safe_interval
                ax.plot([lo, hi], [self.reference_T] * 2, color="#12A56A", linewidth=3,
                        label=rf"approx. safe: ${lo:.3g}<\lambda<{hi:.3g}$")
                ax.plot([lo, hi], [self.reference_T] * 2, linestyle="none", marker="o",
                        markerfacecolor="white", markeredgecolor="#087A4D", markeredgewidth=1.8)
            else:
                ax.text(0.5, 0.08, "no safe rate at the reference T",
                        transform=ax.transAxes, ha="center", color="#9E3A32")
            ax.set_ylim(0.0, y_max)
            ax.legend(fontsize=7.5, loc="best")
        else:
            ax.text(0.5, 0.55, "finite second moment\nfor every T and lambda > 0",
                    transform=ax.transAxes, ha="center", va="center", fontsize=12)
        ax.set_title(self.title, fontweight="bold")
        ax.set_xlabel(r"branching rate $\lambda$")
        ax.set_ylabel(r"horizon $T$")
        ax.set_xlim(float(self.lambdas[0]), float(self.lambdas[-1]))
        ax.grid(True, linestyle=":", alpha=0.5)
        if standalone:
            fig.tight_layout()
            if path is not None:
                out = Path(path)
                out.parent.mkdir(parents=True, exist_ok=True)
                fig.savefig(out, dpi=180)
                plt.close(fig)
        return self


class TimeLambdaComparison:
    """A collection of compatible boundary sweeps."""

    def __init__(self, sweeps: Sequence[TimeLambdaSweep]):
        self.sweeps = list(sweeps)

    def table(self) -> "TimeLambdaComparison":
        print("Full-tree second-moment boundary summary")
        print(f"{'case':<30} {'K':>12} {'peak lambda':>12} {'peak T':>12} "
              f"{'reference T':>12} {'approx. safe interval':>25}")
        for sweep in self.sweeps:
            if sweep.finite_boundary:
                safe = ("empty" if not sweep.safe_interval else
                        f"({sweep.safe_interval[0]:.6g}, {sweep.safe_interval[1]:.6g})")
                print(f"{sweep.title:<30} {sweep.K:12.6g} {sweep.peak_lambda:12.6g} "
                      f"{sweep.peak_T:12.6g} {sweep.reference_T:12.6g} {safe:>25}")
            else:
                print(f"{sweep.title:<30} {'infinity':>12} {'--':>12} {'--':>12} "
                      f"{sweep.reference_T:12.6g} {'all lambda > 0':>25}")
        return self

    def plot(
        self,
        path: Optional[Union[str, Path]] = None,
        figsize: Optional[tuple[float, float]] = None,
        save_individual: bool = False,
    ) -> "TimeLambdaComparison":
        n = len(self.sweeps)
        if n == 0:
            raise ValueError("at least one sweep is required")
        ncols = min(3, n)
        nrows = (n + ncols - 1) // ncols
        fig, axes = plt.subplots(nrows, ncols, figsize=figsize or (5.3 * ncols, 4.4 * nrows))
        flat_axes = np.atleast_1d(axes).ravel()
        for ax, sweep in zip(flat_axes, self.sweeps):
            sweep.plot(ax=ax)
        for ax in flat_axes[n:]:
            ax.set_visible(False)
        fig.suptitle("Full-tree second-moment boundary", fontsize=15, fontweight="bold")
        fig.tight_layout(rect=(0, 0, 1, 0.96))
        if path is not None:
            out = Path(path)
            out.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(out, dpi=180)
            plt.close(fig)
            if save_individual:
                for i, sweep in enumerate(self.sweeps, start=1):
                    sweep.plot(path=out.with_name(f"{out.stem}_{i}.png"))
        return self


def sweep_time_lambda(
    pde,
    *,
    flat_terminal: Optional[float] = None,
    title: Optional[str] = None,
    lambda_min: float = 0.01,
    lambda_max: float = 12.0,
    n_points: int = 401,
    reference_T: float = 0.5,
    quadrature_order: int = 128,
    quadrature_tol: float = 1e-10,
) -> TimeLambdaSweep:
    """Compute the exact-form boundary with a numerically evaluated ``K``.

    Supported inputs are explicit polynomial ``ParabolicPDE`` objects using
    the raw uniform semilinear mechanism, plus the library's standard binary
    control mechanism.  Equality with the boundary is excluded from the safe
    interval.
    """
    numbers = (lambda_min, lambda_max, reference_T)
    if not all(math.isfinite(x) and x > 0.0 for x in numbers):
        raise ValueError("lambda bounds and reference_T must be finite and positive")
    if lambda_max <= lambda_min:
        raise ValueError("lambda_max must exceed lambda_min")
    if n_points < 2:
        raise ValueError("n_points must be at least 2")
    if quadrature_order < 16 or quadrature_order % 2:
        raise ValueError("quadrature_order must be an even integer >= 16")
    if not math.isfinite(quadrature_tol) or quadrature_tol <= 0.0:
        raise ValueError("quadrature_tol must be finite and positive")

    mechanism = getattr(pde, "mechanism", None)
    binary = mechanism is BinaryControlMechanism
    if binary:
        import sympy as sp

        z0 = z_symbols(0)[0]
        matches_standard_binary = (
            isinstance(pde, FullyNonlinearPDE1D)
            and pde.n == 0
            and sp.simplify(pde.f_expr - z0**2) == 0
            and sp.simplify(pde.phi_expr - 1) == 0
        )
        if not matches_standard_binary:
            raise ValueError("BinaryControlMechanism must represent f(u)=u^2 with phi=1")
        if flat_terminal is not None and flat_terminal != 1.0:
            raise ValueError("standard binary control requires flat_terminal=1")
        a, K, error = 1.0, 1.0, 0.0
    else:
        if not isinstance(pde, ParabolicPDE):
            raise TypeError("only polynomial semilinear PDEs and standard binary control are supported")
        if callable(pde.f_derivatives):
            raise TypeError("callable non-polynomial f_derivatives are not supported")
        if mechanism not in (None, SemilinearMechanism) or getattr(pde, "_mechanism", None) not in (None, SemilinearMechanism):
            raise ValueError("only the raw uniform SemilinearMechanism is supported")
        if flat_terminal is None or not math.isfinite(flat_terminal):
            raise ValueError("flat_terminal must explicitly declare the constant terminal value")
        a = float(flat_terminal)
        samples = (float(pde.phi(x)) for x in (-1.0, 0.0, 1.0))
        if any(not math.isclose(value, a, rel_tol=1e-10, abs_tol=1e-12) for value in samples):
            raise ValueError("phi samples disagree with the asserted flat_terminal")
        derivatives = [pde.f, *pde.f_derivatives]
        raw = []
        for k, derivative in enumerate(derivatives):
            if not callable(derivative):
                raise ValueError(f"f derivative {k} must be callable")
            value = float(derivative(a))
            if not math.isfinite(value):
                raise ValueError(f"f derivative {k} is not finite at flat_terminal")
            raw.append(value * value / math.factorial(k))
        if len(pde.f_derivatives) >= 2:
            if not pde.phi_derivatives:
                raise ValueError("nonlinear flat-terminal analysis requires phi' to be provided")
            gradient_samples = (float(pde.phi_derivatives[0](x)) for x in (-1.0, 0.0, 1.0))
            if any(not math.isclose(value, 0.0, abs_tol=1e-12) for value in gradient_samples):
                raise ValueError("phi' samples must vanish for the asserted flat terminal condition")
        while raw and raw[-1] == 0.0:
            raw.pop()
        if not raw or raw[0] == 0.0 or len(raw) <= 2:
            K, error = math.inf, 0.0
        else:
            K_half = _integral_K(raw, quadrature_order // 2)
            K = _integral_K(raw, quadrature_order)
            error = abs(K - K_half)
            if error > quadrature_tol * max(1.0, abs(K)):
                raise ValueError(f"K quadrature did not converge: estimated error {error:.3g}")

    lambdas = np.linspace(lambda_min, lambda_max, n_points)
    if math.isfinite(K):
        boundary = _boundary(lambdas, K)
        peak_lambda = _PEAK_X / math.sqrt(K)
        peak_T = _boundary(peak_lambda, K)
        if reference_T >= peak_T:
            safe = ()
        else:
            fn = lambda log_rate: _boundary(math.exp(log_rate), K) - reference_T
            log_tiny = math.log(np.nextafter(0.0, 1.0))
            log_peak = math.log(peak_lambda)
            if fn(log_tiny) >= 0.0:
                raise ValueError("lower safe endpoint is smaller than a representable positive float")
            log_hi = log_peak + math.log(2.0)
            log_max = math.log(np.finfo(float).max)
            while log_hi < log_max and fn(log_hi) > 0.0:
                log_hi += math.log(2.0)
            log_hi = min(log_hi, log_max)
            if fn(log_hi) > 0.0:
                raise ValueError("upper safe endpoint exceeds the finite float range")
            safe = (
                math.exp(_bisect(fn, log_tiny, log_peak)),
                math.exp(_bisect(fn, log_peak, log_hi)),
            )
    else:
        boundary = np.full_like(lambdas, np.nan)
        peak_lambda = peak_T = math.inf
        safe = (0.0, math.inf)

    return TimeLambdaSweep(
        pde=pde, title=title or getattr(pde, "name", type(pde).__name__),
        flat_terminal=a, K=K, quadrature_error=error, lambdas=lambdas,
        boundary=boundary, peak_lambda=peak_lambda, peak_T=peak_T,
        reference_T=reference_T, safe_interval=safe,
    )


def flat_exact_variance(
    leaf_values: Sequence[float],
    flat_terminal: float,
    rate: float,
    horizons: Sequence[float],
    *,
    K: Optional[float] = None,
    step: float = 1e-3,
) -> np.ndarray:
    """Exact ``Var(H)`` of the flat-data estimator (root ``Id``, ``t = 0``) at one rate.

    ``leaf_values = [f(a), f'(a), ...]`` for constant terminal value ``a``.
    With remaining time ``r`` and ``n_K = m_K = 0`` for identically zero codes,

        n_k' = n_0 n_{k+1},                        n_k(0) = f^(k)(a),
        m_k' = rate m_k + 2 m_0 m_{k+1} / rate,    m_k(0) = f^(k)(a)^2,
        E[H]   = a + int_0^T n_0,
        E[H^2] = e^{rate T} (a^2 + int_0^T e^{-rate s} m_0(s) ds / rate).

    Classical RK4 with at most ``step`` per step (numerical integration, not
    a certificate). With ``K`` given, horizons ``T >= T_2(rate)`` return ``inf``.
    """
    leaf = np.asarray(leaf_values, dtype=float)
    Ts = np.asarray(horizons, dtype=float)
    if Ts.ndim != 1 or np.any(np.diff(Ts) <= 0) or Ts[0] <= 0:
        raise ValueError("horizons must be positive and increasing")
    a, lam = float(flat_terminal), float(rate)
    shift = lambda v: np.append(v[1:], 0.0)

    def rhs(r, y):
        n, m = y[:len(leaf)], y[len(leaf):2 * len(leaf)]
        return np.concatenate((n[0] * shift(n), lam * m + 2.0 * m[0] * shift(m) / lam,
                               [n[0], math.exp(-lam * r) * m[0]]))

    y = np.concatenate((leaf, leaf ** 2, [0.0, 0.0]))
    out = np.empty(len(Ts))
    r = 0.0
    with np.errstate(over="ignore", invalid="ignore"):
        for i, T in enumerate(Ts):
            steps = max(1, int(math.ceil((T - r) / step)))
            h = (T - r) / steps
            for _ in range(steps):
                k1 = rhs(r, y)
                k2 = rhs(r + h / 2, y + h / 2 * k1)
                k3 = rhs(r + h / 2, y + h / 2 * k2)
                k4 = rhs(r + h, y + h * k3)
                y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
                r += h
            mean = a + y[-2]
            out[i] = math.exp(lam * T) * (a * a + y[-1] / lam) - mean * mean
    out[~np.isfinite(out)] = np.inf
    if K is not None and math.isfinite(K):
        out[Ts >= _boundary(lam, K)] = np.inf
    return out


def compare_time_lambda(*sweeps: TimeLambdaSweep) -> TimeLambdaComparison:
    return TimeLambdaComparison(sweeps)
