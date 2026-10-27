import numpy as np
import pytest

from src.communication.channel import ChannelConfig, apply_targeted_loss, gilbert_elliott_params, sample_lost


@pytest.mark.parametrize("p", [0.1, 0.3, 0.5])
def test_iid_loss_rate(p):
    lost = sample_lost(ChannelConfig("iid", p), 400, 10, np.random.default_rng(0))
    assert abs(lost.mean() - p) < 0.01


def test_zero_loss_delivers_everything():
    assert not sample_lost(ChannelConfig("burst", 0.0), 50, 5, np.random.default_rng(0)).any()


@pytest.mark.parametrize("p", [0.1, 0.3, 0.5])
def test_gilbert_elliott_stationary_loss_and_burst_length(p):
    L = 5.0
    lost = sample_lost(ChannelConfig("burst", p, mean_burst=L), 3000, 12, np.random.default_rng(1))
    assert abs(lost.mean() - p) < 0.02
    # mean run length of consecutive losses ~ L
    runs = []
    for k in range(12):
        x = lost[:, 0, k] if False else lost[:, k, (k + 1) % 12]
        run = 0
        for v in x:
            if v: run += 1
            elif run: runs.append(run); run = 0
    assert abs(np.mean(runs) - L) < 0.6


def test_burst_is_more_correlated_than_iid():
    a = sample_lost(ChannelConfig("iid", 0.3), 2000, 6, np.random.default_rng(2))[:, 0, 1]
    b = sample_lost(ChannelConfig("burst", 0.3, 5.0), 2000, 6, np.random.default_rng(2))[:, 0, 1]
    ac = lambda x: np.corrcoef(x[:-1], x[1:])[0, 1]
    assert ac(b) > ac(a) + 0.4


def test_node_burst_is_correlated_across_incoming_links():
    lost = sample_lost(ChannelConfig("node_burst", 0.3, 5.0), 500, 8, np.random.default_rng(3))
    np.testing.assert_array_equal(lost[:, 2, 0], lost[:, 2, 5])        # same receiver => same chain
    assert not np.array_equal(lost[:, 2, 0], lost[:, 3, 0])


def test_ge_params_consistency():
    p_gb, p_bg = gilbert_elliott_params(0.3, 5.0)
    assert abs(p_gb / (p_gb + p_bg) - 0.3) < 1e-12 and abs(p_bg - 0.2) < 1e-12
    with pytest.raises(ValueError):
        gilbert_elliott_params(1.0, 5.0)


def test_targeted_loss_only_hits_active_senders():
    T, N = 200, 6
    lost = np.zeros((T, N, N), bool)
    active = np.zeros((T, N), bool); active[:, 2] = True
    out = apply_targeted_loss(lost, active, 0.7, np.random.default_rng(0))
    assert abs(out[:, :, 2].mean() - 0.7) < 0.05
    assert not out[:, :, [0, 1, 3, 4, 5]].any()
