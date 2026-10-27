"""Named test conditions for the seven experiments.

``family`` controls the episode seeds: conditions that share a family id use *identical* trajectories,
sensor noise and anomaly schedules and differ only in the factor under study (paired comparison).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List

from src.anomalies.injection import AnomalyConfig
from src.simulation.episode import EpisodeConfig


@dataclass
class Condition:
    name: str
    exp: str                       # experiment tag E1..E5
    family: int
    fn: Callable[[EpisodeConfig], None]
    desc: str = ""


def _loss(model, p, targeted=0.0, **extra):
    def f(c: EpisodeConfig):
        c.channel.loss_model, c.channel.loss_rate, c.channel.targeted_loss = model, p, targeted
        for k, v in extra.items():
            setattr(c, k, v)
    return f


def _kind(kind, p):
    def f(c: EpisodeConfig):
        c.anomaly.kind = kind
        c.channel.loss_rate = p
    return f


def _noise(s):
    def f(c: EpisodeConfig):
        c.sensors.noise_scale = s
    return f


def _gen(**kw):
    def f(c: EpisodeConfig):
        c.channel.loss_rate = 0.3
        for k, v in kw.items():
            setattr(c.swarm, k, v)
    return f


def build_conditions() -> List[Condition]:
    C: List[Condition] = []
    for p in (0, 10, 30, 50):
        C.append(Condition(f"iid_{p}", "E1" if p == 0 else "E2", 1, _loss("iid", p / 100), f"iid loss {p}%"))
    for p in (10, 30, 50):
        C.append(Condition(f"burst_{p}", "E3", 1, _loss("burst", p / 100), f"Gilbert-Elliott burst loss {p}% (mean burst 5)"))
    C.append(Condition("nodeburst_30", "E3", 1, _loss("node_burst", 0.3), "receiver-correlated burst loss 30%"))
    for p in (10, 30):
        C.append(Condition(f"targeted_{p}", "E4", 1, _loss("iid", p / 100, targeted=0.7),
                           f"iid {p}% + 70% extra loss on the links of anomalous UAVs"))
    for p in (0, 30):
        C.append(Condition(f"topo_{p}", "E4", 1, _loss("iid", p / 100, blockage_rate=6.0), f"link blockage events + iid {p}%"))
    for kind in ("sudden", "drift", "spoof"):
        for p in (0, 30):
            C.append(Condition(f"type_{kind}_{p}", "E4", 2, _kind(kind, p / 100), f"{kind} anomalies, iid loss {p}%"))
    for s in (1, 2, 3):
        C.append(Condition(f"noise_{s}", "E2", 3, _noise(float(s)), f"noise severity x{s}, no loss"))
    C.append(Condition("gen_n5", "E5", 4, _gen(n_uavs=5), "5 UAVs (train: 10), iid 30%"))
    C.append(Condition("gen_n20", "E5", 4, _gen(n_uavs=20), "20 UAVs (train: 10), iid 30%"))
    C.append(Condition("gen_lissajous", "E5", 4, _gen(trajectory="lissajous"), "unseen trajectory family, iid 30%"))
    C.append(Condition("gen_grid", "E5", 4, _gen(formation="grid"), "unseen grid formation, iid 30%"))
    C.append(Condition("gen_ref", "E5", 4, _gen(), "in-distribution reference for E5, iid 30%"))
    return C
