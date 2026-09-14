"""Certify a weighted wave-profile objective, including exact spatial coordinates."""

from dataclasses import asdict
from fractions import Fraction as F
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import subprocess
import sys
import time

from certified_wave_rate import _decode_wave
from parabolab.profile_certificate import ProfileRateCertificate, verify_profile_rate_certificate
from parabolab.wave_certificate import enclose_wave_moment


GRID = (-2,-1,0,1,2)


def collocation_profile(rate, order=24):
    """Floating diagnostic assembled from sampler tuples, not Taylor recurrence."""
    import math
    import numpy as np
    from numpy.polynomial.chebyshev import chebder, chebval, chebvander
    from scipy.integrate import solve_ivp
    from parabolab.library import allen_cahn_wave_1d
    from parabolab.mechanism import Dx, FDeriv, Id, SemilinearMechanism

    nodes = np.cos(np.arange(order+1)*np.pi/order)
    s=(nodes+1)/2
    s[0],s[-1]=1,0
    basis=np.eye(order+1)
    values=chebvander(nodes,order)
    inverse=np.linalg.inv(values)
    d1=np.column_stack([2*chebval(nodes,chebder(c)) for c in basis])@inverse
    d2=np.column_stack([4*chebval(nodes,chebder(c,2)) for c in basis])@inverse
    diffusion=(s*s*(1-s)**2)[:,None]*d2/2+(s*(1-s)*(1-2*s))[:,None]*d1/2
    pde=allen_cahn_wave_1d(T=.05)
    codes=(Id(),Dx(1),*(FDeriv(1,k) for k in range(4)))
    positions=[-math.inf if v==1 else math.inf if v==0 else math.log((1-v)/v) for v in s]
    initial=np.array([[SemilinearMechanism.terminal(c,pde,x)**2 for x in positions] for c in codes])
    choices=[SemilinearMechanism.tuples(c) for c in codes]

    def value(c,y):
        if SemilinearMechanism.is_identically_zero(c,pde):
            return np.zeros(order+1)
        if isinstance(c,Id):
            return y[0]
        if isinstance(c,Dx):
            return y[1]
        return c.a**2*y[2+c.k]

    def rhs(t,flat):
        y=flat.reshape(6,order+1)
        out=y@diffusion.T+rate*y
        for i,tuples in enumerate(choices):
            out[i]+=sum(len(tuples)*np.prod([value(c,y) for c in zs],axis=0) for zs in tuples)/rate
        return out.ravel()

    solution=solve_ivp(rhs,(0,.05),initial.ravel(),method='DOP853',rtol=2e-11,atol=2e-13)
    if not solution.success:
        raise RuntimeError(solution.message)
    root=solution.y[:order+1,-1]
    coordinates=2/(1+np.exp(np.asarray(GRID,dtype=float)))-1
    return chebval(coordinates,inverse@root).tolist()


def main():
    # Exact interval/convex arithmetic creates fractions above Python's default
    # 4,300 decimal digits. Keep a bounded ceiling for these explicit artifacts.
    sys.set_int_max_str_digits(50000)
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('docs/research/results/profile-certificate'))
    parser.add_argument('--policy-metadata',type=Path,help='also bound the exact binary-float rates in a benchmark setup record')
    modes=parser.add_mutually_exclusive_group()
    modes.add_argument('--verify',type=Path)
    modes.add_argument('--from-witnesses',type=Path,help='recheck saved proposals and rebuild the summary')
    args=parser.parse_args()
    started=time.perf_counter()
    if args.verify or args.from_witnesses:
        source=args.verify or args.from_witnesses
        data=json.loads(gzip.decompress(source.read_bytes()))
        c=ProfileRateCertificate(tuple(_decode_wave(p) for p in data['points']),
            tuple(map(F,data['positions'])),tuple(map(F,data['weights'])),data['exp_terms'])
        valid=verify_profile_rate_certificate(c)
        if not valid:
            raise RuntimeError('profile witness verification failed')
        if args.verify:
            print(json.dumps({'archive':str(source),'all_witnesses_valid':True}))
            return
        if (c.positions!=tuple(map(F,GRID)) or c.weights!=(F(1,5),)*5
                or any(p.moment_box.horizon!=F(1,20) for p in c.points)
                or any(len(series)!=8 for p in c.points for series in p.polynomial)):
            raise ValueError('summary reconstruction requires this driver\'s fixed profile and degree-seven trials')
        points=list(c.points)
    else:
        # Exact rounded versions of both profile heuristics and old root policies.
        rates=tuple(map(F,('.4','.425','.45','.47497','.475','.49227','.5','.525',
                           '.55','.575','.6','.73055','.75','1')))
        points=[]
        for rate in rates:
            point=enclose_wave_moment(rate=rate,degree=7,spatial_splits=2)
            points.append(point)
            print(f'lambda={float(rate):.5f} error<={float(point.error[0]):.9g}',flush=True)
        c=ProfileRateCertificate(tuple(points),tuple(map(F,GRID)),(F(1,5),)*5)
        if not verify_profile_rate_certificate(c):
            raise RuntimeError('profile witness verification failed')
    incumbent=c.incumbent
    intervals={p.rate:c.moment_interval(p) for p in points}
    global_lower=c.global_lower
    mean_lo,mean_hi=c.mean_square_interval
    global_gap=intervals[incumbent.rate][1]-global_lower
    variance_lower=max(F(0),global_lower-mean_hi)
    relative_gap=None if variance_lower<=0 else global_gap/variance_lower
    chosen_rates=(incumbent.rate,F('.47497'),F('.49227'),F('.73055'),F('.75'),F(1))
    diagnostics=[]
    for rate in dict.fromkeys(chosen_rates):
        point=next(p for p in points if p.rate==rate)
        values=[collocation_profile(float(rate),order) for order in (24,36)]
        averages=[sum(v)/len(v) for v in values]
        lo,hi=map(float,intervals[point.rate])
        if not all(lo<=v<=hi for v in averages):
            raise RuntimeError('collocation profile disagrees with rational certificate')
        diagnostics.append({'rate':float(rate),'orders':[24,36],'point_moments':values,
                            'profile_moments':averages,'resolution_difference':abs(averages[0]-averages[1])})

    args.output.mkdir(parents=True,exist_ok=True)
    packed=gzip.compress(json.dumps(asdict(c),default=str,separators=(',',':')).encode(),mtime=0)
    (args.output/'witnesses.json.gz').write_bytes(packed)
    cells,exterior=c.lower_bounds
    selected_upper=intervals[incumbent.rate][1]
    comparisons=[]
    for p in points:
        lo,hi=intervals[p.rate]
        variance=(max(F(0),lo-mean_hi),hi-mean_lo)
        comparisons.append({'rate_exact':str(p.rate),'rate':float(p.rate),
            'moment_interval_exact':[str(lo),str(hi)],'moment_interval':[float(lo),float(hi)],
            'variance_interval_exact':list(map(str,variance)),
            'variance_interval':list(map(float,variance)),
            'global_gap_upper_exact':str(hi-global_lower),'global_gap_upper':float(hi-global_lower),
            'certified_reduction_to_incumbent_exact':str(lo-selected_upper),
            'certified_reduction_to_incumbent':float(lo-selected_upper)})
    root=Path(__file__).resolve().parents[1]
    sources=('parabolab/profile_certificate.py','parabolab/profile_rates.py',
             'parabolab/rate_certificate.py','parabolab/wave_certificate.py',
             'parabolab/mechanism.py','parabolab/library.py',
             'examples/certified_profile_rate.py','examples/certified_wave_rate.py',
             'docs/research/estimator-integrity/profile-rate-efficiency.md',
             'docs/research/estimator-integrity/allen-cahn-mean-identification.md',
             'docs/research/estimator-integrity/wave-numerical-certification-route.md')
    summary={'scope':'raw uniform 1D Allen-Cahn wave, ideal real arithmetic, common scalar rate',
        'horizon':'1/20','positions':list(GRID),'weights':['1/5']*5,
        'polynomial_degree':7,'spatial_splits':2,'exponential_terms':32,
        'selected_rate_exact':str(incumbent.rate),'selected_rate':float(incumbent.rate),
        'global_moment_lower_exact':str(global_lower),'global_moment_lower':float(global_lower),
        'global_variance_gap_upper_exact':str(global_gap),'global_variance_gap_upper':float(global_gap),
        'mean_square_interval_exact':list(map(str,(mean_lo,mean_hi))),
        'mean_square_interval':list(map(float,(mean_lo,mean_hi))),
        'global_variance_lower_exact':str(variance_lower),
        'global_variance_lower':float(variance_lower),
        'relative_variance_excess_upper_exact':None if relative_gap is None else str(relative_gap),
        'relative_variance_excess_upper':None if relative_gap is None else float(relative_gap),
        'cell_lower_exact':list(map(str,cells)),'exterior_lower_exact':list(map(str,exterior)),
        'outside_interval_excluded':all(v>selected_upper for v in exterior),
        'points':comparisons,'collocation_diagnostics':diagnostics,'all_witnesses_valid':True,
        'wall_seconds':time.perf_counter()-started,
        'construction_mode':'rechecked saved witness proposals' if args.from_witnesses else 'generated and checked proposals',
        'source_hash_scope':'executed verification and summary sources; proposal generation is not trusted by the verifier',
        'base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
        'source_sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in sources},
        'archive_sha256':hashlib.sha256(packed).hexdigest(),
        'limitations':['same n per point for profile-MSE interpretation',
                       'candidate nodes are rational rounded rates; benchmark_policy_bounds separately enclose exact binary-float policies',
                       'certificate construction is offline; no runtime benefit follows',
                       'stochastic and analytic bridges are conventional proofs, not Lean program verification']}
    if args.policy_metadata:
        metadata=json.loads(args.policy_metadata.read_text())
        if (metadata['status']!='complete' or metadata['grid']!=list(GRID)
                or metadata['weights']!=[.2]*5 or metadata['horizon']!=.05):
            raise ValueError('policy metadata must describe the completed matching wave-profile experiment')
        bounds=[]
        exact_variances={}
        for policy in metadata['setup']:
            rate=F.from_float(policy['rate'])
            upper=c.interpolated_moment_upper(rate)
            lower=intervals[rate][0] if rate in intervals else global_lower
            variance=(max(F(0),lower-mean_hi),upper-mean_lo)
            gap=upper-global_lower
            exact_variances[policy['variant']]=variance
            bounds.append({'variant':policy['variant'],'rate':policy['rate'],
                'rate_exact_binary':str(rate),'moment_upper_exact':str(upper),
                'variance_interval_exact':list(map(str,variance)),
                'variance_interval':list(map(float,variance)),
                'global_variance_gap_upper_exact':str(gap),'global_variance_gap_upper':float(gap),
                'relative_variance_excess_upper':None if variance_lower<=0 else float(gap/variance_lower)})
        summary['benchmark_policy_bounds']=bounds
        allocation_bounds=[]
        for phase in ('fixed_n','predicted_budget'):
            for reuse in metadata['reuse_counts']:
                rows=[]
                for index,policy in enumerate(metadata['setup']):
                    n=(metadata['fixed_samples_per_point'] if phase=='fixed_n' else
                       metadata['budget_samples_per_point'][str(reuse)][index])
                    lo,hi=(v/n for v in exact_variances[policy['variant']])
                    rows.append({'phase':phase,'reuse':reuse,'variant':policy['variant'],
                        'samples_per_point':n,'expected_mse_lower_exact':str(lo),
                        'expected_mse_upper_exact':str(hi),'expected_mse_interval':[float(lo),float(hi)]})
                reference=next(r for r in rows if r['variant']=='grid_short_uniform')
                ref_lo,ref_hi=F(reference['expected_mse_lower_exact']),F(reference['expected_mse_upper_exact'])
                for row in rows:
                    lo,hi=F(row['expected_mse_lower_exact']),F(row['expected_mse_upper_exact'])
                    row['mse_ratio_to_grid_short_interval']=(
                        [1.,1.] if row is reference else [float(lo/ref_hi),float(hi/ref_lo)])
                    row['certified_worse_than_grid_short']=lo>ref_hi
                allocation_bounds.extend(rows)
        summary['allocation_bounds']=allocation_bounds
        summary['expected_mse_scope']=('Expected mean per-request grid squared error conditional on independent '
            'frozen policies/counts, in the ideal T=1/20 real-arithmetic model. Requests are not pooled; '
            'no wall-time or production-roundoff guarantee.')
        summary['policy_metadata_path']=str(args.policy_metadata)
        summary['policy_metadata_sha256']=hashlib.sha256(args.policy_metadata.read_bytes()).hexdigest()
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ('selected_rate','global_variance_gap_upper',
        'relative_variance_excess_upper','outside_interval_excluded','all_witnesses_valid')},indent=2))


if __name__=='__main__':
    main()
