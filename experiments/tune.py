"""Hyper-parameter selection (learning rate only) on a dedicated tuning seed and the 'tune' split.

Never touches the test split or the evaluation seeds. Writes configs/tuned_lr.yaml.
Usage:  python -m experiments.tune [--epochs 15]
"""
from __future__ import annotations

import argparse
import copy
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pandas as pd
import yaml

from experiments.common import ROOT, base_episode_config, load_config
from src.graph.dataset import make_split
from src.models.detectors import LEARNED_MODELS, build_model, match_capacity, n_params
from src.training.trainer import TrainConfig, train_model

MODELS = LEARNED_MODELS


def _job(args):
    name, lr, epochs = args
    cfg = load_config()
    base = base_episode_config(cfg)
    seed = cfg["experiment"]["tuning_seed"]
    train = make_split(base, "tune", seed, 160)
    val = make_split(base, "val", 100 + seed, 40)
    target = n_params(build_model("rascm"))
    model = match_capacity(name, target)
    tc = TrainConfig.from_dict({**cfg["train"], "lr": lr, "epochs": epochs})
    info = train_model(model, train, val, tc, seed=seed)
    return {"model": name, "lr": lr, "val_pr_auc": info["best_val_pr_auc"], "epochs_run": info["epochs_run"]}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=15)
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--extra-lrs", type=float, nargs="*", default=[],
                    help="extend the grid (e.g. when the optimum sits on the grid boundary); results are merged into tuning.csv")
    a = ap.parse_args()
    cfg = load_config()
    tab = ROOT / "results" / "tables" / "tuning.csv"
    prev = pd.read_csv(tab) if (tab.exists() and a.extra_lrs) else pd.DataFrame()
    grid = a.extra_lrs if a.extra_lrs else cfg["experiment"]["lr_grid"]
    jobs = [(m, lr, a.epochs) for m in MODELS for lr in grid]
    with ProcessPoolExecutor(a.workers) as ex:
        rows = list(ex.map(_job, jobs))
    df = pd.concat([prev, pd.DataFrame(rows)], ignore_index=True)
    tab.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(tab, index=False)
    best = df.loc[df.groupby("model")["val_pr_auc"].idxmax()]
    lr_map = {r.model: float(r.lr) for r in best.itertuples()}
    # ablations of RA-SCM inherit RA-SCM's tuned learning rate; mpnn_e too
    for k in ("rascm_no_rel", "rascm_no_weight", "rascm_no_sheaf", "rascm_no_temporal", "mpnn_e"):
        lr_map[k] = lr_map["rascm"]
    (ROOT / "configs" / "tuned_lr.yaml").write_text(
        "# learning rates selected on the tuning seed/validation split (experiments/tune.py)\n" + yaml.safe_dump(lr_map))
    print(df.to_string(index=False)); print(lr_map)
