"""Evaluation metrics.

PR-AUC is *average precision* as implemented by scikit-learn:  AP = sum_n (R_n - R_{n-1}) P_n,
the step-wise (non-interpolated) area under the precision-recall curve over all evaluated
UAV-steps of a condition (pooled across episodes). Chance level equals the positive rate.

Evaluated UAV-steps exclude 'ambiguous' ones (injection active but offset below the labelling
threshold), see ``Batch.eval_mask``.

The operating point is chosen once per model on the pooled *validation* split as the smallest
threshold whose false-positive rate on negatives is <= ``target_fpr``; it is then frozen for all
test conditions, so FPR/precision/recall/delay differences between conditions are meaningful.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

import numpy as np
from scipy import stats
from sklearn.metrics import average_precision_score, precision_recall_curve, roc_auc_score


def flatten(scores: np.ndarray, labels: np.ndarray, mask: np.ndarray):
    m = mask.astype(bool)
    return scores[m], labels[m].astype(int)


def pr_auc(scores: np.ndarray, labels: np.ndarray, mask: np.ndarray) -> float:
    s, y = flatten(scores, labels, mask)
    return float(average_precision_score(y, s)) if y.sum() > 0 else float("nan")


def roc_auc(scores: np.ndarray, labels: np.ndarray, mask: np.ndarray) -> float:
    s, y = flatten(scores, labels, mask)
    return float(roc_auc_score(y, s)) if 0 < y.sum() < len(y) else float("nan")


def pr_curve(scores, labels, mask, max_points: int = 200):
    s, y = flatten(scores, labels, mask)
    p, r, _ = precision_recall_curve(y, s)
    if len(p) > max_points:
        idx = np.unique(np.linspace(0, len(p) - 1, max_points).astype(int))
        p, r = p[idx], r[idx]
    return p, r


def threshold_at_fpr(scores: np.ndarray, labels: np.ndarray, mask: np.ndarray, target_fpr: float = 0.05) -> float:
    s, y = flatten(scores, labels, mask)
    neg = np.sort(s[y == 0])
    if len(neg) == 0:
        return float("inf")
    k = int(np.ceil((1 - target_fpr) * len(neg))) - 1
    return float(neg[min(max(k, 0), len(neg) - 1)])


def threshold_metrics(scores, labels, mask, thr: float) -> Dict[str, float]:
    s, y = flatten(scores, labels, mask)
    pred = s > thr
    tp = int((pred & (y == 1)).sum()); fp = int((pred & (y == 0)).sum())
    fn = int((~pred & (y == 1)).sum()); tn = int((~pred & (y == 0)).sum())
    prec = tp / (tp + fp) if tp + fp else float("nan")
    rec = tp / (tp + fn) if tp + fn else float("nan")
    f1 = 2 * prec * rec / (prec + rec) if tp > 0 else (0.0 if tp + fp + fn > 0 else float("nan"))
    fpr = fp / (fp + tn) if fp + tn else float("nan")
    return {"precision": prec, "recall": rec, "f1": f1, "fpr": fpr}


def detection_delay(scores: np.ndarray, labels: np.ndarray, thr: float, dt: float, patience: int = 2) -> Dict[str, float]:
    """Delay between the first labelled-anomalous step and the first alarm (``patience`` consecutive
    steps above threshold, to ignore single-step noise), for every (episode, UAV) that becomes anomalous.

    Returns detection rate (alarm at any time at/after onset) and the median / mean delay in seconds
    over detected UAVs. Undetected UAVs are right-censored and *not* included in the delay statistics,
    which is why the detection rate must be reported alongside.
    """
    E, T, N = labels.shape
    delays: List[float] = []
    n_pos = 0
    for e in range(E):
        for i in range(N):
            lab = labels[e, :, i]
            if not lab.any():
                continue
            n_pos += 1
            onset = int(np.argmax(lab))
            above = scores[e, :, i] > thr
            run = 0
            for t in range(onset, T):
                run = run + 1 if above[t] else 0
                if run >= patience:
                    delays.append((t - patience + 1 - onset) * dt)
                    break
    return {"detect_rate": len(delays) / n_pos if n_pos else float("nan"),
            "delay_median_s": float(np.median(delays)) if delays else float("nan"),
            "delay_mean_s": float(np.mean(delays)) if delays else float("nan"),
            "n_anomalous_uavs": n_pos}


def evaluate_condition(scores: np.ndarray, labels: np.ndarray, mask: np.ndarray, thr: float, dt: float) -> Dict[str, float]:
    out = {"pr_auc": pr_auc(scores, labels, mask), "roc_auc": roc_auc(scores, labels, mask),
           "pos_rate": float(labels[mask.astype(bool)].mean())}
    out.update(threshold_metrics(scores, labels, mask, thr))
    out.update(detection_delay(np.where(mask, scores, -np.inf), labels, thr, dt))
    return out


def t_ci(values: Sequence[float], level: float = 0.95) -> tuple[float, float, float]:
    """Mean and two-sided t-interval half-width over independent runs (seeds)."""
    v = np.asarray([x for x in values if not np.isnan(x)], dtype=float)
    n = len(v)
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    if n == 1:
        return float(v[0]), float("nan"), float("nan")
    se = v.std(ddof=1) / np.sqrt(n)
    half = stats.t.ppf(0.5 + level / 2, n - 1) * se
    return float(v.mean()), float(half), float(se)


def paired_diff(a: Sequence[float], b: Sequence[float], level: float = 0.95) -> Dict[str, float]:
    """Paired difference a-b across seeds: mean, t-CI half width, and one-sided p for H1: mean(a-b) > 0."""
    d = np.asarray(a, float) - np.asarray(b, float)
    d = d[~np.isnan(d)]
    n = len(d)
    if n < 2:
        return {"mean": float("nan"), "half": float("nan"), "p_greater": float("nan"), "n": n}
    mean, half, se = t_ci(d, level)
    tstat = d.mean() / (d.std(ddof=1) / np.sqrt(n)) if d.std(ddof=1) > 0 else np.inf * np.sign(d.mean())
    p = float(1 - stats.t.cdf(tstat, n - 1))
    return {"mean": mean, "half": half, "p_greater": p, "n": n}
