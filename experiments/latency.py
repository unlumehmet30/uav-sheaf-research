"""Experiment 7: parameter count and CPU inference latency (batch of one 100-step episode, 1 thread).

Reported time is the amortised cost per UAV-swarm step of a *whole-episode* forward pass (all time steps are
processed in parallel for the spatial part, the GRU is sequential). It is a throughput proxy, NOT a measured
online per-packet latency on embedded hardware. Memory is the process-RSS increase around the forward pass
(approximate; includes allocator effects).
Usage: python -m experiments.latency
"""
from __future__ import annotations

import time

import numpy as np
import pandas as pd
import psutil
import torch

from experiments.common import ROOT, base_episode_config, load_config
from experiments.run_main import ALL_MODELS, PHYSICS
from src.graph.dataset import build_batch
from src.models.detectors import build_model, match_capacity, n_params
from src.models.physics import physics_scores

if __name__ == "__main__":
    torch.set_num_threads(1)
    cfg = load_config()
    base = base_episode_config(cfg)
    target = n_params(build_model("rascm"))
    proc = psutil.Process()
    rows = []
    for n in (5, 10, 20):
        c = base
        c.swarm.n_uavs = n
        b = build_batch([c], [123456])
        for name in ALL_MODELS:
            if name in PHYSICS:
                fn, npar = (lambda aoi=(name == "physics_aoi"): physics_scores(b.tensors, aoi)), 0
            else:
                m = match_capacity(name, target).eval()
                npar = n_params(m)
                fn = lambda m=m: torch.sigmoid(m(b.tensors))
            with torch.no_grad():
                for _ in range(2):
                    fn()
                rss0 = proc.memory_info().rss
                ts = []
                for _ in range(10):
                    t0 = time.perf_counter(); fn(); ts.append(time.perf_counter() - t0)
                rss1 = proc.memory_info().rss
            T = c.swarm.n_steps
            rows.append({"model": name, "n_uavs": n, "n_params": npar, "ms_per_episode": 1e3 * np.median(ts),
                         "ms_per_step": 1e3 * np.median(ts) / T, "rss_delta_mb": (rss1 - rss0) / 2**20})
            print(rows[-1], flush=True)
    out = pd.DataFrame(rows)
    (ROOT / "results" / "tables").mkdir(parents=True, exist_ok=True)
    out.to_csv(ROOT / "results" / "tables" / "latency.csv", index=False)
