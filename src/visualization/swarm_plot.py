"""Plotly figure builders for the dashboard. Pure functions: data in, figure out (no hard-coded results).

Encoding (never colour alone):
  ground truth   = ring around the marker (thick dark ring: injected position anomaly)
  model output   = marker shape + colour: circle grey = true negative, diamond green = detected anomaly (TP),
                   square orange = false alarm (FP), x red = missed anomaly (FN)
  links          = solid line: packet delivered this step; dotted red: in range but packet lost
"""
from __future__ import annotations

from typing import Dict, List, Optional

import numpy as np
import plotly.graph_objects as go

from src.simulation.episode import Episode

C_TN, C_TP, C_FP, C_FN = "#898781", "#1baf7a", "#eb6834", "#e34948"
C_LINK, C_LOST, C_TRUE, C_BLUE = "#6da7ec", "#e34948", "#0b0b0b", "#2a78d6"
STYLE = {"TN": ("circle", C_TN, "normal, not flagged"), "TP": ("diamond", C_TP, "anomaly detected (TP)"),
         "FP": ("square", C_FP, "false alarm (FP)"), "FN": ("x", C_FN, "anomaly missed (FN)")}


def _status(label: np.ndarray, pred: np.ndarray) -> np.ndarray:
    return np.where(label & pred, "TP", np.where(~label & pred, "FP", np.where(label & ~pred, "FN", "TN")))


def _links(ep: Episode, t: int):
    """x/y polylines (None-separated) for delivered links and lost links at step t (true positions, i<j)."""
    pos = ep.true_pos[t]
    adj, deliv = ep.obs.adj[t], ep.obs.delivered[t]
    xd, yd, xl, yl = [], [], [], []
    N = pos.shape[0]
    for i in range(N):
        for j in range(i + 1, N):
            if not adj[i, j]:
                continue
            ok = deliv[i, j] or deliv[j, i]
            both_lost = not deliv[i, j] and not deliv[j, i]
            tx, ty = (xl, yl) if both_lost else (xd, yd)
            tx += [pos[i, 0], pos[j, 0], None]
            ty += [pos[i, 1], pos[j, 1], None]
    return xd, yd, xl, yl


def swarm_figure(ep: Episode, scores: np.ndarray, thr: float, show_reported: bool = True) -> go.Figure:
    """Animated swarm. ``scores`` is [T,N] for this episode."""
    T, N, _ = ep.true_pos.shape
    pred = scores > thr
    lab = ep.labels
    st = np.stack([_status(lab[t], pred[t]) for t in range(T)])
    lo = ep.true_pos.reshape(-1, 2).min(0) - 25
    hi = ep.true_pos.reshape(-1, 2).max(0) + 25

    def frame_traces(t):
        xd, yd, xl, yl = _links(ep, t)
        tr = [go.Scatter(x=xd, y=yd, mode="lines", line=dict(color=C_LINK, width=1.5), name="link delivered", hoverinfo="skip", legendgroup="l"),
              go.Scatter(x=xl, y=yl, mode="lines", line=dict(color=C_LOST, width=1.5, dash="dot"), name="link: packet lost", hoverinfo="skip", legendgroup="l")]
        # ground-truth anomaly ring (at the REAL position)
        gt = lab[t]
        tr.append(go.Scatter(x=ep.true_pos[t, gt, 0], y=ep.true_pos[t, gt, 1], mode="markers",
                             marker=dict(size=24, color="rgba(0,0,0,0)", line=dict(color=C_TRUE, width=2.5)),
                             name="ground truth: injected anomaly (ring)", hoverinfo="skip"))
        if show_reported:
            off = lab[t] | ep.active[t]
            xs, ys = [], []
            for i in np.where(off)[0]:
                xs += [ep.true_pos[t, i, 0], ep.rep_pos[t, i, 0], None]
                ys += [ep.true_pos[t, i, 1], ep.rep_pos[t, i, 1], None]
            tr.append(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=C_TRUE, width=1, dash="dash"), name="reported − real offset", hoverinfo="skip"))
        for code, (sym, col, name) in STYLE.items():
            m = st[t] == code
            tr.append(go.Scatter(
                x=ep.true_pos[t, m, 0], y=ep.true_pos[t, m, 1], mode="markers+text", text=[str(i) for i in np.where(m)[0]],
                textposition="top center", textfont=dict(size=9),
                marker=dict(size=11, symbol=sym, color=col, line=dict(width=1, color="white")), name=name,
                customdata=np.stack([scores[t, m], ep.labels[t, m]], -1) if m.any() else None,
                hovertemplate="UAV %{text}<br>score %{customdata[0]:.3f}<extra></extra>"))
        return tr

    base = frame_traces(0)
    frames = [go.Frame(data=frame_traces(t), name=str(t)) for t in range(T)]
    fig = go.Figure(data=base, frames=frames)
    fig.update_layout(
        height=560, margin=dict(l=10, r=10, t=30, b=10), plot_bgcolor="#fcfcfb", paper_bgcolor="#fcfcfb",
        xaxis=dict(range=[lo[0], hi[0]], scaleanchor="y", showgrid=True, gridcolor="#e1e0d9", title="x [m] (real positions shown)"),
        yaxis=dict(range=[lo[1], hi[1]], showgrid=True, gridcolor="#e1e0d9", title="y [m]"),
        legend=dict(orientation="h", y=-0.18, font=dict(size=10)),
        updatemenus=[dict(type="buttons", direction="left", x=0.0, y=-0.06, showactive=False, buttons=[
            dict(label="▶ play", method="animate", args=[None, dict(frame=dict(duration=120, redraw=True), fromcurrent=True, transition=dict(duration=0))]),
            dict(label="⏸ pause", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])])],
        sliders=[dict(active=0, x=0.18, len=0.8, y=-0.04, currentvalue=dict(prefix="step ", font=dict(size=11)),
                      steps=[dict(method="animate", label=str(t), args=[[str(t)], dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))]) for t in range(0, T)])])
    return fig


def score_heatmap(scores: np.ndarray, labels: np.ndarray, thr: float) -> go.Figure:
    T, N = scores.shape
    fig = go.Figure(go.Heatmap(z=scores.T, x=np.arange(T), y=[f"UAV {i}" for i in range(N)], colorscale=[[0, "#cde2fb"], [1, "#0d366b"]],
                               colorbar=dict(title="score"), hovertemplate="step %{x}, %{y}<br>score %{z:.3f}<extra></extra>"))
    ys, xs = np.where(labels.T)
    fig.add_trace(go.Scatter(x=xs, y=[f"UAV {i}" for i in ys], mode="markers", marker=dict(symbol="square-open", size=5, color="#e34948"), name="ground-truth anomaly", hoverinfo="skip"))
    fig.update_layout(height=340, margin=dict(l=10, r=10, t=30, b=10), plot_bgcolor="#fcfcfb", paper_bgcolor="#fcfcfb", xaxis_title="step",
                      title=dict(text=f"detection score per UAV (threshold {thr:.3g}); red squares: ground-truth anomaly", font=dict(size=12)))
    return fig


def score_timeseries(scores: np.ndarray, labels: np.ndarray, thr: float, uav: int) -> go.Figure:
    T = scores.shape[0]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.arange(T), y=scores[:, uav], mode="lines", line=dict(color=C_BLUE, width=2), name="detection score"))
    fig.add_hline(y=thr, line=dict(color="#898781", dash="dot"), annotation_text="threshold", annotation_position="top left")
    on = labels[:, uav]
    if on.any():
        t0 = int(np.argmax(on))
        fig.add_vrect(x0=t0, x1=T - 1, fillcolor="#e34948", opacity=0.08, line_width=0, annotation_text="ground-truth anomaly", annotation_position="top left")
    fig.update_layout(height=280, margin=dict(l=10, r=10, t=30, b=10), plot_bgcolor="#fcfcfb", paper_bgcolor="#fcfcfb", xaxis_title="step",
                      yaxis_title="score", title=dict(text=f"UAV {uav}", font=dict(size=12)))
    return fig


def pr_figure(curves: Dict[str, Dict[str, list]], colors: Dict[str, str], title: str = "") -> go.Figure:
    fig = go.Figure()
    for name, c in curves.items():
        fig.add_trace(go.Scatter(x=c["recall"], y=c["precision"], mode="lines", name=name, line=dict(color=colors.get(name, "#898781"), width=2.2)))
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=40, b=10), plot_bgcolor="#fcfcfb", paper_bgcolor="#fcfcfb", xaxis=dict(title="recall", range=[0, 1]),
                      yaxis=dict(title="precision", range=[0, 1.02]), title=dict(text=title, font=dict(size=12)), legend=dict(orientation="h", y=-0.3))
    return fig
