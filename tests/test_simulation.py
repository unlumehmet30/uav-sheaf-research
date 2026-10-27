import numpy as np
import pytest

from src.anomalies.injection import AnomalyConfig
from src.communication.channel import ChannelConfig
from src.simulation.episode import EpisodeConfig, SensorConfig, generate_episode
from src.simulation.swarm import SwarmConfig, simulate_truth


def _cfg(**kw):
    cfg = EpisodeConfig()
    for k, v in kw.items():
        setattr(cfg.swarm, k, v)
    return cfg


def test_determinism_and_seed_sensitivity():
    a, b, c = (generate_episode(EpisodeConfig(), s) for s in (1, 1, 2))
    np.testing.assert_array_equal(a.true_pos, b.true_pos)
    np.testing.assert_array_equal(a.rep_pos, b.rep_pos)
    assert not np.allclose(a.true_pos, c.true_pos)


@pytest.mark.parametrize("n", [5, 10, 20])
@pytest.mark.parametrize("traj", ["random_turn", "circle", "lissajous"])
def test_shapes_and_finite(n, traj):
    ep = generate_episode(_cfg(n_uavs=n, trajectory=traj), 0)
    T = ep.cfg.swarm.n_steps
    assert ep.true_pos.shape == (T, n, 2) and ep.obs.delivered.shape == (T, n, n)
    assert np.isfinite(ep.true_pos).all() and np.isfinite(ep.obs.rel_meas).all()


@pytest.mark.parametrize("formation", ["circle", "line", "wedge", "grid"])
def test_formation_tracking_is_bounded(formation):
    cfg = SwarmConfig(formation=formation)
    rng = np.random.default_rng(0)
    truth = simulate_truth(cfg, rng)
    err = np.linalg.norm(truth.pos - truth.des_pos, axis=-1)
    assert err[10:].max() < 8.0          # PD tracking keeps UAVs near their slots (after settling)
    acc = np.linalg.norm(np.diff(truth.vel, axis=0) / cfg.dt, axis=-1)
    assert acc.max() < cfg.a_max + 6 * cfg.wind_std * 3 + 1.0   # bounded control + wind


def test_real_measured_reported_are_distinct_and_consistent():
    cfg = EpisodeConfig(anomaly=AnomalyConfig(kind="sudden"))
    ep = generate_episode(cfg, 4)
    assert not np.allclose(ep.true_pos, ep.meas_pos)                       # measurement noise
    np.testing.assert_allclose(ep.rep_pos, ep.meas_pos + ep.schedule.offset)  # reported = measured + injection
    assert ep.labels.any()


def test_noise_levels_match_config():
    cfg = EpisodeConfig(anomaly=AnomalyConfig(kind="none"), sensors=SensorConfig(gnss_sigma=1.0, rel_sigma=0.3, noise_scale=2.0))
    cfg.swarm.n_steps = 300
    ep = generate_episode(cfg, 7)
    gnss = (ep.meas_pos - ep.true_pos).std()
    diff = ep.true_pos[:, None] - ep.true_pos[:, :, None]
    rel = (ep.obs.rel_meas - diff)[ep.obs.adj].std()
    assert abs(gnss - 2.0) < 0.1 and abs(rel - 0.6) < 0.05


def test_adjacency_follows_true_distance_and_is_symmetric():
    ep = generate_episode(EpisodeConfig(), 3)
    adj = ep.obs.adj
    np.testing.assert_array_equal(adj, adj.transpose(0, 2, 1))
    assert not adj[:, np.arange(10), np.arange(10)].any()
    d = np.linalg.norm(ep.true_pos[:, None] - ep.true_pos[:, :, None], axis=-1)
    expected = (d <= ep.cfg.swarm.comm_range) & ~np.eye(10, dtype=bool)[None]
    np.testing.assert_array_equal(adj, expected)          # no blockage by default


def test_dynamic_topology_blockage_removes_links():
    base = generate_episode(EpisodeConfig(), 3)
    cfg = EpisodeConfig(blockage_rate=10.0)
    blk = generate_episode(cfg, 3)
    assert blk.obs.adj.sum() < base.obs.adj.sum()
    np.testing.assert_array_equal(base.true_pos, blk.true_pos)   # same physical motion


def test_channel_only_change_keeps_truth_noise_and_anomalies():
    """Independent RNG streams: paired comparisons across packet-loss levels are possible."""
    a = generate_episode(EpisodeConfig(channel=ChannelConfig(loss_rate=0.0)), 11)
    b = generate_episode(EpisodeConfig(channel=ChannelConfig(loss_rate=0.5, loss_model="burst")), 11)
    np.testing.assert_array_equal(a.true_pos, b.true_pos)
    np.testing.assert_array_equal(a.rep_pos, b.rep_pos)
    np.testing.assert_array_equal(a.labels, b.labels)
    assert a.obs.delivered.sum() > b.obs.delivered.sum()


def test_comm_failure_mask_separate_from_labels_and_only_in_range():
    ep = generate_episode(EpisodeConfig(channel=ChannelConfig(loss_rate=0.3)), 5)
    assert not (ep.comm_fail & ~ep.obs.adj).any()
    np.testing.assert_array_equal(ep.obs.delivered | ep.comm_fail, ep.obs.adj)
    assert not (ep.obs.delivered & ep.comm_fail).any()
