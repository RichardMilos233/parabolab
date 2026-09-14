"""Uniform solver interface: one PDE, several methods, one comparison.

    from functools import partial
    import numpy as np
    from parabolab import CodingTreeMC, compare
    from parabolab.library import allen_cahn_nd

    pde  = partial(allen_cahn_nd, d=1, T=0.5)
    grid = np.linspace(-8.0, 8.0, 27)
    mc   = CodingTreeMC(n_samples=10_000, seed=0).solve(pde, grid)
    compare(pde, mc).table().plot("allen_cahn.png")

Every solver is ``Solver(**budget).solve(pde, grid, t=0.0) -> Curve``, so
swapping one method for another is a one-line edit.  Four are available:

===================  ===========================================  ==========
solver               method                                        cost
===================  ===========================================  ==========
``CodingTreeMC``     pointwise E[H] over coding trees              seconds
                     (JEQ2023 Thm. 1 / JCP2024 Alg. 1)
``DeepBranching``    network fitted to tree samples                GPU-minutes
                     (JCP2024 Alg. 2)
``DeepBSDE``         the authors' deep BSDE baseline (vendored)    GPU-minutes
``DeepGalerkin``     the authors' deep Galerkin baseline           GPU-minutes
===================  ===========================================  ==========

Only ``CodingTreeMC`` is cheap: it is a pointwise expectation, so a whole
profile costs well under a second and needs no training.  The other three
train a network; JCP2024 quotes 28-184 GPU-minutes per run for the budgets
that reproduce its tables.

Two contracts worth reading before use:

**The first argument may be a PDE or a zero-argument factory.**  PDE
objects hold lambdified sympy callables and plain Python closures, so they
cannot be pickled; anything that fans work out to worker processes
(``CodingTreeMC(n_jobs>1)``, ``DeepBranching``) therefore needs a factory
such as ``partial(allen_cahn_nd, d=1, T=0.5)``.  Those solvers raise
``TypeError`` with the fix spelled out when handed an instance, before any
expensive import happens.

**The grid convention is pinned here.**  A scalar grid point ``s`` becomes
the state ``(s, x_mid, ..., x_mid)`` -- the paper's profile convention,
matching ``parabolab.deep.solver._grid_inputs`` -- so Monte Carlo points and
network curves land on the SAME states.  Note that
``parabolab.profiles.last_coordinate_embedding`` uses the other convention,
``(0, ..., 0, s)``: identical at d = 1, silently different beyond.

This module imports torch nowhere at load time; the three network solvers
import it inside ``.solve()``, so ``import parabolab`` stays torch-free.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

import numpy as np

from .pde import FullyNonlinearPDEnD
from .proposals import TupleProposal

__all__ = [
    "Curve",
    "Comparison",
    "Solver",
    "CodingTreeMC",
    "DeepBranching",
    "DeepBSDE",
    "DeepGalerkin",
    "compare",
    "exact_on",
    "grid_states",
]

#: A PDE instance, or a zero-argument callable returning one.
PDELike = Union[object, Callable[[], object]]


# --------------------------------------------------------------- resolution

def _resolve(pde: PDELike, *, need_factory: bool, who: str
             ) -> Tuple[object, Optional[Callable[[], object]]]:
    """Return (instance, factory or None), enforcing the factory contract."""
    if callable(pde) and not hasattr(pde, "T"):
        return pde(), pde
    if need_factory:
        raise TypeError(
            f"{who} runs in worker processes and needs a picklable "
            f"zero-argument factory, not a {type(pde).__name__} instance: "
            f"PDE objects hold lambdified sympy callables and plain "
            f"closures, so they cannot be pickled.  Pass the builder "
            f"instead, e.g. functools.partial(allen_cahn_nd, d=1, T=0.5)."
        )
    return pde, None


# ---------------------------------------------------------------- the grid

def grid_states(pde: PDELike, grid: Sequence[float],
                x_mid: Optional[float] = None) -> np.ndarray:
    """Scalar grid -> states ``(s, x_mid, ..., x_mid)``, shape ``(n, d)``.

    ``x_mid`` defaults to the midpoint of the grid.  See the module
    docstring for why this convention rather than the one in
    ``parabolab.profiles.last_coordinate_embedding``.
    """
    pde, _ = _resolve(pde, need_factory=False, who="grid_states")
    grid = np.asarray(grid, dtype=float)
    point = _point_map(pde, grid, x_mid)
    return np.array([point(s) for s in grid])


def _point_map(pde, grid, x_mid: Optional[float] = None):
    """The single source of truth for the grid convention: s -> state."""
    grid = np.asarray(grid, dtype=float)
    d = getattr(pde, "d", 1)
    if x_mid is None:
        x_mid = 0.5 * (float(grid[0]) + float(grid[-1]))

    def point(s: float) -> np.ndarray:
        x = np.full(d, float(x_mid))
        x[0] = float(s)
        return x

    return point


def _embedding(pde, grid, embed=None):
    """``_point_map``, or None for PDEs whose phi wants a plain float.

    ``FullyNonlinearPDEnD`` evaluates phi at an array; ``ParabolicPDE`` and
    ``FullyNonlinearPDE1D`` want a float, and passing the wrong one raises
    a bare TypeError from inside lambdify.  An explicit ``embed`` (e.g.
    ``profiles.last_coordinate_embedding(d)``, the authors' notebook
    convention) overrides the default map.
    """
    if embed is not None:
        return embed
    if not isinstance(pde, FullyNonlinearPDEnD):
        return None
    return _point_map(pde, grid)


def _points(pde, grid, embed=None) -> tuple:
    """The states a solver evaluates: floats for scalar PDEs, arrays else."""
    fn = _embedding(pde, grid, embed)
    grid = np.asarray(grid, dtype=float)
    return tuple(fn(s) if fn is not None else float(s) for s in grid)


def exact_on(pde: PDELike, grid: Sequence[float], t: float = 0.0,
             embed=None) -> Optional[np.ndarray]:
    """``u(t, .)`` on the grid, or None if the PDE carries no closed form."""
    pde, _ = _resolve(pde, need_factory=False, who="exact_on")
    if getattr(pde, "exact_solution", None) is None:
        return None
    return np.array([pde.exact_solution(t, p)
                     for p in _points(pde, grid, embed)])


def _exact_at(pde, curve: "Curve") -> Optional[np.ndarray]:
    """u(curve.t, .) at the states the curve was actually evaluated on."""
    if getattr(pde, "exact_solution", None) is None:
        return None
    points = curve.points
    if points is None:
        return exact_on(pde, curve.grid, curve.t)
    return np.array([pde.exact_solution(curve.t, p) for p in points])


# ------------------------------------------------------------- one answer

@dataclass(frozen=True)
class Curve:
    """One method's answer for ``u(t, .)`` on the grid.

    ``stderr`` is present only for pointwise methods (Monte Carlo); the
    network solvers return a deterministic curve and leave it None.

    ``points`` records the states actually evaluated -- floats for scalar
    PDEs, d-vectors otherwise -- so the exact solution is compared at
    exactly those states rather than at states re-derived from a
    convention that may since have changed (see the module docstring on
    the two grid conventions).  ``t`` lets one figure carry curves at
    different times.
    """

    label: str
    grid: np.ndarray
    values: np.ndarray
    seconds: float
    stderr: Optional[np.ndarray] = None
    note: str = ""
    t: float = 0.0
    points: Optional[tuple] = None
    #: the s -> state map used, so a finer exact curve can reuse it
    embedding: Optional[Callable] = None


# --------------------------------------------------------------- solvers

class Solver:
    """Base class: configure with a budget, apply with ``.solve``."""

    label = "solver"
    #: whether .solve() refuses a bare PDE instance (multiprocessing)
    needs_factory = False

    def solve(self, pde: PDELike, grid: Sequence[float], t: float = 0.0,
              embed=None) -> Curve:  # pragma: no cover - interface
        raise NotImplementedError

    def _resolve(self, pde):
        return _resolve(pde, need_factory=self.needs_factory,
                        who=type(self).__name__)


class CodingTreeMC(Solver):
    """Pointwise coding-tree Monte Carlo (JEQ2023 Thm. 1 / JCP2024 Alg. 1).

    Each grid point is an independent expectation -- no training, no
    time-marching, no coupling between points. Sampling settings can be
    compared through the same Curve interface as the network solvers.

    ``rate`` is the Exp rate of the branching clock; None uses the package
    default (1.0).  ``n_jobs > 1`` fans sample batches out to worker
    processes and requires a factory; the result is independent of
    ``n_jobs`` but differs from the ``n_jobs=1`` serial draw (different
    seeding scheme -- both are valid, neither is more correct).
    ``tuple_proposal`` optionally supplies the tuple probabilities q_c(Z)
    used by the serial sampler; it requires ``n_jobs=1``.  Pass a proposal
    prepared for the same PDE, then compare its Curve with the baseline.
    """

    label = "coding-tree MC"

    def __init__(self, n_samples: int = 10_000, seed: int = 0,
                 rate: Optional[float] = None, n_jobs: int = 1,
                 label: Optional[str] = None, *,
                 tuple_proposal: Optional[TupleProposal] = None):
        if tuple_proposal is not None and n_jobs > 1:
            raise ValueError("tuple_proposal requires n_jobs=1")
        self.n_samples = n_samples
        self.seed = seed
        self.rate = rate
        self.n_jobs = n_jobs
        self.tuple_proposal = tuple_proposal
        if label is not None:
            self.label = label

    @property
    def needs_factory(self) -> bool:
        return self.n_jobs > 1

    def solve(self, pde: PDELike, grid: Sequence[float], t: float = 0.0,
              embed=None) -> Curve:
        from .profiles import estimate_profile

        instance, factory = self._resolve(pde)
        grid = np.asarray(grid, dtype=float)
        res = estimate_profile(
            instance, t, grid, self.n_samples, seed=self.seed,
            rate=self.rate, embed=_embedding(instance, grid, embed),
            pde_factory=factory, n_jobs=self.n_jobs,
            tuple_proposal=self.tuple_proposal,
        )
        return Curve(
            label=self.label,
            grid=res.xs,
            values=res.estimates,
            seconds=res.seconds,
            stderr=res.stderrs,
            note=(f"{self.n_samples} samples/point, "
                  f"tree nodes mean={res.mean_nodes:.2f} max={res.max_nodes}"),
            t=t,
            points=_points(instance, grid, embed),
            embedding=embed,
        )


class DeepBranching(Solver):
    """Network fitted to coding-tree samples (JCP2024 Alg. 2).  Trains.

    Needs a factory: training data is generated in worker processes, which
    rebuild the PDE on their side.
    """

    label = "deep branching"
    needs_factory = True

    def __init__(self, n_states: int = 1000, m_samples: int = 10_000,
                 epochs: int = 3000, seed: int = 0, n_jobs: int = 4,
                 device: str = "cpu", activation: str = "tanh",
                 label: Optional[str] = None):
        self.n_states = n_states
        self.m_samples = m_samples
        self.epochs = epochs
        self.seed = seed
        self.n_jobs = n_jobs
        self.device = device
        self.activation = activation
        if label is not None:
            self.label = label

    def solve(self, pde: PDELike, grid: Sequence[float], t: float = 0.0,
              embed=None) -> Curve:
        instance, factory = self._resolve(pde)
        if embed is not None:
            raise ValueError(
                "DeepBranching evaluates its network on the paper's own grid "
                "(deep/solver.py::_grid_inputs); a custom embed is not "
                "supported."
            )
        import parabolab.deep as deep

        grid = np.asarray(grid, dtype=float)
        x_lo, x_hi = float(grid[0]), float(grid[-1])
        start = time.perf_counter()
        res = deep.run_experiment(
            factory, x_lo=x_lo, x_hi=x_hi, n_states=self.n_states,
            m_samples=self.m_samples, epochs=self.epochs, n_runs=1,
            seed0=self.seed, n_jobs=self.n_jobs, device=self.device,
            activation=self.activation, verbose=False,
        )
        _, _, net_grid, values, _ = deep.grid_errors(
            res.nets[0], instance, t_val=t, x_lo=x_lo, x_hi=x_hi,
            n_grid=len(grid), device=self.device,
        )
        return Curve(
            label=self.label,
            grid=net_grid,
            values=values,
            seconds=time.perf_counter() - start,
            note=(f"N={self.n_states}, M={self.m_samples}, "
                  f"{self.epochs} epochs"),
            t=t,
            points=_points(instance, grid),
            embedding=None,
        )


class DeepBSDE(Solver):
    """The authors' deep BSDE / 2BSDE baseline (vendored).  Trains.

    ``f_expr`` / ``phi_expr`` override the PDE's sympy expressions -- the
    Merton problem needs the authors' regularized forms to avoid NaN, see
    ``examples/jcp_comparison_baselines.py``.
    """

    label = "deep BSDE"

    def __init__(self, epochs: int = 3000, n_states: int = 1000,
                 n_time_intervals: int = 4, seed: int = 0,
                 f_expr=None, phi_expr=None, label: Optional[str] = None,
                 **net_kwargs):
        self.epochs = epochs
        self.n_states = n_states
        self.n_time_intervals = n_time_intervals
        self.seed = seed
        self.f_expr = f_expr
        self.phi_expr = phi_expr
        self.net_kwargs = net_kwargs
        if label is not None:
            self.label = label

    def solve(self, pde: PDELike, grid: Sequence[float], t: float = 0.0,
              embed=None) -> Curve:
        instance, _ = self._resolve(pde)
        import torch

        from .vendor import BSDENet, bsde_functions, eval_bsde_grid

        grid = np.asarray(grid, dtype=float)
        torch.manual_seed(self.seed)
        start = time.perf_counter()
        model = BSDENet(
            x_lo=float(grid[0]), x_hi=float(grid[-1]), epochs=self.epochs,
            bsde_nb_states=self.n_states,
            bsde_nb_time_intervals=self.n_time_intervals,
            **bsde_functions(instance, f_expr=self.f_expr,
                             phi_expr=self.phi_expr),
            **self.net_kwargs,
        )
        model.train_and_eval()
        values = eval_bsde_grid(model, grid_states(instance, grid))
        return Curve(
            label=self.label,
            grid=grid,
            values=values,
            seconds=time.perf_counter() - start,
            note=(f"{self.epochs} epochs, "
                  f"{self.n_time_intervals} time intervals"),
            t=t,
            points=_points(instance, grid, embed),
            embedding=embed,
        )


class DeepGalerkin(Solver):
    """The authors' deep Galerkin baseline (vendored).  Trains.

    JCP2024 Sec. 4 (d) judges DGM inapplicable to the Merton problem: its
    loss divides by the network's second derivative.  That is an editorial
    judgement the adapter does not enforce -- this solver will happily
    build and run there, and the paper's comparison skips it by
    declaration (``examples/jcp_comparison_baselines.py``).
    """

    label = "deep Galerkin"

    def __init__(self, epochs: int = 3000, n_states: int = 1000,
                 seed: int = 0, f_expr=None, phi_expr=None,
                 label: Optional[str] = None, **net_kwargs):
        self.epochs = epochs
        self.n_states = n_states
        self.seed = seed
        self.f_expr = f_expr
        self.phi_expr = phi_expr
        self.net_kwargs = net_kwargs
        if label is not None:
            self.label = label

    def solve(self, pde: PDELike, grid: Sequence[float], t: float = 0.0,
              embed=None) -> Curve:
        instance, _ = self._resolve(pde)
        import torch

        from .vendor import DGMNet, dgm_functions, eval_dgm_grid

        grid = np.asarray(grid, dtype=float)
        torch.manual_seed(self.seed)
        start = time.perf_counter()
        model = DGMNet(
            x_lo=float(grid[0]), x_hi=float(grid[-1]), epochs=self.epochs,
            dgm_nb_states=self.n_states,
            **dgm_functions(instance, f_expr=self.f_expr,
                            phi_expr=self.phi_expr),
            **self.net_kwargs,
        )
        model.train_and_eval()
        tx = np.column_stack([np.full(len(grid), t),
                              grid_states(instance, grid)])
        values = eval_dgm_grid(model, tx)
        return Curve(
            label=self.label,
            grid=grid,
            values=values,
            seconds=time.perf_counter() - start,
            note=f"{self.epochs} epochs",
            t=t,
            points=_points(instance, grid, embed),
            embedding=embed,
        )


# ------------------------------------------------------------- comparison

class Comparison:
    """Table + figure for one PDE solved by one or more methods.

    Each curve carries its own ``t`` and the states it was evaluated on, so
    one figure can mix times and embeddings and every comparison against
    the closed form happens at exactly the right states.
    """

    def __init__(self, pde: PDELike, curves: Sequence[Curve]):
        self.pde, _ = _resolve(pde, need_factory=False, who="compare")
        self.curves = list(curves)

    @property
    def times(self) -> tuple:
        return tuple(sorted({c.t for c in self.curves}))

    def errors(self) -> Dict[str, Dict[str, float]]:
        """``{label: {'l1': ..., 'l2': ...}}``; empty without a closed form."""
        out: Dict[str, Dict[str, float]] = {}
        for c in self.curves:
            exact = _exact_at(self.pde, c)
            if exact is None:
                continue
            err = np.abs(c.values - exact)
            out[c.label] = {"l1": float(err.mean()),
                            "l2": float((err ** 2).mean())}
        return out

    def table(self) -> "Comparison":
        times = ", ".join(f"{t:g}" for t in self.times)
        print(f"\n{self.pde.name}   t = {times}, T = {self.pde.T}")
        for c in self.curves:
            exact = _exact_at(self.pde, c)
            head = f"{c.label} (t={c.t:g})" if len(self.times) > 1 else c.label
            if c.stderr is not None and exact is not None:
                # Pointwise method: |estimate - exact| / stderr is a
                # self-contained check -- every value below 2 means the
                # closed form is reproduced inside the error bars, with no
                # external reference number needed.
                z = np.abs(c.values - exact) / c.stderr
                print(f"\n  {head}  [{c.note}]")
                print(f"  {'x':>10} {'estimate':>13} {'stderr':>10} "
                      f"{'exact':>13} {'|err|/stderr':>13}")
                for i, x in enumerate(c.grid):
                    print(f"  {x:10.3f} {c.values[i]:13.6f} "
                          f"{c.stderr[i]:10.6f} {exact[i]:13.6f} "
                          f"{z[i]:13.2f}")
                print(f"  -> max |err|/stderr = {z.max():.2f} over "
                      f"{len(c.grid)} points, {c.seconds:.1f}s")
            elif exact is not None:
                err = np.abs(c.values - exact)
                print(f"\n  {head}  [{c.note}]  L1 {err.mean():.2e}  "
                      f"L2 {(err ** 2).mean():.2e}  {c.seconds:.1f}s")
            else:
                print(f"\n  {head}  [{c.note}]  {c.seconds:.1f}s "
                      f"(no closed form to compare against)")
        return self

    def plot(self, path, title: Optional[str] = None,
             reference=None, n_fine: int = 300) -> "Comparison":
        """Save the figure.

        ``reference`` overlays third-party values as ``(xs, values, label)``
        -- e.g. the authors' published CSV, the way the JEQ figure scripts
        show that our profile matches theirs.
        """
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(7, 4.5))
        colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

        if self.curves:
            g = self.curves[0].grid
            fine = np.linspace(float(g[0]), float(g[-1]), n_fine)
            embed = self.curves[0].embedding
            for i, t in enumerate(self.times):
                exact = exact_on(self.pde, fine, t, embed)
                if exact is None:
                    break
                lbl = f"exact $u({t:g},\\cdot)$" if len(self.times) > 1 \
                    else "exact"
                ax.plot(fine, exact, "-", lw=1.6,
                        color="k" if len(self.times) == 1 else colors[i],
                        label=lbl, zorder=1)
            phi = exact_on(self.pde, fine, self.pde.T, embed)
            if phi is not None:
                ax.plot(fine, phi, "k--", lw=1.0, alpha=0.5,
                        label=r"terminal $\phi$", zorder=1)

        for c in self.curves:
            lbl = f"{c.label} ($t={c.t:g}$)" if len(self.times) > 1 \
                else c.label
            if c.stderr is not None:
                ax.errorbar(c.grid, c.values, yerr=3 * c.stderr, fmt="o",
                            mfc="none", capsize=3, ms=5, label=lbl, zorder=3)
            else:
                ax.plot(c.grid, c.values, "--", lw=1.8, label=lbl, zorder=2)

        if reference is not None:
            rx, rv, rlabel = reference
            ax.plot(rx, rv, "s", mfc="none", ms=6, color="tab:green",
                    label=rlabel, zorder=2)

        ax.set_xlabel("$x$")
        ax.set_ylabel("$u(t, x)$" if len(self.times) > 1
                      else f"$u({self.times[0]:g}, x)$" if self.times
                      else "$u$")
        ax.set_title(title or self.pde.name)
        ax.legend()
        fig.tight_layout()
        fig.savefig(path, dpi=150)
        plt.close(fig)
        print(f"\nfigure saved to {path}")
        return self


def compare(pde: PDELike, *curves: Curve) -> Comparison:
    """Bundle one PDE's answers: ``compare(pde, mc).table().plot(path)``."""
    return Comparison(pde, curves)
