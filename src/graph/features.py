"""Observation -> graph tensors.

Only :class:`~src.simulation.episode.Observation` is accepted, so simulator ground truth
(true positions, labels, anomaly offsets, the 'lost' mask of out-of-range pairs) cannot reach
the models. ``tests/test_features.py`` checks that perturbing every hidden field leaves the
output unchanged.

Graph at step t:  nodes = UAVs,  E(t) = pairs inside relative-sensing/communication range
(``adj``).  All pair tensors are indexed [t, receiver i, sender j].

Node features u_i(t)  (NODE_COLS)
    own IMU velocity, own kinematic residual (finite-difference of the reported position minus
    IMU velocity), self-reported accuracy, neighbour count.
Edge features e_ij(t)   (EDGE_COLS); split in two groups so the 'no reliability' ablation can
drop exactly the communication-reliability channel:
    DATA group : r_ij   own relative-position measurement of j
                 res_ij reported-relative minus measured-relative using the *last received* report of j
                        (stale, not motion-compensated)
                 vc_ij  last received velocity report of j
    REL  group : m_ij   packet from j delivered at this step (0/1)
                 age_ij steps since the last delivered packet from j (capped, scaled)
                 q_ij   link-quality proxy
                 has_ij receiver has ever received from j
                 resc_ij age-compensated residual  (cached pos + cached vel * age) - own pos - r_ij
"""
from __future__ import annotations

from typing import Dict

import numpy as np

from src.simulation.episode import Observation

A_MAX = 20                  # age cap for the *feature* (the cache index itself is exact)
RES_SCALE = 5.0             # [m]   scaling of residual-type features
VEL_SCALE = 5.0             # [m/s]

NODE_COLS = ["v_x", "v_y", "kin_x", "kin_y", "sigma", "deg"]
DATA_EDGE_COLS = ["r_x", "r_y", "res_x", "res_y", "vc_x", "vc_y"]
REL_EDGE_COLS = ["m", "age", "q", "has", "resc_x", "resc_y"]
EDGE_COLS = DATA_EDGE_COLS + REL_EDGE_COLS
N_NODE, N_EDGE = len(NODE_COLS), len(EDGE_COLS)
REL_SLICE = slice(len(DATA_EDGE_COLS), len(EDGE_COLS))


def build_features(obs: Observation) -> Dict[str, np.ndarray]:
    T, N, _ = obs.rep_pos.shape
    dt = obs.dt
    R = obs.comm_range
    sig0 = obs.gnss_sigma_nominal

    # ---- node features (own sensors only) ----
    kin = np.zeros_like(obs.rep_pos)
    kin[1:] = (obs.rep_pos[1:] - obs.rep_pos[:-1]) / dt - obs.vel_meas[1:]
    deg = obs.adj.sum(-1)
    node_x = np.concatenate([
        obs.vel_meas / VEL_SCALE,
        kin / VEL_SCALE,
        (obs.sigma_rep / sig0)[..., None],
        (deg / 10.0)[..., None],
    ], axis=-1).astype(np.float32)

    # ---- delivery cache: last received report of sender j at receiver i ----
    cache_pos = np.zeros((N, N, 2))
    cache_vel = np.zeros((N, N, 2))
    last_t = np.full((N, N), -1, dtype=np.int64)
    edge_x = np.zeros((T, N, N, N_EDGE), dtype=np.float32)
    tidx = np.zeros((T, N, N), dtype=np.int64)
    valid = np.zeros((T, N, N), dtype=bool)
    age_steps = np.zeros((T, N, N), dtype=np.float32)
    res_m = np.zeros((T, N, N, 2), dtype=np.float32)     # meters, kept for the physics baseline
    resc_m = np.zeros((T, N, N, 2), dtype=np.float32)

    for t in range(T):
        d = obs.delivered[t]
        cache_pos = np.where(d[..., None], obs.rep_pos[t][None, :, :], cache_pos)
        cache_vel = np.where(d[..., None], obs.vel_meas[t][None, :, :], cache_vel)
        last_t = np.where(d, t, last_t)
        has = last_t >= 0
        age = np.where(has, t - last_t, A_MAX).astype(np.float64)
        adj = obs.adj[t]
        ok = adj & has

        rel = obs.rel_meas[t]
        dpos = cache_pos - obs.rep_pos[t][:, None, :]
        res = np.where(ok[..., None], dpos - rel, 0.0)
        resc = np.where(ok[..., None], (dpos + cache_vel * (age * dt)[..., None]) - rel, 0.0)

        e = edge_x[t]
        e[..., 0:2] = rel / R
        e[..., 2:4] = res / RES_SCALE
        e[..., 4:6] = np.where(ok[..., None], cache_vel / VEL_SCALE, 0.0)
        e[..., 6] = d & adj
        e[..., 7] = np.minimum(age, A_MAX) / A_MAX
        e[..., 8] = obs.link_q[t]
        e[..., 9] = ok
        e[..., 10:12] = resc / RES_SCALE
        e *= adj[..., None]

        tidx[t] = np.where(has, last_t, t)
        valid[t] = ok
        age_steps[t] = np.where(ok, age, 0.0)
        res_m[t], resc_m[t] = res, resc

    return {
        "node_x": node_x,                         # [T,N,N_NODE]
        "edge_x": edge_x,                         # [T,N,N,N_EDGE]
        "adj": obs.adj.astype(np.float32),        # [T,N,N] sensing neighbourhood
        "valid": valid.astype(np.float32),        # [T,N,N] adj & has-cache  (message passing graph)
        "delivered": (obs.delivered & obs.adj).astype(np.float32),   # [T,N,N] delivered now
        "tidx": tidx,                             # [T,N,N] time index of the cached sender state
        # physical-unit quantities for the (non-learned) physics baselines
        "res_m": res_m, "resc_m": resc_m, "age": age_steps,
        "kin_m": kin.astype(np.float32),
        "dt": np.float32(dt),
    }
