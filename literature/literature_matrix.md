# Comparative literature matrix

Status: P = peer-reviewed, W = workshop paper, X = arXiv preprint. Evidence: FT = key sections of the full text read, AB = abstract/metadata page only (items marked [recalled] contain details from the author's prior knowledge that must be re-checked against the full text before submission).

## Hansen & Gebhart 2020, Sheaf Neural Networks, arXiv:2012.06333

`hansen2020sheaf` · status **W** · evidence **AB**

* **Research question:** Can the diffusion step of a GCN be generalised from the graph Laplacian to a sheaf Laplacian?
* **Method:** Replace graph diffusion by sheaf-Laplacian diffusion with vector-space stalks and restriction maps.
* **Data / conditions:** Synthetic semi-supervised node classification on signed graphs.
* **Metrics:** Node-classification accuracy.
* **Main findings:** Sheaf networks outperform Kipf–Welling GCN in the synthetic signed-graph setting (abstract).
* **Assumptions:** Sheaf supplied by the construction of the task; learning the sheaf is not the contribution (a 2025 survey states it was proposed but not implemented — secondary statement).
* **Weaknesses / reproducibility:** Synthetic data only; workshop paper; no real benchmark; no dynamic graphs.
* **Relation to RA-SCM:** Origin of sheaf-based message passing. We reuse the sheaf-Laplacian operator, not any result.

## Bodnar et al. 2022, Neural Sheaf Diffusion, NeurIPS (arXiv:2202.04579)

`bodnar2022neural` · status **P** · evidence **AB**

* **Research question:** How does the (implicit trivial) sheaf of a GNN explain heterophily and oversmoothing, and can learning the sheaf fix both?
* **Method:** Learn restriction maps from node features of the two endpoints of an edge; discretised sheaf diffusion layers; theory on linear separability and asymptotic behaviour.
* **Data / conditions:** Standard node-classification benchmarks, homophilic and heterophilic [recalled: Texas, Wisconsin, Cornell, Film, Squirrel, Chameleon, Cora, Citeseer, Pubmed].
* **Metrics:** Accuracy [recalled].
* **Main findings:** Competitive (NeurIPS/arXiv abstract) or state-of-the-art (ICLR slide page wording) results on heterophilic graphs; non-trivial sheaves give control over diffusion limits.
* **Assumptions:** Static graph; maps conditioned on node features only; no edge features, measurement noise or missing edges; homophily/heterophily as the task structure.
* **Weaknesses / reproducibility:** Fixed benchmark splits; cost grows with stalk dimension; claims concern node classification, not detection of local inconsistencies; wording of the headline claim differs between venues (see search record).
* **Relation to RA-SCM:** Baseline 4 ('standard sheaf') is an NSD-style implementation of this idea in our dense framework. RA-SCM adds edge-conditioned maps, translation term, reliability weights and temporal state.

## Barbero et al. 2022, Sheaf NNs with Connection Laplacians (PMLR 196)

`barbero2022connection` · status **W** · evidence **AB**

* **Research question:** Is it necessary to learn the sheaf, or can restriction maps be computed from geometry?
* **Method:** Orthogonal restriction maps aligning neighbouring local tangent spaces (manifold assumption), not learned.
* **Data / conditions:** Node-classification benchmarks (abstract-level only).
* **Metrics:** Accuracy.
* **Main findings:** Matches or beats the learned-sheaf models of Bodnar et al. on most datasets and beats random sheaves (abstract).
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

`hansen2019spectral` · status **P** · evidence **AB**

* **Research question:** What are the spectral properties of the sheaf Laplacian and how do they relate to cohomology and graph structure?
* **Method:** Hodge-type Laplacian of cellular sheaves; interlacing, sparsification, effective resistance, synchronisation (abstract).
* **Data / conditions:** Theory.
* **Metrics:** n/a
* **Main findings:** Foundations of sheaf Laplacian spectra; links kernel to global sections.
* **Assumptions:** Finite cell complexes; inner products on stalks define the Laplacian [recalled — verify in the text].
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
* **Data / conditions:** Field experiment tracking black bears: 12 GPS collars (6 stationary), four sensor types (collar GPS, VHF, text report, vehicle GPS), 16 observations per 2-h session.
* **Metrics:** Consistency radius (m) and filtration.
* **Main findings:** Radius decreases as the VHF error shrinks when the team approaches; largest discrepancy VHF vs collar GPS at the analysed instant (464.5 m).
* **Assumptions:** Sensor relationships and coordinate conversions specified in advance; time slices analysed independently.
* **Weaknesses / reproducibility:** Radius does not say which measurement is wrong; small case study; no learning, no dynamics, no communication model.
* **Relation to RA-SCM:** Closest prior use of sheaf consistency for geolocation fusion; shows consistency flags disagreement but not its cause — exactly the ambiguity (anomaly vs missing data) we study.

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

## Ribeiro et al. 2025, Cooperative Sheaf Neural Networks, arXiv:2507.00647

`ribeiro2025cooperative` · status **X (ICLR 2026 per arXiv comment)** · evidence **AB**

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

`hernandez2026sheaf` · status **X** · evidence **AB**

* **Research question:** Is the sheaf Laplacian a suitable mechanism for data fusion and consensus in distributed sensing?
* **Method:** Sheaf-theoretic framework (abstract-level).
* **Data / conditions:** not extracted
* **Metrics:** not extracted
* **Main findings:** not extracted
* **Assumptions:** unknown
* **Weaknesses / reproducibility:** Only the abstract page was read; the abstract mentions neither anomaly detection, learning, packet loss nor UAVs.
* **Relation to RA-SCM:** Possible close relative on the model-based side — the full text must be read before claiming novelty.

## Kipf & Welling 2017, GCN, ICLR

`kipf2017semi` · status **P** · evidence **AB [recalled]**

* **Research question:** Scalable semi-supervised learning on graphs.
* **Method:** First-order spectral approximation; Â = D^-1/2 (A+I) D^-1/2.
* **Data / conditions:** Citation networks and a knowledge graph.
* **Metrics:** Accuracy.
* **Main findings:** Outperforms related methods by a significant margin (abstract).
* **Assumptions:** Homophily; static graph; no edge features.
* **Weaknesses / reproducibility:** Oversmoothing with depth; single static graph.
* **Relation to RA-SCM:** Baseline 2 (GCN).

## Veličković et al. 2018, GAT, ICLR

`velickovic2018graph` · status **P** · evidence **AB [recalled]**

* **Research question:** Learn neighbour weights by attention.
* **Method:** Masked self-attention over neighbourhoods, multi-head.
* **Data / conditions:** Citation networks, PPI [recalled].
* **Metrics:** Accuracy / micro-F1 [recalled].
* **Main findings:** State of the art on the four benchmarks at the time [recalled].
* **Assumptions:** Attention scores computed from node features only.
* **Weaknesses / reproducibility:** Attention is not a calibrated reliability weight; no edge features.
* **Relation to RA-SCM:** Baseline 3 (GAT).

## Deng & Hooi 2021, Graph neural network-based anomaly detection in multivariate time series, AAAI 35(5)

`deng2021graph` · status **P** · evidence **AB**

* **Research question:** Detect anomalies in multivariate sensor time series when inter-sensor relationships are unknown.
* **Method:** Learn a sensor graph from embedding similarity; graph-attention forecasting; deviation score; attention-based explanation.
* **Data / conditions:** Two real-world sensor datasets with labelled anomalies (abstract; SWaT/WADI [recalled]).
* **Metrics:** Precision, recall, F1 [recalled].
* **Main findings:** Detects anomalies more accurately than baselines and helps root-cause identification (abstract).
* **Assumptions:** Fixed sensor set, synchronous complete observations, no communication layer; thresholding protocol affects F1 [recalled].
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

`tolstaya2020learning` · status **P** · evidence **AB**

* **Research question:** Learn local controllers for large teams with limited communication.
* **Method:** Aggregation GNNs on time-varying communication graphs, imitation of a centralised controller.
* **Data / conditions:** Simulated flocking with a changing communication graph.
* **Metrics:** Control performance (abstract).
* **Main findings:** Multi-hop information from distant teammates helps more when the communication radius is small or speeds are high (abstract).
* **Assumptions:** Perfect delivery on the current graph.
* **Weaknesses / reproducibility:** Control, not detection; delivery failures not modelled in the abstract.
* **Relation to RA-SCM:** Evidence that GNNs on dynamic swarm graphs are practical; supports the dynamic-graph design (not the reliability question).

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
* **Relation to RA-SCM:** Prior art for uncertainty-weighted aggregation: reliability *weighting* is **not** new in GNNs; our weights use explicit communication metadata (age, delivery, link quality).

