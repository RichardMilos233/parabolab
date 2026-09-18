"""Set-to-field denoiser: attention over a set of noisy coding-tree estimates.

Input  : a context set {(t_i, x_i, y_i, stderr_i)} of one PDE instance plus
         that instance's parameters, and query points (t, x).
Output : u(t, x) at the queries, in the units of y.

All per-instance scaling happens inside the model (the decisive lesson of
the 2026-09-15 ablation): (t, x) are standardised with the context's mean
and std per coordinate, y and stderr with the context's y mean and std,
parameters with fixed family constants; the output is un-scaled with the
context y statistics.  The model is therefore invariant to permutations
of the context and equivariant to affine changes of the y scale.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

import torch
from torch import nn


@dataclass(frozen=True)
class SetLatentState:
    """Encoded context plus every statistic needed to decode it."""

    latent: torch.Tensor
    mu_x: torch.Tensor
    s_x: torch.Tensor
    mu_y: torch.Tensor
    s_y: torch.Tensor
    params: torch.Tensor

    @property
    def physical_scale(self) -> torch.Tensor:
        return self.s_y

    def with_latent(self, latent: torch.Tensor) -> "SetLatentState":
        return replace(self, latent=latent)


class SetDenoiser(nn.Module):
    def __init__(self, d: int, n_params: int, d_model: int = 128,
                 n_heads: int = 4, n_layers: int = 4, dropout: float = 0.0,
                 param_mean=None, param_std=None) -> None:
        super().__init__()
        self.d = d
        self.n_params = n_params
        pm = torch.zeros(n_params) if param_mean is None \
            else torch.as_tensor(param_mean, dtype=torch.float32)
        ps = torch.ones(n_params) if param_std is None \
            else torch.as_tensor(param_std, dtype=torch.float32)
        self.register_buffer("param_mean", pm)
        self.register_buffer("param_std", ps)

        self.ctx_embed = nn.Sequential(
            nn.Linear(d + 1 + 2 + n_params, d_model), nn.GELU(),
            nn.Linear(d_model, d_model))
        layer = nn.TransformerEncoderLayer(
            d_model, n_heads, dim_feedforward=4 * d_model, dropout=dropout,
            activation="gelu", batch_first=True, norm_first=True)
        # norm_first=True on the layer makes nn.TransformerEncoder's own
        # nested-tensor fast path always ineligible; it emits a UserWarning
        # ("enable_nested_tensor is True, but self.use_nested_tensor is
        # False because encoder_layer.norm_first was True") every forward
        # pass otherwise. enable_nested_tensor=False silences it -- no
        # numerical or fast-path effect since the path never engages.
        self.encoder = nn.TransformerEncoder(layer, n_layers, enable_nested_tensor=False)
        self.q_embed = nn.Sequential(
            nn.Linear(d + 1 + n_params, d_model), nn.GELU(),
            nn.Linear(d_model, d_model))
        self.norm_q = nn.LayerNorm(d_model)
        self.norm_c = nn.LayerNorm(d_model)
        self.cross = nn.MultiheadAttention(d_model, n_heads, dropout=dropout,
                                           batch_first=True)
        self.head = nn.Sequential(nn.Linear(d_model, d_model), nn.GELU(),
                                  nn.Linear(d_model, 1))

    @property
    def n_params_total(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    @staticmethod
    def context_stats(ctx_y: torch.Tensor):
        """Per-instance mean and std of the context targets, shapes (B, 1)."""
        mu = ctx_y.mean(dim=1, keepdim=True)
        s = ctx_y.std(dim=1, keepdim=True).clamp_min(1e-8)
        return mu, s

    def encode(self, ctx_tx, ctx_y, ctx_se, params) -> SetLatentState:
        B, N, _ = ctx_tx.shape
        mu_x = ctx_tx.mean(dim=1, keepdim=True)
        s_x = ctx_tx.std(dim=1, keepdim=True).clamp_min(1e-6)   # (B,1,d+1)
        mu_y, s_y = self.context_stats(ctx_y)                    # (B,1)
        p = (params - self.param_mean) / self.param_std           # (B,P)

        ctx = torch.cat([
            (ctx_tx - mu_x) / s_x,
            ((ctx_y - mu_y) / s_y).unsqueeze(-1),
            (ctx_se / s_y).unsqueeze(-1),
            p.unsqueeze(1).expand(B, N, -1),
        ], dim=-1)
        h = self.encoder(self.ctx_embed(ctx))                    # (B,N,D)
        return SetLatentState(h, mu_x, s_x, mu_y, s_y, p)

    def decode(self, state: SetLatentState, q_tx):
        B, Q, _ = q_tx.shape
        q = self.q_embed(torch.cat([(q_tx - state.mu_x) / state.s_x,
                                    state.params.unsqueeze(1).expand(B, Q, -1)], dim=-1))
        hn = self.norm_c(state.latent)
        attn, _ = self.cross(self.norm_q(q), hn, hn)
        q = q + attn
        out = self.head(q).squeeze(-1)                           # (B,Q) scaled
        return out * state.s_y + state.mu_y

    def forward(self, ctx_tx, ctx_y, ctx_se, params, q_tx):
        return self.decode(self.encode(ctx_tx, ctx_y, ctx_se, params), q_tx)
