"""Position-anomaly injection into the *reported* position channel.

The anomaly offset is added to the (noisy) measured position to obtain the reported
position. IMU velocity and the relative-position sensors are left untouched: they
are the independent information that makes the anomaly observable at all.

Types
-----
sudden   step offset of fixed magnitude and random direction at onset.
drift    offset grows linearly (rate in m/step) from onset.
spoof    GPS-spoofing-like: a *group* of UAVs shares (almost) the same offset vector, ramped in
         smoothly over ``spoof_ramp`` steps, so within-group relative geometry stays consistent.
mixed    every anomalous UAV draws one of the three above.
none     no anomaly.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Tuple

import numpy as np

KINDS = ("none", "sudden", "drift", "spoof", "mixed")


@dataclass
class AnomalyConfig:
    kind: str = "mixed"
    n_anomalous: Tuple[int, int] = (1, 2)        # inclusive range of anomalous UAVs per episode
    p_anomaly_free: float = 0.0                  # probability that an episode contains no anomaly at all
    onset_frac: Tuple[float, float] = (0.25, 0.5)
    sudden_mag: Tuple[float, float] = (4.0, 12.0)    # [m]
    drift_rate: Tuple[float, float] = (0.2, 0.6)     # [m/step]
    spoof_mag: Tuple[float, float] = (6.0, 15.0)     # [m]
    spoof_ramp: int = 10                             # steps
    spoof_group: Tuple[int, int] = (1, 3)
    spoof_jitter: float = 0.3                        # [m] per-UAV deviation from the common spoof vector
    label_min_offset: float = 2.0                    # |offset| >= this => labelled anomalous [m]

    @classmethod
    def from_dict(cls, d: dict) -> "AnomalyConfig":
        d = dict(d)
        for k in ("n_anomalous", "onset_frac", "sudden_mag", "drift_rate", "spoof_mag", "spoof_group"):
            if k in d:
                d[k] = tuple(d[k])
        return cls(**d)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AnomalySchedule:
    offset: np.ndarray    # [T, N, 2] additive offset applied to the reported position
    active: np.ndarray    # [T, N] bool: injection currently active (offset != 0)
    label: np.ndarray     # [T, N] bool: active AND |offset| >= label_min_offset
    kind: np.ndarray      # [N] str array: type per UAV ('' for none)


def _unit(rng: np.random.Generator) -> np.ndarray:
    a = rng.uniform(0, 2 * np.pi)
    return np.array([np.cos(a), np.sin(a)])


def sample_anomalies(cfg: AnomalyConfig, T: int, N: int, rng: np.random.Generator) -> AnomalySchedule:
    offset = np.zeros((T, N, 2))
    kind = np.array([""] * N, dtype=object)
    if cfg.kind not in KINDS:
        raise ValueError(f"unknown anomaly kind {cfg.kind!r}")
    if cfg.kind != "none" and rng.random() >= cfg.p_anomaly_free:
        k = int(rng.integers(cfg.n_anomalous[0], cfg.n_anomalous[1] + 1))
        k = max(1, min(k, N))
        victims = list(rng.choice(N, size=k, replace=False))
        steps = np.arange(T)
        while victims:
            i = victims.pop(0)
            ki = cfg.kind if cfg.kind != "mixed" else str(rng.choice(["sudden", "drift", "spoof"]))
            onset = int(rng.uniform(*cfg.onset_frac) * T)
            ramp_to_end = np.clip(steps - onset, 0, None)
            if ki == "sudden":
                offset[:, i] = (steps >= onset)[:, None] * (rng.uniform(*cfg.sudden_mag) * _unit(rng))
                kind[i] = ki
            elif ki == "drift":
                offset[:, i] = ramp_to_end[:, None] * (rng.uniform(*cfg.drift_rate) * _unit(rng))
                kind[i] = ki
            else:  # spoof: pull additional group members from the remaining victims/other UAVs
                size = int(rng.integers(cfg.spoof_group[0], cfg.spoof_group[1] + 1))
                pool = [j for j in range(N) if j != i and kind[j] == ""]
                rng.shuffle(pool)
                members = [i] + pool[: max(0, size - 1)]
                victims = [v for v in victims if v not in members]
                vec = rng.uniform(*cfg.spoof_mag) * _unit(rng)
                ramp = np.clip(ramp_to_end / max(cfg.spoof_ramp, 1), 0.0, 1.0)
                for j in members:
                    offset[:, j] = ramp[:, None] * (vec + rng.normal(0, cfg.spoof_jitter, 2))
                    kind[j] = "spoof"
    active = np.linalg.norm(offset, axis=-1) > 0.0
    label = np.linalg.norm(offset, axis=-1) >= cfg.label_min_offset
    return AnomalySchedule(offset=offset, active=active, label=label, kind=kind)
