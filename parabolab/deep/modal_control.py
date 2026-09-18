"""Training and fixed post-hoc latent controls for the exact heat pilot."""

from __future__ import annotations

import copy
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
import torch

from .modal_data import HeatBatch, evaluate_coeffs, perturb_output_mode, project_coeffs


def _q_tensor(grid, batch_size: int, device: str):
    x = torch.as_tensor(grid, dtype=torch.float32, device=device)
    return torch.stack([torch.zeros_like(x), x], dim=-1).expand(batch_size, -1, -1)


def _cond(batch_size: int, device: str):
    return torch.empty(batch_size, 0, dtype=torch.float32, device=device)


def encode_batch(net, batch: HeatBatch, *, device: str = "cpu"):
    phi = torch.as_tensor(batch.phi, dtype=torch.float32, device=device)
    return net.encode(phi, _cond(len(phi), device))


@torch.no_grad()
def predict_batch(net, batch: HeatBatch, *, device: str = "cpu") -> np.ndarray:
    net = net.to(device).eval()
    state = encode_batch(net, batch, device=device)
    out = net.decode(state, _q_tensor(batch.query_grid, len(batch.phi), device))
    return out.cpu().numpy()


def fit_exact_scalers(net, train: HeatBatch) -> None:
    """Fill corpus-level buffers used by DeepONet (attention is per sample)."""
    with torch.no_grad():
        if hasattr(net, "phi_scale"):
            net.phi_scale.fill_(float(train.phi.std()) or 1.0)
        if hasattr(net, "in_mean"):
            net.in_mean.copy_(torch.tensor([0.0, float(train.query_grid.mean())]))
            net.in_std.copy_(torch.tensor([1.0, float(train.query_grid.std()) or 1.0]))
        if hasattr(net, "out_mean"):
            net.out_mean.fill_(float(train.u.mean()))
            net.out_std.fill_(float(train.u.std()) or 1.0)


@dataclass
class ExactTrainResult:
    train_loss: list[float]
    validation_loss: list[float]


def train_exact_operator(net, train: HeatBatch, validation: HeatBatch, *,
                         steps: int = 20_000, batch_size: int = 32,
                         n_query: int = 64, lr: float = 1e-3,
                         check_every: int = 100, device: str = "cpu",
                         seed: int = 0) -> ExactTrainResult:
    """Train on exact u(0,x); keep the checkpoint with lowest validation MSE."""
    fit_exact_scalers(net, train)
    net = net.to(device).train()
    phi = torch.as_tensor(train.phi, dtype=torch.float32, device=device)
    u = torch.as_tensor(train.u, dtype=torch.float32, device=device)
    q_all = _q_tensor(train.query_grid, len(train.phi), device)
    scale = float(train.u.std()) or 1.0
    rng = np.random.default_rng(seed)
    torch.manual_seed(seed)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=max(steps, 1))
    train_loss, validation_loss = [], []
    best_loss, best_state = float("inf"), None

    for step in range(steps):
        bi = rng.choice(len(train.phi), min(batch_size, len(train.phi)), replace=False)
        qi = rng.choice(len(train.query_grid), min(n_query, len(train.query_grid)), replace=False)
        bi_t = torch.as_tensor(bi, device=device)
        qi_t = torch.as_tensor(qi, device=device)
        pred = net(phi[bi_t], _cond(len(bi), device), q_all[bi_t][:, qi_t])
        loss = torch.mean(((pred - u[bi_t][:, qi_t]) / scale) ** 2)
        if not torch.isfinite(loss):
            raise RuntimeError(f"non-finite exact heat loss at step {step}")
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
        opt.step()
        sched.step()
        train_loss.append(float(loss.detach()))

        if step % check_every == 0 or step == steps - 1:
            val_pred = predict_batch(net, validation, device=device)
            val_loss = float(np.mean(((val_pred - validation.u) / scale) ** 2))
            validation_loss.append(val_loss)
            if val_loss < best_loss:
                best_loss = val_loss
                best_state = copy.deepcopy(net.state_dict())
            net.train()

    if best_state is not None:
        net.load_state_dict(best_state)
    net.eval()
    return ExactTrainResult(train_loss, validation_loss)


@dataclass
class ModalController:
    latent_shape: tuple[int, ...]
    mean: np.ndarray
    components: np.ndarray
    readout: np.ndarray
    intercept: np.ndarray
    directions: np.ndarray
    ridge: float
    calibration_delta: float

    def _arrays(self, state):
        latent = state.latent.reshape(state.latent.shape[0], -1)
        device, dtype = latent.device, latent.dtype
        mean = torch.as_tensor(self.mean, device=device, dtype=dtype)
        components = torch.as_tensor(self.components, device=device, dtype=dtype)
        readout = torch.as_tensor(self.readout, device=device, dtype=dtype)
        intercept = torch.as_tensor(self.intercept, device=device, dtype=dtype)
        return latent, mean, components, readout, intercept

    def predict(self, state) -> torch.Tensor:
        latent, mean, components, readout, intercept = self._arrays(state)
        normalized = (latent - mean) @ components.T
        coefficients = normalized @ readout + intercept
        return coefficients * state.physical_scale

    def edit(self, state, mode: int, *, alpha: float):
        if not 0 <= mode < len(self.directions):
            raise IndexError(f"mode {mode} outside controller")
        prediction = self.predict(state)
        delta = (alpha - 1.0) * prediction[:, mode]
        scale = state.physical_scale[:, 0]
        if torch.any(scale <= 1e-8):
            raise ValueError("latent edit requires physical_scale > 1e-8")
        direction = torch.as_tensor(
            self.directions[mode], device=state.latent.device,
            dtype=state.latent.dtype).reshape((1,) + self.latent_shape)
        view = (len(delta),) + (1,) * len(self.latent_shape)
        edited = state.latent + (delta / scale).reshape(view) * direction
        return state.with_latent(edited), delta

    def save(self, path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        np.savez(
            path, latent_shape=np.asarray(self.latent_shape), mean=self.mean,
            components=self.components, readout=self.readout,
            intercept=self.intercept, directions=self.directions,
            ridge=self.ridge, calibration_delta=self.calibration_delta)


@torch.no_grad()
def fit_modal_controller(net, calibration: HeatBatch, *, pca_dim: int = 32,
                         ridge: float = 1e-4, calibration_delta: float = 0.05,
                         device: str = "cpu") -> ModalController:
    """Fit a supervised, fixed modal controller after network training."""
    net = net.to(device).eval()
    base = encode_batch(net, calibration, device=device)
    latent = base.latent.detach().cpu().numpy()
    latent_shape = latent.shape[1:]
    flat = latent.reshape(len(latent), -1)
    scale = base.physical_scale.detach().cpu().numpy()
    mean = flat.mean(axis=0)
    centered = flat - mean
    _, _, vt = np.linalg.svd(centered, full_matrices=False)
    rank = max(1, min(pca_dim, len(vt), len(flat) - 1, flat.shape[1]))
    components = vt[:rank]
    features = centered @ components.T
    design = np.column_stack([features, np.ones(len(features))])
    penalty = ridge * np.eye(design.shape[1])
    penalty[-1, -1] = 0.0
    target = calibration.output_coeffs / scale
    weights = np.linalg.solve(design.T @ design + penalty, design.T @ target)

    q = _q_tensor(calibration.query_grid, len(calibration.phi), device)
    base_output = net.decode(base, q)
    responses = []
    for component in components:
        direction = torch.as_tensor(
            component.reshape(latent_shape), dtype=base.latent.dtype,
            device=base.latent.device)
        view = (len(scale),) + (1,) * len(latent_shape)
        physical_scale = base.physical_scale[:, 0]
        shifted = base.latent + (calibration_delta / physical_scale).reshape(view) * direction
        response = (net.decode(base.with_latent(shifted), q) - base_output) / calibration_delta
        responses.append(response.cpu().numpy())
    response_matrix = np.stack(responses, axis=-1).reshape(-1, rank)
    gram = response_matrix.T @ response_matrix + ridge * np.eye(rank)
    basis = evaluate_coeffs(
        np.eye(calibration.n_modes), calibration.query_grid,
        x_lo=calibration.x_lo, x_hi=calibration.x_hi)
    directions = []
    for mode in range(calibration.n_modes):
        target = np.tile(basis[mode], len(calibration.phi))
        coordinates = np.linalg.solve(gram, response_matrix.T @ target)
        directions.append((coordinates @ components).reshape(latent_shape))

    return ModalController(
        tuple(latent_shape), mean, components, weights[:-1], weights[-1],
        np.asarray(directions), ridge, calibration_delta)


@torch.no_grad()
def random_direction_controller(net, controller: ModalController,
                                calibration: HeatBatch, *, seed: int = 0,
                                device: str = "cpu") -> ModalController:
    """Norm-match random PCA-subspace directions to learned output effects."""
    net = net.to(device).eval()
    state = encode_batch(net, calibration, device=device)
    q = _q_tensor(calibration.query_grid, len(calibration.phi), device)
    base = net.decode(state, q)
    rng = np.random.default_rng(seed)
    random_directions = []
    scale = state.physical_scale[:, 0]
    view = (len(scale),) + (1,) * len(controller.latent_shape)

    for learned in controller.directions:
        coordinates = rng.normal(size=len(controller.components))
        random = coordinates @ controller.components
        random /= max(float(np.linalg.norm(random)), 1e-12)
        random *= max(float(np.linalg.norm(learned)), 1e-12)

        def response_norm(direction):
            direction_t = torch.as_tensor(
                direction.reshape(controller.latent_shape),
                dtype=state.latent.dtype, device=state.latent.device)
            shifted = state.latent + (
                controller.calibration_delta / scale).reshape(view) * direction_t
            response = net.decode(state.with_latent(shifted), q) - base
            return float(torch.sqrt(torch.mean(response ** 2)))

        learned_norm = response_norm(learned)
        random_norm = response_norm(random)
        if random_norm > 1e-12:
            random *= learned_norm / random_norm
        random_directions.append(random.reshape(controller.latent_shape))
    return replace(controller, directions=np.asarray(random_directions))


def _relative_rms(error, target) -> float:
    denominator = max(float(np.mean(np.asarray(target) ** 2)), 1e-16)
    return float(np.sqrt(np.mean(np.asarray(error) ** 2) / denominator))


@torch.no_grad()
def evaluate_modal_controller(net, controller: ModalController, batch: HeatBatch,
                              *, alphas=(0.0, 0.5, 1.5, 2.0),
                              device: str = "cpu") -> list[dict]:
    """Evaluate decode-before prediction, actual edit, leakage and re-encode control."""
    net = net.to(device).eval()
    state = encode_batch(net, batch, device=device)
    q = _q_tensor(batch.query_grid, len(batch.phi), device)
    base = net.decode(state, q).cpu().numpy()
    readout = controller.predict(state).cpu().numpy()
    basis = evaluate_coeffs(np.eye(batch.n_modes), batch.query_grid,
                            x_lo=batch.x_lo, x_hi=batch.x_hi)
    rows = []
    solve_rel = _relative_rms(base - batch.u, batch.u)
    readout_rel = _relative_rms(readout - batch.output_coeffs, batch.output_coeffs)

    for mode in range(batch.n_modes):
        for alpha in alphas:
            if alpha == 1.0:
                continue
            edited_state, delta_pred_t = controller.edit(state, mode, alpha=alpha)
            edited = net.decode(edited_state, q).cpu().numpy()
            observed = edited - base
            delta_pred = delta_pred_t.cpu().numpy()
            delta_true = (alpha - 1.0) * batch.output_coeffs[:, mode]
            predicted_field = delta_pred[:, None] * basis[mode]
            target_field = delta_true[:, None] * basis[mode]
            observed_coeffs = project_coeffs(
                observed, batch.query_grid, batch.K,
                x_lo=batch.x_lo, x_hi=batch.x_hi)
            target_component = observed_coeffs[:, mode, None] * basis[mode]
            true_changed = perturb_output_mode(batch, mode, delta_true)
            reencoded = predict_batch(net, true_changed, device=device)
            rows.append({
                "mode": mode,
                "alpha": float(alpha),
                "solve_rel_rms": solve_rel,
                "readout_rel_rms": readout_rel,
                "prediction_rel_rms": _relative_rms(observed - predicted_field, predicted_field),
                "control_rel_rms": _relative_rms(
                    observed_coeffs[:, mode] - delta_true, delta_true),
                "leakage_rel_rms": _relative_rms(observed - target_component, target_field),
                "edited_rel_rms": _relative_rms(edited - (batch.u + target_field), batch.u + target_field),
                "reencode_rel_rms": _relative_rms(reencoded - true_changed.u, true_changed.u),
            })
    return rows
