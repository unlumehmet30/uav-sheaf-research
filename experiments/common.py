from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

import numpy as np
import torch
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.simulation.episode import EpisodeConfig  # noqa: E402


def load_config(path: str | Path = ROOT / "configs" / "default.yaml") -> dict:
    return yaml.safe_load(Path(path).read_text())


def base_episode_config(cfg: dict) -> EpisodeConfig:
    return EpisodeConfig.from_dict(cfg["episode"])


def load_lr_map(cfg: dict) -> dict:
    p = ROOT / "configs" / "tuned_lr.yaml"
    return yaml.safe_load(p.read_text()) if p.exists() else {}


def environment_info() -> dict:
    import psutil
    return {
        "platform": platform.platform(), "machine": platform.machine(), "processor": platform.processor(),
        "python": sys.version.split()[0], "torch": torch.__version__, "numpy": np.__version__,
        "cpu_count": psutil.cpu_count(logical=True), "ram_gb": round(psutil.virtual_memory().total / 2**30, 1),
        "device": "cpu",
    }
