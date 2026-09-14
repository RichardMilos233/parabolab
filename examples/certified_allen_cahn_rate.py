"""Generate or recheck exact rational Allen--Cahn moment/rate certificates."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import time

from parabolab.rate_certificate import (
    BoxStep, CertificateFailure, FlatRateCertificate, MomentEnclosure,
    certify_flat_rate, enclose_allen_cahn_moment, factorial_depth_tail_upper,
    verify_flat_rate_certificate, verify_moment_enclosure,
)


def _moment_from_dict(d):
    state = lambda v: None if v is None else tuple(map(Fraction, v))
    witnesses = tuple(BoxStep(Fraction(w['duration']), state(w['upper_start']),
                              state(w['upper_end']), state(w['lower_start']),
                              state(w['lower_end'])) for w in d['witnesses'])
    return MomentEnclosure(d['family'], None if d['phi'] is None else Fraction(d['phi']),
                           Fraction(d['horizon']), tuple(map(Fraction, d['rates'])),
                           Fraction(d['tilt']), state(d['lower']), state(d['upper']),
                           witnesses, d['precision_bits'], d['mechanism'])


def _flat_from_dict(d):
    return FlatRateCertificate(tuple(map(Fraction, d['interval'])), Fraction(d['selected_rate']),
                               _moment_from_dict(d['incumbent']),
                               tuple(_moment_from_dict(v) for v in d['cells']),
                               Fraction(d['lower_optimum']), Fraction(d['excess_bound']),
                               Fraction(d['tolerance']), d['tolerance_met'])


def _independent_flat_reference(rate, horizon=0.05):
    """Floating diagnostic whose ODE is assembled from actual sampler tuples."""
    import numpy as np
    from scipy.integrate import solve_ivp
    from parabolab.library import allen_cahn_flat
    from parabolab.mechanism import Dx, FDeriv, Id, SemilinearMechanism

    pde = allen_cahn_flat(T=horizon)
    codes = (Id(), Dx(1), *(FDeriv(1, k) for k in range(4)))
    terminal = np.array([SemilinearMechanism.terminal(c, pde, 0)**2 for c in codes])

    def value(code, y):
        if SemilinearMechanism.is_identically_zero(code, pde):
            return 0.0
        if isinstance(code, Id):
            return y[0]
        if isinstance(code, Dx):
            return y[1]
        return code.a**2 * y[2 + code.k]

    def rhs(t, y):
        out = rate * y
        for i, code in enumerate(codes):
            choices = SemilinearMechanism.tuples(code)
            out[i] += sum(len(choices) * np.prod([value(z, y) for z in zs])
                          for zs in choices) / rate
        return out

    solution = solve_ivp(rhs, (0, horizon), terminal, rtol=1e-11, atol=1e-13,
                         method='DOP853')
    if not solution.success:
        raise RuntimeError(solution.message)
    return float(solution.y[0, -1])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('docs/research/results/rate-certificate'))
    parser.add_argument('--verify', type=Path, help='recheck a saved .json.gz witness archive')
    parser.add_argument('--steps', type=int, default=200)
    parser.add_argument('--max-splits', type=int, default=160)
    parser.add_argument('--tolerance', default='0.0001')
    args = parser.parse_args()
    if args.verify:
        data = json.loads(gzip.decompress(args.verify.read_bytes()))
        valid = verify_flat_rate_certificate(_flat_from_dict(data['flat'])) and all(
            verify_moment_enclosure(_moment_from_dict(c)) for c in
            [data['rate_one_baseline'], *data['wave']])
        print(json.dumps({'archive': str(args.verify), 'all_witnesses_valid': valid}))
        if not valid:
            raise SystemExit(1)
        return

    started = time.perf_counter()
    flat = certify_flat_rate(steps=args.steps, max_splits=args.max_splits,
                             tolerance=args.tolerance)
    flat_seconds = time.perf_counter() - started
    assert verify_flat_rate_certificate(flat)
    baseline = enclose_allen_cahn_moment(rates=(1, 1), steps=args.steps)
    assert verify_moment_enclosure(baseline)
    wave, failures = [], []
    for tilt in (1, 2, 4):
        try:
            c = enclose_allen_cahn_moment(family='wave', rates=('0.7', '0.8'),
                                          tilt=tilt, steps=args.steps)
            assert verify_moment_enclosure(c)
            wave.append(c)
        except CertificateFailure as error:
            failures.append({'tilt': tilt, 'status': 'inconclusive', 'reason': str(error)})

    from scipy.optimize import minimize_scalar
    from parabolab.library import allen_cahn_flat
    oracle = minimize_scalar(_independent_flat_reference, bounds=(0.2, 2),
                             method='bounded', options={'xatol': 1e-9})
    selected_ref = _independent_flat_reference(float(flat.selected_rate))
    mean_sq = allen_cahn_flat(T=0.05).exact_solution(0, 0)**2
    inside = float(flat.incumbent.root_lower) <= selected_ref <= float(flat.incumbent.root_upper)
    if not inside:
        raise RuntimeError('independent floating reference disagrees with certified enclosure')

    args.output.mkdir(parents=True, exist_ok=True)
    archive = {'flat': asdict(flat), 'rate_one_baseline': asdict(baseline),
               'wave': [asdict(c) for c in wave]}
    packed = gzip.compress(json.dumps(archive, default=str, separators=(',', ':')).encode(), mtime=0)
    witness_path = args.output / 'witnesses.json.gz'
    witness_path.write_bytes(packed)
    root = Path(__file__).resolve().parents[1]
    sources = ('parabolab/rate_certificate.py', 'parabolab/mechanism.py',
               'parabolab/library.py', 'examples/certified_allen_cahn_rate.py',
               'docs/research/estimator-integrity/allen-cahn-codewise-certificate.md',
               'docs/research/estimator-integrity/allen-cahn-mean-identification.md')
    summary = {
        'scope': 'ideal real-arithmetic raw SemilinearMechanism, uniform q, 1D Allen-Cahn',
        'certificate_type': 'exact rational time-step enclosures; conventional tree correspondence',
        'horizon': '1/20', 'flat_phi': '1/2', 'rate_interval': ['1/5', '2'],
        'steps': args.steps, 'precision_bits': 48, 'max_splits': args.max_splits,
        'selected_rate_exact': str(flat.selected_rate), 'selected_rate': float(flat.selected_rate),
        'incumbent_upper_exact': str(flat.incumbent.root_upper),
        'incumbent_upper': float(flat.incumbent.root_upper),
        'optimum_lower_exact': str(flat.lower_optimum), 'optimum_lower': float(flat.lower_optimum),
        'excess_bound_exact': str(flat.excess_bound), 'excess_bound': float(flat.excess_bound),
        'tolerance': args.tolerance, 'tolerance_met': flat.tolerance_met,
        'outside_interval_lower_exact': list(map(str, flat.outside_interval_lower)),
        'global_lower_optimum_exact': str(flat.global_lower_optimum),
        'global_excess_bound_exact': str(flat.global_excess_bound),
        'global_excess_bound': float(flat.global_excess_bound),
        'global_tolerance_met': flat.global_tolerance_met,
        'cells': len(flat.cells), 'flat_selection_seconds': flat_seconds,
        'all_flat_witnesses_verified': True,
        'rate_one_baseline': {
            'moment_lower_exact': str(baseline.root_lower),
            'moment_upper_exact': str(baseline.root_upper),
            'variance_reduction_lower_exact': str(baseline.root_lower-flat.incumbent.root_upper),
            'variance_reduction_lower': float(baseline.root_lower-flat.incumbent.root_upper),
            'meaning': 'additive reduction vs rate one; common PDE mean proved in allen-cahn-mean-identification.md',
        },
        'independent_floating_ode': {
            'role': 'diagnostic, not certificate', 'method': 'DOP853 + bounded scalar minimization',
            'rate': float(oracle.x), 'second_moment': float(oracle.fun),
            'selected_second_moment': selected_ref, 'selected_within_enclosure': inside,
            'exact_solution_squared': mean_sq,
            'selected_variance': selected_ref - mean_sq,
            'optimal_variance': float(oracle.fun) - mean_sq,
            'rate_one_variance': _independent_flat_reference(1) - mean_sq,
        },
        'wave': [{'tilt': str(c.tilt), 'rate_interval': list(map(str, c.rates)),
                  'root_upper_exact': str(c.root_upper), 'root_upper': float(c.root_upper),
                  'factorial_tail_upper': {str(k): float(factorial_depth_tail_upper(c, k))
                                           for k in (2, 4, 6, 8, 10)},
                  'witnesses_verified': True} for c in wave],
        'inconclusive': failures,
        'witness_archive_sha256': hashlib.sha256(packed).hexdigest(),
        'source_sha256': {s: hashlib.sha256((root/s).read_bytes()).hexdigest() for s in sources},
        'base_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
        'python': platform.python_version(),
        'not_covered': ['Gaussian quadrature error for traveling-wave rate selection',
                        'floating-point production sampler roundoff', 'nonuniform tuple proposals',
                        'global optimality of traveling-wave rate selection',
                        'Lean formalization of the stochastic moment correspondence'],
    }
    (args.output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
