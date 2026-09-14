"""Plot the saved deterministic wave certificate; no new moment computations."""

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt


def main():
    folder = Path('docs/research/results/wave-certificate')
    data = json.loads((folder/'summary.json').read_text())
    points = data['points']
    rate = np.array([p['rate'] for p in points])
    lower = np.array([p['lower'] for p in points])
    upper = np.array([p['upper'] for p in points])
    offset, scale = .27235, 1e6
    fig, ax = plt.subplots(figsize=(9,5.5), layout='constrained')
    center = (upper+lower)/2
    ax.errorbar(rate, (center-offset)*scale, yerr=(upper-lower)*scale/2,
                fmt='o', color='#21647b', ms=4, capsize=3,
                label='Certified full-moment interval at each rate')
    from fractions import Fraction
    for i, bound in enumerate(data['cell_lower_exact']):
        height = (float(Fraction(bound))-offset)*scale
        ax.plot(rate[i:i+2], [height,height], color='#bd8441', linewidth=2,
                label='Certified lower bound throughout each cell' if i == 0 else None)
    ax.axhline((data['global_lower']-offset)*scale, color='#84674e', linestyle=':',
                label='Global infimum lower bound')
    ax.axvline(data['selected_rate'], ymax=.24, color='#468779', linewidth=1, alpha=.7)
    ax.axvline(float(Fraction(data['historical_rate_exact'])), color='#707070',
                ymax=.24, linewidth=1, linestyle='--', alpha=.7)
    ax.set(xlabel='Exponential rate λ', ylabel='Second moment minus 0.27235 (×10⁻⁶)',
           title='Traveling-wave rate certificate · T = 0.05, x = 0',
           xlim=(.696,.804))
    ax.text(.01,.96,'Historical λ = 0.73055: global objective gap ≤ 6.14 × 10⁻⁶\n'
                      'Candidate λ = 0.7375: global objective gap ≤ 5.69 × 10⁻⁶',
             transform=ax.transAxes, va='top', fontsize=10)
    ax.spines[['top','right']].set_visible(False)
    ax.grid(axis='y', color='#dddcd8', linewidth=.6)
    ax.legend(loc='upper left', bbox_to_anchor=(.01,.80), frameon=False, fontsize=8)
    fig.text(.02,-.035,'Exact rational bounds, displayed as decimals. Error bars are deterministic enclosures, not confidence intervals.\n'
             'The two candidate intervals overlap; these results do not prove which candidate has the lower true moment.',
             fontsize=8, color='#555555')
    fig.savefig(folder/'rate_enclosures.png',dpi=180,bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    main()
