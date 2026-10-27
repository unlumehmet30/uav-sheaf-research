"""Streamlit dashboard: simulate a UAV swarm, inject anomalies / packet loss, run a detector, inspect results.

    streamlit run app.py

Everything shown is computed by the real pipeline in src/ (simulator -> features -> detector -> metrics) or read from
results/ files written by experiments/. Learned detectors appear only if their checkpoint exists (run
`python -m experiments.run_main --seed 0`); nothing is mocked or hard-coded.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from experiments.common import base_episode_config, load_config
from src.evaluation.metrics import detection_delay, evaluate_condition, pr_curve, threshold_at_fpr
from src.evaluation.runtime import DISPLAY, available_models, nominal_threshold, score_batch, stored_threshold
from src.graph.dataset import build_batch
from src.simulation.episode import generate_episode
from src.visualization.swarm_plot import pr_figure, score_heatmap, score_timeseries, swarm_figure

ROOT = Path(__file__).resolve().parent
TAB = ROOT / "results" / "tables"
COLORS = {"RA-SCM (proposed)": "#2a78d6", "NSD-style sheaf": "#eb6834", "GCN": "#1baf7a", "GAT": "#eda100",
          "GCN (drop lost links)": "#e87ba4", "Physics (AoI-aware)": "#6250d6", "Physics (naive)": "#e34948"}

st.set_page_config(page_title="UAV swarm anomaly lab", layout="wide")
st.title("Position anomalies vs. communication failures in UAV swarms")
st.caption("Simulation-only research prototype. All scores are produced by the models in `src/`; trained models are listed only if a checkpoint exists. "
           "Synthetic results do not demonstrate real-world UAV performance.")

cfg = load_config()
base = base_episode_config(cfg)
avail = available_models(0)

with st.sidebar:
    st.header("Scenario")
    n_uavs = st.select_slider("Number of UAVs", [5, 10, 20], value=10)
    loss = st.select_slider("Packet-loss rate", [0.0, 0.1, 0.3, 0.5], value=0.3, format_func=lambda x: f"{int(x * 100)}%")
    loss_model = st.selectbox("Loss process", ["iid", "burst", "node_burst"], help="burst = per-link Gilbert–Elliott (mean burst 5 steps); node_burst = all links into a receiver fail together")
    targeted = st.checkbox("Targeted blackout on anomalous UAV's links (70%)", value=False)
    noise = st.slider("Noise severity (× nominal)", 1.0, 3.0, 1.0, 0.5)
    kind = st.selectbox("Anomaly type", ["mixed", "sudden", "drift", "spoof", "none"])
    blockage = st.checkbox("Dynamic topology: link blockages", value=False)
    traj = st.selectbox("Trajectory", ["random_turn", "circle", "lissajous"])
    form = st.selectbox("Formation", ["circle", "line", "wedge", "grid"])
    seed = st.number_input("Simulation seed", 0, 10_000, 3)
    st.header("Detector")
    options = [m for m in DISPLAY]
    label = {m: DISPLAY[m] + ("" if avail.get(m, True) else "  (not trained)") for m in options}
    model_name = st.selectbox("Model", options, format_func=lambda m: label[m], index=1)
    if not avail.get(model_name, True):
        st.warning("No checkpoint found for this model. Train it with `python -m experiments.run_main --seed 0` (see README).")
    n_eval = st.slider("Episodes for the metrics tab", 4, 30, 10)

cfg_ep = copy.deepcopy(base)
cfg_ep.swarm.n_uavs, cfg_ep.swarm.trajectory, cfg_ep.swarm.formation = n_uavs, traj, form
cfg_ep.channel.loss_rate, cfg_ep.channel.loss_model = loss, (loss_model if loss > 0 else "iid")
cfg_ep.channel.targeted_loss = 0.7 if targeted else 0.0
cfg_ep.sensors.noise_scale = noise
cfg_ep.anomaly.kind, cfg_ep.anomaly.p_anomaly_free = kind, 0.0
cfg_ep.blockage_rate = 6.0 if blockage else 0.0


@st.cache_data(show_spinner=False)
def run_episode(cfg_json: str, seed: int, model: str):
    from src.simulation.episode import EpisodeConfig
    c = EpisodeConfig.from_dict(json.loads(cfg_json))
    ep = generate_episode(c, seed)
    b = build_batch([c], [seed])
    return ep, score_batch(model, b)[0]


def threshold_for(model: str) -> tuple[float, str]:
    t = stored_threshold(model, 0)
    if t is not None:
        return t, "5% FPR operating point fixed on the validation split of the real experiment run (seed 0)"
    if model.startswith("physics"):
        return nominal_threshold(model, base), "5% FPR on a freshly simulated no-loss set (no experiment run found)"
    return 0.5, "default 0.5 (no stored operating point)"


tab_swarm, tab_scores, tab_metrics, tab_results = st.tabs(["Swarm", "Detection scores", "Metrics on simulated episodes", "Experiment results"])

if not avail.get(model_name, True):
    for t in (tab_swarm, tab_scores, tab_metrics):
        with t:
            st.info("Selected model has no trained checkpoint; choose a physics detector or train the model first.")
else:
    ep, scores = run_episode(json.dumps(cfg_ep.to_dict()), int(seed), model_name)
    thr, thr_note = threshold_for(model_name)
    with tab_swarm:
        st.plotly_chart(swarm_figure(ep, scores, thr), use_container_width=True, theme=None)
        c1, c2, c3 = st.columns(3)
        c1.metric("anomalous UAVs (ground truth)", int(ep.labels.any(0).sum()))
        c2.metric("in-range packets lost", f"{ep.comm_fail.sum() / max(ep.obs.adj.sum(), 1):.0%}")
        c3.metric("UAVs flagged at any step", int((scores > thr).any(0).sum()))
        st.caption(f"Threshold {thr:.3g}: {thr_note}. Ring = simulator ground truth; marker shape/colour = model output. "
                   "Positions drawn are the *real* ones; the dashed line shows the offset of the reported position.")
    with tab_scores:
        uav = st.selectbox("UAV", list(range(n_uavs)), index=int(np.argmax(ep.labels.any(0))) if ep.labels.any() else 0)
        st.plotly_chart(score_heatmap(scores, ep.labels, thr), use_container_width=True, theme=None)
        st.plotly_chart(score_timeseries(scores, ep.labels, thr, uav), use_container_width=True, theme=None)
    with tab_metrics:
        seeds = [int(seed) + 1000 + i for i in range(n_eval)]
        b = build_batch([cfg_ep] * n_eval, seeds)
        s = score_batch(model_name, b)
        m = evaluate_condition(s, b.labels.numpy(), b.eval_mask.numpy(), thr, base.swarm.dt)
        cols = st.columns(6)
        for col, (k, lab) in zip(cols, [("pr_auc", "PR-AUC"), ("precision", "precision"), ("recall", "recall"), ("fpr", "FPR"), ("detect_rate", "detection rate"), ("delay_median_s", "median delay (s)")]):
            col.metric(lab, "n/a" if np.isnan(m[k]) else f"{m[k]:.3f}")
        st.caption(f"{n_eval} fresh episodes of this scenario (seeds {seeds[0]}…{seeds[-1]}); chance PR-AUC = positive rate = {m['pos_rate']:.3f}.")
        p, r = pr_curve(s, b.labels.numpy(), b.eval_mask.numpy())
        st.plotly_chart(pr_figure({DISPLAY[model_name]: {"recall": r, "precision": p}}, COLORS, "precision–recall curve (this scenario)"), use_container_width=True, theme=None)

with tab_results:
    f = TAB / "summary_long.csv"
    if not f.exists():
        st.info("No experiment results found yet. Run `python -m experiments.run_main --seed 0` (and the other seeds), then `python -m experiments.aggregate`.")
    else:
        sm = pd.read_csv(f)
        st.caption("Mean ± 95% t-interval over evaluation seeds, read from `results/tables/summary_long.csv` (produced by experiments/aggregate.py).")
        metric = st.selectbox("Metric", ["pr_auc", "fpr", "recall", "precision", "f1", "roc_auc", "detect_rate", "delay_median_s"])
        fam = st.radio("Sweep", ["iid packet loss", "burst packet loss"], horizontal=True)
        conds = [("iid_0", 0)] + [(f"{'iid' if fam.startswith('iid') else 'burst'}_{p}", p) for p in (10, 30, 50)]
        fig = go.Figure()
        for m_, disp in DISPLAY.items():
            ys, es, xs = [], [], []
            for c_, p_ in conds:
                r_ = sm[(sm.model == m_) & (sm.condition == c_) & (sm.metric == metric)]
                if len(r_):
                    xs.append(p_); ys.append(r_["mean"].iloc[0]); es.append(r_["ci_half"].iloc[0])
            if xs:
                fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", name=disp, line=dict(color=COLORS[disp], dash="dash" if m_.startswith("physics") else "solid"),
                                         error_y=dict(type="data", array=es, visible=True, thickness=1)))
        fig.update_layout(height=380, xaxis_title="packet-loss rate (%)", yaxis_title=metric, plot_bgcolor="#fcfcfb", paper_bgcolor="#fcfcfb", font=dict(color="#0b0b0b"), margin=dict(l=10, r=10, t=20, b=10), legend=dict(orientation="h", y=-0.25))
        st.plotly_chart(fig, use_container_width=True, theme=None)
        wide = sm[sm.metric == metric].pivot(index="model", columns="condition", values="mean")
        st.dataframe(wide.round(3), use_container_width=True)
        for name, title in [("hypothesis_test.csv", "Paired hypothesis tests (RA-SCM − reference)"), ("ablation_paired.csv", "Ablations (full − ablated)"), ("latency.csv", "Inference latency / parameters")]:
            if (TAB / name).exists():
                with st.expander(title):
                    st.dataframe(pd.read_csv(TAB / name).round(4), use_container_width=True)
