"""Aggregate per-seed metric tables into summary tables and the pre-registered hypothesis test.

Outputs (results/tables/):
    summary_long.csv        model x condition x metric: mean, 95% t-CI half width over seeds, n
    results_summary.md      human-readable tables for Experiments 1-7
    hypothesis_test.csv     paired differences RA-SCM vs each competitor (+ per-seed best conventional GNN)
    ablation_paired.csv     paired differences full RA-SCM minus each ablation
Usage: python -m experiments.aggregate
"""
from __future__ import annotations

import glob

import numpy as np
import pandas as pd

from experiments.common import ROOT
from src.evaluation.metrics import paired_diff, t_ci

RAW = ROOT / "results" / "raw"
TAB = ROOT / "results" / "tables"
METRICS = ["pr_auc", "roc_auc", "precision", "recall", "f1", "fpr", "detect_rate", "delay_median_s"]
CONVENTIONAL = ["gcn", "gat", "gcn_drop", "nsd"]
COMPETITORS = ["physics_naive", "physics_aoi", "gcn", "gat", "gcn_drop", "nsd"]
ABLATIONS = ["rascm_no_rel", "rascm_no_weight", "rascm_no_sheaf", "rascm_no_temporal", "mpnn_e"]
MIN_EFFECT = 0.02          # smallest PR-AUC difference regarded as practically relevant (pre-registered)
KEY_CONDS = ["iid_0", "iid_10", "iid_30", "iid_50", "burst_30", "burst_50", "nodeburst_30",
             "targeted_10", "targeted_30"]


def load() -> pd.DataFrame:
    files = sorted(glob.glob(str(RAW / "metrics_seed*.csv")))
    if not files:
        raise SystemExit("no raw metrics found; run experiments/run_main.py first")
    return pd.concat([pd.read_csv(f) for f in files], ignore_index=True)


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (m, c), g in df.groupby(["model", "condition"]):
        for k in METRICS:
            mean, half, _ = t_ci(g[k].values)
            rows.append({"model": m, "condition": c, "exp": g["exp"].iloc[0], "metric": k, "mean": mean,
                         "ci_half": half, "n_seeds": g[k].notna().sum()})
    return pd.DataFrame(rows)


def _wide(df, metric, models, conds, digits=3):
    out = {}
    for m in models:
        row = {}
        for c in conds:
            g = df[(df.model == m) & (df.condition == c)][metric].values
            mean, half, _ = t_ci(g)
            row[c] = f"{mean:.{digits}f} ± {half:.{digits}f}" if not np.isnan(mean) else "n/a"
        out[m] = row
    return pd.DataFrame(out).T


def paired_table(df: pd.DataFrame, a: str, others, conds, metric="pr_auc") -> pd.DataFrame:
    rows = []
    for c in conds:
        pa = df[(df.model == a) & (df.condition == c)].set_index("seed")[metric]
        for o in others:
            if o == "best_conventional":
                ref = df[(df.model.isin(CONVENTIONAL)) & (df.condition == c)].pivot(index="seed", columns="model", values=metric).max(1)
            else:
                ref = df[(df.model == o) & (df.condition == c)].set_index("seed")[metric]
            seeds = sorted(set(pa.index) & set(ref.index))
            d = paired_diff(pa.loc[seeds].values, ref.loc[seeds].values)
            lo = d["mean"] - d["half"] if not np.isnan(d["half"]) else float("nan")
            rows.append({"condition": c, "model": a, "reference": o, "metric": metric, "mean_diff": d["mean"],
                         "ci_low": lo, "ci_high": d["mean"] + d["half"], "p_one_sided": d["p_greater"], "n_seeds": d["n"],
                         "supports_H1": bool(lo > 0 and d["mean"] >= MIN_EFFECT)})
    return pd.DataFrame(rows)


def main() -> None:
    TAB.mkdir(parents=True, exist_ok=True)
    df = load()
    seeds = sorted(df.seed.unique())
    summ = summarize(df)
    summ.to_csv(TAB / "summary_long.csv", index=False)
    all_conds = list(df.condition.unique())
    main_models = ["physics_naive", "physics_aoi", "gcn", "gcn_drop", "gat", "nsd", "rascm"]
    have = [m for m in main_models if m in set(df.model)]

    md = [f"# Results summary\n\nSeeds: {seeds} (n = {len(seeds)}). Cells: mean ± 95% t-interval half-width over seeds. "
          "PR-AUC = average precision (scikit-learn definition). All numbers come from `results/raw/`; "
          "operating point = threshold with 5% FPR on the validation split, frozen for all test conditions.\n"]

    def block(title, metric, conds, models=have, digits=3):
        md.append(f"\n## {title}\n")
        md.append(_wide(df, metric, models, [c for c in conds if c in all_conds], digits).to_markdown() + "\n")

    block("E1/E2 — PR-AUC vs iid packet loss", "pr_auc", ["iid_0", "iid_10", "iid_30", "iid_50"])
    block("E2 — FPR at the frozen operating point vs iid packet loss", "fpr", ["iid_0", "iid_10", "iid_30", "iid_50"])
    block("E2 — recall at the frozen operating point vs iid packet loss", "recall", ["iid_0", "iid_10", "iid_30", "iid_50"])
    block("E2 — noise severity (no packet loss), PR-AUC", "pr_auc", ["noise_1", "noise_2", "noise_3"])
    block("E2 — noise severity (no packet loss), FPR", "fpr", ["noise_1", "noise_2", "noise_3"])
    block("E3 — PR-AUC under burst / correlated loss", "pr_auc", ["burst_10", "burst_30", "burst_50", "nodeburst_30"])
    block("E3 — FPR under burst / correlated loss", "fpr", ["burst_10", "burst_30", "burst_50", "nodeburst_30"])
    block("E4 — PR-AUC: anomalies + communication failures", "pr_auc", ["targeted_10", "targeted_30", "topo_0", "topo_30"])
    block("E4 — recall: anomalies + communication failures", "recall", ["targeted_10", "targeted_30", "topo_0", "topo_30"])
    block("E4 — PR-AUC by anomaly type", "pr_auc", [f"type_{k}_{p}" for k in ("sudden", "drift", "spoof") for p in (0, 30)])
    block("E4 — detection delay (median, s) by anomaly type", "delay_median_s", [f"type_{k}_{p}" for k in ("sudden", "drift", "spoof") for p in (0, 30)], digits=2)
    block("E4 — detection rate by anomaly type", "detect_rate", [f"type_{k}_{p}" for k in ("sudden", "drift", "spoof") for p in (0, 30)], digits=2)
    block("E5 — generalisation (loss 30%): PR-AUC", "pr_auc", ["gen_ref", "gen_n5", "gen_n20", "gen_lissajous", "gen_grid"])
    block("E5 — generalisation (loss 30%): FPR", "fpr", ["gen_ref", "gen_n5", "gen_n20", "gen_lissajous", "gen_grid"])

    abl = [m for m in ["rascm"] + ABLATIONS if m in set(df.model)]
    md.append("\n## E6 — ablations, PR-AUC\n")
    md.append(_wide(df, "pr_auc", abl, [c for c in KEY_CONDS + ["gen_n20", "gen_lissajous"] if c in all_conds]).to_markdown() + "\n")

    par = (df.groupby("model")[["n_params", "train_s", "epochs"]].mean().round(1))
    md.append("\n## E7 — parameters and training cost (mean over seeds)\n")
    md.append(par.to_markdown() + "\n")

    # -------- hypothesis test --------
    if "rascm" in set(df.model):
        others = [o for o in COMPETITORS if o in set(df.model)]
        if any(m in set(df.model) for m in CONVENTIONAL):
            others.append("best_conventional")
        ht = paired_table(df, "rascm", others, all_conds)
        ht.to_csv(TAB / "hypothesis_test.csv", index=False)
        key = ht[ht.condition.isin(KEY_CONDS)]
        md.append("\n## Hypothesis test — paired PR-AUC difference (RA-SCM − reference), key conditions\n")
        md.append("`supports_H1` = lower 95% CI bound > 0 **and** mean difference ≥ 0.02 (pre-registered decision rule). "
                  "`best_conventional` = per-seed best of GCN/GAT/GCN-drop/NSD (conservative for the proposed model).\n\n")
        md.append(key.round(4).to_markdown(index=False) + "\n")
        sub = ht[ht.reference == "best_conventional"]
        md.append("\n### Summary over all conditions vs best conventional GNN\n")
        md.append(f"conditions where H1 supported: {int(sub.supports_H1.sum())} / {len(sub)}; "
                  f"conditions where the CI excludes 0 in favour of the baseline (mean diff < 0, CI high < 0): "
                  f"{int(((sub.ci_high < 0)).sum())} / {len(sub)}\n")
        ab = paired_table(df, "rascm", [a for a in ABLATIONS if a in set(df.model)], all_conds)
        ab.to_csv(TAB / "ablation_paired.csv", index=False)
        md.append("\n## Ablation — paired PR-AUC difference (full RA-SCM − ablation), key conditions\n")
        md.append("Positive = the removed component helped. \n\n" + ab[ab.condition.isin(KEY_CONDS)].round(4).to_markdown(index=False) + "\n")

    lat = TAB / "latency.csv"
    if lat.exists():
        md.append("\n## E7 — inference latency (CPU, batch 1)\n\n" + pd.read_csv(lat).round(3).to_markdown(index=False) + "\n")
    (TAB / "results_summary.md").write_text("\n".join(md))
    print("wrote", TAB / "results_summary.md")


if __name__ == "__main__":
    main()
