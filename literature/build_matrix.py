"""Builds literature/literature_matrix.csv and literature_matrix.md from the entries below.

Evidence level:  FT = key sections of the full text were read;  AB = abstract/metadata page (plus the author's prior
knowledge for the textbook papers GCN/GAT/NSD) — cells marked [recalled] were not re-checked against the full text in this
session and MUST be verified by the author before submission.
Status:  P = peer-reviewed (journal / main conference);  W = workshop paper;  X = arXiv preprint.
"""
import csv
from pathlib import Path

E = []


def add(**kw):
    E.append(kw)


add(key="hansen2020sheaf", ref="Hansen & Gebhart 2020, Sheaf Neural Networks, arXiv:2012.06333", status="W", ev="AB",
    rq="Can the diffusion step of a GCN be generalised from the graph Laplacian to a sheaf Laplacian?",
    method="Replace graph diffusion by sheaf-Laplacian diffusion with vector-space stalks and restriction maps.",
    data="Synthetic semi-supervised node classification on signed graphs.",
    metrics="Node-classification accuracy.",
    findings="Sheaf networks outperform Kipf–Welling GCN in the synthetic signed-graph setting (abstract).",
    assumptions="Sheaf supplied by the construction of the task; learning the sheaf is not the contribution (a 2025 survey states it was proposed but not implemented — secondary statement).",
    weaknesses="Synthetic data only; workshop paper; no real benchmark; no dynamic graphs.",
    relation="Origin of sheaf-based message passing. We reuse the sheaf-Laplacian operator, not any result.")
add(key="bodnar2022neural", ref="Bodnar et al. 2022, Neural Sheaf Diffusion, NeurIPS (arXiv:2202.04579)", status="P", ev="AB",
    rq="How does the (implicit trivial) sheaf of a GNN explain heterophily and oversmoothing, and can learning the sheaf fix both?",
    method="Learn restriction maps from node features of the two endpoints of an edge; discretised sheaf diffusion layers; theory on linear separability and asymptotic behaviour.",
    data="Standard node-classification benchmarks, homophilic and heterophilic [recalled: Texas, Wisconsin, Cornell, Film, Squirrel, Chameleon, Cora, Citeseer, Pubmed].",
    metrics="Accuracy [recalled].",
    findings="Competitive (NeurIPS/arXiv abstract) or state-of-the-art (ICLR slide page wording) results on heterophilic graphs; non-trivial sheaves give control over diffusion limits.",
    assumptions="Static graph; maps conditioned on node features only; no edge features, measurement noise or missing edges; homophily/heterophily as the task structure.",
    weaknesses="Fixed benchmark splits; cost grows with stalk dimension; claims concern node classification, not detection of local inconsistencies; wording of the headline claim differs between venues (see search record).",
    relation="Baseline 4 ('standard sheaf') is an NSD-style implementation of this idea in our dense framework. RA-SCM adds edge-conditioned maps, translation term, reliability weights and temporal state.")
add(key="barbero2022connection", ref="Barbero et al. 2022, Sheaf NNs with Connection Laplacians (PMLR 196)", status="W", ev="AB",
    rq="Is it necessary to learn the sheaf, or can restriction maps be computed from geometry?",
    method="Orthogonal restriction maps aligning neighbouring local tangent spaces (manifold assumption), not learned.",
    data="Node-classification benchmarks (abstract-level only).",
    metrics="Accuracy.",
    findings="Matches or beats the learned-sheaf models of Bodnar et al. on most datasets and beats random sheaves (abstract).",
    assumptions="Data lie on a low-dimensional manifold; features are sufficient to estimate tangent spaces.",
    weaknesses="Workshop paper; assumption is unverified for sensor data; static graphs.",
    relation="Partly contradicts the need for learned maps (vs NSD) and motivates physically-derived maps; our physics baseline is the extreme 'fixed map' case.")
add(key="zaghen2024nonlinear", ref="Zaghen et al. 2024, Nonlinear Sheaf Diffusion (PMLR 251)", status="W", ev="AB",
    rq="Can a learned nonlinearity inside the sheaf Laplacian capture antagonistic or bounded-confidence interactions?",
    method="Nonlinear sheaf Laplacian with an adaptive learned function.",
    data="Synthetic community-detection dataset.",
    metrics="Node-classification accuracy.",
    findings="Beats linear sheaf networks and common GNN baselines on the synthetic task (abstract).",
    assumptions="Synthetic opinion-dynamics-like interactions.",
    weaknesses="Synthetic only, workshop paper.",
    relation="A robust (bounded) nonlinear aggregator could resist large anomalous residuals; not implemented here.")
add(key="hansen2019spectral", ref="Hansen & Ghrist 2019, Toward a spectral theory of cellular sheaves, J. Appl. Comput. Topol. 3(4)", status="P", ev="AB",
    rq="What are the spectral properties of the sheaf Laplacian and how do they relate to cohomology and graph structure?",
    method="Hodge-type Laplacian of cellular sheaves; interlacing, sparsification, effective resistance, synchronisation (abstract).",
    data="Theory.", metrics="n/a",
    findings="Foundations of sheaf Laplacian spectra; links kernel to global sections.",
    assumptions="Finite cell complexes; inner products on stalks define the Laplacian [recalled — verify in the text].",
    weaknesses="No learning or noisy data.",
    relation="Justifies treating reliability weights as a choice of inner product on edge stalks (L_w = δᵀWδ) rather than a new operator.")
add(key="robinson2017sheaves", ref="Robinson 2017, Sheaves are the canonical data structure for sensor integration, Information Fusion 36", status="P", ev="AB",
    rq="What mathematical structure can represent heterogeneous information sources faithfully and expose inconsistency?",
    method="Sheaves of sensor data; consistency radius, constrained fusion, cohomology for 'blind spots'.",
    data="Expository, illustrative examples.", metrics="n/a",
    findings="Sheaves give a sensor-agnostic consistency measure, fusion method and blind-spot detection (abstract).",
    assumptions="Sensor relationships must be specified by the modeller; exact data model.",
    weaknesses="Expository; no learning, no quantitative evaluation of detection.",
    relation="Conceptual foundation of the inconsistency measure r_ij and of the identifiability discussion.")
add(key="joslyn2020sheaf", ref="Joslyn et al. 2020, A sheaf theoretical approach to uncertainty quantification of heterogeneous geolocation information, Sensors 20(12)", status="P", ev="FT(partial)",
    rq="How can the agreement among heterogeneous geolocation sensors be quantified?",
    method="Sheaf over a simplicial complex of sensors; ε-consistency radius and consistency filtration; comparison with a Kalman-filter dynamic linear model.",
    data="Field experiment tracking black bears: 12 GPS collars (6 stationary), four sensor types (collar GPS, VHF, text report, vehicle GPS), 16 observations per 2-h session.",
    metrics="Consistency radius (m) and filtration.",
    findings="Radius decreases as the VHF error shrinks when the team approaches; largest discrepancy VHF vs collar GPS at the analysed instant (464.5 m).",
    assumptions="Sensor relationships and coordinate conversions specified in advance; time slices analysed independently.",
    weaknesses="Radius does not say which measurement is wrong; small case study; no learning, no dynamics, no communication model.",
    relation="Closest prior use of sheaf consistency for geolocation fusion; shows consistency flags disagreement but not its cause — exactly the ambiguity (anomaly vs missing data) we study.")
add(key="hanks2025distributed", ref="Hanks et al. 2025, Distributed multi-agent coordination over cellular sheaves, arXiv:2504.02049", status="X", ev="FT(partial)",
    rq="Can heterogeneous multi-agent coordination (consensus, formation, flocking) be cast over cellular sheaves?",
    method="Nonlinear homological programs on sheaves; ADMM with a local nonlinear sheaf heat equation.",
    data="Simulations with three planar double-integrator vehicles; a UAV/USV/UUV case study described but not simulated.",
    metrics="Convergence of simulated goals.",
    findings="Consensus, formation and flocking solved in the examples.",
    assumptions="Fixed undirected topology; no packet loss, delay or failures modelled; convex potentials.",
    weaknesses="Tiny simulations; preprint; learning/GNN integration listed only as future work.",
    relation="Shows sheaves for multi-agent *control* under reliable fixed topology — contrasts with our time-varying unreliable network.")
add(key="ribeiro2025cooperative", ref="Ribeiro et al. 2025, Cooperative Sheaf Neural Networks, arXiv:2507.00647", status="X (ICLR 2026 per arXiv comment)", ev="AB",
    rq="How to extend sheaf networks to directed graphs?",
    method="Cooperative sheaf Laplacian with a pair of learned maps per node [abstract-level].",
    data="not extracted", metrics="not extracted", findings="not extracted",
    assumptions="Directed message flow.", weaknesses="Not read beyond abstract.",
    relation="Directed links resemble asymmetric packet delivery; not used.")
add(key="asif2026temporal", ref="Asif et al. 2026, Temporal Sheaf NNs with Dynamic Orthogonal Transport, arXiv:2606.10071", status="X", ev="AB",
    rq="Can time-varying node frames improve temporal link prediction?",
    method="Per-node time-varying orthogonal frames (Householder products), transport before comparison, geometric-residual decoder, causal computation.",
    data="TGB v2 and DGB temporal-graph benchmarks.",
    metrics="Link-prediction metrics (abstract: 'matches or beats strong prior methods on most tasks').",
    findings="Gains attributed to dynamic frames, orthogonal transport and geometric-residual decoder (ablations).",
    assumptions="Event streams, no measurement noise or missing observation semantics.",
    weaknesses="Preprint; peer review not indicated; task is link prediction.",
    relation="Closest sheaf + dynamic-graph work; confirms that dynamic sheaves are of current interest but for a different task. Not anomaly detection, not reliability-aware.")
add(key="hernandez2026sheaf", ref="Hernández & Sánchez-Soto 2026, The Sheaf Laplacian: data fusion and consensus in distributed sensing networks, arXiv:2606.19529", status="X", ev="AB",
    rq="Is the sheaf Laplacian a suitable mechanism for data fusion and consensus in distributed sensing?",
    method="Sheaf-theoretic framework (abstract-level).",
    data="not extracted", metrics="not extracted", findings="not extracted",
    assumptions="unknown", weaknesses="Only the abstract page was read; the abstract mentions neither anomaly detection, learning, packet loss nor UAVs.",
    relation="Possible close relative on the model-based side — the full text must be read before claiming novelty.")
add(key="kipf2017semi", ref="Kipf & Welling 2017, GCN, ICLR", status="P", ev="AB [recalled]",
    rq="Scalable semi-supervised learning on graphs.", method="First-order spectral approximation; Â = D^-1/2 (A+I) D^-1/2.",
    data="Citation networks and a knowledge graph.", metrics="Accuracy.", findings="Outperforms related methods by a significant margin (abstract).",
    assumptions="Homophily; static graph; no edge features.", weaknesses="Oversmoothing with depth; single static graph.",
    relation="Baseline 2 (GCN).")
add(key="velickovic2018graph", ref="Veličković et al. 2018, GAT, ICLR", status="P", ev="AB [recalled]",
    rq="Learn neighbour weights by attention.", method="Masked self-attention over neighbourhoods, multi-head.",
    data="Citation networks, PPI [recalled].", metrics="Accuracy / micro-F1 [recalled].", findings="State of the art on the four benchmarks at the time [recalled].",
    assumptions="Attention scores computed from node features only.", weaknesses="Attention is not a calibrated reliability weight; no edge features.",
    relation="Baseline 3 (GAT).")
add(key="deng2021graph", ref="Deng & Hooi 2021, Graph neural network-based anomaly detection in multivariate time series, AAAI 35(5)", status="P", ev="AB",
    rq="Detect anomalies in multivariate sensor time series when inter-sensor relationships are unknown.",
    method="Learn a sensor graph from embedding similarity; graph-attention forecasting; deviation score; attention-based explanation.",
    data="Two real-world sensor datasets with labelled anomalies (abstract; SWaT/WADI [recalled]).",
    metrics="Precision, recall, F1 [recalled].",
    findings="Detects anomalies more accurately than baselines and helps root-cause identification (abstract).",
    assumptions="Fixed sensor set, synchronous complete observations, no communication layer; thresholding protocol affects F1 [recalled].",
    weaknesses="F1 depends on threshold rule; no missing-data semantics; static learned graph.",
    relation="Representative of graph-based sensor anomaly detection; we add missingness/staleness as a first-class confound and a dynamic physical graph.")
add(key="dang2023graphic", ref="Dang, Karakoc & Jäntti 2023, GNN-based GPS spoofing detection for cellular-connected UAV swarm, IEEE VTC-Spring", status="P", ev="FT",
    rq="Detect GPS spoofing in a UAV swarm using a GNN.",
    method="GCN (SimGNN-style) + GRU compare the swarm GPS topology (distances) with the communication topology (free-space path loss); threshold on predicted graph-edit similarity.",
    data="Own Python/TensorFlow simulator with 6, 8 and 10 UAVs, wind and GPS noise, a spoofing attacker; no real data.",
    metrics="Accuracy (>90% for 10 UAVs), computation time (<10 ms vs ≈16 s for exact GED).",
    findings="Accuracy decreases as GPS error grows; GRU converges faster than LSTM.",
    assumptions="Spoofing does not affect swarm/BS communication; communication topology reflects true geometry (path-loss); path loss is a reliable reference.",
    weaknesses="Simulation only; accuracy without class balance or PR-AUC; communication treated as trustworthy ground reference, packet loss/staleness not modelled although the text acknowledges environmental effects on the communication topology.",
    relation="Closest GNN spoof-detector for swarms; it uses the channel as *independent evidence*, whereas we treat the channel as an *unreliable* source and test robustness to it.")
add(key="mykytyn2023gps", ref="Mykytyn et al. 2023, GPS-spoofing attack detection mechanism for UAV swarms, MECO (arXiv:2301.12766)", status="P", ev="FT",
    rq="Detect single- and multi-transmitter GPS spoofing in a swarm without extra hardware beyond ranging.",
    method="Compare GPS-derived inter-UAV distances with IR-UWB ranging; flag if the discrepancy exceeds a threshold (with timestamp tolerance).",
    data="None — the text states this is the initial stage and that detection and false-positive rates will be presented later.",
    metrics="None reported.",
    findings="Qualitative argument that the mechanism is simple and low-cost.",
    assumptions="Ranging available and synchronised with GPS timestamps; thresholds from sensor accuracy.",
    weaknesses="No empirical results in the version read; thresholding only.",
    relation="Defines the independent-ranging principle used by our physics baseline and by the identifiability condition.")
add(key="bi2024detection", ref="Bi et al. 2024, Detection and mitigation of position spoofing attacks on cooperative UAV swarm formations, IEEE TIFS 19", status="P", ev="FT(partial)",
    rq="Identify malicious UAVs that falsify reported positions (distributed, collusion, mixed attacks).",
    method="Localisation-feasibility problem with reported positions + pairwise distance measurements; semidefinite relaxation; two algorithms exploiting neighbour proximity.",
    data="Matlab simulations of swarms with Gaussian position and ranging noise.",
    metrics="Detection success rate (up to +65%, +55%, +51% vs benchmarks).",
    findings="Outperforms benchmarks against the three attack types in simulation.",
    assumptions="All UAVs report positions and range neighbours; reports and measurements are received (no packet loss appears in the text); snapshot (non-temporal) formulation.",
    weaknesses="Convex-relaxation cost; no temporal evidence; no unreliable-communication model; no learning.",
    relation="Strongest model-based competitor in principle (not re-implemented here — disclosed). Its feasibility test is the identifiability principle we use; communication unreliability would convert 'infeasible' into 'missing'.")
add(key="tolstaya2020learning", ref="Tolstaya et al. 2020, Learning decentralized controllers for robot swarms with GNNs, CoRL (PMLR 100)", status="P", ev="AB",
    rq="Learn local controllers for large teams with limited communication.",
    method="Aggregation GNNs on time-varying communication graphs, imitation of a centralised controller.",
    data="Simulated flocking with a changing communication graph.",
    metrics="Control performance (abstract).",
    findings="Multi-hop information from distant teammates helps more when the communication radius is small or speeds are high (abstract).",
    assumptions="Perfect delivery on the current graph.",
    weaknesses="Control, not detection; delivery failures not modelled in the abstract.",
    relation="Evidence that GNNs on dynamic swarm graphs are practical; supports the dynamic-graph design (not the reliability question).")
add(key="cini2022filling", ref="Cini, Marisca & Alippi 2022, GRIN: multivariate time-series imputation by GNNs, ICLR", status="P", ev="AB",
    rq="Reconstruct missing values in sensor-network time series.",
    method="Bidirectional spatio-temporal message passing recurrent GNN.",
    data="Real-world sensor benchmarks (abstract-level).", metrics="MAE (improvements often >20% over prior state of the art, abstract).",
    findings="Graph-aware imputation beats non-graph imputers.",
    assumptions="Missingness is the only data defect (no adversarial or drifting values).",
    weaknesses="Does not separate missing from corrupted data; imputation, not detection.",
    relation="Shows graphs help with *missing* data; our problem is the confusion between missing and *corrupted* data.")
add(key="zhu2019robust", ref="Zhu et al. 2019, Robust GCNs against adversarial attacks, KDD", status="P", ev="AB",
    rq="Make GCNs robust to adversarially perturbed graphs.",
    method="Gaussian node representations; variance-based attention reduces the weight of nodes with high variance.",
    data="Three benchmark citation graphs.", metrics="Node-classification accuracy.",
    findings="Substantial accuracy gains against several attack strategies (abstract).",
    assumptions="Variance reflects attack influence.", weaknesses="Variance is learned, not tied to a physical reliability variable.",
    relation="Prior art for uncertainty-weighted aggregation: reliability *weighting* is **not** new in GNNs; our weights use explicit communication metadata (age, delivery, link quality).")

COLS = ["key", "ref", "status", "ev", "rq", "method", "data", "metrics", "findings", "assumptions", "weaknesses", "relation"]
HEAD = ["ID", "Reference", "Status", "Evidence", "Research question", "Method", "Data / conditions", "Metrics", "Main findings",
        "Assumptions", "Weaknesses / reproducibility", "Relation to RA-SCM"]

out = Path(__file__).parent
with open(out / "literature_matrix.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(HEAD)
    for e in E:
        w.writerow([e[c] for c in COLS])
with open(out / "literature_matrix.md", "w") as f:
    f.write("# Comparative literature matrix\n\n"
            "Status: P = peer-reviewed, W = workshop paper, X = arXiv preprint. Evidence: FT = key sections of the full text read, "
            "AB = abstract/metadata page only (items marked [recalled] contain details from the author's prior knowledge that "
            "must be re-checked against the full text before submission).\n\n")
    for e in E:
        f.write(f"## {e['ref']}\n\n`{e['key']}` · status **{e['status']}** · evidence **{e['ev']}**\n\n")
        for c, h in zip(COLS[4:], HEAD[4:]):
            f.write(f"* **{h}:** {e[c]}\n")
        f.write("\n")
print(len(E), "entries written")
