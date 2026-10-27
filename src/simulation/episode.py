"""Episode generation: truth + sensing + anomalies + communication, with strict separation of
*real*, *measured* and *reported* states and of simulator-only labels.

Definitions (all arrays are [T, ...]; pair arrays are indexed [t, receiver, sender])
------------------------------------------------------------------------------------
real state       ``true_pos`` / ``true_vel``        simulator ground truth, never a model input
measured state   ``meas_pos``                       onboard GNSS-like estimate = real + white noise
reported state   ``rep_pos``                        measured + anomaly offset; what a UAV broadcasts
                                                    and uses as its own position estimate
IMU velocity     ``vel_meas``                       real velocity + noise (independent of the position channel)
relative sensing ``rel_meas[t, r, s]``              r's own noisy measurement of (pos_s - pos_r), available
                                                    iff the pair is in range and not blocked (``adj``)
delivery         ``delivered[t, r, s]``             r received s's packet at step t (only if ``adj``)

Only :class:`Observation` (see :meth:`Episode.observable`) may be used to build model inputs.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Optional

import numpy as np

from src.anomalies.injection import AnomalyConfig, AnomalySchedule, sample_anomalies
from src.communication.channel import ChannelConfig, apply_targeted_loss, sample_lost
from src.simulation.swarm import SwarmConfig, simulate_truth


@dataclass
class SensorConfig:
    gnss_sigma: float = 1.0        # [m] white noise of the onboard position estimate
    rel_sigma: float = 0.3         # [m] relative-position sensor noise (UWB / vision-like)
    vel_sigma: float = 0.2         # [m/s] IMU/odometry velocity noise
    noise_scale: float = 1.0       # multiplies gnss_sigma and rel_sigma ('noise severity')

    @classmethod
    def from_dict(cls, d: dict) -> "SensorConfig":
        return cls(**d)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class EpisodeConfig:
    swarm: SwarmConfig = field(default_factory=SwarmConfig)
    sensors: SensorConfig = field(default_factory=SensorConfig)
    anomaly: AnomalyConfig = field(default_factory=AnomalyConfig)
    channel: ChannelConfig = field(default_factory=ChannelConfig)
    blockage_rate: float = 0.0     # expected link-blockage events per episode per 10 UAVs (topology changes)

    @classmethod
    def from_dict(cls, d: dict) -> "EpisodeConfig":
        return cls(
            swarm=SwarmConfig.from_dict(d.get("swarm", {})),
            sensors=SensorConfig.from_dict(d.get("sensors", {})),
            anomaly=AnomalyConfig.from_dict(d.get("anomaly", {})),
            channel=ChannelConfig.from_dict(d.get("channel", {})),
            blockage_rate=d.get("blockage_rate", 0.0),
        )

    def to_dict(self) -> dict:
        return {"swarm": self.swarm.to_dict(), "sensors": self.sensors.to_dict(),
                "anomaly": self.anomaly.to_dict(), "channel": self.channel.to_dict(),
                "blockage_rate": self.blockage_rate}


@dataclass
class Observation:
    """Everything a detector is allowed to see. No ground truth, no labels, no true positions."""
    rep_pos: np.ndarray     # [T, N, 2]
    vel_meas: np.ndarray    # [T, N, 2]
    sigma_rep: np.ndarray   # [T, N]    self-reported position accuracy
    adj: np.ndarray         # [T, N, N] bool, relative-sensing / hello-beacon neighbourhood (symmetric)
    rel_meas: np.ndarray    # [T, N, N, 2]
    link_q: np.ndarray      # [T, N, N] RSSI-like link-quality proxy
    delivered: np.ndarray   # [T, N, N] bool, [t, receiver, sender]
    dt: float
    comm_range: float
    gnss_sigma_nominal: float


@dataclass
class Episode:
    cfg: EpisodeConfig
    seed: int
    # --- simulator ground truth (hidden from models) ---
    true_pos: np.ndarray
    true_vel: np.ndarray
    meas_pos: np.ndarray
    schedule: AnomalySchedule
    comm_fail: np.ndarray            # [T, N, N] in-range packets that were lost (receiver, sender)
    # --- observable channel ---
    obs: Observation

    @property
    def rep_pos(self) -> np.ndarray:
        return self.obs.rep_pos

    @property
    def labels(self) -> np.ndarray:
        return self.schedule.label

    @property
    def active(self) -> np.ndarray:
        return self.schedule.active

    def observable(self) -> Observation:
        return self.obs


def _blockage(T: int, N: int, rate: float, rng: np.random.Generator) -> np.ndarray:
    """[T, N, N] bool, True = pair blocked (symmetric)."""
    blocked = np.zeros((T, N, N), dtype=bool)
    if rate <= 0:
        return blocked
    n_events = rng.poisson(rate * N / 10.0)
    for _ in range(n_events):
        i, j = rng.choice(N, size=2, replace=False)
        t0 = int(rng.integers(0, T))
        dur = int(rng.integers(5, 26))
        blocked[t0:t0 + dur, i, j] = True
        blocked[t0:t0 + dur, j, i] = True
    return blocked


def generate_episode(cfg: EpisodeConfig, seed: int) -> Episode:
    """Deterministic given (cfg, seed). Independent RNG streams make episodes with the same
    seed share trajectory, sensor noise and anomaly schedule when only the channel changes."""
    ss = np.random.SeedSequence(seed)
    r_traj, r_sens, r_anom, r_chan, r_topo = (np.random.default_rng(s) for s in ss.spawn(5))
    sw, se = cfg.swarm, cfg.sensors
    T, N = sw.n_steps, sw.n_uavs

    truth = simulate_truth(sw, r_traj)
    sched = sample_anomalies(cfg.anomaly, T, N, r_anom)

    s = se.noise_scale
    meas_pos = truth.pos + r_sens.normal(0, se.gnss_sigma * s, truth.pos.shape)
    rep_pos = meas_pos + sched.offset
    vel_meas = truth.vel + r_sens.normal(0, se.vel_sigma, truth.vel.shape)
    sigma_rep = np.abs(se.gnss_sigma * s * (1.0 + 0.1 * r_sens.standard_normal((T, N))))

    diff = truth.pos[:, None, :, :] - truth.pos[:, :, None, :]          # [t, r, s] = p_s - p_r
    dist = np.linalg.norm(diff, axis=-1)
    eye = np.eye(N, dtype=bool)[None]
    blocked = _blockage(T, N, cfg.blockage_rate, r_topo)
    adj = (dist <= sw.comm_range) & ~eye & ~blocked
    rel_meas = diff + r_sens.normal(0, se.rel_sigma * s, diff.shape)
    rel_meas = np.where(adj[..., None], rel_meas, 0.0)
    link_q = np.clip(1.0 - dist / sw.comm_range + r_sens.normal(0, 0.05, dist.shape), 0.0, 1.2)
    link_q = np.where(adj, link_q, 0.0)

    lost = sample_lost(cfg.channel, T, N, r_chan)
    lost = apply_targeted_loss(lost, sched.active, cfg.channel.targeted_loss, r_chan)
    delivered = adj & ~lost
    comm_fail = adj & lost

    obs = Observation(rep_pos=rep_pos, vel_meas=vel_meas, sigma_rep=sigma_rep, adj=adj, rel_meas=rel_meas,
                      link_q=link_q, delivered=delivered, dt=sw.dt, comm_range=sw.comm_range,
                      gnss_sigma_nominal=se.gnss_sigma)
    return Episode(cfg=cfg, seed=seed, true_pos=truth.pos, true_vel=truth.vel, meas_pos=meas_pos,
                   schedule=sched, comm_fail=comm_fail, obs=obs)
