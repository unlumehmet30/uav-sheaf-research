"""Graph construction + information-leakage tests."""
import copy
import dataclasses

import numpy as np
import pytest

from src.anomalies.injection import AnomalyConfig
from src.communication.channel import ChannelConfig
from src.graph.features import A_MAX, EDGE_COLS, N_EDGE, N_NODE, build_features
from src.simulation.episode import Episode, EpisodeConfig, Observation, generate_episode

HIDDEN = {"true_pos", "true_vel", "meas_pos", "schedule", "comm_fail", "labels", "offset", "label", "active"}


def _ep(loss=0.3, model="iid", seed=2, **kw):
    cfg = EpisodeConfig(channel=ChannelConfig(model, loss), **kw)
    return generate_episode(cfg, seed)


def test_observation_exposes_no_ground_truth_fields():
    names = {f.name for f in dataclasses.fields(Observation)}
    assert not (names & HIDDEN)


def test_build_features_rejects_full_episode():
    ep = _ep()
    with pytest.raises(AttributeError):
        build_features(ep)       # an Episode (with ground truth) is not accepted: needs Observation attributes


def test_features_are_function_of_observation_only():
    """Replace every hidden field by garbage: features must be bit-identical."""
    ep = _ep()
    f1 = build_features(ep.observable())
    ep2 = copy.deepcopy(ep)
    ep2.true_pos[:] = np.random.default_rng(0).normal(size=ep2.true_pos.shape)
    ep2.meas_pos[:] = 0
    ep2.schedule.offset[:] = 99
    ep2.schedule.label[:] = ~ep2.schedule.label
    ep2.comm_fail[:] = ~ep2.comm_fail
    f2 = build_features(ep2.observable())
    for k in f1:
        np.testing.assert_array_equal(np.asarray(f1[k]), np.asarray(f2[k]))


def test_features_are_causal():
    """Changing observations after step t0 must not change features at steps <= t0."""
    ep = _ep(loss=0.4)
    t0 = 40
    f1 = build_features(ep.observable())
    obs2 = copy.deepcopy(ep.observable())
    rng = np.random.default_rng(1)
    obs2.rep_pos[t0 + 1:] += rng.normal(0, 5, obs2.rep_pos[t0 + 1:].shape)
    obs2.vel_meas[t0 + 1:] += 3.0
    obs2.rel_meas[t0 + 1:] += 2.0
    obs2.delivered[t0 + 1:] = ~obs2.delivered[t0 + 1:]
    f2 = build_features(obs2)
    for k in ("node_x", "edge_x", "valid", "delivered", "tidx", "res_m", "resc_m", "age", "kin_m"):
        np.testing.assert_array_equal(f1[k][:t0 + 1], f2[k][:t0 + 1], err_msg=k)


def test_cache_index_semantics():
    ep = _ep(loss=0.5, model="burst")
    f = build_features(ep.observable())
    T, N = f["tidx"].shape[:2]
    t = np.arange(T)[:, None, None]
    assert (f["tidx"] <= t).all()                                  # never reads the future
    deliv = ep.obs.delivered
    for tt in (10, 30, 60):
        for r in range(N):
            for s in range(N):
                got = np.where(deliv[: tt + 1, r, s])[0]
                if f["valid"][tt, r, s] > 0:
                    assert f["tidx"][tt, r, s] == got.max()
                    assert abs(f["age"][tt, r, s] - (tt - got.max())) < 1e-6
    # message graph is a subset of the sensing graph
    assert (f["valid"] <= f["adj"]).all() and (f["delivered"] <= f["valid"]).all()


def test_no_loss_means_fresh_data_and_compensation_is_identity():
    ep = _ep(loss=0.0)
    f = build_features(ep.observable())
    assert (f["age"] == 0).all()
    np.testing.assert_allclose(f["res_m"], f["resc_m"])
    assert (f["valid"] == f["adj"]).all()


def test_stale_data_is_compensated_by_velocity():
    """Without anomalies/noise the age-compensated residual must be much smaller than the raw stale one."""
    cfg = EpisodeConfig(anomaly=AnomalyConfig(kind="none"), channel=ChannelConfig("iid", 0.6))
    ep = generate_episode(cfg, 8)
    f = build_features(ep.observable())
    stale = f["age"] >= 3
    assert stale.sum() > 100
    raw = np.linalg.norm(f["res_m"], axis=-1)[stale].mean()
    comp = np.linalg.norm(f["resc_m"], axis=-1)[stale].mean()
    assert comp < 0.5 * raw


def test_shapes_for_swarm_sizes():
    for n in (5, 10, 20):
        cfg = EpisodeConfig()
        cfg.swarm.n_uavs = n
        f = build_features(generate_episode(cfg, 0).observable())
        T = cfg.swarm.n_steps
        assert f["node_x"].shape == (T, n, N_NODE) and f["edge_x"].shape == (T, n, n, N_EDGE)
        assert np.isfinite(f["edge_x"]).all() and np.isfinite(f["node_x"]).all()
        assert len(EDGE_COLS) == N_EDGE
