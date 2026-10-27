"""Packet-loss processes for directed UAV-to-UAV links.

``delivered[t, r, s]`` is True when receiver ``r`` gets sender ``s``'s packet at
step ``t``. Loss models:

* ``iid``        independent Bernoulli loss with probability ``loss_rate``.
* ``burst``      per-link two-state Gilbert-Elliott chain (Gilbert 1960, Elliott 1963),
                 good state = no loss, bad state = loss, mean burst length
                 ``mean_burst`` steps, stationary loss probability ``loss_rate``.
* ``node_burst`` as ``burst`` but one chain per *receiver*, so all incoming
                 links of a receiver fail together (spatially correlated loss).

The ground-truth communication-failure mask is kept separate from anomaly labels.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np

LOSS_MODELS = ("iid", "burst", "node_burst")


@dataclass
class ChannelConfig:
    loss_model: str = "iid"
    loss_rate: float = 0.0
    mean_burst: float = 5.0          # mean bad-state sojourn [steps] for burst models
    targeted_loss: float = 0.0       # extra loss prob. on outgoing links of nodes with an active anomaly

    @classmethod
    def from_dict(cls, d: dict) -> "ChannelConfig":
        return cls(**d)

    def to_dict(self) -> dict:
        return asdict(self)


def gilbert_elliott_params(loss_rate: float, mean_burst: float) -> tuple[float, float]:
    """Return (p_gb, p_bg) so that the stationary bad-state probability equals ``loss_rate``."""
    if not 0.0 <= loss_rate < 1.0:
        raise ValueError("loss_rate must be in [0, 1)")
    p_bg = 1.0 / max(mean_burst, 1.0)
    p_gb = p_bg * loss_rate / (1.0 - loss_rate)
    return min(p_gb, 1.0), p_bg


def _ge_chain(shape: tuple[int, ...], T: int, loss_rate: float, mean_burst: float,
              rng: np.random.Generator) -> np.ndarray:
    """Boolean ``lost`` array of shape [T, *shape] following independent Gilbert-Elliott chains."""
    p_gb, p_bg = gilbert_elliott_params(loss_rate, mean_burst)
    bad = rng.random(shape) < loss_rate          # stationary initial state
    out = np.zeros((T,) + shape, dtype=bool)
    for t in range(T):
        out[t] = bad
        u = rng.random(shape)
        bad = np.where(bad, u >= p_bg, u < p_gb)
    return out


def sample_lost(cfg: ChannelConfig, T: int, n: int, rng: np.random.Generator) -> np.ndarray:
    """Background packet-loss mask ``lost[t, r, s]`` (True = packet lost)."""
    if cfg.loss_rate <= 0.0:
        return np.zeros((T, n, n), dtype=bool)
    if cfg.loss_model == "iid":
        return rng.random((T, n, n)) < cfg.loss_rate
    if cfg.loss_model == "burst":
        return _ge_chain((n, n), T, cfg.loss_rate, cfg.mean_burst, rng)
    if cfg.loss_model == "node_burst":
        per_recv = _ge_chain((n,), T, cfg.loss_rate, cfg.mean_burst, rng)    # [T, n]
        return np.broadcast_to(per_recv[:, :, None], (T, n, n)).copy()
    raise ValueError(f"unknown loss model {cfg.loss_model!r}")


def apply_targeted_loss(lost: np.ndarray, anomaly_active: np.ndarray, targeted_loss: float,
                        rng: np.random.Generator) -> np.ndarray:
    """Additional iid loss on the outgoing links of senders whose position report is currently anomalous.

    ``anomaly_active`` is [T, N] (sender axis). This models an adversary that also degrades the
    link of the node it manipulates, i.e. the confounded 'anomaly + communication failure' case.
    """
    if targeted_loss <= 0.0:
        return lost
    extra = rng.random(lost.shape) < targeted_loss
    return lost | (extra & anomaly_active[:, None, :])
