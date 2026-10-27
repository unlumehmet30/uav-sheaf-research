"""Main experiment runner: one evaluation seed -> raw metric table for every model and condition.

For a given seed: generate train/val splits (episode-level disjoint) and the shared test sets; train every learned
model with an identical budget; fix each model's operating point on the validation split; evaluate on all test
conditions. Physics baselines are not trained. Everything is reproducible from (config, seed).

Usage:
    python -m experiments.run_main --seed 0
    python -m experiments.run_main --seed 0 --models rascm gcn --quick
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from experiments.common import ROOT, base_episode_config, environment_info, load_config, load_lr_map
from experiments.conditions import build_conditions
from src.evaluation.metrics import evaluate_condition, pr_curve, threshold_at_fpr
from src.graph.dataset import make_condition_set, make_split
from src.models.detectors import ABLATIONS, LEARNED_MODELS, build_model, match_capacity, n_params
from src.models.physics import physics_scores
from src.training.trainer import TrainConfig, predict, train_model

PHYSICS = ["physics_naive", "physics_aoi"]
ALL_MODELS = PHYSICS + LEARNED_MODELS + ABLATIONS
CURVE_CONDITIONS = ["iid_0", "iid_30", "iid_50", "burst_50", "targeted_30"]


def run_seed(seed: int, models, cfg: dict, out_dir: Path, quick: bool = False) -> pd.DataFrame:
    base = base_episode_config(cfg)
    dcfg, ecfg = cfg["data"], cfg["experiment"]
    n_train, n_val, n_test = dcfg["n_train"], dcfg["n_val"], dcfg["n_test_per_condition"]
    if quick:
        n_train, n_val, n_test = 40, 20, 8
    lr_map = load_lr_map(cfg)
    t0 = time.time()
    train = make_split(base, "train", seed, n_train)
    val = make_split(base, "val", seed, n_val)
    conds = build_conditions()
    tests = {c.name: make_condition_set(base, c.fn, "test", seed, c.family, n_test) for c in conds}
    print(f"[seed {seed}] data ready in {time.time() - t0:.0f}s: train {len(train)}, val {len(val)}, "
          f"{len(conds)} test conditions x {n_test} episodes", flush=True)

    target_params = n_params(build_model("rascm"))
    rows, curves = [], {}
    for name in models:
        info = {"train_s": 0.0, "epochs": 0, "lr": float("nan")}
        if name in PHYSICS:
            aoi = name == "physics_aoi"
            score = lambda b, aoi=aoi: physics_scores(b.tensors, aoi).numpy()
            n_par = 0
        else:
            model = match_capacity(name, target_params)
            n_par = n_params(model)
            tc = dict(cfg["train"])
            tc["lr"] = lr_map.get(name, tc["lr"])
            if quick:
                tc["epochs"] = 3
            tcfg = TrainConfig.from_dict(tc)
            print(f"[seed {seed}] training {name} ({n_par} params, lr {tcfg.lr})", flush=True)
            ti = train_model(model, train, val, tcfg, seed=seed,
                             log_path=out_dir / "logs" / f"{name}_seed{seed}.json",
                             ckpt_path=ROOT / "results" / "checkpoints" / f"{name}_seed{seed}.pt", verbose=False)
            info = {"train_s": ti["train_seconds"], "epochs": ti["epochs_run"], "lr": tcfg.lr}
            print(f"[seed {seed}]   {name}: val PR-AUC {ti['best_val_pr_auc']:.3f}, {ti['epochs_run']} epochs, "
                  f"{ti['train_seconds']:.0f}s", flush=True)
            score = lambda b, m=model: predict(m, b)
        vs = score(val)
        thr = threshold_at_fpr(vs, val.labels.numpy(), val.eval_mask.numpy(), ecfg["target_fpr"])
        for c in conds:
            b = tests[c.name]
            s = score(b)
            m = evaluate_condition(s, b.labels.numpy(), b.eval_mask.numpy(), thr, b.meta[0]["dt"])
            rows.append({"seed": seed, "model": name, "condition": c.name, "exp": c.exp, "n_params": n_par,
                         "threshold": thr, **info, **m})
            if c.name in CURVE_CONDITIONS:
                p, r = pr_curve(s, b.labels.numpy(), b.eval_mask.numpy())
                curves[f"{name}|{c.name}"] = {"precision": p.round(4).tolist(), "recall": r.round(4).tolist()}
        print(f"[seed {seed}] evaluated {name}", flush=True)
        pd.DataFrame(rows).to_csv(out_dir / f"metrics_seed{seed}.csv", index=False)

    df = pd.DataFrame(rows)
    df.to_csv(out_dir / f"metrics_seed{seed}.csv", index=False)
    (out_dir / f"curves_seed{seed}.json").write_text(json.dumps(curves))
    return df


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--models", nargs="*", default=ALL_MODELS)
    ap.add_argument("--out", default=str(ROOT / "results" / "raw"))
    ap.add_argument("--quick", action="store_true", help="tiny smoke run (NOT for reported results)")
    a = ap.parse_args()
    out = Path(a.out)
    (out / "logs").mkdir(parents=True, exist_ok=True)
    cfg = load_config()
    (ROOT / "results" / "env.json").write_text(json.dumps(environment_info(), indent=1))
    run_seed(a.seed, a.models, cfg, out, quick=a.quick)
