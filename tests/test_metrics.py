import numpy as np
import pytest
from sklearn.metrics import average_precision_score

from src.evaluation.metrics import (detection_delay, evaluate_condition, paired_diff, pr_auc, roc_auc,
                                    t_ci, threshold_at_fpr, threshold_metrics)


def test_pr_auc_perfect_and_chance():
    y = np.array([[0, 0, 1, 1, 0, 1, 0, 0]])
    m = np.ones_like(y, bool)
    assert pr_auc(y.astype(float), y, m) == 1.0
    rng = np.random.default_rng(0)
    yy = (rng.random((1, 20000)) < 0.1).astype(int)
    assert abs(pr_auc(rng.random(yy.shape), yy, np.ones_like(yy, bool)) - 0.1) < 0.01


def test_pr_auc_matches_manual_step_ap():
    s = np.array([0.9, 0.8, 0.7, 0.6, 0.5, 0.4])
    y = np.array([1, 0, 1, 0, 0, 1])
    # precision at each positive: 1/1, 2/3, 3/6 ; recall steps of 1/3
    manual = (1 / 3) * (1 + 2 / 3 + 3 / 6)
    assert pr_auc(s[None], y[None], np.ones((1, 6), bool)) == pytest.approx(manual)
    assert manual == pytest.approx(average_precision_score(y, s))


def test_mask_excludes_ambiguous_steps():
    s = np.array([[0.1, 0.9, 0.2, 0.8]]); y = np.array([[0, 0, 0, 1]]); m = np.array([[1, 0, 1, 1]], bool)
    assert pr_auc(s, y, m) == 1.0            # the high-scoring 'ambiguous' negative is ignored


def test_threshold_at_fpr_and_threshold_metrics():
    rng = np.random.default_rng(1)
    y = np.r_[np.zeros(1000), np.ones(200)].astype(int)[None]
    s = np.r_[rng.normal(0, 1, 1000), rng.normal(3, 1, 200)][None]
    m = np.ones_like(y, bool)
    thr = threshold_at_fpr(s, y, m, 0.05)
    tm = threshold_metrics(s, y, m, thr)
    assert tm["fpr"] <= 0.05 + 1e-9 and tm["fpr"] > 0.03
    assert 0.8 < tm["recall"] < 1.0 and 0.5 < tm["precision"] <= 1.0
    assert tm["f1"] == pytest.approx(2 * tm["precision"] * tm["recall"] / (tm["precision"] + tm["recall"]))


def test_roc_auc_perfect():
    y = np.array([[0, 0, 1, 1]]); assert roc_auc(y.astype(float), y, np.ones_like(y, bool)) == 1.0


def test_detection_delay_known_case():
    labels = np.zeros((2, 20, 2), bool)
    labels[0, 5:, 0] = True           # episode 0 / uav 0 anomalous from step 5
    labels[1, 8:, 1] = True           # episode 1 / uav 1 from step 8 (never detected)
    scores = np.zeros((2, 20, 2))
    scores[0, 8:, 0] = 1.0            # alarm from step 8, patience 2 -> first alarm step 8
    out = detection_delay(scores, labels, thr=0.5, dt=0.5, patience=2)
    assert out["n_anomalous_uavs"] == 2 and out["detect_rate"] == 0.5
    assert out["delay_median_s"] == pytest.approx((8 - 5) * 0.5)


def test_single_step_spike_is_ignored_with_patience():
    labels = np.zeros((1, 10, 1), bool); labels[0, 2:, 0] = True
    scores = np.zeros((1, 10, 1)); scores[0, 4, 0] = 1.0
    assert detection_delay(scores, labels, 0.5, 1.0, patience=2)["detect_rate"] == 0.0


def test_t_ci_and_paired_diff():
    m, half, se = t_ci([1, 2, 3, 4, 5])
    assert m == 3 and half == pytest.approx(2.776 * np.std([1, 2, 3, 4, 5], ddof=1) / np.sqrt(5), rel=1e-3)
    d = paired_diff([2, 3, 4, 5, 6], [1, 2, 3, 4, 5])
    assert d["mean"] == 1.0 and d["p_greater"] < 0.01
    d0 = paired_diff([1, 2, 3, 4, 5], [1.5, 1.5, 3.5, 3.5, 5.0])
    assert d0["p_greater"] > 0.3


def test_evaluate_condition_keys():
    rng = np.random.default_rng(0)
    y = rng.random((3, 30, 4)) < 0.2
    out = evaluate_condition(rng.random(y.shape) + y, y, np.ones_like(y, bool), 0.8, 0.5)
    for k in ("pr_auc", "roc_auc", "precision", "recall", "f1", "fpr", "detect_rate", "delay_median_s"):
        assert k in out
