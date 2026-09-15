"""Multi-instance training corpora on top of the coding-tree sampler.

An *instance* is one PDE from a parametrised family (its parameters are
its identity) together with the sampler's noisy point estimates at N
states, drawn ``n_draws`` times independently at the SAME states: draw 0
is what a model sees, draw 1 is a Noise2Noise target.  The exact solution
is stored for evaluation only.  The ablation's single-PDE datasets
(deep.datasets) are the one-instance, one-draw special case.
"""

from __future__ import annotations

import dataclasses
import functools
import json
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from .. import library
from ..mechanism import DxN
from .generator import generate_training_data
from .solver import _grid_inputs

DERIV_CODES = {"Dx1": DxN((1,)), "Dx2": DxN((2,))}


@dataclass(frozen=True)
class Family:
    key: str
    param_names: Tuple[str, ...]
    ranges: Tuple[Tuple[float, float], ...]
    x_lo: float
    x_hi: float
    d: int
    factory_name: str
    fixed_kwargs: Tuple[Tuple[str, float], ...]
    deriv_factory_name: Optional[str] = None

    def make_factory(self, params: Sequence[float]) -> functools.partial:
        kwargs = dict(self.fixed_kwargs)
        kwargs.update(zip(self.param_names, (float(p) for p in params)))
        return functools.partial(getattr(library, self.factory_name), **kwargs)


FAMILIES: Dict[str, Family] = {
    "ac1": Family("ac1", ("T", "shift"), ((0.1, 0.5), (-3.0, 3.0)),
                  -8.0, 8.0, 1, "allen_cahn_nd", (("d", 1),)),
    "merton": Family("merton", ("gamma", "mu", "sigma"),
                     ((0.3, 0.8), (0.02, 0.06), (0.08, 0.2)),
                     100.0, 200.0, 1, "merton_hjb",
                     (("T", 0.1), ("rho", 0.01)),
                     "merton_hjb_derivatives"),
}


@dataclass(frozen=True)
class InstanceSpec:
    family: str
    params: Tuple[float, ...]
    n_states: int
    m_samples: int
    seed: int
    n_draws: int = 2
    deriv_codes: Tuple[str, ...] = ()

    def to_json(self) -> str:
        return json.dumps(dataclasses.asdict(self), sort_keys=True)


def sample_instances(family: str, n: int, seed: int, *, n_states: int,
                     m_samples: int, n_draws: int = 2) -> List[InstanceSpec]:
    fam = FAMILIES[family]
    rng = np.random.default_rng(seed)
    specs = []
    for i in range(n):
        params = tuple(float(rng.uniform(lo, hi)) for lo, hi in fam.ranges)
        specs.append(InstanceSpec(family, params, n_states, m_samples,
                                  1_000_000 * seed + i, n_draws))
    return specs


@dataclass
class Instance:
    spec: InstanceSpec
    t: np.ndarray          # (N,)
    x: np.ndarray          # (N, d)
    y: np.ndarray          # (n_draws, N)
    stderr: np.ndarray     # (n_draws, N)
    u_exact: np.ndarray    # (N,)
    grid: np.ndarray       # (101,)
    u_grid: np.ndarray     # (101,)
    rate: float
    deriv: Optional[np.ndarray] = None          # (n_codes, N)
    deriv_stderr: Optional[np.ndarray] = None
    deriv_exact: Optional[np.ndarray] = None

    @property
    def finite(self) -> np.ndarray:
        ok = np.isfinite(self.y).all(axis=0) & np.isfinite(self.stderr).all(axis=0)
        if self.deriv is not None:
            ok &= np.isfinite(self.deriv).all(axis=0) & np.isfinite(self.deriv_stderr).all(axis=0)
        return ok


def _draw_states(spec: InstanceSpec, fam: Family):
    rng = np.random.default_rng(spec.seed)
    margin = 0.1 * (fam.x_hi - fam.x_lo)
    xs = np.full((spec.n_states, fam.d), 0.5 * (fam.x_lo + fam.x_hi))
    xs[:, 0] = rng.uniform(fam.x_lo - margin, fam.x_hi + margin,
                           size=spec.n_states)
    return np.zeros(spec.n_states), xs


def generate_instance(spec: InstanceSpec, *,
                      executor: Optional[ProcessPoolExecutor] = None,
                      n_jobs: int = 1) -> Instance:
    fam = FAMILIES[spec.family]
    factory = fam.make_factory(spec.params)
    pde = factory()
    ts, xs = _draw_states(spec, fam)
    ys, ses, rate = [], [], None
    for draw in range(spec.n_draws):
        data = generate_training_data(
            factory, n_states=spec.n_states, m_samples=spec.m_samples,
            seed=1000 * spec.seed + draw, x_lo=fam.x_lo, x_hi=fam.x_hi,
            states=(ts, xs), executor=executor, n_jobs=n_jobs)
        ys.append(data.y)
        ses.append(data.stderr)
        rate = data.rate
    u_exact = np.array([pde.exact_solution(0.0, xs[i])
                        for i in range(spec.n_states)])
    grid, xg, _ = _grid_inputs(fam.d, 0.0, fam.x_lo, fam.x_hi)
    u_grid = np.array([pde.exact_solution(0.0, xg[i]) for i in range(len(grid))])

    deriv = deriv_se = deriv_exact = None
    if spec.deriv_codes:
        if fam.deriv_factory_name is None:
            raise ValueError(f"family {fam.key!r} has no exact derivatives")
        kwargs = dict(fam.fixed_kwargs); kwargs.update(zip(fam.param_names, spec.params))
        dfuns = getattr(library, fam.deriv_factory_name)(**kwargs)
        dvals, dses, dex = [], [], []
        for k, name in enumerate(spec.deriv_codes):
            data = generate_training_data(
                factory, n_states=spec.n_states, m_samples=spec.m_samples,
                seed=1000 * spec.seed + 100 + k, x_lo=fam.x_lo, x_hi=fam.x_hi,
                states=(ts, xs), code=DERIV_CODES[name], executor=executor,
                n_jobs=n_jobs)
            dvals.append(data.y); dses.append(data.stderr)
            fn = dfuns[("Dx1", "Dx2").index(name)]
            dex.append(np.array([fn(0.0, xs[i]) for i in range(spec.n_states)]))
        deriv, deriv_se, deriv_exact = np.array(dvals), np.array(dses), np.array(dex)

    return Instance(spec, ts, xs, np.array(ys), np.array(ses), u_exact,
                    grid, u_grid, float(rate), deriv, deriv_se, deriv_exact)


def instance_path(spec: InstanceSpec, root) -> Path:
    return Path(root) / spec.family / f"{spec.seed}.npz"


def _save_instance(inst: Instance, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    extra = {}
    if inst.deriv is not None:
        extra["deriv"] = inst.deriv
        extra["deriv_stderr"] = inst.deriv_stderr
        extra["deriv_exact"] = inst.deriv_exact
    np.savez(path, spec=inst.spec.to_json(), t=inst.t, x=inst.x, y=inst.y,
             stderr=inst.stderr, u_exact=inst.u_exact, grid=inst.grid,
             u_grid=inst.u_grid, rate=inst.rate, **extra)


def _load_instance(spec: InstanceSpec, path: Path) -> Optional[Instance]:
    """Return the cached instance, None if unreadable, raise on spec mismatch."""
    try:
        with np.load(path, allow_pickle=False) as f:
            stored = str(f["spec"])
            # files written before deriv_codes existed lack the key: they
            # are derivative-less instances, i.e. deriv_codes == ().
            stored_dict = json.loads(stored)
            stored_dict.setdefault("deriv_codes", [])
            if json.dumps(stored_dict, sort_keys=True) != spec.to_json():
                raise ValueError(f"{path} holds spec {stored}, requested "
                                 f"{spec.to_json()}")
            return Instance(spec, f["t"], f["x"], f["y"], f["stderr"],
                            f["u_exact"], f["grid"], f["u_grid"],
                            float(f["rate"]),
                            f["deriv"] if "deriv" in f else None,
                            f["deriv_stderr"] if "deriv_stderr" in f else None,
                            f["deriv_exact"] if "deriv_exact" in f else None)
    except ValueError as exc:
        if "spec" in str(exc):
            raise
        print(f"{path} unreadable ({exc}); regenerating", flush=True)
    except (OSError, KeyError) as exc:
        print(f"{path} unreadable ({exc}); regenerating", flush=True)
    return None


def load_or_generate_corpus(specs: Sequence[InstanceSpec], root, *,
                            n_jobs: int = 1, verbose: bool = False,
                            min_finite: int = 50) -> List[Instance]:
    executor = ProcessPoolExecutor(max_workers=n_jobs) if n_jobs > 1 else None
    out = []
    try:
        for k, spec in enumerate(specs):
            path = instance_path(spec, root)
            inst = _load_instance(spec, path) if path.exists() else None
            if inst is None:
                if verbose:
                    print(f"[{k + 1}/{len(specs)}] generating {path}", flush=True)
                inst = generate_instance(spec, executor=executor, n_jobs=n_jobs)
                _save_instance(inst, path)
            n_ok = int(inst.finite.sum())
            if n_ok < min_finite:
                print(f"skipping {path}: only {n_ok} finite rows "
                      f"(< {min_finite})", flush=True)
                continue
            out.append(inst)
    finally:
        if executor is not None:
            executor.shutdown()
    return out


def collate(instances: Sequence[Instance], *, n_context: int, n_query: int,
            rng: np.random.Generator) -> Dict[str, np.ndarray]:
    """Random context/query subsets of each instance's finite rows.

    Context = draw-0 rows; query targets = draw-1 rows (Noise2Noise) and the
    exact solution.  Rows are sampled with replacement when an instance has
    fewer finite rows than requested.
    """
    B = len(instances)
    d = instances[0].x.shape[1]
    P = len(instances[0].spec.params)
    ctx_tx = np.empty((B, n_context, d + 1)); ctx_y = np.empty((B, n_context))
    ctx_se = np.empty((B, n_context)); params = np.empty((B, P))
    q_tx = np.empty((B, n_query, d + 1)); q_y = np.empty((B, n_query))
    q_u = np.empty((B, n_query))
    for b, inst in enumerate(instances):
        ok = np.flatnonzero(inst.finite)
        ci = rng.choice(ok, size=n_context, replace=len(ok) < n_context)
        qi = rng.choice(ok, size=n_query, replace=len(ok) < n_query)
        tx = np.column_stack([inst.t, inst.x])
        ctx_tx[b] = tx[ci]; ctx_y[b] = inst.y[0, ci]; ctx_se[b] = inst.stderr[0, ci]
        params[b] = inst.spec.params
        q_tx[b] = tx[qi]; q_y[b] = inst.y[min(1, inst.y.shape[0] - 1), qi]
        q_u[b] = inst.u_exact[qi]
    return {"ctx_tx": ctx_tx, "ctx_y": ctx_y, "ctx_se": ctx_se,
            "params": params, "q_tx": q_tx, "q_y": q_y, "q_u": q_u}
