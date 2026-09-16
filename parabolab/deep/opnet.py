"""phi -> u operator backbones sharing forward(phi_grid (B,S), q_tx (B,Q,2)) -> (B,Q).

DeepONet   branch(phi) . trunk(t, x)
FNO1d      spectral convolutions on the sensor grid, queries by linear
           interpolation along the grid
AttnOperator  SetDenoiser reused: phi samples are the context tokens
           (x_j, phi_j, se=0), the query attends to them
Scalers phi_scale / in_* / out_* are buffers filled by optrain.fit_operator_scalers
(AttnOperator scales internally and ignores them).
"""

from __future__ import annotations

import numpy as np
import torch
from torch import nn

from .setnet import SetDenoiser


class _OperatorBase(nn.Module):
    needs_grid = False

    def _register_scalers(self):
        self.register_buffer("phi_scale", torch.ones(()))
        self.register_buffer("in_mean", torch.zeros(2))
        self.register_buffer("in_std", torch.ones(2))
        self.register_buffer("out_mean", torch.zeros(()))
        self.register_buffer("out_std", torch.ones(()))

    @property
    def n_params_total(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


def _mlp(sizes):
    layers = []
    for a, b in zip(sizes[:-1], sizes[1:]):
        layers += [nn.Linear(a, b), nn.GELU()]
    return nn.Sequential(*layers[:-1])


class DeepONet(_OperatorBase):
    def __init__(self, n_sensors: int = 101, p: int = 64, width: int = 128) -> None:
        super().__init__()
        self._register_scalers()
        self.branch = _mlp([n_sensors, width, width, p])
        self.trunk = _mlp([2, width, width, p])
        self.bias = nn.Parameter(torch.zeros(()))

    def forward(self, phi_grid, q_tx):
        b = self.branch(phi_grid / self.phi_scale)                       # (B,p)
        t = torch.nn.functional.gelu(self.trunk((q_tx - self.in_mean) / self.in_std))  # (B,Q,p)
        out = (t * b.unsqueeze(1)).sum(-1) + self.bias
        return out * self.out_std + self.out_mean


class SpectralConv1d(nn.Module):
    def __init__(self, width: int, modes: int) -> None:
        super().__init__()
        self.modes = modes
        scale = 1.0 / (width * width)
        self.weight = nn.Parameter(scale * torch.randn(width, width, modes, dtype=torch.cfloat))

    def forward(self, x):                        # x (B, width, S)
        xf = torch.fft.rfft(x)
        m = min(self.modes, xf.shape[-1])
        out = torch.zeros_like(xf)
        out[..., :m] = torch.einsum("bim,iom->bom", xf[..., :m], self.weight[..., :m])
        return torch.fft.irfft(out, n=x.shape[-1])


class FNO1d(_OperatorBase):
    needs_grid = True

    def __init__(self, grid, width: int = 32, modes: int = 16, n_layers: int = 4) -> None:
        super().__init__()
        self._register_scalers()
        grid = np.asarray(grid, dtype=float)
        steps = np.diff(grid)
        assert np.allclose(steps, steps[0]), "FNO1d needs a uniform sensor grid"
        self.register_buffer("grid", torch.as_tensor(grid, dtype=torch.float32))
        self.lift = nn.Linear(2, width)
        self.spectral = nn.ModuleList([SpectralConv1d(width, modes) for _ in range(n_layers)])
        self.pointwise = nn.ModuleList([nn.Conv1d(width, width, 1) for _ in range(n_layers)])
        self.proj = nn.Sequential(nn.Linear(width, 128), nn.GELU(), nn.Linear(128, 1))

    def on_grid(self, phi_grid):                 # (B,S) -> (B,S) scaled-output units
        B, S = phi_grid.shape
        xs = (self.grid / self.grid.abs().max()).expand(B, S)
        h = self.lift(torch.stack([phi_grid / self.phi_scale, xs], -1)).permute(0, 2, 1)  # (B,W,S)
        for spec, pw in zip(self.spectral, self.pointwise):
            h = torch.nn.functional.gelu(spec(h) + pw(h))
        return self.proj(h.permute(0, 2, 1)).squeeze(-1) * self.out_std + self.out_mean

    def forward(self, phi_grid, q_tx):
        vals = self.on_grid(phi_grid)            # (B,S)
        x = q_tx[..., 1]
        lo, hi, S = self.grid[0], self.grid[-1], self.grid.shape[0]
        pos = (x - lo) / (hi - lo) * (S - 1)
        i0 = pos.floor().clamp(0, S - 2).long()
        w = (pos - i0.float()).clamp(0.0, 1.0)
        v0 = torch.gather(vals, 1, i0)
        v1 = torch.gather(vals, 1, i0 + 1)
        return v0 * (1 - w) + v1 * w


class AttnOperator(_OperatorBase):
    needs_grid = True

    def __init__(self, grid=None, d_model: int = 128, n_heads: int = 4, n_layers: int = 4) -> None:
        super().__init__()
        self._register_scalers()
        self.core = SetDenoiser(d=1, n_params=1, d_model=d_model, n_heads=n_heads, n_layers=n_layers)
        grid = np.linspace(-8.0, 8.0, 101) if grid is None else np.asarray(grid, dtype=float)
        self.register_buffer("grid", torch.as_tensor(grid, dtype=torch.float32))

    def forward_tokens(self, xs, phi, q_tx):     # xs (B,S), phi (B,S)
        B, S = phi.shape
        ctx_tx = torch.stack([torch.zeros_like(xs), xs], -1)
        params = torch.zeros(B, 1, dtype=phi.dtype, device=phi.device)
        return self.core(ctx_tx, phi, torch.zeros_like(phi), params, q_tx)

    def forward(self, phi_grid, q_tx):
        xs = self.grid.expand(phi_grid.shape[0], -1)
        return self.forward_tokens(xs, phi_grid, q_tx)


def make_operator(name: str, grid, **kw):
    if name == "deeponet":
        return DeepONet(n_sensors=len(grid), **kw)
    if name == "fno":
        return FNO1d(grid, **kw)
    if name == "attn":
        return AttnOperator(grid, **kw)
    raise ValueError(f"unknown operator {name!r}; use deeponet, fno or attn")
