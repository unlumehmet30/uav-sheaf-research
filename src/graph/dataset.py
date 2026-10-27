"""Dataset generation: lists of episode configs -> stacked tensors (episode-level splits).

Splits are separated by *episode seeds* drawn from disjoint integer ranges, so no episode,
trajectory or time window appears in more than one split.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Sequence

import numpy as np
import torch

from src.graph.features import build_features
from src.simulation.episode import EpisodeConfig, generate_episode

# disjoint seed ranges: seed = base(split) + 100_000 * experiment_seed + episode_index
SPLIT_BASE = {"train": 1_000_000, "val": 2_000_000, "test": 3_000_000, "tune": 4_000_000}


def episode_seed(split: str, experiment_seed: int, index: int, cond_id: int = 0) -> int:
    return SPLIT_BASE[split] + 100_000 * experiment_seed + 1_000 * cond_id + index


@dataclass
class Batch:
    """Stacked episodes [E, T, ...]; numpy -> torch conversion is explicit."""
    tensors: Dict[str, torch.Tensor]
    labels: torch.Tensor           # [E,T,N] bool
    eval_mask: torch.Tensor        # [E,T,N] bool: False for 'ambiguous' (injection active but below label threshold)
    kinds: List[np.ndarray]        # per episode: anomaly kind per UAV
    meta: List[dict]

    def __len__(self) -> int:
        return self.labels.shape[0]

    def index(self, idx) -> "Batch":
        idx = torch.as_tensor(idx)
        return Batch({k: v[idx] for k, v in self.tensors.items()}, self.labels[idx], self.eval_mask[idx],
                     [self.kinds[i] for i in idx.tolist()], [self.meta[i] for i in idx.tolist()])


_TENSOR_KEYS = ["node_x", "edge_x", "adj", "valid", "delivered", "tidx", "res_m", "resc_m", "age", "kin_m"]


def build_batch(cfgs: Sequence[EpisodeConfig], seeds: Sequence[int]) -> Batch:
    feats: List[Dict[str, np.ndarray]] = []
    labels, masks, kinds, meta = [], [], [], []
    for cfg, seed in zip(cfgs, seeds):
        ep = generate_episode(cfg, int(seed))
        feats.append(build_features(ep.observable()))
        labels.append(ep.labels)
        masks.append(~(ep.active & ~ep.labels))
        kinds.append(ep.schedule.kind)
        meta.append({"seed": int(seed), "n_uavs": cfg.swarm.n_uavs, "dt": cfg.swarm.dt})
    tens = {}
    for k in _TENSOR_KEYS:
        arr = np.stack([f[k] for f in feats])
        tens[k] = torch.from_numpy(arr).long() if k == "tidx" else torch.from_numpy(arr).float()
    tens["dt"] = torch.tensor(float(feats[0]["dt"]))
    return Batch(tens, torch.from_numpy(np.stack(labels)), torch.from_numpy(np.stack(masks)), kinds, meta)


# --------------------------------------------------------------------------------------
# Training distribution (a mixture over conditions) and test conditions
# --------------------------------------------------------------------------------------
def sample_train_config(base: EpisodeConfig, rng: np.random.Generator) -> EpisodeConfig:
    """Draw one training-episode config from the training mixture (seen conditions only)."""
    cfg = copy.deepcopy(base)
    cfg.swarm.trajectory = str(rng.choice(["random_turn", "circle"]))
    cfg.swarm.formation = str(rng.choice(["circle", "line", "wedge"]))
    cfg.sensors.noise_scale = float(rng.choice([1.0, 1.5, 2.0]))
    cfg.channel.loss_rate = float(rng.choice([0.0, 0.1, 0.3, 0.5]))
    cfg.channel.loss_model = str(rng.choice(["iid", "burst", "node_burst"])) if cfg.channel.loss_rate > 0 else "iid"
    cfg.channel.targeted_loss = float(rng.choice([0.0, 0.0, 0.7]))
    cfg.blockage_rate = float(rng.choice([0.0, 0.0, 3.0]))
    cfg.anomaly.kind = str(rng.choice(["mixed", "sudden", "drift", "spoof"], p=[0.4, 0.2, 0.2, 0.2]))
    cfg.anomaly.p_anomaly_free = 0.25
    return cfg


def make_split(base: EpisodeConfig, split: str, experiment_seed: int, n_episodes: int) -> Batch:
    rng = np.random.default_rng(episode_seed(split, experiment_seed, 999))
    cfgs = [sample_train_config(base, rng) for _ in range(n_episodes)]
    seeds = [episode_seed(split, experiment_seed, i) for i in range(n_episodes)]
    return build_batch(cfgs, seeds)


def make_condition_set(base: EpisodeConfig, overrides: Callable[[EpisodeConfig], None], split: str,
                       experiment_seed: int, cond_id: int, n_episodes: int) -> Batch:
    """Test episodes for one named condition. Episode seeds depend on (split, seed, cond_id, i) only,
    never on the model, so all models are evaluated on identical episodes."""
    cfgs = []
    for _ in range(n_episodes):
        c = copy.deepcopy(base)
        overrides(c)
        cfgs.append(c)
    seeds = [episode_seed(split, experiment_seed, i, cond_id) for i in range(n_episodes)]
    return build_batch(cfgs, seeds)
