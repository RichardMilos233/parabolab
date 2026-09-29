"""Independent exact finite-law checks and flat moment references; not a PDE certificate."""
from fractions import Fraction as F
from itertools import product
import hashlib
import json
import math
from pathlib import Path
import platform
import random
import time

import numpy as np
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent


def kernel(rate, a, b, c):
    return ((rate + 1) / (3 * rate)) * (a + b + c) - a * b * c / rate


def conditional_second(rate, mean, second):
    alpha = (rate + 1) / (3 * rate)
    beta = 1 / rate
    return alpha**2 * (3 * second + 6 * mean**2) - 6 * alpha * beta * second * mean**2 + beta**2 * second**3


def main():
    started = time.perf_counter()
    rng = random.Random(9262026)
    cases = 120
    checked = 0
    for _ in range(cases):
        support = [F(rng.randint(-10, 10), 10) for _ in range(3)]
        weights = [rng.randint(1, 10) for _ in range(3)]
        probs = [F(w, sum(weights)) for w in weights]
        mean = sum(p * x for p, x in zip(probs, support))
        second = sum(p * x * x for p, x in zip(probs, support))
        generators = []
        for rate in [F(2), F(5, 2), F(3)]:
            direct_mean = F(0)
            direct_second = F(0)
            for i, j, k in product(range(3), repeat=3):
                mass = probs[i] * probs[j] * probs[k]
                value = kernel(rate, support[i], support[j], support[k])
                assert -1 <= value <= 1
                direct_mean += mass * value
                direct_second += mass * value**2
                checked += 1
            assert direct_mean == mean + (mean - mean**3) / rate
            assert direct_second == conditional_second(rate, mean, second)
            generators.append(rate * (direct_second - second))
        assert generators[0] >= generators[1] >= generators[2]
    for rate in [F(1), F(3, 2), F(199, 100)]:
        assert kernel(rate, F(1), F(1), F(-1)) > 1

    horizons = np.array([.05, .25, .5, 1, 1.5, 2])
    rows = []
    max_refinement_gap = 0.0
    for rate in [2., 2.5, 3.]:
        def rhs(t, y):
            mean = 1 / math.sqrt(1 + 3 * math.exp(-2*t))
            return [rate * (conditional_second(rate, mean, y[0]) - y[0])]
        coarse = solve_ivp(rhs, (0., 2.), [.25], t_eval=horizons, rtol=1e-9, atol=1e-11)
        fine = solve_ivp(rhs, (0., 2.), [.25], t_eval=horizons, method='DOP853', rtol=1e-12, atol=1e-14)
        assert coarse.success and fine.success
        for index, horizon in enumerate(horizons):
            second = float(fine.y[0, index])
            mean = 1 / math.sqrt(1 + 3 * math.exp(-2*float(horizon)))
            variance = second - mean**2
            gap = abs(second - float(coarse.y[0, index]))
            max_refinement_gap = max(max_refinement_gap, gap)
            assert mean**2 - 1e-11 <= second <= 1 + 1e-11
            rows.append(dict(rate=rate, horizon=float(horizon), mean=mean, second_moment=second,
                             variance=variance, expected_nodes=(3*math.exp(2*rate*float(horizon))-1)/2,
                             refinement_gap=gap))
    for horizon in horizons:
        values = [r['variance'] for r in rows if r['horizon'] == float(horizon)]
        assert all(a + 1e-10 >= b for a, b in zip(values, values[1:]))
    assert max_refinement_gap < 1e-7
    payload = dict(scope='Exact finite-support conditional-law checks; floating flat moment ODE references, not a validated certificate',
                   discrete_laws=cases, exact_kernel_evaluations=checked, seed=9262026,
                   corner_counterexamples_below_rate_two=3, all_checks_passed=True,
                   flat_moment_rows=rows, max_refinement_gap=max_refinement_gap,
                   seconds=time.perf_counter()-started, python=platform.python_version(),
                   script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE / 'bounded-theory-checks.json').write_text(json.dumps(payload, indent=2)+'\n')
    print(json.dumps({k:v for k,v in payload.items() if k != 'flat_moment_rows'}, indent=2))

if __name__ == '__main__':
    main()
