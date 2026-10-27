"""Correctness tests for the dense layers and the detectors."""
import numpy as np
import pytest
import torch

from src.graph.dataset import make_split
from src.graph.features import N_EDGE, N_NODE, REL_SLICE
from src.models.detectors import ABLATIONS, LEARNED_MODELS, aggregate_edge_stats, build_model, match_capacity, n_params
from src.models.layers import (DenseGATLayer, DenseGCNLayer, SheafLayer, delayed_gather, sheaf_message)
from src.models.physics import physics_scores
from src.simulation.episode import EpisodeConfig

torch.manual_seed(0)


def _now(B, T, N):
    return torch.arange(T).view(1, T, 1, 1).expand(B, T, N, N).contiguous()


def _sym_adj(B, T, N, p=0.5):
    a = (torch.rand(B, T, N, N) < p).float()
    a = torch.triu(a, 1)
    return a + a.transpose(-1, -2)


def test_delayed_gather_picks_the_right_time_and_sender():
    B, T, N, K = 2, 6, 4, 3
    x = torch.randn(B, T, N, K)
    tidx = torch.randint(0, T, (B, T, N, N))
    out = delayed_gather(x, tidx)
    for b, t, i, j in [(0, 3, 1, 2), (1, 5, 0, 3), (1, 0, 2, 2)]:
        torch.testing.assert_close(out[b, t, i, j], x[b, tidx[b, t, i, j], j])


def test_gcn_layer_matches_pyg_gcnconv():
    pyg = pytest.importorskip("torch_geometric.nn")
    N, din, dout = 7, 5, 4
    A = _sym_adj(1, 1, N)
    h = torch.randn(1, 1, N, din)
    layer = DenseGCNLayer(din, dout)
    conv = pyg.GCNConv(din, dout, add_self_loops=True, normalize=True)
    with torch.no_grad():
        conv.lin.weight.copy_(layer.lin.weight); conv.bias.copy_(layer.bias)
    ei = A[0, 0].nonzero().t()
    ref = conv(h[0, 0], ei)
    out = layer(h, _now(1, 1, N), A)[0, 0]
    torch.testing.assert_close(out, ref, atol=1e-5, rtol=1e-5)


def test_gat_layer_matches_pyg_gatconv():
    pyg = pytest.importorskip("torch_geometric.nn")
    N, din, C, H = 6, 5, 3, 2
    A = _sym_adj(1, 1, N, 0.6)
    h = torch.randn(1, 1, N, din)
    layer = DenseGATLayer(din, C, H)
    conv = pyg.GATConv(din, C, heads=H, concat=True, add_self_loops=True)
    with torch.no_grad():
        conv.lin.weight.copy_(layer.lin.weight)
        conv.att_src.copy_(layer.att_src.view(1, H, C)); conv.att_dst.copy_(layer.att_dst.view(1, H, C))
        conv.bias.copy_(layer.bias)
    ref = conv(h[0, 0], A[0, 0].nonzero().t())
    out = layer(h, _now(1, 1, N), A)[0, 0]
    torch.testing.assert_close(out, ref, atol=1e-5, rtol=1e-5)


def test_gnn_layers_only_use_delayed_sender_state():
    """Changing a sender's state at a time that is *not* the cached time must not change the receiver output."""
    B, T, N, K = 1, 5, 4, 3
    A = torch.ones(B, T, N, N) - torch.eye(N)
    tidx = torch.zeros(B, T, N, N, dtype=torch.long)        # everybody uses the state from t=0
    for L in (DenseGCNLayer(K, K), DenseGATLayer(K, K, 1)):
        h = torch.randn(B, T, N, K)
        h2 = h.clone(); h2[:, 3, 2] += 5.0                  # change sender 2 at t=3 (cached time is 0)
        o1, o2 = L(h, tidx, A), L(h2, tidx, A)
        mask = torch.ones(N, dtype=bool); mask[2] = False   # receivers other than 2 see no change at t=3
        torch.testing.assert_close(o1[:, 3, mask], o2[:, 3, mask])


def _laplacian_blocks(adj, F1, F2, w):
    """Explicit coboundary / weighted sheaf Laplacian for a symmetric graph (consistent edge maps)."""
    N, d = adj.shape[0], F1.shape[-1]
    edges = [(i, j) for i in range(N) for j in range(i + 1, N) if adj[i, j] > 0]
    delta = torch.zeros(len(edges) * d, N * d, dtype=torch.float64)
    W = torch.zeros(len(edges) * d, len(edges) * d, dtype=torch.float64)
    for e, (i, j) in enumerate(edges):
        delta[e * d:(e + 1) * d, i * d:(i + 1) * d] = F1[i, j]          # F_{i<e}
        delta[e * d:(e + 1) * d, j * d:(j + 1) * d] = -F1[j, i]         # -F_{j<e}
        W[e * d:(e + 1) * d, e * d:(e + 1) * d] = w[i, j] * torch.eye(d, dtype=torch.float64)
    return delta, W


def test_sheaf_message_equals_explicit_weighted_laplacian_and_is_psd():
    N, d, f = 6, 3, 2
    adj = _sym_adj(1, 1, N, 0.7)[0, 0].double()
    F1 = torch.randn(N, N, d, d, dtype=torch.float64)           # F1[i,j] = restriction map of node i on edge {i,j}
    F2 = F1.transpose(0, 1).clone()                              # consistency: map of j on the same edge is F1[j,i]
    w = torch.rand(N, N, dtype=torch.float64); w = (w + w.T) / 2 * adj
    x = torch.randn(N, d, f, dtype=torch.float64)
    xj = x.unsqueeze(0).expand(N, N, d, f)
    msg, _ = sheaf_message(F1, F2, x.unsqueeze(1), xj, None, w)
    delta, W = _laplacian_blocks(adj, F1, F2, w)
    L = delta.T @ W @ delta
    ref = (L @ x.reshape(N * d, f)).reshape(N, d, f)
    torch.testing.assert_close(msg, ref, atol=1e-9, rtol=1e-9)
    assert torch.linalg.eigvalsh((L + L.T) / 2).min() > -1e-9    # PSD for non-negative weights


def test_sheaf_layer_identity_case_is_graph_laplacian():
    B, T, N, d, f = 1, 2, 5, 2, 3
    A = _sym_adj(B, T, N, 0.8)
    X = torch.randn(B, T, N, d, f)
    layer = SheafLayer(d, f, N_EDGE, learn_F=False, use_edge=False, use_b=False, use_w=False)
    with torch.no_grad():
        layer.mix.weight.copy_(torch.eye(f))
        layer.norm.weight.fill_(1.0)
    X2, energy, mass = layer(X, torch.zeros(B, T, N, N, N_EDGE), _now(B, T, N), A)
    deg = A.sum(-1)
    lap = (deg[..., None, None] * X - torch.einsum("btij,btjdf->btidf", A, X)) / (deg + 1e-3)[..., None, None]
    expect = X - torch.nn.functional.elu(lap)
    expect = torch.nn.functional.layer_norm(expect.reshape(B, T, N, -1), (d * f,)).view_as(X)
    torch.testing.assert_close(X2, expect, atol=1e-5, rtol=1e-5)
    torch.testing.assert_close(mass, deg)


def test_zero_reliability_weight_equals_removed_edge():
    """w_ij ~ 0 for links with m=0 must give the same output as deleting those links from the graph."""
    B, T, N, d, f = 1, 1, 6, 2, 2
    A = _sym_adj(B, T, N, 0.9)
    E = torch.randn(B, T, N, N, N_EDGE)
    E[..., 6] = (torch.rand(B, T, N, N) < 0.5).float()            # m = delivered-now flag
    layer = SheafLayer(d, f, N_EDGE, learn_F=True, use_edge=True, use_b=True, use_w=True)
    with torch.no_grad():                                          # w = sigmoid(60*m - 30): ~1 if m=1, ~0 if m=0
        for p in layer.wnet.parameters():
            p.zero_()
        layer.wnet[0].weight[:, 0] = 1.0
        layer.wnet[0].bias.fill_(0.0)
        layer.wnet[2].weight.fill_(0.0)
        # hand-set a monotone map m -> w by overriding the MLP with a single linear layer
    layer.wnet = torch.nn.Sequential(torch.nn.Linear(4, 1))
    with torch.no_grad():
        layer.wnet[0].weight.zero_(); layer.wnet[0].weight[0, 0] = 60.0; layer.wnet[0].bias.fill_(-30.0)
    X = torch.randn(B, T, N, d, f)
    o_w, e_w, mass_w = layer(X, E, _now(B, T, N), A)
    A_removed = A * E[..., 6]
    layer_nw = SheafLayer(d, f, N_EDGE, learn_F=True, use_edge=True, use_b=True, use_w=False)
    layer_nw.load_state_dict(layer.state_dict(), strict=False)
    o_r, e_r, mass_r = layer_nw(X, E, _now(B, T, N), A_removed)
    torch.testing.assert_close(o_w, o_r, atol=1e-5, rtol=1e-5)
    torch.testing.assert_close(mass_w, mass_r, atol=1e-5, rtol=1e-5)


@pytest.mark.parametrize("name", LEARNED_MODELS + ABLATIONS)
def test_detector_shapes_finite_and_backprop(name):
    b = make_split(EpisodeConfig(), "train", 0, 2)
    m = build_model(name)
    out = m(b.tensors)
    assert out.shape == b.labels.shape and torch.isfinite(out).all()
    out.mean().backward()
    assert all(p.grad is None or torch.isfinite(p.grad).all() for p in m.parameters())


@pytest.mark.parametrize("name", ["gcn", "gat", "nsd", "rascm", "rascm_no_weight"])
def test_detectors_are_causal_in_time(name):
    b = make_split(EpisodeConfig(), "train", 0, 1)
    m = build_model(name).eval()
    t0 = 40
    base = m(b.tensors)
    t2 = {k: v.clone() if v.dim() > 0 else v for k, v in b.tensors.items()}
    for k in ("node_x", "edge_x"):
        t2[k][:, t0 + 1:] += torch.randn_like(t2[k][:, t0 + 1:])
    out2 = m(t2)
    torch.testing.assert_close(base[:, :t0 + 1], out2[:, :t0 + 1], atol=1e-5, rtol=1e-5)


def test_no_rel_ablation_ignores_reliability_channel():
    b = make_split(EpisodeConfig(), "train", 0, 1)
    m = build_model("rascm_no_rel").eval()
    t2 = {k: v.clone() if v.dim() > 0 else v for k, v in b.tensors.items()}
    t2["edge_x"][..., REL_SLICE] = torch.randn_like(t2["edge_x"][..., REL_SLICE])
    torch.testing.assert_close(m(b.tensors), m(t2))
    m_full = build_model("rascm").eval()
    assert not torch.allclose(m_full(b.tensors), m_full(t2))


def test_capacity_matching_brings_baselines_within_10_percent():
    target = n_params(build_model("rascm"))
    for name in ("gcn", "gat", "gcn_drop", "nsd"):
        got = n_params(match_capacity(name, target))
        assert abs(got - target) / target < 0.10, (name, got, target)


def test_aggregate_edge_stats_shape():
    E = torch.randn(1, 2, 4, 4, N_EDGE); V = torch.ones(1, 2, 4, 4)
    assert aggregate_edge_stats(E, V).shape == (1, 2, 4, 2 * N_EDGE)


def test_physics_aoi_awareness_reduces_false_alarms_under_loss():
    from src.anomalies.injection import AnomalyConfig
    from src.communication.channel import ChannelConfig
    from src.graph.dataset import make_condition_set

    def f(c):
        c.anomaly = AnomalyConfig(kind="none"); c.channel = ChannelConfig("iid", 0.5)
    b = make_condition_set(EpisodeConfig(), f, "test", 0, 1, 6)
    naive = physics_scores(b.tensors, aoi_aware=False)
    aoi = physics_scores(b.tensors, aoi_aware=True)
    assert naive.mean() > 1.5 * aoi.mean()
    assert aoi.shape == b.labels.shape and torch.isfinite(aoi).all()
