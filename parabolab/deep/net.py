"""The feed-forward residual network of JCP2024 eq. (3.2)-(3.3).

Architecture (matching the paper's NN^zeta_{d+1,l,m} and the authors'
branch.py):

    input (t, x) in R^{d+1}
    -> Linear(d+1, m) -> zeta -> BatchNorm            (first hidden layer)
    -> [ Linear(m, m) -> zeta -> BatchNorm, + skip ]  x (l - 1)  (residual)
    -> Linear(m, 1)                                   (identity output)

Defaults l = 6 hidden layers of m = 20 neurons, zeta = tanh, batch
normalization AFTER the activation (Remark 3.1 iv / branch.py order).
The paper counts the first (non-residual) hidden layer in l, i.e. l = 6
means 1 plain + 5 residual hidden layers, like the authors' layers=5.
"""

from __future__ import annotations

import torch


_ACTIVATIONS = {
    "tanh": torch.nn.Tanh,
    "relu": torch.nn.ReLU,
    "id": torch.nn.Identity,
}


class DeepBranchNet(torch.nn.Module):
    def __init__(
        self,
        d: int,
        hidden_layers: int = 6,
        neurons: int = 20,
        activation: str = "tanh",
        batch_norm: bool = True,
        device=None,
    ) -> None:
        super().__init__()
        if hidden_layers < 1:
            raise ValueError("need at least one hidden layer")
        self.d = d
        self.activation = _ACTIVATIONS[activation]()
        self.batch_norm = batch_norm
        self.linears = torch.nn.ModuleList(
            [torch.nn.Linear(d + 1, neurons, device=device)]
            + [torch.nn.Linear(neurons, neurons, device=device)
               for _ in range(hidden_layers - 1)]
            + [torch.nn.Linear(neurons, 1, device=device)]
        )
        self.bns = torch.nn.ModuleList(
            [torch.nn.BatchNorm1d(neurons, device=device)
             for _ in range(hidden_layers)]
        )

    def forward(self, tx: torch.Tensor) -> torch.Tensor:
        """tx of shape (batch, d+1) = (t, x_1..x_d) -> (batch,)."""
        y = tx
        for idx, (lin, bn) in enumerate(zip(self.linears[:-1], self.bns)):
            tmp = self.activation(lin(y))
            if self.batch_norm:
                tmp = bn(tmp)
            y = tmp if idx == 0 else tmp + y   # residual skip after layer 0
        return self.linears[-1](y).reshape(-1)
