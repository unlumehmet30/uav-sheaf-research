"""Fills {{...}} placeholders in the report markdown with numbers read from results/tables/*.csv, so no result number in
the report is typed by hand (design parameters are copied from configs/default.yaml).

  {{m:model:condition:metric[:digits]}}   mean over seeds           e.g. {{m:rascm:iid_50:pr_auc}}
  {{mc:model:condition:metric}}           mean ± 95% t half-width   e.g. 0.975 ±.012
  {{dh:condition:reference}}              paired PR-AUC diff RA-SCM − reference with CI from hypothesis_test.csv
  {{da:condition:ablation}}               paired diff full − ablation from ablation_paired.csv
  {{dd:model:cond0:cond1:metric}}         mean(cond1) − mean(cond0)
  {{tbl:name}}                            generated markdown table
  {{n:name}}                              named scalar (see SCALARS)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "results" / "tables"
LABEL = {"physics_naive": "Physics (naive)", "physics_aoi": "Physics (AoI-aware)", "gcn": "GCN", "gcn_drop": "GCN-drop", "gat": "GAT",
         "nsd": "NSD-style sheaf", "rascm": "**RA-SCM**", "rascm_no_rel": "− reliability info", "rascm_no_weight": "− reliability weights",
         "rascm_no_sheaf": "− sheaf maps (F = I)", "rascm_no_temporal": "− temporal (GRU)", "mpnn_e": "− maps − weights (MPNN-E)"}
MAIN = ["physics_naive", "physics_aoi", "gcn", "gcn_drop", "gat", "nsd", "rascm"]
ABL = ["rascm_no_rel", "rascm_no_weight", "rascm_no_sheaf", "rascm_no_temporal", "mpnn_e"]
CONVENTIONAL = ["gcn", "gat", "gcn_drop", "nsd"]
CSTAR = ["iid_30", "iid_50", "burst_30", "burst_50", "nodeburst_30", "targeted_30"]
COND = {"iid_0": "iid 0%", "iid_30": "iid 30%", "iid_50": "iid 50%", "burst_30": "burst 30%", "burst_50": "burst 50%",
        "nodeburst_30": "rx-burst 30%", "targeted_30": "targeted 30%"}


def num(x: float, digits: int = 3, sign: bool = False) -> str:
    """Formats a number with a typographic minus; a value that rounds to zero is printed without a sign."""
    s = f"{x:+.{digits}f}" if sign else f"{x:.{digits}f}"
    if float(s) == 0:
        s = f"{0:.{digits}f}" if not sign or x >= 0 else "−" + f"{0:.{digits}f}"
    return s.replace("-", "−")


def _load():
    S = pd.read_csv(TAB / "summary_long.csv")
    H = pd.read_csv(TAB / "hypothesis_test.csv") if (TAB / "hypothesis_test.csv").exists() else pd.DataFrame()
    A = pd.read_csv(TAB / "ablation_paired.csv") if (TAB / "ablation_paired.csv").exists() else pd.DataFrame()
    L = pd.read_csv(TAB / "latency.csv") if (TAB / "latency.csv").exists() else pd.DataFrame()
    return S, H, A, L


S, H, A, L = _load()


def _row(model, cond, metric):
    r = S[(S.model == model) & (S.condition == cond) & (S.metric == metric)]
    if not len(r):
        return None
    return r.iloc[0]


def fmt_ci(model, cond, metric, digits=3):
    r = _row(model, cond, metric)
    if r is None or np.isnan(r["mean"]):
        return "n/a"
    ci = f"{r['ci_half']:.{digits}f}".lstrip("0") if r["ci_half"] < 1 else f"{r['ci_half']:.{digits}f}"
    return f"{r['mean']:.{digits}f} ±{ci}"


def fmt_m(model, cond, metric, digits=3):
    r = _row(model, cond, metric)
    return "n/a" if r is None or np.isnan(r["mean"]) else f"{r['mean']:.{digits}f}"


def fmt_diff(df, cond, ref):
    if df.empty:
        return "n/a"
    r = df[(df.condition == cond) & (df.reference == ref)]
    if not len(r):
        return "n/a"
    r = r.iloc[0]
    mean = num(r.mean_diff) if abs(r.mean_diff) < 0.0005 else num(r.mean_diff, sign=True)
    return f"{mean} [{num(r.ci_low, sign=True)}, {num(r.ci_high, sign=True)}]"


def table_main():
    conds = ["iid_0", "iid_30", "iid_50", "burst_30", "burst_50", "nodeburst_30", "targeted_30"]
    hdr = "| PR-AUC | iid 0% | iid 30% | iid 50% | burst 30% | burst 50% | rx-burst 30% | targeted 30% |\n|:--|--:|--:|--:|--:|--:|--:|--:|\n"
    rows = [f"| {LABEL[m]} | " + " | ".join(fmt_ci(m, c, "pr_auc") for c in conds) + " |" for m in MAIN]
    return hdr + "\n".join(rows)


def table_secondary():
    out = "| model | FPR iid 0% | FPR iid 50% | FPR burst 50% | FPR noise ×3 | recall iid 50% | recall burst 50% | delay burst 50% [s] | detect rate burst 50% |\n|:--|--:|--:|--:|--:|--:|--:|--:|--:|\n"
    for m in MAIN:
        out += (f"| {LABEL[m]} | {fmt_m(m, 'iid_0', 'fpr')} | {fmt_m(m, 'iid_50', 'fpr')} | {fmt_m(m, 'burst_50', 'fpr')} | {fmt_m(m, 'noise_3', 'fpr')} | "
                f"{fmt_m(m, 'iid_50', 'recall')} | {fmt_m(m, 'burst_50', 'recall')} | {fmt_m(m, 'burst_50', 'delay_median_s', 2)} | {fmt_m(m, 'burst_50', 'detect_rate', 2)} |\n")
    return out.rstrip()


def table_hypothesis():
    if H.empty:
        return "(hypothesis table not available)"
    conds = ["iid_30", "iid_50", "burst_30", "burst_50", "nodeburst_30", "targeted_30"]
    out = "| condition | Δ vs best conventional GNN [95% CI] | H1 met? | Δ vs AoI-aware physics [95% CI] |\n|:--|:--|:--:|:--|\n"
    for c in conds:
        r = H[(H.condition == c) & (H.reference == "best_conventional")]
        met = "yes" if len(r) and bool(r.iloc[0].supports_H1) else "no"
        out += f"| {COND[c]} | {fmt_diff(H, c, 'best_conventional')} | {met} | {fmt_diff(H, c, 'physics_aoi')} |\n"
    return out.rstrip()


def table_ablation():
    if A.empty:
        return "(ablation table not available)"
    conds = ["iid_0", "iid_50", "burst_50", "nodeburst_30", "targeted_30"]
    out = "| removed component | " + " | ".join(COND[c] for c in conds) + " |\n|:--|" + "--:|" * len(conds) + "\n"
    for a in ABL:
        out += f"| {LABEL[a]} | " + " | ".join(fmt_diff(A, c, a) for c in conds) + " |\n"
    return out.rstrip()


def table_cost():
    par = S.drop_duplicates("model")
    out = "| model | parameters | ms per swarm step, N=5 / 10 / 20 | train time per seed [min] |\n|:--|--:|:--|--:|\n"
    raw = pd.concat([pd.read_csv(f) for f in sorted((ROOT / "results" / "raw").glob("metrics_seed*.csv"))])
    meta = raw.groupby("model")[["n_params", "train_s"]].mean()
    for m in MAIN + ABL:
        if m not in meta.index:
            continue
        lat = " / ".join((f"{L[(L.model == m) & (L.n_uavs == n)].ms_per_step.iloc[0]:.2f}" if (not L.empty and len(L[(L.model == m) & (L.n_uavs == n)])) else "n/a") for n in (5, 10, 20))
        out += f"| {LABEL[m]} | {int(meta.loc[m, 'n_params'])} | {lat} | {meta.loc[m, 'train_s'] / 60:.1f} |\n"
    return out.rstrip()


TABLES = {"main": table_main, "secondary": table_secondary, "hypothesis": table_hypothesis, "ablation": table_ablation, "cost": table_cost}


def scalars() -> dict:
    raw = pd.concat([pd.read_csv(f) for f in sorted((ROOT / "results" / "raw").glob("metrics_seed*.csv"))])
    env = json.loads((ROOT / "results" / "env.json").read_text())
    rascm_tr = raw[raw.model == "rascm"].drop_duplicates("seed").train_s
    total_train = raw.drop_duplicates(["seed", "model"]).groupby("seed").train_s.sum()
    pos = raw[(raw.condition == "iid_0")].drop_duplicates("seed").pos_rate.mean()
    nd = H[(H.reference == "best_conventional") & H.condition.isin(["iid_30", "iid_50", "burst_30", "burst_50", "nodeburst_30", "targeted_30"])]
    ndp = H[(H.reference == "physics_aoi") & H.condition.isin(["iid_30", "iid_50", "burst_30", "burst_50", "nodeburst_30", "targeted_30"])]
    keyc = ["iid_0", "iid_50", "burst_50", "nodeburst_30", "targeted_30"]
    sh = A[(A.reference == "rascm_no_sheaf") & A.condition.isin(keyc)] if not A.empty else A
    single = H[H.reference.isin(CONVENTIONAL) & H.condition.isin(CSTAR)]
    # seed-to-seed SD of the paired difference, recovered from the t-interval, and the effect a 95% interval would
    # exclude 0 for with 80% probability (post hoc, n = number of seeds)
    from scipy import stats
    n = int(nd.n_seeds.iloc[0]) if len(nd) else 5
    t975, t80 = stats.t.ppf(0.975, n - 1), stats.t.ppf(0.80, n - 1)
    sd = (nd.ci_high - nd.ci_low) / 2 * np.sqrt(n) / t975
    mde = (t975 + t80) * sd / np.sqrt(n)
    other = raw[~raw.condition.isin(["iid_0", "iid_10", "iid_30", "iid_50", "burst_10", "burst_30", "burst_50", "nodeburst_30",
                                     "targeted_10", "targeted_30", "topo_30", "topo_0"])].groupby("condition").pos_rate.mean()
    lat = {m: L[(L.model == m) & (L.n_uavs == 10)].ms_per_step for m in ("rascm", "gat")} if not L.empty else {}
    gat = H[(H.reference == "gat") & H.condition.isin(CSTAR)].mean_diff
    return {
        "gat_gap": f"{gat.min():.2f}–{gat.max():.2f}" if len(gat) else "n/a",
        "phys_gap": f"{ndp.mean_diff.min():.2f}–{ndp.mean_diff.max():.2f}" if len(ndp) else "n/a",
        "lat_rascm10": f"{lat['rascm'].iloc[0]:.2f}" if len(lat.get("rascm", [])) else "n/a",
        "lat_gat10": f"{lat['gat'].iloc[0]:.2f}" if len(lat.get("gat", [])) else "n/a",
        "single_pairs": str(len(single)),
        "single_ci_pos": str(int((single.ci_low > 0).sum())),
        "single_h1": str(int(single.supports_H1.sum())),
        "single_h1_gcn": str(int(single[single.reference == "gcn"].supports_H1.sum())),
        "phys_better": str(int((ndp.ci_low > 0).sum())),
        "sd_range": f"{sd.min():.3f}–{sd.max():.3f}",
        "mde_range": f"{mde.min():.3f}–{mde.max():.3f}",
        "pos_rate_other": f"{other.min():.3f}–{other.max():.3f}" if len(other) else "n/a",
        "sheaf_maxabs": f"{sh.mean_diff.abs().max():.3f}" if len(sh) else "n/a",
        "sheaf_ci0": f"{int(((sh.ci_low <= 0) & (sh.ci_high >= 0)).sum())} of {len(sh)}" if len(sh) else "n/a",
        "n_seeds": str(raw.seed.nunique()),
        "wall_min_per_seed": f"{total_train.mean() / 60:.0f}",
        "rascm_train_min": f"{rascm_tr.mean() / 60:.0f}",
        "pos_rate": f"{pos:.3f}",
        "cpu": f"{env.get('cpu_model', env['machine'])}, {env['cpu_count']} logical cores, {env['ram_gb']:.0f} GB RAM",
        "h1_count": str(int(nd.supports_H1.sum())),
        "h1_total": str(len(nd)),
        "ci_zero_count": str(int((nd.ci_low <= 0).sum())),
        "phys_notbetter": str(int((ndp.mean_diff <= 0).sum())),
    }


def fill(md: str) -> str:
    sc = scalars() if (TAB / "hypothesis_test.csv").exists() else {}

    def rep(m):
        kind, rest = m.group(1), m.group(2)
        a = rest.split(":")
        if kind == "m":
            return fmt_m(a[0], a[1], a[2], int(a[3]) if len(a) > 3 else 3)
        if kind == "mc":
            return fmt_ci(a[0], a[1], a[2])
        if kind == "dh":
            return fmt_diff(H, a[0], a[1])
        if kind == "da":
            return fmt_diff(A, a[0], a[1])
        if kind == "dd":      # difference of means: cond1 - cond0
            r0, r1 = _row(a[0], a[1], a[3]), _row(a[0], a[2], a[3])
            return "n/a" if r0 is None or r1 is None else num(r1['mean'] - r0['mean'], sign=True)
        if kind == "tbl":
            return TABLES[a[0]]()
        if kind == "n":
            return sc.get(a[0], "n/a")
        raise ValueError(kind)

    return re.sub(r"\{\{(\w+):([^}]*)\}\}", rep, md)
