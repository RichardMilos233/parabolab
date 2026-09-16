"""Generate/recheck rational full-tree traveling-wave rate certificates."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import time

from parabolab.rate_certificate import BoxStep, MomentEnclosure, enclose_allen_cahn_moment
from parabolab.wave_certificate import (
    ErrorStep, WaveMomentCertificate, WaveRateCertificate, enclose_wave_moment,
    verify_wave_moment_certificate, verify_wave_rate_certificate,
)


def _decode_moment(d):
    state = lambda v: None if v is None else tuple(map(F,v))
    return MomentEnclosure(d['family'], None if d['phi'] is None else F(d['phi']),
                           F(d['horizon']), tuple(map(F,d['rates'])), F(d['tilt']),
                           state(d['lower']), state(d['upper']),
                           tuple(BoxStep(F(w['duration']),state(w['upper_start']),
                                         state(w['upper_end']),state(w['lower_start']),
                                         state(w['lower_end'])) for w in d['witnesses']),
                           d['precision_bits'], d['mechanism'])


def _decode_wave(d):
    return WaveMomentCertificate(F(d['rate']), _decode_moment(d['moment_box']),
                                  tuple(tuple(tuple(map(F,p)) for p in series)
                                        for series in d['polynomial']),
                                  tuple(map(F,d['magnitude'])), tuple(map(F,d['residual'])),
                                  tuple(ErrorStep(F(w['duration']),tuple(map(F,w['start'])),
                                                  tuple(map(F,w['end']))) for w in d['error_steps']),
                                  d['spatial_splits'])


def collocation_reference(rate, horizon=0.05, order=24):
    """Floating diagnostic: Chebyshev collocation, actual sampler tuple assembly.

    This computation is independent of the rational polynomial recurrence and
    carries no rigorous error claim. Resolution agreement is diagnostic only.
    """
    import math
    import numpy as np
    from numpy.polynomial.chebyshev import chebder, chebval, chebvander
    from scipy.integrate import solve_ivp
    from parabolab.library import allen_cahn_wave_1d
    from parabolab.mechanism import Dx, FDeriv, Id, SemilinearMechanism

    nodes = np.cos(np.arange(order+1)*np.pi/order)
    s = (nodes+1)/2
    s[0], s[-1] = 1, 0
    basis = np.eye(order+1)
    values = chebvander(nodes,order)
    d1 = np.column_stack([2*chebval(nodes,chebder(c)) for c in basis]) @ np.linalg.inv(values)
    d2 = np.column_stack([4*chebval(nodes,chebder(c,2)) for c in basis]) @ np.linalg.inv(values)
    diffusion = (s*s*(1-s)**2)[:,None]*d2/2 + (s*(1-s)*(1-2*s))[:,None]*d1/2
    pde = allen_cahn_wave_1d(T=horizon)
    codes = (Id(), Dx(1), *(FDeriv(1,k) for k in range(4)))
    positions = [-math.inf if v == 1 else math.inf if v == 0 else math.log((1-v)/v) for v in s]
    initial = np.array([[SemilinearMechanism.terminal(c,pde,x)**2 for x in positions] for c in codes])

    def value(code,y):
        if SemilinearMechanism.is_identically_zero(code,pde):
            return np.zeros(order+1)
        if isinstance(code,Id):
            return y[0]
        if isinstance(code,Dx):
            return y[1]
        return code.a**2*y[2+code.k]

    tuples = [SemilinearMechanism.tuples(c) for c in codes]

    def rhs(t, flattened):
        y = flattened.reshape(6,order+1)
        out = y @ diffusion.T + rate*y
        for i,choices in enumerate(tuples):
            out[i] += sum(len(choices)*np.prod([value(c,y) for c in zs],axis=0)
                          for zs in choices)/rate
        return out.ravel()

    solution = solve_ivp(rhs,(0,horizon),initial.ravel(),method='DOP853',rtol=2e-11,atol=2e-13)
    if not solution.success:
        raise RuntimeError(solution.message)
    root = solution.y[:order+1,-1]
    return float(chebval(0,np.linalg.solve(values,root)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('docs/research/results/wave-certificate'))
    parser.add_argument('--verify',type=Path)
    parser.add_argument('--degree',type=int,default=5)
    parser.add_argument('--spatial-splits',type=int,default=2)
    args = parser.parse_args()
    if args.verify:
        data = json.loads(gzip.decompress(args.verify.read_bytes()))
        certificate = WaveRateCertificate(tuple(_decode_wave(d) for d in data['points']),F(data['coordinate']))
        valid = verify_wave_rate_certificate(certificate) and verify_wave_moment_certificate(_decode_wave(data['baseline']))
        print(json.dumps({'archive':str(args.verify),'all_witnesses_valid':valid}))
        if not valid:
            raise SystemExit(1)
        return

    started = time.perf_counter()
    box = enclose_allen_cahn_moment(family='wave',rates=('0.7','0.8'),steps=200)
    rates = tuple(map(F,('0.7','0.7125','0.725','0.73055','0.7375','0.75',
                         '0.7625','0.775','0.7875','0.8')))
    points = []
    for rate in rates:
        c = enclose_wave_moment(rate=rate,moment_box=box,degree=args.degree,
                                spatial_splits=args.spatial_splits)
        points.append(c)
        print(f'lambda={float(rate):.5f} root_error<={float(c.error[0]):.9g}',flush=True)
    certificate = WaveRateCertificate(tuple(points))
    baseline = enclose_wave_moment(rate=1,degree=args.degree,spatial_splits=args.spatial_splits)
    if not verify_wave_rate_certificate(certificate) or not verify_wave_moment_certificate(baseline):
        raise RuntimeError('exact witness verification failed')

    from parabolab.library import allen_cahn_wave_1d
    incumbent = certificate.incumbent
    historical = next(c for c in points if c.rate == F('0.73055'))
    diagnostics = []
    for c in (incumbent,historical,baseline):
        values = [collocation_reference(float(c.rate),order=n) for n in (24,36)]
        lower,upper = map(float,c.moment_at())
        if not all(lower <= v <= upper for v in values):
            raise RuntimeError('independent collocation falls outside certified interval')
        diagnostics.append({'rate':float(c.rate),'orders':[24,36],'moments':values,
                            'resolution_difference':abs(values[1]-values[0])})
    args.output.mkdir(parents=True,exist_ok=True)
    payload = {'coordinate':str(certificate.coordinate),'points':[asdict(c) for c in points],
               'baseline':asdict(baseline)}
    packed = gzip.compress(json.dumps(payload,default=str,separators=(',',':')).encode(),mtime=0)
    archive = args.output/'witnesses.json.gz'
    archive.write_bytes(packed)
    cells,exterior = certificate.lower_bounds
    root = Path(__file__).resolve().parents[1]
    sources = ('parabolab/wave_certificate.py','parabolab/rate_certificate.py',
               'parabolab/mechanism.py','parabolab/library.py','examples/certified_wave_rate.py',
               'docs/research/estimator-integrity/wave-numerical-certification-route.md',
               'docs/research/estimator-integrity/allen-cahn-codewise-certificate.md',
               'docs/research/estimator-integrity/allen-cahn-mean-identification.md')
    summary = {
        'scope':'ideal real-arithmetic raw uniform SemilinearMechanism; 1D Allen-Cahn wave',
        'certificate_type':'rational polynomial residual, moment box, linear error witnesses, convex extrapolation',
        'horizon':'1/20','coordinate':'1/2','x':0,'degree':args.degree,
        'spatial_splits':args.spatial_splits,'error_steps':100,'precision_bits':60,
        'points':[{'rate_exact':str(c.rate),'rate':float(c.rate),
                   'lower_exact':str(c.moment_at()[0]),'upper_exact':str(c.moment_at()[1]),
                   'lower':float(c.moment_at()[0]),'upper':float(c.moment_at()[1]),
                   'root_error':float(c.error[0])} for c in points],
        'selected_rate_exact':str(incumbent.rate),'selected_rate':float(incumbent.rate),
        'global_lower_exact':str(certificate.global_lower),'global_lower':float(certificate.global_lower),
        'global_excess_bound_exact':str(certificate.global_gap),'global_excess_bound':float(certificate.global_gap),
        'historical_rate_exact':str(historical.rate),
        'historical_rate_global_excess_bound_exact':str(historical.moment_at()[1]-certificate.global_lower),
        'historical_rate_global_excess_bound':float(historical.moment_at()[1]-certificate.global_lower),
        'cell_lower_exact':list(map(str,cells)),
        'exterior_lower_exact':list(map(str,exterior)),
        'exterior_lower':list(map(float,exterior)),
        'outside_interval_excluded':all(bound>incumbent.moment_at()[1] for bound in exterior),
        'baseline_moment_interval_exact':list(map(str,baseline.moment_at())),
        'baseline_moment_interval':list(map(float,baseline.moment_at())),
        'guaranteed_additive_variance_reduction_vs_rate_one_exact':str(baseline.moment_at()[0]-incumbent.moment_at()[1]),
        'guaranteed_additive_variance_reduction_vs_rate_one':float(baseline.moment_at()[0]-incumbent.moment_at()[1]),
        'variance_translation':'common PDE mean proved in allen-cahn-mean-identification.md; conventional, not Lean stochastic proof',
        'mean_squared_diagnostic':allen_cahn_wave_1d(T=.05).exact_solution(0,0)**2,
        'collocation_diagnostics':diagnostics,'all_witnesses_valid':True,
        'wall_seconds':time.perf_counter()-started,'python':platform.python_version(),
        'platform':platform.platform(),
        'base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
        'source_sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in sources},
        'archive_sha256':hashlib.sha256(packed).hexdigest(),
        'limitations':['certifies objective excess, not parameter distance to minimizer',
                       'one horizon and spatial root, uniform raw mechanism only',
                       'not a sampler floating-point or Lean stochastic soundness certificate',
                       'collocation is a separate floating diagnostic, not the source of rigorous bounds'],
    }
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ('selected_rate','global_excess_bound',
                                             'historical_rate_global_excess_bound',
                                             'outside_interval_excluded','all_witnesses_valid')},indent=2))


if __name__ == '__main__':
    main()
