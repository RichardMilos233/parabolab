"""Multiprocessing driver for pointwise MC estimation.

The recursive pure-Python sampler (tree.py / mc.py) remains the reference
implementation; this module only fans SAMPLE BATCHES out to worker
processes and recombines the exact sums, so

    estimate_parallel(factory, ..., n_jobs=1) == estimate_parallel(..., n_jobs=8)

bit-for-bit (chunking and per-chunk seeds do not depend on n_jobs; tested).

PDE objects hold lambdified sympy callables and are not picklable, so the
caller passes a zero-argument *factory* (e.g. ``library.hjb_nd`` or a
functools.partial) and every worker builds its own PDE instance -- table
and lambdify caches are per-process.
"""

from __future__ import annotations

import math
from concurrent.futures import ProcessPoolExecutor
from typing import Callable, Optional

import numpy as np

from .mc import MCResult
from .tree import default_rate, sample_tree


def _chunk_sums(args):
    factory, t, x, n, seed, rate, code, prune_zero = args
    pde = factory()
    rng = np.random.default_rng(seed)
    if rate is None:
        rate = default_rate(pde.T)
    kwargs = {} if code is None else {"code": code}
    s = s2 = 0.0
    nodes = 0
    max_nodes = 0
    for _ in range(n):
        smp = sample_tree(pde, t, x, rng=rng, rate=rate,
                          prune_zero=prune_zero, **kwargs)
        s += smp.value
        s2 += smp.value * smp.value
        nodes += smp.n_nodes
        max_nodes = max(max_nodes, smp.n_nodes)
    return n, s, s2, nodes, max_nodes


def estimate_parallel(
    pde_factory: Callable[[], object],
    t: float,
    x,
    n_samples: int,
    *,
    seed: int = 0,
    rate: Optional[float] = None,
    n_jobs: int = 4,
    n_chunks: int = 32,
    code=None,
    prune_zero: bool = True,
) -> MCResult:
    """Estimate u(t, x) = E[H] with n_samples trees over n_jobs processes.

    Chunk seeds are spawned deterministically from ``seed`` via
    numpy SeedSequence; the result is independent of n_jobs.
    """
    import time

    n_chunks = max(1, min(n_chunks, n_samples))
    sizes = [n_samples // n_chunks] * n_chunks
    for i in range(n_samples % n_chunks):
        sizes[i] += 1
    seeds = np.random.SeedSequence(seed).spawn(n_chunks)
    jobs = [
        (pde_factory, t, x, n, s, rate, code, prune_zero)
        for n, s in zip(sizes, seeds)
    ]

    start = time.perf_counter()
    if n_jobs == 1:
        results = [_chunk_sums(j) for j in jobs]
    else:
        with ProcessPoolExecutor(max_workers=n_jobs) as ex:
            results = list(ex.map(_chunk_sums, jobs))
    seconds = time.perf_counter() - start

    n = sum(r[0] for r in results)
    s = sum(r[1] for r in results)
    s2 = sum(r[2] for r in results)
    nodes = sum(r[3] for r in results)
    max_nodes = max(r[4] for r in results)
    mean = s / n
    var = (s2 - n * mean * mean) / (n - 1)
    if rate is None:
        rate = default_rate(pde_factory().T)
    return MCResult(
        estimate=mean,
        stderr=math.sqrt(max(var, 0.0) / n),
        n_samples=n,
        rate=rate,
        mean_nodes=nodes / n,
        max_nodes=max_nodes,
        seconds=seconds,
    )
