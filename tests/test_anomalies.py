import numpy as np

from src.anomalies.injection import AnomalyConfig, sample_anomalies


def _run(kind, seed=0, T=100, N=10, **kw):
    cfg = AnomalyConfig(kind=kind, **kw)
    return cfg, sample_anomalies(cfg, T, N, np.random.default_rng(seed))


def test_none_has_no_offset():
    _, s = _run("none")
    assert not s.offset.any() and not s.label.any() and not s.active.any()


def test_sudden_is_a_step():
    cfg, s = _run("sudden", seed=1)
    i = int(np.argmax(s.active.any(0)))
    mags = np.linalg.norm(s.offset[:, i], axis=-1)
    onset = int(np.argmax(mags > 0))
    assert mags[:onset].max() == 0 and np.allclose(mags[onset:], mags[onset])
    assert cfg.sudden_mag[0] <= mags[onset] <= cfg.sudden_mag[1]


def test_drift_is_linear():
    cfg, s = _run("drift", seed=2)
    i = int(np.argmax(s.active.any(0)))
    m = np.linalg.norm(s.offset[:, i], axis=-1)
    onset = int(np.argmax(m > 0)) - 1
    steps = np.arange(len(m)) - onset
    rate = m[-1] / steps[-1]
    assert cfg.drift_rate[0] <= rate <= cfg.drift_rate[1]
    np.testing.assert_allclose(m[onset:], rate * steps[onset:], atol=1e-9)


def test_spoof_group_shares_offset_vector():
    cfg, s = _run("spoof", seed=3, spoof_group=(3, 3), n_anomalous=(1, 1))
    idx = np.where(s.kind == "spoof")[0]
    assert len(idx) == 3
    final = s.offset[-1, idx]
    assert np.linalg.norm(final - final.mean(0), axis=-1).max() < 6 * cfg.spoof_jitter   # common-mode
    assert np.linalg.norm(final.mean(0)) >= cfg.spoof_mag[0] * 0.8


def test_labels_threshold_and_ambiguous_region():
    cfg, s = _run("drift", seed=4, label_min_offset=2.0)
    n = np.linalg.norm(s.offset, axis=-1)
    np.testing.assert_array_equal(s.label, n >= 2.0)
    assert (s.active & ~s.label).any()           # early drift steps exist and are 'ambiguous'


def test_count_and_onset_ranges():
    for seed in range(20):
        cfg, s = _run("mixed", seed=seed, n_anomalous=(1, 2), onset_frac=(0.25, 0.5), spoof_group=(1, 1))
        n_anom = s.active.any(0).sum()
        assert 1 <= n_anom <= 2
        first = int(np.argmax(s.active.any(1)))
        assert first >= 25 - 1


def test_anomaly_free_probability():
    free = sum(not _run("mixed", seed=s, p_anomaly_free=0.5)[1].active.any() for s in range(200))
    assert 70 < free < 130
