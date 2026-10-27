import numpy as np
import torch

from src.graph.dataset import SPLIT_BASE, episode_seed, make_condition_set, make_split
from src.simulation.episode import EpisodeConfig


def test_split_seed_ranges_are_disjoint():
    ranges = {}
    for split in SPLIT_BASE:
        seeds = {episode_seed(split, s, i, c) for s in range(10) for i in range(300) for c in range(40)}
        ranges[split] = seeds
    names = list(ranges)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            assert not (ranges[names[i]] & ranges[names[j]]), (names[i], names[j])


def test_splits_share_no_episode():
    base = EpisodeConfig()
    tr, va = make_split(base, "train", 0, 6), make_split(base, "val", 0, 6)
    assert not ({m["seed"] for m in tr.meta} & {m["seed"] for m in va.meta})
    assert not torch.allclose(tr.tensors["node_x"][0], va.tensors["node_x"][0])


def test_condition_sets_identical_across_calls_and_paired_across_loss():
    base = EpisodeConfig()
    def at(p):
        def f(c): c.channel.loss_rate = p
        return f
    a = make_condition_set(base, at(0.3), "test", 0, 5, 4)
    b = make_condition_set(base, at(0.3), "test", 0, 5, 4)
    c = make_condition_set(base, at(0.0), "test", 0, 5, 4)
    torch.testing.assert_close(a.tensors["edge_x"], b.tensors["edge_x"])
    assert torch.equal(a.labels, c.labels)                       # same episodes, only the channel differs
    assert a.tensors["delivered"].sum() < c.tensors["delivered"].sum()


def test_batch_has_separate_label_and_feature_tensors():
    tr = make_split(EpisodeConfig(), "train", 0, 4)
    assert "labels" not in tr.tensors
    assert tr.tensors["node_x"].shape[0] == 4 and tr.labels.dtype == torch.bool
    assert (tr.eval_mask | ~tr.labels).all()           # positives are always evaluated
