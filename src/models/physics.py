"""Non-learned physics-based consistency detectors (Baseline 1).

Two variants that differ ONLY in how they treat stale (lost-packet) data:

``physics_naive``  treats the last received report of a neighbour as if it were current.
``physics_aoi``    age-of-information-aware: motion-compensates the cached report with the neighbour's
                   IMU velocity and inflates the residual variance with the age (precision weighting).
                   This is the 'simple alternative' a reliability-aware GNN has to beat.

Both combine
 (i)  relative-position consistency: for UAV i the statistic  sum_j [w_ji e_ji - w_ij e_ij] / sqrt(W),
      where e_ij = (reported_j - reported_i) - measured_rel_ij; under 'only UAV i is displaced by o_i'
      its expectation is 2 w (o_i - mean o_j) and under no anomaly it has unit-variance noise;
 (ii) kinematic consistency: reported-position finite difference vs IMU velocity,
and smooth both with a causal exponential filter. Score = max of the two normalised statistics.

Nominal sensor specifications (gnss 1 m, relative 0.3 m, velocity 0.2 m/s, manoeuvre acceleration 0.6 m/s^2)
are fixed constants, not tuned on any evaluation split.
"""
from __future__ import annotations

import torch

REL_OVER_GNSS = 0.3     # nominal relative-sensor sigma / GNSS sigma
SIGMA_V = 0.2           # [m/s]
SIGMA_ACC = 0.6         # [m/s^2] unmodelled acceleration over the age interval


def _ema(x: torch.Tensor, lam: float) -> torch.Tensor:
    """Causal EMA along dim 1, rescaled so unit-variance white input stays unit variance."""
    out = torch.zeros_like(x)
    prev = torch.zeros_like(x[:, 0])
    for t in range(x.shape[1]):
        prev = lam * prev + (1 - lam) * x[:, t]
        out[:, t] = prev
    return out * ((1 + lam) / (1 - lam)) ** 0.5


@torch.no_grad()
def physics_scores(b: dict, aoi_aware: bool, lam_rel: float = 0.7, lam_kin: float = 0.8) -> torch.Tensor:
    node_x, valid, age = b["node_x"], b["valid"], b["age"]
    dt = float(b["dt"])
    sig_ratio = node_x[..., 4]                                   # self-reported sigma / nominal sigma
    # normalised unit: nominal GNSS sigma = 1 (all quantities below in units of nominal sigma_g * meters)
    sg = sig_ratio                                               # [B,T,N]  (sigma_g,i / sigma_nominal)
    # residual variance (in meters^2 for sigma_nominal = 1 m, which is the default sensor config)
    var = sg.unsqueeze(-1) ** 2 + sg.unsqueeze(-2) ** 2 + (REL_OVER_GNSS * sg.unsqueeze(-1)) ** 2   # [B,T,N,N]
    if aoi_aware:
        a = age * dt
        var = var + (a * SIGMA_V) ** 2 + (0.5 * SIGMA_ACC * a ** 2) ** 2
        e = b["resc_m"]
    else:
        e = b["res_m"]
    w = valid / var                                              # receiver-centric precision weights
    num_in = (w.unsqueeze(-1) * e).sum(3)                        # sum_j w_ij e_ij        [B,T,N,2]
    wT = w.transpose(2, 3)
    eT = e.transpose(2, 3)
    num_out = (wT.unsqueeze(-1) * eT).sum(3)                     # sum_j w_ji e_ji
    W = w.sum(-1) + wT.sum(-1)
    u = (num_out - num_in) / W.clamp(min=1e-6).sqrt().unsqueeze(-1)
    u = torch.where(W.unsqueeze(-1) > 0, u, torch.zeros_like(u))
    z_rel = _ema(u, lam_rel).norm(dim=-1)

    sig_k = (2 * sg ** 2 / dt ** 2 + SIGMA_V ** 2).sqrt()
    uk = b["kin_m"] / sig_k.unsqueeze(-1)
    z_kin = _ema(uk, lam_kin).norm(dim=-1)
    return torch.maximum(z_rel, z_kin)                           # [B,T,N]
