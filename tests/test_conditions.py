import numpy as np

from experiments.aggregate import paired_table
from experiments.conditions import build_conditions
from src.graph.dataset import make_condition_set
from src.simulation.episode import EpisodeConfig
import pandas as pd


def test_condition_names_unique_and_cover_all_seven_experiment_families():
    cs = build_conditions()
    names = [c.name for c in cs]
    assert len(names) == len(set(names))
    assert {c.exp for c in cs} == {"E1", "E2", "E3", "E4", "E5"}
    required = {"iid_0", "iid_10", "iid_30", "iid_50", "burst_10", "burst_30", "burst_50", "targeted_30",
                "gen_n5", "gen_n20", "gen_lissajous", "gen_grid", "topo_30", "noise_3"}
    assert required <= set(names)


def test_loss_conditions_share_trajectories_and_labels():
    by = {c.name: c for c in build_conditions()}
    sets = {n: make_condition_set(EpisodeConfig(), by[n].fn, "test", 0, by[n].family, 3) for n in ("iid_0", "iid_50", "burst_50", "targeted_30")}
    for n in ("iid_50", "burst_50", "targeted_30"):
        np.testing.assert_array_equal(sets["iid_0"].labels.numpy(), sets[n].labels.numpy())


def test_generalisation_conditions_really_change_the_swarm():
    by = {c.name: c for c in build_conditions()}
    assert make_condition_set(EpisodeConfig(), by["gen_n20"].fn, "test", 0, 4, 1).tensors["node_x"].shape[2] == 20
    assert make_condition_set(EpisodeConfig(), by["gen_n5"].fn, "test", 0, 4, 1).tensors["node_x"].shape[2] == 5


def test_paired_table_decision_rule():
    rows = []
    for s in range(5):
        for m, v in (("rascm", 0.90 + 0.001 * s), ("gcn", 0.80 + 0.001 * s), ("nsd", 0.85), ("gat", 0.84), ("gcn_drop", 0.83)):
            rows.append({"seed": s, "model": m, "condition": "c", "pr_auc": v})
    t = paired_table(pd.DataFrame(rows), "rascm", ["gcn", "best_conventional"], ["c"])
    assert t.supports_H1.all() and (t.mean_diff > 0.04).all()
    rows2 = [{**r, "pr_auc": r["pr_auc"] if r["model"] != "rascm" else 0.855 + 0.02 * (r["seed"] % 2)} for r in rows]
    t2 = paired_table(pd.DataFrame(rows2), "rascm", ["best_conventional"], ["c"])
    assert not t2.supports_H1.any()
