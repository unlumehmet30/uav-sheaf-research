"""Figures for the report from results/tables/*.csv and results/raw/curves_seed*.json.
Usage: python -m experiments.make_figures
Colour follows the model (fixed entity->slot map, validated reference palette); baselines that are
not learned use dashed lines + hollow markers as a second encoding channel.
"""
from __future__ import annotations

import glob
import json

import matplotlib

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
LABEL = {"rascm": "RA-SCM (proposed)", "nsd": "NSD-style sheaf", "gcn": "GCN", "gat": "GAT", "gcn_drop": "GCN (drop lost links)",
         "physics_aoi": "Physics (AoI-aware)", "physics_naive": "Physics (naive)",
         "rascm_no_rel": "− reliability info", "rascm_no_weight": "− reliability weights", "rascm_no_sheaf": "− sheaf maps (identity)",
         "rascm_no_temporal": "− temporal (GRU)", "mpnn_e": "− sheaf − weights (MPNN-E)"}
DASHED = {"physics_aoi", "physics_naive"}
MAIN = ["physics_naive", "physics_aoi", "gcn", "gcn_drop", "gat", "nsd", "rascm"]

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": "#c3c2b7", "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
    "text.color": INK, "font.family": "sans-serif", "font.size": 9, "axes.titlesize": 10, "axes.titleweight": "regular",
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.axisbelow": True, "legend.frameon": False, "lines.linewidth": 1.8, "lines.markersize": 5, "figure.dpi": 150,
})


def _s(summ, model, cond, metric):
    r = summ[(summ.model == model) & (summ.condition == cond) & (summ.metric == metric)]
    return (r["mean"].iloc[0], r["ci_half"].iloc[0]) if len(r) else (np.nan, np.nan)


def _style(m):
    return dict(color=COLORS[m], ls="--" if m in DASHED else "-", marker="o" if m not in DASHED else "s",
                mfc=SURFACE if m in DASHED else COLORS[m], mec=COLORS[m], mew=1.4)


def sweep(summ, metric, ylabel, fname, title_iid, title_burst, hline=None, ylim=None):
    fig, axs = plt.subplots(1, 2, figsize=(9.2, 3.5), sharey=True)
    for ax, kind, title in zip(axs, ("iid", "burst"), (title_iid, title_burst)):
        conds = [("iid_0", 0)] + [(f"{kind}_{p}", p) for p in (10, 30, 50)]
        for m in MAIN:
            mu = np.array([_s(summ, m, c, metric)[0] for c, _ in conds])
            ci = np.array([_s(summ, m, c, metric)[1] for c, _ in conds])
            x = [p for _, p in conds]
            ax.plot(x, mu, label=LABEL[m], **_style(m), zorder=3 if m == "rascm" else 2)
            ax.fill_between(x, mu - ci, mu + ci, color=COLORS[m], alpha=0.12, lw=0)
        if hline is not None:
            ax.axhline(hline, color=MUTED, lw=1, ls=":")
        ax.set_xticks([0, 10, 30, 50]); ax.set_xlabel("average packet-loss rate (%)"); ax.set_title(title)
        if ylim: ax.set_ylim(*ylim)
    axs[0].set_ylabel(ylabel)
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, fontsize=8, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    fig.savefig(FIG / fname, bbox_inches="tight"); plt.close(fig)


def pr_curves():
    files = sorted(glob.glob(str(RAW / "curves_seed0.json")))
    if not files:
        return
    cur = json.load(open(files[0]))
    conds = [("iid_0", "no packet loss"), ("iid_50", "iid loss 50%"), ("burst_50", "burst loss 50%"), ("targeted_30", "30% loss + targeted blackout")]
    fig, axs = plt.subplots(1, 4, figsize=(11, 2.9), sharey=True, sharex=True)
    for ax, (c, t) in zip(axs, conds):
        for m in MAIN:
            k = f"{m}|{c}"
            if k in cur:
                ax.plot(cur[k]["recall"], cur[k]["precision"], label=LABEL[m], color=COLORS[m], ls="--" if m in DASHED else "-",
                        lw=2.2 if m == "rascm" else 1.4, zorder=3 if m == "rascm" else 2)
        ax.set_title(t); ax.set_xlabel("recall"); ax.set_xlim(0, 1); ax.set_ylim(0, 1.02)
    axs[0].set_ylabel("precision")
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=7, fontsize=7.5, bbox_to_anchor=(0.5, -0.06))
    fig.tight_layout(rect=(0, 0.08, 1, 1)); fig.savefig(FIG / "fig_pr_curves.png", bbox_inches="tight"); plt.close(fig)


def forest(ht, fname):
    conds = ["iid_0", "iid_30", "iid_50", "burst_30", "burst_50", "nodeburst_30", "targeted_30", "gen_n20"]
    refs = [("best_conventional", "vs. best conventional GNN (per seed)"), ("physics_aoi", "vs. physics (AoI-aware)")]
    fig, axs = plt.subplots(1, 2, figsize=(9.2, 3.4), sharey=True)
    for ax, (ref, title) in zip(axs, refs):
        for i, c in enumerate(conds):
            r = ht[(ht.condition == c) & (ht.reference == ref)]
            if not len(r):
                continue
            r = r.iloc[0]
            col = COLORS["rascm"] if r.supports_H1 else (COLORS["physics_naive"] if r.ci_high < 0 else MUTED)
            ax.errorbar(r.mean_diff, i, xerr=[[r.mean_diff - r.ci_low], [r.ci_high - r.mean_diff]], fmt="o", color=col, capsize=3, mfc=col)
        ax.axvline(0, color=INK2, lw=1); ax.axvspan(0, 0.02, color=GRID, alpha=0.6, lw=0)
        ax.set_yticks(range(len(conds))); ax.set_yticklabels(conds); ax.invert_yaxis()
        ax.set_xlabel("paired ΔPR-AUC (RA-SCM − reference), 95% CI"); ax.set_title(title)
    fig.text(0.5, -0.02, "blue: H1 criterion met (CI > 0 and Δ ≥ 0.02, shaded band)   red: reference significantly better   grey: inconclusive",
             ha="center", fontsize=8, color=INK2)
    fig.tight_layout(); fig.savefig(FIG / fname, bbox_inches="tight"); plt.close(fig)


def ablation(ab, fname):
    conds = ["iid_0", "iid_30", "iid_50", "burst_50", "targeted_30"]
    abls = ["rascm_no_rel", "rascm_no_weight", "rascm_no_sheaf", "rascm_no_temporal", "mpnn_e"]
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
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
    ax.set_yticks(range(len(conds))); ax.set_yticklabels(conds); ax.invert_yaxis()
    ax.set_xlabel("paired ΔPR-AUC (full RA-SCM − ablated variant), 95% CI;  >0: removed component helped")
    ax.legend(fontsize=8, loc="best")
    fig.tight_layout(); fig.savefig(FIG / fname, bbox_inches="tight"); plt.close(fig)


def generalization(summ, fname):
    conds = ["gen_ref", "gen_n5", "gen_n20", "gen_lissajous", "gen_grid"]
    names = ["in-distribution", "5 UAVs", "20 UAVs", "unseen trajectory", "unseen formation"]
    fig, ax = plt.subplots(figsize=(8.6, 3.4))
    w = 0.11
    for j, m in enumerate(MAIN):
        mu = [_s(summ, m, c, "pr_auc")[0] for c in conds]; ci = [_s(summ, m, c, "pr_auc")[1] for c in conds]
        ax.bar(np.arange(len(conds)) + (j - 3) * w, mu, w * 0.88, yerr=ci, color=COLORS[m], label=LABEL[m], error_kw=dict(lw=1, capsize=1.5, ecolor=INK2),
               hatch="//" if m in DASHED else None, edgecolor=SURFACE if m not in DASHED else COLORS[m], lw=0.6)
    ax.set_xticks(range(len(conds))); ax.set_xticklabels(names); ax.set_ylabel("PR-AUC"); ax.set_ylim(0, 1.02)
    ax.legend(ncol=4, fontsize=7.5, loc="lower center", bbox_to_anchor=(0.5, -0.32))
    fig.tight_layout(); fig.savefig(FIG / fname, bbox_inches="tight"); plt.close(fig)


def delay(summ, fname):
    kinds = ["sudden", "drift", "spoof"]
    fig, axs = plt.subplots(1, 3, figsize=(10, 3.2), sharey=True)
    for ax, k in zip(axs, kinds):
        for p, off in ((0, -0.15), (30, 0.15)):
            for j, m in enumerate(MAIN):
                mu, ci = _s(summ, m, f"type_{k}_{p}", "delay_median_s")
                ax.errorbar(j + off, mu, yerr=ci, fmt="o" if p == 0 else "^", color=COLORS[m], mfc=COLORS[m] if p == 0 else SURFACE, capsize=2, ms=5)
        ax.set_xticks(range(len(MAIN))); ax.set_xticklabels([LABEL[m].split(" (")[0].replace("Physics", "Phys.") + (" AoI" if m == "physics_aoi" else "") for m in MAIN], rotation=60, ha="right", fontsize=7.5)
        ax.set_title(f"{k} anomalies")
    axs[0].set_ylabel("median detection delay (s)")
    axs[1].text(0.5, -0.5, "filled circles: no loss   hollow triangles: 30% iid loss   (delay over detected UAVs only; see detection rate)", transform=axs[1].transAxes, ha="center", fontsize=8, color=INK2)
    fig.tight_layout(); fig.savefig(FIG / fname, bbox_inches="tight"); plt.close(fig)


def latency(fname):
    f = TAB / "latency.csv"
    if not f.exists():
        return
    d = pd.read_csv(f)
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.2))
    for m in MAIN:
        g = d[d.model == m]
        axs[0].plot(g.n_uavs, g.ms_per_step, label=LABEL[m], **_style(m))
    axs[0].set_yscale("log"); axs[0].set_xticks([5, 10, 20]); axs[0].set_xlabel("UAVs"); axs[0].set_ylabel("ms per swarm step (amortised)")
    g = d[d.n_uavs == 10].set_index("model").loc[[m for m in MAIN if m not in DASHED]]
    axs[1].barh([LABEL[m] for m in g.index], g.n_params, color=[COLORS[m] for m in g.index])
    axs[1].set_xlabel("trainable parameters"); axs[1].invert_yaxis()
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, fontsize=7.5, bbox_to_anchor=(0.5, -0.1))
    fig.tight_layout(rect=(0, 0.08, 1, 1)); fig.savefig(FIG / fname, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    summ = pd.read_csv(TAB / "summary_long.csv")
    sweep(summ, "pr_auc", "PR-AUC (average precision)", "fig_pr_auc_vs_loss.png", "iid packet loss (E1/E2)", "Gilbert–Elliott burst loss (E3)", ylim=(0, 1.02))
    sweep(summ, "fpr", "false-positive rate at frozen threshold", "fig_fpr_vs_loss.png", "iid packet loss", "burst packet loss", hline=0.05)
    pr_curves()
    if (TAB / "hypothesis_test.csv").exists():
        forest(pd.read_csv(TAB / "hypothesis_test.csv"), "fig_hypothesis_forest.png")
        ablation(pd.read_csv(TAB / "ablation_paired.csv"), "fig_ablation.png")
    generalization(summ, "fig_generalization.png")
    delay(summ, "fig_delay.png")
    latency("fig_latency.png")
    print("figures written to", FIG)
