"""Learned per-UAV, per-step anomaly detectors sharing one wrapper.

    spatial module (GCN | GAT | Neural-Sheaf-Diffusion-style | RA-SCM | ablations)
        -> z_i(t) [+ sheaf energy features]  ->  GRU over time (optional)  ->  MLP head  ->  logit_i(t)

Input-information policy (see report, Section 8):
* GCN / GAT / NSD baselines receive the *same raw information* as RA-SCM, but edge features enter
  only through permutation-invariant neighbourhood statistics appended to the node vector
  (mean and mean-|.| of e_ij over messaging neighbours), because these layers have no edge-feature input.
* RA-SCM and its ablations consume e_ij directly (restriction maps, translation term, reliability weights).
* The control ``mpnn_e`` (identity maps, no weights) separates the effect of edge-conditioning from
  the effect of the sheaf maps / reliability weights.
"""
from __future__ import annotations

from typing import Dict, Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

from src.graph.features import N_EDGE, N_NODE, REL_SLICE
from src.models.layers import DenseGATLayer, DenseGCNLayer, SheafLayer, mlp


def aggregate_edge_stats(edge_x: torch.Tensor, valid: torch.Tensor) -> torch.Tensor:
    """Mean and mean-absolute edge features over messaging neighbours -> [B,T,N,2*N_EDGE]."""
    cnt = valid.sum(-1, keepdim=True).clamp(min=1.0)
    m = (edge_x * valid.unsqueeze(-1)).sum(3) / cnt
    a = (edge_x.abs() * valid.unsqueeze(-1)).sum(3) / cnt
    return torch.cat([m, a], dim=-1)


class GCNSpatial(nn.Module):
    def __init__(self, hidden: int, layers: int = 2):
        super().__init__()
        self.enc = mlp(N_NODE + 2 * N_EDGE, hidden, hidden)
        self.convs = nn.ModuleList([DenseGCNLayer(hidden, hidden) for _ in range(layers)])
        self.extra_dim = 0
        self.out_dim = hidden

    def forward(self, b, graph):
        h = self.enc(torch.cat([b["node_x"], aggregate_edge_stats(b["edge_x"], graph["valid"])], -1))
        for conv in self.convs:
            h = F.elu(conv(h, graph["tidx"], graph["valid"])) + h
        return h, None


class GATSpatial(nn.Module):
    def __init__(self, hidden: int, layers: int = 2, heads: int = 4):
        super().__init__()
        self.enc = mlp(N_NODE + 2 * N_EDGE, hidden, hidden)
        self.convs = nn.ModuleList([DenseGATLayer(hidden, hidden // heads, heads) for _ in range(layers)])
        self.extra_dim = 0
        self.out_dim = hidden

    def forward(self, b, graph):
        h = self.enc(torch.cat([b["node_x"], aggregate_edge_stats(b["edge_x"], graph["valid"])], -1))
        for conv in self.convs:
            h = F.elu(conv(h, graph["tidx"], graph["valid"])) + h
        return h, None


class SheafSpatial(nn.Module):
    """Neural-Sheaf-Diffusion-style baseline ('standard sheaf'): maps from node states only,
    no edge input, no translation term, no reliability weights (w = message-graph mask)."""

    def __init__(self, d: int, f: int, layers: int = 2, hidden: int = 32):
        super().__init__()
        self.d, self.f = d, f
        self.enc = mlp(N_NODE + 2 * N_EDGE, 32, d * f)
        self.layers = nn.ModuleList([
            SheafLayer(d, f, N_EDGE, learn_F=True, use_edge=False, use_b=False, use_w=False, hidden=hidden)
            for _ in range(layers)])
        self.extra_dim = 1
        self.out_dim = d * f

    def forward(self, b, graph):
        B, T, N, _ = b["node_x"].shape
        h = self.enc(torch.cat([b["node_x"], aggregate_edge_stats(b["edge_x"], graph["valid"])], -1))
        X = h.view(B, T, N, self.d, self.f)
        energies = []
        for layer in self.layers:
            X, e, _ = layer(X, b["edge_x"], graph["tidx"], graph["valid"])
            energies.append(e)
        energy = torch.stack(energies).mean(0)
        return X.reshape(B, T, N, -1), torch.log1p(energy).unsqueeze(-1)


class RASCMSpatial(nn.Module):
    """Reliability-Aware Sheaf Consistency Model (and ablations via flags).

    use_rel    False -> REL feature group zeroed (no m, age, q, has, compensated residual) and w = 1
    use_weight False -> reliability weights w_ij = 1 (features still available)
    learn_F    False -> trivial sheaf (identity restriction maps)
    """

    def __init__(self, d: int, f: int, layers: int = 2, hidden: int = 32, *, use_rel: bool = True,
                 use_weight: bool = True, learn_F: bool = True):
        super().__init__()
        self.d, self.f, self.use_rel = d, f, use_rel
        self.enc = mlp(N_NODE, hidden, d * f)
        self.layers = nn.ModuleList([
            SheafLayer(d, f, N_EDGE, learn_F=learn_F, use_edge=True, use_b=True,
                       use_w=use_weight and use_rel, hidden=hidden) for _ in range(layers)])
        self.extra_dim = 2
        self.out_dim = d * f
        mask = torch.ones(N_EDGE)
        if not use_rel:
            mask[REL_SLICE] = 0.0
        self.register_buffer("edge_mask", mask)

    def forward(self, b, graph):
        B, T, N, _ = b["node_x"].shape
        edge_x = b["edge_x"] * self.edge_mask
        X = self.enc(b["node_x"]).view(B, T, N, self.d, self.f)
        energies, mass = [], None
        for layer in self.layers:
            X, e, mass = layer(X, edge_x, graph["tidx"], graph["valid"])
            energies.append(e)
        energy = torch.stack(energies).mean(0)
        extra = torch.stack([torch.log1p(energy), torch.log1p(mass)], dim=-1)
        return X.reshape(B, T, N, -1), extra


class Detector(nn.Module):
    def __init__(self, spatial: nn.Module, *, temporal: bool = True, head_hidden: int = 32,
                 graph_mode: str = "delayed"):
        super().__init__()
        assert graph_mode in ("delayed", "delivered_now")
        self.spatial, self.temporal, self.graph_mode = spatial, temporal, graph_mode
        H, E = spatial.out_dim, spatial.extra_dim
        self.norm = nn.LayerNorm(H)
        if temporal:
            self.gru = nn.GRU(H + E, H, batch_first=True)
            self.head = mlp(H + E, head_hidden, 1)
        else:
            self.head = mlp(H + E, head_hidden, 1)

    def _graph(self, b: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        if self.graph_mode == "delayed":
            return {"valid": b["valid"], "tidx": b["tidx"]}
        B, T, N, _ = b["node_x"].shape
        now = torch.arange(T, device=b["node_x"].device).view(1, T, 1, 1).expand(B, T, N, N)
        return {"valid": b["delivered"], "tidx": now}

    def forward(self, b: Dict[str, torch.Tensor]) -> torch.Tensor:
        z, extra = self.spatial(b, self._graph(b))
        z = self.norm(z)
        u = z if extra is None else torch.cat([z, extra], -1)
        if self.temporal:
            B, T, N, K = u.shape
            seq = u.permute(0, 2, 1, 3).reshape(B * N, T, K)
            out, _ = self.gru(seq)
            out = out.reshape(B, N, T, -1).permute(0, 2, 1, 3)
            u = out if extra is None else torch.cat([out, extra], -1)
        return self.head(u).squeeze(-1)                                   # [B,T,N] logits


def n_params(m: nn.Module) -> int:
    return sum(p.numel() for p in m.parameters() if p.requires_grad)


# --------------------------------------------------------------------------------------
# Registry
# --------------------------------------------------------------------------------------
LEARNED_MODELS = ["gcn", "gat", "gcn_drop", "nsd", "rascm"]
ABLATIONS = ["rascm_no_rel", "rascm_no_weight", "rascm_no_sheaf", "rascm_no_temporal", "mpnn_e"]


def build_model(name: str, hidden: int = 32, d: int = 4, f: int = 8) -> Detector:
    """Models with default widths; use :func:`match_capacity` to equalise parameter counts.
    ``hidden`` is the node width for GCN/GAT variants and the Phi-MLP width for the sheaf models."""
    if name == "gcn":
        return Detector(GCNSpatial(hidden))
    if name == "gcn_drop":
        return Detector(GCNSpatial(hidden), graph_mode="delivered_now")
    if name == "gat":
        return Detector(GATSpatial(hidden))
    if name == "nsd":
        return Detector(SheafSpatial(d, f, hidden=hidden))
    if name == "rascm":
        return Detector(RASCMSpatial(d, f))
    if name == "rascm_no_rel":
        return Detector(RASCMSpatial(d, f, use_rel=False))
    if name == "rascm_no_weight":
        return Detector(RASCMSpatial(d, f, use_weight=False))
    if name == "rascm_no_sheaf":
        return Detector(RASCMSpatial(d, f, learn_F=False))
    if name == "rascm_no_temporal":
        return Detector(RASCMSpatial(d, f), temporal=False)
    if name == "mpnn_e":
        return Detector(RASCMSpatial(d, f, use_weight=False, learn_F=False))
    raise ValueError(f"unknown model {name!r}")


def match_capacity(name: str, target: int, tol: float = 0.10) -> Detector:
    """For the GCN/GAT/NSD baselines pick the width whose parameter count is closest to ``target``
    (the RA-SCM parameter count), so baselines are capacity-matched rather than under-sized."""
    if name not in ("gcn", "gat", "gcn_drop", "nsd"):
        return build_model(name)
    best, best_gap = None, 1e18
    for h in range(16, 129, 2):
        m = build_model(name, hidden=h)
        gap = abs(n_params(m) - target)
        if gap < best_gap:
            best, best_gap = m, gap
    return best
