"""Lightweight 2-D UAV swarm ground-truth dynamics.

Each UAV tracks a slot in a moving formation with a critically damped PD law
(double-integrator, bounded acceleration, random wind acceleration). This is a
deliberately simple model: no aerodynamics, no collision avoidance, no 3-D.
Only the *true* state is produced here; sensing, anomalies and communication
are layered on top in separate modules.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Tuple

import numpy as np

TRAJECTORIES = ("random_turn", "circle", "lissajous")
FORMATIONS = ("circle", "line", "wedge", "grid")


@dataclass
class SwarmConfig:
    n_uavs: int = 10
    n_steps: int = 100
    dt: float = 0.5                      # seconds per step
    trajectory: str = "random_turn"      # leader reference trajectory family
    formation: str = "circle"
    spacing: float = 12.0                # nominal inter-slot spacing [m]
    breathing: float = 0.35              # relative amplitude of formation scale oscillation
    leader_speed: Tuple[float, float] = (3.0, 7.0)   # [m/s]
    kp: float = 1.2
    kd: float = 2.0
    a_max: float = 4.0                   # acceleration bound [m/s^2]
    wind_std: float = 0.3                # std of random acceleration disturbance [m/s^2]
    comm_range: float = 30.0             # communication AND relative-sensing range [m]

    @classmethod
    def from_dict(cls, d: dict) -> "SwarmConfig":
        d = dict(d)
        if "leader_speed" in d:
            d["leader_speed"] = tuple(d["leader_speed"])
        return cls(**d)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TrueState:
    pos: np.ndarray      # [T, N, 2] real positions
    vel: np.ndarray      # [T, N, 2] real velocities
    des_pos: np.ndarray  # [T, N, 2] formation slot positions (reference)


def _leader(cfg: SwarmConfig, rng: np.random.Generator) -> np.ndarray:
    """Leader (formation centre) trajectory, shape [T, 2]."""
    T, dt = cfg.n_steps, cfg.dt
    t = np.arange(T) * dt
    speed = rng.uniform(*cfg.leader_speed)
    if cfg.trajectory == "random_turn":
        theta = rng.uniform(0, 2 * np.pi)
        omega, c = 0.0, np.zeros((T, 2))
        for k in range(1, T):
            omega += -omega * dt / 8.0 + 0.06 * np.sqrt(dt) * rng.standard_normal()
            omega = float(np.clip(omega, -0.12, 0.12))   # bounded turn rate [rad/s]
            theta += omega * dt
            c[k] = c[k - 1] + speed * dt * np.array([np.cos(theta), np.sin(theta)])
        return c
    if cfg.trajectory == "circle":
        r = rng.uniform(40, 80)
        w = rng.choice([-1, 1]) * speed / r
        phi = rng.uniform(0, 2 * np.pi)
        return np.stack([r * np.cos(w * t + phi), r * np.sin(w * t + phi)], -1)
    if cfg.trajectory == "lissajous":  # never used for training: unseen-trajectory test
        a, b = rng.uniform(50, 80), rng.uniform(40, 70)
        w1 = speed / (1.6 * a)
        w2 = w1 * rng.uniform(1.1, 1.5)
        p1, p2 = rng.uniform(0, 2 * np.pi, 2)
        return np.stack([a * np.sin(w1 * t + p1), b * np.sin(w2 * t + p2)], -1)
    raise ValueError(f"unknown trajectory {cfg.trajectory!r}")


def formation_offsets(cfg: SwarmConfig, rng: np.random.Generator) -> np.ndarray:
    """Slot offsets in the leader frame (x forward, y left), shape [N, 2]."""
    n, s = cfg.n_uavs, cfg.spacing
    i = np.arange(n)
    if cfg.formation == "circle":
        radius = s / (2 * np.sin(np.pi / max(n, 3)))
        ang = 2 * np.pi * i / n
        off = np.stack([radius * np.cos(ang), radius * np.sin(ang)], -1)
    elif cfg.formation == "line":
        off = np.stack([np.zeros(n), (i - (n - 1) / 2) * s], -1)
    elif cfg.formation == "wedge":
        side = np.where(i % 2 == 0, 1.0, -1.0)
        rank = np.ceil(i / 2.0)
        off = np.stack([-0.8 * s * rank, 0.8 * s * rank * side], -1)
    elif cfg.formation == "grid":  # never used for training: unseen-formation test
        cols = int(np.ceil(np.sqrt(n)))
        off = np.stack([-(i // cols) * s, ((i % cols) - (cols - 1) / 2) * s], -1)
    else:
        raise ValueError(f"unknown formation {cfg.formation!r}")
    off = off - off.mean(0)
    return off + rng.normal(0, 0.08 * s, off.shape)


def simulate_truth(cfg: SwarmConfig, rng: np.random.Generator) -> TrueState:
    T, N, dt = cfg.n_steps, cfg.n_uavs, cfg.dt
    c = _leader(cfg, rng)
    vel_c = np.gradient(c, dt, axis=0)
    heading = np.unwrap(np.arctan2(vel_c[:, 1], vel_c[:, 0]))
    k = 8  # smoothing of the formation orientation
    heading = np.convolve(np.pad(heading, (k, k), mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), "valid")
    t = np.arange(T) * dt
    scale = 1.0 + cfg.breathing * np.sin(2 * np.pi * t / rng.uniform(20, 40) + rng.uniform(0, 2 * np.pi))
    off = formation_offsets(cfg, rng)

    cos, sin = np.cos(heading), np.sin(heading)
    rot = np.stack([np.stack([cos, -sin], -1), np.stack([sin, cos], -1)], -2)       # [T,2,2]
    des = c[:, None, :] + scale[:, None, None] * np.einsum("tab,nb->tna", rot, off)  # [T,N,2]
    des_vel = np.gradient(des, dt, axis=0)

    pos = np.zeros((T, N, 2))
    vel = np.zeros((T, N, 2))
    pos[0] = des[0] + rng.normal(0, 2.0, (N, 2))
    vel[0] = des_vel[0] + rng.normal(0, 0.3, (N, 2))
    for k in range(T - 1):
        a = cfg.kp * (des[k] - pos[k]) + cfg.kd * (des_vel[k] - vel[k])
        norm = np.linalg.norm(a, axis=-1, keepdims=True)
        a = a * np.minimum(1.0, cfg.a_max / np.maximum(norm, 1e-9))
        a = a + rng.normal(0, cfg.wind_std, a.shape)
        vel[k + 1] = vel[k] + a * dt
        pos[k + 1] = pos[k] + vel[k + 1] * dt
    return TrueState(pos=pos, vel=vel, des_pos=des)
