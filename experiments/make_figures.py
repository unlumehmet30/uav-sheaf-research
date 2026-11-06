"""Figures for the report from results/tables/*.csv and results/raw/curves_seed*.json.
Usage: python -m experiments.make_figures
Colour follows the model (fixed entity->slot map, validated reference palette); baselines that are
not learned use dashed lines + hollow markers as a second encoding channel.
"""
from __future__ import annotations

import glob
import json

import matplotlib
import matplotlib.ticker

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from experiments.common import ROOT

TAB, FIG, RAW = ROOT / "results" / "tables", ROOT / "report" / "figures", ROOT / "results" / "raw"
FIG.mkdir(parents=True, exist_ok=True)

SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
COLORS = {"rascm": "#2a78d6", "nsd": "#eb6834", "gcn": "#1baf7a", "gat": "#eda100", "gcn_drop": "#e87ba4",
          "physics_aoi": "#6250d6", "physics_naive": "#e34948",
          "rascm_no_rel": "#2a78d6", "rascm_no_weight": "#eb6834", "rascm_no_sheaf": "#1baf7a",
          "rascm_no_temporal": "#eda100", "mpnn_e": "#6250d6"}
LABEL = {"rascm": "RA-SCM (proposed)", "nsd": "NSD-style sheaf", "gcn": "GCN", "gat": "GAT", "gcn_drop": "GCN-drop (lost links removed)",
         "physics_aoi": "Physics (AoI-aware)", "physics_naive": "Physics (naive)",
         "rascm_no_rel": "− reliability info", "rascm_no_weight": "− reliability weights", "rascm_no_sheaf": "− sheaf maps (F = I)",
         "rascm_no_temporal": "− temporal (GRU)", "mpnn_e": "− maps − weights (MPNN-E)"}
# display names of test conditions (same as the report tables)
COND = {"iid_0": "iid 0%", "iid_30": "iid 30%", "iid_50": "iid 50%", "burst_30": "burst 30%", "burst_50": "burst 50%",
        "nodeburst_30": "rx-burst 30%", "targeted_30": "targeted 30%", "gen_n20": "20 UAVs, iid 30%"}
SHORT = {"physics_naive": "Phys.", "physics_aoi": "Phys. AoI", "gcn": "GCN", "gcn_drop": "GCN-drop", "gat": "GAT", "nsd": "NSD",
         "rascm": "RA-SCM"}
DASHED = {"physics_aoi", "physics_naive"}
MAIN = ["physics_naive", "physics_aoi", "gcn", "gcn_drop", "gat", "nsd", "rascm"]

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": "#c3c2b7", "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
    "text.color": INK, "font.family": "sans-serif", "font.size": 10, "axes.titlesize": 10.5, "axes.titleweight": "regular",
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.axisbelow": True, "legend.frameon": False, "lines.linewidth": 1.8, "lines.markersize": 5, "figure.dpi": 150,
})


def _s(summ, model, cond, metric):
    r = summ[(summ.model == model) & (summ.condition == cond) & (summ.metric == metric)]
    return (r["mean"].iloc[0], r["ci_half"].iloc[0]) if len(r) else (np.nan, np.nan)


def _style(m):
    return dict(color=COLORS[m], ls="--" if m in DASHED else "-", marker="o" if m not in DASHED else "s",
                mfc=SURFACE if m in DASHED else COLORS[m], mec=COLORS[m], mew=1.4)


def sweep(summ, metric, ylabel, fname, title_iid, title_burst, hline=None, ylims=((0, 1.02),)):
    """One row per entry of ``ylims`` (full range first, optional zoomed range second)."""
    nrow = len(ylims)
    fig, axs = plt.subplots(nrow, 2, figsize=(7.6, 2.8 * nrow + 0.5), sharey="row", squeeze=False)
    for r, ylim in enumerate(ylims):
        for ax, kind, title in zip(axs[r], ("iid", "burst"), (title_iid, title_burst)):
            conds = [("iid_0", 0)] + [(f"{kind}_{p}", p) for p in (10, 30, 50)]
            for m in MAIN:
                mu = np.array([_s(summ, m, c, metric)[0] for c, _ in conds])
                ci = np.array([_s(summ, m, c, metric)[1] for c, _ in conds])
                x = [p for _, p in conds]
                ax.plot(x, mu, label=LABEL[m], **_style(m), zorder=3 if m == "rascm" else 2)
                ax.fill_between(x, mu - ci, mu + ci, color=COLORS[m], alpha=0.12, lw=0)
            if hline is not None:
                ax.axhline(hline, color=MUTED, lw=1, ls=":")
            ax.set_xticks([0, 10, 30, 50]); ax.set_ylim(*ylim)
            ax.set_title(title if r == 0 else "zoom on the upper range", fontsize=9 if r else 10)
            if r == nrow - 1:
                ax.set_xlabel("average packet-loss rate (%)")
        axs[r][0].set_ylabel(ylabel)
    h, l = axs[0][0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, fontsize=9, bbox_to_anchor=(0.5, -0.03))
    fig.tight_layout(rect=(0, 0.12 if nrow == 1 else 0.08, 1, 1))
    fig.savefig(FIG / fname, bbox_inches="tight"); plt.close(fig)


def pr_curves():
    files = sorted(glob.glob(str(RAW / "curves_seed0.json")))
    if not files:
        return
    cur = json.load(open(files[0]))
    conds = [("iid_0", "no packet loss"), ("iid_50", "iid loss 50%"), ("burst_50", "burst loss 50%"), ("targeted_30", "30% loss + targeted blackout")]
    fig, axs = plt.subplots(1, 4, figsize=(9.4, 2.9), sharey=True, sharex=True)
    for ax, (c, t) in zip(axs, conds):
        for m in MAIN:
            k = f"{m}|{c}"
            if k in cur:
                ax.plot(cur[k]["recall"], cur[k]["precision"], label=LABEL[m], color=COLORS[m], ls="--" if m in DASHED else "-",
                        lw=2.2 if m == "rascm" else 1.4, zorder=3 if m == "rascm" else 2)
        ax.set_title(t); ax.set_xlabel("recall"); ax.set_xlim(0, 1); ax.set_ylim(0, 1.02)
    axs[0].set_ylabel("precision")
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, fontsize=9, bbox_to_anchor=(0.5, -0.12))
    fig.tight_layout(rect=(0, 0.12, 1, 1)); fig.savefig(FIG / "fig_pr_curves.png", bbox_inches="tight"); plt.close(fig)


def forest(ht, fname):
    conds = ["iid_0", "iid_30", "iid_50", "burst_30", "burst_50", "nodeburst_30", "targeted_30", "gen_n20"]
    refs = [("best_conventional", "vs. best conventional GNN (per seed)"), ("physics_aoi", "vs. physics (AoI-aware)")]
    fig, axs = plt.subplots(1, 2, figsize=(7.8, 3.4), sharey=True)
    for ax, (ref, title) in zip(axs, refs):
        for i, c in enumerate(conds):
            r = ht[(ht.condition == c) & (ht.reference == ref)]
            if not len(r):
                continue
            r = r.iloc[0]
            col = COLORS["rascm"] if r.supports_H1 else (COLORS["physics_naive"] if r.ci_high < 0 else MUTED)
            ax.errorbar(r.mean_diff, i, xerr=[[r.mean_diff - r.ci_low], [r.ci_high - r.mean_diff]], fmt="o", color=col, capsize=3, mfc=col)
        ax.axvline(0, color=INK2, lw=1); ax.axvspan(0, 0.02, color=GRID, alpha=0.6, lw=0)
        ax.set_yticks(range(len(conds))); ax.set_yticklabels([COND[c] for c in conds])
        ax.set_xlabel("paired ΔPR-AUC (RA-SCM − reference)"); ax.set_title(title)
    axs[0].invert_yaxis()   # the y axis is shared: invert once, otherwise the two calls cancel
    fig.tight_layout(); fig.savefig(FIG / fname, bbox_inches="tight"); plt.close(fig)


def ablation(ab, fname):
    conds = ["iid_0", "iid_50", "burst_50", "nodeburst_30", "targeted_30"]
    abls = ["rascm_no_rel", "rascm_no_weight", "rascm_no_sheaf", "rascm_no_temporal", "mpnn_e"]
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    h = 0.14
    for j, a in enumerate(abls):
        for i, c in enumerate(conds):
            r = ab[(ab.condition == c) & (ab.reference == a)]
            if not len(r):
                continue
            r = r.iloc[0]
            y = i + (j - 2) * h
            ax.errorbar(r.mean_diff, y, xerr=[[r.mean_diff - r.ci_low], [r.ci_high - r.mean_diff]], fmt="o", ms=4.5,
                        color=COLORS[a], capsize=2, label=LABEL[a] if i == 0 else None)
    ax.axvline(0, color=INK2, lw=1)
    ax.set_yticks(range(len(conds))); ax.set_yticklabels([COND[c] for c in conds]); ax.invert_yaxis()
    ax.set_xlabel("paired ΔPR-AUC (full RA-SCM − ablated variant), 95% CI")
    ax.legend(fontsize=9, loc="lower right")
    fig.tight_layout(); fig.savefig(FIG / fname, bbox_inches="tight"); plt.close(fig)


def generalization(summ, fname):
    conds = ["gen_ref", "gen_n5", "gen_n20", "gen_lissajous", "gen_grid"]
    names = ["in-distribution", "5 UAVs", "20 UAVs", "unseen\ntrajectory", "unseen\nformation"]
    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    w = 0.11
    for j, m in enumerate(MAIN):
        mu = [_s(summ, m, c, "pr_auc")[0] for c in conds]; ci = [_s(summ, m, c, "pr_auc")[1] for c in conds]
        ax.bar(np.arange(len(conds)) + (j - 3) * w, mu, w * 0.88, yerr=ci, color=COLORS[m], label=LABEL[m], error_kw=dict(lw=1, capsize=1.5, ecolor=INK2),
               hatch="//" if m in DASHED else None, edgecolor=SURFACE if m not in DASHED else COLORS[m], lw=0.6)
    ax.set_xticks(range(len(conds))); ax.set_xticklabels(names); ax.set_ylabel("PR-AUC"); ax.set_ylim(0, 1.02)
    ax.legend(ncol=4, fontsize=8.5, loc="lower center", bbox_to_anchor=(0.5, -0.46))
    fig.tight_layout(); fig.savefig(FIG / fname, bbox_inches="tight"); plt.close(fig)


def delay(summ, fname):
    kinds = ["sudden", "drift", "spoof"]
    fig, axs = plt.subplots(1, 3, figsize=(8.2, 3.2), sharey=True)
    for ax, k in zip(axs, kinds):
        for p, off in ((0, -0.15), (30, 0.15)):
            for j, m in enumerate(MAIN):
                mu, ci = _s(summ, m, f"type_{k}_{p}", "delay_median_s")
                ax.errorbar(j + off, mu, yerr=ci, fmt="o" if p == 0 else "^", color=COLORS[m], mfc=COLORS[m] if p == 0 else SURFACE, capsize=2, ms=5)
        ax.set_xticks(range(len(MAIN))); ax.set_xticklabels([SHORT[m] for m in MAIN], rotation=60, ha="right", fontsize=9)
        ax.set_title(f"{k} anomalies")
    axs[0].set_ylabel("median detection delay (s)")
    fig.tight_layout(); fig.savefig(FIG / fname, bbox_inches="tight"); plt.close(fig)


def latency(fname):
    f = TAB / "latency.csv"
    if not f.exists():
        return
    d = pd.read_csv(f)
    fig, axs = plt.subplots(1, 2, figsize=(7.8, 3.3))
    for m in MAIN:
        g = d[d.model == m]
        lab = "Physics (naive / AoI-aware, identical)" if m == "physics_aoi" else (None if m == "physics_naive" else LABEL[m])
        axs[0].plot(g.n_uavs, g.ms_per_step, label=lab, **_style(m))
    axs[0].set_yscale("log"); axs[0].set_yticks([0.02, 0.05, 0.1, 0.2, 0.5, 1.0])
    axs[0].yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter()); axs[0].yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    axs[0].set_xticks([5, 10, 20]); axs[0].set_xlabel("UAVs"); axs[0].set_ylabel("ms per swarm step (amortised)")
    g = d[d.n_uavs == 10].set_index("model").loc[[m for m in MAIN if m not in DASHED]]
    axs[1].barh([LABEL[m] for m in g.index], g.n_params, color=[COLORS[m] for m in g.index])
    axs[1].set_xlabel("trainable parameters"); axs[1].invert_yaxis()
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, fontsize=8.5, bbox_to_anchor=(0.5, -0.12))
    fig.tight_layout(rect=(0, 0.12, 1, 1)); fig.savefig(FIG / fname, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    summ = pd.read_csv(TAB / "summary_long.csv")
    sweep(summ, "pr_auc", "PR-AUC (average precision)", "fig_pr_auc_vs_loss.png", "iid packet loss (E1/E2)", "Gilbert–Elliott burst loss (E3)", ylims=((0.4, 1.01), (0.86, 1.0)))
    sweep(summ, "fpr", "FPR at frozen threshold", "fig_fpr_vs_loss.png", "iid packet loss", "burst packet loss", hline=0.05,
          ylims=((0, 0.25),))
    pr_curves()
    if (TAB / "hypothesis_test.csv").exists():
        forest(pd.read_csv(TAB / "hypothesis_test.csv"), "fig_hypothesis_forest.png")
        ablation(pd.read_csv(TAB / "ablation_paired.csv"), "fig_ablation.png")
    generalization(summ, "fig_generalization.png")
    delay(summ, "fig_delay.png")
    latency("fig_latency.png")
    print("figures written to", FIG)
