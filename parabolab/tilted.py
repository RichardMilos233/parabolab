"""Supersolution-tilted coding trees for scalar semilinear PDEs in any dimension.

This samples the *same* derivative-coded expansion as ``SemilinearMechanism``
(codes Id, (f^(k))*, d/dx_i) under a proposal tilted by a spatially constant
theta-supersolution of the absolute (majorant) system.  Theory:
``docs/research/paper/01-tilted-sampler-theory.md`` (Theorem B, Sec. 5).

In d dimensions the gradient codes D_1..D_d aggregate exactly: with
envelopes l_i >= sup |d_i phi|, every W_{D_i} = (l_i / l_D) W_D with
l_D = (sum_i l_i^2)^(1/2), so the supersolution ODE is the one-dimensional
one with l_D in place of sup |phi'|, and the tuple (D_i, D_i, F_{k+2}) is
chosen with direction i drawn with probability l_i^2 / l_D^2.  Nothing in
the ODE, the output bound or the work bound depends on d beyond l_D.

With remaining time s and envelopes l_c >= sup |terminal value of code c|,
the supersolution solves

    W_c(s) = theta * ( l_c + sum_j |kappa_j| int_0^s prod_i W_{c_ji}(r) dr ).

A node (c, s, y) becomes a leaf with probability l_c / W_c(s), branches into
tuple j with probability |kappa_j| B_cj(s) / W_c(s), and otherwise is killed
(the whole root returns 0).  The returned value H = W_Id(T - t) * S with
S in [-1, 1], so |H| <= W_Id(T - t) on every sample, the estimator is
unbiased for the tree functional, and the expected number of generated
nodes is at most theta_eff / (theta_eff - 1).

The supersolution is tabulated as a step function (right-endpoint values on
a uniform grid).  All sampling probabilities and densities are computed from
that same step function, so unbiasedness does not depend on the accuracy of
the ODE solve; only the certified ``theta_eff`` (the smallest ratio in the
supersolution inequality over the grid) does, and it is checked, not assumed.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Optional, Sequence, Tuple

import numpy as np
from scipy.integrate import solve_ivp

from .solve import Curve, Solver, _points

__all__ = [
    "SemilinearProblem",
    "SupEnvelope",
    "Supersolution",
    "TiltedSamples",
    "TiltedSupersolutionMC",
    "build_supersolution",
    "majorant_horizon",
    "sample_tilted",
]

ID = 0  # code index of Id; F_k is 1 + k; gradient is 2 + m; -1 marks a zero code.


@dataclass(frozen=True)
class SupEnvelope:
    """Declared bounds l_c >= sup_x |c(u)(T, x)| for the terminal data.

    phi:   sup |phi|
    f:     (sup |f(phi)|, sup |f'(phi)|, ..., sup |f^(m)(phi)|); codes F_k with
           k > m are declared identically zero (polynomial f of degree m).
    dphi:  sup |phi'| (d = 1), or a sequence of per-direction bounds
           (sup |d_1 phi|, ..., sup |d_d phi|).

    These are trusted declarations about the whole domain; ``sample_tilted``
    raises if a sampled leaf violates them, but sampling cannot prove them.
    """

    phi: float
    f: Tuple[float, ...]
    dphi: object

    def __post_init__(self):
        dirs = self.dphi_dirs
        vals = (self.phi, *self.f, *dirs)
        if not self.f:
            raise ValueError("f envelope needs at least sup|f(phi)|")
        if not dirs:
            raise ValueError("dphi needs at least one direction")
        if any((not math.isfinite(v)) or v < 0.0 for v in vals):
            raise ValueError("envelopes must be finite and nonnegative")

    @property
    def degree(self) -> int:
        return len(self.f) - 1

    @property
    def dphi_dirs(self) -> Tuple[float, ...]:
        if isinstance(self.dphi, (int, float, np.floating, np.integer)):
            return (float(self.dphi),)
        return tuple(float(v) for v in self.dphi)

    @property
    def dphi_norm(self) -> float:
        """l_D = (sum_i l_i^2)^(1/2), the aggregated gradient envelope."""
        return math.sqrt(sum(v * v for v in self.dphi_dirs))

    @classmethod
    def from_grid(cls, pde, xs: np.ndarray, margin: float = 0.0) -> "SupEnvelope":
        """Envelope from sampled values on ``xs``, inflated by ``1 + margin``.

        Only a numerical declaration: correct when |phi|, |f^(k)(phi)| and
        |phi'| attain their suprema on (or are bounded by the inflated maxima
        over) the supplied points.
        """
        xs = np.asarray(xs, dtype=float)
        phis = np.array([pde.phi(float(x)) for x in xs])
        fs = []
        k = 0
        while True:
            fk = pde.f_derivative(k)
            if fk is None:
                break
            fs.append(max(abs(float(fk(float(p)))) for p in phis))
            k += 1
            if k > 64:
                raise ValueError("f must have finitely many nonzero derivatives")
        dphi = max(abs(float(pde.phi_derivative(1)(float(x)))) for x in xs)
        s = 1.0 + margin
        return cls(float(np.max(np.abs(phis))) * s, tuple(v * s for v in fs), dphi * s)


@dataclass(frozen=True)
class SemilinearProblem:
    """u_t + (1/2) Laplacian u + f(u) = 0 on R^d (or a torus), u(T) = phi.

    fks:  (f, f', ..., f^(m)) as scalar callables (polynomial f of degree m).
    phi:  callable on a length-d array.
    dphi: callable (z, i) -> d_i phi(z).
    """

    T: float
    d: int
    fks: Tuple
    phi: object
    dphi: object
    name: str = ""

    @classmethod
    def from_pde(cls, pde) -> "SemilinearProblem":
        """Adapter for a d = 1 ``ParabolicPDE`` (polynomial f)."""
        fks = []
        k = 0
        while (fk := pde.f_derivative(k)) is not None:
            fks.append(fk)
            k += 1
            if k > 64:
                raise ValueError("f must have finitely many nonzero derivatives")
        phi, dphi = pde.phi, pde.phi_derivative(1)
        return cls(
            T=float(pde.T), d=1, fks=tuple(fks),
            phi=lambda z: phi(float(z[0])),
            dphi=lambda z, i: dphi(float(z[0])),
            name=pde.name,
        )


def _as_problem(obj) -> SemilinearProblem:
    if isinstance(obj, SemilinearProblem):
        return obj
    if getattr(obj, "d", None) == 1 and hasattr(obj, "f_derivative"):
        return SemilinearProblem.from_pde(obj)
    raise TypeError("expected a SemilinearProblem or a d = 1 ParabolicPDE")


def _mechanism(m: int):
    """Tuples (kappa, children) for the codes Id, F_0..F_m, D (aggregated)."""
    D = 2 + m

    def F(k):
        return 1 + k if k <= m else -1

    table = [[(1.0, (F(0),))]]  # Id -> (F_0)
    for k in range(m + 1):
        table.append([(1.0, (F(0), F(k + 1))), (-0.5, (D, D, F(k + 2)))])
    table.append([(1.0, (F(1), D))])  # D -> (F_1, D)
    return table


@dataclass(frozen=True)
class Supersolution:
    """Step-function theta-supersolution on a grid 0 = s_0 < ... < s_M."""

    s: np.ndarray  # (M + 1,) cell endpoints in remaining time
    W: np.ndarray  # (n_codes, M + 1); W[c, i] is the value on (s_{i-1}, s_i]
    ell: np.ndarray  # (n_codes,)
    tuples: tuple  # per code: tuple of (kappa, children, prod(M+1,), G(M+1,))
    theta: float  # design value used in the ODE
    theta_eff: float  # certified min ratio over the grid
    dirs: Tuple[float, ...] = (0.0,)  # per-direction gradient envelopes l_i

    @property
    def horizon(self) -> float:
        return float(self.s[-1])

    def bound(self, s: float) -> float:
        """Output bound W_Id(s) (step value) for remaining time s."""
        return float(self.W[ID, self._cell(s)])

    def _cell(self, s: float) -> int:
        M = self.s.size - 1
        return min(max(int(np.searchsorted(self.s, s, side="left")), 1), M)


def _rhs(table, theta):
    n = len(table)

    def rhs(_s, w):
        out = np.zeros(n)
        for c, tups in enumerate(table):
            acc = 0.0
            for kappa, kids in tups:
                p = abs(kappa)
                for k in kids:
                    p *= 0.0 if k < 0 else w[k]
                acc += p
            out[c] = theta * acc
        return out

    return rhs


def majorant_horizon(env: SupEnvelope, theta: float = 1.0, cap: float = 1e12) -> float:
    """Blow-up time of the theta-majorant ODE (5.1) (math.inf if none by 1e3).

    For theta = 1 this is the guaranteed horizon tau_sup of the sup envelope;
    W^theta is finite exactly below majorant_horizon(env, theta).  Floating
    estimate: the time at which W_Id reaches ``cap`` or the solver stalls.
    """
    table = _mechanism(env.degree)
    ell = np.array([env.phi, *env.f, env.dphi_norm], dtype=float)

    def big(_s, w):
        return np.max(w) - cap

    big.terminal = True
    sol = solve_ivp(
        _rhs(table, theta), (0.0, 1e3), theta * ell, method="DOP853",
        events=big, rtol=1e-12, atol=1e-15,
    )
    if sol.t_events[0].size:
        return float(sol.t_events[0][0])
    return float(sol.t[-1]) if sol.status == -1 else math.inf


def _adaptive_grid(sol, horizon: float, eta: float, max_width: float):
    """Cells on which every positive W_c grows by at most a factor 1 + eta."""
    pts = [0.0]
    s = 0.0
    while s < horizon:
        hi = min(s + max_width, horizon)
        w0 = sol.sol(s)
        pos = w0 > 0.0

        def ok(r):
            return np.all(sol.sol(r)[pos] <= (1.0 + eta) * w0[pos])

        if not ok(hi):
            lo = s
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if ok(mid):
                    lo = mid
                else:
                    hi = mid
            hi = max(lo, s + 1e-15 * max(1.0, horizon))
        s = hi
        pts.append(s)
        if len(pts) > 10_000_000:
            raise ValueError("adaptive grid too fine; the ODE is too close to blow-up")
    return np.array(pts)


def build_supersolution(
    env: SupEnvelope,
    horizon: float,
    theta: float = 1.05,
    steps: int = 2000,
    eta: float = 1e-3,
) -> Supersolution:
    """Solve the theta-majorant ODE on [0, horizon] and certify theta_eff.

    The grid has at most ``horizon / steps`` spacing and at most a factor
    ``1 + eta`` growth of every positive W_c per cell (refined near blow-up).
    Raises ``ValueError`` if the ODE blows up before ``horizon`` (the
    sup-majorant horizon is too short for this theta) or if the tabulated
    step function fails the supersolution inequality with ratio >= 1.
    """
    if not (theta >= 1.0 and math.isfinite(theta)):
        raise ValueError("theta must be finite and >= 1")
    if not (horizon > 0.0 and math.isfinite(horizon)):
        raise ValueError("horizon must be finite and positive")
    table = _mechanism(env.degree)
    ell = np.array([env.phi, *env.f, env.dphi_norm], dtype=float)
    sol = solve_ivp(
        _rhs(table, theta), (0.0, horizon), theta * ell, method="DOP853",
        dense_output=True, rtol=1e-12, atol=1e-15,
    )
    if sol.status != 0 or not np.all(np.isfinite(sol.y)):
        raise ValueError(
            f"theta-majorant ODE did not reach horizon {horizon} "
            f"(theta={theta}); the sup-majorant horizon is too short"
        )
    grid = _adaptive_grid(sol, horizon, eta, horizon / steps)
    W = np.maximum.accumulate(sol.sol(grid), axis=1)  # monotone step values
    widths = np.diff(grid)
    M = grid.size - 1

    tuples = []
    ratios = []
    for c, tups in enumerate(table):
        entries = []
        branch_total = np.zeros(M + 1)
        for kappa, kids in tups:
            prod = np.ones(M + 1)
            for k in kids:
                prod = prod * (0.0 if k < 0 else W[k])
            prod[0] = 0.0  # no mass at s = 0
            G = np.concatenate([[0.0], np.cumsum(widths * prod[1:])])
            entries.append((kappa, kids, prod, G))
            branch_total += abs(kappa) * G
        tuples.append(tuple(entries))
        denom = ell[c] + branch_total[1:]
        mask = denom > 0.0
        if np.any(mask):
            ratios.append(np.min(W[c, 1:][mask] / denom[mask]))
    theta_eff = float(min(ratios)) if ratios else math.inf
    if not theta_eff >= 1.0:
        raise ValueError(
            f"tabulated step function is not a supersolution (ratio {theta_eff}); "
            "increase theta or steps"
        )
    return Supersolution(
        grid, W, ell, tuple(tuples), float(theta), theta_eff, env.dphi_dirs
    )


class _Buffered:
    """Block-buffered uniform / normal draws from a numpy Generator."""

    def __init__(self, rng, block: int = 1 << 16):
        self.rng, self.block = rng, block
        self._u = rng.random(block)
        self._z = rng.standard_normal(block)
        self.iu = self.iz = 0

    def uniform(self) -> float:
        if self.iu == self.block:
            self._u, self.iu = self.rng.random(self.block), 0
        v = self._u[self.iu]
        self.iu += 1
        return v

    def normals(self, d: int) -> np.ndarray:
        if self.iz + d > self.block:
            self._z, self.iz = self.rng.standard_normal(max(self.block, d)), 0
        v = self._z[self.iz : self.iz + d]
        self.iz += d
        return v


class _Killed(Exception):
    pass


@dataclass(frozen=True)
class TiltedSamples:
    values: np.ndarray
    node_counts: np.ndarray
    killed: np.ndarray
    bound: float
    theta_eff: float
    seconds: float

    @property
    def estimate(self) -> float:
        return float(self.values.mean())

    @property
    def stderr(self) -> float:
        n = self.values.size
        return float(self.values.std(ddof=1) / math.sqrt(n)) if n > 1 else float("nan")

    @property
    def mean_nodes(self) -> float:
        return float(self.node_counts.mean())

    @property
    def work_bound(self) -> float:
        te = self.theta_eff
        return te / (te - 1.0) if te > 1.0 else math.inf

    def hoeffding_halfwidth(self, alpha: float = 0.05) -> float:
        """Non-asymptotic (1 - alpha) half-width from |H| <= bound."""
        n = self.values.size
        return self.bound * math.sqrt(2.0 * math.log(2.0 / alpha) / n)


def sample_tilted(
    problem,
    sup: Supersolution,
    t: float,
    x,
    n_samples: int,
    *,
    seed: Optional[int] = None,
    rng=None,
) -> TiltedSamples:
    """Draw ``n_samples`` tilted trees for u(t, x).

    ``problem`` is a ``SemilinearProblem`` or a d = 1 ``ParabolicPDE``;
    ``x`` is a point of R^d (a float is accepted when d = 1).
    """
    if rng is not None and seed is not None:
        raise ValueError("pass either rng or seed, not both")
    if rng is None:
        rng = np.random.default_rng(seed)
    prob = _as_problem(problem)
    d = prob.d
    x = np.atleast_1d(np.asarray(x, dtype=float))
    if x.shape != (d,):
        raise ValueError(f"x must have shape ({d},)")
    if len(sup.dirs) != d:
        raise ValueError("envelope has a different number of gradient directions")
    s_root = float(prob.T) - float(t)
    if not (0.0 < s_root <= sup.horizon * (1 + 1e-12)):
        raise ValueError("remaining time T - t must lie in (0, sup.horizon]")
    m = len(sup.ell) - 3
    D = 2 + m
    if len(prob.fks) < m + 1:
        raise ValueError("problem provides fewer f-derivatives than the envelope")
    fks = prob.fks
    phi, dphi = prob.phi, prob.dphi
    ell, W, sgrid = sup.ell, sup.W, sup.s
    tuples = sup.tuples
    cell = sup._cell
    dirs = np.asarray(sup.dirs, dtype=float)
    lD2 = float(np.sum(dirs**2))
    cum_dirs = np.cumsum(dirs**2) / lD2 if lD2 > 0 else None
    buf = _Buffered(rng)
    tol = 1e-9
    count = [0]

    def leaf_ratio(c, z, direction):
        if c == ID:
            return phi(z) / ell[ID]
        if c == D:
            return dphi(z, direction) / dirs[direction]
        return fks[c - 1](phi(z)) / ell[c]

    def node(c, s, y, direction=-1):
        count[0] += 1
        i = cell(s)
        Wc = W[c, i]
        u = buf.uniform() * Wc
        if u < ell[c]:
            z = y + math.sqrt(s) * buf.normals(d)
            ratio = leaf_ratio(c, z, direction)
            if abs(ratio) > 1.0 + tol:
                raise ValueError(
                    f"envelope violated: code {c} (direction {direction}) at {z}: "
                    f"ratio {ratio}"
                )
            return ratio
        u -= ell[c]
        s_lo = sgrid[i - 1]
        for kappa, kids, prod, G in tuples[c]:
            mass = G[i - 1] + (s - s_lo) * prod[i]
            b = abs(kappa) * mass
            if u < b:
                target = u / abs(kappa)  # uniform on (0, mass)
                if target <= G[i - 1]:
                    k = int(np.searchsorted(G, target, side="left"))
                    k = min(max(k, 1), i - 1)
                    r = sgrid[k - 1] + (target - G[k - 1]) / prod[k]
                else:
                    r = s_lo + (target - G[i - 1]) / prod[i]
                r = min(max(r, 0.0), s)
                z = y + math.sqrt(s - r) * buf.normals(d)
                if D in kids:
                    # D_i -> (F_1, D_i) keeps the direction; F_k -> (D_i, D_i,
                    # F_{k+2}) draws i with probability l_i^2 / l_D^2.
                    if c != D:
                        direction = int(np.searchsorted(cum_dirs, buf.uniform(), side="right"))
                        direction = min(direction, d - 1)
                out = 1.0 if kappa > 0 else -1.0
                for kid in kids:
                    out *= node(kid, r, z, direction if kid == D else -1)
                return out
            u -= b
        raise _Killed

    values = np.empty(n_samples)
    counts = np.empty(n_samples, dtype=np.int64)
    killed = np.zeros(n_samples, dtype=bool)
    bound = sup.bound(s_root)
    start = time.perf_counter()
    for n in range(n_samples):
        count[0] = 0
        try:
            values[n] = bound * node(ID, s_root, x)
        except _Killed:
            values[n] = 0.0
            killed[n] = True
        counts[n] = count[0]
    seconds = time.perf_counter() - start
    return TiltedSamples(values, counts, killed, bound, sup.theta_eff, seconds)


class TiltedSupersolutionMC(Solver):
    """Pointwise bounded-output coding-tree MC via a sup-majorant tilt (d = 1).

    ``envelope`` is a trusted ``SupEnvelope`` declaration for the terminal
    data.  One supersolution table is built for the largest remaining time
    on the call and reused at every grid point.
    """

    label = "tilted coding tree"

    def __init__(
        self,
        envelope: SupEnvelope,
        n_samples: int = 10_000,
        seed: int = 0,
        theta: float = 1.05,
        steps: int = 4000,
        label: Optional[str] = None,
    ):
        self.envelope = envelope
        self.n_samples = int(n_samples)
        self.seed = seed
        self.theta = float(theta)
        self.steps = int(steps)
        if label is not None:
            self.label = label

    def solve(self, pde, grid, t: float = 0.0, embed=None) -> Curve:
        instance, _ = self._resolve(pde)
        if getattr(instance, "d", None) != 1:
            raise NotImplementedError("TiltedSupersolutionMC supports d = 1 only")
        grid = np.asarray(grid, dtype=float)
        points = _points(instance, grid, embed)
        sup = build_supersolution(
            self.envelope, float(instance.T) - float(t), self.theta, self.steps
        )
        values = np.empty(grid.size)
        stderrs = np.empty(grid.size)
        nodes = 0.0
        kills = 0
        start = time.perf_counter()
        for i, point in enumerate(points):
            res = sample_tilted(
                instance, sup, t, point, self.n_samples, seed=self.seed + i
            )
            values[i], stderrs[i] = res.estimate, res.stderr
            nodes += res.node_counts.sum()
            kills += int(res.killed.sum())
        seconds = time.perf_counter() - start
        total = self.n_samples * grid.size
        return Curve(
            label=self.label,
            grid=grid,
            values=values,
            seconds=seconds,
            stderr=stderrs,
            note=(
                f"{self.n_samples} samples/point, theta={self.theta:g} "
                f"(certified {sup.theta_eff:.4f}), |H|<={sup.bound(float(instance.T) - t):.4g}, "
                f"nodes mean={nodes / total:.2f}, killed={kills / total:.3f}"
            ),
            t=t,
            points=points,
            embedding=embed,
        )
