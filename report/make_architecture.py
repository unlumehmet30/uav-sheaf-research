"""Draws the architecture / information-flow diagram used in the report (report/figures/fig_architecture.png)."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)
SURFACE, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
BLUE, ORANGE, AQUA, VIOLET, RED = "#2a78d6", "#eb6834", "#1baf7a", "#6250d6", "#e34948"

fig, ax = plt.subplots(figsize=(12.6, 6.6))
ax.set_xlim(0, 126); ax.set_ylim(-3, 66); ax.axis("off"); fig.patch.set_facecolor(SURFACE)


def box(x, y, w, h, title, lines=(), edge=INK2, fill="#ffffff", fs=8.0, lw=1.2, line_gap=2.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=1.0", fc=fill, ec=edge, lw=lw))
    ax.text(x + w / 2, y + h - 1.6, title, ha="center", va="top", fontsize=fs + 0.8, fontweight="bold", color=INK)
    for i, l in enumerate(lines):
        ax.text(x + w / 2, y + h - 4.5 - i * line_gap, l, ha="center", va="top", fontsize=fs - 0.8, color=INK2)


def arrow(p, q, color=INK2, ls="-", lw=1.3, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=10, color=color, lw=lw, ls=ls, connectionstyle=f"arc3,rad={rad}"))


def head(x, text, color=INK):
    ax.text(x, 64.2, text, ha="center", fontsize=9.6, fontweight="bold", color=color)


# ---------------- column 1: simulator ----------------
head(10.5, "① Simulator")
box(1, 50, 19, 10, "Real state", ["position, velocity", "formation PD tracking"], edge=MUTED, fill="#f3f2ee")
box(1, 35.5, 19, 12.5, "Measured → reported", ["GNSS-like estimate + noise", "+ anomaly offset", "(sudden · drift · spoof)"], edge=RED)
box(1, 17.5, 19, 15.5, "Channel", ["in-range pairs only", "iid / Gilbert–Elliott loss", "targeted blackout", "→ delivered[t, recv, send]"], edge=ORANGE)
box(1, 4, 19, 11.5, "Relative sensing", ["r_ij = p_j − p_i + noise", "IMU velocity (independent)"], edge=AQUA)
arrow((10.5, 50), (10.5, 48.2), color=MUTED)
ax.add_patch(plt.Rectangle((22, 2), 0.8, 60, fc=RED, ec="none"))
ax.text(22.4, 0.6, "observation barrier: no truth,\nno labels cross it", fontsize=7, color=RED, ha="center", va="top")

# ---------------- column 2: tensors ----------------
head(37, "② Observation → tensors")
box(26, 42, 22, 18, "Node features u_i(t)", ["IMU velocity", "kinematic residual", "self-reported σ, degree"])
box(26, 9, 22, 30, "Edge features e_ij(t)", ["DATA group:", "relative measurement r_ij,", "stale residual, cached velocity", "REL group:", "delivered, age, link quality,", "has-cache, age-compensated", "residual;  cache index t − age"], edge=ORANGE)
arrow((20.3, 41), (26, 50), color=INK2); arrow((20.3, 25), (26, 25), color=ORANGE); arrow((20.3, 10), (26, 16), color=AQUA)

# ---------------- column 3: RA-SCM ----------------
ax.add_patch(FancyBboxPatch((52, 2.5), 48, 59, boxstyle="round,pad=0.3,rounding_size=1.4", fc="#eef4fd", ec=BLUE, lw=1.8))
head(76, "③ RA-SCM", BLUE)
ax.text(76, 59.6, "Reliability-Aware Sheaf Consistency Model", ha="center", fontsize=7.6, color=BLUE)
box(54.5, 49, 43, 8, "Encoder", ["node features → stalk state x_i ∈ R^(d×f)"], edge=BLUE, fs=7.8, line_gap=2.2)
box(54.5, 15, 43, 32, "Sheaf layer × 2", [
    "messages use x_j from the last delivered packet (t − age_ij)",
    "maps F_i, F_j = tanh Φ(x_i, x_j, e_ij);   translation b_ij = g(e_ij)",
    "residual  ρ_ij = F_i x_i − F_j x_j − b_ij",
    "weight  w_ij = σ( MLP[ delivered, age, link q, has-cache ] )",
    "msg_i = Σ_j w_ij F_iᵀ ρ_ij / Σ_j w_ij",
    "x_i ← LayerNorm( x_i − ELU(msg_i · W) )",
    "also emits: weighted energy s_i = Σ w‖ρ‖² / Σ w",
    "and evidence mass Σ_j w_ij"], edge=BLUE, fs=7.8, line_gap=2.5)
box(54.5, 5, 20, 7.5, "GRU over time", [], edge=BLUE, fs=7.8)
box(77.5, 5, 20, 7.5, "MLP head → score", [], edge=BLUE, fs=7.8)
arrow((48.3, 52), (54.5, 54), color=INK2)
arrow((48.3, 24), (54.5, 28), color=ORANGE)
ax.text(51.2, 21.2, "e_ij", fontsize=7, color=ORANGE, ha="center")
arrow((76, 49), (76, 47.2), color=BLUE); arrow((64.5, 15), (64.5, 12.7), color=BLUE); arrow((74.8, 8.7), (77.5, 8.7), color=BLUE)

# ---------------- column 4: comparison ----------------
head(112, "④ Comparison")
box(103, 43, 22, 17, "Baselines", ["same inputs, capacity-matched", "Physics: naive / AoI-aware", "GCN · GCN-drop · GAT", "NSD-style sheaf"], edge=VIOLET, fs=7.8)
box(103, 26, 22, 14, "Ablations of RA-SCM", ["− reliability info, − weights", "− sheaf maps, − temporal", "MPNN-E control"], edge=ORANGE, fs=7.8)
box(103, 5, 22, 18, "Evaluation", ["PR-AUC · FPR · delay", "5 %-FPR threshold fixed", "on validation split", "5 seeds, paired 95 % CI"], edge=INK2, fs=7.8)
arrow((97.8, 8.7), (103, 12), color=BLUE)
for yy, col in ((51.5, VIOLET), (33, ORANGE)):
    ax.plot([103, 101.6], [yy, yy], color=col, lw=1.3)
ax.plot([101.6, 101.6], [51.5, 14], color=INK2, lw=1.3)
arrow((101.6, 14), (103, 14), color=INK2)
fig.savefig(OUT / "fig_architecture.png", dpi=170, bbox_inches="tight", facecolor=SURFACE)
print("saved", OUT / "fig_architecture.png")
