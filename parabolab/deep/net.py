"""The feed-forward residual network of JCP2024 eq. (3.2)-(3.3), plus the
knobs of the 2026-09-15 ablation study.

Paper architecture (matching NN^zeta_{d+1,l,m} and the authors' branch.py):

    input (t, x) in R^{d+1}
    -> Linear(d+1, m) -> zeta -> BatchNorm            (first hidden layer)
    -> [ Linear(m, m) -> zeta -> BatchNorm, + skip ]  x (l - 1)  (residual)
    -> Linear(m, 1)                                   (identity output)

Defaults l = 6 hidden layers of m = 20 neurons, zeta = tanh, batch
normalization AFTER the activation (Remark 3.1 iv / branch.py order).
The paper counts the first (non-residual) hidden layer in l, i.e. l = 6
means 1 plain + 5 residual hidden layers, like the authors' layers=5.

Ablation knobs (all default to the paper's behaviour):

    norm              "batch" | "layer" | "none"   (after the activation)
    activation        + "silu" | "gelu" | "sin"
    fourier_features  F > 0 maps x -> [cos(2 pi B x), sin(2 pi B x)],
                      B ~ N(0, fourier_sigma^2) fixed at construction;
                      t is passed through unchanged
    scale_input /     fixed affine maps stored as buffers (in_mean, in_std,
    scale_output      out_mean, out_std); identity until fit_scalers() in
                      solver.py fills them from the training data
"""

from __future__ import annotations

import math

import torch


class Sine(torch.nn.Module):
    def forward(self, x):
        return torch.sin(x)


_ACTIVATIONS = {
    "tanh": torch.nn.Tanh,
    "relu": torch.nn.ReLU,
    "id": torch.nn.Identity,
    "silu": torch.nn.SiLU,
    "gelu": torch.nn.GELU,
    "sin": Sine,
}


def _make_norm(kind: str, neurons: int, device):
    if kind == "batch":
        return torch.nn.BatchNorm1d(neurons, device=device)
    if kind == "layer":
        return torch.nn.LayerNorm(neurons, device=device)
    if kind == "none":
        return torch.nn.Identity()
    raise ValueError(f"unknown norm {kind!r}; use batch, layer or none")


class DeepBranchNet(torch.nn.Module):
    def __init__(
        self,
        d: int,
        hidden_layers: int = 6,
        neurons: int = 20,
        activation: str = "tanh",
        batch_norm: bool = True,
        device=None,
        *,
        norm: str | None = None,
        fourier_features: int = 0,
        fourier_sigma: float = 1.0,
        scale_input: bool = False,
        scale_output: bool = False,
    ) -> None:
        super().__init__()
        if hidden_layers < 1:
            raise ValueError("need at least one hidden layer")
        if fourier_features < 0:
            raise ValueError("fourier_features must be >= 0")
        if norm is None:
            norm = "batch" if batch_norm else "none"
        self.d = d
        self.norm = norm
        self.batch_norm = norm == "batch"      # kept for callers of the flag
        self.fourier_features = fourier_features
        self.scale_input = scale_input
        self.scale_output = scale_output
        self.activation = _ACTIVATIONS[activation]()

        in_dim = d + 1
        if fourier_features > 0:
            self.register_buffer(
                "fourier_B",
                fourier_sigma * torch.randn(d, fourier_features, device=device))
            in_dim = 1 + 2 * fourier_features
        self.register_buffer("in_mean", torch.zeros(d + 1, device=device))
        self.register_buffer("in_std", torch.ones(d + 1, device=device))
        self.register_buffer("out_mean", torch.zeros((), device=device))
        self.register_buffer("out_std", torch.ones((), device=device))

        self.linears = torch.nn.ModuleList(
            [torch.nn.Linear(in_dim, neurons, device=device)]
            + [torch.nn.Linear(neurons, neurons, device=device)
               for _ in range(hidden_layers - 1)]
            + [torch.nn.Linear(neurons, 1, device=device)]
        )
        self.bns = torch.nn.ModuleList(
            [_make_norm(norm, neurons, device) for _ in range(hidden_layers)]
        )

    @property
    def n_params(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def forward(self, tx: torch.Tensor) -> torch.Tensor:
        """tx of shape (batch, d+1) = (t, x_1..x_d) -> (batch,)."""
        z = (tx - self.in_mean) / self.in_std
        if self.fourier_features > 0:
            proj = 2.0 * math.pi * (z[:, 1:] @ self.fourier_B)
            z = torch.cat([z[:, :1], torch.cos(proj), torch.sin(proj)], dim=1)
        y = z
        for idx, (lin, bn) in enumerate(zip(self.linears[:-1], self.bns)):
            tmp = bn(self.activation(lin(y)))
            y = tmp if idx == 0 else tmp + y   # residual skip after layer 0
        out = self.linears[-1](y).reshape(-1)
        return out * self.out_std + self.out_mean
