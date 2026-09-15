"""Parameter-conditioned network u(t, x; theta) on the ablation's R5A trunk.

mode="concat": theta (scaled) is appended to the (t, x) input.
mode="film":   theta drives per-layer scale/shift of the trunk's hidden
               activations, h -> h * (1 + alpha_l) + beta_l, from a small MLP
               whose last layer is zero-initialised (so the net equals the
               plain trunk at initialisation).
Scalers (in_mean/in_std for (t, x), out_mean/out_std for u, param_mean/
param_std for theta) are buffers; condtrain.fit_conditioned_scalers fills
the first two from the pooled corpus.
"""

from __future__ import annotations

import torch
from torch import nn


def autograd_derivatives(fn, tx: torch.Tensor, *, create_graph: bool = False):
    """(u, u_x, u_xx) of fn(tx) w.r.t. column 1 of tx (first spatial coord)."""
    tx = tx.detach().requires_grad_(True)
    u = fn(tx)
    (g,) = torch.autograd.grad(u.sum(), tx, create_graph=True)
    ux = g[:, 1]
    (g2,) = torch.autograd.grad(ux.sum(), tx, create_graph=create_graph)
    uxx = g2[:, 1]
    if not create_graph:
        u, ux, uxx = u.detach(), ux.detach(), uxx.detach()
    return u, ux, uxx


class ConditionedNet(nn.Module):
    def __init__(self, d: int, n_params: int, mode: str = "concat",
                 hidden_layers: int = 6, neurons: int = 64,
                 param_mean=None, param_std=None) -> None:
        super().__init__()
        if mode not in ("concat", "film"):
            raise ValueError(f"mode must be 'concat' or 'film', got {mode!r}")
        self.d, self.n_params, self.mode = d, n_params, mode
        self.hidden_layers, self.neurons = hidden_layers, neurons
        self.register_buffer("in_mean", torch.zeros(d + 1))
        self.register_buffer("in_std", torch.ones(d + 1))
        self.register_buffer("out_mean", torch.zeros(()))
        self.register_buffer("out_std", torch.ones(()))
        pm = torch.zeros(n_params) if param_mean is None else torch.as_tensor(param_mean, dtype=torch.float32)
        ps = torch.ones(n_params) if param_std is None else torch.as_tensor(param_std, dtype=torch.float32)
        self.register_buffer("param_mean", pm)
        self.register_buffer("param_std", ps)
        in_dim = d + 1 + (n_params if mode == "concat" else 0)
        self.linears = nn.ModuleList(
            [nn.Linear(in_dim, neurons)]
            + [nn.Linear(neurons, neurons) for _ in range(hidden_layers - 1)]
            + [nn.Linear(neurons, 1)])
        self.act = nn.GELU()
        if mode == "film":
            self.film = nn.Sequential(nn.Linear(n_params, 64), nn.GELU(),
                                      nn.Linear(64, 2 * hidden_layers * neurons))
            nn.init.zeros_(self.film[-1].weight)
            nn.init.zeros_(self.film[-1].bias)

    @property
    def n_params_total(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def forward(self, tx: torch.Tensor, params: torch.Tensor) -> torch.Tensor:
        z = (tx - self.in_mean) / self.in_std
        p = (params - self.param_mean) / self.param_std
        y = torch.cat([z, p], dim=-1) if self.mode == "concat" else z
        ab = None
        if self.mode == "film":
            ab = self.film(p).view(-1, self.hidden_layers, 2, self.neurons)
        for idx, lin in enumerate(self.linears[:-1]):
            h = self.act(lin(y))
            if ab is not None:
                h = h * (1 + ab[:, idx, 0]) + ab[:, idx, 1]
            y = h if idx == 0 else h + y
        return self.linears[-1](y).squeeze(-1) * self.out_std + self.out_mean
