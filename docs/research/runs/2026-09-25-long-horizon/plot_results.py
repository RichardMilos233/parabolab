"""Scientific overview from the fixed long-horizon experiment and analytic boundaries."""
from pathlib import Path
import json
import math

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad

RUN = Path(__file__).resolve().parent


def main():
    records = json.loads((RUN/'numerics/bounded-results.json').read_text())['rows']
    front = [r for r in records if 'wave' in r['problem'].lower()
             and abs(r['x'] - 1.5*r['horizon']) < 1e-10]
    front2 = sorted([r for r in front if r['rate'] == 2], key=lambda r:r['horizon'])
    assert len(front2) == 6
    c, _ = quad(lambda z: 1/(9/64+z/16+4.5*z*z+6*z**3), 0, np.inf,
                epsabs=1e-12, epsrel=1e-12)
    tabs = (3*math.pi-2*math.log(3))/5
    blue, green, orange, gray = '#285475', '#46856b', '#B07131', '#555C61'
    plt.rcParams.update({'font.size':10, 'axes.spines.top':False, 'axes.spines.right':False,
                         'axes.titleweight':'bold', 'axes.labelcolor':'#30383D',
                         'axes.edgecolor':'#B8C0C4', 'grid.color':'#E5E9EB'})
    fig, axes = plt.subplots(2,2,figsize=(12,8.4), constrained_layout=True)
    rates=np.linspace(.01,5,500)
    ax=axes[0,0]
    for p,color,label in [(.5,blue,'Raw uniform p=0.5'),(.95,green,'Raw supported p=0.95')]:
        horizon=np.log1p(rates*rates*p*c)/rates
        ax.plot(rates,horizon,label=label,color=color,lw=2)
    ax.axhline(tabs,color=gray,ls='--',label=f'Raw absolute-moment ceiling {tabs:.5f}')
    ax.set(xlabel='Common raw clock rate λ',ylabel='Critical horizon T (boundary excluded)',
           title='A. Proposal tuning has a finite horizon',ylim=(0,1.65))
    ax.legend(fontsize=8.5,loc='lower right'); ax.grid(alpha=.6)
    ax.text(.02,.95,'Flat terminal value 1/2; curves use the exact moment formula',
            transform=ax.transAxes,va='top',fontsize=8,color=gray)

    ax=axes[0,1]; times=np.linspace(0,2,300)
    ax.plot(times,100*(1-np.exp(-times)),color=blue,label='Raw fixed λ=1')
    ax.plot(times,100*(1-np.exp(-2*times)),color=green,label='Bounded ternary rate=2')
    ax.plot(times[1:],np.full_like(times[1:],5),color=orange,ls='--',label='Paper λ=−log(0.95)/T, T>0')
    ax.set(xlabel='Horizon T',ylabel='Probability root branches (%)',
           title='B. Scaling λ as 1/T keeps branching rare',ylim=(0,105))
    ax.legend(fontsize=8.5,loc='lower right'); ax.grid(alpha=.6)

    ax=axes[1,0]
    ts=np.array([r['horizon'] for r in front2]); means=np.array([r['mean'] for r in front2])
    radii=np.array([math.sqrt(2*math.log(40)/r['n_samples']) for r in front2])
    ax.errorbar(ts,means,yerr=radii,fmt='o',capsize=3,color=green,label='Bounded MC: pointwise 95% Hoeffding')
    ax.axhline(-.5,color=gray,ls='--',label='Exact traveling-wave value')
    ax.set(xlabel='Horizon T; root position x=1.5T',ylabel='Estimated PDE value u(0, x)',
           title='C. A moving-front check remains nontrivial')
    ax.legend(fontsize=8,loc='lower left'); ax.grid(alpha=.6)
    ax.text(.98,.97,'2048 complete roots per point; rate=2\nIntervals assume exact bounded arithmetic',
            transform=ax.transAxes,ha='right',va='top',fontsize=8,color=gray)

    ax=axes[1,1]
    ax.semilogy(times,(3*np.exp(4*times)-1)/2,color=green,label='Expected nodes (3e^(4T)−1)/2')
    ax.semilogy(ts,[r['mean_nodes'] for r in front2],'o',color=blue,label='Observed mean, moving front')
    ax.set(xlabel='Horizon T',ylabel='Sampled nodes per complete root (log scale)',
           title='D. Finite variance retains exponential work')
    ax.legend(fontsize=8.5,loc='upper left'); ax.grid(alpha=.6,which='both')
    fig.suptitle('Allen–Cahn: extending the branching horizon',fontsize=17,fontweight='bold')
    fig.text(.5,-.015,'Source: long-horizon research run, 25–26 Sep 2026; exact formulas and complete-tree Monte Carlo.',
             ha='center',fontsize=8,color=gray)
    fig.savefig(RUN/'long-horizon-overview.png',dpi=190,bbox_inches='tight')
    fig.savefig(RUN/'long-horizon-overview.pdf',bbox_inches='tight')
    print(RUN/'long-horizon-overview.png')

if __name__=='__main__':
    main()
