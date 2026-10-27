"""Dense (batched) message-passing layers for small swarm graphs (N <= ~20).

All layers share the same *delayed-message* semantics: the message that receiver ``i`` uses from
sender ``j`` at step ``t`` is the sender's layer input from the time of the last delivered packet,
``t - age_ij(t)`` (``tidx``).  Hence no layer can use sender information that has not been
communicated.  Own-node quantities always use the current step.

Tensor conventions: x [B,T,N,K], pair tensors [B,T,N(receiver),N(sender),...].
"""
from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F


def delayed_gather(x: torch.Tensor, tidx: torch.Tensor) -> torch.Tensor:
    """x [B,T,N,K], tidx [B,T,N,N] (receiver i, sender j) -> out[b,t,i,j] = x[b, tidx[b,t,i,j], j]."""
    B, T, N, _ = x.shape
    b = torch.arange(B, device=x.device).view(B, 1, 1, 1)
    j = torch.arange(N, device=x.device).view(1, 1, 1, N)
    return x[b, tidx, j]


class DenseGCNLayer(nn.Module):
    """Kipf & Welling GCN layer, A_hat = D^-1/2 (A + I) D^-1/2, with delayed sender messages."""

    def __init__(self, din: int, dout: int):
        super().__init__()
        self.lin = nn.Linear(din, dout, bias=False)
        self.bias = nn.Parameter(torch.zeros(dout))

    def forward(self, h, tidx, valid):
        deg = valid.sum(-1) + 1.0                       # [B,T,N]
        dinv = deg.rsqrt()
        coef = dinv.unsqueeze(-1) * valid * dinv.unsqueeze(-2)          # [B,T,N,N]
        hp = self.lin(h)
        msg = (coef.unsqueeze(-1) * delayed_gather(hp, tidx)).sum(-2)
        return msg + hp / deg.unsqueeze(-1) + self.bias


class DenseGATLayer(nn.Module):
    """Single-layer GAT (Velickovic et al.) with self loops, delayed sender messages."""

    def __init__(self, din: int, dout_per_head: int, heads: int, negative_slope: float = 0.2):
        super().__init__()
        self.h, self.c = heads, dout_per_head
        self.lin = nn.Linear(din, heads * dout_per_head, bias=False)
        self.att_src = nn.Parameter(torch.empty(1, 1, 1, heads, dout_per_head))
        self.att_dst = nn.Parameter(torch.empty(1, 1, 1, heads, dout_per_head))
        self.bias = nn.Parameter(torch.zeros(heads * dout_per_head))
        self.slope = negative_slope
        nn.init.xavier_uniform_(self.att_src.view(heads, -1))
        nn.init.xavier_uniform_(self.att_dst.view(heads, -1))

    def forward(self, h, tidx, valid):
        B, T, N, _ = h.shape
        hp = self.lin(h).view(B, T, N, self.h, self.c)
        hj = delayed_gather(hp.reshape(B, T, N, -1), tidx).view(B, T, N, N, self.h, self.c)
        a_dst = (hp * self.att_dst.squeeze(0)).sum(-1)                  # [B,T,N,H]
        a_src_j = (hj * self.att_src.unsqueeze(0)).sum(-1)              # [B,T,N,N,H]
        a_src_self = (hp * self.att_src.squeeze(0)).sum(-1)             # [B,T,N,H]
        e_nb = F.leaky_relu(a_dst.unsqueeze(3) + a_src_j, self.slope)   # [B,T,N,N,H]
        e_self = F.leaky_relu(a_dst + a_src_self, self.slope)           # [B,T,N,H]
        mask = valid.unsqueeze(-1) > 0
        e_nb = e_nb.masked_fill(~mask, float("-inf"))
        logits = torch.cat([e_nb, e_self.unsqueeze(3)], dim=3)          # neighbours + self loop
        alpha = torch.softmax(logits, dim=3)
        out = (alpha[:, :, :, :-1].unsqueeze(-1) * hj).sum(3) + alpha[:, :, :, -1].unsqueeze(-1) * hp
        return out.reshape(B, T, N, -1) + self.bias


class SheafLayer(nn.Module):
    """Sheaf-diffusion layer on node stalks X_i in R^{d x f} (d stalk dimension, f channels).

    For receiver i and sender j (delayed state x_j):

        rho_ij = F1_ij x_i - F2_ij x_j - b_ij               (coboundary, optionally affine)
        msg_i  = sum_j w_ij F1_ij^T rho_ij / (sum_j w_ij + eps)
        X_i   <- LayerNorm( X_i - ELU(msg_i W) )

    * ``learn_F``  restriction maps F1,F2 = tanh(Phi(.)) (Neural Sheaf Diffusion style); otherwise identity
                   (trivial sheaf = ordinary graph Laplacian).
    * ``use_edge`` Phi additionally sees the edge feature vector e_ij.
    * ``use_b``    adds the data-dependent translation b_ij = g(e_ij): the sheaf is then defined on stalks
                   augmented with a constant coordinate, so  rho = F1 x_i - F2 x_j - b  is the coboundary of
                   a genuine sheaf on R^{d+1}-stalks (the extra coordinate is held at 1).
    * ``use_w``    reliability weights w_ij = valid_ij * sigmoid(MLP([m, age, q, has])) are the diagonal of a
                   learned inner product on the edge stalks (weighted sheaf Laplacian L_w = delta^T W delta);
                   otherwise w_ij = valid_ij.

    With F1=F2=I, b=0, w=valid and zero delay, msg_i equals the random-walk graph Laplacian action (L_rw X)_i.
    Returns the new state, the local weighted energy s_i = sum_j w_ij ||rho_ij||^2 / (sum_j w_ij+eps)
    and the evidence mass sum_j w_ij.
    """

    def __init__(self, d: int, f: int, edge_dim: int, *, learn_F: bool, use_edge: bool, use_b: bool,
                 use_w: bool, hidden: int = 32, rel_idx=(6, 7, 8, 9)):
        super().__init__()
        self.d, self.f = d, f
        H = d * f
        self.learn_F, self.use_edge, self.use_b, self.use_w = learn_F, use_edge, use_b, use_w
        self.rel_idx = list(rel_idx)
        out_dim = (d * d if learn_F else 0) + (d * f if use_b else 0)
        in_dim = 2 * H + (edge_dim if use_edge else 0)
        self.phi = None
        if out_dim > 0:
            self.phi = nn.Sequential(nn.Linear(in_dim, hidden), nn.ELU(), nn.Linear(hidden, out_dim))
        if use_w:
            self.wnet = nn.Sequential(nn.Linear(len(self.rel_idx), 16), nn.ELU(), nn.Linear(16, 1))
        self.mix = nn.Linear(f, f, bias=False)
        self.norm = nn.LayerNorm(H)
        self.register_buffer("eye", torch.eye(d))

    def forward(self, X, edge_x, tidx, valid, return_rho: bool = False):
        B, T, N, d, f = X.shape
        H = d * f
        Xf = X.reshape(B, T, N, H)
        Xj = delayed_gather(Xf, tidx)                                      # [B,T,N,N,H]
        Xi = Xf.unsqueeze(3).expand(B, T, N, N, H)
        if self.phi is not None:
            e = [edge_x] if self.use_edge else []
            o1 = self.phi(torch.cat([Xi, Xj] + e, dim=-1))
            o2 = self.phi(torch.cat([Xj, Xi] + e, dim=-1)) if self.learn_F else None
        off = 0
        if self.learn_F:
            F1 = torch.tanh(o1[..., :d * d]).view(B, T, N, N, d, d)
            F2 = torch.tanh(o2[..., :d * d]).view(B, T, N, N, d, d)
            off = d * d
        else:
            F1 = F2 = self.eye.expand(B, T, N, N, d, d)
        xi = X.unsqueeze(3)                                                # [B,T,N,1,d,f]
        xj = Xj.view(B, T, N, N, d, f)
        b = o1[..., off:off + d * f].view(B, T, N, N, d, f) if self.use_b else None
        if self.use_w:
            w = valid * torch.sigmoid(self.wnet(edge_x[..., self.rel_idx])).squeeze(-1)
        else:
            w = valid
        mass = w.sum(-1)                                                   # [B,T,N]
        denom = (mass + 1e-3).view(B, T, N, 1, 1)
        msg, rho = sheaf_message(F1, F2, xi, xj, b, w)
        msg = msg / denom                                                  # [B,T,N,d,f]
        energy = (w * rho.pow(2).sum((-1, -2))).sum(-1) / (mass + 1e-3)    # [B,T,N]
        upd = F.elu(self.mix(msg))                                         # channel mixing
        Xn = self.norm((X - upd).reshape(B, T, N, H)).view(B, T, N, d, f)
        if return_rho:
            return Xn, energy, mass, rho
        return Xn, energy, mass


def sheaf_message(F1, F2, xi, xj, b, w):
    """Weighted sheaf-Laplacian message (pure function, unit-tested against an explicit coboundary).

    F1,F2 [..,N,N,d,d]; xi [..,N,1,d,f]; xj [..,N,N,d,f]; b [..,N,N,d,f] or None; w [..,N,N].
    Returns (sum_j w_ij F1_ij^T rho_ij, rho)."""
    rho = torch.matmul(F1, xi.expand_as(xj)) - torch.matmul(F2, xj)
    if b is not None:
        rho = rho - b
    back = torch.matmul(F1.transpose(-1, -2), rho)
    return (w[..., None, None] * back).sum(-3), rho


def mlp(din: int, hidden: int, dout: int) -> nn.Sequential:
    return nn.Sequential(nn.Linear(din, hidden), nn.ELU(), nn.Linear(hidden, dout))
