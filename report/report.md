---
title: "Reliability-Aware Sheaf Consistency for Distinguishing UAV Position Anomalies from Communication Failures: A Falsifiable Simulation Study"
lang: en
---

<p class="author">Mehmet Ünlü (040230253) · unlu23@itu.edu.tr · Istanbul Technical University, Electronics and Communication Engineering · EHB 420E Artificial Neural Networks · HW1 – From Curiosity to Scientific Discovery · 6 November 2026</p>
<p class="subtitle-note">Supplementary material (separate PDF): literature matrix, search log, gap analysis. Code, data and dashboard: https://github.com/unlumehmet30/uav-sheaf-research</p>

<div class="abstract"><p><strong>Abstract.</strong> A UAV swarm must tell a wrong position report from a merely stale one, because packet loss and localisation faults both create inconsistencies between reported and measured relative positions. Cooperative localisation tolerates lost links and faulty measurements jointly, and learned swarm detectors have been simulated with packet loss, but in the literature we searched none compares detectors of UAV position anomalies under controlled, condition-stratified loss, burst loss and age of information against an age-aware physical-consistency baseline. We propose RA-SCM (Reliability-Aware Sheaf Consistency Model), a sheaf-diffusion detector whose messages are read from the time of the last delivered packet, with edge-conditioned restriction maps and reliability weights derived from delivery state, age and link quality. We hypothesise that it beats the best capacity-matched GCN, GAT or neural-sheaf baseline by at least 0.02 PR-AUC (area under the precision–recall curve) in four of six loss conditions. A simulator with sudden, drift and spoof-like anomalies, iid, Gilbert–Elliott and targeted communication failures, leakage tests and five seeds supplies the evidence; nothing is validated on real flights. RA-SCM has the highest mean PR-AUC in all seven main conditions (0.975 at 50% iid loss, 0.967 at 50% bursts) and beats an age-aware physics test, but the hypothesis is not supported: its margin over the best conventional GNN reaches 0.02 only under 50% bursts (+0.028 [+0.013, +0.043], 95% CI) and is absent without loss. Ablations attribute the gain to the reliability inputs, not to learned sheaf maps. The contribution is a falsifiable benchmark and a negative-leaning answer.</p></div>


## 1. Introduction and motivation

A cooperative UAV swarm keeps its formation by exchanging position estimates and comparing them with local relative measurements. Two very different failures disturb this exchange in a similar way. A *localisation failure* (GNSS spoofing, drift, a jump in the position filter) makes a UAV report a wrong position; a *communication failure* (packet loss, bursts, link blockage) makes the receivers work with old reports. In both cases a receiver that compares a neighbour's last report with its own relative measurement sees a discrepancy. If an outage is read as an attack, the swarm raises false alarms and may break formation unnecessarily; if an attack is read as a link problem, it goes unnoticed. This matters to operators of inspection and search-and-rescue swarms and to those who certify them.

We became interested while comparing swarm spoofing detectors: they use communication or ranging as independent evidence, and those we reviewed assume that it arrives, treat the channel itself as a trusted reference, or include loss in the simulator without testing whether it is mistaken for an attack (Section 3). Neural sheaf diffusion (NSD) expresses edge-wise consistency naturally [@bodnar2022neural], so we ask whether a reliability-aware sheaf model, the Reliability-Aware Sheaf Consistency Model (RA-SCM), helps or a simpler statistical test suffices, and design the experiment so that it can fail.

## 2. Problem statement and supporting evidence

**Setting.** UAVs $i=1,\dots,N$ move in the plane. UAV $i$ has a real state $(p_i, v_i)$, a *measured* position $\tilde p_i = p_i + w_i$, and broadcasts a *reported* position $\hat p_i = \tilde p_i + o_i(t)$, where $o_i(t)$ is an anomaly offset (0 in normal operation). An IMU supplies a velocity estimate $\hat v_i$, and a relative sensor gives $r_{ij} = p_j - p_i + n_{ij}$ for neighbours within range. Packets from $j$ reach $i$ with an indicator $m_{ij}(t)\in\{0,1\}$; $a_{ij}(t)$, the number of steps since the last delivery, is the age of information (AoI) of the link [@kaul2012realtime]. **Task:** output for each UAV and step a score for the event $\lVert o_i(t)\rVert\ge\theta$ ($\theta=2$ m), using only information a UAV could have received.

**Evidence that the problem exists.** (i) GNSS spoofing has captured a small UAV in a field test [@kerns2014unmanned], and spoofing several receivers at once, as in a swarm, has been analysed theoretically [@tippenhauer2011requirements]. (ii) UAV-to-UAV links are intermittent because of mobility, range and environment [@hayat2016survey; @dang2023graphic]. (iii) In our simulation (Section 9) a consistency test that treats the last received report as current falls from 0.894 PR-AUC without loss to 0.519 under 50% burst loss (a simulation outcome, not field data). We found no public dataset that combines labelled position anomalies with logged packet loss, hence the simulation.

**Root cause or symptom?** The root cause is a modelling assumption at the *detection* stage: swarm detectors assume that reports and ranges arrive, trust the channel, or include loss without measuring its confounding effect, while estimators that handle lost or stale data down-weight or exclude it without deciding whether a report is wrong or merely stale (Section 3). It is unsolved because a stale and a wrong report produce similar residuals, so separating them needs explicit delivery metadata (Section 5); because most detectors were evaluated only in simulation and none with loss-stratified results (Table 1); and because no shared dataset exists.

## 3. Critical literature review

**Search protocol.** Round 1 (27 October 2026): a general web search tool, the arXiv and Crossref APIs and publisher pages (22 queries). Round 2 (6 November 2026): 24 structured queries over OpenAlex (14), Crossref restricted to IEEE and ACM records (5) and Semantic Scholar (5), from 2018 on (765 titles and 83 abstracts screened), plus reference chasing in cooperative localisation; IEEE Xplore and ACM DL themselves were not queried. Keywords: *sheaf neural network / sheaf Laplacian / graph neural network* × *anomaly or fault detection, GNSS spoofing, UAV swarm, cooperative localization, packet loss, age of information, missing data*. *Included:* sheaf learning, sensor sheaves, GNN anomaly/spoofing detection, swarm consistency and cooperative localisation under faults or lossy links, GNNs under missing data; verifiable, peer-reviewed or labelled preprints. *Excluded:* patents, aggregators, network intrusion detection, single-UAV GNSS authentication, unreviewed low-visibility items. Of 43 references, key sections of 19 were read in full text, the rest at abstract level (per-paper evidence level in the supplementary literature matrix).

**Sheaf learning.** Sheaf Laplacians generalise graph diffusion: hand-built sheaves beat GCN on synthetic signed graphs [@hansen2020sheaf], and maps learned from node features are competitive on heterophilic node classification and provably control oversmoothing better than a trivial sheaf [@bodnar2022neural]. *Contested:* by the authors' account, maps *computed* from geometry match or beat learned ones on most of nine benchmarks but trail them on the dense Squirrel and Chameleon graphs (and slightly on Cora) [@barbero2022connection]. Nonlinear [@zaghen2024nonlinear], directed [@ribeiro2025cooperative] and temporal [@asif2026temporal] variants target classification or link prediction.

**Sheaves for consistency and faults.** Sensor sheaves measure disagreement [@robinson2017sheaves]. In a field study (six sessions with decoy collars, six with GPS collars on three black bears) a consistency filtration attributes disagreement to sensors, but the authors note that neither it nor the radius says which measurements are trustworthy, and staleness is not modelled [@joslyn2020sheaf]. A conceptual preprint proposes the sheaf Dirichlet energy as an anomaly score that localises a faulty node and names packet loss as a challenge, without experiments [@hernandez2026sheaf]; finite-trace sheaves with affine maps localise a corrupted observation on a drone pose graph [@moustafa2026finite]; sheaf coordination assumes a fixed, lossless topology [@hanks2025distributed]. None is learned or evaluated under modelled loss.

**Swarm position-fault and spoofing detectors** compare reported positions with ranges: thresholds without reported detection rates [@mykytyn2023gps], a semidefinite feasibility test [@bi2024detection], $\chi^2$ edge tests with faulty-vertex identification [@chen2022cooperative], multimodal consistency [@michieletto2023robust], and range-based integrity monitoring, demonstrated in mixed-reality flights with real Crazyflies, that assumes synchronous communication [@vijay2025range]. Learned ones use a GCN+GRU on GPS-versus-communication topology, assuming spoofing leaves the channel unaffected and using path loss as reference [@dang2023graphic], a graph-attention VAE on ranging sequences [@pan2026satellite], or a zero-trust GAT in which bandwidth is a constraint and packet delivery an outcome, not a confounder [@sophia2026zerotrust]. The closest are two learned spoofing detectors combining Kalman residuals with GNNs, run in simulators with delay and bursty loss (Gilbert–Elliott in one, freshness gating in the other) and compared with paired $t$-tests; neither reports loss-stratified results or a physics-only arm, and one avoids inter-UAV ranging [@tariq2026tristream; @tariq2026mission]. No relative-only detector can see a rigid common-mode shift of the swarm [@park2026rigid].

**Estimation with lost, stale or faulty data.** Lost packets are intermittent observations [@sinopoli2004kalman], estimates with unknown correlation are fused by covariance intersection [@julier1997nondivergent], and residual tests detect faulty measurements [@willsky1976survey; @brown1992baseline]. Recent cooperative localisation handles failed links and faulty measurements *together*: M-estimation with motion-model propagation [@he2024robust], an innovation gate under jamming [@kargartasooji2025distributed], learned confidence with fault isolation [@ou2023fpecmv], and a neighbour quality score combining AoI, covariance and packet loss [@cao2026quality]. They down-weight or exclude data and are scored by localisation error; none decides whether a report is *wrong* or merely *stale*. In graph learning, imputation fills *missing* values [@cini2022filling] and variance-based attention resists *adversarially corrupted* graphs [@zhu2019robust]; neither separates the two. GDN forecasts sensors from a complete, synchronous window [@deng2021graph]; decentralised GNN controllers read $k$-hop data $k$ steps late but model no loss [@tolstaya2020learning].

**Contradictions, metrics, reproducibility.** Whether maps must be learned is contested; the independent evidence differs (ranging, path loss, inertia). Metrics are incomparable (accuracy, success rate, localisation error, F1, none); no detector reports precision–recall area or false alarms under controlled loss. In the sections read, only one UAV paper states released code [@park2026rigid] (not systematically checked), and most use their own simulators. **Transfer risk:** sheaf gains concern node classification, not local inconsistency detection on a time-varying swarm graph.

| Work | Approach; evidence | Metric (result) | Unreliable delivery | Limitation here |
|---|---|---|---|---|
| Bodnar et al. 2022 | NSD, learned maps; 9 node-classification benchmarks | accuracy (1st on 5 of 6 heterophilic) | no | static graph, no edge features |
| Barbero et al. 2022 (W) | maps computed from geometry; same benchmarks | accuracy (≈ learned on most) | no | manifold assumption |
| Joslyn et al. 2020 | consistency radius and filtration; GPS-collar field study | radius (m) | no | missing vs wrong not separated |
| Hernández & Sánchez-Soto 2026 (X) | Dirichlet energy as anomaly score; conceptual | none | named only | no evaluation |
| Moustafa & Abdelghany 2026 | finite-trace sheaf, affine maps; drone pose graph | residual localisation | non-simultaneous data | not learned, no loss model |
| Dang et al. 2023 | GCN+GRU, GPS vs channel topology; simulation | accuracy (>90%) | no (channel is reference) | no class-balanced metric |
| Bi et al. 2024 | semidefinite feasibility; simulation | success rate | no | snapshot, all data received |
| Chen et al. 2022 | $\chi^2$ edge tests, ML vertex identification; simulation | detection, recovery | no | current data assumed |
| Vijay et al. 2025 | range-based integrity monitoring; SITL, Crazyflie | detection, error | no (synchronous) | delivery assumed |
| Sophia et al. 2026 | GAT + zero-trust layer; UAVSwarm + overlay | Byzantine F1 (0.968) | bandwidth only | no physics baseline |
| Pan et al. 2026 | GAT + time-attention VAE on ranging; simulation | localisation (+25.9%) | no | delivery assumed |
| Tariq et al. 2026; Tariq & Shaukat 2026 | Kalman residuals + GNN (CNN/LSTM or transformer); simulation, 3-UAV pilot | accuracy (≈97–98%), paired $t$-tests | delay, bursty loss; staleness gating (one) | no loss-stratified results; no physics-only arm |
| He et al. 2024 | decoupled CL, M-estimation; simulation | localisation error | failed links | estimation, not detection |
| Kargar Tasooji & Parasuraman 2025 | cubature KF, innovation gate; Robotarium | localisation error | binary link failure | detection not scored |
| Cao et al. 2026 | AoI × covariance × link-quality score; Monte Carlo | RMSE | AoI, packet loss | estimator, not detector |
| Cini et al. 2022 | graph imputation (GRIN); sensor data | MAE | missing values | corruption not flagged |
| Deng & Hooi 2021 | GDN, attention forecasting; SWaT, WADI | F1 (0.81, 0.57) | no (complete window) | threshold-dependent F1 |

*Table 1. Closest works (W workshop paper, X preprint, CL cooperative localisation, KF Kalman filter, ML maximum likelihood). Research questions, assumptions and evidence levels: supplementary literature matrix.*

## 4. Research gap

> Model-based cooperative localisation already tolerates failed links, packet loss and AoI together with faulty measurements, and learned graph detectors of swarm spoofing have been run in simulators that include packet loss. Within the sources we could access, however, no study reports how detectors of UAV position anomalies, learned graph- or sheaf-based ones in particular, built on the consistency of reported positions with inter-UAV relative measurements, perform when **iid loss, burst loss and AoI are controlled and results are stratified by condition**, compared against **a standalone age-aware physical-consistency baseline**.

*Supporting publications:* swarm detectors assume that reports and ranges arrive [@bi2024detection; @chen2022cooperative; @vijay2025range] or use the channel as reference [@dang2023graphic]; learned ones treat communication as a bandwidth constraint [@sophia2026zerotrust], assume delivery [@pan2026satellite], or simulate loss but report no loss-stratified results or physics-only test [@tariq2026tristream; @tariq2026mission]; robust estimators down-weight data and are scored by localisation error [@he2024robust; @kargartasooji2025distributed; @cao2026quality]; sheaf methods localise inconsistent sensors without a loss model [@joslyn2020sheaf; @hernandez2026sheaf; @moustafa2026finite]. The gap is *experimental and methodological*. Caveats: IEEE Xplore and ACM DL were reached only through metadata indexes, and seven works of Table 1 were read at abstract level only. If nobody closes it, detectors stay validated on links that never fail, and those that ignore staleness read outages as attacks (in our simulation: 0.894 → 0.519 PR-AUC under 50% bursts).

## 5. Proposed solution: RA-SCM

**Inconsistency measure.** For receiver $i$ and neighbour $j$ with last delivery $\tau_{ij}=t-a_{ij}$,
$$e_{ij}(t)=\big(\hat p_j(\tau_{ij})+\hat v_j(\tau_{ij})\,a_{ij}\Delta t-\hat p_i(t)\big)-r_{ij}(t).$$
If only $i$ is displaced by a constant $o_i$, then $E[e_{ij}]={-o_i}$ and $E[e_{ji}]={+o_i}$ (in general $o_i(\tau_{ji})$); if $j$'s cached report was displaced, $E[e_{ij}]=o_j(\tau_{ij})$. Without anomaly the covariance grows with age,
$$\Sigma_{ij}(a)=(\sigma_i^2+\sigma_j^2+\sigma_r^2)I+\big[(a\Delta t\,\sigma_v)^2+(\tfrac12\sigma_{acc}(a\Delta t)^2)^2\big]I .$$
Summed over pairs, $\sum e_{ij}^\top\Sigma_{ij}^{-1}e_{ij}=\lVert\delta x-r\rVert_W^2$ is the affine Dirichlet energy of a cellular sheaf with stalks $(\hat p,\hat v)$, receiver map $[I\;\,0]$, sender map $[I\;\;a_{ij}\Delta t\,I]$ on the cached state, edge datum $r_{ij}$ and edge inner product $\Sigma_e^{-1}$; its quadratic part is $x^\top L_w x$, $L_w=\delta^\top W\delta$ [@hansen2019spectral]. The **AoI-aware physics test** (Baseline 1) uses these residuals and precision weights $w_{ij}$ with fixed maps and scores UAV $i$ by $u_i=\big(\sum_j w_{ji}e_{ji}-\sum_j w_{ij}e_{ij}\big)/\sqrt{W_i}$, $W_i=\sum_j(w_{ij}+w_{ji})$, half the energy gradient with respect to a shift of $\hat p_i$: for an offset of $i$ alone $E[u_i]=\sqrt{W_i}\,o_i$, so the displaced UAV is localised. $u_i$ is smoothed causally and combined (maximum) with an IMU-versus-position kinematic test. It extends the edge tests of @chen2022cooperative with an age-dependent covariance; the naive variant uses the uncompensated residual and no age term.

**Four situations kept apart.** *Out of range* (no edge); *in range, never received* ($w=0$: no evidence, never a fault); *received but stale* (small $w$, motion-compensated residual); *corrupted report* (fresh data, residuals consistent across neighbours). In the physics test missing data only lowers a weight; in RA-SCM delivery state and age also enter $\Phi$, the translation and the head, so the separation is a design goal the model must learn, not a guarantee. *Identifiability:* a common offset of all UAVs leaves every relative quantity unchanged [@park2026rigid]; only its changes are seen, through the IMU velocity versus the position difference (jumps and ramps, not a static bias after onset). A spoofed group is visible only on boundary edges, and a UAV without usable neighbours keeps only this kinematic check.

**Architecture** (Figure A1). Node features (IMU velocity, kinematic residual, self-reported accuracy, degree) are encoded into stalk states $x_i\in\mathbb R^{d\times f}$. Each of two sheaf layers reads neighbour states *from the time of the last delivered packet*, computes restriction maps $F_i,F_j=\tanh\Phi(x_i,x_j,e_{ij})$, a translation $b_{ij}\in\mathbb R^{d\times f}$ from a second head of $\Phi$, the residual $\rho_{ij}=F_ix_i-F_jx_j-b_{ij}$ (a sheaf on stalks augmented by $f$ constant coordinates), weights $w_{ij}=\sigma(\text{MLP}[m_{ij},a_{ij},q_{ij},h_{ij}])$ from delivery, age, a link-quality proxy $q_{ij}$ and a has-ever-received flag $h_{ij}$, and updates $x_i\leftarrow\text{LN}\big(x_i-\text{ELU}\big((\textstyle\sum_j w_{ij}F_i^\top\rho_{ij}/\sum_j w_{ij})\,\Theta\big)\big)$ with a learned $\Theta\in\mathbb R^{f\times f}$. The weighted energy and the evidence mass $\sum_jw_{ij}$ feed a GRU and an MLP head (17.6k parameters; cost $O(|E|(2df+F_e)K+|E|d^2 f)$ per layer, $F_e$ edge features, $K$ width of $\Phi$). Because $\Phi$ sees direction-specific features and $w_{ij}\neq w_{ji}$, each receiver uses its own maps: the layer is a receiver-centric, *sheaf-inspired* diffusion that equals the weighted sheaf Laplacian only for symmetric maps and weights and zero ages (the unit-tested case).

**What is original.** *Taken:* sheaf Laplacian, NSD-style diffusion, GCN/GAT, uncertainty weighting, Gilbert–Elliott loss, AoI, edge consistency tests [@chen2022cooperative]. *Adapted:* delayed-message semantics, extending the delayed information structure of decentralised GNN controllers [@tolstaya2020learning] to the age of the last delivered packet; affine restriction [used, non-learned, by @moustafa2026finite]. *New in combination:* receiver-specific reliability weights learned from delivery metadata, with evidence mass, inside sheaf-style diffusion; weighting neighbours by AoI and link quality is itself known from estimation [@cao2026quality]. The main claim is the *protocol*, whose elements partly appear elsewhere [modelled loss and paired seeds in @tariq2026tristream] but not in combination: loss, burst and targeted-blackout confounding, a frozen operating point, paired seeds, an age-aware physics control and ablations that separate edge conditioning, maps, weights, the reliability channel and temporal memory. *Failure modes:* maps collapsing to identity (RA-SCM then equals an edge-conditioned message-passing network, MPNN-E), saturated weights, shortcut reliance on age. *Simpler alternatives:* the AoI-aware physics test; GCN/GAT with the same inputs. *Weakest assumption:* that white Gaussian noise and a two-state Gilbert–Elliott channel represent real UAV sensing and links; with longer-memory loss or heavy-tailed noise the learned weights and frozen thresholds may not transfer, which is why the €500 plan calibrates channel and noise first. 


## 6. Methodology and experimental design

**Data (simulated).** A 2-D swarm of 5, 10 or 20 UAVs tracks formation slots (circle, line, wedge; grid unseen) behind a leader (random-turn, circle; Lissajous unseen) with a proportional–derivative law, bounded acceleration and wind (*T* = 100 steps of 0.5 s). Sensors: GNSS-like noise 1 m, relative sensor 0.3 m, IMU velocity 0.2 m/s, range 30 m, formation "breathing" that changes the graph. *Anomalies* are added to the reported position: sudden step (4–12 m), drift (0.2–0.6 m/step), spoof-like common offset of 1–3 UAVs (6–15 m, ramped), or a mixture; steps with $\lVert o_i\rVert\ge 2$ m are positive, and active injections below 2 m are excluded from scoring. *Communication:* iid loss, per-link Gilbert–Elliott bursts [@gilbert1960capacity; @elliott1963estimates] (mean length 5), *rx-burst* (one burst chain per receiver, so all links into a UAV fail together), *targeted blackout* (70% extra loss on a UAV's links while its report is anomalous) and link blockage; loss levels 0, 10, 30, 50%. Truth, labels and the failure mask are stored apart from the `Observation` type that models receive; unit tests check that the feature builder accepts only that type, that overwriting hidden positions, offsets, labels and the failure mask changes no feature, and that no feature uses future data.

**Models.** Baseline 1: physics test, *naive* and *AoI-aware* (Section 5). Baseline 2: GCN [@kipf2017semi] and GCN-drop (lost links removed). Baseline 3: GAT [@velickovic2018graph]. Baseline 4: NSD-style sheaf [@bodnar2022neural] (our dense re-implementation with general $d\times d$ maps and random-walk instead of symmetric normalisation; not the original code). Proposed: RA-SCM. All learned models share the GRU/head, delayed-message semantics, inputs, training budget (≤30 epochs, early stopping) and parameter counts within 10% of RA-SCM (tested); GCN/GAT/NSD receive edge information as neighbourhood statistics, and MPNN-E removes this asymmetry. GCN/GAT layers were cross-checked against PyTorch Geometric. The detector of @bi2024detection and classical cooperative localisation were **not** implemented.

**Protocol** (Table 2). Per seed (0–4): 200 training and 60 validation episodes from a mixture of seen conditions and 40 test episodes per condition (26 conditions), from disjoint seed ranges. Conditions of one *family* (e.g. all 12 loss and blockage conditions, including $C^*$ of Section 8) share trajectories, noise and anomaly schedules, so cross-condition comparisons are paired and the conditions of $C^*$ are not independent. Learning rates were chosen on a separate tuning seed (grid 0.001–0.03). Every model's threshold gives a 5% false-positive rate (FPR) on pooled validation data and is frozen for all tests. Metrics: **PR-AUC** (average precision, scikit-learn; chance = positive rate) as primary; precision, recall, F1, FPR, ROC-AUC, detection rate and delay (first of two consecutive alarms), parameters, CPU latency; mean ± 95% $t$-interval over seeds and paired differences.

**Sample size.** The unit of replication is the training seed (UAV-steps within an episode are correlated). Five seeds were fixed in the project plan as the minimum for one laptop; no a-priori power analysis was done. Post hoc, the seed-to-seed SD of the paired $\Delta_c$ (Section 8) was 0.003–0.013, so a true $\Delta_c$ of about 0.005–0.022 would give an interval above 0 with 80% probability; since the rule also requires a mean ≥0.02, a true effect of exactly 0.02 would be declared only about half the time (a conservative rule). Each 10-UAV condition yields up to 40,000 scored UAV-steps per seed.

| Exp. | Question | Conditions (independent variable) |
|---|---|---|
| E1 | detection without loss | iid 0% |
| E2 | graceful degradation | iid 10/30/50%; noise ×1/2/3 |
| E3 | bursty / correlated loss | Gilbert–Elliott 10/30/50%; rx-burst 30% |
| E4 | anomaly + communication failure | targeted blackout; link blockage; anomaly type (sudden, drift, spoof) at 0/30% |
| E5 | generalisation | 5 and 20 UAVs; unseen trajectory; unseen formation (loss 30%) |
| E6 | ablations | − reliability info, − weights, − sheaf maps, − temporal, − maps − weights (MPNN-E) |
| E7 | complexity | parameters, amortised CPU latency for N = 5/10/20 |

*Table 2. Experiments. Controlled: swarm size 10, anomaly mixture, noise, training budget.*

## 7. Feasibility and limitations

**Resources.** One laptop CPU (Apple M1, 16 GB, no GPU): training the ten learned variants took 56 min per seed (one thread per process; five seeds in parallel, roughly an hour in total). Software is open source (Python, PyTorch, Streamlit); expertise: graph learning and estimation theory; time: three months (Section 10). With **€500** the minimum meaningful extension is *calibration, not flight*: about 6 ESP32 boards (≈€60) to log packet-loss traces and fit the Gilbert–Elliott parameters, and 4 UWB boards and 2 GNSS modules (≈€250) to measure ranging and GNSS noise on a walked test (rough retail estimates, October 2026).

**Ethics, safety, regulation.** The work is defensive; the attack models are generic perturbations, not tooling. Real swarm logs would need anonymisation; none are used. An unvalidated detector could cause needless aborts or miss attacks; these results are not certification evidence. Transmitting spoofing or jamming signals without authorisation is prohibited under radio-spectrum law, and flight tests fall under drone rules (EU Implementing Regulation 2019/947; in Turkey, the civil aviation authority SHGM), so this study is simulation-only.

**Limitations.** (i) Simulation-to-reality gap: Gaussian noise, a light kinematic model, a hand-designed channel family and a simulator written for this study (by the author with an AI coding assistant), the same source as the proposed model (benchmark bias). (ii) Physics baselines use nominal sensor specifications. (iii) Five seeds give wide intervals. (iv) Training used 10-UAV swarms; GCN/GCN-drop learning rates lie on the grid edge. (v) NSD is a re-implementation. (vi) Latency is amortised CPU throughput. **Beyond our capability:** flight experiments, adaptive attackers, formal guarantees.

## 8. Validation and falsifiable hypothesis

Let $\Delta_c=\text{PR-AUC}_c(\text{RA-SCM})-\max_{m\in\{\text{GCN, GAT, GCN-drop, NSD}\}}\text{PR-AUC}_c(m)$, paired by seed (maximum taken per seed), on $C^*=\{$iid 30%, iid 50%, burst 30%, burst 50%, rx-burst 30%, targeted 30%$\}$.

* **H0:** $E[\Delta_c]\le 0$ (no benefit over capacity-matched conventional GNNs). **H1:** $E[\Delta_c]\ge 0.02$ (smallest effect of interest); $0<E[\Delta_c]<0.02$ does not support H1.
* **Decision rule:** H1 is accepted at $c$ if the 95% $t$-interval of $\Delta_c$ lies above 0 and its mean is ≥0.02 (a pragmatic rule, not a formal minimum-effect test; no multiplicity correction). The contribution is *supported* only if H1 holds in ≥4 of 6 conditions **and** RA-SCM's FPR at 50% iid loss exceeds the best conventional GNN's (implemented as the lowest of the four) by at most 0.02.
* **What disproves the idea:** the interval of $\Delta_c$ contains 0 or is negative in ≥3 conditions; or the AoI-aware physics test is at least as good as RA-SCM on $C^*$; or ablations show that the gain comes from edge conditioning, not from maps or reliability weights (MPNN-E ≈ RA-SCM).
* **Timing.** The per-condition criterion was committed with the analysis code before the results. $C^*$, the ≥4-of-6 aggregation, the FPR clause and the falsification clauses were fixed before RA-SCM results were inspected but committed together with the results, so their timing cannot be verified from the repository.
* **Bias, overfitting, alternatives, reproducibility:** frozen operating point, disjoint seed ranges, paired seeds, capacity matching, tuning on a separate seed, identical inputs, ablations for parameter and information confounds, fixed seeds and configs. **Negative results** would still show where reliability-aware sheaf modelling does not pay.


## 9. Results obtained and expected impact

All result numbers are produced by the repository pipeline (5 seeds, 26 conditions × 40 test episodes) and inserted automatically from `results/tables/`. The positive rate (= chance PR-AUC) is 0.094 in the conditions of Tables 3–5 and 0.045–0.176 elsewhere (20 vs 5 UAVs). Hardware: Apple M1, 8 logical cores, 16 GB RAM. **These are synthetic-simulation results; they do not demonstrate real-world UAV performance.**

| PR-AUC | iid 0% | iid 30% | iid 50% | burst 30% | burst 50% | rx-burst 30% | targeted 30% |
|:--|--:|--:|--:|--:|--:|--:|--:|
| Physics (naive) | 0.894 ±.025 | 0.863 ±.029 | 0.804 ±.033 | 0.605 ±.056 | 0.519 ±.057 | 0.389 ±.047 | 0.779 ±.035 |
| Physics (AoI-aware) | 0.894 ±.025 | 0.891 ±.024 | 0.888 ±.023 | 0.885 ±.023 | 0.877 ±.022 | 0.885 ±.029 | 0.890 ±.021 |
| GCN | 0.960 ±.019 | 0.958 ±.018 | 0.951 ±.016 | 0.919 ±.024 | 0.889 ±.023 | 0.929 ±.029 | 0.961 ±.016 |
| GCN-drop | 0.965 ±.014 | 0.959 ±.016 | 0.949 ±.019 | 0.953 ±.015 | 0.939 ±.023 | 0.907 ±.020 | 0.986 ±.005 |
| GAT | 0.968 ±.016 | 0.963 ±.020 | 0.956 ±.021 | 0.929 ±.027 | 0.909 ±.021 | 0.943 ±.018 | 0.968 ±.018 |
| NSD-style sheaf | 0.968 ±.019 | 0.967 ±.016 | 0.959 ±.016 | 0.937 ±.012 | 0.907 ±.014 | 0.948 ±.016 | 0.968 ±.016 |
| **RA-SCM** | 0.974 ±.019 | 0.975 ±.018 | 0.975 ±.019 | 0.972 ±.020 | 0.967 ±.026 | 0.958 ±.022 | 0.988 ±.007 |

*Table 3. PR-AUC, mean ± 95% $t$-interval half-width over 5 seeds (E1–E4). Chance level = 0.094.*

**Missing versus wrong information is a real confusion in the simulator, and mostly a bookkeeping problem (E2–E4).** A test that treats stale reports as current keeps 0.894 without loss but falls to 0.519 under 50% bursts (Figure A2) and 0.389 under rx-burst loss; modelling the age of the report (AoI-aware physics) removes most of the damage (0.877, 0.885). Under iid loss the naive test degrades less (0.804 at 50%), plausibly because stale errors of a rigidly moving formation are common-mode and cancel (untested).

**Learned graph models beat both physics tests; RA-SCM has the highest mean in every column of Table 3, by small margins.** With identical inputs the conventional GNNs reach 0.960–0.968 without loss (physics 0.894; RA-SCM 0.974). From 0% to 50% bursts RA-SCM changes by −0.007, against −0.059 (GAT), −0.072 (GCN) and −0.026 (GCN-drop). Table 4 gives the pre-specified test (plotted in Figure A3; precision–recall curves in Figure A7).

| condition | Δ vs best conventional GNN [95% CI] | H1 met? | Δ vs AoI-aware physics [95% CI] |
|:--|:--|:--:|:--|
| iid 30% | +0.005 [−0.006, +0.016] | no | +0.084 [+0.054, +0.113] |
| iid 50% | +0.013 [−0.004, +0.029] | no | +0.087 [+0.055, +0.119] |
| burst 30% | +0.019 [+0.011, +0.026] | no | +0.087 [+0.056, +0.119] |
| burst 50% | +0.028 [+0.013, +0.043] | yes | +0.090 [+0.059, +0.121] |
| rx-burst 30% | +0.007 [−0.008, +0.022] | no | +0.073 [+0.045, +0.101] |
| targeted 30% | +0.002 [−0.002, +0.006] | no | +0.098 [+0.075, +0.121] |

*Table 4. Paired PR-AUC difference RA-SCM − reference (mean [95% CI over seeds]); H1 requires CI > 0 and mean ≥ 0.02.*

**Decision.** H1 is met in 1 of 6 conditions (≥4 required) and the interval contains 0 in 4 (≥3 falsifies): by the rule fixed beforehand, **H1 is not supported and its falsification clause is met**. The other two clauses are not met: RA-SCM beats the AoI-aware test in 6 of 6 conditions (+0.090 [+0.059, +0.121] at 50% bursts), and in the two burst conditions, the only ones where its interval lies above 0, MPNN-E is worse (+0.021 [+0.004, +0.037], +0.035 [+0.018, +0.052]; intervals include 0 elsewhere on $C^*$). The reference is harsh (a per-seed maximum over four models is biased upward): against single baselines (post hoc, uncorrected) RA-SCM's interval lies above 0 in 19 of 24 condition–baseline pairs on $C^*$ and the full H1 criterion holds in 13 (against GCN in 5 of 6, e.g. +0.078 [+0.049, +0.107] at 50% bursts). *Post hoc:* RA-SCM's advantage over the best conventional GNN is practically relevant only under 50% bursts (+0.028 [+0.013, +0.043]) and absent without loss (+0.002 [−0.011, +0.014]), pointing to loss handling rather than capacity. The FPR clause is met (0.031 vs 0.029 for GCN, the lowest).

**Other experiments.**

* *Noise (E2):* at ×3 noise all models lose accuracy (RA-SCM 0.896, NSD 0.894, GAT 0.883) and the frozen thresholds fail (FPR 0.133 for RA-SCM, 0.316 for GCN-drop; Table B1).
* *Anomaly type (E4):* sudden jumps are nearly always detected; drift and spoofing are harder (spoof at 30% loss: RA-SCM 0.965, conventional GNNs 0.936–0.948) and detected later (Figure A8).
* *Targeted blackout (E4):* it hurts no learned model and helps those using per-link delivery state (from iid 30% on the same episodes: RA-SCM 0.975 → 0.988, GCN-drop 0.959 → 0.986), while the naive test falls (0.863 → 0.779). The extra loss coincides exactly with the anomaly and a third of training episodes contain it, so missing packets can themselves become anomaly evidence (fewer neighbours receiving the corrupted reports is another, untested explanation); the condition overstates detectability against an attacker who does not degrade its own links.
* *Generalisation (E5, Figure A6):* trained on 10 UAVs, learned models transfer to 20 UAVs (RA-SCM 0.981), an unseen trajectory (0.976) and formation (0.975), but **not to 5 UAVs** (RA-SCM 0.830, GAT 0.839, GCN 0.841), where few neighbours give little evidence.
* *Frozen-threshold metrics* (Table B1) differ partly because realised FPRs differ; the AoI-aware physics test is poorly calibrated by the validation rule (FPR 0.124 at 0% loss, target 0.05). *Cost* (Table B2, Figure A9): RA-SCM needs 0.18 ms per step at N = 10 versus 0.05 ms for GAT, and 10 min of training per seed.

| removed component | iid 0% | iid 50% | burst 50% | rx-burst 30% | targeted 30% |
|:--|--:|--:|--:|--:|--:|
| − reliability info | +0.008 [−0.003, +0.019] | +0.026 [+0.009, +0.042] | +0.088 [+0.051, +0.125] | +0.044 [+0.021, +0.068] | +0.017 [+0.011, +0.024] |
| − reliability weights | −0.003 [−0.017, +0.012] | 0.000 [−0.014, +0.013] | +0.021 [+0.004, +0.038] | +0.006 [−0.009, +0.022] | +0.005 [−0.002, +0.011] |
| − sheaf maps (F = I) | +0.007 [−0.008, +0.022] | +0.004 [−0.009, +0.017] | +0.007 [−0.010, +0.023] | +0.010 [−0.005, +0.024] | 0.000 [−0.004, +0.003] |
| − temporal (GRU) | +0.005 [−0.002, +0.012] | +0.013 [−0.000, +0.027] | +0.018 [+0.002, +0.035] | +0.020 [+0.011, +0.029] | +0.009 [+0.002, +0.016] |
| − maps − weights (MPNN-E) | +0.007 [−0.008, +0.023] | +0.009 [−0.004, +0.021] | +0.035 [+0.018, +0.052] | +0.007 [−0.012, +0.027] | +0.015 [−0.000, +0.031] |

*Table 5. Ablations (E6, also Figure A4): paired PR-AUC difference full RA-SCM − ablated variant (mean [95% CI]); positive = the removed component helped.*

**Reading the ablations (exploratory beyond the MPNN-E clause).** The reliability *channel* (delivery state, age, link quality, age-compensated residual) matters most: removing it costs +0.088 [+0.051, +0.125] under 50% bursts, leaving RA-SCM below all four conventional GNNs there (0.879 vs 0.889–0.939), and +0.044 [+0.021, +0.068] under rx-burst loss. Learned *weights* matter only under 50% bursts (+0.021 [+0.004, +0.038], just above 0.02; ≈0 in the other Table 5 conditions). **Learned sheaf maps showed no measurable benefit:** identity maps change PR-AUC by at most 0.010, with the interval including 0 in 5 of 5 conditions; with 5 UAVs the identity variant has a higher mean (−0.033 [−0.074, +0.008], interval includes 0) and MPNN-E is better than RA-SCM (−0.030 [−0.055, −0.005]). The GRU helps under bursts and at ×3 noise (0.758 without vs 0.896). MPNN-E is worse than RA-SCM under 50% bursts (+0.035 [+0.018, +0.052]), more than either single removal, so the experiment cannot separate maps from weights. The benefit under loss is best attributed to *how reliability metadata enters the model* (edge features and, under bursts, learned weights, with temporal memory), not to sheaf structure.

**Threats to validity** (besides Section 7). (i) Realised FPRs differ across models. (ii) RA-SCM consumes edge features directly, the baselines in aggregated form; MPNN-E partly addresses this, but a GAT with edge features was not run. (iii) Learning rates were tuned on one seed. (iv) Targeted blackout rewards models that read delivery state; it is not a test against an adaptive attacker.

**Expected scientific impact.** The outcome is a *controlled benchmark and a negative-leaning answer*: reliability-aware sheaf modelling is at best a small improvement over strong graph baselines, and the cheapest effective step is to model the age of the evidence. Researchers gain loss models and an age-aware control for evaluating swarm detectors; designers gain evidence on thresholds under degraded links. For society, a detector that does not mistake outages for attacks would reduce needless aborts of inspection and search-and-rescue swarms and make multi-UAV safety cases more credible. *Possible harms:* an adversary could pair spoofing with more selective link degradation than tested here, and a benchmark can encourage over-trust in simulated accuracy. *New questions:* threshold calibration under noise shift; detection with few neighbours; whether margins survive measured noise and loss traces; adaptive attackers; whether computed physical maps [@barbero2022connection] can replace learned ones.


## 10. Researcher's reflection

**1. The Skeptic — "this research is unnecessary."** In our controlled simulation a consistency test that treats stale reports as current falls from 0.894 to 0.519 PR-AUC under bursty loss (0.389 under rx-burst loss), and no detector we reviewed was tested with loss as a controlled confounder. The expert is partly right: an age-aware test restores most of the loss (0.877) and a plain GAT with the same inputs reaches 0.909; the sheaf machinery is not what fixes the problem. What is necessary is the controlled evaluation, not the architecture.

**2. The Failure — "after a year the hypothesis is wrong."** By our own rule it already is, in its strong form. What remains: a reproducible benchmark with paired seeds and an age-aware control; the finding that the reliability channel carries the benefit (+0.088 [+0.051, +0.125] when removed) while learned maps show none; the limit for small swarms (5 UAVs: 0.830); the failure of frozen thresholds under noise shift; tested code and a dashboard.

**3. The Originality — "remove everything borrowed."** Sheaf Laplacians, NSD-style layers, GCN/GAT, uncertainty weighting, Gilbert–Elliott loss, AoI and consistency tests are borrowed. What is ours: (a) framing the task as *confounded evidence* (missing versus wrong) with explicit observability conditions; (b) applying delayed-message semantics [@tolstaya2020learning] uniformly to every architecture and extending them to lost packets, so comparisons cannot leak; (c) the protocol — loss as a controlled confounder, frozen operating point, paired seeds, age-aware physics control, component ablations; (d) the findings, including the negative ones. We do not claim a new algorithm.

**4. The Reality — €500, one computer, three months.** The minimum meaningful experiment is E3 (burst loss) with both physics tests, the four conventional GNNs and RA-SCM over five seeds; on the existing simulator it needs about 20 minutes of training per seed on one laptop (Table B2) at no hardware cost. From scratch: month 1 for literature, simulator and leakage tests; month 2 for logging loss traces (six ESP32 boards, ≈€60) and UWB/GNSS noise (≈€250) while building baselines; month 3 for fitting the channel and noise models, re-running E3 and writing. If RA-SCM's margin over the best conventional GNN stays below 0.02 on fitted parameters, the negative conclusion stands.

**5. The Intellectual Honesty — "strongest argument against."** A plain GAT with the same inputs comes within 0.01–0.06 PR-AUC of RA-SCM on $C^*$; a 20-line age-aware test removes most of the damage of stale reports (though it stays 0.07–0.10 below RA-SCM); learned maps add nothing measurable; and simulator, baselines and model share one source. We would change our minds if, on measured loss and noise, RA-SCM beat the best conventional GNN by ≥0.02 with an interval above 0 in at least four conditions *and* the identity-map ablation fell behind by ≥0.01 — or, conversely, if the age-aware test matched the learned models on real traces.

**Declaration of AI assistance (HW1 academic-integrity rules).** The project was carried out with Claude Sonnet 5.5 (Anthropic) in Claude Code (27–30 October 2026), which proposed and ran the searches, summarised the papers, wrote the simulator, model, test and analysis code, ran the experiments, produced the figures and drafted the text, including first drafts of the reflection. A pre-submission check with Claude Opus 5.5 (6 November 2026) re-verified every reference against its DOI or arXiv record (and the full text where details are discussed), extended the search, recomputed the result numbers and led to the corrections in this version. "We" refers to the author working with this assistant. All result numbers (Tables 3–5, B1–B2 and every PR-AUC, FPR, difference and count in Sections 9–10) are inserted automatically from result files; design parameters are copied from `configs/default.yaml`. The author chose the problem, directed the work, reviewed the final text and remains responsible for verifying every claim and citation.

## 11. References

::: {#refs}
:::

<div class="pagebreak"></div>

## Appendix A. Figures (optional visuals, not counted in the page limit)

![**Figure A1.** Architecture and information flow. Simulator ground truth never crosses the observation barrier; RA-SCM consumes node and edge features and reads neighbour states from the time of the last delivered packet.](figures/fig_architecture.png){width=100%}

![**Figure A2.** PR-AUC versus packet loss (mean ± 95% interval over 5 seeds); top: full range, bottom: zoom on the learned models.](figures/fig_pr_auc_vs_loss.png){width=86%}

![**Figure A3.** Paired PR-AUC difference RA-SCM − reference with 95% intervals. Blue: interval above 0 and mean ≥ 0.02 (in the left panel the pre-specified H1 criterion; shaded band 0–0.02); grey: inconclusive. The rows iid 0% and 20 UAVs are shown for context and are not part of $C^*$.](figures/fig_hypothesis_forest.png){width=88%}

![**Figure A4.** Ablations: paired PR-AUC difference full RA-SCM − ablated variant (same conditions as Table 5).](figures/fig_ablation.png){width=70%}

![**Figure A5.** False-positive rate at the threshold frozen on validation data (dotted line: 5% target).](figures/fig_fpr_vs_loss.png){width=75%}

![**Figure A6.** PR-AUC under changed swarm size, unseen trajectory and unseen formation (loss 30%).](figures/fig_generalization.png){width=80%}

![**Figure A7.** Precision–recall curves (seed 0) for four conditions.](figures/fig_pr_curves.png){width=100%}

![**Figure A8.** Median detection delay by anomaly type. Filled circles: no loss; hollow triangles: 30% iid loss; delay over detected UAVs only.](figures/fig_delay.png){width=85%}

![**Figure A9.** Amortised CPU inference time (log scale; the two physics tests have identical cost) and parameter counts.](figures/fig_latency.png){width=80%}

## Appendix B. Supplementary tables (optional, not counted in the page limit)

| model | FPR iid 0% | FPR iid 50% | FPR burst 50% | FPR noise ×3 | recall iid 50% | recall burst 50% | delay burst 50% [s] | detect rate burst 50% |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| Physics (naive) | 0.038 | 0.068 | 0.196 | 0.000 | 0.847 | 0.848 | 2.10 | 1.00 |
| Physics (AoI-aware) | 0.124 | 0.115 | 0.101 | 0.012 | 0.940 | 0.927 | 1.40 | 1.00 |
| GCN | 0.015 | 0.029 | 0.075 | 0.117 | 0.932 | 0.907 | 1.50 | 1.00 |
| GCN-drop | 0.021 | 0.039 | 0.054 | 0.316 | 0.944 | 0.940 | 1.10 | 1.00 |
| GAT | 0.020 | 0.029 | 0.074 | 0.064 | 0.942 | 0.917 | 1.35 | 1.00 |
| NSD-style sheaf | 0.019 | 0.031 | 0.070 | 0.081 | 0.942 | 0.910 | 1.60 | 1.00 |
| **RA-SCM** | 0.032 | 0.031 | 0.041 | 0.133 | 0.969 | 0.964 | 0.50 | 1.00 |

*Table B1. Frozen-threshold secondary metrics (means over seeds; delay over detected UAVs only).*

| model | parameters | ms per swarm step, N=5 / 10 / 20 | train time per seed [min] |
|:--|--:|:--|--:|
| Physics (naive) | 0 | 0.02 / 0.02 / 0.02 | 0.0 |
| Physics (AoI-aware) | 0 | 0.02 / 0.02 / 0.02 | 0.0 |
| GCN | 17425 | 0.02 / 0.03 / 0.08 | 1.1 |
| GCN-drop | 17425 | 0.02 / 0.03 / 0.08 | 0.9 |
| GAT | 17585 | 0.02 / 0.05 / 0.14 | 1.6 |
| NSD-style sheaf | 17729 | 0.05 / 0.18 / 0.71 | 5.8 |
| **RA-SCM** | 17571 | 0.05 / 0.18 / 0.76 | 9.7 |
| − reliability info | 17377 | 0.05 / 0.17 / 0.72 | 9.6 |
| − reliability weights | 17377 | 0.05 / 0.17 / 0.71 | 7.8 |
| − sheaf maps (F = I) | 16515 | 0.04 / 0.13 / 0.52 | 5.9 |
| − temporal (GRU) | 11043 | 0.04 / 0.17 / 0.75 | 9.0 |
| − maps − weights (MPNN-E) | 16321 | 0.04 / 0.12 / 0.47 | 4.8 |

*Table B2. Parameters, amortised CPU inference time and training time. RA-SCM costs far more compute than GCN/GAT for a modest accuracy gain.*
