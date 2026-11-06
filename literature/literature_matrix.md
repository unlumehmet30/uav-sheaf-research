# Comparative literature matrix

Status: P = peer-reviewed, W = workshop paper, X = arXiv preprint. Evidence: FT = key sections of the full text read (section, table or equation numbers are given where a detail comes from the full text), AB = abstract/metadata page only. Full-text details were checked in an AI-assisted pre-submission check on 6 November 2026 (see the AI-assistance declaration in the report).

## Hansen & Gebhart 2020, Sheaf Neural Networks, arXiv:2012.06333

`hansen2020sheaf` · status **W** · evidence **FT**

* **Research question:** Can the diffusion step of a GCN be generalised from the graph Laplacian to a sheaf Laplacian?
* **Method:** Replace graph diffusion by sheaf-Laplacian diffusion with vector-space stalks and restriction maps.
* **Data / conditions:** Synthetic semi-supervised node classification on signed graphs.
* **Metrics:** Node-classification accuracy.
* **Main findings:** Sheaf networks outperform Kipf–Welling GCN in the synthetic signed-graph setting (abstract).
* **Assumptions:** The sheaf is hand-built from signed edge weights because standard datasets lack obvious sheaf structure (Sec. 4); learning the sheaf from data is listed only as future work (Sec. 5). The paper makes no claim about heterophily or oversmoothing.
* **Weaknesses / reproducibility:** Synthetic data only; workshop paper; no real benchmark; no dynamic graphs.
* **Relation to RA-SCM:** Origin of sheaf-based message passing. We reuse the sheaf-Laplacian operator, not any result.

## Bodnar et al. 2022, Neural Sheaf Diffusion, NeurIPS (arXiv:2202.04579)

`bodnar2022neural` · status **P** · evidence **FT**

* **Research question:** How does the (implicit trivial) sheaf of a GNN explain heterophily and oversmoothing, and can learning the sheaf fix both?
* **Method:** Learn restriction maps from node features of the two endpoints of an edge; discretised sheaf diffusion layers; theory on linear separability and asymptotic behaviour.
* **Data / conditions:** Nine node-classification benchmarks ordered by edge homophily h = 0.11–0.81: Texas, Wisconsin, Film, Squirrel, Chameleon, Cornell (heterophilic, h ≤ 0.30) and Citeseer, Pubmed, Cora (homophilic); 10 fixed 48/32/20 % splits of Pei et al. (Sec. 6, Table 1); plus a synthetic linear-separation experiment (Fig. 5).
* **Metrics:** Mean test accuracy ± standard deviation over the 10 fixed splits (Sec. 6, Table 1); baseline figures are copied from Yan et al., Lingam et al. and Zhu et al. on the same splits, not re-run.
* **Main findings:** Competitive (NeurIPS/arXiv abstract) or state-of-the-art (ICLR 2022 GTRL workshop abstract) results on heterophilic graphs; full text: first on 5 of 6 heterophilic benchmarks, second on Chameleon, top three on 8/9 datasets (Sec. 6, Table 1); non-trivial sheaves give control over diffusion limits.
* **Assumptions:** Static graph; maps conditioned on node features only; no edge features, measurement noise or missing edges; homophily/heterophily as the task structure.
* **Weaknesses / reproducibility:** Fixed benchmark splits; cost grows with stalk dimension; claims concern node classification, not detection of local inconsistencies; wording of the headline claim differs between venues (see search record).
* **Relation to RA-SCM:** Baseline 4 (NSD-style sheaf) is an NSD-style implementation of this idea in our dense framework. RA-SCM adds edge-conditioned maps, translation term, reliability weights and temporal state.

## Barbero et al. 2022, Sheaf NNs with Connection Laplacians (PMLR 196)

`barbero2022connection` · status **W** · evidence **FT** (Table 1, Sec. 5)

* **Research question:** Is it necessary to learn the sheaf, or can restriction maps be computed from geometry?
* **Method:** Orthogonal restriction maps aligning neighbouring local tangent spaces (manifold assumption), not learned.
* **Data / conditions:** Node-classification benchmarks (abstract-level only).
* **Metrics:** Accuracy.
* **Main findings:** By the authors' conclusion (Sec. 5), matches or beats the learned-sheaf models of Bodnar et al. on most datasets; Table 1 shows Conn-NSD best only on Texas and Film and clearly below learned NSD on Squirrel (45.19 vs 56.34), Chameleon (65.21 vs 68.68) and Cora (83.74 vs 87.30). The abstract claims only 'promising results with less computational overhead'.
* **Assumptions:** Data lie on a low-dimensional manifold; features are sufficient to estimate tangent spaces.
* **Weaknesses / reproducibility:** Workshop paper; assumption is unverified for sensor data; static graphs.
* **Relation to RA-SCM:** Partly contradicts the need for learned maps (vs NSD) and motivates physically-derived maps; our physics baseline is the extreme 'fixed map' case.

## Zaghen et al. 2024, Nonlinear Sheaf Diffusion (PMLR 251)

`zaghen2024nonlinear` · status **W** · evidence **AB**

* **Research question:** Can a learned nonlinearity inside the sheaf Laplacian capture antagonistic or bounded-confidence interactions?
* **Method:** Nonlinear sheaf Laplacian with an adaptive learned function.
* **Data / conditions:** Synthetic community-detection dataset.
* **Metrics:** Node-classification accuracy.
* **Main findings:** Beats linear sheaf networks and common GNN baselines on the synthetic task (abstract).
* **Assumptions:** Synthetic opinion-dynamics-like interactions.
* **Weaknesses / reproducibility:** Synthetic only, workshop paper.
* **Relation to RA-SCM:** A robust (bounded) nonlinear aggregator could resist large anomalous residuals; not implemented here.

## Hansen & Ghrist 2019, Toward a spectral theory of cellular sheaves, J. Appl. Comput. Topol. 3(4)

`hansen2019spectral` · status **P** · evidence **FT**

* **Research question:** What are the spectral properties of the sheaf Laplacian and how do they relate to cohomology and graph structure?
* **Method:** Hodge-type Laplacian of cellular sheaves; interlacing, sparsification, effective resistance, synchronisation (abstract).
* **Data / conditions:** Theory.
* **Metrics:** n/a
* **Main findings:** Foundations of sheaf Laplacian spectra; links kernel to global sections.
* **Assumptions:** Finite regular cell complexes with finite-dimensional stalks (Sec. 3.3); a weighted sheaf puts inner products on stalks, which fix the adjoint δ* and so the Laplacian Δ = δ*δ + δδ* (Secs 3.1–3.2); scaling an edge stalk's inner product changes the weight given to discrepancies over that edge (Sec. 3.5).
* **Weaknesses / reproducibility:** No learning or noisy data.
* **Relation to RA-SCM:** Justifies treating reliability weights as a choice of inner product on edge stalks (L_w = δᵀWδ) rather than a new operator.

## Robinson 2017, Sheaves are the canonical data structure for sensor integration, Information Fusion 36

`robinson2017sheaves` · status **P** · evidence **AB**

* **Research question:** What mathematical structure can represent heterogeneous information sources faithfully and expose inconsistency?
* **Method:** Sheaves of sensor data; consistency radius, constrained fusion, cohomology for 'blind spots'.
* **Data / conditions:** Expository, illustrative examples.
* **Metrics:** n/a
* **Main findings:** Sheaves give a sensor-agnostic consistency measure, fusion method and blind-spot detection (abstract).
* **Assumptions:** Sensor relationships must be specified by the modeller; exact data model.
* **Weaknesses / reproducibility:** Expository; no learning, no quantitative evaluation of detection.
* **Relation to RA-SCM:** Conceptual foundation of the inconsistency measure r_ij and of the identifiability discussion.

## Joslyn et al. 2020, A sheaf theoretical approach to uncertainty quantification of heterogeneous geolocation information, Sensors 20(12)

`joslyn2020sheaf` · status **P** · evidence **FT(partial)**

* **Research question:** How can the agreement among heterogeneous geolocation sensors be quantified?
* **Method:** Sheaf over a simplicial complex of sensors; ε-consistency radius and consistency filtration; comparison with a Kalman-filter dynamic linear model.
* **Data / conditions:** Field experiment: 12 GPS collars (6 stationary decoy collars and 6 active collars on three wild black bears; twelve locating sessions), four sensor types (collar GPS, VHF, text report, vehicle GPS), 16 observations per 2-h session (Secs 3.2, 5).
* **Metrics:** Consistency radius (m) and filtration.
* **Main findings:** Radius decreases as the VHF error shrinks when the team approaches; largest discrepancy VHF vs collar GPS at the analysed instant (464.5 m).
* **Assumptions:** Sensor relationships and coordinate conversions specified in advance; time slices analysed independently.
* **Weaknesses / reproducibility:** The radius alone does not say which measurement is wrong; the consistency filtration attributes disagreement to sensors (Sec. 4, 5.1), but the authors state that neither reports which measurements are trustworthy (Conclusion); small case study; no learning, no dynamics, no communication or missing-data model.
* **Relation to RA-SCM:** Closest prior use of sheaf consistency for geolocation fusion; shows that consistency can flag and attribute disagreement, but not separate missing from wrong data — the ambiguity we study.

## Hanks et al. 2025, Distributed multi-agent coordination over cellular sheaves, arXiv:2504.02049

`hanks2025distributed` · status **X** · evidence **FT(partial)**

* **Research question:** Can heterogeneous multi-agent coordination (consensus, formation, flocking) be cast over cellular sheaves?
* **Method:** Nonlinear homological programs on sheaves; ADMM with a local nonlinear sheaf heat equation.
* **Data / conditions:** Simulations with three planar double-integrator vehicles; a UAV/USV/UUV case study described but not simulated.
* **Metrics:** Convergence of simulated goals.
* **Main findings:** Consensus, formation and flocking solved in the examples.
* **Assumptions:** Fixed undirected topology; no packet loss, delay or failures modelled; convex potentials.
* **Weaknesses / reproducibility:** Tiny simulations; preprint; learning/GNN integration listed only as future work.
* **Relation to RA-SCM:** Shows sheaves for multi-agent *control* under reliable fixed topology — contrasts with our time-varying unreliable network.

## Ribeiro et al. 2026, Cooperative Sheaf Neural Networks, ICLR 2026 (arXiv:2507.00647)

`ribeiro2025cooperative` · status **P** (ICLR 2026 poster, OpenReview AHpexliCTM) · evidence **AB**

* **Research question:** How to extend sheaf networks to directed graphs?
* **Method:** Cooperative sheaf Laplacian with a pair of learned maps per node [abstract-level].
* **Data / conditions:** not extracted
* **Metrics:** not extracted
* **Main findings:** not extracted
* **Assumptions:** Directed message flow.
* **Weaknesses / reproducibility:** Not read beyond abstract.
* **Relation to RA-SCM:** Directed links resemble asymmetric packet delivery; not used.

## Asif et al. 2026, Temporal Sheaf NNs with Dynamic Orthogonal Transport, arXiv:2606.10071

`asif2026temporal` · status **X** · evidence **AB**

* **Research question:** Can time-varying node frames improve temporal link prediction?
* **Method:** Per-node time-varying orthogonal frames (Householder products), transport before comparison, geometric-residual decoder, causal computation.
* **Data / conditions:** TGB v2 and DGB temporal-graph benchmarks.
* **Metrics:** Link-prediction metrics (abstract: 'matches or beats strong prior methods on most tasks').
* **Main findings:** Gains attributed to dynamic frames, orthogonal transport and geometric-residual decoder (ablations).
* **Assumptions:** Event streams, no measurement noise or missing observation semantics.
* **Weaknesses / reproducibility:** Preprint; peer review not indicated; task is link prediction.
* **Relation to RA-SCM:** Closest sheaf + dynamic-graph work; confirms that dynamic sheaves are of current interest but for a different task. Not anomaly detection, not reliability-aware.

## Hernández & Sánchez-Soto 2026, The Sheaf Laplacian: data fusion and consensus in distributed sensing networks, arXiv:2606.19529

`hernandez2026sheaf` · status **X** · evidence **FT**

* **Research question:** Is the sheaf Laplacian a suitable mechanism for data fusion and consensus in distributed sensing?
* **Method:** Sheaf-theoretic framework; Sec. 7 proposes the sheaf Dirichlet energy and a spectral variant as anomaly scores and localises a faulty node from per-edge energy contributions (Sec. 7.3).
* **Data / conditions:** None (conceptual paper, 10 pp.); drone swarms named as an application (Sec. 1).
* **Metrics:** None.
* **Main findings:** Proposes Dirichlet-energy anomaly detection and faulty-node localisation; no evaluation.
* **Assumptions:** Fixed maps; packet loss, intermittent links and topology changes named as challenges (Sec. 2.1) but not modelled inside the detector.
* **Weaknesses / reproducibility:** No experiments, no loss model, no learning.
* **Relation to RA-SCM:** An unweighted, loss-free ancestor of our AoI-aware physics baseline; it contradicts any claim that sheaf work ignores anomaly detection.

## Kipf & Welling 2017, GCN, ICLR

`kipf2017semi` · status **P** · evidence **FT**

* **Research question:** Scalable semi-supervised learning on graphs.
* **Method:** Localised first-order approximation of spectral graph convolutions with the renormalisation trick Â = D̃^-1/2 Ã D̃^-1/2, Ã = A + I, D̃ = degree matrix of Ã (Sec. 2, Eqs 2 and 8).
* **Data / conditions:** Citation networks Citeseer, Cora, Pubmed and the NELL knowledge-graph dataset; splits of Yang et al. (2016) (citation networks: 20 labels per class), 500 validation and 1,000 test nodes (Secs 5.1–5.2, Table 1).
* **Metrics:** Classification accuracy (%), mean of 100 runs with random weight initialisations; wall-clock training time (Sec. 6.1, Table 2).
* **Main findings:** Outperforms related methods by a significant margin (abstract): 70.3 / 81.5 / 79.0 / 66.0 % on Citeseer / Cora / Pubmed / NELL vs best baselines 69.1 / 75.7 / 77.2 / 61.9 % (Table 2).
* **Assumptions:** Undirected graph without native edge features; implicit locality and equal weight of self-loop and neighbours (Sec. 7.2); single static graph, transductive node classification (Sec. 4.2). The label-homophily assumption is stated for Laplacian regularisation (Sec. 1), which GCN replaces.
* **Weaknesses / reproducibility:** Degrades with depth: best at 2–3 layers, hard to train beyond 7 layers without residual connections (App. B); full-batch memory grows linearly with graph size (Sec. 7.2); single static graph; below an MLP on heterophilic graphs in NSD's Table 1 (e.g. Texas 55.1 vs 80.8 %).
* **Relation to RA-SCM:** Baseline 2 (GCN).

## Veličković et al. 2018, GAT, ICLR

`velickovic2018graph` · status **P** · evidence **FT**

* **Research question:** Learn neighbour weights by attention.
* **Method:** Masked self-attention over first-order neighbourhoods (LeakyReLU scores, softmax-normalised), K heads concatenated or averaged in the output layer (Sec. 2.1).
* **Data / conditions:** Transductive: Cora, Citeseer, Pubmed citation networks (20 labels per class, 500 validation / 1,000 test nodes); inductive: PPI, 20 / 2 / 2 train / val / test graphs with test graphs unseen, 121 multi-labels (Sec. 3.1).
* **Metrics:** Transductive: mean accuracy ± s.d. over 100 runs; inductive: micro-averaged F1 on the two unseen test graphs, mean of 10 runs (Sec. 3.4, Tables 2–3).
* **Main findings:** Achieves or matches state of the art on all four benchmarks (Tables 2–3): +1.5 / +1.6 points over the best GCN on Cora / Citeseer (83.0 / 72.5 %), equal to GCN on Pubmed (79.0 %); PPI micro-F1 0.973 vs 0.768 (best GraphSAGE) and 0.934 (constant-attention GAT).
* **Assumptions:** Attention scores computed from node features only, a^T[Wh_i ‖ Wh_j] (Sec. 2.1).
* **Weaknesses / reproducibility:** Attention is not a calibrated reliability weight; no edge features (left to future work, Sec. 4).
* **Relation to RA-SCM:** Baseline 3 (GAT).

## Deng & Hooi 2021, Graph neural network-based anomaly detection in multivariate time series, AAAI 35(5)

`deng2021graph` · status **P** · evidence **FT**

* **Research question:** Detect anomalies in multivariate sensor time series when inter-sensor relationships are unknown.
* **Method:** Learn a sensor graph from embedding similarity; graph-attention forecasting; deviation score; attention-based explanation.
* **Data / conditions:** SWaT (51 sensors) and WADI (127 sensors) water-treatment testbeds: two weeks of normal operation for training, test sets with staged attacks (11.97 % / 5.99 % anomalous); 10-s median downsampling, first 2160 samples dropped (Sec. 4.1, Table 1).
* **Metrics:** Precision, recall and F1 over test time ticks, chosen for class imbalance (Sec. 4.3, Table 2).
* **Main findings:** Detects anomalies more accurately than baselines and helps root-cause identification (abstract): F1 0.81 on SWaT and 0.57 on WADI with precision ≈ 0.98–0.99 but recall 0.40–0.68 (Table 2; part of the baseline numbers taken from Li et al. 2019).
* **Assumptions:** Same fixed N sensors in training and test, training data assumed normal, one complete N-dimensional reading per time tick (Sec. 3.1); no missing-data or communication model; single fixed threshold = max of the SMA-smoothed score on validation data (Secs 3.6, 4.3), so reported F1 is tied to this rule (alternatives such as EVT mentioned, not evaluated).
* **Weaknesses / reproducibility:** F1 depends on threshold rule; no missing-data semantics; static learned graph.
* **Relation to RA-SCM:** Representative of graph-based sensor anomaly detection; we add missingness/staleness as a first-class confound and a dynamic physical graph.

## Dang, Karakoc & Jäntti 2023, GNN-based GPS spoofing detection for cellular-connected UAV swarm, IEEE VTC-Spring

`dang2023graphic` · status **P** · evidence **FT**

* **Research question:** Detect GPS spoofing in a UAV swarm using a GNN.
* **Method:** GCN (SimGNN-style) + GRU compare the swarm GPS topology (distances) with the communication topology (free-space path loss); threshold on predicted graph-edit similarity.
* **Data / conditions:** Own Python/TensorFlow simulator with 6, 8 and 10 UAVs, wind and GPS noise, a spoofing attacker; no real data.
* **Metrics:** Accuracy (>90% for 10 UAVs), computation time (<10 ms vs ≈16 s for exact GED).
* **Main findings:** Accuracy decreases as GPS error grows; GRU converges faster than LSTM.
* **Assumptions:** Spoofing does not affect swarm/BS communication; communication topology reflects true geometry (path-loss); path loss is a reliable reference.
* **Weaknesses / reproducibility:** Simulation only; accuracy without class balance or PR-AUC; communication treated as trustworthy ground reference, packet loss/staleness not modelled although the text acknowledges environmental effects on the communication topology.
* **Relation to RA-SCM:** Closest GNN spoof-detector for swarms; it uses the channel as *independent evidence*, whereas we treat the channel as an *unreliable* source and test robustness to it.

## Mykytyn et al. 2023, GPS-spoofing attack detection mechanism for UAV swarms, MECO (arXiv:2301.12766)

`mykytyn2023gps` · status **P** · evidence **FT**

* **Research question:** Detect single- and multi-transmitter GPS spoofing in a swarm without extra hardware beyond ranging.
* **Method:** Compare GPS-derived inter-UAV distances with IR-UWB ranging; flag if the discrepancy exceeds a threshold (with timestamp tolerance).
* **Data / conditions:** None — the text states this is the initial stage and that detection and false-positive rates will be presented later.
* **Metrics:** None reported.
* **Main findings:** Qualitative argument that the mechanism is simple and low-cost.
* **Assumptions:** Ranging available and synchronised with GPS timestamps; thresholds from sensor accuracy.
* **Weaknesses / reproducibility:** No empirical results in the version read; thresholding only.
* **Relation to RA-SCM:** Defines the independent-ranging principle used by our physics baseline and by the identifiability condition.

## Bi et al. 2024, Detection and mitigation of position spoofing attacks on cooperative UAV swarm formations, IEEE TIFS 19

`bi2024detection` · status **P** · evidence **FT(partial)**

* **Research question:** Identify malicious UAVs that falsify reported positions (distributed, collusion, mixed attacks).
* **Method:** Localisation-feasibility problem with reported positions + pairwise distance measurements; semidefinite relaxation; two algorithms exploiting neighbour proximity.
* **Data / conditions:** Matlab simulations of swarms with Gaussian position and ranging noise.
* **Metrics:** Detection success rate (up to +65%, +55%, +51% vs benchmarks).
* **Main findings:** Outperforms benchmarks against the three attack types in simulation.
* **Assumptions:** All UAVs report positions and range neighbours; reports and measurements are received (no packet loss appears in the text); snapshot (non-temporal) formulation.
* **Weaknesses / reproducibility:** Convex-relaxation cost; no temporal evidence; no unreliable-communication model; no learning.
* **Relation to RA-SCM:** Strongest model-based competitor in principle (not re-implemented here — disclosed). Its feasibility test is the identifiability principle we use; communication unreliability would convert 'infeasible' into 'missing'.

## Tolstaya et al. 2020, Learning decentralized controllers for robot swarms with GNNs, CoRL (PMLR 100)

`tolstaya2020learning` · status **P** · evidence **FT**

* **Research question:** Learn local controllers for large teams with limited communication.
* **Method:** Aggregation GNNs on time-varying communication graphs, imitation of a centralised controller.
* **Data / conditions:** Simulated flocking with a changing communication graph.
* **Metrics:** Control performance (abstract).
* **Main findings:** Multi-hop information from distant teammates helps more when the communication radius is small or speeds are high (abstract).
* **Assumptions:** Each communication exchange adds one step of delay (k-hop information is k steps old, Secs 2–3, 'Delayed Aggregation GNNs'); no packet loss or link failure.
* **Weaknesses / reproducibility:** Control, not detection; delivery failures not modelled.
* **Relation to RA-SCM:** Evidence that GNNs on dynamic swarm graphs are practical; its delayed information structure is the precursor of our delayed-message semantics.

## Cini, Marisca & Alippi 2022, GRIN: multivariate time-series imputation by GNNs, ICLR

`cini2022filling` · status **P** · evidence **AB**

* **Research question:** Reconstruct missing values in sensor-network time series.
* **Method:** Bidirectional spatio-temporal message passing recurrent GNN.
* **Data / conditions:** Real-world sensor benchmarks (abstract-level).
* **Metrics:** MAE (improvements often >20% over prior state of the art, abstract).
* **Main findings:** Graph-aware imputation beats non-graph imputers.
* **Assumptions:** Missingness is the only data defect (no adversarial or drifting values).
* **Weaknesses / reproducibility:** Does not separate missing from corrupted data; imputation, not detection.
* **Relation to RA-SCM:** Shows graphs help with *missing* data; our problem is the confusion between missing and *corrupted* data.

## Zhu et al. 2019, Robust GCNs against adversarial attacks, KDD

`zhu2019robust` · status **P** · evidence **AB**

* **Research question:** Make GCNs robust to adversarially perturbed graphs.
* **Method:** Gaussian node representations; variance-based attention reduces the weight of nodes with high variance.
* **Data / conditions:** Three benchmark citation graphs.
* **Metrics:** Node-classification accuracy.
* **Main findings:** Substantial accuracy gains against several attack strategies (abstract).
* **Assumptions:** Variance reflects attack influence.
* **Weaknesses / reproducibility:** Variance is learned, not tied to a physical reliability variable.
* **Relation to RA-SCM:** Prior art for uncertainty-weighted aggregation against *corrupted* (adversarial) inputs, not missing data: reliability *weighting* is **not** new in GNNs; our weights use explicit communication metadata (age, delivery, link quality).


---

# Round 2 additions (pre-submission check, 6 November 2026)

The entries below were added after the IEEE/ACM-oriented search of round 2 (see S1). Every record was confirmed on Crossref or the arXiv API; content statements come from the abstract (AB) or from the stated full-text sections (FT).

## Chen, Meng, Li & Liao 2022, Cooperative fault detection and recovery in the GNSS positioning of mobile agent swarms based on relative distance measurements, Chinese J. Aeronautics 35(5)

`chen2022cooperative` · status **P** · evidence **AB** (publisher PDF not accessible)

* **Method:** Noncentral χ² test of each edge (reported versus measured distance), maximum-likelihood identification of the faulty vertex, distance-based recovery; detectability and recoverability related to the structure of the relative-measurement network.
* **Data / conditions:** Simulation of a swarm crossing a GNSS spoofing zone.
* **Assumptions:** Current, delivered measurements; no packet loss, delay or staleness mentioned.
* **Relation to RA-SCM:** Direct model-based predecessor of our physics baseline; our AoI-aware variant adds an age-dependent covariance.

## He, Shan & Huang 2024, Robust Cooperative Localization With Failed Communication and Biased Measurements, IEEE RA-L 9(3)

`he2024robust` · status **P** · evidence **AB**

* **Method:** Decentralised CL that decouples measurement from communication; other robots' states propagated by an approximate motion model during outages; M-estimation down-weights biased measurements. Simulation.
* **Relation to RA-SCM:** Handles failed communication and faulty measurements *jointly*, but as robust estimation scored by localisation error, not as detection; not UAV-specific, not learned.

## Kargar Tasooji & Parasuraman 2025, Distributed Fault-Tolerant Multi-Robot Cooperative Localization in Adversarial Environments, IROS 2025

`kargartasooji2025distributed` · status **P** · evidence **FT** (arXiv:2507.06750, Sec. III-B, Eq. 8)

* **Method:** Distributed cubature Kalman filter; innovation-norm gate discards manipulated measurements; binary per-link success indicator in jammed zones (prediction-only on failure); adaptive event-triggered communication. Robotarium ground robots.
* **Metrics:** Localisation error (MSLE) and communication rate; detection itself is not scored (no ROC/AUC/F1, no seeds).
* **Relation to RA-SCM:** Closest classical work combining attacks and link failure; link loss is ridden through, not distinguished from attacks.

## Cao, Zhao, Wu, Wang & Gong 2026, Quality-Aware Distributed State Estimation for Multi-UAV Cooperative Localization Under Communication and Navigation Constraints, Drones 10(6)

`cao2026quality` · status **P** · evidence **AB**

* **Method:** Per-neighbour multiplicative quality score from freshness (AoI), accuracy (covariance trace) and link reliability (packet loss, channel noise); AND-gate excludes neighbours degraded in both AoI and covariance; quality-squared information update with covariance-intersection fallback; theorems on soft attenuation of single-axis faults.
* **Metrics:** Position RMSE in Monte Carlo runs (3–50 UAVs).
* **Relation to RA-SCM:** Closest model-based analogue of AoI- and link-quality-driven weighting; an estimator, not a detector, with no learned or graph comparison.

## Ou, Liang & Lam 2023, FPECMV: Learning-Based Fault-Tolerant Collaborative Localization Under Limited Connectivity, IROS 2023

`ou2023fpecmv` · status **P** · evidence **AB**

* **Method:** CNN-based confidence evaluation and a fault-isolation module using randomly occurring relative measurements, for CL with limited or discontinued observation and communication; BULLET simulation and physical robots (21.0% localisation improvement).
* **Relation to RA-SCM:** Learned fault handling under limited connectivity, but judged on localisation accuracy, ground robots, no controlled loss model.

## Vijay et al. 2025, Range-Based Multi-Robot Integrity Monitoring For Cyberattacks and Faults: An Anchor-Free Approach, IEEE RA-L 10(3)

`vijay2025range` · status **P** · evidence **FT** (arXiv:2408.11155, Sec. III-B)

* **Method:** Inter-robot ranges detect and identify attacked or faulty robots and reconstruct their errors (sequential convex programming + ADMM); PX4-SITL/Gazebo under GNSS spoofing and real Crazyflie UAVs.
* **Assumptions:** Synchronous communication between neighbours (Sec. III-B).
* **Relation to RA-SCM:** Strongest model-based range-consistency detector found; delivery assumed.

## Michieletto, Formaggio, Cenedese & Tomasin 2023, Robust Localization for Secure Navigation of UAV Formations Under GNSS Spoofing Attack, IEEE T-ASE 20(4)

`michieletto2023robust` · status **P** · evidence **AB**

* **Method:** Information-theoretic threshold test of consistency between inertial, relative-ranging and GNSS data, then reliability-based fusion; numerical validation.
* **Relation to RA-SCM:** Multimodal consistency testing for formations; no communication-loss model.

## Park & Yoo 2026, Rigid-Covert GNSS Spoofing of UAV Swarms, arXiv:2608.06885

`park2026rigid` · status **X** · evidence **FT**

* **Main findings:** A common, slowly varying offset of the whole swarm preserves all pairwise distances and is unobservable to relative-only detectors (distance-verification and SDP baselines near chance AUC over 200 seeds); anchor-based detection floor and recovery (simulation, SITL, Gazebo). Ranging packet loss is swept only for recovery.
* **Relation to RA-SCM:** Formal support for our identifiability statement; RA-SCM inherits this blind spot.

## Sophia et al. 2026, Zero-trust graph-attentive intelligence for Byzantine-resilient UAV swarms under communication constraints, Discover Electronics 3(1)

`sophia2026zerotrust` · status **P** · evidence **AB** (Springer full text not retrievable)

* **Method:** 8-head GAT with a zero-trust layer (behavioural scoring, attestation, neighbourhood analysis); UAVSwarm data with a Byzantine and communication overlay (spoofing, replay, Sybil, gradient poisoning; 5–33% corrupted nodes).
* **Metrics:** Byzantine F1 96.8% (model-level comparison; 92.83% mean over 12 attack × corruption conditions), trust accuracy, consensus latency, packet delivery ratio.
* **Relation to RA-SCM:** Learned graph detector for swarms in which communication is a bandwidth constraint and an outcome, not a modelled confounder of position-consistency evidence; no physics baseline.

## Pan et al. 2026, Satellite-Aided Multi-UAV Secure Collaborative Localization via Spatio-Temporal Anomaly Detection and Diagnosis, Drones 10(1)

`pan2026satellite` · status **P** · evidence **AB**

* **Method:** GAT with a time-attention VAE on multidimensional ranging sequences detects false ranging data from malicious UAVs; diagnosis by anomaly scoring; KNN correction (simulation; +25.9% localisation accuracy).
* **Relation to RA-SCM:** Closest learned graph detector on relative (ranging) data; delivery of measurements assumed.

## Tariq, Ahanger & Shaukat 2026, Tri-stream multi-model architecture for real-time detection of BeiDou signal manipulation in UAV swarms, Scientific Reports 16

`tariq2026tristream` · status **P** · evidence **FT** (PMC full text)

* **Method:** Kalman-residual tracking plus CNN/LSTM/GNN fusion and a transformer-based language model; software-in-the-loop simulation (97 ± 0.6% detection accuracy).
* **Conditions:** Simulator with per-packet delay, burst-capable packet drop, bandwidth caps, freshness-window gating and jamming; paired t-tests over matched seeds. Inter-UAV ranging is not used.
* **Relation to RA-SCM:** A learned graph swarm detector run under modelled loss (sensitivity to delay and loss is mentioned but not shown); no loss-stratified results and no physics-only arm are reported.

## Tariq & Shaukat 2026, Mission-aware BeiDou spoofing defense in UAV swarms with LLM-assisted context validation, Frontiers in Communications and Networks 7

`tariq2026mission` · status **P** · evidence **FT**

* **Method:** OrbitGuardNet: transformer encoders, GNNs and Kalman-residual analysis with LLM context validation; UWB inter-UAV ranging; simulation and pilot flights with three UAVs (software-injected spoofing).
* **Conditions:** Gilbert–Elliott channel with delays and bursty loss (Sec. 2.1.3); paired t-tests; packet loss named as a future test condition, not varied.
* **Relation to RA-SCM:** Closest learned work; lacks loss as a controlled confounder and a standalone age-aware physics baseline.

## Moustafa & Abdelghany 2026, Finite-Trace Cellular Sheaves for Validation and Estimation of Hybrid Dynamical Systems, IEEE Control Systems Letters 10

`moustafa2026finite` · status **P** · evidence **AB**

* **Method:** Finite-trace cellular sheaf with affine restriction maps for hybrid and networked executions with partial and non-simultaneous data; convex best-section estimator; per-cell residual scores localise model inconsistency; demonstrated on a DC microgrid and a linearised drone pose graph (corrupted-observation localisation).
* **Relation to RA-SCM:** Non-learned sheaf fault localisation with affine maps; no packet-loss or AoI model.

## Foundational and context sources (round 2)

| Key | Work | Status / evidence | Used for |
|---|---|---|---|
| `kaul2012realtime` | Kaul, Yates & Gruteser 2012, Real-time status: how often should one update?, IEEE INFOCOM | P / AB | definition of age of information |
| `sinopoli2004kalman` | Sinopoli et al. 2004, Kalman filtering with intermittent observations, IEEE TAC 49(9) | P / AB | lost packets as intermittent observations |
| `julier1997nondivergent` | Julier & Uhlmann 1997, covariance intersection, ACC | P / AB | fusion under unknown correlation (no detection) |
| `willsky1976survey` | Willsky 1976, failure detection in dynamic systems, Automatica 12(6) | P / AB | residual-based fault detection |
| `brown1992baseline` | Brown 1992, a baseline GPS RAIM scheme, Navigation 39(3) | P / AB | GPS integrity monitoring |
| `kerns2014unmanned` | Kerns et al. 2014, UAV capture via GPS spoofing, J. Field Robotics 31(4) | P / AB | field evidence of UAV spoofing |
| `tippenhauer2011requirements` | Tippenhauer et al. 2011, requirements for GPS spoofing attacks, ACM CCS | P / AB | spoofing several receivers |
| `hayat2016survey` | Hayat, Yanmaz & Muzaffar 2016, UAV networks survey, IEEE COMST 18(4) | P / AB | intermittent UAV links |
| `gilbert1960capacity` | Gilbert 1960, capacity of a burst-noise channel, Bell Syst. Tech. J. 39(5) | P / AB | Gilbert–Elliott burst-loss model (round 1) |
| `elliott1963estimates` | Elliott 1963, error rates on burst-noise channels, Bell Syst. Tech. J. 42(5) | P / AB | Gilbert–Elliott burst-loss model (round 1) |
