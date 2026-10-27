"""Shared helpers for loading trained detectors and scoring episodes (used by the dashboard and scripts).

A learned detector is available only if ``results/checkpoints/<name>_seed<k>.pt`` exists, i.e. only after
``experiments/run_main.py`` has trained it. Nothing is faked: if a checkpoint is missing, the model is reported
as 'not trained'.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import torch

from src.graph.dataset import Batch, build_batch
from src.models.detectors import ABLATIONS, LEARNED_MODELS, build_model, match_capacity, n_params
from src.models.physics import physics_scores
from src.simulation.episode import Episode, EpisodeConfig, generate_episode
from src.graph.features import build_features

ROOT = Path(__file__).resolve().parents[2]
CKPT = ROOT / "results" / "checkpoints"
RAW = ROOT / "results" / "raw"
PHYSICS = ["physics_naive", "physics_aoi"]
DISPLAY = {"physics_naive": "Physics (naive)", "physics_aoi": "Physics (AoI-aware)", "gcn": "GCN", "gcn_drop": "GCN (drop lost links)",
           "gat": "GAT", "nsd": "NSD-style sheaf", "rascm": "RA-SCM (proposed)"}


def checkpoint_path(name: str, seed: int = 0) -> Path:
    return CKPT / f"{name}_seed{seed}.pt"


def available_models(seed: int = 0) -> Dict[str, bool]:
    """model -> is it usable right now? (physics always; learned only with a checkpoint)."""
    out = {m: True for m in PHYSICS}
    for m in LEARNED_MODELS:
        out[m] = checkpoint_path(m, seed).exists()
    return out


@lru_cache(maxsize=16)
def _load(name: str, seed: int):
    target = n_params(build_model("rascm"))
    model = match_capacity(name, target)
    ck = torch.load(checkpoint_path(name, seed), map_location="cpu", weights_only=True)
    model.load_state_dict(ck["state_dict"])
    return model.eval()


def stored_threshold(name: str, seed: int = 0) -> Optional[float]:
    """Operating point fixed on the validation split during the real experiment run (5% FPR)."""
    f = RAW / f"metrics_seed{seed}.csv"
    if not f.exists():
        return None
    df = pd.read_csv(f)
    t = df[df.model == name]["threshold"]
    return float(t.iloc[0]) if len(t) else None


def score_batch(name: str, batch: Batch, seed: int = 0) -> np.ndarray:
    if name in PHYSICS:
        return physics_scores(batch.tensors, name == "physics_aoi").numpy()
    model = _load(name, seed)
    with torch.no_grad():
        return torch.sigmoid(model(batch.tensors)).numpy()


def episodes_to_batch(cfgs: List[EpisodeConfig], seeds: List[int]) -> Batch:
    return build_batch(cfgs, seeds)


def nominal_threshold(name: str, base: EpisodeConfig, n_ep: int = 12, target_fpr: float = 0.05, seed: int = 777) -> float:
    """Fallback for physics detectors when no stored threshold exists: 5% FPR on a *nominal* (no-loss) simulated set."""
    import copy
    from src.evaluation.metrics import threshold_at_fpr
    cfg = copy.deepcopy(base)
    cfg.channel.loss_rate = 0.0
    b = build_batch([cfg] * n_ep, [900_000 + seed + i for i in range(n_ep)])
    s = score_batch(name, b)
    return threshold_at_fpr(s, b.labels.numpy(), b.eval_mask.numpy(), target_fpr)
