"""Check an architectural identity, not trained-model performance.

Run with --repo pointing to the inspected parabolab checkout.
The Fourier calculation checks the initial Allen--Cahn time derivative.
"""
import argparse
import json
import math
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', required=True)
args = parser.parse_args()
sys.path.insert(0, args.repo)

import torch
from parabolab.deep.opnet import AttnOperator

torch.set_num_threads(1)
torch.manual_seed(17)
grid = torch.linspace(-8, 8, 101, dtype=torch.float64)
net = AttnOperator(grid=grid.numpy(), d_model=16, n_heads=4, n_layers=1).double().eval()
phi = (0.25 * torch.cos(math.pi * grid / 8)
       + 0.15 * torch.sin(2 * math.pi * grid / 8))[None]
query = torch.stack([torch.zeros_like(grid), grid], -1)[None]
states = []
handle = net.core.encoder.register_forward_hook(
    lambda module, inputs, output: states.append(output.detach().clone()))
alpha, beta = 1.7, 0.12
with torch.no_grad():
    y = net(phi, query)
    y_affine = net(alpha * phi + beta, query)
handle.remove()

# Periodic [0,2pi), endpoint excluded. For v=a*cos(x):
# d_tau v = 0.5*v_xx + v - v^3; its cos(3x) coefficient is -a^3/4.
x = torch.arange(128, dtype=torch.float64) * (2 * math.pi / 128)
coefficients = []
for amplitude in (0.2, 0.4):
    v = amplitude * torch.cos(x)
    derivative = 0.5 * (-v) + v - v**3
    coefficient = float(2 * torch.mean(derivative * torch.cos(3*x)))
    coefficients.append({'amplitude': amplitude, 'measured_cos3_derivative': coefficient,
                         'analytic_cos3_derivative': -amplitude**3 / 4})
result = {
    'scope': 'Untrained architecture identity and analytic initial-time derivative; no training or rollout',
    'torch_version': torch.__version__, 'seed': 17, 'dtype': 'float64',
    'model': {'d_model': 16, 'n_heads': 4, 'n_layers': 1, 'sensors': 101},
    'alpha': alpha, 'beta': beta,
    'encoder_max_abs_difference': float((states[1] - states[0]).abs().max()),
    'affine_prediction_max_abs_residual': float((y_affine - alpha*y - beta).abs().max()),
    'allen_cahn_initial_derivative': coefficients,
    'cos3_derivative_ratio_a04_over_a02': coefficients[1]['measured_cos3_derivative'] / coefficients[0]['measured_cos3_derivative'],
    'homogeneous_architecture_prediction_ratio': 2.0,
}
print(json.dumps(result, indent=2))
