"""Independent falsification checks; exact finite algebra and floating tree kernels.
Not a numerical proof of a stochastic theorem. Run from repository root.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time
import numpy as np
from scipy.special import logsumexp

start = time.perf_counter()
out = Path(__file__).resolve().parent
accepted = 0
min_margin = None
for a in map(F, range(9)):
    for b in map(F, range(9)):
        for k in range(10, 20):
            p = F(k, 20)
            if p * (a + b) > a:
                continue
            for da in (F(0), F(1, 7), F(4)):
                for scale in (F(0), F(1, 3), F(1)):
                    A, B = a + da, scale * b
                    margin = 2*(A+B) - A/p - B/(1-p)
                    assert margin >= 0
                    accepted += 1
                    min_margin = margin if min_margin is None else min(min_margin, margin)

# A finite sum of whole-tree likelihood kernels, with independent nonnegative weights.
# This is a topology-kernel stress test, not samples from the production estimator.
rng = np.random.default_rng(20260916)
counts = rng.integers(0, 8, size=(100, 3, 2))
N = counts.sum(axis=(1, 2)) + rng.integers(0, 8, size=100)
L = 0.2*(1 + 2*N*rng.random(100))
logw = rng.normal(0, 3, 100)

def log_objective(theta):
    lam, *p = theta
    probs = np.asarray(p)
    kernels = lam*L - N*np.log(lam) - (
        counts[:,:,0]*np.log(probs) + counts[:,:,1]*np.log1p(-probs)
    ).sum(axis=1)
    return logsumexp(logw + kernels)

max_convex_residual = -np.inf
minimum_hessian_eigenvalue = np.inf
for _ in range(1000):
    left = np.r_[rng.uniform(.1, 3), rng.uniform(.03, .97, 3)]
    right = np.r_[rng.uniform(.1, 3), rng.uniform(.03, .97, 3)]
    t = rng.uniform()
    theta = (1-t)*left+t*right
    residual = log_objective(theta) - ((1-t)*log_objective(left)+t*log_objective(right))
    max_convex_residual = max(max_convex_residual, residual)
    assert residual < 1e-10
    lam, *p = theta
    p = np.asarray(p)
    j = int(rng.integers(len(N)))
    score = np.r_[L[j]-N[j]/lam, -counts[j,:,0]/p+counts[j,:,1]/(1-p)]
    diagonal = np.r_[N[j]/lam**2, counts[j,:,0]/p**2+counts[j,:,1]/(1-p)**2]
    eig = np.linalg.eigvalsh(np.outer(score, score)+np.diag(diagonal))[0]
    minimum_hessian_eigenvalue = min(minimum_hessian_eigenvalue, eig)
    assert eig >= -1e-9

# Exact counterexample: support alone / proxy greedification is insufficient.
p = F(10, 11)
proxy_counterexample = 1/p+1/(1-p)
assert proxy_counterexample == F(121, 10) and proxy_counterexample > 4
result = {
    'exact_binary_gate_cases': accepted,
    'minimum_exact_margin': str(min_margin),
    'finite_kernel_convexity_trials': 1000,
    'maximum_logconvexity_residual': float(max_convex_residual),
    'minimum_kernel_scaled_hessian_eigenvalue': float(minimum_hessian_eigenvalue),
    'proxy_counterexample': {'true_A': 1, 'true_B': 1, 'proxy_scores': [100, 1],
                            'baseline': 4, 'candidate': str(proxy_counterexample)},
    'seed': 20260916,
    'scope': 'Exact finite binary algebra plus floating finite likelihood-kernel checks, not stochastic theorem proof',
    'elapsed_seconds': time.perf_counter()-start,
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(out/'theory-checks.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
