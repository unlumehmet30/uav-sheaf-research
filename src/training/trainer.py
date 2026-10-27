"""Training / inference utilities (identical budget for every learned model)."""
from __future__ import annotations

import copy
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from src.evaluation.metrics import pr_auc
from src.graph.dataset import Batch
from src.models.detectors import Detector, n_params


@dataclass
class TrainConfig:
    epochs: int = 30
    batch_size: int = 16
    lr: float = 3e-3
    weight_decay: float = 1e-5
    grad_clip: float = 1.0
    patience: int = 8
    pos_weight_max: float = 10.0
    threads: int = 4

    @classmethod
    def from_dict(cls, d: dict) -> "TrainConfig":
        return cls(**d)


def set_seed(seed: int) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)


@torch.no_grad()
def predict(model: nn.Module, batch: Batch, chunk: int = 16) -> np.ndarray:
    """Sigmoid scores [E,T,N] for a whole batch of episodes."""
    model.eval()
    outs = []
    E = len(batch)
    for s in range(0, E, chunk):
        sub = {k: (v[s:s + chunk] if v.dim() > 0 else v) for k, v in batch.tensors.items()}
        outs.append(torch.sigmoid(model(sub)).numpy())
    return np.concatenate(outs, 0)


def _loss(logits, labels, mask, pos_weight):
    l = F.binary_cross_entropy_with_logits(logits, labels.float(), reduction="none",
                                           pos_weight=pos_weight)
    m = mask.float()
    return (l * m).sum() / m.sum().clamp(min=1.0)


def train_model(model: Detector, train: Batch, val: Batch, cfg: TrainConfig, seed: int,
                log_path: Optional[Path] = None, ckpt_path: Optional[Path] = None, verbose: bool = False) -> Dict:
    set_seed(seed)
    torch.set_num_threads(cfg.threads)
    opt = torch.optim.Adam(model.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)
    m = train.eval_mask
    pos = (train.labels & m).sum().item()
    neg = ((~train.labels) & m).sum().item()
    pos_weight = torch.tensor(min(cfg.pos_weight_max, neg / max(pos, 1)))
    g = torch.Generator().manual_seed(seed)

    best, best_state, bad, history = -1.0, None, 0, []
    t0 = time.time()
    for epoch in range(cfg.epochs):
        model.train()
        perm = torch.randperm(len(train), generator=g)
        tot, nb = 0.0, 0
        for s in range(0, len(train), cfg.batch_size):
            idx = perm[s:s + cfg.batch_size]
            sub = {k: (v[idx] if v.dim() > 0 else v) for k, v in train.tensors.items()}
            logits = model(sub)
            loss = _loss(logits, train.labels[idx], train.eval_mask[idx], pos_weight)
            opt.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), cfg.grad_clip)
            opt.step()
            tot += loss.item(); nb += 1
        vs = predict(model, val)
        val_ap = pr_auc(vs, val.labels.numpy(), val.eval_mask.numpy())
        history.append({"epoch": epoch, "train_loss": tot / nb, "val_pr_auc": val_ap, "elapsed_s": time.time() - t0})
        if verbose:
            print(f"  ep{epoch:02d} loss {tot / nb:.4f} val_ap {val_ap:.4f} ({time.time() - t0:.0f}s)", flush=True)
        if val_ap > best:
            best, bad = val_ap, 0
            best_state = copy.deepcopy(model.state_dict())
        else:
            bad += 1
            if bad >= cfg.patience:
                break
    model.load_state_dict(best_state)
    info = {"best_val_pr_auc": best, "epochs_run": len(history), "train_seconds": time.time() - t0,
            "n_params": n_params(model), "history": history, "seed": seed, "config": asdict(cfg)}
    if log_path is not None:
        Path(log_path).parent.mkdir(parents=True, exist_ok=True)
        Path(log_path).write_text(json.dumps(info, indent=1))
    if ckpt_path is not None:
        Path(ckpt_path).parent.mkdir(parents=True, exist_ok=True)
        torch.save({"state_dict": model.state_dict(), "seed": seed}, ckpt_path)
    return info
